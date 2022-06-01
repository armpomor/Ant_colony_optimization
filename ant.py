from random import randint
from config import *
from graph import Graph
from itertools import accumulate, pairwise


class Ant_colony:
    def __init__(self):
        self.visited_nodes = []          # Посещенные вершины
        self.graph_cls = Graph()
        self.graph = self.graph_cls.graph
        self.all_paths = []       # Список маршрутов с расстояниями
        # Список ребер графа (городов) с близостями (Q / длина маршрута)
        self.edge_proximity = []
        # Список средних расстояний пройденных маршрутов на каждой итерации
        self.distances = [] 

    def desire(self, node_1, node_2):
        """Вычисляем "желание" муравья перейти из node_1 в node_2"""
        return pow(1 / self.graph_cls.value(node_1, node_2), BETA) * pow(self.graph_cls.pheromone(node_1, node_2), ALPHA)

    def sum_desires(self, node):
        """Вычисляем сумму "желаний" для непосещенных узлов"""
        return sum([self.desire(node, i) for i in self.nodes_to_visit(node)])

    def nodes_to_visit(self, node):
        """Формируем множество узлов для посещения, удаляя посещенные узлы"""
        return [i for i in self.graph_cls.get_outgoing_edges(node) if i not in self.visited_nodes]

    def probability_route(self, node):
        """Вычисляем вероятности перехода из node во все доступные и непосещенные узлы
        и возвращаем список (узел, вероятность)"""
        return [(i, 100 * self.desire(node, i) / self.sum_desires(node)) for i in self.nodes_to_visit(node)]

    def next_node(self, node):
        """Крутим рулетку и получаем следующий узел для посещения из node"""
        # Список только значений вероятностей
        p = [i[1] for i in self.probability_route(node)]
        # Создаем диапазоны для рулетки
        p = accumulate(p, initial=0)
        d = [range(int(i[0]), int(i[1]) + 1) for i in pairwise(p)]
        # Крутим рулетку
        r = randint(0, 99)
        # и определяем индекс узла, в который пойдет муравей
        index = [r in i for i in d].index(True)
        return self.probability_route(node)[index][0]

    def start_ant(self, start_node):
        """Запускаем муравья. Возвращаем маршрут и пройденное расстояние"""
        path = []
        length_route = 0
        self.visited_nodes = []
        self.visited_nodes.append(start_node)
        prev_node = start_node
        for i in range(NUMBER_NODES - 1):
            move = self.next_node(prev_node)
            path.append((prev_node, move))
            length_route += self.graph_cls.value(prev_node, move)
            prev_node = move
            self.visited_nodes.append(move)
        path.append((prev_node, start_node))      # Добавляем последнее ребро
        length_route += self.graph_cls.value(prev_node, start_node)
        return path, length_route

    def all_ants_start(self):
        """Все муравьи стартуют и каждый из своего города. Возвращаем список 
        ребер с их близостями, т.е. Q / длина маршрута"""
        self.all_paths = []
        self.edge_proximity = []
        for i in self.graph_cls.nodes:
            self.all_paths.append(self.start_ant(i))
        # Преобразуем список маршрутов с расстояниями в список ребер с близостями
        for i in self.all_paths:
            for j in i[:-1]:
                for x in j:
                    self.edge_proximity.append((x, round(Q / i[-1], 3)))
        return self.edge_proximity

    def lessen_pheromone(self):
        """Уменьшаем значения феромона на всех ребрах, умножая на коэф. испарения"""
        for i in self.graph:
            for j in self.graph[i]:
                self.graph[i][j] = self.graph[i][j][0], P * \
                    self.graph_cls.pheromone(i, j)
        return self.graph

    def update_pheromone(self):
        """Обновляем значения феромона на всех ребрах. По сути эта функция представляет 
        собой одну итерацию, в которой все муравьи стартуют с разных городов один раз."""
        self.all_ants_start()
        self.lessen_pheromone()

        for i in self.edge_proximity:
            self.graph[i[0][0]][i[0][1]] = self.graph_cls.value(
                i[0][0], i[0][1]), self.graph_cls.pheromone(*i[0]) + i[1]
            # Делаем значения феромона в графе симметричными
            self.graph[i[0][1]][i[0][0]] = self.graph_cls.value(
                i[0][0], i[0][1]), self.graph_cls.pheromone(*i[0][::-1]) + i[1]
        return self.graph

    def run_iteration(self):
        for i in range(NUM_ITER):
            self.update_pheromone()
            self.distances.append(int(sum([i[1] for i in self.all_paths]) / NUMBER_NODES))
        return self.all_paths
    
    def favorite_route(self):
        """Список x и список y координат узлов маршрута и его длина, по которому 
        чаще всего пробегают муравьи за заданное количество итераций"""
        length = min([i[1] for i in self.all_paths])
        route = [i for i in self.all_paths if i[1] == length][0]
            
        list_nodes = []
        for i in route[0]:
            for j in i:
                if j not in list_nodes[1:]:
                    list_nodes.append(j)
                   
        x = [self.graph_cls.coord_node(i)[0] for i in list_nodes]
        y = [self.graph_cls.coord_node(i)[1] for i in list_nodes]
        return x, y, length

        

if __name__ == "__main__":
    a = Ant_colony()
    a.run_iteration()
    print(a.favorite_route())
