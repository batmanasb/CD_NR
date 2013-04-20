##dev log
#known bugs:
#	*shell hitboxes aren't aligned with the images when facing backwards

## import modules
import os, pygame, pygame.mixer, sys, glob, time, math, random
## import custom made modules 
import land, mouse, player, sword, fist, spear, rifle, bullet, pellets, settings, sounds
## put commonly used in global namespace
from pygame.locals import *
pygame.init()

pygame.display.set_caption("Collateral Damage: No Regrets!")
clock = pygame.time.Clock()
s = settings.Settings()
random.seed()
option = 0

##starting menu
#asks the user for the resolution to run the game in
while True:
	try:
		print("Select a resolution:\n1. 1600 x 800\n2. 1200 x 600\n3. 800 x 400\n4. Quit")
		option = int(input())
		if option == 1 or option == 2 or option == 3:
			break
		elif option == 4:
			sys.exit()
	except BaseException as e:
		if isinstance(e,SystemExit):
			sys.exit()
		print "Error:\nSelect either 1, 2, 3, or 4\n"

##determine the scalar
#images are scaled to match the resolution size
#this isn't as perfect as real graphics
#but it does look better when going into fullscreen
#scalar is the value all images are scaled by
#also, every time an image is moved, it has to move by a scaled amount
#so that the movement is consistant in all resolutions
#note: multiplication can substitute scaling, so u either multiply a number or add/subtract by a number*scalar
if option == 1:
	screenSize = width, height = 1600,800
	scalar = 2
elif option == 2:
	screenSize = width, height = 1200,600
	scalar = 1.5
else:
	screenSize = width, height = 800,400
	scalar = 1

##fullscreen menu
while True:
	try:
		print("Fullscreen?\n1. yes\n2. no\n3. Quit")
		option = int(input())
		if option == 1 or option == 2:
			break
		elif option == 3:
			sys.exit()
	except BaseException as e:
		if isinstance(e,SystemExit):
			sys.exit()
		print "Error:\nSelect either 1, 2, or 3\n"

if option == 1:
	screen = pygame.display.set_mode(screenSize,  pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE) 
elif option == 2:
	screen = pygame.display.set_mode(screenSize)
	
font = pygame.font.SysFont("Comic Sans MS", int(10*scalar))

##loading functions

#returns a set of images Globbed together
#may also return a dust image (last image in the animation files)
#may also scale the image by an extra amount
def loadImages(name,dust = False,extraScale = 1):
	try:
		filenames = os.path.join( 'images', name+"*.png" )
		frameFiles = glob.glob(filenames)
		frameFiles.sort()
		frames = []
		for i in range(len(frameFiles)):
			image = pygame.image.load(frameFiles[i])
			image = pygame.transform.scale(image,(int(image.get_width()*scalar*extraScale),int(image.get_width()*scalar*extraScale)))
			frames.append(image.convert())
	except pygame.error, message:
		print 'Cannot load '+name+' images:'
		raise SystemExit, message
	if dust:
		return frames,frameFiles[-1][7:-4]
	else:
		return frames

#returns a single image
def loadImage(name,extraScale = 1):
	try:
		filename = os.path.join( 'images', name+".png" )
		image = pygame.image.load(filename)
		image = pygame.transform.scale(image,(int(image.get_width()*scalar*extraScale),int(image.get_width()*scalar*extraScale)))
		image = image.convert()
	except pygame.error, message:
		print 'Cannot load mouseBlockImage image:'
		raise SystemExit, message
	return image

##loading

#the naming convention is to call:
# sets of images used for animations end with "Frames"
# ex: walkingFrames
# single images end with "Image"
# ex: faceImage
# an exception to the Image rule is the coin rule:
#  images used for weapon coins (the thing u pick up and it gives u a weapon) end with "Coin"
#  ex: pistolCoin

#all you do to load an animation is:
# draw a set of images in Aseprite
# save them in the Images folder
# save using a unique name so that the * of another name doesn't grab your images too
# ex: say I made an animation called laser, the files are saved as laser0, laser2, ..., laser33
#	then I name another animation called laserRifle, the files are saved as laserRifle0, laserRifle1, ...,laserRifle5
#	when I load "laser", the function loads "laser*.png", therefor making a set of anything starting with "laser"... including laserRifle
#	a solution is possible by laoding images in their own folders... but hasn't been implemented yet
# make a variable, and set it equal to a load function
# write the name of the animation as a string in the parameters (*.png is taken care of for you) 

mouseBlockImage = loadImage("mouseBlock")
bulletImpactFrames = loadImages("bullet_impact")
headFrames = loadImages("newHead")
chestFrames = loadImages("newChest")
goldSwordFrames = loadImages("goldSword")
swordCoin = loadImage("swordCoin")
fistFrames = loadImages("fist")
spearFrames = loadImages("spear")
spearCoin = loadImage("longSpearCoin")
akRifleFrames = loadImages("akRifle")
rifleCoin = loadImage("rifleCoin")
rifleBulletFrames = loadImages("rifleBullet")
shotGunFrames = loadImages("shotGun")
shotGunCoin = loadImage("theShotGunCoin")
pelletFrames = loadImages("pellet")
pelletShellImage = loadImage("shellOfShotgun")
leafFrames,leafDust = loadImages("leafBlock",True)
treeFrames,treeDust = loadImages("treeBlock",True)
stoneFrames,stoneDust = loadImages("stoneBlock",True)
dirtFrames,dirtDust = loadImages("dirtBlock",True)
brickFrames,brickDust = loadImages("brickBlock",True)
crateFrames,crateDust = loadImages("crateBlock",True)
bridgeFrames,bridgeDust = loadImages("bridgeBlock",True)
portalFrames,portalDust = loadImages("portalDoor",True)
tntFrames,tntDust = loadImages("tntBlock",True)
invisibleFrames,invisibleDust = loadImages("invisibleBlock",True)
magnetPlatformFrames,magnetPlatformDust = loadImages("magnetPlatformBlock",True)
barsFrames,barsDust = loadImages("barsBlock",True)
blackFrames,blackDust = loadImages("blackBlock",True)
voidMistFrames,voidMistDust = loadImages("voidMistBlock",True)
	
