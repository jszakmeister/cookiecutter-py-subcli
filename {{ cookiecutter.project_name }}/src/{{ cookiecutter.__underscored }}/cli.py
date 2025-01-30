import argparse
import logging
import sys

from pathlib import Path

from . import __version__ as VERSION


log = logging.getLogger("")


{% if cookiecutter.with_subcommands %}
def add_common_options(parser):
    parser.add_argument(
        "--debug",
        help="Turn on verbose logging.",
        default=False,
        action="store_true")
    parser.add_argument(
        "--traceback",
        default=False,
        action="store_true",
        help="Print traceback of error.")
    parser.add_argument(
        "--version",
        action="version",
        version=VERSION)


def command_dummy(args):
    print("Temporary dummy command.")

{% else %}
def do_work(args):
    print("do work here")

{% endif %}

def main():
    parser = argparse.ArgumentParser()

    {% if cookiecutter.with_subcommands %}
    add_common_options(parser)
    parser.set_defaults(command=lambda args: parser.print_help())

    subparsers = parser.add_subparsers()

    cmd = subparsers.add_parser(
        "dummy",
        help="Temporary dummy command.")

    add_common_options(cmd)

    cmd.set_defaults(command=command_dummy)
    {% else %}
    parser.add_argument(
        "--debug",
        help="Turn on verbose logging.",
        default=False,
        action="store_true")
    parser.add_argument(
        "--traceback",
        default=False,
        action="store_true",
        help="Print traceback of error.")
    parser.add_argument(
        "--version",
        action="version",
        version=VERSION)
    {% endif %}

    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout,
                        level=logging.DEBUG if args.debug else logging.ERROR,
                        format="%(levelname)s: %(message)s")

    try:
        {% if cookiecutter.with_subcommands %}
        args.command(args)
        {% else %}
        do_work(args)
        {% endif %}
    except KeyboardInterrupt:
        pass
    except Exception as e:
        if args.traceback:
            raise

        print(f"ERROR: {e!s}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
