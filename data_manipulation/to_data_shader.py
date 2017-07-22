import json, datetime, time, heapq
import datashader as ds
import datashader.transfer_functions as tf
import pandas as pd


def get_location_id(d, key):
    if key not in d:
        d[key] = len(d.keys())
    return d[key]


def from_index_to_csv(index_file, output_file):
    """
    Flatten the index.json created from Approach1.py to a table
    :param index_file: file path of index file
    :param output_file: path where to save the table.csv
    :return: None
    """
    with open(index_file, 'r') as f:
        print 'Started at {}'.format(str(datetime.datetime.now()))
        location_id_map = {}
        index = json.loads(f.read())
        print 'Completed loading the index at {}'.format(str(datetime.datetime.now()))

        # Order users
        user_order = []
        for user in index:
            time_frames_for_locations = map(lambda loc: len(index[user][loc]), index[user])  # [1, 1, 1]
            user_score = sum(time_frames_for_locations)
            heapq.heappush(user_order, (user_score, user))

        # Save results in that order
        with open(output_file, 'w') as o:
            users_count = len(index)
            print 'Found {} users'.format(users_count)
            user_numeric_id = 0
            while len(user_order) > 0:
                _, user = heapq.heappop(user_order)
                user_numeric_id += 1
                for location in index[user]:
                    location_id = get_location_id(location_id_map, location)
                    for time_frame in index[user][location]:
                        start_timestamp = time.mktime(datetime.datetime.strptime(time_frame[0], "%Y-%m-%d").timetuple())
                        end_timestamp = time.mktime(datetime.datetime.strptime(time_frame[1], "%Y-%m-%d").timetuple())
                        o.write(",".join(map(lambda x: str(x),
                                             [user_numeric_id, location_id, start_timestamp, end_timestamp])) + "\n")
                if user_numeric_id % 1000 == 0:
                    print 'Completed processing {} users'.format(user_numeric_id)
            print 'Finished at {}'.format(str(datetime.datetime.now()))


def create_datashader_image(source_file, outimg_file):
    df = pd.read_csv(source_file)
    cvs = ds.Canvas(plot_width=5800, plot_height=1440)
    agg = cvs.line(df, 'user', 'location', ds.mean('start_date'))
    img = tf.shade(agg, cmap=['lightblue', 'darkblue'], how='linear')
    img.to_pil().save(outimg_file)


def main():
    # from_index_to_csv('../data/approach1_index.json', '../data/user_location_timeframe.csv')
    create_datashader_image('../data/user_location_timeframe.csv', "../data/charts/plot_output.jpg")


if __name__ == '__main__':
    main()
