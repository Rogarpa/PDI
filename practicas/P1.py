from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror

class Aplicacion(Frame):

    def __init__(self, parent):
        # llama a constructor padre
        super().__init__(parent)
        self.filters = Filters()


        # Create left and right frames
        self.left_frame = Frame(parent, width=200, height=700, bg='grey')
        self.left_frame.grid(row=0, column=0, padx=10, pady=5)

        self.right_frame = Frame(parent, width=650, height=700, bg='grey')
        self.right_frame.grid(row=0, column=1, padx=10, pady=5)

        # Create frames and labels in left_frame
        Label(self.left_frame, text="Original Image").grid(row=0, column=0, padx=5, pady=5)

        # Select image
        # self.to_edit_image_fp = "./forest.jpg"
        # self.to_edit_image_fp = StringVar()
        
        self.select_file()

        self.im = Image.open(self.to_edit_image_fp)
        self.test = ImageTk.PhotoImage(self.im)

        self.img_buffer = Image.new(self.im.mode, self.im.size)

        self.im_resized = self.im.resize((300,300))
        self.test_resized = ImageTk.PhotoImage(self.im_resized)
        
        # Frames images
        self.main_image_label = Label(self.right_frame, image=self.test)
        self.main_image_label.grid(row=0,column=0, padx=5, pady=5)
        
        self.mini_image_label = Label(self.left_frame, image=self.test_resized)
        self.mini_image_label.grid(row=1, column=0, padx=5, pady=5)

        # Create tool bar frame
        self.tool_bar = Frame(self.left_frame, width=300, height=300, bg='red')
        self.tool_bar.grid(row=2, column=0, padx=5, pady=5)

        # Widgets of tool bar frame
            # 1th row

        
        self.button_revert_img = Button(
            self.tool_bar, text="Revert", command=self.revertChanges)
        self.button_revert_img.grid(row=0, column=0, padx=5, pady=3, ipadx=10)

        self.button_gray_filter = Button(
            self.tool_bar, text="ToGray", command=self.applyToGray)
        self.button_gray_filter.grid(row=0, column=1, padx=5, pady=3, ipadx=10)

        self.button_mosaic_filter = Button(
            self.tool_bar, text="Mosaic", command=self.applyToMosaic)
        self.button_mosaic_filter.grid(row=0, column=2, padx=5, pady=3, ipadx=10)

        self.open_button = Button(
            self.tool_bar,
            text='Open a File',
            command=self.select_file
        ).grid(row=0, column=3, padx=5, pady=3, ipadx=10)


        self.mosaic_length = Label(self.tool_bar, text="Mosaic Length:")
        self.mosaic_length.grid(row=3, column=0, padx=5, pady=3, ipadx=10)

        self.mosaic_length = Label(self.tool_bar, text="Mosaic Width:")
        self.mosaic_length.grid(row=4, column=0, padx=5, pady=3, ipadx=10)
        
        self.mosaic_length_box = Entry(self.tool_bar, width = 4)
        self.mosaic_length_box.grid(row=3, column=3, padx=5, pady=3, ipadx=10)

        self.mosaic_width_box = Entry(self.tool_bar, text='Width', width = 4)
        self.mosaic_width_box.grid(row=4, column=3, padx=5, pady=3, ipadx=10)

            # 5th row

        self.button_toGrayRedChannel_filter = Button(
        self.tool_bar, text="toGrayRedChannel", command=self.applyToGrayRedChannel)
        self.button_toGrayRedChannel_filter.grid(row=5, column=0, padx=5, pady=3, ipadx=10)

        self.button_toGrayGreenChannel_filter = Button(
        self.tool_bar, text="toGrayGreenChannel", command=self.applyToGrayGreenChannel)
        self.button_toGrayGreenChannel_filter.grid(row=5, column=1, padx=5, pady=3, ipadx=10)

        self.button_toGrayBlueChannel_filter = Button(
        self.tool_bar, text="toGrayBlueChannel", command=self.applyToGrayBlueChannel)
        self.button_toGrayBlueChannel_filter.grid(row=5, column=2, padx=5, pady=3, ipadx=10)

        self.button_mica_filter = Button(
        self.tool_bar, text="Colour Filter", command=self.applyMica)
        self.button_mica_filter.grid(row=5, column=3, padx=5, pady=3, ipadx=10)

            # 6th row
        self.red_channel_label = Label(self.tool_bar, text="Red component (0-255):")
        self.red_channel_label.grid(row=6, column=0, padx=5, pady=3, ipadx=10)

        self.red_channel_box = Entry(self.tool_bar, width = 4)
        self.red_channel_box.grid(row=6, column=1, padx=5, pady=3, ipadx=10)

            # 7th row
    
        self.green_channel_label = Label(self.tool_bar, text="Green component (0-255):")
        self.green_channel_label.grid(row=7, column=0, padx=5, pady=3, ipadx=10)

        self.green_channel_box = Entry(self.tool_bar, width = 4)
        self.green_channel_box.grid(row=7, column=1, padx=5, pady=3, ipadx=10)
        
            # 8th row
        self.blue_channel_label = Label(self.tool_bar, text="Blue component (0-255):")
        self.blue_channel_label.grid(row=8, column=0, padx=5, pady=3, ipadx=10)

        self.blue_channel_box = Entry(self.tool_bar, width = 4)
        self.blue_channel_box.grid(row=8, column=1, padx=5, pady=3, ipadx=10)
        

    def select_file(self):
        filetypes = (
            ('text files', '*.jpg'),
            ('All files', '*.*')
        )

        self.to_edit_image_fp = fd.askopenfilename(
            title='Open a file',
            # initialdir='/home/rodriginsky/Desktop/Practicas\ Concurrente/ComputacionConcurrente2023-2/P1',
            initialdir='~/Desktop/Practicas PDI/P1',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=self.to_edit_image_fp
        )
        
        
    def applyToGray(self):
        self.revertChanges()
        try:
            self.filters.toGrayPromiddle(
                                    (self.im.load())
                                    ,(self.im.size[0])
                                    ,(self.im.size[1]))
            self.update_main_image()
        except ValueError as error:
            showerror(title='Error', message=error)
    
    def applyToMosaic(self):
        self.revertChanges()
        try:
            self.filters.mosaicFilter(
                                    int(self.mosaic_length_box.get())
                                    ,int(self.mosaic_width_box.get())
                                    ,(self.im.load())
                                    ,(self.im.size[0])
                                    , (self.im.size[1]))
            self.update_main_image()
        except ValueError as error:
            showerror(title='Error', message=error)



    def applyToGrayPromiddle(self):
        self.revertChanges()
        try:
            self.filters.applyToGrayPromiddle(
                                    (self.im.load())
                                    ,(self.im.size[0])
                                    , (self.im.size[1]))
            self.update_main_image()
        except ValueError as error:
            showerror(title='Error', message=error)



    def applyToGrayRedChannel(self):
        self.revertChanges()
        try:
            self.filters.toGrayRedChannel(
                                    (self.im.load())
                                    ,(self.im.size[0])
                                    , (self.im.size[1]))
            self.update_main_image()
        except ValueError as error:
            showerror(title='Error', message=error)



    def applyToGrayGreenChannel(self):
        
        self.revertChanges()
        try:
            self.filters.toGrayGreenChannel(
                                    (self.im.load())
                                    ,(self.im.size[0])
                                    , (self.im.size[1]))
            self.update_main_image()
        except ValueError as error:
            showerror(title='Error', message=error)



    def applyToGrayBlueChannel(self):
        self.revertChanges()
        try:
            self.filters.toGrayBlueChannel(
                                    (self.im.load())
                                    ,(self.im.size[0])
                                    , (self.im.size[1]))
            self.update_main_image()
        except ValueError as error:
            showerror(title='Error', message=error)

    def applyMica(self):
        self.revertChanges()
        try:
            self.filters.mica(
                                    (self.im.load())
                                    ,int(self.red_channel_box.get())
                                    ,int(self.green_channel_box.get())
                                    ,int(self.blue_channel_box.get())
                                    ,(self.im.size[0])
                                    , (self.im.size[1]))
            self.update_main_image()
        except ValueError as error:
            showerror(title='Error', message=error)



    def update_main_image(self):
        self.new_test = ImageTk.PhotoImage(self.im)
        self.main_image_label.config(image=self.new_test)

    def revertChanges(self):
        self.im = Image.open(self.to_edit_image_fp)
        # self.update_main_image()
    


