import sqlite3
from flask import Flask, request, jsonify
from errors import NotFoundError, BadRequestError


app = Flask(__name__)
app.config['MAX_ITEMS'] = 100
app.config['DB_FILE'] = 'netflix.db'


@app.errorhandler(404)
@app.errorhandler(NotFoundError)
def not_found_error(error):
    return 'Not found', 404


@app.errorhandler(BadRequestError)
def not_found_error(error):
    return 'Bad request', 400


def run_sql(sql: str):
    conn = sqlite3.connect(app.config['DB_FILE'])
    cursor = conn.cursor()
    results = cursor.execute(sql).fetchall()
    conn.close()
    return results


def make_results_lst(results: list):
    return [{'title': line[0], 'country': line[1], 'release_year': line[2], 'genre': line[3], 'description': line[4]}
            for line in results]


@app.route('/movie/title/')
def show_movie():
    results = []
    if name := request.args.get('s'):

        # to show only one found film
        sql = f"select title, country, release_year, listed_in, description from netflix" \
              f" where lower(title) like '%{name.lower()}%' order by release_year desc limit 1"

        # to show all found films
        #         sql = f"select title, country, release_year, listed_in, description from netflix" \
        #               f" where lower(title) like '%{name.lower()}%'"

        results = run_sql(sql)
    if not results:
        raise NotFoundError
    return jsonify(make_results_lst(results)[0])


@app.route('/movie/year/<int:year1>/<int:year2>')
def show_movie_by_year(year1: int, year2: int):
    sql = f"select title, release_year from netflix" \
          f" where release_year between {year1} and {year2} limit {app.config['MAX_ITEMS']}"
    if not (results := run_sql(sql)):
        raise NotFoundError
    return jsonify([{'title': line[0], 'release_year': line[1]} for line in results])


@app.route('/rating/<category>/')
def show_films_for_category(category: str):
    categories = {'children': ['G'], 'family': ['PG', 'PG-13'], 'adult': ['R', 'NC-17']}
    results = []
    if category in categories:
        str_ = '\', \''.join(categories[category])
        sql = f"select title, rating, description from netflix where rating in ('{str_}')"
        results = run_sql(sql)
    if not results:
        raise NotFoundError
    return jsonify([{'title': line[0], 'rating': line[1], 'description': line[2]} for line in results])


@app.route('/genre/<genre>')
def show_movie_by_genre(genre):
    sql = f"select title, description from netflix" \
          f" where lower(listed_in) like '%{genre.lower()}%' order by release_year desc limit 10"
    if not (results := run_sql(sql)):
        raise NotFoundError
    return jsonify([{'title': line[0], 'description': line[1]} for line in results])


@app.route('/2actors/')
def show_pairs():
    if (actor1 := request.args.get('actor1')) and (actor2 := request.args.get('actor2')):
        actor1 = ' '.join(actor1.split('%')).lower()
        actor2 = ' '.join(actor2.split('%')).lower()
    # actor1 = "Rose McIver" #"Jack Black"  #
    # actor2 = "Ben Lamb"  #"Dustin Hoffman"  #

        sql = f"select \"cast\" from netflix" \
              f" where lower(\"cast\") like '%{actor1}%' and lower(\"cast\")" \
              f" like '%{actor2}%'"
    else:
        raise BadRequestError

    if not (results := run_sql(sql)):
        raise NotFoundError

    actors = {}
    for film in results:
        film_actors = film[0].split(', ')
        for actor in film_actors:
            if actor1 not in actor.lower() and actor2 not in actor.lower():
                actors[actor] = actors.get(actor, 0) + 1

    if not (final_results := [a for a, c in actors.items() if c > 2]):
        raise NotFoundError

    return jsonify(final_results)


if __name__ == '__main__':
    app.run()
