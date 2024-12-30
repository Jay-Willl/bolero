import pymysql
import pandas as pd

from config import DB_CONFIG

IN_FILE = '../data/dump.json'
SQL_INSERT_COMPOSER_OPENOPUS = """
INSERT INTO COMPOSER_OPENOPUS (name, complete_name, birth, death, epoch, recommended, popular)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
SQL_INSERT_WORK_OPENOPUS = """
INSERT INTO WORK_OPENOPUS (composer_id, title, subtitle, searchterms, genre, recommended, popular)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

composer_columns = ['composer_id', 'name', 'complete_name', 'birth', 'death', 'epoch', 'recommended', 'popular']
composers = pd.DataFrame(columns=composer_columns)

works_columns = ['work_id', 'composer_id', 'title', 'subtitle', 'searchterms', 'genre', 'recommended', 'popular']
works = pd.DataFrame(columns=works_columns)


def read():
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


def inspect():
    print(composers.head())
    print(works.head())


def insert():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            for index, composer in composers.iterrows():
                cursor.execute(SQL_INSERT_COMPOSER_OPENOPUS, (
                    None if pd.isna(composer['name']) else composer['name'],
                    None if pd.isna(composer['complete_name']) else composer['complete_name'],
                    None if pd.isna(composer['birth']) else composer['birth'],
                    None if pd.isna(composer['death']) else composer['death'],
                    None if pd.isna(composer['epoch']) else composer['epoch'],
                    None if pd.isna(composer['recommended']) else composer['recommended'],
                    None if pd.isna(composer['popular']) else composer['popular']
                ))
            for index, work in works.iterrows():
                cursor.execute(SQL_INSERT_WORK_OPENOPUS, (
                    None if pd.isna(work['composer_id']) else work['composer_id'],
                    None if pd.isna(work['title']) else work['title'],
                    None if pd.isna(work['subtitle']) else work['subtitle'],
                    None if pd.isna(work['searchterms']) else work['searchterms'],
                    None if pd.isna(work['genre']) else work['genre'],
                    None if pd.isna(work['recommended']) else work['recommended'],
                    None if pd.isna(work['popular']) else work['popular']
                ))
            connection.commit()
    finally:
        connection.close()


def testinsert():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute(SQL_INSERT_COMPOSER_OPENOPUS,
                           (1, None, "test", "2000-01-01", "2100-01-01", "test", None, 0))
            connection.commit()
    finally:
        connection.close()


if __name__ == '__main__':
    read()
    inspect()
    insert()
