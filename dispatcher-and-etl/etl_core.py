import pandas as pd
import uuid

from sqlalchemy import create_engine
from util import *


def normalise_data(df):
    df = df.melt(
        id_vars=['user_id', 'name', 'email', 'instagram_handle', 'tiktok_handle', 'joined_at', 'id'],
        value_vars=['advocacy_programs']).drop('variable', axis=1)
    df = df.reset_index(drop=True)
    normalised_advocacy_programs = pd.json_normalize(df['value']).fillna("").reset_index(drop=True)
    df = df.join(normalised_advocacy_programs)
    df = df.explode('tasks_completed')
    """
    if we have multiple tasks, we need to set total_sales_attributed to 0 for all but the first task
    this is to avoid double counting sales attributed to multiple tasks
    """
    is_duplicated = df.index.duplicated(keep='first')
    df.loc[is_duplicated, 'total_sales_attributed'] = 0
    df = df.reset_index(drop=True)
    normalised_tasks_completed = pd.json_normalize(df['tasks_completed'])
    """
        We do not expect to see identical tasks across the same program, so we eliminate duplicates here..
        We also do not expects to see identical tasks across different programs, this also eliminates that...

        Assumption: post_url is unique to a task and use, hence we do not expect to see the same post_url across different tasks
    """
    df_unique_tasks = normalised_tasks_completed.drop_duplicates(subset=['task_id', 'platform', 'post_url', 'likes', 'comments', 'shares', 'reach'])
    df = df.join(df_unique_tasks, how='right').reset_index(drop=True)
    final_columns = ['user_id', 'name', 'email', 'instagram_handle', 'tiktok_handle', 'joined_at',          'program_id',
                     'brand', 'total_sales_attributed', 'task_id', 'platform', 'post_url', 'likes', 'comments',
                     'shares', 'reach', 'id']
    return df[final_columns]



def transform_data(df):
    """ Step 1: Standardizing text formats """
    df[['user_id', 'program_id', 'task_id', 'email', 'instagram_handle', 'tiktok_handle', 'post_url', 'platform']] = (
    df[['user_id', 'program_id', 'task_id', 'email', 'instagram_handle', 'tiktok_handle', 'post_url', 'platform']]
    .astype(str).apply(lambda col: col.fillna("").str.lower().str.strip())
)
    df['name'] = df['name'].astype(str).str.title().str.strip()
    df['brand'] = df['brand'].astype(str).str.title().str.strip()
    df['platform'] = df['platform'].astype(str).str.capitalize().str.strip()
    df.loc[df['platform'] == 'Tiktok', 'platform'] = 'TikTok'
    # this will be sorted later.....
    df['joined_at'] = df['joined_at'].astype(str)

    # set value to -1 so we can identify missing values - -1 is a safe value since 0 may be an actual value
    df['likes'] = pd.to_numeric(df['likes'], errors='coerce').astype('Int64').fillna(0)
    df['comments'] = pd.to_numeric(df['comments'], errors='coerce').astype('Int64').fillna(0)
    df['shares'] = pd.to_numeric(df['shares'], errors='coerce').astype('Int64').fillna(0)
    df['reach'] = pd.to_numeric(df['reach'], errors='coerce').astype('Int64').fillna(0)
    df['total_sales_attributed'] = pd.to_numeric(df['total_sales_attributed'], errors='coerce').astype('Float64').fillna(-1.0)

    """ Step 2: Use validation functions to identify invalid data and set them to identificaiton and quarantine """

    validators = {
        'user_id': is_uuid,
        'name': is_valid_name,
        'email': is_valid_email,
        'instagram_handle': is_valid_instagram_handle,
        'tiktok_handle':is_valid_tiktok_handle,
        'joined_at': is_valid_date,
        'program_id': is_uuid,
        'total_sales_attributed': lambda x: isinstance(x, (int, float)) and x >= 0,
        'task_id': is_uuid,
        'platform': is_valid_platform,
        'post_url': is_valid_url,
        'likes': lambda x: x >= 0,
        'comments': lambda x: x >= 0,
        'shares': lambda x: x >= 0,
        'reach': lambda x: x >= 0
    }

    #display(df)
    #print("post validator -----")
    for col, validator in validators.items():
        dtype = df[col].dtype
        df[col] = df[col].apply(lambda x: x if validator(x) else pd.NA)
        # prevents everything from being converted back to object
        df[col] = df[col].astype(dtype)


    """ Step 3: Remove duplicates """
    # already handled in normalisation step
    # in case the same record has been placed in multiple files.....
    #deduplicated_df = df.drop_duplicates(subset=['user_id', 'name', 'email', 'instagram_handle', 'tiktok_handle', 'joined_at', 'program_id',
    #                 'brand', 'total_sales_attributed', 'task_id', 'platform', 'post_url', 'likes', 'comments',
    #                 'shares', 'reach'])

    return df[~df.isna().any(axis=1)], df[df.isna().any(axis=1)], df


