from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

class Aplicacion(Frame):
    self.buffer = Image.new()
    def __init__(self, parent):
        # llama a constructor padre
        super().__init__(parent)
        # Create left and right frames
        self.left_frame = Frame(parent, width=200, height=400, bg='grey')
        self.left_frame.grid(row=0, column=0, padx=10, pady=5)

        self.right_frame = Frame(parent, width=650, height=400, bg='grey')
        self.right_frame.grid(row=0, column=1, padx=10, pady=5)

        # Create frames and labels in left_frame
        Label(self.left_frame, text="Original Image").grid(row=0, column=0, padx=5, pady=5)

        # Select image
        self.to_edit_image_fp = "fp"
        self.select_file()

        self.im = Image.open(self.to_edit_image_fp)
        self.test = ImageTk.PhotoImage(self.im)

        self.im_resized = self.im.resize((300,300))
        self.test_resized = ImageTk.PhotoImage(self.im_resized)
        
        # Frames
        Label(self.right_frame, image=self.test).grid(row=0,column=0, padx=5, pady=5)
        Label(self.left_frame, image=self.test_resized).grid(row=1, column=0, padx=5, pady=5)

        # Create tool bar frame
        self.tool_bar = Frame(self.left_frame, width=180, height=185)
        self.tool_bar.grid(row=2, column=0, padx=5, pady=5)

        # Example labels that serve as placeholders for other widgets
        # Label(self.tool_bar, text="Tools", relief=RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10)  # ipadx is padding inside the Label widget
        # Label(self.tool_bar, text="Filters", relief=RAISED).grid(row=0, column=1, padx=5, pady=3, ipadx=10)

        Label(self.tool_bar, text="Filters", relief=RAISED).grid(row=0, column=1, padx=5, pady=3, ipadx=10)

        self.boton_convertir = Button(
            self.tool_bar, text="ToGray", command=self.convertToGray).grid(row=0, column=2, padx=5, pady=3, ipadx=10)

        # Example labels that could be displayed under the "Tool" menu
        # Label(self.tool_bar, text="Select").grid(row=1, column=0, padx=5, pady=5)


        # open_button = Button(
        #     self.tool_bar,
        #     text='Open a File',
        #     command=self.select_file
        # ).grid(row=0, column=3, padx=5, pady=3, ipadx=10)

        # Label(self.tool_bar, text=self.to_edit_image_fp).grid(row=1, column=2, padx=5, pady=5)

        


        
        # .pack(expand=True)

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
        
    def convertToGray(self):




root = Tk()  # create root window
root.title("P1")  # title of the GUI window
root.maxsize(900, 600)  # specify the max size the window can expand to
root.config(bg="skyblue")  # specify background color


app = Aplicacion(root)

root.mainloop()


# # Example labels that could be displayed under the "Tool" menu
# Label(tool_bar, text="Select").grid(row=1, column=0, padx=5, pady=5)
# Label(tool_bar, text="Crop").grid(row=2, column=0, padx=5, pady=5)
# Label(tool_bar, text="Rotate & Flip").grid(row=3, column=0, padx=5, pady=5)
# Label(tool_bar, text="Resize").grid(row=4, column=0, padx=5, pady=5)
# Label(tool_bar, text="Exposure").grid(row=5, column=0, padx=5, pady=5)