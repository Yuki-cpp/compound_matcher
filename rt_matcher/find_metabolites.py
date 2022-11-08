#!/usr/bin/env python3

# Copyright 2022 Leo Ghafari
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import argparse
import fuzzysearch


def _parse_args():

    parser = argparse.ArgumentParser(
        prog="rt-matching",
        description="Find molecules in the inventory",
        epilog="Plz Gib Moar Moni",
    )

    optional = parser._action_groups.pop()
    required = parser.add_argument_group("required arguments")

    required.add_argument(
        "-m",
        "--molecules",
        help="CSV input file for the list of molecules",
        type=argparse.FileType("r"),
        required=True,
    )
    required.add_argument(
        "-I",
        "--inventory",
        help="CSV input file for the inventory",
        type=argparse.FileType("r"),
        required=True,
    )

    optional.add_argument(
        "--use-fuzzy-matching",
        action="store_true",
        help="Enables fuzzy matching. When fuzzy matching is enabled, similarity between counpound names uses Levenshtein Distance instead of requiring an exact match",
    )

    parser.add_argument(
        "-o",
        "--output",
        action="store",
        type=argparse.FileType("w"),
        dest="output",
        help="output file to store matches in. If not provided, the matches will only be displayed.",
    )

    parser._action_groups.append(optional)

    return parser.parse_args()


def _print_matches(matches):
    for match in matches:
        qualifier = "FUZZY" if not match.is_exact else "EXACT"
        print(f"{qualifier} match found: {match.lhs}) -- {match.rhs}")


def _save_matches(matches, out):
    for match in matches:
        fuzzy_qualifier = "EXACT" if match.is_exact else "FUZZY"
        tolerance_qualifier = (
            "WITHIN_TOLERANCE" if match.is_within_tolerance else "OUTSIDE_OF_TOLERANCE"
        )
        out.write(
            f"{match.lhs.name}, {match.lhs.rt_value}, {match.rhs.name}, {match.rhs.rt_value}, {fuzzy_qualifier}, {tolerance_qualifier}\n"
        )


def main():

    args = _parse_args()

    molecules = [s.strip() for s in args.molecules.readlines()]
    inventory = []

    for line in args.inventory.readlines():
        split = line.split(",")
        inventory.append((split[0], split[1].strip()))
        print((split[0], split[1].strip()))

    for m in molecules:
        found = False

        for m2, loc in inventory:
            if len(fuzzysearch.find_near_matches(m, m2, max_l_dist=1)) > 0:
                if not found:
                    print(f"{m} can be found in:")
                    found = True
                print(f"\t-{loc}  (as {m2})")

        if not found:
            print(f"{m} can not be found")


if __name__ == "__main__":
    main()
