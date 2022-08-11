# Windows Detailed Pictorial Install Guide

If you are on a Windows computer, this guide has a lot of detailed instructions and screenshots that can be referenced when using this script. 

## Step 1: Install Python

You will want to go to the Python website and download Python:

<img width="600" alt="0_Download_Python_Windows" src="https://user-images.githubusercontent.com/55162529/174458009-9604c715-22d5-458f-bbcd-61986bde385b.PNG">

Once you have downloaded the Python installer, you will need to run it.

<img width="600" alt="1_Install_Python_Windows" src="https://user-images.githubusercontent.com/55162529/174458021-38aae87f-256b-41f9-ad02-2cea822e2bb7.png">

When the installer finishes, you should get this message:

<img width="600" alt="2_Python_success_Windows" src="https://user-images.githubusercontent.com/55162529/174458028-7db5bacb-d1f2-4533-a4da-7e58f37c52fb.png">

## Step 2: Install Python packages

There are a few packages you're going to need, which can be installed in a couple different ways. I will describe two ways here, one using Windows Powershell and the other using MiniConda.

### Step 2: Powershell version

If you want to do this via Powershell, start by opening Windows Powershell. Then type in ``py -m pip install json5`` and hit enter. It should look something like the screenshot below. Once that succeeds, next do ``py -m pip install pillow`` and ``py -m pip install argparse`` in the same way. If you are not getting something like the screenshot below, and in particular if you aren't getting success messages after each install, try the MiniConda method. 

<img width="600" alt="5_pip_install_success" src="https://user-images.githubusercontent.com/55162529/174458179-a7c69957-d6e3-4ca0-a053-5cad86d3cdb1.png">

### Step 2: MiniConda version

If you want to do this via MiniConda, start by installing Miniconda. Go to the website here: https://docs.conda.io/en/latest/miniconda.html and scroll down to the Windows installer section. By default, pick the topmost installer.

<img width="600" alt="3_Miniconda_installers" src="https://user-images.githubusercontent.com/55162529/174458210-ef55c046-e28c-4837-99e5-f0c79cd9ab4f.png">

Once you have the installer downloaded, you will need to run it.

<img width="600" alt="4_Install_Conda" src="https://user-images.githubusercontent.com/55162529/174458219-818efd11-89c8-48ad-a482-13d7face9796.png">

Go through the installation, and when it finishes it should show something like this.

<img width="600" alt="4_Success_Conda_install" src="https://user-images.githubusercontent.com/55162529/174458232-008782fb-3433-4c83-8554-d16f6e75e344.png">

After that, you can now open the Anaconda Prompt app, which will give you better access to Python commands than cmd or Powershell.

<img width="300" alt="5_Open_conda_prompt" src="https://user-images.githubusercontent.com/55162529/174458240-5bb8d5d9-0a96-4c5e-9ba3-b3a722165a2b.png">

Type in ``pip install json5`` and hit enter. It should look something like the screenshot below. Once that succeeds, next do ``pip install pillow`` and ``pip install argparse`` in the same way. If you are not getting something like the screenshot below, and in particular if you aren't getting success messages after each install, take a screenshot and ping me on Discord. 

<img width="600" alt="5_pip_install_Conda" src="https://user-images.githubusercontent.com/55162529/174458303-3cd76b25-5be0-46f2-ab83-0884465c80d2.png">

## Step 3: Download the script code

You will want to download the script code directly from Github.

<img width="600" alt="5_Download_code_Mac" src="https://user-images.githubusercontent.com/55162529/174455001-298d8cca-c2d6-4798-8042-3e7e38b8d695.png">

Once it is downloaded, you will need to unzip the folder. To do this, right click on the zip and pick `Extract All`. You may need to move around the folders if this creates some kind of nested folder or extracts somewhere strange.

<img width="600" alt="6_Unzip_code_Windows" src="https://user-images.githubusercontent.com/55162529/174458434-e12990ef-54d9-43b1-aa6c-6fa434f8f8f2.png">

## Step 4: Place mod inside the script folder

For whatever mod you're interested in converting, start by moving it to the script folder, and then rename it to `original`.

<img width="600" alt="8_Rename_mod_Windows" src="https://user-images.githubusercontent.com/55162529/174458455-e44bf55a-8fa5-44d6-b166-5f05ef1b4dc7.png">

It should look like this afterwards.

<img width="600" alt="8_Rename_success_Windows" src="https://user-images.githubusercontent.com/55162529/174458475-f4d3e0f9-719b-4cc1-9cf7-4d17cf8f155f.png">

## Step 5: Open a Terminal Window in the script folder

There are a few different ways to do this. I will again divide these into Powershell and MiniConda techniques.

## Step 5: Powershell version

While in File Explorer, navigate to the folder with the script in it. Next, go to the address bar, type in ``powershell`` and hit enter. This will open a Powershell window located in the folder.

<img width="600" alt="9_Open_Powershell" src="https://user-images.githubusercontent.com/55162529/174458527-6e6cc08d-d980-4dd0-8bb6-107e5dd4111b.png">

## Step 5: MiniConda version

While in the Anaconda Prompt app (which you should already have opened earlier), you will need to use the `cd` command to naviagte to the folder. Ideally, it will be located somewhere nice, like in the Downloads folder. If that is the case, all you need to type is ``cd Downloads/FurnitureConverter-main`` and then hit return, as in the following screenshot. If your folder is somewhere more creative, you will need to type in the address of the folder. 

<img width="600" alt="9_Open_Conda" src="https://user-images.githubusercontent.com/55162529/174458585-79281086-4e10-4b52-a672-8a5899d221c8.png">

## Step 6: Run the script

Once you have a Powershell or Anaconda Prompt window open and the script folder is the active folder, you can then run the script. 

Type `python furniture_converter.py --modName SOMENAMEHERE` but with `SOMENAMEHERE` swapped out for a descriptive string into terminal and hit return
  * Putting `--modName SOMENAMEHERE` in is required. 
  * Putting `--modAuthor MODAUTHORNAME` is optional, but recommended if there's anything weird in the author field
  * Putting `--sellAt SHOPNAME` is optional, and adds a json to the DGA mod that sells all the furniture at a specified store. The options for the store names are here: https://github.com/spacechase0/StardewValleyMods/blob/develop/DynamicGameAssets/docs/author-guide.md#valid-shop-ids-for-vanilla and putting in something that isn't there will either throw an error when the mod is loaded or just silently not work, I'm not sure which.

Below are examples of what running the script looks like (with success being shown by the lack of error message). If you get an error message, please take a screenshot and ping me on Discord with a link to the furniture pack you are converting.

Powershell example:

<img width="600" alt="10_Powershell_run_success" src="https://user-images.githubusercontent.com/55162529/174458591-b69fbbfd-0135-4482-a5b1-f80f1de5bd5c.png">

Anaconda Prompt example:

<img width="600" alt="10_Conda_run_success" src="https://user-images.githubusercontent.com/55162529/174458626-103f770f-1923-4a34-bb17-b0df5dc79cba.png">

## Step 7: Use the mod

You can find the converted mod inside the script folder, and you can move it to your Mods folder just like any other mod. 

<img width="600" alt="11_Finished" src="https://user-images.githubusercontent.com/55162529/174458637-6f9ab84c-2c25-47e9-8dec-b4decdc13ff0.png">
