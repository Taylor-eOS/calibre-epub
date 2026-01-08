import os
import json
import subprocess
import sys

input_file = "input.html"
cover_file = "cover.jpg"
metadata_file = "metadata.json"
css_file = "custom_style.css"
create_table_of_contents = True

def check_required_files():
    required = [input_file, cover_file, metadata_file]
    for f in required:
        if not os.path.exists(f):
            print(f"Error: {f} is missing. Please place it in the same folder.")
            sys.exit(1)

def load_metadata():
    with open(metadata_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    title = data.get("title", "Untitled")
    author = data.get("author", "Unknown")
    language = data.get("language", "en")
    return title, author, language

def build_base_options(title, author, language):
    metadata_opts = ["--cover", cover_file, "--title", title, "--authors", author, "--language", language]
    css_opts = ["--extra-css", css_file] if os.path.exists(css_file) else []
    pdf_opts = ["--paper-size", "a4", "--margin-left", "57", "--margin-right", "57", "--margin-top", "71", "--margin-bottom", "71", "--pdf-page-numbers", "--preserve-cover-aspect-ratio", "--pdf-default-font-size", "12", "--pdf-serif-family", "Liberation Serif"]
    return metadata_opts, css_opts, pdf_opts

def run_conversion(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Conversion failed.")
        if result.stderr:
            print(result.stderr)
        return False
    return True

def create_pdf_with_toc(title, metadata_opts, css_opts, pdf_opts):
    epub_file = "intermediate.epub"
    epub_cmd = ["ebook-convert", input_file, epub_file] + metadata_opts + css_opts + ["--chapter", "//h:h1", "--level1-toc", "//h:h1", "--level2-toc", "//h:h2", "--epub-inline-toc"]
    if not run_conversion(epub_cmd):
        print("Intermediate EPUB creation failed.")
        sys.exit(1)
    pdf_cmd = ["ebook-convert", epub_file, f"{title}.pdf"] + pdf_opts + ["--page-breaks-before", "/"]
    success = run_conversion(pdf_cmd)
    if success:
        print(f"Conversion completed: {title}.pdf")
        if os.path.exists(epub_file):
            os.remove(epub_file)
    else:
        print("PDF conversion failed. Intermediate EPUB kept for inspection.")

def create_pdf_without_toc(title, metadata_opts, css_opts, pdf_opts):
    cmd = ["ebook-convert", input_file, f"{title}.pdf"] + metadata_opts + css_opts + pdf_opts + ["--level1-toc", "//h:h1", "--level2-toc", "//h:h2", "--page-breaks-before", "//h:h1"]
    success = run_conversion(cmd)
    if success:
        print(f"Conversion completed: {title}.pdf")
    else:
        print("Conversion failed.")

def create_pdf():
    check_required_files()
    title, author, language = load_metadata()
    metadata_opts, css_opts, pdf_opts = build_base_options(title, author, language)
    if create_table_of_contents:
        create_pdf_with_toc(title, metadata_opts, css_opts, pdf_opts)
    else:
        create_pdf_without_toc(title, metadata_opts, css_opts, pdf_opts)

if __name__ == "__main__":
    create_pdf()
