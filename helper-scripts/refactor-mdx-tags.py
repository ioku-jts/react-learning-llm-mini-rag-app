import re, os

for filename in os.listdir("data/raw"):
    if filename.endswith(".md"):
        path = os.path.join("data/raw", filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        # Replace MDX tags with nothing
        cleaned = re.sub(r"<[^>]+>", "", text)
        with open(path, "w", encoding="utf-8") as f:
            f.write(cleaned)