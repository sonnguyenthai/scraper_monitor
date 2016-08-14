import urllib, json
import traceback
from datetime import datetime
from urlparse import urljoin

from django.conf import settings

import requests
import pymongo


def json_get(url, path):
    url = urljoin(url, path)
    return json.loads(urllib.urlopen(url).read())

def check_running(url):
    """list-running - list running spiders"""
    try:
        if json_get(url, 'crawler/engine/open_spiders'):
            return 'Running'
        return 'Stop'
    except:
        return 'Stop'

def verify_spider(spider_name, url, project_name):
    result = {"status": "Not Running",
              "code": False,
              "start_time": "None",
              "end_time": "None"
              }
    try:
        response = requests.get(url, params={'project': project_name})
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == "ok":
                for i in data.get("running"):
                    if i['spider'] == spider_name:
                        result['status'] = "Running"
                        result['code'] = True
                        result['start_time'] = i['start_time']
                        result['job_id'] = i['id']
                        # result['end_time'] = i['end_time']
                        return result
                for i in data.get("pending"):
                    if i['spider'] == spider_name:
                        result['status'] = "Pending"
                        result['code'] = False
                        return result
                for i in data.get("finished"):
                    if i['spider'] == spider_name:
                        result['status'] = "Finished"
                        result['code'] = True
                        result['start_time'] = i['start_time']
                        result['end_time'] = i['end_time']
                        return result
    except:
        print traceback.format_exc()
        return result
    return result


def start_spider(spider_name, url, project_name):
    try:
        res = requests.post(url, data={'project': project_name, 'spider': spider_name})
        if res.status_code == 200:
            data = res.json()
            if data['status'] == 'ok':
                return data['jobid']
    except:
        print traceback.format_exc()
    return None


def stop_spider(project_name, url, job_id):
    try:
        res = requests.post(url, data={'project': project_name, 'job': job_id})
        if res.status_code == 200:
            data = res.json()
            if data['status'] == 'ok':
                return True
    except:
        print traceback.format_exc()
    return False



def str_2_time(str):
    """
    Converts time in string with format %Y-%m-%d %H:%M:%S.%f to datetime object
    :param str:
    :return:
    """
    return datetime.strptime(str, "%Y-%m-%d %H:%M:%S.%f")


def get_mongo_stats():
    """
    Returns number of items and number items with images in MongoDB db
    :return: a tuple
    """
    client = pymongo.MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DATABASE]
    col = db[settings.MONGO_POSTCARDS_COLLECTION]
    items_num = col.count()
    images_num = col.count({'$or': [{'front_image':{'$exists': True}}, {'back_image':{'$exists': True}}]})
    return items_num, images_num