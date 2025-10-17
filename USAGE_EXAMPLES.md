# 📘 AutoPPT 使用示例

## 基本使用

### 方式 1：使用命令行腳本

```bash
# 修改 ai_html_to_ppt.py 中的 TEXT_CONTENT
python ai_html_to_ppt.py
```

### 方式 2：使用 AutoPPT 類（推薦）

```python
from ai_html_to_ppt import AutoPPT
import os

# 初始化
api_key = os.getenv("GEMINI_API_KEY")
auto_ppt = AutoPPT(api_key=api_key, use_images=False)

# 生成簡報
data = auto_ppt.generate(
    text_content="你的簡報內容...",
    pdf_file=None,  # 可選的 PDF 文件
    save_files=True  # 自動保存 HTML 和 JSON
)
```

## 進階用法

### 示例 1：純文字簡報

```python
from ai_html_to_ppt import AutoPPT
import os

# 準備內容
content = """
產品發表會

主要亮點：
- 創新設計理念
- 卓越性能表現
- 超值性價比

技術規格：
- 處理器：最新 AI 晶片
- 記憶體：16GB RAM
- 儲存：512GB SSD
"""

# 生成
auto_ppt = AutoPPT(api_key=os.getenv("GEMINI_API_KEY"))
data = auto_ppt.generate(text_content=content)
```

### 示例 2：帶圖片的簡報

```python
from ai_html_to_ppt import AutoPPT
import os

# 確保圖片在 downloaded_images/ 目錄

content = """
旅遊推廣簡報

行程特色：
- 世界遺產景點
- 特色美食體驗
- 豪華住宿安排
"""

# 啟用圖片
auto_ppt = AutoPPT(
    api_key=os.getenv("GEMINI_API_KEY"),
    use_images=True  # 啟用圖片功能
)

data = auto_ppt.generate(text_content=content)
```

### 示例 3：從 PDF 生成簡報

```python
from ai_html_to_ppt import AutoPPT
import os

# 準備 PDF 文件
pdf_path = "報告.pdf"

content = "請根據提供的 PDF 生成簡報"

auto_ppt = AutoPPT(api_key=os.getenv("GEMINI_API_KEY"))
data = auto_ppt.generate(
    text_content=content,
    pdf_file=pdf_path  # 指定 PDF
)
```

### 示例 4：分步控制生成流程

```python
from ai_html_to_ppt import AutoPPT
import os

auto_ppt = AutoPPT(
    api_key=os.getenv("GEMINI_API_KEY"),
    use_images=True
)

# 步驟 1：載入圖片
auto_ppt.load_images()

# 步驟 2：生成簡報結構
data = auto_ppt.generate_presentation(
    text_content="你的內容...",
    pdf_file="文件.pdf",
    model="gemini-2.5-flash"  # 可指定模型
)

# 步驟 3：查看生成的結構
print(f"標題：{data['title']}")
print(f"幻燈片數量：{len(data['slides'])}")

# 步驟 4：保存文件
html_file = auto_ppt.save_html(data)
json_file = auto_ppt.save_json(data)

print(f"已保存：{html_file}, {json_file}")
```

### 示例 5：自定義文件名

```python
from ai_html_to_ppt import AutoPPT
import os

auto_ppt = AutoPPT(api_key=os.getenv("GEMINI_API_KEY"))

# 生成簡報
data = auto_ppt.generate_presentation(
    text_content="你的內容...",
    save_files=False  # 不自動保存
)

# 自定義文件名保存
auto_ppt.save_html(data, filename="我的簡報.html")
auto_ppt.save_json(data, filename="我的簡報_數據.json")
auto_ppt.save_pptx(data, filename="我的簡報.pptx")
```

### 示例 6：僅生成數據不保存

```python
from ai_html_to_ppt import AutoPPT
import os

auto_ppt = AutoPPT(api_key=os.getenv("GEMINI_API_KEY"))

# 僅生成數據
data = auto_ppt.generate(
    text_content="你的內容...",
    save_files=False  # 不保存文件
)

# 手動處理數據
for slide in data['slides']:
    print(f"類型：{slide['slide_type']}")
    if 'title' in slide:
        print(f"標題：{slide['title']}")
```

### 示例 7：批量生成多個簡報

```python
from ai_html_to_ppt import AutoPPT
import os

auto_ppt = AutoPPT(api_key=os.getenv("GEMINI_API_KEY"))

# 多個主題
topics = [
    "產品介紹",
    "市場分析", 
    "財務報告"
]

for topic in topics:
    content = f"{topic}\n\n相關內容..."
    
    try:
        data = auto_ppt.generate(text_content=content)
        print(f"✅ {topic} - 生成成功")
    except Exception as e:
        print(f"❌ {topic} - 生成失敗：{e}")
```

### 示例 8：僅生成 PPTX

