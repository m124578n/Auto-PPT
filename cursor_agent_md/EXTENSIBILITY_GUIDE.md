# 擴充性指南：如何添加新的 Slide 類型

## 🎯 設計理念

本項目使用 **Strategy Pattern** + **Registry Pattern**，讓新增 Slide 類型變得非常簡單。每個 Slide 類型都是一個獨立的類，自動註冊到系統中，無需修改任何其他代碼。

## ✨ 核心特性

### 1. 自動 JSON 示例生成

每個 Slide 類型都定義自己的 JSON schema，AI prompt 會自動從所有已註冊的類型中收集示例。

**優點：**
- ✅ 新增類型時，AI 自動知道如何使用
- ✅ 保持 DRY 原則（Don't Repeat Yourself）
- ✅ 減少人為錯誤
- ✅ 更易維護

### 2. 統一的介面

所有 Slide 類型實現四個方法：
- `get_json_example()`: 提供 JSON 示例（類方法）
- `get_description()`: 提供類型說明（類方法）
- `generate_html()`: 生成 HTML 片段
- `generate_pptx()`: 生成 PPTX slide

## 📝 如何添加新的 Slide 類型

### 步驟 1：創建新的 Slide 類

在 `slide_types.py` 中添加：

```python
@SlideTypeRegistry.register('your_new_type')
class YourNewSlide(SlideType):
    """你的新 Slide 類型描述"""
    
    @classmethod
    def get_json_example(cls) -> Dict[str, Any]:
        """定義 JSON 示例（會自動出現在 AI prompt 中）"""
        return {
            "slide_type": "your_new_type",
            "title": "標題",
            "custom_field": "自定義欄位"
        }
    
    @classmethod
    def get_description(cls) -> str:
        """定義類型說明（會自動出現在 AI prompt 中）"""
        return "你的新類型（適用場景說明）"
    
    def generate_html(self) -> str:
        """生成 HTML"""
        title = self.data.get('title', '')
        custom_field = self.data.get('custom_field', '')
        
        return f"""
        <div class="slide slide-your-type">
            <div class="slide-content">
                <h2>{title}</h2>
                <p>{custom_field}</p>
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
            title_frame.paragraphs[0].font.size = Pt(36)
            title_frame.paragraphs[0].font.bold = True
        
        # 添加自定義內容
        custom_field = self.data.get('custom_field', '')
        if custom_field:
            content_box = slide.shapes.add_textbox(
                Inches(1), Inches(2.5), Inches(8), Inches(3)
            )
            content_frame = content_box.text_frame
            content_frame.text = custom_field
            content_frame.paragraphs[0].font.size = Pt(24)
        
        return slide
```

### 步驟 2：就這樣！

是的，**就這麼簡單**！不需要：
- ❌ 修改 `ai_html_to_ppt.py`
- ❌ 修改 `slide_generator.py`
- ❌ 手動更新 AI prompt
- ❌ 修改任何配置文件

系統會自動：
- ✅ 註冊你的新類型
- ✅ 將 JSON 示例添加到 AI prompt
- ✅ 支持 HTML 和 PPTX 生成

## 🧪 測試新類型

### 方法 1：單元測試

```python
from slide_types import YourNewSlide
from pptx import Presentation

# 測試數據
test_data = {
    "slide_type": "your_new_type",
    "title": "測試標題",
    "custom_field": "測試內容"
}

# 測試 HTML 生成
slide_instance = YourNewSlide(test_data)
html = slide_instance.generate_html()
print(html)

# 測試 PPTX 生成
prs = Presentation()
slide = slide_instance.generate_pptx(prs)
prs.save('test_your_new_type.pptx')
```

### 方法 2：整合測試

```python
from slide_generator import HTMLGenerator, PPTXGenerator

test_data = {
    "title": "測試簡報",
    "topic": "test",
    "slides": [
        {
            "slide_type": "your_new_type",
            "title": "測試標題",
            "custom_field": "測試內容"
        }
    ]
}

# 生成 HTML
html_gen = HTMLGenerator()
html_content = html_gen.generate_from_data(test_data)
with open('test.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

# 生成 PPTX
pptx_gen = PPTXGenerator()
prs = pptx_gen.generate_from_data(test_data)
pptx_gen.save('test.pptx')
```

