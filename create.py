import os
import sys
import json
import subprocess
import re
import glob

input_file = "input.html"
cover_file = "cover_image.jpg"
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
    css_content = metadata.get("css", "")
    #with open(css_file, "w") as cf:
    #    cf.write(css_content)
    #safe_title = re.sub(r'[\\/*?:"<>|]',"", title).replace(" ", "_")
    output_file = f"{title}.epub"
    cmd = [
        "ebook-convert", input_file, output_file,
        "--cover", cover_file,
        "--extra-css", css_file,
        "--chapter", "//h1",
        "--title", title,
        "--authors", author
    ]
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"Conversion completed: {output_file}")
    else:
        print("Conversion failed.")

create_epub()

