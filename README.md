# FurnitureConverter

This is a tool for use when converting Custom Furniture (CF) mods to either use Dynamic Game Assets (DGA) in the current 1.5.6 version of Stardew Valley, or Content Patcher (CP) in a future version of Stardew Valley. 

Right now, this is not finished, and may fail if the CF json is formatted in an unexpected way. Feedback is welcome via Github issues or the Stardew Valley Discord (please include the exact error encountered and ideally the json file as well via smapi.io/json).

## Basic Instructions on How to Use

* Install python 3 of some sort: https://www.python.org/downloads/
* Install the packages used, if needed
  * In a Terminal (Mac or Linux) window, type `pip install json5` and hit return. If you're in Windows, use Powershell and type ``py -m pip install json5`` instead.
  * Similarly, type `pip install pillow` (or `py -m pip install pillow`) and hit return
  * Similarly, type `pip install argparse` (or `py -m pip install argparse`) and hit return
  * The other packages used should be default python packages
* Download the python script from Github (Green "Code" button, then "Download as .zip" option, then unzip)
* Place the CF furniture mod to be converted into the same folder as the python script, and rename the folder to `original`
* Use `cd` to navigate into the folder with the python script and the json, or open a terminal window in that folder
  * On a Mac, see the detailed guide for three different ways to do this.
  * On Windows, open File Explorer to the folder you want, click on the address bar, type `powershell`, and hit return.
  * If you use Linux you should probably know how to use `cd` (or see Mac guide)
* Type `python furniture_converter.py --modName SOMENAMEHERE` but with `SOMENAMEHERE` swapped out for a descriptive string into terminal and hit return
  * Putting `--modName SOMENAMEHERE` in is required. Some examples: BeechFurniture, FlowerPrideBanners, SpringFurniture
  * Putting `--fileName ORIGONALJSONANME` is required if the json file in the CF pack is not named `content.json`. Do not put `.json` into this, just the filename.
  * Putting `--modAuthor MODAUTHORNAME` is optional, but recommended if there's anything weird in the author field
  * Putting `--sellAt SHOPNAME` is optional, and adds a json to the DGA mod that sells all the furniture at a specified store. The options for the store names are here: https://github.com/spacechase0/StardewValleyMods/blob/develop/DynamicGameAssets/docs/author-guide.md#valid-shop-ids-for-vanilla and putting in something that isn't there will either throw an error when the mod is loaded or just silently not work, I'm not sure which.
* It should create two new folders in the same folder as the script, one containing a DGA mod and one containing a CP mod. **The CP mod will not work until a future version of the game.** The two folders should be named something reasonable, and you should be able to use them as fully functional mods. 

## Detailed Tutorials on How to Use

Here's a detailed guide on how to use this script, with screenshots, for Mac users: https://github.com/elizabethcd/FurnitureConverter/blob/main/docs/Mac_guide.md#mac-detailed-pictorial-install-guide

Here's a detailed guide on how to use this script, with screenshots, for Windows users:
https://github.com/elizabethcd/FurnitureConverter/blob/main/docs/Windows_guide.md#windows-detailed-pictorial-install-guide

If you're a Linux user, the Mac guide should pretty much work. Otherwise, you're probably going to have to ask a Linux resource what's wrong.

## Simple Edits You Can Make Afterwards

* You may want to add in or edit the front textures of the furniture. 
  * As of right now that doesn't appear to be supported in CP, but conveniently in the DGA conversions there is a .png automatically created for front textures. You can then find the area corresponding to the view of the furniture in question on `dga_furniture_tilesheet.png`, and use an image editor to draw a front texture in the exact same area on `dga_front_tilesheet.png`. 
  * If the furniture already has a front texture, you may notice the shadow is doubled. You can fix this by removing the shadow areas from `dga_front_tilesheet.png`.
  * If the furniture has seats, the front texture will automatically be added by this script. (It's just sometimes a blank area of the .png.) If it doesn't, then you'll have to add a FrontTexture field to the configuration of the furniture in questions, which is a bit more advanced but is pretty easy: just copy the texture field, change the name to FrontTexture, and the png name from `dga_furniture_tilesheet.png` to `dga_front_tilesheet.png` (keep the colon and the number after the .png name). Check your commas afterwards!
* You may want to change where the furniture is sold.
  * You can do this by specifying a shop name, and then going into the DGA folder and finding `shopEntries.json` and editing the shop name in the entry corresponding to the furniture you want to be a different valid shop name. 
* You may want to change when the furniture is sold.
  * In this case you actually have to learn the DGA format, and use EnableConditions on the shop entries to selectively enable or disable the shop entries. 
* You may want to change whether the furniture is sold in the catalogue.
  * Again, you're going to have to learn the DGA format, but all you need to do is add the `ShowInCatalogue` property and set it to false.

## Planned Improvements

* Animated furniture converted automatically
* Error-checking on the shop names
* Only save front textures image if needed
* Add catalogue property for easier editing
* Estimated FrontTexture support for armchairs from the side

Could add if requested:
* Ability to handle multiple furniture jsons at once

Waiting on DGA update:
* Default sitting locations for couches, benches, and armchairs
* Display name overrides for furniture categories
