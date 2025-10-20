from .slide_registry import SlideTypeRegistry
from .slide_types import *

__all__ = ["SlideTypeRegistry", *SlideTypeRegistry.get_type_names()]
