from __future__ import print_function
import string
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import numpy,time,datetime,os
from random import randint
from copy import deepcopy
import csv
import os,sys

#Backfiller

def checkInput(listOfItems):
	try:			
		null = listOfItems[0]
		questionForUser = "To edit one of the options choose number between 1 and " + str(len(listOfItems)) + " or Press Enter to accept them all (q to quit) "	
		enterToAccept = True
	except:
		questionForUser = "Choose number between 1 and " + str(len(listOfItems)) + " (q to quit) "
		enterToAccept = False
	userNumber = input(questionForUser)
	incorrectEntry = True
	skipWhileLoop = False
	if userNumber == "q" or userNumber == "Q" or userNumber == "Quit":
		print("Exiting...")
		print ()
		sys.exit(0)
	elif enterToAccept and userNumber == '':
		print ("Accepting config data...")
		numberChosen = -1
		skipWhileLoop = True
	else:
		while incorrectEntry:
			try:
				numberChosen = int(userNumber)
				incorrectEntry = False
			except:
				print ()
				print ("Opps that's not a number")
				userNumber,skipWhileLoop = checkInput(listOfItems)

	while numberChosen < 1 or numberChosen > len(listOfItems): 
		if skipWhileLoop:
			break
		else:
			if len(listOfItems) == 1:
				print ()
				print ("You need to choose '1'!")				
				userNumber,skipWhileLoop = checkInput(listOfItems)
			else:	
				print ()
				print ("Opps that number is not between 1 and ", len(listOfItems))
				userNumber,skipWhileLoop = checkInput(listOfItems)
		
			numberChosen = userNumber
	return ([numberChosen,skipWhileLoop])

def chooseItem(listOfItems):
	for index,item in enumerate(listOfItems):
		print(index+1,") ",item) # Make the number list start at 1 rather than 0
	print()
	numberChosen,skipWhileLoop = checkInput(listOfItems)
	if numberChosen == -1: #Using config data
		print ("Will use config data...") #Then adjust for the list starting at 0 in python
		itemName = "UseConfig"
	else:	
		print ("You chose: ", numberChosen,") ",listOfItems[numberChosen-1]) #Then adjust for the list starting at 0 in python
		itemName = listOfItems[numberChosen-1]
	return([numberChosen-1,itemName,skipWhileLoop])

def getUserTextInput(inputType):
	print ("Enter your ",inputType," below...")
	userInput = input ("Press enter when done: ")
	while True:
		print()
		print ("You entered: ",userInput)
		print()
		userConfirm = input("Press enter to confirm - Enter any other character followed by enter to re-enter :")
		if userConfirm == "":
			break
		else:
			userInput = getUserTextInput(inputType)
	#print (userInput)
	return (userInput)


def char_to_pixels(text, path, fontsize=14):
	"""
	Based on https://stackoverflow.com/a/27753869/190597 (jsheperd)
	"""
	font = ImageFont.truetype(path, fontsize)
	w, h = font.getsize(text)  
	h *= 2
	image = Image.new('L', (w, h), 1)  
	draw = ImageDraw.Draw(image)
	draw.text((0, 0), text, font=font)
	arr = numpy.asarray(image)
	arr = numpy.where(arr, 0, 1)
	arr = arr[(arr != 0).any(axis=1)]
	return arr

def display(arr):
	result = numpy.where(arr, 'o', ' ')
	print('\n'.join([''.join(row) for row in result]))

def timeStamp ():
	ts = time.time()	
	dateTimeString = datetime.datetime.fromtimestamp(ts).strftime('%y%m%d%H%M')
	return (dateTimeString)	

def initialiseMatrix():
	layer = numpy.empty(shape=(5,5))
	value = 1
	layer.fill(int(value))
	print (layer)

def getHeight (randomStuds,height):
	if randomStuds:
		height= randint(1,3)
		if height == 2:
			height = 1
	else:
		null = 0
	return height

def randomLayer(x,y,noRandom):
	studMatrix = []
	Width = x
	Depth = y
	print ("Layer is ",Width, "x" ,Depth)
	for i in range (0,Width):
		for j in range(0,Depth):
			if noRandom == 1:
				stud = randint(0,1)
			else:
				stud = 1
			studMatrix.append(stud)
	randomLayer = numpy.array(studMatrix).reshape(Depth,Width);
	return randomLayer	

def layerMatrix(depth,width,randomStuds,height):
	studMatrix = []
	for i in range (0,width):
		for j in range(0,depth):
			height = getHeight(randomStuds,height)
			studMatrix.append(height)
	baseMatrix = numpy.array(studMatrix).reshape(depth,width)
	return baseMatrix	

def excludeBricks(width,depth):
	if width == 3 or width == 4:
		depth = randint(1,2)
	if depth == 3 or width == 4:
		width = randint(1,2)
	return([width,depth])

def getBrickMatrix():
	width = randint(1,4)
	depth = randint(1,4)
	width,depth = excludeBricks(width,depth)
	#Force Brick Dimensions for testing
	forceBrick = False
	if forceBrick:
		forceBrick = randint(0,1)
		if forceBrick == 0:
			width = 1
			depth = 4
		else:
			width = 4
			depth = 1
	#==================================
	height= randint(1,3)
	if height == 2:
		height = 1 #This is better for packing
	brickMatrix = layerMatrix(width,depth,False,height)
	return brickMatrix

def evenDistribution():
	#A function to create a 50/50 distribution of bricks and plates
	evenDistribution = randint(1,2) #Select bricks or plates with a 50/50 chance
	if evenDistribution == 1:
		height = 1
	else:
		height = 3
	return(height)

def get1x1Brick():
	width = randint(1,1)
	depth = randint(1,1)
	height= randint(1,3)
	if height == 2:
		height = 1 #This is better for packing
	brickMatrix = layerMatrix(width,depth,False,height)
	return brickMatrix

def getLayerMin(layerMatrix,randomLayerMatrix):
	layerHeightFromRandom = []
	yLayerSize, xLayerSize = layerMatrix.shape
	for y in range(0,yLayerSize):
		for x in range(0,xLayerSize):
			randomMatrixValue = randomLayerMatrix[y][x]
			if randomMatrixValue == 1:
				layerMatrixValue = layerMatrix[y][x]
				if layerMatrixValue not in layerHeightFromRandom:
					layerHeightFromRandom.append(layerMatrixValue)
	layerHeightFromRandom.sort()
	print ("layerHeightFromRandom",layerHeightFromRandom)				
	layerMin = layerHeightFromRandom[0]
	print()
	return (layerMin)

