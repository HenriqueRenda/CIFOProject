# Importing required libraries
import random
from tetris import Tetris
import tetrisUtils as TUtils

# Tetris agent class
class GeneticAgent:
	def __init__(self):
		self.action_queue = []	# Empty queue for storing actions for corresponding game

		self.weight_height = random.uniform(0, 1)	# Height from board as described in report
		self.weight_holes = random.uniform(0, 1)	# No of holes as described in report
		self.weight_bumpiness = random.uniform(0, 1)	# Bumpiness of the board as described in report
		self.weight_line_clear = random.uniform(0, 1)	# Lines Cleared as described in report

	# Method for fetching action to perform in game
	def get_action(self, tetris):
		# If action queue is empty then run this
		if len(self.action_queue) == 0:
			# Calculate actions to be performed
			self.action_queue = self.calculate_actions(tetris.board, tetris.stone, (tetris.stone_x, tetris.stone_y))
		# Returning first element of the queue and removing it at the same time
		return self.action_queue.pop(0)

	# Method for getting fitness of the board
	def get_fitness(self, board):
		score = 0
		# Check if the board has any completed rows
		future_board, clear_count = TUtils.get_board_and_lines_cleared(board)
		# Calculate the line-clear score and apply weights
		score += self.weight_line_clear * clear_count
		# Calculate the aggregate height of future board and apply weights
		score += self.weight_height * sum(TUtils.get_col_heights(future_board))
		# Calculate the holes score and apply weights
		score += self.weight_holes * TUtils.get_hole_count(future_board)
		# Calculate the "smoothness" score and apply weights
		score += self.weight_bumpiness * TUtils.get_bumpiness(future_board)
		# Return the final score
		return score


	# Method for calculating actions
	def calculate_actions(self, board, current_tile, offsets):
		best_fitness = -9999	# Variable for keeping track of best fitness among all stone orientations
		best_rotation = -1	# Variable for keeping track of best rotation
		best_x = -1	# Variable for keeping track of best coordinate

		tile = current_tile	# Current tile
		# Looping through all the possible 4 stone rotations for best rotation
		for rotation_count in range(0, 4):
			# Looping through all the columns for best X cordinate
			for x in range(0, 10 - len(tile[0]) + 1):
				new_board = TUtils.get_future_board_with_tile(board, tile, (x, offsets[1]), True)	# Getting future board with stone placed with current configuration
				fitness = self.get_fitness(new_board)	# Calculating fitness of the board
				# If current fitness is greater among all possible orientations fitness change best fitness
				if fitness > best_fitness:
					best_fitness = fitness	# Changing best fitness
					best_rotation = rotation_count	# Changing best rotation
					best_x = x	# Changing best X
			tile = TUtils.get_rotated_tile(tile)	# Rotating tile for next rotation

		actions = []	# Empty list for keeping track of actions
		for _ in range(best_rotation):
			actions.append(3)	# Adding rotation action
		temp_x = offsets[0]
		# Adding horizontal movement action
		while temp_x != best_x:
			direction = 1 if temp_x < best_x else -1	# Direction -1 means Left, 1 means Right
			temp_x += direction	# Incrementing temp_x in moved direction
			actions.append(2 if direction == 1 else 1)	# 1 Indicates Left movement, 2 indicates Right movement
		actions.append(4)	# Adding Instant drop action
		return actions	# Returning action list