## 📚 完整範例

### 範例 1：雙欄文字頁

```python
@SlideTypeRegistry.register('two_column_text')
class TwoColumnTextSlide(SlideType):
    """雙欄文字佈局"""
    
    @classmethod
    def get_json_example(cls) -> Dict[str, Any]:
        return {
            "slide_type": "two_column_text",
            "title": "標題",
            "left_content": "左側內容",
            "right_content": "右側內容"
        }
    
    def generate_html(self) -> str:
        title = self.data.get('title', '')
        left = self.data.get('left_content', '')
        right = self.data.get('right_content', '')
        
        return f"""
        <div class="slide slide-two-column">
            <div class="slide-content">
                <h2 class="slide-title">{title}</h2>
                <div class="two-columns">
                    <div class="column-left">{left}</div>
                    <div class="column-right">{right}</div>
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
                Inches(0.6), Inches(0.5), Inches(8.8), Inches(0.8)
            )
            title_frame = title_box.text_frame
            title_frame.text = title
            title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
            title_frame.paragraphs[0].font.size = Pt(36)
            title_frame.paragraphs[0].font.bold = True
            title_frame.paragraphs[0].font.color.rgb = RGBColor(44, 62, 80)
        
        # 左欄
        left_content = self.data.get('left_content', '')
        if left_content:
            left_box = slide.shapes.add_textbox(
                Inches(0.6), Inches(1.8), Inches(4.2), Inches(5)
            )
            left_frame = left_box.text_frame
            left_frame.text = left_content
            left_frame.word_wrap = True
            left_frame.paragraphs[0].font.size = Pt(20)
        
        # 右欄
        right_content = self.data.get('right_content', '')
        if right_content:
            right_box = slide.shapes.add_textbox(
                Inches(5.2), Inches(1.8), Inches(4.2), Inches(5)
            )
            right_frame = right_box.text_frame
            right_frame.text = right_content
            right_frame.word_wrap = True
            right_frame.paragraphs[0].font.size = Pt(20)
        
        return slide
```

### 範例 2：引用卡片頁

```python
@SlideTypeRegistry.register('quote_card')
class QuoteCardSlide(SlideType):
    """引用卡片佈局"""
    
    @classmethod
    def get_json_example(cls) -> Dict[str, Any]:
        return {
            "slide_type": "quote_card",
            "quote": "引用文字",
            "author": "作者",
            "background_color": "#3498db"
        }
    
    def generate_html(self) -> str:
        quote = self.data.get('quote', '')
        author = self.data.get('author', '')
        bg_color = self.data.get('background_color', '#3498db')
        
        return f"""
        <div class="slide slide-quote" style="background-color: {bg_color};">
            <div class="slide-content">
                <blockquote class="quote-text">"{quote}"</blockquote>
                {f'<p class="quote-author">— {author}</p>' if author else ''}
            </div>
        </div>
        """
    
    def generate_pptx(self, prs: Presentation) -> Slide:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # 背景色
        bg_color = self.data.get('background_color', '#3498db')
        # 將十六進制轉為 RGB
        bg_color = bg_color.lstrip('#')
        r, g, b = tuple(int(bg_color[i:i+2], 16) for i in (0, 2, 4))
        
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(r, g, b)
        bg.line.fill.background()
        
        # 引用文字
        quote = self.data.get('quote', '')
        if quote:
            quote_box = slide.shapes.add_textbox(
                Inches(1.5), Inches(2.5), Inches(7), Inches(2)
            )
            quote_frame = quote_box.text_frame
            quote_frame.text = f'"{quote}"'
            quote_frame.word_wrap = True
            p = quote_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.font.size = Pt(36)
            p.font.italic = True
            p.font.color.rgb = RGBColor(255, 255, 255)
        
        # 作者
        author = self.data.get('author', '')
        if author:
            author_box = slide.shapes.add_textbox(
                Inches(1.5), Inches(5), Inches(7), Inches(0.8)
            )
            author_frame = author_box.text_frame
            author_frame.text = f'— {author}'
            p = author_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.font.size = Pt(24)
            p.font.color.rgb = RGBColor(255, 255, 255)
        
        return slide
```

## 🔍 查看已註冊的類型

