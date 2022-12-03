from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
import numpy as np
import maze 
from settings import *
from utils import *

class IDGenerator:
    def __init__(self):
        self.id = -1
        
    def genNewID(self):
        self.id += 1
        return self.id
class RigidBody():
    _idGenerator = IDGenerator() # Static variable
    
    def __init__(self, pos, v, result_status=RESULT_TICK_A):
        self.id = RigidBody._idGenerator.genNewID()
        self.pos = pos
        self.v = v
        self.result_status = result_status
        self.collisionTargets = set() # Collided objects to this rigid body
        self.collisionRange = [[False, False]]*3 # Collided constraint lines
        
    # Result Status represents whether current result of Object is belongs to A or B.
    def get_result_status(self):
        return self.result_status
    
    def resetCollision(self):
        for i in range(3):
            for j in range(2):
                self.collisionRange[i][j] = False
        self.collisionTargets = set()
    
    def update(self):
        self.resetCollision() # Reset collisionObjects for new state
        self.pos += self.v*TICK 

    # [RigidBody-RigidBody] Test collision was processed before, if not, return True
    def tryCollideWithTarget(self, target: 'RigidBody'): 
        if target.id in self.collisionTargets:
            return False
        self.collisionTargets.add(target.id)
        target.tryCollideWithTarget(self)
        return True

    # [RigidBody-Line] Test collision was processed before, if not, return True
    def tryCollideWithLine(self, ax, i):
        if self.collisionRange[ax][i]:
            return False
        self.collisionRange[ax][i] = True
        return True
    
    def draw(self):
        pass 
    
class Ball(RigidBody):
    def __init__(self, radius=UNIT_LENGTH*0.5, pos=gen_np_f32_array([0, 0, 0]), v=gen_np_f32_array([0, 0, 0.5])): 
        self.radius = radius
        
        super().__init__(pos, v)
        
    def draw(self):
        glColor3f(0, 1, 1)
        glPushMatrix()
        glTranslatef(*self.pos)
        glutSolidSphere(self.radius, 100, 100)
        glPopMatrix()
        glColor3f(1, 1, 1)

class ConstraintBox():
    def __init__(self, cLines=gen_np_f32_array([[-UNIT_LENGTH, UNIT_LENGTH], [-UNIT_LENGTH, UNIT_LENGTH], [-UNIT_LENGTH, UNIT_LENGTH]])): # Initialize constraint lines
        assert cLines[0][0] < cLines[0][1] and cLines[1][0] < cLines[1][1] and cLines[2][0] < cLines[2][1]
        self.cLines = cLines
        
    def testBall(self, b: Ball): # return (normal vector, error, line) on collision, otherwise 0 vector
        for i in range(3):
            if (b.pos[i]-b.radius) <= self.cLines[i][0]:
                return (EYE_MATRIX[i], (b.radius-(b.pos[i]-self.cLines[i][0])), (i, 0))
            elif (b.pos[i]+b.radius) >= self.cLines[i][1]:
                return (-EYE_MATRIX[i], (b.radius-(self.cLines[i][1]-b.pos[i])), (i, 1))
        
        return (ZERO_VECTOR, ZERO_VECTOR, None) 
