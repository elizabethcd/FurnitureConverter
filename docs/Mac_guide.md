# Mac Detailed Pictorial Install Guide

If you are on a Mac, this guide has a lot of detailed instructions and screenshots that can be referenced when using this script. 

## Step 1: Install Python

You will want to go to the Python website and download Python:

<img width="600" alt="0_Download_Python_Mac" src="https://user-images.githubusercontent.com/55162529/174454724-c9bcc110-2e88-4814-a69d-4cc646afb3c2.png">

Once you have downloaded the Python installer, you will need to run it.

<img width="600" alt="1_Install_Python_Mac" src="https://user-images.githubusercontent.com/55162529/174454749-d9f9ab0d-fb42-482a-9ae9-bd7484b8c6f1.png">

When the installer finishes, you should get this message:

<img width="600" alt="2_Python_success_Mac" src="https://user-images.githubusercontent.com/55162529/174454766-5e8d3891-eee9-4f5a-9dbf-6b2336496d15.png">

## Step 2: Install Python packages

First, open Terminal. You can search for this application via Launchpad, or you can go into your Applications folder and into the Utilities folder there.

<img width="600" alt="3_Open_Terminal_Mac" src="https://user-images.githubusercontent.com/55162529/174454799-48cb9159-b62b-4f89-a467-14f29895c2db.png">

Once you have a Terminal window open, you're going to be using <code>pip</code> to install the python packages needed. Type ``pip install json5`` to start with, and then hit return, and it should look something like the following screenshot but without grey bars over personal info (in particular, it should end with "success" in some way). If this does not work, please take a screenshot of the result and ping me on Discord.

<img width="600" alt="4_pip_install" src="https://user-images.githubusercontent.com/55162529/174454853-54277e43-a499-4fce-8637-afd67cdf38af.png">

Repeat this process for ``pip install pillow`` and ``pip install argparse``. Once it's finished, you should have three success messages as shown in red.

<img width="600" alt="4_pip_success" src="https://user-images.githubusercontent.com/55162529/174455201-bb0ee137-4272-40bb-a5e9-ef886eb328e3.png">

## Step 3: Download the script code

You will want to download the script code directly from Github.

<img width="600" alt="5_Download_code_Mac" src="https://user-images.githubusercontent.com/55162529/174455001-298d8cca-c2d6-4798-8042-3e7e38b8d695.png">

Once it is downloaded, you will need to unzip the folder (unless your computer has already done this for you). On a Mac, this can be done with right click on the zip > pick `Open`.

<img width="600" alt="6_Unzip_code_Mac" src="https://user-images.githubusercontent.com/55162529/174455021-1c73da72-f127-4a41-ba44-32aef187f007.png">

## Step 4: Place mod inside the script folder

For whatever mod you're interested in converting, start by moving it to the script folder.

<img width="600" alt="7_Place_mod_Mac" src="https://user-images.githubusercontent.com/55162529/174455258-a9277b76-c852-488c-bb17-09654243992b.png">

After that, rename the folder name to `original`. 

<img width="600" alt="8_Rename_mod_Mac" src="https://user-images.githubusercontent.com/55162529/174455269-765be9b1-1cac-48b2-9c8b-8f248516d75e.png">

## Step 5: Open a Terminal Window in the script folder

There are a few different ways to do this. If you're familiar with the ``cd`` command to move to a specified folder, you can use that, as in the following screenshot.

<img width="600" alt="9_cd_Mac" src="https://user-images.githubusercontent.com/55162529/174455283-7a5d7265-0c22-4a37-b463-c7a886c60e8b.png">

If you prefer a drag and drop method, you can drag the script folder onto the Terminal icon in the dock.

<img width="600" alt="9_Drag_to_Terminal_Mac" src="https://user-images.githubusercontent.com/55162529/174455290-5d1d3b91-61e4-48eb-a02a-f5184f4d7b2d.png">

Finally, you can alternatively right click on the folder and select ``Open in Terminal`` if that's an option on your version of MacOS. It may look slightly different than the screenshot.

<img width="600" alt="9_Terminal_From_Finder_Mac" src="https://user-images.githubusercontent.com/55162529/174455312-3067df4c-408d-4e71-b575-b5ba70905920.png">

## Step 6: Run the script

Once you have a terminal window open and the script folder is the active folder, you can then run the script. 

Type `python furniture_converter.py --modName SOMENAMEHERE` but with `SOMENAMEHERE` swapped out for a descriptive string into terminal and hit return
  * Putting `--modName SOMENAMEHERE` in is required. 
  * Putting `--modAuthor MODAUTHORNAME` is optional, but recommended if there's anything weird in the author field
  * Putting `--sellAt SHOPNAME` is optional, and adds a json to the DGA mod that sells all the furniture at a specified store. The options for the store names are here: https://github.com/spacechase0/StardewValleyMods/blob/develop/DynamicGameAssets/docs/author-guide.md#valid-shop-ids-for-vanilla and putting in something that isn't there will either throw an error when the mod is loaded or just silently not work, I'm not sure which.

Here's an example of what running the script looks like (with success being shown by the lack of error message). If you get an error message, please take a screenshot and ping me on Discord with a link to the furniture pack you are converting.

<img width="600" alt="10_Run_script" src="https://user-images.githubusercontent.com/55162529/174455398-7bacc19d-5428-4bf9-9c5a-9126e20e74c2.png">

## Step 7: Use the mod

You can find the converted mod inside the script folder, and you can move it to your Mods folder just like any other mod. 

<img width="600" alt="11_Success" src="https://user-images.githubusercontent.com/55162529/174455412-9e46d59f-dce6-47a2-931c-a24fea09f31f.png">
