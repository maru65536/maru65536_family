import json
import os

import MySQLdb
from flask import Flask,url_for,render_template,request

app=Flask(__name__)

connection = MySQLdb.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    passwd=os.environ['DB_PASS'],
    db='family')
cursor = connection.cursor()

def user_infomation():
    sql="select id,rating,is_using,is_hidden,atcoder_id,rate_hidden from family"
    cursor.execute(sql)
    tmp=list(cursor.fetchall())
    for i in range(len(tmp)):
        tmp[i]=list(tmp[i])
        if tmp[i][5]:
            tmp[i][1]=-1
        tmp[i].pop()
    tmp.sort(key=lambda x:-x[1])
    return tmp

def i_u_count():
    sql="select main_id from family where is_using=1"
    cursor.execute(sql)
    tmp=cursor.fetchall()
    ID_count=len(tmp)
    user_count=len(set(tmp))
    return ID_count,user_count

def hensati(score):
    sql="select main_id,rating from family where is_using=1"
    cursor.execute(sql)
    d={}
    for main_id,rating in cursor.fetchall():
        if rating==-1:
            rating+=1
        d[main_id]=rating
    li=d.values()
    average=sum(li)/len(li)
    SD=(sum([(i-average)**2 for i in li])/len(li))**0.5
    SS=10*((score-average)/SD)+50
    return SS

@app.route('/')
def index():
    ID_count,user_count=i_u_count()
    return render_template('index.html',data=user_infomation(),ID_count=ID_count,user_count=user_count,show=False)

@app.route('/users/<ID>')
def user_page(ID):
    tmp="@"+ID
    sql="select rating,is_hidden from family where id='{}'".format(tmp)
    cursor.execute(sql)
    try:
        rating,hidden=list(cursor.fetchall())[0]
    except:
        return "404だよ(ごめんね)"
    SS=str(hensati(rating))[:4]
    return render_template('users.html',ID=ID,rating=rating,hidden=hidden,hensati=SS)

@app.route('/youbo',methods=["POST"])
def youbo():
    print(request.form["youbo"])
    return 'ありがとうございました!後ろ向きに検討します<br><a href="https://marufamily.tk/">戻る</a>'

@app.route('/<secret>')
def debug(secret):
    if secret!=os.environ['DB_PASS']:
        return "カス"
    ID_count,user_count=users()
    return render_template('index.html',data=user_infomation(),ID_count=ID_count,user_count=user_count,show=True)

@app.route('/favicon.ico')
def favcon():
    return url_for('static',filename='favicon.ico')

@app.route('/test.css')
def css():
    return url_for('static',filename='test.css')

@app.route("/.well-known/acme-challenge/GHBq1txa4FEQa4R5il7fZPzNfX4BmGh_moPxgqu_phU")
def acme_challenge():
    return "GHBq1txa4FEQa4R5il7fZPzNfX4BmGh_moPxgqu_phU.Y-hG_7ZXJzsPTHH49htN8Grz-v9kSawKbjXhXFs48fU"

if __name__=='__main__':
    #import ssl
    #ssl_context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    #ssl_context.load_cert_chain('fullchain.pem','privkey.pem')
    app.run(host="0.0.0.0",port=80)#port=443,ssl_context=ssl_context

