#original class for launching projectiles from a rifle class weapon

import math,pygame,random
pygame.init()
random.seed()

class Bullet:
	def __init__(self,frames,x,y,flipped,angle):
		self.flipped = flipped
		self.frames = frames
		self.shell = frames[0]
		self.currentFrame = 0
		self.numFrames = len(frames)
		self.bx = x + frames[0].get_rect()[2]*8 - int(math.cos(math.radians(angle+50))*frames[0].get_rect()[2]*2.5)
		self.by = y + frames[0].get_rect()[2]*8 + int(math.sin(math.radians(angle+50))*frames[0].get_rect()[2]*2.5)
		if self.flipped:
			self.sx = x + frames[0].get_rect()[2]*8 - int(math.cos(math.radians(angle+50))*frames[0].get_rect()[2]*-2.5)
			self.sy = y + frames[0].get_rect()[2]*8 + int(math.sin(math.radians(angle+50))*frames[0].get_rect()[2]*-2.5)
		else:
			self.sx = self.bx
			self.sy = self.by
		self.bulletRect = frames[0].get_rect().move(self.bx,self.by)
		self.bulletRect = self.bulletRect.inflate(-self.bulletRect[2]/4,-self.bulletRect[2]/4)
		self.shellRect = self.bulletRect.move(0,0)
		self.bulletAngle = angle+45
		if self.flipped:
			self.shellAngle = angle+45-180
		else:
			self.shellAngle = angle+45
		self.bulletActive = True
		self.shellActive = True
		self.impact = False
		self.bulletSpeed = 20
		self.shellFalling = True
		self.time = 0
		self.shellAngleSpin = 0
		self.clearRect = pygame.Rect(0,0,0,0)
		self.shellPopoutAngle = random.randrange(100,130,1)
	
	def draw(self,world):
		if self.shellActive:	
			world.blit(self.rot_center(self.shell,self.shellAngle-50 + self.shellAngleSpin),(self.sx,self.sy))
		if self.bulletActive:
			world.blit(self.rot_center(self.frames[self.currentFrame],self.bulletAngle-45),(self.bx,self.by))
	
	def update(self,scalar):
		self.time += 0.5
		#bullet
		if self.bulletActive:
			if self.impact:
				self.currentFrame += 1
				if self.currentFrame > self.numFrames - 1:
					self.bulletActive = False
					self.bulletRect = self.clearRect
			else:
				xOff = int(math.cos(math.radians(self.bulletAngle))*scalar * self.bulletSpeed)
				yOff = int(math.sin(math.radians(self.bulletAngle))*scalar * self.bulletSpeed)
				self.bx += xOff
				self.by -= yOff
				self.bulletRect.move_ip(xOff,-yOff)
		#shell
		if self.shellFalling:
			xOff = int(math.cos(math.radians(self.shellAngle+self.shellPopoutAngle))*5) + int(math.cos(math.radians(self.shellAngle-110))*self.time)
			yOff = int(math.sin(math.radians(self.shellAngle+self.shellPopoutAngle))*5) + int(math.sin(math.radians(self.shellAngle-110))*self.time)
			if self.flipped:
				xOff = -xOff
			self.sx += xOff
			self.sy -= yOff
			self.shellRect.move_ip(xOff,-yOff)
			self.shellAngleSpin+=self.time*2
		if self.time > 20:
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