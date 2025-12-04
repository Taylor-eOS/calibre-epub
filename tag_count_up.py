import re
import sys
from pathlib import Path

input_file = "output.txt"

def renumber_h3_headings(input_path: Path, output_path: Path | None = None) -> None:
    if not input_path.exists():
        print(f"Error: File {input_path} does not exist.")
        sys.exit(1)
    text = input_path.read_text(encoding="utf-8")
    pattern = r'({"label":\s*"h3",\s*"text":\s*")(\d+)(")'
    counter = 1
    def replacement(match: re.Match) -> str:
        nonlocal counter
        new_number = str(counter)
        counter += 1
        return match.group(1) + new_number + match.group(3)
    new_text, substitutions = re.subn(pattern, replacement, text)
    if substitutions == 0:
        print("No h3 headings were found.")
    else:
        print(f"Renumbered {substitutions} h3 headings (now 1 to {substitutions}).")
    output_file = output_path or Path("output.txt")
    output_file.write_text(new_text, encoding="utf-8")
    print(f"Result written to {output_file}")

if __name__ == "__main__":
    input_file = Path(input_file)
    renumber_h3_headings(input_file)

