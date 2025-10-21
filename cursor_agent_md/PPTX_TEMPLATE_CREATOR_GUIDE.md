# 🎨 PPTX 轉 JSON 模板工具使用指南

## 📋 功能說明

這個工具可以將現有的 PowerPoint（PPTX）文件轉換成 JSON 模板格式，讓 AutoPPT 可以使用。

### 主要功能

1. **自動分析 PPTX 結構**
   - 提取每張 slide 的佈局
   - 識別文本框、圖片、形狀
   - 獲取位置、大小、樣式信息

2. **智能識別元素用途**
   - 根據位置和樣式自動判斷是標題、副標題還是內容
   - 提取字體大小、顏色、對齊方式
   - 識別背景顏色

3. **使用 Gemini AI 生成模板**
   - 將分析結果轉換成標準 JSON 格式
   - 自動生成 LLM 指令和 JSON Schema
   - 保持原有設計風格

## 🚀 快速開始

### 方法 1：命令行使用

```bash
# 設置 API Key（如果還沒設置）
export GOOGLE_API_KEY="your_api_key_here"

# 或者在 .env 文件中添加
echo "GOOGLE_API_KEY=your_api_key_here" >> .env

# 運行工具
uv run pptx_template_creator.py
```

### 方法 2：Python 腳本使用

```python
import os
from dotenv import load_dotenv
from pptx_template_creator import PPTXTemplateCreator

# 加載環境變量
load_dotenv()

# 創建轉換器
creator = PPTXTemplateCreator(api_key=os.getenv('GOOGLE_API_KEY'))

# 轉換 PPTX
output_path = creator.create_template_from_pptx(
    pptx_path="pptx_template/test.pptx",
    output_path="templates/my_template.json",
    template_name="我的自定義模板"
)

print(f"✅ 模板已生成：{output_path}")
```

### 方法 3：分步驟使用

```python
from pptx_template_creator import PPTXTemplateCreator

creator = PPTXTemplateCreator(api_key="your_key")

# 步驟 1：分析 PPTX
analysis = creator.analyze_pptx("my_template.pptx")

# 檢查分析結果
print(f"總共 {analysis['total_slides']} 張 slides")
for slide in analysis['slides']:
    print(f"Slide {slide['slide_number']}: {len(slide['elements'])} 個元素")

# 步驟 2：生成 JSON 模板
template_json = creator.generate_template_json(analysis, "我的模板")

# 步驟 3：保存模板
with open("my_template.json", "w", encoding="utf-8") as f:
    f.write(template_json)
```

## 📊 工作流程

```
PPTX 文件
    ↓
┌─────────────────────┐
│  1. 分析 PPTX 結構  │
│  - 讀取所有 slides  │
│  - 提取元素信息     │
│  - 識別樣式         │
└─────────────────────┘
    ↓
分析結果（JSON）
    ↓
┌─────────────────────┐
│  2. Gemini AI 處理  │
│  - 理解結構         │
│  - 生成 LLM 指令    │
│  - 創建 JSON Schema │
└─────────────────────┘
    ↓
JSON 模板
    ↓
┌─────────────────────┐
│  3. 驗證模板        │
│  - 檢查格式         │
│  - 驗證完整性       │
└─────────────────────┘
    ↓
可用的 JSON 模板
```

## 📁 生成的文件

運行工具後會生成兩個文件：

1. **`*_analysis.json`** - PPTX 分析結果
   ```json
   {
     "slide_width": 10.0,
     "slide_height": 7.5,
     "total_slides": 5,
     "slides": [
       {
         "slide_number": 1,
         "layout_name": "Title Slide",
         "background": {...},
         "elements": [...]
       }
     ]
   }
   ```

2. **`*_template.json`** - 可用的 JSON 模板
   ```json
   {
     "template_info": {
       "name": "我的模板",
       "version": "1.0.0",
       "description": "...",
       "slide_width": 10.0,
       "slide_height": 7.5
     },
     "slide_types": [
       {
         "type_id": "opening",
         "name": "開場頁",
         "description": "...",
         "llm_instruction": "...",
         "json_schema": {...},
         "pptx_layout": {...}
       }
     ]
   }
   ```

