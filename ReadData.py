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