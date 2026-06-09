# API 接口认证说明

## 认证方式：API Key + HMAC-SHA256 签名

本服务使用 API Key + HMAC-SHA256 签名的方式进行接口认证，确保请求的合法性、完整性和防重放。

## 申请 API Key

调用 `POST /api/v1/auth/apply` 接口申请 API Key：

```json
{
  "app_name": "我的应用",
  "description": "应用描述（可选）",
  "expires_at": "2027-01-01T00:00:00Z（可选）"
}
```

成功返回：

```json
{
  "code": 0,
  "message": "API Key created successfully. Please save the client_secret as it will not be shown again.",
  "data": {
    "app_id": "ak_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "app_name": "我的应用",
    "client_secret": "sk_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
    "expires_at": null
  }
}
```

> **注意**：`client_secret` 仅在创建时返回一次，请妥善保存。

## 签名算法

### 请求头参数

所有需要认证的请求必须携带以下四个 Header：

| Header | 说明 | 示例 |
|--------|------|------|
| `X-App-ID` | 申请的 API Key ID | `ak_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `X-Timestamp` | 当前 UTC 时间戳（秒） | `1736400000` |
| `X-Nonce` | 随机字符串，每次请求唯一 | `nonce_abc123def456` |
| `X-Signature` | HMAC-SHA256 签名 | `abcdef1234567890...` |

### 签名步骤

1. **构造签名字符串**：
   ```
   HTTP方法
   请求路径
   时间戳
   Nonce
   请求体（仅 POST/PUT/PATCH 有）
   ```

   示例（GET 请求）：
   ```
   GET
   /api/v1/health
   1736400000
   nonce_abc123def456
   ```

   示例（POST 请求）：
   ```
   POST
   /api/v1/auth/keys
   1736400001
   nonce_def789ghi012
   {"key":"value"}
   ```

2. **计算签名**：
   ```python
   import hashlib
   import hmac
   
   signature = hmac.new(
       client_secret.encode('utf-8'),
       message.encode('utf-8'),
       hashlib.sha256
   ).hexdigest()
   ```

3. **发送请求**：将 `X-App-ID`、`X-Timestamp`、`X-Nonce`、`X-Signature` 放入请求头。

## 服务端验证流程

1. 根据 `X-App-ID` 查找 API Key 记录
2. 检查 API Key 状态是否为 `active`
3. 检查 API Key 是否过期
4. 验证 `X-Timestamp` 是否在 ±5 分钟时间窗口内
5. 验证 `X-Nonce` 是否已被使用（防重放攻击）
6. 使用存储的 `client_secret` 重新计算签名并比对

## 示例代码

### Python

```python
import hashlib
import hmac
import time
import uuid
import requests

app_id = "ak_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
client_secret = "sk_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"

method = "GET"
path = "/api/v1/health"
timestamp = str(int(time.time()))
nonce = uuid.uuid4().hex

message = "\n".join([method, path, timestamp, nonce])
signature = hmac.new(
    client_secret.encode("utf-8"),
    message.encode("utf-8"),
    hashlib.sha256,
).hexdigest()

response = requests.get(
    f"http://localhost:8000{path}",
    headers={
        "X-App-ID": app_id,
        "X-Timestamp": timestamp,
        "X-Nonce": nonce,
        "X-Signature": signature,
    },
)
print(response.json())
```
