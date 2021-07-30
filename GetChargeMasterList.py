import sys
from ExtractHospitalChargeMasters import find_form_locations
from TransformHospitalChargeMasters import export_charge_masters

if __name__ == "__main__":
    charge_master_folderpath = str(sys.argv[1])
    extract_results = str(sys.argv[2])
    transform_results = str(sys.argv[3])

    find_form_locations(charge_master_folderpath, extract_results)
    export_charge_masters(extract_results, transform_results)