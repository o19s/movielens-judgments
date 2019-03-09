import csv

def tagDict(tagsFile='ml-20m/genome-tags.csv'):
    rdr = csv.reader(open(tagsFile))
    next(rdr, None)

    tags = {}

    for row in rdr:
        tagId = row[0]; tag = row[1]
        tags[tagId] = tag

    return tags

def movieDict(moviesFile='ml-20m/movies.csv'):
    rdr = csv.reader(open(moviesFile))
    next(rdr, None)

    moviesToName = {}

    for row in rdr:
        movieId = row[0]; movieName=row[1]
        moviesToName[movieId] = movieName

    return moviesToName


def genomeTagged(genomeFile='ml-20m/genome-scores.csv'):
    rdr = csv.reader(open(genomeFile))
    next(rdr, None)

    tagsToMovies = {}

    for row in rdr:
        movieId = row[0]; tagId = row[1]; score=row[2]
        if tagId not in tagsToMovies:
            tagsToMovies[tagId] = []

        tagsToMovies[tagId].append( (movieId, score) )

    # Sort each by score
    for tagId, scoredMovies in tagsToMovies.items():
        scoredMovies.sort(key=lambda x: x[1], reverse=True)


    return tagsToMovies


def printBestMoviesPerTag(tags, movies, tagsToMovies):
    for tagId, scoredMovies in tagsToMovies.items():
        print(tags[tagId])
        for i in range(0,5):
            print("  %s %s" % (movies[scoredMovies[i][0]], scoredMovies[i][1]))
        print("  =================")
        for i in range(60,70):
            print("  %s %s" % (movies[scoredMovies[i][0]], scoredMovies[i][1]))
        print("  =================")
        for i in range(1,6):
            print("  %s %s" % (movies[scoredMovies[-i][0]], scoredMovies[-i][1]))


if __name__ == "__main__":
    tags = tagDict()
    movies = movieDict()
    tagsToMovies = genomeTagged()
    printBestMoviesPerTag(tags, movies, tagsToMovies)


