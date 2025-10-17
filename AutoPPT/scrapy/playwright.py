import asyncio
import base64
import hashlib
import io
import json
import os
import random
import re
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse

import aiofiles
import numpy as np
import requests
from bs4 import BeautifulSoup, Comment
from fake_useragent import UserAgent
from PIL import Image
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

from AutoPPT.scrapy.base_scrapy import BaseScrapy


class SimpleProxyManager:
    def __init__(self):
        # 代理列表，您可以添加更多
        # TODO 自己去找尋可用的代理
        self.proxies = [
            "52.188.28.218:3128",
            "176.126.103.194:44214",
            "14.235.71.53:8080",
            "190.242.157.215:8080",
            "8.243.68.10:8080",
            "185.112.151.207:8022",
            "103.242.104.149:8080",
            "190.242.157.215:8080",
        ]
        self.current_index = 0

    def get_random_proxy(self):
        """獲取隨機代理"""
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    def get_next_proxy(self):
        """按順序獲取下一個代理"""
        if not self.proxies:
            return None
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy

    def test_proxy(self, proxy, target_url):
        """簡單測試代理是否可用"""
        import requests

        try:
            proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            response = requests.get(target_url, proxies=proxies, timeout=10)
            if response.status_code == 200:
                print(f"代理測試成功: {proxy}")
                return True
        except Exception as e:
            print(f"代理測試失敗: {proxy} - {e}")
        return False


