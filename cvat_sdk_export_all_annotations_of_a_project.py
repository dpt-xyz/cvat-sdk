'''Export all annotations of a project with project_id=1'''

# SDK support: https://github.com/cvat-ai/cvat/issues/6197 

from cvat_sdk import make_client
import os

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
    
    for task in tasks: # Export each task's annotations separately
        task_name = os.path.splitext(task_name)[0] # I assume that my task name is like 'abc.mp4', and I want to strip the extension
        # print("here!")
        output_file = os.path.join(output_dir, f'{task.name}.xml')
        # output_file = os.path.join(output_dir, f'task_{task.id}_annotations.xml') # OR

        # Export task annotations without images
        task.export_dataset(format_name=format, filename=output_file, include_images=False)
        print(f"Exported annotations for task {task.id} to {output_file}")

    # client.projects.retrieve(project_id).export_dataset(format, filename, include_images=False)

# ..................................................................................................
