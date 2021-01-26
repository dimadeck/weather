import argparse

from weather.report import ReportWeather

DEFAULT_RESULT_DIR = 'results'


def parse_args():
    parser = argparse.ArgumentParser(description="Weather")
    parser.add_argument('-k', '--api_key')
    parser.add_argument('-c', '--city')
    parser.add_argument('-d', '--distance')
    parser.add_argument('-w', '--weather_list_filename')
    parser.add_argument('-r', '--result_dir', default=DEFAULT_RESULT_DIR)

    args = parser.parse_args()
    return args.api_key, args.city, args.distance, args.weather_list_filename, args.result_dir


def main():
    api_key, city, distance, weather_list_filename, result_dir = parse_args()
    rw = ReportWeather(api_key=api_key, city=city, distance=distance, weather_list_filename=weather_list_filename,
                       result_dir=result_dir)
    rw.run()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
