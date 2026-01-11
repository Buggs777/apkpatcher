import os
import argparse
import shutil
from core import generate_key, unpack, repack, patch_smali
from utils.common import cmd

TEMP_DIR = "workingdir"
KEYSTORE_PATH = "debug.keystore"       
KEYSTORE_PASS = "android"              
ALIAS_NAME = "androiddebugkey" 
FINAL_APK_NAME = "patched_final.apk"

def main():
    parser = argparse.ArgumentParser(description="Smali APK Patcher")
    parser.add_argument("-i", "--input", required=True, help="Input APK file")
    parser.add_argument("-p", "--path-smali-patch", required=True, help="Relative path to the smali file inside unpacked dir")
    parser.add_argument("-f", "--function-to-patch", required=True, help="Name of the function to patch")
    args = parser.parse_args()

    apk_input_path = os.path.abspath(args.input)
    
    if not os.path.exists(KEYSTORE_PATH):
        print(f"Generating a keystore, keypass : {KEYSTORE_PASS}...")
        generate_key()

    unpack(apk_input_path, TEMP_DIR)

    full_smali_path = os.path.join(TEMP_DIR, args.path_smali_patch)
    
    if os.path.exists(full_smali_path):
        print(f"Patching {args.function_to_patch} in {full_smali_path}")
        patch_smali(full_smali_path, args.function_to_patch)
    else:
        print(f"Error: Smali file not found at {full_smali_path}")
        exit(1)

    while True:
        answ = input("Patch another function in the same file? (y/n): ")
        if answ.lower() == "y":
            func_name = input("Function name: ")
            patch_smali(full_smali_path, func_name)
        else:
            break

    print("Restoring META-INF services...")
    try:
        cmd(f"unzip -o {apk_input_path} \"META-INF/services/*\" -d {TEMP_DIR}")
    except Exception as e:
        print("No META-INF/services found or unzip failed (ignoring).")

    repack(TEMP_DIR, 'repacked.apk')
    cmd("mkdir aligned")
    
    aligned_apk = os.path.join("aligned", os.path.basename(apk_input_path))
    
    cmd(f"zip -d repacked.apk \"META-INF/*.RSA\" \"META-INF/*.SF\" \"META-INF/MANIFEST.MF\" 2>/dev/null || true")
    cmd(f"zipalign -p -f 4 repacked.apk {aligned_apk}")
    
    temp_signed = "signed_temp.apk"
    cmd(f"apksigner sign --ks {KEYSTORE_PATH} --ks-pass pass:{KEYSTORE_PASS} --out {temp_signed} {aligned_apk}")
    shutil.move(temp_signed, apk_input_path)
    cmd("rm -f repacked.apk")
    cmd("rm -rf aligned")
    cmd(f'rm -rf {TEMP_DIR}')
    print(f"{apk_input_path} has been patched.")

if __name__ == "__main__":
    main()