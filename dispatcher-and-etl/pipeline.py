import glob
import os
import sys
import uuid

from dotenv import load_dotenv
from etl_core import *

def load_batch():
    batch_files = glob.glob(os.getenv('DATA_FOLDER') + '/*.json')
    batch_df = []
    for filename in batch_files:
        df = pd.read_json(filename)
        df['id'] = str(uuid.uuid4())
        batch_df.append(df)
    return pd.concat(batch_df)

def save_in_db(df):
    engine = create_engine(os.getenv('PGSQL_DSN'))
    df.to_sql(os.getenv('DATABASE_TABLE'), engine, if_exists=os.getenv('DATABASE_MODE'), index=False)




# Load .env file
load_dotenv()

# List required environment variables
REQUIRED_VARS = ['DATA_FOLDER', 'DATABASE_TABLE', 'PGSQL_DSN', 'DATABASE_MODE']
missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
if missing:
    print(f"Missing required environment variables: {', '.join(missing)}'\nPlease consult the ReadMe file for a guide on how to get started", file=sys.stderr)
    sys.exit(1)


print("1 of 5. Loading JSON Files into memory.....")
batch_dfs = load_batch()
print("2 of 5. Normalising Data.....")
normalised_data = normalise_data(batch_dfs)
print("3 of 5. Cleaning Data.....")
clean_data, incomplete_data, all_data = transform_data(normalised_data)
print("4 of 5. Attempting to restore Missing Data.....")
restored_data = restore_missing_data(all_data, incomplete_data)
print("5 of 5. Uploading clean data to Postgres.....")
complete_df = pd.concat([clean_data, restored_data], ignore_index=True)
save_in_db(complete_df)
print(" --- Completed 5 of 5 tasks: The ETL pipeline has terminated ----")
