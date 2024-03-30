import json
import json5
import re
import math
import argparse
from PIL import Image
from pathlib import Path

#### Important inputs
CFfilename = "*.json"
originalLocation = "original"
tilesheetLocation = "Mods"
dgaTilesheetName = "dga_furniture_tilesheet.png"
dgaFrontTilesheetName = "dga_front_tilesheet.png"

# TODO: Handle default sitting for armchairs, benches, couches

def main(CFfilename, originalLocation, tilesheetLocation):
	# Create the parser
	parser = argparse.ArgumentParser()
	# Add an argument
	parser.add_argument('--modName', type=str, required=False, help="Name of the mod (no spaces), should be identifying")
	parser.add_argument('--modAuthor', type=str, required=False, help="Author of the original mod (no spaces)")
	parser.add_argument('--sellAt', type=str, required=False, help="Name of shop to sell furniture at. Options are found at https://github.com/spacechase0/StardewValleyMods/blob/develop/DynamicGameAssets/docs/author-guide.md#valid-shop-ids-for-vanilla")
	parser.add_argument('--outputDir', type=str, required=False, help="Optional specific output directory. Will add -1.6 to end for 1.6 version")
	parser.add_argument('--inputDir', type=str, required=False, help="Optional specific input directory")
	# Parse the argument
	args = parser.parse_args()

	# Set information based on inputs
	shouldSell = True if args.sellAt is not None else False
	shopName = None if args.sellAt is None else check_shop_name(args.sellAt)

	## Load up the furniture json!
	folderName = args.inputDir if args.inputDir is not None else originalLocation
	folderPath = Path(folderName)
	
	## Read the manifest json in as text
	manifest = load_json(folderPath, 'manifest.json')
	# Check that the manifest contains the necessary information
	if not check_manifest(manifest):
		print('Malformed manifest, quitting...')
		return
	
	furniture_data = []
	
	## check individual files
	for f in folderPath.glob(CFfilename):
		if not f.is_file():
			continue
			
		data = load_json(folderPath, f.name)
		if f.name == 'manifest.json': continue
		# Check that the furniture json is not empty
		if not data or 'furniture' not in data:
			print("No furniture in %s json, skipping..." % f.name)
			continue
		furniture_data.extend(data["furniture"])

	# Gather useful data out of the manifest
	modAuthor = args.modAuthor if args.modAuthor is not None else manifest['Author']
	modName = args.modName if args.modName is not None else manifest['UniqueID'].split('.')[-1]
	# Strip out spaces and punctuation and such from mod author and mod name
	modAuthor = re.sub(r'[^A-Za-z0-9_\.-]+', '', modAuthor)
	modName = re.sub(r'[^A-Za-z0-9_\.-]+', '', modName)
	uniqueString = modAuthor + "." + modName
	modIDToken = '{{ModId}}'

	#### Time to process!
	cp_data = {}
	dga_data = []
	cp_default = {}
	dga_default = {}
	dga_shop_entries = []
	allTextures = set()
	imageDict = {}
	imageLocationDict = {}
	imageWidthDict = {}
	imageHeightDict = {}
	animatedImages = {}
	cpFrontImages = {}
	count = 0
	for item in furniture_data:
		#### Set up basic information
		if not check_item(item):
			print("Malformed furniture item, skipping to next item...")
			break
		itemName = item["name"]
		itemTexture = item["texture"]
		itemIndex = item["index"]
		itemWidth = item["width"]
		itemHeight = item["height"]
		itemID = re.sub("[^a-zA-Z]+", "", itemName) + str(count)
		itemType = item["type"].casefold() if "type" in item else "other"
		itemDescription = item["description"] if "description" in item else "A piece of furniture."
		itemPrice = item["price"] if "price" in item else 100
		numRotations = item["rotations"] if "rotations" in item else 1
		rotatedWidth = item["rotatedWidth"] if "rotatedWidth" in item else get_rotated_dims(itemType,itemWidth,itemHeight)[0]
		rotatedHeight = item["rotatedHeight"] if "rotatedHeight" in item else get_rotated_dims(itemType,itemWidth,itemHeight)[1]
		boxWidth = item["boxWidth"] if "boxWidth" in item else itemWidth
		boxHeight = item["boxHeight"] if "boxHeight" in item else itemHeight
		rotatedBoxHeight = item["rotatedBoxHeight"] if "rotatedBoxHeight" in item else get_rotated_collision(itemType, boxHeight, rotatedHeight)

		#### Save textures for later
		if "animationFrames" in item:
			if item["animationFrames"] == 0:
				del item["animationFrames"]
		if "animationFrames" in item:
			## Save the animated images separately
			numFrames = item["animationFrames"]
			numRotations = 1
			tilesheetImage = Image.open(folderPath.joinpath(itemTexture))
			itemImage = get_animated_image_info(tilesheetImage, itemIndex, itemWidth, itemHeight, numFrames)
			animatedImages[itemID] = itemImage
		else:
			allTextures.add(itemTexture)
			tilesheetImage = Image.open(folderPath.joinpath(itemTexture))
			# Extract images, locations, widths, and heights from the texture image
			itemImageList, itemImageWidths, itemImageHeights = get_image_info(tilesheetImage, itemIndex, itemWidth, itemHeight, rotatedWidth, rotatedHeight, numRotations, itemType)
			# Extract front textures for CP
			frontCoordsList = get_front_image_info(tilesheetImage, itemIndex, itemWidth, itemHeight, rotatedWidth, rotatedHeight, numRotations, itemType)
			if (itemTexture not in cpFrontImages and frontCoordsList):
				cpFrontImages[itemTexture] = Image.new(mode="RGBA",size=tilesheetImage.size)
			for coords in frontCoordsList:
				cpFrontImages[itemTexture].paste(tilesheetImage.crop(coords),(coords[0],coords[1]))
			# Save data associated with textures of this item
			imageDict[itemID] = itemImageList
			imageHeightDict[itemID] = itemImageHeights
			imageWidthDict[itemID] = itemImageWidths

		count = count + 1

		#### DGA
		# Set up the basic furniture data
		dga_item_data = {}
		dga_item_data["$ItemType"] = "Furniture"
		dga_item_data["ID"] = itemID
		dga_item_data["Type"] = get_dga_type(itemID, itemType)
		dga_item_data["FakeType"] = itemType # Save the original item type for reference later (will be removed)
		dga_item_data["ShowInCatalogue"] = True
		# Save the item name and description into default.json
		dga_default["furniture." + itemID + ".name"] = itemName
		dga_default["furniture." + itemID + ".description"] = itemDescription
		# Generate the different configurations
		if "animationFrames" in item:
			speed = 60//item["fps"] if ("fps" in item and item["fps"] > 0) else 12
			dgaItemTexture = "animated/" + itemID + ".png:0.." + str(item["animationFrames"]-1) + "@" + str(speed)
		else:
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
		if hasSeats(itemType, itemName):
			dgaConfigs = add_dga_seats(dgaConfigs, itemType, itemName, numRotations, itemWidth)
		if "animationFrames" not in item and (itemType == "window" or itemType == "lamp" or itemType == "sconce"):
			dgaConfigs[0]["NightTexture"] = dgaFrontTilesheetName + ":0" # Placeholder
		dga_item_data["Configurations"] = dgaConfigs
		# Save to the json array
		dga_data.append(dga_item_data)
		# If shop entries desired, save data for that
		if shouldSell:
			dga_shop_entries.append({
				"$ItemType": "ShopEntry",
					"Item": { "Value": modAuthor + ".DGA." + modName + "/" + itemID },
					"ShopId": shopName,
					"MaxSold": 1,
					"Cost": itemPrice,
			},)

		#### CP
		# Set up the basic furniture data
		uniqueItemID = modIDToken + "_" + itemID
		itemType = get_cp_type(itemType, itemName)
		itemSize = str(itemWidth) + " " + str(itemHeight)
		itemBoxSize = str(boxWidth) + " " + str(boxHeight)
		displayName = "{{i18n:" + itemID + ".name}}"
		placementRestrict = str(-1)
		tilesheetIndex = str(itemIndex)
		tilesheetPath = tilesheetLocation + "\\" + modIDToken + "\\" + itemTexture[:-4]
		cp_item_data = [uniqueItemID, str(itemType), itemSize, itemBoxSize, str(numRotations), 
			str(itemPrice), placementRestrict, displayName, tilesheetIndex, tilesheetPath]
		cp_item_data = "/".join(cp_item_data)
		# Save to the json dictionary
		cp_default[itemID + ".name"] = itemName
		cp_data[uniqueItemID] = cp_item_data

	# Build lists of all the sprite heights and widths
	allImageWidths, allImageHeights = get_all_widths_heights(imageWidthDict, imageHeightDict)

	# Start placing down sprites
	takenTiles = set()
	tilesheetWidth = get_best_tilesheet_width(allImageWidths)
	tilesheetHeight = 0
	newTilesheet = Image.new(mode="RGBA",size=(tilesheetWidth*16,12000))
	dgaFrontTilesheet = Image.new(mode="RGBA",size=(tilesheetWidth*16,12000))
	for ht in allImageHeights:
		for wth in allImageWidths:
			for item in imageDict:
				for imInfo in imageDict[item]:
					# Unpack the tuple into the image plus its location's name
					im = imInfo[0]
					imLocName = imInfo[1]
					# Get the image size in tiles
					imW, imH = im.size
					imW = int(imW/16)
					imH = int(imH/16)
					# If the image is the right dimensions, place it down
					if imH == ht and imW == wth:
						# Find a valid location for the image on the tilesheet
						imageLoc, imageTileInd = get_image_location(takenTiles, imW, imH, tilesheetWidth, tilesheetHeight)
						# Once a valid location is found, make sure to block out the tiles used
						for x in range(imW):
								for y in range(imH):
									takenTiles.add(imageTileInd + x + tilesheetWidth * y)
						# Set the tilesheet height higher if needed
						if tilesheetHeight < imH * (((imageLoc * imW) // tilesheetWidth) + 1):
							tilesheetHeight = imH * (((imageLoc * imW) // tilesheetWidth) + 1)
						# Set the index in the relevant configuration
						hasFront = False
						frontIsForSideView = False
						for furn in dga_data:
							if furn["ID"] == item:
								try:
									furn["Configurations"][imLocName]["Texture"] = dgaTilesheetName + ":" + str(imageLoc)
									if "FrontTexture" in furn["Configurations"][imLocName]:
										furn["Configurations"][imLocName]["FrontTexture"] = dgaFrontTilesheetName + ":" + str(imageLoc)
										# Add a real front texture if the player is sitting facing upwards
										if furn["Configurations"][imLocName]["SittingDirection"] == "Up":
											hasFront = True
										# Add a partial front texture to the sides of armchairs and couches
										if (furn["Configurations"][imLocName]["SittingDirection"] == "Right" or furn["Configurations"][imLocName]["SittingDirection"] == "Left") and (furn["FakeType"] == "armchair" or furn["FakeType"] == "couch"):
											hasFront = True
											frontIsForSideView = True
									if "NightTexture" in furn["Configurations"][imLocName]:
										furn["Configurations"][imLocName]["NightTexture"] = dgaFrontTilesheetName + ":" + str(imageLoc)
								except Exception as ex:
									try:
										furn["Configurations"][0][imLocName] = dgaTilesheetName + ":" + str(imageLoc)
									except:
										print("Something bad happened when setting the image index " + str(imIng) + " for a texture in " + item + "...")
						# Paste the image into the tilesheet
						imXLoc = 16*((imageLoc * imW) % tilesheetWidth)
						imYLoc = 16*(((imageLoc * imW) // tilesheetWidth) * imH)
						newTilesheet.paste(im,(imXLoc,imYLoc))
						# Paste the image into the front tilesheet if needed
						if hasFront:
							# For the furniture with "arms", add a front texture that's the bottom tile of the side view
							if frontIsForSideView:
								im = im.crop((0, (imH-1)*16, imW*16, imH*16))
								dgaFrontTilesheet.paste(im,(imXLoc,imYLoc+(imH-1)*16))
							else:
								dgaFrontTilesheet.paste(im,(imXLoc,imYLoc))
	# Remove the fake item types
	for furn in dga_data:
		furn.pop("FakeType", None)

	# Add the extra stuff to the CP json
	actual_cp_data = {
			"Format": "2.0.0",
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
			"Target": tilesheetLocation + "/" + modIDToken + "/" + tex[:-4],
			"FromFile": tex
			})
	# Add in loading the front textures
	for imName in cpFrontImages:
		actual_cp_data["Changes"].append({
			"Action": "Load",
			"Target": tilesheetLocation + "/" + modIDToken + "/" + imName[:-4] + "Front",
			"FromFile": imName[:-4] + "Front.png"
			})

	# Create the content.json for DGA
	dga_content_data = [
		{
					"$ItemType": "ContentIndex",
					"FilePath": "furniture.json"
			},
	]

	# Add shop entries json to DGA content if needed
	if shouldSell:
		dga_content_data.append({
					"$ItemType": "ContentIndex",
					"FilePath": "shopEntries.json"
			},)

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
		"UniqueID": modAuthor + '.' + modName,
		"UpdateKeys": manifest["UpdateKeys"] if 'UpdateKeys' in manifest else [],
		"ContentPackFor": {
			"UniqueID": "Pathoschild.ContentPatcher",
			"MinimumVersion": "2.0.0",
		}
	}

	## Save all the DGA json files in an appropriately named folder
	dga_folder_path = Path(args.outputDir) if args.outputDir else Path("[DGA] " + manifest["Name"])
	dga_i18n_path = dga_folder_path.joinpath("i18n")
	save_json(dga_data, dga_folder_path, "furniture.json")
	save_json(dga_content_data, dga_folder_path, "content.json")
	save_json(dga_manifest, dga_folder_path, "manifest.json")
	save_json(dga_default, dga_i18n_path, "default.json")
	if shouldSell:
		save_json(dga_shop_entries, dga_folder_path, "shopEntries.json")

	## Save all of the CP json files in an appropriately named folder
	cp_folder_path = Path(args.outputDir + '-1.6') if args.outputDir else Path("[CP] " + manifest["Name"])
	cp_i18n_path = cp_folder_path.joinpath("i18n")
	save_json(actual_cp_data, cp_folder_path,"content.json")
	save_json(cp_manifest,cp_folder_path,"manifest.json")
	save_json(cp_default, cp_i18n_path, "default.json")

	## Save the new DGA tilesheets if needed
	if tilesheetHeight > 0:
		newTilesheet = newTilesheet.crop((0,0,tilesheetWidth*16,tilesheetHeight*16))
		newTilesheet.save(dga_folder_path.joinpath(dgaTilesheetName))
		dgaFrontTilesheet = dgaFrontTilesheet.crop((0,0,tilesheetWidth*16,tilesheetHeight*16))
		dgaFrontTilesheet.save(dga_folder_path.joinpath(dgaFrontTilesheetName))
	if animatedImages:
		dga_anim_path = dga_folder_path.joinpath("animated")
		dga_anim_path.mkdir(exist_ok=True)
		for imName, im in animatedImages.items():
			im.save(dga_anim_path.joinpath(imName + ".png"))

	## Save the CP tilesheets
	for tex in allTextures:
		texIm = Image.open(folderPath.joinpath(tex))
		cp_folder_path.joinpath(Path(tex).parent).mkdir(exist_ok=True)
		texIm.save(cp_folder_path.joinpath(tex))
	for imName in cpFrontImages:
		im = cpFrontImages[imName]
		cp_folder_path.joinpath(Path(imName).parent).mkdir(exist_ok=True)
		im.save(cp_folder_path.joinpath(Path(imName).stem+"Front.png"))

def load_json(filepath, filename):
	# Read the json in as text
	file_contents = filepath.joinpath(filename).read_text(encoding="UTF-8")

	# Some third-party JSON files begin with extraneous characters - try to fix them up.
	unused_chars, opening_bracket, rest_of_file = file_contents.partition("{")
	file_contents = opening_bracket + rest_of_file  # Discard the extra characters.

	# Some JSON files have curly quotes in them, replace them with normal quotes
	file_contents = file_contents.replace(u'\u201c', '"').replace(u'\u201d', '"')

	try:
			# Try using the standard module first because it's fast and handles most cases.
		data = json.loads(file_contents)
	except json.decoder.JSONDecodeError:
			# The json5 module is much slower, but is more lenient about formatting issues.
			try:
				data = json5.loads(file_contents)
			except json.decoder.JSONDecodeError:
				data = {}
				print("The json file (" + filename + ") specified is not a valid json file. Please try putting it through smapi.io/json and correcting any errors shown there.")

	# Return the data loaded
	return data

def save_json(data, pathname, filename):
	# Make the folder if needed, pulling in relative filepath from filename if needed
	pathname.joinpath(Path(filename).parent).mkdir(exist_ok=True)
	# Save the file
	with pathname.joinpath(filename).open("w", encoding="utf-8") as write_file:
		json.dump(data, write_file, indent=4, ensure_ascii=False)

def check_manifest(manifest):
	if "Author" not in manifest:
		print("Author field missing from manifest! Please correct and try again.")
		return False
	if "Name" not in manifest:
		print("Name field missing from manifest! Please correct and try again.")
		return False
	if "Description" not in manifest:
		print("Description field missing from manifest! Please correct and try again.")
		return False
	return True

def check_item(item):
	if "name" not in item:
		print("Name field missing from a furniture item")
		return False
	if "id" not in item:
		print("ID field missing from " + item["name"])
		return False
	if "texture" not in item:
		print("Texture field missing from " + item["name"])
		return False
	if "index" not in item:
		print("Index field missing from " + item["name"])
		return False
	if "width" not in item:
		print("Width field missing from " + item["name"])
		return False
	if "height" not in item:
		print("Height field missing from " + item["name"])
		return False
	return True

def get_front_image_info(tilesheetImage, itemIndex, itemWidth, itemHeight, rotatedWidth, rotatedHeight, numRotations, itemType):
	w, h = tilesheetImage.size
	tilesheetWide = w/16
	tilesheetTall = h/16
	xLoc = (int)(itemIndex % tilesheetWide) * 16
	yLoc = (int)(itemIndex // tilesheetWide) * 16
	frontImageCoordsList = []
	imageCoords = (xLoc, yLoc, xLoc+16*itemWidth, yLoc+16*itemHeight)
	if (itemType == "chair" or itemType == "bench"):
		if (numRotations == 4):
			frontImageCoordsList.append((xLoc+16*itemWidth+16*rotatedWidth, yLoc, xLoc+32*itemWidth+16*rotatedWidth, yLoc+16*itemHeight))
	elif (itemType == "armchair" or itemType == "couch"):
		if (numRotations == 4):
			frontImageCoordsList.append((xLoc+16*itemWidth, yLoc+16*(rotatedHeight-1), xLoc+16*itemWidth+16*rotatedWidth, yLoc+16*rotatedHeight))
			frontImageCoordsList.append((xLoc+16*itemWidth+16*rotatedWidth, yLoc, xLoc+32*itemWidth+16*rotatedWidth, yLoc+16*itemHeight))
	return frontImageCoordsList

def get_image_info(tilesheetImage, itemIndex, itemWidth, itemHeight, rotatedWidth, rotatedHeight, numRotations, itemType):
	w, h = tilesheetImage.size
	tilesheetWide = w/16
	tilesheetTall = h/16
	xLoc = (itemIndex % tilesheetWide) * 16
	yLoc = (itemIndex // tilesheetWide) * 16
	itemImageList = [] # Store the images and their location's names
	itemImageWidths = [] # Store the widths
	itemImageHeights = [] # Store the heights
	imageCoords = (xLoc, yLoc, xLoc+16*itemWidth, yLoc+16*itemHeight)
	itemImageList.append((tilesheetImage.crop(imageCoords),0))
	itemImageWidths.append(itemWidth)
	itemImageHeights.append(itemHeight)
	# Check the number of rotations is valid for vanilla
	if numRotations != 1 and numRotations != 2 and numRotations != 4:
		print("Warning: number of rotations (" + str(numRotations) + ") nonstandard. Defaulting to 1 rotation")
	# For furniture with rotations, automatically look in the expected places for rotation images
	if numRotations == 2 or numRotations == 4:
		imageCoords = (xLoc+16*itemWidth, yLoc, xLoc+16*itemWidth+16*rotatedWidth, yLoc+16*rotatedHeight)
		itemImageList.append((tilesheetImage.crop(imageCoords),1))
		itemImageWidths.append(rotatedWidth)
		itemImageHeights.append(rotatedHeight)
	if numRotations == 4:
		imageCoords = (xLoc+16*itemWidth+16*rotatedWidth, yLoc, xLoc+32*itemWidth+16*rotatedWidth, yLoc+16*itemHeight)
		itemImageList.append((tilesheetImage.crop(imageCoords),2))
		itemImageWidths.append(itemWidth)
		itemImageHeights.append(itemHeight)
		imageCoords = (xLoc+16*itemWidth, yLoc, xLoc+16*itemWidth+16*rotatedWidth, yLoc+16*rotatedHeight)
		itemImageList.append((tilesheetImage.crop(imageCoords).transpose(Image.Transpose.FLIP_LEFT_RIGHT),3))
		itemImageWidths.append(rotatedWidth)
		itemImageHeights.append(rotatedHeight)
	# For windows and lamps, save the night textures
	if itemType == "window" or itemType == "lamp":
		imageCoords = (xLoc+16*itemWidth, yLoc, xLoc+16*itemWidth*2, yLoc+16*itemHeight)
		itemImageList.append((tilesheetImage.crop(imageCoords),"NightTexture"))
		itemImageWidths.append(itemWidth)
		itemImageHeights.append(itemHeight)
	return itemImageList, itemImageWidths, itemImageHeights

def get_animated_image_info(tilesheetImage, itemIndex, itemWidth, itemHeight, numFrames):
	w, h = tilesheetImage.size
	tilesheetWide = w/16
	tilesheetTall = h/16
	xLoc = (itemIndex % tilesheetWide) * 16
	yLoc = (itemIndex // tilesheetWide) * 16
	imageCoords = (xLoc, yLoc, xLoc+16*itemWidth*numFrames, yLoc+16*itemHeight)
	return tilesheetImage.crop(imageCoords)

def check_shop_name(shopName):
	validShopIDs = ["BlueBoat","GeMagic","FishShop","Club","DesertMerchant",
		"Sandy","HatMouse","AnimalSupplies","TravelingMerchant","IslandMerchant",
		"QiGemShop","ResortBar","VolcanoShop","AdventurerGuild","Dwarf",
		"Carpenter","Blacksmith","Hospital","IceCreamStand","Joja","Krobus",
		"Theater_BoxOffice","SeedShop","Saloon","Festival.spring13","Festival.spring24",
		"Festival.summer11","Festival.summer28","Festival.fall16","Festival.fall27",
		"Festival.winter8","Festival.winter25"]
	if shopName in validShopIDs:
		return shopName
	else:
		print("Shop name to sell at not valid, defaulting to Robin's shop.")
		return "Carpenter"

def get_dga_type(itemID, itemType):
	furnitureTypesConversion = {
		"chair": "Decoration",
		"bench": "Decoration",
		"couch": "Decoration",
		"armchair": "Decoration",
		"dresser": "Dresser",
		"long table": "Table",
		"painting": "Painting",
		"lamp": "Lamp",
		"decor": "Decoration",
		"other": "Decoration",
		"bookcase": "Decoration",
		"table": "Table",
		"rug": "Rug",
		"window": "Window",
		"fireplace": "Fireplace",
		"bed": "Bed",
		"sconce": "Sconce",
		"stool": "Decoration"
	}
	if itemType in furnitureTypesConversion:
		return furnitureTypesConversion[itemType]
	else:
		print("Bad item type for " + itemID + " of " + itemType + ", defaulting to 'other'")
		return furnitureTypesConversion["other"]

def get_cp_type(itemType, itemName):
	if "stool" in itemName.lower():
		return "chair"
	furnitureTypesConversion = {
		"chair": "chair",
		"bench": "bench",
		"couch": "couch",
		"armchair": "armchair",
		"dresser": "dresser",
		"long table": "longTable",
		"painting": "painting",
		"lamp": "lamp",
		"decor": "decor",
		"other": "other",
		"bookcase": "bookcase",
		"table": "table",
		"rug": "rug",
		"window": "window",
		"fireplace": "fireplace",
		"bed": "bed",
		"sconce": "sconce",
		"stool": "chair"
	}
	if itemType in furnitureTypesConversion:
		return furnitureTypesConversion[itemType]
	else:
		print("Bad item type for " + itemName + " of " + itemType + ", defaulting to 'other'")
		return furnitureTypesConversion["other"]

def get_rotated_dims(itemType, width, height):
	if (itemType == "chair" or itemType == "stool" or itemType == "lamp"):
		return (width, height)
	else:
		return (height, width)

def get_rotated_collision(itemType, boxHeight, rotatedHeight):
	if (itemType == "chair" or itemType == "stool" or itemType == "lamp"):
		return boxHeight
	else:
		return rotatedHeight

def add_dga_seats(dgaConfigs, itemType, itemName, numRotations, itemWidth):
	# Set the directions of sitting depending on how many rotations there are
	if numRotations == 1:
		sitDirections = ["Down"]
	elif numRotations == 2:
		sitDirections = ["Down","Up"]
	elif numRotations == 4:
		sitDirections = ["Down","Right","Up","Left"]
	else:
		sitDirections = ["Down"]

	# Put the stool seats in if it's a stool
	if itemType == "stool" or "stool" in itemName.lower():
		for i in range(numRotations):
			if i < len(dgaConfigs):
				dgaConfigs[i]["Seats"] = [{"X": 0, "Y": 0}]
				dgaConfigs[i]["SittingDirection"] = "Any"
				dgaConfigs[i]["FrontTexture"] = dgaFrontTilesheetName + ":0" # Placeholder
		return dgaConfigs

	# Put the chair seats in if it's a chair
	if itemType == "chair":
		for i in range(numRotations):
			if i < len(dgaConfigs):
				dgaConfigs[i]["Seats"] = [{"X": 0, "Y": 0}]
				dgaConfigs[i]["SittingDirection"] = sitDirections[i]
				dgaConfigs[i]["FrontTexture"] = dgaFrontTilesheetName + ":0" # Placeholder
		return dgaConfigs

	armchairSeats = [{"X": 0.5, "Y": 0},{"X": 1, "Y": 0},{"X": 0.5, "Y": 0},{"X": 0, "Y": 0}]
	if itemType == "armchair":
		for i in range(numRotations):
			if i < len(dgaConfigs):
				dgaConfigs[i]["Seats"] = [armchairSeats[i]]
				dgaConfigs[i]["SittingDirection"] = sitDirections[i]
				dgaConfigs[i]["FrontTexture"] = dgaFrontTilesheetName + ":0" # Placeholder
		return dgaConfigs

	if itemType == "couch":
		for i in range(numRotations):
			if i < len(dgaConfigs):
				seatLocs = []
				for s in range(itemWidth - 1):
					if i == 0:
						seatLocs.append({"X": s+1, "Y": 0})
					elif (i == 1 and numRotations == 4):
						seatLocs.append({"X": 1, "Y": s+1})
					elif (i == 2 and numRotations == 4) or (i == 1 and numRotations == 2):
						seatLocs.append({"X": s+1, "Y": 0})
					elif i == 3:
						seatLocs.append({"X": 0, "Y": s+1})
					dgaConfigs[i]["Seats"] = seatLocs
				dgaConfigs[i]["SittingDirection"] = sitDirections[i]
				dgaConfigs[i]["FrontTexture"] = dgaFrontTilesheetName + ":0" # Placeholder
		return dgaConfigs

	if itemType == "bench":
		for i in range(numRotations):
			if i < len(dgaConfigs):
				seatLocs = []
				for s in range(itemWidth):
					if i == 0:
						seatLocs.append({"X": s+0.5, "Y": 0})
					elif (i == 1 and numRotations == 4):
						seatLocs.append({"X": 1, "Y": s+0.5})
					elif (i == 2 and numRotations == 4) or (i == 1 and numRotations == 2):
						seatLocs.append({"X": s+0.5, "Y": 0})
					elif i == 3:
						seatLocs.append({"X": 0, "Y": s+0.5})
					dgaConfigs[i]["Seats"] = seatLocs
				dgaConfigs[i]["SittingDirection"] = sitDirections[i]
				dgaConfigs[i]["FrontTexture"] = dgaFrontTilesheetName + ":0" # Placeholder
		return dgaConfigs

	return dgaConfigs

def hasSeats(itemType, itemName):
	if itemType == "chair" or itemType == "armchair" or itemType == "bench" or itemType == "couch" or itemType == "stool" or "stool" in itemName.lower():
		return True
	else:
		return False

def get_all_widths_heights(imageWidthDict, imageHeightDict):
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
	return allImageWidths, allImageHeights

def get_best_tilesheet_width(allImageWidths):
	tilesheetWidth = 1
	for i in allImageWidths:
		tilesheetWidth = tilesheetWidth*i//math.gcd(tilesheetWidth, i)
	tilesheetWidth = tilesheetWidth if tilesheetWidth > 12 else 12
	return tilesheetWidth

def get_image_location(takenTiles, imW, imH, tilesheetWidth, tilesheetHeight):
	imageLoc = 0
	canPlace = False
	while not canPlace and imageLoc < 10000:
		imageTileInd = ((imageLoc * imW) // tilesheetWidth) * imH * tilesheetWidth + (imageLoc * imW) % tilesheetWidth
		canPlace = True
		for x in range(imW):
			for y in range(imH):
				if (imageTileInd + x + tilesheetWidth * y) in takenTiles:
					canPlace = False
		if canPlace:
			break
		imageLoc = imageLoc + 1
	if imageLoc > 1000:
		print("Warning: Image being placed extremely far down tilesheet. Check DGA tilesheet once created.")
	return imageLoc, imageTileInd

# Call the main() function to actually do things
main(CFfilename, originalLocation, tilesheetLocation)

## Some fun facts for reference
dgaFurnitureTypes = ["Bed", "Decoration", "Dresser", "Fireplace", "FishTank", "Lamp", "Painting", "Rug",
	"Table", "Sconce", "TV", "Window"]
# In Content Patcher furniture: 
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
