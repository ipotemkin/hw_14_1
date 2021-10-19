from __init__ import app
from utils import run_sql, make_results
from flask import request, jsonify, render_template
from errors import NotFoundError, BadRequestError, ValidationError


@app.errorhandler(404)
@app.errorhandler(NotFoundError)
def not_found_error(error):
    return 'Not found', 404


@app.errorhandler(BadRequestError)
def not_found_error(error):
    return 'Bad request', 400


@app.errorhandler(ValidationError)
def validation_error(error):
    return 'Validation error', 400


# instructions
@app.route('/')
def index():
    return render_template('index.html')


# returns a movie by title
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
    return jsonify(make_results('title', 'country', 'release_year', 'genre', 'description', data=results)[0])


# returns MAX_ITEMS movies by years (between year1 and year2)
@app.route('/movie/year/<int:year1>/<int:year2>')
def show_movie_by_year(year1: int, year2: int):
    sql = f"select title, release_year from netflix" \
          f" where release_year between {year1} and {year2} limit {app.config['MAX_ITEMS']}"
    if not (results := run_sql(sql)):
        raise NotFoundError
    return jsonify(make_results('title', 'release_year', data=results))


# returns movies by category
@app.route('/rating/<category>/')
def show_films_for_category(category: str):
    results = []
    if category in app.config['CATEGORIES']:
        str_ = '\', \''.join(app.config['CATEGORIES'][category])
        sql = f"select title, rating, description from netflix where rating in ('{str_}')"
        results = run_sql(sql)
    if not results:
        raise NotFoundError
    return jsonify(make_results('title', 'rating', 'description', data=results))


# shows a movie by genre
@app.route('/genre/<genre>')
def show_movie_by_genre(genre):
    sql = f"select title, description from netflix" \
          f" where lower(listed_in) like '%{genre.lower()}%' order by release_year desc limit 10"
    if not (results := run_sql(sql)):
        raise NotFoundError
    return jsonify(make_results('title', 'description', data=results))


# shows pairs to the two given actors
@app.route('/2actors/')
def show_pairs():
    if (actor1 := request.args.get('actor1')) and (actor2 := request.args.get('actor2')):
        actor1 = ' '.join(actor1.split('%')).lower()  # to test through a browser
        actor2 = ' '.join(actor2.split('%')).lower()  # to test through a browser

    # sample testing data
    # actor1 = "Rose McIver" #"Jack Black"  #
    # actor2 = "Ben Lamb"  #"Dustin Hoffman"  #

        sql = f"select \"cast\" from netflix where lower(\"cast\") like '%{actor1}%'" \
              f" and lower(\"cast\") like '%{actor2}%'"
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


# finds a movie by type, year or genre
@app.route('/movie/')
def find_movie():
    sql_start = "select title, description from netflix where "
    sql_lst = []
    sql = ''
    if type_ := request.args.get('type'):
        sql_lst.append(f" type = '{type_}'")
    if year := request.args.get('year'):
        sql_lst.append(f" release_year = '{year}'")
    if genre := request.args.get('genre'):
        sql_lst.append(f" listed_in like '%{genre}%'")
    if sql_lst:
        sql = sql_start + ' and '.join(sql_lst)

    if not (results := run_sql(sql)):
        raise NotFoundError

    return jsonify(make_results('title', 'description', data=results))
