import json
import html
import re
import bleach
from move_footers import reorder_footers
from merge_blocks import combine_consecutive_blocks

input_json = 'output.json'
output_html = 'input.html'
metadata_file = "metadata.json"

def preprocessing(entry):
    entry['text'] = re.sub(r'TIlis', 'This', entry['text'])
    entry['text'] = re.sub(r'(?<=\w) \n(?=\w)', '', entry['text']) #in-sentence line shifts
    entry['text'] = re.sub(r'(?<=\w)-\n(?=\w)', '', entry['text']) #end-of-line hyphens
    entry['text'] = re.sub(r'\bi(\d{3})\b', r'1\1', entry['text']) #years starting in i
    entry['text'] = re.sub(r'([a-z])\.([A-Z])', r'\1. \2', entry['text']) #missing space after period
    while '  ' in entry['text']: entry['text'] = entry['text'].replace('  ', ' ')
    return entry

def main():
    with open(metadata_file, "r") as mf:
        metadata = json.load(mf)
    print("Remember to manually nest headers before JSON parsing.")
    allowed_labels = {'h1', 'h2', 'h3', 'p', 'blockquote', 'footer'}
    skipping_labels = {'0', 'exclude'}
    bleach_allowed_tags = ['b', 'i', 'u', 'sup', 'sub', 'ul', 'ol', 'li', 'a']
    bleach_allowed_tags.extend(list(allowed_labels))
    allowed_attributes = {'*': ['class', 'id', 'href', 'title', 'target', 'alt', 'src', 'data-*']}
    title_input = metadata.get("title", "Untitled")
    entries = []
    processed_json = "output_processed.json"
    reorder_footers(input_json, processed_json)
    combine_consecutive_blocks(processed_json, processed_json)
    with open(processed_json, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Skipping line {line_number}. Not valid JSON. ({e})")
                continue
            if 'label' not in entry or 'text' not in entry:
                print(f"Skipping line {line_number}. Missing 'label' or 'text'.")
                continue
            label = entry['label']
            #progressive_label_map = {'header': 'h1', 'body': 'p', 'footer': 'footer', 'quote': 'blockquote', 'exclude': 'exclude'}
            #label = progressive_label_map[label]
            if label in skipping_labels:
                print(f"Skipping '{label}' block at line {line_number}.")
                continue
            elif label not in allowed_labels:
                print(f"Skipping line {line_number}. Invalid label '{label}'.")
                continue
            entries.append(entry)
    #Step 3: Generate HTML elements from valid entries
    html_elements = []
    print("Applying preprocessing")
    for entry in entries:
        entry = preprocessing(entry)
        label = entry['label']
        #escaped_text = html.escape(entry['text'])
        escaped_text = entry['text']
        if False: escaped_text = """<p>This is safe text.<sup>1</sup></p><br><p style="color: red;">This is another safe text with <a href="https://example.com">link</a>.</p><br><script>alert("XSS")</script><br><img src="cover.jpg" onerror="alert('Hacked!')"/><br><a href="javascript:alert('XSS')">Unsafe link</a>"""
        escaped_text = bleach.clean(escaped_text, tags=bleach_allowed_tags, attributes=allowed_attributes)
        if label == 'footer':
            element = f'    <p class="footnote">{escaped_text}</p>'
        else:
            element = f'    <{label}>{escaped_text}</{label}>'
        html_elements.append(element)
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title_input}</title>
</head>
<body>
{{}}
</body>
</html>""".replace('{}', '\n'.join(html_elements))
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Created {output_html}")

if __name__ == '__main__':
    main()

