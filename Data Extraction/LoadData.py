from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, IntegerType, ArrayType
from pyspark.sql.functions import split, explode, sequence, col
from pathlib import Path
from itertools import chain
import pandas as pd
import xlrd
import config

def get_excel_files(folder):
    # returns the path of each excel file
    xlsx_files = Path(folder).rglob('*.xlsx')
    xls_files = Path(folder).rglob('*.xls')
    all_files = sorted(chain(xlsx_files, xls_files))
    return all_files

def get_sheet_names(files):
    filepaths, sheetnames = [], []
    match_string = 'Evaluation & Management Services (CPT Codes 99201-99499)'

    for file in files:
        try:
            wb = xlrd.open_workbook(file)
            for sheet in wb.sheets():
                for row in sheet.get_rows():
                    if any([r.value == match_string for r in row]):
                        filepaths.append(file)
                        sheetnames.append(sheet.name)
        except xlrd.biffh.XLRDError:
            print("File restricted from reading")
            pass
    return filepaths, sheetnames

# Connect to blob storage
spark = SparkSession.builder.appName("app").getOrCreate()
spark.conf.set("fs.azure.account.key.cahospitalstorage.blob.core.windows.net", \
    "w3EYeDH//L+J0uscsn3BYDatbFCcB7CUXK4MfOSNmwc16v3WAQ7EPcw2IpchUrelLVuowjfugmv99e0Os8J5Sw==")

# Get all target excel sheets
data = r"C:\Users\Beatrice Tierra\Documents\Springboard\US-Hospital-Charges-Data\2020-hospital-chargemasters\Chargemaster CDM 2020"
excel_files = get_excel_files(data)
filepaths, sheetnames = get_sheet_names(excel_files)

# Read each target excel sheet and concatentate all rows with CPT code
schema = StructType([
    StructField('Description', StringType(), True),
    StructField('CPT', StringType(), True),
    StructField('Charge', StringType(), False)
])
df_all = spark.createDataFrame(spark.sparkContext.emptyRDD(), schema)

for filepath, sheet in zip(filepaths, sheetnames):
    pdf = pd.read_excel(filepath, sheet_name = sheet, 
                        usecols=[0,1,2], 
                        names = ['Description', 'CPT', 'Charge'])

    df_tmp = spark.createDataFrame(pdf, schema=schema)
    df_tmp = df_tmp.filter(df_tmp.CPT.rlike("\d{5}"))
    df_all = df_all.union(df_tmp)

# Clean up df_all
## Ex. ranges => CPT Code 97161-9763 -> 97161, 97162, 97163
## Ex. splits => CPT Code 81002 or 81003
df_ranges = df_all.filter(df_all.CPT.contains("-"))
df_split  = df_all.filter(df_all.CPT.rlike("/|or"))
df_int  = df_all.filter(~df_all.CPT.rlike("-|/|or"))

# df_ranges
df_array = df_ranges.withColumn('CPT_array', split('CPT', '-').cast(ArrayType(IntegerType())))
df_array = df_array.withColumn('CPT', explode(sequence(col('CPT_array')[0], col('CPT_array')[1])))
df_array = df_array.select(['Description', 'CPT', 'Charge'])

# df_split
df_split = df_split.withColumn('CPT',explode(split('CPT',"\/|or"))) 

# combine
df_new_rows = df_array.union(df_split)
df_final = df_new_rows.union(df_int)

# Export final df to blob storage
cloud_storage_path = "wasbs://chargemasters@cahospitalstorage.blob.core.windows.net/"
df_final.write.parquet(cloud_storage_path + "sample_output")