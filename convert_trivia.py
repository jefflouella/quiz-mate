#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import json
import subprocess
import re

# Extract the XML from the DOCX file
result = subprocess.run(
    ['unzip', '-p', 'Internet Legends Trivia Questions.docx', 'word/document.xml'],
    capture_output=True,
    text=True
)

xml_content = result.stdout

# Parse the XML
root = ET.fromstring(xml_content)

# Define namespaces
ns = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
}

# Extract all text elements with their formatting
paragraphs = []
for para in root.findall('.//w:p', ns):
    text_parts = []
    is_bold = False
    is_red = False
    
    for run in para.findall('.//w:r', ns):
        # Check formatting
        rPr = run.find('w:rPr', ns)
        if rPr is not None:
            bold = rPr.find('w:b', ns)
            color = rPr.find('w:color', ns)
            is_bold = bold is not None
            is_red = color is not None and color.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') == '980000'
        
        # Get text
        t = run.find('w:t', ns)
        if t is not None and t.text:
            text_parts.append({
                'text': t.text,
                'bold': is_bold,
                'red': is_red
            })
    
    if text_parts:
        paragraphs.append(text_parts)

# Process paragraphs into questions
questions = []
current_question = None
current_answers = []

for para in paragraphs:
    full_text = ''.join([p['text'] for p in para]).strip()
    
    if not full_text:
        continue
    
    # Check if this is a question (ends with ?)
    if full_text.endswith('?'):
        # Save previous question if exists and has exactly 4 answers
        if current_question and len(current_answers) == 4:
            questions.append({
                'question': current_question,
                'answers': current_answers,
                'correct_index': next((i for i, ans in enumerate(current_answers) if ans['is_correct']), 0)
            })
        
        current_question = full_text
        current_answers = []
    
    # Check if this is an answer (starts with A), B), C), D))
    elif re.match(r'^[A-D]\)', full_text) and len(current_answers) < 4:
        # Remove the letter and parenthesis
        answer_text = re.sub(r'^[A-D]\)\s*', '', full_text)
        # Check if this answer is marked as correct (red and bold)
        is_correct = any(p['red'] and p['bold'] for p in para)
        current_answers.append({
            'text': answer_text,
            'is_correct': is_correct
        })

# Add the last question if it has exactly 4 answers
if current_question and len(current_answers) == 4:
    questions.append({
        'question': current_question,
        'answers': current_answers,
        'correct_index': next((i for i, ans in enumerate(current_answers) if ans['is_correct']), 0)
    })

# Convert to the required JSON format
output = {
    "title": "Internet Legends Trivia",
    "questions": []
}

for q in questions:
    output["questions"].append({
        "question": q['question'],
        "correct": q['correct_index'],
        "answers": [ans['text'] for ans in q['answers']]
    })

# Write to JSON file
with open('internet-legends-trivia.json', 'w') as f:
    json.dump(output, f, indent=4)

print(f"Converted {len(questions)} questions to JSON format")
print(f"Output saved to: internet-legends-trivia.json")
