import scraper.aclu_scraper as aclu_scraper
import scraper.lambda_scraper as lambda_scraper
import json


def main():
    aclu_cases = aclu_scraper.get_all_cases()
    write_cases('visual/data/aclu.json', aclu_cases)

    lambda_cases = lambda_scraper.get_all_cases()
    write_cases('visual/data/lambda.json', lambda_cases)


def write_cases(path, cases):
    with open(path, 'w') as file:
        file.write(json.dumps(cases, indent=4))


if __name__ == '__main__':
    main()
