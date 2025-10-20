# 📝 Logger 使用指南

## 🌟 功能特性

### ✨ 核心功能
- ✅ **彩色输出** - 终端美观的彩色日志
- ✅ **文件记录** - 自动保存到日志文件
- ✅ **日志轮转** - 自动管理日志文件大小
- ✅ **性能监控** - 内置计时器和性能分析
- ✅ **装饰器支持** - 方便的函数监控
- ✅ **进度显示** - 进度条和表格输出
- ✅ **异常捕获** - 自动记录异常堆栈
- ✅ **多级别日志** - DEBUG, INFO, WARNING, ERROR, CRITICAL

### 🎨 视觉特性
- 🔍 DEBUG - 灰色
- 📝 INFO - 青色
- ⚠️  WARNING - 黄色
- ❌ ERROR - 红色
- 🔥 CRITICAL - 红底白字

## 🚀 快速开始

### 1. 基本使用

```python
from AutoPPT.utils.logger import AppLogger

# 创建日志器
logger = AppLogger(
    name="MyApp",
    log_dir="logs",
    level=logging.INFO
)

# 记录日志
logger.info("程序启动")
logger.warning("这是一个警告")
logger.error("发生错误")
logger.success("操作成功！")
```

### 2. 使用全局日志器

```python
from AutoPPT.utils.logger import get_logger

# 获取全局日志器
logger = get_logger(name="AutoPPT")

# 使用
logger.info("这是信息日志")
```

### 3. 便捷函数

```python
from AutoPPT.utils import logger

# 直接使用
logger.info("快速记录日志")
logger.success("操作成功")
logger.error("发生错误")
```

## 📖 详细用法

### 基本日志级别

```python
logger = AppLogger(name="App")

logger.debug("调试信息 - 详细的执行流程")
logger.info("普通信息 - 程序运行状态")
logger.warning("警告信息 - 潜在问题")
logger.error("错误信息 - 出现错误但程序继续")
logger.critical("严重错误 - 程序可能崩溃")
logger.exception("异常信息 - 包含完整堆栈跟踪")
```

### 特殊日志方法

```python
# 成功信息（带 ✅ 图标）
logger.success("文件下载成功")

# 失败信息（带 ❌ 图标）
logger.failure("连接数据库失败")

# 章节标题
logger.section("数据处理模块")

# 子章节标题
logger.subsection("步骤 1: 数据加载")
```

### 进度条

```python
total_items = 100

for i in range(1, total_items + 1):
    # 处理数据...
    logger.progress(i, total_items, f"处理项目 {i}")
```

**输出**：
```
[████████████░░░░░░] 45.0% (45/100) - 处理项目 45
```

### 表格输出

```python
logger.table(
    headers=["名称", "状态", "耗时"],
    rows=[
        ["任务1", "完成", "2.3s"],
        ["任务2", "进行中", "1.1s"],
        ["任务3", "等待", "-"],
    ]
)
```

**输出**：
```
+------+--------+------+
| 名称 | 状态   | 耗时 |
+------+--------+------+
| 任务1| 完成   | 2.3s |
| 任务2| 进行中 | 1.1s |
| 任务3| 等待   | -    |
+------+--------+------+
```

### 字典输出

```python
config = {
    "database": {
        "host": "localhost",
        "port": 5432
    },
    "cache": {
        "enabled": True
    }
}

logger.log_dict("配置信息", config)
```

**输出**：
```
配置信息:
  database:
    host: localhost
    port: 5432
  cache:
    enabled: True
```

## ⏱️ 性能监控

### 使用计时器

#### 方式 1: 上下文管理器

```python
with logger.timer("数据处理"):
    # 你的代码
    process_data()
    
# 自动输出: ⏱️ 数据处理: 2.35s
```

#### 方式 2: 手动控制

```python
logger.performance.start_timer("下载文件")

# 你的代码
download_file()

logger.performance.end_timer("下载文件")
# 输出: ⏱️ 下载文件: 1.23s
```

### 内存监控

```python
logger.performance.log_memory()
# 输出: 💾 内存使用: 128.45 MB
```

## 🎯 装饰器

### 性能监控装饰器

```python
@logger.log_performance
def process_data(n: int) -> list:
    """处理数据"""
    # 自动记录：
    # - 函数调用（参数）
    # - 执行时间
    # - 返回值
    
    result = [i * 2 for i in range(n)]
    return result

# 使用
data = process_data(1000)
```

**输出**：
```
🔧 调用函数: process_data(1000)
⏱️ 计时器启动: process_data
↩️ process_data 返回: [0, 2, 4, ..., 1998]
⏱️ process_data: 15.23ms
```

### 异常捕获装饰器

