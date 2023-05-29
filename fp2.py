from PIL import Image
import numpy as np

class Filters:
    def prueba_convolution(self,array, width, length, kernel_matrix):
        intervalo = 8

        radio = len(kernel_matrix)//2

        for y in range(0,length,intervalo):
            
            # Refreshes the square size each column iteration

            
            # matrix_buffer = [[0] * kernel_matrix_size for i in range(kernel_matrix_size)]

            for x in range(0,width,intervalo):
                start_matrix_coordinate = [0,0]
                start_kernel_coordinate = [0,0]

                pixel_buffer = (0,0,0)

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

                print((x,y))
                print('radio' + str(radio))
                print(start_matrix_coordinate)
                print(start_kernel_coordinate)
                print(padding_x_left)
                print(padding_x_right)
                # print(y_range)

                for i in range(x_range):
                    for j in range(y_range):
                        
                        array[((start_matrix_coordinate[0])+i),((start_matrix_coordinate[1])+j)] = (kernel_matrix[(start_kernel_coordinate[0]+i)][(start_kernel_coordinate[1]+j)]
                                    ,kernel_matrix[(start_kernel_coordinate[0]+i)][(start_kernel_coordinate[1]+j)]
                                    ,kernel_matrix[(start_kernel_coordinate[0]+i)][(start_kernel_coordinate[1]+j)])
                
                            

    def convolution_kernel_filter(self,array, width, length, kernel_matrix):
        # falta probar que kernel tenga sentido
        radio = len(kernel_matrix)//2

        for x in range(width):
            
            # Refreshes the square size each column iteration

            
            # matrix_buffer = [[0] * kernel_matrix_size for i in range(kernel_matrix_size)]

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
    
# def blur(array, width, length):
    




size =500


im = Image.open('forest.jpg')

pixelMap = im.load()
# pixelMap = im.resize((size,size)).load()

proof = Image.new( im.mode, (size, size))
pixelProof = proof.load()

div = 1/5

width = im.size[0]
length = im.size[1]
# width = proof.size[0]
# length = proof.size[1]
# convolution_matrix_proof = [[div,div,div],[div,div,div], [div,div,div]]
# convolution_matrix_proof = [[div,div,div,div,div],[div,div,div,div,div],[div,div,div,div,div],[div,div,div,div,div],[div,div,div,div,div]]
# convolution_matrix_proof = [[0,div,0],[div,div,div], [0,div,0]]
# convolution_matrix_proof = [[0,0,div,0,0],[0,div,div,div,0],[0,0,div,0,0],[0,div,div,div,0], [0,0,div,0,0]]


f = Filters()

# convolution_matrix_proof = [[0,div,0],[div,div,div], [0,div,0]]

# f.convolution_kernel_filter(pixelMap, width, length, convolution_matrix_proof)
# convolution_kernel_filter(pixelMap, size,size, convolution_matrix_proof)
# prueba_convolution(pixelProof, width, length, convolution_matrix_proof)
# prueba_convolution(pixelMap, size,size, convolution_matrix_proof)

# f.blur(pixelMap, width, length)
# f.motion_blur(pixelMap, width, length)
# f.finde_edges(pixelMap, width, length)
# f.sharpen(pixelMap, width, length)
# f.emboss(pixelMap, width, length)
# f.mean(pixelMap, width, length)

im.show()
# proof.show()

# im.save('foresb.jpg')