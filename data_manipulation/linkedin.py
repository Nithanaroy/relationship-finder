#!/usr/local/bin/python
# -*- coding: utf-8

import requests, json, re, unicodedata, sys, traceback, datetime, math
from time import sleep
from pymongo import MongoClient
import pymongo

MAX_DOC_LENGTH = 16793598.0

url_prefix = "https://www.linkedin.com/voyager/api/identity/profiles"
state_persist_file = "linkedin_parsing_status.txt"
max_depth = 2
headers = {"authority": 'www.linkedin.com',
           "method": 'GET',
           "scheme": 'https',
           "accept": 'application/vnd.linkedin.normalized+json',
           "accept-encoding": 'gzip, deflate, br',
           "accept-language": 'en-US,en;q=0.8,en-GB;q=0.6',
           "cache-control": 'no-cache',
           "cookie": 'JSESSIONID="ajax:1348591311292006406"; bcookie="v=2&aaff8c02-85f6-44d1-8045-6c311b8c347f"; bscookie="v=1&20170728071715c125eacf-0252-41ee-8f1f-361b6e35f7a3AQHPnzplBCnbFC-5Ba8yA4ewyInhyhfF"; _ga=GA1.2.1123751443.1501226238; visit="v=1&M"; _lipt=CwEAAAFdlNsEVHpB1MiGmNQez1UhaswGF4opY707AVeMHyqNWk4_LJC9yPvr5v0gx_iX0gsvttdmDRCQ8YnVJ8IVone08Lrshv55f3jKDJHMtsZsIoKpOaWRmGRhstZ68e3-mXi2QrAbr3zJVsjP_MEp4920CwW6TDznjoOm7343WH3Om56YSRxt18G2cxCu8SjzmMF3CMf9J1VV2eHjEAJaNVWPTsXIqKHNOC-54byykbqi8YzsGg5ePCix6jjPfiWi4Pf1UhZjVW-6P7aFnQ4Nsj7I_nFjK6VtBIQj7KANQlew5sITYWL_loyXxivmvaZoC6P7wdI2oUWzDo2O4_iBFMUSpntptoNgcDWCce2AJKYscoUATatYcM68jglkeayssmjwx3MZAnq8bHXxXE721fnsr2aYDWKgOx-G6OQXaSeNBOizwrGzG22TwhacnnOLLrrBqNQd-8S5mOPIKxMJTFmsS5_AEyp6AsjpWpbnHGwLz9pZ4RcIcsSrHXuCzvCsOOgCSZju76QnjTca22TtZde2G8q-hnRH1oazmyQ5qmu-kTVx6J7RqcC3OSuOOcnwvTDhvL1R3fpYS3C7PcmOQ1pbqJi0FcGkuKsaEW0uk-GsBaR4COgb_ABzUOwfUXLK8SSK1fo3mc4dmXt9yA0fzEDEKgkU0Ai3XEqYSsxmme2U48d6AC1ojIxhzAEjefDoq0DYknJXjAWTgtp6vFHTxSFtf5qF; lidc="b=OB62:g=346:u=265:i=1501440746:t=1501519050:s=AQHWt3YMLr8gfO-bk6cbstJMvQ3WIRzB"; join_wall=v=2&AQHjmU6GfV1OfQAAAV2UzuMyLrDYuV4tfX31qqz-TVnYaT-m1HfRNmshGfmwDQmgkqZjj6QE7d2UtSzK-vRl3yRhiSU0PMZBOfJmn7LescFeoGrjttebZmuuaUskHrLvv3GbEifspsV8Ig; RT=s=1501440582957&r=https%3A%2F%2Fwww.linkedin.com%2Fuas%2Fconsumer-captcha-v2%3FchallengeId%3DAQG2RKuZgf8mDAAAAV2Uz_mfn8hUbbsrb9CVPil1HyIo5B596Ogd0Z7p6ijjRdmGUCVNE24_0WRmldZOqUk9mm04E4Q1P7M7Kg; sl="v=1&Ta-kX"; li_at=AQEDAQLi8o4D_iIUAAABXZTUJwwAAAFdloubDFYARlIX-3DAL-SgKJVhhb1_iqDKLKFC9JGdV47nzyVVUpOg17-idDntUoUYllbssY9-D0kQmDihZk36YngErMVPlkZZRUMFkALuMrXb2fZtbp_R7vfe; liap=true; _gat=1; lang="v=2&lang=en-us"; sdsc=22%3A1%2C1501440729958%7EJOBS%2C063BzV75HHjXyv7n%2FX91CM7SjOFI%3D',
           "csrf-token": 'ajax:1348591311292006406',
           "dnt": '1',
           "pragma": 'no-cache',
           "referer": 'https://www.linkedin.com/',
           "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
           "x-li-lang": 'en_US',
           "x-li-page-instance": 'urn:li:page:d_flagship3_profile_view_base;cm/DtV3uR1SUd+FZhwhcEA==',
           "x-li-track": '{"clientVersion":"1.0.*","osName":"web","timezoneOffset":-7,"deviceFormFactor":"DESKTOP"}',
           "x-requested-with": 'XMLHttpRequest',
           "x-restli-protocol-version": '2.0.0'}

