import re
import requests


def parse_title(title_):
#     PATTERN = re.compile(r'''
# ^
# (?P<title>[^,"]+?)
# (?:                                              # ============ no. x [in x major] ============
#     \s+no\.\s*(?P<number>\d+)                    # "no. 3"
#     (?:\s+in\s+(?P<tonality>[A-G](?:\s(?:flat|sharp))?\s+major))?
# )?
# (?:                                              # =========== , op. x [no. y] ===============
#     ,\s*op\.\s*(?P<opus>\d+)                     # "op. 70"
#     (?:\s+no\.\s*(?P<opus_no>\d+))?              # "no. 1"
# )?
# (?:                                              # ============ , K.551 / BWV 1024  ============
#     ,\s*(?P<catalog_abr>[A-Z][A-Za-z0-9]*)      # catalog_abr = K, BWV, Hob, etc.
#     (?:\.|\s)(?P<catalog_no>\d+(?:\.\d+)?)       # catalog_no = 551, 1024, 6.3, etc.
# )?
# (?:
#     ,\s*"(?P<nickname>[^"]+)"
# )?$
# ''', re.VERBOSE)
    PATTERN = re.compile(r'''
^(?P<title>
  [^,"]+                            #   先吃掉任意非逗号/引号字符
  (?:,[^,"]+)*                      #   后续允许出现若干次 「逗号 + 非逗号/引号的字符」
)?                                  #   这一整段可选（有些标题可能只由结构化信息组成……虽不常见）
(?:                                  # ============= 可选的 no. X in X major ===============
  ,?\s*no\.\s*(?P<number>\d+)       #   允许前面有可选逗号, 然后 "no. 3" -> 捕获 3
  (?:\s+in\s+(?P<tonality>[A-G](?:\s(?:flat|sharp))?\s+major))?
)?                                  #   整块可选
(?:                                  # ============= 可选的 op. X [no. Y] ==================
  ,?\s*op\.\s*(?P<opus>\d+)         #   允许前面有可选逗号, 然后 "op. 66" -> 捕获 66
  (?:\s+no\.\s*(?P<opus_no>\d+))?   #   允许多捕获一个 "no. X"
)?                                  #   整块可选
(?:                                  # ============= 可选的 目录缩写 + 编号 =================
  ,?\s*(?P<catalog_abr>[A-Z][A-Za-z0-9]*)   # 允许前面有可选逗号, 匹配 "B", "K", "BWV" 等
  (?:\.|\s)(?P<catalog_no>\d+(?:\.\d+)?)     # 再匹配点或空格, 然后是数字(可带小数点)
)?                                  #   整块可选
(?:                                  # ============= 可选的 昵称 "..." =====================
  ,?\s*"(?P<nickname>[^"]+)"        #   允许前面有可选逗号, 再匹配引号中的任意字符
)?$''', re.VERBOSE)
    match = PATTERN.match(title_)
    result = dict()
    if match:
        result['title'] = match.group('title')
        result['number'] = match.group('number')
        result['tonality'] = match.group('tonality')
        result['opus'] = match.group('opus')
        result['opus_no'] = match.group('opus_no')
        result['catalog_abr'] = match.group('catalog_abr')
        result['catalog_no'] = match.group('catalog_no')
        result['nickname'] = match.group('nickname')
    return result


