import os
import shutil
from utils.common import cmd

def unpack(apk_file, output_dir):
    print(f"Unpacking {apk_file}...")
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    cmd(f"apktool d -f -o {output_dir} {apk_file}")

def repack(work_dir, output_apk):
    print(f"Repacking {work_dir} to {output_apk}...")

    if os.path.exists(output_apk):
        os.remove(output_apk)

    cmd(f"apktool b -o {output_apk} {work_dir}")