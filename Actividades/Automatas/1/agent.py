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
        self.condition = "Live"
        self._next_condition = None

    def step(self):
        """
        This method is the step method for the agent.
        """
 
        upperR = None
        upper = None
        upperL = None

        neighbors = self.model.grid.iter_neighbors(self.pos,True)
        for neighbor in neighbors:
            if neighbor.pos[0] == self.pos[0] - 1 and neighbor.pos[1] == (self.pos[1] + 1)%50:
                upperR = neighbor
                
            elif neighbor.pos[0] == self.pos[0] and neighbor.pos[1] == (self.pos[1] + 1)%50:
                upper = neighbor
            elif neighbor.pos[0] == self.pos[0] + 1 and neighbor.pos[1] == (self.pos[1] + 1)%50:
                upperL = neighbor
        
        if upperR is not None and upper is not None and upperL is not None:
        
            state = '-'.join([neighbor.condition for neighbor in [upperR, upper, upperL]])


            lookup = {
                "Unborn-Unborn-Unborn": "Unborn",
                "Unborn-Unborn-Live": "Live",
                "Unborn-Live-Unborn": "Unborn",
                "Unborn-Live-Live": "Live",
                "Live-Unborn-Unborn": "Live",
                "Live-Unborn-Live": "Unborn",
                "Live-Live-Unborn": "Live",
                "Live-Live-Live": "Unborn"
            }

            self._next_condition = lookup[state]
        
        
    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition