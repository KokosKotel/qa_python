import pytest
from main import BooksCollector


class TestBooksCollector:

    #Проверяем добавление одной книги с разными названиями
    @pytest.mark.parametrize('book_name, result', [
        ('Марсианин', True),
        ('', False),
        ('Очень длинное название книги, которое точно больше сорока символов', False)
    ])
    def test_add_new_book_with_different_names(self, book_name, result):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert (book_name in collector.get_books_genre()) == result

    #Проверяем добавление разного жанра книг
    @pytest.mark.parametrize('book_name, genre, result', [
        ('Автостопом по галактике', 'Фантастика', True),
        ('Несуществующая книга', 'Ужасы', False),
        ('50 оттенков серого', 'Романтика', False)
    ])
    def test_set_book_genre_with_different_genre(self, book_name, genre, result):
        collector = BooksCollector()
        if result:
            collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)

        if result:
            assert collector.get_book_genre(book_name) == genre
        else:
            assert collector.get_book_genre(book_name) != genre

    #Проверяем получение списка книг по выбранному жанру
    def test_get_books_with_specific_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Доктор Кто')
        collector.set_book_genre('Доктор Кто', 'Фантастика')
        collector.add_new_book('Ходячие мертвецы')
        collector.set_book_genre('Ходячие мертвецы', 'Фантастика')
        collector.add_new_book('Детективное агенство Дирка Джентли')
        collector.set_book_genre('Детективное агенство Дирка Джентли', 'Детектив')
        fantasy = collector.get_books_with_specific_genre('Фантастика')
        assert 'Доктор Кто' in fantasy
        assert 'Ходячие мертвецы' in fantasy
        assert 'Детективное агенство Дирка Джентли' not in fantasy
        assert len(fantasy) == 2

    #Проверяем получение списка книг для детей
    def test_get_books_for_children(self):
        collector = BooksCollector()
        collector.add_new_book('Метро 2033')
        collector.set_book_genre('Метро 2033', 'Фантастика')
        collector.add_new_book('Откровение людоеда')
        collector.set_book_genre('Откровение людоеда', 'Детектив')
        children = collector.get_books_for_children()
        assert 'Метро 2033' in children
        assert 'Откровение людоеда' not in children
        assert len(children) == 1

    #Проверяем добавление книг в Избранное
    def test_add_book_to_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Pytest Тестирование')
        collector.add_book_in_favorites('Pytest Тестирование')
        assert 'Pytest Тестирование' in collector.get_list_of_favorites_books()

    #Проверяем добавление уже добавленной книги в Избранное
    def test_add_already_favorited_book(self):
        collector = BooksCollector()
        collector.add_new_book('Pytest')
        collector.add_book_in_favorites('Pytest')
        initial_favorites = collector.get_list_of_favorites_books()
        collector.add_book_in_favorites('Pytest')
        updated_favorites = collector.get_list_of_favorites_books()
        assert initial_favorites == updated_favorites

    #Проверяем удаление книги из Избранного
    def test_remove_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Основы тестирования')
        collector.add_book_in_favorites('Основы тестирования')
        collector.delete_book_from_favorites('Основы тестирования')
        updated_favorites = collector.get_list_of_favorites_books()
        assert 'Основы тестирования' not in updated_favorites

    #Проверяем удаление книги не добавленной в Избранное
    def test_remove_non_favorited_book(self):
        collector = BooksCollector()
        initial_favorites = collector.get_list_of_favorites_books()
        collector.delete_book_from_favorites('Кровь, пот и пиксели')
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
