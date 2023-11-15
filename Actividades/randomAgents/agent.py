from mesa import Agent

class Trash(Agent):
    #Class for trash
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
class Battery(Agent):
    #Class for battery
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class RandomAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.steps_taken = 0

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=True) 
        self.battery -= 1
        # Checks which grid cells are empty
        freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

        next_moves = [p for p,f in zip(possible_steps, freeSpaces) if f == True]
       
        dirty = [position for position in possible_steps if any(isinstance(agent, Trash) for agent in self.model.grid.get_cell_list_contents([position]))]
        #self.batterylife=-1
        #if the cells are dirty, the agent will clean them
        if dirty:
            next_moves.extend(dirty)
        next_move = self.random.choice(next_moves)
        if self.random.random() < 0.5:
            self.model.grid.move_agent(self, next_move)
            self.steps_taken += 1
            agents = self.model.grid.get_cell_list_contents([next_move])
            for agent in agents:
                if isinstance(agent, Trash):
                    self.model.grid.remove_agent(agent)
                    self.model.schedule.remove(agent)
    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        # Randomly choose a direction
        self.direction = self.random.randrange(8)

        self.move()

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    #add obstacles to a grid
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    def step(self):
        pass
    #eliminate trash
    def step(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
    

class BatteryAgent(Agent):
    """
    Battery agent. Just to add obstacles to the grid.
    """
    #define battery
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.battery = 100
        self.charge = 0
        self.steps_taken = 0
    def charge(self):
        self.charge = self.battery
    def step(self):
        pass

    
