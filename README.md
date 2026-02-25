# just-artcritic
This is a small addition to a great art project.

# Usage

### 1. create a virtual environment in the folder of the artcritic.py file:
```bash
cd /absolute/path/to/the/directory/with/the/python/script
python3 -m venv venv
```

### 2. activate the virtual environment (while still in the directory with the artcritic.py file):

on MacOS/Linux:
```bash
source venv/bin/activate
```
on Windows:
```bash
venv\Scripts\activate
```

### 3. install the required packages with
```bash
python -m pip instal -r requirements.txt
```

### 4. create a file called .env in the same folder with these environment variables:
```text
ANTHROPIC_API_KEY="your-anthropic-api-key-here"
WATCH_DIR="/absolute/path/to/your/watchfolder"
TARGET_DIR="/absolute/path/to/your/target_folder"
```

### 5. adjust the system prompt in system_prompt.txt to your liking

### 6. start the script with
```bash
python artcritic.py
```
now, as long as the script runs, whenever a jpg is added to the watchfolder,
it gets a title from claude and saves it in a textfile alongside
a copy of the image in the target folder.
if an error occurrs in the naming process, "Untitled" is used instead.

### 7. to stop just use a keyboard interrupt (<ctrl>+c),
there is currently no way to gracefully shut down the script.


# CAVEATS:
This script has NOT been thoroughly testet.
No checks and safeguards are in place.
It currently ONLY works with .jpg files.
