import pytest
import pandas as pd
import glob
from etl_core import normalise_data, transform_data, fill_row, restore_missing_data
import uuid

@pytest.fixture
def missing_sample_df():
    batch_files = ['./test-data/json-payload/sample-d.json', './test-data/json-payload/sample-e.json']
    batch_df = []
    for filename in batch_files:
        df = pd.read_json(filename)
        df['id'] = str(uuid.uuid4())
        batch_df.append(df)
    return pd.concat(batch_df)

@pytest.fixture
def single_sample_df():
    df = pd.read_json('./test-data/json-payload/sample-c.json')
    df['id'] = str(uuid.uuid4())
    return pd.concat([df])

@pytest.fixture
def single_faulty_sample_df():
    df = pd.read_json('./test-data/json-payload/sample-b.json')
    df['id'] = str(uuid.uuid4())
    return pd.concat([df])

def test_normalise_data(single_sample_df):
    df_norm = normalise_data(single_sample_df)
    assert 'program_id' in df_norm.columns
    assert 'task_id' in df_norm.columns
    assert len(df_norm) == 1
    assert df_norm['likes'].iloc[0] == 488

def test_transform_data(single_faulty_sample_df):
    df_norm = normalise_data(single_faulty_sample_df)
    valid, quarantine, all_records = transform_data(df_norm)
    # Check standardization
    assert valid['platform'].iloc[0] == 'Facebook'
    assert valid['likes'].iloc[0] == 0

def test_restore_missing_data(missing_sample_df):
    df_norm = normalise_data(missing_sample_df)
    valid, quarantine, all_records = transform_data(df_norm)
    if not quarantine.empty:
        restored = restore_missing_data(valid, quarantine)
        assert not restored.isna().all(axis=1).any()  # No row should be completely NaN
        assert restored.shape[0] == quarantine.shape[0]  # Same number of rows
