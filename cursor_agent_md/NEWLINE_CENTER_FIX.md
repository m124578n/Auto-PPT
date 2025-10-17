# 換行符號置中優化

## 🎯 問題描述

當文字內容包含換行符號 `\n` 時，如果直接使用 `text_frame.text = "line1\nline2"`，PowerPoint 只會將第一行的對齊方式應用到整個文字框，導致後續行無法正確置中。

**問題範例：**
```json
{
  "subtext": "立即預訂，開啟您的日本北陸絕景之旅！\nAPP獨享！輸碼【Hokuriku1000】現折1千"
}
```

在這種情況下，第二行 "APP獨享！..." 不會被置中對齊。

## ✅ 解決方案

為每一行創建獨立的 paragraph，並為每個 paragraph 單獨設置置中對齊。

### 修改前（❌ 錯誤）
```python
title_frame.text = main_title
title_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
title_frame.paragraphs[0].font.size = Pt(52)
# 只有第一行會置中，後續行靠左
```

### 修改後（✅ 正確）
```python
# 處理換行符號，為每一行創建單獨的段落
lines = main_title.split('\n')
for i, line in enumerate(lines):
    if i == 0:
        p = title_frame.paragraphs[0]
    else:
        p = title_frame.add_paragraph()
    
    p.text = line
    p.alignment = PP_ALIGN.CENTER  # 每一行都置中
    p.font.size = Pt(52)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
```

## 📋 已優化的 Slide 類型

### 1. OpeningSlide（開場頁）
- ✅ 主標題 - 支援換行並置中
- ✅ 副標題 - 支援換行並置中

**測試範例：**
```json
{
  "slide_type": "opening",
  "title": "歡迎來到測試簡報",
  "subtitle": "這是第一行\n這是第二行\n這是第三行"
}
```

### 2. SectionSlide（章節分隔頁）
- ✅ 章節標題 - 支援換行並置中

**測試範例：**
```json
{
  "slide_type": "section_divider",
  "section_title": "第一章節\n章節副標題"
}
```

### 3. TextContentSlide（純文字內容頁）
- ✅ 標題 - 支援換行並置中

**測試範例：**
```json
{
  "slide_type": "text_content",
  "title": "主要特點\n（2025年版）",
  "bullets": ["要點1", "要點2"]
}
```

### 4. ImageTextSlide（圖文混合頁）
- ✅ 標題 - 支援換行並置中

**測試範例：**
```json
{
  "slide_type": "image_with_text",
  "title": "圖片展示\n精彩瞬間",
  "image_id": "img_01",
  "text": "說明文字"
}
```

### 5. FullImageSlide（大圖展示頁）
- ✅ 標題 - 支援換行並置中
- ✅ 圖片說明 - 支援換行並置中

**測試範例：**
```json
{
  "slide_type": "full_image",
  "title": "立山黑部\n阿爾卑斯山路線",
  "image_id": "img_02",
  "caption": "壯麗的雪壁景觀\n每年4-6月限定"
}
```

### 6. ClosingSlide（結尾頁）
- ✅ 結尾標題 - 支援換行並置中
- ✅ 副文字 - 支援換行並置中

**測試範例：**
```json
{
  "slide_type": "closing",
  "closing_text": "謝謝觀看",
  "subtext": "立即預訂，開啟您的旅程！\nAPP獨享！輸碼現折1千"
}
```

## 🔍 技術細節

### 為什麼需要分段落？

PowerPoint 的文字框架（TextFrame）中的對齊設置是基於 paragraph 的，而不是整個文字框。當直接設置包含 `\n` 的文字時：

```python
# ❌ 這樣只有第一個 paragraph 有對齊設置
text_frame.text = "Line 1\nLine 2\nLine 3"
text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
# 結果：只有 Line 1 置中，Line 2 和 Line 3 靠左
```

正確的做法是為每一行創建獨立的 paragraph：

```python
# ✅ 每一行都有自己的對齊設置
lines = text.split('\n')
for i, line in enumerate(lines):
    p = text_frame.paragraphs[0] if i == 0 else text_frame.add_paragraph()
    p.text = line
    p.alignment = PP_ALIGN.CENTER
# 結果：所有行都正確置中
```

### 字體大小和樣式

每個 paragraph 都需要單獨設置：
- 字體大小（font.size）
- 字體粗細（font.bold）
- 字體顏色（font.color）
- 對齊方式（alignment）

這樣可以確保所有行的樣式保持一致。

## 🧪 測試結果

### 基本測試
```bash
$ python test_refactored.py
✅ 所有測試通過！
```

### 換行符測試
```bash
$ python -c "..." # 測試包含換行符的數據
✅ 換行符測試完成！生成文件：test_newline.pptx
```

**測試內容：**
- ✅ 單行文字 - 正常置中
- ✅ 兩行文字 - 兩行都置中
- ✅ 多行文字 - 所有行都置中
- ✅ 混合中英文 - 正確處理
- ✅ 包含標點符號 - 正確處理

## 📊 改進前後對比

### 改進前
```
                第一行（置中）
第二行（靠左）
第三行（靠左）
```
❌ 只有第一行置中，不整齊

