import json

import requests


class CityData:
    DEFAULT_CITY_LIST_PATH = 'data/city_list.json'
    KM_DEGREE = 0.009
    BBOX_ZOOM = 10

    def __init__(self, city_path=DEFAULT_CITY_LIST_PATH):
        """
        Класс CityData хранит словарь с данными городов

        :param city_path: Путь к json файлу с данными о городах (http://bulk.openweathermap.org/sample/)
        """
        self._city_data = self._get_data(city_path)

    @staticmethod
    def _get_data(path):
        """
        Метод для преобразования данных openweathermap в структуру {'city': {'id', 'lon', 'lat'}}

        :param path: Путь к json файлу с данными о городах
        :return: {'city': {'id', 'lon', 'lat'}}
        """
        with open(path, 'r') as js_file:
            city_list = json.load(js_file)
        city_data = {}
        for city in city_list:
            city_data[city.get('name')] = {'id': city.get('id'), 'lon': city.get('coord', {}).get('lon'),
                                           'lat': city.get('coord', {}).get('lat')}
        return city_data

    def get_bbox(self, city, distance):
        """
        :param city: Название города латиницей
        :param distance: Расстояние в км до границы квадрата расстояние, в километрах, от
            выбранного города до ребра области заданной квадратом
        :return: 'left,bottom,right,top,zoom'
        """
        city = self._city_data.get(city)
        if not city:
            raise ValueError('City not found')
        degree_dist = distance * self.KM_DEGREE
        lat, lon = city.get('lat'), city.get('lon')
        bbox = [lon - degree_dist, lat + degree_dist, lon + degree_dist, lat - degree_dist, self.BBOX_ZOOM]
        return ",".join([str(item) for item in bbox])


class Weather:
    def __init__(self, api_key):
        """
        Класс для получения данных о погоде через сервис api.openweathermap.org
        :param api_key: Ключ для доступа к ресурсу
        """
        self.api_key = api_key
        self._city_data = CityData()

    def get_weather(self, city, distance):
        """
        Метод для получения данных о погоде для выбранного города и расстояния

        Получение границ области
        Формирование URL для запроса
        Возврат ответа от сервиса

        :param city: Город латиницей
        :param distance: Расстояние в км
        :return: Ответ от сервиса в формате json
        """
        bbox = self._city_data.get_bbox(city, distance)
        url = self._get_url(bbox)
        return self._request_data(url)

    def _get_url(self, bbox):
        """
        Формирование url для запроса

        :param bbox: Строка с описанием границ вида 'left,bottom,right,top,zoom'
        :return: URL
        """
        return f'https://api.openweathermap.org/data/2.5/box/city?bbox={bbox}&appid={self.api_key}'

    @staticmethod
    def _request_data(url):
        """
        Отправка запроса и получение ответа в формате json
        :param url:
        :return: Ответ от ресурса
        """
        response = requests.get(url)
        return response.json()
