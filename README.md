# Auto APK Patcher

A lightweight automation tool to unpack, hex-patch, repack, and sign Android APKs in a single command.

## Prerequisites

You **must** have the following tools installed and added to your system **PATH**:

1.  **Python 3.x**
    
2.  **Java JDK** (Required for `jarsigner` and `keytool`)
    
3.  **Apktool** (Required for `apktool d` and `apktool b`)
    

> **Check:** Run `apktool -version` and `java -version` in your terminal to verify.
---


## Usage
```
python main.py -i <APK_FILE> -f <FIND_HEX> -p <REPLACE_HEX> [options]
```
### Arguments

| Flag            | Description           | Required | Example      |
| :-------------- | :-------------------- | :------- | :----------- |
| `-i`, `--input` | Path to input APK     | Yes   | `game.apk`   |
| `-o`, `--output`| Output filename       | No    | `patched.apk`|
| `-f`, `--find`  | Hex pattern to find (where you want to patch) | Yes   | `00F020E3`   |
| `-p`, `--patch` | Hex code replacement (your patched instructions) | Yes   | `01F020E3`   |
| `--dump`        |	Path to external decrypted .so file | No | `/libil2cpp.so`|
| `-l`, `--lib`   | Specific lib name (when your lib are not encrypted)   | No    | `libil2cpp`  |



### Examples

**1. Standard Usage (Static Patching)** Use this for non-protected games where the library is not encrypted.

```
python apkpatcher.py -i game.apk -f "20008052" -p "1F2003D5" -l libil2cpp

```

**2. Injection Mode (For Protected/Encrypted APKs)** Use this when you have a decrypted file (from Il2CppDumper or another tool) that needs to replace the encrypted original file inside the APK. The script automatically detects where the file belongs in the APK structure.

```
python apkpatcher.py -i protected_game.apk --dump ./dumps/libil2cpp.so -f "20008052" -p "1F2003D5"

```

_Note: In this mode, the script finds the matching filename inside the APK, replaces it with your dump, applies the patch, and repacks everything._

_For educational purposes only._
