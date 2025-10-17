# 架構說明與擴展指南

## 🏗️ 架構設計

### 設計模式
1. **Strategy Pattern（策略模式）**：每種 slide 類型是一個獨立的策略
2. **Registry Pattern（註冊模式）**：自動註冊所有 slide 類型
3. **Template Method Pattern（模板方法模式）**：定義統一的 slide 處理流程

### 核心模組

```
auto-ppt/
├── slide_types.py          # Slide 類型定義（核心）
├── slide_generator.py      # HTML 和 PPTX 生成器
├── ai_html_to_ppt.py       # AI 生成簡報主程序
├── convert_html_to_pptx.py # 轉換器主程序
└── README_ARCHITECTURE.md  # 本文件
```

### 模組職責

#### 1. `slide_types.py`
- **SlideTypeRegistry**：Slide 類型註冊表
- **SlideType**：抽象基類，定義 slide 的統一介面
- **具體 Slide 類型**：OpeningSlide, SectionSlide, TextContentSlide 等

#### 2. `slide_generator.py`
- **HTMLGenerator**：從 JSON 數據生成 HTML
- **PPTXGenerator**：從 JSON 數據生成 PPTX
- **HTMLToPPTXParser**：解析 HTML 轉換為 PPTX（向後兼容）

#### 3. 主程序
- **ai_html_to_ppt.py**：使用 AI 分析內容並生成簡報
- **convert_html_to_pptx.py**：轉換 HTML/JSON 為 PPTX

---

## 🎯 如何新增 Slide 類型

### 步驟 1：創建新的 SlideType 類

在 `slide_types.py` 中添加新類：

```python
@SlideTypeRegistry.register('your_slide_type')
class YourSlideType(SlideType):
    """你的 slide 類型說明"""
    
    def generate_html(self) -> str:
        """生成 HTML 片段"""
        # 從 self.data 獲取數據
        title = self.data.get('title', '')
        content = self.data.get('content', '')
        
        return f"""
        <div class="slide slide-your-type">
            <div class="slide-content">
                <h2>{title}</h2>
                <p>{content}</p>
            </div>
        </div>
        """
    
    def generate_pptx(self, prs: Presentation) -> Slide:
        """生成 PPTX slide"""
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # 添加標題
        title = self.data.get('title', '')
        if title:
            title_box = slide.shapes.add_textbox(
                Inches(1), Inches(1), Inches(8), Inches(1)
            )
            title_frame = title_box.text_frame
            title_frame.text = title
            title_frame.paragraphs[0].font.size = Pt(32)
        
        # 添加內容
        content = self.data.get('content', '')
        if content:
            content_box = slide.shapes.add_textbox(
                Inches(1), Inches(2.5), Inches(8), Inches(4)
            )
            content_frame = content_box.text_frame
            content_frame.text = content
        
        return slide
```

### 步驟 2：定義 JSON Schema

在 AI Prompt 中添加新類型的說明：

```json
{
  "slide_type": "your_slide_type",
  "title": "標題",
  "content": "內容"
}
```

### 步驟 3：更新 CSS（如果需要）

在 `slide_generator.py` 的 `_build_full_html` 方法中添加 CSS：

```css
/* 你的 slide 類型樣式 */
.slide-your-type {
    background: #f0f0f0;
}

.slide-your-type .slide-content {
    padding: 60px;
}
```

### 步驟 4：測試

```python
# 創建測試數據
test_data = {
    'slides': [
        {
            'slide_type': 'your_slide_type',
            'title': '測試標題',
            'content': '測試內容'
        }
    ]
}

# 生成 HTML
from slide_generator import HTMLGenerator
html_gen = HTMLGenerator()
html = html_gen.generate_from_data(test_data)

# 生成 PPTX
from slide_generator import PPTXGenerator
pptx_gen = PPTXGenerator()
prs = pptx_gen.generate_from_data(test_data)
pptx_gen.save('test.pptx')
```

---

## 📊 現有 Slide 類型

### 1. Opening Slide（開場頁）
```json
{
  "slide_type": "opening",
  "title": "主標題",
  "subtitle": "副標題"
}
```

