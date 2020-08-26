from libs.orm import db
from user.models import User


class Weibo(db.Model):
    __tablename__ = 'weibo'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    updated = db.Column(db.DateTime, nullable=False)

    @property
    def author(self):
        '''获取当前微博的作者'''
        user = User.query.get(self.uid)
        return user