# 🚀 新架構快速開始指南

## ✅ 修復完成

已修復 `Position.from_dict()` 方法，現在支持：
- `width` / `height`（固定尺寸）
- `max_width` / `max_height`（最大尺寸，用於圖片）

## 🎯 核心改進

### 修復前
```python
# 只支持 width/height
position = Position.from_dict({
    'left': 1.0,
    'top': 2.0,
    'width': 8.0,      # 必須
    'height': 5.0      # 必須
})
```

### 修復後
```python
# 支持 width/height 或 max_width/max_height
position = Position.from_dict({
    'left': 1.0,
    'top': 2.0,
    'max_width': 8.0,   # 可以使用 max_width
    'max_height': 5.0   # 可以使用 max_height
})

# 或者使用默認值
position = Position.from_dict({
    'left': 1.0,
    'top': 2.0
    # width/height 默認為 0
})
```

## 🧪 測試

### 驗證模板

```bash
uv run verify_template.py
```

**預期輸出**：
```
✅ 找到模板文件：templates/default_template.json
✅ JSON 格式正確
✅ 模板驗證完成！
```

### 運行示例

```bash
uv run example_new_architecture.py
```

**預期輸出**：
- ✅ 示例 2：檢查模板內容
- ✅ 示例 3：查看生成的 AI Prompt
- ✅ 示例 4：自定義模板
- ✅ 示例 5：查看模板元素

## 💻 實際使用

### 1. 基本使用（默認模板）

```python
from AutoPPT import AutoPPT
import os

# 初始化
auto_ppt = AutoPPT(
    api_key=os.getenv('GOOGLE_API_KEY')
)

# 生成簡報
data = auto_ppt.generate(
    prompt='生成一個關於 Python 的簡報',
    save_files=True
)
```

### 2. 使用自定義模板

```python
from AutoPPT import AutoPPT
import os

# 使用自定義模板
auto_ppt = AutoPPT(
    api_key=os.getenv('GOOGLE_API_KEY'),
    template_path='templates/my_custom_template.json'
)

# 生成簡報
data = auto_ppt.generate(
    prompt='生成簡報',
    save_files=True
)
```

### 3. 直接使用 Template Engine

```python
from AutoPPT.template_engine import PPTXTemplate

# 加載模板
template = PPTXTemplate('templates/default_template.json')

# 查看 Slide 類型
slide_types = template.get_all_slide_type_ids()
print(f"可用 Slide 類型：{slide_types}")

# 生成 AI Prompt
prompt = template.generate_ai_prompt(
    user_prompt='生成一個簡報'
)
print(prompt)
```

## 📋 JSON 模板結構

### 最小模板

```json
{
  "template_info": {
    "name": "我的模板",
    "version": "1.0.0",
    "description": "簡單描述",
    "slide_width": 10.0,
    "slide_height": 7.5
  },
  "slide_types": [
    {
      "type_id": "opening",
      "name": "開場頁",
      "description": "簡報的封面頁",
      "llm_instruction": "用於簡報開始",
      "json_schema": {
        "slide_type": "opening",
        "title": "標題"
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
            "position": {
              "left": 1.0,
              "top": 3.0,
              "width": 8.0,
              "height": 1.5
            },
            "style": {
              "font_size": 48,
              "font_bold": true,
              "font_color": "#000000",
              "alignment": "center"
            }
          }
        ]
      }
    }
  ]
}
```

### 元素類型

#### 文本框（textbox）

```json
{
  "type": "textbox",
  "name": "title",
  "position": {
    "left": 1.0,
    "top": 2.0,
    "width": 8.0,
    "height": 1.5
  },
  "style": {
    "font_size": 48,
    "font_bold": true,
    "font_color": "#000000",
    "alignment": "center"
  }
}
```

#### 圖片（image）

```json
{
  "type": "image",
  "name": "main_image",
  "position": {
    "left": 1.0,
    "top": 2.0,
    "max_width": 8.0,
    "max_height": 5.0
  }
}
```

或使用 layout 相關位置：

```json
{
  "type": "image",
  "name": "main_image",
  "position_horizontal": {
    "left": 0.7,
    "top": 2.5,
    "max_width": 4.4,
    "max_height": 5.0
  },
  "position_vertical": {
    "left": 1.0,
    "top": 2.5,
    "max_width": 8.0,
    "max_height": 3.2
  }
}
```

#### 形狀（shape）

```json
{
  "type": "shape",
  "name": "decoration_line",
  "shape_type": "rectangle",
  "position": {
    "left": 4.0,
    "top": 2.6,
    "width": 2.0,
    "height": 0.04
  },
  "style": {
    "fill_color": "#FFFFFF"
  }
}
```