### 2. Section Divider（章節分隔頁）
```json
{
  "slide_type": "section_divider",
  "section_title": "章節名稱"
}
```

### 3. Text Content（純文字內容頁）
```json
{
  "slide_type": "text_content",
  "title": "頁面標題",
  "bullets": ["要點1", "要點2", "要點3"],
  "indent_levels": [0, 0, 1]
}
```

### 4. Image with Text（圖文混合頁）
```json
{
  "slide_type": "image_with_text",
  "title": "標題",
  "image_id": "img_01",
  "text": "說明文字",
  "layout": "horizontal"  // or "vertical"
}
```

### 5. Full Image（大圖展示頁）
```json
{
  "slide_type": "full_image",
  "title": "標題",
  "image_id": "img_02",
  "caption": "圖片說明"
}
```

### 6. Closing Slide（結尾頁）
```json
{
  "slide_type": "closing",
  "closing_text": "謝謝觀看",
  "subtext": "期待與您同行"
}
```

---

## 🔧 擴展範例

### 範例 1：創建「兩欄文字」Slide

```python
@SlideTypeRegistry.register('two_column_text')
class TwoColumnTextSlide(SlideType):
    """兩欄文字對比頁"""
    
    def generate_html(self) -> str:
        title = self.data.get('title', '')
        left_content = self.data.get('left_content', '')
        right_content = self.data.get('right_content', '')
        
        return f"""
        <div class="slide slide-content">
            <div class="slide-content">
                <h2 class="slide-title">{title}</h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px;">
                    <div>
                        <h3>左欄</h3>
                        <p>{left_content}</p>
                    </div>
                    <div>
                        <h3>右欄</h3>
                        <p>{right_content}</p>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def generate_pptx(self, prs: Presentation) -> Slide:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # 標題
        title = self.data.get('title', '')
        if title:
            title_box = slide.shapes.add_textbox(
                Inches(0.6), Inches(0.6), Inches(8.8), Inches(0.8)
            )
            title_frame = title_box.text_frame
            title_frame.text = title
            title_frame.paragraphs[0].font.size = Pt(38)
            title_frame.paragraphs[0].font.bold = True
        
        # 左欄
        left_content = self.data.get('left_content', '')
        if left_content:
            left_box = slide.shapes.add_textbox(
                Inches(0.6), Inches(1.8), Inches(4.2), Inches(5)
            )
            left_frame = left_box.text_frame
            left_frame.text = left_content
            left_frame.word_wrap = True
        
        # 右欄
        right_content = self.data.get('right_content', '')
        if right_content:
            right_box = slide.shapes.add_textbox(
                Inches(5.2), Inches(1.8), Inches(4.2), Inches(5)
            )
            right_frame = right_box.text_frame
            right_frame.text = right_content
            right_frame.word_wrap = True
        
        return slide
```

### 範例 2：創建「時間軸」Slide

```python
@SlideTypeRegistry.register('timeline')
class TimelineSlide(SlideType):
    """時間軸頁"""
    
    def generate_html(self) -> str:
        title = self.data.get('title', '')
        events = self.data.get('events', [])
        
        events_html = ""
        for event in events:
            time = event.get('time', '')
            description = event.get('description', '')
            events_html += f"""
            <div class="timeline-item">
                <div class="timeline-time">{time}</div>
                <div class="timeline-description">{description}</div>
            </div>
            """
        
        return f"""
        <div class="slide slide-content">
            <div class="slide-content">
                <h2 class="slide-title">{title}</h2>
                <div class="timeline">
                    {events_html}
                </div>
            </div>
        </div>
        """
    
    def generate_pptx(self, prs: Presentation) -> Slide:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # 標題
        title = self.data.get('title', '')
        if title:
            title_box = slide.shapes.add_textbox(
                Inches(0.6), Inches(0.6), Inches(8.8), Inches(0.8)
            )
            title_frame = title_box.text_frame
            title_frame.text = title
            title_frame.paragraphs[0].font.size = Pt(38)
            title_frame.paragraphs[0].font.bold = True
        
        # 時間軸事件
        events = self.data.get('events', [])
        y_position = 1.8
        
        for event in events:
            time = event.get('time', '')
            description = event.get('description', '')
            
            # 時間點
            time_box = slide.shapes.add_textbox(
                Inches(1), Inches(y_position), Inches(2), Inches(0.5)
            )
            time_frame = time_box.text_frame
            time_frame.text = time
            time_frame.paragraphs[0].font.size = Pt(20)
            time_frame.paragraphs[0].font.bold = True
            
            # 描述
            desc_box = slide.shapes.add_textbox(
                Inches(3.5), Inches(y_position), Inches(5.5), Inches(0.8)
            )
            desc_frame = desc_box.text_frame
            desc_frame.text = description
            desc_frame.paragraphs[0].font.size = Pt(18)
            desc_frame.word_wrap = True
            
            y_position += 1.2
        
        return slide
```

