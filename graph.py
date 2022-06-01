from collections import defaultdict
from random import sample
from itertools import combinations
from math import dist
from string import ascii_letters
from config import *


class Graph:
    """Генерируем полный взвешенный граф с весами ребер и количеством феромона на ребрах."""

    def __init__(self):
        self.nodes = sample(ascii_letters, NUMBER_NODES)
        self.graph = self.construct_graph()

    def __repr__(self) -> str:
        return repr(self.graph)

    def coordinates_nodes(self):
        """Генерируем координаты узлов и возвращаем список узлов с их координатами"""
        coordinates = [sample(range(N), 2) for i in range(len(self.nodes))]
        self.nodes_coordinates = list(zip(self.nodes, coordinates))
        return self.nodes_coordinates

    def connect_nodes(self):
        """Генерируем связи между узлами и возвращаем список связанных узлов
        с их координатами. Все узлы в данном графе связаны между собой."""
        self.coordinates_nodes()
        return [list(i) for i in combinations(self.nodes_coordinates, 2)]

    def construct_list_nodes_costs(self):
        """Вычисляем длину ребер между узлами и возвращаем список связанных узлов и 
        вес ребер между ними"""
        return [[i[0][0]] + [i[1][0]] + [int(dist(i[0][1], i[1][1]))] for i in self.connect_nodes()]

    def add_pheromone(self):
        """В список связанных узлов с расстояниями добавляем количество феромона
        между этими узлами."""
        return [i + [PHEROMONE] for i in self.construct_list_nodes_costs()]

    def construct_graph(self):
        graph = defaultdict(dict)
        # i и j - это узлы, k - это вес ребра, p - феромон
        for i, j, k, p in self.add_pheromone():
            graph[i][j] = graph[j][i] = k, p
        return graph
    
    def coord_node(self, node):
        """Возвращаем координаты узла"""
        d = {i[0]: i[1] for i in self.nodes_coordinates}
        return d[node]

    def get_outgoing_edges(self, node):
        """Доступные узлы из текущего узла"""
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections

    def value(self, node1, node2):
        """Вес ребра между узлами (расстояние между узлами)"""
        return self.graph[node1][node2][0]

    def pheromone(self, node1, node2):
        """Количество феромона на ребре"""
        return self.graph[node1][node2][1]


if __name__ == '__main__':
    g = Graph()
    print(g)
  



