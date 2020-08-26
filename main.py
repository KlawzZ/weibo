from flask import Flask
from flask import redirect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from libs.orm import db
from user.views import user_bp
from weibo.views import weibo_bp

# 初始化 app
app = Flask(__name__)
app.secret_key = r'sodifjwoehoHOHH23OSHO234@234Ohsoepfho1@#i009()90U#$%DFPOIJASO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Klaw:z4226089q@localhost:3306/weibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 每次请求结束后都会自动提交数据库中的变动

# 初始化 manager
manager = Manager(app)

# 初始化 db 和 migrate
db.init_app(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(weibo_bp)


@app.route('/')
def home():
    '''首页'''
    return redirect('/weibo/index')


if __name__ == "__main__":
    manager.run()
