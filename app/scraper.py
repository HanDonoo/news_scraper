import os
import time
import html
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def fetch_article_with_selenium(url, headless=True):
    """使用 Selenium 模拟浏览器加载并抓取环球网文章内容"""
    os.environ["PYDEVD_USE_CYTHON"] = "NO"  # 解决 PyCharm 调试问题

    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1280,1024")

    print("启动 Chrome 浏览器...")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    print(f"正在访问 {url}")
    driver.get(url)
    time.sleep(3)  # 等待页面加载（可调整）

    html_content = driver.page_source
    driver.quit()
    print("页面加载完成，开始解析内容...")

    return parse_article_html(html_content)

def parse_article_html(html_content):
    """解析 Selenium 获取的 HTML，提取标题、正文（保留图片位置）、封面"""
    soup = BeautifulSoup(html_content, "html.parser")

    # === 标题 ===
    title_tag = soup.find("textarea", class_="article-title")
    title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

    # === 正文 ===
    content_textarea = soup.find("textarea", class_="article-content")
    content_blocks = []  # 顺序保存文本与图片
    images = []
    seen_images = set()  # 防止重复添加图片

    if content_textarea:
        raw_html = html.unescape(content_textarea.get_text(strip=True))
        content_soup = BeautifulSoup(raw_html, "html.parser")

        # 遍历正文结构（主要看 p 和 i）
        for element in content_soup.find_all(["p", "i"], recursive=True):
            # --- 段落文字 ---
            text = element.get_text(strip=True)
            if text:
                content_blocks.append(text)

            # --- 查找图片 ---
            img = element.find("img")
            if img and img.get("src"):
                src = normalize_img_url(img["src"])
                if src not in seen_images:
                    seen_images.add(src)
                    content_blocks.append(f"[IMAGE:{src}]")
                    images.append(src)

    # === 封面 ===
    cover_tag = soup.find("textarea", class_="article-cover")
    cover = cover_tag.get_text(strip=True) if cover_tag else ""
    cover = normalize_img_url(cover)

    return {
        "title": title,
        "content_blocks": content_blocks,  # 含图片位置标记
        "images": images,
        "cover": cover
    }

def normalize_img_url(src):
    """统一补全 https:// 开头的图片链接"""
    if src and src.startswith("//"):
        return "https:" + src
    return src
