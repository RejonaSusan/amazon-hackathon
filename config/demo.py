import re
import spacy
import os
from PIL import Image
import pytesseract
import os

def extract_text_from_image(image_path):

    img = Image.open(image_path)

    text = pytesseract.image_to_string(img)
    return text


nlp = spacy.load('en_core_web_sm')

def identify_entity_values(text):
    doc = nlp(text)
    entities = {"weight": ['gram',
        'kilogram',
        'microgram',
        'milligram',
        'ounce',
        'pound',
        'ton']}
    
    weight_pattern = re.compile(r'\b\d+(\.\d+)?\s?(kg|g|grams|kilograms)\b', re.IGNORECASE)
    
    for match in weight_pattern.finditer(text):
        entities["weight"].append(match.group())
    
    return entities

def process_images_in_folder(image_folder):
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        print(f"Processing {image_file}...")
        
        extracted_text = extract_text_from_image(image_path)
        print(f"Extracted Text: {extracted_text}")
        
        entities = identify_entity_values(extracted_text)
        print(f"Entities Found: {entities}")

image_folder = '/Users/rejonasusan/Desktop/student_resource 3/dataset/imgs'
process_images_in_folder(image_folder)