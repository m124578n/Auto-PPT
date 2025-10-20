import asyncio
import os
import tempfile

from dotenv import load_dotenv

from AutoPPT import AutoPPT
from AutoPPT.scrapy import AsyncScrapyPlaywright
from AutoPPT.slide_types import SlideTypeRegistry

load_dotenv()

# ==================== 配置 ====================
API_KEY = os.getenv("GEMINI_API_KEY")

# 文字內容
TEXT_CONTENT = "請根據我提供的pdf當成content來生成簡報"
# TEXT_CONTENT = """
# APP獨享！日本黑部立山絕景
# 輸碼【Hokuriku1000】現折1千
# 省最大北陸旅遊｜立山雪壁絕景x粉紅芝櫻花毯！合掌村.兼六園.打卡秘境～奈良井宿.犬山城.信州牛壽喜燒.福朋喜來登溫泉六日

# ☆ 北陸年度限定 震撼２個月 ☆
# ★ 立山黑部雪壁奇景ｘ粉紅芝櫻花毯 ★

# 特別安排：
# ★ 特別安排搭乘六項交通工具～登上【立山黑部】漫步雪牆森呼吸
# ★ 期間限定！天空花迴廊【２０２５茶臼山高原芝櫻祭】
# ★ 打卡秘境景點・跟團最方便～【奈良井宿】
# ★ 世界文化遺產【白川鄉合掌村】、日本三大名園【兼六園】
# ★ 日本國寶【犬山城】
# ★ 【三光稻荷神社】

# 特色餐食：
# ★信州牛&長野地產菇菇壽喜燒御膳
# ★岐阜名物~朴葉味噌燒飛驒牛料理

# 出發日期：2025/05/12 - 2025/05/31
# 價格：TWD 43,900 - 47,900

# 行程安排：
# DAY 1: 台北 → 名古屋中部國際機場
# DAY 2: 世界文化遺產【白川鄉合掌村】→ 日本三大名園【兼六園】→ 金澤城跡
# DAY 3: 立山黑部阿爾卑斯路線 - 搭乘六種交通工具登山
# DAY 4: 【奈良井宿】→ 【茶臼山高原芝櫻祭】→ 名古屋市區
# DAY 5: 【熱田神宮】→ 【三光稻荷神社】→ 【犬山城】→ 常滑購物中心
# DAY 6: 名古屋中部國際機場 → 台北
# """

USE_IMAGES = True


# ==================== 主程序 ====================
def main():
    """使用 AutoPPT 類的簡化主程序"""
    print("🎨 AI 驅動的 HTML → PPTX 生成器（重構版）")
    print("=" * 60)
    print(f"📊 已註冊的 Slide 類型：{', '.join(SlideTypeRegistry.all_types())}")
    print("=" * 60)

    # 初始化 AutoPPT
    tempfile_dir = tempfile.mkdtemp(dir="temp_dir")
    auto_ppt = AutoPPT(api_key=API_KEY, use_images=USE_IMAGES, output_dir=tempfile_dir)

    # 生成簡報（可選擇是否使用 PDF）
    pdf_file = (
        "投資月報_20250930.pdf" if os.path.exists("投資月報_20250930.pdf") else None
    )

    auto_ppt.generate(prompt=TEXT_CONTENT, other_files=[pdf_file], save_files=True)


def scrapy_and_generate():
    prompt = "請幫我統整這兩個旅遊的行程, 並生成簡報"
    tempfile_dir = tempfile.mkdtemp(dir="temp_dir")
    auto_ppt = AutoPPT(api_key=API_KEY, use_images=USE_IMAGES, output_dir=tempfile_dir)
    auto_ppt.generate(
        prompt=prompt,
        save_files=True,
        url_links=[
            "https://travel.liontravel.com/detail?NormGroupID=8a2fd4bf-0b87-4e5c-9c6b-3a38d81362af&GroupID=25XMD28CX-T&Platform=APP",
            "https://travel.liontravel.com/detail?NormGroupID=a854db3d-5df3-4bff-9dd4-f022f0d6d565&GroupID=25XMD29EK5-T&Platform=APP",
        ],
    )


if __name__ == "__main__":
    # main()
    scrapy_and_generate()
