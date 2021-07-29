import pandas as pd
import numpy as np
import re

def get_charge_master_locations():
    file_locations = pd.read_csv(r"C:\Users\Beatrice Tierra\Documents\Springboard\US-Hospital-Charges\Datasets\ChargeMasterLocations.csv")
    filepaths = file_locations['filepath']
    sheetnames = file_locations['sheetname']
    return filepaths, sheetnames

def read_charge_masters(filepaths, sheetnames):
    df = pd.DataFrame()
    for filepath, sheetname in zip(filepaths, sheetnames):
        hospital = filepath.split('\\')[-2]
        df_tmp = pd.read_excel(filepath, sheet_name = sheetname, usecols=[0,1,2], names = ['Description', 'CPT', 'Charge'])
        df_tmp['CPT'] = df_tmp['CPT'].astype(str)
        df_tmp = df_tmp.loc[df_tmp.CPT.str.contains('\d\d\d\d\d', na=False),:]
        df_tmp['Hospital'] = hospital
        df = df.append(df_tmp)
    return df

def clean_up(df):
    ## Ex. ranges => CPT Code 97161-9763 -> 97161, 97162, 97163
    ## Ex. splits => CPT Code 81002 or 81003 
    df_range = extract_cpt_range(df)
    df_split = extract_cpt_split(df)
    df_int = extract_cpt_int(df)

    # re-combine dataframes
    df_all = pd.concat([df_range, df_split, df_int], ignore_index=True)
    df_all.sort_values(by='Hospital', inplace=True)
    df_all.drop_duplicates(keep='first', inplace=True, ignore_index=True)

def extract_cpt_range(df):
    df_range_tmp = df[df['CPT'].str.contains('-')]
    df_range = create_separate_rows(df_range_tmp, '-')
    return df_range

def extract_cpt_split(df):
    df_split_tmp = df[df['CPT'].str.contains('or|/')]
    df_split = create_separate_rows(df_split_tmp, 'or|/')
    return df_split 

def extract_cpt_int(df):
    df_int = df[~df['CPT'].str.contains('-|or|/')]
    df_int = df_int[~df_int['Description'].str.contains('Facility')]
    df_int = df_int[['Hospital', 'Description', 'CPT', 'Charge']]
    return df_int

def create_separate_rows(df_tmp, parser):
    hospital, desc, cpt, charge = [], [], [], []
    for row in df_tmp.itertuples():
        num1 = int(re.split(parser, row.CPT)[0])
        try:
            num2 = int(re.split(parser, row.CPT)[1])
            if parser == 'or|/':
                num_range = [num1, num2]
            elif parser == '-':
                num_range = list(range(num1, num2+1))
        except: # in case num2 cannot be int
            num_range = [num1]

        # Add to lists to 
        num_rows = len(num_range)
        hospital.extend([row.Hospital] * num_rows)
        desc.extend([row.Description] * num_rows)
        cpt.extend(num_range)
        charge.extend([row.Charge] * num_rows)
    df_separated_rows =  pd.DataFrame({'Hospital':hospital, 'Description':desc, 'CPT': cpt, 'Charge': charge})
    return df_separated_rows

# 4. Merge separate dataframes into one
df_all.to_csv(r"C:\Users\Beatrice Tierra\Documents\Springboard\US-Hospital-Charges\Datasets\ChargeMasterList.csv", index=False)