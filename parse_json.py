import json
import html

def main():
    print("Manually combine and nest headers before JSON parsing")
    input_json = 'output.json'
    output_html = 'input.html'
    allowed_labels = {'h1', 'h2', 'h3', 'p', 'blockquote', 'footnote'}
    title_input = input("Title: ")

    # Step 1: Read and parse the JSON lines file
    entries = []
    with open(input_json, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Error: Line {line_number} is not valid JSON. Skipping. ({e})")
                continue
            
            # Step 2: Validate required fields and allowed labels
            if 'label' not in entry or 'text' not in entry:
                print(f"Warning: Line {line_number} is missing 'label' or 'text'. Skipping.")
                continue
            label = entry['label']
            if label not in allowed_labels:
                print(f"Warning: Line {line_number} has invalid label '{label}'. Skipping.")
                continue
            
            entries.append(entry)

    # Step 3: Generate HTML elements from valid entries
    html_elements = []
    for entry in entries:
        label = entry['label']
        escaped_text = html.escape(entry['text'])
        
        # Handle footnote as a special case
        if label == 'footnote':
            element = f'    <p class="footnote">{escaped_text}</p>'
        else:
            element = f'    <{label}>{escaped_text}</{label}>'
        
        html_elements.append(element)

    # Step 4: Construct the HTML document
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title_input}</title>
</head>
<body>
{{}}
</body>
</html>""".replace('{}', '\n'.join(html_elements))

    # Step 5: Write the HTML content to the output file
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    main()
    print("Done")
