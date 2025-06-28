#!/usr/bin/env python3
import os
import sys
import argparse
import json


from pkg_module import api
from pkg_module import data_compare


def check_answer(filepath: str) -> bool:
    """
    Проверяет подтверждение для сохранения файла по пути.
    Необходимо ответить <y> или <n> (регистр не имеет значения).
    :param filepath: стандартный путь для файла рядом с исполняемым файлом
     и название результирующего файла
    :return: булево значение
    """
    print(f"Are you sure to save result json file by path: {filepath} ?")
    choice = input("press Y/n to continue...\n").lower()
    if choice == "y":
        return True
    return False


def main() -> None:
    """
    Основная функция для запуска утилиты. Парсит командную строку.
    Аргументы: <branch1> <branch 2> --output <filename.json>.
    Спрашивает подтверждения сохранения по пути. Если не получит <y>, тогда
    программа завершит свое выполнение.
    :return: None
    """
    parser = argparse.ArgumentParser(description="ALT Linux utility for comparing branch pairs.")
    parser.add_argument(
        "branches", nargs="*",
        help="Branch names for comparing (default: sisyphus p11)", default=("sisyphus", "p11"))
    parser.add_argument("--output", default="result.json", help="Output file (default: result.json")
    # ToDo: Добавить логгирование
    try:
        args = parser.parse_args()
        path_to_save_json = f"{os.path.dirname(os.path.abspath(__file__))}/{args.output}"
        choice = check_answer(path_to_save_json)
        if choice:
            response_data = api.get_json(*args.branches)
            first_branch_pkgs, second_branch_pkgs = response_data[0]["packages"], response_data[1]["packages"]
            grouped_first_branch= data_compare.group_by_arch(first_branch_pkgs)
            grouped_second_branch= data_compare.group_by_arch(second_branch_pkgs)
            result = data_compare.comparator(
                grouped_first_branch, grouped_second_branch, args.branches[0], args.branches[1])
            # print(json.dumps(result, indent=2))
            with open(args.output, "w") as file:
                json.dump(result, file, indent=2)
            print(f"json file is saved: {path_to_save_json}")
            print(f"Comparing branch_1: <{args.branches[0]}> and branch_2: <{args.branches[1]}> is finished")
        else:
            print("You need to confirm the path to save result json file by answers <y> or <n>")
            sys.exit(1)
    except argparse.ArgumentError as err:
        print(f"Error occurred in command line args: {err}")
        parser.print_help()
    except Exception as err:
        print(f"Error occurred: {err}")


if __name__ == "__main__":
    main()