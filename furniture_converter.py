import json
import json5
import re

filename = "original_furniture.json"
uniqueString = "examplemod.user"
tilesheetLocation = "Mods"

furnitureTypes = {
	"Chair": 0,
	"Bench": 1,
	"Couch": 2,
	"Armchair": 3,
	"Dresser": 4,
	"Long Table": 5,
	"Painting": 6,
	"Lamp": 7,
	"Decor": 8,
	"Other": 9,
	"Bookcase": 10,
	"Table": 11,
	"Rug": 12,
	"Window": 13,
	"Fireplace": 14,
	"Bed": 15,
	"Torch": 16,
	"Sconce": 17
}

dgaFurnitureTypes = ["Bed", "Decoration", "Dresser", "Fireplace", "FishTank", "Lamp", "Painting", "Rug",
	"Table", "Sconce", "TV", "Window"]

try:
    # Try using the standard module first because it's fast and handles most cases.
    with open(filename, "r") as read_file:
	    data = json.load(read_file)
except json.decoder.JSONDecodeError:
    # The json5 module is much slower, but is more lenient about formatting issues.
    with open(filename, "r") as read_file:
	    data = json5.load(read_file)

furniture_data = data["furniture"]
cp_data = {}
dga_data = []
cp_default = {}
dga_default = {}
allTextures = set()
for item in furniture_data:
	##### DGA
	# Set up the basic furniture data
	dga_item_data = {}
	dga_item_data["$ItemType"] = "Furniture"
	itemID = re.sub("[^a-zA-Z]+", "", item["name"])
	dga_item_data["ID"] = itemID
	dga_item_data["Type"] = item["type"].capitalize() # This needs more data sanitizing
	itemTexture = item["texture"]
	# Save the item name and description into default.json
	dga_default["furniture." + itemID + ".name"] = item["name"]
	dga_default["furniture." + itemID + ".description"] = item["description"]
	# Generate the different configurations
	numRotations = item["rotations"]
	# Check the number of rotations is valid for vanilla
	if numRotations != 1 and numRotations != 2 and numRotations != 4:
		print("Warning: number of rotations nonstandard. Defaulting to 1 rotation")
	dgaItemTexture = itemTexture + ":" + str(item["index"]) # This is actively wrong unless all the furniture is 1x1
	dgaItemDisplaySize = {"X": item["width"], "Y": item["height"]}
	dgaItemCollisionHeight = item["boxHeight"]
	dga_item_data["Configurations"] = [ {
		"Texture": dgaItemTexture, 
		"DisplaySize": dgaItemDisplaySize, 
		"CollisionHeight": dgaItemCollisionHeight }]
	# Save to the json array
	dga_data.append(dga_item_data)

	##### CP
	# Save textures for later
	allTextures.add(itemTexture)
	# Set up the basic furniture data
	uniqueItemID = uniqueString + "." + itemID
	itemType = furnitureTypes[item["type"].capitalize()]
	itemSize = str(item["width"]) + " " + str(item["height"])
	itemBoxSize = str(item["boxWidth"]) + " " + str(item["boxHeight"])
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
	# Index 6 for display name
	# Index 7 for indoors/outdoors
	# Index 8 for the index in the tilesheet
	# Index 9 for the tilesheet path
	cp_item_data = [uniqueItemID, str(itemType), itemSize, itemBoxSize, str(numRotations), 
		itemPrice, displayName, placementRestrict, tilesheetIndex, tilesheetPath]
	cp_item_data = "/".join(cp_item_data)
	# Save to the json dictionary
	cp_default[uniqueItemID + ".name"] = item["name"]
	cp_data[uniqueItemID] = cp_item_data

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

with open("converted_furniture_dga.json", "w") as write_file:
	json.dump(dga_data, write_file, indent=4)

with open("default_dga.json", "w") as write_file:
	json.dump(dga_default, write_file, indent=4)

with open("converted_furniture_cp.json", "w") as write_file:
    json.dump(actual_cp_data, write_file, indent=4)

with open("default_cp.json", "w") as write_file:
	json.dump(cp_default, write_file, indent=4)