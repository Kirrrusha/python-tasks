# main.py

import sys
from typing import Optional, List
from errors import (
    LibraryError,
    MissingFilterError,
    InvalidCommandError,
    InvalidSortParamError,
)

# Допустим, у нас есть функция-обработчик аргументов командной строки
def parse_args(args: List[str]) -> dict:
    """
    Пример: python main.py --command list --filter "author=Pushkin" --sort title
    """
    opts = {}
    i = 1
    while i < len(args):
        if args[i].startswith("--"):
            key = args[i][2:]
            if i + 1 >= len(args) or args[i+1].startswith("--"):
                # Значение не передано
                opts[key] = None
            else:
                opts[key] = args[i+1]
                i += 1
        i += 1
    return opts


def validate_input(opts: dict):
    command = opts.get("command")
    if not command:
        raise InvalidCommandError("<none>")
    if command not in {"list", "search", "add", "remove"}:
        raise InvalidCommandError(command)

    if command in {"search", "list"}:
        filter_text = opts.get("filter")
        if not filter_text:
            raise MissingFilterError()

    sort_param = opts.get("sort")
    if sort_param:
        allowed_sorts = {"title", "author", "year"}
        if sort_param not in allowed_sorts:
            raise InvalidSortParamError(sort_param, allowed=allowed_sorts)


def main():
    try:
        opts = parse_args(sys.argv)
        validate_input(opts)
        print("✅ Input validated successfully:", opts)

        # Здесь могла бы быть логика выполнения команды
        # Например: execute_command(opts)

    except MissingFilterError as e:
        print(f"❌ MissingFilterError: {e}", file=sys.stderr)

    except InvalidCommandError as e:
        print(f"❌ InvalidCommandError: {e}", file=sys.stderr)

    except InvalidSortParamError as e:
        print(f"❌ InvalidSortParamError: {e}", file=sys.stderr)

    except Exception as e:
        print(f"💥 Unexpected error: {type(e).__name__}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()