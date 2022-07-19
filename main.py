import json
import flask
from utils import search_by_title, search_by_year, search_by_rating, search_by_genre


app = flask.Flask("__name__")


@app.get('/movie/<title>/')
def search_by_title_view(title):
    result = search_by_title(title=title)
    return app.response_class(response=json.dumps(result, ensure_ascii=False, indent=4),
                              status=200, mimetype="application/json")


@app.get('/movie/<int:year1>/to/<int:year2>/')
def search_by_year_view(year1, year2):
    result = search_by_year(year_one=year1, year_two=year2)
    return app.response_class(response=json.dumps(result, ensure_ascii=False, indent=4),
                              status=200, mimetype="application/json")


@app.get('/rating/<rating>/')
def search_by_rating_view(rating):
    result = search_by_rating(rating=rating)
    return app.response_class(response=json.dumps(result, ensure_ascii=False, indent=4),
                              status=200, mimetype="application/json")


@app.get('/genre/<genre>/')
def search_by_genre_view(genre):
    result = search_by_genre(genre=genre)
    return app.response_class(response=json.dumps(result, ensure_ascii=False, indent=4),
                              status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run()
