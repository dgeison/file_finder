from datetime import datetime
from file_finder.exceptions import InvalidInputError
import platform


def get_folders(path):
    """
    Obtém todos os subdiretorios no diretório pesquisado.
    :param path: Um objeto Path() que representa o diretório
    :return: uma lista de objetos Path() em que cada elemento
    será um diretorio que existe em `path`
    """
    return [item for item in path.iterdir() if item.is_dir()]


def get_files(path):
    """
    Obtém todos os arquivos no diretório pesquisado.
    :param path: Um objeto Path() que representa o diretório
    :return: uma lista de objetos Path() em que cada elemento
    será um arquivo que existe em `path`
    """
    return [item for item in path.iterdir() if item.is_file()]


def find_by_name(path, value):
    """
    Obtém todos os arquivos no diretório pesquisado que tenham um nome
    igual a `value` (independente da extensão).
    :param path: Um objeto Path() que representa o diretório
    :param value: str que representa o nome que os arquivos podem ter.
    :return: uma lista de objetos Path() em que cada elemento será um
    arquivo em `path` com um nome igual a `value`.
    """
    files = get_files(path)
    return [file for file in files if file.stem == value]


def find_by_ext(path, value):
    """
    Obtém todos os arquivos no diretório pesquisado que tenham a extensão
    igual a `value` (independente do nome).
    :param path: Um objeto Path() que representa o diretório
    :param value: str que representa a ext. que os arquivos podem ter.
    :return: uma lista de objetos Path() em que cada elemento será um
    arquivo em `path` com uma extensão igual a `value`.
    """
    files = get_files(path)
    return [file for file in files if file.suffix == value]


def find_by_mod(path, value):
    """
    Obtém todos os arquivos no diretório pesquisado que tenham a data de
    modificação igual ao parametro informado.
    :param path: Um objeto Path() que representa o diretório
    :param value: str que representa a data de modificação que os arquivos
    podem ter.
    :return: uma lista de objetos Path() em que cada elemento será um
    arquivo em `path` com uma data de modificação igual a `value`.
    """
    # input: dd/mm/yyyy
    try:
        datetime_obj = datetime.strptime(value, "%d/%m/%Y")
    except ValueError:
        raise InvalidInputError(f"Data de modificação inválida: {value}")

    return [
        file
        for file in get_files(path)
        if datetime.fromtimestamp(file.stat().st_mtime) >= datetime_obj
    ]


def timestamp_to_string(system_timestamp):
    """
    Converte um timestamp do sistema para uma string no formato
    dd/mm/YYYY HH:MM:SS:ms
    :param system_timestamp: timestamp do sistema
    :return: str
    """
    datetime_obj = datetime.fromtimestamp(system_timestamp)
    return datetime_obj.strftime("%d/%m/%Y %H:%M:%S:%f")


def get_files_details(files):
    """
    Obtém uma lista de listas contendo os detalhes importantes
    para cada arquivo representado em 'files'.
    :param files: uma lista de objetos Path() apontando para arquivos
    no sistema de arquivos.
    :return: uma lista de listas em que cada elemento das listas internas
    contém: nome, data de criação, data de modificação e localização dos
    arquivos em 'files'.
    """
    files_details = []
    for file in files:
        stat = file.stat()
        details = [
            file.name,
            timestamp_to_string(get_created_timestamp(stat)),
            timestamp_to_string(stat.st_mtime),
            file.absolute(),
        ]

        files_details.append(details)

    return files_details

def get_created_timestamp(stat):
    if platform.system() == 'Darwin':
        return 'st_birthtime'
    
    return 'st_ctime'