class Filters:
    

    def mosaicFilter(self,sqOgLength, sqOgWidth, array, width, length):
    
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
    def pixelPerPixelFilter(self, array, width, length, fourTupleFunction):
        
        # falta aumentar nn y rowsOfSquares una para residuos
        for n in range(width):
            for m in range(length):
                array[n,m] = fourTupleFunction(array[n,m][0],array[n,m][1],array[n,m][2])
    # optimizable al guardar r+g...
    def toGrayPromiddle(self, array, width, length):
        fourTupleFunction = lambda r, g, b: ((r+g+b)//3,(r+g+b)//3,(r+g+b)//3,255)
                                
        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)

    def toGrayRedChannel(self, array, width, length):
        fourTupleFunction = lambda r, g, b: (r,r,r,255)
        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)

    def toGrayGreenChannel(self, array, width, length):
        fourTupleFunction = lambda r, g, b: (g,g,g,255)
        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)

    def toGrayBlueChannel(self, array, width, length):
        fourTupleFunction = lambda r, g, b: (b,b,b,255)

        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)

    def mica(self, array, rChannel, gChannel, bChannel, width, length):
        fourTupleFunction = lambda r, g, b: (rChannel and r
                                            , gChannel and g
                                            , bChannel and b
                                            ,255
                                            )

        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)




root = Tk()  # create root window
root.title("P1")  # title of the GUI window
root.maxsize(900, 600)  # specify the max size the window can expand to
root.config(bg="skyblue")  # specify background color


app = Aplicacion(root)

root.mainloop()
