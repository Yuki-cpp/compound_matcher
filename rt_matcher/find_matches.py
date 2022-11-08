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
from fuzzysearch import find_near_matches


def _parse_args():

    parser = argparse.ArgumentParser(
        prog="rt-matching",
        description="Find matches between two list of conpounds (Peak and Metabolites) based on their name and RT values. Each list is given as a CSV file with each entry formatted as follows: 'entry name' , 'entry RT value'",
        epilog="Plz Gib Moni",
    )

    optional = parser._action_groups.pop()
    required = parser.add_argument_group("required arguments")

    required.add_argument(
        "-F",
        "--features",
        help="CSV input file for the list of features",
        type=argparse.FileType("r"),
        required=True,
    )
    required.add_argument(
        "-L",
        "--library",
        help="CSV input file for the compound library",
        type=argparse.FileType("r"),
        required=True,
    )

    optional.add_argument(
        "-t",
        "--tolerance",
        help="RT tolerance threshold (default 0.5). Two counpounds will be considered a match if their name is a match and if the difference between their RT values is within the given tolerance",
        type=float,
        default=0.5,
    )

    optional.add_argument(
        "--use-fuzzy-matching",
        action="store_true",
        help="Enables fuzzy matching. When fuzzy matching is enabled, similarity between counpound names uses Levenshtein Distance instead of requiring an exact match",
    )

    optional.add_argument(
        "-i",
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


def _print_matches(matches):
    for match in matches:
        qualifier = "FUZZY" if match["fuzzy"] else "EXACT"
        k1 = match["k1"]
        v1 = match["v1"]
        k2 = match["k2"]
        v2 = match["v2"]

        print(f"{qualifier} match found: {k1} (RT {v1}) -- {k2} (RT {v2})")


def _save_matches(matches, out):
    for match in matches:
        qualifier = "FUZZY" if match["fuzzy"] else "EXACT"
        k1 = match["k1"]
        v1 = match["v1"]
        k2 = match["k2"]
        v2 = match["v2"]

        out.write(f"{k1}, {v1}, {k2}, {v2}, {qualifier}\n")

    print(f"{len(matches)} entries written...")


def main():

    args = _parse_args()

    peak = {}
    for line in args.peak.readlines():
        split = line.split(",")
        peak[split[0]] = float(split[1])

    metabolites = {}
    for line in args.metabolites.readlines():
        split = line.split(",")
        metabolites[split[0]] = float(split[1])

    def fuzzy_match(k1, k2):
        is_potential_match = len(find_near_matches(k1, k2, max_l_dist=1)) > 0

        if args.interactive and is_potential_match and k1 != k2:
            answer = input(f"Is {k1} // {k2} a valid match? [Y/n]")
            if answer.upper() in ["Y", "YES"]:
                return True
            elif answer.upper() in ["N", "NO"]:
                return False

        return is_potential_match

    def exact_match(k1, k2):
        return k1 == k2

    matcher = fuzzy_match if args.use_fuzzy_matching else exact_match

    matches = []
    for key, value in peak.items():
        for key2, value2 in metabolites.items():
            if abs(value2 - value) < args.tolerance and matcher(key, key2):
                matches.append(
                    {"k1": key, "k2": key2, "v1": value, "v2": value2, "fuzzy": key != key2}
                )

    if args.output:
        _save_matches(matches, args.output)
    else:
        _print_matches(matches)


if __name__ == "__main__":
    main()
