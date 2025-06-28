import requests


TARGET_URL: str = "https://rdb.altlinux.org/api/export/branch_binary_packages/"


def get_json() -> list[dict]:
    """
    Получает json по веткам sisyphus и p11
    :return: список с данными по веткам
    """
    result_data = []
    for branch in ["sisyphus", "p11"]:
       url = f"{TARGET_URL}{branch}"
       request = requests.get(url)
       response = request.json()
       result_data.append(response)
    return result_data


