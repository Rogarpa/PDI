from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from threading import *
from math import *
import os 

# detalles:
# mosaicos tienen que tener forma correcta
# 

class Aplication(Frame):
    
    def __init__(self):
        a = 0

    def __init__(self, parent):
        self.parent = parent

        # llama a constructor padre
        super().__init__(parent)
        self.create_main_frames()
        self.create_toolbar_widgets()

    def create_main_frames(self):
        # Create left and right frames
        self.left_frame = Frame(self.parent, width=200, height=700, bg='grey')
        self.left_frame.grid(row=0, column=0, padx=10, pady=5)

        self.right_frame = Frame(self.parent, width=650, height=700, bg='grey')
        self.right_frame.grid(row=0, column=1, padx=10, pady=5)

        # Create frames and labels in left_frame
        Label(self.left_frame, text="Original Image").grid(row=0, column=0, padx=5, pady=5)

        # Select image
        self.to_edit_image_fp = self.select_image()
        print(self.to_edit_image_fp)

        self.to_edit_images_fps =  self.select_files()


        # Update status of filter 
        self.update = StringVar(self.parent,'hola', "s1")
        self.update.trace('w', self.setUpdate)
        self.filters = Filters(self.update)
        
        # Open images
        self.main_image = Image.open(self.to_edit_image_fp)
        self.main_image_tk = ImageTk.PhotoImage(self.main_image)

        self.main_image_resized = self.main_image.resize((300,300))
        self.main_image_resized_tk = ImageTk.PhotoImage(self.main_image)
        
        # Frames images labels
        self.main_image_label = Label(self.right_frame, image=self.main_image_tk)
        self.main_image_label.grid(row=0,column=0, padx=5, pady=5)


        self.mini_image_label = Label(self.left_frame, image=self.main_image_tk)
        self.mini_image_label.grid(row=1, column=0, padx=5, pady=5)

        # Refreshing main image
        self.autorefresh_main_image()
        self.autorefresh_mini_image()
        
        # Progress label
        self.program_state = Label(self.left_frame, text = 'state')
        self.program_state.grid(row=1, column=1, padx=5, pady=5)

        # Create tool bar frame
        self.tool_bar = Frame(self.left_frame, width=300, height=300, bg='red')
        self.tool_bar.grid(row=2, column=0, padx=5, pady=5)

        # f.photoMosaic(p,p,pixelMap,width, length, self.to_edit_images_fps)
        
    def create_toolbar_widgets(self):
        self.button_revert_img = Button(
            self.tool_bar, text="Revert", command=self.revertChanges)
        self.button_revert_img.grid(row=0, column=0, padx=5, pady=3, ipadx=10)

        self.open_button = Button(
            self.tool_bar,
            text='Open a File',
            command=self.reselect_image
        )
        self.open_button.grid(row=0, column=3, padx=5, pady=3, ipadx=10)

        self.save_button = Button(
            self.tool_bar,
            text='Save the File',
            command=self.save_image
        ).grid(row=0, column=4, padx=5, pady=3, ipadx=10)

        self.process_images = Button(
        self.tool_bar, text="Process images", command=self.process_images)
        self.process_images.grid(row=5, column=1, padx=5, pady=3, ipadx=10)

        self.photomosaic_button = Button(
        self.tool_bar, text="Create photomosaic", command=self.createPhotomosaic)
        self.photomosaic_button.grid(row=5, column=2, padx=5, pady=3, ipadx=10)
        
        self.html_photomosaic_buton = Button(
        self.tool_bar, text="Process Images", command=self.createHtmlPhotomosaic)
        self.html_photomosaic_buton.grid(row=5, column=3, padx=5, pady=3, ipadx=10)

    def reselect_image(self):
        filetypes = (
            ('text files', '*.jpg'),
            ('All files', '*.*')
        )

        fp = fd.askopenfilename(
            title='Open a file',
            # initialdir='/home/rodriginsky/Desktop/Practicas\ Concurrente/ComputacionConcurrente2023-2/P1',
            initialdir='~/Desktop/Practicas PDI/P1',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=fp
        )
        self.to_edit_image_fp = fp
        self.main_image = Image.open(fp)
        self.main_image_tk = ImageTk.PhotoImage(self.main_image)

        self.main_image_resized = self.main_image.resize((300,300))
        self.main_image_resized_tk = ImageTk.PhotoImage(self.main_image_resized)
        
        # Frames images labels
        self.main_image_label.config(image=self.main_image_tk)

        self.mini_image_label.config(image=self.main_image_resized_tk)

        self.parent.update_idletasks()

    def select_image(self):
        filetypes = (
            ('text files', '*.jpg'),
            ('All files', '*.*')
        )

        fp = fd.askopenfilename(
            title='Open a file',
            # initialdir='/home/rodriginsky/Desktop/Practicas\ Concurrente/ComputacionConcurrente2023-2/P1',
            initialdir='~/Desktop/Practicas PDI/P1',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=fp
        )
        return fp
    
    def select_mosaics(self):
        filetypes = (
            ('text files', '*.jpg'),
            ('All files', '*.*')
        )

        fps = fd.askopenfilenames(
            title='Select mosaic images',
            # initialdir='/home/rodriginsky/Desktop/Practicas\ Concurrente/ComputacionConcurrente2023-2/P1',
            initialdir='~/Desktop/Practicas PDI/P1',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=fps
        )
        self.filters.process_mosaics(fps)

        return fps

    def save_image(self):
        filetypes = (
            ('text files', '*.jpg'),
            ('All files', '*.*')
        )

        save_fp = fd.asksaveasfile(
            title='Open a file',
            # initialdir='/home/rodriginsky/Desktop/Practicas\ Concurrente/ComputacionConcurrente2023-2/P1',
            initialdir='~/Desktop/Practicas PDI/P1',
            filetypes=filetypes
            )

        showinfo(
            title='Selected File',
            message="Guardado"
        )
        self.main_image.save(save_fp)

        
    def autorefresh_main_image(self):
        self.update_main_image()
        self.parent.update_idletasks()
        self.parent.after(500, self.autorefresh_main_image)
    
    def autorefresh_mini_image(self):
        self.update_main_image()
        self.parent.update_idletasks()
        self.parent.after(500, self.autorefresh_main_image)
    
    def setUpdate(self, a=None,b=None,c=None):
        self.program_state.config(text = self.update.get())
        self.parent.update_idletasks()
        self.parent.after(0, self.setUpdate)

    



    def update_main_image(self):

        self.refreshed_image = ImageTk.PhotoImage(self.main_image)
        self.main_image_label.config(image=self.refreshed_image)

    def update_mini_image(self):
        self.refreshed_resized_image = ImageTk.PhotoImage(self.main_image.resize((300,300)))
        self.mini_image_label.config(image=self.refreshed_resized_image)

    def revertChanges(self):
        self.main_image = Image.open(self.to_edit_image_fp)
        self.update_main_image()
    


    def select_file(self):
        filetypes = (
            ('text files', '*.jpg'),
            ('All files', '*.*')
        )

        file = fd.askopenfilename(
            title='Open a file',
            # initialdir='/home/rodriginsky/Desktop/Practicas\ Concurrente/ComputacionConcurrente2023-2/P1',
            initialdir='~/Desktop/Practicas PDI/P1/',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=self.to_edit_image_fp
        )
        return file
    
    def select_files(self):
        filetypes = (
            ('text files', '*.jpg'),
            ('All files', '*.*')
        )

        files = fd.askopenfilenames(
            title='Open a file',
            # initialdir='/home/rodriginsky/Desktop/Practicas\ Concurrente/ComputacionConcurrente2023-2/P1',
            initialdir='~/Desktop/Practicas PDI/P1/',
            )

        showinfo(
            title='Selected File',
            message=self.to_edit_image_fp
        )
        return files
    
    def process_images(self):
        try:
            self.filters.process_mosaics(
                                    self.to_edit_images_fps
                                )

        except ValueError as error:
            showerror(title='Error', message=error)

    def createPhotomosaic(self):
        try:
            self.filters.photoMosaic(20, 20, self.main_image.load()
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1])
                                    ,self.to_edit_images_fps
                                    )

        except ValueError as error:
            showerror(title='Error', message=error)
    
    def createHtmlPhotomosaic(self):
        try:
            self.filters.htmlPhotoMosaic(10, 10, self.main_image.load()
                                    ,(self.main_image.size[0])
                                    , (self.main_image.size[1])
                                    ,self.to_edit_images_fps
                                    )

        except ValueError as error:
            showerror(title='Error', message=error)








        
    #     # self.to_edit_image_fp = "forest.jpg"
    #         # self.to_edit_image_fp = "b.jpg"
    #     # self.to_edit_image_fp =  self.select_file()
    #         # self.to_edit_images_fps = ""

    #         # self.to_edit_images_fps =  self.select_files()
    #     # self.to_edit_images_fps =  os.listdir(self.to_edit_images_fps)
    #     # self.mosaic_lists =  os.listdir(self.to_edit_images_fps)
    #     # self.mosaic_lists =  os.listdir('./col/')

    #     # print(self.to_edit_images_fps)
    #     # im = Image.open('at.jpg')
    #     # im = Image.open(self.to_edit_image_fp)
    #     # pixelMap = im.load()

    #     # pixelMap = im.resize((size,size)).load()

    #     # proof = Image.new( im.mode, (size, size))
    #     # pixelProof = proof.load()


    #     # width = im.size[0]
    #     # length = im.size[1]
    #     # width = proof.size[0]
    #     # length = proof.size[1]

    #     # f = Filters()
        
    #     # v = 15
    #     # search = [v,v,v]

    #     # metric = lambda c1,c2: int(sqrt(
    #     #                     pow((c1[0]-c2[0]),2)
    #     #                     +pow((c1[1]-c2[1]),2)
    #     #                     +pow(abs(c1[2]-c2[2]),2))
    #     #                     )

        
        
        
        
            
        
    #     # f.process_mosaics(fp_list)
    #     # print(self.to_edit_images_fps)
    #     # print(self.to_edit_image_fp)
    #     # f.color_creator(self.to_edit_image_fp, "./buffer_mosaico/")
    #     # f.process_mosaics(self.to_edit_images_fps)
    #     # print(f.search_nearest_color_fp(search, self.to_edit_images_fps, metric))
    #     # p = 30
    #         # f.photoMosaic(p,p,pixelMap,width, length, self.to_edit_images_fps)
    #     # f.blend(pixelMap, 200,0, 0, width, length)

    #         # im.show()
    #     # proof.show()

    #         # im.save('foresb.jpg')
    