def brickDensity(layerMatrix,brickMatrix,processLayerMatrix):
	layerMin = getLayerMin(layerMatrix,processLayerMatrix)
	layerMax = numpy.max(layerMatrix)
	yLayerSize, xLayerSize = layerMatrix.shape
	xSizeBrick, ySizeBrick = brickMatrix.shape
	layerSize = yLayerSize*xLayerSize
	minCoverage = numpy.count_nonzero(layerMatrix == layerMin)
	minPercentage = (minCoverage/layerSize)*100
	#escapeBrick = 0
	x = 0
	y = 0
	exitLoop = 0
	for j in range(0,yLayerSize):
		for i in range(0,xLayerSize):
			layerValue = layerMatrix[j][i]
			processLayerValue = processLayerMatrix[j][i]	
			#print (layerValue,j,i)
			if layerValue == layerMin and processLayerValue == 1:
				exitLoop = 1
				break
		if exitLoop == 1:	
			break
	x = i
	y = j			
	print(y,x)
	#input()		
	print("layerMin",layerMin,"layerSize",layerSize,"minCoverage",minCoverage,"minPercentage",minPercentage)

	while y < yLayerSize:
		while x < xLayerSize:
			while True:
				brickFail = checkXYBasedOnBrickShape(brickMatrix,layerMatrix,x,y)
				if brickFail:
					brickMatrix = getBrickMatrix()
					print ("New brick is \n",brickMatrix)
					xSizeBrick, ySizeBrick = brickMatrix.shape
				else:
					print ("Old brick is \n",brickMatrix)
					print ("leaving loop...")
					break
			print(x,y)
			checkBrickFit = subMatrix( layerMatrix, y, x, xSizeBrick,ySizeBrick)
			checkBrickFitRandomLayer = subMatrix( processLayerMatrix, y, x, xSizeBrick,ySizeBrick)
			if numpy.all(checkBrickFit == layerMin) and numpy.all(checkBrickFitRandomLayer == 1): #All sub matrix = lowest value of matrix
				print ("Brick Size is:")
				print (brickMatrix)
				print ("BRICK OK at",x, y)
				#print("in LAYER")
				#print (layerMatrix)
				brickNoFit = 0
				return ([x,y,brickNoFit,minPercentage,layerMin,brickMatrix])
			else:
				print ("Brick Size is:")
				print (brickMatrix)
				print ("BRICK WILL NOT FIT at",x, y,"(",xLayerSize,yLayerSize,")")
				#print("in LAYER")
				#print (layerMatrix)
				print()
				#print (processLayerMatrix)
				brickNoFit = 1
				x+=1
		y+=1
	return ([x,y,brickNoFit,minPercentage,layerMin,brickMatrix])	

def addAtPos(layerMatrix, brickMatrix,fileName,dateTimeStamp,maxHeight,randomLayerMatrix,heightApproximation,totalStudCount,hue,textToCreate,layerStudCount): # From https://stackoverflow.com/questions/9886303/adding-different-sized-shaped-displaced-numpy-matrices
	print(brickMatrix)
	exitLoop = False
	print()
	#CALCULATE THE BRICK FIT (DENSITY)
	x,y,brickNoFit,minPercentage,layerMin,brickMatrix = brickDensity(layerMatrix,brickMatrix,randomLayerMatrix)
	print ("In addAtPos",x, y)
	ySize, xSize = brickMatrix.shape
	xLayerMax,yLayerMax = layerMatrix.shape
	xMax, yMax = (x + xSize), (y + ySize)
	#layerStudCount = numpy.count_nonzero(brickMatrix)
	print ("******")
	print ("brickMatrix,x,y,xSize,ySize\n",brickMatrix,"\n",x,y,xSize,ySize)
	print ("******")
	try: 
		if brickNoFit == 1:
			brickMatrix = get1x1Brick()
			print ("New Brick is...\n", brickMatrix)
			x,y,brickNoFit,minPercentage,layerMin,brickMatrix = brickDensity(layerMatrix,brickMatrix,randomLayerMatrix)
	except: # Skip if it's the first pass
		print("Setting up...")
	ySize, xSize = brickMatrix.shape
	xMax, yMax = (x + xSize), (y + ySize)
	#print ("layerMatrix, brickMatrix,x,y,xMax,yMax,brickNoFit,brickFail\n",layerMatrix,"\n", brickMatrix,"\n",x,y,xMax,yMax,brickNoFit,brickFail)
	#THE FOLLOWING LINE IS THE ACTUAL ADD FUNCTION
	layerMatrix[y:yMax, x:xMax] += brickMatrix
	print ("Added layerMatrix")
	#print (layerMatrix)
	#This function makes sure that an individual brick stayes "level" and the brick matrix doesn't "stagger" across the buld matrix
	layerMatrix,brickDetails = checkResultOfMatixAdditionToAllowForUplift(layerMatrix,brickMatrix,x,y,xSize,ySize,fileName,dateTimeStamp)
	#Check the output of the addition
	#print (layerMatrix)
	height = layerMatrix[y,x]
	brickDetails.extend((x,y,height))
	print ("Brick Dimensions x,y / PartID / Rotation / Placement x,y / Height")
	print (brickDetails)
	print (x,y)
	#input()   #Watch the output after the addition
	print ("!=!=!=!=!=!=!=!=!=!=!=!=!=!=!=!=!=!=!=!=!=!=!=!=!=!=")
	#Keep a track of the number of studs added to each layer
	layerStudCount = layerStudCount + (ySize*xSize)
	#ADD LEGO BRICK HERE?
	addBrickPart(brickDetails,fileName,dateTimeStamp,maxHeight,hue,textToCreate)
	#input() #Watch the output and the ldr file
	return ([layerStudCount,layerMatrix])	

def calculateHeight(heightApproximation):
	heightApproximation = heightApproximation + 1
	return(heightApproximation)

def checkXYBasedOnBrickShape(brickMatrix,layerMatrix,y,x):
	#This function ensures that bricks do not spill over the edge of the base matrix bay calculating the size of the brick and then adjusting the random positioning accordingly.
	print ("Checking brick fits on base...")
	brickFail = False
	xBrickSize, yBrickSize = brickMatrix.shape
	xLayerSize, yLayerSize = layerMatrix.shape
	print("y,yBrickSize,yLayerSize",y,yBrickSize,yLayerSize)
	print("x,xBrickSize,xLayerSize",x,xBrickSize,xLayerSize)
	print ("x+xBrickSize",x+xBrickSize)
	print ("y+yBrickSize",y+yBrickSize)
	if x+xBrickSize > xLayerSize:
		print ("Brick too large to fit on base in X")
		brickFail = True
	elif y+yBrickSize > yLayerSize:
		print ("Brick too large to fit on base in Y")
		brickFail = True
	else:
		brickFail = False	
	return brickFail

def addBrickPart(brickDetails,fileName,dateTimeStamp,maxHeight,hue,textToCreate):
	partID = brickDetails[2]
	height = brickDetails[6]
	print(height)
	colour = 7 # Set everything to "Grey"
	brickStage = 1 #Used to manage colour distribution over height
	#colour = colourMeBrick(height,brickStage,maxHeight) #Use advanced colours
	#colour = randomColour()
	if textToCreate == "Lego" and hue == "Yellows":
		print("Skipping...")
		#brickStage = 7 #Use for Lego Logo
		#colour = colourMeBrick(height,brickStage,maxHeight) #Use for Lego Logo		
	else:
		if hue == "Random Colours":
			colour = randomColour()
		else:
			colour = selectColour(hue)
	partID = fixForTransparency(colour,partID)
	#if colour == 47:#If transparent - Make sure it's only a basic 1x2 brick (the others don't exist in transparency)
	#	if partID == "30136.dat" or partID == "98283.dat" or partID == "2877.dat":
	#		partID = "3004.dat"	
	#Get the LDraw line data
	width,depth,height,m1,m2,m3,m4,m5,m6,m7,m8,m9 = brickPlacementAdjustments(brickDetails)
	#Build the LDraw line
	ldrLine = activeLine(1, colour, width, height, depth, m1, m2, m3, m4, m5, m6, m7, m8, m9,partID)	
	print (ldrLine)
	#print (fileName,dateTimeStamp) #Check the name and datestame
	#Write out the LDraw line
	legoWriter(fileName,dateTimeStamp,ldrLine)

def fixForTransparency(colour,partID):
	listOfTransparency = [36,38,46,35,293,33,52,44,47,40,45,37,39,40,234,231,57]
	if colour in listOfTransparency :#If transparent - Make sure it's only a basic 1x2 brick (the others don't exist in transparency)
		if partID == "30136.dat" or partID == "98283.dat" or partID == "2877.dat":
			partID = "3004.dat"	
	return(partID)

def selectColour(hue):
	colour,colourList = selectColourAndHues(hue,True)
	return (colour)

def randomColour():
	randomColour = randint(1,15)
	return(randomColour)

