import subprocess

# Create a simple HTML file
html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Example Test Book</title>
</head>
<body>
    <h1>Chapter 1</h1>
    <p>This is the first chapter.<sup>1</sup></p>
    <footer>This is a footnote in the text.</footer>
    <p>This is the first chapter.<br>In two sentences.</p>
    <h1>Chapter 2</h1>
    <h2>First Words</h2>
    <h3>Level three subchapter</h3>
    <p>This is the second chapter.</p>
    <blockquote>This is a quote.<br>In two sentences.</blockquote>
    <footer>This is a footnote at the end of a chapter.</footer>
    <h1>Chapter 3</h1>
    <p>This is the third chapter.</p>
    <p>Where the lines have their own tags.</p>
    <blockquote>This is a quote.</blockquote>
    <blockquote>Where each line has its own tag.</blockquote>
    <p>Some more text.</p>
    <p>In EPUB formatting, line-height refers to the amount of vertical space between lines of text. It plays an essential role in making text more readable by controlling the amount of space between consecutive lines of a paragraph. A good line-height helps avoid the text feeling cramped or too spaced out. The line-height is usually set in CSS (Cascading Style Sheets) for EPUB documents, typically using a unit like em, px, or %. For instance, a line-height of 1.5 (or 150%) means that the space between lines is 1.5 times the height of the font, making the text easier to read.</p>
</body>
</html>"""

with open("test_book.html", "w") as file:
    file.write(html_content)

# Convert the HTML file to EPUB using Calibre's ebook-convert
subprocess.run(["ebook-convert", "test_book.html", "test_book.epub"])

