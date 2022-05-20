import json
import json5
import re
import math
import argparse
from PIL import Image
from pathlib import Path

#### Important inputs
filename = "content.json"
originalLocation = "original"
tilesheetLocation = "Mods"

# Create the parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--modName', type=str, required=True, help="Name of the mod (no spaces), should be identifying")
parser.add_argument('--modAuthor', type=str, required=False, help="Author of the original mod (no spaces)")
parser.add_argument('--fileName', type=str, required=False, help="Name of the json file where the original mod declared the furniture (no spaces)")
# Parse the argument
args = parser.parse_args()

modName = args.modName
filename = filename if args.fileName is None else args.fileName + ".json"

#### Define some useful constants
furnitureTypesConversion = {
	"table": "Table",
	"long table": "Table",
	"stool": "Decoration", # May need to add in a special check to see if the name contains "stool"
	"chair": "Decoration",
	"bench": "Decoration",
	"couch": "Decoration",
	"armchair": "Decoration",
	"dresser": "Dresser",
	"painting": "Painting",
	"lamp": "Lamp",
	"rug": "Rug",
	"window": "Window",
	"bookcase": "Decoration",
	"decor": "Decoration",
	"other": "Decoration"
}

dgaFurnitureTypes = ["Bed", "Decoration", "Dresser", "Fireplace", "FishTank", "Lamp", "Painting", "Rug",
	"Table", "Sconce", "TV", "Window"]

dgaSitDirections = ["Down","Right","Up","Left"]

dgaTilesheetName = "dga_furniture_tilesheet.png"
frontTilesheetName = "dga_front_tilesheet.png"

# TODO: Define default chair sitting properties
# TODO: Handle FrontTexture for chairs
# TODO: Handle NightTexture for windows, lamps

#### Load up the furniture json!
folderPath = Path(originalLocation)

# Read the furniture json in as text
file_contents = folderPath.joinpath(filename).read_text()

# Some third-party JSON files begin with extraneous characters - try to fix them up.
unused_chars, opening_bracket, rest_of_file = file_contents.partition("{")
file_contents = opening_bracket + rest_of_file  # Discard the extra characters.

try:
    # Try using the standard module first because it's fast and handles most cases.
	data = json.loads(file_contents)
except json.decoder.JSONDecodeError:
    # The json5 module is much slower, but is more lenient about formatting issues.
	data = json5.loads(file_contents)

# Read the manifest json in as text
file_contents = folderPath.joinpath("manifest.json").read_text()

# Some third-party JSON files begin with extraneous characters - try to fix them up.
unused_chars, opening_bracket, rest_of_file = file_contents.partition("{")
file_contents = opening_bracket + rest_of_file  # Discard the extra characters.
try:
    # Try using the standard module first because it's fast and handles most cases.
	manifest = json.loads(file_contents)
except json.decoder.JSONDecodeError:
    # The json5 module is much slower, but is more lenient about formatting issues.
	manifest = json5.loads(file_contents)

modAuthor = args.modAuthor if args.modAuthor is not None else manifest["Author"]
uniqueString = modAuthor + "." + modName

