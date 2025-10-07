import pytest
import pandas as pd
import glob
from etl_core import normalise_data, transform_data

@pytest.fixture
def sample_df():
    batch_files = glob.glob('./test-data/json-payload/*.json')
    batch_df = []
    for filename in batch_files:
        df = pd.read_json(filename)
        df['file_name'] = filename
        batch_df.append(df)
    return pd.concat(batch_df)

@pytest.fixture
def single_sample_df():
    batch_files = ['./test-data/json-payload/sample-c.json']
    single_sample_df = []
    for filename in batch_files:
        df = pd.read_json(filename)
        df['file_name'] = filename
        single_sample_df.append(df)
    return pd.concat(single_sample_df)

def test_normalise_data(single_sample_df):
    df_norm = normalise_data(single_sample_df)
    assert 'program_id' in df_norm.columns
    assert 'task_id' in df_norm.columns
    assert len(df_norm) == 1
    assert df_norm['likes'].iloc[0] == 488

def test_transform_data(sample_df):
    df_norm = normalise_data(sample_df)
    valid, quarantine = transform_data(df_norm)
    assert not valid.empty
    assert quarantine.empty
    # Check standardization
    assert valid['name'].iloc[0] == 'John Doe'
    assert valid['platform'].iloc[0] == 'Instagram'
    assert valid['likes'].iloc[0] == 10

def test_transform_data_invalid_email(sample_df):
    df = sample_df.copy()
    df.at[0, 'email'] = 'not-an-email'
    df_norm = normalise_data(df)
    valid, quarantine = transform_data(df_norm)
    assert valid.empty
    assert not quarantine.empty
    assert pd.isna(quarantine['email'].iloc[0])
