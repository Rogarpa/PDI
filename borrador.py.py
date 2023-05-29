from PIL import Image
from numpy import asarray
 
 
# load the image and convert into
# numpy array
img = Image.open('Sample.png')
 
# asarray() class is used to convert
# PIL images into NumPy arrays
numpydata = asarray(img)





# numpydata = asarray(img)
# numpydata = np.array(img)
# numpydata[4,3] = [255,255,255]

# print(numpydata)
# print(len(numpydata))
# print(len(numpydata[0]))

# pilImage = Image.fromarray(numpydata)
# pilarr = pilImage.load()

# ribbon(
# pilImage.size[0],
# pilImage.size[1],
# pilarr
# )

# pilImage.show()


# img.show()
im.show()

# for i in range(img.size[0]):
#     for j in range(img.size[1]):
#         if 205 in pixelMap[i,j]:
#             pixelMap[i,j] = (0,0,0,255)
#         else:





