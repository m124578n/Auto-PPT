# 📁 項目文件說明

## 核心文件

### 主程式

| 文件 | 說明 | 用途 |
|-----|------|------|
| `ai_html_to_ppt.py` | AI 生成器 | 使用 Gemini AI 分析內容並生成簡報 |
| `convert_html_to_pptx.py` | 格式轉換器 | 將 HTML 文件轉換為 PPTX 格式 |
| `slide_types.py` | Slide 類型定義 | 定義所有 Slide 類型的核心邏輯 |
| `slide_generator.py` | 生成器類 | HTML 和 PPTX 生成器的實現 |

### 配置文件

| 文件 | 說明 |
|-----|------|
| `pyproject.toml` | 項目配置和依賴 |
| `.env` | API Key 等敏感配置（需自行創建） |
| `.gitignore` | Git 忽略規則 |
| `.python-version` | Python 版本鎖定 |

## 示例和測試

| 文件 | 說明 |
|-----|------|
| `example_new_slide_type.py` | 自定義 Slide 類型示例 |
| `test_refactored.py` | 單元測試 |

## 文檔

| 文件 | 說明 |
|-----|------|
| `README.md` | 項目主文檔 |
| `QUICKSTART.md` | 快速開始指南 |
| `LICENSE` | MIT 開源協議 |
| `PROJECT_FILES.md` | 本文件，項目文件說明 |

### 詳細文檔（cursor_agent_md/）

| 文件 | 說明 |
|-----|------|
| `EXTENSIBILITY_GUIDE.md` | 擴展指南 - 如何添加新 Slide 類型 |
| `JSON_SCHEMA_EXTRACTION_SUMMARY.md` | JSON Schema 自動提取機制 |
| `DESCRIPTION_EXTRACTION_UPDATE.md` | 類型說明自動提取更新 |
| `README_ARCHITECTURE.md` | 架構設計文檔 |
| `LAYOUT_FIX_SUMMARY.md` | 佈局優化總結 |
| `NEWLINE_CENTER_FIX.md` | 換行符置中優化 |
| `IMAGE_TEXT_ALIGNMENT.md` | 圖文對齊優化 |

## 輸出文件

運行程式後會生成以下文件：

| 文件模式 | 說明 |
|---------|------|
| `*_presentation.html` | HTML 格式的簡報 |
| `*_data.json` | 簡報數據（JSON 格式） |
| `*.pptx` | PowerPoint 格式的簡報 |

## 資源目錄

| 目錄 | 說明 |
|-----|------|
| `downloaded_images/` | 存放簡報使用的圖片 |
| `cursor_agent_md/` | 詳細文檔目錄 |
| `old_py/` | 重構前的原始代碼 |

## 文件依賴關係

```
ai_html_to_ppt.py
├── slide_types.py
│   └── slide_generator.py
└── .env

convert_html_to_pptx.py
├── slide_types.py
│   └── slide_generator.py
└── *_presentation.html (輸入)
    └── *.pptx (輸出)

example_new_slide_type.py
└── slide_types.py

test_refactored.py
├── slide_types.py
└── slide_generator.py
```

## 推薦閱讀順序

### 新手入門

1. 📖 `README.md` - 了解項目概況
2. 🚀 `QUICKSTART.md` - 5 分鐘快速上手
3. 📁 `PROJECT_FILES.md` - 本文件
4. 🔧 `slide_types.py` - 查看 Slide 類型定義

### 進階使用

5. 📚 `cursor_agent_md/EXTENSIBILITY_GUIDE.md` - 學習如何擴展
6. 🏗️ `cursor_agent_md/README_ARCHITECTURE.md` - 理解架構設計
7. 📝 `example_new_slide_type.py` - 查看擴展示例

### 深入研究

8. 🔍 `cursor_agent_md/JSON_SCHEMA_EXTRACTION_SUMMARY.md` - 自動化機制
9. 🎨 `cursor_agent_md/LAYOUT_FIX_SUMMARY.md` - 佈局技術
10. 🧪 `test_refactored.py` - 測試用例

## 重要提示

### 必須創建的文件

- `.env` - 包含你的 API Key（參考 README.md）

### 不要提交的文件

- `.env` - 包含敏感信息
- `*.pptx` - 生成的輸出文件
- `*_presentation.html` - 生成的輸出文件
- `*_data.json` - 生成的數據文件
- `downloaded_images/*` - 具體的圖片文件（目錄保留）

這些文件已在 `.gitignore` 中配置。

## 文件大小參考

| 類型 | 大小 |
|-----|------|
| 核心代碼文件 | ~200-800 行 |
| 文檔文件 | ~300-600 行 |
| 測試文件 | ~270 行 |
| 生成的 PPTX | 依內容而定 |
| 生成的 HTML | 依內容而定 |

## 更新頻率

### 經常修改
- `ai_html_to_ppt.py` - 調整 AI prompt 和文字內容
- `slide_types.py` - 調整樣式或添加新類型

### 偶爾修改
- `convert_html_to_pptx.py` - 優化轉換邏輯
- `slide_generator.py` - 優化生成器

### 很少修改
- 配置文件
- 文檔文件
- 測試文件

---

**最後更新**: 2025-10-17  
**版本**: 1.0.0