## 🎨 擴展新 Slide 類型

### 步驟 1：修改 JSON 模板

在 `templates/default_template.json` 的 `slide_types` 數組中添加：

```json
{
  "type_id": "two_column",
  "name": "雙欄對比頁",
  "description": "左右兩欄對比內容",
  "llm_instruction": "用於對比兩個概念或項目",
  "json_schema": {
    "slide_type": "two_column",
    "title": "標題",
    "left_content": "左側內容",
    "right_content": "右側內容"
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
        "position": {"left": 0.5, "top": 0.5, "width": 9.0, "height": 0.8},
        "style": {
          "font_size": 36,
          "font_bold": true,
          "font_color": "#2C3E50",
          "alignment": "center"
        }
      },
      {
        "type": "textbox",
        "name": "left_content",
        "position": {"left": 0.5, "top": 2.0, "width": 4.5, "height": 5.0},
        "style": {
          "font_size": 20,
          "font_color": "#2C3E50"
        }
      },
      {
        "type": "textbox",
        "name": "right_content",
        "position": {"left": 5.0, "top": 2.0, "width": 4.5, "height": 5.0},
        "style": {
          "font_size": 20,
          "font_color": "#2C3E50"
        }
      }
    ]
  }
}
```

### 步驟 2：立即使用

無需修改任何 Python 代碼！AI 會自動識別新的 Slide 類型並使用。

## 🔧 常見問題

### Q1: 如何驗證模板是否正確？

```bash
uv run verify_template.py
```

### Q2: 如何查看生成的 AI Prompt？

```python
from AutoPPT.template_engine import PPTXTemplate

template = PPTXTemplate('templates/default_template.json')
prompt = template.generate_ai_prompt(user_prompt='測試')
print(prompt)
```

### Q3: 如何使用不同的顏色？

顏色使用十六進制格式（Hex）：

```json
{
  "font_color": "#FF0000"  // 紅色
  "fill_color": "#00FF00"  // 綠色
  "color": "#0000FF"       // 藍色
}
```

常用顏色：
- 黑色：`#000000`
- 白色：`#FFFFFF`
- 灰色：`#808080`
- 深藍：`#2C3E50`
- 藍色：`#4682B4`

### Q4: 位置單位是什麼？

所有位置都使用**英寸（inches）**：

```json
{
  "left": 1.0,    // 距離左邊 1 英寸
  "top": 2.0,     // 距離頂部 2 英寸
  "width": 8.0,   // 寬度 8 英寸
  "height": 1.5   // 高度 1.5 英寸
}
```

標準幻燈片尺寸（16:9）：
- 寬度：10.0 英寸
- 高度：7.5 英寸

### Q5: 如何調整字體大小？

```json
{
  "font_size": 48  // 單位：pt (點)
}
```

建議字體大小：
- 標題：48-60 pt
- 副標題：28-36 pt
- 正文：20-24 pt
- 說明文字：14-16 pt

## 📊 模板最佳實踐

### 1. 命名規範

- **type_id**：使用小寫和下劃線（`opening`, `two_column`）
- **name**：使用中文描述（"開場頁", "雙欄對比頁"）
- **element name**：使用有意義的名稱（`title`, `main_content`）

### 2. 顏色方案

保持一致的配色：

```json
{
  "primary_color": "#2C3E50",    // 主色
  "secondary_color": "#4682B4",  // 輔助色
  "text_color": "#2C3E50",       // 文字色
  "background": "#FFFFFF"        // 背景色
}
```

### 3. 間距一致性

保持統一的邊距：

```json
{
  "margin_left": 0.5,     // 左邊距
  "margin_right": 0.5,    // 右邊距
  "margin_top": 0.5,      // 上邊距
  "content_padding": 0.2  // 內容間距
}
```

### 4. 版本管理

在每次修改時更新版本號：

```json
{
  "template_info": {
    "version": "1.0.1",
    "last_updated": "2025-10-21"
  }
}
```

## 🎯 下一步

1. ✅ 基礎架構已完成
2. 📝 創建自己的模板
3. 🎨 調整顏色和樣式
4. 🔄 添加新的 Slide 類型
5. 📊 測試和優化

## 📚 相關文檔

- `NEW_ARCHITECTURE_SUMMARY.md` - 完整架構說明
- `templates/default_template.json` - 默認模板
- `verify_template.py` - 驗證工具
- `example_new_architecture.py` - 使用示例

---

**Made with ❤️ by 智造業 john**

🎉 **開始使用 JSON 驅動的簡報生成吧！**