### 在代碼中

```python
from slide_types import SlideTypeRegistry

# 獲取所有類型名稱
types = SlideTypeRegistry.all_types()
print(types)  # ['opening', 'section_divider', 'text_content', ...]

# 獲取所有 JSON 示例
examples = SlideTypeRegistry.get_all_json_examples()
for example in examples:
    print(example)
```

### 運行時查看

```bash
python -c "
from slide_types import SlideTypeRegistry
import json

print('已註冊的 Slide 類型：')
for slide_type in SlideTypeRegistry.all_types():
    print(f'  - {slide_type}')

print('\nJSON 示例：')
for example in SlideTypeRegistry.get_all_json_examples():
    print(json.dumps(example, ensure_ascii=False, indent=2))
    print()
"
```

## 💡 最佳實踐

### 1. 命名規範

- **類名**：使用 PascalCase，以 `Slide` 結尾
  - ✅ `TwoColumnTextSlide`
  - ❌ `twoColumnText`

- **slide_type**：使用 snake_case
  - ✅ `two_column_text`
  - ❌ `twoColumnText`

### 2. JSON 示例

- 包含所有必需欄位
- 使用有意義的示例值
- 添加註釋說明特殊欄位

```python
@classmethod
def get_json_example(cls) -> Dict[str, Any]:
    return {
        "slide_type": "image_with_text",
        "title": "標題",
        "image_id": "img_01",  # 使用 img_01, img_02 格式
        "text": "說明文字",
        "layout": "horizontal"  # 可選: "horizontal" 或 "vertical"
    }
```

### 3. HTML 生成

- 使用語義化標籤
- 添加適當的 CSS 類名
- 保持結構一致

```python
def generate_html(self) -> str:
    return f"""
    <div class="slide slide-{type_name}">
        <div class="slide-content">
            <!-- 內容 -->
        </div>
    </div>
    """
```

### 4. PPTX 生成

- 使用 `Inches()` 而非像素
- 設置適當的字體大小和顏色
- 處理可選欄位（檢查 `if` 條件）
- 保持與其他頁面一致的邊距和間距

```python
def generate_pptx(self, prs: Presentation) -> Slide:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 總是檢查欄位是否存在
    title = self.data.get('title', '')
    if title:
        # 添加內容
        pass
    
    return slide
```

### 5. 錯誤處理

```python
def generate_pptx(self, prs: Presentation) -> Slide:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 圖片處理
    image_id = self.data.get('image_id', '')
    image_path = self._get_image_path(image_id)
    
    if image_path and os.path.exists(image_path):
        try:
            slide.shapes.add_picture(image_path, ...)
            print(f"   ✓ 添加圖片：{os.path.basename(image_path)}")
        except Exception as e:
            print(f"   ⚠️ 圖片添加失敗：{e}")
    else:
        if image_id:
            print(f"   ⚠️ 圖片不存在：{image_id}")
    
    return slide
```

## 🎨 樣式指南

### 標準尺寸（英寸）

```python
# 幻燈片尺寸
SLIDE_WIDTH = 10.0
SLIDE_HEIGHT = 7.5

# 常用邊距
MARGIN_TOP = 0.5
MARGIN_BOTTOM = 0.5
MARGIN_LEFT = 0.6
MARGIN_RIGHT = 0.6

# 標題區域
TITLE_TOP = 0.5
TITLE_HEIGHT = 0.75

# 內容區域
CONTENT_TOP = 1.8  # 標題下方
CONTENT_HEIGHT = 5.4  # 剩餘空間
```

### 標準字體大小（Pt）

```python
# 標題
TITLE_SIZE = 36  # 一般標題
BIG_TITLE_SIZE = 50  # 開場/結尾頁

# 內容
CONTENT_SIZE = 20-24  # 正文
CAPTION_SIZE = 16  # 圖片說明
BULLET_SIZE = 22  # 項目符號
```

### 標準顏色（RGB）

```python
# 文字顏色
DARK_TEXT = RGBColor(44, 62, 80)  # #2c3e50
LIGHT_TEXT = RGBColor(255, 255, 255)  # #ffffff
GRAY_TEXT = RGBColor(127, 140, 141)  # #7f8c8d

# 背景顏色
BLUE_BG = RGBColor(57, 112, 161)  # #3970a1
PURPLE_BG = RGBColor(110, 114, 198)  # #6e72c6
PINK_BG = RGBColor(243, 117, 180)  # #f375b4
```

