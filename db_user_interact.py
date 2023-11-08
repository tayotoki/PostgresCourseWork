#!/usr/bin/env python3

import argparse

from database.manager import DBManager

db_manager = DBManager()


def get_db_result(args):
    if args.keyword:
        return db_manager.get_vacancies_with_keyword(args.keyword)
    if args.get_all_vacs:
        return db_manager.get_all_vacancies()
    if args.get_comp_and_vac_count:
        return db_manager.get_companies_and_vacancies_count()
    if args.get_vacs_with_higher_salary:
        return db_manager.get_vacancies_with_higher_salary()
    if args.get_avg_salary:
        return db_manager.get_avg_salary()


parser = argparse.ArgumentParser(description="Database-User adapter")
parser.add_argument(
    "-gcvc",
    "--get_comp_and_vac_count",
    action="store_true",
    help="Show company name with vacancies count"
)
parser.add_argument(
    "-gvwhs",
    "--get_vacs_with_higher_salary",
    action="store_true",
    help="Show vacancies with greater than average salary"
)
parser.add_argument(
    "-gvwk",
    "--get_vacs_with_keyword",
    dest="keyword",
    type=str,
    help="Shows vacancies whose names contain the passed keyword"
)
parser.add_argument(
    "-gav",
    "--get_all_vacs",
    action="store_true",
    help="Show all vacancies"
)
parser.add_argument(
    "-gas",
    "--get_avg_salary",
    action="store_true",
    help="Show average low and high salary"
)


if __name__ == "__main__":
    args = parser.parse_args()
    if not vars(args):
        parser.print_usage()
    else:
        try:
            print(*get_db_result(args=args), sep="\n\n")
        except TypeError as e:
            print("Пустой результат")
            parser.print_usage()
