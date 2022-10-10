from app import db


class User(db.Model):
    __tablename__ = 'users'
    soinik_number = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.String(255))
    name = db.Column(db.String(255))
    company = db.Column(db.String(255))
    password = db.Column(db.String(255))
    total_firing_count = db.Column(db.Integer)
    best_grouping = db.Column(db.String(255))

    def __init__(self, soinik_number, rank, name, company):
        self.soinik_number = soinik_number
        self.rank = rank
        self.name = name
        self.company = company
        self.password = 'admin'
        self.total_firing_count = 0
        self.best_grouping = '0'

    def __repr__(self):
        return '<User %r>' % self.soinik_number


class Record(db.Model):
    __tablename__ = 'records'
    soinik_number = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255), primary_key=True)
    sub_label = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255))
    total_hit = db.Column(db.Integer)
    grouping = db.Column(db.String(255))
    error = db.Column(db.Integer)

    def __init__(self, soinik_number, date, sub_label, file_name):
        self.soinik_number = soinik_number
        self.date = date
        self.sub_label = sub_label
        self.file_name = file_name
        self.total_hit = 0
        self.grouping = ''
        self.error = ''

    def __repr__(self):
        return "<Record (soinik_number='%s', date='%s', sub_label='%s')>" % (
            self.soinik_number,
            self.date,
            self.sub_label,
        )
