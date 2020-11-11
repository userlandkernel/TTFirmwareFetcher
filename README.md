# TTFirmwareFetcher
A download client for TomTom firmware using python3 and various sources

## Depends
- python3
- bs4 (from python's pip3)
- cabextract
- requests

## How to use
1. Clone this repository
2. Run pip3 install -r cabs/requirements.txt
3. Run python3 cabs/download.py and wait for the firmware to be downloaded
4. Run ./extract.sh and wait for the firmware to be extracted
5. You'll find the extracted firmware in the firmware directory, use `cd firmware`
6. That's it!

* In case you face "permission issues" do not forget to make the extract script executable with chmod +x cabs/extract.sh

## Remarks
- This script is written very lazily, pull requests are welcome
