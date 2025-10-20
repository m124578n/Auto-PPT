# 🌐 Playwright 爬虫使用指南

## 📚 概览

本模块提供了两种版本的 Playwright 爬虫：

1. **AsyncScrapyPlaywright** - 异步版本（推荐用于高并发场景）
2. **SyncScrapyPlaywright** - 同步版本（推荐用于简单场景或脚本）

## 🚀 快速开始

### 1. 异步版本（AsyncScrapyPlaywright）

适用于：
- 需要高性能和并发处理
- 已有异步代码环境
- 需要同时爬取多个网站

```python
import asyncio
from AutoPPT.scrapy.playwright import AsyncScrapyPlaywright

async def main():
    scrapy = AsyncScrapyPlaywright()
    
    await scrapy.start(
        target_url="https://example.com",
        extracted_content_file="content.txt",
        images_downloaded_dir="images"
    )
    
    print("爬取完成！")

# 运行异步函数
if __name__ == "__main__":
    asyncio.run(main())
```

### 2. 同步版本（SyncScrapyPlaywright）

适用于：
- 简单的爬虫脚本
- 顺序执行的场景
- 不需要处理异步的情况

```python
from AutoPPT.scrapy.playwright import SyncScrapyPlaywright

def main():
    scrapy = SyncScrapyPlaywright()
    
    scrapy.start(
        target_url="https://example.com",
        extracted_content_file="content.txt",
        images_downloaded_dir="images"
    )
    
    print("爬取完成！")

if __name__ == "__main__":
    main()
```

## 📖 详细使用

### 基本参数说明

| 参数 | 类型 | 说明 | 必填 |
|------|------|------|------|
| `target_url` | str | 目标网页URL | ✅ |
| `extracted_content_file` | str | 提取内容保存路径 | ✅ |
| `images_downloaded_dir` | str | 图片下载目录 | ✅ |

### 输出文件

#### 1. 提取的文字内容
```
extracted_content.txt
├── === 文字内容 ===
├── 文字1
├── 文字2
└── ...
```

#### 2. 下载的图片
```
images_downloaded_dir/
├── abc123.jpg           # 处理后的图片
├── def456.webp
└── ...

images_downloaded_dir_original_images/
├── original_abc123.jpg  # 原始图片
├── original_def456.webp
└── ...
```

#### 3. 全页面截图（当图片不足时）
```
images_downloaded_dir/
├── screenshot_000.jpg
├── screenshot_001.jpg
└── ...
```

## 🔧 高级用法

### 1. 并发爬取多个网站（异步版本）

```python
import asyncio
from AutoPPT.scrapy.playwright import AsyncScrapyPlaywright

async def scrape_single(url: str, output_dir: str):
    """爬取单个网站"""
    scrapy = AsyncScrapyPlaywright()
    
    content_file = f"{output_dir}/content.txt"
    images_dir = f"{output_dir}/images"
    
    await scrapy.start(url, content_file, images_dir)

async def scrape_multiple(urls: list):
    """并发爬取多个网站"""
    tasks = []
    
    for i, url in enumerate(urls):
        output_dir = f"output_{i}"
        task = scrape_single(url, output_dir)
        tasks.append(task)
    
    # 并发执行所有任务
    await asyncio.gather(*tasks)
    
    print(f"完成 {len(urls)} 个网站的爬取！")

# 使用示例
urls = [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com",
]

asyncio.run(scrape_multiple(urls))
```

### 2. 批量爬取（同步版本）

```python
from AutoPPT.scrapy.playwright import SyncScrapyPlaywright

def scrape_batch(urls: list):
    """批量爬取网站"""
    scrapy = SyncScrapyPlaywright()
    
    for i, url in enumerate(urls):
        print(f"\n[{i+1}/{len(urls)}] 爬取: {url}")
        
        try:
            scrapy.start(
                target_url=url,
                extracted_content_file=f"output_{i}/content.txt",
                images_downloaded_dir=f"output_{i}/images"
            )
            print(f"✅ 完成: {url}")
            
        except Exception as e:
            print(f"❌ 失败: {url} - {e}")
            continue
    
    print(f"\n批量爬取完成！")

# 使用示例
urls = [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com",
]

scrape_batch(urls)
```

### 3. 自定义配置

```python
from AutoPPT.scrapy.playwright import SyncScrapyPlaywright

class CustomScrapy(SyncScrapyPlaywright):
    """自定义爬虫配置"""
    
    def start(self, target_url, extracted_content_file, images_downloaded_dir):
        print(f"🚀 开始爬取: {target_url}")
        
        # 调用父类方法
        super().start(target_url, extracted_content_file, images_downloaded_dir)
        
        print(f"✅ 爬取完成: {target_url}")

# 使用自定义爬虫
scrapy = CustomScrapy()
scrapy.start("https://example.com", "content.txt", "images")
```

## 🎯 使用场景对比

### 何时使用异步版本（AsyncScrapyPlaywright）

✅ **推荐场景**：
- 需要同时爬取多个网站
- 高并发需求
- 与其他异步代码集成
- 需要最大化性能

❌ **不推荐**：
- 简单的单次爬取
- 不熟悉异步编程
- 顺序处理就足够

**示例**：
```python
# 并发爬取 10 个网站，速度快
urls = [f"https://example{i}.com" for i in range(10)]
await asyncio.gather(*[scrape(url) for url in urls])
```

