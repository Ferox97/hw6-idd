import os
import json

def rename_key_in_dict(d, old_key, new_key):
    if old_key in d:
        d[new_key] = d.pop(old_key)
    for key, value in d.items():
        if isinstance(value, dict):
            rename_key_in_dict(value, old_key, new_key)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    rename_key_in_dict(item, old_key, new_key)

def merge_json_files(directory):
    merged_data = []
    
   
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            
        
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                  
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                rename_key_in_dict(item, "company", "name")
                        merged_data.extend(data)
                    elif isinstance(data, dict):
                        rename_key_in_dict(data, "company", "name")
                        merged_data.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error reading {file_path}: {e}")
    
  
    with open('merged_output.json', 'w') as output_file:
        json.dump(merged_data, output_file, indent=4)

    print("Merging completed. The merged data is saved in 'merged_output.json'.")


directory = 'sourcesJSON'

merge_json_files(directory)
