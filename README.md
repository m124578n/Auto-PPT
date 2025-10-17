# 🎨 Auto-PPT

> AI 驅動的智能簡報生成器 - 從文字和圖片自動生成精美的 HTML 和 PPTX 演示文稿

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-black.svg)](https://github.com/psf/black)

## ✨ 功能特點

### 🤖 AI 智能生成
- 使用 Google Gemini AI 自動分析內容
- 智能識別主題並組織簡報結構
- 自動安排圖片和文字佈局
- 生成專業的演示文稿

### 🎯 多格式輸出
- **HTML 預覽**：可在瀏覽器中交互預覽
- **PPTX 匯出**：完整的 PowerPoint 文件
- **JSON 數據**：結構化數據供後續處理
- 保持一致的樣式和佈局

### 🏗️ 高度可擴展
- **Strategy Pattern**：每個 Slide 類型獨立實現
- **Registry Pattern**：自動註冊和管理
- **零配置擴展**：添加新類型無需修改現有代碼
- **自動化 AI Prompt**：JSON Schema 和類型說明自動生成
- **模塊化架構**：清晰的包結構，易於維護

### 🎨 豐富的 Slide 類型

#### 標準類型
- **Opening** 開場頁 - 漸層背景，適合標題頁
- **Section Divider** 章節分隔頁 - 藍色背景，分隔主題
- **Text Content** 純文字內容頁 - 項目符號列表
- **Image with Text** 圖文混合頁 - 左圖右文或上圖下文
- **Full Image** 大圖展示頁 - 大幅圖片配說明
- **Closing** 結尾頁 - 漸層背景，感謝頁面

#### 自定義擴展
- **Two Column Text** 兩欄文字對比頁
- **Quote Card** 引用卡片頁
- **輕鬆添加更多...**

### 📐 智能佈局
- 圖片自動保持寬高比
- 文字和圖片頂部對齊
- 動態字體大小調整（防止內容溢出）
- 箭頭符號大小固定（視覺統一）
- 換行符智能處理
- 自動文件管理（隨機前綴 + 輸出目錄）

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

3. **配置 API Key**

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
1. 使用 AI 分析 `TEXT_CONTENT` 和圖片（或 PDF）
2. 生成簡報結構（JSON）
3. 自動生成 HTML 文件供預覽
4. **自動生成 PPTX 文件** ✨
5. 所有文件保存到 `output/` 目錄

**輸出文件：**
```
output/
├── 123456_簡報主題_presentation.html
├── 123456_簡報主題_data.json
└── 123456_簡報主題.pptx
```

#### 方式 2：使用 AutoPPT 類（推薦）

```python
from AutoPPT import AutoPPT
import os

# 初始化
auto_ppt = AutoPPT(
    api_key=os.getenv("GEMINI_API_KEY"),
    use_images=False,  # 是否使用圖片
    save_dir="output"  # 輸出目錄
)

# 一鍵生成 HTML + JSON + PPTX
data = auto_ppt.generate(
    text_content="你的簡報內容...",
    pdf_file="報告.pdf",  # 可選：PDF 文件路徑
    save_files=True  # 自動保存所有格式
)
```

#### 方式 3：使用快速示例

```bash
python quick_example.py
```

查看 `quick_example.py` 獲取更多示例。

#### 方式 4：轉換現有 JSON 為 PPTX

```python
from AutoPPT.slide_generator import PPTXGenerator
import json

# 載入 JSON 數據
with open("output/123456_簡報主題_data.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# 生成 PPTX
pptx_gen = PPTXGenerator({})
prs = pptx_gen.generate_from_data(data)
prs.save("新簡報.pptx")
```

## 📖 詳細使用

### 準備素材

#### 1. 準備文字內容

編輯 `main.py` 中的 `TEXT_CONTENT`：

```python
TEXT_CONTENT = """
探索日本北陸的自然奇觀與文化精粹

行程特色：
1. 世界遺產白川鄉合掌村
2. 日本三大名園之一的兼六園
3. 立山黑部阿爾卑斯山路線
...
"""
```

#### 2. 準備圖片（可選）

將圖片放入 `downloaded_images/` 目錄：
```
downloaded_images/
├── 001.jpg
├── 002.jpg
└── ...
```

在 `main.py` 中設置 `USE_IMAGES = True` 啟用圖片功能。

#### 3. 準備 PDF（可選）

將 PDF 文件放在項目根目錄，AI 會自動分析內容。

### 自定義配置

#### 修改輸出目錄

```python
auto_ppt = AutoPPT(
    api_key=API_KEY,
    save_dir="my_presentations"  # 自定義輸出目錄
)
```

#### 修改 AI 生成參數

在 `AutoPPT/auto_ppt.py` 的 `generate_prompt` 方法中：

```python
**要求**：
1. 自動分析內容，識別2-4個主題
2. 每個主題有章節分隔頁
3. 合理安排圖片（如有）
4. 總共10-15張幻燈片  # 可自定義頁數
```

#### 調整樣式

修改 `AutoPPT/slide_types.py` 中各個 Slide 類型的：
- 字體大小
- 顏色
- 位置和尺寸
- 間距

## 🏗️ 架構設計

### 項目結構

```
auto-ppt/
├── AutoPPT/                        # 核心包
│   ├── __init__.py                # 包初始化（匯出 AutoPPT）
│   ├── auto_ppt.py                # AutoPPT 主類
│   ├── slide_types.py             # Slide 類型定義（核心）
│   ├── slide_generator.py         # HTML/PPTX 生成器
│   ├── convert_html_to_pptx.py    # 轉換工具
│   ├── example_new_slide_type.py  # 擴展示例
│   └── test_refactored.py         # 單元測試
├── main.py                        # 主入口程序
├── quick_example.py               # 快速示例
├── output/                        # 生成的文件
│   ├── 123456_主題_presentation.html
│   ├── 123456_主題_data.json
│   └── 123456_主題.pptx
├── downloaded_images/             # 圖片資源目錄
├── old_py/                        # 原始代碼（已重構）
├── cursor_agent_md/               # 詳細文檔
│   ├── AUTO_PPT_CLASS.md         # AutoPPT 類說明
│   ├── USAGE_EXAMPLES.md         # 使用示例
│   ├── BULLET_ARROW_FIX.md       # 箭頭符號修復說明
│   └── ...
├── .env                           # API Key 配置
├── pyproject.toml                 # 項目配置
├── QUICKSTART.md                  # 快速開始指南
└── README.md                      # 本文件
```

### 核心設計模式

```
┌─────────────────────────────────────────────────┐
│           SlideTypeRegistry (註冊表)            │
│  - 管理所有 Slide 類型                         │
│  - 自動收集 JSON 示例和類型說明                │
└─────────────────┬───────────────────────────────┘
                  │
                  ├─────────────────────────────────┐
                  ↓                                 ↓
         ┌─────────────────┐            ┌──────────────────┐
         │   SlideType     │            │   HTMLGenerator  │
         │   (抽象基類)     │            │   PPTXGenerator  │
         └────────┬────────┘            └──────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ↓             ↓              ↓
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Opening  │ │ Section  │ │  Text    │  ... 6+ 個類型
│  Slide   │ │  Slide   │ │ Content  │
└──────────┘ └──────────┘ └──────────┘
```

### 關鍵特性

#### 1. AutoPPT 類（核心 API）

```python
class AutoPPT:
    """AI 驅動的自動簡報生成器"""
    
    def __init__(self, api_key, use_images=False, save_dir="output"):
        """初始化"""
    
    def load_images(self, image_dir="downloaded_images"):
        """載入圖片資源"""
    
    def generate_prompt(self, text_content):
        """生成 AI Prompt（自動包含所有 Slide 類型）"""
    
    def generate_presentation(self, text_content, pdf_file=None, model="gemini-2.5-flash"):
        """使用 AI 生成簡報結構"""
    
    def save_html(self, data, filename=None):
        """保存 HTML 文件"""
    
    def save_json(self, data, filename=None):
        """保存 JSON 數據文件"""
    
    def save_pptx(self, data, filename=None):
        """保存 PPTX 文件"""
    
    def generate(self, text_content, pdf_file=None, save_files=True):
        """完整的生成流程（一鍵生成）"""
```

#### 2. 自動化 AI Prompt

```python
# 每個 Slide 類型定義自己的信息
@SlideTypeRegistry.register('opening')
class OpeningSlide(SlideType):
    
    @classmethod
    def get_json_example(cls):
        return {"slide_type": "opening", "title": "...", ...}
    
    @classmethod
    def get_description(cls):
        return "開場頁（漸層背景）"
    
    def generate_html(self): ...
    def generate_pptx(self, prs): ...
```

系統自動：
- ✅ 收集所有類型的 JSON 示例
- ✅ 收集所有類型的說明文字
- ✅ 動態生成 AI Prompt
- ✅ 無需手動維護配置

#### 3. 統一的處理流程

```python
# HTMLGenerator
for slide_data in slides:
    slide_type = slide_data['slide_type']
    slide_class = SlideTypeRegistry.get(slide_type)
    html += slide_class(slide_data, context).generate_html()

# PPTXGenerator
for slide_data in slides:
    slide_type = slide_data['slide_type']
    slide_class = SlideTypeRegistry.get(slide_type)
    slide_class(slide_data, context).generate_pptx(prs)
```

#### 4. 智能文件管理

- 自動生成 6 位隨機前綴（避免文件名衝突）
- 統一輸出到 `output/` 目錄
- 文件命名格式：`123456_主題_類型.ext`

## 🔧 擴展指南

### 添加新的 Slide 類型

只需 4 步，無需修改任何現有代碼！

#### 步驟 1：創建新類

在 `AutoPPT/slide_types.py` 或獨立文件中：

```python
from AutoPPT.slide_types import SlideType, SlideTypeRegistry

@SlideTypeRegistry.register('timeline')
class TimelineSlide(SlideType):
    """時間軸頁"""
    
    @classmethod
    def get_json_example(cls):
        return {
            "slide_type": "timeline",
            "title": "發展歷程",
            "events": [
                {"year": "2020", "description": "成立"},
                {"year": "2021", "description": "擴張"}
            ]
        }
    
    @classmethod
    def get_description(cls):
        return "時間軸頁（展示時間線上的重要事件）"
    
    def generate_html(self):
        title = self.data.get('title', '')
        events = self.data.get('events', [])
        
        events_html = ""
        for event in events:
            events_html += f"""
                <div class="event">
                    <h3>{event['year']}</h3>
                    <p>{event['description']}</p>
                </div>
            """
        
        return f"""
        <div class="slide slide-timeline">
            <h2>{title}</h2>
            <div class="timeline">{events_html}</div>
        </div>
        """
    
    def generate_pptx(self, prs):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # 添加標題
        title = self.data.get('title', '')
        # ... 實現 PPTX 佈局
        
        return slide
```

#### 步驟 2：就這樣！

- ✅ 類型自動註冊
- ✅ AI Prompt 自動更新
- ✅ JSON 示例自動包含
- ✅ 類型說明自動包含
- ✅ HTML/PPTX 生成自動支持

AI 會自動學會使用你的新類型！

### 查看所有可用類型

```bash
python -c "
from AutoPPT.slide_types import SlideTypeRegistry

print('可用的 Slide 類型：')
for slide_type in SlideTypeRegistry.all_types():
    slide_class = SlideTypeRegistry.get(slide_type)
    print(f'  - {slide_type}: {slide_class.get_description()}')
"
```

### 擴展示例

查看 `AutoPPT/example_new_slide_type.py` 獲取完整的擴展示例：
- TwoColumnTextSlide（兩欄文字）
- QuoteCardSlide（引用卡片）

## 📚 使用示例

### 示例 1：旅遊行程簡報

**輸入文字：**
```python
TEXT_CONTENT = """
探索日本北陸的自然奇觀與文化精粹

行程特色：
- 世界遺產白川鄉合掌村
- 日本三大名園之一的兼六園
- 立山黑部阿爾卑斯山路線
"""
```

**輸入圖片：**
```
downloaded_images/
├── 白川鄉.jpg
├── 兼六園.jpg
├── 立山黑部.jpg
```

**生成結果：**
```
output/
├── 123456_探索日本北陸_presentation.html
├── 123456_探索日本北陸_data.json
└── 123456_探索日本北陸.pptx
```

### 示例 2：產品介紹

```python
from AutoPPT import AutoPPT
import os

auto_ppt = AutoPPT(api_key=os.getenv("GEMINI_API_KEY"))

data = auto_ppt.generate(
    text_content="""
智能手錶 X1 產品介紹

主要功能：
- 全天候健康監測
- 50米防水設計
- 超長續航 14 天
    """,
    save_files=True
)
```

### 示例 3：從 PDF 生成

```python
from AutoPPT import AutoPPT
import os

auto_ppt = AutoPPT(api_key=os.getenv("GEMINI_API_KEY"))

data = auto_ppt.generate(
    text_content="請根據 PDF 內容生成簡報",
    pdf_file="投資月報_20250930.pdf",
    save_files=True
)
```

### 示例 4：批量生成

```python
from AutoPPT import AutoPPT
import os

auto_ppt = AutoPPT(api_key=os.getenv("GEMINI_API_KEY"))

topics = ["產品介紹", "市場分析", "財務報告"]

for topic in topics:
    data = auto_ppt.generate(
        text_content=f"{topic}\n\n相關內容...",
        save_files=True
    )
    print(f"✅ {topic} 生成完成")
```

## 🧪 測試

運行單元測試：

```bash
cd AutoPPT
python test_refactored.py
```

測試覆蓋：
- ✅ Slide 類型註冊
- ✅ HTML 生成
- ✅ PPTX 生成
- ✅ JSON 示例收集
- ✅ 類型說明收集
- ✅ AutoPPT 類方法

## 🎨 樣式定製

### 修改顏色

在 `AutoPPT/slide_types.py` 中：

```python
# 開場頁背景色
bg.fill.fore_color.rgb = RGBColor(110, 114, 198)  # 紫色

# 章節頁背景色
bg.fill.fore_color.rgb = RGBColor(57, 112, 161)   # 藍色

# 文字顏色
p.font.color.rgb = RGBColor(44, 62, 80)  # 深灰
```

### 修改字體大小

```python
# 標題
p.font.size = Pt(36)  # 36 點

# 正文
p.font.size = Pt(20)  # 20 點

# 箭頭符號（固定大小）
run_bullet.font.size = Pt(26)  # 主要項目
run_bullet.font.size = Pt(20)  # 次要項目
```

### 修改佈局

```python
# 文字框位置和尺寸
text_box = slide.shapes.add_textbox(
    Inches(1),      # 左邊距
    Inches(2),      # 上邊距
    Inches(8),      # 寬度
    Inches(4)       # 高度
)
```

## 🔍 常見問題

### Q: 如何獲取 Gemini API Key？

A: 訪問 [Google AI Studio](https://aistudio.google.com/apikey) 並創建 API Key。

### Q: 圖片格式有要求嗎？

A: 支持常見格式：JPG, PNG, GIF, WEBP。建議使用高質量圖片以獲得最佳效果。

### Q: 如何控制簡報的頁數？

A: 在 `AutoPPT/auto_ppt.py` 的 `generate_prompt` 方法中修改：
```python
**要求**：
4. 總共10-15張幻燈片  # 修改這裡
```

### Q: 如何修改輸出目錄？

A: 在初始化 AutoPPT 時指定：
```python
auto_ppt = AutoPPT(
    api_key=API_KEY,
    save_dir="my_output"  # 自定義目錄
)
```

### Q: 文件名前綴是怎麼生成的？

A: 自動生成 6 位隨機數字（100000-999999），避免文件名衝突。

### Q: 能否使用其他 AI 模型？

A: 可以！修改 `generate_presentation` 方法的 `model` 參數：
```python
data = auto_ppt.generate_presentation(
    text_content="...",
    model="gemini-2.0-flash-exp"  # 不同模型
)
```

### Q: 如何貢獻新的 Slide 類型？

A: 
1. Fork 本倉庫
2. 在 `AutoPPT/slide_types.py` 中創建新類型
3. 添加測試
4. 提交 Pull Request

### Q: 支持中文以外的語言嗎？

A: 完全支持！只需在文字內容中使用相應語言即可。

### Q: 箭頭符號大小問題？

A: 已修復！箭頭符號現在使用固定大小（26pt/20pt），不會隨文字大小變化。詳見 `cursor_agent_md/BULLET_ARROW_FIX.md`。

## 📖 詳細文檔

更多詳細信息，請查看 `cursor_agent_md/` 目錄：

- [AUTO_PPT_CLASS.md](cursor_agent_md/AUTO_PPT_CLASS.md) - AutoPPT 類完整說明
- [USAGE_EXAMPLES.md](cursor_agent_md/USAGE_EXAMPLES.md) - 詳細使用示例
- [BULLET_ARROW_FIX.md](cursor_agent_md/BULLET_ARROW_FIX.md) - 箭頭符號修復說明
- [EXTENSIBILITY_GUIDE.md](cursor_agent_md/EXTENSIBILITY_GUIDE.md) - 擴展指南
- [JSON_SCHEMA_EXTRACTION_SUMMARY.md](cursor_agent_md/JSON_SCHEMA_EXTRACTION_SUMMARY.md) - 自動化機制詳解

## 🤝 貢獻

歡迎貢獻！請：

1. Fork 本倉庫
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 貢獻指南

- 遵循現有代碼風格
- 為新功能添加測試
- 更新相關文檔
- 確保所有測試通過
- 新的 Slide 類型需包含 `get_json_example` 和 `get_description` 方法

## 📝 更新日誌

### v1.2.0 (2025-10-17)

#### 項目結構重構
- ✅ 重構為 Python 包結構（`AutoPPT/` 包）
- ✅ 統一入口：`main.py`
- ✅ 清晰的模塊化架構
- ✅ 改進的導入方式

#### 文件管理優化
- ✅ 自動輸出到 `output/` 目錄
- ✅ 隨機前綴避免文件衝突
- ✅ 統一的文件命名規範

#### Bug 修復
- ✅ 修復箭頭符號大小問題（固定 26pt/20pt）
- ✅ 使用 Run 對象分別控制箭頭和文字
- ✅ 提高視覺一致性

### v1.1.0 (2025-10-17)

#### 核心功能
- ✅ AutoPPT 類封裝
- ✅ 一鍵生成 HTML + JSON + PPTX
- ✅ 支持 PDF 輸入

### v1.0.0 (2025-10-17)

#### 核心功能
- ✅ AI 驅動的智能簡報生成
- ✅ 支持 HTML 和 PPTX 雙格式輸出
- ✅ 6 種標準 Slide 類型
- ✅ 2 種擴展示例類型

#### 架構優化
- ✅ Strategy Pattern + Registry Pattern
- ✅ JSON Schema 自動提取和生成
- ✅ 類型說明自動收集
- ✅ AI Prompt 完全動態生成

#### 佈局優化
- ✅ 圖片自動保持寬高比
- ✅ 圖文智能對齊
- ✅ 動態字體大小調整
- ✅ 防跑版技術
- ✅ 換行符智能處理

## 🌟 特別鳴謝

- [Google Gemini](https://ai.google.dev/) - AI 能力支持
- [python-pptx](https://python-pptx.readthedocs.io/) - PPTX 生成庫
- [Pillow](https://pillow.readthedocs.io/) - 圖片處理庫

## 📋 TODO 路線圖

以下是計劃中的功能和改進，按優先級排列：

### 🎯 高優先級

#### 1. 多輸入源支持
- [ ] **URL 鏈接解析**
  - 支持網頁內容提取
  - 自動爬取文字和圖片
  - 智能內容清理和格式化
  
- [ ] **PDF 增強功能**
  - ✅ 已支持：PDF 文字內容提取
  - [ ] PDF 圖片提取和識別
  - [ ] PDF 表格結構解析
  - [ ] 多 PDF 文件合併分析
  
- [ ] **PPT 文件解析**
  - [ ] 解析現有 PPT/PPTX 文件
  - [ ] 提取文字內容
  - [ ] 分離圖片資源
  - [ ] 保留格式和結構信息
  
- [ ] **多源內容整合**
  - [ ] 同時處理多個不同類型的輸入
  - [ ] 支持：URL + PDF + PPT + 文字
  - [ ] 智能合併和去重
  - [ ] 內容優先級設定

#### 2. 交互式大綱生成
- [ ] **內容分析預覽**
  - [ ] 在生成 JSON 前顯示內容摘要
  - [ ] AI 建議的主題和結構
  - [ ] 預估幻燈片數量
  
- [ ] **用戶自定義選項**
  - [ ] 選擇簡報主題（商業/教育/產品/報告等）
  - [ ] 設定目標對象（管理層/技術人員/客戶等）
  - [ ] 調整簡報風格（正式/活潑/專業等）
  - [ ] 指定頁數範圍
  
- [ ] **大綱編輯和確認**
  - [ ] 顯示生成的大綱結構
  - [ ] 允許用戶調整章節順序
  - [ ] 添加/刪除/合併章節
  - [ ] 確認後再生成完整 JSON

#### 3. Slide 樣式擴充
- [ ] **新增標準類型**
  - [ ] 數據圖表頁（支持條形圖、餅圖、折線圖）
  - [ ] 比較對照頁（左右對比、優缺點）
  - [ ] 流程圖頁（步驟流程、時間軸）
  - [ ] 團隊介紹頁（成員卡片）
  - [ ] 聯繫方式頁（QR Code、社交媒體）
  
- [ ] **進階類型**
  - [ ] 互動式問答頁
  - [ ] 影片嵌入頁
  - [ ] 3D 圖表頁
  - [ ] 動畫效果頁
  
- [ ] **行業特定類型**
  - [ ] 財務報表頁
  - [ ] 產品規格頁
  - [ ] 路線圖頁
  - [ ] SWOT 分析頁

### 🔧 中優先級

#### 4. PPT 模板支持
- [ ] **自定義模板導入**
  - [ ] 讀取現有 PPTX 作為模板
  - [ ] 提取母版樣式
  - [ ] 應用到生成的簡報
  
- [ ] **模板庫**
  - [ ] 內建多種專業模板
  - [ ] 分類管理（商業、教育、創意等）
  - [ ] 模板預覽功能
  - [ ] 一鍵切換模板
  
- [ ] **樣式自定義**
  - [ ] 自定義配色方案
  - [ ] 字體族選擇
  - [ ] 佈局參數調整
  - [ ] 保存為自定義模板

#### 5. AI 模型擴充
- [ ] **多 AI 後端支持**
  - ✅ 已支持：Google Gemini
  - [ ] OpenAI GPT-4/GPT-4 Turbo
  - [ ] Anthropic Claude
  - [ ] Azure OpenAI
  - [ ] 本地模型（Ollama、LM Studio）
  
- [ ] **模型切換機制**
  - [ ] 統一的 AI 接口抽象
  - [ ] 配置文件管理多個 API Key
  - [ ] 自動 fallback 機制
  - [ ] 成本和性能對比
  
- [ ] **專用模型優化**
  - [ ] 針對不同任務使用最適合的模型
  - [ ] 內容分析用 Model A
  - [ ] 圖片生成用 Model B
  - [ ] 成本優化策略

#### 6. AI 圖片生成整合
- [ ] **圖片需求檢測**
  - [ ] AI 識別需要配圖的內容
  - [ ] 自動生成圖片描述（prompt）
  - [ ] 用戶確認或修改 prompt
  
- [ ] **圖片生成 API 整合**
  - [ ] DALL-E 3 整合
  - [ ] Midjourney API
  - [ ] Stable Diffusion
  - [ ] 其他圖片生成服務
  
- [ ] **圖片管理**
  - [ ] 生成圖片的本地緩存
  - [ ] 圖片質量檢查
  - [ ] 替代圖片建議
  - [ ] 圖片授權信息追蹤

### 💡 低優先級

#### 7. 協作和分享
- [ ] **團隊協作**
  - [ ] 多用戶編輯
  - [ ] 版本控制
  - [ ] 評論和建議功能
  
- [ ] **雲端整合**
  - [ ] Google Drive 整合
  - [ ] OneDrive 整合
  - [ ] 直接上傳到雲端
  
- [ ] **分享功能**
  - [ ] 生成分享鏈接
  - [ ] 嵌入式預覽
  - [ ] 權限管理

#### 8. 性能和優化
- [ ] **快取機制**
  - [ ] AI 回應快取
  - [ ] 圖片處理快取
  - [ ] 增量生成
  
- [ ] **批量處理**
  - [ ] 批量生成多個簡報
  - [ ] 並行處理
  - [ ] 進度追蹤
  
- [ ] **資源優化**
  - [ ] 圖片壓縮
  - [ ] 懶加載
  - [ ] 內存管理

#### 9. 用戶體驗
- [ ] **圖形化界面**
  - [ ] Web UI（Gradio/Streamlit）
  - [ ] 桌面應用（Electron）
  - [ ] 拖放式操作
  
- [ ] **實時預覽**
  - [ ] 即時渲染預覽
  - [ ] 修改即時更新
  - [ ] 雙屏對比
  
- [ ] **多語言支持**
  - [ ] 界面多語言
  - [ ] 內容翻譯
  - [ ] 本地化模板

### 📊 進度追蹤

當前版本：**v1.2.0**

- ✅ 已完成：核心功能、6種標準Slide類型、AI自動生成、HTML/PPTX輸出
- 🚧 進行中：箭頭符號優化、佈局調整、文檔完善
- 📅 計劃中：上述 TODO 項目


## 📄 License

本項目採用 MIT License - 詳見 [LICENSE](LICENSE) 文件

## 💬 聯繫方式

- 項目地址：[GitHub Repository]
- 問題反饋：[Issues]
- 討論區：[Discussions]

---

**Made with ❤️ by 智造業 john**

**⭐ 如果這個項目對你有幫助，請給我們一個 Star！**
