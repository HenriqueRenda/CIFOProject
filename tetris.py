

#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Very simple tetris implementation
# 
# Control keys:
# Down - Drop stone faster
# Left/Right - Move stone
# Up - Rotate Stone clockwise
# Escape - Quit game
# P - Pause game
#
# Have fun!

# Copyright (c) 2010 "Kevin Chabowski"<kevin@kch42.de>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

'''
This script is used apply genes to from the training script
'''
from random import choice
from random import randrange as rand
import pygame, sys, numpy, math, time
import tetrisUtils as TUtils
# The configuration
config = {
	'cell_size':  7,
	'cols':    10,
	'rows':    24,
	'delay':  750,
	'maxfps':  30
	}

colors = [
	(0,   0,   0  ),
	(255, 0,   0  ),
	(0,   150, 0  ),
	(0,   0,   255),
	(255, 120, 0  ),
	(255, 255, 0  ),
	(180, 0,   255),
	(0,   220, 220),
	(255, 255, 255)
]

# Define the shapes of the single parts
tetris_shapes = [
	[[1, 1, 1],
	[0, 1, 0]],

	[[0, 2, 2],
	[2, 2, 0]],

	[[3, 3, 0],
	[0, 3, 3]],

	[[4, 0, 0],
	[4, 4, 4]],

	[[0, 0, 5],
	[5, 5, 5]],

	[[6, 6, 6, 6]],

	[[7, 7],
	[7, 7]]
]

# Rotates a shape clockwise
def rotate_clockwise(shape):
	return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]

# checks if there is a collision in any direction
def check_collision(board, shape, offset):
	off_x, off_y = offset
	for cy, row in enumerate(shape):
		for cx, cell in enumerate(row):
			try:
				if cell and board[ cy + off_y ][ cx + off_x ]:
				  return True
			except IndexError:
				return True
	return False

# clearing a row for getting points
def remove_row(board, row):
	del board[row]
	return [[0 for i in range(config['cols'])]] + board

# Used for adding a stone to the board
def join_matrixes(mat1, mat2, mat2_off):
	off_x, off_y = mat2_off
	for cy, row in enumerate(mat2):
		for cx, val in enumerate(row):
			mat1[cy+off_y-1][cx+off_x] += val
	return mat1

# new game
def new_board():
	board = [[0 for x in range(config['cols'])] for y in range(config['rows'])]
	board += [[8 for x in range(config['cols'])]]
	return board

