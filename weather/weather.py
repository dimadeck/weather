import csv

import requests


class OpenWeatherHelper:
    """
    Класс для получения данных с сервиса OpenWeatherMap.org. Для отправки запросов необходим API_KEY
    """
    BASE_URL = 'https://api.openweathermap.org/data/2.5/'
    KM_DEGREE = 0.009
    BBOX_ZOOM = 10

    def __init__(self, api_key):
        if not api_key:
            raise ValueError("Need API key")
        self._api_key = api_key

    def get_weather_data(self, city, distance):
        """
        Определение координат города
        Получение параметра bbox для запроса данных в искомой области
        Получение и возврат данных о погоде в области

        :param city: Город - центр области
        :param distance: Расстояние до границы
        :return: Данные о погоде в искомой области
        """
        coord = self._get_city_coord(city)
        lon, lat = coord.get('lon'), coord.get('lat')
        if not (lon and lat):
            raise ValueError('Coords not found')
        bbox = self._get_bbox_param(lon, lat, distance)
        return self._make_request(self._get_bbox_url(bbox))

    def _get_city_coord(self, city):
        """
        Метод для получения координат города

        :param city: Город
        :return: {'lon', 'lat'}
        """
        weather_data = self._make_request(self._get_weather_url(city))
        return weather_data.get('coord', {})

    def _get_bbox_param(self, lon, lat, distance):
        """
        Метод для определения параметра bbox

        :param lon: Долгота
        :param lat: Широта
        :param distance: Расстояние до границы
        :return: 'left,bottom,right,top,zoom'
        """
        degree_dist = int(distance) * self.KM_DEGREE
        bbox = [lon - degree_dist, lat + degree_dist, lon + degree_dist, lat - degree_dist, self.BBOX_ZOOM]
        return ",".join([str(item) for item in bbox])

    def _get_bbox_url(self, bbox):
        """
        Метод для получения ссылки на маршрут определение погоды в заданной области

        :param bbox: Строка вида 'left,bottom,right,top,zoom'
        :return: URL
        """
        return f'{self.BASE_URL}box/city?bbox={bbox}&appid={self._api_key}&units=metric'

    def _get_weather_url(self, city):
        """
        Метод для получения ссылки на маршрут определение данных о погоде в городе

        :param city: Город
        :return: URL
        """
        return f'{self.BASE_URL}weather?q={city}&appid={self._api_key}'

    @staticmethod
    def _make_request(url):
        """
        Метод для отправки GET запроса по указанному маршруту

        :param url: Маршрут
        :return: JSON ответ от сервиса
        """
        return requests.get(url).json()


class Weather:
    """
    Класс для определения текущей температуры воздуха в городах с выводом средней температуры в области
    """

    def __init__(self, api_key):
        self.open_weather = OpenWeatherHelper(api_key)

    def determinate_weather(self, city=None, distance=None, weather_list_filename=None):
        """
        Генерации списка городов
        Определения температуры воздуха в списке городов
        Вывод в порядке возрастания средней температуры

        :param city: Город
        :param distance: Расстояние
        :param weather_list_filename: Путь к файлу со списком городов
        :return:
        """
        cities = self.get_cities(city, distance, weather_list_filename)
        results = [self._get_city_weather_data(city, distance) for city, distance in cities]
        for city in sorted(results, key=lambda k: k['avg']):
            print(f"[{city.get('name')}]: {city.get('temp')} C°, AVG: {city.get('avg')} C°")

    @staticmethod
    def get_cities(city, distance, weather_list_filename):
        """
        Метод для генерации списка городов из файла или из значений city, distance

        :param city: Город
        :param distance: Расстояние
        :param weather_list_filename: Путь к файлу csv со списком городов
        :return: [(city_1, distance_1), ...]
        """
        if not (city and distance or weather_list_filename):
            raise ValueError("Need city and distance or weather_list_filename")
        cities = []
        if weather_list_filename:
            with open(weather_list_filename, "r") as csv_file:
                reader = csv.reader(csv_file, delimiter=';')
                for row in reader:
                    cities.append(row)
        else:
            cities.append([city, distance])
        return cities

    def _get_city_weather_data(self, city, distance):
        """
        Определение температуры в городе

        :param city: Город
        :param distance: Расстояние
        :return: Данные о погоде вида {'name', 'temp', 'avg'}
        """
        print(f'Determining the weather in {city} (+{distance}km)...')
        try:
            weather_data = self.open_weather.get_weather_data(city, distance)
            if weather_data.get('message'):
                raise ValueError(weather_data.get('message'))

            temperatures = [city.get('main', {}).get('temp') for city in weather_data.get('list', [])]
            if not temperatures:
                raise ValueError('Weather Data not found')
            return {
                'name': weather_data.get('list')[0].get('name'), 'temp': temperatures[0],
                'avg': round(sum(temperatures) / len(temperatures), 2)
            }
        except ValueError as e:
            print(e)
