import os
import pandas as pd
from openpyxl import load_workbook

def get_data(path, files):
    if len(files) == 0:
        return 
    elif len(files) == 1:
        filepath = path + "\\" + files[0]
        sheets = get_sheets(filepath)
        return [read_sheet(filepath, sheet) for sheet in sheets]
    elif len(files) > 1:
        files = get_files(files)
        filepaths = list(map(lambda file: path + "\\" + file, files))
        return [read_sheet(filepath) for filepath in filepaths]

def get_files(files):
    filtered = []
    for file in files:
        if 'Common25' in file:
            filtered.append(file)
    return filtered

def get_sheets(filepath):
    xl = pd.ExcelFile(filepath)
    keys = ['1045', '25', 'Common']

    sheets= [sheet for sheet in xl.sheet_names if 
            any([key for key in keys if key in sheet])]
    return sheets

def read_sheet(filepath, sheet=0):
    df = pd.read_excel(filepath, 
                   sheet_name=sheet, 
                   header=None,
                   names=['Description', 'CPT Code', 'Amount'])

    df['CPT Code'] = pd.to_numeric(df['CPT Code'], errors='coerce')
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

    df.dropna(axis=0, inplace=True)
    df['CPT Code'] = df['CPT Code'].astype(int)
    return df

def dict_to_excel(dictionary):
    filename = r"C:\Users\Beatrice Tierra\Documents\Springboard\US-Hospital-Charges\Results.xlsx"
    writer = pd.ExcelWriter(filename) # pylint: disable=abstract-class-instantiated
    for df_name, l in dictionary.items():
        try:
            for df in l:
                df.to_excel(writer, sheet_name=df_name)
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
    data = get_data(path, excel_files)
    hospital_charges[name] = data

# Export to excel file
dict_to_excel(hospital_charges)