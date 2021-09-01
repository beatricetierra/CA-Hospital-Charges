import xlrd
from pathlib import Path
from itertools import chain
import pandas as pd
import logging

def log_execution():
    logFilePath = "logs/ChargeMaster.log"
    logLevel = logging.DEBUG 
    logging.basicConfig(filename=logFilePath,filemode='a',level=logLevel, \
                        format ='%(asctime)s %(levelname)s %(message)s', \
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.debug("Logging is configured - Log Level %s , Log File: %s",str(logLevel),logFilePath) 

def find_form_locations(folder, destination):
    log_execution()
    all_files = get_excel_files(folder)
    form_locations = get_sheet_names(all_files)
    try:
        form_locations.to_csv(destination)
        logging.info("Saved all found Common OP Procedure forms under: ", destination)
    except:
        logging.error("Could not save ", destination)

def get_excel_files(folder):
    xlsx_files = Path(folder).rglob('*.xlsx')
    xls_files = Path(folder).rglob('*.xls')
    all_files = sorted(chain(xlsx_files, xls_files))
    return all_files

def get_sheet_names(all_files):
    df = pd.DataFrame(columns=['filepath', 'sheetname'])
    match_string = 'Evaluation & Management Services (CPT Codes 99201-99499)'

    for file in all_files:
        try:
            wb = xlrd.open_workbook(file)
            for sheet in wb.sheets():
                for row in sheet.get_rows():
                    if any([r.value == match_string for r in row]):
                        df = df.append({'filepath':file, 'sheetname':sheet.name}, ignore_index=True)
                        logging.info("Found Common OP Procedures form for %s under sheetname: %s", file, sheet.name)
        except xlrd.biffh.XLRDError:
            logging.error("Excel file is restricted from reading file: %s", file)
            pass
    return df


if __name__ == "__main__":
    # default folder and destination values
    folder = r"C:\Users\Beatrice Tierra\Documents\SpringBoard\US-Hospital-Charges\Datasets\Chargemaster Dataset"
    destination = r".\results.csv"
    find_form_locations(folder, destination)