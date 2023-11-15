from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import DataCollector
from agent import RandomAgent, ObstacleAgent, Trash
import random

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def randompos(width, height):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        return x, y
    def __init__(self, N,M,T, width, height):
        self.num_agents = N
        self.num_agents = M
        self.num_agents = T
        # Multigrid is a special type of grid where each cell can contain multiple agents.
        self.grid = MultiGrid(width,height,torus = False) 

        # RandomActivation is a scheduler that activates each agent once per step, in random order.
        self.schedule = RandomActivation(self)
        
        self.running = True 

        self.datacollector = DataCollector( 
        agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, RandomAgent) else 0})

        # Creates the border of the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        # Add obstacles to the grid
        for i in range(len(border)):
            self.grid.place_agent(ObstacleAgent(i, self), border[i])
            self.schedule.add(ObstacleAgent(i, self))


        #Function to create trash in the grid
        trash_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
        #Randomly add trash to the grid without needing a postion
        for i in range(10):
            self.grid.place_agent(ObstacleAgent(i+100, self), trash_gen(width,height))
            self.schedule.add(ObstacleAgent(i+100, self))
            # pos = randompos(self.grid.width, self.grid.height)
            
        

        

        

        # Function to generate random positions
        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))

        
        self.datacollector.collect(self)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
        self.datacollector.collect(self)