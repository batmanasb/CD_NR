import random
random.seed()
#u may use random numbers for settings
#ex: self.speed = random.randrange(0,1000)

class Settings:
	def __init__(self):
		
		##weapon cooldowns
		self.swordCoolDown = 1 
		self.spearCoolDown = 1
		self.shotgunCoolDown = 1
		self.akCoolDown = 1
		self.swordCoolDownAI = 100 
		self.spearCoolDownAI = 100
		self.shotgunCoolDownAI = 100
		self.akCoolDownAI = 100
		
		##engine tweaks
		self.startingLevel = 0
		self.fps = 30
		self.slowMoFPS = 1 
		
		##damage to blocks
		self.swordDmgToBlocks = 1
		self.spearDmgToBlocks = 1
		self.fistDmgToBlocks = 1
		self.bulletDmgToBlocks = 1
		self.pelletDmgToBlocks = 1
		self.pedBulletDmgToBlocks = 1
		self.pedPelletDmgToBlocks = 1
		
		##dust settings (unstable)
		self.dustScaling = 0.4
		self.dustClearsWhenSizeHasBeenMultipliedBy = 2
		
		##User damage to AI
		self.swordDmgToUserHead = 1
		self.swordDmgToPedsChest = 1
		self.swordDmgToPedsFeet = 1
		self.spearDmgToPedsHead = 1
		self.spearDmgToPedsChest = 1
		self.spearDmgToPedsFeet = 1
		self.fistDmgToPedsHead = 1
		self.fistDmgToPedsChest = 1
		self.fistDmgToPedsFeet = 1
		self.akRifleMeleeDmgToPedsHead = 1
		self.akRifleMeleeDmgToPedsChest = 1
		self.akRifleMeleeDmgToPedsFeet = 1
		self.shotgunMeleeDmgToPedsHead = 1
		self.shotgunMeleeDmgToPedsChest = 1
		self.shotgunMeleeDmgToPedsFeet = 1
		self.bulletDmgToPedsHead = 5
		self.bulletDmgToPedsChest = 5
		self.bulletDmgToPedsFeet = 5
		self.bulletDmgToBlocks = 1
		self.pelletDmgToPedsHead = 1
		self.pelletDmgToPedsChest = 1
		self.pelletDmgToPedsFeet = 1
		
		##AI behavior
		self.swordPedsMinRangeFromUser = 40
		self.swordPedsMaxRangeFromUser = 45
		self.spearPedsMinRangeFromUser = 45
		self.spearPedsMaxRangeFromUser = 55
		self.shotgunPedsMinRangeFromUser = 180
		self.shotgunPedsMaxRangeFromUser = 220
		self.akRiflePedsMinRangeFromUser = 580
		self.akRiflePedsMaxRangeFromUser = 620
		self.howLongPedsKeepJumpingToTryToGetOverBlocks = 5
		
		##AI damage to User
		self.pedsBulletDmgToUsersHead = 1
		self.pedsBulletDmgToUsersChest = 1
		self.pedsBulletDmgToUsersFeet = 1
		self.pedsPelletDmgToUsersHead = 1
		self.pedsPelletDmgToUsersChest = 1
		self.pedsPelletDmgToUsersFeet = 1
		self.pedsMeleeDmgToUsersHead = 1
		self.pedsMeleeDmgToUsersChest = 1
		self.pedsMeleeDmgToUsersFeet = 1
		
		##Movement of AI and User
		self.landBlockFallSpeed = 6
		self.dustFallSpeed = 1
		self.playerMaxWalkSpeed = 4
		self.playerMaxFallSpeed = 7
		self.playerWalkAcceleration = 0.4
		self.playerWalkFriction = 0.7
		self.playerFallAcceleration = 1.0
		self.playerJumpSpeed = 1
		self.playerRiseSpeed = -5
		self.playerBounceOffSpeed = 2
		
		##Movement of platforms
		self.horizontalPlatformSpeed = 1
		self.verticalPlatformSpeed = 1
		
		##TNT fuses
		self.fuse1 = 100
		self.fuse2 = 200
		self.fuse3 = 300
		self.fuse4 = 400
		
		##commented out
		# self. = 
		# self. = 
		# self. = 
		# self. = 
		# self. = 
		# self. = 
		# self. = 
		# self. = 
		# self. = 
		# self. = 
		# self. = 
		# self. = 
		# self. = 
		# self. = 
		# self. = 
		# self. = 
		# self. = 