class CollisionDetector():
    def __init__(self):
        self.balls = []
        self.constraintBox = ConstraintBox(cLines=gen_np_f32_array([[-3*UNIT_LENGTH, UNIT_LENGTH], [-3*UNIT_LENGTH, 3*UNIT_LENGTH], [-3*UNIT_LENGTH, 3*UNIT_LENGTH]]))
        # TODO: matrix needed
    
    def testAll(self):
        for i in range(len(self.balls)):
            self.testCollisionOnOneBall(self.balls[i])
            for j in range(len(self.balls)):
                if i < j:
                    self.testCollisionOnTwoBalls(self.balls[i], self.balls[j])
                    
    def addBall(self, b):
        # TODO: 
        self.balls.append(b)

    def testCollisionOnOneBall(self, b: Ball):
        normalFromWall, err, line = self.constraintBox.testBall(b)
        
        if np.linalg.norm(normalFromWall) == 0:
            return

        if not b.tryCollideWithLine(*line): # Already triggered
            return
        
        self.triggerOnOneBall(normalFromWall, err, b)
        
    def testCollisionOnTwoBalls(self, b1: Ball, b2: Ball):
        min_dist = b1.radius + b2.radius
        cur_dist = np.linalg.norm(b1.pos-b2.pos)
        
        if min_dist >= cur_dist:
            if not b1.tryCollideWithTarget(b2): # Already triggered
                return 
            err = min_dist-cur_dist
            self.triggerOnTwoBalls(err, b1, b2)
        
        
    def triggerOnOneBall(self, n, err, b):
        
        assert np.linalg.norm(n) == 1

        b.pos = b.pos + n*err # Error correction
        b.v = b.v - (2 * (b.v@n))*n 
        
    def triggerOnTwoBalls(self, err, b1: Ball, b2: Ball):
        normal = b2.pos-b1.pos 
        unitNormal = normal/np.linalg.norm(normal) # unit normal vector from b1 to b2
        
        normalB1 = (b1.v @ unitNormal) * unitNormal
        normalB2 = (b2.v @ unitNormal) * unitNormal
        
        b1.pos = b1.pos - unitNormal*(err/2) # Error correction
        b2.pos = b2.pos + unitNormal*(err/2)
        
        b1.v = b1.v - normalB1 + normalB2
        b2.v = b2.v - normalB2 + normalB1
        

