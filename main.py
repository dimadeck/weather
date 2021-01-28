import argparse

from weather.weather import Weather


def parse_args():
    parser = argparse.ArgumentParser(description="Weather")
    parser.add_argument('-k', '--api_key')
    parser.add_argument('-c', '--city')
    parser.add_argument('-d', '--distance')
    parser.add_argument('-w', '--weather_list_filename')

    args = parser.parse_args()
    return args.api_key, args.city, args.distance, args.weather_list_filename


def main():
    api_key, city, distance, weather_list_filename = parse_args()
    weather = Weather(api_key)
    weather.determinate_weather(city=city, distance=distance, weather_list_filename=weather_list_filename)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
