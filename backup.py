import shutil
import os
from datetime import datetime
from configparser import ConfigParser 

print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")


config = ConfigParser()
config.read('\\'.join(__file__.split("\\")[:-1])+"\\config.ini")

src = config['backup_config']['source_dir']
dst = config['backup_config']['destination_dir']
identifier = config['backup_config']['folder_identifier']

folderstamp = datetime.now().strftime("%Y%m%d%H%M%S")
dst_full = dst + "/" + identifier + folderstamp

def log(log_text): 
    log_text = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]: ") + log_text
    print(log_text)
    with open(dst + "/main-log.txt", "a") as fileLog:
        fileLog.write(log_text + "\n")
    if os.path.exists(dst_full):
        with open(dst_full + "/" + identifier + "folder-log.txt", "a") as fileLog:
            fileLog.write(log_text + "\n")
    return (log_text)

def spacer(log_text):
    with open(dst + "/main-log.txt", "a") as fileLog:
        fileLog.write(''.join(['-' for i in range(len(log_text))])+'\n')

if not os.path.exists(dst):
    print(f"ERROR: Destination ({dst}) is not a valid path!")
    exit()

log("Starting Checkup...")

try:
    max_backups = int(config['backup_config']['backups_kept'])
except ValueError as error_string:
    spacer(log(f"ERROR: Value of backups_kept is not valid | {error_string}"))
    exit()

if not os.path.exists(src):
    spacer(log(f"ERROR: Source ({src}) is not a valid path!"))
    exit()

if os.path.exists(dst_full):
    spacer(log(f"ERROR: Folder ({identifier}{folderstamp}) already exists!"))
    exit()

while len([x for x in os.listdir(dst) if x[0:len(identifier)]==identifier]) >= max_backups:
    try:
        shutil.rmtree(dst + "/" + [x for x in os.listdir(dst) if x[0:len(identifier)]==identifier][0])

    except Exception as error_string:        
        spacer(log(f"ERROR: {error_string} ({identifier}{folderstamp})"))
        exit();


log("Creating Backup...")

try:
    shutil.copytree(src=src ,dst=dst_full)
except Exception as error_string:
    spacer(log(f"ERROR: {error_string} ({identifier}{folderstamp})"))
    exit();

spacer(log(f"Backup Completed! ({identifier}{folderstamp})"))