```python
@logger.catch_exceptions(reraise=False)
def risky_function():
    """可能出错的函数"""
    raise ValueError("出错了")
    
# 使用
risky_function()  # 不会崩溃，错误会被记录
```

## 🔧 高级配置

### 完整配置示例

```python
logger = AppLogger(
    name="MyApp",              # 日志器名称
    log_dir="logs",            # 日志目录
    log_file="app.log",        # 日志文件名（可选）
    level=logging.DEBUG,       # 日志级别
    console_output=True,       # 是否输出到控制台
    file_output=True,          # 是否输出到文件
    max_file_size=10*1024*1024,# 单文件最大 10MB
    backup_count=5,            # 保留 5 个备份
    colored=True               # 彩色输出
)
```

### 动态修改日志级别

```python
import logging

# 设置为 DEBUG 级别
logger.set_level(logging.DEBUG)

# 设置为 WARNING 级别
logger.set_level(logging.WARNING)
```

### 禁用彩色输出

```python
logger = AppLogger(
    name="MyApp",
    colored=False  # 禁用彩色
)
```

### 仅输出到控制台

```python
logger = AppLogger(
    name="MyApp",
    console_output=True,
    file_output=False  # 不保存到文件
)
```

### 仅输出到文件

```python
logger = AppLogger(
    name="MyApp",
    console_output=False,  # 不显示在控制台
    file_output=True
)
```

## 📦 在项目中集成

### 方式 1: 在主程序中初始化

```python
# main.py
from AutoPPT.utils.logger import get_logger

# 初始化全局日志器
logger = get_logger(
    name="AutoPPT",
    log_dir="logs",
    level=logging.INFO
)

logger.section("程序启动")

# 其他模块会使用同一个日志器
from my_module import process

process()

logger.section("程序结束")
logger.close()
```

### 方式 2: 在每个模块中使用

```python
# my_module.py
from AutoPPT.utils.logger import get_logger

logger = get_logger()  # 获取全局日志器

def process():
    logger.info("开始处理数据")
    # ...
    logger.success("处理完成")
```

### 方式 3: 集成到类中

```python
from AutoPPT.utils.logger import AppLogger

class DataProcessor:
    def __init__(self):
        self.logger = AppLogger(name="DataProcessor")
    
    def process(self, data):
        self.logger.subsection("数据处理")
        
        with self.logger.timer("处理时间"):
            # 处理逻辑
            self.logger.info(f"处理 {len(data)} 条记录")
            result = self._do_process(data)
        
        self.logger.success("处理完成")
        return result
    
    @property
    def log(self):
        return self.logger
```

## 🎨 实际使用示例

### 示例 1: 爬虫程序

```python
from AutoPPT.utils.logger import AppLogger

logger = AppLogger(name="Scrapy", level=logging.INFO)

def scrape_website(url: str):
    logger.section("网页爬取")
    logger.info(f"目标 URL: {url}")
    
    try:
        with logger.timer("爬取时间"):
            # 爬取逻辑
            logger.info("正在连接...")
            response = requests.get(url)
            
            logger.info("正在解析内容...")
            content = parse_content(response.text)
            
            logger.info(f"提取了 {len(content)} 个元素")
        
        logger.success("爬取成功")
        return content
        
    except Exception as e:
        logger.error(f"爬取失败: {e}")
        logger.exception("详细错误信息")
        return None
```

### 示例 2: 数据处理流程

```python
from AutoPPT.utils.logger import AppLogger

logger = AppLogger(name="DataPipeline")

def run_pipeline(data):
    logger.section("数据处理流程")
    
    # 步骤 1
    logger.subsection("步骤 1: 数据清洗")
    with logger.timer("清洗时间"):
        cleaned = clean_data(data)
    logger.info(f"清洗后: {len(cleaned)} 条记录")
    
    # 步骤 2
    logger.subsection("步骤 2: 数据转换")
    with logger.timer("转换时间"):
        transformed = transform_data(cleaned)
    logger.info(f"转换后: {len(transformed)} 条记录")
    
    # 步骤 3
    logger.subsection("步骤 3: 数据保存")
    with logger.timer("保存时间"):
        save_data(transformed)
    
    # 统计
    logger.subsection("处理统计")
    logger.table(
        headers=["步骤", "输入", "输出", "耗时"],
        rows=[
            ["清洗", len(data), len(cleaned), "0.5s"],
            ["转换", len(cleaned), len(transformed), "1.2s"],
            ["保存", len(transformed), len(transformed), "0.3s"],
        ]
    )
    
    logger.success("流程完成")
```

### 示例 3: AI 生成简报

