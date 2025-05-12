import os
import csv
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_back.settings')
django.setup()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PARTS_DIR = os.path.join(SCRIPT_DIR, 'db_parts')

from foods.models import Product
from exercises.models import Exercise

def clean_float(value):
    if not value:
        return 0
    
    numeric_part = re.sub(r'[^\d.\-]', '', value)
    
    if not numeric_part:
        return 0
    
    try:
        return float(numeric_part)
    except ValueError:
        return 0

def import_products():
    csv_file_path = os.path.join(DB_PARTS_DIR, 'products.csv')
    
    if not os.path.exists(csv_file_path):
        print(f"Error: File not found: {csv_file_path}")
        return False
    
    Product.objects.all().delete()
    
    count = 0
    errors = 0
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
        print(f"CSV Preview: {content[:500]}...")
        
        
        file.seek(0)
        
        reader = csv.DictReader(file)
        for row_num, row in enumerate(reader, start=2):
            try:
                calories = clean_float(row.get('calories', '0'))
                protein = clean_float(row.get('protein', '0'))
                fat = clean_float(row.get('fat', '0'))
                carbs = clean_float(row.get('carbs', '0'))
                fiber = clean_float(row.get('fiber', '0'))
                sugar = clean_float(row.get('sugar', '0'))
                sodium = clean_float(row.get('sodium', '0'))
                
                Product.objects.create(
                    name=row.get('name', f"Product {row_num}"),
                    calories=calories,
                    protein=protein,
                    fat=fat,
                    carbs=carbs,
                    fiber=fiber,
                    sugar=sugar,
                    sodium=sodium,
                    allergens=row.get('allergens', '')
                )
                count += 1

            except Exception as e:
                errors += 1
                print(f"Error in row {row_num}: {str(e)}")
                print(f"Row data: {row}")

                continue
    
    print(f"Successfully imported {count} products.")
    if errors > 0:
        print(f"Encountered {errors} errors during import.")
    return count > 0

def import_exercises():
    csv_file_path = os.path.join(DB_PARTS_DIR, 'exercises.csv')
    
    if not os.path.exists(csv_file_path):
        print(f"Error: File not found: {csv_file_path}")
        return False
    
    Exercise.objects.all().delete()
    
    count = 0
    errors = 0
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        print(f"CSV Preview: {content[:500]}...")
        
        file.seek(0)
        
        reader = csv.DictReader(file)
        for row_num, row in enumerate(reader, start=2):
            try:
                intensity_mapping = {
                    'low': 'низька',
                    'medium': 'середня',
                    'high': 'висока'
                }
                
                intensity = intensity_mapping.get(row.get('intensity', ''), 'medium')
                
                Exercise.objects.create(
                    name=row.get('name', f"Exercise {row_num}"),
                    type=row.get('type', 'other'),
                    description=row.get('description', ''),
                    duration=int(clean_float(row.get('duration', '0'))),
                    intensity=intensity,
                    calories_burned=int(clean_float(row.get('calories_burned', '0')))
                )
                count += 1
            except Exception as e:
                errors += 1
                print(f"Error in row {row_num}: {str(e)}")
                print(f"Row data: {row}")

                continue
    
    print(f"Successfully imported {count} exercises.")
    if errors > 0:
        print(f"Encountered {errors} errors during import.")
    return count > 0

def import_all_data():
    print("Starting data import...")
    products_result = import_products()
    exercises_result = import_exercises()
    
    if products_result and exercises_result:
        print("All data successfully imported!")
    else:
        print("Some imports failed. Check the error messages above.")

if __name__ == "__main__":
    import_all_data() 