"""
完整的日志系统
提供彩色输出、文件记录、性能监控等功能
"""
import logging
import os
import sys
import time
import traceback
from datetime import datetime
from functools import wraps
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Callable, Optional


# ANSI 颜色代码
class Colors:
    """终端颜色代码"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # 前景色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # 亮色
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # 背景色
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'


class ColoredFormatter(logging.Formatter):
    """彩色日志格式化器"""
    
    # 日志级别对应的颜色
    COLORS = {
        'DEBUG': Colors.BRIGHT_BLACK,
        'INFO': Colors.BRIGHT_CYAN,
        'WARNING': Colors.BRIGHT_YELLOW,
        'ERROR': Colors.BRIGHT_RED,
        'CRITICAL': Colors.BG_RED + Colors.BRIGHT_WHITE,
    }
    
    # 日志级别对应的图标
    ICONS = {
        'DEBUG': '🔍',
        'INFO': '📝',
        'WARNING': '⚠️ ',
        'ERROR': '❌',
        'CRITICAL': '🔥',
    }
    
    def format(self, record):
        """格式化日志记录"""
        # 保存原始级别名
        levelname = record.levelname
        
        # 添加颜色
        if levelname in self.COLORS:
            colored_levelname = (
                f"{self.COLORS[levelname]}"
                f"{self.ICONS.get(levelname, '')} {levelname}"
                f"{Colors.RESET}"
            )
            record.levelname = colored_levelname
        
        # 给函数名添加颜色
        if hasattr(record, 'funcName'):
            record.funcName = f"{Colors.BRIGHT_MAGENTA}{record.funcName}{Colors.RESET}"
        
        # 格式化消息
        formatted = super().format(record)
        
        # 恢复原始级别名（避免影响其他 handler）
        record.levelname = levelname
        
        return formatted


class PerformanceLogger:
    """性能监控日志器"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self._timers = {}
    
    def start_timer(self, name: str):
        """开始计时"""
        self._timers[name] = time.time()
        self.logger.debug(f"⏱️  计时器启动: {name}")
    
    def end_timer(self, name: str, log_level: str = 'INFO'):
        """结束计时并记录"""
        if name not in self._timers:
            self.logger.warning(f"计时器 '{name}' 未启动")
            return
        
        elapsed = time.time() - self._timers[name]
        del self._timers[name]
        
        # 格式化时间
        if elapsed < 1:
            time_str = f"{elapsed*1000:.2f}ms"
        elif elapsed < 60:
            time_str = f"{elapsed:.2f}s"
        else:
            minutes = int(elapsed // 60)
            seconds = elapsed % 60
            time_str = f"{minutes}m {seconds:.2f}s"
        
        log_func = getattr(self.logger, log_level.lower())
        log_func(f"⏱️  {name}: {time_str}")
        
        return elapsed
    
    def log_memory(self):
        """记录内存使用情况"""
        try:
            import psutil
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            self.logger.info(f"💾 内存使用: {memory_mb:.2f} MB")
        except ImportError:
            self.logger.debug("psutil 未安装，无法记录内存使用")


class AppLogger:
    """应用日志管理器"""
    
    def __init__(
        self,
        name: str = "AutoPPT",
        log_dir: str = "logs",
        log_file: Optional[str] = None,
        level: int = logging.INFO,
        console_output: bool = True,
        file_output: bool = True,
        max_file_size: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        colored: bool = True
    ):
        """
        初始化日志管理器
        
        Args:
            name: 日志器名称
            log_dir: 日志文件目录
            log_file: 日志文件名（None 则自动生成）
            level: 日志级别
            console_output: 是否输出到控制台
            file_output: 是否输出到文件
            max_file_size: 单个日志文件最大大小
            backup_count: 保留的日志文件数量
            colored: 控制台是否使用彩色输出
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.level = level
        
        # 创建日志目录
        if file_output:
            self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成日志文件名
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = f"{name}_{timestamp}.log"
        
        self.log_file = self.log_dir / log_file
        
        # 创建 logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False
        
        # 清除已有的 handlers
        self.logger.handlers.clear()
        
        # 创建格式化器
        detailed_format = (
            '%(asctime)s | '
            '%(levelname)-8s | '
            '%(name)s.%(funcName)s:%(lineno)d | '
            '%(message)s'
        )
        
        simple_format = (
            '%(asctime)s | '
            '%(levelname)-8s | '
            '%(message)s'
        )
        
        date_format = '%Y-%m-%d %H:%M:%S'
        
        # 控制台 handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            
            if colored and sys.stdout.isatty():
                console_formatter = ColoredFormatter(
                    simple_format,
                    datefmt=date_format
                )
            else:
                console_formatter = logging.Formatter(
                    simple_format,
                    datefmt=date_format
                )
            
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
        
        # 文件 handler（带轮转）
        if file_output:
            file_handler = RotatingFileHandler(
                self.log_file,
                maxBytes=max_file_size,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(level)
            file_formatter = logging.Formatter(
                detailed_format,
                datefmt=date_format
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        
        # 创建性能监控器
        self.performance = PerformanceLogger(self.logger)
        
        # 记录初始化信息
        self.logger.info("=" * 60)
        self.logger.info(f"🚀 {name} 日志系统已启动")
        self.logger.info(f"📁 日志文件: {self.log_file if file_output else '无'}")
        self.logger.info(f"📊 日志级别: {logging.getLevelName(level)}")
        self.logger.info("=" * 60)
    
    def debug(self, message: str, **kwargs):
        """调试日志"""
        self.logger.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """信息日志"""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """警告日志"""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """错误日志"""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """严重错误日志"""
        self.logger.critical(message, **kwargs)
    
    def exception(self, message: str, **kwargs):
        """异常日志（包含堆栈跟踪）"""
        self.logger.exception(message, **kwargs)
    
    def section(self, title: str):
        """记录章节标题"""
        self.logger.info("")
        self.logger.info("=" * 60)
        self.logger.info(f"📌 {title}")
        self.logger.info("=" * 60)
    
    def subsection(self, title: str):
        """记录子章节标题"""
        self.logger.info("")
        self.logger.info(f"▶ {title}")
        self.logger.info("-" * 60)
    
    def success(self, message: str):
        """成功信息"""
        self.logger.info(f"✅ {message}")
    
    def failure(self, message: str):
        """失败信息"""
        self.logger.error(f"❌ {message}")
    
    def progress(self, current: int, total: int, message: str = ""):
        """进度信息"""
        percentage = (current / total * 100) if total > 0 else 0
        bar_length = 30
        filled = int(bar_length * current / total) if total > 0 else 0
        bar = "█" * filled + "░" * (bar_length - filled)
        
        progress_msg = f"[{bar}] {percentage:.1f}% ({current}/{total})"
        if message:
            progress_msg += f" - {message}"
        
        self.logger.info(progress_msg)
    
    def table(self, headers: list, rows: list):
        """记录表格"""
        # 计算列宽
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # 分隔线
        separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
        
        # 表头
        self.logger.info(separator)
        header_row = "|" + "|".join(
            f" {h:<{col_widths[i]}} " for i, h in enumerate(headers)
        ) + "|"
        self.logger.info(header_row)
        self.logger.info(separator)
        
        # 数据行
        for row in rows:
            data_row = "|" + "|".join(
                f" {str(cell):<{col_widths[i]}} " for i, cell in enumerate(row)
            ) + "|"
            self.logger.info(data_row)
        
        self.logger.info(separator)
    
    def log_dict(self, title: str, data: dict, indent: int = 0):
        """记录字典数据"""
        self.logger.info(f"{' ' * indent}{title}:")
        for key, value in data.items():
            if isinstance(value, dict):
                self.log_dict(key, value, indent + 2)
            else:
                self.logger.info(f"{' ' * (indent + 2)}{key}: {value}")
    
    def log_function_call(self, func_name: str, args: tuple = (), kwargs: dict = None):
        """记录函数调用"""
        kwargs = kwargs or {}
        args_str = ", ".join(map(str, args))
        kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        params = ", ".join(filter(None, [args_str, kwargs_str]))
        
        self.logger.debug(f"🔧 调用函数: {func_name}({params})")
    
    def log_return(self, func_name: str, result: Any):
        """记录函数返回值"""
        self.logger.debug(f"↩️  {func_name} 返回: {result}")
    
    def timer(self, name: str):
        """计时器上下文管理器"""
        class TimerContext:
            def __init__(ctx_self, logger_instance):
                ctx_self.logger = logger_instance
                ctx_self.name = name
            
            def __enter__(ctx_self):
                ctx_self.logger.performance.start_timer(name)
                return ctx_self
            
            def __exit__(ctx_self, exc_type, exc_val, exc_tb):
                ctx_self.logger.performance.end_timer(name)
        
        return TimerContext(self)
    
    def catch_exceptions(self, reraise: bool = True):
        """异常捕获装饰器"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self.logger.error(f"函数 {func.__name__} 发生异常: {e}")
                    self.logger.debug(f"异常详情:\n{traceback.format_exc()}")
                    if reraise:
                        raise
                    return None
            return wrapper
        return decorator
    
    def log_performance(self, func: Callable) -> Callable:
        """性能监控装饰器"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            self.log_function_call(func_name, args, kwargs)
            self.performance.start_timer(func_name)
            
            try:
                result = func(*args, **kwargs)
                self.log_return(func_name, result)
                return result
            finally:
                self.performance.end_timer(func_name)
        
        return wrapper
    
    def set_level(self, level: int):
        """设置日志级别"""
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)
        self.logger.info(f"日志级别已更改为: {logging.getLevelName(level)}")
    
    def close(self):
        """关闭日志系统"""
        self.logger.info("=" * 60)
        self.logger.info(f"👋 {self.name} 日志系统已关闭")
        self.logger.info("=" * 60)
        
        for handler in self.logger.handlers:
            handler.close()


# 创建全局日志实例
_global_logger: Optional[AppLogger] = None


def get_logger(
    name: str = "AutoPPT",
    log_dir: str = "logs",
    level: int = logging.INFO,
    **kwargs
) -> AppLogger:
    """
    获取或创建全局日志实例
    
    Args:
        name: 日志器名称
        log_dir: 日志目录
        level: 日志级别
        **kwargs: 其他参数传递给 AppLogger
    
    Returns:
        AppLogger 实例
    """
    global _global_logger
    
    if _global_logger is None:
        _global_logger = AppLogger(
            name=name,
            log_dir=log_dir,
            level=level,
            **kwargs
        )
    
    return _global_logger


# 便捷函数
def debug(message: str):
    """调试日志"""
    get_logger().debug(message)


def info(message: str):
    """信息日志"""
    get_logger().info(message)


def warning(message: str):
    """警告日志"""
    get_logger().warning(message)


def error(message: str):
    """错误日志"""
    get_logger().error(message)


def critical(message: str):
    """严重错误日志"""
    get_logger().critical(message)


def success(message: str):
    """成功信息"""
    get_logger().success(message)


def section(title: str):
    """章节标题"""
    get_logger().section(title)


# 示例使用
if __name__ == "__main__":
    # 创建日志器
    logger = AppLogger(
        name="TestApp",
        log_dir="test_logs",
        level=logging.DEBUG
    )
    
    # 基本日志
    logger.section("基本日志测试")
    logger.debug("这是调试信息")
    logger.info("这是普通信息")
    logger.warning("这是警告信息")
    logger.error("这是错误信息")
    logger.success("这是成功信息")
    
    # 进度条
    logger.subsection("进度条测试")
    for i in range(1, 11):
        logger.progress(i, 10, f"处理项目 {i}")
        time.sleep(0.1)
    
    # 表格
    logger.subsection("表格测试")
    logger.table(
        headers=["名称", "年龄", "城市"],
        rows=[
            ["张三", 25, "北京"],
            ["李四", 30, "上海"],
            ["王五", 28, "广州"],
        ]
    )
    
    # 字典
    logger.subsection("字典测试")
    logger.log_dict("配置信息", {
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "testdb"
        },
        "cache": {
            "enabled": True,
            "ttl": 3600
        }
    })
    
    # 性能监控
    logger.subsection("性能监控测试")
    with logger.timer("数据处理"):
        time.sleep(1)
        logger.info("处理中...")
        time.sleep(0.5)
    
    # 装饰器
    @logger.log_performance
    def slow_function(n: int) -> int:
        """一个慢函数"""
        time.sleep(0.5)
        return n * 2
    
    logger.subsection("装饰器测试")
    result = slow_function(5)
    
    # 关闭日志
    logger.close()

