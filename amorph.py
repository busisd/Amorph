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
		self.big_enemy_group = pygame.sprite.Group()
		self.biter_enemy_group = pygame.sprite.Group()
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
		self.size = (40,40)
		self.radius = 19
		self.rect = pygame.Rect(self.pos, self.size)
		
		self.speed = 3.2
		
		self.image = pygame.Surface(self.size, pygame.SRCALPHA)
		self.color = pygame.Color(30,30,30)
		pygame.gfxdraw.filled_circle(self.image, int(self.size[0]/2), int(self.size[0]/2), self.radius, self.color)

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
		self.size = (40,40)
		self.radius = 19
		
		self.death_event = pygame.event.Event(pygame.USEREVENT, {"descript":"blob_death"})
		
		angle = 2*math.pi*random.random()
		self.direction = [math.cos(angle), math.sin(angle)]
		self.speed = 2.5
		
		self.w, self.h = pygame.display.get_surface().get_size()
		
		self.pos = self._random_start_pos()
		self.rect = pygame.Rect(self.pos, self.size)
		
		self.image = pygame.Surface(self.size, pygame.SRCALPHA)
		self.color = pygame.Color(0,random.randrange(100,200),0)
		pygame.gfxdraw.filled_circle(self.image, int(self.size[0]/2), int(self.size[0]/2), self.radius, self.color)
		
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