## 🚀 實戰技巧

### 技巧 1：複用現有輔助方法

```python
# 獲取圖片路徑
image_path = self._get_image_path(image_id)

# 計算保持寬高比的圖片尺寸
img_width, img_height = self._calculate_image_size(
    image_path, max_width=7.0, max_height=4.0
)
```

### 技巧 2：處理換行符號

```python
# 為每一行創建單獨的段落，確保置中對齊
lines = text.split('\n')
for i, line in enumerate(lines):
    if i == 0:
        p = text_frame.paragraphs[0]
    else:
        p = text_frame.add_paragraph()
    
    p.text = line
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(24)
```

### 技巧 3：動態字體大小

```python
# 根據文字長度調整字體大小
text_content = self.data.get('text', '')
if len(text_content) > 200:
    font_size = 18
elif len(text_content) > 100:
    font_size = 20
else:
    font_size = 22
```

### 技巧 4：圖片居中對齊

```python
# 在限定區域內居中對齊圖片
max_width = 7.0
max_height = 4.0
img_width, img_height = self._calculate_image_size(
    image_path, max_width, max_height
)

# 水平居中
left = Inches(1.5 + (max_width - img_width) / 2)
# 垂直居中
top = Inches(2.0 + (max_height - img_height) / 2)

slide.shapes.add_picture(
    image_path, left, top,
    width=Inches(img_width),
    height=Inches(img_height)
)
```

## 📖 參考資料

### 官方文檔

- [python-pptx Documentation](https://python-pptx.readthedocs.io/)
- [PIL/Pillow Documentation](https://pillow.readthedocs.io/)

### 項目文檔

- [README_ARCHITECTURE.md](./README_ARCHITECTURE.md) - 架構設計詳解
- [REFACTOR_SUMMARY.md](./REFACTOR_SUMMARY.md) - 重構總結
- [example_new_slide_type.py](./example_new_slide_type.py) - 實際範例

## ❓ 常見問題

### Q: 需要重啟程式才能看到新類型嗎？

A: 不需要！只要在 import 時載入了 `slide_types.py`，新類型就會自動註冊。

### Q: AI 會自動使用新類型嗎？

A: 是的！因為 JSON 示例會自動添加到 prompt 中，AI 會知道如何使用新類型。

### Q: 可以覆寫現有類型嗎？

A: 可以，只要使用相同的 `slide_type` 名稱註冊，新類會覆蓋舊類。

### Q: 如何測試 JSON 示例是否正確？

A: 運行：
```bash
python -c "
from slide_types import SlideTypeRegistry
import json
examples = SlideTypeRegistry.get_all_json_examples()
print(json.dumps(examples, ensure_ascii=False, indent=2))
"
```

### Q: 可以在不同文件中定義 Slide 類型嗎？

A: 可以！只要 import 該文件，類型會自動註冊：
```python
# my_custom_slides.py
from slide_types import SlideTypeRegistry, SlideType

@SlideTypeRegistry.register('my_custom_type')
class MyCustomSlide(SlideType):
    # ...
```

```python
# main.py
import slide_types  # 載入標準類型
import my_custom_slides  # 載入自定義類型
```

## 🎉 總結

添加新的 Slide 類型只需要：

1. ✅ 創建一個類，繼承 `SlideType`
2. ✅ 使用 `@SlideTypeRegistry.register()` 裝飾器
3. ✅ 實現四個方法：
   - `get_json_example()` - JSON 示例
   - `get_description()` - 類型說明
   - `generate_html()` - HTML 生成
   - `generate_pptx()` - PPTX 生成
4. ✅ 就這樣！

系統會自動處理其他一切：
- 🤖 AI prompt 自動更新（包含 JSON 示例和類型說明）
- 📝 JSON 示例自動收集
- 📋 類型說明自動收集
- 🎨 HTML/PPTX 生成自動支持

**擴充從未如此簡單！** 🚀

---

**版本**: 1.0  
**更新日期**: 2025-10-17  
**作者**: Auto-PPT Team

