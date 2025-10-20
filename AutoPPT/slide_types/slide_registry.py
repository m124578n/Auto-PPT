from typing import Dict, List

from AutoPPT.utils.logger import get_logger

logger = get_logger()


# ==================== Registry ====================
class SlideTypeRegistry:
    """Slide 類型註冊表"""

    _registry: Dict[str, type] = {}

    @classmethod
    def register(cls, slide_type: str):
        """裝飾器：註冊 slide 類型"""

        def decorator(slide_class):
            cls._registry[slide_type] = slide_class
            logger.info(f"註冊 slide 類型：{slide_type}")
            return slide_class

        return decorator

    @classmethod
    def get(cls, slide_type: str):
        """獲取 slide 類型類"""
        return cls._registry.get(slide_type)

    @classmethod
    def get_type_names(cls) -> List[str]:
        """獲取所有已註冊的 slide 類型名稱"""
        return [str(slide_class) for slide_class in cls._registry.values()]

    @classmethod
    def all_types(cls):
        """獲取所有已註冊的類型"""
        return list(cls._registry.keys())

    @classmethod
    def get_all_json_examples(cls) -> list:
        """獲取所有已註冊類型的 JSON 示例"""
        examples = []
        for slide_type, slide_class in cls._registry.items():
            examples.append(slide_class.get_json_example())
        return examples

    @classmethod
    def get_all_descriptions(cls) -> Dict[str, str]:
        """獲取所有已註冊類型的說明文字"""
        descriptions = {}
        for slide_type, slide_class in cls._registry.items():
            descriptions[slide_type] = slide_class.get_description()
        return descriptions
