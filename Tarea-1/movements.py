from figuras import *

class movements:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vel_x = 1
        self.vel_y = 1
        self.rebote = 0

    def dibujar(self, pipeline, S): # Se encarga de las transformaciones que se debe realizar al objeto en cada rebote
        if self.rebote == 1 or self.rebote == 3: # En estos casos escala a la figura
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
                tr.translate(self.x, self.y, 0.0), tr.scale(600/800 * S, 800/600 * S, 1), tr.rotationZ((self.rebote) * pi/2) 
                ]))
        else: #En este caso no realiza ningún escalamiento de la figura
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
                tr.translate(self.x, self.y, 0.0), tr.rotationZ((self.rebote) * pi/2) 
                ]))


    def desplazar(self, dx, dy): # Genera un desplazamiento en la figura de valor "x" en el eje x, e "y" en el eje y
        self.x += dx*self.vel_x
        self.y += dy*self.vel_y
    

    def choque(self, pipeline, S, dx, dy): # Ve los casos de borde para la figura cuando está en escala normal
        # (0.2 * 600/800 * S) y (0.2 * 800/600 * S) son las nuevas distancias desde los bordes 
        # de la figura al centro (luego de escalar la figura)

        if self.x >= 1 - 0.2 and (dx*self.vel_x) > 0: #Caso en que choca con el borde derecho
            self.vel_x = -self.vel_x
            self.rebote = (self.rebote + 1)%4
            # Se desplaza de forma de que la figura no salga del borde
            self.x = 1 - 0.2 * 600/800 * S 

        elif self.x <= -1 + 0.2 and (dx*self.vel_x) < 0: #Caso en que choca con el borde izquierdo
            self.vel_x = -self.vel_x
            self.rebote = (self.rebote + 1)%4
            # Se desplaza de forma de que la figura no salga del borde
            self.x = -1 + 0.2 * 600/800 * S

        if self.y >= 1 - 0.2 and (dy*self.vel_y) > 0: #Caso en que choca con el borde superior
            self.vel_y = -self.vel_y
            self.rebote = (self.rebote + 1)%4
            # Se desplaza de forma de que la figura no salga del borde
            self.y = 1 - 0.2 * 800/600 * S

        elif self.y <= -1 + 0.2 and (dy*self.vel_y) < 0: #Caso en que choca con el borde inferior
            self.vel_y = -self.vel_y
            self.rebote = (self.rebote + 1)%4
            # Se desplaza de forma de que la figura no salga del borde
            self.y = -1 + 0.2 * 800/600 * S
    

    def choque_escalado(self, pipeline, S, dx, dy): # Ve los casos de borde para la figura cuando está escalada
        # (0.2 * 600/800 * S) y (0.2 * 800/600 * S) son las distancias desde los bordes de la figura al centro 
        # cuando la figura está escalada

        if self.x >= 1 - 0.2 * 600/800 * S  and (dx*self.vel_x) > 0:#Caso en que choca con el borde derecho
            self.vel_x = -self.vel_x
            self.rebote = (self.rebote + 1)%4
            # Se desplaza de forma de que la figura no salga del borde
            self.x = 1 - 0.2

        elif self.x <= -1 + 0.2 * 600/800 * S and (dx*self.vel_x) < 0: #Caso en que choca con el borde izquierdo
            self.vel_x = -self.vel_x
            self.rebote = (self.rebote + 1)%4
            # Se desplaza de forma de que la figura no salga del borde
            self.x = -1 + 0.2

        if self.y >= 1 - 0.2 * 800/600 * S and (dy*self.vel_y) > 0: #Caso en que choca con el borde superior
            self.vel_y = -self.vel_y
            self.rebote = (self.rebote + 1)%4
            # Se desplaza de forma de que la figura no salga del borde
            self.y = 1 - 0.2

        elif self.y <= -1 + 0.2 * 800/600 * S and (dy*self.vel_y) < 0: #Caso en que choca con el borde inferior
            self.vel_y = -self.vel_y
            self.rebote = (self.rebote + 1)%4
            # Se desplaza de forma de que la figura no salga del borde
            self.y = -1 + 0.2