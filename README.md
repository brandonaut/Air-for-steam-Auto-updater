# Air-for-Steam Updater

Air-for-Steam Updater makes it easier to download and install the latest Air-for-Steam skin, without losing your configuration settings.

NOTE: This has only been tested on Windows 10, but it should work for OSX and Linux as well.

## Usage:
Run `air-updater` without any arguments. It will try to determine the path to your Steam installation. If it can't find it, it will prompt you for the root of your Steam directory (Usually 'C:\Program Files (x86)\Steam' on Windows). air-updater will save this in air-updater.ini, so you should only have to set it the first time you run it.

## Config:
Place your Air-for-Steam configuration file ('config.ini') in the root of your Steam skins folder. air-updater will copy this into the new Air-for-Steam version after each update.

air-updater also has its own configuration file, air-updater.ini (created after the first run in the same folder as air-updater). You can set the following settings in air-updater.ini:
  - Dark mode: Set to 'True' to enable dark mode after performing the update
  - Square avatars: Set to 'True' to enable square avatars after performing the update

## To build
  - Python 3.5
  - Dependencies: requests, pyinstaller

##License
The license is the CC 3.0 NZ attribution-noncomercial license. A human readable version is available here: https://creativecommons.org/licenses/by-nc/3.0/nz/.
