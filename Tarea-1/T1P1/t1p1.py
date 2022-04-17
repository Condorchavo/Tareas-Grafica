# coding=utf-8
######################################################################
"""Tarea 1 parte 1: Salvapantallas DVD"""
# Nombre: Vicente Gatica Pérez
######################################################################

import sys
from movements import *
from figuras import *

if len(sys.argv) == 4:
    nombre = sys.argv[1]
    iniciales = sys.argv[2]
    RUT = int(sys.argv[3])
else:
    nombre = ""
    iniciales = ""
    RUT = 0


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    #Se define un objeto de la clase movements para modelar el movimiento de la figura
    fig = movements()

    # Se define el ancho y alto de la ventana
    width = 800
    height = 600

    # Se definen ancho y alto de la hitbox
    ancho = 160
    alto = 120

    window = glfw.create_window(width, height, "Tarea 1 parte 1: Salvapantallas DVD", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)
 
    # Creating our shader program and telling OpenGL to use it

    pipeline = SimpleTransformShader()
    glUseProgram(pipeline.shaderProgram)

    # Define el color de fondo de la ventana
    glClearColor(0, 0, 0, 1.0)

    #Se define el tiempo inicial
    t0 = glfw.get_time()

    #Parámetros para el escalamiento
    S = (20658195/20000000)**3

    

##########################################################################################################################################

    while not glfw.window_should_close(window):
        t1=glfw.get_time()
        dt = t1 - t0 # Se guarda la diferencia de tiempo entre dos "ciclos" dentro del while
        t0 = t1 # Se almacena el tiempo final como el tiempo inicial para la siguiente vez que entre en el ciclo

        # Se genera la figura y se envía a la gpu
        figura = figures(0, 0)
        figura.hitbox(width, height, ancho, alto)   
        (a1, b1) = (figura.vertices, figura.indices)
        gpuC1 = GPUShape().initBuffers()
        pipeline.setupVAO(gpuC1)
        gpuC1.fillBuffers(a1, b1)

        glfw.poll_events()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glClear(GL_COLOR_BUFFER_BIT)
        
        #Se genera la velocidad en cada eje
        iniciales= "VG" # Las iniciales del nombre y apellido
        alpha = ord(iniciales[0]) * ord(iniciales[1])
        x = 350 * cos(alpha) / 800
        y = 350 * sin(alpha) / 600

        #Se define la variación de la posición
        (dx, dy) = (x*dt, y*dt)
        
        if fig.rebote == 1 or fig.rebote == 3: # Representa los casos en que la figura debe estar escalada
            fig.choque_escalado(pipeline, S, dx, dy)
            fig.desplazar(dx, dy)
        else: # Representa los casos en que la figura está en escala normal
            fig.choque(pipeline, S, dx, dy)
            fig.desplazar(dx, dy)
            
        # Se almacena la figura junto con sus respectivas transformaciones
        fig.dibujar(pipeline, S)

        # Se dibuja en la ventana la figura
        pipeline.drawCall(gpuC1)
        
        glfw.swap_buffers(window)
    
    # Se borran los valores almacenados de la figura al cerrar la ventana
    gpuC1.clear()
    glfw.terminate()
