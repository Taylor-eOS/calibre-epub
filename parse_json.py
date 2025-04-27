import json
import re
import bleach
from move_footers import reorder_footers
from merge_blocks import combine_consecutive_blocks

input_json = 'output.json'
output_html = 'input.html'
metadata_file = "metadata.json"

def preprocessing(entry):
    replacements = [
        (r'TIlis', 'This'),
        (r'teh', 'the')]
    for pattern, replacement in replacements:
        entry['text'] = re.sub(pattern, replacement, entry['text'])
    entry['text'] = re.sub(r'\n', '', entry['text'])
    entry['text'] = re.sub(r'(?<=\w)-\n(?=\w)', '', entry['text'])
    entry['text'] = re.sub(r'\bi(\d{3})\b', r'1\1', entry['text'])
    entry['text'] = re.sub(r'([a-z])\.([A-Z])', r'\1. \2', entry['text'])
    while '  ' in entry['text']:
        entry['text'] = entry['text'].replace('  ', ' ')
    return entry

def main():
    with open(metadata_file) as mf:
        metadata = json.load(mf)
    allowed_labels = {'h1', 'h2', 'h3', 'p', 'blockquote', 'footer'}
    skipping_labels = {'0', 'exclude'}
    bleach_allowed_tags = ['b', 'i', 'u', 'sup', 'sub', 'ul', 'ol', 'li', 'a'] + list(allowed_labels)
    allowed_attributes = {'*': ['class', 'id', 'href', 'title', 'target', 'alt', 'src', 'data-*']}
    title_input = metadata.get("title", "Untitled")
    entries = []
    processed_json = "intermediary.json"
    reorder_footers(input_json, processed_json)
    combine_consecutive_blocks(processed_json, processed_json)
    with open(processed_json, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if 'label' not in entry or 'text' not in entry:
                continue
            label = entry['label']
            if label in skipping_labels or label not in allowed_labels:
                continue
            entries.append(entry)

    html_elements = []
    open_levels = []  # stack of open heading levels
    counts = {1: 0, 2: 0, 3: 0}

    for entry in entries:
        entry = preprocessing(entry)
        label = entry['label']
        text = bleach.clean(entry['text'], tags=bleach_allowed_tags, attributes=allowed_attributes)

        if label in ('h1', 'h2', 'h3'):
            level = int(label[1])
            while open_levels and open_levels[-1] >= level:
                html_elements.append('</section>')
                open_levels.pop()
            counts[level] += 1
            for lower in (l for l in (2,3) if l > level):
                counts[lower] = 0
            sec_id = 'section-' + '-'.join(str(counts[l]) for l in sorted(counts) if counts[l] and l <= level)
            html_elements.append(f'<section id="{sec_id}">')
            html_elements.append(f'<{label}>{text}</{label}>')
            open_levels.append(level)

        elif label == 'footer':
            html_elements.append(f'<p class="footnote">{text}</p>')
        else:
            html_elements.append(f'<{label}>{text}</{label}>')

    while open_levels:
        html_elements.append('</section>')
        open_levels.pop()

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title_input}</title>
</head>
<body>
{''.join(html_elements)}
</body>
</html>"""

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Created {output_html}")

if __name__ == '__main__':
    main()