def get_nationality(name_):
    SEARCH_URL = 'https://www.wikidata.org/w/api.php'
    SEARCH_PARAMS = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",  # 搜索所用语言
        "search": name_
    }

    try:
        response = requests.get(SEARCH_URL, params=SEARCH_PARAMS)
        data = response.json()
        if "search" in data and len(data["search"]) > 0:
            qid = data["search"][0]["id"]
        else:
            return None
    except Exception:
        return None

    ENTITY_URL = 'https://www.wikidata.org/w/api.php'
    ENTITY_PARAMS = {
        "action": "wbgetentities",
        "format": "json",
        "ids": qid,
        "props": "claims|labels",
        "languages": "en"
    }

    try:
        response = requests.get(ENTITY_URL, params=ENTITY_PARAMS)
        data = response.json()

        entity_data = data["entities"].get(qid, {})
        claims = entity_data.get("claims", {})
        if "P27" not in claims:
            return None
        country_claim = claims["P27"][0]
        country_value = (country_claim["mainsnak"]
                         .get("datavalue", {})
                         .get("value", {}))
        country_qid = country_value.get("id")
        if not country_qid:
            return None
    except Exception:
        return None

    COUNTRY_ENTITY_PARAMS = {
        "action": "wbgetentities",
        "format": "json",
        "ids": country_qid,
        "props": "labels",
        "languages": "en"
    }

    response = requests.get(ENTITY_URL, params=COUNTRY_ENTITY_PARAMS)
    data = response.json()
    country_entity = data["entities"].get(country_qid, {})
    labels = country_entity.get("labels", {})

    if "en" in labels and "value" in labels["en"]:
        country_label = labels["en"]["value"]
    else:
        country_label = labels.get("en", {}).get("value", None)

    return country_label


def get_portrait(name_):
    SEARCH_URL = 'https://www.wikidata.org/w/api.php'
    SEARCH_PARAMS = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",  # 搜索所用语言
        "search": name_
    }

    try:
        response = requests.get(SEARCH_URL, params=SEARCH_PARAMS)
        data = response.json()
        if "search" in data and len(data["search"]) > 0:
            qid = data["search"][0]["id"]
        else:
            return None
    except Exception:
        return None

    ENTITY_URL = 'https://www.wikidata.org/w/api.php'
    ENTITY_PARAMS = {
        "action": "wbgetentities",
        "format": "json",
        "ids": qid,
        "props": "claims",
        "languages": "en"
    }

    try:
        response = requests.get(ENTITY_URL, params=ENTITY_PARAMS)
        data = response.json()

        entity_data = data["entities"].get(qid, {})
        claims = entity_data.get("claims", {})
        if "P18" not in claims:
            return None
        portrait_claim = claims["P18"][0]
        portrait_value = "File:" + portrait_claim["mainsnak"]["datavalue"]["value"]
    except Exception:
        return None

    COMMONS_URL = "https://en.wikipedia.org/w/api.php"
    COMMONS_PARAMS = {
        "action": "query",
        "titles": portrait_value,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }

    try:
        response = requests.get(COMMONS_URL, params=COMMONS_PARAMS)
        data = response.json()
        pages = data["query"]["pages"]
        for index, page in pages.items():
            imageinfo = page.get("imageinfo", [])
            if imageinfo:
                return imageinfo[0].get('url')


    except Exception:
        return None


def test_parse_title():
    samples = [
        "6 Mazurkas de salon, for piano, op. 66, B.12"
    ]
    for sample in samples:
        result = parse_title(sample)
        print(result)


def test_get_nationality():
    samples = [
        "Wolfgang Amadeus Mozart",
        "Pyotr Ilyich Tchaikovsky",
        "Johann Sebastian Bach",
        "Frederic Chopin",
        "Giacomo Puccini",
        "Carl Philipp Emanuel Bach",
        "Alexander von Zemlinsky",
        "xxxx yyy"
    ]
    for sample in samples:
        result = get_nationality(sample)
        print(result)


def test_get_portrait():
    samples = [
        "Wolfgang Amadeus Mozart",
        "Pyotr Ilyich Tchaikovsky",
        "Johann Sebastian Bach",
        "Frederic Chopin",
        "Giacomo Puccini",
        "Carl Philipp Emanuel Bach",
        "Alexander von Zemlinsky",
        "xxxx yyy"
    ]
    for sample in samples:
        result = get_portrait(sample)
        print(result)


if __name__ == '__main__':
    test_parse_title()
    # test_get_nationality()
    # test_get_portrait()
