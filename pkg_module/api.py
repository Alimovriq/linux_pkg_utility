import requests


# url адрес для запросов
TARGET_URL: str = "https://rdb.altlinux.org/api/export/branch_binary_packages/"


def get_json() -> list[dict]:
    """
    Получает json по веткам sisyphus и p11
    :return: список с данными по веткам
    """
    result_data = []
    for branch in ["sisyphus", "p11"]:
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