```python
from AutoPPT.utils.logger import get_logger

logger = get_logger(name="AutoPPT")

def generate_presentation(text_content: str):
    logger.section("AI 简报生成")
    
    # 1. 分析内容
    logger.subsection("阶段 1: 内容分析")
    with logger.timer("AI 分析"):
        structure = analyze_content(text_content)
    logger.info(f"识别到 {structure['slides_count']} 张幻灯片")
    
    # 2. 生成 HTML
    logger.subsection("阶段 2: 生成 HTML")
    with logger.timer("HTML 生成"):
        html = generate_html(structure)
    logger.success(f"HTML 已生成: {len(html)} 字符")
    
    # 3. 生成 PPTX
    logger.subsection("阶段 3: 生成 PPTX")
    total_slides = structure['slides_count']
    
    for i in range(1, total_slides + 1):
        generate_slide(i)
        logger.progress(i, total_slides, f"幻灯片 {i}")
    
    logger.success("PPTX 生成完成")
    
    # 内存使用
    logger.performance.log_memory()
    
    logger.section("生成完成")
```

## 🐛 调试技巧

### 临时启用 DEBUG 级别

```python
logger = AppLogger(name="App", level=logging.INFO)

# 某个复杂函数需要详细日志
logger.set_level(logging.DEBUG)
complex_function()

# 恢复正常级别
logger.set_level(logging.INFO)
```

### 记录函数调用

```python
def my_function(a, b, c=10):
    logger.log_function_call("my_function", args=(a, b), kwargs={"c": c})
    
    result = a + b + c
    
    logger.log_return("my_function", result)
    return result
```

### 捕获和记录异常

```python
try:
    risky_operation()
except Exception as e:
    logger.exception("操作失败")  # 自动记录堆栈
    # 或
    logger.error(f"操作失败: {e}")
```

## 📁 日志文件管理

### 日志文件位置

```
logs/
├── AutoPPT_20250117_103045.log      # 当前日志
├── AutoPPT_20250117_103045.log.1    # 备份 1
├── AutoPPT_20250117_103045.log.2    # 备份 2
└── ...
```

### 日志轮转

- 单个文件最大 10MB（可配置）
- 保留最近 5 个文件（可配置）
- 自动清理旧文件

### 清理日志

```python
import shutil
from pathlib import Path

# 删除旧日志
log_dir = Path("logs")
for log_file in log_dir.glob("*.log.*"):
    if log_file.stat().st_mtime < old_threshold:
        log_file.unlink()
```

## ⚡ 性能考虑

### 日志级别影响

| 级别 | 输出内容 | 性能影响 |
|------|----------|----------|
| DEBUG | 所有日志 | 最大 |
| INFO | INFO 及以上 | 中等 |
| WARNING | WARNING 及以上 | 较小 |
| ERROR | ERROR 及以上 | 最小 |

### 生产环境建议

```python
# 开发环境
logger = AppLogger(level=logging.DEBUG, colored=True)

# 生产环境
logger = AppLogger(level=logging.INFO, colored=False)
```

## 🔒 最佳实践

1. **统一使用全局日志器**
   ```python
   logger = get_logger()  # 所有模块使用同一个
   ```

2. **合理使用日志级别**
   - DEBUG: 详细的调试信息
   - INFO: 正常的程序流程
   - WARNING: 警告但不影响运行
   - ERROR: 错误但程序继续
   - CRITICAL: 严重错误

3. **使用计时器监控性能**
   ```python
   with logger.timer("关键操作"):
       critical_operation()
   ```

4. **记录重要的状态变化**
   ```python
   logger.info(f"状态从 {old_state} 变为 {new_state}")
   ```

5. **使用装饰器简化代码**
   ```python
   @logger.log_performance
   def important_function():
       pass
   ```

6. **程序结束时关闭日志器**
   ```python
   logger.close()
   ```

## 🎯 常见问题

### Q: 如何在多线程中使用？

A: Logger 是线程安全的，直接使用即可：
```python
from threading import Thread

def worker():
    logger.info(f"线程 {Thread.current_thread().name} 执行")

threads = [Thread(target=worker) for _ in range(5)]
for t in threads:
    t.start()
```

### Q: 如何禁用彩色输出？

A: 设置 `colored=False`：
```python
logger = AppLogger(colored=False)
```

### Q: 如何修改日志格式？

A: 修改 `AppLogger` 类中的格式化字符串。

### Q: 日志文件太大怎么办？

A: 调整 `max_file_size` 和 `backup_count`：
```python
logger = AppLogger(
    max_file_size=5*1024*1024,  # 5MB
    backup_count=10  # 保留 10 个文件
)
```

---

**最后更新**: 2025-10-17  
**维护者**: 智造業 john