class BigGreenSprite(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.size = (60,60)
		self.radius = 29
		
		self.death_event = pygame.event.Event(pygame.USEREVENT, {"descript":"big_blob_death"})
		
		self.angle = 2*math.pi*random.random()
		self.speed = 2
		self.rotate_speed = math.pi/120
		
		self.w, self.h = pygame.display.get_surface().get_size()
		
		self.pos = self._random_start_pos()
		self.rect = pygame.Rect(self.pos, self.size)
		
		self.image = pygame.Surface(self.size, pygame.SRCALPHA)
		self.color = pygame.Color(0,random.randrange(100,200),0)
		pygame.gfxdraw.filled_circle(self.image, int(self.size[0]/2), int(self.size[0]/2), self.radius, self.color)
		
	def update(self, player_pos):			
		x_dif = player_pos[0] - self.pos[0] 
		y_dif =  player_pos[1] - self.pos[1]
		if x_dif == 0 and y_dif == 0:
			target_angle = 0
		elif x_dif == 0:
			if y_dif > 0:
				target_angle = math.pi/2
			else:
				target_angle = math.pi*3/2
		elif y_dif == 0:
			if x_dif > 0:
				target_angle = 0
			else:
				target_angle = math.pi
		else:
			target_angle = math.atan2(y_dif, x_dif)
		target_angle = self._normify_angle(target_angle)
		
		angle_dif = self._normify_angle(target_angle - self.angle)
		if abs(angle_dif) < self.rotate_speed:
			self.angle = target_angle
		else:
			if angle_dif < math.pi:
				self.angle += self.rotate_speed
			else:
				self.angle -= self.rotate_speed
			self.angle = self._normify_angle(self.angle)
		
		direction = [math.cos(self.angle), math.sin(self.angle)]
		self.pos[0] += self.speed*direction[0]
		self.pos[1] += self.speed*direction[1]
		if (self.pos[0] > self.w + self.size[0]/2
				or self.pos[1]>self.h + self.size[1]/2
				or self.pos[0]<-self.size[0]/2
				or self.pos[1]<-self.size[1]/2):
			pygame.event.post(self.death_event)
			self.kill()

		self.rect = pygame.Rect((self.pos[0]-self.size[0]/2, self.pos[1]-self.size[1]/2), self.size)	

	def _normify_angle(self, angle):
		if angle > 2*math.pi:
			angle -= 2*math.pi
		if angle < 0:
			angle += 2*math.pi
		return angle
	
	def _random_start_pos(self):
		direction = [math.cos(self.angle), math.sin(self.angle)]
		horiz_edge = bool(random.getrandbits(1))
		if horiz_edge:
			start_pos_x = random.randrange(self.w+1)
			start_pos_y = 0
			if direction[1] < 0:
				start_pos_y = self.h
			return [start_pos_x, start_pos_y]
		else:
			start_pos_y = random.randrange(self.h+1)
			start_pos_x = 0
			if direction[0] < 0:
				start_pos_x = self.w
			return [start_pos_x, start_pos_y]

			
			
class BiterSprite(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.size = (40,40)
		self.radius = 19
		
		self.death_event = pygame.event.Event(pygame.USEREVENT, {"descript":"biter_death"})
		
		self.angle = 2*math.pi*random.random()
		self.rotate_speed = math.pi/150
		
		self.w, self.h = pygame.display.get_surface().get_size()
		
		self.pos = self._random_start_pos()
		self.rect = pygame.Rect(self.pos, self.size)
		
		self.image = pygame.Surface(self.size, pygame.SRCALPHA)
		self.color_chase = pygame.Color(0,0,random.randrange(100,200))
		self.color_lunge = pygame.Color(random.randrange(100,200),0,0)
		pygame.gfxdraw.filled_circle(self.image, int(self.size[0]/2), int(self.size[0]/2), self.radius, self.color_chase)
		
		self.is_lunging = False
		self.lunge_cur_ticks = 0
		self.lunge_max_ticks = 60
		self.lunge_speed = 4.5
		self.chase_speed = 2.6
		self.lunge_max_dist = self.lunge_max_ticks*self.lunge_speed
		
	def update(self, player_pos):
		if self.is_lunging:
			self.update_lunge(player_pos)
		else:
			self.update_chase(player_pos)
	
	def update_lunge(self, player_pos):
		direction = [math.cos(self.angle), math.sin(self.angle)]
		self.pos[0] += self.lunge_speed*direction[0]
		self.pos[1] += self.lunge_speed*direction[1]
		self.lunge_cur_ticks += 1
		if self.lunge_cur_ticks > self.lunge_max_ticks:
			self.lunge_cur_ticks = 0
			self.is_lunging = False
			pygame.gfxdraw.filled_circle(self.image, int(self.size[0]/2), int(self.size[0]/2), self.radius, self.color_chase)
		if (self.pos[0] > self.w + self.size[0]/2
				or self.pos[1]>self.h + self.size[1]/2
				or self.pos[0]<-self.size[0]/2
				or self.pos[1]<-self.size[1]/2):
			pygame.event.post(self.death_event)
			self.kill()
		self.rect = pygame.Rect((self.pos[0]-self.size[0]/2, self.pos[1]-self.size[1]/2), self.size)	
	
	def update_chase(self, player_pos):
		x_dif = player_pos[0] - self.pos[0] 
		y_dif =  player_pos[1] - self.pos[1]
		if x_dif == 0 and y_dif == 0:
			target_angle = 0
		elif x_dif == 0:
			if y_dif > 0:
				target_angle = math.pi/2
			else:
				target_angle = math.pi*3/2
		elif y_dif == 0:
			if x_dif > 0:
				target_angle = 0
			else:
				target_angle = math.pi
		else:
			target_angle = math.atan2(y_dif, x_dif)
				
		target_angle = self._normify_angle(target_angle)
		
		angle_dif = self._normify_angle(target_angle - self.angle)
		if abs(angle_dif) < self.rotate_speed:
			self.angle = target_angle
			
			dist_to_player = (x_dif**2+y_dif**2)**(1/2)
			if dist_to_player < self.lunge_max_dist:
				self.is_lunging = True
				pygame.gfxdraw.filled_circle(self.image, int(self.size[0]/2), int(self.size[0]/2), self.radius, self.color_lunge)
		else:
			if angle_dif < math.pi:
				self.angle += self.rotate_speed
			else:
				self.angle -= self.rotate_speed
			self.angle = self._normify_angle(self.angle)
		
		direction = [math.cos(self.angle), math.sin(self.angle)]
		self.pos[0] += self.chase_speed*direction[0]
		self.pos[1] += self.chase_speed*direction[1]
		
		if (self.pos[0] > self.w + self.size[0]/2
				or self.pos[1]>self.h + self.size[1]/2
				or self.pos[0]<-self.size[0]/2
				or self.pos[1]<-self.size[1]/2):
			pygame.event.post(self.death_event)
			self.kill()

		self.rect = pygame.Rect((self.pos[0]-self.size[0]/2, self.pos[1]-self.size[1]/2), self.size)	

	def _normify_angle(self, angle):
		if angle > 2*math.pi:
			angle -= 2*math.pi
		if angle < 0:
			angle += 2*math.pi
		return angle
	
	def _random_start_pos(self):
		direction = [math.cos(self.angle), math.sin(self.angle)]
		horiz_edge = bool(random.getrandbits(1))
		if horiz_edge:
			start_pos_x = random.randrange(self.w+1)
			start_pos_y = 0
			if direction[1] < 0:
				start_pos_y = self.h
			return [start_pos_x, start_pos_y]
		else:
			start_pos_y = random.randrange(self.h+1)
			start_pos_x = 0
			if direction[0] < 0:
				start_pos_x = self.w
			return [start_pos_x, start_pos_y]

def main():
	pygame.init()	
	
	game_control = AmorphGameController()
	pygame.display.set_caption("Amorph")	
	
	for i in range(10):
		game_control.enemy_group.add(GreenSprite())
	game_control.big_enemy_group.add(BigGreenSprite())
	game_control.biter_enemy_group.add(BiterSprite())
	
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
				if event.descript=="blob_death":
					game_control.enemy_group.add(GreenSprite())
				if event.descript=="big_blob_death":
					game_control.big_enemy_group.add(BigGreenSprite())
				if event.descript=="biter_death":
					game_control.biter_enemy_group.add(BiterSprite())


		_check_blob_bounces(game_control)
		_check_big_small_bounces(game_control)
		game_control.player_group.update()
		game_control.enemy_group.update()
		game_control.big_enemy_group.update(game_control.player_group.sprite.pos)
		game_control.biter_enemy_group.update(game_control.player_group.sprite.pos)
		_update_screen(game_control)
		game_control.game_clock.tick(60)
	pygame.quit()

def _update_screen(game_control):
	game_control.screen.fill(game_control.bg_color)
	game_control.enemy_group.draw(game_control.screen)
	game_control.big_enemy_group.draw(game_control.screen)
	game_control.biter_enemy_group.draw(game_control.screen)
	game_control.player_group.draw(game_control.screen)
	#print(pygame.sprite.spritecollide(game_control.player_group.sprite, game_control.enemy_group, False, collided=pygame.sprite.collide_circle))
	pygame.display.update()

def _check_blob_bounces(game_control):
	blob_list = game_control.enemy_group.sprites()
	for i in range(len(blob_list)-1):
		for j in range(i+1, len(blob_list)):
			if pygame.sprite.collide_circle(blob_list[i], blob_list[j]):
				_bounce_smalls(blob_list[i],blob_list[j])

def _check_big_small_bounces(game_control):
	small_blob_list = game_control.enemy_group.sprites()
	big_blob_list = game_control.big_enemy_group.sprites()
	for small_blob in small_blob_list:
		for big_blob in big_blob_list:
			if pygame.sprite.collide_circle(small_blob, big_blob):
				_bounce_small_big(small_blob,big_blob)
	
def _bounce_smalls(blob1, blob2):
	cent1 = blob1.pos
	cent2 = blob2.pos
	direc1 = [cent1[i]-cent2[i] for i in range(2)]
	direc1_len = (direc1[0]**2+direc1[1]**2)**(1/2)
	if direc1_len==0:
		direc1_len=.1
	direc1 = [a/direc1_len for a in direc1]
	direc2 = [-a for a in direc1]
	blob1.direction = direc1
	blob2.direction = direc2
	
def _bounce_small_big(small_blob, big_blob):
	cent1 = small_blob.pos
	cent2 = big_blob.pos
	direc = [cent1[i]-cent2[i] for i in range(2)]
	direc_len = (direc[0]**2+direc[1]**2)**(1/2)
	if direc_len==0:
		direc_len=.1
	direc = [a/direc_len for a in direc]
	small_blob.direction = direc
	
if __name__=="__main__":
	main()
