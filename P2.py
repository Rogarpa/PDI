from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from threading import Thread

class Filters:
    def convolution_kernel_filter(self,array, width, length, kernel_matrix):
        # falta probar que kernel tenga sentido
        radio = len(kernel_matrix)//2

        for x in range(width):
            
            # Refreshes the square size each column iteration
            

            for y in range(length):

                pixel_buffer = [0,0,0]
                start_matrix_coordinate = [0,0]
                start_kernel_coordinate = [0,0]

                padding_x_left = x
                if(padding_x_left > radio):
                    padding_x_left = radio
                padding_x_right = (width-x)-1
                if(padding_x_right > radio):
                    padding_x_right = radio
                padding_y_up = y
                if(padding_y_up > radio):
                    padding_y_up = radio
                padding_y_down = (length - y)-1
                if(padding_y_down > radio):
                    padding_y_down = radio


                start_matrix_coordinate = [x - padding_x_left, y-padding_y_up]
                start_kernel_coordinate = [radio-padding_x_left, radio-padding_y_up]
            
                x_range = padding_x_left + padding_x_right + 1
                y_range = padding_y_up + padding_y_down + 1

                # print((x,y))
                # print('radio' + str(radio))
                # print(start_matrix_coordinate)
                # print(start_kernel_coordinate)
                # print(padding_x_left)
                # print(padding_x_right)
                # # print(y_range)


                for i in range(x_range):
                    for j in range(y_range):
                        
                        pixel_buffer[0] += int((array[(start_matrix_coordinate[0]+i),(start_matrix_coordinate[1]+j)][0]) 
                                                * (kernel_matrix[(start_kernel_coordinate[0]+i)][(start_kernel_coordinate[1]+j)]))
                        pixel_buffer[1] += int((array[(start_matrix_coordinate[0]+i), (start_matrix_coordinate[1]+j)][1])
                                            *kernel_matrix[(start_kernel_coordinate[0]+i)][(start_kernel_coordinate[1]+j)])
                        pixel_buffer[2] += int((array[(start_matrix_coordinate[0]+i), (start_matrix_coordinate[1]+j)][2])
                                            *kernel_matrix[(start_kernel_coordinate[0]+i)][(start_kernel_coordinate[1]+j)])
                
                array[x,y] = (pixel_buffer[0],pixel_buffer[1], pixel_buffer[2])

    
    def blur(self,array, width, length):
        div = 1/5

        blur_convolution_matrix = [[0,div,0],[div,div,div], [0,div,0]]
        self.convolution_kernel_filter(array, width, length, blur_convolution_matrix)
    
    def motion_blur(self,array, width, length):
        div = 1/9

        motion_blur_convolution_matrix = [
                                    [div,0,0,0,0,0,0,0,0]
                                    ,[0,div,0,0,0,0,0,0,0]
                                    ,[0,0,div,0,0,0,0,0,0]
                                    ,[0,0,0,div,0,0,0,0,0]
                                    ,[0,0,0,0,div,0,0,0,0]
                                    ,[0,0,0,0,0,div,0,0,0]
                                    ,[0,0,0,0,0,0,div,0,0]
                                    ,[0,0,0,0,0,0,0,div,0]
                                    ,[0,0,0,0,0,0,0,0,div]
                                  ]
        self.convolution_kernel_filter(array, width, length, motion_blur_convolution_matrix)
    
    def finde_edges(self,array, width, length):
        finde_edges_convolution_matrix = [
                                    [0,0,-1,0,0]
                                    ,[0,0,-1,0,0]
                                    ,[0,0,2,0,0]
                                    ,[0,0,0,0,0]
                                    ,[0,0,0,0,0]
                                  ]
        self.convolution_kernel_filter(array, width, length, finde_edges_convolution_matrix)

    def finde_edges(self,array, width, length):
        finde_edges_convolution_matrix = [
                                    [0,0,-1,0,0]
                                    ,[0,0,-1,0,0]
                                    ,[0,0,2,0,0]
                                    ,[0,0,0,0,0]
                                    ,[0,0,0,0,0]
                                  ]
        self.convolution_kernel_filter(array, width, length, finde_edges_convolution_matrix)

    def sharpen(self,array, width, length):

        sharpen_convolution_matrix = [
                                     [-1,-1,-1]
                                    ,[-1,9,-1]
                                    ,[-1,-1,-1]
        ]
        self.convolution_kernel_filter(array, width, length, sharpen_convolution_matrix)

    def emboss(self,array, width, length):
        emboss_convolution_matrix = [
                                    [-1, -1,  0]
                                    ,[-1,  0,  1]
                                    ,[0,  1,  1]
                                    ]
        self.convolution_kernel_filter(array, width, length, emboss_convolution_matrix)

    def mean(self,array, width, length):
        div = 1/9

        mean_convolution_matrix = [
                                    [div,div,div]
                                    ,[div,div,div]
                                    ,[div,div,div]
                                  ]
        self.convolution_kernel_filter(array, width, length, mean_convolution_matrix)
    

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
        self.to_edit_image_fp = "./forest.jpg"
        # self.to_edit_image_fp = StringVar()
        
        # self.select_file()

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

        # self.button_gray_filter = Button(
        #     self.tool_bar, text="ToGray", command=self.applyToGray)
        # self.button_gray_filter.grid(row=0, column=1, padx=5, pady=3, ipadx=10)

        # self.button_mosaic_filter = Button(
        #     self.tool_bar, text="Mosaic", command=self.applyToMosaic)
        # self.button_mosaic_filter.grid(row=0, column=2, padx=5, pady=3, ipadx=10)

        self.open_button = Button(
            self.tool_bar,
            text='Open a File',
            command=self.select_file
        ).grid(row=0, column=3, padx=5, pady=3, ipadx=10)


        # self.mosaic_length = Label(self.tool_bar, text="Mosaic Length:")
        # self.mosaic_length.grid(row=3, column=0, padx=5, pady=3, ipadx=10)

        # self.mosaic_length = Label(self.tool_bar, text="Mosaic Width:")
        # self.mosaic_length.grid(row=4, column=0, padx=5, pady=3, ipadx=10)
        
        # self.mosaic_length_box = Entry(self.tool_bar, width = 4)
        # self.mosaic_length_box.grid(row=3, column=3, padx=5, pady=3, ipadx=10)

        # self.mosaic_width_box = Entry(self.tool_bar, text='Width', width = 4)
        # self.mosaic_width_box.grid(row=4, column=3, padx=5, pady=3, ipadx=10)

            # 5th row

        self.button_toBlur_filter = Button(
        self.tool_bar, text="Blur", command=self.applyBlur)
        self.button_toBlur_filter.grid(row=5, column=0, padx=5, pady=3, ipadx=10)

        self.button_toMotionBlur_filter = Button(
        self.tool_bar, text="Motion Blur", command=self.applyMotionBlur)
        self.button_toMotionBlur_filter.grid(row=5, column=1, padx=5, pady=3, ipadx=10)

        self.button_toFindEdges_filter = Button(
        self.tool_bar, text="Find Edges", command=self.applyFindEdges)
        self.button_toFindEdges_filter.grid(row=5, column=2, padx=5, pady=3, ipadx=10)
        
        self.button_toSharpen_filter = Button(
        self.tool_bar, text="Sharpen", command=self.applySharpen)
        self.button_toSharpen_filter.grid(row=5, column=3, padx=5, pady=3, ipadx=10)

        self.button_toEmboss_filter = Button(
        self.tool_bar, text="Emboss", command=self.applyEmboss)
        self.button_toEmboss_filter.grid(row=5, column=4, padx=5, pady=3, ipadx=10)

        self.button_toMean_filter = Button(
        self.tool_bar, text="Mean", command=self.applyMean)
        self.button_toMean_filter.grid(row=5, column=5, padx=5, pady=3, ipadx=10)

        self.filter_progressbar = ttk.Progressbar(self.tool_bar, mode="indeterminate", length = 300)
        # self.filter_progressbar = ttk.Progressbar(self.tool_bar, length = 300)
        self.filter_progressbar.grid(row=6, column=0, padx=5, pady=3, ipadx=10)

        # self.button_toGrayGreenChannel_filter = Button(
        # self.tool_bar, text="toGrayGreenChannel", command=self.applyToGrayGreenChannel)
        # self.button_toGrayGreenChannel_filter.grid(row=5, column=1, padx=5, pady=3, ipadx=10)

        # self.button_toGrayBlueChannel_filter = Button(
        # self.tool_bar, text="toGrayBlueChannel", command=self.applyToGrayBlueChannel)
        # self.button_toGrayBlueChannel_filter.grid(row=5, column=2, padx=5, pady=3, ipadx=10)

        # self.button_mica_filter = Button(
        # self.tool_bar, text="Colour Filter", command=self.applyMica)
        # self.button_mica_filter.grid(row=5, column=3, padx=5, pady=3, ipadx=10)

        #     # 6th row
        # self.red_channel_label = Label(self.tool_bar, text="Red component (0-255):")
        # self.red_channel_label.grid(row=6, column=0, padx=5, pady=3, ipadx=10)

        # self.red_channel_box = Entry(self.tool_bar, width = 4)
        # self.red_channel_box.grid(row=6, column=1, padx=5, pady=3, ipadx=10)

        #     # 7th row
    
        # self.green_channel_label = Label(self.tool_bar, text="Green component (0-255):")
        # self.green_channel_label.grid(row=7, column=0, padx=5, pady=3, ipadx=10)

        # self.green_channel_box = Entry(self.tool_bar, width = 4)
        # self.green_channel_box.grid(row=7, column=1, padx=5, pady=3, ipadx=10)
        
        #     # 8th row
        # self.blue_channel_label = Label(self.tool_bar, text="Blue component (0-255):")
        # self.blue_channel_label.grid(row=8, column=0, padx=5, pady=3, ipadx=10)

        # self.blue_channel_box = Entry(self.tool_bar, width = 4)
        # self.blue_channel_box.grid(row=8, column=1, padx=5, pady=3, ipadx=10)
        

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
        

    def applyBlur(self):
        self.revertChanges()
        try:
            # self.filter_progressbar.step(50)
            Thread(target=self.filter_progressbar.start(50)).start()
            
            self.filters.blur(
                                    (self.im.load())
                                    ,(self.im.size[0])
                                    , (self.im.size[1]))
            self.filter_progressbar.stop()

            self.update_main_image()
        except ValueError as error:
            showerror(title='Error', message=error)
    
    def applyMotionBlur(self):
        self.revertChanges()
        try:
            self.filter_progressbar.start(500)
            self.filters.motion_blur(
                                    (self.im.load())
                                    ,(self.im.size[0])
                                    , (self.im.size[1]))
            self.filter_progressbar.stop()

            self.update_main_image()
        except ValueError as error:
            showerror(title='Error', message=error)

    def applyFindEdges(self):
        self.revertChanges()
        try:
            self.filter_progressbar.start(500)
            self.filters.finde_edges(
                                    (self.im.load())
                                    ,(self.im.size[0])
                                    , (self.im.size[1]))
            self.filter_progressbar.stop()

            self.update_main_image()
        except ValueError as error:
            showerror(title='Error', message=error)
    
    def applySharpen(self):
        self.revertChanges()
        try:
            self.filter_progressbar.start(500)
            self.filters.sharpen(
                                    (self.im.load())
                                    ,(self.im.size[0])
                                    , (self.im.size[1]))
            self.filter_progressbar.stop()

            self.update_main_image()
        except ValueError as error:
            showerror(title='Error', message=error)
    
    def applyEmboss(self):
        self.revertChanges()
        try:
            self.filter_progressbar.start(500)
            self.filters.emboss(
                                    (self.im.load())
                                    ,(self.im.size[0])
                                    , (self.im.size[1]))
            self.filter_progressbar.stop()

            self.update_main_image()
        except ValueError as error:
            showerror(title='Error', message=error)
    
    def applyMean(self):
        self.revertChanges()
        try:
            self.filter_progressbar.start(500)
            self.filters.motion_blur(
                                    (self.im.load())
                                    ,(self.im.size[0])
                                    , (self.im.size[1]))
            self.filter_progressbar.stop()

            self.update_main_image()
        except ValueError as error:
            showerror(title='Error', message=error)

    def update_main_image(self):
        self.new_test = ImageTk.PhotoImage(self.im)
        self.main_image_label.config(image=self.new_test)

    def revertChanges(self):
        self.im = Image.open(self.to_edit_image_fp)
        # self.update_main_image()
    


root = Tk()  # create root window
root.title("P1")  # title of the GUI window
root.maxsize(900, 600)  # specify the max size the window can expand to
root.config(bg="skyblue")  # specify background color


app = Aplicacion(root)

root.mainloop()












