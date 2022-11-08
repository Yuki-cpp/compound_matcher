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
import rt_matcher.compound as rt


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
        "--name-only",
        action="store_true",
        help="Only perform matching on compounds names.",
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

    print(f"{len(matches)} entries written...")


def main():

    args = _parse_args()

    features = []
    for line in args.features.readlines():
        features.append(rt.Compound.from_string(line))

    library = []
    for line in args.library.readlines():
        library.append(rt.Compound.from_string(line))

    matches = []
    for feature_compound in features:
        for library_compound in library:
            match = rt.Match.make(
                feature_compound, library_compound, args.use_fuzzy_matching, args.tolerance
            )
            if match is not None:

                if args.interactive and not match.is_exact:
                    answer = input(f"Is {match.lhs.name} // {match.rhs.name} a valid match? [Y/n]")
                    if answer.upper() in ["Y", "YES"]:
                        pass
                    elif answer.upper() in ["N", "NO"]:
                        continue

                if args.name_only or match.is_within_tolerance:
                    matches.append(match)

    if args.output:
        _save_matches(matches, args.output)
    else:
        _print_matches(matches)


if __name__ == "__main__":
    main()
