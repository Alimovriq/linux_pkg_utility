import json
import rpm


from api import get_json


def rpm_compare(
        common_pkg_names: set, result_data: dict, key: str,
        sisyphus_pkgs_by_name: dict, p11_pkgs_by_name: dict) -> None:
    """
    Сравнивает version-release пакетов согласно rpm правилам.
    Добавляет пакет из ветки sisyphus, если version-release больше пакета p11
    в результирующий словарь.
    :param common_pkg_names: общие наименования пакетов
    :param result_data: результирующий словарь
    :param key: ключ, по которому добавлять в словарь
    :param sisyphus_pkgs_by_name: сгруппированная ветка sisyphus по наименованиям пактов
    :param p11_pkgs_by_name: сгруппированная ветка p11 по наименованиям пактов
    :return: None
    """
    for name in common_pkg_names:

        a_s_pkg = sisyphus_pkgs_by_name[name]
        a_p11_pkg = p11_pkgs_by_name[name]

        v1 = rpm.hdr()
        v2 = rpm.hdr()
        v1[rpm.RPMTAG_EPOCH] = a_s_pkg.get('epoch', 0)
        v2[rpm.RPMTAG_EPOCH] = a_p11_pkg.get('epoch', 0)
        v1[rpm.RPMTAG_RELEASE] = a_s_pkg['release']
        v2[rpm.RPMTAG_RELEASE] = a_p11_pkg['release']
        v1[rpm.RPMTAG_VERSION] = a_s_pkg['version']
        v2[rpm.RPMTAG_VERSION] = a_p11_pkg['version']

        if rpm.versionCompare(v1, v2) == 1:
            result_data[key].append(a_s_pkg)


def comparator(sisyphus_pkg: dict, p11_pkg: dict) -> dict:
    """
    Сравнивает ветки sisyphus и p11.
    1. все пакеты, которые есть в p11, но отсутствуют в sisyphus
    2. все пакеты, которые есть в sisyphus, но отсутствуют в p11
    3. все пакеты, version-release которых больше в sisyphus, чем в p11
    :param sisyphus_pkg: сгруппированный словарь по архитектуре ветки sisyphus
    :param p11_pkg: сгруппированный словарь по архитектуре ветки p11
    :return: результирующий словарь
    """
    result_data = {
            "only_in_p11": [],
            "only_in_sisyphus": [],
            "sisyphus_version_releases": []
    }

    sisyphus_archs = set(sisyphus_pkg.keys())
    p11_archs = set(p11_pkg.keys())

    # ToDo 1. архитектуры только в sisyphus
    # ToDo 2. архитектуры только в p11
    # only_sisyphus_archs = sisyphus_archs.difference(p11_archs)
    # only_p11_archs_archs = p11_archs.difference(sisyphus_archs)

    # общие наименования архитектур
    archs_sisyphus_p11 = sisyphus_archs.intersection(p11_archs)
    for arch in archs_sisyphus_p11:
        # наименования пакетов в ветках
        sisyphus_pkg_names = set([i["name"] for i in sisyphus_pkg.get(arch)])
        p11_pkg_names = set([j["name"] for j in p11_pkg.get(arch)])

        # все пакеты, которые есть в p11, но отсутствуют в sisyphus
        only_p11_pkg_names = p11_pkg_names.difference(sisyphus_pkg_names)
        only_p11_pkgs = [s for s in p11_pkg[arch] if s["name"] in only_p11_pkg_names]
        result_data["only_in_p11"].extend(only_p11_pkgs)

        # все пакеты, которые есть в sisyphus, но отсутствуют в p11
        only_sisyphus_pkg_names = sisyphus_pkg_names.difference(p11_pkg_names)
        only_sisyphus_pkgs = [p for p in sisyphus_pkg[arch] if p["name"] in only_sisyphus_pkg_names]
        result_data["only_in_sisyphus"].extend(only_sisyphus_pkgs)

        # общие наименования пакетов
        sisyphus_p11_pkg_names = sisyphus_pkg_names.intersection(p11_pkg_names)
        # группировка веток наименованию пакетов
        sisyphus_pkgs_by_name = {pkg["name"]: pkg for pkg in sisyphus_pkg[arch]}
        p11_pkgs_by_name = {pkg["name"]: pkg for pkg in p11_pkg[arch]}
        # все пакеты, version-release которых больше в sisyphus, чем в p11
        rpm_compare(sisyphus_p11_pkg_names, result_data, "sisyphus_version_releases",
                    sisyphus_pkgs_by_name, p11_pkgs_by_name)

    return result_data


def group_by_arch(data: dict) -> dict:
    """
    Группировка по архитектуре. Ключ: архитектура, значение: список с пакетами
    :param data: словарь с данными по пакету
    :return: сгруппированный словарь по архитектуре
    """
    grouped_data = {}
    for item in data:
        arch = item.get("arch")
        if arch is not None:
            if arch not in grouped_data.keys():
                grouped_data[arch] = [item]
            else:
                grouped_data[arch].append(item)
    return grouped_data


def main() -> None:
    """
    Основная функция для запуска процесса сравнения пакетов.
    :return: None
    """
    data = get_json()
    if data:
        sisyphus, p11 = data[0].get("packages"), data[1].get("packages")
        grouped_sisyphus = group_by_arch(sisyphus)
        grouped_p11 = group_by_arch(p11)
        result = comparator(grouped_sisyphus, grouped_p11)
    else:
        result = "<Данные не были получены>"
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()