```python
from ai_html_to_ppt import AutoPPT
import os

auto_ppt = AutoPPT(api_key=os.getenv("GEMINI_API_KEY"))

# 生成簡報數據
data = auto_ppt.generate_presentation(
    text_content="你的內容...",
    pdf_file="報告.pdf"
)

# 僅保存 PPTX（不需要 HTML）
pptx_file = auto_ppt.save_pptx(data, "最終簡報.pptx")
print(f"✅ PPTX 已保存：{pptx_file}")
```

### 示例 9：錯誤處理

```python
from ai_html_to_ppt import AutoPPT
import os

auto_ppt = AutoPPT(api_key=os.getenv("GEMINI_API_KEY"))

try:
    data = auto_ppt.generate(
        text_content="你的內容...",
        pdf_file="不存在.pdf"  # 不存在的文件會被忽略
    )
    print("✅ 生成成功")
    
except json.JSONDecodeError as e:
    print(f"❌ AI 返回格式錯誤：{e}")
    
except Exception as e:
    print(f"❌ 其他錯誤：{e}")
```

## 🔧 API 參考

### AutoPPT 類

```python
class AutoPPT:
    def __init__(self, api_key: str, use_images: bool = False)
    """
    Args:
        api_key: Google Gemini API Key
        use_images: 是否使用圖片資源
    """
```

### 主要方法

#### generate()
```python
def generate(
    text_content: str, 
    pdf_file: str = None,
    save_files: bool = True
) -> Dict
"""
完整的簡報生成流程
    
Args:
    text_content: 文字內容
    pdf_file: PDF 文件路徑（可選）
    save_files: 是否保存文件
    
Returns:
    簡報數據（dict）
"""
```

#### generate_presentation()
```python
def generate_presentation(
    text_content: str, 
    pdf_file: str = None,
    model: str = "gemini-2.5-flash"
) -> Dict
"""
使用 AI 生成簡報結構
    
Args:
    text_content: 文字內容
    pdf_file: PDF 文件路徑（可選）
    model: AI 模型名稱
    
Returns:
    簡報數據（dict）
"""
```

#### save_html()
```python
def save_html(data: Dict, filename: str = None) -> str
"""
保存 HTML 文件
    
Args:
    data: 簡報數據
    filename: 文件名（可選，默認根據 topic 生成）
    
Returns:
    文件路徑
"""
```

#### save_json()
```python
def save_json(data: Dict, filename: str = None) -> str
"""
保存 JSON 數據文件
    
Args:
    data: 簡報數據
    filename: 文件名（可選，默認根據 topic 生成）
    
Returns:
    文件路徑
"""
```

#### save_pptx()
```python
def save_pptx(data: Dict, filename: str = None) -> str
"""
保存 PPTX 文件
    
Args:
    data: 簡報數據
    filename: 文件名（可選，默認根據 topic 生成）
    
Returns:
    文件路徑
"""
```

#### load_images()
```python
def load_images(image_dir: str = "downloaded_images")
"""
載入圖片資源
    
Args:
    image_dir: 圖片目錄路徑
"""
```

## 💡 實用技巧

### 技巧 1：使用環境變數

```python
from ai_html_to_ppt import AutoPPT
from dotenv import load_dotenv
import os

load_dotenv()  # 從 .env 載入

auto_ppt = AutoPPT(api_key=os.getenv("GEMINI_API_KEY"))
```

### 技巧 2：重用 AutoPPT 實例

```python
auto_ppt = AutoPPT(api_key=os.getenv("GEMINI_API_KEY"))

# 生成多個簡報
for content in contents_list:
    auto_ppt.generate(text_content=content)
```

### 技巧 3：查看生成的 Prompt

```python
auto_ppt = AutoPPT(api_key=os.getenv("GEMINI_API_KEY"))

# 查看生成的 prompt
prompt = auto_ppt.generate_prompt("你的內容...")
print(prompt)  # 可以看到發送給 AI 的完整 prompt
```

### 技巧 4：修改 AI 模型

```python
# 使用更強大的模型
data = auto_ppt.generate_presentation(
    text_content="複雜的內容...",
    model="gemini-2.0-flash-exp"  # 試驗性模型
)
```

## 🚀 快速開始範本

將以下代碼保存為 `my_presentation.py`：

```python
#!/usr/bin/env python3
"""
快速生成簡報範本
"""

from ai_html_to_ppt import AutoPPT
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

# 你的內容
CONTENT = """
在這裡輸入你的簡報內容...

可以包含：
- 標題
- 列表
- 段落
- 等等...
"""

def main():
    # 初始化
    auto_ppt = AutoPPT(
        api_key=os.getenv("GEMINI_API_KEY"),
        use_images=False  # 是否使用圖片
    )
    
    # 生成
    auto_ppt.generate(
        text_content=CONTENT,
        pdf_file=None,  # 如果有 PDF 就填路徑
        save_files=True
    )

if __name__ == "__main__":
    main()
```

運行：
```bash
python my_presentation.py
```

---

**更多示例請參考：**
- [README.md](README.md) - 完整文檔
- [QUICKSTART.md](QUICKSTART.md) - 快速開始
- [test_refactored.py](test_refactored.py) - 測試用例

