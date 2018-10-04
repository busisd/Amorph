#Coded by Daniel Busis
#Inspired by (and art taken from) https://bongo.cat
#Bongo sounds from https://www.freesound.org
#Music from: https://www.bensound.com

import pygame
import random

class AmorphGameController():
	def __init__(self):
		self.enemy_group = pygame.sprite.Group()
		self.player_group = pygame.sprite.Group()
		self.player = PlayerSprite()
		self.player_group.add(self.player)

		self.SCREEN_X = 800
		self.SCREEN_Y = 600

		self.bg_color = pygame.Color(200,200,200)
		self.screen = pygame.display.set_mode((self.SCREEN_X,self.SCREEN_Y))
		
class PlayerSprite(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([30,30])
		self.color = pygame.Color(10,10,10)
		self.image.fill(self.color)
		self.pos = [400,200]
		self.size = (30,30)
		self.rect = pygame.Rect(self.pos, self.size)
		
		self.speed = 2.5
		
	def update(self):
		mouse_pos = pygame.mouse.get_pos()

		vec = [mouse_pos[0]-self.pos[0], mouse_pos[1]-self.pos[1]]
		vec_len = (vec[0]**2+vec[1]**2)**(1/2)
		if vec_len > self.speed:
			move_vec = [vec[0]/vec_len*self.speed, vec[1]/vec_len*self.speed]
			self.pos[0] += move_vec[0]
			self.pos[1] += move_vec[1]
		else:
			self.pos = [mouse_pos[0], mouse_pos[1]]
		self.rect = pygame.Rect((self.pos[0]-self.size[0]/2, self.pos[1]-self.size[1]/2), self.size)	
		
		
def main():
	pygame.init()	
	
	game_control = AmorphGameController()
	pygame.display.set_caption("Amorph")
	
	game_control.game_clock = pygame.time.Clock()
	
	running = True
	while(running):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button==1:
					print("click!")
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button==1:
					print("unclick!")

		game_control.player_group.update()
		_update_screen(game_control)
		game_control.game_clock.tick(60)
	pygame.quit()

def _update_screen(game_control):
	game_control.screen.fill(game_control.bg_color)
	game_control.player_group.draw(game_control.screen)
	pygame.display.update()
			
if __name__=="__main__":
	main()
