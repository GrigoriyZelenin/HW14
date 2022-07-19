from collections import Counter
import json
import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "netflix.db")


def search_query(sql):
    with sqlite3.connect(db_path) as con:
        con.row_factory = sqlite3.Row
        result = con.execute(sql).fetchall()
        return result


def search_by_title(title):
    sql = f"""
            SELECT *
            FROM netflix
            WHERE title = '{title}'
            ORDER BY release_year DESC
            LIMIT 1"""
    set_ = search_query(sql)
    for item in set_:
        result = dict(item)

    return result


def search_by_year(year_one, year_two):
    sql = f"""
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN '{year_one}' AND '{year_two}'
            LIMIT 100"""
    set_ = search_query(sql)
    result = []
    for item in set_:
        result.append(dict(item))
    return result


def search_by_rating(rating):
    dict_rating = {
        'children': ('G', 'G'),
        'family': ('G', 'PG', 'PG-13'),
        'adult': ('R', 'NC-17')}
    sql = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating in {dict_rating.get(rating, ('R', 'R'))}"""
    set_ = search_query(sql)
    result = []
    for item in set_:
        result.append(dict(item))
    return result


def search_by_genre(genre):
    sql = f"""
            SELECT *
            FROM netflix
            WHERE listed_in LIKE '%{genre}%'
            ORDER BY release_year DESC
            LIMIT 10"""
    set_ = search_query(sql)
    result = []
    for item in set_:
        result.append(dict(item))
    return result


def search_by_cast(cast_one, cast_two):
    sql = f"""
            SELECT "cast"
            FROM netflix
            WHERE "cast" LIKE '%{cast_one}%' AND "cast" LIKE '%{cast_two}%'"""
    set_ = search_query(sql)
    set_names = []
    for item in set_:
        names = set(dict(item).get('cast').split(', ')) - set([cast_one, cast_two])
        for name in names:
            set_names.append(name)
    result = []
    x = Counter(set_names)
    for k, v in dict(x).items():
        if v > 2:
            result.append(k)

    return result


def search_by_parameters(type_, year, genre):
    sql = f"""
                SELECT title, description, listed_in
                FROM netflix
                WHERE type = '{type_}'
                AND release_year = '{year}'
                AND listed_in LIKE '%{genre}%'"""
    set_ = search_query(sql)
    result = []
    for item in set_:
        result.append(dict(item))
    return json.dumps(result)
