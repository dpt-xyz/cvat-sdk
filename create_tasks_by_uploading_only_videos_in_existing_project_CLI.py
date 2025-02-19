"Create CVAT tasks under an existing project by uploading all video files in the specified directory."

import os
import sys
import subprocess
from pathlib import Path

# Configuration
VIDEO_DIR = "/xyz/original_videos"
PROJECT_ID = 6 # MANUALLY CHECK THIS FROM CVAT GUI
CVAT_USERNAME = ""
CVAT_PASSWORD = ""
SERVER_HOST = "http://xx.x.xx.xxx"
SERVER_PORT = 8080
video_dir = VIDEO_DIR
project_id = PROJECT_ID
cvat_username = CVAT_USERNAME
cvat_password = CVAT_PASSWORD
server_host = SERVER_HOST
server_port = SERVER_PORT
image_quality=70
frame_step=5 # Modify to the "frame step value for your videos"
bug_tracker_template="https://bug-tracker.com/{task_id}"

"""
Args:
    video_dir (str): Directory containing video files
    project_id (int): CVAT project ID
    cvat_username (str): CVAT username
    cvat_password (str): CVAT password
    server_host (str): CVAT server host
    server_port (int): CVAT server port
    image_quality (int): Image quality for frames (default: 70)
    frame_step (int): Frame step for video sampling (default: 5)
    bug_tracker_template (str): Template for bug tracker URL
"""
# Supported video extensions
# video_extensions = ('.mp4', '.avi', '.mov', '.mkv')
video_extensions = ('.mp4')

# Get all video files in the directory

video_files = sorted(
    f for f in os.listdir(video_dir) 
    if f.lower().endswith(video_extensions)
)

if not video_files:
    print(f"No video files found in {video_dir}")
    sys.exit()

print(f"Found {len(video_files)} video files")

# Process each video file
for video_file in video_files:
    video_path = os.path.join(video_dir, video_file)
    # task_name = Path(video_file).stem  # Get filename without extension
    task_name = Path(video_file)  # Get filename with extension
    
    # Construct the command
    command = [
        "cvat-cli",
        "--auth", f"{cvat_username}:{cvat_password}",
        "--server-host", server_host,
        "--server-port", str(server_port),
        "task", "create",
        task_name,
        "--project_id", str(project_id),
        "--bug_tracker", bug_tracker_template.format(task_id=task_name),
        "--image_quality", str(image_quality),
        "--frame_step", str(frame_step),
        "local",
        video_path
    ]
    
    try:
        # Execute the command
        print(f"\nCreating task for {video_file}...")
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Successfully created task '{task_name}'")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating task for {video_file}:")
        print(f"Exit code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        
    except Exception as e:
        print(f"Unexpected error creating task for {video_file}: {str(e)}")


