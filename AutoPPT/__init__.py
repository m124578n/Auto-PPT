from .auto_ppt import AutoPPT
from .slide_generator import HTMLGenerator, PPTXGenerator
from .slide_types import SlideTypeRegistry
from .utils import get_logger

logger = get_logger()

__all__ = ["AutoPPT", "HTMLGenerator", "PPTXGenerator", "SlideTypeRegistry", "logger"]
