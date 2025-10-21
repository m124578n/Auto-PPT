# 🎨 使用 PPTX 模板功能

## 📋 功能說明

AutoPPT 現在支持使用實際的 PowerPoint（PPTX）文件作為模板，完全保留原始設計風格！

### 兩種模式

1. **JSON 配置模式**（原有功能）
   - 使用 JSON 定義 slide 類型、位置、樣式
   - 從頭創建 PPTX
   - 完全自定義

2. **PPTX 模板模式**（新功能）✨
   - 使用實際的 PPTX 文件作為模板
   - 保留原始設計和樣式
   - JSON 配置作為映射和指令

## 🚀 快速開始

### 準備工作

1. **PPTX 模板文件**：例如 `pptx_template/test.pptx`
   - 包含你想要的設計風格
   - 定義好各種布局（layouts）

2. **JSON 配置文件**：例如 `templates/test_template.json`
   - 定義 slide 類型
   - 指定使用哪個 layout
   - 提供 AI 生成指令

### 使用方法

```python
from AutoPPT import AutoPPT
import os

# 初始化 AutoPPT（使用 PPTX 模板）
auto_ppt = AutoPPT(
    api_key=os.getenv('GEMINI_API_KEY'),
    template_json_path='templates/test_template.json',  # JSON 配置
    template_pptx_path='pptx_template/test.pptx'       # PPTX 模板
)

# 生成簡報
data = auto_ppt.generate(
    prompt='生成一個關於AI的簡報',
    save_files=True
)
```

### 工作流程

```
PPTX 模板文件 + JSON 配置
         ↓
    AutoPPT 初始化
         ↓
    AI 生成內容結構
         ↓
    從 PPTX 提取布局
         ↓
    填充內容到佔位符
         ↓
   保留原始設計風格的 PPTX
```

## 📐 JSON 配置說明

JSON 配置文件定義了如何使用 PPTX 模板：

```json
{
  "template_info": {
    "name": "測試模板",
    "version": "1.0.0",
    "slide_width": 13.333333333333334,
    "slide_height": 7.5
  },
  "slide_types": [
    {
      "type_id": "title_slide",
      "name": "標題投影片",
      "description": "簡報的標題頁面",
      "llm_instruction": "用於簡報的開頭，展示簡報的標題",
      "json_schema": {
        "slide_type": "title_slide",
        "title": "簡報標題"
      },
      "pptx_layout": {
        "layout_index": 0,  // ← 使用 PPTX 的第 0 個布局
        "background": {...},
        "elements": [...]
      }
    }
  ]
}
```

### 關鍵字段

- **`layout_index`**：PPTX 模板中布局的索引（0, 1, 2, ...）
- **`type_id`**：slide 類型的唯一標識
- **`llm_instruction`**：告訴 AI 什麼時候使用這個布局
- **`json_schema`**：定義這個 slide 需要的數據

## 🎯 布局索引（Layout Index）

查看 PPTX 模板中的布局：

```python
from pptx import Presentation

prs = Presentation('pptx_template/test.pptx')

for i, layout in enumerate(prs.slide_layouts):
    print(f"Layout {i}: {layout.name}")
```

輸出示例：
```
Layout 0: 標題投影片
Layout 1: 含影像的標題及內容
Layout 2: 章節標題
Layout 3: 標題、子標題及影像
...
```

## 📝 示例配置

### 示例 1：標題頁

```json
{
  "type_id": "opening",
  "name": "開場頁",
  "llm_instruction": "簡報的第一張，顯示主標題和副標題",
  "json_schema": {
    "slide_type": "opening",
    "title": "主標題",
    "subtitle": "副標題"
  },
  "pptx_layout": {
    "layout_index": 0  // 使用 PPTX 的「標題投影片」布局
  }
}
```

### 示例 2：內容頁

```json
{
  "type_id": "content_bullets",
  "name": "項目符號內容頁",
  "llm_instruction": "用於展示要點列表",
  "json_schema": {
    "slide_type": "content_bullets",
    "title": "標題",
    "bullets": ["要點1", "要點2", "要點3"],
    "indent_levels": [0, 0, 1]
  },
  "pptx_layout": {
    "layout_index": 6  // 使用 PPTX 的「標題及內容」布局
  }
}
```

## 🔧 高級功能

### 1. 自動填充佔位符

系統會自動識別和填充 PPTX 中的佔位符：

- **標題佔位符**：填充 `title` 或 `section_title`
- **內容佔位符**：填充 `subtitle`、`text`、`content` 或 `bullets`
- **圖片佔位符**：填充 `image_id` 指定的圖片

### 2. Bullet 列表支持

