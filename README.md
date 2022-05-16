# FurnitureConverter

This is a tool for use when converting Custom Furniture (CF) mods to either use Dynamic Game Assets (DGA) in the current 1.5.6 version of Stardew Valley, or Content Patcher (CP) in a future version of Stardew Valley. 

Right now, this is not finished, and may fail on some furniture types. It also does not add in anything beyond the basic furniture definition. 

## How to Use

* Install python 3 of some sort
* Install the packages used, if needed
  * In a terminal window, type `pip install json5` and hit return 
  * Similarly, type `pip install pillow` and hit return
  * Similarly, type `pip install argparse` and hit return
  * The other packages used should be default python packages, I believe
* Download the python script from Github (Green "Code" button, then "Download as .zip" option, then unzip)
* Place the CF furniture mod to be converted into the same folder as the python script, and rename the folder to `original`
* Use `cd` to navigate into the folder with the python script and the json, or open a terminal window in that folder
  * On a Mac, right click on the folder name and pick "New Terminal at Folder"
  * On Windows, hold shift, right click in the folder background, and pick one of "Open in Command Prompt", "Open in PowerShell", or "Open in Windows Terminal" (depending on your system settings).
  * Not sure what Linux does, but if you use Linux you probably know how to use `cd`
* Type `python furniture_converter.py --modName SOMENAMEHERE` but with `SOMENAMEHERE` swapped out for a descriptive string into terminal and hit return
  * Putting `--modName SOMENAMEHERE` in is required. Some examples: BeechFurniture, FlowerPrideBanners, SpringFurniture
  * Putting `--fileName ORIGONALJSONANME` is required if the json file in the CF pack is not named `content.json`. Do not put `.json` into this, just the filename.
  * Putting `--modAuthor MODAUTHORNAME` is optional, but recommended if there's anything weird in the author field
* It should create two new folders in the same folder as the script, one containing a DGA mod and one containing a CP mod. The two folders should be named something reasonable, and you should be able to use them as fully functional mods. 

## Planned Improvements

* Better error-checking/handling of furniture types
* FrontTexture support for chairs
* Default sitting locations for chairs
* Display name overrides for furniture categories
* NightTexture support for lamps and windows