##create game world
#the world is one large Surface
#images are blit to the world, and then the world is blit to the screen
#this enables scrolling
#because Surfaces have a max size, I've been forced to limit the maps to 200 x 200 blocks
world_width, world_height = int(width*9.5), int(width*9.5)
world = pygame.Surface((world_width, world_height))


##game objects
#all the objects are created here except for the blocks that make up maps
#maps = mapGen.Generator(scalar)
testBox = mouse.Mouse(pygame.mouse.get_pos(),0,0,mouseBlockImage)
sampleBlock = land.Land(dirtFrames,0,0, stoneDust, "joint")
user = player.Player(sampleBlock.size*22,200*scalar,headFrames,chestFrames,chestFrames,scalar)
fist = fist.Fist(fistFrames,0,0)
goldSword = sword.Sword(goldSwordFrames,sampleBlock.size*1,160*scalar,swordCoin,s.swordCoolDown)
longSpear = spear.Spear(spearFrames,sampleBlock.size*1,160*scalar,spearCoin,s.spearCoolDown)
akRifle = rifle.Rifle(akRifleFrames,sampleBlock.size*1,160*scalar,rifleCoin,3,s.akCoolDown)
shotGun = rifle.Rifle(shotGunFrames,sampleBlock.size*1,160*scalar,shotGunCoin,2,s.shotgunCoolDown)
portal = land.Land(portalFrames,sampleBlock.size*1,170*scalar, portalDust, "stone")
portal.rect = portal.rect.inflate(-60*scalar,0)

def levelGen(blocks,peds,file):
	pedWeapons = []
	delBlocks = blocks[:]
	for block in delBlocks:
		blocks.remove(block)
	delPeds = peds[:]
	for ped in delPeds:
		peds.remove(ped)
	
	f = open(file,"r")
	line = ""
	
	y_loc = sampleBlock.size*20
	for b in range(200):
		x_loc = sampleBlock.size*20
		line = f.readline()
		for i in range(200):
			#land blocks
			if line[i] == "B":
				blocks.append(land.Land(bridgeFrames,x_loc,y_loc, bridgeDust, "bridge", "B"))
			elif line[i] == "C":
				blocks.append(land.Land(crateFrames,x_loc,y_loc, crateDust, "stone", "C"))
			elif line[i] == "D":
				blocks.append(land.Land(dirtFrames,x_loc,y_loc, dirtDust, "stone", "D"))
			elif line[i] == "S":
				blocks.append(land.Land(stoneFrames,x_loc,y_loc, stoneDust, "stone", "S"))
			elif line[i] == "T":
				blocks.append(land.Land(treeFrames,x_loc,y_loc, treeDust, "bridge", "T"))
			elif line[i] == "R":
				blocks.append(land.Land(brickFrames,x_loc,y_loc, brickDust, "stone", "R"))
			elif line[i] == "L":
				blocks.append(land.Land(leafFrames,x_loc,y_loc, leafDust, "leaf", "L"))
			elif line[i] == "_":
				blocks.append(land.Land(magnetPlatformFrames,x_loc,y_loc, magnetPlatformDust, "joint", "_"))
			elif line[i] == "|":
				blocks.append(land.Land(magnetPlatformFrames,x_loc,y_loc, magnetPlatformDust, "joint", "|"))
			elif line[i] == "/":
				blocks.append(land.Land(magnetPlatformFrames,x_loc,y_loc, magnetPlatformDust, "joint", "/"))
			elif line[i] == "\\":
				blocks.append(land.Land(magnetPlatformFrames,x_loc,y_loc, magnetPlatformDust, "joint", "\\"))
			elif line[i] == "X":
				blocks.append(land.Land(blackFrames,x_loc,y_loc, blackDust, "joint", "="))
			elif line[i] == "J":
				blocks.append(land.Land(barsFrames,x_loc,y_loc, barsDust, "joint", "="))
			elif line[i] == "V":
				blocks.append(land.Land(voidMistFrames,x_loc,y_loc, voidMistDust, "joint", "="))
			elif line[i] == "@":
				blocks.append(land.Land(tntFrames,x_loc,y_loc, tntDust, "bridge", "@",s.fuse1))
			elif line[i] == "#":
				blocks.append(land.Land(tntFrames,x_loc,y_loc, tntDust, "bridge", "#",s.fuse2))
			elif line[i] == "$":
				blocks.append(land.Land(tntFrames,x_loc,y_loc, tntDust, "bridge", "$",s.fuse3))
			elif line[i] == "%":
				blocks.append(land.Land(tntFrames,x_loc,y_loc, tntDust, "bridge", "%",s.fuse4))
			# elif line[i] == "":
				
			#weapons
			elif line[i] == "0":
				goldSword.update(0,0,0,0,False,False,True)
				goldSword.reset(x_loc-10*scalar,y_loc)
			elif line[i] == "1":
				longSpear.update(0,0,0,0,False,False,True)
				longSpear.reset(x_loc-10*scalar,y_loc)
			elif line[i] == "2":
				shotGun.update(0,0,0,0,False,False,True)
				shotGun.reset(x_loc-10*scalar,y_loc)
			elif line[i] == "3":
				akRifle.update(0,0,0,0,False,False,True)
				akRifle.reset(x_loc-10*scalar,y_loc)
			
			#user and portal
			elif line[i] == "<":
				user.reset(x_loc,y_loc)
			elif line[i] == ">":
				portal.reset(x_loc,y_loc)
			
			#AI
			elif line[i] == "q":
				peds.append(player.Player(x_loc,y_loc-sampleBlock.size*3,headFrames,chestFrames,chestFrames,scalar))
				weapon = sword.Sword(goldSwordFrames,sampleBlock.size*60,160*scalar,swordCoin,s.swordCoolDownAI)
				weapon.active = True
				pedWeapons.append(weapon)
			elif line[i] == "w":
				peds.append(player.Player(x_loc,y_loc-sampleBlock.size*3,headFrames,chestFrames,chestFrames,scalar))
				weapon = spear.Spear(spearFrames,sampleBlock.size*23,160*scalar,spearCoin,s.spearCoolDownAI)
				weapon.active = True
				pedWeapons.append(weapon)
			elif line[i] == "e":
				peds.append(player.Player(x_loc,y_loc-sampleBlock.size*3,headFrames,chestFrames,chestFrames,scalar))
				weapon = rifle.Rifle(shotGunFrames,sampleBlock.size*30,160*scalar,shotGunCoin,2,s.shotgunCoolDownAI,"sg")
				weapon.active = True
				pedWeapons.append(weapon)
			elif line[i] == "r":
				peds.append(player.Player(x_loc,y_loc-sampleBlock.size*3,headFrames,chestFrames,chestFrames,scalar))
				weapon = rifle.Rifle(akRifleFrames,sampleBlock.size*40,160*scalar,rifleCoin,3,s.akCoolDownAI,"ak")
				weapon.active = True
				pedWeapons.append(weapon)
			# elif line[i] == "":
				

			x_loc += sampleBlock.size - 2*scalar
		y_loc += sampleBlock.size - 2*scalar
	f.close()

	blocks.reverse() #this makes the game run faster on average (faster in middle and end, slower at start)... i think
	
	#might help them get out of walls...
	for p in peds: 
		p.speedDuringCollision = -1
	return len(peds),pedWeapons	
	
