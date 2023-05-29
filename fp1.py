from PIL import Image
import numpy as np

# Modifies the received array of pixels [(r,g,b,brightness),...]
# to make it look like a chess table
def chessTable(sqOgLength, sqOgWidth, array, width, length):
    
    if (sqOgLength>width or sqOgWidth > length):
        return

    
    columnsOfSquares =(width//sqOgWidth)+1
    rowsOfSquares = (length//sqOgLength)+1

    # falta orillas usarlas modificando sqsize
    blackwhite = 1

    sqWidth = sqOgWidth
    # falta aumentar nn y rowsOfSquares una para residuos
    for n in range(columnsOfSquares):

        # cambia ajedrez cada fila si long par
        if ((columnsOfSquares%2) == 0):
            blackwhite = (blackwhite+1)%2
        # cambia 
        
        # Refreshes the square size each column iteration
        sqLength = sqOgLength

        # Modifies range of j for if last column
        if (n == (columnsOfSquares-1)):
            sqWidth = width - ((columnsOfSquares-1)*sqOgWidth)

        for m in range(rowsOfSquares):
            # changes te color each square iterated
            blackwhite = (blackwhite+1)%2

            # Modifies range of j for if last row
            if (m == (rowsOfSquares-1)):
                sqLength = length - ((rowsOfSquares-1)*sqOgLength)
        
            for i in range(sqWidth):
                for j in range(sqLength):
                    x = (n*sqOgWidth)+i
                    y = (m*sqOgLength)+j
                    array[x,y] = (255*blackwhite,255*blackwhite,255*blackwhite,255)


# Modifies the received array of pixels [(r,g,b,brightness),...]
# into same size image with squares of sqOgLengthxsqOgWidth with same promiddle color
def mosaicFilter(sqOgLength, sqOgWidth, array, width, length):
    
    if (sqOgLength>width or sqOgWidth > length):
        return

    
    columnsOfSquares =(width//sqOgWidth)+1
    rowsOfSquares = (length//sqOgLength)+1
    promiddleOfSquare = [0,0,0]


    sqWidth = sqOgWidth
    for n in range(columnsOfSquares):

        
        # Refreshes the square size each column iteration
        sqLength = sqOgLength

        # Modifies range of j for if last column
        if (n == (columnsOfSquares-1)):
            sqWidth = width - ((columnsOfSquares-1)*sqOgWidth)

        for m in range(rowsOfSquares):
            
            # Modifies range of j for if last row
            if (m == (rowsOfSquares-1)):
                sqLength = length - ((rowsOfSquares-1)*sqOgLength)

            promiddleOfSquare = [0,0,0]

            for i in range(sqWidth):
                for j in range(sqLength):
                    x = (n*sqOgWidth)+i
                    y = (m*sqOgLength)+j
                    promiddleOfSquare[0] = ((array[x,y])[0] + promiddleOfSquare[0])//2
                    promiddleOfSquare[1] = ((array[x,y])[1] + promiddleOfSquare[1])//2
                    promiddleOfSquare[2] = ((array[x,y])[2] + promiddleOfSquare[2])//2
            
            for i in range(sqWidth):
                for j in range(sqLength):
                    x = (n*sqOgWidth)+i
                    y = (m*sqOgLength)+j
                    (array[x,y]) = (promiddleOfSquare[0], promiddleOfSquare[1], promiddleOfSquare[2])
        

# Modifies the received array of pixels [(r,g,b,brightness),...]
# to make it look like a chess table
def pixelPerPixelFilter(array, width, length, fourTupleFunction):
    
    # falta aumentar nn y rowsOfSquares una para residuos
    for n in range(width):
        for m in range(length):
            array[n,m] = fourTupleFunction(array[n,m][0],array[n,m][1],array[n,m][2])
# optimizable al guardar r+g...
def toGrayPromiddle(array, width, length):
    fourTupleFunction = lambda r, g, b: ((r+g+b)//3,(r+g+b)//3,(r+g+b)//3,255)
                            
    pixelPerPixelFilter(array, width, length, fourTupleFunction)

def toGrayRedChannel(array, width, length):
    fourTupleFunction = lambda r, g, b: (r,r,r,255)
    pixelPerPixelFilter(array, width, length, fourTupleFunction)

def toGrayGreenChannel(array, width, length):
    fourTupleFunction = lambda r, g, b: (g,g,g,255)
    pixelPerPixelFilter(array, width, length, fourTupleFunction)

def toGrayBlueChannel(array, width, length):
    fourTupleFunction = lambda r, g, b: (b,b,b,255)

    pixelPerPixelFilter(array, width, length, fourTupleFunction)

def mica(array, rChannel, gChannel, bChannel, width, length):
    fourTupleFunction = lambda r, g, b: (rChannel and r
                                         , gChannel and g
                                         , bChannel and b
                                         ,255
                                        )

    pixelPerPixelFilter(array, width, length, fourTupleFunction)

# red ribbon
color = (255,0,0,255)

# x columnas, y filas iz-der arr-abajo
def ribbon(width, length, array):
    for i in range(width):
                array[i,0] = color
                array[i,length-1] = color

    for i in range(length):
                array[0,i] = color
                array[width-1,i] = color








im = Image.open('forest.jpg')
pixelMap = im.load()

size =10
proof = Image.new( im.mode, (size, size))
pixelProof = proof.load()


width = proof.size[0]
length = proof.size[1]

same = 1
sqW = same
sqL = same

# squarer(sqW,sqL,pixelsNew, width, length)
# mosaicFilter(1,1,pixelsNew, width, length)


# PRIMERA
chessTable(sqW,sqL,pixelProof, width, length)
pixelProof[1,8] = color

# mosaicFilter(sqW,sqL,pixelMap, width, length)
# toGrayPromiddle(pixelMap, width, length)
# toGrayRedChannel(pixelMap, width, length)
# toGrayGreenChannel(pixelMap, width, length)
# toGrayBlueChannel(pixelMap, width, length)
# mica(pixelMap,255,0,255, width, length)


# SEGUNDA

proof.show()
im.save('foresb.jpg')