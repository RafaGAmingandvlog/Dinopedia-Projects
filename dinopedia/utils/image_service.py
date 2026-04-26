# Image Service
import os
import requests

class ImageService:
    CACHE_DIR = "data/images"

    @staticmethod
    def fetch_dino_image(name: str):
        try:
            if not os.path.exists(ImageService.CACHE_DIR):
                os.makedirs(ImageService.CACHE_DIR)

            formatted = name.strip().title().replace(" ", "_")
            filename = f"{ImageService.CACHE_DIR}/{formatted}.jpg"

            # 🔥 pakai cache kalau sudah ada
            if os.path.exists(filename):
                return filename

            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted}"

            headers = {
                "User-Agent": "DinopediaApp/1.0"
            }

            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code != 200:
                print("Wiki error:", response.status_code)
                return ""

            data = response.json()

            # 🔥 cek thumbnail ada atau tidak
            if "thumbnail" not in data:
                print("No thumbnail for:", name)
                return ""

            img_url = data["thumbnail"]["source"]

            # 🔥 download image
            img_response = requests.get(img_url, headers=headers, timeout=5)

            # 🔥 VALIDASI PENTING
            content_type = img_response.headers.get("Content-Type", "")
            if "image" not in content_type:
                print("Invalid image content:", content_type)
                return ""

            if img_response.status_code != 200:
                print("Image download failed")
                return ""

            with open(filename, "wb") as f:
                f.write(img_response.content)

            return filename

        except Exception as e:
            print("Image fetch error:", e)
            return ""