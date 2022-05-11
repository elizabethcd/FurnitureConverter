# FurnitureConverter

This is a tool for use when converting Custom Furniture (CF) mods to either use Dynamic Game Assets (DGA) in the current 1.5.6 version of Stardew Valley, or Content Patcher (CP) in a future version of Stardew Valley. 

Right now, this is not finished, and may fail on some furniture types. It also does not add in anything beyond the basic furniture definition. 

## How to Use

* Install python of some sort
* Install the packages used, if needed
  * In a terminal window, type `pip install json5` and hit return 
  * Similarly, type `pip install pillow` and hit return
  * The other packages used should be default python packages, I believe
* Place your CF furniture json, renamed to `original_furniture.json`, into the same folder as the python script
* Use `cd` to navigate into the folder with the python script and the json, or open a terminal window in that folder
* Type `python furniture_converter.py` into terminal and hit return
* It should spit out four json files you can rename and use in either DGA or CP mods. See the documentation for both frameworks for more details. The `default_cp.json` and `default_dga.json` are for use in i18n translations. You will need to rename them. It will also spit out one tilesheet, `dga_furniture_tilesheet.png`, which has the furnitures rearranged to fit the DGA conventions.

## Planned Improvements

* Better error-checking/handling of furniture types
* FrontTexture support for chairs
* Default sitting locations for chairs
* Display name overrides for furniture categories
* NightTexture support for lamps and windows
