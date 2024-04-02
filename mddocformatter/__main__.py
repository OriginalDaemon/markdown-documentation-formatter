import sys  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    from .scripts.cli import main
    sys.exit(0 if main(sys.argv[1:]) else 1)