### 何时使用同步版本（SyncScrapyPlaywright）

✅ **推荐场景**：
- 简单的脚本任务
- 单个或少量网站爬取
- 顺序处理即可
- 代码简单易懂

❌ **不推荐**：
- 需要高并发
- 性能要求高
- 已有异步架构

**示例**：
```python
# 简单直接，一个接一个爬取
for url in urls:
    scrapy.start(url, ...)
```

## 📊 性能对比

| 场景 | 异步版本 | 同步版本 | 性能差异 |
|------|----------|----------|----------|
| 单个网站 | ~10秒 | ~10秒 | 无差异 |
| 3个网站（并发） | ~12秒 | ~30秒 | **2.5x** ⬆️ |
| 10个网站（并发） | ~15秒 | ~100秒 | **6.7x** ⬆️ |
| 内存占用 | 稍高 | 正常 | - |
| 代码复杂度 | 中 | 低 | - |

## 🔍 功能特性

### 两个版本共同特性

✅ **自动代理检测和切换**
- 自动测试目标URL是否可访问
- 失败时自动尝试代理列表
- 智能选择可用代理

✅ **智能图片下载**
- 拦截所有图片响应
- 支持 JPG、JPEG、WebP 格式
- 自动过滤太小的图片（<350x350）
- 自动过滤太大的文件（>13MB）
- 保存原图和处理后的图片

✅ **全页面截图**
- 图片不足时自动启用
- 分段截图，避免单张过大
- 最多30张截图

✅ **内容提取**
- 提取所有可见文字
- 过滤导航、页脚等无关内容
- 保存为结构化文本

✅ **反爬虫特性**
- 随机 User-Agent
- 完整的浏览器特征模拟
- Playwright Stealth 插件
- 自然的滚动行为

## ⚠️ 注意事项

### 1. 依赖安装

```bash
# 安装 Playwright
pip install playwright playwright-stealth

# 安装浏览器
playwright install chromium
```

### 2. 异步版本注意事项

```python
# ❌ 错误：忘记 await
scrapy = AsyncScrapyPlaywright()
scrapy.start(...)  # 返回 coroutine，不会执行

# ✅ 正确：使用 await
await scrapy.start(...)

# ❌ 错误：在非异步函数中使用
def main():
    await scrapy.start(...)  # SyntaxError

# ✅ 正确：在异步函数中使用
async def main():
    await scrapy.start(...)
```

### 3. 同步版本注意事项

```python
# ❌ 错误：尝试并发
for url in urls:
    # 这是顺序执行，不是并发
    scrapy.start(url, ...)

# ✅ 如需并发，使用异步版本
```

### 4. 资源管理

```python
# ✅ 推荐：为每个任务创建独立的目录
for i, url in enumerate(urls):
    scrapy.start(
        url,
        f"output_{i}/content.txt",
        f"output_{i}/images"
    )
```

## 🐛 常见问题

### Q1: 如何选择异步还是同步？

**A**: 
- 爬取1-3个网站 → 同步版本
- 爬取4个以上网站 → 异步版本
- 需要集成到异步项目 → 异步版本
- 简单脚本 → 同步版本

### Q2: 异步版本报错 "RuntimeError: asyncio.run() cannot be called from a running event loop"

**A**: 
```python
# 在 Jupyter Notebook 中使用
import nest_asyncio
nest_asyncio.apply()

await scrapy.start(...)  # 直接 await，不用 asyncio.run()
```

### Q3: 如何禁用代理？

**A**: 
```python
# 修改 SimpleProxyManager
proxy_manager = SimpleProxyManager()
proxy_manager.proxies = []  # 清空代理列表
```

### Q4: 如何增加超时时间？

**A**: 
```python
# 在代码中修改
page.set_default_timeout(120000)  # 改为120秒
```

## 📝 完整示例

### 示例1：简单爬取（同步）

```python
from AutoPPT.scrapy.playwright import SyncScrapyPlaywright

scrapy = SyncScrapyPlaywright()
scrapy.start(
    target_url="https://example.com",
    extracted_content_file="content.txt",
    images_downloaded_dir="images"
)
```

### 示例2：并发爬取（异步）

```python
import asyncio
from AutoPPT.scrapy.playwright import AsyncScrapyPlaywright

async def main():
    urls = ["https://example1.com", "https://example2.com"]
    scrapy = AsyncScrapyPlaywright()
    
    tasks = []
    for i, url in enumerate(urls):
        task = scrapy.start(
            url,
            f"output_{i}/content.txt",
            f"output_{i}/images"
        )
        tasks.append(task)
    
    await asyncio.gather(*tasks)

asyncio.run(main())
```

### 示例3：错误处理

```python
from AutoPPT.scrapy.playwright import SyncScrapyPlaywright

scrapy = SyncScrapyPlaywright()

try:
    scrapy.start(
        target_url="https://example.com",
        extracted_content_file="content.txt",
        images_downloaded_dir="images"
    )
    print("✅ 爬取成功")
    
except Exception as e:
    print(f"❌ 爬取失败: {e}")
    # 处理错误...
```

## 🔗 相关文档

- [Playwright 官方文档](https://playwright.dev/python/)
- [Playwright Stealth](https://github.com/AtuboDad/playwright_stealth)
- [Python 异步编程指南](https://docs.python.org/3/library/asyncio.html)

---

**最后更新**: 2025-10-17  
**维护者**: 智造業 john

