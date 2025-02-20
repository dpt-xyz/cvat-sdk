'''
Export all annotations of a project with project_id=1

Description:
This code downloads the ZIP file of the exported task from a locally hosted CVAT server, 
extracts the XML, renames it to <task_name>.xml, and deletes the ZIP file after extraction.
'''
# SDK support: https://github.com/cvat-ai/cvat/issues/6197 

from cvat_sdk import make_client
import os
import zipfile
from tqdm import tqdm

host="http://xx.x.xx.xxx"
port=8080
user=''
password=""
format='CVAT for video 1.1'
project_id=1 # Confirm from GUI and modify
output_dir='project1' # Fetch from local and modify # This folder contains xml files (annotations)


os.makedirs(output_dir, exist_ok=True) # Create output directory if it doesn't exist

with make_client(host, port=port, credentials=(user, password)) as client:
    project = client.projects.retrieve(project_id) # Get project details
    tasks = project.get_tasks() # Get all tasks in the project

    for task in tqdm(tasks): # Export each task's annotations separately
        task_name = os.path.splitext(task.name)[0] # Strip file extension
        zip_file = os.path.join(output_dir, f'{task_name}.zip')
        xml_file = os.path.join(output_dir, f'{task_name}.xml')
        
        # Export task annotations as a ZIP file
        task.export_dataset(format_name=format, filename=zip_file, include_images=False)
        print(f"Exported annotations for task {task.id} to {zip_file}")
        
        # Extract the XML file from the ZIP
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            extracted_files = zip_ref.namelist()
            for file in extracted_files:
                if file.endswith(".xml"):  # Ensure we're extracting only XML
                    zip_ref.extract(file, output_dir)
                    extracted_xml_path = os.path.join(output_dir, file)
                    os.rename(extracted_xml_path, xml_file)
                    print(f"Extracted and renamed: {xml_file}")
                    break  # Stop after extracting the first XML file
        
        # Delete the ZIP file after successful extraction
        os.remove(zip_file)
        print(f"Deleted ZIP file: {zip_file}")
