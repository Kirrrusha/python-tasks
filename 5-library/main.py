import sys

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

# Проверяем наличие обязательного параметра action
if len(sys.argv) < 2:
    print("Ошибка: необходимо указать действие (filter или sort)")
    sys.exit(1)

action = sys.argv[1]

if action == "filter":
    # Проверяем наличие обязательного параметра для фильтрации
    if len(sys.argv) < 3:
        print("Ошибка: для действия 'filter' необходимо указать автора")
        sys.exit(1)
    
    author_to_filter = sys.argv[2]
    
    # Фильтруем книги по автору
    filtered_books = filter(lambda item: item[1] == author_to_filter, books.items())
    
    # Преобразуем результат в список строк "Книга — Автор"
    result = list(map(lambda item: f"{item[0]} — {item[1]}", filtered_books))
    
    # Выводим результат
    if result:
        print(f"Книги автора '{author_to_filter}':")
        for book in result:
            print(f"  {book}")
    else:
        print(f"Книги автора '{author_to_filter}' не найдены")

elif action == "sort":
    # Проверяем наличие параметра сортировки
    if len(sys.argv) < 3:
        print("Ошибка: для действия 'sort' необходимо указать 'author' или 'book'")
        sys.exit(1)
    
    sort_by = sys.argv[2]
    
    # Преобразуем словарь в список строк "Книга — Автор"
    books_list = list(map(lambda item: f"{item[0]} — {item[1]}", books.items()))
    
    # Сортируем в зависимости от параметра
    if sort_by == "author":
        # Сортируем по автору (второй элемент после разделения)
        books_list.sort(key=lambda x: x.split(" — ")[1])
        print("Книги, отсортированные по автору:")
    elif sort_by == "book":
        # Сортируем по названию книги (первый элемент)
        books_list.sort(key=lambda x: x.split(" — ")[0])
        print("Книги, отсортированные по названию:")
    else:
        print("Ошибка: неверный параметр сортировки. Используйте 'author' или 'book'")
        sys.exit(1)
    
    # Выводим результат
    for book in books_list:
        print(f"  {book}")

else:
    print(f"Ошибка: неизвестное действие '{action}'. Используйте 'filter' или 'sort'")
    sys.exit(1)