### 改進後
```
            第一行（置中）
            第二行（置中）
            第三行（置中）
```
✅ 所有行都置中，整齊美觀

## 💡 使用建議

### 1. 在 JSON 中使用換行符

```json
{
  "closing_text": "謝謝觀看",
  "subtext": "第一行文字\n第二行文字\n第三行文字"
}
```

### 2. 控制行數

建議每個文字框不要超過 3-4 行：
- ✅ 2-3 行：最佳，易讀美觀
- ⚠️ 4-5 行：可接受，但要注意字體大小
- ❌ 6+ 行：可能超出邊界，不推薦

### 3. 行長度控制

每行文字建議：
- **主標題**：15-25 字/行
- **副標題**：20-35 字/行
- **說明文字**：30-50 字/行

### 4. 換行位置選擇

在合適的位置換行，保持語意完整：

**好的換行 ✅**
```
立即預訂，開啟您的旅程！
APP獨享！輸碼現折1千
```

**不好的換行 ❌**
```
立即預訂，開啟您的旅
程！APP獨享！輸碼現折1千
```

## 🎨 視覺效果

### 開場頁範例
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━
          歡迎來到測試簡報
          
          這是第一行
          這是第二行
          這是第三行
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 結尾頁範例
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━
          謝謝觀看
          
    立即預訂，開啟您的旅程！
      APP獨享！輸碼現折1千
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🔄 兼容性

### 完全兼容
- ✅ 無換行符的文字（正常運作）
- ✅ 包含換行符的文字（正確置中）
- ✅ 空字符串（正常處理）
- ✅ 只有換行符（正常處理）

### 向後兼容
現有的 JSON 數據無需修改：
- 沒有換行符的數據 → 繼續正常運作
- 有換行符的數據 → 現在會正確置中

## 📝 代碼示例

### 完整範例

```python
from slide_generator import PPTXGenerator

# 包含換行符的數據
test_data = {
    'title': '日本北陸之旅',
    'topic': 'hokuriku_tour',
    'slides': [
        {
            'slide_type': 'opening',
            'title': '日本北陸深度之旅',
            'subtitle': '探索自然奇觀\n體驗文化精粹\n享受美食饗宴'
        },
        {
            'slide_type': 'section_divider',
            'section_title': '行程亮點\n2025 精選路線'
        },
        {
            'slide_type': 'closing',
            'closing_text': '立即開始您的旅程',
            'subtext': '現在預訂享優惠\nAPP獨享折扣碼【TOUR2025】'
        }
    ]
}

# 生成 PPTX
pptx_gen = PPTXGenerator()
prs = pptx_gen.generate_from_data(test_data)
pptx_gen.save('hokuriku_tour.pptx')
```

## ✨ 實際應用案例

### 案例 1：旅遊行程
```json
{
  "slide_type": "closing",
  "closing_text": "期待與您相見",
  "subtext": "立即預訂，開啟您的日本北陸絕景之旅！\nAPP獨享！輸碼【Hokuriku1000】現折1千"
}
```

**效果：**
- 第一行：立即預訂，開啟您的日本北陸絕景之旅！
- 第二行：APP獨享！輸碼【Hokuriku1000】現折1千
- 兩行都完美置中對齊

### 案例 2：活動宣傳
```json
{
  "slide_type": "opening",
  "title": "2025 春季特別活動",
  "subtitle": "限時優惠\n早鳥價 85 折\n名額有限，立即報名"
}
```

**效果：**
- 三行副標題整齊置中
- 視覺層次分明
- 易讀美觀

### 案例 3：產品介紹
```json
{
  "slide_type": "section_divider",
  "section_title": "新產品發布\n改變世界的創新"
}
```

**效果：**
- 標題和副標題都置中
- 強調重點清晰
- 專業商務風格

## 🔧 故障排除

### Q: 換行後文字還是靠左？
A: 確保使用的是最新版本的 `slide_types.py`，所有文字框都已經更新為分段落處理。

### Q: 換行後字體大小不一致？
A: 檢查是否為每個 paragraph 都設置了字體大小，確保在循環中設置 `p.font.size`。

### Q: 換行後顏色不對？
A: 確保為每個 paragraph 都設置了顏色，`p.font.color.rgb = RGBColor(...)`。

### Q: 有些行置中，有些行靠左？
A: 檢查是否漏掉某些 slide 類型的更新，所有需要置中的文字都應該使用分段落處理。

## 📚 相關文檔

- [LAYOUT_FIX_SUMMARY.md](./LAYOUT_FIX_SUMMARY.md) - 防跑版優化總結
- [REFACTOR_SUMMARY.md](./REFACTOR_SUMMARY.md) - 重構總結
- [README_ARCHITECTURE.md](./README_ARCHITECTURE.md) - 架構說明

## 🎉 結論

通過為每一行創建獨立的 paragraph 並設置對齊方式，現在所有包含換行符的文字都能完美置中顯示，讓簡報更加整齊美觀！

**核心改進：**
- ✅ 支援換行符號
- ✅ 每行都正確置中
- ✅ 保持樣式一致
- ✅ 完全向後兼容
- ✅ 所有測試通過

---

**版本**: 2.2  
**更新日期**: 2025-10-16  
**狀態**: ✅ 完成並測試通過

