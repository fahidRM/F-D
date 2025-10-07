
import json
import os
import shutil
import sys

from dotenv import load_dotenv
from jsonschema import Draft7Validator
from json_repair import repair_json
from schema import schema



def check_for_structural_and_schema_issues(filename):
    validator = Draft7Validator(schema)
    filepath = os.path.join(os.getenv('DATA_FOLDER'), filename)
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            # if it loads then it is a valid JSON doc so we can validate against teh schema
            errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
            if errors:
                quarantine_file(filename)
        except json.JSONDecodeError:
            fix_structural_issues(filename)
        except:
            quarantine_file(filename)

def check_for_structural_and_schema_issues_iter():
    for filename in os.listdir(os.getenv('DATA_FOLDER')):
        if filename.endswith(".json"):
            check_for_structural_and_schema_issues(filename)

def fix_structural_issues(filename):
    fixed_file_name = f"fixed_{filename}"
    fixed_file_path = os.path.join(os.getenv('DATA_FOLDER'), fixed_file_name)
    file_path = os.path.join(os.getenv('DATA_FOLDER'), filename)

    broken_json = ""
    with open(file_path, 'r', encoding='utf-8') as f:
        broken_json = f.read()

    fixed_json = repair_json(broken_json)
    if fixed_json:
        with open(fixed_file_path, 'w', encoding='utf-8') as fw:
            fw.write(fixed_json)
        check_for_structural_and_schema_issues(fixed_file_name)

    quarantine_file(filename)

def quarantine_file(filename):
    src_path = os.path.join(os.getenv('DATA_FOLDER'), filename)
    dest_path = os.path.join(os.getenv('QUARANTINE_FOLDER'), filename)
    os.makedirs(os.getenv('QUARANTINE_FOLDER'), exist_ok=True)
    shutil.move(src_path, dest_path)


# Load .env file
load_dotenv()

# List required environment variables
REQUIRED_VARS = ['DATA_FOLDER', 'QUARANTINE_FOLDER', 'PGSQL_DSN']

missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
if missing:
    print(f"Missing required environment variables: {', '.join(missing)}'\nPlease consult the ReadMe file for a guide on how to get started", file=sys.stderr)
    sys.exit(1)

check_for_structural_and_schema_issues_iter()
print(" ---- Finished Structural and Schema checks -----")
print(" --- all files in quarantine folder have issues: some were fixed and added into the data folder ---")