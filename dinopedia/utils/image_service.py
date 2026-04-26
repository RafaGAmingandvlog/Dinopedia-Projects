# Image Service
import requests
import os

class ImageService:
    @staticmethod
    def fetch_dino_image(name):
        try:
            import urllib.parse

            formatted = name.strip().replace(" ", "_")
            encoded = urllib.parse.quote(formatted)

            # Wikipedia
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
            response = requests.get(url, timeout=5)

            if response.status_code != 200:
                return ""
            
            data = response.json()

            if "thumbnail" not in data:
                return ""
            
            # =====================
            # 🔥 CACHE SYSTEM
            # =====================
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            CACHE_DIR = os.path.join(BASE_DIR, "data", "images")
            
            if not os.path.exists(CACHE_DIR):
                os.makedirs(CACHE_DIR)

            filename = f"{CACHE_DIR}/{formatted}.jpg"

            # kalau sudah ada → pakai cache
            if os.path.exists(filename):
                return filename

            # download image
            img_url = data["thumbnail"]["source"]
            img_data = requests.get(img_url).content

            with open(filename, "wb") as f:
                f.write(img_data)

            return filename

        except Exception as e:
            print("Image fetch error:", e)
            return ""