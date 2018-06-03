import requests
from yaml import load, Loader


if __name__ == "__main__":
    print("All of Github's supported languages and their search extensions are:")
    langs = requests.get("https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml")
    parsed_langs = load(langs.text, Loader=Loader)
    for lang in parsed_langs:
        if parsed_langs.get(lang).get("type") == "programming":
            print(lang)
            aliases = parsed_langs.get(lang).get("aliases")
            if aliases is not None:
                for alias in aliases:
                    print("\t" + alias)
