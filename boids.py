"""
Extra rules to implement:
-tend_to_place
-perching
-scattering the flock

Keeping the boids on screen? right now there is no limiter in movement as to
	where a boid can move to

"""

import random
import math
from time import sleep
from tkinter import *


############################## GLOBAL CONSTANTS ###############################

HEIGHT = 1000 		# Height of screen in px - small for testing
WIDTH = 1000  		# Width of screen in px - small for testing
BOID_LENGTH = 20
BOIDS_NUM = 20    	# Number of boids to animate
SPEED_LIMIT = 20	# max amount of pixels to move in any direction
XMIN = 0			# min x position boids should go
YMIN = 0			# min y position boids should go
ZONE_SIZE = 100		
SEP_SIZE = 50		# how far boids should stay from eachother

###############################################################################


"""
A 2D vector class with the two elements represented as x and y
-Contains vector addition, subtraction, division, etc. functions
"""
class vector:
	# initialize the vector for a given x and y
	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)

	# represent the vector - dont think this will be needed
	def __repr__(self):
		return 'x = ' + str(self.x) + ', y = ' + str(self.y)

	# add two vectors and return the resulting vector
	def __add__(self, other):
		return vector(self.x + other.x, self.y + other.y)

	# subtract two vectors and return the resulting vector
	def __sub__(self, other):
		return vector(self.x - other.x, self.y - other.y)

	# multiply two vectors and return the resulting vector
	def __mul__(self, other):
		return vector(self.x * other, self.y * other)

	# divide two vectors and return the resulting vector
	def __div__(self, other):
		return vector(self.x / other, self.y / other)

	# add another vector to this vector
	def __iadd__(self, other):
		self.x += other.x
		self.y += other.y
		return self

	# subtract another vector from this vector
	def __isub__(self, other):
		self.x -= other.x
		self.y -= other.y
		return self

	# divide this vector by another vector
	def __itruediv__(self, other):
		if isinstance(other, vector):
			self.x /= other.x if other.x else 1
			self.y /= other.y if other.y else 1
		else:
			self.x /= other
			self.y /= other
		return self

	# return the magnitude of this vector
	def mag(self):
		return ((self.x ** 2) + (self.y ** 2)) ** 0.5

"""
Class for a boid
-Attributes:
	position = a 2D vector where:
		position.x = x coorditate of boid
		position.y = y coorditate of boid
	velocity = a 2D vector where:
		velocity.x = velocity boid is moving along the x axis
		velocity.y = velocity boid is moving along the y axis
-Functions:
	random_start = initialize x and y as random while keeping in the defined
		width and height of the screen
	rule1, rule2, and rule3 are the the cohesion, separation, and alignment
		rules respectively
"""
class boid:
	#initialize with random starting point and velocity of 0
	def __init__(self, width, height):
		self.velocity = vector(0,0)
		self.position = self.random_start(width, height)

	# Return a vecotr with a random position within the bounds of the screen
	def random_start (self, width, height):
		y = random.randint(0, height)
		x = random.randint(0, width)
		return vector(x,y)
		# note that with this starting method it is possible to start 2 boids 
		# in the same location, though as the size of the screen grows, the
		# liklihood of this happening decreases

	# move a boid
	# *plan = have bools indicating whether or not to apply a given rule for 
	#	demonstration purposes 
	def move(self, boids, limitSpeed, boundPos, wind):
		v1 = self.rule1(boids)
		v2 = self.rule2(boids)
		v3 = self.rule3(boids)
		self.velocity += v1 + v2 + v3
		# speed limit check
		self.bound_position()
		if (self.velocity.mag() > SPEED_LIMIT):
			self.velocity /= self.velocity.mag() 
			self.velocity *= SPEED_LIMIT
		#if boundPos:
		self.bound_position()
		if wind:
			self.strong_wind()
		self.position += self.velocity
		


	# Flock cohesion
	def rule1(self, boids):
		vec = vector(0,0)
		for b in boids:
			if b is not self:
				vec += b.position
		vec /= len(boids) - 1
		res = (vec - self.position)
		res /= 100
		return res

	# Separation
	def rule2(self, boids):
		vec = vector(0,0)
		for b in boids:
			if b is not self:
				if (b.position - self.position).mag() < SEP_SIZE:
					vec -= (b.position - self.position)
		return vec

	# Alignment
	def rule3(self, boids):
		vec = vector(0,0)
		for b in boids:
			if b is not self:
				vec += b.velocity
		vec /= len(boids) - 1
		res = (vec - self.velocity)
		res /= 8
		return res

	# Keep boids on screen - extra tweak
	def bound_position(self):
		if self.position.x < XMIN:
			self.velocity.x += 10
		if self.position.y < YMIN:
			self.velocity.y += 10
		if self.position.x > HEIGHT:
			self.velocity.x -= 10
		if self.position.y > WIDTH:
			self.velocity.y -= 10

	# Wind simulation - extra tweak
	def strong_wind(self):
		wind = vector(5, 5) # define the wind direction and velocity
		self.velocity += wind




