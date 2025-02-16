import subprocess
import os
import sys

# Filenames
input_file = "input.html"
cover_file = "cover_image.jpg"
stylesheet_file = "custom_style.css"
output_file = "output.epub"

# Ensure required files exist
for file in [input_file, cover_file]:
    if not os.path.exists(file):
        print(f"Error: {file} is missing. Please place it in the same folder.")
        sys.exit(1)

# Create custom CSS for styling
css_content = """
body {
    margin: 0 !important;
}
.footnote {
    font-size: 80%;
}
"""

with open(stylesheet_file, "w") as css_file:
    css_file.write(css_content)

# Convert HTML to EPUB with cover and custom styles
subprocess.run([
    "ebook-convert", input_file, output_file,
    "--cover", cover_file,
    "--extra-css", stylesheet_file,
    "--chapter", "//h1"
])

print(f"Conversion completed: {output_file}")

