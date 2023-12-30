import click

from tabulate import tabulate
from pathlib import Path
from utils import find_by_ext
from utils import find_by_name
from utils import find_by_mod


from utils import get_files_details
from utils import get_folders
from datetime import datetime


import shutil


def process_search(path, key, value, recursive):
    search_mapping = {
        "name": find_by_name,
        "ext": find_by_ext,
        "mod": find_by_mod,
    }

    files = search_mapping[key](path, value)

    if recursive:
        subdirs = get_folders(path)
        for subdir in subdirs:
            files += process_search(subdir, key, value, recursive)

    return files


def process_results(files, key, value):
    if not files:
        click.echo(f"Nenhum arquivo com o {key} {value} foi encontrado.")
    else:
        # for f in files:
        #     click.echo(
        #         f"Nome do arquivo: {f.name}\n"
        #         f"Data de Criação: {timestamp_to_string(f.stat().st_ctime)}\n"
        #         f"Data de Modificação: {timestamp_to_string(f.stat().st_mtime)}\n"
        #         f"Localização: {f.parent.absolute()}"
        #     )
        table_haders = ["Nome", "Data de Criação", "Data de Modificação", "Localização"]
        table_data = get_files_details(files)
        tabulate_data = tabulate(
            tabular_data=table_data, headers=table_haders, tablefmt="tsv"
        )
        click.echo(tabulate_data)
        return tabulate_data


@click.command()
@click.argument("path", default="")
@click.option("-k", "--key", required=True, type=click.Choice(["name", "ext", "mod"]))
@click.option("-v", "--value", required=True)
@click.option("-s", "--save", is_flag=True, default=False)
@click.option("-r", "--recursive", is_flag=True, default=False)
@click.option("-c", "--copy-to")
def finder(path, key, value, recursive, copy_to, save):
    root = Path(path)

    if not root.is_dir():
        raise Exception("O caminho informado não representa um diretório válido.")

    click.echo(f"O diretório selecionado foi {root.absolute()}")

    # pesquisar arquivos
    files = process_search(path=root, key=key, value=value, recursive=recursive)
    report = process_results(files=files, key=key, value=value)

    if save:
        if report:
            report_file_path = (
                root / f'finder_report_{datetime.now().strftime("%Y%m%d%H%M%S%f")}.txt'
            )
            with open(report_file_path.absolute(), mode="w") as report_file:
                report_file.write(report)
    if copy_to:
        copy_path = Path(copy_to)

        if not copy_path.is_dir():
            copy_path.mkdir(parents=True)

        for file in files:
            dst_file = (
                copy_path / file.name
            )  # Path("/caminho/para/destino") / "nome_do_arquivo.txt"
            if dst_file.is_file():
                dst_file = (
                    copy_path
                    / f"{file.stem}{datetime.now().strftime('%Y%m%d%H%M%S%f')}{file.suffix}"
                )
            shutil.copy(src=file.absolute(), dst=dst_file)


finder()
