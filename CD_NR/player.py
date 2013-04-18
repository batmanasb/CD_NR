import random, settings
random.seed()
s=settings.Settings()

class Player:
	def __init__(self,x,y,head,chest,feet,scalar):
		self.x = x
		self.y = y
		self.dx = 0
		self.dy = 0
		
		self.head = head
		self.chest = chest
		self.feet = feet
		
		self.headRect = self.head[0].get_rect()
		self.headSize =self.headRect[3]
		self.headAt = 0
		self.headLen = len(self.head)
		self.headX = self.x+self.headSize/2
		self.headY=  self.y+self.headSize
		self.headRect.move_ip(self.headX,self.headY)
		
		self.chestRect = self.chest[0].get_rect()
		self.chestSize = self.chestRect[3]
		self.chestAt = 0
		self.chestLen = len(self.chest)
		self.chestX =  self.x
		self.chestY=  self.y + self.chestSize 
		self.chestRect.move_ip(self.chestX,self.chestY)
		
		self.feetRect = self.feet[0].get_rect()
		self.feetSize = self.feetRect[3]
		self.feetAt = 0
		self.feetLen = len(self.feet)
		self.feetX =  self.x
		self.feetY= 	self.chestY + self.feetSize
		self.feetRect.move_ip(self.feetX,self.feetY)
		
		##various variables
		self.walkSpeed = 0
		self.fallSpeed = 0
		self.maxWalkSpeed = s.playerMaxWalkSpeed*scalar
		self.maxFallSpeed = s.playerMaxFallSpeed*scalar
		self.walkAcc = s.playerWalkAcceleration*scalar
		self.walkFriction = s.playerWalkFriction*scalar
		self.fallAcc = s.playerFallAcceleration*scalar
		self.jumping = False
		self.time = 0.0
		self.timeChange = 0.1
		self.jumpSpeed = s.playerJumpSpeed*scalar
		self.riseSpeed = s.playerRiseSpeed*scalar
		self.bounceOffSpeed = s.playerBounceOffSpeed*scalar
		self.speedDuringCollision = 0
		self.dead = False
		
		##AI only
		self.jump = False
		self.jumpDuration = 0
		
	def draw(self,world):
		world.blit(self.head[self.headAt],(self.headX,self.headY))
		world.blit(self.feet[self.feetAt],(self.feetX,self.feetY))
		world.blit(self.chest[self.chestAt],(self.chestX,self.chestY))
	
	def update(self,jump,left,right,headCollisions,topCollisions,chestCollisions,feetCollisions):
		if self.headAt == self.headLen-1 or self.chestAt == self.chestLen-1 or self.feetAt == self.feetLen-1:
			self.dead = True
		##bouncing
		if chestCollisions < 1:
			if int(self.walkSpeed) == 0:
				self.walkSpeed == 0
			self.speedDuringCollision = self.walkSpeed
		else:
			if topCollisions > 0 and feetCollisions < 1:
				self.fallSpeed = self.bounceOffSpeed
			else:
				if self.speedDuringCollision > 0:
					self.walkSpeed = -self.bounceOffSpeed
				if self.speedDuringCollision < 0:
					self.walkSpeed = self.bounceOffSpeed
				
		##vertical motion
		if feetCollisions < 1:
			self.time += self.timeChange
			self.fallSpeed += self.fallAcc * self.time
		elif chestCollisions > 0 and not self.fallSpeed == 0 and topCollisions < 1:
			self.jumping = False
			self.time = 0
			self.fallSpeed = self.riseSpeed
		else:
			self.fallSpeed = 0
			self.time = 0
			self.jumping = False
		
		if jump and not self.jumping and feetCollisions > 0  and topCollisions < 1:
			self.jumping = True
			if self.jumpDuration < 0:
				self.jumpDuration = 0
			elif self.jumpDuration > 0:
				self.jumpDuration -= 1
			if self.jumpDuration == 0:
				self.jump = False
			self.fallSpeed -= self.maxFallSpeed
		
		##horizontal motion
		if right and self.walkSpeed < self.maxWalkSpeed and (chestCollisions < 1 or self.speedDuringCollision < 0):
			self.walkSpeed += self.walkAcc

		if left and self.walkSpeed > -self.maxWalkSpeed and (chestCollisions < 1 or self.speedDuringCollision > 0):
			self.walkSpeed -= self.walkAcc

		if not right and not left and not int(self.walkSpeed) == 0:
			if self.walkSpeed > 0:

				self.walkSpeed -= self.walkFriction
			else:

				self.walkSpeed += self.walkFriction
		if int(self.walkSpeed) == 0:
			self.walkSpeed == 0
			
		##applying motion to player
		self.y += int(self.fallSpeed)
		self.x += int(self.walkSpeed)
		
		self.dx = int(self.walkSpeed)
		self.dy = int(self.fallSpeed)
		
		self.headX = self.x+self.headSize/2
		self.headY=  self.y+self.headSize
		self.chestX =  self.x
		self.chestY=  self.y + self.chestSize 
		self.feetX =  self.x
		self.feetY= 	self.chestY + self.feetSize
		self.headRect.move_ip(int(self.walkSpeed),int(self.fallSpeed))
		self.chestRect.move_ip(int(self.walkSpeed),int(self.fallSpeed))
		self.feetRect.move_ip(int(self.walkSpeed),int(self.fallSpeed))
		
	def reset(self,x,y):
		self.x = x
		self.y = y
		self.headRect.move_ip(x+self.headSize/2-self.headRect[0],y+self.headSize-self.headRect[1])
		self.chestRect.move_ip(x-self.chestRect[0],y+self.chestSize-self.chestRect[1])
		self.feetRect.move_ip(x-self.feetRect[0],y+self.feetSize*2-self.feetRect[1])
		self.headAt = 0
		self.chestAt = 0
		self.feetAt = 0
	
	def teleport(self,x,y):
		self.x = x
		self.y = y
		self.headRect.move_ip(x+self.headSize/2-self.headRect[0],y+self.headSize-self.headRect[1])
		self.chestRect.move_ip(x-self.chestRect[0],y+self.chestSize-self.chestRect[1])
		self.feetRect.move_ip(x-self.feetRect[0],y+self.feetSize*2-self.feetRect[1])
		
































		