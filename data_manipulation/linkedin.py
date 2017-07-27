#!/usr/local/bin/python
# -*- coding: utf-8

import requests, json, regex, unicodedata, sys, traceback, datetime
from time import sleep
from pymongo import MongoClient
import pymongo

url_prefix = "https://www.linkedin.com/voyager/api/identity/profiles"
max_depth = 2
headers = {"authority": 'www.linkedin.com',
           "method": 'GET',
           "scheme": 'https',
           "accept": 'application/vnd.linkedin.normalized+json',
           "accept-encoding": 'gzip, deflate, br',
           "accept-language": 'en-US,en;q=0.8,en-GB;q=0.6',
           "cache-control": 'no-cache',
           "cookie": 'bcookie="v=2&02a27746-7a07-4237-867e-5cdd12ce44c4"; bscookie="v=1&20160809041846b3a0f450-69f6-4a08-8cd6-5207af763cb1AQHX9xShptrKu8MD9i9R_YfM1Blkvsoa"; wutan=Ezmyd1qpFeKH/lI6c87PqUyOY+R0H1J1HkAAvFtq+VQ=; visit="v=1&M"; __utma=226841088.1914582579.1470720178.1483334359.1483334359.1; __utmc=226841088; _cb_ls=1; _cb=Cf-NJmCKZwvpCkfSl2; _chartbeat2=.1474917126138.1483334360596.0000000000000001.CUfpN8rvFZ-zPstcDChuH9CMHaAo; ELOQUA=GUID=3657cc531f804115925b87150d0ed8e4; share_setting=PUBLIC; lil-lang=en_US; PLAY_SESSION=598a4b4062ba0b53c42acb9db5928cae9f974378-chsInfo=7ec12aef-454b-4464-8781-15b1a9c3ff53+premium_inmail_search_upsell; SID=c36a17cd-6d1a-4b22-8341-e9ccdc101e1a; VID=V_2017_07_08_06_1314; lihc_auth_en=1499817419; lihc_auth_str=TUeIkEFbqFXwCzxdnT8KTw%2FKYiwPh2a3yOLaKBmxSyAqU0f6%2FQ4yCUvaUSSvoethF4hU6YAKu%2F4CG1jF2R26PSK70gcLJk%2BSRg8QuKq7Ib%2F3%2FykoLrEwHIWkT6SUeNeHq0IncGVUZhX4GfqjXfPR6UEzSnZS5%2BCAjuQOmO0JbTnN6ui8FstTsYZwWni58Q2f9%2BGk8Y8xbIhriPkVudwkgQTJjeXCEWBhx5%2BpUvWQjPrI0gVlgkpGVtFjfg3lXe8%2FXftcAy77W1IXF0toCIAa5KIXucujgZCnA0f8VuWWNozv5mx2Fv%2BLuA%3D%3D; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; lidc="b=OB62:g=341:u=265:i=1501035696:t=1501122096:s=AQHFZl1ehAUSW2l1AYdaFLrIUvVL3ypZ"; li_at=AQEDAQLi8o4B7BgyAAABXSFdeJ8AAAFdgpl2XlYAXoKxpULxOQaRiEAgbZDarsEwN9Xr_MXnK7rRJWjjiODWAG8_1tFTFnGYwYF-tv7GwzRHkjg6C52_nJbNBQnGvjsiYkB9dpQOSZi1l2bR39exvdBe; liap=true; sl="v=1&lx-Te"; JSESSIONID="ajax:5955892876341589979"; lang="v=2&lang=en-us"; _ga=GA1.2.1914582579.1470720178; _gat=1; _lipt=CwEAAAFdgVIDRkAQtIrHsCaAE-JhR_NiYM2okqaKSzSsCOIWIatm2pmnx6BGLPdq-wy462CYkJLVTa78WR-Llz0MSlsGkpOvsjbR-C8iTldZ9godPQCdp0vgREIa_j5gdTp9aTikkjsNQHuKJ-grXXsyHf4_iKYNM8kwEN_Gv2h8Pta1i9m6TXfcrDN32TFTy2d8mHx1KzM-jwwkBYZobWSGC8ihRa5jrvsUe7LABNLqTdKNs5pwIG8ZvGPquZA2PeLYbhp-uXAW9H9u74w2nWfePBAsG8Gbx5_BA_E9vGRfPjh3hhCO_vtG3NS87Nbm2WDq7D1NWpSxtnPdsVIk5cReRLaUZugCC0po0Nm-7cC2jB0tRCtSYXYclgPOsg7l7lDlr0IKBw_rc297rS1IQC35oIdISO9ou4STuaim4JsqENawGWWC1A8MyiGI0mbxoj1CvrCXaJv-pzcslRZFQQK6xEiEcYJ-6lwDWZ1ZgWixgE6IJlwUMx4Ux0pDmIZG3ImneaO2p8IUPx-OmgsupFtQ2IsJZ70A65EdIApKxAIw_BezIm6df-hOzQpaH2TzVm_PN84i3BeCM8ZxCBDxC4cdup2ovGyUBqUAHk3urroP10da-orkCKEa_MygE2O-JlOgoEYH966x-QanKie1O4w_G9cjsOG0B5Hd0HOrBZRXwEsOPI5OFo5NqZ-JWW2n0T1kEbwqrC_Y984wY2VkLr_-ZAUPOgmtiKA',
           "csrf-token": 'ajax:5955892876341589979',
           "dnt": '1',
           "pragma": 'no-cache',
           "referer": 'https://www.linkedin.com/',
           "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
           "x-li-lang": 'en_US',
           "x-li-page-instance": 'urn:li:page:d_flagship3_profile_view_base;cm/DtV3uR1SUd+FZhwhcEA==',
           "x-li-track": '{"clientVersion":"1.0.*","osName":"web","timezoneOffset":-7,"deviceFormFactor":"DESKTOP"}',
           "x-requested-with": 'XMLHttpRequest',
           "x-restli-protocol-version": '2.0.0'}

