import os
import sys
from ExtractHospitalChargeMasters import find_form_locations
from TransformHospitalChargeMasters import export_charge_masters

if __name__ == "__main__":
    charge_master_folderpath = str(sys.argv[1])
    results = str(sys.argv[2])
    intermediate_file = os.path.join(charge_master_folderpath, "Locations.csv")

    find_form_locations(charge_master_folderpath, intermediate_file)
    export_charge_masters(intermediate_file, results)