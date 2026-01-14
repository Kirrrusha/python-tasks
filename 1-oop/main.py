class BankAccount:
    # Классовый атрибут для подсчета созданных счетов
    _accounts_created = 0
    
    def __init__(self, owner, account_number, balance=0):
        """
        Создание нового банковского счета
        
        Args:
            owner (str): Владелец счета
            account_number (str or int): Номер счета
            balance (float or int): Начальный баланс (по умолчанию 0)
        """
        # Валидация входных данных
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Владелец счета должен быть непустой строкой")
        
        # Проверка баланса
        if balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")
        
        self.owner = owner.strip()
        self.account_number = str(account_number)  # Приводим к строке для единообразия
        self._balance = float(balance)  # Используем float для поддержки дробных сумм
        
        # Увеличиваем счетчик созданных счетов
        BankAccount._accounts_created += 1
    
    def deposit(self, amount):
        """
        Пополнение счета
        
        Args:
            amount (float or int): Сумма для пополнения
            
        Returns:
            float: Новый баланс
        """
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        
        self._balance += amount
        return self._balance
    
    def withdraw(self, amount):
        """
        Снятие денег со счета
        
        Args:
            amount (float or int): Сумма для снятия
            
        Returns:
            float: Новый баланс
            
        Raises:
            ValueError: Если сумма снятия превышает баланс
        """
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        
        if amount > self._balance:
            raise ValueError(f"Недостаточно средств. Баланс: {self._balance:.2f}, запрошено: {amount:.2f}")
        
        self._balance -= amount
        return self._balance
    
    def transfer_to(self, other_account, amount):
        """
        Перевод денег на другой счет
        
        Args:
            other_account (BankAccount): Целевой счет для перевода
            amount (float or int): Сумма перевода
            
        Returns:
            tuple: (Баланс текущего счета, Баланс целевого счета)
            
        Raises:
            TypeError: Если other_account не является экземпляром BankAccount
        """
        if not isinstance(other_account, BankAccount):
            raise TypeError("Целевой счет должен быть экземпляром класса BankAccount")
        
        # Снимаем деньги с текущего счета
        self.withdraw(amount)
        
        # Пополняем целевой счет
        other_account.deposit(amount)
        
        return (self._balance, other_account._balance)
    
    def info(self):
        """
        Краткая информация о счете
        
        Returns:
            str: Строка с информацией о счете
        """
        return f"Счет №{self.account_number}, владелец: {self.owner}, баланс: {self._balance:.2f}"
    
    @property
    def balance(self):
        """Геттер для баланса"""
        return self._balance
    
    @classmethod
    def get_accounts_created(cls):
        """
        Количество созданных счетов
        
        Returns:
            int: Количество созданных счетов
        """
        return cls._accounts_created
    
    def __str__(self):
        """Строковое представление счета"""
        return self.info()
    
    def __repr__(self):
        """Техническое строковое представление"""
        return f"BankAccount(owner='{self.owner}', account_number='{self.account_number}', balance={self._balance:.2f})"


# Демонстрация работы класса
if __name__ == "__main__":
    print("Демонстрация работы класса BankAccount")
    print("=" * 50)
    
    # Счетчики должны быть 0 вначале
    print(f"Создано счетов до создания объектов: {BankAccount.get_accounts_created()}")
    
    # Создание счетов
    print("\n1. Создаем счета:")
    try:
        account1 = BankAccount("Иван Иванов", "40817810099910004312", 1000)
        print(f"   Создан: {account1.info()}")
        
        account2 = BankAccount("Петр Петров", "40817810099910004313", 500)
        print(f"   Создан: {account2.info()}")
        
        account3 = BankAccount("Мария Сидорова", "40817810099910004314")
        print(f"   Создан: {account3.info()} (баланс по умолчанию)")
    except ValueError as e:
        print(f"   Ошибка при создании счета: {e}")
    
    print(f"\n   Всего создано счетов: {BankAccount.get_accounts_created()}")
    
    # Пополнение счета
    print("\n2. Пополнение счета:")
    try:
        new_balance = account1.deposit(500)
        print(f"   {account1.owner} пополнил счет на 500. Новый баланс: {new_balance:.2f}")
    except ValueError as e:
        print(f"   Ошибка при пополнении: {e}")
    
    # Снятие денег
    print("\n3. Снятие денег со счета:")
    try:
        new_balance = account1.withdraw(300)
        print(f"   {account1.owner} снял 300. Новый баланс: {new_balance:.2f}")
    except ValueError as e:
        print(f"   Ошибка при снятии: {e}")
    
    # Попытка снять больше, чем есть
    print("\n4. Попытка снять больше, чем есть на счете:")
    try:
        new_balance = account3.withdraw(100)
        print(f"   {account3.owner} снял 100. Новый баланс: {new_balance:.2f}")
    except ValueError as e:
        print(f"   Ошибка: {e}")
    
    # Перевод денег
    print("\n5. Перевод денег между счетами:")
    print(f"   До перевода:")
    print(f"   - {account1.info()}")
    print(f"   - {account2.info()}")
    
    try:
        balances = account1.transfer_to(account2, 200)
        print(f"   {account1.owner} перевел 200 {account2.owner}")
        print(f"   После перевода:")
        print(f"   - {account1.info()}")
        print(f"   - {account2.info()}")
    except (ValueError, TypeError) as e:
        print(f"   Ошибка при переводе: {e}")
    
    # Перевод с неверным типом счета
    print("\n6. Попытка перевода на не-BankAccount объект:")
    try:
        account1.transfer_to("не счет", 100)
    except TypeError as e:
        print(f"   Ошибка: {e}")
    
    # Использование геттера balance
    print("\n7. Использование геттера balance:")
    print(f"   Баланс {account1.owner}: {account1.balance:.2f}")
    
    # Использование __str__ и __repr__
    print("\n8. Строковые представления:")
    print(f"   str(account1): {account1}")
    print(f"   repr(account1): {repr(account1)}")
    
    # Создание счета с отрицательным балансом
    print("\n9. Попытка создать счет с отрицательным балансом:")
    try:
        bad_account = BankAccount("Ошибка", "12345", -100)
        print(f"   Создан: {bad_account}")
    except ValueError as e:
        print(f"   Ошибка: {e}")
    
    # Создание счета с пустым именем
    print("\n10. Попытка создать счет с пустым именем:")
    try:
        bad_account = BankAccount("", "12345", 100)
        print(f"   Создан: {bad_account}")
    except ValueError as e:
        print(f"   Ошибка: {e}")
    
    print(f"\nИтоговое количество созданных счетов: {BankAccount.get_accounts_created()}")