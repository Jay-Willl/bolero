import pymysql

from config import DB_CONFIG
from getdata import get_nationality, parse_title, get_portrait

FAILED_PATH = '../data/parse_failed_titles.txt'

SQL_SELECT_ALL_COMPOSER_OPENOPUS = """
SELECT * FROM COMPOSER_OPENOPUS
"""

SQL_SELECT_ALL_WORK_OPENOPUS = """
SELECT * FROM WORK_OPENOPUS
"""

SQL_INSERT_COMPOSER = """
INSERT INTO COMPOSER (name, complete_name, portrait, birth, death, epoch, nationality, recommended, popular)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

SQL_INSERT_WORK = """
INSERT INTO WORK (composer_id, title, subtitle, searchterms, genre, recommended, popular, number, tonality, opus, opus_no, catalog_abr, catalog_no, nickname)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

failed = list()

def migrate_composer():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute(SQL_SELECT_ALL_COMPOSER_OPENOPUS)
            result = cursor.fetchall()
            for record in result:
                cursor.execute(SQL_INSERT_COMPOSER, (
                    record[1],  # name
                    record[2],  # complete_name
                    get_portrait(record[2]),  # portrait
                    record[4],  # birth
                    record[5],  # death
                    record[6],  # epoch
                    get_nationality(record[2]),  # nationality
                    0 if record[8] is None or record[8] == 0 else 1,  # recommended
                    record[9]  # popular
                ))
                print((
                    record[1],  # name
                    record[2],  # complete_name
                    get_portrait(record[2]),  # portrait
                    record[4],  # birth
                    record[5],  # death
                    record[6],  # epoch
                    get_nationality(record[2]),  # nationality
                    0 if record[8] is None or record[8] == 0 else 1,  # recommended
                    record[9]
                ))
                connection.commit()
    except Exception:
        pass


def migrate_work():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute(SQL_SELECT_ALL_WORK_OPENOPUS)
            result = cursor.fetchall()
            for record in result:
                parsed_title = parse_title(record[2])
                if len(parsed_title) != 8:
                    failed.append(record[2])
                    continue
                new_record = (
                    record[1],  # composer_id
                    record[2],  # title
                    None if len(record[3]) == 0 else record[3],  # subtitle
                    None if len(record[4]) == 0 else record[4],  # searchterms
                    record[5],  # genre
                    record[7],  # recommended
                    record[8],  # popular
                    parsed_title['number'],
                    parsed_title['tonality'],
                    parsed_title['opus'],
                    parsed_title['opus_no'],
                    parsed_title['catalog_abr'],
                    parsed_title['catalog_no'],
                    parsed_title['nickname']
                )
                print('Parsing:', record[2], new_record)
                cursor.execute(SQL_INSERT_WORK, new_record)
            connection.commit()
    except Exception as e:
        failed.append(record[2])
        pass


def testinsert():
    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            cursor.execute(SQL_INSERT_WORK,
                           (0, 'Berceuse élégiaque', 'For chamber orchestra', None, 'Orchestral', 0, 0, None, None, None,
                            None, None, None, None))
            connection.commit()
    except Exception as e:
        e.with_traceback()



if __name__ == '__main__':
    # migrate_composer()
    migrate_work()
    with open(FAILED_PATH, 'w') as f:
        for title in failed:
            f.write(title + '\n')
    # testinsert()
