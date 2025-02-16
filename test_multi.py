import subprocess

html_file = "input.html"
epub_file = "test_book.epub"

head = """<!DOCTYPE html>
<html>
<head>
    <title>Example Test Book</title>
    <link rel="stylesheet" type="text/css" href="custom_style.css"/>
</head>
<p class="body">"""

html_content1 = head + """
<h1>Chapter 1</h1>
    <p>This is text in the first chapter.<sup>1</sup></p>
    <p class="footnote">This is a footnote in the text.</p>
    <p>This is text in the first chapter.<br>In two sentences.</p></p>
</html>"""
html_content2 = head + """
<h1>Chapter 2</h1>
    <h2>First Words</h2>
    <h3>Level three subchapter</h3>
    <p>This is text in the second chapter.</p>
    <blockquote>This is a quote.<br>With two sentences in the same tag.</blockquote>
    <p class="footnote">This is a footnote at the end of a chapter.</p>
</p>
</html>"""
html_content3 = head + """
<h1>Chapter 3</h1>
    <p>This is text in the third chapter.</p>
    <p>Where the lines have their own tags.</p>
    <blockquote>This is a quote.</blockquote>
    <blockquote>Where each line has its own tag.</blockquote>
    <p>Some more text.</p>
    <p>In EPUB formatting, line-height refers to the amount of vertical space between lines of text. It plays an essential role in making text more readable by controlling the amount of space between consecutive lines of a paragraph. A good line-height helps avoid the text feeling cramped or too spaced out. The line-height is usually set in CSS (Cascading Style Sheets) for EPUB documents, typically using a unit like em, px, or %. For instance, a line-height of 1.5 (or 150%) means that the space between lines is 1.5 times the height of the font, making the text easier to read.</p>
</p>
</html>"""

html_contents = [html_content1, html_content2, html_content3]

for filename, html_content in zip([f"chapter_{i:03}.html" for i in range(1, 4)], html_contents):
    with open(filename, "w") as file:
        file.write(html_content)

print("Done")
# Convert the HTML file to EPUB using Calibre's ebook-convert
#subprocess.run(["ebook-convert", html_file1, epub_file])

