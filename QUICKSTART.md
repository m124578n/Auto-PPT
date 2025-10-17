# 🚀 快速開始指南

## 5 分鐘上手 Auto-PPT

### 1️⃣ 安裝依賴

```bash
# 使用 uv (推薦)
uv sync

# 或使用 pip
pip install -e .
```

### 2️⃣ 配置 API Key

創建 `.env` 文件：

```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

> 🔑 獲取 API Key：https://aistudio.google.com/apikey

### 3️⃣ 準備素材

#### 選項 A：使用默認示例（純文字）

```python
# ai_html_to_ppt.py 中已有示例文字
USE_IMAGES = False  # 不使用圖片
```

直接運行即可！

#### 選項 B：添加自己的內容

**準備文字：**

編輯 `ai_html_to_ppt.py`：

```python
TEXT_CONTENT = """
你的簡報標題

你的內容...
- 要點 1
- 要點 2
...
"""
```

**準備圖片（可選）：**

```bash
mkdir -p downloaded_images
# 將圖片放入這個目錄
cp your_images/*.jpg downloaded_images/
```

啟用圖片：
```python
USE_IMAGES = True
```

### 4️⃣ 生成簡報

```bash
# 生成 HTML（含 JSON 數據）
python ai_html_to_ppt.py

# 轉換為 PPTX
python convert_html_to_pptx.py
```

### 5️⃣ 查看結果

- **HTML**：用瀏覽器打開 `*_presentation.html`
- **PPTX**：用 PowerPoint 打開 `*.pptx`

## 🎯 第一次運行示例

```bash
# 1. 確保在項目目錄
cd auto-ppt

# 2. 生成示例簡報
python ai_html_to_ppt.py

# 輸出類似：
# 🎨 AI 驅動的 HTML → PPTX 生成器（重構版）
# ============================================================
# 📊 已註冊的 Slide 類型：opening, section_divider, ...
# ============================================================
# 
# 🤖 AI 分析內容並生成簡報結構...
#    ✓ AI 分析完成
#    📊 Token 使用：...
# 
# 📋 簡報資訊：
#    標題：探索日本北陸的自然奇觀與文化精粹
#    主題：...
#    幻燈片數量：12
# 
# 🎨 生成 HTML 演示文稿...
#    ✓ HTML 已保存：..._presentation.html
# 
# ✅ 生成完成！

# 3. 轉換為 PPTX
python convert_html_to_pptx.py

# 輸出類似：
# 🎨 HTML → PPTX 轉換器
# ...
# ✅ PPTX 已保存：探索日本北陸的自然奇觀與文化精粹.pptx
```

## 📝 常見問題

### Q: API Key 錯誤？

```bash
# 檢查 .env 文件
cat .env

# 確保格式正確（無引號）
GEMINI_API_KEY=AIza...
```

### Q: 模組未找到？

```bash
# 重新安裝依賴
uv sync
# 或
pip install -e .
```

### Q: 圖片未顯示？

```bash
# 檢查圖片目錄
ls downloaded_images/

# 確保路徑正確
# 圖片應該直接在 downloaded_images/ 目錄下
```

### Q: 生成的簡報不符合預期？

調整 `ai_html_to_ppt.py` 中的 prompt：

```python
prompt = f"""
...
**要求**：
1. 自動分析內容，識別2-4個主題  # 調整主題數
2. 每個主題有章節分隔頁
3. 合理安排圖片（如有）
4. 總共10-15張幻燈片  # 調整頁數
"""
```

## 🎨 下一步

- 📖 閱讀 [README.md](README.md) 了解完整功能
- 🔧 查看 [擴展指南](cursor_agent_md/EXTENSIBILITY_GUIDE.md) 學習如何添加新類型
- 🎯 運行 `python test_refactored.py` 查看測試

## 💡 提示

1. **第一次生成較慢**
   - AI 需要分析內容
   - 圖片需要上傳
   - 耐心等待 30-60 秒

2. **HTML 預覽**
   - 用瀏覽器打開 HTML 文件
   - 可以預覽所有幻燈片
   - 使用鍵盤方向鍵切換

3. **修改樣式**
   - 顏色、字體、佈局都可在 `slide_types.py` 中調整
   - 修改後重新運行 `python convert_html_to_pptx.py` 即可

4. **保存中間結果**
   - JSON 數據文件：`*_data.json`
   - 可以手動編輯後再轉換
   - 無需重新調用 AI

## 🎉 成功！

現在你已經掌握了 Auto-PPT 的基本使用！

試試創建你自己的第一份 AI 生成的簡報吧！ 🚀
