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
        prog="metabolites-finder",
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

    optional.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive fuzzy maching. When set, all fuzzy matches will require the user confirmation to be outputed",
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


def main():

    args = _parse_args()

    molecules = [s.strip() for s in args.molecules.readlines()]
    inventory = []

    for line in args.inventory.readlines():
        split = line.split(",")
        inventory.append((split[0].strip(), split[1].strip()))

    if args.output:
        args.output.write("molecule, location, matching name\n")

    for m in molecules:
        found = False

        for m2, loc in inventory:

            is_matching = (
                m == m2
                if not args.use_fuzzy_matching
                else len(fuzzysearch.find_near_matches(m, m2, max_l_dist=1)) > 0
            )
            if is_matching:

                if args.interactive and is_matching and m != m2:
                    answer = input(f"Is {m} // {m2} a valid match? [Y/n]")
                    if answer.upper() in ["Y", "YES"]:
                        pass
                    elif answer.upper() in ["N", "NO"]:
                        continue

                if not found and not args.output:
                    print(f"{m} can be found in:")
                    found = True

                if not args.output:
                    print(f"\t-{loc}  (as {m2})")

                if args.output:
                    args.output.write(f"{m}, {loc}, {m2}\n")

        if not found and not args.output:
            print(f"{m} can not be found")


if __name__ == "__main__":
    main()
