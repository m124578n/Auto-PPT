"""
AI 驅動的 HTML → PPTX 生成器（重構版）

流程：內容分析 → 生成 HTML → 瀏覽器預覽 → 轉換 PPTX

優化點：
1. 使用 Strategy Pattern，slide 類型解耦
2. HTML 和 PPTX 生成邏輯統一在 slide_types.py
3. 新增 slide 類型只需添加新的 SlideType 子類
"""

import json
import os
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv
from google import genai
from google.genai import types

from slide_generator import HTMLGenerator
from slide_types import SlideTypeRegistry

load_dotenv()
# ==================== 配置 ====================
API_KEY = os.getenv("GEMINI_API_KEY")

# 文字內容
TEXT_CONTENT = """
APP獨享！日本黑部立山絕景
輸碼【Hokuriku1000】現折1千
省最大北陸旅遊｜立山雪壁絕景x粉紅芝櫻花毯！合掌村.兼六園.打卡秘境～奈良井宿.犬山城.信州牛壽喜燒.福朋喜來登溫泉六日

☆ 北陸年度限定 震撼２個月 ☆
★ 立山黑部雪壁奇景ｘ粉紅芝櫻花毯 ★

特別安排：
★ 特別安排搭乘六項交通工具～登上【立山黑部】漫步雪牆森呼吸
★ 期間限定！天空花迴廊【２０２５茶臼山高原芝櫻祭】
★ 打卡秘境景點・跟團最方便～【奈良井宿】
★ 世界文化遺產【白川鄉合掌村】、日本三大名園【兼六園】
★ 日本國寶【犬山城】
★ 【三光稻荷神社】

特色餐食：
★信州牛&長野地產菇菇壽喜燒御膳
★岐阜名物~朴葉味噌燒飛驒牛料理

出發日期：2025/05/12 - 2025/05/31
價格：TWD 43,900 - 47,900

行程安排：
DAY 1: 台北 → 名古屋中部國際機場
DAY 2: 世界文化遺產【白川鄉合掌村】→ 日本三大名園【兼六園】→ 金澤城跡
DAY 3: 立山黑部阿爾卑斯路線 - 搭乘六種交通工具登山
DAY 4: 【奈良井宿】→ 【茶臼山高原芝櫻祭】→ 名古屋市區
DAY 5: 【熱田神宮】→ 【三光稻荷神社】→ 【犬山城】→ 常滑購物中心
DAY 6: 名古屋中部國際機場 → 台北
"""

USE_IMAGES = True


# ==================== 主程序 ====================
def main():
    print("🎨 AI 驅動的 HTML → PPTX 生成器（重構版）")
    print("=" * 60)
    print(f"📊 已註冊的 Slide 類型：{', '.join(SlideTypeRegistry.all_types())}")
    print("=" * 60)
    
    # 初始化 AI 客戶端
    client = genai.Client(api_key=API_KEY)
    
    # 載入圖片
    image_files = []
    image_metadata = {}
    
    if USE_IMAGES and os.path.exists("downloaded_images"):
        print("\n📸 載入圖片資源...")
        for index, file in enumerate(sorted(os.listdir("downloaded_images"))):
            if file.endswith(('.jpg', '.jpeg', '.png')):
                image_file = client.files.upload(file=f"downloaded_images/{file}")
                print(f"   ✓ 上傳圖片 {index + 1}: {file}")
                
                image_id = f"img_{index+1:02d}"
                image_files.append(image_file)
                image_metadata[image_id] = {
                    "filename": file,
                    "path": f"downloaded_images/{file}",
                    "gemini_file": image_file,
                    "index": index + 1,
                }
    
    image_list_info = "\n".join(
        [f"- {img_id}: {data['filename']}" for img_id, data in image_metadata.items()]
    ) if image_metadata else "無圖片資源（純文字簡報）"

    # AI 生成簡報結構
    print("\n🤖 AI 分析內容並生成簡報結構...")
    
    # 動態生成 JSON 示例
    json_examples = SlideTypeRegistry.get_all_json_examples()
    slides_examples_str = ",\n    ".join([
        json.dumps(example, ensure_ascii=False, indent=2).replace('\n', '\n    ')
        for example in json_examples
    ])
    
    # 動態生成類型說明
    descriptions = SlideTypeRegistry.get_all_descriptions()
    descriptions_str = "\n".join([
        f"- {slide_type}: {description}"
        for slide_type, description in descriptions.items()
    ])
    
    prompt = f"""請分析以下內容，生成一個結構化的演示文稿（適合 HTML 格式）。

**文字內容**：
{TEXT_CONTENT}

**可用圖片**：
{image_list_info}

**輸出 JSON 格式**：
{{
  "title": "簡報標題",
  "topic": "簡報主題",
  "slides": [
    {slides_examples_str}
  ]
}}

**可用的 slide 類型說明**：
{descriptions_str}

**要求**：
1. 自動分析內容，識別2-4個主題
2. 每個主題有章節分隔頁
3. 合理安排圖片（如有）
4. 總共10-15張幻燈片
"""
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
        contents=[prompt, *image_files]
    )
    
    print("   ✓ AI 分析完成")
    print(f"   📊 Token 使用：{response.usage_metadata}")
    
    # 解析 AI 回應
    try:
        ai_data = json.loads(response.text)
        
        print(f"\n📋 簡報資訊：")
        print(f"   標題：{ai_data.get('title', '')}")
        print(f"   主題：{ai_data.get('topic', '')}")
        print(f"   幻燈片數量：{len(ai_data.get('slides', []))}")
        
        # 生成 HTML
        print("\n🎨 生成 HTML 演示文稿...")
        html_gen = HTMLGenerator(image_metadata)
        html_content = html_gen.generate_from_data(ai_data)
        
        # 保存 HTML
        html_filename = f"{ai_data['topic'].replace(' ', '_')}_presentation.html"
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"   ✓ HTML 已保存：{html_filename}")
        print(f"\n🌐 請在瀏覽器中打開：")
        print(f"   file://{os.path.abspath(html_filename)}")
        
        # 保存 JSON（供轉換 PPTX 使用）
        json_filename = f"{ai_data['topic'].replace(' ', '_')}_data.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(ai_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 數據已保存：{json_filename}")
        print(f"   （可用於後續轉換為 PPTX）")
        
        print("\n" + "=" * 60)
        print("✅ 生成完成！")
        print("💡 提示：")
        print("   - 在瀏覽器中預覽 HTML")
        print("   - 使用方向鍵或點擊按鈕切換幻燈片")
        print("   - 運行 convert_html_to_pptx.py 轉換為 PPTX 格式")
        print("=" * 60)
        
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON 解析錯誤：{e}")
        print(f"原始回應：{response.text}")
    except Exception as e:
        print(f"\n❌ 發生錯誤：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

