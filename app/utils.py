import requests
import os


def print_article(data):
    print("=== Title ===")
    print(data["title"], "\n")

    print("=== Content ===")
    for i, para in enumerate(data["paragraphs"], start=1):
        print(f"{i}: {para}\n")

    print("=== Images ===")
    for i, url in enumerate(data["images"], start=1):
        print(f"{i}: {url}")


def download_images(image_urls, folder="images"):
    os.makedirs(folder, exist_ok=True)
    for i, url in enumerate(image_urls, start=1):
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                filename = os.path.join(folder, f"{i}_{os.path.basename(url)}")
                with open(filename, "wb") as f:
                    f.write(resp.content)
                print(f"Saved {filename}")
            else:
                print(f"Failed to download {url}, status {resp.status_code}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")
