import pymysql
import pandas as pd

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'casper',
    'database': 'bolero'
}

IN_FILE = '../data/dump.json'
OUT_FILE_COMPOSER = '../data/composer.csv'
OUT_FILE_WORK = '../data/work.csv'

composer_columns = ['composer_id', 'name', 'complete_name', 'birth', 'death', 'epoch', 'recommended', 'popular']
composers = pd.DataFrame(columns=composer_columns)

works_columns = ['work_id', 'composer_id', 'title', 'subtitle', 'searchterms', 'genre', 'recommended', 'popular']
works = pd.DataFrame(columns=works_columns)


def export():
    global composers
    global works
    raw_composers = pd.read_json(IN_FILE, orient='records')
    for index, raw_composer in raw_composers.iterrows():
        print('Processing', raw_composer['name'], index)
        composer = {'composer_id': index, **raw_composer}
        composers = pd.concat([composers, pd.DataFrame([composer]).filter(composer_columns)], ignore_index=True)
        raw_works = composer['works']
        cnt = 0
        for raw_work in raw_works:
            work = {'work_id': cnt, 'composer_id': index, **raw_work}
            cnt += 1
            works = pd.concat([works, pd.DataFrame([work])], ignore_index=True)
    composers = composers.where(pd.notnull(composers), None)
    works = works.where(pd.notnull(works), None)
    composers.to_csv(OUT_FILE_COMPOSER, index=False)
    works.to_csv(OUT_FILE_WORK, index=False)


if __name__ == '__main__':
    export()
