import hashlib
import hmac
import time
from typing import Optional

from app.core.exceptions.handlers import InvalidSignatureError, AuthenticationError, ApiKeyExpiredError
from app.models.api_key import ApiKey

# 内存 nonce 缓存，用于防重放攻击（key: nonce, value: timestamp）
# TODO: 生产环境替换为 Redis
_nonce_cache: dict[str, int] = {}
_NONCE_TTL = 300  # 5 分钟
_TIMESTAMP_WINDOW = 300  # 时间窗口 ±5 分钟


def verify_signature(
    api_key: ApiKey,
    signature: str,
    timestamp: str,
    nonce: str,
    method: str,
    path: str,
    body: Optional[str] = None,
) -> None:
    """验证 HMAC-SHA256 签名"""
    # 1. 检查状态
    if api_key.status != "active":
        raise AuthenticationError("API Key 未启用或已禁用")

    # 2. 检查是否过期
    if api_key.expires_at and time.time() > api_key.expires_at.timestamp():
        raise ApiKeyExpiredError()

    # 3. 验证时间戳
    try:
        ts = int(timestamp)
    except (ValueError, TypeError):
        raise InvalidSignatureError("无效的时间戳")

    now = time.time()
    if abs(now - ts) > _TIMESTAMP_WINDOW:
        raise InvalidSignatureError("时间戳超出允许的时间窗口")

    # 4. 验证 nonce（防重放攻击）
    if nonce in _nonce_cache:
        raise InvalidSignatureError("Nonce 已被使用过")

    # 清理过期的 nonce
    _clean_expired_nonces()

    # 5. 重新计算签名并比对
    message = _build_signature_string(method, path, timestamp, nonce, body)
    expected_signature = hmac.new(
        api_key.client_secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        raise InvalidSignatureError("签名不匹配")

    # 6. 缓存 nonce
    _nonce_cache[nonce] = int(now)


def _build_signature_string(method: str, path: str, timestamp: str, nonce: str, body: Optional[str] = None) -> str:
    """构建待签名字符串"""
    parts = [method.upper(), path, timestamp, nonce]
    if body:
        parts.append(body)
    return "\n".join(parts)


def _clean_expired_nonces() -> None:
    """清理已过期的 nonce"""
    now = time.time()
    expired = [k for k, v in _nonce_cache.items() if now - v > _NONCE_TTL]
    for k in expired:
        _nonce_cache.pop(k, None)
