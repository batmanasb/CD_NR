

import pygame,os
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.set_num_channels(300)

soundEffects = {}

#ambience sound effects
soundEffects['Background'] = os.path.join('ambience','Background.mp3')

#Gun sound effects
soundEffects['RifleShot'] = os.path.join('guns','RifleShot.wav')
soundEffects['ShotgunShot'] = os.path.join('guns','ShotgunShot.wav')
soundEffects['ShotgunPump'] = os.path.join('guns','ShotgunPump.wav')

#Player sound effects
soundEffects['PlayerHit'] = os.path.join('player','PlayerHit.mp3')

#Monster and enemy sound effects
soundEffects['AlienScream'] = os.path.join('enemy','AlienScream.mp3')
soundEffects['InsectScreech'] = os.path.join('enemy','InsectScreech.mp3')
soundEffects['MonsterHorseScream'] = os.path.join('enemy','MonsterHorseScream.mp3')
soundEffects['MonsterHorseScream2'] = os.path.join('enemy','MonsterHorseScream2.mp3')
soundEffects['MonsterScreech'] = os.path.join('enemy','MonsterScreech.mp3')

def play(soundName):
	sound = pygame.mixer.Sound(os.path.join('sounds', soundEffects[soundName]))
	sound.set_volume(1.0)
	sound.play(0)
	
def loop(soundName):
	sound = pygame.mixer.music.load(os.path.join('sounds', soundEffects[soundName]))
	pygame.mixer.music.play(-1)
		
