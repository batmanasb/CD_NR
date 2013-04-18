import settings
s=settings.Settings()

class Land:
	def __init__(self,frames,x,y,dust,physics = "stone",type = "?",clock = 0):
		self.type = type
		self.dust = dust
		self.frames = frames
		self.x = x
		self.y = y
		self.clock = clock
		self.clockShift = int(clock/11)
		self.tick = 0
		self.direction = 1
		self.directionChangeCD = 0
		self.rect = frames[0].get_rect()
		self.size = self.rect[2]
		self.dustSize = self.size
		self.rect.move_ip(x,y)
		self.currentFrame = 0
		self.numFrames = len(self.frames) - 1
		self.falling = False
		self.broken = False
		if physics == "bridge":
			self.limit = 2
		elif physics == "stone":
			self.limit = 1
		elif physics == "joint":
			self.limit = 0
		else:
			self.limit = 3
		
	
	def draw(self,world):
		world.blit(self.frames[self.currentFrame],(self.x,self.y))
		
	def update(self,scalar,damage,collisions):
		if self.type == "=": #invisible blocks are invincible
			damage = 0
		if self.type in ("@","#","$","%"):
			#print "thing:",
			if self.clock > 0:
				self.clock -= 1
				self.tick += 1
				if self.tick == self.clockShift:
					self.tick = 0
					self.currentFrame += 1
				if self.clock == 0:
					self.currentFrame = self.numFrames
		self.currentFrame += damage
		if self.currentFrame > self.numFrames:
			self.currentFrame = self.numFrames
		if self.currentFrame == self.numFrames:
			self.falling = True
			self.broken = True
		elif collisions < self.limit:
			self.falling = True
		else:
			self.falling = False
		if self.falling and not self.broken:
			self.y += int(s.landBlockFallSpeed*scalar)
			self.rect.move_ip(0,int(s.landBlockFallSpeed*scalar))
		elif self.falling and self.broken:
			self.y += int(s.dustFallSpeed*scalar)
			self.rect.move_ip(0,int(s.dustFallSpeed*scalar))
		elif self.limit == 0:
			if self.directionChangeCD != 0:
				self.directionChangeCD -= 1
			if self.type == "_":
				self.x += int(s.horizontalPlatformSpeed*self.direction*scalar)
				self.rect.move_ip(int(s.horizontalPlatformSpeed*self.direction*scalar),0)
			if self.type == "|":
				self.y += int(s.verticalPlatformSpeed*self.direction*scalar)
				self.rect.move_ip(0,int(s.verticalPlatformSpeed*self.direction*scalar))
			if self.type == "/":
				self.x -= int(s.horizontalPlatformSpeed*self.direction*scalar)
				self.y += int(s.verticalPlatformSpeed*self.direction*scalar)
				self.rect.move_ip(int(-s.horizontalPlatformSpeed*self.direction*scalar),int(s.verticalPlatformSpeed*self.direction*scalar))
			if self.type == "\\":
				self.x += int(s.horizontalPlatformSpeed*self.direction*scalar)
				self.y += int(s.verticalPlatformSpeed*self.direction*scalar)
				self.rect.move_ip(int(s.horizontalPlatformSpeed*self.direction*scalar),int(s.verticalPlatformSpeed*self.direction*scalar))
	
	def changeDirection(self):
		if self.directionChangeCD == 0:
			self.direction = -self.direction
			self.directionChangeCD = 3
	
	def reset(self,x,y):
		self.x = x
		self.y = y
		self.rect.move_ip(x+self.rect[3]/2-self.rect[0],y-self.rect[1])