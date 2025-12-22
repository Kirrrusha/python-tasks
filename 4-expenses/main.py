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
    return f"{rub_amount}.{kop_amount:02d} ₽"

# Чтение ввода
text_input = input()
result = parse_sum(text_input)
print(result)