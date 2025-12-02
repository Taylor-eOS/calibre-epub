import json
import re
import bleach
import os
import sys
from move_footers import reorder_footers
from merge_blocks import combine_consecutive_blocks

input_json = 'output.json'
intermediate_json = 'intermediary.json'
output_html = 'input.html'
metadata_file = "metadata.json"
merge_consecutive = True
skip_merging_for_large_files = True

def preprocessing(entry):
    replacements = [(r'TIlis', 'This'),(r'teh', 'the')]
    for patt, repl in replacements:
        entry['text'] = re.sub(patt, repl, entry['text'])
    entry['text'] = re.sub(r'\n', '', entry['text'])
    entry['text'] = re.sub(r'(?<=\w)-\n(?=\w)', '', entry['text'])
    entry['text'] = re.sub(r'\bi(\d{3})\b', r'1\1', entry['text'])
    entry['text'] = re.sub(r'([a-z])\.([A-Z])', r'\1. \2', entry['text'])
    while '  ' in entry['text']:
        entry['text'] = entry['text'].replace('  ', ' ')
    return entry

def main():
    if not os.path.exists(metadata_file):
        print(f"Error: {metadata_file} is missing")
        sys.exit(1)
    with open(metadata_file, encoding='utf-8') as mf:
        metadata = json.load(mf)
    allowed_labels = {'h1','h2','h3','p','blockquote','footer'}
    skipping = {'0','exclude'}
    bleach_tags = ['b','i','u','sup','sub','ul','ol','li','a'] + list(allowed_labels)
    bleach_attrs = {'*': ['class','id','href','title','target','alt','src','data-*']}
    reorder_footers(input_json, intermediate_json)
    source_for_parsing = intermediate_json
    if merge_consecutive:
        merged_file = 'merged.json'
        combine_consecutive_blocks(intermediate_json, merged_file)
        source_for_parsing = merged_file
    else:
        print("Merging of consecutive blocks disabled (merge_consecutive = False)")
    entries = []
    with open(source_for_parsing, encoding='utf-8') as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            if 'label' not in e or 'text' not in e:
                continue
            if e['label'] in skipping or e['label'] not in allowed_labels:
                continue
            entries.append(e)
    levels = {'h1':1, 'h2':2, 'h3':3}
    html = []
    section_open = False
    section_count = 0
    content_since_header = False
    for entry in entries:
        entry = preprocessing(entry)
        lbl = entry['label']
        txt = bleach.clean(entry['text'], tags=bleach_tags, attributes=bleach_attrs, strip=True)
        if lbl in levels:
            lvl = levels[lbl]
            if lvl == 1:
                if section_open:
                    html.append('</section>')
                section_count += 1
                html.append(f'<section id="section-{section_count}">')
                section_open = True
                content_since_header = False
            else:
                if section_open and content_since_header and lvl > 1:
                    html.append('</section>')
                    section_count += 1
                    html.append(f'<section id="section-{section_count}">')
                    content_since_header = False
            html.append(f'<{lbl}>{txt}</{lbl}>')
        else:
            if lbl == 'footer':
                html.append(f'<p class="footnote">{txt}</p>')
            else:
                html.append(f'<{lbl}>{txt}</{lbl}>')
            content_since_header = True
    if section_open:
        html.append('</section>')
    out = f"""<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{metadata.get("title","Untitled")}</title>
</head>
<body>
{''.join(html)}
</body>
</html>"""
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(out)
    if merge_consecutive and source_for_parsing != intermediate_json:
        try:
            os.remove(source_for_parsing)
        except OSError:
            pass
    print(f"Created {output_html} (merging was {'disabled' if not merge_consecutive else 'enabled'})")

if __name__ == '__main__':
    main()

