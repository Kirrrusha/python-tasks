# errors.py (или внутри main.py)

class LibraryError(Exception):
    """Базовый класс для всех ошибок библиотеки."""
    pass


class MissingFilterError(LibraryError):
    """Ошибка: не передан текст фильтра."""
    def __init__(self, message="Filter text is missing"):
        self.message = message
        super().__init__(self.message)


class InvalidCommandError(LibraryError):
    """Ошибка: передана некорректная команда."""
    def __init__(self, command, message=None):
        self.command = command
        self.message = message or f"Invalid command: '{command}'"
        super().__init__(self.message)


class InvalidSortParamError(LibraryError):
    """Ошибка: передан некорректный параметр сортировки."""
    def __init__(self, sort_param, allowed=None, message=None):
        self.sort_param = sort_param
        allowed_str = f" (allowed: {', '.join(allowed)})" if allowed else ""
        self.message = message or f"Invalid sort parameter: '{sort_param}'{allowed_str}"
        super().__init__(self.message)