## 🎯 分析功能詳解

### 1. 元素識別

工具會自動識別以下類型的元素：

| 元素類型 | 識別特徵 | 生成的 name |
|---------|---------|------------|
| 標題 | 頂部、大字體(>30pt)、粗體、居中 | `title` |
| 副標題 | 靠近頂部、中等字體(>20pt)、居中 | `subtitle` |
| 內容 | 中間位置、較大區域(高度>3英寸) | `content` |
| 說明文字 | 小字體(<20pt) | `caption` |
| 圖片 | PICTURE 類型 | `image_placeholder` |
| 形狀 | 矩形、線條等 | `shape_*` |

### 2. 樣式提取

自動提取以下樣式信息：

- **字體大小** (`font_size`)
- **字體顏色** (`font_color`)  
- **粗體** (`font_bold`)
- **對齊方式** (`alignment`)
- **填充顏色** (`fill_color`)
- **位置和尺寸** (`position`)

### 3. 位置信息

所有位置使用**英寸（inches）**為單位：

```json
{
  "position": {
    "left": 1.0,    // 距離左邊 1 英寸
    "top": 2.0,     // 距離頂部 2 英寸
    "width": 8.0,   // 寬度 8 英寸
    "height": 1.5   // 高度 1.5 英寸
  }
}
```

## 🤖 Gemini AI 的作用

Gemini AI 負責：

1. **理解 PPTX 結構**
   - 分析每個元素的用途
   - 識別 slide 的類型
   - 理解設計意圖

2. **生成 LLM 指令**
   - 為每個 slide 類型寫使用說明
   - 定義什麼時候使用這個佈局
   - 說明數據要求

3. **創建 JSON Schema**
   - 定義需要哪些字段
   - 指定字段類型
   - 設置必填項

4. **命名和描述**
   - 給 slide 類型起有意義的名字
   - 寫清晰的中文描述
   - 生成易懂的文檔

## 💡 最佳實踐

### 1. PPTX 準備

**✅ 建議**：
- 使用清晰的佈局結構
- 每種類型的 slide 保留一張作為模板
- 使用一致的字體和顏色
- 避免過於複雜的設計

**❌ 避免**：
- 太多重疊的元素
- 過於複雜的形狀
- 不規則的佈局
- 動畫和轉場效果（會被忽略）

### 2. 模板命名

```python
# ✅ 好的命名
creator.create_template_from_pptx(
    pptx_path="business_presentation.pptx",
    template_name="商務簡報模板"
)

# ❌ 不好的命名
creator.create_template_from_pptx(
    pptx_path="template.pptx",
    template_name="Template"
)
```

### 3. 檢查生成結果

```python
# 生成後檢查
import json

with open("my_template.json", "r") as f:
    template = json.load(f)

# 查看 slide 類型
for st in template["slide_types"]:
    print(f"✓ {st['name']} ({st['type_id']})")
    print(f"  元素: {len(st['pptx_layout']['elements'])} 個")
```

### 4. 使用生成的模板

```python
from AutoPPT import AutoPPT

# 使用自定義模板
auto_ppt = AutoPPT(
    api_key="your_key",
    template_path="templates/my_template.json"
)

# 生成簡報
data = auto_ppt.generate(
    prompt="生成一個關於 AI 的簡報",
    save_files=True
)
```

## 🔧 進階配置

### 自定義元素識別規則

如果需要修改元素識別邏輯，可以編輯 `_guess_textbox_purpose` 方法：

```python
def _guess_textbox_purpose(self, text: str, position: Dict, style: Dict) -> str:
    """根據位置和樣式推測文本框用途"""
    top = position.get("top", 0)
    font_size = style.get("font_size", 0)
    
    # 添加自定義規則
    if "總結" in text or "結論" in text:
        return "conclusion"
    
    # 原有邏輯...
```

