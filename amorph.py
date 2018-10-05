#Coded by Daniel Busis
#Inspired by (and art taken from) https://bongo.cat
#Bongo sounds from https://www.freesound.org
#Music from: https://www.bensound.com

import pygame
import pygame.gfxdraw
import random
import math

class AmorphGameController():
	def __init__(self):
		self.enemy_group = pygame.sprite.Group()
		self.player_group = pygame.sprite.GroupSingle()
		self.player = PlayerSprite()
		self.player_group.add(self.player)

		self.SCREEN_X = 800
		self.SCREEN_Y = 600

		self.bg_color = pygame.Color(200,200,200)
		self.screen = pygame.display.set_mode((self.SCREEN_X,self.SCREEN_Y))
		
		self.game_clock = pygame.time.Clock()
		
		
class PlayerSprite(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.pos = [400,200]
		self.size = (30,30)
		self.radius = 14
		self.rect = pygame.Rect(self.pos, self.size)
		
		self.speed = 3.5
		
		self.image = pygame.Surface([30,30], pygame.SRCALPHA)
		self.color = pygame.Color(30,30,30)
		pygame.gfxdraw.filled_circle(self.image, 15, 15, self.radius, self.color)

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
		
		
class GreenSprite(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.size = (30,30)
		self.radius = 14
		
		self.death_event = pygame.event.Event(pygame.USEREVENT, {"descript":"enemy_death"})
		
		angle = 2*math.pi*random.random()
		self.direction = [math.cos(angle), math.sin(angle)]
		self.speed = 2
		
		self.w, self.h = pygame.display.get_surface().get_size()
		
		self.pos = self._random_start_pos()
		self.rect = pygame.Rect(self.pos, self.size)
		
		self.image = pygame.Surface([30, 30], pygame.SRCALPHA)
		self.color = pygame.Color(0,random.randrange(100,200),0)
		pygame.gfxdraw.filled_circle(self.image, 15, 15, self.radius, self.color)
		
	def update(self):
		self.pos[0] += self.speed*self.direction[0]
		self.pos[1] += self.speed*self.direction[1]
		if (self.pos[0] > self.w + self.size[0]/2
				or self.pos[1]>self.h + self.size[1]/2
				or self.pos[0]<-self.size[0]/2
				or self.pos[1]<-self.size[1]/2):
			pygame.event.post(self.death_event)
			self.kill()

		self.rect = pygame.Rect((self.pos[0]-self.size[0]/2, self.pos[1]-self.size[1]/2), self.size)	
		
	def _random_start_pos(self):
		horiz_edge = bool(random.getrandbits(1))
		if horiz_edge:
			start_pos_x = random.randrange(self.w+1)
			start_pos_y = 0
			if self.direction[1] < 0:
				start_pos_y = self.h
			return [start_pos_x, start_pos_y]
		else:
			start_pos_y = random.randrange(self.h+1)
			start_pos_x = 0
			if self.direction[0] < 0:
				start_pos_x = self.w
			return [start_pos_x, start_pos_y]

def main():
	pygame.init()	
	
	game_control = AmorphGameController()
	pygame.display.set_caption("Amorph")	
	
	for i in range(10):
		game_control.enemy_group.add(GreenSprite())
	
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
			if event.type == pygame.USEREVENT:
				if event.descript=="enemy_death":
					game_control.enemy_group.add(GreenSprite())

		_check_blob_bounces(game_control)
		game_control.player_group.update()
		game_control.enemy_group.update()
		_update_screen(game_control)
		game_control.game_clock.tick(60)
	pygame.quit()

def _update_screen(game_control):
	game_control.screen.fill(game_control.bg_color)
	game_control.enemy_group.draw(game_control.screen)
	game_control.player_group.draw(game_control.screen)
	#print(pygame.sprite.spritecollide(game_control.player_group.sprite, game_control.enemy_group, False, collided=pygame.sprite.collide_circle))
	pygame.display.update()

def _check_blob_bounces(game_control):
	blob_list = game_control.enemy_group.sprites()
	for i in range(len(blob_list)-1):
		for j in range(i+1, len(blob_list)):
			if pygame.sprite.collide_circle(blob_list[i], blob_list[j]):
				_bounce(blob_list[i],blob_list[j])

def _bounce(blob1, blob2):
	cent1 = blob1.pos
	cent2 = blob2.pos
	direc1 = [cent1[i]-cent2[i] for i in range(2)]
	direc1_len = (direc1[0]**2+direc1[1]**2)**(1/2)
	direc1 = [a/direc1_len for a in direc1]
	direc2 = [-a for a in direc1]
	blob1.direction = direc1
	blob2.direction = direc2
	
if __name__=="__main__":
	main()
