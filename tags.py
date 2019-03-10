import csv
from judgments import Judgment, judgmentsToFile

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


def tmdbIdLookup(moviesFile='ml-20m/links.csv'):
    rdr = csv.reader(open(moviesFile))
    next(rdr, None)

    mlensToTmdb = {}

    for row in rdr:
        movieId = row[0]; tmdbId=row[2]
        mlensToTmdb[movieId] = tmdbId

    return mlensToTmdb


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


def buildJudgments(tags, movies, mlensToTmdbId, tagsToMovies):
    print("Building Judgments")
    qid = 1
    judgments = []
    for tagId, scoredMovies in tagsToMovies.items():
        tagName = tags[tagId]
        for movie in scoredMovies:
            score = float(movie[1])
            movieId = movie[0]
            #movieName = movies[movieId]
            tmdbId = mlensToTmdbId[movieId]
            grade = 0

            if score >= 0.9:
                grade = 4
            elif score >= 0.8:
                grade = 3
            elif score >= 0.6:
                grade = 2
            elif score >= 0.4:
                grade = 1

            judgment = Judgment(grade=grade, qid=qid,
                                keywords=tagName, docId=tmdbId)
            judgments.append(judgment)
        qid += 1
    return judgments


if __name__ == "__main__":
    tags = tagDict()
    movies = movieDict()
    tagsToMovies = genomeTagged()
    mlensToTmdbId = tmdbIdLookup()

    judgments = buildJudgments(tags, movies, mlensToTmdbId, tagsToMovies)
    judgmentsToFile('genome_judgments.txt', judgments)