#### Time to process!
furniture_data = data["furniture"]
cp_data = {}
dga_data = []
cp_default = {}
dga_default = {}
allTextures = set()
imageDict = {}
imageLocationDict = {}
imageWidthDict = {}
imageHeightDict = {}
for item in furniture_data:
	#### Set up basic information
	itemID = re.sub("[^a-zA-Z]+", "", item["name"]) + str(item["id"])
	itemTexture = item["texture"]
	numRotations = item["rotations"] if "rotations" in item else 1
	itemWidth = item["width"]
	itemHeight = item["height"]
	rotatedWidth = item["rotatedWidth"] if "rotatedWidth" in item else item["height"]
	rotatedHeight = item["rotatedHeight"] if "rotatedHeight" in item else item["width"]
	boxWidth = item["boxWidth"] if "boxWidth" in item else itemWidth
	boxHeight = item["boxHeight"] if "boxHeight" in item else itemHeight
	rotatedBoxHeight = item["rotatedBoxHeight"] if "rotatedBoxHeight" in item else rotatedHeight

	#### Save textures for later
	allTextures.add(itemTexture)
	tilesheetImage = Image.open(folderPath.joinpath(itemTexture))
	w, h = tilesheetImage.size
	tilesheetWide = w/16
	tilesheetTall = h/16
	xLoc = (item["index"] % tilesheetWide) * 16
	yLoc = (item["index"] // tilesheetWide) * 16
	itemImages = []
	itemImageLocs = []
	itemImageWidths = []
	itemImageHeights = []
	imageCoords = (xLoc, yLoc, xLoc+16*itemWidth, yLoc+16*itemHeight)
	itemImages.append(tilesheetImage.crop(imageCoords))
	itemImageLocs.append(0)
	itemImageWidths.append(itemWidth)
	itemImageHeights.append(itemHeight)
	# Check the number of rotations is valid for vanilla
	if numRotations != 1 and numRotations != 2 and numRotations != 4:
		print("Warning: number of rotations nonstandard. Defaulting to 1 rotation")
	if numRotations == 2 or numRotations == 4:
		imageCoords = (xLoc+16*itemWidth, yLoc, xLoc+16*itemWidth+16*rotatedWidth, yLoc+16*rotatedHeight)
		itemImages.append(tilesheetImage.crop(imageCoords))
		itemImageLocs.append(1)
		itemImageWidths.append(rotatedWidth)
		itemImageHeights.append(rotatedHeight)
	if numRotations == 4:
		imageCoords = (xLoc+16*itemWidth+16*rotatedWidth, yLoc, xLoc+32*itemWidth+16*rotatedWidth, yLoc+16*itemHeight)
		itemImages.append(tilesheetImage.crop(imageCoords))
		itemImageLocs.append(2)
		itemImageWidths.append(itemWidth)
		itemImageHeights.append(itemHeight)
		imageCoords = (xLoc+16*itemWidth, yLoc, xLoc+16*itemWidth+16*rotatedWidth, yLoc+16*rotatedHeight)
		itemImages.append(tilesheetImage.crop(imageCoords).transpose(Image.Transpose.FLIP_LEFT_RIGHT))
		itemImageLocs.append(3)
		itemImageWidths.append(rotatedWidth)
		itemImageHeights.append(rotatedHeight)
	# For windows and lamps, save the night textures
	if item["type"] == "window" or item["type"] == "lamp":
		imageCoords = (xLoc+16*itemWidth, yLoc, xLoc+16*itemWidth*2, yLoc+16*itemHeight)
		itemImages.append(tilesheetImage.crop(imageCoords))
		itemImageLocs.append("NightTexture")
		itemImageWidths.append(itemWidth)
		itemImageHeights.append(itemHeight)
	imageDict[itemID] = itemImages
	imageLocationDict[itemID] = itemImageLocs
	imageHeightDict[itemID] = itemImageHeights
	imageWidthDict[itemID] = itemImageWidths

	#### DGA
	# Set up the basic furniture data
	dga_item_data = {}
	dga_item_data["$ItemType"] = "Furniture"
	dga_item_data["ID"] = itemID
	if item["type"] in furnitureTypesConversion:
		dga_item_data["Type"] = furnitureTypesConversion[item["type"]] # This needs more data sanitizing/validation
	else:
		dga_item_data["Type"] = furnitureTypesConversion["other"]
		print("Bad item type for " + itemID + " of " + item["type"] + ", defaulting to 'other'")
	# Save the item name and description into default.json
	dga_default["furniture." + itemID + ".name"] = item["name"]
	dga_default["furniture." + itemID + ".description"] = item["description"]
	# Generate the different configurations
	# TODO: add for loop here
	dgaItemTexture = dgaTilesheetName + ":0" # Placeholder
	dgaConfigs = [ {
		"Texture": dgaItemTexture, 
		"DisplaySize": {"X": itemWidth, "Y": itemHeight}, 
		"CollisionHeight": boxHeight
		}]
	if numRotations == 2 or numRotations == 4:
		dgaConfigs.append({
			"Texture": dgaItemTexture,
			"DisplaySize": {"X": rotatedWidth, "Y": rotatedHeight}, 
			"CollisionHeight": rotatedBoxHeight
			})
	if numRotations == 4:
		dgaConfigs.append({
			"Texture": dgaItemTexture,
			"DisplaySize": {"X": itemWidth, "Y": itemHeight}, 
			"CollisionHeight": boxHeight
			})
		dgaConfigs.append({
			"Texture": dgaItemTexture,
			"DisplaySize": {"X": rotatedWidth, "Y": rotatedHeight}, 
			"CollisionHeight": rotatedBoxHeight
			})
	if item["type"] == "chair":
		for i in range(numRotations):
			dgaConfigs[i]["Seats"] = [{"X": 0, "Y": 0}]
			dgaConfigs[i]["SittingDirection"] = dgaSitDirections[i]
			dgaConfigs[i]["FrontTexture"] = frontTilesheetName + ":0" # Placeholder
	if item["type"] == "window":
		dgaConfigs[0]["NightTexture"] = frontTilesheetName + ":0" # Placeholder
	dga_item_data["Configurations"] = dgaConfigs
	# Save to the json array
	dga_data.append(dga_item_data)

	#### CP
	# Set up the basic furniture data
	uniqueItemID = uniqueString + "." + itemID
	itemType = item["type"] # TODO: sanity-check the stool thing
	itemSize = str(itemWidth) + " " + str(itemHeight)
	itemBoxSize = str(boxWidth) + " " + str(boxHeight)
	itemPrice = str(item["price"])
	displayName = "{{i18n:" + uniqueItemID + ".name}}"
	placementRestrict = str(-1)
	tilesheetIndex = str(item["index"])
	tilesheetPath = tilesheetLocation + "\\" + uniqueString + "\\" + itemTexture[:-4]
	# Index 0 for display name
	# Index 1 for type
	# Index 2 for tilesheet size (width height)
	# Index 3 for bounding box size
	# Index 4 for rotations
	# Index 5 for price
	# Index 6 for indoors/outdoors
	# Index 7 for display name
	# Index 8 for the index in the tilesheet
	# Index 9 for the tilesheet path
	cp_item_data = [uniqueItemID, str(itemType), itemSize, itemBoxSize, str(numRotations), 
		itemPrice, placementRestrict, displayName, tilesheetIndex, tilesheetPath]
	cp_item_data = "/".join(cp_item_data)
	# Save to the json dictionary
	cp_default[uniqueItemID + ".name"] = item["name"]
	cp_data[uniqueItemID] = cp_item_data

# Build lists of all the sprite heights and widths
allImageHeights = [];
allImageWidths = [];
for hts in imageHeightDict:
	allImageHeights.extend(imageHeightDict[hts])
for wths in imageWidthDict:
	allImageWidths.extend(imageWidthDict[wths])
allImageHeights = list(set(allImageHeights))
allImageHeights.sort(reverse=True)
allImageWidths = list(set(allImageWidths))
allImageWidths.sort(reverse=True)

# Start placing down sprites
takenTiles = set()
tilesheetWidth = 1
tilesheetHeight = 0
for i in allImageWidths:
	tilesheetWidth = tilesheetWidth*i//math.gcd(tilesheetWidth, i)
tilesheetWidth = tilesheetWidth if tilesheetWidth > 12 else 12
newTilesheet = Image.new(mode="RGBA",size=(tilesheetWidth*16,1200))
frontTilesheet = Image.new(mode="RGBA",size=(tilesheetWidth*16,1200))
for ht in allImageHeights:
	for wth in allImageWidths:
		for item in imageDict:
			for im in imageDict[item]:
				# Get the item index from the dictionary
				imInd = imageLocationDict[item][imageDict[item].index(im)]
				# Get the image size in tiles
				imW, imH = im.size
				imW = int(imW/16)
				imH = int(imH/16)
				# If the image is the right dimensions, place it down
				imageLoc = 0
				canPlace = False
				if imH == ht and imW == wth:
					while not canPlace and imageLoc < 1000:
						imageTileInd = ((imageLoc * imW) // tilesheetWidth) * imH * tilesheetWidth + (imageLoc * imW) % tilesheetWidth
						canPlace = True
						for x in range(imW):
							for y in range(imH):
								if (imageTileInd + x + tilesheetWidth * y) in takenTiles:
									canPlace = False
						if canPlace:
							break
						imageLoc = imageLoc + 1
					# Once a valid location is found, make sure to block out the tiles used
					for x in range(imW):
							for y in range(imH):
								takenTiles.add(imageTileInd + x + tilesheetWidth * y)
					# Set the tilesheet height higher if needed
					if tilesheetHeight < imH * (((imageLoc * imW) // tilesheetWidth) + 1):
						tilesheetHeight = imH * (((imageLoc * imW) // tilesheetWidth) + 1)
					# Set the index in the relevant configuration
					hasFront = False
					for furn in dga_data:
						if furn["ID"] == item:
							try:
								furn["Configurations"][imInd]["Texture"] = dgaTilesheetName + ":" + str(imageLoc)
								if "FrontTexture" in furn["Configurations"][imInd]:
									furn["Configurations"][imInd]["FrontTexture"] = frontTilesheetName + ":" + str(imageLoc)
									if imInd == 2:
										hasFront = True
								if "NightTexture" in furn["Configurations"][imInd]:
									furn["Configurations"][imInd]["NightTexture"] = frontTilesheetName + ":" + str(imageLoc)
							except:
								furn["Configurations"][0][imInd] = dgaTilesheetName + ":" + str(imageLoc)
					# Paste the image into the tilesheet
					imXLoc = 16*((imageLoc * imW) % tilesheetWidth)
					imYLoc = 16*(((imageLoc * imW) // tilesheetWidth) * imH)
					newTilesheet.paste(im,(imXLoc,imYLoc))
					# Paste the image into the front tilesheet if needed
					if hasFront:
						frontTilesheet.paste(im,(imXLoc,imYLoc))

# Add the extra stuff to the CP json
actual_cp_data = {
    "Format": "1.26.0",
    "Changes": [
        {
            "Action": "EditData",
            "Target": "Data/Furniture",
            "Entries": cp_data
        },
    ]
}

# Add in loading the textures
for tex in allTextures:
	actual_cp_data["Changes"].append({
		"Action": "Load",
		"Target": tilesheetLocation + "/" + uniqueString + "/" + tex[:-4],
		"FromFile": tex
		})

# Create the content.json for DGA
dga_content_data = [
	{
        "$ItemType": "ContentIndex",
        "FilePath": "furniture.json"
    },
]

# Make a new manifest for DGA
dga_manifest = {
	"Name": manifest["Name"],
	"Author": modAuthor,
	"Version": "1.0.0",
	"Description": manifest["Description"],
	"UniqueID": modAuthor + ".DGA." + modName,
	"UpdateKeys": [],
	"ContentPackFor": {
		"UniqueID": "spacechase0.DynamicGameAssets",
		"MinimumVersion": "1.4.2",
	},
	"DGA.FormatVersion": 2,
    "DGA.ConditionsFormatVersion": "1.25.0"
}

# Make a new manifest for CP
cp_manifest = {
	"Name": manifest["Name"],
	"Author": modAuthor,
	"Version": "1.0.0",
	"Description": manifest["Description"],
	"UniqueID": modAuthor + ".CP." + modName,
	"UpdateKeys": [],
	"ContentPackFor": {
		"UniqueID": "Pathoschild.ContentPatcher",
		"MinimumVersion": "1.26.0",
	}
}

## Save all the json files
dga_folder_path = Path("[DGA] " + manifest["Name"])
dga_folder_path.mkdir(exist_ok=True)
with dga_folder_path.joinpath("furniture.json").open("w") as write_file:
	json.dump(dga_data, write_file, indent=4)

with dga_folder_path.joinpath("content.json").open("w") as write_file:
	json.dump(dga_content_data, write_file, indent=4)

with dga_folder_path.joinpath("manifest.json").open("w") as write_file:
	json.dump(dga_manifest, write_file, indent=4)

dga_i18n_path = dga_folder_path.joinpath("i18n")
dga_i18n_path.mkdir(exist_ok=True)
with dga_i18n_path.joinpath("default.json").open("w") as write_file:
	json.dump(dga_default, write_file, indent=4)

cp_folder_path = Path("[CP] " + manifest["Name"])
cp_folder_path.mkdir(exist_ok=True)
with cp_folder_path.joinpath("content.json").open("w") as write_file:
    json.dump(actual_cp_data, write_file, indent=4)

with cp_folder_path.joinpath("manifest.json").open("w") as write_file:
    json.dump(cp_manifest, write_file, indent=4)  

cp_i18n_path = cp_folder_path.joinpath("i18n")
cp_i18n_path.mkdir(exist_ok=True)
with cp_i18n_path.joinpath("default.json").open("w") as write_file:
	json.dump(cp_default, write_file, indent=4)

## Save the new DGA tilesheets
newTilesheet = newTilesheet.crop((0,0,tilesheetWidth*16,tilesheetHeight*16))
newTilesheet.save(dga_folder_path.joinpath(dgaTilesheetName))
frontTilesheet = frontTilesheet.crop((0,0,tilesheetWidth*16,tilesheetHeight*16))
frontTilesheet.save(dga_folder_path.joinpath(frontTilesheetName))

## Save the CP tilesheets
for tex in allTextures:
	texIm = Image.open(folderPath.joinpath(tex))
	texIm.save(cp_folder_path.joinpath(tex))