def colourMeBrick(height,brickStage,maxHeight):	#Basic colour function - needs work
	colour = colourFinder(height,brickStage,maxHeight)
	if height > 6 and height < maxHeight - 5:
		print ("Transparency available")
		trans = randint(0,4)
		if trans == 4:
			colour = 47 # Set colour to transparent
	return colour 

def selectColourAndHues(hue,transparency): #Colour hue selector
	if transparency:
		transparency = 0
	else:
		transparency = 1


	simpleColours = {   #Allow for selection of both light and dark if needed
		'Blues':['LightBlues','DarkBlues'],								
		'Pinks':['LightPinks','DarkPinks'],										
		'Greys':['LightGreys','DarkGreys'],										
		'Browns':['LightBrowns','DarkBrowns'],
		}

	colourAndHues = {   #FIRST NUMBER IS TRANS
		'Reds':[36,4,216,320],					
		'Oranges':[38,25,191,366,462],								
		'Yellows':[46,14,18,226],								
		'Greens':[35,2,10,27,74],								
		'LightBlues':[293,9,73,212,232,321,322],								
		'DarkBlues':[33,1,85,89,112],								
		'Indigos':[52,23,85,219],								
		'Violets':[44,22,26,30,218],								
		'Whites':[47,15,503],							
		'Blacks':[40,0,308],	
		'LightPinks':[45,13,29,77,100,295],										
		'DarkPinks':[37,5,69,351],										
		'LightGreys':[39,7,20,378],										
		'DarkGreys':[40,8,72,379],										
		'Beiges':[234,12,18,19,68,78],										
		'LightBrowns':[231,84,125,191,450],
		'DarkBrowns':[57,6,70,84,86,128,484]
		}
	try: #See if a simple colour like Blues, Pinks, Greys or Brows has been selected - if so randomly choose light or dark hues
		lightOrDarkList = simpleColours.get(hue)
		lightOrDark = lightOrDarkList[randint(0,1)]
		listOfColourValues = colourAndHues.get(lightOrDark)
		#print(listOfColourValues)
	except:	#Otherwise just use the value given
		listOfColourValues = colourAndHues.get(hue)
	lengthOfList = len(listOfColourValues)-1 #-1 to compensate for starting at zero
	colourValue = listOfColourValues[randint(transparency,lengthOfList)] #Skip the trans value by starting at 1
	colourList = list(colourAndHues.keys())
	#print(colourList)
	#print (colourValue)
	return([colourValue,colourList])

def colourFinder(height,brickStage,maxHeight): #Colour hue selector - needs works
	#if brickStage == 6:
	#	colour,colourList = selectColourAndHues("Whites",False)
	if height < 4:
		if brickStage == 3: #Choose blues
			colour,colourList = selectColourAndHues("Blues",False)
		elif brickStage == 5: #Choose Browns
			colour,colourList = selectColourAndHues("Greens",False)
		else:
			colour,colourList = selectColourAndHues("Reds",False)
	elif height < 10:#Lowest layer - 1 brick height
		if brickStage == 1:
			colour,colourList = selectColourAndHues("Greys",False)
		else:
			colour,colourList = selectColourAndHues("Whites",True)
	elif height < 12: #Brick Red
		colour,colourList = selectColourAndHues("Reds",False)
	else:
		colour,colourList = selectColourAndHues("Greys",False)
	
	if brickStage == 4:
		colour,colourList = selectColourAndHues("Beiges",False)
	
	#For lego logo only
	if brickStage == 7 and height < 5:
		colour,colourList = selectColourAndHues("Yellows",False)
	else:
		colour,colourList = selectColourAndHues("Greens",True)
	if brickStage == 9:
		colour,colourList = selectColourAndHues("Whites",False)
	if brickStage == 8 and height < 4:
		colour,colourList = selectColourAndHues("Reds",False)
	elif brickStage == 8:
		colour,colourList = selectColourAndHues("Whites",False)

	return colour

def brickPlacementAdjustments(brickDetails): #Move the brick depending on the dimesions of the brick and it's rotation
	brickX = brickDetails[0]
	brickY = brickDetails[1]
	rotate = brickDetails[3]
	width = brickDetails[5] #x
	depth = brickDetails[4] #y
	height = brickDetails[6]
	#print ("Original Values", width,depth,height)
	#Change into Lego Units
	width = width*20-20
	depth = depth*20-20
	height = (height*-8)+8

	#PLACEMENT CORRECTIONS
	#Make brick adjustments for bricks based on dimensions
	if (brickX == 1 and brickY == 2) or (brickY == 1 and brickX == 2):
		#Adjust placement for 1x2 bricks
		depth = depth - 10

	if (brickX == 1 and brickY == 1):
		#Adjust placement for 1x1 bricks
		depth = depth - 10
		width = width - 10

	if (brickX == 3 and brickY == 1) or (brickY == 3 and brickX == 1):
		#Adjust placement for 1x3 bricks
		depth = depth - 10
		width = width + 10


	if (brickX == 3 and brickY == 2) or (brickY == 3 and brickX == 2):
		#Adjust placement for 2x3 bricks
		width = width + 10

	if (brickX == 4 and brickY == 1) or (brickY == 4 and brickX == 1):
		#Adjust placement for 1x4 bricks
		print("NOT ROTATED")
		depth = depth - 10 #side/side
		width = width + 20 #up/down

	if (brickX == 4 and brickY == 2) or (brickY == 4 and brickX == 2):
		#Adjust placement for 2x3 bricks
		depth = depth + 10
		width = width + 10

	#ROTATION CORRECTIONS
	if rotate == 1: #Brick has been rotated
		#Adjust placement for rotation
		depth = depth + 10
		width = width - 10

		if (brickX == 3 and brickY == 1) or (brickY == 3 and brickX == 1):
			depth = depth + 10
			width = width - 10

		if (brickX == 4 and brickY == 1) or (brickY == 4 and brickX == 1):
			depth = depth + 20 #side/side
			width = width - 20
		m1=0;m2=0;m3=1;m4=0;m5=1;m6=0;m7=-1;m8=0;m9=0
	else:
		m1=-1;m2=0;m3=0;m4=0;m5=1;m6=0;m7=0;m8=0;m9=-1

	return ([width,depth,height,m1,m2,m3,m4,m5,m6,m7,m8,m9])

def subMatrix( matrix, startRow, startCol, xSize,ySize): #FROM https://stackoverflow.com/questions/36692484/python-extracting-a-smaller-matrix-from-a-larger-one
	#This function is used a lot to analyse a part of a larger matrix - so it allows to look at where a brick is  being placed in the build matrix 
	x = numpy.array(matrix)
	return x[startRow:startRow+xSize,startCol:startCol+ySize]

def checkResultOfMatixAdditionToAllowForUplift(passLayerMatrix,brickMatrix,x,y,xSize,ySize,fileName,dateTimeStamp):
	#This checks that the when bricks are added at the same height (so they don't step or stagger across the matrix)
	listToReturn = []
	print ("brickMatrix")
	print (brickMatrix)
	print ("Checking for brick uplift")
	checkBrickMatrix = subMatrix(passLayerMatrix,y,x,ySize,xSize)
	print (checkBrickMatrix)
	maxMatrixValue = numpy.max(checkBrickMatrix)
	print (maxMatrixValue)
	if numpy.all(maxMatrixValue == checkBrickMatrix):
		print ("No uplift needed")
	else:
		print ("UPLIFTING BRICK...")
		correctionMatrix = layerMatrix(ySize,xSize,False,maxMatrixValue)
		print (correctionMatrix)
		passLayerMatrix[y:y+ySize,x:x+xSize] = correctionMatrix
		print (passLayerMatrix)
	#Get brick dimensions from matrix
	brickDetails = getBrickDimensionsFromMatrix(brickMatrix,fileName,dateTimeStamp)
	listToReturn.extend((passLayerMatrix,brickDetails))
	#print (listToReturn)
	#input() #Check that bricks have been "uplifted correctly"
	return listToReturn

