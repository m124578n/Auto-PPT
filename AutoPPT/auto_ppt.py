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
from AutoPPT.slide_generator import HTMLGenerator, PPTXGenerator
from AutoPPT.template_engine import PPTXTemplate
from AutoPPT.utils.logger import get_logger

# 获取日志器
logger = get_logger()

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
        template_path: str = None,
    ):
        """
        初始化 AutoPPT

        Args:
            api_key: Google Gemini API Key
            use_images: 是否使用圖片資源
            output_dir: 輸出目錄
            scrapy: 爬蟲實例
            template_path: 模板 JSON 文件路徑（可選）
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

        # 加載模板
        self.template = PPTXTemplate(template_path)
        logger.info(f"   🎨 模板：{self.template}")

    def load_images(self):
        """載入圖片資源"""
        if not self.use_images or not os.path.exists(self.save_image_dir):
            return

        logger.info("📸 載入圖片資源...")
        for index, file in enumerate(sorted(os.listdir(self.save_image_dir))):
            if file.endswith(('.jpg', '.jpeg', '.png')):
                image_file = self.client.files.upload(
                    file=f"{self.save_image_dir}/{file}"
                )
                logger.info(f"   ✓ 上傳圖片 {index + 1}: {file}")

                image_id = f"img_{index+1:02d}"
                self.image_files.append(image_file)
                self.image_metadata[image_id] = {
                    "filename": file,
                    "path": f"{self.save_image_dir}/{file}",
                    "gemini_file": image_file,
                    "index": index + 1,
                }

    def generate_prompt(self, prompt: str) -> str:
        """生成 AI Prompt（使用模板引擎）"""
        return self.template.generate_ai_prompt(
            image_metadata=self.image_metadata, user_prompt=prompt
        )

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
        # 列出template的slide_types
        logger.info(f"🤖 模板：{self.template.slide_types.keys()}")
        logger.info("🤖 AI 分析內容並生成簡報結構...")

        # 調用 AI
        response = self.client.models.generate_content(
            model=model,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
            contents=contents,
        )

        logger.info("   ✓ AI 分析完成")
        logger.info(f"   📊 Token 使用：{response.usage_metadata}")

        # 解析結果
        ai_data = json.loads(response.text)

        logger.info(f"   📋 簡報資訊：")
        logger.info(f"   標題：{ai_data.get('title', '')}")
        logger.info(f"   主題：{ai_data.get('topic', '')}")
        logger.info(f"   幻燈片數量：{len(ai_data.get('slides', []))}")

        return ai_data

    def upload_files(self, files: List[str]) -> List[str]:
        """上傳檔案"""
        uploaded_files = []
        for file in files:
            if os.path.exists(file):
                uploaded_file = self.client.files.upload(file=file)
            else:
                logger.info(f"   ❌ 檔案不存在：{file}")
                continue
            uploaded_files.append(uploaded_file)
            logger.info(f"   ✓ 已上傳檔案：{file}")
        return uploaded_files

    def scrape_urls(self, urls: List[str]) -> None:
        """爬取 URL"""
        if not urls:
            return
        logger.info(f"🌐 開始爬取 {len(urls)} 個 URL...")
        for url in urls:
            uid = uuid.uuid4()
            content_file = os.path.join(self.save_content_dir, f"{uid}.txt")
            self.scrapy.start(
                target_url=url,
                extracted_content_file=content_file,
                images_downloaded_dir=self.save_image_dir,
            )
            self.text_content_files.append(content_file)
            logger.info(f"   ✓ 已爬取 URL：{url} 並保存到 {content_file}")

    def save_html(self, data: Dict, filename: str = None) -> str:
        """保存 HTML 文件"""
        logger.info("🎨 生成 HTML 演示文稿...")

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

        logger.info(f"   ✓ HTML 已保存：{filename}")
        logger.info(f"   🌐 請在瀏覽器中打開：")
        logger.info(f"   file://{os.path.abspath(filename)}")

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

        logger.info(f"   💾 數據已保存：{filename}")
        logger.info(f"   （可用於後續轉換為 PPTX）")

        return filename

    def save_pptx(self, data: Dict, filename: str = None) -> str:
        """保存 PPTX 文件（使用模板引擎）"""
        logger.info("📊 生成 PPTX 演示文稿...")

        pptx_gen = PPTXGenerator(self.image_metadata, template=self.template)
        prs = pptx_gen.generate_from_data(data)

        # 生成文件名
        if not filename:
            filename = os.path.join(
                self.save_output_dir,
                f"{self.random_filename_prefix}_{data['topic']}.pptx",
            )

        prs.save(filename)

        logger.info(f"   ✓ PPTX 已保存：{filename}")

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
            self.scrape_urls(url_links)

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

            logger.info("=" * 60)
            logger.info("✅ 生成完成！")
            logger.info("💡 提示：")
            logger.info("   - 在瀏覽器中預覽 HTML")
            logger.info("   - 使用 PowerPoint 打開 PPTX 文件")
            logger.info("   - JSON 數據可用於後續處理")
            logger.info("=" * 60)

            return data

        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON 解析錯誤：{e}")
            raise
        except Exception as e:
            logger.error(f"❌ 發生錯誤：{e}")
            import traceback

            logger.error(f"異常詳情: {traceback.format_exc()}")
            raise
