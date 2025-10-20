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
import random
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types

from AutoPPT.scrapy import SyncScrapyPlaywright

from .slide_generator import HTMLGenerator, PPTXGenerator
from .slide_types import SlideTypeRegistry

load_dotenv()


def get_random_filename_prefix() -> str:
    return f"{random.randint(100000, 999999)}"


class AutoPPT:
    """AI 驅動的自動簡報生成器"""

    def __init__(
        self,
        api_key: str,
        use_images: bool = False,
        output_dir: str = "temp_dir",
        scrapy: SyncScrapyPlaywright = None,
    ):
        """
        初始化 AutoPPT

        Args:
            api_key: Google Gemini API Key
            use_images: 是否使用圖片資源
        """
        self.client = genai.Client(api_key=api_key)
        self.use_images = use_images
        self.image_metadata = {}
        self.image_files = []
        self.text_content_files = []
        self.save_output_dir = os.path.join(output_dir, "output")
        self.save_content_dir = os.path.join(output_dir, "content")
        self.save_image_dir = os.path.join(output_dir, "images")
        if not os.path.exists(self.save_output_dir):
            os.makedirs(self.save_output_dir)
        if not os.path.exists(self.save_content_dir):
            os.makedirs(self.save_content_dir)
        if not os.path.exists(self.save_image_dir):
            os.makedirs(self.save_image_dir)
        self.random_filename_prefix = get_random_filename_prefix()
        self.scrapy = scrapy or SyncScrapyPlaywright()

    def load_images(self):
        """載入圖片資源"""
        if not self.use_images or not os.path.exists(self.save_image_dir):
            return

        print("\n📸 載入圖片資源...")
        for index, file in enumerate(sorted(os.listdir(self.save_image_dir))):
            if file.endswith(('.jpg', '.jpeg', '.png')):
                image_file = self.client.files.upload(
                    file=f"{self.save_image_dir}/{file}"
                )
                print(f"   ✓ 上傳圖片 {index + 1}: {file}")

                image_id = f"img_{index+1:02d}"
                self.image_files.append(image_file)
                self.image_metadata[image_id] = {
                    "filename": file,
                    "path": f"{self.save_image_dir}/{file}",
                    "gemini_file": image_file,
                    "index": index + 1,
                }

    def generate_prompt(self, prompt: str) -> str:
        """生成 AI Prompt"""
        # 圖片列表信息
        image_list_info = (
            "\n".join(
                [
                    f"- {img_id}: {data['filename']}"
                    for img_id, data in self.image_metadata.items()
                ]
            )
            if self.image_metadata
            else "無圖片資源（純文字簡報）"
        )

        # 動態生成 JSON 示例
        json_examples = SlideTypeRegistry.get_all_json_examples()
        slides_examples_str = ",\n    ".join(
            [
                json.dumps(example, ensure_ascii=False, indent=2).replace(
                    "\n", "\n    "
                )
                for example in json_examples
            ]
        )

        # 動態生成類型說明
        descriptions = SlideTypeRegistry.get_all_descriptions()
        descriptions_str = "\n".join(
            [
                f"- {slide_type}: {description}"
                for slide_type, description in descriptions.items()
            ]
        )

        return f"""請分析以下內容，生成一個結構化的演示文稿（適合 HTML 格式）。

**使用者輸入**
{prompt}

**文字內容**：
請讀取我上傳的檔案，當作其內容。

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

    def generate_presentation(
        self, contents: List[str], model: str = "gemini-2.5-flash"
    ) -> Dict:
        """
        使用 AI 生成簡報結構

        Args:
            contents: 內容列表
            model: AI 模型名稱

        Returns:
            簡報數據（dict）
        """
        print("\n🤖 AI 分析內容並生成簡報結構...")

        # 調用 AI
        response = self.client.models.generate_content(
            model=model,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
            contents=contents,
        )

        print("   ✓ AI 分析完成")
        print(f"   📊 Token 使用：{response.usage_metadata}")

        # 解析結果
        ai_data = json.loads(response.text)

        print(f"\n📋 簡報資訊：")
        print(f"   標題：{ai_data.get('title', '')}")
        print(f"   主題：{ai_data.get('topic', '')}")
        print(f"   幻燈片數量：{len(ai_data.get('slides', []))}")

        return ai_data

    def upload_files(self, files: List[str]) -> List[str]:
        """上傳檔案"""
        uploaded_files = []
        for file in files:
            if os.path.exists(file):
                uploaded_file = self.client.files.upload(file=file)
            else:
                print(f"   ❌ 檔案不存在：{file}")
                continue
            uploaded_files.append(uploaded_file)
            print(f"   ✓ 已上傳檔案：{file}")
        return uploaded_files

    def scrape_url(self, url: str) -> None:
        """爬取 URL"""

        uid = uuid.uuid4()
        content_file = os.path.join(self.save_content_dir, f"{uid}.txt")
        self.scrapy.start(
            target_url=url,
            extracted_content_file=content_file,
            images_downloaded_dir=self.save_image_dir,
        )
        self.text_content_files.append(content_file)
        print(f"   ✓ 已爬取 URL：{url} 並保存到 {content_file}")

    def save_html(self, data: Dict, filename: str = None) -> str:
        """保存 HTML 文件"""
        print("\n🎨 生成 HTML 演示文稿...")

        html_gen = HTMLGenerator(self.image_metadata)
        html_content = html_gen.generate_from_data(data)

        # 生成文件名
        if not filename:
            filename = os.path.join(
                self.save_output_dir,
                f"{self.random_filename_prefix}_{data['topic']}_presentation.html",
            )

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"   ✓ HTML 已保存：{filename}")
        print(f"\n🌐 請在瀏覽器中打開：")
        print(f"   file://{os.path.abspath(filename)}")

        return filename

    def save_json(self, data: Dict, filename: str = None) -> str:
        """保存 JSON 數據文件"""
        if not filename:
            filename = os.path.join(
                self.save_output_dir,
                f"{self.random_filename_prefix}_{data['topic']}_data.json",
            )

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n💾 數據已保存：{filename}")
        print(f"   （可用於後續轉換為 PPTX）")

        return filename

    def save_pptx(self, data: Dict, filename: str = None) -> str:
        """保存 PPTX 文件"""
        print("\n📊 生成 PPTX 演示文稿...")

        pptx_gen = PPTXGenerator(self.image_metadata)
        prs = pptx_gen.generate_from_data(data)

        # 生成文件名
        if not filename:
            filename = os.path.join(
                self.save_output_dir,
                f"{self.random_filename_prefix}_{data['topic']}.pptx",
            )

        prs.save(filename)

        print(f"   ✓ PPTX 已保存：{filename}")

        return filename

    def generate(
        self,
        prompt: str,
        save_files: bool = True,
        url_links: Optional[List[str]] = None,
        other_files: List[str] = [],
    ) -> Dict:
        """
        完整的簡報生成流程

        Args:
            prompt: 提示詞
            save_files: 是否保存文件
            url_links: 網頁連結列表（可選）
            other_files: 其他檔案列表（默認空列表）

        Returns:
            簡報數據（dict）
        """
        try:
            # 爬蟲
            if url_links:
                for url in url_links:
                    self.scrape_url(url)

            # 載入圖片
            self.load_images()

            # 準備內容
            contents = [
                self.generate_prompt(prompt),
                *self.image_files,
                *self.upload_files(other_files + self.text_content_files),
            ]

            # 生成簡報結構
            data = self.generate_presentation(contents)

            # 保存文件
            if save_files:
                self.save_html(data)
                self.save_json(data)
                self.save_pptx(data)

            print("\n" + "=" * 60)
            print("✅ 生成完成！")
            print("💡 提示：")
            print("   - 在瀏覽器中預覽 HTML")
            print("   - 使用 PowerPoint 打開 PPTX 文件")
            print("   - JSON 數據可用於後續處理")
            print("=" * 60)

            return data

        except json.JSONDecodeError as e:
            print(f"\n❌ JSON 解析錯誤：{e}")
            raise
        except Exception as e:
            print(f"\n❌ 發生錯誤：{e}")
            import traceback

            traceback.print_exc()
            raise
