import fitz  # PyMuPDF
import os
import json
import re
from collections import Counter

def clean_text(text):

    text = re.sub(r'\s+', ' ', text).strip()
    return "".join(char for char in text if char.isprintable())

def analyze_pdf_structure(pdf_path):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF {pdf_path}: {e}")
        return None

    styles = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_DICT)["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                       
                        if span['text'].strip():
                            styles.append({
                                'size': round(span['size']),
                                'font': span['font'],
                                'bold': "bold" in span['font'].lower(),
                                'text': clean_text(span['text']),
                                'page': page_num + 1
                            })
    
    if not styles:
        return {"title": "No text content found", "outline": []}

    font_sizes = [s['size'] for s in styles]
    if not font_sizes:
         return {"title": "No text content found", "outline": []}
    
    paragraph_size = Counter(font_sizes).most_common(1)[0][0]

    potential_headings = []
    title_candidate = {'size': 0, 'text': 'Untitled Document', 'page': 1}

    for style in styles:
        
        if style['page'] <= 2 and style['size'] > title_candidate['size']:
            title_candidate = style

  
    for style in styles:
        
        is_heading_candidate = style['size'] > paragraph_size and (style['bold'] or style['size'] >= paragraph_size + 2)
        
       
        is_not_title = style['text'] != title_candidate['text']

        if is_heading_candidate and is_not_title:
            potential_headings.append(style)

   
    heading_sizes = sorted(list(set([h['size'] for h in potential_headings])), reverse=True)
    
    size_to_level = {}
    if len(heading_sizes) > 0:
        size_to_level[heading_sizes[0]] = "H1"
    if len(heading_sizes) > 1:
        size_to_level[heading_sizes[1]] = "H2"
    if len(heading_sizes) > 2:
        size_to_level[heading_sizes[2]] = "H3"

  
    outline = []
    for heading in potential_headings:
        level = size_to_level.get(heading['size'])
        if level:
            outline.append({
                "level": level,
                "text": heading['text'],
                "page": heading['page']
            })

  
    outline.sort(key=lambda x: x['page'])

    return {
        "title": title_candidate['text'],
        "outline": outline
    }

def main():
   
    input_dir = "/app/input"
    output_dir = "/app/output"

   
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            print(f"Processing {pdf_path}...")
            
            result = analyze_pdf_structure(pdf_path)
            
            if result:
               
                base_name = os.path.splitext(filename)[0]
                output_path = os.path.join(output_dir, f"{base_name}.json")
                
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
                
                print(f"Successfully created outline at {output_path}")

if __name__ == "__main__":
    main()
