import fuzzysearch


class Compound(object):
    def __init__(self, name, rt_value=None):
        self.name = name
        self.rt_value = rt_value

    @staticmethod
    def from_string(data, sep=","):
        split = data.split(sep)
        return Compound(split[0], float(split[1]))

    def __str__(self):
        return f"{self.name}<{self.rt_value}>"


def exact_match(c1: Compound, c2: Compound, tolerance):
    match_tolerance = False
    if c1.rt_value is not None and c2.rt_value is not None:
        match_tolerance = True if tolerance is None else abs(c1.rt_value - c2.rt_value) < tolerance

    return c1.name == c2.name, match_tolerance


def fuzzy_match(c1: Compound, c2: Compound, tolerance):
    match_tolerance = False
    if c1.rt_value is not None and c2.rt_value is not None:
        match_tolerance = True if tolerance is None else abs(c1.rt_value - c2.rt_value) < tolerance

    matches = fuzzysearch.find_near_matches(c1.name, c2.name, max_l_dist=1)

    return len(matches) > 0, match_tolerance


class Match(object):
    def __init__(self, lhs: Compound, rhs: Compound, tolerance):
        self.lhs = lhs
        self.rhs = rhs
        self.is_exact, self.is_within_tolerance = exact_match(lhs, rhs, tolerance)

    @staticmethod
    def make(c1: Compound, c2: Compound, use_fuzzy_search, tolerance):
        matcher = fuzzy_match if use_fuzzy_search else exact_match
        is_matching, _ = matcher(c1, c2, tolerance)
        if is_matching:
            return Match(c1, c2, tolerance)
        else:
            return None