```json
{
  "slide_type": "content",
  "title": "主要功能",
  "bullets": [
    "功能 1",
    "功能 2",
    "  子功能 2.1",
    "  子功能 2.2",
    "功能 3"
  ],
  "indent_levels": [0, 0, 1, 1, 0]
}
```

### 3. 圖片支持

```json
{
  "slide_type": "image_content",
  "title": "產品展示",
  "image_id": "img_01",
  "text": "產品說明..."
}
```

## 💡 最佳實踐

### 1. 準備 PPTX 模板

✅ **建議**：
- 為每種類型的 slide 創建一個布局
- 使用清晰的佔位符（標題、內容、圖片）
- 保持一致的設計風格
- 測試所有布局是否正常工作

❌ **避免**：
- 過於複雜的布局
- 太多重疊的元素
- 不規則的佔位符位置

### 2. 配置 JSON 文件

✅ **建議**：
- 為每個布局寫清楚的 `llm_instruction`
- 使用有意義的 `type_id`
- 測試 AI 是否能正確選擇布局

### 3. 驗證設置

```python
# 創建 AutoPPT 後，檢查日誌
auto_ppt = AutoPPT(
    api_key=api_key,
    template_json_path='templates/test_template.json',
    template_pptx_path='pptx_template/test.pptx'
)

# 應該看到：
# ✓ 使用 PPTX 模板：pptx_template/test.pptx
# ✓ 配置文件：templates/test_template.json
# ✓ 可用布局數量：13
```

## 🔍 故障排除

### 問題 1：布局索引錯誤

```
⚠️ 布局索引 10 超出範圍，使用空白布局
```

**解決方案**：
- 檢查 PPTX 模板有多少個布局
- 調整 JSON 配置中的 `layout_index`

### 問題 2：佔位符未填充

**可能原因**：
- JSON 數據字段名稱不匹配
- PPTX 布局沒有佔位符

**解決方案**：
- 檢查 JSON schema 中的字段名稱
- 確保 PPTX 布局包含正確的佔位符

### 問題 3：圖片未顯示

**可能原因**：
- 圖片文件不存在
- `image_id` 不正確
- 布局沒有圖片佔位符

**解決方案**：
- 檢查圖片路徑
- 驗證 `image_metadata`
- 確保使用的布局支持圖片

## 📚 完整示例

### 創建模板

1. **準備 PPTX 文件**（`my_template.pptx`）
   - 創建多個布局
   - 添加佔位符

2. **使用工具生成 JSON 配置**

```python
from pptx_template_creator import PPTXTemplateCreator

creator = PPTXTemplateCreator(api_key='your_key')
creator.create_template_from_pptx(
    pptx_path='my_template.pptx',
    output_path='templates/my_template.json',
    template_name='我的模板'
)
```

3. **使用模板生成簡報**

```python
from AutoPPT import AutoPPT

auto_ppt = AutoPPT(
    api_key='your_key',
    template_json_path='templates/my_template.json',
    template_pptx_path='my_template.pptx'
)

data = auto_ppt.generate(
    prompt='生成簡報',
    save_files=True
)
```

## 🆚 對比

### JSON 配置模式 vs PPTX 模板模式

| 特性 | JSON 配置 | PPTX 模板 |
|------|-----------|-----------|
| 設計自由度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 保留原始設計 | ❌ | ✅ |
| 配置複雜度 | 高 | 中 |
| 易於調整 | 中 | 高 |
| 適合場景 | 從頭創建 | 使用現有模板 |

### 何時使用哪種模式？

**使用 JSON 配置**：
- 需要完全自定義的設計
- 從頭創建新的風格
- 需要精確控制每個元素

**使用 PPTX 模板**：
- 已有設計好的 PPTX 模板
- 需要保留公司/品牌風格
- 想要快速開始，不想配置細節

**混合使用**：
- 使用 PPTX 模板保留主要設計
- 用 JSON 配置定義 slide 類型和映射
- 最靈活的方案！✨

## 📖 相關文檔

- `PPTX_TEMPLATE_CREATOR_GUIDE.md` - 如何轉換 PPTX 為 JSON 配置
- `templates/test_template.json` - 示例配置文件
- `pptx_template_creator.py` - 轉換工具源碼

## 🎉 總結

使用 PPTX 模板功能，你可以：

✅ 保留原始 PowerPoint 設計
✅ 快速生成專業簡報
✅ 維持品牌一致性
✅ 靈活配置 AI 生成行為

開始使用：

```bash
# 測試 PPTX 模板功能
uv run test_pptx_template.py
```

---

**Made with ❤️ by 智造業 john**

🎨 **讓 AI 使用你的 PowerPoint 風格！**

