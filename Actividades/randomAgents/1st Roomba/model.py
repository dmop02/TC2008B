from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agent import RandomAgent, ObstacleAgent, TrashAgent, chargingStation
import networkx as nx
import random

class RandomModel(Model):
    def __init__(self, N, M, T, width, height):
        self.num_agents = N
        self.num_obstacles = M
        self.num_trash = T

        self.grid = MultiGrid(10, 10, torus=False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.current_id = 0
        self.datacollector = DataCollector(
            agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, RandomAgent) else 0},
            model_reporters={
                "Time needed for all cells to be clean": "time_to_clean",
                "Percentage of clean cells": "percentage_clean_cells",
                "Number of movements made by the agent": "total_agent_movements"
            }
        )
        self.G = nx.Graph()
        for contents, (x, y) in self.grid.coord_iter():
            if not contents:
                self.G.add_node((x, y))
            
            

        # Add trash to the grid
        for _ in range(T):
            trash = TrashAgent(self.next_id(), self)
            self.schedule.add(trash)


        
        # Create charging station 
        charge = chargingStation(self.next_id(), self)
        self.schedule.add(charge)
        self.grid.place_agent(charge, (1, 1))

        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
        #Create Obstacles
        for i in range(M):
            pos = pos_gen(self.grid.width, self.grid.height)

            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            
            obstacle = ObstacleAgent(self.next_id(), self)
            self.grid.place_agent(obstacle, pos)

        # Agent
        for _ in range(N):
            agent = RandomAgent(self.next_id(), self)
            self.schedule.add(agent)
            
            # Ensure that the agent starts at position {1, 1}
            x, y = (1, 1) if _ == 0 else self.random_empty_pos()
            self.grid.place_agent(agent, (x, y))

        # Randomly add obstacles to the grid without needing a position
        for _ in range(M):
            obstacle = ObstacleAgent(self.next_id(), self)
            self.schedule.add(obstacle)
            print(f"Obstacle agent {obstacle.unique_id} placed at ({x}, {y}).")
            
            self.grid.place_agent(obstacle, (x, y))

        self.datacollector.collect(self)
    
    def next_id(self):
        self.current_id += 1
        return self.current_id
    def time_to_clean(self, model):
        """
        Calculate the time needed for all cells to be clean.
        """
        return model.schedule.steps

    def percentage_clean_cells(self, model):
        """
        Calculate the percentage of clean cells.
        """
        total_cells = model.grid.width * model.grid.height
        clean_cells = sum(
            isinstance(agent, TrashAgent)
            for cell in model.grid.coord_iter()
            for agent in cell[0]
        )
        return (clean_cells / total_cells) * 100

    def total_agent_movements(self, model):
        """
        Calculate the total number of movements made by the agent.
        """
        return sum(agent.steps_taken for agent in model.schedule.agents if isinstance(agent, RandomAgent))
    

    def step(self):
        """
        Advance the model by one step.
        """
        self.stepnum += 1
        self.schedule.step()
        self.datacollector.collect(self)
