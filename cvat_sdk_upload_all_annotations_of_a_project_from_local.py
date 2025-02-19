""" Import annotations for tasks in a CVAT project from matching XML files. """
'''
This script:

Connects to your CVAT instance
Gets all tasks in the specified project
Looks for matching annotation files in the specified directory
Imports annotations for each task from its corresponding XML file

The matching logic works as follows:

For a task named "check1.mp4", it will look for files like:
"check1.xml"
'''

from cvat_sdk import make_client
import os

host="http://xx.x.xx.xxx"
port=8080
user=''
password=""
format='CVAT 1.1'
project_id=6 # modify to Project ID to which you want to upload the annotations
annotations_dir='/xyz/output_updated_xml_annots' # Directory containing annotation XML files


with make_client(host, port=port, credentials=(user, password)) as client:
    project = client.projects.retrieve(project_id) # Get project details
    tasks = project.get_tasks() # Get all tasks in the project
    annotation_files = [f for f in os.listdir(annotations_dir) if f.endswith('.xml')] # Get list of annotation files in the directory
    
    for task in tasks: # Process each task
        task_name = task.name # say, if task name on cvat is 'check', then the corresponding annotation file name should be 'check_annotations.xml'
        task_name = os.path.splitext(task_name)[0]  # Get filename without extension
        extension = os.path.splitext(task.name)[1][1:]

        # Look for matching annotation file
        matching_files = [
            f for f in annotation_files 
            if task_name in f or f.startswith(f"{task_name}")
        ]
        
        if matching_files:
            # Use the first matching file if multiple matches found
            annotation_file = matching_files[0]
            file_path = os.path.join(annotations_dir, annotation_file)
            
            try:
                # Import annotations for the task
                task.import_annotations(format, file_path)
                print(f"Successfully imported annotations for task '{task_name}.{extension}' from {annotation_file}")
                
            except Exception as e:
                print(f"Error importing annotations for task '{task_name}': {str(e)}")
        else:
            print(f"No matching annotation file found for task '{task_name}'")