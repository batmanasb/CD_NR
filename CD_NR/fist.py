#modification of sword class, taking off "grab and drop" and replacing it with auto activate when no weapon in hand
#ranges ajusted for smaller range
#removed cooldown

import math,pygame
pygame.init()

class Fist:
	def __init__(self,frames,x,y,type = "melee"):
		self.type = type
		self.active = True
		self.frames = frames
		self.currentFrame = 0
		self.numFrames = len(self.frames)
		self.x = x
		self.y = y
		self.angle = 0
		self.rect = frames[0].get_rect()
		self.shift = self.rect[2] / 2
		self.attacking = False
		self.rect = self.rect.inflate(-self.shift*1.9,-self.shift*1.9)
		self.startingRect = self.rect
		self.FistShift = self.rect[2]*3
		self.startingHitBoxShift = self.rect[2]
		self.retracting = False
		self.clearRect = pygame.Rect(0,0,0,0)
		
		
	def draw(self,world):
		if self.active:
			world.blit(self.rot_center(self.frames[self.currentFrame],self.angle),(self.x,self.y))
		
	def update(self,x,y,mx,my,start):
		if not self.active:
			self.rect = self.clearRect
		
		if self.active:
			self.x = x - self.shift + self.FistShift/2
			self.y = y - self.shift + self.FistShift*1.5
			dx,dy = mx-x,my-y-self.FistShift
			self.angle = math.degrees(math.atan2(dx,dy)) - 135
			
			if start and not self.attacking:
				self.attacking = True
			if self.attacking and not self.retracting:
				self.currentFrame += 1
				if self.currentFrame == self.numFrames-1:
					self.retracting = True
			elif self.retracting:
				self.currentFrame -= 1
				if self.currentFrame == 0:
					self.attacking = False
					self.retracting = False
					
			self.hitBoxShift = self.startingHitBoxShift*(2+self.currentFrame*0.6)
			self.rect = self.startingRect.move(self.x +  int(math.cos(math.radians(self.angle+45))*self.hitBoxShift) , self.y - int(math.sin(math.radians(self.angle+45))*self.hitBoxShift))
		
	##function from pygame wiki
	def rot_center(self,image, angle):
		#rotate an image while keeping its center and size
		orig_rect = image.get_rect()
		rot_image = pygame.transform.rotate(image, angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()
		return rot_image