#########################################################################################################################################
# Archivo recuperado/utilizado del auxiliar 3. No comprendo del todo el uso de shaders fuera de los comentarios ya agregados, por lo que 
# no puedo comentar de manera apropiada o muy extensa las funciones fuera de dichos comentarios.
#########################################################################################################################################

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class SimpleShader():

    def __init__(self):
        # Defining shaders for our pipeline
        vertex_shader = """
            #version 330

            in vec3 position;
            in vec3 color;

            out vec3 newColor;
            void main()
            {
                gl_Position = vec4(position, 1.0f);
                newColor = color;
            }
        """

        fragment_shader = """
            #version 330
            in vec3 newColor;

            out vec4 outColor;
            void main()
            {
                outColor = vec4(newColor, 1.0f);
            }
        """
        # Binding artificial vertex array object for validation
        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)
        # Assembling the shader program (pipeline) with both shaders
        self.shaderProgram = compileProgram(
            compileShader(vertex_shader, GL_VERTEX_SHADER),
            compileShader(fragment_shader, GL_FRAGMENT_SHADER)
        )

    def setupVAO(self, gpuShape):
        
        glBindVertexArray(gpuShape.vao)

        glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)

        position = glGetAttribLocation(self.shaderProgram, "position")
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(position)
        
        color = glGetAttribLocation(self.shaderProgram, "color")
        glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(color)

        glBindVertexArray(0)
    
    def drawCall(self, gpuShape): # Dibuja la imagen en pantalla

        glBindVertexArray(gpuShape.vao)
        glDrawElements(GL_TRIANGLES, gpuShape.size, GL_UNSIGNED_INT, None)
        
        glBindVertexArray(0)


class SimpleTransformShader(SimpleShader):
    
    def __init__(self):
        # Defining shaders for our pipeline
        vertex_shader = """
            #version 330
            
            uniform mat4 transform;

            in vec3 position;
            in vec3 color;

            out vec3 newColor;

            void main()
            {
                gl_Position = transform * vec4(position, 1.0f);
                newColor = color;
            }
            """

        fragment_shader = """
            #version 330
            in vec3 newColor;

            out vec4 outColor;

            void main()
            {
                outColor = vec4(newColor, 1.0f);
            }
            """

        # Binding artificial vertex array object for validation
        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        # Assembling the shader program (pipeline) with both shaders
        self.shaderProgram = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(vertex_shader, OpenGL.GL.GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(fragment_shader, OpenGL.GL.GL_FRAGMENT_SHADER))
        