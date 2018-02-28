# -*- coding:utf-8 -*-
__author__ = 'zjuPeco'

import numpy as np

class Queue(object):
    """
    队列
    """
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)

    def print_queue(self):
        for item in self.items:
            print (item)


class PathBuilder(object):
    def __init__(self, wind_matrix, rain_matrix, wind_threshold=15.0, rain_threshold=4.0):
        self.wind_matrix = wind_matrix
        self.rain_matrix = rain_matrix
        self.wind_threshold = wind_threshold
        self.rain_threshold = rain_threshold
        self.x_limit, self.y_limit, self.t_limit = self.wind_matrix.shape

    def in_range(self, xid, yid):
        return (xid >= 1) & (xid <= self.x_limit) & (yid >= 1) & (yid <= self.y_limit)

    @staticmethod
    def get_direction(start_x, start_y, tmp_x, tmp_y):
        """
        0 - 自身
        1 - 正右， 2 - 正上， 3 - 正左， 4 - 正下
        5 - 右上， 6 - 左上， 7 - 左下， 8 - 右下
        """
        if start_x == tmp_x and start_y == tmp_y:
            return 0
        if start_x < tmp_x and start_y == tmp_y:
            return 1
        if start_x  == tmp_x and start_y < tmp_y:
            return 2
        if start_x > tmp_x and start_y == tmp_y:
            return 3
        if start_x == tmp_x and start_y > tmp_y:
            return 4
        if start_x < tmp_x and start_y < tmp_y:
            return 5
        if start_x > tmp_x and start_y < tmp_y:
            return 6
        if start_x > tmp_x and start_y > tmp_y:
            return 7
        if start_x < tmp_x and start_y > tmp_y:
            return 8

    @staticmethod
    def get_distance(start_x, start_y, tar_x, tar_y):
        return 2 * (abs(start_x - tar_x) + abs(start_y - tar_y))

    def bfs(self, xid, yid, pre_distance):
        q = Queue()
        start_x = xid
        start_y = yid
        res = np.ones([self.x_limit, self.y_limit]) * 3
        wind = self.wind_matrix[xid - 1][yid - 1][pre_distance // 60]
        rain = self.rain_matrix[xid - 1][yid - 1][pre_distance // 60]
        if wind < self.wind_threshold and rain < self.rain_threshold:
            q.enqueue((xid, yid))
            wind_coef = wind / self.wind_threshold
            rain_coef = rain / self.rain_threshold
            res[xid - 1][yid - 1] = max(wind_coef, rain_coef)
        while not q.is_empty():
            tmp_x, tmp_y = q.dequeue()
            direction = self.get_direction(start_x, start_y, tmp_x, tmp_y)
            choice_list = []
            if direction == 0:
                choice_list.append((tmp_x + 1, tmp_y))
                choice_list.append((tmp_x, tmp_y + 1))
                choice_list.append((tmp_x - 1, tmp_y))
                choice_list.append((tmp_x, tmp_y - 1))
            elif direction == 1:
                choice_list.append((tmp_x + 1, tmp_y))
                choice_list.append((tmp_x, tmp_y + 1))
                choice_list.append((tmp_x, tmp_y - 1))
            elif direction == 2:
                choice_list.append((tmp_x + 1, tmp_y))
                choice_list.append((tmp_x, tmp_y + 1))
                choice_list.append((tmp_x - 1, tmp_y))
            elif direction == 3:
                choice_list.append((tmp_x, tmp_y + 1))
                choice_list.append((tmp_x - 1, tmp_y))
                choice_list.append((tmp_x, tmp_y - 1))
            elif direction == 4:
                choice_list.append((tmp_x + 1, tmp_y))
                choice_list.append((tmp_x - 1, tmp_y))
                choice_list.append((tmp_x, tmp_y - 1))
            elif direction == 5:
                choice_list.append((tmp_x + 1, tmp_y))
                choice_list.append((tmp_x, tmp_y + 1))
            elif direction == 6:
                choice_list.append((tmp_x, tmp_y + 1))
                choice_list.append((tmp_x - 1, tmp_y))
            elif direction == 7:
                choice_list.append((tmp_x - 1, tmp_y))
                choice_list.append((tmp_x, tmp_y - 1))
            elif direction == 8:
                choice_list.append((tmp_x, tmp_y - 1))
                choice_list.append((tmp_x + 1, tmp_y))

            for choice in choice_list:
                if self.in_range(choice[0], choice[1]):
                    dis = pre_distance + self.get_distance(start_x, start_y, choice[0], choice[1])
                    if dis // 60 >= self.t_limit:
                        continue
                    wind = self.wind_matrix[choice[0] - 1][choice[1] - 1][dis // 60]
                    rain = self.rain_matrix[choice[0] - 1][choice[1] - 1][dis // 60]
                    if wind < self.wind_threshold and rain < self.rain_threshold and res[choice[0] - 1][choice[1] - 1] == 3:
                        wind_coef = wind / self.wind_threshold
                        rain_coef = rain / self.rain_threshold
                        res[choice[0] - 1][choice[1] - 1] = max(wind_coef, rain_coef)
                        q.enqueue(choice)
        return res

    def bfs2(self, xid, yid, reach_time):
        q = Queue()
        tar_x = xid
        tar_y = yid
        res = np.ones([self.x_limit, self.y_limit]) * 3
        wind = self.wind_matrix[xid - 1][yid - 1][reach_time // 60]
        rain = self.rain_matrix[xid - 1][yid - 1][reach_time // 60]
        if wind < self.wind_threshold and rain < self.rain_threshold:
            q.enqueue((xid, yid))
            wind_coef = wind / self.wind_threshold
            rain_coef = rain / self.rain_threshold
            res[xid - 1][yid - 1] = max(wind_coef, rain_coef)
        while not q.is_empty():
            tmp_x, tmp_y = q.dequeue()
            direction = self.get_direction(tmp_x, tmp_y, tar_x, tar_y)
            choice_list = []
            if direction == 0:
                choice_list.append((tmp_x + 1, tmp_y))
                choice_list.append((tmp_x, tmp_y + 1))
                choice_list.append((tmp_x - 1, tmp_y))
                choice_list.append((tmp_x, tmp_y - 1))
            elif direction == 1:
                choice_list.append((tmp_x - 1, tmp_y))
                choice_list.append((tmp_x, tmp_y + 1))
                choice_list.append((tmp_x, tmp_y - 1))
            elif direction == 2:
                choice_list.append((tmp_x + 1, tmp_y))
                choice_list.append((tmp_x, tmp_y - 1))
                choice_list.append((tmp_x - 1, tmp_y))
            elif direction == 3:
                choice_list.append((tmp_x, tmp_y + 1))
                choice_list.append((tmp_x + 1, tmp_y))
                choice_list.append((tmp_x, tmp_y - 1))
            elif direction == 4:
                choice_list.append((tmp_x + 1, tmp_y))
                choice_list.append((tmp_x - 1, tmp_y))
                choice_list.append((tmp_x, tmp_y + 1))
            elif direction == 5:
                choice_list.append((tmp_x - 1, tmp_y))
                choice_list.append((tmp_x, tmp_y - 1))
            elif direction == 6:
                choice_list.append((tmp_x, tmp_y - 1))
                choice_list.append((tmp_x + 1, tmp_y))
            elif direction == 7:
                choice_list.append((tmp_x + 1, tmp_y))
                choice_list.append((tmp_x, tmp_y + 1))
            elif direction == 8:
                choice_list.append((tmp_x, tmp_y + 1))
                choice_list.append((tmp_x - 1, tmp_y))

            for choice in choice_list:
                if self.in_range(choice[0], choice[1]):
                    dis = reach_time - self.get_distance(choice[0], choice[1], tar_x, tar_y)
                    if dis // 60 < 0:
                        continue
                    wind = self.wind_matrix[choice[0] - 1][choice[1] - 1][dis // 60]
                    rain = self.rain_matrix[choice[0] - 1][choice[1] - 1][dis // 60]
                    if wind < self.wind_threshold and rain < self.rain_threshold and res[choice[0] - 1][choice[1] - 1] == 3:
                        wind_coef = wind / self.wind_threshold
                        rain_coef = rain / self.rain_threshold
                        res[choice[0] - 1][choice[1] - 1] = max(wind_coef, rain_coef)
                        q.enqueue(choice)
        return res

    def get_map(self, xid, yid, pre_distance=0):
        if not self.in_range(xid, yid):
            print ('xid or yid is over limit')
            return None
        return self.bfs(xid, yid, pre_distance)

    def get_reversed_map(self, xid, yid, reach_time):
        if not self.in_range(xid, yid):
            print ('xid or yid is over limit')
            return None
        return self.bfs2(xid, yid, reach_time)