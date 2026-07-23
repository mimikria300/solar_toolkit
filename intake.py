import os

to_upload = [
    #('ACE_AC_H0_SWE_v01_u2026-05-20T13-35-00.zip', 'ACE_AC_H0_SWE_v01_matchfile.json'),
    #('WIND_WI_K0_SWE_v01_u2026-05-20T13-36-00.zip','WIND_WI_K0_SWE_v01_matchfile.json'),
    #('WIND_WI_OR_PRE_v01_u2026-05-20T13-37-00.zip','WIND_WI_OR_PRE_v01_matchfile.json'),
    ('ACE_AC_H0_MFI_v00_umatchtest.zip','ACE_AC_H1_MFI_v00_matchfile.json'),
    #('ACE_AC_OR_SSC_v00_umatchtest.zip','ACE_AC_OR_SSC_v00_matchfile.json'),
    #('WIND_WI_K0_SWE_v00_umatchtest.zip','WIND_WI_K0_SWE_v00_matchfile.json'),
    #('WIND_WI_OR_PRE_v00_umatchtest.zip','WIND_WI_OR_PRE_v00_matchfile.json'),
    #('',''),
]

#a little section to store pastable undo commands
'''
2026-05-20T13-35-00_ACE_AC_H0_SWE_v01 ACE_AC_H0_SWE_v01
umatchtest_ACE_AC_H0_MFI_v00 ACE_AC_H0_MFI_v00
'''

# Path to manage.py
manage_py = "/home/mxxun/dev/solarbase/solar_project_2/solar_project/olarterra/manage.py"

def get_dataset_tag(zip_filename):
    return zip_filename.split('_u')[0]

def get_upload_tag(zip_filename):
    return zip_filename.split('_u')[-1].replace('.zip', '')

for z, m in to_upload:
    dataset_tag = get_dataset_tag(z)
    upload_tag = get_upload_tag(z)
    
    print(f"\n{'='*60}")
    print(f"Processing: {dataset_tag}")
    print(f"{'='*60}")
    
    # 1. evaluate
    cmd = f"python3 {manage_py} evaluate {z} {m}"
    print(f"Running: {cmd}")
    ret = os.system(cmd)
    if ret != 0:
        print(f"ERROR: evaluate failed for {dataset_tag}")
        continue
    
    # 2. makemigrations
    cmd = f"python3 {manage_py} makemigrations data_cdf --skip-checks"
    print(f"Running: {cmd}")
    ret = os.system(cmd)
    if ret != 0:
        print(f"ERROR: makemigrations failed for {dataset_tag}")
        continue
    
    # 3. migrate
    cmd = f"python3 {manage_py} migrate data_cdf --skip-checks"
    print(f"Running: {cmd}")
    ret = os.system(cmd)
    if ret != 0:
        print(f"ERROR: migrate failed for {dataset_tag}")
        continue
    
    # 4. save_data
    cmd = f"python3 {manage_py} save_data {upload_tag} {dataset_tag}"
    print(f"Running: {cmd}")
    ret = os.system(cmd)
    if ret != 0:
        print(f"ERROR: save_data failed for {dataset_tag}")
        continue
    
    print(f"SUCCESS: {dataset_tag} uploaded")

print("\nDone.") 