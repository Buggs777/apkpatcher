import os
import argparse
import sys
import shutil
from core import unpack, repack, sign_apk, find_pattern, patch_library, get_libs, find_lib_path_by_name

DEFAULT_OUTPUT = "apk_patch.apk"
TEMP_DIR = "apkpatcher_workingdir"

def main():
    parser = argparse.ArgumentParser(description="APK Patcher")
    parser.add_argument("-i", "--input", required=True, help="Input APK file")
    parser.add_argument("-o", "--output", default="apk_patched.apk", help="Output APK file")
    parser.add_argument("-f", "--find", required=True, help="Hex pattern to find (ex: '00F020E3')")
    parser.add_argument("-p", "--patch", required=True, help="Hex replacement (ex: '01F020E3')")
    parser.add_argument("--dump", help="Path to your decrypted .so file (from dumper)")
    parser.add_argument("-l", "--lib", help="Target lib name (optional if --dump is used)")
    args = parser.parse_args()

    unpack(args.input, TEMP_DIR)
    target_internal_path = None

    if args.dump:
        if not os.path.isfile(args.dump):
            sys.exit(f"Error: Dump file not found at {args.dump}")
        dump_filename = os.path.basename(args.dump)
        matches = find_lib_path_by_name(TEMP_DIR, dump_filename)

        if len(matches) == 0:
            sys.exit(f"Error: Could not find '{dump_filename}' anywhere inside the APK.")
        else:
            target_internal_path = matches[0]
            print(f"Found match: {target_internal_path}")

        full_dest_path = os.path.join(TEMP_DIR, target_internal_path)
        print(f"Injecting dumped lib...")
        try:
            shutil.copy2(args.dump, full_dest_path)
            print(f"Injection successful.")
        except Exception as e:
            sys.exit(f"Injection failed: {e}")

    else:
        target_internal_path = get_libs(TEMP_DIR, args.lib)
    try:
        full_lib_path = os.path.join(TEMP_DIR, target_internal_path)
        offsets = find_pattern(full_lib_path, args.find)
        patch_library(TEMP_DIR, target_internal_path, offsets, args.patch)

    except ValueError as e:
        print(f"Patching Logic Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Critical Error: {e}")
        sys.exit(1)

    repack(TEMP_DIR, args.output)
    sign_apk(args.output)
    
    print(f"\nSuccess, patched APK: {args.output}")

if __name__ == "__main__":
    main()