print "PyMongo Version, %s" % (pymongo.version,)

client = MongoClient()
db = client.linkedin_graph


def find(test, arr, default={}):
    for e in arr:
        if test(e):
            return e
    return default


def clean(inp):
    return unicodedata.normalize('NFKD', inp).encode('utf-8', 'ignore')


def parse_positions(positions, user):
    result = []
    for position in positions.get('data', {"elements": []}).get('elements', []):
        position_id = re.findall(r',(\d+)\)$', position)[0]
        relevant_details = filter(lambda detail: detail.get('$id', "").find(position_id) >= 0, positions['included'])
        start_date_obj = find(lambda d: d['$id'].endswith(",timePeriod,startDate"), relevant_details)
        end_date_obj = find(lambda d: d['$id'].endswith(",timePeriod,endDate"), relevant_details)
        # company_meta = find(lambda d: d['$id'].endswith(",company"), relevant_details)
        # company_id = re.findall(r',(\d+)\),company$', company_meta['$id'])[0]  # Non standard companies will not have this
        company_obj = find(
            lambda detail: detail.get("entityUrn", "") == "urn:li:fs_position:({},{})".format(user, position_id),
            positions['included'])
        start_date = "{}-{}".format(start_date_obj.get('year', ''), start_date_obj.get('month', ''))
        end_date = "{}-{}".format(end_date_obj.get('year', ''), end_date_obj.get('month', ''))
        company_name = company_obj.get('companyName', '')
        company_id = company_obj.get('companyUrn', 'urn:li:fs_miniCompany:' + company_name)[
                     len(u'urn:li:fs_miniCompany:'):]  # Default to company name if ID not found
        worked_as = company_obj.get('title', '')
        result.append({"sdate": start_date, "edate": end_date,
                       "cname": company_name, "cid": company_id, "role": worked_as})
    return result


def parse_education(education, user):
    result = []
    for ed in education.get('data', {"elements": []}).get('elements', []):
        ed_id = re.findall(r',(\d+)\)$', ed)[0]
        relevant_details = filter(lambda detail: detail.get('$id', "").find(ed_id) >= 0, education['included'])
        start_date_obj = find(lambda d: d['$id'].endswith(",timePeriod,startDate"), relevant_details)
        end_date_obj = find(lambda d: d['$id'].endswith(",timePeriod,endDate"), relevant_details)
        institution_obj = find(
            lambda detail: detail.get("entityUrn", "") == "urn:li:fs_education:({},{})".format(user, ed_id),
            education['included'])
        start_date = start_date_obj.get('year', '')
        end_date = end_date_obj.get('year', '')
        school_name = institution_obj.get('schoolName', '')
        school_id = institution_obj.get('schoolUrn', 'urn:li:fs_miniCompany:' + school_name)[
                    len(u'urn:li:fs_miniCompany:'):]  # Default to school name if ID not found
        degree = institution_obj.get('degreeName', '')
        field = institution_obj.get('fieldOfStudy', '')
        result.append({"sdate": start_date, "edate": end_date,
                       "sname": school_name, "sid": school_id, "role": degree, "field": field})
    return result


def parse_connections(connections_resp_json):
    connections = filter(lambda c: c['$type'] == 'com.linkedin.voyager.identity.shared.MiniProfile',
                         connections_resp_json.get('included', []))
    return map(lambda connection: {"fname": connection['firstName'], "lname": connection.get('lastName', ''),
                                   "id": connection['entityUrn'][len('urn:li:fs_miniProfile:'):]}, connections)


def mongodump(user, raw_positions, raw_connections, raw_education, positions, connections, education):
    raw = json.loads(
        json.dumps({"_id": user["id"], "fname": user["fname"], "lname": user["lname"], "pos": raw_positions,
                    "conn": raw_connections, "ed": raw_education}).replace("$", "__").replace(".", "_"))
    raw_pos = {"_id": user['id'], "pos": raw['pos']}
    raw_conn = {"_id": user['id'], "conn": raw['conn']}
    raw_ed = {"_id": user['id'], "ed": raw['ed']}
    processed = {"_id": user["id"], "fname": user["fname"], "lname": user["lname"], "pos": positions,
                 "conn": connections, "ed": education}

    if not db.raw.find_one({"_id": user['id']}):
        # Raw JSON objects can be huge and raise BSON size exception, hence splitting into multiple
        db.raw.insert_one({"_id": user['id'], "fname": user['fname'], "lname": user['lname']})
        db.raw_pos.insert_one(raw_pos)
        raw_conn_len = len(json.dumps(raw_conn))
        if raw_conn_len > MAX_DOC_LENGTH:
            raw_conn['conn'] = "SKIPPED_TOO_BIG"
        db.raw_conn.insert_one(raw_conn)
        db.raw_ed.insert_one(raw_ed)
    else:
        print '{}: Raw info for user, {}, already exists'.format(str(datetime.datetime.now()), user)

    if not db.graph.find_one({"_id": user['id']}):
        curr_doc_len = len(json.dumps(processed))
        if curr_doc_len > MAX_DOC_LENGTH:
            pieces = math.ceil(curr_doc_len / MAX_DOC_LENGTH)
            piece_size = int(math.ceil(connections / pieces))
            processed.pop("conn", None)
            chunk_start = 0
            chunk_index = 0
            while chunk_index < pieces:
                processed["_id"] = "part{}_{}".format(chunk_index, user['id'])
                processed['conn'] = connections[chunk_start: chunk_start + piece_size]
                db.graph.insert_one(processed)
                chunk_start += piece_size
                chunk_index += 1
        else:
            db.graph.insert_one(processed)
    else:
        print '{}: Raw info for user, {}, already exists'.format(str(datetime.datetime.now()), user)


