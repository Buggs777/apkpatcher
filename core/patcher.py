import binascii
import os

def patch_library(work_dir, lib_subpath, offset, hex_data):
    full_path = os.path.join(work_dir, lib_subpath)
    print(f"Patching {full_path} at offset {hex(offset)}...")
    try:
        patch_bytes = binascii.unhexlify(hex_data)
        with open(full_path, 'r+b') as f:
            f.seek(offset)
            f.write(patch_bytes)
            print(f"Patched data  {hex_data}")
            
    except Exception as e:
        print(f"Error : {e}")
        exit(1)