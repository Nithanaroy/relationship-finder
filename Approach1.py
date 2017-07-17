import json, datetime, bisect


class Approach():
    def __init__(self):
        self.index = {}

    def create_index(self, filename, outfile):
        line = 0
        self.index = {}
        print 'Started at {}'.format(str(datetime.datetime.now()))

        try:
            with open(filename) as f:
                for review_str in f:
                    review = json.loads(review_str)
                    if review['useruser_id'] in self.index:
                        if review['businessuser_id'] in self.index[review['useruser_id']]:
                            bisect.insort_left(self.index[review['useruser_id']][['businessuser_id']],
                                               self.get_date_range(review['date']))
                        else:
                            self.index[review['useruser_id']][review['businessuser_id']] = [
                                self.get_date_range(review['date'])]
                    else:
                        self.index[review['useruser_id']] = {
                            review['businessuser_id']: [self.get_date_range(review['date'])]}
                    line += 1
                    if line % 1000 == 0:
                        print '{}: Completed {} lines'.format(str(datetime.datetime.now()), line)
        except:
            print 'Failed after {} lines'.format(line)

        print 'Saving index to {}'.format(outfile)
        with open(outfile, 'w') as f:
            f.write(json.dumps(self.index))

        print 'Ended at {}'.format(str(datetime.datetime.now()))

    def load_index(self, filename):
        with open(filename) as f:
            self.index = json.loads(f.read())

    def relationship(self, person1, person2):
        res = {}
        common_locations = set(self.index[person1].keys()).intersection(self.index[person2].keys())
        for location in common_locations:
            match = self.find_intersecting_time_frames(self.index[person1][location], self.index[person2][location])
            if len(match) > 0:
                res[location] = match
        return res

    @staticmethod
    def find_intersecting_time_frames(times1, times2):
        res = []
        for time_frame1 in times1:
            for time_frame2 in times2:
                if not (time_frame1[1] < time_frame2[0] or time_frame1[0] > time_frame2[1]):
                    res.append((time_frame1, time_frame2))
        return res

    @staticmethod
    def get_date_range(date_str):
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        start_date = date + datetime.timedelta(days=-1)
        end_date = date + datetime.timedelta(days=1)
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


if __name__ == '__main__':
    a = Approach()
    a.create_index("./yelp_dataset_challenge_round9/yelp_academic_dataset_review.json", "./data/approach1_index.json")
    print 'Started running Approach1\nLoading index...'
    a.load_index("./data/approach1_index.json")
    while True:
        inp = raw_input('Enter user ids separated by a space (empty input to exit): ')
        if len(inp.strip()) == 0:
            print "Exiting"
            break
        p1, p2 = map(lambda p: p.strip(), inp.split(" "))
        print a.relationship(p1, p2)


# { "user_id" : "PcvbBOCOcs6_suRDH7TSTg", "review_count" : 137 }
# { "user_id" : "mTM1yxoV9I0_SSK1mLldmA", "review_count" : 113 }
# { "user_id" : "1DsuFRjdW0gDA23Xswzoqg", "review_count" : 164 }
# { "user_id" : "UByCy7oxeiqFKOLmGUVm3g", "review_count" : 104 }
# { "user_id" : "HdOMMT-x4R_HRpSgjRnoug", "review_count" : 104 }
# { "user_id" : "aD263WOD4RShoqgvVhcKqQ", "review_count" : 117 }
# { "user_id" : "bJTKxBIvb_AR8d4SuLPV8g", "review_count" : 137 }
# { "user_id" : "khyig4aF00tZsTYw4F4GLg", "review_count" : 155 }
# { "user_id" : "eRDWzHCldd6YXypRECvHYg", "review_count" : 121 }
# { "user_id" : "UmXzwFM2OkZHWJ5cJZlqkg", "review_count" : 195 }
# { "user_id" : "ehzvSXsijzgxsYHvXeaS-Q", "review_count" : 125 }
# { "user_id" : "owlUazXSDLaxlOV7z8181g", "review_count" : 195 }
# { "user_id" : "S9Jw00eZHVj5_0sOM_C5Rg", "review_count" : 284 }
# { "user_id" : "-50XWnmQGqBgEI-9ANvLlg", "review_count" : 106 }
# { "user_id" : "tH0uKD-vNwMoEc3Xk3Cbdg", "review_count" : 304 }
# { "user_id" : "xVV86BToDOQGxE1gt9MMvg", "review_count" : 143 }
# { "user_id" : "r-zUIQPaHzvIyL93wQaoiQ", "review_count" : 143 }
# { "user_id" : "_Ab2puRl7Tb9rlgOuPZJQA", "review_count" : 168 }
# { "user_id" : "clmrlflES5HrXS-gl_YmrQ", "review_count" : 138 }
# { "user_id" : "gVmUR8rqUFdbSeZbsg6z_w", "review_count" : 188 }

# Success case
# Users = khyig4aF00tZsTYw4F4GLg 3MO--ENqKScLFQFuW1751g, Answer = {u'eZcCFV-8X91ZSnmB9807bw': [([u'2010-08-03', u'2010-08-05'], [u'2010-08-05', u'2010-08-07'])]}
# Users = sa5zd7bwBQzajQB48Y9SUw _K2q8hN-3_KLaKrsH1KxIg, Answer = {u'eZcCFV-8X91ZSnmB9807bw': [([u'2010-07-17', u'2010-07-19'], [u'2010-07-17', u'2010-07-19'])]}
