from PIL import Image
import numpy as np
# matriz de combolucion, si encuentra hoyos quiero que 
class Filters:
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

    def atandt(self, array, width, length, bar_length, wave_padding):
        for y in range(0,length,bar_length):
            for x in range(width):
                for white_padding in range(wave_padding):
                    array[x,y+white_padding] = (255,255,255)
            
            y = y + wave_padding

            for x in range(width):
                    
                padding_y_down = length-y
                if(padding_y_down > bar_length):
                    padding_y_down = bar_length
                

                number_of_black_pixels = 0

                for l in range(padding_y_down):
                    if(array[x,y+l][0] == 0):
                        number_of_black_pixels += 1
                    # cuenta pero no pone blanco
                    array[x,y+l] = (255,255,255)
                vertical_centering = (padding_y_down-number_of_black_pixels)//2
                for black in range(number_of_black_pixels):
                        array[x,vertical_centering+y+black] = (0,0,0)
                
    def white(self, array, width, length):
        for x in range(width):
            for y in range(length):
                array[x,y] = (255,255,255)

size =500


im = Image.open('at.jpg')

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

f.white(pixelProof, proof.size[0], proof.size[1])
# f.convolution_kernel_filter(pixelMap, width, length, convolution_matrix_proof)

# f.black(pixelMap, width, length, convolution_matrix_proof)
# f.dithering(pixelMap, width, length, convolution_matrix_proof)
# f.jarvisDithering(pixelMap, width, length)
# f.steinbergDithering(pixelMap, width, length)
f.atandt(pixelMap, width, length,10,2)
# f.atandt(pixelProof, proof.size[0], proof.size[1],2)

# convolution_kernel_filter(pixelMap, size,size, convolution_matrix_proof)
# prueba_convolution(pixelProof, width, length, convolution_matrix_proof)
# prueba_convolution(pixelMap, size,size, convolution_matrix_proof)

im.show()
# proof.show()

# im.save('foresb.jpg')