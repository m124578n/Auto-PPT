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
- 保持一致的樣式和佈局

### 🏗️ 高度可擴展
- **Strategy Pattern**：每個 Slide 類型獨立實現
- **Registry Pattern**：自動註冊和管理
- **零配置擴展**：添加新類型無需修改現有代碼
- **自動化 AI Prompt**：JSON Schema 和類型說明自動生成

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
- 動態字體大小調整
- 防止內容溢出（防跑版）
- 換行符智能處理

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

#### 1. AI 生成簡報

```bash
python ai_html_to_ppt.py
```

這會：
1. 使用 AI 分析 `TEXT_CONTENT` 和圖片
2. 生成簡報結構（JSON）
3. 輸出 HTML 文件供預覽
4. 保存數據文件供後續使用

#### 2. 轉換為 PPTX

```bash
python convert_html_to_pptx.py
```

這會讀取 HTML 文件並生成對應的 PPTX 文件。

## 📖 詳細使用

### 準備素材

#### 1. 準備文字內容

編輯 `ai_html_to_ppt.py` 中的 `TEXT_CONTENT`：

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

設置 `USE_IMAGES = True` 啟用圖片功能。

### 自定義配置

#### 修改 AI 生成參數

在 `ai_html_to_ppt.py` 中：

```python
# 要求部分可自定義
**要求**：
1. 自動分析內容，識別2-4個主題
2. 每個主題有章節分隔頁
3. 合理安排圖片（如有）
4. 總共10-15張幻燈片
```

#### 調整樣式

修改 `slide_types.py` 中各個 Slide 類型的：
- 字體大小
- 顏色
- 位置和尺寸
- 間距

## 🏗️ 架構設計

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

#### 1. 自動化 AI Prompt

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

#### 2. 統一的處理流程

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

## 🔧 擴展指南

### 添加新的 Slide 類型

只需 4 步，無需修改任何現有代碼！

#### 步驟 1：創建新類

```python
# slide_types.py 或獨立文件
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
from slide_types import SlideTypeRegistry

print('可用的 Slide 類型：')
for slide_type in SlideTypeRegistry.all_types():
    slide_class = SlideTypeRegistry.get(slide_type)
    print(f'  - {slide_type}: {slide_class.get_description()}')
"
```

## 📊 項目結構

```
auto-ppt/
├── ai_html_to_ppt.py           # AI 生成簡報主程式
├── convert_html_to_pptx.py     # HTML 轉 PPTX 工具
├── slide_types.py              # Slide 類型定義（核心）
├── slide_generator.py          # HTML/PPTX 生成器
├── example_new_slide_type.py   # 擴展示例
├── test_refactored.py          # 單元測試
├── downloaded_images/          # 圖片資源目錄
├── cursor_agent_md/            # 詳細文檔
│   ├── EXTENSIBILITY_GUIDE.md  # 擴展指南
│   └── ...
├── old_py/                     # 原始代碼（已重構）
├── .env                        # API Key 配置
├── pyproject.toml              # 項目配置
└── README.md                   # 本文件
```

## 📚 示例

### 示例 1：旅遊行程簡報

**輸入文字：**
```
探索日本北陸的自然奇觀與文化精粹

行程特色：
- 世界遺產白川鄉合掌村
- 日本三大名園之一的兼六園
- 立山黑部阿爾卑斯山路線
...
```

**輸入圖片：**
```
downloaded_images/
├── 白川鄉.jpg
├── 兼六園.jpg
├── 立山黑部.jpg
```

**生成結果：**
- 📄 HTML 文件：可交互預覽
- 📊 PPTX 文件：完整 PowerPoint
- 10-15 張精美幻燈片
- 自動安排圖片和文字佈局

### 示例 2：產品介紹

**輸入文字：**
```
智能手錶 X1 產品介紹

主要功能：
- 全天候健康監測
- 50米防水設計
- 超長續航 14 天
...
```

**生成結果：**
- 開場頁（產品名稱）
- 功能介紹（文字列表）
- 圖片展示（產品照片）
- 規格對比（兩欄對比）
- 結尾頁（購買信息）

## 🧪 測試

運行單元測試：

```bash
python test_refactored.py
```

測試覆蓋：
- ✅ Slide 類型註冊
- ✅ HTML 生成
- ✅ PPTX 生成
- ✅ JSON 示例收集
- ✅ 類型說明收集

## 🎨 樣式定製

### 修改顏色

在 `slide_types.py` 中：

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

A: 在 `ai_html_to_ppt.py` 的 prompt 中修改：
```python
**要求**：
4. 總共10-15張幻燈片  # 修改這裡
```

### Q: 能否使用其他 AI 模型？

A: 可以！只需修改 `ai_html_to_ppt.py` 中的 `model` 參數，或替換整個 AI 調用部分。

### Q: 如何貢獻新的 Slide 類型？

A: 
1. Fork 本倉庫
2. 創建新的 Slide 類型（參考擴展指南）
3. 添加測試
4. 提交 Pull Request

### Q: 支持中文以外的語言嗎？

A: 完全支持！只需在文字內容中使用相應語言即可。

## 📖 詳細文檔

更多詳細信息，請查看：

- [擴展指南](cursor_agent_md/EXTENSIBILITY_GUIDE.md) - 如何添加新的 Slide 類型
- [JSON Schema 提取](cursor_agent_md/JSON_SCHEMA_EXTRACTION_SUMMARY.md) - 自動化機制詳解
- [架構設計](cursor_agent_md/README_ARCHITECTURE.md) - 設計模式和原理
- [佈局優化](cursor_agent_md/LAYOUT_FIX_SUMMARY.md) - 防跑版技術

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

## 📝 更新日誌

### v1.0.0 (2025-10-17)

#### 核心功能
- ✅ AI 驅動的智能簡報生成
- ✅ 支持 HTML 和 PPTX 雙格式輸出
- ✅ 6 種標準 Slide 類型
- ✅ 2 種擴展示例類型

#### 架構優化
- ✅ 重構為 Strategy Pattern + Registry Pattern
- ✅ JSON Schema 自動提取和生成
- ✅ 類型說明自動收集
- ✅ AI Prompt 完全動態生成

#### 佈局優化
- ✅ 圖片自動保持寬高比
- ✅ 圖文智能對齊
- ✅ 動態字體大小調整
- ✅ 防跑版技術
- ✅ 換行符智能處理

#### 開發體驗
- ✅ 零配置擴展新類型
- ✅ 完整的單元測試
- ✅ 詳細的文檔和示例

## 🌟 特別鳴謝

- [Google Gemini](https://ai.google.dev/) - AI 能力支持
- [python-pptx](https://python-pptx.readthedocs.io/) - PPTX 生成庫
- [Pillow](https://pillow.readthedocs.io/) - 圖片處理庫

## 📄 License

本項目採用 MIT License - 詳見 [LICENSE](LICENSE) 文件

## 💬 聯繫方式

- 項目地址：[GitHub Repository]
- 問題反饋：[Issues]
- 討論區：[Discussions]

---

**Made with ❤️ by Auto-PPT Team**

**⭐ 如果這個項目對你有幫助，請給我們一個 Star！**