def fill_row(target_cols, row, source_df, min_matches=1, suppress=None):
    missing_cols = [col for col in target_cols if pd.isna(row[col])]
    present_cols = [col for col in target_cols if not pd.isna(row[col])]

    if suppress is not None and suppress in missing_cols:
        missing_cols.remove(suppress)

    if len(present_cols)  >= min_matches and len(missing_cols) > 0:
        mask = pd.Series([True] * len(source_df))

        for col in present_cols:
            mask &= source_df[col] == row[col]

        # Exclude the row itself
        mask &= source_df.index != row.name
        matches = source_df[mask]
        if not matches.empty:
            # Take first matching row (can be improved for multiple matches)
            match = matches.iloc[0]
            for col in missing_cols:
                if not pd.isna(match[col]):
                    row[col] = match[col]
    return row



def restore_missing_data(full_df, incomplete_df):
    """ Attempting to restore missing user identifiers from the full dataset """
    user_identifiers = ['user_id', 'name', 'email', 'instagram_handle', 'tiktok_handle']
    incomplete_df = incomplete_df.apply(lambda row: fill_row(user_identifiers, row, full_df), axis=1)
    """ Attempting to restore missing joined_at from the full dataset """
    """

        Here, we require at least 2 matches to fill in the data for the following reasons:
        - because they have the same brand does not mean they are the same program or are performing the same task (similar for program)

        We also exempt task_id from being field and pass it for suppression to ensure we never try to fill in task_id as having the same program and brand does not indicate same task
    """
    campaign_identifiers = ['program_id', 'brand', 'task_id']
    incomplete_df = incomplete_df.apply(lambda row: fill_row(campaign_identifiers, row, full_df, 2, 'task_id'), axis=1)

    """ Extracting those that are acceptably incomplete """
    """
        - if we have been unable to restore the user_id, we can assign a new one, the implication being if we get a record for the same user_id later, it will be treated as a different user. A solution to this is to use the database to resolve missing fields instead of the batch dataframe as was done here (this was the initial plan but we scaled down due to time constraints)
        - if we have been unable to restore the joined_at, we can assign a new one, the implication being that the joined_at may be incorrect. Joined_at has no bearing in our analysis and adds no value except for information purpose or if time on plaform is required in future analysis [we assume it is not required for now]
        - if we have been unable to restore the program_id and brand, it means tha this is the single record for that program or all records for the program are incomplete, hence we drop the record
        - if we have been unable to restore the task_id, it means that this is the single record for that task or all records for the task are incomplete, hence we drop the record
        - If the record lacks all user identifiers it is dropped as we have no way of identifying the user - we could argue that we could accept if if task and performance detail exists to give a full picture of the task performance, but we assume that the idea is to maintain relationships with advocates and if you cant identify your advocate you can not maintain a relationship with them or reward them.
    """

    # ensuring at least one user identifier exists
    filtered_df = incomplete_df[~incomplete_df[user_identifiers].isna().all(axis=1)]
    # dropping all records without platform, brand and program_id
    filtered_df = filtered_df.dropna(subset=['platform', 'brand', 'program_id'])


    # patching missing user_id and joined_at with new values

    missing_count = filtered_df['user_id'].isna().sum()
    new_uuids = [str(uuid.uuid4()) for _ in range(missing_count)]
    filtered_df.loc[filtered_df['user_id'].isna(), 'user_id'] = new_uuids

    filtered_df['instagram_handle'] = filtered_df['instagram_handle'].fillna("")
    filtered_df['tiktok_handle'] = filtered_df['tiktok_handle'].fillna("")
    filtered_df['post_url'] = filtered_df['post_url'].fillna("")
    filtered_df['joined_at'] = filtered_df['joined_at'].fillna(arrow.now().format("YYYY-MM-DD HH:mm:ss ZZ"))
    filtered_df['total_sales_attributed'] = filtered_df['total_sales_attributed'].fillna(0.0)
    filtered_df['likes'] = filtered_df['likes'].fillna(0)
    filtered_df['comments'] = filtered_df['comments'].fillna(0)
    filtered_df['shares'] = filtered_df['shares'].fillna(0)
    filtered_df['reach'] = filtered_df['reach'].fillna(0)
    filtered_df['user_id'] = filtered_df['user_id'].fillna("").astype(str)
    filtered_df['program_id'] = filtered_df['program_id'].fillna("").astype(str)
    filtered_df['name'] = filtered_df['name'].fillna("").astype(str)
    filtered_df['email'] = filtered_df['email'].fillna("")


    return filtered_df




