# Importing required libraries
import pygame
from tetris import Tetris
import random
from tetrisAgents import GeneticAgent
from charles import selection, crossover, mutation


# Tetris population class
class PopulationTetris:
	def __init__(self, populationSize, mutationRate, maxGenerations):
		self.populationSize = populationSize	# No of game instances to run
		self.mutationRate = mutationRate	# Mutation rate to mutate each game genetics
		self.maxGenerations = maxGenerations	# Maximum generations the game should run
		self.tetrisPool = []	# Empty tetris pool for tetris games
		self.agentPool = []	# Empty agent pool for game decision
		self.SCREEN_WIDTH = 1000	# Screen width of the window
		self.SCREEN_HEIGHT = 700	# Screen height of the window
		self.generation = 1	# Variable for keeping track of generation
		self.bestInGen = 0	# Variable for keeping track of best individual in generation
		self.best = 0	# Variable for keeping track of best among all generations
		# Pygame intialization start
		pygame.init()
		pygame.key.set_repeat(250, 25)
		self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
		pygame.event.set_blocked(pygame.MOUSEMOTION)
		self.screen.fill((255, 255, 255))
		# Pygame intialization end

		# Generate initial population
		self.generateInitialPopulation()
	# Method for generating initial population
	def generateInitialPopulation(self):
		cntX = 0	# Tracking X coordinate
		cntY = 0	# Tracking Y coordinate
		# Loop to generate population
		for i in range(self.populationSize):
			self.tetrisPool.append(Tetris(self.screen, (cntX, cntY)))	# Adding tetris game to population
			self.agentPool.append(GeneticAgent())	# Adding tetris agent to population
			if (i+1)%10 == 0:
				cntX = -11	# Resetting X coordinate to build next line of games
				cntY += 25	# Updating Y coordinate when 10 games are created
			cntX += 11	# Updating X coordinate after initializing every game
	
	# Method for generating new population
	def generateNewPopulation(self):
		newAgentPool = []	# Initializing empty pool
		# Looping till new pool length reaches population size
		while(len(newAgentPool)<len(self.agentPool)):
			child1 = GeneticAgent()	# Creating first child
			child2 = GeneticAgent()	# Creating second child
			parent1 = self.agentPool[selection.fps(self.tetrisPool)]	# Choosing first parent out of population
			parent2 = self.agentPool[selection.fps(self.tetrisPool)]	# Choosing second parent out of population
			# Stacking genes
			parent1Gene = [parent1.weight_height, parent1.weight_holes, parent1.weight_bumpiness, parent1.weight_line_clear]
			parent2Gene = [parent2.weight_height, parent2.weight_holes, parent2.weight_bumpiness, parent2.weight_line_clear]
			
			# Generating childs from crossover
			gene1, gene2 = crossover.single_point_co(parent1Gene, parent2Gene)	# Comment/Uncomment out for running the corresponding method
			# gene1, gene2 = crossover.arithmetic_co(parent1Gene, parent2Gene)	# Comment/Uncomment out for running the corresponding method

			# Mutating child genes
			child1Gene = mutation.random_mutation(gene1, self.mutationRate)
			child2Gene = mutation.random_mutation(gene2, self.mutationRate)
			# Changing genes of created childrens
			child1.weight_height, child1.weight_holes, child1.weight_bumpiness, child1.weight_line_clear = child1Gene
			child2.weight_height, child2.weight_holes, child2.weight_bumpiness, child2.weight_line_clear = child2Gene
			newAgentPool.append(child1)	# Adding child to population
			newAgentPool.append(child2)	# Adding child to population
		self.agentPool = newAgentPool	# Changing old pool to new pool

	# Method for running game
	def update(self):
		global time_elapsed	# Getting global variable
		# Dealing inputs
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		time_elapsed += 1	# Incrementing time_elapsed on every call
		# Condition executed if state of all game in population is gameover or if time_elapsed reaches 1000
		if all(game.gameover for game in self.tetrisPool) or time_elapsed%1000==0:
			self.screen.fill((255, 255, 255))
			time_elapsed = 0	# Changing time_elapsed 
			self.bestInGen = 0	# Keeping track of best in each generation
			# Looping through the population for finding best
			for i in self.tetrisPool:
				# Changing best in generation if current score is maximum till now
				if(i.score>self.bestInGen):
					self.bestInGen = i.score
			# Changing the best in all the generations if current generation score is higher than till now
			if(self.bestInGen>self.best):
				self.best = self.bestInGen
			# Generating new population
			self.generateNewPopulation()
			# Updating generation count
			self.generation += 1
			# Resetting each game
			for tetris in self.tetrisPool:
				tetris.start_game()
		# Running each game with the help of inputs received from agents
		for index, game in enumerate(self.tetrisPool):
			# if not game.gameover:
			game.run(self.agentPool[index].get_action(game))
		pygame.display.update()	# Updating screen
		# Displaying message
		msg = f"Generation\n{self.generation}\n \nBest in Generation\n{self.bestInGen}\n \nBest till now\n{self.best}\n \nTime Limit\n{time_elapsed}/1000"
		# Drawing message on screen
		self.drawText(msg, 885)
		dont_burn_my_cpu.tick(30)

	# Method for drawing text on screen
	def drawText(self, msg, xCord):
		for i, line in enumerate(msg.splitlines()):
			msg_image =  pygame.font.Font(pygame.font.get_default_font(), 20).render(line, False, (0,0,0), (255,255,255))
			msgim_center_x, msgim_center_y = msg_image.get_size()
			msgim_center_x //= 2
			msgim_center_y //= 2
			position = (xCord - msgim_center_x,
						self.SCREEN_HEIGHT // 4 - msgim_center_y + i*25)
			self.screen.blit(msg_image, position)


populationSize = 40	# Population size
mutationRate = 0.1	# Mutation rate
maxGenerations = 50	# Maximum generations

# Creating population object
population = PopulationTetris(populationSize, mutationRate, maxGenerations)
pygame.time.set_timer(pygame.USEREVENT+1, 750)
dont_burn_my_cpu = pygame.time.Clock()
time_elapsed = 0
# Running game till max generations
while population.generation<population.maxGenerations:
	population.update()	# Calling update

# Loop for not closing the screen automatically
while True:
	population.screen.fill((255, 255, 255))	# Filling the screen
	# Handling inputs
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
	# Message to display
	msg = f"Completed\n \nGenerations\n{population.generation}\n \nBest Score\n{population.best}"
	# Drawing message on screen in center
	population.drawText(msg, 500)
	# Updating screen
	pygame.display.update()