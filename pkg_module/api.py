import requests


# url адрес для запросов
TARGET_URL: str = "https://rdb.altlinux.org/api/export/branch_binary_packages/"


def get_json(first_branch: str, second_branch: str) -> list[dict | None]:
    """
    Получает json по двум веткам
    :return: список с данными по веткам
    """
    result_data = []
    for branch in [first_branch, second_branch]:
       url = f"{TARGET_URL}{branch}"
       try:
           request = requests.get(url)
           request.raise_for_status()
           response = request.json()
           result_data.append(response)
       except requests.exceptions.RequestException as err:
           print(f"Ошибка при запросе к API: {err}")
           break
    return result_data


