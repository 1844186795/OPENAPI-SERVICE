"""达人订单 Excel 解析器

继承 BaseExcelParser，实现达人订单专属的字段映射和数据清洗逻辑。
"""
from datetime import datetime
from typing import Optional

from app.core.excel.base_parser import BaseExcelParser


class DarenOrderParser(BaseExcelParser):
    """达人订单 Excel 解析器"""

    # 预期表头（与示例 Excel 文件完全一致）
    @property
    def expected_headers(self) -> list[str]:
        return [
            "订单 ID", "商品 ID", "商品名称", "SKU ID", "商品价格", "支付金额",
            "货币单位", "下单件数", "已全部退货或全额退款", "付款方式", "订单状态",
            "达人用户名", "内容形式", "内容ID", "commission model",
            "标准佣金率", "预估计佣金额", "预计标准佣金付款",
            "实际计佣金额", "实际佣金",
            "店铺广告佣金率", "预计店铺广告佣金付款", "实际店铺广告佣金付款",
            "预估合资达人奖金", "实际合资达人奖金",
            "创建时间", "支付时间", "订单送达时间", "佣金结算时间",
            "平台",
        ]

    # ==================== 字段映射索引 ====================
    # 注意：Excel 列序号从 0 开始
    IDX_ORDER_ID = 0
    IDX_PRODUCT_ID = 1
    IDX_PRODUCT_NAME = 2
    IDX_SKU_ID = 3
    IDX_PRODUCT_PRICE = 4
    IDX_PAYMENT_AMOUNT = 5
    IDX_CURRENCY = 6
    IDX_QUANTITY = 7
    IDX_FULL_REFUND = 8
    IDX_PAYMENT_METHOD = 9
    IDX_ORDER_STATUS = 10
    IDX_INFLUENCER_USERNAME = 11
    IDX_CONTENT_TYPE = 12
    IDX_CONTENT_ID = 13
    IDX_COMMISSION_MODEL = 14
    IDX_STANDARD_COMMISSION_RATE = 15
    IDX_ESTIMATED_COMMISSION_AMOUNT = 16
    IDX_ESTIMATED_STANDARD_COMMISSION = 17
    IDX_ACTUAL_COMMISSION_AMOUNT = 18
    IDX_ACTUAL_COMMISSION = 19
    IDX_STORE_AD_COMMISSION_RATE = 20
    IDX_ESTIMATED_STORE_AD_COMMISSION = 21
    IDX_ACTUAL_STORE_AD_COMMISSION = 22
    IDX_ESTIMATED_JOINT_BONUS = 23
    IDX_ACTUAL_JOINT_BONUS = 24
    IDX_CREATED_TIME = 25
    IDX_PAYMENT_TIME = 26
    IDX_DELIVERY_TIME = 27
    IDX_SETTLEMENT_TIME = 28
    IDX_PLATFORM = 29

    # ==================== 数据解析逻辑 ====================

    def parse_row(self, row_index: int, row_data: list) -> Optional[dict]:
        """解析单行达人订单数据"""
        # 基本校验：关键字段不能为空
        order_id = self._safe_str(row_data, self.IDX_ORDER_ID)
        influencer_username = self._safe_str(row_data, self.IDX_INFLUENCER_USERNAME)
        product_name = self._safe_str(row_data, self.IDX_PRODUCT_NAME)

        errors = []
        if not order_id:
            errors.append("订单ID为空")
        if not influencer_username:
            errors.append("达人用户名为空")
        if not product_name:
            errors.append("商品名称为空")

        if errors:
            return None

        return {
            "order_id": order_id,
            "product_id": self._safe_str(row_data, self.IDX_PRODUCT_ID),
            "product_name": product_name,
            "sku_id": self._safe_str(row_data, self.IDX_SKU_ID),
            "product_price": self._to_decimal(row_data, self.IDX_PRODUCT_PRICE),
            "payment_amount": self._to_decimal(row_data, self.IDX_PAYMENT_AMOUNT),
            "currency": self._safe_str(row_data, self.IDX_CURRENCY),
            "quantity": self._to_int(row_data, self.IDX_QUANTITY),
            "is_full_refund": self._safe_str(row_data, self.IDX_FULL_REFUND),
            "payment_method": self._safe_str(row_data, self.IDX_PAYMENT_METHOD),
            "order_status": self._safe_str(row_data, self.IDX_ORDER_STATUS),
            "influencer_username": influencer_username,
            "content_type": self._safe_str(row_data, self.IDX_CONTENT_TYPE),
            "content_id": self._safe_str(row_data, self.IDX_CONTENT_ID),
            "commission_model": self._safe_str(row_data, self.IDX_COMMISSION_MODEL),
            "standard_commission_rate": self._safe_str(row_data, self.IDX_STANDARD_COMMISSION_RATE),
            "estimated_commission_amount": self._to_decimal(row_data, self.IDX_ESTIMATED_COMMISSION_AMOUNT),
            "estimated_standard_commission": self._to_decimal(row_data, self.IDX_ESTIMATED_STANDARD_COMMISSION),
            "actual_commission_amount": self._to_decimal(row_data, self.IDX_ACTUAL_COMMISSION_AMOUNT),
            "actual_commission": self._to_decimal(row_data, self.IDX_ACTUAL_COMMISSION),
            "store_ad_commission_rate": self._safe_str(row_data, self.IDX_STORE_AD_COMMISSION_RATE),
            "estimated_store_ad_commission": self._to_decimal(row_data, self.IDX_ESTIMATED_STORE_AD_COMMISSION),
            "actual_store_ad_commission": self._to_decimal(row_data, self.IDX_ACTUAL_STORE_AD_COMMISSION),
            "estimated_joint_bonus": self._to_decimal(row_data, self.IDX_ESTIMATED_JOINT_BONUS),
            "actual_joint_bonus": self._to_decimal(row_data, self.IDX_ACTUAL_JOINT_BONUS),
            "created_time": self._parse_datetime(row_data, self.IDX_CREATED_TIME),
            "payment_time": self._parse_datetime(row_data, self.IDX_PAYMENT_TIME),
            "delivery_time": self._parse_datetime(row_data, self.IDX_DELIVERY_TIME),
            "settlement_time": self._parse_datetime(row_data, self.IDX_SETTLEMENT_TIME),
            "platform": self._safe_str(row_data, self.IDX_PLATFORM),
        }

    # ==================== 辅助方法 ====================

    @staticmethod
    def _safe_str(row_data: list, index: int) -> Optional[str]:
        """安全获取字符串值"""
        value = row_data[index] if index < len(row_data) else None
        if value is None:
            return None
        value = str(value).strip()
        return value if value else None

    @staticmethod
    def _to_decimal(row_data: list, index: int) -> Optional[float]:
        """将字符串转换为浮点数"""
        value = row_data[index] if index < len(row_data) else None
        if value is None:
            return None
        try:
            # 移除可能的货币符号、逗号等
            cleaned = str(value).replace(",", "").replace("$", "").replace("€", "").replace("¥", "").strip()
            return round(float(cleaned), 2)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _to_int(row_data: list, index: int) -> Optional[int]:
        """将字符串转换为整数"""
        value = row_data[index] if index < len(row_data) else None
        if value is None:
            return None
        try:
            return int(float(str(value).strip()))
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _parse_datetime(row_data: list, index: int) -> Optional[str]:
        """解析日期时间字符串，返回 ISO 格式字符串"""
        value = row_data[index] if index < len(row_data) else None
        if value is None:
            return None
        try:
            # 格式：dd/MM/yyyy HH:mm:ss
            dt = datetime.strptime(str(value).strip(), "%d/%m/%Y %H:%M:%S")
            return dt.isoformat()
        except (ValueError, TypeError):
            return None
