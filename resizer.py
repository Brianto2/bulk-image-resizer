import os
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import Image


# Main frame
def UI():
    gui = Tk()
    gui.geometry("375x175")
    gui.title("Bulk image resizer")
    # Create a style
    style = ttk.Style(gui)

    # Set the theme with the theme_use method
    style.theme_use('vista')

    src_path = StringVar()
    width = StringVar()
    dpi = StringVar()
    options = [
        600,
        600,
        300,
        144,
        72
    ]

    width.set(1920)

    # first row, source folder
    s_label = Label(gui, text="Source Folder")
    s_entry = Entry(gui, textvariable=src_path)
    s_browse = ttk.Button(gui, text="Browse Folder", command=lambda: getFolderPath(src_path))

    s_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 5))
    s_entry.grid(row=0, column=1, padx=(10, 10), pady=(10, 5))
    s_browse.grid(row=0, column=2, padx=(10, 10), pady=(10, 5))

    # second row, resize width
    w_label = ttk.Label(gui, text="Width (Pixels)")
    w_entry = ttk.Entry(gui, textvariable=width)

    w_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 5))
    w_entry.grid(row=1, column=1, padx=(10, 10), pady=(10, 5))

    # third row, dpi
    d_label = ttk.Label(gui, text="Quality (DPI)")
    d_option = ttk.OptionMenu(gui, dpi, *options)

    d_label.grid(row=2, column=0, padx=(10, 10), pady=(10, 5))
    d_option.grid(row=2, column=1, padx=(10, 10), pady=(10, 5))

    # start button
    c = ttk.Button(gui, text="Resize images", command=lambda: resize(src_path, width, dpi))
    c.grid(row=2, column=2, padx=(10, 10), pady=(10, 10))

    return gui


# Sets the directory when the button is clicked
def getFolderPath(folder_path):
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)


# bulk resize images
# vars: dir = directory, width = width to resize to, res = image resolution in dpi (dots per inch)

def resize(folder, width, res):
    folder = folder.get()
    width = int(width.get())
    res = float(res.get())

    # Don't do anything unless directory path is specified
    if folder == "":
        messagebox.showwarning(title="BW Image Mover", message="Input source folders")
        return

    # Small image warning
    if width < 800:
        o = messagebox.askokcancel(title="BW Image Mover", message="Resize width is less than 800px Continue?")
        if not o:
            return
    # Massive image warning
    if width > 7680:
        o = messagebox.askokcancel(title="BW Image Mover", message="Resize width is more than 7680px (8K) Continue?")
        if not o:
            return
    # Get the user to confirm
    mstring = "Resizing Images in " + folder + " to a width of " + str(width) + " at " + str(res) + \
              "dpi. THIS CANNOT BE UNDONE."
    option = messagebox.askokcancel(title="BW Image Mover", message=mstring)  # returns True or False
    if not option:
        return

    # grabs all the images in the given folder above
    for file in os.listdir(folder):
        # open the image
        f_img = folder + "/" + file
        img = Image.open(f_img)

        # don't resize if the image is already that size, and ignore gifs
        w, h = img.size
        if w != width and not f_img.endswith("gif"):
            # Calculate resize percentage
            wpercent = (width / float(img.size[0]))

            # Calculate new high using above
            hsize = int((float(img.size[1]) * float(wpercent)))

            # Resize and save image
            img = img.resize((width, hsize), Image.ANTIALIAS)
            img.save(f_img, dpi=(res, res))
            img.close()


mainframe = UI()
mainframe.mainloop()
