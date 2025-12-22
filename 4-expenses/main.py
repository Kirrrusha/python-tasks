import re

def parse_sum(text):
    # Приводим к нижнему регистру и убираем лишние пробелы
    text = text.lower().strip()
    
    # Определяем словари для единиц измерения
    rub_words = ["руб", "рублей", "рубль"]
    kop_words = ["коп", "копеек", "копейка", "копейки"]
    
    # Ищем рублевую часть
    rub_amount = None
    kop_amount = 0
    
    # Паттерн для поиска чисел с десятичными разделителями
    # Сначала ищем формат "XXX руб YYY коп"
    pattern1 = r'(\d+)\s*(?:' + '|'.join(rub_words) + r')\s*(\d+)\s*(?:' + '|'.join(kop_words) + r')'
    match1 = re.search(pattern1, text)
    
    if match1:
        rub_amount = int(match1.group(1))
        kop_amount = int(match1.group(2))
    else:
        # Если не нашли, пробуем формат "XXX руб"
        pattern2 = r'(\d+)\s*(?:' + '|'.join(rub_words) + r')'
        match2 = re.search(pattern2, text)
        
        if match2:
            rub_amount = int(match2.group(1))
        else:
            # Если не нашли рубли, пробуем найти только копейки
            pattern3 = r'(\d+)\s*(?:' + '|'.join(kop_words) + r')'
            match3 = re.search(pattern3, text)
            
            if match3:
                # Если только копейки, переводим их в рубли
                total_kop = int(match3.group(1))
                rub_amount = total_kop // 100
                kop_amount = total_kop % 100
            else:
                # Пробуем найти просто число (без указания единиц)
                numbers = re.findall(r'\d+', text)
                if len(numbers) == 1:
                    # Одно число - трактуем как рубли
                    rub_amount = int(numbers[0])
                elif len(numbers) == 2:
                    # Два числа - первое рубли, второе копейки
                    rub_amount = int(numbers[0])
                    kop_amount = int(numbers[1])
                else:
                    return "Некорректный формат суммы"
    
    # Проверка корректности копеек
    if kop_amount >= 100:
        # Если копеек больше 100, добавляем рубли
        rub_amount += kop_amount // 100
        kop_amount = kop_amount % 100
    
    if rub_amount is None:
        return "Некорректный формат суммы"
    
    # Форматируем результат
    return f"{rub_amount}.{kop_amount:02d}"

def display_menu():
    """Отображает меню управления расходами"""
    print("\n" + "="*40)
    print("МЕНЮ УПРАВЛЕНИЯ РАСХОДАМИ")
    print("="*40)
    print("1. Добавить расход")
    print("2. Показать все расходы")
    print("3. Показать сумму и средний расход")
    print("4. Удалить расход по номеру")
    print("5. Выход")
    print("="*40)

def main():
    expenses = []  # Список для хранения расходов
    next_id = 1    # Счетчик для нумерации расходов
    
    while True:
        display_menu()
        
        try:
            choice = input("Выберите пункт меню (1-5): ").strip()
            
            if choice == "1":
                # Добавить расход
                print("\n--- Добавление расхода ---")
                description = input("Введите описание расхода: ").strip()
                amount_input = input("Введите сумму (например: '100 руб 50 коп'): ").strip()
                
                amount = parse_sum(amount_input)
                if "Некорректный" in amount:
                    print(f"Ошибка: {amount}")
                else:
                    expense = {
                        'id': next_id,
                        'description': description,
                        'amount': amount + " ₽",
                        'amount_value': float(amount)  # сохраняем числовое значение для расчетов
                    }
                    expenses.append(expense)
                    print(f"✓ Расход №{next_id} успешно добавлен: {description} - {amount} ₽")
                    next_id += 1
                    
            elif choice == "2":
                # Показать все расходы
                print("\n--- Все расходы ---")
                if not expenses:
                    print("Список расходов пуст")
                else:
                    for expense in expenses:
                        print(f"№{expense['id']}: {expense['description']} - {expense['amount']}")
                        
            elif choice == "3":
                # Показать сумму и средний расход
                print("\n--- Сумма и средний расход ---")
                if not expenses:
                    print("Нет данных для расчета")
                else:
                    total = sum(expense['amount_value'] for expense in expenses)
                    average = total / len(expenses)
                    print(f"Всего расходов: {len(expenses)}")
                    print(f"Общая сумма: {total:.2f} ₽")
                    print(f"Средний расход: {average:.2f} ₽")
                    
            elif choice == "4":
                # Удалить расход по номеру
                print("\n--- Удаление расхода ---")
                if not expenses:
                    print("Список расходов пуст")
                else:
                    # Показываем текущие расходы
                    print("Текущие расходы:")
                    for expense in expenses:
                        print(f"№{expense['id']}: {expense['description']} - {expense['amount']}")
                    
                    try:
                        expense_id = int(input("\nВведите номер расхода для удаления: ").strip())
                        # Ищем расход по ID
                        found = False
                        for i, expense in enumerate(expenses):
                            if expense['id'] == expense_id:
                                del expenses[i]
                                print(f"✓ Расход №{expense_id} удален")
                                found = True
                                break
                        
                        if not found:
                            print(f"Расход с номером {expense_id} не найден")
                            
                    except ValueError:
                        print("Ошибка: введите корректный номер расхода")
                        
            elif choice == "5":
                # Выход
                print("\nВыход из программы. До свидания!")
                break
                
            else:
                print("Ошибка: выберите пункт от 1 до 5")
                
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()