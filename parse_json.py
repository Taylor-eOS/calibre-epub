import os
import sys
import re
import json
import bleach
from move_footers import reorder_footers
from merge_blocks import combine_consecutive_blocks

input_json = 'input.json'
intermediate_json = 'intermediate.json'
output_html = 'input.html'
metadata_file = "metadata.json"
merge_consecutive = False

def preprocessing(entry):
    replacements = [(r'TIlis ', 'This '),(r' teh ', ' the '),(r' taht ', ' that '),(r' jsut ', ' just ')]
    for patt, repl in replacements:
        entry['text'] = re.sub(patt, repl, entry['text'])
    entry['text'] = re.sub(r'\n', '', entry['text'])
    entry['text'] = re.sub(r'(?<=\w)-\n(?=\w)', '', entry['text'])
    entry['text'] = re.sub(r'\bi(\d{3})\b', r'1\1', entry['text'])
    entry['text'] = re.sub(r'([a-z])\.([A-Z])', r'\1. \2', entry['text'])
    while '  ' in entry['text']:
        entry['text'] = entry['text'].replace('  ', ' ')
    return entry

def load_metadata():
    if not os.path.exists(metadata_file):
        print(f"Error: {metadata_file} is missing")
        sys.exit(1)
    with open(metadata_file, encoding='utf-8') as mf:
        return json.load(mf)

def get_entries_to_process(source_file):
    allowed_labels = {'h1','h2','h3','p','blockquote','footer'}
    skipping = {'0','exclude'}
    entries = []
    with open(source_file, encoding='utf-8') as f:
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
    return entries

def build_html_content(entries, title_text):
    levels = {'h1':1, 'h2':2, 'h3':3}
    bleach_tags = ['b','i','u','sup','sub','ul','ol','li','a','br','h1','h2','h3','p','blockquote','footer']
    bleach_attrs = {'*': ['class','id','href','title','target','alt','src','data-*']}
    html = []
    section_open = False
    section_count = 0
    content_since_header = False
    html.append('<!DOCTYPE html>')
    html.append('<html xmlns="http://www.w3.org/1999/xhtml">')
    html.append('<head>')
    html.append('    <title>' + title_text + '</title>')
    html.append('    <meta charset="utf-8">')
    html.append('</head>')
    html.append('<body>')
    html.append('<p style="font-size: 3em; text-align: center; margin-top: 40%; font-weight: bold;">' + title_text + '</p>')
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
                html.append('<section id="section-' + str(section_count) + '">')
                section_open = True
                content_since_header = False
            else:
                if section_open and content_since_header and lvl > 1:
                    html.append('</section>')
                    section_count += 1
                    html.append('<section id="section-' + str(section_count) + '">')
                    content_since_header = False
            html.append('<' + lbl + '>' + txt + '</' + lbl + '>')
        else:
            if lbl == 'footer':
                html.append('<p class="footnote">' + txt + '</p>')
            else:
                html.append('<' + lbl + '>' + txt + '</' + lbl + '>')
            content_since_header = True
    if section_open:
        html.append('</section>')
    html.append('</body>')
    html.append('</html>')
    return html

def write_output(html_lines):
    out = '\n'.join(html_lines)
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(out)

def create_html():
    metadata = load_metadata()
    title_text = metadata.get("title", "Untitled")
    reorder_footers(input_json, intermediate_json)
    source_for_parsing = intermediate_json
    if merge_consecutive:
        merged_file = 'merged.json'
        combine_consecutive_blocks(intermediate_json, merged_file)
        source_for_parsing = merged_file
    else:
        print("Merging of consecutive blocks disabled (merge_consecutive = False)")
    entries = get_entries_to_process(source_for_parsing)
    html_lines = build_html_content(entries, title_text)
    write_output(html_lines)
    if merge_consecutive and source_for_parsing != intermediate_json:
        try:
            os.remove(source_for_parsing)
        except OSError:
            pass
    print(f"Created {output_html}")

if __name__ == '__main__':
    create_html()