class Filters():
    def __init__(self, update_string):
        self.update_string = update_string


    def pixelPerPixelFilter(self, array, width, length, fourTupleFunction):
        
        for n in range(width):
            for m in range(length):
                array[n,m] = fourTupleFunction(array[n,m][0],array[n,m][1],array[n,m][2])
    
    def process_mosaics(self, filespaths_list):
        
        self.update_string.set('100/100')
    

        promiddle = [0,0,0]

        # Clear file
        open('imagen.txt', 'w').close()

        for f in range(len(filespaths_list)):
            file_path = filespaths_list[f]

            self.update_string.set("processing mosaic: " + file_path
            +" " +str(int((f/len(filespaths_list))*100)) + '/100%')

            buffer_image = Image.open(file_path)
            buffer_pixelmap = buffer_image.load()

            for x in range(buffer_image.size[0]):
                for y in range(buffer_image.size[1]):
                    promiddle[0] = ((promiddle[0]) + (buffer_pixelmap[x,y][0]))//2
                    promiddle[1] = ((promiddle[1]) + (buffer_pixelmap[x,y][1]))//2
                    promiddle[2] = ((promiddle[2]) + (buffer_pixelmap[x,y][2]))//2
            

            print("saving"+file_path + str(promiddle)+ '.jpg')
            # buffer_image.save(file_path+ str(promiddle)+('.jpg'))
            
            with open('./imagen.txt', 'a') as f:
                f.write("\n" + str(promiddle) + ":" + file_path)
        with open('./imagen.txt', 'a') as f:
                f.write("\n")
        self.update_string.set("processing mosaic: " + '100/100%')


    def color_creator(self, input_fp, output_fp):
        print('color c')
        buffer_image = Image.open(input_fp)
        buffer_pixelmap = buffer_image.load()
        width = buffer_image.size[0]
        length = buffer_image.size[1]
        interval = 70
        for r in range(0,255,interval):
            for g in range(0,255,interval):
                for b in range (0,255,interval):
                    # for x in range(width):
                    #     for y in range(length):
                    #         buffer_pixelmap[x,y] = (r,g,b)
                    # self.blend(buffer_pixelmap, r,g,b,width,length)
                    self.blend(buffer_pixelmap, r,g,b,width,length)
                    print((r,g,b))
                    name = str((r,g,b))+".jpg"
                    buffer_image.save(output_fp+name)
                    buffer_image = Image.open(input_fp)
                    buffer_pixelmap = buffer_image.load()
    def search_nearest_color_fp(self, color_to_compare, colors_list, metric_function):
        better_fp = ''
        min_metric_value = 500
        color = [0,0,0]
        with open('./imagen.txt','r') as f:
            dictionary = f.readlines()
        for i in range(1,len(dictionary),1):
            
            
            
            # file_name = (((colors_list[i]).split('/'))[-1:])[0]
            # Obtenemos el color
            # print((dictionary[i].split(':')[0])[3:-1])
            color_string = (str((dictionary[i].split(':')[0])[1:-1]).split(','))
            color = [0,0,0]
            
            for v in range(3):
                color[v] = int(color_string[v])




            buffer_value = metric_function(color_to_compare,color)

            if(buffer_value <= min_metric_value):
                min_metric_value = buffer_value
                better_fp = (dictionary[i].split(':'))[1][:-1]
        
        return better_fp
            
    
    def photoMosaic(self,sqOgLength, sqOgWidth, array, width, length, mosaics_fps):

        if (sqOgLength>width or sqOgWidth > length):
            return

        metric = lambda c1,c2: int(sqrt(
                            pow((c1[0]-c2[0]),2)
                            +pow((c1[1]-c2[1]),2)
                            +pow(abs(c1[2]-c2[2]),2))
                            )


        columnsOfSquares =(width//sqOgWidth)+1
        rowsOfSquares = (length//sqOgLength)+1
        promiddleOfSquare = [0,0,0]


        sqWidth = sqOgWidth
        for n in range(columnsOfSquares):
            self.update_string.set("photomosaic creation:"+str(int((n/columnsOfSquares)*100)) + '/100%')
            
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
                
                # substitute mosaic by image
             
                fp_substitute_mosaic_image = self.search_nearest_color_fp(promiddleOfSquare, mosaics_fps, metric)
                mosaic = Image.open(fp_substitute_mosaic_image)
                mosaic = mosaic.resize((sqOgWidth,sqOgLength))
                mosaic_pixel_matrix = mosaic.load()

                for i in range(sqWidth):
                    for j in range(sqLength):
                        x = (n*sqOgWidth)+i
                        y = (m*sqOgLength)+j
                        array[x,y] = mosaic_pixel_matrix[i,j]
        self.update_string.set('100/100')
    # def htmlPhotoMosaic(self,sqOgLength, sqOgWidth, array, width, length, mosaics_fps):

    #     if (sqOgLength>width or sqOgWidth > length):
    #         return

    #     metric = lambda c1,c2: int(sqrt(
    #                         pow((c1[0]-c2[0]),2)
    #                         +pow((c1[1]-c2[1]),2)
    #                         +pow(abs(c1[2]-c2[2]),2))
    #                         )


    #     columnsOfSquares =(width//sqOgWidth)+1
    #     rowsOfSquares = (length//sqOgLength)+1
    #     promiddleOfSquare = [0,0,0]
        
    #     open("photomosaic.html").close()
    #     with open('photomosaic.html', 'a') as f:
    #                 f.write("<table border=\"0\" cellspacing=\"0\" cellpadding=\"0\">")


    #     sqWidth = sqOgWidth
    #     for n in range(columnsOfSquares):
    #         self.update_string.set("html_photomosaic creation:"+str(int((n/columnsOfSquares)*100)) + '/100%')
            
    #         # Refreshes the square size each column iteration
    #         sqLength = sqOgLength

    #         # Modifies range of j for if last column
    #         if (n == (columnsOfSquares-1)):
    #             sqWidth = width - ((columnsOfSquares-1)*sqOgWidth)
    #         # line break
    #         with open('photomosaic.html', 'a') as f:
    #                 f.write("<tr><td><nobr>")

    #         for m in range(rowsOfSquares):

    #             # Modifies range of j for if last row
    #             if (m == (rowsOfSquares-1)):
    #                 sqLength = length - ((rowsOfSquares-1)*sqOgLength)

    #             promiddleOfSquare = [0,0,0]

    #             for i in range(sqWidth):
    #                 for j in range(sqLength):
    #                     x = (n*sqOgWidth)+i
    #                     y = (m*sqOgLength)+j
    #                     promiddleOfSquare[0] = ((array[x,y])[0] + promiddleOfSquare[0])//2
    #                     promiddleOfSquare[1] = ((array[x,y])[1] + promiddleOfSquare[1])//2
    #                     promiddleOfSquare[2] = ((array[x,y])[2] + promiddleOfSquare[2])//2
                
    #             # substitute mosaic by image
             
    #             fp_substitute_mosaic_image = self.search_nearest_color_fp(promiddleOfSquare, mosaics_fps, metric)
    #             print("encontrado es: ")
    #             print(fp_substitute_mosaic_image)
    #             table_cell = "<img src=\"{fp}\" width=\"{widt}\" height=\"{height}\">".format(fp = fp_substitute_mosaic_image, widt = "20", height = "30")
    #             with open('photomosaic.html', 'a') as f:
    #                 f.write(table_cell)
    #         with open('photomosaic.html', 'a') as f:
    #                 f.write("</nobr></td></tr> \n")
    #     with open('photomosaic.html', 'a') as f:
    #                 f.write("</table>")
    #     self.update_string.set('100/100')
    
    def htmlPhotoMosaic(self,sqOgLength, sqOgWidth, array, width, length, mosaics_fps):

        if (sqOgLength>width or sqOgWidth > length):
            return

        metric = lambda c1,c2: int(sqrt(
                            pow((c1[0]-c2[0]),2)
                            +pow((c1[1]-c2[1]),2)
                            +pow(abs(c1[2]-c2[2]),2))
                            )


        columnsOfSquares =(width//sqOgWidth)+1
        rowsOfSquares = (length//sqOgLength)+1
        promiddleOfSquare = [0,0,0]
        
        open("photomosaic.html", 'w').close()
        with open('photomosaic.html', 'a') as f:
                    f.write("<table border=\"0\" cellspacing=\"0\" cellpadding=\"0\">")


        sqLength = sqOgLength
        for m in range(rowsOfSquares):

            self.update_string.set("html_photomosaic creation:"+str(int((m/rowsOfSquares)*100)) + '/100%')

            # Modifies range of j for if last row
            if (m == (rowsOfSquares-1)):
                sqLength = length - ((rowsOfSquares-1)*sqOgLength)

            # line break
            with open('photomosaic.html', 'a') as f:
                    f.write("<tr><td><nobr>")

            sqWidth = sqOgWidth
            for n in range(columnsOfSquares):
                
                # Refreshes the square size each column iteration

                # Modifies range of j for if last column
                if (n == (columnsOfSquares-1)):
                    sqWidth = width - ((columnsOfSquares-1)*sqOgWidth)

                promiddleOfSquare = [0,0,0]

                for i in range(sqWidth):
                    for j in range(sqLength):
                        x = (n*sqOgWidth)+i
                        y = (m*sqOgLength)+j
                        promiddleOfSquare[0] = ((array[x,y])[0] + promiddleOfSquare[0])//2
                        promiddleOfSquare[1] = ((array[x,y])[1] + promiddleOfSquare[1])//2
                        promiddleOfSquare[2] = ((array[x,y])[2] + promiddleOfSquare[2])//2
                
                # substitute mosaic by image
             
                fp_substitute_mosaic_image = self.search_nearest_color_fp(promiddleOfSquare, mosaics_fps, metric)
                print("encontrado es: ")
                print(fp_substitute_mosaic_image)
                table_cell = "<img src=\"{fp}\" width=\"{widt}\" height=\"{height}\">".format(fp = fp_substitute_mosaic_image, widt = "20", height = "30")
                with open('photomosaic.html', 'a') as f:
                    f.write(table_cell)
            with open('photomosaic.html', 'a') as f:
                    f.write("</nobr></td></tr> \n")
        with open('photomosaic.html', 'a') as f:
                    f.write("</table>")
        self.update_string.set('100/100')
    
    def blend(self, array, rChannel, gChannel, bChannel, width, length):
        fourTupleFunction = lambda r, g, b: (int(rChannel *(r/255))
                                            ,int(gChannel *(g/255))
                                            ,int(bChannel *(b/255))
                                            ,255
                                            )

        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)
    
    def mica(self, array, rChannel, gChannel, bChannel, width, length):
        fourTupleFunction = lambda r, g, b: (rChannel and r
                                            , gChannel and g
                                            , bChannel and b
                                            ,255
                                            )

        self.pixelPerPixelFilter(array, width, length, fourTupleFunction)
    

root = Tk()  # create root window
root.title("Proyecto Final")  # title of the GUI window
root.maxsize(900, 600)  # specify the max size the window can expand to
root.config(bg="skyblue")  # specify background color
app = Aplication(root)
root.mainloop()

