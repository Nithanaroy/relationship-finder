import requests, json, regex

url_prefix = "https://www.linkedin.com/voyager/api/identity/profiles"
user = "ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w"
count = 5
offset = 30
positions_url = "{}/{}/positions?count={}&start={}".format(url_prefix, user, count, offset)
connections_url = "{}/{}/memberConnections?count={}&q=connections&start={}".format(url_prefix, user, count, offset)
headers = {"authority": 'www.linkedin.com',
           "method": 'GET',
           "scheme": 'https',
           "accept": 'application/vnd.linkedin.normalized+json',
           "accept-encoding": 'gzip, deflate, br',
           "accept-language": 'en-US,en;q=0.8,en-GB;q=0.6',
           "cache-control": 'no-cache',
           "cookie": 'bcookie="v=2&02a27746-7a07-4237-867e-5cdd12ce44c4"; bscookie="v=1&20160809041846b3a0f450-69f6-4a08-8cd6-5207af763cb1AQHX9xShptrKu8MD9i9R_YfM1Blkvsoa"; wutan=Ezmyd1qpFeKH/lI6c87PqUyOY+R0H1J1HkAAvFtq+VQ=; visit="v=1&M"; __utma=226841088.1914582579.1470720178.1483334359.1483334359.1; __utmc=226841088; _cb_ls=1; _cb=Cf-NJmCKZwvpCkfSl2; _chartbeat2=.1474917126138.1483334360596.0000000000000001.CUfpN8rvFZ-zPstcDChuH9CMHaAo; ELOQUA=GUID=3657cc531f804115925b87150d0ed8e4; share_setting=PUBLIC; lil-lang=en_US; PLAY_SESSION=598a4b4062ba0b53c42acb9db5928cae9f974378-chsInfo=7ec12aef-454b-4464-8781-15b1a9c3ff53+premium_inmail_search_upsell; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; SID=c36a17cd-6d1a-4b22-8341-e9ccdc101e1a; VID=V_2017_07_08_06_1314; li_at=AQEDAQLi8o4B7BgyAAABXSFdeJ8AAAFdNVNIw1YABpj2ZPUidzSvnyJ6vWnLt5lyzaw3OTvbDc1YGwP_9Wplo-8j0A5Mqh5pPUhyGoGcKnF-KANsQap-CP1yYDvwDvtYYbJSR_mciGeRKu0612pGWO-Q; liap=true; sl="v=1&cFAVF"; JSESSIONID="ajax:5955892876341589979"; _gat=1; _ga=GA1.2.1914582579.1470720178; lidc="b=OB62:g=325:u=255:i=1499817405:t=1499870178:s=AQGePlyrdoGIvWTvJ3AljH8U3n5fGXTI"; lihc_auth_en=1499817419; lihc_auth_str=TUeIkEFbqFXwCzxdnT8KTw%2FKYiwPh2a3yOLaKBmxSyAqU0f6%2FQ4yCUvaUSSvoethF4hU6YAKu%2F4CG1jF2R26PSK70gcLJk%2BSRg8QuKq7Ib%2F3%2FykoLrEwHIWkT6SUeNeHq0IncGVUZhX4GfqjXfPR6UEzSnZS5%2BCAjuQOmO0JbTnN6ui8FstTsYZwWni58Q2f9%2BGk8Y8xbIhriPkVudwkgQTJjeXCEWBhx5%2BpUvWQjPrI0gVlgkpGVtFjfg3lXe8%2FXftcAy77W1IXF0toCIAa5KIXucujgZCnA0f8VuWWNozv5mx2Fv%2BLuA%3D%3D; lang=v=2&lang=en-US; RT=s=1499817454226&r=https%3A%2F%2Fdeveloper.linkedin.com%2Fdocs%2Fapply-with-linkedin; _lipt=CwEAAAFdNBh_nhWcL6EkYQ4SZL1MdsXURO_CWuQlyAQ1quBouWbrurnWzkG4xpkYivl_G8YOKUTaMYX217OMY6uTeP0XleXInpx2JCGUaRKdDe7R2aEg6f1uupnjnpQzTrFB2MfYjnJ0QXi18SvOxH0SqrGce1Z1FKeTu4bWhkI3VW_BeAt7KmFb3McTh-ddkHW-lyNBvCi71uLB5LptxXg1L6RBdu0ol7-ta7IeLfkU7igltmM2RPXij46HBjXLhyKYc8fVUagXXD8ophfQ7Dl6KNL5BoYqewAg2eagJYjzf1RWoFHBSOT0hntGeGrtF8sMMY8KE539Yc-rGWvdrzl6MT02tPrxHTWh0E2mTAX3H_LA7X9jyCJW9ammbxmfuNX9bPjkiyd3Yv8Ol66JXCh3qSqY0VTaP_gxh5SiyeFyxzWMUxIRR44GI8NeGiuoR16ov98WJuFTZHnNmp5Ub_uNxEqteWeLKAKOBKRRbYfvMv8p8wY-MZswJZiwsEehZqITay8CL7TSdFMFivk1n4hQ6Thu_jW4z78IKKcFjgFUgb8CMhM20-3nVXBFNOex7smkLP-ZN2MvIkBHYvBHw__nxCvfdgKd8JKWiXWtDM3zypIfi0kILDaB4ziA3UGX8rxTzuDf0garsEnM9HMBgKhQnTS8eRQHPhGjiQyF9f7uWQcPNylzRY-fDZXo_fvVDSz4SymruN8DhWoEPGzDKKfWPowE',
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
# r = requests.get(positions_url, headers=headers)
# print r

positions_response_str = r'{"data":{"elements":["urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692889)","urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692971)","urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731694535)"],"paging":{"total":8,"count":5,"start":5,"links":[]}},"included":[{"$deletedFields":["day"],"month":6,"year":2013,"$type":"com.linkedin.common.Date","$id":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692971),timePeriod,startDate"},{"$deletedFields":["day"],"month":7,"year":2015,"$type":"com.linkedin.common.Date","$id":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692889),timePeriod,endDate"},{"$deletedFields":["day"],"month":12,"year":2013,"$type":"com.linkedin.common.Date","$id":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692971),timePeriod,endDate"},{"$deletedFields":["day"],"month":6,"year":2012,"$type":"com.linkedin.common.Date","$id":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731694535),timePeriod,startDate"},{"$deletedFields":["day"],"month":7,"year":2012,"$type":"com.linkedin.common.Date","$id":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731694535),timePeriod,endDate"},{"$deletedFields":["day"],"month":7,"year":2014,"$type":"com.linkedin.common.Date","$id":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692889),timePeriod,startDate"},{"$deletedFields":[],"endDate":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692971),timePeriod,endDate","startDate":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692971),timePeriod,startDate","$type":"com.linkedin.voyager.common.DateRange","$id":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692971),timePeriod"},{"$deletedFields":[],"endDate":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692889),timePeriod,endDate","startDate":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692889),timePeriod,startDate","$type":"com.linkedin.voyager.common.DateRange","$id":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692889),timePeriod"},{"$deletedFields":[],"endDate":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731694535),timePeriod,endDate","startDate":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731694535),timePeriod,startDate","$type":"com.linkedin.voyager.common.DateRange","$id":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731694535),timePeriod"},{"$deletedFields":["attribution"],"id":"/AAEAAQAAAAAAAAgDAAAAJGEyMmQ5NWI3LWYxYjEtNGU0Ny1iYjllLTI5Mzk5NDljZTk1ZA.png","$type":"com.linkedin.voyager.common.MediaProcessorImage","$id":"urn:li:fs_miniCompany:3338050,logo,com.linkedin.voyager.common.MediaProcessorImage"},{"$deletedFields":["attribution"],"id":"/AAEAAQAAAAAAAAoJAAAAJGZlMTQ1NjY2LTVjMWMtNDYxMC1hMTNmLWZkMTkyMDM3N2JjOQ.png","$type":"com.linkedin.voyager.common.MediaProcessorImage","$id":"urn:li:fs_miniCompany:3725643,logo,com.linkedin.voyager.common.MediaProcessorImage"},{"$deletedFields":[],"objectUrn":"urn:li:company:3338050","entityUrn":"urn:li:fs_miniCompany:3338050","name":"Netskope","showcase":false,"active":true,"logo":{"com.linkedin.voyager.common.MediaProcessorImage":"urn:li:fs_miniCompany:3338050,logo,com.linkedin.voyager.common.MediaProcessorImage"},"trackingId":"DfJXAtkjTrOzoLsJw2G9Qw==","$type":"com.linkedin.voyager.entities.shared.MiniCompany"},{"$deletedFields":["logo"],"objectUrn":"urn:li:company:1005244","entityUrn":"urn:li:fs_miniCompany:1005244","name":"INDIAN OVERSEAS BANK","showcase":false,"active":true,"trackingId":"5TX96duSSFyUkIuuiUzDqw==","$type":"com.linkedin.voyager.entities.shared.MiniCompany"},{"$deletedFields":[],"objectUrn":"urn:li:company:3725643","entityUrn":"urn:li:fs_miniCompany:3725643","name":"Oracle India Pvt. Ltd","showcase":false,"active":true,"logo":{"com.linkedin.voyager.common.MediaProcessorImage":"urn:li:fs_miniCompany:3725643,logo,com.linkedin.voyager.common.MediaProcessorImage"},"trackingId":"LmlaE8hqQJW4WNNYVGIDDQ==","$type":"com.linkedin.voyager.entities.shared.MiniCompany"},{"$deletedFields":[],"start":201,"end":500,"$type":"com.linkedin.voyager.identity.profile.EmployeeCountRange","$id":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692971),company,employeeCountRange"},{"$deletedFields":["end"],"start":10001,"$type":"com.linkedin.voyager.identity.profile.EmployeeCountRange","$id":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731694535),company,employeeCountRange"},{"$deletedFields":["end"],"start":10001,"$type":"com.linkedin.voyager.identity.profile.EmployeeCountRange","$id":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692889),company,employeeCountRange"},{"$deletedFields":["courses","projects","honors","entityLocale","organizations"],"locationName":"Chennai Area, India","entityUrn":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731694535)","companyName":"INDIAN OVERSEAS BANK","timePeriod":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731694535),timePeriod","description":"Developed Complaint register form using Microsoft Visual Studio and SQL database ","company":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731694535),company","title":"Full time Intern","region":"urn:li:fs_region:(in,6891)","companyUrn":"urn:li:fs_miniCompany:1005244","recommendations":[],"$type":"com.linkedin.voyager.identity.profile.Position"},{"$deletedFields":["courses","projects","honors","entityLocale","organizations"],"locationName":"Bengaluru Area, India","entityUrn":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692889)","companyName":"Oracle India Pvt. Ltd","timePeriod":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692889),timePeriod","description":"Worked for Server Technologies Department under Database Team\nDeveloped network benchmark tool using NetStress tool and PL/SQL statements for Inter-process communication on TCP-IP and UDP protocols for packet transfer, size ranging from 2GB to 32GB on Real Application Cluster having four nodes\n Worked with Intel Debug Registers to Improve performance of hardware watch points of Oracle RDBMS feature\nDeveloped Version Control program which updates all latest versions of DLL files when new version files are released\nDeveloped scripting tool using shell script to analyze CFS and NIFS performance on 50GB file\n ","company":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692889),company","title":"Member of Technical Staff","region":"urn:li:fs_region:(in,5281)","companyUrn":"urn:li:fs_miniCompany:3725643","recommendations":[],"$type":"com.linkedin.voyager.identity.profile.Position"},{"locationName":"Bengaluru Area, India","projects":["urn:li:fs_project:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,1861604649)"],"companyName":"Netskope","description":"Cloud Security Research on Cloud Storage Applications\nAnalyzed HTTP,HTPPS network protocols using temper-data add-on on Firefox browser for various SAAS, PAAS and IAAS Cloud Applications\nDeveloped connector tool using XML language to notify about user actions done on cloud applications\nAnalyzed data packets consisting MIME,JSON,GWT,TEXT,BASE 64 encoded techniques using wireshark tool and developed python add-ons to parse the connector tool with database","title":"Full time Intern","companyUrn":"urn:li:fs_miniCompany:3338050","recommendations":[],"$type":"com.linkedin.voyager.identity.profile.Position","$deletedFields":["courses","honors","entityLocale","organizations"],"entityUrn":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692971)","timePeriod":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692971),timePeriod","company":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692971),company","region":"urn:li:fs_region:(in,5281)"},{"employeeCountRange":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692971),company,employeeCountRange","$deletedFields":[],"miniCompany":"urn:li:fs_miniCompany:3338050","industries":["Computer Software"],"$type":"com.linkedin.voyager.identity.profile.PositionCompany","$id":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692971),company"},{"employeeCountRange":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692889),company,employeeCountRange","$deletedFields":[],"miniCompany":"urn:li:fs_miniCompany:3725643","industries":["Information Technology and Services"],"$type":"com.linkedin.voyager.identity.profile.PositionCompany","$id":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731692889),company"},{"employeeCountRange":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731694535),company,employeeCountRange","$deletedFields":[],"miniCompany":"urn:li:fs_miniCompany:1005244","industries":["Banking"],"$type":"com.linkedin.voyager.identity.profile.PositionCompany","$id":"urn:li:fs_position:(ACoAAAc0XbsB4tM8YmZfw0KUp8abP9hn5HlHI_w,731694535),company"}]}'
positions = json.loads(positions_response_str, encoding='utf-8')

for position in positions['data']['elements']:
    position_id = regex.findall(r',(\d+)\)$', position)[0]
    relevant_details = filter(lambda detail: detail.get('$id', "").find(position_id) >= 0, positions['included'])
    start_date_obj = filter(lambda d: d['$id'].endswith(",timePeriod,startDate"), relevant_details)[0]
    end_date_obj = filter(lambda d: d['$id'].endswith(",timePeriod,endDate"), relevant_details)[0]
    company_meta = filter(lambda d: d['$id'].endswith(",company"), relevant_details)[0]
    company_id = regex.findall(r',(\d+)\),company$', company_meta['$id'])[0]
    company_obj = filter(lambda detail: detail.get('company', "").find(company_id) >= 0, positions['included'])[0]
    start_date = "{}-{}".format(start_date_obj['year'], start_date_obj['month'])
    end_date = "{}-{}".format(end_date_obj['year'], end_date_obj['month'])
    company = company_obj['companyName']
    print start_date, end_date, company
