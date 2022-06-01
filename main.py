import plotly.graph_objs as go
from ant import Ant_colony
from itertools import pairwise
from config import *


def f1(ants):
    """Строим график зависимости средней длины маршрута на итерации от номера итерации."""
    ants.run_iteration()
    x = ants.distances

    fig = go.Figure()
    fig.update_layout(title=dict(text='Ant colony optimization',
                      font=dict(size=20)), margin=dict(l=0, t=30, b=0, r=0))

    fig.add_trace(go.Scatter(y=x, mode='lines+markers',
                  marker=dict(size=10, color='red'), line=dict(width=5, color='gray')))

    fig.update_xaxes(title='Номер итерации')
    fig.update_yaxes(title='Средняя длина маршрута на итерации')
    
    fig.show()


def f2(ants):
    """Наиболее популярный маршрут за заданное количество итераций."""
    route = ants.favorite_route()

    # Вычисляем координаты ребер маршрута
    x1 = route[0]
    y1 = route[1]
    couple_x = pairwise(x1)
    couple_y = pairwise(y1)
    edges = zip(couple_x, couple_y)

    fig = go.Figure()
    fig.update_layout(title=dict(text=f'Длина наиболее популярного маршрута {route[2]} за {NUM_ITER} итераций.',
                                  font=dict(size=20)), margin=dict(l=0, t=30, b=0, r=0))

    fig.add_trace(go.Scatter(x=x1, y=y1, mode='markers', marker=dict(size=20, color='black', symbol="circle"),
                              name='City', text=[(route[0].index(i) + 1) for i in route[0]], hoverinfo='text',
                              textposition='bottom right'))

    routes = [go.Scatter(x=i[0], y=i[1], mode='lines', line=dict(width=5)) for i in edges]
    for i in routes:
        fig.add_trace(i)

    fig.show()


if NUMBER_NODES > 52:
    print("Set fewer graph nodes!")
else:
    ants = Ant_colony()
    f1(ants)
    f2(ants)
