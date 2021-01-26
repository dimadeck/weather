# Weather

### Описание
Консольное приложение для получения значений температуры воздуха в городах.

Программа должна получить название города и расстояние, в километрах, от 
выбранного города до ребра области заданной квадратом из командной строки.
Программа должна вывести погоду в заданном городе, и среднюю температуру в
полученном квадрате с центом в заданном городе.

Реализовать возможность задать список параметров в файле, в формате

    город1;расстояние1;
    город2;расстояние2;
    ...
    городN;расстояниеN;
    
Отсортировать вывод по возрастанию средней температуры.

Расстояние - целое число в км.

### Настройка и запуск

    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    
### Запуск

    $ python main.py --api_key 870560c80e7bd4ec59bce136398643a4 --weather_list_filename weather_list.csv
    
    Determining the weather in Tver (+250km)...
    Determining the weather in Moscow (+100km)...
    Determining the weather in Yaroslavl (+200km)...
    =============================================
    [Moscow]: -3.62 C°
    [AVG (+100 km)]: -2.85 C°
    [Measurements]: [-3.62, -3.35, -1.58]
    =============================================
    [Yaroslavl]: 1 C°
    [AVG (+200 km)]: 0.86 C°
    [Measurements]: [1, 1, 1, 1, 1, 0.59, 1, 0.98, 1, 1, 0.75, 0.83, 0.93, 0.66, 0.72, 0.55, 0.97, 0.54, 0.02, 0.09, 0.6, 0.37, 0.84, 0.86, 0.83, 0.08, 2, 0.9, 1.22, 1.12, 0, 1, 1.6, 1.44, 1, 1, 1.33]
    =============================================
    [Tver']: 0.64 C°
    [AVG (+250 km)]: 1.33 C°
    [Measurements]: [0.64, 0.88, 0.82, 2, 0.92, 0.85, 1.19, 2, 0.79, 1.23, 2, 1.09, 0.77, 1.5, 1.15, 2, 2, 1.57, 1.56, 1.58, 0.97, 1.57, 2, 1.08, 2, 0.56, 2, 1.83, 1, 1.19, 1.22, 1.22, 1.6, 1.56, 1.56, 1.07, 1.56, 1.2, 1.23, 1.23, 1.24, 1.25, 1.27, 1.41, 1.02, 1.29, 1.2, 0.56, 2.23, 0.56, 0.71, 1.67, 1.32, 1.35, 1.29, 1.57, 1.48]

    
    $ python main.py --api_key 870560c80e7bd4ec59bce136398643a4 --city Tver --distance 100
    
    Determining the weather in Tver (+100km)...
    =============================================
    [Tver']: 0.64 C°
    [AVG (+100 km)]: 1.18 C°
    [Measurements]: [0.64, 0.88, 2, 1.19]



    