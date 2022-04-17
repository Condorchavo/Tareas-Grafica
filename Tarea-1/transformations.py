#########################################################################################################################################
# Archivo recuperado/utilizado del auxiliar 3
#########################################################################################################################################

import numpy as np

def translate(tx, ty, tz): # Genera la matriz de traslación para los parámetros entregados
    return np.array([
        [1,0,0,tx],
        [0,1,0,ty],
        [0,0,1,tz],
        [0,0,0,1]], dtype = np.float32)


def scale(sx, sy, sz): # Genera la matriz de escalamiento para los parámetros entregados
    return np.array([
        [sx,0,0,0],
        [0,sy,0,0],
        [0,0,sz,0],
        [0,0,0,1]], dtype = np.float32)


def rotationX(theta): # Genera la matriz de rotación con respecto al eje X
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [1,0,0,0],
        [0,cos_theta,-sin_theta,0],
        [0,sin_theta,cos_theta,0],
        [0,0,0,1]], dtype = np.float32)


def rotationY(theta): # Genera la matriz de rotación con respecto al eje Y
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [cos_theta,0,sin_theta,0],
        [0,1,0,0],
        [-sin_theta,0,cos_theta,0],
        [0,0,0,1]], dtype = np.float32)


def rotationZ(theta): # Genera la matriz de rotación con respecto al eje Z
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    return np.array([
        [cos_theta,-sin_theta,0,0],
        [sin_theta,cos_theta,0,0],
        [0,0,1,0],
        [0,0,0,1]], dtype = np.float32)


def matmul(mats): # Multiplica las matrices quue se le entregan
    out = mats[0]
    for i in range(1, len(mats)):
        out = np.matmul(out, mats[i])

    return out


