import xlrd
from pathlib import Path
from itertools import chain
import pandas as pd

# 1. Get all excel files
sheet_data = []   
folder = r"C:\Users\Beatrice Tierra\Documents\Springboard\US-Hospital-Charges\Datasets\Chargemaster Dataset"
xlsx_files = Path(folder).rglob('*.xlsx')
xls_files = Path(folder).rglob('*.xls')
all_files = sorted(chain(xlsx_files, xls_files))

# 2. Get all 'Common OP Procedure' sheet from each excel file
df = pd.DataFrame(columns=['filepath', 'sheetname'])
match_string = 'Evaluation & Management Services (CPT Codes 99201-99499)'

for file in all_files:
    try:
        wb = xlrd.open_workbook(file)
        for sheet in wb.sheets():
            for row in sheet.get_rows():
                if any([r.value == match_string for r in row]):
                    df = df.append({'filepath':file, 'sheetname':sheet.name}, ignore_index=True)
    except xlrd.biffh.XLRDError:
        pass

# 3. Export filepath and sheetname info
df.to_csv(r"C:\Users\Beatrice Tierra\Documents\Springboard\US-Hospital-Charges\Datasets\ChargeMasterLocations.csv")