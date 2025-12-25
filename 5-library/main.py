# Создаем словарь books
books = {}

# Добавляем книги
books["Преступление и наказание"] = "Фёдор Достоевский"
books["Идиот"] = "Фёдор Достоевский"
books["Война и мир"] = "Лев Толстой"
books["Анна Каренина"] = "Лев Толстой"
books["Мастер и Маргарита"] = "Михаил Булгаков"
books["1984"] = "Джордж Оруэлл"
books["Скотный двор"] = "Джордж Оруэлл"

# Выводим список всех книг
print("=" * 50)
print("СПИСОК ВСЕХ КНИГ:")
print("=" * 50)
for i, book in enumerate(books.keys(), 1):
    print(f"{i:2}. {book}")
print()

# Выводим список всех уникальных авторов
unique_authors = set(books.values())
print("=" * 50)
print("СПИСОК УНИКАЛЬНЫХ АВТОРОВ:")
print("=" * 50)
for i, author in enumerate(sorted(unique_authors), 1):
    print(f"{i:2}. {author}")
print()

# Дополнительно: показываем книги каждого автора
print("=" * 50)
print("КНИГИ ПО АВТОРАМ:")
print("=" * 50)

# Создаем обратный словарь: автор -> список книг
authors_books = {}
for book, author in books.items():
    if author not in authors_books:
        authors_books[author] = []
    authors_books[author].append(book)

# Выводим результат
for author in sorted(authors_books.keys()):
    print(f"\n{author}:")
    for book in sorted(authors_books[author]):
        print(f"  • {book}")