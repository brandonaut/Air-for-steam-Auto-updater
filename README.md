# Air-for-Steam Updater

Air-for-Steam Updater makes it easier to download and install the latest Air-for-Steam skin, without losing your configuration settings.

NOTE: This has only been tested on Windows 10, but it should work for OSX and Linux as well.

## Usage:
Place your Air-for-Steam configuration file ('config.ini') in the root of your Steam skins folder. air-updater will copy this into the new Air-for-Steam version after each update.

Configure your settings in air-updater.ini and then run `air-updater.exe`.

### Settings

air-updater also has its own configuration file, air-updater.ini (in the same folder as air-updater), which contains the following settings:
  - Steam path: This is the path to your Steam installation (usually 'C:\Program Files (x86)\Steam' on Windows)
  - Dark mode: Set to 'True' to enable dark mode after performing each update
  - Square avatars: Set to 'True' to enable square avatars after performing each update

## To build
  - Python 3.5
  - Dependencies: requests, pyinstaller

## License
The license is the CC 3.0 NZ attribution-noncomercial license. A human readable version is available here: https://creativecommons.org/licenses/by-nc/3.0/nz/.
