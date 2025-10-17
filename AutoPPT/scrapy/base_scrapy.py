from abc import ABC, abstractmethod


class BaseScrapy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def start(self, target_url, extracted_content_file, images_downloaded_dir):
        """
        爬取目標網站，並將爬取的內容保存到 extracted_content_file 和 images_downloaded_dir 中
        ::param target_url: 目標網站
        ::param extracted_content_file: 爬取的內容保存到 extracted_content_file 中
        ::param images_downloaded_dir: 爬取的圖片保存到 images_downloaded_dir 中
        ::return: 爬取的內容和圖片
        """
        pass