### 手動調整生成的模板

生成的模板可以手動編輯：

```json
{
  "type_id": "opening",
  "name": "開場頁",
  "llm_instruction": "用於簡報開始，展示主題和講者信息。應該簡潔有力。",
  "json_schema": {
    "slide_type": "opening",
    "title": "主標題（必填）",
    "subtitle": "副標題（選填）",
    "author": "講者姓名（選填）"  // 手動添加新字段
  },
  "pptx_layout": {
    "elements": [
      // 可以手動調整位置、樣式
      {
        "type": "textbox",
        "name": "title",
        "position": {"left": 1.0, "top": 2.5, "width": 8.0, "height": 1.5},
        "style": {
          "font_size": 52,  // 調整字體大小
          "font_bold": true,
          "font_color": "#1E3A8A",  // 更換顏色
          "alignment": "center"
        }
      }
    ]
  }
}
```

## 📊 示例

### 完整示例

```python
#!/usr/bin/env python3
"""
示例：轉換 PowerPoint 模板
"""
import os
from dotenv import load_dotenv
from pptx_template_creator import PPTXTemplateCreator

def main():
    # 加載環境變量
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ 請設置 GOOGLE_API_KEY")
        return
    
    # 創建轉換器
    print("🎨 PPTX 轉 JSON 模板工具")
    print("="*50)
    
    creator = PPTXTemplateCreator(api_key=api_key)
    
    # 要轉換的 PPTX 文件列表
    templates = [
        {
            "pptx": "templates/business.pptx",
            "output": "templates/business_template.json",
            "name": "商務簡報模板"
        },
        {
            "pptx": "templates/academic.pptx",
            "output": "templates/academic_template.json",
            "name": "學術簡報模板"
        }
    ]
    
    # 批次轉換
    for tmpl in templates:
        if not os.path.exists(tmpl["pptx"]):
            print(f"⚠️  跳過：{tmpl['pptx']} (文件不存在)")
            continue
        
        print(f"\n📄 處理：{tmpl['pptx']}")
        
        try:
            output = creator.create_template_from_pptx(
                pptx_path=tmpl["pptx"],
                output_path=tmpl["output"],
                template_name=tmpl["name"]
            )
            print(f"✅ 成功：{output}")
            
        except Exception as e:
            print(f"❌ 失敗：{e}")
    
    print("\n" + "="*50)
    print("🎉 全部完成！")

if __name__ == '__main__':
    main()
```

## 🐛 故障排除

### 問題 1：API Key 錯誤

```
❌ 請設置 GOOGLE_API_KEY 環境變量
```

**解決方案**：
```bash
# 方法 1：命令行設置
export GOOGLE_API_KEY="your_key"

# 方法 2：.env 文件
echo "GOOGLE_API_KEY=your_key" >> .env
```

### 問題 2：無法識別某些元素

**解決方案**：
- 檢查 `*_analysis.json` 文件查看分析結果
- 手動調整生成的模板
- 簡化 PPTX 設計

### 問題 3：生成的模板格式不對

**解決方案**：
- 運行工具會自動驗證格式
- 如果驗證失敗，檢查錯誤信息
- 手動編輯 JSON 文件修正問題

### 問題 4：Gemini 生成的結果不理想

**解決方案**：
- 多運行幾次（AI 生成有隨機性）
- 手動編輯 `llm_instruction` 和 `description`
- 調整 PPTX 使其結構更清晰

## 📚 相關文檔

- `templates/default_template.json` - 默認模板參考
- `AutoPPT/template_engine.py` - 模板引擎源碼
- `NEW_ARCHITECTURE_SUMMARY.md` - 架構文檔

## 🎯 下一步

1. ✅ 轉換你的 PPTX 文件
2. 📝 檢查生成的模板
3. ✏️ 手動調整（如果需要）
4. 🚀 使用模板生成簡報

---

**Made with ❤️ by 智造業 john**

🎨 **讓 AI 學習你的 PowerPoint 風格！**

