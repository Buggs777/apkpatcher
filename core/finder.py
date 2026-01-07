import binascii
import sys
import os

def find_pattern(file_path, hex_pattern):
    try:
        pattern_bytes = binascii.unhexlify(hex_pattern.replace(" ", ""))
    except binascii.Error:
        raise ValueError("Le format du pattern Hexa est invalide.")
    found_offset = []

    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            
            start = 0
            while True:
                offset = data.find(pattern_bytes, start)
                if offset == -1:
                    break
                found_offset.append(offset)
                start = offset + 1
                
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")

    if len(found_offset) == 0:
        raise ValueError("Pattern not found in the apk")

    if len(found_offset) > 1:
        raise ValueError(f"Pattern found {len(found_offset)} times in the apk, please add more bytes to it to get a more precise search")

    return found_offset

def get_libs(work_dir, filter_name=None):
    libs = []
    for root, _, files in os.walk(os.path.join(work_dir, "lib")):
        for file in files:
            if file.endswith(".so"):
                libs.append(os.path.relpath(os.path.join(root, file), work_dir))

    if not libs:
        sys.exit("No libraries found.")

    if filter_name:
        for lib in libs:
            if filter_name in lib: return lib
        sys.exit(f"Library containing '{filter_name}' not found.")

    print("\nAvailable libraries:")
    for i, lib in enumerate(libs):
        print(f"[{i}] {lib}")
    try:
        choice = int(input("Select library ID: "))
        return libs[choice]
    except:
        sys.exit("Invalid selection.")


def find_lib_path_by_name(base_dir, filename):
    matches = []
    for root, _, files in os.walk(base_dir):
        if filename in files:
            full_path = os.path.join(root, filename)
            matches.append(os.path.relpath(full_path, base_dir))
    return matches