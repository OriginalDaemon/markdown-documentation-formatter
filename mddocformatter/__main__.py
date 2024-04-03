import sys
from .cli import run


def main():
    sys.exit(0 if run(sys.argv[1:]) else 1)


if __name__ == "__main__":
    main()
