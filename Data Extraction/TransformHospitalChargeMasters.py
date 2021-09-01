import pandas as pd
import numpy as np
import logging
import re

def log_execution():
    logFilePath = "logs/ChargeMaster.log"
    logLevel = logging.DEBUG 
    logging.basicConfig(filename=logFilePath,filemode='a',level=logLevel, \
                        format ='%(asctime)s %(levelname)s %(message)s', \
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.debug("Logging is configured - Log Level %s , Log File: %s",str(logLevel),logFilePath) 

def export_charge_masters(filepath, destination):
    log_execution()
    filenames, sheetnames = get_charge_master_locations(filepath)
    charge_master_df = read_charge_masters(filenames, sheetnames)
    combined_charge_masters = clean_up(charge_master_df)
    try:
        combined_charge_masters.to_csv(destination, index=False)
        logging.info("Exported clean Charge Masters under %s", str(destination))
    except:
        logging.error("Could not save %s", destination)

def get_charge_master_locations(filepath):
    try:
        logging.info("Reading %s", filepath)
        file_locations = pd.read_csv(filepath)
        filenames = file_locations['filepath']
        sheetnames = file_locations['sheetname']
        return filenames, sheetnames
    except:
        logging.error("Cannot read file %s.", filepath)

def read_charge_masters(filenames, sheetnames):
    df = pd.DataFrame()
    for filename, sheetname in zip(filenames, sheetnames):
        try:
            hospital = filename.split('\\')[-2]
            df_tmp = pd.read_excel(filename, sheet_name = sheetname, usecols=[0,1,2], names = ['Description', 'CPT', 'Charge'])
            df_tmp['CPT'] = df_tmp['CPT'].astype(str)
            df_tmp = df_tmp.loc[df_tmp.CPT.str.contains('\d\d\d\d\d', na=False),:]
            df_tmp['Hospital'] = hospital
            df = df.append(df_tmp)
            logging.info("Finished reading %s in %s", sheetname, filename)
        except:            
            logging.error("Cannot read file under filename: %s", filename) 
            pass
    return df

def clean_up(df):
    ## Ex. ranges => CPT Code 97161-9763 -> 97161, 97162, 97163
    ## Ex. splits => CPT Code 81002 or 81003
    try:
        logging.info("Cleaning dataframe...")
        df_range = extract_cpt_range(df)
        df_split = extract_cpt_split(df)
        df_int = extract_cpt_int(df)

        # re-combine dataframes
        df_all = pd.concat([df_range, df_split, df_int], ignore_index=True)
        df_all.sort_values(by='Hospital', inplace=True)
        df_all.drop_duplicates(keep='first', inplace=True, ignore_index=True)
        logging.info("Finished cleaning dataframe.")
        return df_all
    except:
        logging.error("Could not clean up final dataframe. Saving coarse data instead.")
        return df     

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

if __name__ == "__main__":
    # default folder and destination values
    folder = r".\Locations.csv"
    #folder = r"C:\Users\Beatrice Tierra\Documents\SpringBoard\US-Hospital-Charges\Datasets\ChargeMasterLocations.csv"
    destination = r".\Results.csv"
    export_charge_masters(folder, destination)