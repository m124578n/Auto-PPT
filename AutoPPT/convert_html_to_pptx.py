"""
HTML → PPTX 轉換器（重構版）

優化點：
1. 使用統一的 slide_generator 模組
2. 支持兩種模式：
   - JSON → PPTX（推薦）
   - HTML → PPTX（向後兼容）
3. 新增 slide 類型不需修改此文件
"""

import json
import os

from pptx import Presentation
from slide_generator import HTMLToPPTXParser, PPTXGenerator
from slide_types import SlideTypeRegistry

from AutoPPT import logger


def convert_from_json(json_file: str, output_file: str = None):
    """從 JSON 數據生成 PPTX（推薦方式）"""
    logger.info(f"\n📂 讀取 JSON 數據：{json_file}")

    with open(json_file, 'r', encoding='utf-8') as f:
        ai_data = json.load(f)

    logger.info(f"   ✓ 已載入數據")
    logger.info(f"   標題：{ai_data.get('title', '')}")
    logger.info(f"   幻燈片數量：{len(ai_data.get('slides', []))}")

    # 建立圖片 metadata（如果需要）
    image_metadata = {}
    if os.path.exists("downloaded_images"):
        for index, file in enumerate(sorted(os.listdir("downloaded_images"))):
            if file.endswith(('.jpg', '.jpeg', '.png')):
                image_id = f"img_{index+1:02d}"
                image_metadata[image_id] = {
                    "filename": file,
                    "path": f"downloaded_images/{file}",
                    "index": index + 1,
                }

    # 生成 PPTX
    logger.info("\n🎨 生成 PPTX...")
    generator = PPTXGenerator(image_metadata)
    prs = generator.generate_from_data(ai_data)

    # 保存
    if not output_file:
        output_file = json_file.replace('_data.json', '.pptx')

    generator.save(output_file)

    # 驗證
    verify_pptx(output_file)


def convert_from_html(html_file: str, output_file: str = None):
    """從 HTML 文件轉換為 PPTX（向後兼容）"""
    logger.info(f"\n⚠️ 使用舊版 HTML → PPTX 轉換")
    logger.info(f"   建議使用 JSON → PPTX 轉換以獲得更好的效果")

    # 建立圖片 metadata（如果需要）
    image_metadata = {}
    if os.path.exists("downloaded_images"):
        for file in os.listdir("downloaded_images"):
            if file.endswith(('.jpg', '.jpeg', '.png')):
                # 對於 HTML 轉換，直接使用文件路徑作為 key
                image_metadata[f"downloaded_images/{file}"] = {
                    "filename": file,
                    "path": f"downloaded_images/{file}",
                }

    # 解析並轉換
    parser = HTMLToPPTXParser(image_metadata)
    parser.parse_html_file(html_file)

    # 保存
    if not output_file:
        output_file = html_file.replace('_presentation.html', '.pptx')

    parser.save(output_file)

    # 驗證
    verify_pptx(output_file)


def verify_pptx(output_file: str):
    """驗證生成的 PPTX 文件"""
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        logger.info(f"\n📦 檔案資訊：")
        logger.info(f"   路徑：{os.path.abspath(output_file)}")
        logger.info(f"   大小：{file_size:,} bytes ({file_size/1024/1024:.2f} MB)")

        try:
            verify_prs = Presentation(output_file)
            logger.info(f"   幻燈片數：{len(verify_prs.slides)}")
        except Exception as e:
            logger.info(f"   ⚠️ 驗證失敗：{e}")


def main():
    logger.info("🔄 HTML → PPTX 轉換器（重構版）")
    logger.info("=" * 60)
    logger.info(f"📊 支援的 Slide 類型：{', '.join(SlideTypeRegistry.all_types())}")
    logger.info("=" * 60)

    # 尋找可轉換的文件
    json_files = [f for f in os.listdir(".") if f.endswith("_data.json")]
    html_files = [f for f in os.listdir(".") if f.endswith("_presentation.html")]

    if not json_files and not html_files:
        logger.info("\n❌ 找不到可轉換的文件")
        logger.info("   請確保存在以下文件之一：")
        logger.info("   - *_data.json (推薦)")
        logger.info("   - *_presentation.html")
        return

    # 優先使用 JSON
    if json_files:
        logger.info(f"\n✅ 找到 {len(json_files)} 個 JSON 數據文件")

        if len(json_files) > 1:
            logger.info("\n📋 可用的 JSON 文件：")
            for i, f in enumerate(json_files, 1):
                logger.info(f"   {i}. {f}")

            choice = input("\n請選擇要轉換的文件編號（直接按 Enter 選擇第一個）: ").strip()

            if choice and choice.isdigit() and 1 <= int(choice) <= len(json_files):
                json_file = json_files[int(choice) - 1]
            else:
                json_file = json_files[0]
        else:
            json_file = json_files[0]

        logger.info(f"\n📂 選擇的文件：{json_file}")
        convert_from_json(json_file)

    elif html_files:
        logger.info(f"\n⚠️ 只找到 HTML 文件（建議使用 JSON 方式）")

        if len(html_files) > 1:
            logger.info("\n📋 可用的 HTML 文件：")
            for i, f in enumerate(html_files, 1):
                logger.info(f"   {i}. {f}")

            choice = input("\n請選擇要轉換的文件編號（直接按 Enter 選擇第一個）: ").strip()

            if choice and choice.isdigit() and 1 <= int(choice) <= len(html_files):
                html_file = html_files[int(choice) - 1]
            else:
                html_file = html_files[0]
        else:
            html_file = html_files[0]

        logger.info(f"\n📂 選擇的文件：{html_file}")
        convert_from_html(html_file)

    logger.info("\n" + "=" * 60)
    logger.info("✅ 轉換完成！")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
