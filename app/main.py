import pandas as pd
from scraper import fetch_article_with_selenium
from translator import translate_via_api

def main():
    urls = [
        "https://m.huanqiu.com/article/4OwsQhxR5g0",
        # 这里添加更多待爬链接
    ]

    articles = []

    for url in urls:
        print(f"\n====== 抓取文章 ======\n{url}")
        article = fetch_article_with_selenium(url, headless=True)

        # 原文内容
        full_content = "\n".join(article["content_blocks"])

        # 调用翻译
        translation = translate_via_api(article["title"], full_content)

        # 获取翻译后的内容
        title_en = translation.get("title_translated", "")
        content_en = translation.get("content_translated", "")

        # 写入文件
        articles.append({
            "title_zh": article["title"],
            "title_en": title_en,
            "content_zh": full_content,
            "content_en": content_en,
            "cover": article["cover"],
            "url": url
        })

    # 保存结果
    df = pd.DataFrame(articles)
    print("\n抓取与翻译结果预览：")
    print(df.head())

    df.to_csv("articles_translated.csv", index=False, encoding="utf-8-sig")
    print("\nCSV 文件保存完成：articles_translated.csv")

if __name__ == "__main__":
    main()
