from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from PIL import Image
from pptx.presentation import Presentation
from pptx.slide import Slide

from AutoPPT.utils.logger import get_logger

# 获取日志器
logger = get_logger()


# ==================== 抽象基類 ====================
class SlideType(ABC):
    """Slide 類型抽象基類"""

    def __init__(self, data: Dict[str, Any], context: Optional[Dict] = None):
        """
        Args:
            data: slide 的數據（標題、內容等）
            context: 上下文資訊（圖片路徑、presentation 對象等）
        """
        self.data = data
        self.context = context or {}

    def __str__(self) -> str:
        # 返回 slide 類型的名稱
        return self.__class__.__name__

    @abstractmethod
    def generate_html(self) -> str:
        """生成 HTML 片段"""
        pass

    @abstractmethod
    def generate_pptx(self, prs: Presentation) -> Slide:
        """生成 PPTX slide"""
        pass

    @classmethod
    def get_json_example(cls) -> Dict[str, Any]:
        """
        返回此 slide 類型的 JSON 示例（用於 AI prompt）
        子類應該重寫此方法以提供具體示例
        """
        return {
            "slide_type": "unknown",
            "description": "請在子類中實現 get_json_example()",
        }

    @classmethod
    def get_description(cls) -> str:
        """
        返回此 slide 類型的說明文字（用於 AI prompt）
        子類應該重寫此方法以提供具體說明
        """
        return "未定義說明"

    # ========== 輔助方法 ==========
    def _get_image_path(self, image_id: str) -> Optional[str]:
        """獲取圖片路徑"""
        image_metadata = self.context.get("image_metadata", {})
        if image_id in image_metadata:
            return image_metadata[image_id]["path"]
        return None

    def _calculate_image_size(
        self, image_path: str, max_width: float, max_height: float
    ) -> tuple:
        """計算保持寬高比的圖片尺寸（英寸）"""
        try:
            with Image.open(image_path) as img:
                img_width, img_height = img.size
                aspect_ratio = img_width / img_height

                # 基於寬度
                width_based = max_width
                height_based = max_width / aspect_ratio

                # 基於高度
                height_limit = max_height
                width_limit = max_height * aspect_ratio

                # 選擇不超出邊界的最大尺寸
                if height_based <= max_height:
                    return (width_based, height_based)
                else:
                    return (width_limit, height_limit)
        except Exception as e:
            logger.info(f"   ⚠️ 無法讀取圖片尺寸：{e}")
            return (max_width, max_height)