def bfs():
    page_size = 100
    positions_url_template = "{}/{}/positions?count={}&start={}"
    education_url_template = "{}/{}/educations?count={}&start={}"
    connections_url_template = "{}/{}/memberConnections?count={}&q=connections&start={}"
    user_id, fname, lname, depth = ("ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w", "Alekhya", "Cheruvu", 0)
    q, visited = restore_state([(user_id, fname, lname, depth)], set([]))
    try:
        while len(q) > 0:
            user_id, fname, lname, depth = q.pop()
            if depth > max_depth:
                continue
            positions, positions_json_resp = fetch_all_positions(page_size, positions_url_template, user_id)
            connections, connections_json_resp = fetch_all_connections(connections_url_template, page_size, user_id)
            education, education_json_resp = fetch_all_education(page_size, education_url_template, user_id)
            for connection in connections:
                if connection['id'] not in visited:
                    q.append((connection['id'], connection["fname"], connection["lname"], depth + 1))
            user = {"id": user_id, "fname": fname, "lname": lname}
            mongodump(user, positions_json_resp, connections_json_resp, education_json_resp, positions, connections,
                      education)
            visited.add(user_id)
            if len(visited) % 10 == 0:
                print '{}: Completed parsing {} at depth, {}. Parsed {} connections. {} more to go'.format(
                    str(datetime.datetime.now()), user_id, depth, len(visited), len(q))
            sleep(0.3)
        # BFS complete. Save the state as we did not complete the entire graph
        with open(state_persist_file, 'w') as f:
            f.write(json.dumps({"q": q, "visited": list(visited)}))
    except:
        traceback.print_exc(file=sys.stdout)
        # Add this user back to Q as we did not process him / her yet
        q.insert(0, (user_id, fname, lname, depth))
        # Save Q and Visited lists to a file
        with open(state_persist_file, 'w') as f:
            f.write(json.dumps({"q": q, "visited": list(visited)}))
        raise


def restore_state(default_q, default_visited):
    """
    Restore state of BFS viz. values of Q and visited lists
    :param default_q: value of q if no state found
    :param default_visited: value of q if no state found
    :return: Q and visited lists
    """
    try:
        with open(state_persist_file, 'r') as f:
            inp = f.readline()
        if len(inp) > 0:
            parsed_inp = json.loads(inp)
            q = parsed_inp['q']
            if len(q) == 0:
                q = default_q
            visited = set(parsed_inp['visited'])
            if len(visited) == 0:
                visited = default_visited
            return q, visited
        return default_q, default_visited
    except IOError:
        return default_q, default_visited


def fetch_all_connections(connections_url_template, page_size, user):
    connections = []
    connections_jsons = []
    offset = 0
    while True:
        connections_url = connections_url_template.format(url_prefix, user, page_size, offset)
        connections_json_resp = requests.get(connections_url, headers=headers).json()
        new_connections = parse_connections(connections_json_resp)
        if len(new_connections) == 0:
            return connections, connections_jsons
        connections += new_connections
        connections_jsons.append(connections_json_resp)
        offset += page_size
        sleep(0.3)
        # return connections, connections_jsons


def fetch_all_positions(page_size, positions_url_template, user):
    positions = []
    positions_jsons = []
    offset = 0
    while True:
        positions_url = positions_url_template.format(url_prefix, user, page_size, offset)
        positions_json_resp = requests.get(positions_url, headers=headers).json()
        new_positions = parse_positions(positions_json_resp, user)
        if len(new_positions) == 0:
            return positions, positions_jsons
        positions += new_positions
        positions_jsons.append(positions_json_resp)
        offset += page_size
        sleep(0.3)


def fetch_all_education(page_size, education_url_template, user):
    education = []
    education_jsons = []
    offset = 0
    while True:
        education_url = education_url_template.format(url_prefix, user, page_size, offset)
        education_json_resp = requests.get(education_url, headers=headers).json()
        new_education = parse_education(education_json_resp, user)
        if len(new_education) == 0:
            return education, education_jsons
        education += new_education
        education_jsons.append(education_json_resp)
        offset += page_size
        sleep(0.3)


def main():
    print '{}: Started BFS'.format(str(datetime.datetime.now()))
    bfs()
    print '{}: Completed BFS'.format(str(datetime.datetime.now()))


if __name__ == '__main__':
    main()