---

## 🎨 設計原則

### 1. 單一職責原則
每個 SlideType 類只負責一種 slide 的渲染邏輯。

### 2. 開放封閉原則
對擴展開放（可以添加新的 slide 類型），對修改封閉（不需要修改現有代碼）。

### 3. 依賴倒置原則
高層模組（HTMLGenerator, PPTXGenerator）依賴於抽象（SlideType），不依賴於具體實現。

### 4. 統一介面
所有 slide 類型都實現相同的介面：
- `generate_html()` - 生成 HTML
- `generate_pptx()` - 生成 PPTX

---

## 📝 最佳實踐

### 1. 命名規範
- 類名：使用 PascalCase，例如 `TwoColumnTextSlide`
- slide_type：使用 snake_case，例如 `two_column_text`

### 2. 數據結構
在 `self.data` 中定義清晰的數據結構，並提供預設值：
```python
title = self.data.get('title', '')
content = self.data.get('content', '')
```

### 3. 錯誤處理
在處理圖片或外部資源時，添加錯誤處理：
```python
try:
    image_path = self._get_image_path(image_id)
    if image_path and os.path.exists(image_path):
        # 處理圖片
except Exception as e:
    print(f"⚠️ 處理失敗：{e}")
```

### 4. 響應式設計
在 HTML 中考慮不同螢幕尺寸：
```css
@media (max-width: 768px) {
    .slide-content {
        padding: 30px 40px;
    }
}
```

### 5. 可讀性
添加清晰的註釋和文檔字符串：
```python
def generate_html(self) -> str:
    """生成 HTML 片段
    
    Returns:
        完整的 slide HTML 字符串
    """
```

---

## 🚀 快速開始

### 1. 生成新簡報
```bash
python ai_html_to_ppt.py
```

### 2. 轉換為 PPTX
```bash
python convert_html_to_pptx.py
```

### 3. 查看已註冊的 slide 類型
```python
from slide_types import SlideTypeRegistry
print(SlideTypeRegistry.all_types())
```

---

## 💡 常見問題

### Q: 如何修改現有 slide 的樣式？
A: 修改對應的 SlideType 類中的 `generate_html()` 和 `generate_pptx()` 方法。

### Q: AI 不認識我的新 slide 類型怎麼辦？
A: 更新 AI prompt，添加新類型的 JSON schema 和使用說明。

### Q: 如何處理複雜的佈局？
A: 可以在 SlideType 類中添加輔助方法，或創建子類繼承現有類型。

### Q: 如何調試 slide 生成？
A: 添加 print 語句或使用 logging 模組：
```python
print(f"   ✓ 處理 {self.data.get('slide_type')} 類型")
```

---

## 📚 參考資源

- [python-pptx 文檔](https://python-pptx.readthedocs.io/)
- [設計模式](https://refactoring.guru/design-patterns)
- [Google Gemini API](https://ai.google.dev/)

---

## 🤝 貢獻指南

歡迎貢獻新的 slide 類型！請遵循以下步驟：

1. Fork 專案
2. 創建新的 SlideType 類
3. 添加測試
4. 更新文檔
5. 提交 Pull Request

---

**版本**：2.0  
**最後更新**：2025-10-16

