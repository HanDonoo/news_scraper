import pandas as pd
from scraper import fetch_article_with_selenium


def main():
    urls = [
        "https://finance.huanqiu.com/article/4Ox2cVt88xU",
        # 可以在这里添加更多链接
    ]

    articles = []

    for url in urls:
        print(f"\n====== 抓取文章 ======\n{url}")
        article = fetch_article_with_selenium(url, headless=True)

        articles.append({
            "title": article["title"],
            "content": "\n".join(article["content_blocks"]),  # 保留图片位置
            "cover": article["cover"],
            "url": url
        })

    # 转成 DataFrame
    df = pd.DataFrame(articles)
    print("\n📊 抓取结果预览：")
    print(df.head())

    # 保存到 CSV
    df.to_csv("articles.csv", index=False, encoding="utf-8-sig")
    print("\n📁 CSV 文件保存完成：articles.csv")


if __name__ == "__main__":
    main()
