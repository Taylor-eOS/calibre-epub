import json

def reorder_footers(input_json, output_json):
    entries = []
    #Read entries from the input file
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
    #Process entries to reorganize footers
    chapters = []
    current_chapter = None
    for entry in entries:
        label = entry.get('label', '')
        if label == 'h1':
            if current_chapter is not None:
                chapters.append(current_chapter)
            current_chapter = {
                'entries': [entry],
                'footers': []}
        else:
            if current_chapter is None:
                #Handle entries before the first h1
                current_chapter = {
                    'entries': [],
                    'footers': []}
            if label == 'footer':
                current_chapter['footers'].append(entry)
            else:
                current_chapter['entries'].append(entry)
    #Add the last chapter after processing all entries
    if current_chapter is not None:
        chapters.append(current_chapter)
    #Flatten the chapters into the result list
    result = []
    for chapter in chapters:
        result.extend(chapter['entries'])
        result.extend(chapter['footers'])
    #Write the reordered entries to the output file
    with open(output_json, 'w', encoding='utf-8') as f:
        for entry in result:
            json_line = json.dumps(entry, ensure_ascii=False)
            f.write(json_line + '\n')

if __name__ == '__main__':
    reorder_footers('footer_test.json', 'footer_test_output.json')

