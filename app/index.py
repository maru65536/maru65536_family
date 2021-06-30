import os
import MySQLdb
from flask import Flask, url_for, render_template, request, redirect, flash
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.consumer import oauth_authorized
from flask_login import LoginManager, login_user, logout_user, login_required
from app.use_case.auth.find_login_user_usercase import FindLoginUserUseCase
from app.use_case.family.find_family_use_case import FindFamilyUseCase

app=Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
blueprint = make_twitter_blueprint(
    api_key=os.environ["TWITTER_API_KEY"],
    api_secret=os.environ["TWITTER_API_SECRET"],
)
app.register_blueprint(blueprint, url_prefix="/login")

login_manager = LoginManager()
login_manager.init_app(app)

connection = MySQLdb.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    passwd=os.environ['DB_PASS'],
    db=os.environ['DB_NAME'] or 'family')
cursor = connection.cursor()


@login_manager.user_loader
def user_loader(user_id):
    return FindFamilyUseCase(connection).exec(user_id)


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
    cursor.execute("SELECT count(1), count(distinct main_id) FROM family WHERE is_using = 1")
    result = cursor.fetchone()
    
    return result[0], result[1]

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
    content = request.form["youbo"]
    print(content)
    
    cursor.execute(
        "INSERT INTO youbo (IP, content, created_at) VALUES (%s, %s, NOW())",
        (request.remote_addr, content)
    )
    connection.commit()
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


@oauth_authorized.connect
def redirect_to_next_url(blueprint, token):
    blueprint.token = token

    family = FindLoginUserUseCase(connection).exec(int(token["user_id"]), token["screen_name"])
    if family is not None:
        login_user(family)
        flash("ログインしました", "primary")
    else:
        flash("ログインに失敗しました", "danger")

    return redirect("/")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ログアウトしました", "primary")
    return redirect("/")


if __name__=='__main__':
    import ssl
    ssl_context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain('fullchain.pem','privkey.pem')
    app.run(host="0.0.0.0",port=443,ssl_context=ssl_context)
