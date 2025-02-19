'''
After exporting all annotations of say project_id=1, in the directory 'project_1',
I observed that the xml is preceded by gibbrish characters.
The following code, cleans xml by removing those gibberish characters

The script will:
- Remove any content before the XML declaration
- Remove any content after </annotations>
- Handle different encodings
- Verify that the cleaning was successful
'''

import os
import re
import chardet

directory_path = "/data3/deepti.rawat/check/project1"

"""
Process all XML files in the given directory to:
1. Remove content before the XML declaration
2. Remove content after </annotations>

Args:
    directory_path (str): Path to directory containing XML files
"""
# Patterns for cleaning
start_pattern = rb'^.*?(?=<\?xml version="1.0" encoding="utf-8"\?>)'
end_pattern = rb'</annotations>.*$'

# Get all XML files in the directory
xml_files = [f for f in os.listdir(directory_path) if f.endswith('.xml')]

for xml_file in xml_files:
    file_path = os.path.join(directory_path, xml_file)
    
    try:
        # Read the file in binary mode first
        with open(file_path, 'rb') as file:
            content = file.read()
        
        # Remove binary content before XML declaration
        cleaned_content = re.sub(start_pattern, b'', content, flags=re.DOTALL)
        
        # If no XML declaration found, try to find it with a more lenient pattern
        if b'<?xml' not in cleaned_content:
            lenient_pattern = rb'^.*?(?=<\?xml)'
            cleaned_content = re.sub(lenient_pattern, b'', content, flags=re.DOTALL)
        
        # Remove content after </annotations>
        cleaned_content = re.sub(end_pattern, b'</annotations>', cleaned_content, flags=re.DOTALL)
        
        # Detect the encoding of the cleaned content
        detection = chardet.detect(cleaned_content)
        encoding = detection['encoding'] if detection['encoding'] else 'utf-8'
        
        try:
            # Decode the cleaned content
            decoded_content = cleaned_content.decode(encoding)
            # Ensure it's in UTF-8
            final_content = decoded_content.encode('utf-8').decode('utf-8')
            
            # Write the cleaned content back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(final_content)
            
            print(f"Successfully cleaned {xml_file}")
            
        except UnicodeError:
            # If decoding fails, try writing the binary content directly
            with open(file_path, 'wb') as file:
                file.write(cleaned_content)
            print(f"Successfully cleaned {xml_file} (binary mode)")
            
    except Exception as e:
        print(f"Error processing {xml_file}: {str(e)}")
        
    # Verify the cleaning
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            final_check = file.read()
            if not final_check.endswith('</annotations>'):
                print(f"Warning: {xml_file} might not be properly cleaned. Please check manually.")
    except Exception as e:
        print(f"Warning: Could not verify {xml_file}: {str(e)}")
