import rpm


from pkg_module.logger import logger


class BranchPackageContext:
    """
    Хранит в себе информацию по двум сравниваемым веткам:
    - Текущая архитектура
    - Наименование ветки
    - Список пакетов ветки;
    - отсортированный список пакетов по наименованию пакетов (ключ).
    При использовании метода get_pkgs - возвращает список пакетов, которые
    есть в первой ветке, но отсутствуют во второй
    """

    def __init__(self, arch, first_branch_name, first_branch_pkg,
                 second_branch_name, second_branch_pkg) -> None:

        self.arch = arch
        self.first_branch_name = first_branch_name
        self.first_branch_pkg = first_branch_pkg
        self.second_branch_name = second_branch_name
        self.second_branch_pkg = second_branch_pkg
        self.first_branch_pkg_names = set([i["name"] for i in self.first_branch_pkg[self.arch]])
        self.second_branch_pkg_names = set([j["name"] for j in self.second_branch_pkg[self.arch]])

    def get_pkgs(self, reverse: bool) -> list[dict]:
        """
        Возвращает пакеты, которые есть в первой ветке, но отсутствуют во второй
        :param reverse: меняет местами сравнение веток
        :return: список пакетов
        """

        if reverse:
            only_pkg_names = self.first_branch_pkg_names.difference(self.second_branch_pkg_names)
            result_pkgs = [pkg for pkg in self.first_branch_pkg[self.arch] if pkg["name"] in only_pkg_names]
        else:
            only_pkg_names = self.second_branch_pkg_names.difference(self.first_branch_pkg_names)
            result_pkgs = [pkg for pkg in self.second_branch_pkg[self.arch] if pkg["name"] in only_pkg_names]
        return result_pkgs


def rpm_compare(
        cmp_context: BranchPackageContext, result_data: dict, key: str,
        first_branch_pkgs_by_name: dict, second_branch_pkgs_by_name: dict) -> None:
    """
    Сравнивает version-release пакетов согласно rpm правилам.
    Добавляет пакет из первой ветки (напр., sisyphus), если version-release больше пакета
    второй ветки (напр., p11) в результирующий словарь.
    :param cmp_context: Класс с данными по веткам
    :param result_data: результирующий словарь
    :param key: ключ, по которому добавлять в результирующий словарь
    :param first_branch_pkgs_by_name: сгруппированная первая ветка по наименованиям пакетов
    :param second_branch_pkgs_by_name: сгруппированная вторая ветка по наименованиям пактов
    :return: None
    """

    # общие наименования пакетов
    all_branches_pkg_names = cmp_context.first_branch_pkg_names.intersection(
        cmp_context.second_branch_pkg_names)
    for name in all_branches_pkg_names:

        first_branch_pkg = first_branch_pkgs_by_name[name]
        second_branch_pkg = second_branch_pkgs_by_name[name]

        v1 = rpm.hdr()
        v2 = rpm.hdr()
        v1[rpm.RPMTAG_EPOCH] = first_branch_pkg.get('epoch', 0)
        v2[rpm.RPMTAG_EPOCH] = second_branch_pkg.get('epoch', 0)
        v1[rpm.RPMTAG_RELEASE] = first_branch_pkg['release']
        v2[rpm.RPMTAG_RELEASE] = second_branch_pkg['release']
        v1[rpm.RPMTAG_VERSION] = first_branch_pkg['version']
        v2[rpm.RPMTAG_VERSION] = second_branch_pkg['version']

        if rpm.versionCompare(v1, v2) == 1:
            result_data[key].append(first_branch_pkg)


def comparator(first_branch_pkg: dict, second_branch_pkg: dict,
               first_branch_name: str, second_branch_name: str) -> dict:
    """
    Сравнивает ветку № 1 (напр., sisyphus) и ветку № 2 (напр., p11)
    Алгоритм:
    1. все пакеты, которые есть в second_branch_pkg, но отсутствуют в first_branch_pkg
    2. все пакеты, которые есть в first_branch_pkg, но отсутствуют в second_branch_pkg
    3. все пакеты, version-release которых больше в first_branch_pkg, чем в second_branch_pkg
    :param first_branch_pkg: сгруппированный словарь по архитектуре первой ветки
    :param second_branch_pkg: сгруппированный словарь по архитектуре второй ветки
    :param first_branch_name: наименование первой ветки
    :param second_branch_name: наименование второй ветки
    :return: результирующий словарь
    """

    result_data = {
            f"only_in_{first_branch_name}": [],
            f"only_in_{second_branch_name}": [],
            f"newest_in_{first_branch_name}": []
    }

    first_branch_archs = set(first_branch_pkg.keys())
    second_branch_archs = set(second_branch_pkg.keys())

    # ToDo 1. архитектуры только в first_branch. Уточнить необходимость, можно добавить
    # ToDo 2. архитектуры только в second_branch. Уточнить необходимость, можно добавить

    # общие наименования архитектур
    archs_all_branches = first_branch_archs.intersection(second_branch_archs)
    for arch in archs_all_branches:

        cmp_context = BranchPackageContext(arch, first_branch_name, first_branch_pkg, second_branch_name, second_branch_pkg)
        logger.info(f"Started filling data by arch: <{arch}>")
        fill_result_data(cmp_context, result_data)

        # группировка веток наименованию пакетов
        logger.debug(f"Grouping packages by name")
        first_branch_pkgs_by_name, second_branch_pkgs_by_name = group_by_name(arch, first_branch_pkg, second_branch_pkg)
        logger.info(f"Comparing package version-release")
        # все пакеты, version-release которых больше в первой ветке, чем во второй
        rpm_compare(cmp_context, result_data, f"newest_in_{first_branch_name}",
                    first_branch_pkgs_by_name, second_branch_pkgs_by_name)

    return result_data


def fill_result_data(cmp_context: BranchPackageContext, result_data: dict) -> None:
    """
    Функция для заполнения результирующего словаря.
    :param cmp_context: Класс с данными по веткам
    :param result_data: Результирующий словарь с пакетами
    :return: None
    """

    # все пакеты, которые есть во второй ветке, но отсутствуют в первой
    logger.info(f"Adding packages only in branch <{cmp_context.second_branch_name}>")
    only_second_branch_pkgs = cmp_context.get_pkgs(False)
    result_data[f"only_in_{cmp_context.second_branch_name}"].extend(only_second_branch_pkgs)

    # все пакеты, которые есть в первой ветке, но отсутствуют во второй
    logger.info(f"Adding packages only in branch <{cmp_context.first_branch_name}>")
    only_first_branch_pkgs = cmp_context.get_pkgs(True)
    result_data[f"only_in_{cmp_context.first_branch_name}"].extend(only_first_branch_pkgs)


def group_by_name(arch: str, first_branch_pkg: dict, second_branch_pkg: dict) -> tuple:
    """
    Группирует пакеты веток по наименованию пакетов. Первый ключ: наименование пакета
    :param arch: архитектура
    :param first_branch_pkg: пакеты первой ветки
    :param second_branch_pkg: пакеты второй ветки
    :return: кортеж с группированными пакетами по двум веткам
    """

    first_branch_pkgs_by_name = {pkg["name"]: pkg for pkg in first_branch_pkg[arch]}
    second_branch_pkgs_by_name = {pkg["name"]: pkg for pkg in second_branch_pkg[arch]}
    return first_branch_pkgs_by_name, second_branch_pkgs_by_name


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
