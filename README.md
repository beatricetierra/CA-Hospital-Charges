# US-Hospital-Charges

## Purpose
To increase the transparency of medical bills to patients, all hospitals in the US are required to release the standard charges, or “chargemasters”, on 300 of their most common services on their website. While this was a commendable attempt to help patients make more informed decisions on their health, the lack of accessibility to these chargemaster reports makes it extremely laborious to get any useful information. 

Firstly, the CMS (Centers for Medicare & Medicaid Services) has only required hospitals to make their charges available on their website. However, these reports are often hard to find and require users to click through many links before finding the information in large Excel or CSV files. After downloading the files, the patient must then search through the thousands of rows to find the specific treatment they are seeking.This is hardly an effort to make service costs transparent to their patients. 
Another issue is the lack of centralized data on hospital charges. Once a patient finally finds the cost of their expected treatment, they must redo the same process on another hospital’s website (most likely under different descriptions) to find the same information. This makes it much harder and longer for people to compare prices, negating the purpose of making the chargemasters public. 

To resolve the challenges in finding and comparing hospital treatment costs, I would like to build a data warehouse sourced from prices posted by each hospital in California and the cost patients would pay out-of-pocket based on insurance. The data warehouse would be centered around the cost per treatment per hospital based on the chargemaster datasets provided by each hospital. The key attributes would be the CPT code (medical service ID), hospital, insurance cost, hospital charges, and the time of the treatment. 

The hospital prices in California will come from the chargemasters aggregated from all hospitals since 2011 on the California Health and Human Services Agency website. All chargemasters per year are downloadable from the site and are stored in Excel files. Additionally, the average cost paid out-of-pocket by patients would be retrieved from the Fair Health Consumer healthcare estimator, which has collected 33 billion private health care claims and 36 billion Medicare claims for over 10,000 services in the US. This website does not make their database public as a single source, but offers a search tool to look up treatment cost per CPT code and zip code. As a work-around, web scraping will be used to gather all the average costs (in-network vs. out-of-network) per area in California. With over 300 hospitals and 10 years of data in California to process, I would first start by creating a small data warehouse for the year 2020, and migrate to a cloud warehouse to run on all years. 

In addition to the Hospital Chargemaster dataset, I also want to include a dataset of the CPT codes, hospital locations, insurance cost on each procedure, and the insurance providers offered at each hospital. A entity-relationship diagram is shown below to illustrate the final data warehouse.

![alt text](https://github.com/beatricetierra/US-Hospital-Charges/blob/main/ERD.png)

## Acquiring datasets

### Datasets:
1. Charge Masters
2. CA Hospital Profiles
3. CA Insurances
4. CPT Codes
5. Patient Expenses

### 1. Charge Masters
1. Download "Datasets/Chargemaster Dataset". This contains all CA hospitals' submitted chargemaster for 2020. 
2. Run script GetChargeMasterList.py using the command "python GetChargeMasterList.py <foldepath from step one> <output filename>.
   Example: python GetChargeMasterList.py "./Datasets/Chargemaster Dataset" "./results.csv"
  
### 2. CA Hospital Profiles 
1. Located in HospitalProfiles.csv 
  
### 3. CA Insurances 
1. Located in CAInsurances.csv 
  
### 4. CPT Codes
1. Located in "Datasets/CPTCodes"
  
### 5. Patient Expenses
1. Run GetInsuranceCost.py using the command "python GetInsuranceCost.py"
