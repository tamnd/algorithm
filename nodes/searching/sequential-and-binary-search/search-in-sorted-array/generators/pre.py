"""The precondition of the search problem: a is sorted in non-decreasing order. The shrinker keeps only inputs that meet it."""


def pre(args):
    a = args["a"]
    for i in range(1, len(a)):
        if a[i - 1] > a[i]:
            return "a is not sorted at index %d" % i
    return None
