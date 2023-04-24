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
from lib.helpers import err_print

if sys.version_info < (3, 7):
    err_print("RFuzz requires python 3.7 or higher")
    sys.exit(1)


def main():
    pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        err_print("Caught KeyboardInterrupt, exiting.")
        pass