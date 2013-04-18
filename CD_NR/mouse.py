class Mouse:
	def __init__(self,(mx,my),wx,wy,image):
		self.x = mx-wx
		self.y = my-wy
		self.screen_x = mx
		self.screen_y = my
		self.image = image
		self.rect = image.get_rect()
		self.rect.move_ip(self.x,self.y)
	
	def draw(self,world):
		world.blit(self.image,(self.x,self.y))
	
	def update(self,(mx,my),wx,wy):
		self.x = mx-wx
		self.y = my-wy
		self.screen_x = mx
		self.screen_y = my
		self.rect = self.image.get_rect()
		self.rect.move_ip(self.x,self.y)