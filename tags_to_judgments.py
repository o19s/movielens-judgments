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
        for idx, movie in enumerate(scoredMovies):
            score = float(movie[1])
            movieId = movie[0]
            #movieName = movies[movieId]
            tmdbId = mlensToTmdbId[movieId]
            grade = 0; sample=True

            if score >= 0.9:
                grade = 4
            elif score >= 0.8:
                grade = 3
            elif score >= 0.6:
                sample = False
                grade = 2
            elif score >= 0.4:
                sample = False
                grade = 1
            else:
                sample = ((idx % 10) == 0)

            try:
                if sample:
                    tmdbIdAsInt = int(tmdbId)
                    judgment = Judgment(grade=grade, qid=qid,
                                        keywords=tagName, docId=tmdbId)
                    judgments.append(judgment)
                else:
                    print("DONT SAMPLE %s %s %s %s" % (grade, qid, tagName, tmdbId))

            except ValueError as e:
                print("SKIPPING %s %s %s %s" % (grade, qid, tagName, tmdbId))

        qid += 1
    return judgments


if __name__ == "__main__":
    tags = tagDict()
    movies = movieDict()
    tagsToMovies = genomeTagged()
    mlensToTmdbId = tmdbIdLookup()

    judgments = buildJudgments(tags, movies, mlensToTmdbId, tagsToMovies)
    judgmentsToFile('genome_judgments.txt', judgments)