def getAvailableFonts(selectedFont):
	dictionaryOfFontsToFind = {
	"missing.ttf":"Missing Font",	
	"arial.ttf":"Arial",
	"ariblk.ttf":"Arial Black",
	"arialbi.ttf":"Arial Bold Italic",
	"BrushScriptStd.otf":"Brush Script",
	"comicbd.ttf":"Comic Sans",
	"COOPBL.TTF":"Cooper Black",
	"courbd.ttf":"Courier Bold",
	"timesbd.ttf":"Times Bold",
	"wingding.ttf":"Wingdings"
	}
	if selectedFont == '':
		selectedFont = confirmFontExists(dictionaryOfFontsToFind)
	return ([selectedFont,dictionaryOfFontsToFind])

def confirmFontExists(dictionaryOfFontsToFind):
	listFromFontDictionary = list(dictionaryOfFontsToFind.keys())
	pathToFonts = 'C://Windows//Fonts//'
	availableFonts=[]
	for font in listFromFontDictionary:
		fontPath = pathToFonts + font
		if os.path.exists(fontPath):
			fontName = dictionaryOfFontsToFind.get(font)
			print ("Found Font: ",fontName)
			#input("Found Font")
			availableFonts.append(fontName)
		else:
			fontName = dictionaryOfFontsToFind.get(font)
			print (fontName)
			print("Font not available")
	#print (availableFonts)
	availableFonts.append("--- Enter Your Own Font ---")
	selectedFont = chooseFont(availableFonts)
	if selectedFont == "--- Enter Your Own Font ---":
		print ("Enter the name of your font as a .ttf file name")
		inputType = "font name"
		fontName = getUserTextInput(inputType)
		selectedFont = checkFontExists(fontName,pathToFonts)
	else:
		selectedKey = next(key for key, value in dictionaryOfFontsToFind.items() if value == selectedFont)
		selectedFont = selectedKey
	return(selectedFont)

def checkFontExists(fontName,pathToFonts):
	fontPath = pathToFonts + fontName
	inputType = "font name"
	while True:
		fontPath = pathToFonts + fontName
		if os.path.exists(fontPath) and fontName !='':
			print ("Found User Font: ",fontName)
			#input("Found Font")
			break
		else:
			print()
			print("FONT NOT AVAILABLE")
			print()
			print ("Enter the name of your font as a .ttf file name - Enter Q to quit")
			fontName = getUserTextInput(inputType)
			if fontName == "q" or fontName == "Q" or fontName == "Quit":
				print ("Exiting...")
				sys.exit(0)
			#print (fontName)
			fontName = checkFontExists(fontName,pathToFonts)
	return(fontName)

def chooseFont(availableFonts):
	print()
	print("Choose A Font:")
	numberChosen,selectedItem,skipWhileLoop = chooseItem(availableFonts)
	return(selectedItem)

'''
def userFont(inputType):
	print ("Enter the name of your font as a .ttf file name")
	fontName = getUserTextInput(inputType)
'''

def getFontSize():
	fontSize = [12,14,16,20,24,28,32]
	numberChosen,selectedItem,skipWhileLoop = chooseItem(fontSize)
	return(selectedItem)

def getBrickSizes():
	brickSizeDictionaryKeysList=[]
	plateSizeDictionaryKeysList=[]
	print("Getting availale bricks...")
	partID = "1,1,1"
	brickSelection,brickDimensionListAsString = brickPartDictionary(partID)
	print (brickDimensionListAsString)
#	input("Wait")

	brickDimensionList = csv.reader(brickDimensionListAsString)
	brickDimensionList = list(brickDimensionList)
	#brickDimensionList.reverse()
	print (brickDimensionList)
	print()
	for brickDimension in brickDimensionList:
		dimension = int(brickDimension[0])*int(brickDimension[1])
		density = dimension * int(brickDimension[2])
		#print(dimension,density)
		if int(brickDimension[2]) == 3: #Bricks
			brickSizeDictionaryKeysList.append(dimension)
		else: #Plates
			plateSizeDictionaryKeysList.append(dimension)
	brickSizeDictionary = dict(zip(brickSizeDictionaryKeysList, brickDimensionListAsString))
	plateSizeDictionary = dict(zip(plateSizeDictionaryKeysList, brickDimensionListAsString))
	print (brickSizeDictionary)
	print (plateSizeDictionary)
	getSortedBrickMatrix(plateSizeDictionary)
	input("Wait")
	

def getSortedBrickMatrix(plateSizeDictionary):
	d = plateSizeDictionary
	sortedDictionary = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]

	#for key in sorted(plateSizeDictionary).reverse():
	print (sortedDictionary)

def brickPartDictionary(partID):
	print("Getting Brick Part...",partID)
	#brickParts 
	#1x1 PLATE 30008.dat	#1x2 PLATE 6225.dat	#1x3 3623.DAT	#1x4 3710.DAT	#2x2 PLATE 3022.dat		#2x3 3021.DAT	#2x4 3020.DAT
	#1x1 BRICK 30071.dat 	#1x2 BRICK 3004.dat #1x3 3622.DAT	#1x4 3010.DAT	#2x2 BRICK 3003.dat		#2x3 3002.DAT	#2x4 3001.DAT
	brickDictionary = {               					#[xSize,ySize,height][BrickShapes]
		'1,1,1':["30008.dat","30057.dat"],					#1x1 plates
		'1,2,1':["6225.dat"],								#1x2 plates
		'1,3,1':["3623.dat"],								#1x3 plates
		'1,4,1':["3710.dat"],								#1x4 plates
		'2,2,1':["3022.dat"],								#2x2 plates
		'2,3,1':["3021.dat"],								#2x3 plates
		'2,4,1':["3020.dat"],								#2x4 plates
		'1,1,3':["30071.dat","30068.dat"],							#1x1 bricks
		'1,2,3':["30136.dat","98283.dat","2877.dat","3004.dat"],	#1x2 bricks
		'1,3,3':["3622.dat"],										#1x3 bricks
		'1,4,3':["3010.dat"],										#1x4 bricks
		'2,2,3':["3003.dat"],										#2x2 bricks
		'2,3,3':["3002.dat"],										#2x3 bricks
		'2,4,3':["3001.dat"]										#2x4 bricks
		}
	brickOptions = brickDictionary.get(partID)
	brickDemensionList = list(brickDictionary.keys())
	if len(brickOptions)>1:
		print (len(brickOptions),brickOptions)
		randomBrick = randint(0,len(brickOptions)-1) #Because lists start at 0 but len counts from 1!
		brickSelection = brickOptions[randomBrick]
	else:
		brickSelection = brickOptions[0]
	return ([brickSelection,brickDemensionList])

def getBrickDimensionsFromMatrix(brickMatrix,fileName,dateTimeStamp):
	brickDetails = []
	rotate = 0
	ySize, xSize = brickMatrix.shape
	print (brickMatrix)
	if xSize > ySize:
		rotate = 1
		partID = [ySize,xSize]
	else:
		partID = [xSize,ySize]
	if numpy.all(brickMatrix == 1):
		part = "PLATE"
		partID.append(1)
	else:
		part = "BRICK"
		partID.append(3)
	print (partID,rotate) #This is what you need to return ([x,y,height],rotate)
	partID = ','.join(map(str, partID)) 
	partID,brickDemensionList = brickPartDictionary(partID)

	brickDetails.extend((xSize,ySize,partID,rotate))
	print (brickDetails)
	return brickDetails

