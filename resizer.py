# Resizes image to a fixed width while maintaining the aspect ratio
import os.path
from tkinter import Tk
from tkinter.filedialog import askdirectory

from PIL import Image

# File path, warning: python will go into each folder inside each folder and modify each file
# Unless you want to change all the folders too make sure this is the only folder inside the folder
Tk().withdraw()  # hides ui since we only need the open folder ui
f = askdirectory()

# grabs all the images in the given folder above
for file in os.listdir(f):
    # open the image
    f_img = f + "/" + file
    img = Image.open(f_img)

    basewidth = 1920

    # Calculate resize percentage
    wpercent = (basewidth / float(img.size[0]))

    # Calculate new high using above
    hsize = int((float(img.size[1]) * float(wpercent)))

    # Resize and save image
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(f_img, dpi=(300, 300))
    img.close()
