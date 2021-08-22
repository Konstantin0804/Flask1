from api import db


class AuthorModel(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(32), unique=True)
   surname = db.Column(db.String(32), unique=True)
   middlename = db.Column(db.String(32), default="Unknown")
   quotes = db.relationship('QuoteModel', backref='author', lazy='joined')

   def __init__(self, name, surname):
       self.name = name
       self.surname = surname

   def to_dict(self):
        # value = "name"
        # getattr(self, value) --> self.name
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))
        quotes = self.quotes
        d["quotes"] = [quote.to_dict() for quote in quotes]
        return d