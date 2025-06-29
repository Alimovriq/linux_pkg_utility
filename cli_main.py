#!/usr/bin/env python3
import os
import sys
import argparse
import json


from pkg_module import api
from pkg_module import data_compare
from pkg_module.logger import logger


def check_answer(filepath: str) -> bool:
    """
    Проверяет подтверждение для сохранения файла по пути.
    Необходимо ответить <y> или <n> (регистр не имеет значения).
    :param filepath: стандартный путь для файла рядом с исполняемым файлом
     и название результирующего файла
    :return: булево значение
    """
    while True:
        print(f"Are you sure to save result file by path/name: {filepath} ?")
        choice = input("press Y/n to continue...\n").lower()
        if choice == "y":
            return True
        elif choice == "n":
            return False


def main() -> None:
    """
    Основная функция для запуска утилиты. Парсит командную строку.
    Аргументы: <branch1> <branch 2> --output <filename.json>.
    Спрашивает подтверждения сохранения по пути. Если получит <y>, тогда
    программа продолжит выполнение, если <n>, тогда завершит работу.
    :return: None
    """
    parser = argparse.ArgumentParser(description="ALT Linux utility for comparing branch pairs.")
    parser.add_argument(
        "branches", nargs="*",
        help="Branch names for comparing (default: sisyphus p11)", default=("sisyphus", "p11"))
    parser.add_argument("--output", default="result.json", help="Output file (default: result.json")
    try:
        logger.debug("Starting parsing arguments")
        args = parser.parse_args()
        logger.info(f"Get arguments of branches: <{args.branches[0]}>, <{args.branches[1]}>")
        path_to_save_json = f"{os.path.dirname(os.path.abspath(__file__))}/{args.output}"
        choice = check_answer(path_to_save_json)
        if choice:
            logger.info(f"Set file path/name: {path_to_save_json}")
            response_data = api.get_json(*args.branches)
            first_branch_pkgs, second_branch_pkgs = response_data[0]["packages"], response_data[1]["packages"]
            logger.info(f"Starting the process of grouping packages by arch")
            grouped_first_branch= data_compare.group_by_arch(first_branch_pkgs)
            grouped_second_branch= data_compare.group_by_arch(second_branch_pkgs)
            result = data_compare.comparator(
                grouped_first_branch, grouped_second_branch, args.branches[0], args.branches[1])
            logger.info(f"Prepared data with keys: {list(result.keys())}")
            # print(json.dumps(result, indent=2))
            logger.info(f"Starting the process of saving file <{args.output}>")
            with open(args.output, "w") as file:
                json.dump(result, file, indent=2)
            logger.info(f"File s successfully saved: {path_to_save_json}")
            logger.info(f"Comparing branch_1: <{args.branches[0]}> and branch_2: <{args.branches[1]}> - is finished.")
        else:
            logger.warning(f"Get input command <n>. CLI-utility is finished working")
            sys.exit(1)
    except argparse.ArgumentError as err:
        logger.critical(f"Error occurred in command line args: {err}")
        parser.print_help()
    except Exception as err:
        logger.critical(f"Error occurred: {err}")
    finally:
        logger.info("CLI-utility is finished working")


if __name__ == "__main__":
    logger.debug("Starting CLI-utility")
    main()

    # добавил логгирование
    # исправил баг с переменно first pkg in data_compare
    # check_answer - цикл While True
    #