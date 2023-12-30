from utils import find_by_ext
from utils import find_by_name
from utils import find_by_mod

SEARCH_MAPPING = {
    "name": find_by_name,
    "ext": find_by_ext,
    "mod": find_by_mod,
}

TABLE_HEADERS = ["Nome", "Data de Criação", "Data de Modificação", "Localização"]
