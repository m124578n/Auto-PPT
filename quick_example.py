#!/usr/bin/env python3
"""
AutoPPT 快速示例 - 一鍵生成完整簡報（HTML + JSON + PPTX）
"""

from ai_html_to_ppt import AutoPPT
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

# 你的簡報內容
CONTENT = """
產品發表會

核心亮點：
- 創新設計理念
- 卓越性能表現  
- 超值性價比

技術規格：
- 處理器：最新 AI 晶片
- 記憶體：16GB RAM
- 儲存：512GB SSD
"""

def main():
    print("🎨 AutoPPT 快速示例\n")
    print("=" * 60)
    
    # 初始化 AutoPPT
    auto_ppt = AutoPPT(
        api_key=os.getenv("GEMINI_API_KEY"),
        use_images=False  # 是否使用圖片
    )
    
    # 一鍵生成所有格式（HTML + JSON + PPTX）
    data = auto_ppt.generate(
        text_content=CONTENT,
        pdf_file=None,  # 如果有 PDF 就填路徑
        save_files=True  # 自動保存所有格式
    )
    
    print("\n✅ 成功生成：")
    print(f"   - {data['topic']}_presentation.html")
    print(f"   - {data['topic']}_data.json")
    print(f"   - {data['topic']}.pptx")
    print("\n💡 使用說明：")
    print("   1. 在瀏覽器中打開 HTML 預覽")
    print("   2. 使用 PowerPoint 打開 PPTX 文件")
    print("   3. JSON 可用於後續處理")
    print("=" * 60)

if __name__ == "__main__":
    main()
