import sys
from ExtractHospitalChargeMasters import find_form_locations

if __name__ == "__main__":
    charge_master_folderpath = str(sys.argv[1])
    result_filepath = str(sys.argv[2])
    find_form_locations(charge_master_folderpath, result_filepath)