class Viewer:
    def __init__(self):
        self.cameraMatrix = gen_np_f32_array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.mode = 0 # 0: default, 1: rotation, 2: translation
        self.rx = 0
        self.ry = 0
        self.fov = 60
        self.zoom = 1
        self.degx = 0.0
        self.degy = -90.0
        self.trans = gen_np_f32_array([-10*UNIT_LENGTH, UNIT_LENGTH*2, UNIT_LENGTH, .0])
        self.w = 800
        self.h = 800
        self.maze = maze.getMaze(MAP_SIZE)
        self.sample_ball = [
            Ball(pos=gen_np_f32_array([-1*UNIT_LENGTH, 1.5*UNIT_LENGTH, -1*UNIT_LENGTH]), v=gen_np_f32_array([0, 0.5, 0.5])),
            Ball(pos=gen_np_f32_array([-1*UNIT_LENGTH, 1*UNIT_LENGTH, 1*UNIT_LENGTH]), v=gen_np_f32_array([0, 0, 0.5])),
            Ball(pos=gen_np_f32_array([-1*UNIT_LENGTH, 0, 0]), v=gen_np_f32_array([0, -1, 0]))
        ]
        self.collisionDetector = CollisionDetector()
        for ball in self.sample_ball:
            self.collisionDetector.addBall(ball)
            print(ball.id)
        
    def light(self, pos=[0, 50, 100.0, 1]):
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)

        # feel free to adjust light colors
        lightAmbient = [0.0, 0.0, 0.0, 1.0]
        lightDiffuse = [1.0, 1.0, 1.0, 1.0]
        lightSpecular = [0, 1, 0, 1.0]
        
        glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDiffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecular)
        glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.1)
        glLightfv(GL_LIGHT0, GL_POSITION, pos)
        glEnable(GL_LIGHT0)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)
        d = 1
        if self.fov > 0:
            d = 1/np.tan(np.radians(self.fov / 2))

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glScalef(self.zoom, self.zoom, 1)
   
        gluPerspective(self.fov, self.w/self.h, 0.0001, 10000)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        self.cameraMatrix = rotationx(self.degx) @ rotationy(self.degy)
        pos = gen_np_f32_array([0, 0, 0, 0]) @ self.cameraMatrix + self.trans 
        at = gen_np_f32_array([0, 0, -d, 0]) @ self.cameraMatrix + self.trans
        up = (gen_np_f32_array([0, 1, 0, 0])) @ self.cameraMatrix
        self.light(pos=(0, 0, 0, 1.0)) # (pos[0], pos[1], pos[2]
        gluLookAt(*(pos[:3]), *(at[:3]), *(up[:3]))

        glColor3f(1, 1, 1)
        # drawCube(size=(0.1, 0.1, 0.1), pos=(0.1, 0.1, 0.1))
        # glColor3f(0, 0, 1)
        # drawCube(size=(0.1, 0.1, 0.1), pos=(0.3, 0.1, 0.1))
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                if self.maze[i][j] == 1:
                    drawCube(size=(UNIT_LENGTH, UNIT_LENGTH*WALL_HEIGHT, UNIT_LENGTH), pos=(UNIT_LENGTH*i, UNIT_LENGTH*WALL_HEIGHT/2, UNIT_LENGTH*j))
                else:
                    drawCube(size=(UNIT_LENGTH, UNIT_LENGTH*ROAD_HEIGHT, UNIT_LENGTH), pos=(UNIT_LENGTH*i, UNIT_LENGTH*ROAD_HEIGHT/2, UNIT_LENGTH*j))
        
        self.sample_ball[0].update()
        self.sample_ball[1].update()
        self.sample_ball[2].update()
        
        self.collisionDetector.testAll()
        
       
        
        self.sample_ball[0].draw()
        self.sample_ball[1].draw()
        self.sample_ball[2].draw()
        
        glutSwapBuffers()

    def keyboard(self, key, x, y):
        d = 1
        if self.fov > 0:
            d = 1/np.tan(np.radians(self.fov / 2))
        pos = gen_np_f32_array([0, 0, 0, 0]) @ self.cameraMatrix + self.trans 
        at = gen_np_f32_array([0, 0, -d, 0]) @ self.cameraMatrix + self.trans
        up = (gen_np_f32_array([0, 1, 0, 0])) @ self.cameraMatrix
        left, _, front = getCameraVectors(*(pos[:3]), *(at[:3]), *(up[:3]))
        left[1] = 0
        if np.linalg.norm(left) != 0:
            left = left / np.linalg.norm(left)
        left = np.append(left, [0])
        front[1] = 0
        if np.linalg.norm(front) != 0:
            front = front / np.linalg.norm(front)
        front = np.append(front, [0])
        if key == MOVE_FRONT:
            self.trans -= front * VELOCITY
        if key == MOVE_BACK:
            self.trans += front * VELOCITY
        if key == MOVE_RIGHT:
            self.trans -= left * VELOCITY
        if key == MOVE_LEFT:
            self.trans += left * VELOCITY
        if key == b'\x1b':
            exit()

    def special(self, key, x, y):
        if key == 101:
            self.fov += 5
            self.fov = min(self.fov, 90)
        if key == 103:
            self.fov -= 5
            self.fov = max(self.fov, 0)

    def mouse(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON:
            if state == 0:
                self.mode = 1
                self.rx = x
                self.ry = y
            if state == 1:
                self.mode = 0

    def motion(self, x, y):
        if self.mode == 1:
            d = 1
            if x > self.rx:
                self.degy -= d
            if x < self.rx:
                self.degy += d
            if y > self.ry:
                self.degx += d
            if y < self.ry:
                self.degx -= d
            self.degx = max(self.degx, -90)
            self.degx = min(self.degx, 90)
            self.rx = x
            self.ry = y
        if self.mode == 2:
            pos = gen_np_f32_array([0, 0, 1, 0]) @ self.cameraMatrix + self.trans
            at = gen_np_f32_array([0, 0, 0, 0]) + self.trans
            up = gen_np_f32_array([0, 1, 0, 0]) @ self.cameraMatrix
            vx, vy, _ = getCameraVectors(*(pos[:3]), *(at[:3]), *(up[:3]))
            self.trans -= (x - self.rx) * np.append(vx, [0]) * 0.002
            self.trans += (y - self.ry) * np.append(vy, [0]) * 0.002
            self.rx = x
            self.ry = y

    def reshape(self, w, h):
        print(f"window size: {w} x {h}")
        t = min(w, h)
        glViewport(0, 0, w, h)
        self.w = w
        self.h = h

    def timer(self, value):
        glutPostRedisplay()
        glutTimerFunc(1000//FPS, self.timer, FPS)

    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(800, 800)
        glutInitWindowPosition(0, 0)
        glutCreateWindow(b"CS471 Computer Graphics #2")

        self.timer(FPS)
        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.special)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)
        glutReshapeFunc(self.reshape)

        # self.light()

        glutMainLoop()


if __name__ == "__main__":
    viewer = Viewer()
    viewer.run()
