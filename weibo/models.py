import random

from libs.orm import db
from libs.utils import random_zh_str
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

    @classmethod
    def fake_weibos(cls, uid_list, num):
        wb_list = []
        for i in range(num):
            year = random.randint(2010, 2019)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            date = '%04d-%02d-%02d' % (year, month, day)

            uid = random.choice(uid_list)
            content = random_zh_str(random.randint(70, 140))
            wb = cls(uid=uid, content=content, created=date, updated=date)
            wb_list.append(wb)

        db.session.add_all(wb_list)
        db.session.commit()