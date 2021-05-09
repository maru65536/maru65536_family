import json
import os
import requests
from bs4 import BeautifulSoup
import MySQLdb


def rating_fetch(id):
    try:
        url = "https://atcoder.jp/ranking?f.UserScreenName={}".format(id)
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        rating = soup.find('b').get_text()
        return int(rating)
    except:
        return -1

def update_ratings():
    sql='select atcoder_id from family'
    cursor.execute(sql)
    atcoder_ids=cursor.fetchall()
    for atcoder_id in atcoder_ids:
        atcoder_id=atcoder_id[0]
        rating=rating_fetch(atcoder_id)
        sql='update family set rating={} where atcoder_id="{}"'.format(rating,atcoder_id)
        cursor.execute(sql)

connection = MySQLdb.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    passwd=os.environ['DB_PASS'],
    db='family')

cursor = connection.cursor()
update_ratings()

connection.commit()
connection.close()
