import datetime
from math import ceil

from flask import Blueprint
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask import abort


from libs.orm import db
from libs.utils import login_required
from weibo.models import Weibo


weibo_bp = Blueprint('weibo', __name__, url_prefix='/weibo')
weibo_bp.template_folder = './templates'


@weibo_bp.route('/index')
def index():
    '''微博首页'''
    page = int(request.args.get('page', 1))
    per_page = 30
    offset = per_page * (page - 1)
    wb_list = Weibo.query.order_by(Weibo.updated.desc()).limit(per_page).offset(offset)

    max_page = ceil(Weibo.query.count() / per_page)  # 最大页码

    if max_page > 7:
        if page <= 3:
            start, end = 1, 7  # 起始处的页码范围
        elif page > (max_page - 3):
            start, end = max_page - 6, max_page  # 结尾处的页码范围
        else:
            start, end = (page - 3), (page + 3)
    else:
        start, end = 1, max_page
    pages = range(start, end + 1)
    return render_template('index.html', wb_list=wb_list, pages=pages, page=page, max_page=max_page)


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

        # 检查微博内容是否为空
        if not content:
            return render_template('edit.html', weibo=weibo, err='微博内容不允许为空')

        # 更新微博内容
        weibo.content = content
        weibo.updated = now
        db.session.commit()

        return redirect(f'/weibo/read?wid={wid}')
    else:
        #获取微博，并传到模板中
        weibo = Weibo.query.get(wid)
        return render_template('edit.html', weibo=weibo)


@weibo_bp.route('/delete')
@login_required
def delete_weibo():
    '''删除微博'''
    wid = int(request.args.get('wid'))
    # 检查是否是在删除自己的微博
    weibo = Weibo.query.get(wid)

    if weibo.uid == session['uid']:
        db.session.delete(weibo)
        db.session.commit()
        return redirect('/')
    else:
        abort(403)