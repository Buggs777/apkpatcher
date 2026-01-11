import binascii
import os
import re

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

def patch_smali(path, fonction):
    with open(path, 'r') as f:
        content = f.read()
        pattern = rf"\.method public final {fonction}\(\)Z.*?\.end method"
        replacement = (
            f".method public final {fonction}()Z\n"
            "    .locals 1\n"
            "    const/4 v0, 0x1\n"
            "    return v0\n"
            ".end method"
            )
        new_content = re.sub(pattern, replacement, content, flags=re.S)
        with open(path, 'w') as f:
            f.write(new_content)
            print("Function Patched")