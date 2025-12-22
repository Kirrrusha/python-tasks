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
                    return None
    
    # Проверка корректности копеек
    if kop_amount >= 100:
        # Если копеек больше 100, добавляем рубли
        rub_amount += kop_amount // 100
        kop_amount = kop_amount % 100
    
    if rub_amount is None:
        return None
    
    # Возвращаем числовое значение
    return float(f"{rub_amount}.{kop_amount:02d}")

def add_expense(expenses, value):
    """Добавляет расход в список"""
    expenses.append(value)
    return expenses

def delete_expense(expenses, index):
    """Удаляет расход по индексу"""
    if 0 <= index < len(expenses):
        deleted_value = expenses.pop(index)
        return True, deleted_value
    return False, None

def get_total(expenses):
    """Возвращает общую сумму расходов"""
    return sum(expenses)

def get_average(expenses):
    """Возвращает средний расход"""
    if not expenses:
        return 0
    return sum(expenses) / len(expenses)

def print_report(expenses):
    """Печатает красивый отчёт"""
    print("\n" + "="*50)
    print("ОТЧЁТ ПО РАСХОДАМ".center(50))
    print("="*50)
    
    if not expenses:
        print("Нет данных о расходах".center(50))
    else:
        print(f"{'№':<5} {'Сумма, ₽':<15}")
        print("-" * 50)
        
        total = 0
        for i, expense in enumerate(expenses, 1):
            print(f"{i:<5} {expense:>15.2f}")
            total += expense
        
        print("-" * 50)
        print(f"{'ИТОГО:':<20} {total:>15.2f} ₽")
        print(f"{'СРЕДНИЙ РАСХОД:':<20} {get_average(expenses):>15.2f} ₽")
    
    print("="*50)

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
    
    while True:
        display_menu()
        
        try:
            choice = input("Выберите пункт меню (1-5): ").strip()
            
            if choice == "1":
                # Добавить расход
                print("\n--- Добавление расхода ---")
                amount_input = input("Введите сумму (например: '100 руб 50 коп'): ").strip()
                
                amount = parse_sum(amount_input)
                if amount is None:
                    print("Ошибка: некорректный формат суммы")
                else:
                    add_expense(expenses, amount)
                    print(f"✓ Расход успешно добавлен: {amount:.2f} ₽")
                    
            elif choice == "2":
                # Показать все расходы
                print("\n--- Все расходы ---")
                if not expenses:
                    print("Список расходов пуст")
                else:
                    for i, expense in enumerate(expenses, 1):
                        print(f"№{i}: {expense:.2f} ₽")
                        
            elif choice == "3":
                # Показать сумму и средний расход
                print("\n--- Сумма и средний расход ---")
                if not expenses:
                    print("Нет данных для расчета")
                else:
                    total = get_total(expenses)
                    average = get_average(expenses)
                    print(f"Всего расходов: {len(expenses)}")
                    print(f"Общая сумма: {total:.2f} ₽")
                    print(f"Средний расход: {average:.2f} ₽")
                    
            elif choice == "4":
                # Удалить расход по номеру
                print("\n--- Удаление расхода ---")
                if not expenses:
                    print("Список расходов пуст")
                else:
                    print("Текущие расходы:")
                    for i, expense in enumerate(expenses, 1):
                        print(f"№{i}: {expense:.2f} ₽")
                    
                    try:
                        expense_num = int(input("\nВведите номер расхода для удаления: ").strip())
                        # Конвертируем номер в индекс (нумерация с 1)
                        index = expense_num - 1
                        success, deleted_value = delete_expense(expenses, index)
                        
                        if success:
                            print(f"✓ Расход №{expense_num} ({deleted_value:.2f} ₽) удален")
                        else:
                            print(f"Ошибка: расход с номером {expense_num} не найден")
                            
                    except ValueError:
                        print("Ошибка: введите корректный номер расхода")
                        
            elif choice == "5":
                # Показать финальный отчёт и выйти
                print_report(expenses)
                print("\nВыход из программы. До свидания!")
                break
                
            else:
                print("Ошибка: выберите пункт от 1 до 5")
                
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()