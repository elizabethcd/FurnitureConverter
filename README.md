# FurnitureConverter

This is a tool for use when converting Custom Furniture (CF) mods to either use Dynamic Game Assets (DGA) in the current 1.5.6 version of Stardew Valley, or Content Patcher (CP) in a future version of Stardew Valley. 

Right now, this is not finished, and may fail if the CF json is formatted in an unexpected way. Feedback is welcome via Github issues or the Stardew Valley Discord (please include the exact error encountered and ideally the json file as well via smapi.io/json).

## How to Use

* Install python 3 of some sort: https://www.python.org/downloads/
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
  * Putting `--sellAt SHOPNAME` is optional, and adds a json to the DGA mod that sells all the furniture at a specified store. The options for the store names are here: https://github.com/spacechase0/StardewValleyMods/blob/develop/DynamicGameAssets/docs/author-guide.md#valid-shop-ids-for-vanilla and putting in something that isn't there will either throw an error when the mod is loaded or just silently not work, I'm not sure which.
* It should create two new folders in the same folder as the script, one containing a DGA mod and one containing a CP mod. **The CP mod will not work until a future version of the game.** The two folders should be named something reasonable, and you should be able to use them as fully functional mods. 

## Planned Improvements

* Error-checking on the shop names
* Ability to handle multiple furniture jsons at once
* Estimated FrontTexture support for armchairs from the side
* Default sitting locations for couches, benches, and armchairs
* Display name overrides for furniture categories (requires DGA to update first though)
