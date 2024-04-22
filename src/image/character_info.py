import requests
import requests_cache
from thefuzz import process, fuzz

requests_cache.install_cache('name_api_cache', expire_after=3600)
CHARACTER_LIST_URL = ("https://huggingface.co/spaces/cagliostrolab"
                      "/animagine-xl-3.1/raw/main/wildcard/characterfull.txt")


def get_all_characters() -> list[str]:
    """
    Get all characters from the character list.
    """
    response = requests.get(CHARACTER_LIST_URL, timeout=3)
    response.raise_for_status()
    text: list[str] = response.text.split("\n")
    return text


def get_closest_character(name):
    """
    Get the closest character name from the character list.
    """
    res = process.extractOne(query=name.lower(), choices=get_all_characters(),
                             scorer=fuzz.partial_token_sort_ratio, score_cutoff=50)
    if res:
        return res[0]
    return None


def get_closest_characters(name, limit=3):
    """
    Get the closest character names from the character list.
    """
    res = process.extractBests(query=name.lower(), choices=get_all_characters(),
                               scorer=fuzz.partial_token_sort_ratio, score_cutoff=50, limit=limit)
    if res[0][1] >= 90:
        return [res[0][0]]
    return [r[0] for r in res]


if __name__ == "__main__":
    print(get_closest_character("Naruto Uzumaki"))
    print(get_closest_character("kita ikuyo"))
    print(get_closest_character("Asuka Langley"))
    print(get_closest_character("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"))
    print(get_closest_characters("Naruto Uzumaki"))
    print(get_closest_characters("kita ikuyo"))
    print(get_closest_characters("Asuka Langley"))