class Tetris(object):
	def __init__(self, screen, offsetScreen):
		self.width = config['cell_size']*config['cols']
		self.height = config['cell_size']*config['rows']
		self.screen = screen
		self.offsetScreen = offsetScreen
		self.gameover = False
		self.init_game()

	'''
	Creates random shape
	places shape at the top of the boar din the middle
	checks if collision - if yes game over
	'''  
	def new_stone(self):
		self.score += 1	# Updating score after every new stone
		self.stone = tetris_shapes[rand(len(tetris_shapes))]
		self.stone_x = int(config['cols'] / 2 - len(self.stone[0])/2)
		self.stone_y = 0
		if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
			self.gameover = True

	'''
	Starts a new game
	- new board
	- new stone
	'''
	def init_game(self):
		self.score = 0
		self.board = new_board()
		self.new_stone()

	# Show given message at the center of the board (for losing)
	def center_msg(self, msg):
		for i, line in enumerate(msg.splitlines()):
			msg_image =  pygame.font.Font(pygame.font.get_default_font(), 12).render(line, False, (255,255,255), (0,0,0))
			msgim_center_x, msgim_center_y = msg_image.get_size()
			msgim_center_x //= 2
			msgim_center_y //= 2
			self.screen.blit(msg_image, (self.width // 2-msgim_center_x + self.offsetScreen[0]*config['cell_size'], self.height // 2-msgim_center_y+i*22  + self.offsetScreen[1]*config['cell_size']))

	# Show given message at the center of the board (for losing)
	def show_score(self, msg):
		for i, line in enumerate(msg.splitlines()):
			msg_image =  pygame.font.Font(pygame.font.get_default_font(), 12).render(line, False, (255, 255, 255), (0,0,0))
			msgim_center_x, msgim_center_y = msg_image.get_size()
			msgim_center_x //= 2
			msgim_center_y //= 2
			self.screen.blit(msg_image, ((self.width)/10 + self.offsetScreen[0]*config['cell_size'], (self.height)/10 + self.offsetScreen[1]*config['cell_size']))

	'''
	draws a given matrix
	- used for both the board and the piece
	'''
	def draw_matrix(self, matrix, offset):
		off_x, off_y  = offset
		for y, row in enumerate(matrix):
			for x, val in enumerate(row):
				pygame.draw.rect(self.screen, colors[val], pygame.Rect((off_x+x)*config['cell_size']+self.offsetScreen[0]*config['cell_size'],(off_y+y)*config['cell_size']+self.offsetScreen[1]*config['cell_size'], config['cell_size'], config['cell_size']),0)
		self.show_score(str(self.score))

	# move a piece horizontally
	def move(self, delta_x):
		if not self.gameover:
			new_x = self.stone_x + delta_x
			if new_x < 0:
				new_x = 0
			if new_x > config['cols'] - len(self.stone[0]):
				new_x = config['cols'] - len(self.stone[0])
			if not check_collision(self.board, self.stone, (new_x, self.stone_y)):
				self.stone_x = new_x


	# quit game
	def quit(self):
		self.center_msg("Exiting...")
		pygame.display.update()
		sys.exit()

	'''
	Try moving piece down
	- if collision:
	1. add stone to board
	2. create new piece
	3. Check for row completion
	'''
	def drop(self, instant=False):
		if not self.gameover:
			# If instant is true
			if instant:
				# Calculate the effective height as described in the report
				self.stone_y = 1 + TUtils.get_effective_height(self.board, self.stone, (self.stone_x, self.stone_y))
			else:
				# Otherwise drop block by 1 each frame
				self.stone_y += 1

			if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
				self.board = join_matrixes(self.board, self.stone, (self.stone_x, self.stone_y))
				self.new_stone()
				rowClear = 0
				for i, row in enumerate(self.board[:-1]):
					if 0 not in row:
						rowClear += 1
						self.board = remove_row(self.board, i)
				self.score += rowClear*20	# Updating score for every line cleared
 
	'''
	Rotate stone if no collision
	'''
	def rotate_stone(self):
		if not self.gameover:
			new_stone = rotate_clockwise(self.stone)
			if not check_collision(self.board, new_stone, (self.stone_x, self.stone_y)):
				self.stone = new_stone

	# start new game if gameover 
	def start_game(self):
		self.init_game()
		self.gameover = False
 
	'''
	Runs the game
	setup game mechanics
	'''
	def run(self, step):
		# Don't run if game is over
		if self.gameover:
			self.center_msg("Game Over!")
			return
		# If movement is left side
		if step == 1:
			self.move(-1)
		# If movement is right side
		elif step == 2:
			self.move(1)
		# If movement is rotation
		elif step == 3:
			self.rotate_stone()
		# If movement is instant drop
		elif step == 4:
			self.drop(True)
		# Dropping tile by 1 each frame
		self.drop()
		# Drawing the board
		self.draw_matrix(self.board, (0,0))
		# Drawing the tetris stone/block
		self.draw_matrix(self.stone, (self.stone_x, self.stone_y))
	

	def get_state(self):
		return {"board": numpy.copy(self.board), "stone": numpy.copy(self.stone), "stone_x": self.stone_x, "stone_y": self.stone_y, "score": self.score, "gameover": self.gameover, "needs_actions": self.needs_actions}

#if __name__ == '__main__':
 #  App = Tetris()
  # App.run()