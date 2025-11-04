import requests

def translate_via_api(title, content):
    """使用 Cloudflare Workers 翻译接口"""
    url = "https://translator.lhanddong.workers.dev/"
    payload = {"title": title, "content": content}

    try:
        print("🌍 调用翻译 API 中...")
        response = requests.post(url, json=payload, timeout=100)

        if response.status_code == 200:
            data = response.json()
            # 假设返回结构为 {"title_en": "...", "content_en": "..."}
            return data
        else:
            print(f"⚠️ 翻译请求失败：HTTP {response.status_code}")
            return {"title_en": "", "content_en": ""}
    except Exception as e:
        print(f"❌ 翻译接口调用出错：{e}")
        return {"title_en": "", "content_en": ""}