def main():
	yolo = 0
	##various variables that don't reset every frame
	filenames = os.path.join( 'maps', "level*.txt" ) #put all the level text files in one list
	maps = glob.glob(filenames)
	maps.sort()
	level = s.startingLevel
	# levelChanged = True
	blocks = []
	peds = []
	#pedCount,pedWeapons = map1(blocks,peds)
	
	pedCount,pedWeapons = levelGen(blocks,peds,maps[level])
	world_x , world_y = user.x,user.y
	world_dx, world_dy = 50*scalar,50*scalar
	fps = s.fps
	weaponEquipped = False
	ridingHor = False
	ridingHorDirection = 1
	ridingVer = False
	ridingVerDirection = 1
	bullets = []
	pedBullets = []
	pelletsList = []
	pedPelletsList = []
	deletePedBulletsList = []
	deletePedPelletsList = []
	
	sounds.loop('Background')	
	
	while True:		
		clock.tick(fps)
		yolo += 1
		
		##resetting variables
		damage = 0
		damages = []
		pedHeadCollisions,pedChestCollisions,pedFeetCollisions,pedTopCollisions = [],[],[],[]
		for p in range(pedCount):
			damages.append(0)
			pedHeadCollisions.append(0)
			pedChestCollisions.append(0)
			pedFeetCollisions.append(0)
			pedTopCollisions.append(0)
		world.fill((0,0,0))
		headCollisions,chestCollisions,feetCollisions,topCollisions = 0,0,0,0
		world_x = -user.x + 100*scalar
		world_y = -user.y + 220*scalar
		message = None
		drop = False
		grabbing = False
		grabSword = False
		drawSword = True
		grabSpear = False
		drawSpear = True
		grabRifle = False
		drawRifle = True
		grabShotGun = False
		drawShotGun = True
		pDamage,pCollisions = 0,0
		
		##slow event getter, for one click events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				sys.exit()
			elif event.type == KEYDOWN and event.key == K_p:
				timestamp = time.localtime()[3:6] #get the current hour, min, sec
				filename = os.path.join('screenshots', 'screenshot'+str(timestamp[0])+str(timestamp[1])+str(timestamp[2])+'.jpg')
				pygame.image.save(screen, filename) #take screenshot and name it after the current time
				message = font.render("Screenshot Taken!", 1, (255,255,255))
			elif event.type == KEYDOWN and event.key == K_q:
				drop = True
			# elif event.type == KEYDOWN and event.key == K_j: #debugging
				# print "weapons:",len(pedWeapons)
				# print "peds:",len(peds)
				#for w in pedWeapons:
				#	print w.type
			
		##constant  key logger, for "holding" keys
		pressed = pygame.key.get_pressed() #place the state of every key into a list
		# if pressed[K_w]:
			# up = True
		# else:
			# up = False
		# if pressed[K_s]:
			# down = True
		# else:
			# down = False
		if pressed[K_d]:
			right = True
		else:
			right = False
		if pressed[K_a]:
			left = True
		else:
			left = False
		if pressed[K_SPACE]:
			jump = True
		else:
			jump = False
		# if pressed[K_UP]:
			# world_y += world_dy
		# if pressed[K_DOWN]:
			# world_y -= world_dy
		# if pressed[K_LEFT]:
			# world_x += world_dx
		# if pressed[K_RIGHT]:
			# world_x -= world_dx
		# if pressed[K_j]:
			# print len(blocks)
		if pressed[K_g]:
			fps = s.slowMoFPS
		else:
			fps = s.fps
	
		##boundries
		if world_x > 0:
			world_x = 0
		if world_x < -(world_width-width):
			world_x = -(world_width-width)

		if world_y > 0:
			world_y = 0
		if world_y < -(world_height-height):
			world_y = -(world_height-height)
		
		##mouse tracking
		mousePos = pygame.mouse.get_pos()
		mousex = mousePos[0] - world_x
		mousey = mousePos[1] - world_y
		
		##weapon pick up
		#if the user colliides with a weapon coin and isn't holding a weapon
		#then the user picks up the weapon
		if not goldSword.active:
			if goldSword.x < user.x + 1100*scalar and goldSword.x > user.x - 300 * scalar:
				if user.feetRect.colliderect(goldSword.iconRect) or user.chestRect.colliderect(goldSword.iconRect) or user.headRect.colliderect(goldSword.iconRect):
					if not weaponEquipped and not grabbing:
						grabSword = True
						grabbing = True
			else:
				drawSword = False
				
		if not longSpear.active:
			if longSpear.x < user.x + 1100*scalar and longSpear.x > user.x - 300 * scalar:
				if user.feetRect.colliderect(longSpear.iconRect) or user.chestRect.colliderect(longSpear.iconRect) or user.headRect.colliderect(longSpear.iconRect):
					if not weaponEquipped and not grabbing:
						grabSpear = True
						grabbing = True
			else:
				drawSpear = False
				
		if not akRifle.active:
			if akRifle.x < user.x + 1100*scalar and akRifle.x > user.x - 300 * scalar:
				if user.feetRect.colliderect(akRifle.iconRect) or user.chestRect.colliderect(akRifle.iconRect) or user.headRect.colliderect(akRifle.iconRect):
					if not weaponEquipped and not grabbing:
						grabRifle = True
						grabbing = True
			else:
				drawRifle = False
		
		if not shotGun.active:
			if shotGun.x < user.x + 1100*scalar and shotGun.x > user.x - 300 * scalar:
				if user.feetRect.colliderect(shotGun.iconRect) or user.chestRect.colliderect(shotGun.iconRect) or user.headRect.colliderect(shotGun.iconRect):
					if not weaponEquipped and not grabbing:
						grabShotGun = True
						grabbing = True
			else:
				drawShotGun = False
		
		##draw user
		user.draw(world)
		
		##draw the peds and their weapons
		pNum = -1
		for p in peds:
			pNum+=1
			if p.x < user.x + 1100*scalar and p.x > user.x - 300 * scalar:
				p.draw(world)
				pedWeapons[pNum].draw(world)
		
		##hold out fist if the user is unarmed
		if weaponEquipped:
			fist.active = False
		else:
			fist.active = True
		fist.update(user.x,user.y,mousex,mousey,pygame.mouse.get_pressed()[0])
		if not goldSword.active and not longSpear.active and not akRifle.active and not shotGun.active:
			fist.draw(world)
			weaponEquipped = False
		else:
			weaponEquipped = True
		
		##draw weapons
		if drawSword:
			goldSword.update(user.x,user.y,mousex,mousey,pygame.mouse.get_pressed()[0],drop,grabSword)
			goldSword.draw(world)
		
		if drawSpear:
			longSpear.update(user.x,user.y,mousex,mousey,pygame.mouse.get_pressed()[0],drop,grabSpear)
			longSpear.draw(world)
			
		if drawRifle:
			akRifle.update(user.x,user.y,mousex,mousey,pygame.mouse.get_pressed()[0],drop,grabRifle)
			if akRifle.currentFrame == 1 and not akRifle.retracting:
				bullets.append(bullet.Bullet(rifleBulletFrames,akRifle.muzzelx,akRifle.muzzely,akRifle.flipped,akRifle.angle))
			for item in bullets:
				item.update(scalar)
				item.draw(world)
			akRifle.draw(world)
			
		if drawShotGun:
			shotGun.update(user.x,user.y,mousex,mousey,pygame.mouse.get_pressed()[0],drop,grabShotGun)
			if shotGun.currentFrame == 1 and not shotGun.retracting:
				pelletsList.append(pellets.Pellets(pelletFrames,pelletShellImage,shotGun.muzzelx,shotGun.muzzely,shotGun.flipped,shotGun.angle))
			for item in pelletsList:
				item.update(scalar)
				item.draw(world)
			shotGun.draw(world)
		
		##update the mouse pointer
		testBox.update(mousePos,world_x,world_y)
		
		##block collision detection system
		#aka collision loop
		
		#detete lists are used to delete blocks after the collision loop
		deleteList = []
		deleteBulletsList = []
		deletePelletsList = []
		
		#loop through every block in the map
		for block in blocks:
			#variables for the current block
			damage = 0
			collisions = 0
			if block.x < user.x + 1200*scalar and block.x > user.x - 400 * scalar: #is block in range? test
				#find collisions with the portal
				if block.rect.colliderect(portal.rect):
					pCollisions += 1
					collisions += 1
			if block.x < user.x + 1100*scalar and block.x > user.x - 300 * scalar: #is block in range? test
				
				#find collisions with peds
				pNum = -1
				for p in peds:
					pNum += 1
					if p.x < user.x + 1100*scalar and p.x > user.x - 300 * scalar:
						if not block.broken:
							if not block.falling:
								if pedFeetCollisions[pNum] == 0:
									if not p.jumping:
										if p.feetRect.colliderect(block.rect):
											pedFeetCollisions[pNum] += 1
									else:
										if p.feetRect.move(0,sampleBlock.size/2).colliderect(block.rect):
											pedFeetCollisions[pNum] += 1
								if pedChestCollisions[pNum] == 0:
									if p.chestRect.colliderect(block.rect):
										pedChestCollisions[pNum] += 1
								if pedHeadCollisions[pNum] == 0:
									if p.headRect.colliderect(block.rect):
										pedHeadCollisions[pNum] += 1
								if pedTopCollisions[pNum] == 0:
									if p.headRect.inflate(p.headSize,0).colliderect(block.rect):
										pedTopCollisions[pNum] += 1
				
				#find collisions with user
				if not block.broken:
					if not block.falling and block.type != "=":
						if feetCollisions == 0:
							if not user.jumping:
								if user.feetRect.colliderect(block.rect):
									feetCollisions += 1
									# if (block.type == "_" or block.type == "|" or block.type == "/" or block.type == "\\"):
										# user.reset(block.x,block.y-user.chestSize*3)
									if block.type == "_" :
										ridingHor = True
										ridingVer = False
										ridingHorDirection = block.direction
									elif block.type == "|":
										ridingVer = True
										ridingHor = False
										ridingVerDirection = block.direction
									elif block.type == "/":
										ridingVer = True
										ridingHor = True
										ridingVerDirection = block.direction
										ridingHorDirection = -block.direction
									elif block.type == "\\":
										ridingVer = True
										ridingHor = True
										ridingVerDirection = block.direction
										ridingHorDirection = block.direction
									else:
										ridingHor = False
										ridingVer = False
										
							else:
								if user.feetRect.move(0,sampleBlock.size/2).colliderect(block.rect): #move the block down a bit so that it detects ground, stops the fall, then falls again... reducing the sink glitch
									feetCollisions += 1
									
						if chestCollisions == 0:
							if user.chestRect.colliderect(block.rect):
								chestCollisions += 1
						if headCollisions == 0:
							if user.headRect.colliderect(block.rect):
								headCollisions += 1
						if topCollisions == 0:
							if user.headRect.inflate(user.headSize,0).colliderect(block.rect):
								topCollisions += 1
								
					#enable for mouse destruction (used for testing)
					# if block.rect.colliderect(testBox.rect):
						# damage += 1
					
					#if the hitbox of a weapon collides with the current block 
					if goldSword.attacking:
						if block.rect.colliderect(goldSword.rect):
							damage += s.swordDmgToBlocks
						
					if longSpear.attacking:
						if block.rect.colliderect(longSpear.rect):
							damage += s.spearDmgToBlocks
						
					if fist.attacking:
						if block.rect.colliderect(fist.rect):
							damage += s.fistDmgToBlocks
					
					#hitting blocks with the back of the gun turned out to be pretty annoying, yolo
					# if akRifle.attacking: #hit with end of rifle
						# if block.rect.colliderect(akRifle.rect):
							# damage += 1
					
					# if shotGun.attacking: #hit with end of rifle
						# if block.rect.colliderect(shotGun.rect):
							# damage += 1
									
					#check if any bullet collides with the current block
					for item in bullets:
						if item.bulletActive:
							if item.bx > user.x+ 1100*scalar and item.bx < user.x - 300 * scalar:
								item.bulletActive = False
							if item.bulletRect.colliderect(block.rect):
								if block.type != "=":
									damage += s.bulletDmgToBlocks
									item.impact = True
						if item.shellActive:
							if item.shellRect.colliderect(block.rect):
								item.shellFalling = False
						if not item.shellActive:
							if not item in deleteBulletsList:
								deleteBulletsList.append(item)
								
					#check if any pellet collides with the current block
					for item in pelletsList:
						for i in range(8):
							if item.pxs[i] < user.x + 1100*scalar and item.pxs[i] > user.x - 300 * scalar:
								if item.px > user.x+ 1100*scalar and item.px < user.x - 300 * scalar:
									item.pelletActives[i] = False
								if item.pelletsActive[i]:
									if item.pelletRects[i].colliderect(block.rect):
										if block.type != "=":
											damage += s.pelletDmgToBlocks
											item.impacts[i] = True
							if item.shellActive:
								if item.shellRect.colliderect(block.rect):
									item.shellFalling = False
							if not item.shellActive:
								if not item in deletePelletsList:
									deletePelletsList.append(item)
									
					#check if any ped bullets shot the block
					for item in pedBullets:
						if item.bulletActive:
							if item.bx > user.x+ 1100*scalar or item.bx < user.x - 300 * scalar:
								item.bulletActive = False
							if item.bx < user.x + 1100*scalar and item.bx > user.x - 300 * scalar:
								if item.bulletRect.colliderect(block.rect):
									if block.type != "=":
										item.impact = True
										damage += s.pedBulletDmgToBlocks
						if not item.shellActive:
							if not item in deletePedBulletsList:
								deletePedBulletsList.append(item)	
								
					#check if any ped pellets shot the block
					for item in pedPelletsList:
						for i in range(8):
							if item.pxs[i] < user.x + 1100*scalar or item.pxs[i] > user.x - 300 * scalar:
								if item.px > user.x+ 1100*scalar and item.px < user.x - 300 * scalar:
									item.pelletActives[i] = False
								if item.pelletsActive[i]:
									if user.x < user.x + 1100*scalar and user.x > user.x - 300 * scalar:
										if item.pelletRects[i].colliderect(block.rect):
											if block.type != "=":
												item.impacts[i] = True
												damage += s.pedPelletDmgToBlocks
							if not item.shellActive:
								if not item in deletePedPelletsList:
									deletePedPelletsList.append(item)
						
					#check if the current block collides with any other block
					for otherBlock in blocks:
						if collisions >= block.limit and not (block.type == "_" or block.type == "|" or block.type == "/" or block.type == "\\"):
							break
						if otherBlock.broken:
							continue
						if otherBlock.x < user.x + 1100*scalar + sampleBlock.size and otherBlock.x > user.x - 300*scalar - sampleBlock.size:
							if otherBlock is not block:
								if block.rect.colliderect(otherBlock.rect):
									collisions += 1
									if (block.type == "_" or block.type == "|" or block.type == "/" or block.type == "\\") and not (otherBlock.type == "_" or otherBlock.type == "|" or otherBlock.type == "/" or otherBlock.type == "\\"):
										block.changeDirection()
										
				else:
					block.dustSize += s.dustScaling*scalar
					block.frames[block.currentFrame] = pygame.transform.scale(loadImage(block.dust), (int(block.dustSize),int(block.dustSize)))
					if block.dustSize > block.size*s.dustClearsWhenSizeHasBeenMultipliedBy:
						deleteList.append(block)
				block.update(scalar,damage,collisions)
				block.draw(world)
			if block.rect[1] > world_height:
				deleteList.append(block)
		
		##ped damage calc
		if goldSword.attacking:
			for p in peds:
				if p.headAt < p.headLen-1:
					if goldSword.rect.colliderect(p.headRect):
						p.headAt+=s.swordDmgToPedsHead
				if p.chestAt < p.chestLen-1:
					if goldSword.rect.colliderect(p.chestRect):
						p.chestAt+=s.swordDmgToPedsChest
				if p.feetAt < p.feetLen-1:
					if goldSword.rect.colliderect(p.feetRect):
						p.feetAt+=s.swordDmgToPedsFeet
		if longSpear.attacking:
			for p in peds:
				if p.headAt < p.headLen-1:
					if longSpear.rect.colliderect(p.headRect):
						p.headAt+=s.spearDmgToPedsHead
				if p.chestAt < p.chestLen-1:
					if longSpear.rect.colliderect(p.chestRect):
						p.chestAt+=s.spearDmgToPedsChest
				if p.feetAt < p.feetLen-1:
					if longSpear.rect.colliderect(p.feetRect):
						p.feetAt+=s.spearDmgToPedsFeet
		if fist.attacking:
			for p in peds:
				if p.headAt < p.headLen-1:
					if fist.rect.colliderect(p.headRect):
						p.headAt+=s.fistDmgToPedsHead
				if p.chestAt < p.chestLen-1:
					if fist.rect.colliderect(p.chestRect):
						p.chestAt+=s.fistDmgToPedsChest
				if p.feetAt < p.feetLen-1:
					if fist.rect.colliderect(p.feetRect):
						p.feetAt+=s.fistDmgToPedsFeet
		if akRifle.attacking: #hit with end of rifle
			for p in peds:
				if p.headAt < p.headLen-1:
					if akRifle.rect.colliderect(p.headRect):
						p.headAt+=s.akRifleMeleeDmgToPedsHead
				if p.chestAt < p.chestLen-1:
					if akRifle.rect.colliderect(p.chestRect):
						p.chestAt+=s.akRifleMeleeDmgToPedsChest
				if p.feetAt < p.feetLen-1:
					if akRifle.rect.colliderect(p.feetRect):
						p.feetAt+=s.akRifleMeleeDmgToPedsFeet
		if shotGun.attacking: #hit with end of rifle
			for p in peds:
				if p.headAt < p.headLen-1:
					if shotGun.rect.colliderect(p.headRect):
						p.headAt+=s.shotgunMeleeDmgToPedsHead
				if p.chestAt < p.chestLen-1:
					if shotGun.rect.colliderect(p.chestRect):
						p.chestAt+=s.shotgunMeleeDmgToPedsChest
				if p.feetAt < p.feetLen-1:
					if shotGun.rect.colliderect(p.feetRect):
						p.feetAt+=s.shotgunMeleeDmgToPedsFeet
						
		#check if any bullet collides with any ped
		for item in bullets:
			if item.bulletActive:
				if item.bx > user.x+ 1100*scalar and item.bx < user.x - 300 * scalar:
					item.bulletActive = False
				for p in peds:
					if item.bx < p.x + 50*scalar and item.bx > p.x - 50 * scalar:
						if p.headAt < p.headLen-1:
							if item.bulletRect.colliderect(p.headRect):
								p.headAt+=s.bulletDmgToPedsHead
								item.impact = True
						if p.chestAt < p.chestLen-1:
							if item.bulletRect.colliderect(p.chestRect):
								p.chestAt+=s.bulletDmgToPedsChest
								item.impact = True
						if p.feetAt < p.feetLen-1:
							if item.bulletRect.colliderect(p.feetRect):
								p.feetAt+=s.bulletDmgToPedsFeet
								item.impact = True
				# if item.bulletRect.colliderect(block.rect):
					# damage += s.bulletDmgToBlocks
					# if block.type != "=":
						# item.impact = True
			if item.shellActive:
				if item.shellRect.colliderect(block.rect):
					item.shellFalling = False
			if not item.shellActive:
				if not item in deleteBulletsList:
					deleteBulletsList.append(item)
					
		#check if any pellet collides with any ped
		for item in pelletsList:
			for i in range(8):
				if item.pxs[i] < user.x + 1100*scalar and item.pxs[i] > user.x - 300 * scalar:
					if item.px > user.x+ 1100*scalar and item.px < user.x - 300 * scalar:
						item.pelletActives[i] = False
					if item.pelletsActive[i]:
						for p in peds:
							if p.x < user.x + 1100*scalar and p.x > user.x - 300 * scalar:
								if p.headAt < p.headLen-1:
									if item.pelletRects[i].colliderect(p.headRect):
										p.headAt+=s.pelletDmgToPedsHead
										item.impacts[i] = True
								if p.chestAt < p.chestLen-1:
									if item.pelletRects[i].colliderect(p.chestRect):
										p.chestAt+=s.pelletDmgToPedsChest
										item.impacts[i] = True
								if p.feetAt < p.feetLen-1:
									if item.pelletRects[i].colliderect(p.feetRect):
										p.feetAt+=s.pelletDmgToPedsFeet
										item.impacts[i] = True
				if item.shellActive:
					if item.shellRect.colliderect(block.rect):
						item.shellFalling = False
				if not item.shellActive:
					if not item in deletePelletsList:
						deletePelletsList.append(item)
		
		

		##portal
		#if the user collides with the portal
		#then bring him into the next map
		if portal.x < user.x + 100*scalar and portal.x > user.x - 100 * scalar:
			if user.headRect.colliderect(portal.rect) or user.chestRect.colliderect(portal.rect) or user.feetRect.colliderect(portal.rect):
				level += 1
				if level == len(maps):
					print "You Won!"
					sys.exit()
				else:
					pedCount,pedWeapons = levelGen(blocks,peds,maps[level])
		
		##object erasing
		for block in deleteList:
			blocks.remove(block)
			deleteList.remove(block)
			
		for item in deleteBulletsList:
			bullets.remove(item)
			deleteBulletsList.remove(item)
			
		for item in deletePedBulletsList:
			pedBullets.remove(item)
			deletePedBulletsList.remove(item)
			
		for item in deletePelletsList:
			pelletsList.remove(item)
			deletePelletsList.remove(item)
			
		for item in deletePedPelletsList:
			pedPelletsList.remove(item)
			deletePedPelletsList.remove(item)
		
		##update and draw portal
		if portal.x < user.x + 1100*scalar and portal.x > user.x - 300 * scalar:
			portal.update(scalar,pDamage,pCollisions)
			portal.draw(world)
		
		##update the user
		if ridingHor:
			user.teleport(user.x+s.horizontalPlatformSpeed*2*ridingHorDirection,user.y)
		if ridingVer:
			user.teleport(user.x,user.y+s.verticalPlatformSpeed*2*ridingVerDirection)
		user.update(jump,left,right,headCollisions,topCollisions,chestCollisions,feetCollisions)
		print user.y/sampleBlock.size
		
		##ped AI and updating
		pNum = -1
		for p in peds:
			pNum+=1
			if p.x < user.x + 1100*scalar and p.x > user.x - 300 * scalar:
				left,right = False,False
				#determine how they move based on their weapon type
				if pedWeapons[pNum].type == "sword":
					if user.x + s.swordPedsMinRangeFromUser*scalar < p.x:
						left = True
					if user.x + s.swordPedsMaxRangeFromUser*scalar > p.x:
						right = True
					if pedChestCollisions[pNum] > 0:
						p.jump = True
						p.jumpDuration = 5
				elif pedWeapons[pNum].type == "spear":
					if user.x + s.spearPedsMinRangeFromUser*scalar < p.x:
						left = True
					if user.x + s.spearPedsMaxRangeFromUser*scalar > p.x:
						right = True
					if pedChestCollisions[pNum] > 0:
						p.jump = True
						p.jumpDuration = 5
				elif pedWeapons[pNum].type == "sg":
					if user.x +s.shotgunPedsMinRangeFromUser*scalar < p.x:
						left = True
					if user.x + s.shotgunPedsMaxRangeFromUser*scalar > p.x:
						right = True
					if pedChestCollisions[pNum] > 0:
						p.jump = True
						p.jumpDuration = 5
				elif pedWeapons[pNum].type == "ak":
					if user.x + s.akRiflePedsMinRangeFromUser*scalar < p.x or user.x + 300*scalar < p.x:
						left = True
					if user.x + s.akRiflePedsMaxRangeFromUser*scalar > p.x or user.x + 300*scalar > p.x:
						right = True
					if pedChestCollisions[pNum] > 0:
						p.jump = True
						p.jumpDuration = s.howLongPedsKeepJumpingToTryToGetOverBlocks
				p.update(p.jump,left,right,pedHeadCollisions[pNum],pedTopCollisions[pNum],pedChestCollisions[pNum],pedFeetCollisions[pNum])
				pedWeapons[pNum].update(p.x,p.y,user.chestX,user.chestY,True,False,False)
				#fire the proper projectile(s) based on the weapon type
				if pedWeapons[pNum].currentFrame == 1 and not pedWeapons[pNum].retracting and pedWeapons[pNum].type == "ak":
					pedBullets.append(bullet.Bullet(rifleBulletFrames,pedWeapons[pNum].muzzelx,pedWeapons[pNum].muzzely,pedWeapons[pNum].flipped,pedWeapons[pNum].angle))
				if pedWeapons[pNum].currentFrame == 1 and not pedWeapons[pNum].retracting and pedWeapons[pNum].type == "sg":
					pedPelletsList.append(pellets.Pellets(pelletFrames,pelletShellImage,pedWeapons[pNum].muzzelx,pedWeapons[pNum].muzzely,pedWeapons[pNum].flipped,pedWeapons[pNum].angle))
				#erase the ped if he died or falls off the map
				if p.y > world_height or p.dead:
					peds.remove(p)
					del pedWeapons[pNum]
		
		##update and draw projectiles
		for item in pedBullets:
			item.update(scalar)
			item.draw(world)
		for item in pedPelletsList:
			item.update(scalar)
			item.draw(world)
		
		##check if any ped projectiles shot the user
		for item in pedBullets:
			if item.bulletActive:
				if item.bx > user.x+ 1100*scalar or item.bx < user.x - 300 * scalar:
					item.bulletActive = False
				if item.bx < user.x + 50*scalar and item.bx > user.x - 50 * scalar:
					if user.headAt < user.headLen-1:
						if item.bulletRect.colliderect(user.headRect):
							user.headAt+=s.pedsBulletDmgToUsersHead
							item.impact = True
					if user.chestAt < user.chestLen-1:
						if item.bulletRect.colliderect(user.chestRect):
							user.chestAt+=s.pedsBulletDmgToUsersChest
							item.impact = True
					if user.feetAt < user.feetLen-1:
						if item.bulletRect.colliderect(user.feetRect):
							user.feetAt+=s.pedsBulletDmgToUsersFeet
							item.impact = True
					# for block in blocks:
						# if block.x < user.x + 1100*scalar and block.x > user.x - 300 * scalar:
							# if item.bulletRect.colliderect(block.rect):
								# item.bulletActive = False
			if not item.shellActive:
				if not item in deletePedBulletsList:
					deletePedBulletsList.append(item)
					
		for item in pedPelletsList:
			for i in range(8):
				if item.pxs[i] < user.x + 1100*scalar or item.pxs[i] > user.x - 300 * scalar:
					if item.px > user.x+ 1100*scalar and item.px < user.x - 300 * scalar:
						item.pelletActives[i] = False
					if item.pelletsActive[i]:
						if user.x < user.x + 1100*scalar and user.x > user.x - 300 * scalar:
							if user.headAt < user.headLen-1:
								if item.pelletRects[i].colliderect(user.headRect):
									user.headAt+=s.pedsPelletDmgToUsersHead
									item.impacts[i] = True
							if user.chestAt < user.chestLen-1:
								if item.pelletRects[i].colliderect(user.chestRect):
									user.chestAt+=s.pedsPelletDmgToUsersChest
									item.impacts[i] = True
							if user.feetAt < user.feetLen-1:
								if item.pelletRects[i].colliderect(user.feetRect):
									user.feetAt+=s.pedsPelletDmgToUsersFeet
									item.impacts[i] = True
				if not item.shellActive:
					if not item in deletePedPelletsList:
						deletePedPelletsList.append(item)
		
		##check if any ped weapons hit the user (non-projectile)
		pNum = -1
		for p in peds:
			pNum+=1
			if p.x < user.x + 100*scalar and p.x > user.x - 100 * scalar:
				if pedWeapons[pNum].attacking:
					if user.headAt < user.headLen-1:
						if pedWeapons[pNum].rect.colliderect(user.headRect):
							user.headAt+=s.pedsMeleeDmgToUsersHead
					if user.chestAt < user.chestLen-1:
						if pedWeapons[pNum].rect.colliderect(user.chestRect):
							user.chestAt+=s.pedsMeleeDmgToUsersChest
					if user.feetAt < user.feetLen-1:
						if pedWeapons[pNum].rect.colliderect(user.feetRect):
							user.feetAt+=s.pedsMeleeDmgToUsersFeet
		
		if user.y > world_height or user.dead:
			print "You Lost!",world_height/sampleBlock.size, world_width/sampleBlock.size
			sys.exit()
		
		##show hitboxes
		#doesn't show ped hitboxes yet
		if pressed[K_h]:
			pygame.draw.rect(world,(255,0,0),portal.rect)
			pygame.draw.rect(world,(255,0,0),shotGun.iconRect)
			pygame.draw.rect(world,(255,0,0),shotGun.rect)
			pygame.draw.rect(world,(255,0,0),akRifle.iconRect)
			pygame.draw.rect(world,(255,0,0),akRifle.rect)
			pygame.draw.rect(world,(255,0,0),goldSword.iconRect)
			pygame.draw.rect(world,(255,0,0),goldSword.rect)
			pygame.draw.rect(world,(255,0,0),longSpear.iconRect)
			pygame.draw.rect(world,(255,0,0),longSpear.rect)
			pygame.draw.rect(world,(255,0,0),fist.rect)
			pygame.draw.rect(world,(255,0,0),testBox.rect)
			pygame.draw.rect(world,(150,0,0),user.headRect.inflate(user.headSize,0))
			pygame.draw.rect(world,(255,0,0),user.headRect)
			pygame.draw.rect(world,(255,0,0),user.chestRect)
			pygame.draw.rect(world,(255,0,0),user.feetRect)
			#pygame.draw.rect(world,(255,0,0),block1.rect)
			for block in blocks:
				pygame.draw.rect(world,(255,0,0),block.rect)
			
			for item in bullets:
				pygame.draw.rect(world,(255,0,0),item.bulletRect)
				pygame.draw.rect(world,(255,0,0),item.shellRect)
				
			for item in pelletsList:
				for i in range(8):
					pygame.draw.rect(world,(255,0,0),item.pelletRects[i])
				pygame.draw.rect(world,(255,0,0),item.shellRect)
		
		##draw the mouse box
		testBox.draw(world)
		
		##draw the world to screen
		screen.blit(world, (world_x, world_y, width, height))
		
		##onscreen debugging
		label2 = font.render(str(int(clock.get_fps())), 1, (255,255,255))
		screen.blit(label2, (30*scalar,30*scalar))
		
		##display a message on the screen
		if not message is None:
			screen.blit(message, (380*scalar,50*scalar))
		pygame.display.flip()
		if not message is None: #dat grammar :D
			pygame.time.wait(3000)


## this calls the 'main' function when this script is executed
if __name__ == '__main__': main()