"""
Draws the boids to the canvas
"""
def draw_boids(window,canvas,boids):
	
	#draw boids
	for boid in boids:
		centerX = boid.position.x
		centerY = boid.position.y
		vectorX = boid.velocity.x
		vectorY = boid.velocity.y
		
		a = ((centerX),(centerY - 2*(BOID_LENGTH/3)))
		b = ((centerX - BOID_LENGTH/3),(centerY + BOID_LENGTH/3))
		c = ((centerX + BOID_LENGTH/3),(centerY + BOID_LENGTH/3))

		if (vectorX != 0):

			angle = math.atan2(vectorX,vectorY)
			
			if angle < 0:
				angle = 2*math.pi + angle
				
			if angle < math.pi:
				angle = math.pi - angle
				
			if angle > math.pi:
				angle = angle - math.pi
				angle = 2*math.pi - angle
	
			a = ((centerX + math.cos(angle) * (a[0] - centerX) - math.sin(angle) * (a[1] - centerY)),
				(centerY + math.sin(angle) * (a[0] - centerX) + math.cos(angle) * (a[1] - centerY)))
			
			b = ((centerX + math.cos(angle) * (b[0] - centerX) - math.sin(angle) * (b[1] - centerY)),
				(centerY + math.sin(angle) * (b[0] - centerX) + math.cos(angle) * (b[1] - centerY)))
			
			c = ((centerX + math.cos(angle) * (c[0] - centerX) - math.sin(angle) * (c[1] - centerY)),
				(centerY + math.sin(angle) * (c[0] - centerX) + math.cos(angle) * (c[1] - centerY)))
			
		canvas.create_polygon(a,b,c)
			
	canvas.pack()
	window.update()
	sleep(0.1)
	canvas.delete(ALL)
	
	
"""
Initializes a list of n boids
"""
def initialize():
	boids = [boid(WIDTH, HEIGHT) for b in range(BOIDS_NUM)]
	return boids

"""
Moves a list of boid
"""
def move_boids(boids, limitSpeed, boundPos, wind):
	for b in boids:
		b.move(boids, limitSpeed, boundPos, wind)
	return boids

"""
Animate one frame for a list of boids
"""
"""
def draw(boids):
	#testDraw(boids) # redirect to testing method
	draw_boids(boids)
"""

"""
Testing function in absence of animation
Simulates with a list in which a 0 represents a boid
"""
def testDraw(boids):
	screen = [[0 for i in range(HEIGHT+1)] for j in range(WIDTH)]
	for b in boids:
		try:
			x = int(b.position.x)
			y = int(b.position.y)
			print(b.position) # debug
			if (screen[x][y] == 1):
				# if triggered on first iteration, this is not an unforseen 
				# error, and should correct itself after initialization
				raise Exception("Collision at x:" + b.position.x 
					+ " y:" + b.position.y)
			else:
				screen[x][y] = 1
		except Exception as e:
			print(e)
	for row in screen:
		print("|", end='')
		for element in row:
			if element == 0:
				print(' ', end='')
			else:
				print('0', end='')
		print("|")
	


def main():
	boids = initialize()
	#creates gui canvas
	window = Tk()
	canvas = Canvas(window,width=WIDTH,height=HEIGHT)
	draw_boids(window,canvas,boids)
	# debug - this will be similar to how you would loop through each frame
	for i in range(10000):
		#if (i >= 100) and (i < 200): 		# Implement speed limit
			#if (i == 100):
			#	print ("Implementing speed limit.") # DEBUG
		#	boids = move_boids(boids, True, False, False)
		#elif (i >= 200) and (i < 300):	# Implement bound_position()
			#if (i == 200):
			#	print ("Implementing bound_position.") # DEBUG
		#	boids = move_boids(boids, True, True, False)
		#if ((i/100)%2 == 0): 	# Implement wind
			#if (i == 300):
		#	print ("Implementing wind.") # DEBUG
		#	boids = move_boids(boids, True, True, True)
		#else: #dont implement any extra tweaks
			#if (i % 100) == 0:
			#	print("No extra tweaks implemented.")
		boids = move_boids(boids, False, False, False)

		draw_boids(window,canvas,boids)
		
	window.mainloop()
		
main() #execute main function

