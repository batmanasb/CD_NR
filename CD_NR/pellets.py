#modification of bullet class to allow 8 projectiles but only 1 shell

import math,pygame,random
pygame.init()
random.seed()

class Pellets:
	def __init__(self,frames,shell,x,y,flipped,angle):
		self.flipped = flipped
		self.frames = frames
		self.shell = shell
		self.currentFrame = 0
		self.numFrames = len(frames)
		self.px = x + frames[0].get_rect()[2]*8 - int(math.cos(math.radians(angle+45))*frames[0].get_rect()[2]*3.5)
		self.py = y + frames[0].get_rect()[2]*8 + int(math.sin(math.radians(angle+45))*frames[0].get_rect()[2]*3.5)
		if self.flipped:
			self.sx = x + frames[0].get_rect()[2]*8 - int(math.cos(math.radians(angle+45))*frames[0].get_rect()[2]*-0.5)
			self.sy = y + frames[0].get_rect()[2]*8 + int(math.sin(math.radians(angle+45))*frames[0].get_rect()[2]*-0.5)
		else:
			self.sx = self.px
			self.sy = self.py
		self.pelletRect = frames[0].get_rect().move(self.px,self.py)
		self.pelletRect = self.pelletRect.inflate(-self.pelletRect[2]/4,-self.pelletRect[2]/4)
		self.shellRect = self.pelletRect.move(0,0)	
		self.pelletAngle = angle+45
		if self.flipped:
			self.shellAngle = angle+45-180
		else:
			self.shellAngle = angle+45
		self.pelletActive = True
		self.shellActive = True
		self.impact = False
		self.pelletSpeed = 20
		self.shellFalling = True
		self.time = 0
		self.shellAngleSpin = 0
		self.clearRect = pygame.Rect(0,0,0,0)
		self.shellPopoutAngle = random.randrange(95,135,1)
		
		self.currentFrames = []
		self.pxs = []
		self.pys = []
		self.pelletRects = []
		self.pelletsActive = []
		self.impacts = []
		self.pelletAngles = []
		for i in range(8):
			self.currentFrames.append(0)
			self.pxs.append(self.px)
			self.pys.append(self.py)
			self.pelletRects.append(self.pelletRect.move(0,0))
			self.pelletsActive.append(True)
			self.impacts.append(False)
			self.pelletAngles.append(self.pelletAngle+random.randrange(-5,5,1))
	
	def draw(self,world):
		if self.shellActive:	
			world.blit(self.rot_center(self.shell,self.shellAngle-45 + self.shellAngleSpin),(self.sx,self.sy))

		for i in range(8):
			if self.pelletsActive[i]:
				world.blit(self.rot_center(self.frames[self.currentFrames[i]],self.pelletAngles[i]-45),(self.pxs[i],self.pys[i]))
	
	def update(self,scalar):
		#pellet
		for i in range(8):
			if self.pelletsActive[i]:
				if self.impacts[i]:
					self.currentFrames[i] += 1
					if self.currentFrames[i] > self.numFrames - 1:
						self.pelletsActive[i] = False
						self.pelletRects[i] = self.clearRect
				else:
					xOff = int(math.cos(math.radians(self.pelletAngles[i]))*scalar * self.pelletSpeed)
					yOff = int(math.sin(math.radians(self.pelletAngles[i]))*scalar * self.pelletSpeed)
					self.pxs[i] += xOff
					self.pys[i] -= yOff
					self.pelletRects[i].move_ip(xOff,-yOff)
				
		#shell
		self.time += 0.5
		if self.shellFalling:
			xOff = int(math.cos(math.radians(self.shellAngle+self.shellPopoutAngle))*5) + int(math.cos(math.radians(self.shellAngle-110))*self.time)
			yOff = int(math.sin(math.radians(self.shellAngle+self.shellPopoutAngle))*5) + int(math.sin(math.radians(self.shellAngle-110))*self.time)
			if self.flipped:
				xOff = -xOff
			self.sx += xOff
			self.sy -= yOff
			self.shellRect.move_ip(xOff,-yOff)
			self.shellAngleSpin+=self.time*2
		if self.time > 100:
			self.shellActive = False


##function from pygame wiki
	def rot_center(self,image, angle):
		#rotate an image while keeping its center and size
		orig_rect = image.get_rect()
		rot_image = pygame.transform.rotate(image, angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()
		return rot_image	