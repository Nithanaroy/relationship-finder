import json, datetime, bisect


class Approach():
    def create_index(self, filename, outfile):
        index = {}
        with open(filename) as f:
            for review_str in f:
                review = json.loads(review_str)
                if review['user_id'] in index:
                    if review['business_id'] in index[review['user_id']]:
                        bisect.insort_left(index[review['user_id']][['business_id']],
                                           self.get_date_range(review['date']))
                    else:
                        index[review['user_id']][review['business_id']] = [self.get_date_range(review['date'])]
                else:
                    index[review['user_id']] = {review['business_id']: [self.get_date_range(review['date'])]}
                break
            print index
        with open(outfile, 'w') as f:
            f.write(json.dumps(index))

    def get_date_range(self, date_str):
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        start_date = date + datetime.timedelta(days=-1)
        end_date = date + datetime.timedelta(days=1)
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


a = Approach()
a.create_index("./yelp_dataset_challenge_round9/yelp_academic_dataset_review.json", "index.json")
