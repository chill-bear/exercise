
import json
from pathlib import Path
from urllib.parse import urlparse

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class URLShortener:
    def __init__(self, storage_file="urls.json", max_url_length=2048):
        self.storage_file = Path(storage_file)
        self.max_url_length = max_url_length

        # short_code -> original_url
        self.code_to_url = {}

        # original_url -> short_code
        self.url_to_code = {}

        self.next_id = 1
        self.load()

    def encode_base62(self, number):
        if number == 0:
            return BASE62[0]

        result = ""
        # 125/62: number : 2 remainder = 1
        # 2/62: number: 0, remainder = 2
        # 125 -> 21
        while number > 0:
            number, remainder = divmod(number, 62)
            result = BASE62[remainder] + result

        return result

    def validate_url(self, url):
        if not isinstance(url, str) or not url:
            raise ValueError("URL cannot be empty")

        if len(url) > self.max_url_length:
            raise ValueError("URL is too long")

        if any(char.isspace() for char in url):
            raise ValueError("URL cannot contain whitespace")

        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            raise ValueError("Invalid URL")

        try:
            parsed.port
        except ValueError:
            raise ValueError("Invalid URL port")

    def shorten(self, url):
        self.validate_url(url)

        # Return existing code for duplicate URLs
        if url in self.url_to_code:
            return self.url_to_code[url]

        # Generate unique code
        code = self.encode_base62(self.next_id)

        # # Defensive collision handling
        # while code in self.code_to_url:
        #     self.next_id += 1
        #     code = self.encode_base62(self.next_id)

        self.code_to_url[code] = url
        self.url_to_code[url] = code
        self.next_id += 1

        self.save()
        return code

    def resolve(self, code):
        if code not in self.code_to_url:
            raise KeyError("Short URL not found")

        return self.code_to_url[code]

    def save(self):
        data = {
            "next_id": self.next_id,
            "urls": self.code_to_url,
        }
        # simple solution or below
        self.storage_file.write_text(json.dumps(data, indent=2))
        # Write to a temporary file, then replace
        temp_file = self.storage_file.with_suffix(".tmp")
        temp_file.write_text(json.dumps(data, indent=2))
        temp_file.replace(self.storage_file)

    def load(self):
        if not self.storage_file.exists():
            return

        data = json.loads(self.storage_file.read_text())

        self.code_to_url = data["urls"]
        self.url_to_code = {
            url: code for code, url in self.code_to_url.items()
        }
        self.next_id = data["next_id"]


def main():
    shortener = URLShortener()

    while True:
        print("\n1. Shorten URL")
        print("2. Resolve URL")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                url = input("Enter URL: ").strip()
                code = shortener.shorten(url)
                print(f"Short URL: http://localhost:8000/{code}")

            elif choice == "2":
                code = input("Enter short code: ").strip()
                print(f"Original URL: {shortener.resolve(code)}")

            elif choice == "3":
                break

            else:
                print("Invalid option")

        except (ValueError, KeyError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
