# -*- coding:utf-8 -*-
__author__ = 'zjuPeco'


import numpy as np
import pickle
import pandas as pd
import time


class Queue(object):
    """
    queue
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
        self.visited = []

    def in_range(self, xid, yid):
        return (xid >= 1) & (xid <= self.x_limit) & (yid >= 1) & (yid <= self.y_limit)

    @staticmethod
    def get_direction(start_x, start_y, tmp_x, tmp_y):
        """
        0 - Self
        1 - Right， 2 - Top， 3 - Left， 4 - Down
        5 - Top right， 6 - Top Left， 7 - Bottom Left， 8 - Bottom Right
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

    def bfs(self, xid, yid, start_time):
        q = Queue()
        start_x = xid
        start_y = yid
        res = np.ones([self.x_limit, self.y_limit]) * 3
        points = []
        wind = self.wind_matrix[xid - 1][yid - 1][start_time // 60]
        rain = self.rain_matrix[xid - 1][yid - 1][start_time // 60]
        if wind < self.wind_threshold and rain < self.rain_threshold:
            q.enqueue((xid, yid))
            wind_coef = wind / self.wind_threshold
            rain_coef = rain / self.rain_threshold
            res[xid - 1][yid - 1] = max(wind_coef, rain_coef)
        while not q.is_empty():
            tmp_x, tmp_y = q.dequeue()
            points.append((tmp_x, tmp_y))
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
                    dis = start_time + self.get_distance(start_x, start_y, choice[0], choice[1])
                    if dis // 60 >= self.t_limit:
                        continue
                    wind = self.wind_matrix[choice[0] - 1][choice[1] - 1][dis // 60]
                    rain = self.rain_matrix[choice[0] - 1][choice[1] - 1][dis // 60]
                    if wind < self.wind_threshold and rain < self.rain_threshold and res[choice[0] - 1][choice[1] - 1] == 3:
                        wind_coef = wind / self.wind_threshold
                        rain_coef = rain / self.rain_threshold
                        res[choice[0] - 1][choice[1] - 1] = max(wind_coef, rain_coef)
                        q.enqueue(choice)
        return res, points

    def bfs2(self, xid, yid, reach_time):
        q = Queue()
        tar_x = xid
        tar_y = yid
        res = np.ones([self.x_limit, self.y_limit]) * 3
        points = []
        wind = self.wind_matrix[xid - 1][yid - 1][reach_time // 60]
        rain = self.rain_matrix[xid - 1][yid - 1][reach_time // 60]
        if wind < self.wind_threshold and rain < self.rain_threshold:
            q.enqueue((xid, yid))
            wind_coef = wind / self.wind_threshold
            rain_coef = rain / self.rain_threshold
            res[xid - 1][yid - 1] = max(wind_coef, rain_coef)

        while not q.is_empty():
            tmp_x, tmp_y = q.dequeue()
            points.append((tmp_x, tmp_y))
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
        return res, points

    def get_points(self, start_x, start_y, tar_x, tar_y, point_num, start_time, reach_time, limit_nums, min_num, eta):
        if start_time >= 18 * 60:
            return False
        score_map, points = self.bfs(start_x, start_y, start_time)
        if point_num == 0:
            if (tar_x, tar_y) in points:
                dis = self.get_distance(start_x, start_y, tar_x, tar_y)
                self.visited.append((tar_x, tar_y, score_map[tar_x - 1][tar_y - 1], start_time, dis + start_time))
                return True
            else:
                return False

        while points and limit_nums:
            idx = np.random.randint(len(points))
            tmp_x, tmp_y = points[idx]
            points.pop(idx)
            direction = self.get_direction(start_x, start_y, tar_x, tar_y)
            direction2 = self.get_direction(tmp_x, tmp_y, tar_x, tar_y)
            if direction == direction2:
                continue
            else:
                dis = self.get_distance(start_x, start_y, tmp_x, tmp_y)
                dis2 = self.get_distance(tar_x, tar_y, tmp_x, tmp_y)
                if dis + dis2 + start_time > reach_time:
                    continue
                self.visited.append((tmp_x, tmp_y, score_map[tmp_x - 1][tmp_y - 1], start_time, dis + start_time))
                if self.get_points(tmp_x, tmp_y, tar_x, tar_y, point_num - 1, start_time + dis, reach_time, max(limit_nums*eta, min_num), min_num, eta):
                    return True
                else:
                    self.visited.pop(-1)
            limit_nums -= 1

        return False

    def get_points2(self, start_x, start_y, tar_x, tar_y, point_num, start_time, reach_time, limit_nums, min_num, eta):
        if reach_time < 0:
            return False
        score_map, points = self.bfs2(tar_x, tar_y, reach_time)
        if point_num == 0:
            if (start_x, start_y) in points:
                dis = self.get_distance(start_x, start_y, tar_x, tar_y)
                self.visited.append((tar_x, tar_y, score_map[tar_x - 1][tar_y - 1], reach_time, reach_time - dis))
                return True
            else:
                return False

        while points and limit_nums:
            idx = np.random.randint(len(points))
            tmp_x, tmp_y = points[idx]
            points.pop(idx)
            direction = self.get_direction(tar_x, tar_y, start_x, start_y)
            direction2 = self.get_direction(tar_x, tar_y, tmp_x, tmp_y)
            if direction == direction2:
                continue
            else:
                dis = self.get_distance(tar_x, tar_y, tmp_x, tmp_y)
                dis2 = self.get_distance(start_x, start_y, tmp_x, tmp_y)
                if start_time + dis + dis2 > reach_time:
                    continue
                self.visited.append((tmp_x, tmp_y, score_map[tmp_x - 1][tmp_y - 1], reach_time, reach_time - dis))
                if self.get_points2(start_x, start_y, tmp_x, tmp_y, point_num - 1, start_time, reach_time - dis, max(limit_nums*eta, min_num), min_num, eta):
                    return True
                else:
                    self.visited.pop(-1)
            limit_nums -= 1

        return False

    def forward_points(self, start_x, start_y, tar_x, tar_y, point_num, start_time=0, reach_time=1080, limit_nums=50, min_num=5, eta=0.5):
        if self.get_points(start_x, start_y, tar_x, tar_y, point_num, start_time, reach_time, limit_nums, min_num, eta):
            print ('points found!')
            return self.visited
        else:
            print ('failed to find points')
            return None

    def backward_points(self, start_x, start_y, tar_x, tar_y, point_num, start_time, reach_time, limit_nums=50, min_num=5, eta=0.5):
        if self.get_points2(start_x, start_y, tar_x, tar_y, point_num, start_time, reach_time, limit_nums, min_num, eta):
            print ('points found!')
            return self.visited
        else:
            print ('failed to find points')
            return None


def main():

    day = 6
    path_id = 1
    Forward = False

    t1 = time.time()
    with open('../dataset/day' + str(day) + '/wind_matrix_lgb.pickle', 'rb') as f:
        wind_matrix = pickle.load(f)
    with open('../dataset/day' + str(day) + '/rain_matrix_lgb.pickle', 'rb') as f:
        rain_matrix = pickle.load(f)
    path_builder = PathBuilder(wind_matrix, rain_matrix, wind_threshold=15.0, rain_threshold=4.0)
    city_data = pd.read_csv('../dataset/CityData.csv')
    if Forward:
        points = path_builder.forward_points(city_data['xid'][0], city_data['yid'][0], city_data['xid'][path_id],
                                             city_data['yid'][path_id], point_num=1, start_time=0, 
                                             reach_time=400, limit_nums=50)
    else:
        points = path_builder.backward_points(city_data['xid'][0], city_data['yid'][0], city_data['xid'][path_id],
                                              city_data['yid'][path_id], point_num=1, start_time=700, 
                                              reach_time=1062, limit_nums=50)
    if points:
        print (points)
    t2 = time.time()
    print ('cost {0}s'.format(t2 - t1))

if __name__ == '__main__':
    main()