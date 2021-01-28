# Weather

### Описание
Консольное приложение для получения значений температуры воздуха в городах.

Программа должна получить название города и расстояние, в километрах, от 
выбранного города до ребра области заданной квадратом из командной строки.
Программа должна вывести погоду в заданном городе, и среднюю температуру в
полученном квадрате с центом в заданном городе.

Реализовать возможность задать список параметров в файле, в формате

    город1;расстояние1
    город2;расстояние2
    ...
    городN;расстояниеN
    
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
    [Tver']: -2.12 C°, AVG: -0.78 C°
    [Yaroslavl]: 1 C°, AVG: -0.23 C°
    [Moscow]: 0.05 C°, AVG: 0.02 C°

    
    $ python main.py --api_key 870560c80e7bd4ec59bce136398643a4 --city Tver --distance 100
    
    Determining the weather in Tver (+100km)...
    [Tver']: -2.12 C°, AVG: -1.78 C°




    