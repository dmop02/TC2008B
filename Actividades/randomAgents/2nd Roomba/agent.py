from mesa import Agent
import networkx as nx

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class TrashAgent(Agent):
    """
    Trash agent. Removed if it is in the same cell as random.
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class RandomAgent(Agent):
    def __init__(self, unique_id, model, initial_charging_station):
        super().__init__(unique_id, model)
        self.steps_taken = 0
        self.explored_cells = {initial_charging_station}
        self.know_empty_cells = {initial_charging_station}
        self.trash_cells = set()
        self.obstacle_cells = set()
        self.battery = 100
        self.initial_charging_station = initial_charging_station

    def move(self):
        x, y = self.pos
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=True
        )
        trash_neighbors, empty_neighbors, obstacle_neighbors = self.find_interest_neighbors(
            possible_steps
        )

        self.apppend_obstacle_cells(obstacle_neighbors)
        self.apppend_trash_cells(trash_neighbors)
        self.count_empty_cells(empty_neighbors)

        backtracked_grid = self.generate_backtrack_grid()
        unexplored_grid = self.generate_exploration_grid()

        path = nx.astar_path(backtracked_grid, (0, 0), (y - 1, x - 1))
        path_to_unexplored = nx.shortest_path(unexplored_grid, (y, x))

        if path_to_unexplored is None:
            self.model.running = False
            return
        next_move = path_to_unexplored[1]

        trash_agent = [
            agent
            for agent in self.model.grid.get_cell_list_contents([self.pos])
            if isinstance(agent, TrashAgent)
        ]

        if trash_agent:
            self.model.grid.remove_agent(trash_agent[0])
            self.trash_cells.remove(self.pos)
            next_move = self.pos
        elif self.trash_cells:
            trash_grid = self.generate_trash_grid(unexplored_grid)
            path_to_trash = nx.shortest_path(trash_grid, (y, x))
            next_move = path_to_trash[1]

        if self.battery < len(path) + 2 and self.pos != (1, 1):
            next_move = (path[-2][1] + 1, path[-2][0] + 1)

        if self.battery < 100 and self.pos == self.initial_charging_station:
            self.battery += 5
            next_move = self.initial_charging_station if self.battery > 100 else next_move
        else:
            self.battery -= 1

        self.steps_taken += 1
        self.model.grid.move_agent(self, next_move)
        if next_move not in self.explored_cells:
            self.explored_cells.add(next_move)

        total_trash_agents = sum(
            isinstance(agent, TrashAgent)
            for cell in self.model.grid.coord_iter()
            for agent in cell[0]
        )
        if total_trash_agents == 0:
            self.model.running = False

    def apppend_obstacle_cells(self, obstacle_neighbors):
        self.obstacle_cells.update(obstacle_neighbors)

    def apppend_trash_cells(self, trash_neighbors):
        self.trash_cells.update(trash_neighbors)

    def step(self):
        self.move()

    def generate_backtrack_grid(self):
        bounds = self.find_list_edges()
        known_grid = [
            [1 if (x, y) in self.know_empty_cells else 0 for x in range(bounds["min_x"], bounds["max_x"] + 1)]
            for y in range(bounds["min_y"], bounds["max_y"] + 1)
        ]
        return known_grid

    def generate_exploration_grid(self):
        bounds = self.find_list_edges()
        grid = [
            [1 if (x, y) in self.explored_cells else 0 for x in range(bounds["min_x"], bounds["max_x"] + 1)]
            for y in range(bounds["min_y"], bounds["max_y"] + 1)
        ]
        for cell in self.obstacle_cells:
            x, y = cell
            grid[y - bounds["min_y"]][x - bounds["min_x"]] = 2
        return grid

    def generate_trash_grid(self, exploration_grid):
        result_grid = [
            [2 if element == 0 else element for element in row] for row in exploration_grid
        ]
        for cell in self.trash_cells:
            x, y = cell
            result_grid[y - self.find_list_edges()["min_y"]][x - self.find_list_edges()["min_x"]] = 0
        return result_grid

    def find_interest_neighbors(self, possible_steps):
        trash_neighbors, empty_neighbors, obstacle_neighbors = [], [], []

        for cell in possible_steps:
            agents_in_cell = self.model.grid.get_cell_list_contents([cell])
            if not agents_in_cell:
                empty_neighbors.append(cell)
            for agent in agents_in_cell:
                if isinstance(agent, TrashAgent):
                    trash_neighbors.append(cell)
                    empty_neighbors.append(cell)
                elif isinstance(agent, ObstacleAgent):
                    obstacle_neighbors.append(cell)

        return trash_neighbors, empty_neighbors, obstacle_neighbors

    def count_empty_cells(self, empty_neighbors):
        self.know_empty_cells.update(empty_neighbors)

    def find_list_edges(self):
        min_x, max_x, min_y, max_y = float("inf"), float("-inf"), float("inf"), float("-inf")

        for cell in self.know_empty_cells.union(self.obstacle_cells):
            x, y = cell
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        return {"min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y}
