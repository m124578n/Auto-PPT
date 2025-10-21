# 🎨 Auto-PPT

> AI 驅動的智能簡報生成器 - 從網頁、PDF、文字和圖片自動生成精美的 HTML 和 PPTX 演示文稿

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-black.svg)](https://github.com/psf/black)

## ✨ 功能特點

### 🤖 AI 智能生成
- 使用 Google Gemini AI（gemini-2.5-flash）自動分析內容
- 智能識別主題並組織簡報結構
- 自動安排圖片和文字佈局
- 生成專業的演示文稿

### 🌐 多源內容支持
- **網頁爬取**：自動從 URL 提取文字和圖片（基於 Playwright）
- **PDF 解析**：智能解析 PDF 文件內容
- **圖片資源**：支持本地圖片上傳和使用
- **文字內容**：直接輸入或從文件讀取
- **混合輸入**：可同時處理多種來源的內容

### 🎨 強大的模板系統
- **PPTX 模板支持**：使用現有 PowerPoint 文件作為模板
- **JSON 配置**：靈活的模板定義格式
- **自動轉換工具**：將 PPTX 轉換為 JSON 模板
- **保留原始設計**：維持模板的版面配置和樣式
- **動態元素佈局**：智能處理水平和垂直排列

### 🎯 多格式輸出
- **HTML 預覽**：可在瀏覽器中交互預覽
- **PPTX 匯出**：完整的 PowerPoint 文件
- **JSON 數據**：結構化數據供後續處理
- 保持一致的樣式和佈局

### 🏗️ 高度可擴展
- **模板引擎架構**：動態加載和管理 Slide 類型
- **JSON 驅動**：通過配置文件定義新的 Slide 類型
- **零代碼擴展**：無需編寫代碼即可創建新模板
- **自動化 AI Prompt**：從模板自動生成 LLM 指令
- **模塊化架構**：清晰的包結構，易於維護

### 📐 智能佈局
- 圖片自動保持寬高比
- 文字和圖片智能對齊
- 動態字體大小調整（防止內容溢出）
- 水平和垂直元素排列支持
- 自動文件管理（臨時目錄 + 隨機前綴）
- 完整的日誌系統

## 🚀 快速開始

### 前置要求

- Python 3.12 或更高版本
- Google Gemini API Key

### 安裝

1. **克隆倉庫**
```bash
git clone <repository-url>
cd auto-ppt
```

2. **安裝依賴**

使用 uv (推薦):
```bash
uv sync
```

或使用 pip:
```bash
pip install -e .
```

3. **安裝 Playwright 瀏覽器（用於網頁爬取）**

```bash
playwright install chromium
```

4. **配置 API Key**

創建 `.env` 文件：
```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

獲取 API Key：訪問 [Google AI Studio](https://aistudio.google.com/apikey)

### 基本使用

#### 方式 1：使用主程序（最簡單）

```bash
python main.py
```

這會：
1. 使用 AI 分析內容（文字、PDF、圖片）
2. 生成簡報結構（JSON）
3. 自動生成 HTML 文件供預覽
4. **自動生成 PPTX 文件** ✨
5. 所有文件保存到臨時目錄

**輸出文件：**
```
temp_dir/tmpXXXXXX/output/
├── 123456_簡報主題_presentation.html
├── 123456_簡報主題_data.json
└── 123456_簡報主題.pptx
```

#### 方式 2：使用 AutoPPT 類（推薦）

```python
from AutoPPT import AutoPPT
import os
import tempfile

# 初始化
tempfile_dir = tempfile.mkdtemp(dir="temp_dir")
auto_ppt = AutoPPT(
    api_key=os.getenv("GEMINI_API_KEY"),
    use_images=True,  # 是否使用圖片
    output_dir=tempfile_dir,  # 輸出目錄
    template_json_path="templates/test_template.json",  # 可選：模板配置
    template_pptx_path="pptx_template/test.pptx"  # 可選：PPTX 模板
)

# 一鍵生成 HTML + JSON + PPTX
data = auto_ppt.generate(
    prompt="請根據提供的內容生成簡報",
    other_files=["報告.pdf"],  # 可選：其他檔案
    save_files=True  # 自動保存所有格式
)
```

#### 方式 3：從網頁生成簡報

```python
from AutoPPT import AutoPPT
import os
import tempfile

tempfile_dir = tempfile.mkdtemp(dir="temp_dir")
auto_ppt = AutoPPT(
    api_key=os.getenv("GEMINI_API_KEY"),
    use_images=True,
    output_dir=tempfile_dir
)

# 從 URL 爬取內容並生成簡報
data = auto_ppt.generate(
    prompt="請統整這些旅遊行程並生成簡報",
    url_links=[
        "https://example.com/travel-1",
        "https://example.com/travel-2"
    ],
    save_files=True
)
```

#### 方式 4：使用自定義模板

```python
from AutoPPT import AutoPPT
import os
import tempfile

tempfile_dir = tempfile.mkdtemp(dir="temp_dir")

# 使用自己的 PPTX 模板
auto_ppt = AutoPPT(
    api_key=os.getenv("GEMINI_API_KEY"),
    output_dir=tempfile_dir,
    template_json_path="templates/my_custom_template.json",
    template_pptx_path="my_template.pptx"
)

data = auto_ppt.generate(
    prompt="根據模板風格生成簡報",
    save_files=True
)
```

## 📖 詳細使用

### 🎨 使用模板系統

#### 1. 使用內建模板

專案提供了多個預設模板：

```python
from AutoPPT import AutoPPT
import tempfile

# 使用測試模板
auto_ppt = AutoPPT(
    api_key=API_KEY,
    output_dir=tempfile.mkdtemp(dir="temp_dir"),
    template_json_path="templates/test_template.json",
    template_pptx_path="pptx_template/test.pptx"
)
```

可用模板：
- `templates/default_template.json` - 默認模板
- `templates/test_template.json` - 測試模板
- `templates/my_custom_template.json` - 自定義模板示例

#### 2. 創建自己的模板

**方法 A：從 PPTX 自動生成**

使用 `pptx_template_creator.py` 工具：

```bash
# 安裝依賴後運行
python pptx_template_creator.py
```

或在 Python 中：

```python
from pptx_template_creator import PPTXTemplateCreator
import os

creator = PPTXTemplateCreator(api_key=os.getenv('GEMINI_API_KEY'))

# 從現有 PPTX 生成 JSON 模板
creator.create_template_from_pptx(
    pptx_path="my_design.pptx",
    output_path="templates/my_template.json",
    template_name="我的模板"
)
```

**方法 B：手動編寫 JSON**

參考 `templates/test_template.json` 的格式：

```json
{
  "template_info": {
    "name": "我的模板",
    "version": "1.0.0",
    "description": "自定義模板"
  },
  "slide_types": [
    {
      "type_id": "title_slide",
      "name": "標題頁",
      "description": "簡報開頭",
      "llm_instruction": "用於簡報的開頭",
      "json_schema": {
        "slide_type": "title_slide",
        "title": "標題文字"
      },
      "pptx_layout": {
        "layout_index": 0,
        "elements": [...]
      }
    }
  ]
}
```

詳細指南請參考：[PPTX_TEMPLATE_CREATOR_GUIDE.md](cursor_agent_md/PPTX_TEMPLATE_CREATOR_GUIDE.md)

### 🌐 從網頁爬取內容

```python
from AutoPPT import AutoPPT
import tempfile

auto_ppt = AutoPPT(
    api_key=API_KEY,
    use_images=True,  # 自動下載網頁圖片
    output_dir=tempfile.mkdtemp(dir="temp_dir")
)

# 爬取單個網頁
auto_ppt.generate(
    prompt="分析這個網頁內容並生成簡報",
    url_links=["https://example.com/article"],
    save_files=True
)

# 爬取多個網頁並整合
auto_ppt.generate(
    prompt="整合這些產品資訊",
    url_links=[
        "https://example.com/product-1",
        "https://example.com/product-2"
    ],
    save_files=True
)
```

爬蟲功能：
- 自動提取文字內容
- 下載頁面圖片
- 支援動態網頁（Playwright）
- 去除廣告和無關內容

### 📄 從 PDF 生成簡報

```python
from AutoPPT import AutoPPT
import tempfile

auto_ppt = AutoPPT(
    api_key=API_KEY,
    output_dir=tempfile.mkdtemp(dir="temp_dir")
)

# 分析 PDF 並生成簡報
auto_ppt.generate(
    prompt="請根據 PDF 內容生成投資分析簡報",
    other_files=["投資月報_20250930.pdf"],
    save_files=True
)
```

### 🖼️ 使用圖片資源

圖片會自動從以下來源加載：
1. 網頁爬取的圖片（保存到 `temp_dir/tmpXXX/images/`）
2. 手動放置的圖片（放到輸出目錄的 `images/` 子目錄）

```python
# 啟用圖片功能
auto_ppt = AutoPPT(
    api_key=API_KEY,
    use_images=True,  # 啟用圖片
    output_dir=output_dir
)

# 圖片會被自動上傳到 Gemini 並在簡報中使用
auto_ppt.generate(
    prompt="創建旅遊簡報，使用提供的圖片",
    save_files=True
)
```

### 🔧 自定義配置

#### 指定輸出目錄

```python
import tempfile

# 使用自定義臨時目錄
custom_dir = tempfile.mkdtemp(dir="my_output")

auto_ppt = AutoPPT(
    api_key=API_KEY,
    output_dir=custom_dir
)
```

#### 選擇 AI 模型

```python
# 在 generate_presentation 方法中指定
data = auto_ppt.generate_presentation(
    contents=contents,
    model="gemini-2.5-flash"  # 或其他 Gemini 模型
)
```

#### 查看日誌

日誌會自動保存到 `logs/AutoPPT_YYYYMMDD.log`：

```python
# 日誌會記錄：
# - API 調用
# - 檔案處理
# - 錯誤信息
# - Token 使用量
```

## 🏗️ 架構設計

### 項目結構

```
auto-ppt/
├── AutoPPT/                        # 核心包
│   ├── __init__.py                # 包初始化（匯出 AutoPPT）
│   ├── auto_ppt.py                # AutoPPT 主類
│   ├── template_engine.py         # 模板引擎（核心）
│   ├── slide_generator.py         # HTML/PPTX 生成器
│   ├── scrapy/                    # 爬蟲模組
│   │   ├── base_scrapy.py        # 爬蟲基類
│   │   └── playwright.py         # Playwright 實現
│   └── utils/                     # 工具模組
│       └── logger.py              # 日誌系統
├── templates/                     # 模板配置文件
│   ├── default_template.json     # 默認模板
│   ├── test_template.json        # 測試模板
│   └── my_custom_template.json   # 自定義模板
├── pptx_template/                 # PPTX 模板文件
│   ├── test.pptx                 # 測試 PPTX
│   └── test_analysis.json        # 模板分析結果
├── temp_dir/                      # 臨時工作目錄
│   └── tmpXXXXXX/                # 每次運行的臨時目錄
│       ├── content/              # 爬取的文字內容
│       ├── images/               # 下載的圖片
│       └── output/               # 生成的文件
│           ├── 123456_主題_presentation.html
│           ├── 123456_主題_data.json
│           └── 123456_主題.pptx
├── logs/                          # 日誌文件
│   └── AutoPPT_YYYYMMDD.log      # 每日日誌
├── cursor_agent_md/               # 詳細文檔
│   ├── PPTX_TEMPLATE_CREATOR_GUIDE.md  # 模板創建指南
│   ├── AUTO_PPT_CLASS.md                # AutoPPT 類說明
│   ├── USAGE_EXAMPLES.md                # 使用示例
│   └── ...
├── main.py                        # 主入口程序
├── quick_example.py               # 快速示例
├── pptx_template_creator.py       # PPTX 轉 JSON 工具
├── .env                           # API Key 配置
├── pyproject.toml                 # 項目配置（uv）
├── uv.lock                        # 依賴鎖定文件
└── README.md                      # 本文件
```

### 核心設計模式

```
┌─────────────────────────────────────────────────┐
│              PPTXTemplate（模板引擎）            │
│  - 從 JSON/PPTX 加載模板定義                   │
│  - 動態生成 SlideType 類                       │
│  - 生成 AI Prompt                              │
│  - 管理 Slide 佈局和樣式                       │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────┴──────────┐
        ↓                     ↓
┌──────────────────┐  ┌──────────────────┐
│  HTMLGenerator   │  │  PPTXGenerator   │
│  - 生成 HTML     │  │  - 生成 PPTX     │
│  - 使用模板樣式  │  │  - 使用模板佈局  │
└──────────────────┘  └──────────────────┘
        ↑                     ↑
        └─────────┬───────────┘
                  │
        ┌─────────┴──────────┐
        │      AutoPPT       │
        │  - AI 內容分析     │
        │  - 檔案管理        │
        │  - 完整流程控制    │
        └────────────────────┘
                  │
        ┌─────────┴──────────┐
        │   SyncScrapyPlaywright  │
        │  - 網頁爬取        │
        │  - 圖片下載        │
        └────────────────────┘
```

### 關鍵特性

#### 1. AutoPPT 類（核心 API）

```python
class AutoPPT:
    """AI 驅動的自動簡報生成器"""
    
    def __init__(
        self, 
        api_key, 
        use_images=False, 
        output_dir="temp_dir",
        template_json_path=None,
        template_pptx_path=None
    ):
        """初始化，支援自定義模板"""
    
    def scrape_urls(self, urls):
        """爬取網頁內容和圖片"""
    
    def load_images(self):
        """載入圖片資源並上傳到 Gemini"""
    
    def generate_prompt(self, prompt):
        """生成 AI Prompt（從模板自動生成）"""
    
    def generate_presentation(self, contents, model="gemini-2.5-flash"):
        """使用 AI 生成簡報結構"""
    
    def save_html(self, data, filename=None):
        """保存 HTML 文件"""
    
    def save_json(self, data, filename=None):
        """保存 JSON 數據文件"""
    
    def save_pptx(self, data, filename=None):
        """保存 PPTX 文件（使用模板引擎）"""
    
    def generate(self, prompt, url_links=None, other_files=None, save_files=True):
        """完整的生成流程（一鍵生成）"""
```

#### 2. 模板引擎系統

```python
class PPTXTemplate:
    """PPTX 模板引擎"""
    
    def __init__(self, json_path=None, pptx_path=None):
        """從 JSON 或 PPTX 加載模板"""
    
    def load_from_json(self, json_path):
        """從 JSON 文件加載模板定義"""
    
    def load_from_pptx(self, pptx_path):
        """從 PPTX 文件加載母版和佈局"""
    
    def generate_ai_prompt(self, image_metadata, user_prompt):
        """自動生成 AI Prompt"""
    
    def create_slide_type(self, slide_type_def):
        """動態創建 SlideType 類"""
```

模板特性：
- ✅ JSON 驅動的 Slide 類型定義
- ✅ 支援 PPTX 母版和佈局
- ✅ 自動生成 LLM 指令
- ✅ 動態元素佈局（水平/垂直）
- ✅ 完整的樣式系統

#### 3. 爬蟲系統

```python
class SyncScrapyPlaywright:
    """基於 Playwright 的同步爬蟲"""
    
    def start(
        self, 
        target_url, 
        extracted_content_file, 
        images_downloaded_dir
    ):
        """爬取網頁並保存內容和圖片"""
```

特性：
- ✅ 支援動態網頁（JavaScript 渲染）
- ✅ 自動提取主要內容
- ✅ 下載頁面圖片
- ✅ 去除廣告和無關元素

#### 4. 智能文件管理

- 使用臨時目錄系統（`tempfile.mkdtemp`）
- 自動生成 6 位隨機前綴（避免文件名衝突）
- 分類保存：content/、images/、output/
- 文件命名格式：`123456_主題_類型.ext`
- 完整的日誌記錄

## 🔧 擴展指南

### 方法 1：通過 JSON 配置添加新類型（推薦）

最簡單的方式是編輯模板 JSON 文件，無需編寫代碼！

#### 步驟 1：編輯模板 JSON

在 `templates/my_template.json` 中添加新的 slide 類型：

```json
{
  "slide_types": [
    {
      "type_id": "timeline",
      "name": "時間軸頁",
      "description": "展示時間線上的重要事件",
      "llm_instruction": "用於展示公司發展歷程或產品演進歷史",
      "json_schema": {
        "slide_type": "timeline",
        "title": "發展歷程",
        "events": [
          {"year": "2020", "description": "公司成立"},
          {"year": "2021", "description": "A輪融資"}
        ]
      },
      "pptx_layout": {
        "layout_index": 6,
        "background": {
          "type": "solid",
          "color": "#FFFFFF"
        },
        "elements": [
          {
            "type": "textbox",
            "name": "title",
            "position": {"left": 1, "top": 0.5, "width": 12, "height": 1},
            "style": {
              "font_size": 32,
              "font_color": "#2C3E50",
              "bold": true
            }
          },
          {
            "type": "textbox",
            "name": "events",
            "position": {"left": 1, "top": 2, "width": 12, "height": 5},
            "style": {
              "font_size": 18,
              "font_color": "#34495E"
            }
          }
        ]
      }
    }
  ]
}
```

#### 步驟 2：就這樣！

- ✅ 類型自動生成
- ✅ AI Prompt 自動更新
- ✅ JSON Schema 自動包含
- ✅ PPTX 佈局自動應用
- ✅ HTML/PPTX 生成自動支持

### 方法 2：從現有 PPTX 生成模板

使用 `pptx_template_creator.py` 工具：

```bash
python pptx_template_creator.py
```

或在代碼中：

```python
from pptx_template_creator import PPTXTemplateCreator

creator = PPTXTemplateCreator(api_key=API_KEY)

# 分析現有 PPTX 並生成 JSON 模板
creator.create_template_from_pptx(
    pptx_path="my_design.pptx",
    output_path="templates/my_template.json",
    template_name="我的自定義模板"
)
```

這會：
1. 分析 PPTX 的每張投影片
2. 提取佈局、樣式、元素位置
3. 使用 AI 生成 JSON 模板
4. 保存完整的模板定義

### 方法 3：查看模板結構

查看當前模板的所有 Slide 類型：

```python
from AutoPPT import AutoPPT

auto_ppt = AutoPPT(
    api_key=API_KEY,
    template_json_path="templates/test_template.json"
)

print("可用的 Slide 類型：")
for type_id, slide_type in auto_ppt.template.slide_types.items():
    print(f"  - {type_id}: {slide_type['name']}")
    print(f"    {slide_type['description']}")
```

### 模板文檔

完整的模板創建指南請參考：
- [PPTX_TEMPLATE_CREATOR_GUIDE.md](cursor_agent_md/PPTX_TEMPLATE_CREATOR_GUIDE.md)
- [PPTX_TEMPLATE_USAGE.md](cursor_agent_md/PPTX_TEMPLATE_USAGE.md)

## 📚 使用示例

### 示例 1：從網頁爬取旅遊資訊

```python
from AutoPPT import AutoPPT
import os
import tempfile

tempfile_dir = tempfile.mkdtemp(dir="temp_dir")

auto_ppt = AutoPPT(
    api_key=os.getenv("GEMINI_API_KEY"),
    use_images=True,
    output_dir=tempfile_dir
)

# 爬取旅遊網站並生成簡報
data = auto_ppt.generate(
    prompt="請統整這些旅遊行程並生成簡報",
    url_links=[
        "https://travel.example.com/japan-tour",
        "https://travel.example.com/hokkaido-trip"
    ],
    save_files=True
)
```

**生成結果：**
```
temp_dir/tmpXXXXXX/
├── content/
│   ├── uuid1.txt  # 爬取的文字內容
│   └── uuid2.txt
├── images/        # 下載的圖片
│   ├── image1.jpg
│   └── image2.jpg
└── output/
    ├── 123456_旅遊行程_presentation.html
    ├── 123456_旅遊行程_data.json
    └── 123456_旅遊行程.pptx
```

### 示例 2：使用自定義模板生成產品簡報

```python
from AutoPPT import AutoPPT
import os
import tempfile

tempfile_dir = tempfile.mkdtemp(dir="temp_dir")

auto_ppt = AutoPPT(
    api_key=os.getenv("GEMINI_API_KEY"),
    output_dir=tempfile_dir,
    template_json_path="templates/my_custom_template.json",
    template_pptx_path="my_brand_template.pptx"
)

data = auto_ppt.generate(
    prompt="""
    智能手錶 X1 產品介紹
    
    主要功能：
    - 全天候健康監測
    - 50米防水設計
    - 超長續航 14 天
    """,
    save_files=True
)
```

### 示例 3：從 PDF 生成投資分析簡報

```python
from AutoPPT import AutoPPT
import os
import tempfile

tempfile_dir = tempfile.mkdtemp(dir="temp_dir")

auto_ppt = AutoPPT(
    api_key=os.getenv("GEMINI_API_KEY"),
    output_dir=tempfile_dir,
    template_json_path="templates/test_template.json"
)

data = auto_ppt.generate(
    prompt="請根據 PDF 內容生成投資分析簡報",
    other_files=["投資月報_20250930.pdf"],
    save_files=True
)
```

### 示例 4：混合多種來源生成簡報

```python
from AutoPPT import AutoPPT
import os
import tempfile

tempfile_dir = tempfile.mkdtemp(dir="temp_dir")

auto_ppt = AutoPPT(
    api_key=os.getenv("GEMINI_API_KEY"),
    use_images=True,
    output_dir=tempfile_dir
)

# 結合網頁、PDF 和文字提示
data = auto_ppt.generate(
    prompt="整合以下資料，生成市場分析簡報",
    url_links=["https://example.com/market-report"],
    other_files=["財報.pdf", "分析報告.pdf"],
    save_files=True
)
```

### 示例 5：批量生成（使用不同模板）

```python
from AutoPPT import AutoPPT
import os
import tempfile

projects = [
    {
        "name": "產品發表",
        "template": "templates/product_template.json",
        "content": "新產品介紹..."
    },
    {
        "name": "季度報告",
        "template": "templates/report_template.json",
        "content": "Q1 業績分析..."
    }
]

for project in projects:
    tempfile_dir = tempfile.mkdtemp(dir="temp_dir")
    
    auto_ppt = AutoPPT(
        api_key=os.getenv("GEMINI_API_KEY"),
        output_dir=tempfile_dir,
        template_json_path=project["template"]
    )
    
    data = auto_ppt.generate(
        prompt=project["content"],
        save_files=True
    )
    
    print(f"✅ {project['name']} 生成完成")
```

## 🎨 樣式定製

### 方法 1：通過 JSON 模板修改（推薦）

在模板 JSON 中直接修改樣式：

```json
{
  "pptx_layout": {
    "background": {
      "type": "solid",
      "color": "#3498DB"  // 修改背景顏色
    },
    "elements": [
      {
        "type": "textbox",
        "name": "title",
        "style": {
          "font_size": 36,        // 字體大小
          "font_color": "#2C3E50", // 文字顏色
          "bold": true,           // 粗體
          "font_name": "微軟正黑體" // 字體
        }
      }
    ]
  }
}
```

### 方法 2：使用自己設計的 PPTX

1. 在 PowerPoint 中設計好模板
2. 使用 `pptx_template_creator.py` 轉換為 JSON
3. AutoPPT 會自動套用你的設計

### 方法 3：修改現有模板文件

編輯 `templates/test_template.json`：

- 顏色：修改 `color` 欄位（使用 HEX 色碼）
- 字體：修改 `font_size`、`font_name`
- 位置：修改 `position` 的 `left`、`top`、`width`、`height`
- 對齊：修改 `alignment`（LEFT、CENTER、RIGHT）

## 🔍 常見問題

### Q: 如何獲取 Gemini API Key？

A: 訪問 [Google AI Studio](https://aistudio.google.com/apikey) 並創建 API Key。

### Q: 如何使用自己的 PowerPoint 模板？

A: 有兩種方式：
1. 使用 `pptx_template_creator.py` 工具自動轉換現有 PPTX
2. 初始化時指定模板路徑：
```python
auto_ppt = AutoPPT(
    api_key=API_KEY,
    template_pptx_path="my_template.pptx",
    template_json_path="templates/my_config.json"
)
```

### Q: 網頁爬取失敗怎麼辦？

A: 常見原因：
1. 未安裝 Playwright：運行 `playwright install chromium`
2. 網站有反爬蟲機制：某些網站可能阻擋自動化工具
3. 網路連線問題：檢查網路連接

### Q: 如何控制簡報的頁數或風格？

A: 在 `prompt` 中明確指示：
```python
auto_ppt.generate(
    prompt="生成10頁商業風格的產品簡報，包含市場分析和競品比較",
    save_files=True
)
```

### Q: 臨時文件會自動清理嗎？

A: 不會自動清理。臨時文件保存在 `temp_dir/` 中，可以手動刪除舊的臨時目錄：
```bash
rm -rf temp_dir/tmp*
```

### Q: 如何查看生成過程的日誌？

A: 日誌自動保存在 `logs/AutoPPT_YYYYMMDD.log`，包含：
- API 調用記錄
- 檔案處理過程
- 錯誤訊息
- Token 使用量

### Q: 能否使用其他 AI 模型？

A: 目前支援 Google Gemini 系列模型：
```python
data = auto_ppt.generate_presentation(
    contents=contents,
    model="gemini-2.5-flash"  # 或 gemini-2.0-flash-exp
)
```

### Q: 支持哪些文件格式？

A: 
- **輸入**：PDF、網頁 URL、圖片（JPG、PNG、GIF、WEBP）
- **輸出**：HTML、JSON、PPTX

### Q: 如何添加新的 Slide 類型？

A: 編輯模板 JSON 文件，添加新的 `slide_types` 項目即可，無需編寫代碼！詳見[擴展指南](#-擴展指南)。

### Q: 生成的簡報可以在 PowerPoint 中編輯嗎？

A: 可以！生成的 `.pptx` 文件是標準的 PowerPoint 格式，可以在 PowerPoint、Google Slides、WPS 等軟體中打開和編輯。

### Q: 如何貢獻代碼？

A: 
1. Fork 本倉庫
2. 創建功能分支
3. 提交更改並添加測試
4. 開啟 Pull Request

## 📖 詳細文檔

更多詳細信息，請查看 `cursor_agent_md/` 目錄：

### 核心文檔
- [AUTO_PPT_CLASS.md](cursor_agent_md/AUTO_PPT_CLASS.md) - AutoPPT 類完整說明
- [NEW_ARCHITECTURE_SUMMARY.md](cursor_agent_md/NEW_ARCHITECTURE_SUMMARY.md) - 新架構總覽
- [QUICKSTART_NEW_ARCHITECTURE.md](cursor_agent_md/QUICKSTART_NEW_ARCHITECTURE.md) - 快速開始指南

### 模板系統
- [PPTX_TEMPLATE_CREATOR_GUIDE.md](cursor_agent_md/PPTX_TEMPLATE_CREATOR_GUIDE.md) - 模板創建完整指南
- [PPTX_TEMPLATE_USAGE.md](cursor_agent_md/PPTX_TEMPLATE_USAGE.md) - 模板使用說明

### 使用指南
- [USAGE_EXAMPLES.md](cursor_agent_md/USAGE_EXAMPLES.md) - 詳細使用示例
- [USAGE.md](cursor_agent_md/USAGE.md) - 使用說明
- [LOGGER_USAGE.md](cursor_agent_md/LOGGER_USAGE.md) - 日誌系統使用

### 技術文檔
- [README_ARCHITECTURE.md](cursor_agent_md/README_ARCHITECTURE.md) - 架構說明
- [EXTENSIBILITY_GUIDE.md](cursor_agent_md/EXTENSIBILITY_GUIDE.md) - 擴展指南
- [REFACTOR_SUMMARY.md](cursor_agent_md/REFACTOR_SUMMARY.md) - 重構總結

## 🤝 貢獻

歡迎貢獻！請：

1. Fork 本倉庫
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 貢獻指南

- 遵循現有代碼風格
- 更新相關文檔
- 測試新功能
- 新的模板建議提供範例 JSON 和說明

## 📝 更新日誌

### v2.0.0 (2025-10-21) 🎉 重大更新

#### 🎨 模板引擎系統
- ✅ 全新的 `PPTXTemplate` 引擎
- ✅ JSON 驅動的 Slide 類型定義
- ✅ 支援 PPTX 模板文件（保留原始設計）
- ✅ 動態生成 SlideType 類
- ✅ 自動化 AI Prompt 生成
- ✅ 水平和垂直元素佈局

#### 🌐 網頁爬取功能
- ✅ 基於 Playwright 的爬蟲系統
- ✅ 自動提取網頁文字內容
- ✅ 自動下載網頁圖片
- ✅ 支援動態網頁（JavaScript 渲染）
- ✅ 多 URL 批量爬取

#### 🔧 PPTX 模板轉換工具
- ✅ `pptx_template_creator.py` 工具
- ✅ 自動分析 PPTX 結構
- ✅ 使用 AI 生成 JSON 模板
- ✅ 提取佈局、樣式、元素位置

#### 📁 文件管理優化
- ✅ 臨時目錄系統（`tempfile`）
- ✅ 分類管理：content/、images/、output/
- ✅ 隨機前綴避免衝突
- ✅ 完整的日誌系統（logs/）

#### 🔄 API 改進
- ✅ 新增 `url_links` 參數（爬取網頁）
- ✅ 新增 `other_files` 參數（支援多檔案）
- ✅ 新增 `template_json_path` 和 `template_pptx_path`
- ✅ `prompt` 參數替代 `text_content`
- ✅ 改進的錯誤處理和日誌

#### 📦 依賴更新
- ✅ 新增 `playwright` 和 `playwright-stealth`
- ✅ 新增 `beautifulsoup4` 和 `lxml`
- ✅ 新增 `aiofiles` 和 `psutil`
- ✅ 更新 `google-genai` 到 v1.33.0

### v1.2.0 (2025-10-17)

#### 項目結構重構
- ✅ 重構為 Python 包結構（`AutoPPT/` 包）
- ✅ 統一入口：`main.py`
- ✅ 清晰的模塊化架構

#### 文件管理優化
- ✅ 自動輸出到 `output/` 目錄
- ✅ 隨機前綴避免文件衝突

### v1.0.0 (2025-10-17)

#### 核心功能
- ✅ AI 驅動的智能簡報生成
- ✅ 支持 HTML 和 PPTX 雙格式輸出
- ✅ 多種 Slide 類型

#### 架構優化
- ✅ Strategy Pattern + Registry Pattern
- ✅ JSON Schema 自動提取和生成
- ✅ AI Prompt 動態生成

## 🌟 特別鳴謝

- [Google Gemini](https://ai.google.dev/) - AI 能力支持
- [python-pptx](https://python-pptx.readthedocs.io/) - PPTX 生成庫
- [Playwright](https://playwright.dev/python/) - 網頁自動化工具
- [Pillow](https://pillow.readthedocs.io/) - 圖片處理庫
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML 解析庫

## 📋 TODO 路線圖

以下是計劃中的功能和改進，按優先級排列：

### ✅ 已完成（v2.0.0）

#### 多輸入源支持
- ✅ **URL 鏈接解析**
  - 支持網頁內容提取
  - 自動爬取文字和圖片
  - 智能內容清理和格式化
  
- ✅ **PDF 支持**
  - PDF 文字內容提取
  - 多 PDF 文件合併分析
  
- ✅ **多源內容整合**
  - 同時處理多個不同類型的輸入
  - 支持：URL + PDF + 圖片 + 文字
  - 智能合併

#### PPT 模板支持
- ✅ **自定義模板系統**
  - 讀取現有 PPTX 作為模板
  - 提取母版樣式
  - 應用到生成的簡報
  
- ✅ **模板工具**
  - PPTX 轉 JSON 工具
  - 自動分析和生成模板
  - JSON 驅動的 Slide 類型定義
  
- ✅ **樣式自定義**
  - 自定義配色方案
  - 字體族選擇
  - 佈局參數調整

### 🎯 高優先級

#### 1. PDF 增強功能
- [ ] PDF 圖片提取和識別
- [ ] PDF 表格結構解析
- [ ] 更智能的內容分析

#### 2. PPT 文件解析
- [ ] 解析現有 PPT/PPTX 文件
- [ ] 提取文字和圖片
- [ ] 保留格式和結構信息

#### 3. 交互式大綱生成
- [ ] 在生成前顯示內容摘要
- [ ] AI 建議的主題和結構
- [ ] 用戶可編輯大綱
- [ ] 確認後再生成完整簡報

#### 4. 更多 Slide 類型
- [ ] 數據圖表頁（條形圖、餅圖、折線圖）
- [ ] 比較對照頁（左右對比）
- [ ] 流程圖頁（步驟流程）
- [ ] 團隊介紹頁
- [ ] SWOT 分析頁

### 🔧 中優先級

#### 5. AI 模型擴充
- ✅ Google Gemini（已支持）
- [ ] OpenAI GPT-4/GPT-4 Turbo
- [ ] Anthropic Claude
- [ ] 本地模型（Ollama）

#### 6. AI 圖片生成整合
- [ ] AI 識別需要配圖的內容
- [ ] DALL-E 3 整合
- [ ] Stable Diffusion 整合
- [ ] 圖片生成和管理

#### 7. 模板庫
- [ ] 內建多種專業模板
- [ ] 分類管理（商業、教育、創意等）
- [ ] 模板預覽功能

### 💡 低優先級

#### 8. 圖形化界面
- [ ] Web UI（Gradio/Streamlit）
- [ ] 拖放式操作
- [ ] 實時預覽

#### 9. 協作和分享
- [ ] 雲端整合（Google Drive、OneDrive）
- [ ] 分享鏈接
- [ ] 版本控制

#### 10. 性能優化
- [ ] AI 回應快取
- [ ] 批量並行處理
- [ ] 圖片壓縮

### 📊 進度追蹤

**當前版本：v2.0.0** 🎉

- ✅ 已完成：模板引擎、網頁爬取、PPTX 模板支持、多源輸入
- 🚧 進行中：文檔完善、模板庫建設
- 📅 計劃中：交互式大綱、更多 Slide 類型、多 AI 模型支持


## 📄 授權

本項目採用 MIT License - 詳見 [LICENSE](LICENSE) 文件

## 💬 聯繫方式

如有問題或建議，歡迎通過以下方式聯繫：

- 📧 Email: chanshunchih@gmail.com
- 💼 LinkedIn: [Chan Shun Chih](https://www.linkedin.com/in/chanshunchih/)
- 🐛 問題反饋：提交 Issue
- 💡 功能建議：開啟 Discussion

---

<div align="center">

**Made with ❤️ by John Chan**

**⭐ 如果這個項目對你有幫助，請給我一個 Star！**

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/auto-ppt&type=Date)](https://star-history.com/#yourusername/auto-ppt&Date)

</div>
