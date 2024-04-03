import sys
from .cli import run


def main():
    # noinspection PyBroadException
    try:
        run(sys.argv[1:])
    except Exception:
        raise
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
