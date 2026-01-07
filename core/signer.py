import os
from utils.common import cmd

KEYSTORE_PATH = "debug.keystore"       
KEYSTORE_PASS = "android"              
ALIAS_NAME = "androiddebugkey"  

def sign_apk(apk_path):
    if not os.path.exists(KEYSTORE_PATH):
        print("Generating a keystore...")
        cmd(f'keytool -genkey -v -keystore {KEYSTORE_PATH} -storepass {KEYSTORE_PASS} -alias {ALIAS_NAME} -keypass {KEYSTORE_PASS} -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=Android Debug,O=Android,C=US"')

    print(f"Signing the APK...")
    cmd(f"jarsigner -sigalg SHA1withRSA -digestalg SHA1 -keystore {KEYSTORE_PATH} -storepass {KEYSTORE_PASS} {apk_path} {ALIAS_NAME}")
