import configparser
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


def UpdateSkinConfig(skins_dir, air_updater_config):
    SKIN_CONFIG_PATH = os.path.join(skins_dir, 'config.ini')
    AIR_FOLDER_PATH = os.path.join(skins_dir, _AIR_FOLDER_NAME)

    # Copy config file
    if os.path.isfile(SKIN_CONFIG_PATH):
        shutil.copy2(SKIN_CONFIG_PATH, os.path.join(skins_dir, _AIR_FOLDER_NAME))
    else:
        print('No config file found (It should be named config.ini)')

    # Copy extras
    if air_updater_config['User Settings']['Dark mode'] == 'True':
        copytree(os.path.join(AIR_FOLDER_PATH, '+Extras', 'Themes', 'Dark'), AIR_FOLDER_PATH)
        print('Dark theme applied')
    if air_updater_config['User Settings']['Square avatars'] == 'True':
        copytree(os.path.join(AIR_FOLDER_PATH, '+Extras', 'Square Avatars'), os.path.join(AIR_FOLDER_PATH, 'Graphics'))
        print('Square avatars applied')


def GetSteamDir():
    steam_dir = None
    if os.name == 'nt':
        if os.path.isdir('''C:\Program Files (x86)\Steam'''):
            steam_dir = '''C:\Program Files (x86)\Steam'''

    if steam_dir:
        print('Found Steam at {}'.format(steam_dir))
    else:
        print('Could not detect Steam installation automatically.')
        while not steam_dir:
            response = input('Please enter your Steam installation directory or (A)bort: ')
            if response.lower() == 'a':
                sys.exit(0)
            else:
                if os.path.isdir(response):
                    steam_dir = response
                else:
                    print('Invalid location')

    return steam_dir


def main():
    # The air-updater.ini should reside in the same location as air-updater.py
    AIR_UPDATER_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    AIR_CONFIG_PATH = os.path.join(AIR_UPDATER_PATH, 'air-updater.ini')
    air_updater_config = configparser.ConfigParser()

    if os.path.isfile(AIR_CONFIG_PATH):
        air_updater_config.read(AIR_CONFIG_PATH)
    else:
        air_updater_config['Global'] = {'Air-for-Steam version installed': 'unknown'}
        air_updater_config['User Settings'] = {
            'Steam path': GetSteamDir(),
            'Dark mode': 'False',
            'Square avatars': 'False',
            }

    SKINS_DIR = os.path.join(air_updater_config['User Settings']['Steam path'], 'skins')

    installed_version = air_updater_config['Global']['Air-for-Steam version installed']
    print('Local version:  {}'.format(installed_version))

    latest_release_info = GetLatestReleaseInfo()
    latest_release_version = latest_release_info.json()['tag_name']
    print('Latest release: {}'.format(latest_release_version))

    if installed_version == latest_release_version:
        print('Air for Steam is already up-to-date')
    else:
        print('Downloading update...')
        DownloadRelease(latest_release_info, SKINS_DIR)

        print('Applying configuration...')
        UpdateSkinConfig(SKINS_DIR, air_updater_config)

        air_updater_config['Global']['Air-for-Steam version installed'] = latest_release_version

        with open(AIR_CONFIG_PATH, 'w', encoding='utf-8') as file:
            air_updater_config.write(file)

        print('Updated successfully. Steam must be restarted for the changes to take effect.')

    input('Press any key to continue...')


if __name__ == '__main__':
    main()