class HTMLTextExtractor:
    def __init__(self):
        # 要排除的標籤
        self.exclude_tags: Set[str] = {
            "header",
            "nav",
            "script",
            "style",
            "noscript",
            # "iframe",
            "footer",
            "dialog",
            "modal",
        }

        # 要排除的 class 關鍵字（部分匹配）
        self.exclude_class_keywords: Set[str] = {
            "header",
            "nav",
            "footer",
            "menu",
            "navigation",
            "popup",
            "modal",
            "dialog",
            "overlay",
            "lightbox",
            "tooltip",
            "drawer",
            "category",
        }

        # 要排除的 id 關鍵字（部分匹配）
        self.exclude_id_keywords: Set[str] = {
            "header",
            "nav",
            "footer",
            "navigation",
            "popup",
            "modal",
            "dialog",
            "overlay",
        }

        # 新增：要排除的路徑關鍵字
        self.exclude_path_keywords: Set[str] = {
            "header",
            "nav",
            "footer",
            "menu",
            "navigation",
            "popup",
            "modal",
            "dialog",
            "overlay",
            "lightbox",
            "tooltip",
            "drawer",
            "category",
            "breadcrumb",  # 常見的麵包屑導航
            "sidebar",  # 側邊欄
            "banner",  # 橫幅
            "advertisement",  # 廣告
            "headcontent",  # 頭部內容
        }

        # 最小文字長度
        self.min_text_length: int = 2

        # 新增：圖片保存路徑
        self.image_dir = "downloaded_images"

        # 新增：圖片檢查閾值
        self.color_threshold = 30  # 判斷黑白的閾值（0-255）
        self.uniformity_threshold = 0.8  # 判斷均勻度的閾值（0-1）

    def has_excluded_class(self, element) -> bool:
        """檢查元素是否包含需要排除的 class"""
        if element.get("class"):
            # 將所有 class 合併成一個字串，轉換為小寫
            class_string = " ".join(element.get("class")).lower()
            # 檢查是否包含任何排除關鍵字
            return any(
                exclude_keyword in class_string
                for exclude_keyword in self.exclude_class_keywords
            )
        return False

    def should_keep_element(self, element) -> bool:
        """判斷是否保留該元素"""
        if not element.parent:
            return False

        if element.parent and isinstance(element, Comment):
            return False

        # 檢查元素的完整路徑
        element_path = self.get_element_path(element).lower()
        if any(keyword in element_path for keyword in self.exclude_path_keywords):
            return False

        # 檢查所有父元素
        for parent in element.parents:
            # 檢查標籤名
            if parent.name in self.exclude_tags:
                return False

            # # 檢查 class
            # if self.has_excluded_class(parent):
            #     return False

            # # 檢查 id
            # if parent.get("id"):
            #     if any(
            #         keyword in parent["id"].lower()
            #         for keyword in self.exclude_id_keywords
            #     ):
            #         return False

            # # 檢查 aria 屬性
            # if parent.get("role") in {"dialog", "alertdialog", "popup", "modal"}:
            #     return False

            # # 檢查 aria-modal 屬性
            # if parent.get("aria-modal") == "true":
            #     return False

            # # 檢查 style 屬性是否包含彈窗相關樣式
            # style = parent.get("style", "").lower()
            # if any(keyword in style for keyword in ["position: fixed", "position:fixed", "z-index:"]):
            #     return False

        return True

    def clean_text(self, text: str) -> str:
        """清理文字內容"""
        # 移除多餘空白
        return " ".join(text.split())

    def get_element_path(self, element) -> str:
        """獲取元素的路徑"""
        path_parts = []
        for parent in element.parents:
            if parent.name == "body":
                break
            if parent.name:
                part = parent.name
                if parent.get("id"):
                    part += f"#{parent['id']}"
                if parent.get("class"):
                    part += f".{'.'.join(parent['class'])}"
                path_parts.append(part)
        return " > ".join(reversed(path_parts))

    def is_uniform_image(self, img_data: bytes) -> bool:
        """檢查圖片是否全白或全黑"""
        try:
            # 從二進制數據創建圖片
            img = Image.open(io.BytesIO(img_data))

            # 轉換為灰度圖
            if img.mode != "L":
                img = img.convert("L")

            # 轉換為numpy數組以加快處理速度
            img_array = np.array(img)

            # 計算像素值的分布
            hist = np.histogram(img_array, bins=256, range=(0, 256))[0]
            total_pixels = img_array.size

            # 檢查暗色像素（接近黑色）
            dark_pixels = np.sum(hist[: self.color_threshold])
            if dark_pixels / total_pixels > self.uniformity_threshold:
                return True

            # 檢查亮色像素（接近白色）
            bright_pixels = np.sum(hist[255 - self.color_threshold :])
            if bright_pixels / total_pixels > self.uniformity_threshold:
                return True

            return False

        except Exception as e:
            print(f"圖片分析錯誤: {e}")
            return False

    def download_image(
        self,
        img_url: str,
        base_url: str,
        temp_dir: str,
        original_images_downloaded_dir: Optional[str] = None,
        proxy_request: Optional[dict] = None,
    ) -> Dict:
        """下載圖片並返回相關信息"""
        try:
            # 檢查是否為 base64 編碼的圖片
            if img_url.startswith("data:image"):
                try:
                    # 解析 base64 數據
                    header, encoded = img_url.split(",", 1)
                    img_data = base64.b64decode(encoded)

                    # 從 header 中獲取圖片格式
                    img_format = header.split(";")[0].split("/")[1]
                    # 只處理 .jpg 或 .jpeg 文件
                    if img_format not in [
                        ".jpg",
                        ".jpeg",
                        "jpg",
                        "jpeg",
                        ".webp",
                        "webp",
                    ]:
                        return {
                            "original_url": (
                                img_url[:100] + "..." if len(img_url) > 100 else img_url
                            ),
                            "status": "skipped",
                            "reason": f"not_jpg_format (format: {img_format})",
                        }

                    # 生成文件名
                    url_hash = hashlib.md5(encoded.encode()).hexdigest()
                    file_extension = f".{img_format}"

                except Exception as e:
                    return {
                        "original_url": "base64_image",
                        "error": f"Base64 解碼錯誤: {str(e)}",
                        "status": "failed",
                    }
            else:
                # 處理一般 URL
                full_url = (
                    img_url
                    if img_url.startswith(("http://", "https://"))
                    else urljoin(base_url, img_url)
                )

                # 使用URL的MD5作為文件名
                url_hash = hashlib.md5(full_url.encode()).hexdigest()
                file_extension = os.path.splitext(urlparse(full_url).path)[1].lower()
                print(f"full_url: {full_url}")
                # 只處理 .jpg 或 .jpeg 文件
                if file_extension not in [
                    ".jpg",
                    ".jpeg",
                    "jpg",
                    "jpeg",
                    ".webp",
                    "webp",
                ]:
                    return {
                        "original_url": (
                            img_url[:100] + "..." if len(img_url) > 100 else img_url
                        ),
                        "status": "skipped",
                        "reason": f"not_jpg_format (format: {file_extension})",
                    }

                else:
                    ua = UserAgent()
                    try:
                        # 下載其他格式的圖片
                        headers = {
                            "User-Agent": ua.random,
                        }
                        response = requests.get(
                            full_url, timeout=10, headers=headers, proxies=proxy_request
                        )
                        response.raise_for_status()
                        img_data = response.content
                        print(f"get")
                    except Exception as e:
                        print("first request failed")
                        headers = {
                            "User-Agent": ua.random,
                            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
                            "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Referer": base_url,
                            "Connection": "keep-alive",
                            "Upgrade-Insecure-Requests": "1",
                        }
                        response = requests.get(
                            full_url, timeout=10, headers=headers, proxies=proxy_request
                        )
                        response.raise_for_status()
                        img_data = response.content
                        print(f"second request success")

            filename = f"{url_hash}{file_extension}"
            original_filename = f"original_{url_hash}{file_extension}"
            filepath = os.path.join(temp_dir, filename)
            original_filepath = os.path.join(
                original_images_downloaded_dir, original_filename
            )

            # 如果文件已存在，直接返回信息
            if os.path.exists(filepath):
                print(f"exists")
                return {
                    "original_url": (
                        img_url[:100] + "..." if len(img_url) > 100 else img_url
                    ),
                    "local_path": filepath,
                    "status": "exists",
                }

            # 檢查圖片尺寸
            try:
                img = Image.open(io.BytesIO(img_data))
                width, height = img.size
                min_width = 500  # 設定最小寬度
                min_height = 500  # 設定最小高度
                print(f"圖片尺寸: {width}x{height}")
                if width < min_width or height < min_height:
                    print(f"圖片太小: {width}x{height}")
                    return {
                        "original_url": (
                            img_url[:100] + "..." if len(img_url) > 100 else img_url
                        ),
                        "status": "skipped",
                        "reason": f"image_too_small (size: {width}x{height})",
                        "dimensions": f"{width}x{height}",
                    }
                else:
                    img.save(original_filepath, quality=95)

            except Exception as e:
                # 如果無法讀取圖片尺寸，記錄錯誤但繼續處理
                print(f"Warning: Could not check image dimensions: {str(e)}")

            # 檢查圖片大小
            if len(img_data) > 13 * 1024 * 1024:
                print(f"檔案太大: {len(img_data)}")
                return {
                    "original_url": (
                        img_url[:100] + "..." if len(img_url) > 100 else img_url
                    ),
                    "status": "skipped",
                    "reason": f"file_too_large (size: {len(img_data)})",
                    "upload_to_blob": False,
                }
            # 保存圖片
            with open(filepath, "wb") as f:
                print(f"save")
                f.write(img_data)

            return {
                "original_url": (
                    img_url[:100] + "..." if len(img_url) > 100 else img_url
                ),
                "local_path": filepath,
                "status": "downloaded",
                "upload_to_blob": True,
            }

        except Exception as e:
            return {
                "original_url": (
                    img_url[:100] + "..." if len(img_url) > 100 else img_url
                ),
                "error": str(e),
                "status": "failed",
            }

    def extract_content(
        self,
        html_content: str,
        base_url: str,
        temp_dir: str,
        image_urls: List[str],
        original_images_downloaded_dir: Optional[str] = None,
        proxy_request: Optional[dict] = None,
    ) -> Dict:
        """提取文字和圖片內容"""
        soup = BeautifulSoup(html_content, "html.parser")
        # 找到並移除 class="recommend_wrapper" 的元素
        recommend_wrapper = soup.find(class_="recommend_wrapper")
        if recommend_wrapper:
            print(f"移除 recommend_wrapper")
            recommend_wrapper.decompose()  # 完全移除元素
            print(f"移除 recommend_wrapper 完成")

        body = soup.find("body")

        if not body:
            return {"texts": [], "images": []}

        # 移除 style 和 script 標籤
        for tag in body.find_all(["style", "script"]):
            tag.decompose()

        # 提取文字
        texts = []
        for element in body.find_all(string=True):
            if element.parent and isinstance(element, Comment):
                continue

            # if not self.should_keep_element(element):
            #     continue

            text = self.clean_text(element.string)
            if not text or len(text) < self.min_text_length:
                continue

            texts.append(
                {
                    "text": text,
                    "path": self.get_element_path(element),
                    "tag": element.parent.name,
                    "classes": element.parent.get("class", []),
                    "id": element.parent.get("id", ""),
                }
            )

        images = []
        for image_url in image_urls:
            img_info = self.download_image(
                image_url,
                base_url,
                temp_dir,
                original_images_downloaded_dir,
                proxy_request,
            )
            if img_info.get("status", None) in ["downloaded", "exists"]:
                images.append(img_info)

        return {"texts": texts, "images": images}

    def get_base_domain(self, url: str) -> str:
        """獲取URL的基本域名"""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}/"




