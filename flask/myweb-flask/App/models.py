from .exts import db


class User(db.Model):
    __tablename__ = 'web_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    identity = db.Column(db.String(50))
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))
    access_token = db.Column(db.String(400), unique=True)
    resources = db.relationship('Resource', backref='user', lazy=True)

    def __repr__(self):
        return str([self.id, self.identity,self.username, self.password, self.access_token])


class Resource(db.Model):
    __tablename__ = 'web_res'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    res_name = db.Column(db.String(50), unique=True)
    res_id = db.Column(db.Integer, db.ForeignKey(User.id))

class PartInventory(db.Model):
    __tablename__='part_inventory'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    配件编号 = db.Column(db.String(50))
    配件名 = db.Column(db.String(50))
    可用库存 = db.Column(db.Integer)
    待检库存 = db.Column(db.Integer)
    供应商 = db.Column(db.String(50))
    库存上限 = db.Column(db.String(50))
    库存下限 = db.Column(db.String(50))
    时间 = db.Column(db.Date)


