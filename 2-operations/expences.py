def get_valid_float(prompt: str) -> float:
    """Запрашивает у пользователя float до тех пор, пока не будет введено корректное значение."""
    while True:
        user_input = input(prompt)
        
        # Удаляем пробелы по краям
        user_input = user_input.strip()
        
        # Разрешаем запятую в качестве разделителя
        if ',' in user_input:
            user_input = user_input.replace(',', '.')
        
        try:
            number = float(user_input)
            return number
        except ValueError:
            print(f"Ошибка: '{user_input}' не является числом. Попробуйте ещё раз.")

def average_of_three(a: float, b: float, c: float):
    """Получает среднее значение"""
    return (a + b + c) / 3

food = get_valid_float("Введите сколько вы потратили на еду: ")

transport = get_valid_float("Введите сколько вы потратили на транспорт: ")

entertainment = get_valid_float("Введите сколько вы потратили на развлечение: ")

print(f"Привет, твои общие траты {sum([food, transport, entertainment])}, твои средние траты {average_of_three(food, transport, entertainment)}")