class AsyncScrapyPlaywright(BaseScrapy):
    async def start(self, target_url, extracted_content_file, images_downloaded_dir):
        proxy_manager = SimpleProxyManager()
        proxy_server = None
        proxy_request = None

        response = requests.get(target_url, timeout=10)
        if response.status_code != 200:
            print("無法訪問頁面，嘗試獲取代理")
            # 嘗試獲取可用的代理
            for attempt in range(len(proxy_manager.proxies)):
                proxy = proxy_manager.get_next_proxy()
                if proxy and proxy_manager.test_proxy(proxy, target_url):
                    proxy_server = f"http://{proxy}"
                    proxy_request = {
                        "http": f"http://{proxy}",
                        "https": f"http://{proxy}",
                    }
                    break
                else:
                    print(f"代理 {proxy} 不可用，嘗試下一個...")

            if not proxy_server:
                print("沒有可用的代理，使用直連")

        async with Stealth().use_async(async_playwright()) as p:
            ua = UserAgent()
            # 修改瀏覽器啟動選項
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    # 基本反檢測參數
                    "--disable-blink-features=AutomationControlled",
                    "--disable-web-security",
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    # 性能和穩定性參數
                    "--disable-dev-shm-usage",
                    "--disable-extensions",
                    "--disable-gpu",
                    # 添加安全的渲染參數
                    "--disable-software-rasterizer",
                    "--disable-background-timer-throttling",
                    "--disable-backgrounding-occluded-windows",
                    "--disable-renderer-backgrounding",
                    "--disable-features=VizDisplayCompositor",
                    # 新增的反檢測參數
                    "--disable-extensions-file-access-check",
                    "--disable-extensions-except",
                    "--disable-plugins-discovery",
                    "--disable-default-apps",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--disable-background-timer-throttling",
                    "--disable-backgrounding-occluded-windows",
                    "--disable-renderer-backgrounding",
                    "--disable-features=TranslateUI,VizDisplayCompositor",
                    "--disable-ipc-flooding-protection",
                    # 模擬真實瀏覽器環境
                    "--enable-webgl",
                    "--use-gl=swiftshader",
                    "--enable-accelerated-2d-canvas",
                ],
                # 移除可能衝突的選項
                devtools=False,  # 確保不啟動開發工具
            )
            if proxy_server:
                proxy = {
                    "server": proxy_server,
                }
            else:
                proxy = None

            # 創建具有特定 user-agent 的上下文
            context = await browser.new_context(
                user_agent=ua.random,
                viewport={"width": 1920, "height": 1080},
                bypass_csp=True,  # 繞過內容安全策略
                java_script_enabled=True,
                # 添加更真實的瀏覽器特徵
                extra_http_headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8,ja;q=0.7",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Cache-Control": "max-age=0",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-User": "?1",
                },
                proxy=proxy,
            )

            page = await context.new_page()

            try:
                # 等待更長時間
                print("等待更長時間")
                page.set_default_timeout(60000)

                base_url = target_url

                image_urls = []

                def handle_response(response):
                    # 檢查 content-type
                    content_type = response.headers.get("content-type", "")
                    if "image" in content_type.lower():
                        if content_type.lower() in ["image/jpeg", "image/png", "image/webp"]:
                            image_urls.append(response.url)
                            print(f"攔截到圖片響應: {response.url[:100]}...")
                            print(f"Content-Type: {content_type}")
                            print(f"狀態碼: {response.status}")

                page.on("response", handle_response)

                # 訪問頁面並等待加載
                print("訪問頁面")
                response = await page.goto(base_url)
                print(f"訪問頁面完成response: {response}")

                # 點擊按鈕
                # for amazon.com 點擊繼續的按鈕
                try:
                    # 沒有這個元素則跳過
                    button_selector = "/html/body/div/div[1]/div[3]/div/div/form/div/div/span/span/button"
                    if page.locator(button_selector).count() == 0:
                        print("沒有這個元素，跳過")
                    else:
                        print(f"嘗試點擊按鈕: {button_selector}")
                        page.click(f"xpath={button_selector}")
                        print("按鈕點擊成功")
                        page.wait_for_timeout(2000)  # 等待點擊後的響應
                except Exception as e:
                    print(f"點擊按鈕失敗: {e}")

                # 等待初始內容加載
                await page.wait_for_load_state("domcontentloaded")
                print("DOM 內容已加載")

                # 滾動頁面觸發懶加載
                print("滾動頁面觸發懶加載...")
                for i in range(10):
                    await page.evaluate("window.scrollBy(0, 300)")
                    await page.wait_for_timeout(500)

                # 滾動到底部
                print("滾動到底部")
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)

                # 等待頁面完全加載
                # print("等待頁面完全加載")
                # await page.wait_for_load_state("networkidle")

                # 額外等待一些動態內容
                print("額外等待一些動態內容")
                await page.wait_for_timeout(2000)

                # 獲取 HTML
                print("獲取 HTML")
                html_content = await page.content()

                # 創建提取器並提取內容
                extractor = HTMLTextExtractor()
                original_images_downloaded_dir = (
                    images_downloaded_dir + "_original_images"
                )
                os.makedirs(images_downloaded_dir, exist_ok=True)
                os.makedirs(original_images_downloaded_dir, exist_ok=True)
                content = await asyncio.to_thread(
                    extractor.extract_content,  # 調用原來的同步方法
                    html_content,
                    base_url,
                    images_downloaded_dir,
                    image_urls,
                    original_images_downloaded_dir,
                    proxy_request,
                )

                # 保存文字結果
                async with aiofiles.open(
                    extracted_content_file, "w", encoding="utf-8"
                ) as f:
                    # 保存文字
                    await f.write("=== 文字內容 ===\n")
                    for item in content["texts"]:
                        await f.write(f"{item['text']}\n")

                # 打印統計信息
                print(f"總共提取了 {len(content['texts'])} 個文字元素")
                print(f"總共下載了 {len(content['images'])} 張圖片")

                if content["images"] == [] or len(content["images"]) <= 3:
                    # 如果沒有下載到任何圖片，進行全頁面截圖
                    print("沒有下載到圖片，開始進行全頁面截圖")

                    # 滾動到頁面頂部
                    await page.evaluate("window.scrollTo(0, 0)")
                    await page.wait_for_timeout(1000)

                    # 獲取頁面總高度
                    total_height = await page.evaluate("document.body.scrollHeight")
                    viewport_height = page.viewport_size["height"]

                    screenshot_count = 0
                    current_position = 0

                    while current_position < total_height:
                        # 截圖
                        screenshot_path = os.path.join(
                            images_downloaded_dir,
                            f"screenshot_{screenshot_count:03d}.jpg",
                        )
                        original_screenshot_path = os.path.join(
                            original_images_downloaded_dir,
                            f"original_screenshot_{screenshot_count:03d}.jpg",
                        )

                        await page.screenshot(path=screenshot_path)
                        await page.screenshot(path=original_screenshot_path)
                        print(f"截圖保存至: {screenshot_path}")

                        # 向下滾動一個視窗高度
                        current_position += viewport_height
                        await page.evaluate(f"window.scrollTo(0, {current_position})")
                        await page.wait_for_timeout(1000)  # 等待頁面穩定

                        screenshot_count += 1

                        # 防止無限循環
                        if screenshot_count > 30:
                            print("截圖數量超過限制，停止截圖")
                            break

                    print(f"完成全頁面截圖，共截取 {screenshot_count} 張圖片")

            except Exception as e:
                print(f"Error: {e}")
                await page.screenshot(path="error.png")
                raise e

            finally:
                await context.close()
                await browser.close()


