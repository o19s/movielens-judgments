import csv

def __tags_to_names(tagsFile='ml-latest/genome-tags.csv'):
    """ Map tag ids to tag names"""
    rdr = csv.reader(open(tagsFile))
    next(rdr, None)

    tags = {}

    for row in rdr:
        tagId = row[0]; tag = row[1]
        tags[tagId] = tag

    return tags

def __movies_to_titles(mlens_to_tmdb, moviesFile='ml-latest/movies.csv'):
    """ Map movielens movie ids to movie names """
    rdr = csv.reader(open(moviesFile))
    next(rdr, None)

    moviesToName = {}

    for row in rdr:
        movieLensId = row[0]; movieName=row[1]
        tmdb_id = mlens_to_tmdb[movieLensId]
        moviesToName[tmdb_id] = movieName

    return moviesToName


def __movielens_to_tmdb(moviesFile='ml-latest/links.csv'):
    rdr = csv.reader(open(moviesFile))
    next(rdr, None)

    mlensToTmdb = {}

    for row in rdr:
        movieLensId = row[0]; tmdbId=row[2]
        mlensToTmdb[movieLensId] = tmdbId

    return mlensToTmdb


def __tags_to_movies(mlens_to_tmdb, movies_to_titles, tags_to_names,
                     genomeFile='ml-latest/genome-scores.csv'):
    """ Tags with each movie scored """
    rdr = csv.reader(open(genomeFile))
    next(rdr, None)

    tagsToMovies = {}

    for row in rdr:
        movieLensId = row[0]; tagId = row[1]; score=row[2]
        tmdb_id = mlens_to_tmdb[movieLensId]
        tagName = tags_to_names[tagId]
        if tagName not in tagsToMovies:
            tagsToMovies[tagName] = []

        title = movies_to_titles[tmdb_id]
        tagsToMovies[tagName].append( (tmdb_id, title, score) )

    # Sort each by score
    for tagId, scoredMovies in tagsToMovies.items():
        scoredMovies.sort(key=lambda x: x[2], reverse=True)

    return tagsToMovies

tags_to_movies = None

if tags_to_movies == None:
    print("Loading movielens Data")
    # Try pickle
    import pickle
    pklPath = '.tmdb_tags.pkl'
    try:
        with open(pklPath, 'rb') as f:
            print("From Pickle...")
            tags_to_movies = pickle.load(f)
    except IOError:
        print("From CSV...")
        __mlens_to_tmdb = __movielens_to_tmdb()
        __tags_to_names = __tags_to_names()
        __movies_to_titles = __movies_to_titles(__mlens_to_tmdb)

        tags_to_movies = __tags_to_movies(__mlens_to_tmdb, __movies_to_titles,
                                          __tags_to_names)
        tags = [tag_name for tag_name, _ in tags_to_movies.items()]
        with open(pklPath, 'wb') as of:
            pickle.dump(tags_to_movies, of)
    tags = [tag_name for tag_name, _ in tags_to_movies.items()]
