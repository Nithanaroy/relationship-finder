import json

from pymongo import MongoClient


def import_yelp_reviews(filename):
    client = MongoClient()
    db = client.relationship
    line = 0
    with open(filename) as f:
        for review in f:
            db.yelp.insert(json.loads(review))
            line += 1
            if line % 1000 == 0:
                print "Imported {} reviews".format(line)


if __name__ == '__main__':
    import_yelp_reviews("./yelp_dataset_challenge_round9/yelp_academic_dataset_review.json")
