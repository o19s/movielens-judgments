from tags import tags_to_movies, tags
import random


def true_preferences(tags_to_movies,
                     revealed, hiddens,
                     revealed_weight=0.8):
    """ Generate a ground truth of a search users preferences
        from movielens genome tags
        where
         - revealed is ostensibly a keyword like 'star trek'
           that exists in the genome tag data (else KeyError)
         - hiddens is a list of hidden preferences as genome tags
           such as the user likes 007, zombie movies, etc
         - revealed_weight is how to weigh the revealed user intent, with
           hiddens receiving 1 - revealed_weight
    """

    revealed_prefs = tags_to_movies[revealed]

    # Build a huge list of all the movies
    hiddenPrefMovies = []
    for tag in hiddens:
        hiddenPrefMovies.extend(tags_to_movies[tag])

    # Consolidate to a dictionary
    collapsed = {}
    for movie in hiddenPrefMovies:
        title = movie[1]
        score = float(movie[2])
        if title not in collapsed:
            collapsed[title] = []
        collapsed[title].append(score)

    # Reduce to an average
    sorted_collapsed = []
    for title, prefs in collapsed.items():
        numItems = len(prefs)
        sumPrefs = sum(prefs)
        sorted_collapsed.append( (title, sumPrefs / numItems))
        collapsed[title] = sumPrefs / numItems

    sorted_collapsed.sort(key=lambda pref: pref[1], reverse=True)

    print("From tags %s" % hiddens)
    for coll in sorted_collapsed[:5]:
        print(coll)

    print("Avg with %s" % revealed)
    tmdb_id_to_score = {}
    for movie in revealed_prefs:
        tmdb_id = movie[0]
        title = movie[1]
        hiddenHere = collapsed[title]
        revealedHere = float(movie[2])

        score = (revealedHere * revealed_weight
                 + hiddenHere * (1 - revealed_weight))

        tmdb_id_to_score[tmdb_id] = score

    return tmdb_id_to_score


def search(es, query, index='tmdb'):
    resp = es.search(index=index,
                     body=query)
    results = []
    for hit in resp['hits']['hits']:
        title = ''
        if 'title' in hit['_source']:
            title = hit['_source']['title']
        results.append((hit['_id'], title))
    return results

def prob_wants_to_watch(tag_score):
    max_score = 0.7
    min_score = 0.5
    if tag_score > max_score:
        return 0.99
    if tag_score < min_score:
        return 0.01
    return (tag_score - min_score) / (max_score - min_score)
    #return min(0.98, (10**(tag_score+1) / (10**(1+max_score))))


if __name__ == "__main__":

    num_to_avg = 5

    random.shuffle(tags)
    hidden = tags[:5]

    revealed = 'star wars'

    prefs = true_preferences(tags_to_movies,
                             revealed=revealed, hiddens=hidden,
                             revealed_weight=0.51)

    query = {
      "query": {
        "bool": {
          "should": [
            {"match": {
                "text_all": revealed
            }},
            {"match": {
                "title": {
                  "query": revealed,
                  "boost": 100}
            }}]
        }
      }
    }

    from elasticsearch import Elasticsearch
    es = Elasticsearch()
    results = search(es, query)
    for result in results:
        tmdb_id = result[0]
        score = 0.01
        if tmdb_id in prefs:
            score = prefs[tmdb_id]
        print("%s %s %s %s" % (tmdb_id, result[1], score, prob_wants_to_watch(score)))
