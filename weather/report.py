import csv
import json
import os

from weather.weather import Weather


class ReportWeather:
    """
    Класс для демонстрации работы класса Weather
    На вход получает API_KEY к сервису, файл со списоком параметров или город и дистанция,
    путь к директории для сохранения результатов
    """

    def __init__(self, api_key, city, distance, weather_list_filename, result_dir):
        self._api_key = api_key
        self._city = city
        self._distance = distance
        self._weather_list_filename = weather_list_filename
        self._result_dir = result_dir
        self._results = []
        if not api_key:
            raise ValueError("Need API key")
        if not (city and distance or weather_list_filename):
            raise ValueError("Need city and distance or weather_list_filename")

    def run(self):
        """Интерфейсный метод для сбора температур и вывод результата на экран"""
        rows = []
        if self._weather_list_filename:
            with open(self._weather_list_filename, "r") as csv_file:
                reader = csv.reader(csv_file, delimiter=';')
                for row in reader:
                    rows.append(row)
        else:
            rows.append([self._city, self._distance])

        os.makedirs(self._result_dir, exist_ok=True)

        for city, distance in rows:
            print(f'Determining the weather in {city} (+{distance}km)...')
            self._handle_city(city, int(distance))
        self._report()

    def _handle_city(self, city, distance):
        """
        Получение показаний погоды для города, добавление результатов замера в историю
        :param city: Город латиницей
        :param distance: Расстояние до границы
        :return:
        """
        weather = Weather(self._api_key)
        data = weather.get_weather(city, distance)
        self._add_result(data, city, distance)

    def _add_result(self, weather_data, city, distance):
        """
        Сохранение результатов, запоминание результата для дальнейшего вывода
        :param weather_data: Ответ от сервиса
        :param city: Город
        :param distance: Расстояние до границы
        :return:
        """
        result_filename = os.path.join(self._result_dir, f'{city}_{distance}_weather.json')
        with open(result_filename, 'w') as js_file:
            json.dump(weather_data, js_file, ensure_ascii=False)

        if weather_data.get('message'):
            raise ValueError(weather_data.get('message'))

        temperatures = [city.get('main', {}).get('temp') for city in weather_data.get('list', [])]
        if not temperatures:
            raise ValueError('Weather Data not found')

        self._results.append({'name': weather_data.get('list')[0].get('name'),
                              'distance': distance,
                              'temp': temperatures[0],
                              'avg': round(sum(temperatures) / len(temperatures), 2),
                              'measurements': temperatures})

    def _report(self):
        """
        Вывод результата на экран (отсортированнный)
        :return:
        """
        for city in sorted(self._results, key=lambda k: k['avg']):
            print('=' * 45)
            print(f"[{city.get('name')}]: {city.get('temp')} C°")
            print(f"[AVG (+{city.get('distance')} km)]: {city.get('avg')} C°")
            print(f"[Measurements]: {city.get('measurements')}")
