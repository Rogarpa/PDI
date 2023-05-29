from PIL import Image
import numpy as np
# matriz de combolucion, si encuentra hoyos quiero que 
class Filters:
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
    def dithering(self, array, width, length, propagation_matrix):
        error_buffer = [[0 for x in range(length)] for y in range(width)]
        black = (255,255,255)
        white = (0,0,0)

        radio = len(propagation_matrix)//2


        for x in range(width):
                
            for y in range(length):
                
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

                print((x,y))
                # print(width)
                # print(length)
                error = array[x,y][0] + error_buffer[x][y]

                if(error-0 < (255-error)):
                    array[x,y] = white
                else:
                    array[x,y] = black

                for i in range(x_range):
                    for j in range(y_range):
                        propagation_factor = (propagation_matrix[(start_kernel_coordinate[0]+i)][(start_kernel_coordinate[1]+j)])
                        if(propagation_factor == 0):
                            break
                        else:
                            error_buffer[(start_kernel_coordinate[0]+i)][(start_kernel_coordinate[1]+j)] = propagation_factor * error

    def black(self, array, width, length, propagation_matrix):
        error_buffer = [[0 for x in range(width)] for y in range(length)]
        black = (255,255,255)
        white = (0,0,0)

        for x in range(width):
                
            for y in range(length):
                error = array[x,y][0]
                if(error-0 < (255-error)):
                    array[x,y] = white
                else:
                    array[x,y] = black
    def steinbergDithering(self, array, width, length):
        div = 1/16
        steinberg_propagation_matrix = [[0,0,0]
                                    ,[0,0,7*div]
                                    ,[3*div,5*div,div]
                                   ]
        self.dithering(array, width, length,steinberg_propagation_matrix)
    def jarvisDithering(self, array, width, length):
        div = 1/48
        jarvis_propagation_matrix = [[0,0,0,0,0]
                                    ,[0,0,0,0,0]
                                    ,[0,0,0,7*div,5*div]
                                    ,[3*div,5*div,7*div,5*div,3*div]
                                    ,[1*div,3*div,5*div,3*div,1*div]
                                   ]
        self.dithering(array, width, length, jarvis_propagation_matrix)

size =500


im = Image.open('forest.jpg')

pixelMap = im.load()
# pixelMap = im.resize((size,size)).load()

proof = Image.new( im.mode, (size, size))
pixelProof = proof.load()


width = im.size[0]
length = im.size[1]
# width = proof.size[0]
# length = proof.size[1]
f = Filters()

div = 1/16
convolution_matrix_proof = [[0,0,0],[0,0,7*div], [3*div,5*div,div]]

# f.convolution_kernel_filter(pixelMap, width, length, convolution_matrix_proof)

# f.black(pixelMap, width, length, convolution_matrix_proof)
# f.dithering(pixelMap, width, length, convolution_matrix_proof)
# f.jarvisDithering(pixelMap, width, length)
f.steinbergDithering(pixelMap, width, length)

# convolution_kernel_filter(pixelMap, size,size, convolution_matrix_proof)
# prueba_convolution(pixelProof, width, length, convolution_matrix_proof)
# prueba_convolution(pixelMap, size,size, convolution_matrix_proof)

im.show()
# proof.show()

# im.save('foresb.jpg')