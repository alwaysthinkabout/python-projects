from app import db


class Current_Qf(db.Model):
    __tablename__ = 'current_qf_tmp'
    id = db.Column(db.Integer, primary_key=True)
    yhbh = db.Column(db.String(60))
    yhmc = db.Column(db.String(60))
    yddz = db.Column(db.String(60))
    dfny = db.Column(db.String(60))
    qf = db.Column(db.Float(2))
    yswyj = db.Column(db.Float(2))
    wyjrq = db.Column(db.String(60))
    fengxianzhi = db.Column(db.Float(2))
    branch_office = db.Column(db.String(60))
