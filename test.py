import subprocess

html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Test Book</title>
</head>
<body>
    <h1>Test Book</h1>
    <p>This is a test book created using Calibre's ebook-convert tool.</p>
</body>
</html>"""
with open("test_book.html", "w") as file:
    file.write(html_content)
subprocess.run(["ebook-convert", "test_book.html", "test_book.epub"])
