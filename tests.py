import pytest
from main import BooksCollector


class TestBooksCollector:

    #Проверяем добавление книг с разными названиями
    @pytest.mark.parametrize('book_name, result', [
        ('Марсианин', True),
        ('', False),
        ('Очень длинное название книги, которое точно больше сорока символов', False)
    ])
    def test_add_new_book_with_different_names(self, book_name, result):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert (book_name in collector.get_books_genre()) == result

    #Проверяем добавление жанра книг для существующей книги
    def test_set_genre_for_existing_book(self):
        collector = BooksCollector()
        book_name = 'Автостопом по галактике'
        genre = 'Фантастика'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == genre

    #Проверяем добавление жанра для несуществующей книги
    def test_set_genre_for_nonexistent_book(self):
        collector = BooksCollector()
        book_name = 'Несуществующая книга'
        genre = 'Ужасы'
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) is None

    #Проверяем добавление жанра, которого нет в БД приложения
    def test_set_nonexistent_genre_for_existing_book(self):
        collector = BooksCollector()
        book_name = '50 оттенков серого'
        genre = 'Романтика'
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == ''

    #Проверяем получение списка книг по выбранному жанру
    def test_get_books_with_specific_genre(self):
        collector = BooksCollector()
        book_and_genre = [
            ('Доктор Кто', 'Фантастика'),
            ('Ходячие мертвецы', 'Фантастика'),
            ('Детективное агенство Дирка Джентли', 'Детектив')
        ]
        for book_name, genre in book_and_genre:
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, genre)

        expected_book = ['Доктор Кто', 'Ходячие мертвецы']
        fantasy = collector.get_books_with_specific_genre('Фантастика')
        assert sorted(fantasy) == sorted(expected_book)

    #Проверяем получение списка книг для детей
    def test_get_books_for_children(self):
        collector = BooksCollector()
        book_and_genre = [
            ('Метро 2033', 'Фантастика'),
            ('Откровение людоеда', 'Детектив')
        ]
        for book_name, genre in book_and_genre:
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, genre)

        expected_book = ['Метро 2033']
        children = collector.get_books_for_children()
        assert sorted(children) == sorted(expected_book)

    #Проверяем добавление книг в Избранное
    def test_add_book_to_favorites(self):
        collector = BooksCollector()
        book_name = 'Pytest Тестирование'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.get_list_of_favorites_books()

    #Проверяем добавление уже добавленной книги в Избранное
    def test_add_already_favorited_book(self):
        collector = BooksCollector()
        book_name = 'Pytest'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        initial_favorites = collector.get_list_of_favorites_books()
        collector.add_book_in_favorites(book_name)
        updated_favorites = collector.get_list_of_favorites_books()
        assert initial_favorites == updated_favorites

    #Проверяем удаление книги из Избранного
    def test_remove_book_from_favorites(self):
        collector = BooksCollector()
        book_name = 'Основы тестирования'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        updated_favorites = collector.get_list_of_favorites_books()
        assert book_name not in updated_favorites

    #Проверяем удаление книги не добавленной в Избранное
    def test_remove_non_favorited_book(self):
        collector = BooksCollector()
        book_name = 'Кровь, пот и пиксели'
        initial_favorites = collector.get_list_of_favorites_books()
        collector.delete_book_from_favorites(book_name)
        updated_favorites = collector.get_list_of_favorites_books()
        assert initial_favorites == updated_favorites

    #Проверяем получение списка Избранного
    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        favorites_book = ['Философский камень', 'Тайная комната', 'Узник Азкабана']
        for book in favorites_book:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)

        favorites_list = collector.get_list_of_favorites_books()
        assert len(favorites_list) == len(favorites_book)