def calculateXYBasedOnBrickShape(brickMatrix,layerMatrix): #not used in this code
	#This function ensures that bricks do not spill over the edge of the base matrix bay calculating the size of the brick and then adjusting the random positioning accordingly.
	yBrickSize, xBrickSize = brickMatrix.shape
	yLayerSize, xLayerSize = layerMatrix.shape
	maxX = xLayerSize - xBrickSize
	maxY = yLayerSize - yBrickSize
	posX = randint(0,maxX)
	posY = randint(0,maxY)
	return (posX,posY)

def getColoursFromUser(colourListOnly):
	colour,colourList = selectColourAndHues("Greys",False)
	colourList.append("Random Colours")
	if colourListOnly: #used to get colourlist only
		hue = colour
	else:
		print()
		print("Now choose a colour...")
		numberChosen,hue,skipWhileLoop = chooseItem(colourList)
	return([hue,colourList])


def getLettersFromUser():		
	textToCreate = getUserTextInput("letters")
	if textToCreate == "":
		print("Er, OK - we\'ll use the word \"Lego\" then!")
		textToCreate = "Lego"
	return(textToCreate)

'''
def buildLetterLayer(textToCreate,selectedFont,fontSize):
	fullPathToFont = 'C://Windows//Fonts//' + selectedFont
	#letterLayerMatrix = char_to_pixels(textToCreate, path=selectedFont, fontsize=14)
	letterLayerMatrix = char_to_pixels(textToCreate, path=selectedFont, fontsize=fontSize)
	return (layerLetterMatrix)
'''
def getFinalConfirmation():
	finalConfirmation = input("Like what you see? Press enter to continue...Any other key to start again - Type Q to quit: ")
	if finalConfirmation == "q" or finalConfirmation == "Q":
		sys.exit(0)
	elif finalConfirmation !='':
		print ("Reloading...")
		execfile("LegoLetters.py")
		sys.exit()


def createModelLayerDescription(fileName,dateTimeStamp,buildHeight,maxHeight,selectedFont,fontSize,textToCreate,hue,colourList,layerStudCount,maxLayerCount):
	#This does the heavy lifting of adding brcks to the model
	#layerStudCount = 0 #Count the studs added to each Layer
	layerCount = 0
	maxLayerCount = int(maxLayerCount)*2 #To adjust for a mixture of plates and bricks
	brickStage = 4
	try:
		buildHeight = int(buildHeight)
	except:
		buildHeight = 2
	useRandomLayer = 0	#0 for letters, 1 for random, 2 for solid layer
	#PART ONE
	if useRandomLayer == 1 or useRandomLayer == 2:
		buildBaseY = 8
		buildBaseX = 8
		letterLayerMatrix = randomLayer(buildBaseX,buildBaseY,useRandomLayer)
	else:
		fullPathToFont = 'C://Windows//Fonts//' + selectedFont
		letterLayerMatrix = char_to_pixels(textToCreate, path=selectedFont, fontsize=fontSize)
	buildBaseX,buildBaseY = letterLayerMatrix.shape
	display(letterLayerMatrix)
	getFinalConfirmation()
	#Set up the base layer and the first brick
	totalStudCount = numpy.count_nonzero(letterLayerMatrix)
	height = 1 # This is the first layer
	#if height == 1:
	maxHeight = buildHeight
	heightApproximation = height
	modelLayerDescription = []
	#Set up initial base layer matrix and add to modelLayerDescription
	baseMatrix = layerMatrix(buildBaseX,buildBaseY,False,height)
	appendLayerMatrix = deepcopy(baseMatrix)
	modelLayerDescription.append(appendLayerMatrix)

	#Get a random brick matrix
	brickMatrix = getBrickMatrix()
	print (baseMatrix)
	print (brickMatrix)
	
	#Add the base matrix and the brick matrix together and add to modelLayerDescription
	layerStudCount,newLayerMatrix = addAtPos(baseMatrix,brickMatrix,fileName,dateTimeStamp,maxHeight,letterLayerMatrix,heightApproximation,totalStudCount,hue,textToCreate,layerStudCount)
	appendLayerMatrix = deepcopy(newLayerMatrix)
	modelLayerDescription.append(appendLayerMatrix)
	#print (appendLayerMatrix)

	#PART TWO
	#Add more layers to modelLayerDescription
	#for i in range(1,buildHeight):
	while True:
		brickMatrix = getBrickMatrix()
		#print(brickMatrix,"\n",i,"\n",letterLayerMatrix)
		if useRandomLayer == 1:#Get a new random layer to see what happens to the density
			letterLayerMatrix = randomLayer(buildBaseX,buildBaseY,1)
		layerStudCount,newLayerMatrix = addAtPos(newLayerMatrix,brickMatrix,fileName,dateTimeStamp,maxHeight,letterLayerMatrix,heightApproximation,totalStudCount,hue,textToCreate,layerStudCount)
		appendLayerMatrix = deepcopy(newLayerMatrix)
		modelLayerDescription.append(appendLayerMatrix)
		if layerStudCount >= totalStudCount:
			layerStudCount = 0
			layerCount = layerCount + 1
			print("Layer",layerCount," is complete")
			if layerCount >= maxLayerCount:
				break
			#input("Press enter to continue")

		#print (newLayerMatrix)
		#if exitLoop:
		#	input("breaking out of second loop")
		#	break
	print()
	#Show each brick layer in modelLayerDescription
	modelLayerDescription,maxHeight = buildLayer3DMatrix(modelLayerDescription,fileName,dateTimeStamp,maxHeight)	
	return (modelLayerDescription,maxHeight,brickStage,textToCreate)

