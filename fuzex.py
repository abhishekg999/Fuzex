#!/usr/bin/env python3
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <https://www.gnu.org/licenses/>.
#
#  Author: Abhishek Govindarasu

import sys
import argparse
from lib.helpers import fprint, err_print

FUZEX_TOO_MANY_WORDS = 100000

if sys.version_info < (3, 7):
    err_print("Fuzex requires python 3.7 or higher")
    sys.exit(1)


def main(args):
    input_cmd = args.cmd
    output_file = args.output
    if args.debug:
        import lib.core
        lib.core.DEBUG = True

    from lib.core.parse import Parser

    parser = Parser(input_cmd)
    expression = parser.parse()

    if args.size:
        print(expression.size())
        sys.exit(0)

    if args.debug:
        err_print("[DEBUG] Expression generated:", expression)
        err_print("[DEBUG] Size of expression:", expression.size())

    if not args.force and expression.size() > FUZEX_TOO_MANY_WORDS:
        err_print(f"The provided expression will generate {expression.size()} lines.")
        err_print("If you still want to run this, use the --force flag.")
        sys.exit(1)

    if args.output == sys.stdout:
        for line in expression.generate():
            sys.stdout.write(line)
            sys.stdout.write("\n")
    else:
        for line in expression.generate():
            fprint(output_file, line)

    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fuzex command line arguments")
    parser.add_argument("-c", "--cmd", help="input command (required)", required=True)
    parser.add_argument(
        "-s",
        "--size",
        help="get the size of the expression",
        action="store_true",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="output file (default: stdout)",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
    )
    parser.add_argument(
        "-f",
        "--force",
        help="Will allow Fuzex to process a large generation of words",
        action="store_true",
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="Enable debug mode",
        action="store_true",
    )

    try:
        args = parser.parse_args()
        main(args)
    except KeyboardInterrupt:
        err_print("exiting...")
        sys.exit(1)
