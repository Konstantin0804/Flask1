from api import api, app
from api.resources.author import AuthorList, Author
from api.resources.quote import QuoteList, QuotesByAuthors, Quote


api.add_resource(QuoteList, "/quotes") # Все цитаты
api.add_resource(Quote, "/quotes", "/author/<int:author_id>/quotes") # Цитаты с методом post и по id автора
api.add_resource(AuthorList, "/author") # Все авторы с их цитатами
api.add_resource(Author, "/author/<int:id>", "/author") # Тоже вывод цитат по авторам (оставил для себя) и добавление нового автора и редактирвоание текущего
api.add_resource(QuotesByAuthors, "/author/<int:author_id>/quotes/<int:quote_id>") #работа с цитататами по id автора и id цитаты? Метод Put не работает корректно, пока не смог разобраться по какой причине

if __name__ == '__main__':
   app.run(debug=True)
