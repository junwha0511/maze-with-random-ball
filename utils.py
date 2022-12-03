from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
import numpy as np
import math
from settings import *

EYE_MATRIX = np.eye(3, dtype=NP_DTYPE)
ZERO_VECTOR = np.zeros(3, dtype=NP_DTYPE)

def gen_np_f32_array(array):
    return np.array(array, dtype=NP_DTYPE)

def abs(x):
    if x < 0:
        return -x
    return x

def getCameraVectors(px, py, pz, ax, ay, az, ux, uy, uz):
    p = gen_np_f32_array([px, py, pz])
    at = gen_np_f32_array([ax, ay, az])
    up = gen_np_f32_array([ux, uy, uz])
    z = p - at
    z = z / np.linalg.norm(z)
    x = np.cross(up, z)
    x = x / np.linalg.norm(x)
    y = np.cross(z, x)
    return (x, y, z)

def rotation(vec, theta):
    uux = vec[0]
    uuy = vec[1]
    uuz = vec[2]

    cos = math.cos(theta)
    sin = math.sin(theta)

    return np.array([
        [cos+uux*uux*(1-cos), uux*uuy*(1-cos)-uuz*sin, uux*uuz*(1-cos)+uuy*sin, 0],
        [uuy*uux*(1-cos)+uuz*sin, cos+uuy*uuy*(1-cos), uuy*uuz*(1-cos)-uux*sin, 0],
        [uuz*uux*(1-cos)-uuy*sin, uuz*uuy*(1-cos)+uux*sin, cos+uuz*uuz*(1-cos), 0],
        [0, 0, 0, 1] 
        ]) 
    
def rotationy(deg):
    deg *= np.pi / 180
    c = np.cos(deg)
    s = np.sin(deg)
    return gen_np_f32_array([[c, 0, -s, 0],
                    [0, 1, 0, 0],
                    [s, 0, c, 0],
                    [0, 0, 0, 1]])

def rotationx(deg):
    deg *= np.pi / 180
    c = np.cos(deg)
    s = np.sin(deg)
    return gen_np_f32_array([[1, 0, 0, 0],
                    [0, c, -s, 0],
                    [0, s, c, 0],
                    [0, 0, 0, 1]])

def f(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def drawCube(size=[0.1, 0.1, 0.1], pos=(0, 0, 0)):
    x, y, z = size
    vertices = (
        (-x/2, -y/2, z/2), (-x/2, -y/2, -z/2), (x/2, -y/2, -z/2), (x/2, -y/2, z/2), 
        (-x/2, y/2, z/2), (-x/2, y/2, -z/2), (x/2, y/2, -z/2), (x/2, y/2, z/2),
    )
    
    surfaces = (
        (TOP_RIGHT_FRONT, BOTTOM_RIGHT_FRONT, BOTTOM_RIGHT_BACK, TOP_RIGHT_BACK),
        (TOP_LEFT_FRONT, TOP_RIGHT_FRONT, TOP_RIGHT_BACK, TOP_LEFT_BACK),
        (TOP_LEFT_FRONT, BOTTOM_LEFT_FRONT, BOTTOM_RIGHT_FRONT, TOP_RIGHT_FRONT),
        (TOP_LEFT_FRONT, TOP_LEFT_BACK, BOTTOM_LEFT_BACK, BOTTOM_LEFT_FRONT),
        (BOTTOM_LEFT_FRONT, BOTTOM_RIGHT_FRONT, BOTTOM_RIGHT_BACK, BOTTOM_LEFT_BACK),
        (TOP_RIGHT_BACK, TOP_LEFT_BACK, BOTTOM_LEFT_BACK, BOTTOM_RIGHT_BACK)
    )
    
    normals = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, -1)
    )
    
    colors = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 0),
        (0, 1, 1),
        (1, 0, 1),
    )
    glBegin(GL_QUADS)
    c = 0
    for s, surface in enumerate(surfaces):
        # glColor3f(*colors[c])
        # glColor3f(1, 1, 1)
        glNormal3f(*(normals[s]))
        for i in surface:
            glVertex3f(*f(vertices[i], pos))	
        c += 1				
    glEnd()
