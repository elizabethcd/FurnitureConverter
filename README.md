# FurnitureConverter

This is a tool for use when converting Custom Furniture (CF) mods to either use Dynamic Game Assets (DGA) in the current 1.5.6 version of Stardew Valley, or Content Patcher (CP) in a future version of Stardew Valley. 

Right now, this is not finished, and will not always produce valid image indexes and/or may fail on some furniture types.

## How to Use

* Install python of some sort
* Install the packages used, if needed
  * In a terminal window, type `pip install json5` and hit return (the other packages used should be default python packages, I believe)
* Place your CF furniture json, renamed to `original_furniture.json`, into the same folder as the python script
* Use `cd` to navigate into the folder with the python script and the json, or open a terminal window in that folder
* Type `python furniture_converter.py` into terminal and hit return
* It should spit out four json files you can rename and use in either DGA or CP mods. See the documentation for both frameworks for more details.
