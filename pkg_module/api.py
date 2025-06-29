import requests


from pkg_module.logger import logger


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
       request = requests.get(url)
       logger.info(f"Sent GET-response: {url}")
       request.raise_for_status()
       response = request.json()
       result_data.append(response)
    return result_data


