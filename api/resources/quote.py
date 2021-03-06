from flask_restful import Resource, reqparse
from api.models.quote import QuoteModel
from api.models.author import AuthorModel
from api import db
from operator import itemgetter, attrgetter, methodcaller

class QuoteResource(Resource):
    def get(self, author_id):
        quotes = QuoteModel.query.filter_by(author_id=author_id).all()
        if quotes:
            quotes = [quote.to_dict() for quote in quotes]
            return quotes, 200
        return {"message": f"quote with author_id={author_id} not found"}, 404

    def post(self, author_id):
        parser = reqparse.RequestParser()
        parser.add_argument("quote")
        quote_data = parser.parse_args()
        author = AuthorModel.query.get(author_id)
        quote = QuoteModel(author, quote_data["quote"])
        db.session.add(quote)
        db.session.commit()
        return quote.to_dict(), 201

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("quote")
        parser.add_argument("rate")
        data = parser.parse_args()
        quote = QuoteModel.query.get(id)
        if quote:
            quote.author = data["author"] or quote.author
            quote.quote = data["quote"] or quote.quote
            quote.rate = data["rate"] or quote.rate
            db.session.commit()
            return quote.to_dict(), 200
        else:
            new_quote = QuoteModel(**data)
            db.session.add(new_quote)
            db.session.commit()
            return quote.to_dict(), 200

    def delete(self, id):
        quote = QuoteModel.query.get(id)
        if quote:
            db.session.delete(quote)
            db.session.commit()
            return quote.to_dict, 200
        return "Not found", 404


class QuoteListResource(Resource):
    def get(self):
        quotes = QuoteModel.query.all()
        quotes = [quote.to_dict() for quote in quotes]
        return quotes, 200


class QuoteListSortedIdResource(Resource):
    def get(self):
        quotes = QuoteModel.query.all()
        quotes = [quote.to_dict() for quote in quotes]
        quotes = sorted(quotes, key=itemgetter('id'))
        return quotes, 200

class QuoteListSortedAuthorNameResource(Resource):
    def get(self):
        quotes = AuthorModel.query.all()
        quotes = [quote.to_dict() for quote in quotes]
        quotes = sorted(quotes, key=itemgetter('name'))
        return quotes, 200

class QuotesByAuthorsResource(Resource):
    def get(self, author_id, quote_id):
        quote = QuoteModel.query.filter_by(author_id=author_id).filter_by(id=quote_id).all()
        print(quote)
        if quote:
            quote = [quote.to_dict() for quote in quote]
            return quote, 200
        return {"message": f"quote with author_id={author_id} and quote_id={quote_id} not found"}, 404

    def put(self, author_id, quote_id):
        parser = reqparse.RequestParser()
        parser.add_argument("quote")
        parser.add_argument("rate")
        data = parser.parse_args()
        quote = QuoteModel.query.get(quote_id)
        if quote and quote.author_id != author_id:
            return f"author {author_id} don't have quote {quote_id}", 400
        if quote:
            quote.quote = data["quote"] or quote.quote
            quote.rate = data["rate"] or quote.rate
            db.session.commit()
            return quote.to_dict(), 200

        new_quote = QuoteModel(**data)
        db.session.add(new_quote)
        db.session.commit()
        quote = [quote.to_dict() for quote in quote]
        return quote, 200

    def delete(self, author_id, quote_id):
        quote = QuoteModel.query.filter_by(author_id=author_id).filter_by(id=quote_id).all()
        print(quote)
        if quote:
            for i in quote:
                db.session.delete(i)
            db.session.commit()
            quote = [quote.to_dict() for quote in quote]
            return quote, 200
        return {"message": f"quote with author_id={author_id} and quote_id={quote_id} not found"}, 404