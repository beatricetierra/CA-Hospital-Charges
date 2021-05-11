import os
import re
import pandas as pd
from openpyxl import load_workbook      
            
def get_data(path, files):
    if len(files) == 1: # contains only compiled excel file
        filepath = path + "\\" + files[0]
        filepath_list = [filepath]
        sheets = get_sheet(filepath)
        return read_sheets(filepath_list, sheets)
    if len(files) > 1:  # contains multiple excel files
        if any('Common25' in f for f in files): # separated summary excel file
            target_files = list(filter(lambda f: 'Common25' in f, files))
            filepaths = list(map(lambda f: path + "\\" + f, target_files))
            return read_sheets(filepaths, [0]*len(filepaths))
        else: # multiple compiled excel files
            filepaths = list(map(lambda f: path + "\\" + f, files))
            sheets = sum([get_sheet(filepath) for filepath in filepaths], [])
            return read_sheets(filepaths, sheets) 

def get_sheet(filepath):
    regex = '(?i)(common|25|1045|top\s?25|\sab)'
    target_sheets = []

    xl = pd.ExcelFile(filepath)
    [target_sheets.append(sheet) for sheet in xl.sheet_names if re.search(regex, sheet)]
    return target_sheets

def read_sheets(filepaths, sheets):
    df = pd.DataFrame()
    for filepath in filepaths:
        for sheet in sheets:
            df_temp = pd.read_excel(filepath, sheet_name = sheet, header=None)
            df = df.append(df_temp, ignore_index=True)
    return df

def dict_to_excel(dictionary):
    filename = r"C:\Users\Beatrice Tierra\Documents\Springboard\US-Hospital-Charges\Results.xlsx"
    writer = pd.ExcelWriter(filename) # pylint: disable=abstract-class-instantiated
    for df_name, df in dictionary.items():
        try:
            df.to_excel(writer, sheet_name=df_name[:31])
        except:
            pass
    writer.save()

# Collect data and load into dictionary
dataset = r"C:\Users\Beatrice Tierra\Documents\Springboard\US-Hospital-Charges\Chargemaster Dataset"
hospital_names = os.listdir(dataset)
hospital_paths = list(map(lambda name: dataset + "\\" + name, hospital_names))
hospital_charges = {}

for name, path in zip(hospital_names, hospital_paths):
    excel_files = [files for files in os.listdir(path) if '.xlsx' in files or '.xls' in files]
    accepted_files = [files for files in excel_files if ('CDM' in files or 'Common25' in files) 
                        and 'Cloud' not in files]
    data = get_data(path, accepted_files)
    hospital_charges[name] = data

# Export to excel file
dict_to_excel(hospital_charges)