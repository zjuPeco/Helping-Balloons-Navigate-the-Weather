from django.shortcuts import render
from django.views import View

from tools.utils import PathBuilder
import pickle
import time
import pandas as pd
from generateMap.Aco import Ant
import json
from bs4 import BeautifulSoup as Soup
# Create your views here.

class ChangeMap(View):
    start_time = 0

    def get(self, request):
        # 0:不撤回 1：撤回
        day = request.GET.get("day", "6")
        isCancel = request.GET.get("isCancel", "0")
        pre_distance = int(request.GET.get("pre_distance", 0))
        wind_threshold = float(request.GET.get("wind_threshold", 15.0))
        rain_threshold = float(request.GET.get("rain_threshold", 4.0))
        self.start_time = int(request.GET.get("start_time", self.start_time))

        tar = int(request.GET.get("path_id", 1))
        # 是否自动生成路径
        ifAutoGenerate = int(request.GET.get("ifAutoGenerate", 0))
        if ifAutoGenerate == 1:
            with open('data/day' + str(day) + '/wind_matrix.pickle', 'rb') as f:
                wind_matrix = pickle.load(f, encoding='latin1')
            with open('data/day' + str(day) + '/rain_matrix.pickle', 'rb') as f:
                rain_matrix = pickle.load(f, encoding='latin1')
            isSuccess = ChangeMap.auto_path_generated(wind_matrix, rain_matrix, day, tar, wind_threshold, rain_threshold,
                                                      self.start_time)
            return render(request, "success.html", {"isSuccess": isSuccess})
        isCancel = int(isCancel)
        if isCancel == 1:
            with open('data/history_path/path_x.pickle', 'rb') as f:
                path_x = pickle.load(f)
            with open('data/history_path/path_y.pickle', 'rb') as f:
                path_y = pickle.load(f)
            path_x.pop(-1)
            path_y.pop(-1)
            with open('data/history_path/path_x.pickle', 'wb') as f:
                pickle.dump(path_x, f)
            with open('data/history_path/path_y.pickle', 'wb') as f:
                pickle.dump(path_y, f)
            pre_distance = 0
            pre_distance += self.start_time
            for i in range(len(path_x) - 1):
                pre_distance += self.calcu_pre_dist(path_x[i], path_y[i], path_x[i+1], path_y[i+1])
            ChangeMap.build_map(path_x[-1], path_y[-1], max(0, int(pre_distance)), day, wind_threshold, rain_threshold)
            with open('data/day'+str(day)+'path8_wind_map.pickle', 'rb') as f:
                wind_map = pickle.load(f, encoding='latin1')
            wind_map = wind_map.transpose().tolist()
            print(wind_map)
            if pre_distance == 0:
                pre_distance = -1
            return render(request, "map.html", {"wind_map": json.dumps(wind_map), "scatter_x": json.dumps(path_x),
                                                "scatter_y": json.dumps(path_y), "pre_distance": pre_distance,
                                                "day_date": day, "wind_threshold": wind_threshold,
                                                "rain_threshold": rain_threshold, "start_time": self.start_time})

        x = request.GET.get("x", "142")
        y = request.GET.get("y", "328")
        x = int(x)
        y = int(y)

        try:
            pre_distance = int(pre_distance)
        except:
            pre_distance = 0

        # 正常情况，无停留
        if pre_distance == 0 & self.start_time == 0:
            # 第一次传pre_distance，为防止其一直为0，令其=-1
            path_x = [142]
            path_y = [328]
            pre_distance = -1
        # 停留start_time
        elif pre_distance < self.start_time & self.start_time > 0:
            path_x = [142]
            path_y = [328]
            pre_distance = self.start_time
        else:
            with open('data/history_path/path_x.pickle', 'rb') as f:
                path_x = pickle.load(f)
            path_x.append(x)
            with open('data/history_path/path_y.pickle', 'rb') as f:
                path_y = pickle.load(f)
            path_y.append(y)
            # 第一次点击某个坐标点
            if pre_distance == -1:
                pre_distance = 0
            pre_distance += self.calcu_pre_dist(path_x[-2], path_y[-2], path_x[-1], path_y[-1])


        with open('data/history_path/path_x.pickle', 'wb') as f:
            pickle.dump(path_x, f)
        with open('data/history_path/path_y.pickle', 'wb') as f:
            pickle.dump(path_y, f)

        ChangeMap.build_map(path_x[-1], path_y[-1], max(0, pre_distance), day, wind_threshold, rain_threshold)
        with open('data/day' + str(day) + 'path8_wind_map.pickle', 'rb') as f:
            wind_map = pickle.load(f, encoding='latin1')
        wind_map = wind_map.transpose().tolist()
        print(wind_map)
        return render(request, "map.html", {"wind_map": json.dumps(wind_map), "scatter_x": json.dumps(path_x),
                                            "scatter_y": json.dumps(path_y), "pre_distance": pre_distance,
                                            "day_date": day, "wind_threshold": wind_threshold,
                                                "rain_threshold": rain_threshold, "start_time": self.start_time})

    @staticmethod
    def calcu_pre_dist(x_pre, y_pre, x_cur, y_cur):
        return 2 * (abs(x_pre - x_cur) + abs(y_pre - y_cur))

    @staticmethod
    def build_map(x, y, pre_distance, day, wind_threshold, rain_threshold):
        path_id = 8
        reverse_map = False

        t1 = time.time()
        with open('data/day' + str(day) + '/wind_matrix.pickle', 'rb') as f:
            wind_matrix = pickle.load(f, encoding='latin1')
        with open('data/day' + str(day) + '/rain_matrix.pickle', 'rb') as f:
            rain_matrix = pickle.load(f, encoding='latin1')
        path_builder = PathBuilder(wind_matrix, rain_matrix, wind_threshold, rain_threshold)
        if reverse_map:
            # wind_map = path_builder.get_reversed_map(city_data['xid'][path_id], city_data['yid'][path_id], 1018)
            wind_map = path_builder.get_reversed_map(x, y, pre_distance)
            with open('data/day' + str(day) + 'path' + str(path_id) + '_reversed_wind_map.pickle', 'wb') as f:
                pickle.dump(wind_map, f, protocol=2)
        else:
            # wind_map = path_builder.get_map(city_data['xid'][0], city_data['yid'][0], 0)
            wind_map = path_builder.get_map(x, y, pre_distance)
            with open('data/day' + str(day) + 'path' + str(path_id) + '_wind_map.pickle', 'wb') as f:
                pickle.dump(wind_map, f, protocol=2)
        t2 = time.time()
        print('cost {0}s'.format(t2 - t1))

    @staticmethod
    def get_path(points, stay_time, wind_matrix, rain_matrix, wind_threshold, rain_threshold):
        if (len(points) != len(stay_time)):
            raise Exception("the length of points and stay_time must be equal")

        if (len(points) < 2):
            raise Exception("the length of points or stay_time should be bigger than 1")

        dis = 0
        path = [points[0]]
        for p_index in range(len(points) - 1):
            # stay at one poinst
            dis += stay_time[p_index]
            path = path + [points[p_index]] * (stay_time[p_index] // 2)
            print('point {}: stay for {} min'.format(points[p_index], stay_time[p_index]))

            # shortest path
            ant = Ant(points[p_index][0], points[p_index][1], points[p_index + 1][0], points[p_index + 1][1],
                      wind_matrix=wind_matrix, rain_matrix=rain_matrix, distance=dis,
                      wind_threshold=wind_threshold[p_index],
                      rain_threshold=rain_threshold[p_index])
            tmp_path = ant.has_shortest_path()
            cost_time = 2 * (len(tmp_path) - 1)
            if len(tmp_path) == 1:
                return "path length is 1"
            if tmp_path:
                path = path + tmp_path[1:]
                dis += cost_time
                print('path {}: cost {} min'.format(p_index + 1, cost_time))
            else:
                print('failed in path between {}, {}'.format(points[p_index], points[p_index + 1]))
                return "failed"

        print('reach {}, cost {}min'.format(points[-1], dis))
        return path


    """
    自动生成路径
    """
    @staticmethod
    def auto_path_generated(wind_matrix, rain_matrix, day, tar, wind_thres, rain_thres, start_time):
        city_data = pd.read_csv('data/CityData.csv')
        start_x, start_y = city_data['xid'][0], city_data['yid'][0]
        tar_x, tar_y = city_data['xid'][tar], city_data['yid'][tar]
        with open('data/history_path/path_x.pickle', 'rb') as f:
            path_x = pickle.load(f)
        with open('data/history_path/path_y.pickle', 'rb') as f:
            path_y = pickle.load(f)
        path_x.append(tar_x)
        path_y.append(tar_y)
        points = []
        for i in range(len(path_x)):
            points.append((path_x[i], path_y[i]))

        stay_time = [0] * len(points)
        stay_time[0] = start_time
        wind_threshold = [wind_thres] * (len(points))
        rain_threshold = [rain_thres] * (len(points))
        path = ChangeMap.get_path(points, stay_time, wind_matrix, rain_matrix, wind_threshold, rain_threshold)
        # 如果存在路径
        if path == "failed":
            return "failed"
        else:
            path_weights = []
            biggest_wind = 0
            biggest_rain = 0
            biggest_coef = 0
            pre_distance = 0
            for p_index, point in enumerate(path):
                wind = wind_matrix[point[0] - 1][point[1] - 1][(pre_distance + p_index * 2) // 60]
                rain = rain_matrix[point[0] - 1][point[1] - 1][(pre_distance + p_index * 2) // 60]
                wind_coef = wind / wind_threshold[0]
                rain_coef = rain / rain_threshold[0]
                path_weights.append((point[0], point[1], wind, rain, max(wind_coef, rain_coef)))
                if wind > biggest_wind:
                    biggest_wind = wind
                if rain > biggest_rain:
                    biggest_rain = rain
                if max(wind_coef, rain_coef) > biggest_coef:
                    biggest_coef = max(wind_coef, rain_coef)
            print('biggest wind:{}, biggest rain: {}, biggest coef: {}'.format(biggest_wind, biggest_rain, biggest_coef))
            for item in path_weights:
                print('({0}, {1}, {2:.2f}, {3:.2f}, {4:.2f})'.format(item[0], item[1], item[2], item[3], item[4]))
            generated_path = "data/generated_path/day" + str(day) + "path" + str(tar) + ".pickle"
            print(generated_path)
            with open(generated_path, 'wb') as f:
                pickle.dump(path, f, protocol=2)
            return "success"