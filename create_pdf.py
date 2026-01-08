import os
import json
import subprocess
import sys

input_file = "input.html"
cover_file = "cover.jpg"
metadata_file = "metadata.json"
css_file = "custom_style.css"

def create_pdf():
    required_files = [input_file, cover_file, metadata_file]
    for f in required_files:
        if not os.path.exists(f):
            print(f"Error: {f} is missing. Please place it in the same folder.")
            sys.exit(1)
    
    with open(metadata_file, "r", encoding="utf-8") as mf:
        metadata = json.load(mf)
    
    title = metadata.get("title", "Untitled")
    author = metadata.get("author", "Unknown")
    language = metadata.get("language", "en")
    
    output_file = f"{title}.pdf"
    
    cmd = [
        "ebook-convert",
        input_file,
        output_file,
        "--cover", cover_file,
        "--title", title,
        "--authors", author,
        "--language", language,
        "--paper-size", "a4",
        "--margin-left", "57",
        "--margin-right", "57",
        "--margin-top", "71",
        "--margin-bottom", "71",
        "--pdf-page-numbers",
        "--page-breaks-before", "//h:h1",
        "--preserve-cover-aspect-ratio",
        "--pdf-default-font-size", "12",
        "--pdf-serif-family", "Liberation Serif",
        "--level1-toc", "//h:h1",
        "--level2-toc", "//h:h2",
        "--level3-toc", "//h:h3"
    ]
    
    if os.path.exists(css_file):
        cmd += ["--extra-css", css_file]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Conversion completed: {output_file}")
    else:
        print("Conversion failed.")
        if result.stderr:
            print(result.stderr)

if __name__ == '__main__':
    create_pdf()
