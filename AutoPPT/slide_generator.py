"""
Slide 生成器（統一的 HTML 和 PPTX 生成接口）

使用 Strategy Pattern，每個 slide 類型負責自己的渲染邏輯
"""

from typing import Any, Dict, List

from pptx import Presentation
from pptx.util import Inches

from AutoPPT.slide_types.slide_types import SlideTypeRegistry
from AutoPPT.utils.logger import get_logger

# 获取日志器
logger = get_logger(name="SlideGenerator")


# ==================== HTML 生成器 ====================
class HTMLGenerator:
    """HTML 演示文稿生成器"""

    def __init__(self, image_metadata: Dict = None):
        self.image_metadata = image_metadata or {}
        self.context = {'image_metadata': self.image_metadata}

    def generate_from_data(self, ai_data: Dict) -> str:
        """從 AI JSON 數據生成完整 HTML
        
        Args:
            ai_data: AI 生成的結構化數據
            
        Returns:
            完整的 HTML 字符串
        """
        slides_html = []

        for slide_data in ai_data.get('slides', []):
            slide_html = self._create_slide_html(slide_data)
            if slide_html:
                slides_html.append(slide_html)

        return self._build_full_html(
            title=ai_data.get('title', '演示文稿'),
            slides_html=slides_html
        )

    def _create_slide_html(self, slide_data: Dict) -> str:
        """根據類型創建單個 slide 的 HTML"""
        slide_type = slide_data.get('slide_type', 'text_content')

        # 從 Registry 獲取對應的 slide 類
        slide_class = SlideTypeRegistry.get(slide_type)

        if not slide_class:
            logger.info(f"⚠️ 未知的 slide 類型：{slide_type}，使用預設類型")
            slide_class = SlideTypeRegistry.get('text_content')

        # 創建 slide 實例並生成 HTML
        slide = slide_class(slide_data, self.context)
        return slide.generate_html()

    def _build_full_html(self, title: str, slides_html: List[str]) -> str:
        """構建完整的 HTML 文檔（包含 CSS 和 JS）"""
        slides_content = '\n'.join(slides_html)

        return f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: '微軟正黑體', 'Microsoft JhengHei', 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .presentation-container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .slide {{
            width: 100%;
            aspect-ratio: 4 / 3;
            background: white;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            border-radius: 12px;
            overflow: hidden;
            position: relative;
            display: none;
        }}
        
        .slide.active {{
            display: block;
            animation: slideIn 0.5s ease-out;
        }}
        
        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .slide-content {{
            padding: 60px 80px;
            height: 100%;
            display: flex;
            flex-direction: column;
        }}
        
        /* 開場頁 */
        .slide-opening {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .slide-opening .slide-content {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
        }}
        
        .slide-opening .main-title {{
            font-size: 64px;
            font-weight: bold;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        }}
        
        .slide-opening .subtitle {{
            font-size: 32px;
            color: rgba(255,255,255,0.95);
            text-align: center;
        }}
        
        /* 章節頁 */
        .slide-section {{
            background: linear-gradient(135deg, #4682b4 0%, #2c5f8d 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .slide-section .slide-content {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
        }}
        
        .slide-section .section-title {{
            font-size: 56px;
            font-weight: bold;
            color: white;
            text-align: center;
            padding: 40px;
        }}
        
        .decoration-line {{
            width: 200px;
            height: 4px;
            background: white;
            margin: 30px auto;
            border-radius: 2px;
        }}
        
        /* 內容頁 */
        .slide-content .slide-title {{
            font-size: 42px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 4px solid #4682b4;
        }}
        
        .bullet-list {{
            list-style: none;
            padding: 0;
        }}
        
        .bullet-list li {{
            font-size: 28px;
            color: #34495e;
            margin: 25px 0;
            padding-left: 50px;
            position: relative;
            line-height: 1.6;
        }}
        
        .bullet-list li:before {{
            content: "▶";
            position: absolute;
            left: 0;
            color: #4682b4;
            font-size: 24px;
        }}
        
        .bullet-list li.indent-1 {{
            padding-left: 100px;
            font-size: 24px;
            color: #555;
        }}
        
        .bullet-list li.indent-1:before {{
            content: "▸";
            left: 50px;
            font-size: 20px;
        }}
        
        /* 圖文混合 */
        .image-text-container {{
            display: grid;
            gap: 40px;
            flex: 1;
        }}
        
        .image-text-container.layout-horizontal {{
            grid-template-columns: 1fr 1fr;
        }}
        
        .image-text-container.layout-vertical {{
            grid-template-rows: auto auto;
        }}
        
        .image-box {{
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .image-box img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        
        .text-box {{
            display: flex;
            align-items: center;
        }}
        
        .text-box p {{
            font-size: 24px;
            color: #2c3e50;
            line-height: 1.8;
        }}
        
        /* 大圖展示 */
        .full-image-container {{
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        
        .full-image-container img {{
            max-width: 90%;
            max-height: 70%;
            object-fit: contain;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        }}
        
        .caption {{
            margin-top: 20px;
            font-size: 20px;
            color: #7f8c8d;
            text-align: center;
        }}
        
        /* 結尾頁 */
        .slide-closing {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .slide-closing .slide-content {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
        }}
        
        .slide-closing .closing-title {{
            font-size: 64px;
            font-weight: bold;
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .slide-closing .closing-subtext {{
            font-size: 28px;
            color: rgba(255,255,255,0.95);
            text-align: center;
        }}
        
        /* 導航控制 */
        .nav-controls {{
            position: fixed;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.7);
            padding: 15px 30px;
            border-radius: 50px;
            display: flex;
            gap: 20px;
            align-items: center;
            backdrop-filter: blur(10px);
        }}
        
        .nav-controls button {{
            background: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
            transition: all 0.3s;
        }}
        
        .nav-controls button:hover {{
            background: #4682b4;
            color: white;
            transform: scale(1.05);
        }}
        
        .nav-controls button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        
        .slide-counter {{
            color: white;
            font-size: 16px;
            font-weight: bold;
            min-width: 80px;
            text-align: center;
        }}
        
        /* 響應式 */
        @media (max-width: 768px) {{
            .slide-content {{
                padding: 30px 40px;
            }}
            
            .slide-opening .main-title {{
                font-size: 40px;
            }}
            
            .image-text-container.layout-horizontal {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="presentation-container">
        {slides_content}
    </div>
    
    <div class="nav-controls">
        <button id="prevBtn">◀ 上一張</button>
        <span class="slide-counter"><span id="currentSlide">1</span> / <span id="totalSlides">0</span></span>
        <button id="nextBtn">下一張 ▶</button>
    </div>
    
    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const currentSlideSpan = document.getElementById('currentSlide');
        const totalSlidesSpan = document.getElementById('totalSlides');
        
        totalSlidesSpan.textContent = totalSlides;
        
        function showSlide(n) {{
            slides.forEach((slide, i) => {{
                slide.classList.remove('active');
                if (i === n) {{
                    slide.classList.add('active');
                }}
            }});
            
            currentSlideSpan.textContent = n + 1;
            prevBtn.disabled = n === 0;
            nextBtn.disabled = n === totalSlides - 1;
        }}
        
        function nextSlide() {{
            if (currentSlide < totalSlides - 1) {{
                currentSlide++;
                showSlide(currentSlide);
            }}
        }}
        
        function prevSlide() {{
            if (currentSlide > 0) {{
                currentSlide--;
                showSlide(currentSlide);
            }}
        }}
        
        prevBtn.addEventListener('click', prevSlide);
        nextBtn.addEventListener('click', nextSlide);
        
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight' || e.key === ' ') {{
                e.preventDefault();
                nextSlide();
            }} else if (e.key === 'ArrowLeft') {{
                e.preventDefault();
                prevSlide();
            }}
        }});
        
        // 初始化
        if (totalSlides > 0) {{
            showSlide(0);
        }}
    </script>
</body>
</html>
        """


# ==================== PPTX 生成器 ====================
class PPTXGenerator:
    """PPTX 演示文稿生成器"""

    def __init__(self, image_metadata: Dict = None):
        self.prs = Presentation()
        self.prs.slide_width = Inches(10)
        self.prs.slide_height = Inches(7.5)
        self.image_metadata = image_metadata or {}
        self.context = {'image_metadata': self.image_metadata}

    def generate_from_data(self, ai_data: Dict) -> Presentation:
        """從 AI JSON 數據生成 PPTX
        
        Args:
            ai_data: AI 生成的結構化數據
            
        Returns:
            Presentation 對象
        """
        for i, slide_data in enumerate(ai_data.get('slides', []), 1):
            logger.info(f"📝 處理第 {i} 張幻燈片...")

            try:
                self._create_slide_pptx(slide_data)
                logger.info(f"   ✓ 創建成功")
            except Exception as e:
                logger.info(f"   ❌ 創建失敗：{e}")
                import traceback
                traceback.logger.info_exc()

        return self.prs

    def _create_slide_pptx(self, slide_data: Dict):
        """根據類型創建單個 PPTX slide"""
        slide_type = slide_data.get('slide_type', 'text_content')

        # 從 Registry 獲取對應的 slide 類
        slide_class = SlideTypeRegistry.get(slide_type)

        if not slide_class:
            logger.info(f"⚠️ 未知的 slide 類型：{slide_type}，使用預設類型")
            slide_class = SlideTypeRegistry.get('text_content')

        # 創建 slide 實例並生成 PPTX
        slide = slide_class(slide_data, self.context)
        slide.generate_pptx(self.prs)

    def save(self, output_path: str):
        """保存 PPTX 文件"""
        self.prs.save(output_path)
        logger.info(f"   ✅ PPTX 已保存：{output_path}")


# ==================== HTML 轉 PPTX 解析器 ====================
class HTMLToPPTXParser:
    """解析 HTML 並轉換為 PPTX（用於向後兼容）"""

    def __init__(self, image_metadata: Dict = None):
        self.generator = PPTXGenerator(image_metadata)

    def parse_html_file(self, html_file: str):
        """解析 HTML 文件並轉換為 PPTX
        
        Note: 這個方法保留是為了向後兼容
        推薦使用 JSON → HTML/PPTX 的新流程
        """
        from bs4 import BeautifulSoup

        logger.info(f"📂 讀取 HTML 文件：{html_file}")

        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")
        container = soup.find("div", class_="presentation-container")

        if not container:
            logger.info("❌ 找不到 presentation-container")
            return

        slides = container.find_all("div", class_="slide")
        logger.info(f"   ✓ 找到 {len(slides)} 張幻燈片")

        for i, slide_elem in enumerate(slides, 1):
            logger.info(f"📝 處理第 {i} 張幻燈片...")

            try:
                # 判斷 slide 類型
                slide_classes = slide_elem.get("class", [])
                slide_data = self._parse_slide_elem(slide_elem, slide_classes)

                if slide_data:
                    self.generator._create_slide_pptx(slide_data)
                    logger.info(f"   ✓ 創建成功")
            except Exception as e:
                logger.info(f"   ❌ 創建失敗：{e}")
                import traceback
                traceback.logger.info_exc()

    def _parse_slide_elem(self, slide_elem, slide_classes: List[str]) -> Dict:
        """從 HTML 元素解析出 slide 數據"""
        if "slide-opening" in slide_classes:
            return self._parse_opening_elem(slide_elem)
        elif "slide-section" in slide_classes:
            return self._parse_section_elem(slide_elem)
        elif "slide-closing" in slide_classes:
            return self._parse_closing_elem(slide_elem)
        else:
            # 檢查是否有圖片
            if slide_elem.find("div", class_="full-image-container"):
                return self._parse_full_image_elem(slide_elem)
            elif slide_elem.find("div", class_="image-text-container"):
                return self._parse_image_text_elem(slide_elem)
            else:
                return self._parse_text_content_elem(slide_elem)

    def _parse_opening_elem(self, elem) -> Dict:
        title = elem.find("h1", class_="main-title")
        subtitle = elem.find("p", class_="subtitle")
        return {
            'slide_type': 'opening',
            'title': title.get_text(strip=True) if title else '',
            'subtitle': subtitle.get_text(strip=True) if subtitle else ''
        }

    def _parse_section_elem(self, elem) -> Dict:
        section_title = elem.find("h2", class_="section-title")
        return {
            'slide_type': 'section_divider',
            'section_title': section_title.get_text(strip=True) if section_title else ''
        }

    def _parse_closing_elem(self, elem) -> Dict:
        closing_title = elem.find("h1", class_="closing-title")
        subtext = elem.find("p", class_="closing-subtext")
        return {
            'slide_type': 'closing',
            'closing_text': closing_title.get_text(strip=True) if closing_title else '謝謝觀看',
            'subtext': subtext.get_text(strip=True) if subtext else ''
        }

    def _parse_text_content_elem(self, elem) -> Dict:
        title = elem.find("h2", class_="slide-title")
        bullet_list = elem.find("ul", class_="bullet-list")

        bullets = []
        indent_levels = []

        if bullet_list:
            for item in bullet_list.find_all("li"):
                bullets.append(item.get_text(strip=True))
                indent_levels.append(1 if "indent-1" in item.get("class", []) else 0)

        return {
            'slide_type': 'text_content',
            'title': title.get_text(strip=True) if title else '',
            'bullets': bullets,
            'indent_levels': indent_levels
        }

    def _parse_image_text_elem(self, elem) -> Dict:
        title = elem.find("h2", class_="slide-title")
        container = elem.find("div", class_="image-text-container")
        img_tag = elem.find("img")
        text_box = elem.find("div", class_="text-box")

        layout = "horizontal"
        if container and "layout-vertical" in container.get("class", []):
            layout = "vertical"

        # 提取 image_id（如果 src 是 downloaded_images/xxx.jpg 格式）
        image_id = ""
        if img_tag:
            src = img_tag.get("src", "")
            # 簡單提取文件名作為 id
            if src:
                image_id = src

        return {
            'slide_type': 'image_with_text',
            'title': title.get_text(strip=True) if title else '',
            'image_id': image_id,
            'text': text_box.get_text(strip=True) if text_box else '',
            'layout': layout
        }

    def _parse_full_image_elem(self, elem) -> Dict:
        title = elem.find("h2", class_="slide-title")
        img_tag = elem.find("img")
        caption = elem.find("p", class_="caption")

        image_id = ""
        if img_tag:
            src = img_tag.get("src", "")
            if src:
                image_id = src

        return {
            'slide_type': 'full_image',
            'title': title.get_text(strip=True) if title else '',
            'image_id': image_id,
            'caption': caption.get_text(strip=True) if caption else ''
        }

    def save(self, output_path: str):
        """保存 PPTX 文件"""
        self.generator.save(output_path)
