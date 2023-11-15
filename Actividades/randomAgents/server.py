from model import RandomModel, ObstacleAgent, Trash, RandomAgent
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    elif (isinstance(agent, RandomAgent)):
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.5
    elif (isinstance(agent, Trash)):
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 3
        portrayal["r"] = 0.5
    
    return portrayal

model_params = {"N":1, "M": 8, "T":6, "width":10, "height":10}

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps")

server = ModularServer(RandomModel, [grid, bar_chart], "Random Agents", model_params)
                       
server.port = 8521 # The default
server.launch()