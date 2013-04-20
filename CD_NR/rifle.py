#modification of sword class to support launching ranged projectiles and attack with the end of the weapon do to "recoil"

import math,pygame,sounds
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

class Rifle:
	def __init__(self,frames,x,y,icon,endOfRifle,cooldownDuration,type = "user's"):
		self.type = type
		self.icon = icon
		self.active = False
		self.frames = frames
		self.currentFrame = 0
		self.numFrames = len(self.frames)
		self.x = x
		self.y = y
		self.mx = 0
		self.angle = 0
		self.rect = frames[0].get_rect()
		self.shift = self.rect[2] / 2
		self.attacking = False
		self.rect = self.rect.inflate(-self.shift*1.9,-self.shift*1.9)
		self.startingRect = self.rect
		self.RifleShift = self.rect[2]*3
		self.startingHitBoxShift = self.rect[2]
		self.iconRect = self.icon.get_rect()
		self.startingIconRect = self.iconRect.inflate(-self.iconRect[2]/4,-self.iconRect[2]/6)
		self.iconRect = self.iconRect.move(self.x,self.y)
		self.iconRect = self.iconRect.inflate(-self.iconRect[2]/4,-self.iconRect[2]/6)
		self.retracting = False
		self.clearRect = pygame.Rect(0,0,0,0)
		self.muzzelx = self.x
		self.muzzely = self.y
		self.flipped = False
		self.endOfRifle = endOfRifle #3 for ak, 2 for shotgun
		self.cooldown = False
		self.cooldownTime = 0
		self.cooldownDuration = cooldownDuration
				
		
	def draw(self,world):
		if self.active:
			if self.x+self.shift-self.shift/4 > self.mx:
				self.flipped = True
				world.blit(self.rot_center(pygame.transform.flip(self.frames[self.currentFrame],True,False),self.angle-90),(self.x,self.y))
			else:
				self.flipped = False
				world.blit(self.rot_center(self.frames[self.currentFrame],self.angle),(self.x,self.y))
		else:
			world.blit(self.icon,(self.x,self.y))
		#world.blit(pygame.transform.rotate(self.frames[self.currentFrame],self.angle),(self.x,self.y))
		#print self.angle
		
	def update(self,x,y,mx,my,start,drop,grab):
		self.mx = mx
		if drop:
			if self.active:
				self.active = False
				self.x -= 100
				self.iconRect = self.startingIconRect.move(self.x,self.y)
				self.rect = self.clearRect
		if grab:
			if not self.active:				
				self.active = True
				self.iconRect = self.clearRect
		if self.active:			
			self.x = x - self.shift + self.RifleShift/2
			self.y = y - self.shift + self.RifleShift*1.3
			dx,dy = mx-x,my-y-self.RifleShift
			self.angle = math.degrees(math.atan2(dx,dy)) - 135
			
			if start and not self.attacking and not self.cooldown:				
				self.attacking = True					
			if self.attacking and not self.retracting:				
				sounds.play('RifleShot')
				self.currentFrame += 1				
				if self.currentFrame == self.numFrames-1:
					self.retracting = True
			elif self.retracting:
				self.currentFrame -= 1
				if self.currentFrame == 0:
					self.attacking = False
					self.retracting = False
					self.cooldown = True
					self.cooldownTime = self.cooldownDuration
			if self.cooldown:
				if self.cooldownTime <= 0:
					self.cooldown = False
				else:
					self.cooldownTime -= 1
			self.hitBoxShift = self.startingHitBoxShift*(-self.endOfRifle-self.currentFrame*0.5)
			self.rect = self.startingRect.move(self.x +  int(math.cos(math.radians(self.angle+60))*self.hitBoxShift) , self.y - int(math.sin(math.radians(self.angle+60))*self.hitBoxShift))
			if self.x+self.shift-self.shift/4 > self.mx:
				self.muzzelx = self.x +  int(math.cos(math.radians(self.angle+60))*(+self.hitBoxShift/3))
				self.muzzely = self.y - int(math.sin(math.radians(self.angle+60))*(+self.hitBoxShift/3))
			else:
				self.muzzelx = self.x +  int(math.cos(math.radians(self.angle+60))*(-self.hitBoxShift))
				self.muzzely = self.y - int(math.sin(math.radians(self.angle+60))*(-self.hitBoxShift))
		
	##function from pygame wiki
	def rot_center(self,image, angle):
		#rotate an image while keeping its center and size
		orig_rect = image.get_rect()
		rot_image = pygame.transform.rotate(image, angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()
		return rot_image
		
	def reset(self,x,y):
		self.x = x
		self.y = y
		self.iconRect.move_ip(x-self.iconRect[0],y-self.iconRect[1])
		if self.active:
			self.x+=self.shift
		self.update(0,0,0,0,False,True,False)