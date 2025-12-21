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

price = get_valid_float("Введите цену товара")
discount = get_valid_float("Введите процент скидки на товар")

print(f"Стоимость вашего товара {price * (discount / 100)}")