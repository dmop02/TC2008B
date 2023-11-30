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
        if self.condition == "Unborn" and self.pos[1] < 49 and 0 < self.pos[0] < 49:
            n = [] #Neighbor List 
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if neighbor.pos[1] == self.pos[1] + 1: # Top Neighbors
                    n.append(neighbor)
            if len(n) >= 3:
                if ((n[0].condition == "Unborn") and (n[1].condition == "Unborn") and (n[2].condition == "Live")or
                    (n[0].condition == "Unborn") and (n[1].condition == "Live") and (n[2].condition == "Live")or
                    (n[0].condition == "Live") and (n[1].condition == "Unborn") and (n[2].condition == "Unborn")or
                    (n[0].condition == "Live") and (n[1].condition == "Live") and (n[2].condition == "Unborn")):
                    self._next_condition = "Live"
        if self.condition == "Live":
            n = [] #Neighbor List
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                if (self.pos[1] == 49 and neighbor.pos[1] == 0) or self.pos[1] + 1 == neighbor.pos[1]: # Se almacenan únicamente los vecinos de arriba
                    n.append(neighbor)
            if len(n) >= 3:
                if ((n[0].condition == "Unborn") and (n[1].condition == "Unborn") and (n[2].condition == "Unborn")or
                    (n[0].condition == "Unborn") and (n[1].condition == "Live") and (n[2].condition == "Unborn")or
                    (n[0].condition == "Live") and (n[1].condition == "Unborn") and (n[2].condition == "Live")or
                    (n[0].condition == "Live") and (n[1].condition == "Live") and (n[2].condition == "Live")):
                    self._next_condition = "Unborn"
        
        
        
    def advance(self):
        """
        Advance the model by one step.
        """
        if self._next_condition is not None:
            self.condition = self._next_condition