def buildLayer3DMatrix(modelLayerDescription,fileName,dateTimeStamp,maxHeight):	
	tmpModelLayerDescription = []
	layer3DMatrix = numpy.dstack(modelLayerDescription)
	print ("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
	widthOfMatrix = layer3DMatrix.shape[0]
	depthOfMatrix = layer3DMatrix.shape[1]
	heightOfMatrix = layer3DMatrix.shape[2]
	print("Analysing Layers for Tiling Matrix - Default = 2: ",heightOfMatrix,"Please wait...")

	for z in range(0,heightOfMatrix):#Print layer slices
		#print(layer3DMatrix[:, :, z])
		#print("Adding to list")
		#print (tmpModelLayerDescription)
		try:
			layer3DMatrix[:, :, z+1]
			#print(layer3DMatrix[:, :, z+1]) # Layer slice
		except:
			print ("Top Layer reached (1)...")
			print ("Calculating Studs For Tiling Matrix - Please wait...")
		
		#print ("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
		for x in range(0,widthOfMatrix):
			for y in range(0,depthOfMatrix):
				sliceValue = layer3DMatrix[x,y,z]
				#print ("sliceValue,x,y,z: ",sliceValue,x,y,z)
				try:
					for zColumn in range(z+1,heightOfMatrix):
						nextLayerSliceValue = layer3DMatrix[x,y,zColumn]
						#print ("nextLayerSliceValue,x,y,zColumn: ",nextLayerSliceValue,x,y,zColumn)
						if sliceValue == nextLayerSliceValue:
							#print ("Matching next layer - Zeroing out next layer...")
							layer3DMatrix[x,y,zColumn]=0
						elif ((nextLayerSliceValue - sliceValue) == 1) or ((nextLayerSliceValue - sliceValue) == 3): # Catch plates and bricks
							#print (nextLayerSliceValue,sliceValue)
							#print ("Value 1 or 3 less than subsequent layer - Zeroing out current layer...")
							layer3DMatrix[x,y,z]=0
						elif (z == 0 and nextLayerSliceValue == 2) or (z == 0 and nextLayerSliceValue == 4):	
							#print ("Fixing first layer...")
							#print ("sliceValue,x,y,z: ",sliceValue,x,y,z)
							#print ("nextLayerSliceValue,x,y,zColumn: ",nextLayerSliceValue,x,y,zColumn)
							layer3DMatrix[x,y,0]=0
							#print (layer3DMatrix[x,y,z])
							#print(layer3DMatrix[:, :, ])
							#input()
						#print(layer3DMatrix[:, :, z])
						#print(layer3DMatrix[:, :, z+1])
						#input()
				except:
					print ("Top Layer reached (2)...")
			#input()
		#print("Adding to list")
		layerSliceFrom3DMatrix = deepcopy(layer3DMatrix[:, :, z])
		tmpModelLayerDescription.append(layerSliceFrom3DMatrix)
		#print (tmpModelLayerDescription)
	print("****************************************")
	tmpLayer3DMatrix = numpy.dstack(tmpModelLayerDescription)
	for z in range(0,heightOfMatrix):
		#print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
		#print(tmpLayer3DMatrix[:, :, z]) #Stud checking
		#input()
		for x in range(0,widthOfMatrix):
			for y in range(0,depthOfMatrix):
				sliceValue = tmpLayer3DMatrix[x,y,z]
				#print ("sliceValue,x,y,z: ",sliceValue,x,y,z)
				try:
					for zColumn in range(z+1,heightOfMatrix):
						nextLayerSliceValue = tmpLayer3DMatrix[x,y,zColumn]
						if sliceValue>1 and nextLayerSliceValue > 1:
							print("Found part above at: ",x,y,z,nextLayerSliceValue)
							maxHeight = nextLayerSliceValue
				except:
					print ("Top Layer reached (2)...")
	try:			
		print (maxHeight)
	except:
		maxHeight = heightOfMatrix
	#input() #THIS ONE
	return (tmpModelLayerDescription, maxHeight)

def activeLine(active,colour,width,height,depth,m1,m2,m3,m4,m5,m6,m7,m8,m9,partID):
	#1 69 -20 -24 -20 0 0 1 0 1 0 -1 0 0 3003.dat
	active = str(active)
	colour = str(colour)	
	width = str(width)
	height = str(height)
	depth = str(depth)
	m1 = str(m1);m2 = str(m2);m3 = str(m3);m4 = str(m4);m5 = str(m5);m6 = str(m6);m7 = str(m7);m8 = str(m8);m9 = str(m9)
	ldrLine = active + " " + colour + " " + width + " " + height+ " " + depth  + " " + m1 + " " + m2 + " " + m3 + " " + m4 + " " + m5 + " " + m6 + " " + m7 + " " + m8 + " " + m9 + " " + partID
	return ldrLine

def resetldrFile(fileName):	
	fileName = fileName
	LDrawFile = open(fileName, 'w').close()
	LDrawFile = open(fileName, 'w')
	LDrawFile.write('0 // Name: '+ fileName +'\n')
	LDrawFile.write('0 // Author:  BRICKALO ' + dateTimeStamp +'\n')
	#LDrawFile.write('1 7 0 0 0 0 0 1 0 1 0 -1 0 0 3031.dat'+'\n') #ADD 4x4 BASE PLATE
	###LDrawFile.write('1 7 40 0 40 0 0 1 0 1 0 -1 0 0 42534.dat'+'\n') #ADD 8x8 BASE PLATE
	#LDrawFile.write('1 4 30 0 30 0 0 1 0 1 0 -1 0 0 6141.dat'+'\n') #ADD 4x4 MARKER STUD
	###LDrawFile.write('1 4 110 0 110 0 0 1 0 1 0 -1 0 0 6141.dat'+'\n') #ADD 8x8 MARKER STUD
	LDrawFile.write('0 STEP\n')
	LDrawFile.write('0 STEP\n')
	#LDrawFile.write(ldrLine)

	
def legoWriter(fileName,dateTimeStamp,ldrLine):
	null = 0
	#print ( fileName)
	if os.path.isfile(fileName): 
		LDrawFile = open(fileName, 'a')
		LDrawFile.write('\n0 STEP\n')
		LDrawFile.write(ldrLine)
	else:
		#Adding base and marker	- NOT USED - see resetldrFile()
		LDrawFile = open(fileName, 'w')
		LDrawFile.write('0 // Name: '+ fileName +'\n')
		LDrawFile.write('0 // Author:  BRICKALO ' + dateTimeStamp +'\n')
		#LDrawFile.write('1 7 0 0 0 0 0 1 0 1 0 -1 0 0 3031.dat'+'\n')
		LDrawFile.write('1 4 30 0 30 0 0 1 0 1 0 -1 0 0 6141.dat'+'\n')
		LDrawFile.write('0 STEP\n')
		LDrawFile.write(ldrLine)
	return fileName

def slopingRoofTile(width, height, depth,colour,maxHeight,brickHeight):
		height = height + 8
		i = randint(1,3)
		if i == 1:
			slopingRoofTiles = "1 " + str(colour) + " " + str(width) +" " + str(height) +" " + str(depth) + " 1 0 0 0 1 0 0 0 1 50746.dat"
		elif i == 2:
			slopingRoofTiles = "1 " + str(colour) + " " + str(width) +" " + str(height) +" " + str(depth) + " 0 0 1 0 1 0 -1 0 0 50746.dat"
		else:
			slopingRoofTiles = "1 " + str(colour) + " " + str(width) +" " + str(height) +" " + str(depth) + " -1 0 0 0 1 0 0 0 -1 50746.dat"
		print (slopingRoofTiles)
		return slopingRoofTiles

def getLineHeight(ldrLine):
	splitLine = ldrLine.split()
	lineHeight = splitLine[3] 
	print ("Line Height:",lineHeight)

def editCurrentLine(currentLine,adjustedheight): #NOT USED IN THIS CODE
	splitLine = currentLine.split()
	print ( "====================================")
	print ( "OLD Current Line ",splitLine)	
	splitLine[3] = (adjustedheight-1)*-8 #To keep the number negative if it already was.
	#To Change Brick Colours to Rainbow Colours use the next line
	splitLine[1] = colourChanger(splitLine[3])
	print ( "NEW Current Line ",splitLine)
	print ( "====================================")
	return splitLine	

def deleteLastLineOfLdrFile(fileName): #NOT USED IN THIS CODE
	readFile = open(fileName)
	lines = readFile.readlines()
	readFile.close()
	w = open(fileName,'w')
	w.writelines([item for item in lines[:-1]])
	w.close()
		
def upadteLastLine(line,item,height,maxValue): #NOT USED IN THIS CODE
	splitLine = line.split()
	print ( "====================================")
	print ( "OLD splitLine",splitLine)
	datFile = splitLine[item]
	splitLine[3] = (maxValue-1)*-8 #To keep the number negative if it already was.
	print ( "NEW splitLine",splitLine)
	print ( "datFile",datFile)
	print ( "====================================")
	return splitLine	

def readAndModifyLastLineOfLDRFile(fileName,height,maxValue): #From https://stackoverflow.com/questions/327985/how-do-i-modify-the-last-line-of-a-file #NOT USED IN THIS CODE
	myFile = fileName
	# read the file into a list of lines
	lines = open(myFile, 'r').readlines()
	# now edit the last line of the list of lines
	oldLastLine = lines[-1]
	newLastLineList = upadteLastLine(oldLastLine,3,height,maxValue)
	newLastLine = " ".join(str(e) for e in newLastLineList)
	print ( "^^^^^^^^^^^^^^^^^^^","LDR LINE UPDATE","^^^^^^^^^^^^^^^^^^^")
	print ( "oldLastLine",oldLastLine)
	print ( "newLastLine",newLastLine)
	print ( "^^^^^^^^^^^^^^^^^^^")
	lines[-1] = newLastLine
	# now write the modified list back out to the file
	if "41539.dat" not in oldLastLine:
		open(myFile, 'w').writelines(lines)	

def readLastLineOfLDRFile(fileName): #From https://stackoverflow.com/questions/327985/how-do-i-modify-the-last-line-of-a-file #NOT USED IN THIS CODE
	myFile = fileName
	# read the file into a list of lines
	lines = open(myFile, 'r').readlines()
	# now edit the last line of the list of lines
	oldLastLine = lines[-1]
	print ( "^^^^^^^^^^^^^^^^^^^","LDR LINE UPDATE","^^^^^^^^^^^^^^^^^^^")
	print ( "oldLastLine",oldLastLine)
	print ( "^^^^^^^^^^^^^^^^^^^")

'''
def addTiles(fileName,dateTimeStamp,modelLayerDescription,maxHeight,brickStage): #CURRENTLY NOT USED 
	input("Press Enter to add tiles...")
	placeStud(fileName,dateTimeStamp,modelLayerDescription,maxHeight,brickStage,hue)#Adds tiles to the models
	input("Press Enter to Finish")
	sys.exit()
'''

def placeStud(fileName,dateTimeStamp,modelLayerDescription,maxHeight,brickStage,textToCreate,hue):
	##############################################################
	print (maxHeight)
	#input()
	for index,eachLayerMatrix in enumerate(modelLayerDescription):
		#Cut off the overscan if there is any...
		#eachLayerMatrix = subMatrix(eachLayerMatrix,1,1,4,4)
		#Orientate the matrix correctly
		#eachLayerMatrix = numpy.rot90(eachLayerMatrix,3)
		print("====================================================")
		
		if index > 0:
			print ("Previous")
			#previousElement = subMatrix(modelLayerDescription[index - 1],0,0,4,4)
			previousElement = modelLayerDescription[index - 1]
			#previousElement = numpy.rot90(previousElement,3)
			#print(previousElement)
		else:
			print("First Layer so skipping previous layer...")
			#print (eachLayerMatrix)
		print("Current")
		#print (eachLayerMatrix)
		try:
			print ("Next")
			#nextElement = subMatrix(modelLayerDescription[index + 1],0,0,4,4)
			nextElement = modelLayerDescription[index + 1]
			#nextElement = numpy.rot90(nextElement,3)
			#print(nextElement)
		except:
			print("Last Layer Skipping so skipping next layer...")	
		print("====================================================")
		#input()
		#print (eachLayerMatrix)
		rows = eachLayerMatrix.shape[0]
		cols = eachLayerMatrix.shape[1]
		for x in range(0, rows):
			for y in range(0, cols):
				if eachLayerMatrix[x,y] > 0: #Deal with Tiles - not working
					#print (x,y,eachLayerMatrix[x,y])
					width = (x * 20)-30
					height = (eachLayerMatrix[x,y]*-8)
					depth = (y * 20)-30
					#colour = 69 #PINK
					if brickStage != 3:
						brickStage = 2
					#if textToCreate == "Lego": #Use for Lego Logo
					#	brickStage = 8	#Use for Lego Logo
					#colour = colourMeBrick((height/-8),brickStage,maxHeight)
					if hue == "Random Colours":
						colour = randomColour()
					else:
						colour = selectColour(hue)
					tileSelector = randint(0,30)
					if tileSelector > 1:
						partID = "30039.dat" #Square
					else:
						partID = "98138.dat" #Round
					print ("height and maxHeight",(height / -8),maxHeight)
					
					#if (height / -8) < (maxHeight) and height / -8 > 1:
					if height / -8 > 1:
						ldrLine = activeLine(1, colour, width, height, depth, 0, 0, 1, 0, 1, 0, -1, 0, 0,partID)
					#else: #FOR TILING GROUND PLANE
						#if textToCreate == "Lego": #Use for Lego Logo
						#	brickStage = 9 #Use for Lego Logo
						#colour = colourMeBrick((height/-8),brickStage,maxHeight)
						#ldrLine = slopingRoofTile(width, height, depth,colour,maxHeight,brickStage)
						#ldrLine = activeLine(0, colour, width, height, depth, 0, 0, 1, 0, 1, 0, -1, 0, 0,partID)
					try:
						legoWriter(fileName,dateTimeStamp,ldrLine)
					except:
						print("Not tilling ground plane...")
					#input()

def tileTheTop(configFileName):
	userInput = input("Would you like to tile the top of your letters? - Press Enter to tile the top or any other key to exit: ")
	if userInput == "":
		tileTop = True
		print ("Choose a colour for your tiles")
		hue,colourList = getColoursFromUser(False)
		#Append data to config file
		lineToAppend = str(tileTop) + "\n" + str(hue) + "\n"
		appendLinesToConfigFile(configFileName,lineToAppend) 
	else:
		tileTop = False
		hue = 0
		colourList = []	
		lineToAppend = str(tileTop) + "\n" + "Greys" + "\n"
		appendLinesToConfigFile(configFileName,lineToAppend)
	return([tileTop,hue,colourList])

def appendLinesToConfigFile(configFileName,lineToAppend):
	with open(configFileName, "a") as configFile:
		configFile.write(lineToAppend)

def listToFile(fileName,listOfItems):
	print ("Writing Config Data...")
	with open(fileName, 'w') as f:
		#f.write(header)
		for item in listOfItems:
			f.write("%s\n" % item)

def checkConfigFile (fileName):
	if os.path.exists(fileName):
		configExists = True
		print ("Found Configuration File...")
		print()
	else:
		configExists = False
	return(configExists)	

def fileToList(fileName):
	configExists = checkConfigFile(fileName)
	if configExists:
		print("Reading Config Data...")
		with open(fileName) as f:
			content = f.readlines()
			# you may also want to remove whitespace characters like `\n` at the end of each line
			content = [x.strip() for x in content] 
	else:
		content = []
	return ([configExists,content])			

def getConfigData(configData,skipWhileLoop):
		#Assign Letters
		textToCreateForList = "Your Letters Are: \"" + configData[0] +"\""
		textToCreate = configData[0]
		#Assign Font
		selectedFont,dictionaryOfFontsToFind = getAvailableFonts(configData[1])
		fontName = dictionaryOfFontsToFind.get(configData[1])
		selectedFontForList = "Your Font Is: " + fontName
		selectedFont = configData[1]
		#Assign Font Size
		fontSizeForList = "The Font Size Is: " + configData[2]
		fontSize = int(configData[2])
		#Assign Colours
		hue,colourList = getColoursFromUser(True)
		hueForList = "The Colour Selection Is: " + configData[3]
		hue = configData[3]
		#Assign the build height
		buildHeightForList = "The APPROXIMATE Height Of The Letters (In Bricks) Is: " + configData[4]
		buildHeight = int(configData[4])
		try: #Beacuse its possible for the 5 and 6 lines of the file not to be present (as these are added after the letters are initially created)
			tileOn = configData[5]
			if tileOn == "True":
				tileOn = True
			else:
				tileOn = False
			tileOnForList = "Tile The Top Of The Letters: " + configData[5]
			tileColour = (configData[6])
			tileColourForList = "Colours Of Top Tile: " + configData[6]
			#input("Try")
		except:
			tileOn = False
			tileOnForList = "Tile the top: " + str(tileOn)
			tileColour = True #Use this to exit out of adding the tiles after the letters have been built
			tileColourForList = "Colour Of Top Tile: None"
			#input("Except")
		#Build the list for the user
		listOfConfigItems = [textToCreateForList,selectedFontForList,fontSizeForList,hueForList,buildHeightForList,tileOnForList,tileColourForList]
		if not skipWhileLoop:
			numberChosen,itemToEdit,skipWhileLoop = chooseItem(listOfConfigItems)
			textToCreate,selectedFont,fontSize,hue,colourList,buildHeight,tileOn,tileColour,skipWhileLoop = editConfigData(configFileName,numberChosen,configData,colourList,skipWhileLoop)
		else:
			null = 0
			#print("exiting...")
		#input([numberChosen,itemToEdit])
		#Add edit items here...
		#input("Wait For Confirmation...")
		return([textToCreate,selectedFont,fontSize,hue,colourList,buildHeight,tileOn,tileColour,skipWhileLoop])

def editConfigData(configFileName,itemToEdit,listOfConfigItems,colourList,skipWhileLoop):
	textToCreate = listOfConfigItems[0]
	selectedFont = listOfConfigItems[1]
	fontSize = listOfConfigItems[2]
	hue = listOfConfigItems[3]
	buildHeight = listOfConfigItems[4]
	try:
		tileOn = listOfConfigItems[5]
	except:
		tileOn = False
	try:
		tileColour = listOfConfigItems[6]
	except:
		tileColour = True	
	if itemToEdit == 0: #Text to create
		lineData = getUserData_textToCreate()
		buildDataForLineUpdate(configFileName,lineData,itemToEdit)
	elif itemToEdit == 1: #Selected Font
		lineData,dictionaryOfFontsToFind = getUserData_selectedFont()
		buildDataForLineUpdate(configFileName,lineData,itemToEdit)
	elif itemToEdit == 2: # Font Size
		lineData = getUserData_fontSize()
		buildDataForLineUpdate(configFileName,lineData,itemToEdit)
	elif itemToEdit == 3: # Hue
		lineData,colourList = getUserData_hue()
		buildDataForLineUpdate(configFileName,lineData,itemToEdit)
	elif itemToEdit == 4: # Build Height
		lineData = getUserData_buildHeight()
		buildDataForLineUpdate(configFileName,lineData,itemToEdit)
	elif itemToEdit == 5: # Add Tiles
		lineData = getUserData_tileOn()
		buildDataForLineUpdate(configFileName,lineData,itemToEdit)
	elif itemToEdit == 6: # TileColours
		lineData,colourList = getUserData_tileColour()
		buildDataForLineUpdate(configFileName,lineData,itemToEdit)
	#Reread the config file...
	configExists,configData = fileToList(configFileName)
	while not skipWhileLoop:
		textToCreate,selectedFont,fontSize,hue,colourList,buildHeight,tileOn,tileColour,skipWhileLoop = getConfigData(configData,skipWhileLoop)
		if skipWhileLoop:
			#print ("Reloading modified config data")
			configExists,configData = fileToList(configFileName)
			#print("*** PRESS ENTER TO PROCEED ***")
			textToCreate,selectedFont,fontSize,hue,colourList,buildHeight,tileOn,tileColour,skipWhileLoop = getConfigData(configData,skipWhileLoop)
			break
	return([textToCreate,selectedFont,int(fontSize),hue,colourList,int(buildHeight),tileOn,tileColour,skipWhileLoop])

def buildDataForLineUpdate(configFileName,lineData,lineNumber):
	lineData = str(lineData) + "\n"
	updateLineInConfigFile(configFileName,lineData,lineNumber)

def updateLineInConfigFile(configFileName,lineData,lineNumber): #From https://stackoverflow.com/questions/4719438/editing-specific-line-in-text-file-in-python
	with open(configFileName, 'r') as file:
		# read a list of lines into data
		data = file.readlines()
	# now change the 2nd line, note that you have to add a newline
	data[lineNumber] = lineData
	# and write everything back
	with open(configFileName, 'w') as file:
		file.writelines( data )

def getUserData():
	textToCreate = getUserData_textToCreate()
	selectedFont,dictionaryOfFontsToFind = getUserData_selectedFont()
	fontSize = getUserData_fontSize()
	hue,colourList = getUserData_hue()
	buildHeight = getUserData_buildHeight()
	writeOutUserDataToConfigFile(configFileName,textToCreate,selectedFont,fontSize,hue,buildHeight)
	return([textToCreate,selectedFont,fontSize,hue,colourList,buildHeight])

def getUserData_textToCreate():
	textToCreate = getLettersFromUser()
	return(textToCreate)

def getUserData_selectedFont():
	selectedFont,dictionaryOfFontsToFind = getAvailableFonts('')
	return(selectedFont,dictionaryOfFontsToFind)

def getUserData_fontSize():
	fontSize = getFontSize()
	return(fontSize)

def getUserData_hue():
	hue,colourList = getColoursFromUser(False)
	return(hue,colourList)

def getUserData_tileColour():
	hue,colourList = getColoursFromUser(False)
	return(hue,colourList)


def getUserData_buildHeight():
	#NEEDS CHECKING
	while True:
		buildHeight = input("APPROXIMATLEY How High Do You Want The Letters (in brick height)? ")
		try:
			int(buildHeight)
			if int(buildHeight) < 1 or int(buildHeight) > 10:
				print ("That is not a valid number - enter a value between 1 and 10")
			else:
				break
		except: 
			print ("That is not a valid number - enter a value between 1 and 10")
	return(buildHeight)

def getUserData_tileOn():
	print ("Do You Want To Add Tiles On Top Of Your Letters? ")
	tileOn = getTileOnFromUser()
	if tileOn == "YES":
		tileOn = True
	else:
		tileOn = False
	return(tileOn)

def getTileOnFromUser():
	tileOn = ["YES","NO"]
	numberChosen,selectedItem,skipWhileLoop = chooseItem(tileOn)
	return(selectedItem)

def writeOutUserDataToConfigFile(configFileName,textToCreate,selectedFont,fontSize,hue,buildHeight):
	configData = [textToCreate,selectedFont,fontSize,hue,buildHeight]
	listToFile(configFileName,configData)



if __name__ == "__main__":
	#test()
	print("====================================================")
	
	configFileName = "configData.txt"

	#TESTING FUNCTIONS AREA
	#Tesing colours and hues
	#selectColourAndHues("Blues") #Colour hue selector
	#tileTheTop(configFileName)
	#input("STOP")

	configExists,configData = fileToList(configFileName)
	if configExists:
		textToCreate,selectedFont,fontSize,hue,colourList,buildHeight,tileOn,tileColour,skipWhileLoop = getConfigData(configData,False)
	else:
		#Get User Input
		textToCreate,selectedFont,fontSize,hue,colourList,buildHeight = getUserData()
		tileOn = False
		tileColour = False

	#maxLayerCount = buildHeight
	layerStudCount = 0
	print("====================================================")
	#input (selectedFont)
	#getBrickSizes()
	

	dateTimeStamp = timeStamp()
	fileName = textToCreate + "_" + dateTimeStamp + ".ldr"
	#fileName = "tester.ldr"
	resetldrFile(fileName)
	
	#maxHeight = buildHeight

	#Set up the model layer discription
	modelLayerDescription,maxHeight,brickStage,textToCreate = createModelLayerDescription(fileName,dateTimeStamp,buildHeight,buildHeight,selectedFont,fontSize,textToCreate,hue,colourList,layerStudCount,buildHeight)
	#Add tiles or not...
	if tileOn: #Read the config data for tiling
		placeStud(fileName,dateTimeStamp,modelLayerDescription,buildHeight,brickStage,textToCreate,tileColour)#Adds tiles to the models
	elif not tileOn and tileColour: #So it has read the value tileOn from the Config file (which always sets tileColur to True if tileOn is False)
		print("Letters complete - No Tiles Applied - Bye")
	else:	
		tileTop,hue,colourList = tileTheTop(configFileName)
		if tileTop:
			placeStud(fileName,dateTimeStamp,modelLayerDescription,buildHeight,brickStage,textToCreate,hue)#Adds tiles to the models
		else:
			print("Letters complete - No Tiles Applied - Bye")
	#input()
else:
	print ( ("...being imported into another module"))

