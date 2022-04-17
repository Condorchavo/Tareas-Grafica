import glfw
from math import cos, sin, pi
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import transformations as tr
from gpu_shape import GPUShape
from easy_shaders import SimpleTransformShader


class figures: # Se crea una clase para las figuras
    def __init__(self, x = 0, y = 0):
        self.color = (0, 0, 0)
        self.vertices = []
        self.indices = []
        self.x = x
        self.y = y
    
    
    def rgb(self, color = None): # Entrega el color en la escala rgb que tendrá la figura
        if isinstance(color, int):
            self.color = (color, color, color)
        else:
            if color == "hitbox":
                self.color = (10, 10, 10)
            elif color == None:
                self.color = (0, 0, 0)
            else:
                l = len(color)
                r = ord(color[0%l]) * ord(color[1%l]) % 255
                g = ord(color[2%l]) * ord(color[3%l]) % 255
                b = ord(color[4%l]) * ord(color[5%l]) % 255
                self.color = (r, g, b)


    def insercion(self, figura): # Inserta los vértices de una figura en el arreglo que contiene las de otra 
                             # tal que se tenga un único arreglo que cree ambas figuras
        (v, i) = (self.vertices, self.indices)
        (v1, i1) = (figura.vertices, figura.indices)

        size = len(v)/6

        for j in range(len(i1)):
            i1[j] +=size
        self.vertices = np.append(v, v1)
        self.indices = np.append(i, i1)
    
    def escalar(self, w, h): # Escala la figura "w" en el eje x, y "h" en el eje y
        for j in range(len(self.vertices)):
            if (j%6) == 0:
                self.vertices[j] = self.vertices[j]*w
            if (j%6) == 1:
                self.vertices[j] = self.vertices[j]*h


    def square(self, lado, color = "Vicente"): # Genera un cuadrado
        l = lado/2  
        self.rgb(color)        
        (r, g, b) = self.color
        (x, y) = (self.x, self.y)

        # Genera los vértices del cuadrado, y los puntos que debe unir para generar triángulos
        self.vertices = np.array([
        #   positions        colors
            -l + x, -l + y, 0.0,  r/255, g/255, b/255,
            l + x, -l + y, 0.0,  r/255, g/255, b/255,
            l + x,  l + y, 0.0,  r/255, g/255, b/255,
            -l + x, l + y, 0.0,  r/255, g/255, b/255
            ], dtype = np.float32)
        self.indices = np.array(
            [0, 1, 2,
            2, 3, 0], dtype= np.uint32)


    def rectangle(self, width, height, color = "Vicente"): # Genera un rectángulo
        a = width/2
        h = height/2
        self.rgb(color)        
        (r, g, b) = self.color
        (x, y) = (self.x, self.y)

        vertexData = np.array([
        #   positions        colors
            -a + x, -h + y, 0.0,  r/255, g/255, b/255,
            a + x, -h + y, 0.0,  r/255, g/255, b/255,
            a + x,  h + y, 0.0,  r/255, g/255, b/255,
            -a + x, h + y, 0.0,  r/255, g/255, b/255
            ], dtype = np.float32)

        indices = np.array(
            [0, 1, 2,
            2, 3, 0], dtype= np.uint32)

        self.vertices = vertexData
        self.indices = indices


    def triangle(self, base, height, color = "Vicente"): # Genera un triángulo
        self.rgb(color)        
        (r, g, b) = self.color
        a = base/2 
        h = height
        (x, y) = (self.x, self.y)

        self.vertices = np.array([
        #   positions        colors
            -a + x, -0.0 + y, 0.0,  r/255, g/255, b/255,
            0.0 + x, h + y, 0.0,  r/255, g/255, b/255,
            a + x,  0.0 + y, 0.0,  r/255, g/255, b/255,
            ], dtype = np.float32)

        self.indices = np.array(
        [0, 1, 2], dtype= np.uint32)
        

    def semicirc(self, N, rad, x = 0, y = 0, color = "Vicente"): #Genera un semi-círculo de radio rad con N puntos
        self.rgb(color)        
        (r, g, b) = self.color
        vertexData = [x, y, 0, r/255, g/255, b/255]
        indices = []
        
        for i in range(N):
            ang = i*pi/(N-1)
            vertexData += [rad*cos(ang) + x, rad*sin(ang) + y, 0, r/255, g/255, b/255]
            indices += [0, i, i + 1]

        self.vertices = np.array(vertexData, dtype=np.float32)
        self.indices = np.array(indices, dtype= np.uint32)

    def puerta(self, width, height, x = 0, y = 0, color = "hitbox"): #Puerta del castillo
        self.rgb(color)
        (r, g, b) = self.color
        (w, h) = (width/2, height)
        fig = figures()

        self.x += x
        self.y += y + h/2

        self.rectangle(2*w, h, color)
        fig.semicirc(20, w, self.x , h/2 + self.y, color)
        self.insercion(fig)
    

    def castillo(self, width, height, ancho, alto): #Junta distintas figuras para crear la figura principal (castillo)
        a = ancho/(width) * 2
        h = alto/(height) * 2

        #Genera las distintas figuras que conforman al castillo
        fig1 = figures(0, -0.2)
        fig1.rectangle(0.9, 0.6)
        fig2 = figures(0.35, 0.2)
        fig2.square(0.2)
        fig3 = figures(-0.35, 0.2)
        fig3.square(0.2)
        fig4 = figures(0, 0.175)
        fig4.rectangle(0.3, 0.15)
        fig5 = figures(0, -0.5)
        fig5.puerta(0.17, 0.21)
        fig6 = figures(0.35, 0.3)
        fig6.triangle(0.2, 0.1)
        fig7 = figures(-0.35, 0.3)
        fig7.triangle(0.2, 0.1)
        fig8 = figures(0, 0.25)
        fig8.triangle(0.3, 0.1)
        
        (v1, i1) = (fig1.vertices, fig1.indices)
        (v2, i2) = (fig2.vertices, fig2.indices)
        (v3, i3) = (fig3.vertices, fig3.indices)
        (v4, i4) = (fig4.vertices, fig4.indices)
        (v5, i5) = (fig5.vertices, fig5.indices)
        (v6, i6) = (fig6.vertices, fig6.indices)
        (v7, i7) = (fig7.vertices, fig7.indices)
        (v8, i8) = (fig8.vertices, fig8.indices)

        #Une todas las figuras en una sola
        self.insercion(fig1)
        self.insercion(fig2)
        self.insercion(fig3)
        self.insercion(fig4)
        self.insercion(fig5)
        self.insercion(fig6)
        self.insercion(fig7)
        self.insercion(fig8)
        
        self.escalar(a, h)

    def hitbox(self, width, height, ancho, alto, x = 0, y = 0): # Genera un cuadro para un ancho y 
                                                                        #alto determinados, en función de las dimensiones de la ventana
        # Defining locations and colors for each vertex of the shape
        #####################################
        (r, g, b) = (10, 10, 10)
        a = (ancho/width)
        h = (alto/height)
        (self.x, self.y) = (x, y)
        self.rectangle(2*a, 2*h, "hitbox") # Genera la hitbox

        fig = figures()
        fig.castillo(width, height, ancho, alto) # Genera el castillo
        (v, i) = (fig.vertices, fig.indices)

        self.insercion(fig) # Se une la hitbox y el castillo

    

