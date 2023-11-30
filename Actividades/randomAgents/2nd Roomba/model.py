from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agent import RandomAgent, ObstacleAgent, TrashAgent
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
            agent_reporters={
                "Steps": lambda a: a.steps_taken if isinstance(a, RandomAgent) else 0,
                "Cleaned Cells": lambda a: a.cleaned_cells if isinstance(a, RandomAgent) else 0
            },
            model_reporters={
                "Time needed for all cells to be clean": "time_to_clean",
                "Percentage of clean cells": "percentage_clean_cells",
                "Number of movements made by the agent": "total_agent_movements"
            }
        )


        # Add trash to the grid
        for _ in range(T):
            trash = TrashAgent(self.next_id(), self)
            self.schedule.add(trash)
            
            x, y = self.random_empty_pos()
            self.grid.place_agent(trash, (x, y))

        # Place obstacles on the grid
        for i in range(M):
            self.grid.place_agent(ObstacleAgent(i, self), (1, 1))
            self.schedule.add(ObstacleAgent(i, self))
        
        # Create charging station 
        self.charging_station = nx.astar_path(self.next_id(), self)
        self.grid.place_agent(self.charging_station, (0, 0))

        # Create the border of the grid
        border = [(x, y) for y in range(height) for x in range(width) if y in [0, height - 1] or x in [0, width - 1]]

        #Randomly place Agent
        for _ in range(100):
            agent = RandomAgent(self.next_id(), self)
            self.schedule.add(agent)
            
            x, y = self.random_empty_pos()
            self.grid.place_agent(agent, (x, y))
        # Randomly add obstacles to the grid without needing a position
        for _ in range(M):
            obstacle = ObstacleAgent(self.next_id(), self)
            self.schedule.add(obstacle)
            
            x, y = self.random_empty_pos()
            print(f"Obstacle agent {obstacle.unique_id} placed at ({x}, {y}).")
            
            self.grid.place_agent(obstacle, (x, y))

        self.datacollector.collect(self)
    def get_empty_positions(self):
        empty_positions = [(x, y) for x in range(self.grid.width) for y in range(self.grid.height) if self.grid.is_cell_empty((x, y))]
        
        return empty_positions
    def random_empty_pos(self):
        empty_positions = self.get_empty_positions()
        return random.choice(empty_positions)
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
