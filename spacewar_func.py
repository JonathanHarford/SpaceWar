"""Handy functions for my Spacewar program"""

import math, os, pygame
from pygame.locals import *  # pygame constants, like "K_ESCAPE".

DISP_WIDTH, DISP_HEIGHT = (800, 600)
SOUND = 1
FPS = 30  # frames per second

WALLS = 1           # Does the universe have bouncy walls? Or is it toroidal?
GRAV_CONST = 0.01   # I like to make this very low, and the sun(s) massive.

SHIP1_THRUST_KEY = K_w
SHIP1_LEFT_KEY =   K_a
SHIP1_RIGHT_KEY =  K_d
SHIP1_SHOOT_KEY =  K_q

SHIP2_THRUST_KEY = K_i
SHIP2_LEFT_KEY   = K_j
SHIP2_RIGHT_KEY  = K_l
SHIP2_SHOOT_KEY  = K_k

SUN_MASS = 2500          # Mass of Sun. 0 = no sun
MAXSPEED = 30
SHIP_ROTATE = 10  # How many degrees a ship can turn in a tick.
THRUST = 0.1
START_ENERGY = 10  # Eventually, 100
CRASH_PAIN = 5
SHOT_SPEED = 6
SHOT_LIFESPAN = 250
SHOT_DELAY = 15
SHOT_PAIN = 5

def sin(x):
	"A sin() for degrees (which pygame prefers)"
	return math.sin(math.pi*x/180)

def cos(x):
	"A cos() for degrees (which pygame prefers)"
	return math.cos(math.pi*x/180)

def dist_sqrd(a,b):
	"Distance (squared) between two points (points == sequence types of length 2)"
	return (a[0] - b[0])**2 + (a[1] - b[1])**2

def normalize(r,n=1):
	"Returns 2-vector r but with a length of n"
	return n * r / math.hypot(r[0],r[1])

# This should be a Body method, right?
def bounce(a,b):
	'''This original "billiard-ball" collision method has loads of
	redundancies, but is relatively easy to understand.'''

	fv = (a.mass * a.v + b.mass * b.v) / (a.mass + b.mass) # Velocity of the center of momentum
	fp = (a.mass * a.p + b.mass * b.p) / (a.mass + b.mass)

	# These are the velocities of the ships in the center of momentum frame.
	fav = a.v - fv
	fbv = b.v - fv

	fap = a.p - fp
	fbp = b.p - fp

	dist  = math.sqrt(dist_sqrd(fap,fbp))
	speed = math.hypot(fav[0],fav[1])
	sinA = -( (fbp[0]-fap[0])*fav[1] - (fbp[1]-fap[1])*fav[0] ) / (dist*speed)
	cosA =  ( (fbp[0]-fap[0])*fav[0] + (fbp[1]-fap[1])*fav[1] ) / (dist*speed)

	# Calculate the new velocities (in the c of m frame).
	fav = -((cosA*cosA-sinA*sinA)*fav[0] - (2*sinA*cosA)*fav[1]),-((2*sinA*cosA)*fav[0] + (cosA*cosA-sinA*sinA)*fav[1])
	fbv = -((cosA*cosA-sinA*sinA)*fbv[0] - (2*sinA*cosA)*fbv[1]),-((2*sinA*cosA)*fbv[0] + (cosA*cosA-sinA*sinA)*fbv[1])

	# Transform back to original frame
	a.v = fav + fv
	b.v = fbv + fv


def load_image(name):
	"Loads image from data directory. Returns the image itself and its bounding rectangle"
	fullname = os.path.join('data', name)
	try:
		image = pygame.image.load(fullname).convert_alpha()
	except pygame.error, message:
		print 'Cannot load image:', fullname
		raise SystemExit, message
	return image, image.get_rect()

def load_sound(name):
	"Loads sound (wav) from data directory"
	class NoneSound:
		def play(self): pass
	if not pygame.mixer or not pygame.mixer.get_init():
		return NoneSound().play
	fullname = os.path.join('data', name)
	try:
		soundplayer = pygame.mixer.Sound(fullname).play
	except pygame.error, message:
		print 'Cannot load sound:', fullname
		raise SystemExit, message
	return soundplayer
