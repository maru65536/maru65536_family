import json
import os

import MySQLdb
from flask import Flask,url_for,render_template,request

app=Flask(__name__)

connection = MySQLdb.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    passwd=os.environ['DB_PASS'],
    db=os.environ['DB_NAME'] or 'family')
cursor = connection.cursor()

def user_infomation():
    sql="select id,rating,is_using,is_hidden,atcoder_id,rate_hidden,comment,birthday from family"
    cursor.execute(sql)
    tmp=list(cursor.fetchall())
    for i in range(len(tmp)):
        tmp[i]=list(tmp[i])
        if tmp[i][7]!=None:
            tmp[i][7]='{}/{}'.format(int(tmp[i][7][:2]),int(tmp[i][7][2:]))
        else:
            tmp[i][7]=''
        if tmp[i][5]:
            tmp[i][1]=-1
        tmp[i].pop(5)
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
    sql="select main_id,rating,is_using from family where is_using=1"
    cursor.execute(sql)
    d={}
    for main_id,rating,is_using in cursor.fetchall():
        if not is_using:
            continue
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

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/users/<id_>')
def user_page(id_):
    import re
    id_match = re.fullmatch(r'@?(\w{1,15})', id_)
    if id_match is None:
        if '\'' in id_ or '#' in id_ or ';' in id_:
            return '400 Bad Request(SQLインジェクションはできないよ)', 400
        return '400 Bad Request', 400
    id_str = f'@{id_match.group(1)}'
    cursor.execute("SELECT `rating`, `is_hidden` FROM `family` where `id`=%s", (id_str,))
    data = cursor.fetchone()
    if data is None:
        return '404だよ(ごめんね)', 404
    rating, hidden = data
    ss = str(hensati(rating))[:4]
    return render_template('users.html', ID=id_, rating=rating, hidden=hidden, hensati=ss)

@app.route('/youbo',methods=["POST"])
def youbo():
    print(request.form["youbo"])
    return 'ありがとうございました!後ろ向きに検討します<br><a href="/">戻る</a>'

@app.route('/<secret>')
def debug(secret):
    if secret!=os.environ['DB_PASS']:
        return "カス"
    ID_count,user_count=i_u_count()
    return render_template('index.html',data=user_infomation(),ID_count=ID_count,user_count=user_count,show=True)

@app.route('/favicon.ico')
def favcon():
    return url_for('static',filename='favicon.ico')

@app.route('/test.css')
def css():
    return url_for('static',filename='test.css')

@app.route("/.well-known/acme-challenge/oXoh_xzxlf1RBvOhDi8LKOmUZ421IXLEYb0XnFqFCCY")
def acme_challenge():
    return "oXoh_xzxlf1RBvOhDi8LKOmUZ421IXLEYb0XnFqFCCY.Y-hG_7ZXJzsPTHH49htN8Grz-v9kSawKbjXhXFs48fU"

if __name__=='__main__':
    import ssl
    ssl_context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain('fullchain.pem','privkey.pem')
    app.run(host="0.0.0.0",port=443,ssl_context=ssl_context)
