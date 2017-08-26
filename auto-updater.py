import requests
import os
import sys
import zipfile
import shutil

_AIR_FOLDER_NAME = 'Air for steam (Auto-updated)'


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)


def GetInstalledVersion(log_path):
    if os.path.isfile(log_path):
        with open(log_path, 'r', encoding='utf-8') as file:
            installed_version = file.read().strip()

    return installed_version


def GetLatestReleaseInfo():
    return requests.get('https://api.github.com/repos/outsetini/Air-for-Steam/releases/latest')


def DownloadRelease(release_info, skins_dir):
    release_zip = requests.get(release_info.json()['zipball_url'])

    TEMP_ZIP_FILEPATH = os.path.join(skins_dir, 'temp.zip')
    with open(TEMP_ZIP_FILEPATH, 'wb') as temp:
        temp.write(release_zip.content)

    #Extract and delete zip
    with zipfile.ZipFile(TEMP_ZIP_FILEPATH) as temp:
        skin = temp.infolist()[0]
        temp.extractall(skins_dir)
    os.remove(TEMP_ZIP_FILEPATH)

    LOCAL_RELEASE_PATH = os.path.join(skins_dir, _AIR_FOLDER_NAME)
    if os.path.exists(LOCAL_RELEASE_PATH):
        shutil.rmtree(LOCAL_RELEASE_PATH) #Remove old skin to force rename
    os.rename(os.path.join(skins_dir, skin.filename[:-1]), LOCAL_RELEASE_PATH)


def CopyConfig(skins_dir):
    SKIN_CONFIG_PATH = os.path.join(skins_dir, 'config.ini')
    CONFIG_PATH = os.path.join(skins_dir, 'config.txt')
    AIR_FOLDER_PATH = os.path.join(skins_dir, _AIR_FOLDER_NAME)

    # Copy config file
    if os.path.isfile(SKIN_CONFIG_PATH):
        shutil.copy2(SKIN_CONFIG_PATH, os.path.join(skins_dir, _AIR_FOLDER_NAME))
    else:
        print('No config file found (It should be named config.ini)')

    # Copy extras
    if os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as file:
            for line in file:
                if line.strip() == 'dark':
                    copytree(os.path.join(AIR_FOLDER_PATH, '+Extras', 'Themes', 'Dark'), AIR_FOLDER_PATH)
                    print('Dark theme applied')
                if line.strip() == 'square':
                    copytree(os.path.join(AIR_FOLDER_PATH, '+Extras', 'Square Avatars'), os.path.join(AIR_FOLDER_PATH, 'Graphics'))
                    print('Square avatars applied')
    else:
        print('No extras applied')


def UpdateLog(log_path, version):
    with open(log_path, 'w', encoding='utf-8') as file:
        file.write(version)


def main():
    STEAM_DIR = 'C:\Program Files (x86)\Steam'  # TODO: Find steam installation location
    SKINS_DIR = os.path.join(STEAM_DIR, 'skins')
    LOG_PATH = os.path.join(SKINS_DIR, 'auto-updater log.txt')

    installed_version = GetInstalledVersion(LOG_PATH)
    print(f'Local version:  {installed_version}')

    latest_release_info = GetLatestReleaseInfo()
    latest_release_version = latest_release_info.json()['tag_name']
    print(f'Latest release: {latest_release_version}')

    if installed_version == latest_release_version:
        print('Air for Steam is already up-to-date')
    else:
        print('Downloading update...')
        DownloadRelease(latest_release_info, SKINS_DIR)

        print('Applying configuration...')
        CopyConfig(SKINS_DIR)

        UpdateLog(LOG_PATH, latest_release_version)
        print('Updated successfully. Steam must be restarted for the changes to take effect.')


if __name__ == '__main__':
    main()
