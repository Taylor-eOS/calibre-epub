import os
import sys
import json
import subprocess
import re

input_file = "input.html"
cover_file = "cover.jpg"
metadata_file = "metadata.json"
css_file = "custom_style.css"

def create_epub():
    for f in [input_file, cover_file, metadata_file]:
        if not os.path.exists(f):
            print(f"Error: {f} is missing. Please place it in the same folder.")
            sys.exit(1)
    with open(metadata_file, "r") as mf:
        metadata = json.load(mf)

    title = metadata.get("title", "Untitled")
    author = metadata.get("author", "Unknown")
    language = metadata.get("language", "en")
    #identifier = metadata.get("isbn", "0")
    output_file = f"{title}.epub"

    cmd = [
        "ebook-convert", input_file, output_file,
        "--cover", cover_file,
        "--extra-css", css_file,
        "--title", title,
        "--authors", author,
        "--language", language,
        #"--identifier", identifier,
        "--chapter", "//h:h1",
        "--level1-toc", "//h:h1",
        "--level2-toc", "//h:h2",
        "--level3-toc", "//h:h3",
        "--toc-threshold", "1",
        "--debug-pipeline", "1",]

    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"Conversion completed: {output_file}")
    else:
        print("Conversion failed.")

create_epub()

