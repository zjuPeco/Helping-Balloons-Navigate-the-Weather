# -*- coding:utf-8 -*-
__author__ = 'zjuPeco'


import networkx as nx
import numpy as np
from generateMap.UnionFind import UnionFind
import pickle


class Ant(object):
    def __init__(self, start_x, start_y, tar_x, tar_y, wind_matrix, rain_matrix, distance=0, wind_threshold=15.0, rain_threshold=4.0, limit_life=18*60):
        self.distance = distance  # 移动的总时长
        self.visited = [(start_x, start_y)]  # 已经走过的位置
        self.x = start_x  # 当前的xid
        self.y = start_y  # 当前的yid
        self.startX = start_x  # 起始的xid
        self.startY = start_y  # 起始的yid
        self.tarX = tar_x  # 目标的xid
        self.tarY = tar_y  # 目标的yid
        self.limit_life = limit_life # 蚂蚁最多能走的时间
        self.wind_matrix = wind_matrix # 地图，三维，小于wind_threshold表示安全，大于等于wind_threshold表示危险
        self.rain_matrix = rain_matrix # 地图，三维，小于rain_threshold表示安全，大于等于rain_threshold表示危险
        self.wind_threshold = wind_threshold # 风速危险界限
        self.rain_threshold = rain_threshold # 降雨量危险界限

    # 当前位置和目标位置在视野内有连通图
    def has_shortest_path(self):
        direction = self.get_direction()
        limit_x = abs(self.tarX - self.x)
        limit_y = abs(self.tarY - self.y)
        groups = []
        move_steps_1 = [(1, 0), (0, 1)]  # 右上
        move_steps_2 = [(-1, 0), (0, 1)]  # 左上
        move_steps_3 = [(-1, 0), (0, -1)]  # 左下
        move_steps_4 = [(1, 0), (0, -1)]  # 右下
        if 1 == direction:
            for i in range(limit_x + 1):
                for j in range(limit_y + 1):
                    wind = self.wind_matrix[self.x + i - 1][self.y + j - 1][(self.distance + 2 * (i + j)) // 60]
                    rain = self.rain_matrix[self.x + i - 1][self.y + j - 1][(self.distance + 2 * (i + j)) // 60]
                    if wind < self.wind_threshold and rain < self.rain_threshold:
                        group = []
                        group.append((self.x + i, self.y + j))
                        for move_step in move_steps_1:
                            if self.x + i + move_step[0] >= self.x and \
                               self.x + i + move_step[0] <= self.tarX and \
                               self.y + j + move_step[1] >= self.y and \
                               self.y + j + move_step[1] <= self.tarY:
                                if (self.distance + 2 * (i + j + abs(move_step[0]) + abs(move_step[1]))) < self.limit_life:
                                    wind = self.wind_matrix[self.x + i + move_step[0] - 1][self.y + j + move_step[1] - 1][(self.distance + 2 * (abs(i + move_step[0]) + abs(j + move_step[1]))) // 60]
                                    rain = self.rain_matrix[self.x + i + move_step[0] - 1][self.y + j + move_step[1] - 1][(self.distance + 2 * (abs(i + move_step[0]) + abs(j + move_step[1]))) // 60]
                                    if wind >= self.wind_threshold or rain >= self.rain_threshold:
                                        continue
                                    group.append((self.x + i + move_step[0], self.y + j + move_step[1]))
                        groups.append(group)
        if 2 == direction:
            for i in range(limit_x + 1):
                for j in range(limit_y + 1):
                    wind = self.wind_matrix[self.x - i - 1][self.y + j - 1][(self.distance + 2 * (i + j)) // 60]
                    rain = self.rain_matrix[self.x - i - 1][self.y + j - 1][(self.distance + 2 * (i + j)) // 60]
                    if wind < self.wind_threshold and rain < self.rain_threshold:
                        group = []
                        group.append((self.x - i, self.y + j))
                        for move_step in move_steps_2:
                            if self.x - i + move_step[0] <= self.x and \
                               self.x - i + move_step[0] >= self.tarX and \
                               self.y + j + move_step[1] >= self.y and \
                               self.y + j + move_step[1] <= self.tarY:
                                if (self.distance + 2 * (i + j + abs(move_step[0]) + abs(move_step[1]))) < self.limit_life:
                                    wind = self.wind_matrix[self.x - i + move_step[0] - 1][self.y + j + move_step[1] - 1] \
                                        [(self.distance + 2 * (
                                                abs(i- move_step[0]) + abs(j + move_step[1]))) // 60]
                                    rain = self.rain_matrix[self.x - i + move_step[0] - 1][self.y + j + move_step[1] - 1] \
                                        [(self.distance + 2 * (
                                            abs(i - move_step[0]) + abs(j + move_step[1]))) // 60]
                                    if wind >= self.wind_threshold or rain >= self.rain_threshold:
                                        continue
                                    group.append((self.x - i + move_step[0], self.y + j + move_step[1]))
                        groups.append(group)
        if 3 == direction:
            for i in range(limit_x + 1):
                for j in range(limit_y + 1):
                    wind = self.wind_matrix[self.x - i - 1][self.y - j - 1][(self.distance + 2 * (i + j)) // 60]
                    rain = self.rain_matrix[self.x - i - 1][self.y - j - 1][(self.distance + 2 * (i + j)) // 60]
                    if wind < self.wind_threshold and rain < self.rain_threshold:
                        group = []
                        group.append((self.x - i, self.y - j))
                        for move_step in move_steps_3:
                            if self.x - i + move_step[0] <= self.x and \
                               self.x - i + move_step[0] >= self.tarX and \
                               self.y - j + move_step[1] <= self.y and \
                               self.y - j + move_step[1] >= self.tarY:
                                if (self.distance + 2 * (i + j + abs(move_step[0]) + abs(move_step[1]))) < self.limit_life:
                                    wind = self.wind_matrix[self.x - i + move_step[0] - 1][self.y - j + move_step[1] - 1][(self.distance + 2 * (abs(i - move_step[0]) + abs(j - move_step[1]))) // 60]
                                    rain = self.rain_matrix[self.x - i + move_step[0] - 1][self.y - j + move_step[1] - 1][(self.distance + 2 * (abs(i - move_step[0]) + abs(j - move_step[1]))) // 60]
                                    if wind >= self.wind_threshold or rain >= self.rain_threshold:
                                        continue
                                    group.append((self.x - i + move_step[0], self.y - j + move_step[1]))
                        groups.append(group)
        if 4 == direction:
            for i in range(limit_x + 1):
                for j in range(limit_y + 1):
                    wind = self.wind_matrix[self.x + i - 1][self.y - j - 1][(self.distance + 2 * (i + j)) // 60]
                    rain = self.rain_matrix[self.x + i - 1][self.y - j - 1][(self.distance + 2 * (i + j)) // 60]
                    if wind < self.wind_threshold and rain < self.rain_threshold:
                        group = []
                        group.append((self.x + i, self.y - j))
                        for move_step in move_steps_4:
                            if self.x + i + move_step[0] >= self.x and \
                               self.x + i + move_step[0] <= self.tarX and \
                               self.y - j + move_step[1] <= self.y and \
                               self.y - j + move_step[1] >= self.tarY:
                                if (self.distance + 2 * (i + j + abs(move_step[0]) + abs(move_step[1]))) < self.limit_life:
                                    wind = self.wind_matrix[self.x + i + move_step[0] - 1][self.y - j + move_step[1] - 1][(self.distance + 2 * (abs(i + move_step[0]) + abs(j - move_step[1]))) // 60]
                                    rain = self.rain_matrix[self.x + i + move_step[0] - 1][self.y - j + move_step[1] - 1][(self.distance + 2 * (abs(i + move_step[0]) + abs(j - move_step[1]))) // 60]
                                    if wind >= self.wind_threshold or rain >= self.rain_threshold:
                                        continue
                                    group.append((self.x + i + move_step[0], self.y - j + move_step[1]))
                        groups.append(group)
        u = UnionFind(groups)
        items = list(u.get_items())
        d = {} # 节点对应的序号
        if u.is_connected((self.x, self.y), (self.tarX, self.tarY)):
            for i, item in enumerate(items):
                d[str(item)] = i
            g = nx.DiGraph()
            for group in groups:
                for i in range(1, len(group)):
                    wind = self.wind_matrix[group[i][0] - 1][group[i][1] - 1][(self.distance + 2 * (abs(group[i][0] - self.x) + abs(group[i][1] - self.y))) // 60]
                    rain = self.rain_matrix[group[i][0] - 1][group[i][1] - 1][(self.distance + 2 * (abs(group[i][0] - self.x) + abs(group[i][1] - self.y))) // 60]
                    wind = wind / self.wind_threshold
                    rain = rain / self.rain_threshold
                    g.add_weighted_edges_from([(d[str(group[0])], d[str(group[i])], max(wind, rain))])
            if nx.has_path(g, source=d[str((self.x, self.y))], target=d[str((self.tarX, self.tarY))]):
                shortest_path = nx.shortest_path(g, source=d[str((self.x, self.y))], target=d[str((self.tarX, self.tarY))], weight='weight')
                shortest_path_label = []
                for path in shortest_path:
                    shortest_path_label.append(items[path])
                return shortest_path_label
            else:
                return []
        else:
            return []

    # 获取移动方向，1为右上，2为左上，3为左下，4为右下
    def get_direction(self):
        delta_x = self.tarX - self.x
        delta_y = self.tarY - self.y
        if delta_x >= 0 and delta_y >= 0:
            return 1
        elif delta_x < 0 and delta_y > 0:
            return 2
        elif delta_x <= 0 and delta_y <= 0:
            return 3
        else:
            return 4
