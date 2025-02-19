# cvat-sdk

## Description

This repository provides scripts to automate the export and import of files on a CVAT server.

## Requirements
`pip install cvat-sdk`
`pip install cvat-cli`

## References
https://docs.cvat.ai/docs/api_sdk/cli/

https://docs.cvat.ai/docs/api_sdk/sdk/highlevel-api/


## I. Create Multiple Tasks in a Project (Upload multiple Videos to CVAT Server)

- Create CVAT tasks under an existing project by uploading all video files from a specified directory.
- A simple bash command for this is provided in Section III ("Other CVAT CLI Commands"), but it uploads only one video at a time.
- The following script allows uploading multiple videos to the same project: `create_tasks_by_uploading_only_videos_in_existing_project_CLI.py`


## II. Import Annotations Corresponding to Videos

- If annotation files (`.xml`) for the uploaded videos are stored locally, upload them to the CVAT server for the relevant videos (tasks) using:
`cvat_sdk_upload_all_annotations_of_a_project_from_local.py`


## III. Export Annotations Corresponding to Videos

- Download all xml annotation files corresponding to a video (task) from the CVAT server using:  
`cvat_sdk_export_all_annotations_of_a_project.py`

-----------------------------------------------------------------------------------------------------------

## Other CVAT CLI Commands

### I. List All Tasks
`cvat-cli --auth <user>:<password> --server-host <http://xx.x.xx.xxx> --server-port <xxxx>  task ls`


### II. Create a Task from a Video, XML and Labels JSON
`cvat-cli --auth <user>:<password> --server-host <http://xx.x.xx.xxx> --server-port <xxxx> task create "<task-name>" --labels <labels.json> --bug_tracker https://bug-tracker.com/0001 --image_quality 70 --annotation_path <annot.xml> --annotation_format "CVAT 1.1" local <video.mp4> --frame_step 5`


### III. Create a Task Within an Existing Project
- Labels from the project will be automatically used, so labels.json is not required.
`cvat-cli --auth <user>:<password> --server-host <http://xx.x.xx.xxx> --server-port <xxxx> task create "<task-name>" --project_id <id> --bug_tracker https://bug-tracker.com/0001 --image_quality 70 --annotation_path <annot.xml> --annotation_format "CVAT 1.1" local <video.mp4> --frame_step 5`


### IV. Import Annotations from a Dataset
- Import annotation into task with ID `105`, in CVAT 1.1 format from the file `annotation.xml`.
`cvat-cli --auth <user>:<password> --server-host <http://xx.x.xx.xxx> --server-port <xxxx> task import-dataset --format "CVAT 1.1" 105 annotation.xml`


### V. Save Specific Frames from a Task
- Save frame `12, 15, 22` from task with ID `119`, into “images” folder with compressed quality:
`cvat-cli --auth <user>:<password> --server-host <http://xx.x.xx.xxx> --server-port <xxxx> task frames --outdir images --quality compressed 119 12 15 22`


### VI. Export Annotations of a Task
- Export annotation from task ID `4`, in the "CVAT for images 1.1" format and save them to `output.zip`.
`cvat-cli --auth <user>:<password> --server-host <http://xx.x.xx.xxx> --server-port <xxxx> task export-dataset --format "CVAT for video 1.1" 4 output.zip`