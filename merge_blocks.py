import json

def combine_consecutive_blocks(input_json, output_json):
    entries = []
    with open(input_json, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                entries.append(entry)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line {line_number}: {e}")
                raise
    processed_entries = []
    for entry in entries:
        if entry.get('label') == 'exclude':
            continue
        if processed_entries and not entry.get('label') == "footer":
            last_entry = processed_entries[-1]
            #Check if the current entry has the same label as the last processed entry
            if(entry.get('label') == last_entry.get('label')):
                last_text = last_entry.get('text', '')
                current_text = entry.get('text', '')
                #Combine the texts, stripping whitespace and joining with a single space
                combined_text = ' '.join([last_text.strip(), current_text.strip()]).strip()
                if combined_text:
                    last_entry['text'] = combined_text
            else:
                processed_entries.append(entry)
        else:
            processed_entries.append(entry)
    with open(output_json, 'w', encoding='utf-8') as f:
        for entry in processed_entries:
            json_line = json.dumps(entry, ensure_ascii=False)
            f.write(json_line + '\n')

if __name__ == '__main__':
    combine_consecutive_blocks('footer_test.json', 'footer_test_output.json')

