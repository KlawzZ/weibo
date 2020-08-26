import datetime

from flask import Blueprint
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask import abort


from libs.orm import db
from libs.utils import login_required
from weibo.models import Weibo
from user.models import User

weibo_bp = Blueprint('weibo', __name__, url_prefix='/weibo')
weibo_bp.template_folder = './templates'


@weibo_bp.route('/index')
def index():
    '''微博首页'''
    weibos = Weibo.query.order_by(Weibo.created.desc()).all()
    return render_template('index.html', weibos=weibos)


@weibo_bp.route('/post', methods=("POST", "GET"))
@login_required
def post_weibo():
    '''发布微博'''
    if request.method == "POST":
        uid = session['uid']
        content = request.form.get('content', '').strip()
        now = datetime.datetime.now()

        #检查微博内容是否为空
        if not content:
            return render_template('post.html', err='微博内容不允许为空')

        weibo = Weibo(uid=uid, content=content, created=now, updated=now)
        db.session.add(weibo)
        db.session.commit()
        return redirect('/weibo/read?wid=%s' % weibo.id)
    else:
        return render_template('post.html')


@weibo_bp.route('/read')
def read_weibo():
    '''阅读微博'''
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)
    # user = User.query.get(weibo.uid)  # 获取微博作者
    return render_template('read.html', weibo=weibo)


@weibo_bp.route('/edit', methods=("POST", "GET"))
@login_required
def edit_weibo():
    '''修改微博'''

    #检查是否是在修改自己的微博
    wid = int(request.form.get('wid', 0)) or int(request.args.get('wid', 0))
    weibo = Weibo.query.get(wid)
    if weibo.uid != session['uid']:
       abort(403)

    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        now = datetime.datetime.now()



    else:
        #获取微博，并传到模板中
        weibo = Weibo.query.get(wid)
        return render_template('edit.html', weibo=weibo)


@weibo_bp.route('/delete')
@login_required
def delete_weibo():
    '''删除微博'''
    wid = int(request.args.get('wid'))
    Weibo.query.filter_by(id=wid).delete()
    db.session.commit()
    return redirect('/weibo/index')
