from mesa import Agent

class TreeCell(Agent):
    """
        A tree cell.
        
        Attributes:
            x, y: Grid coordinates
            condition: Can be "Fine", "On Fire", or "Burned Out"
            unique_id: (x,y) tuple.

            unique_id isn't strictly necessary here, but it's good practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """
        Create a new tree.

        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Unborn"
        self._next_condition = None

    def step(self):
        """
        This method is the step method for the agent.
        """
 
        position_status = {"upper_left": False,"upper_center": False,"upper_right": False}

        neighbors = self.model.grid.iter_neighbors(self.pos,True)
        for neighbor in neighbors:
            difx, dify =(self.pos[0] - neighbor.pos[0], self.pos[1] - neighbor.pos[1])
            print(difx)
            if difx == -1 and dify == -1 and neighbor.condition == "Unborn":
                position_status["upper_left"] = True
            elif difx == 0 and dify == -1 and neighbor.condition == "Unborn":
                position_status["upper_center"]= True
            elif difx == 1 and dify == -1 and neighbor.condition == "Unborn":
                position_status["upper_right"] = True
        if position_status["upper_left"] and position_status["upper_center"] and position_status["upper_right"]:
            self._next_condition = "Live"
        elif position_status["upper_left"] and position_status["upper_center"]:
            self._next_condition = "Unborn"
        elif position_status["upper_left"] and position_status["upper_right"]:
            self._next_condition = "Live"
        elif position_status["upper_center"] and position_status["upper_right"]:
            self._next_condition = "Unborn"
        elif position_status["upper_left"]:
            self._next_condition = "Unborn"
        elif position_status["upper_center"]:
            self._next_condition = "Live"
        elif position_status["upper_right"]:
            self._next_condition = "Unborn"
        elif not position_status["upper_left"] and not position_status["upper_center"] and not position_status["upper_right"] and self.pos[1] == 0:
            self._next_condition = "Live"
        
        
        
        
    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition