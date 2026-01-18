def limit_args(max_value, mode="error"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Обрабатываем позиционные аргументы
            new_args = []
            for arg in args:
                if isinstance(arg, (int, float)):
                    if arg > max_value:
                        if mode == "error":
                            raise ValueError(f"Argument {arg} exceeds maximum allowed value {max_value}")
                        elif mode == "clip":
                            arg = max_value
                new_args.append(arg)
            
            # Обрабатываем именованные аргументы
            new_kwargs = {}
            for key, value in kwargs.items():
                if isinstance(value, (int, float)):
                    if value > max_value:
                        if mode == "error":
                            raise ValueError(f"Argument {key}={value} exceeds maximum allowed value {max_value}")
                        elif mode == "clip":
                            value = max_value
                new_kwargs[key] = value

            return func(*new_args, **new_kwargs)
        return wrapper
    return decorator

@limit_args(max_value=10, mode="clip")
def multiply(a, b):
    return a * b

print(multiply(2, 3))     # 6
print(multiply(100, 3))   # 30