print pymongo.version
# sys.exit(0)

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
    for position in positions['data']['elements']:
        position_id = regex.findall(r',(\d+)\)$', position)[0]
        relevant_details = filter(lambda detail: detail.get('$id', "").find(position_id) >= 0, positions['included'])
        start_date_obj = find(lambda d: d['$id'].endswith(",timePeriod,startDate"), relevant_details)
        end_date_obj = find(lambda d: d['$id'].endswith(",timePeriod,endDate"), relevant_details)
        # company_meta = find(lambda d: d['$id'].endswith(",company"), relevant_details)
        # company_id = regex.findall(r',(\d+)\),company$', company_meta['$id'])[0]  # Non standard companies will not have this
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


def parse_connections(connections_resp_json):
    connections = filter(lambda c: c['$type'] == 'com.linkedin.voyager.identity.shared.MiniProfile',
                         connections_resp_json.get('included', []))
    return map(lambda connection: {"fname": connection['firstName'], "lname": connection['lastName'],
                                   "id": connection['entityUrn'][len('urn:li:fs_miniProfile:'):]}, connections)


def mongodump(user, raw_positions, raw_connections, positions, connections):
    raw = json.loads(
        json.dumps({"_id": user, "pos": raw_positions, "conn": raw_connections}).replace("$", "__").replace(".", "_"))
    processed = {"_id": user, "pos": positions, "conn": connections}

    if not db.raw.find_one({"_id": user}):
        db.raw.insert_one(raw)
    else:
        print '{}: Raw info for user, {}, already exists'.format(str(datetime.datetime.now()), user)

    if not db.graph.find_one({"_id": user}):
        db.graph.insert_one(processed)
    else:
        print '{}: Raw info for user, {}, already exists'.format(str(datetime.datetime.now()), user)


def bfs():
    page_size = 100
    positions_url_template = "{}/{}/positions?count={}&start={}"
    connections_url_template = "{}/{}/memberConnections?count={}&q=connections&start={}"
    q = [("ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w", 0)]
    visited = set([])
    try:
        while len(q) > 0:
            user, depth = q.pop()
            if depth > max_depth:
                continue
            positions, positions_json_resp = fetch_all_positions(page_size, positions_url_template, user)
            connections, connections_json_resp = fetch_all_connections(connections_url_template, page_size, user)
            for connection in connections:
                if connection['id'] not in visited:
                    q.append((connection['id'], depth + 1))
            mongodump(user, positions_json_resp, connections_json_resp, positions, connections)
            if len(visited) % 100 == 0:
                print '{}: Completed parsing {} at depth, {}. Parsed {} connections. {} more to go'.format(
                    str(datetime.datetime.now()), user, depth, len(visited), len(q))
            visited.add(user)
            sleep(0.3)
    except:
        traceback.print_exc(file=sys.stdout)
        with open("linkedin_parsing_status.txt", 'w') as f:
            f.write(json.dumps(list(visited)))


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


def main():
    print '{}: Started BFS'.format(str(datetime.datetime.now()))
    bfs()
    print '{}: Completed BFS'.format(str(datetime.datetime.now()))


if __name__ == '__main__':
    main()
