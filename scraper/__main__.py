import sys

import scraper.aclu_scraper as aclu_scraper
import scraper.lambda_scraper as lambda_scraper
import scraper.case_cleaner as case_cleaner
import json


def main():
    if len(sys.argv) < 2:
        return

    if sys.argv[1] == 'scrape':
        scrape_all()
    elif sys.argv[1] == 'clean':
        clean_all()


def scrape_all():
    aclu_cases = aclu_scraper.get_all_cases()
    write_cases('visual/data/aclu.json', aclu_cases)

    lambda_cases = lambda_scraper.get_all_cases()
    write_cases('visual/data/lambda.json', lambda_cases)


def clean_all():
    aclu_cases = read_cases('visual/data/aclu.json')
    lambda_cases = read_cases('visual/data/lambda.json')
    all_cases = aclu_cases + lambda_cases

    all_cases = case_cleaner.clean_cases(all_cases)

    write_cases('visual/data/all.json', all_cases)


def write_cases(path, cases):
    with open(path, 'w') as file:
        file.write(json.dumps(cases, indent=4))


def read_cases(path):
    with open(path, 'r') as file:
        return json.load(file)


if __name__ == '__main__':
    main()
