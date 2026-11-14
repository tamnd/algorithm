# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variable-type-analysis/. The authors are listed in prov/5D67PN.jsonl.

import random

import oomodel
from oomodel import MAIN
from variable_type_analysis import components, graph_and_seeds, prune, variable_type_analysis


def plain_vta(prog, initial):
    """The same graph, solved by pushing classes along every edge until
    nothing changes."""
    succ, seed = graph_and_seeds(prog, initial)
    types = {v: set(seed.get(v, ())) for v in succ}
    changed = True
    while changed:
        changed = False
        for v in succ:
            for w in succ[v]:
                if not types[v] <= types[w]:
                    types[w] |= types[v]
                    changed = True
    return prune(prog, initial, types)


def programs(seed, count):
    rng = random.Random(seed)
    for _ in range(count):
        yield rng, oomodel.random_program(rng, rng.randint(2, 7), rng.randint(1, 4), rng.randint(0, 2), 8)


def test_page_example():
    reach, edges = variable_type_analysis(oomodel.shapes())
    circle, square = ("Circle", "grow"), ("Square", "grow")
    assert reach == {MAIN, circle, square}
    assert edges == {("s1", circle), ("s2", square), ("s3", circle), ("s3", square)}


def test_page_example_from_cha_graph():
    prog = oomodel.shapes()
    assert variable_type_analysis(prog, oomodel.cha_spec(prog)) == variable_type_analysis(prog)


def test_class_flows_through_a_field():
    prog = {
        "classes": {"A": None, "B": "A", "H": None},
        "methods": {"m": ("A", "A", "A")},
        "fields": {"f": ("H", "A")},
        "bodies": {
            ("A", "m"): ({"this": "A", "p": "A", "ret": "A"}, []),
            ("B", "m"): ({"this": "B", "p": "A", "ret": "A"}, []),
            MAIN: (
                {"a": "A", "o": "A", "h": "H", "x": "A"},
                [
                    ("new", "a", "B"),
                    ("new", "o", "A"),
                    ("new", "h", "H"),
                    ("store", "h", "f", "a"),
                    ("load", "x", "h", "f"),
                    ("call", "s1", None, "x", "m", None),
                    ("call", "s2", None, "o", "m", None),
                ],
            ),
        },
    }
    reach, edges = variable_type_analysis(prog)
    assert edges == {("s1", ("B", "m")), ("s2", ("A", "m"))}
    assert len(oomodel.rta_spec(prog)[1]) == 4


def test_components_match_mutual_reachability():
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randint(1, 12)
        succ = {v: {w for w in range(n) if rng.random() < 0.15} for v in range(n)}
        comps = components(succ)
        assert sorted(v for c in comps for v in c) == list(range(n))
        reach = {}
        for v in range(n):
            seen, stack = {v}, [v]
            while stack:
                for w in succ[stack.pop()]:
                    if w not in seen:
                        seen.add(w)
                        stack.append(w)
            reach[v] = seen
        where = {v: i for i, c in enumerate(comps) for v in c}
        for v in range(n):
            for w in range(n):
                assert (where[v] == where[w]) == (w in reach[v] and v in reach[w])
                if w in succ[v] and where[v] != where[w]:
                    assert where[w] < where[v]  # sinks come first


def test_same_as_plain_iteration():
    for _, prog in programs(2000, 400):
        initial = oomodel.rta_spec(prog)
        assert variable_type_analysis(prog, initial) == plain_vta(prog, initial), oomodel.show(prog)


def test_sound_against_concrete_runs():
    for rng, prog in programs(79, 300):
        reach, edges = variable_type_analysis(prog)
        for _ in range(5):
            seen_edges, entered = oomodel.run(prog, rng)
            assert seen_edges <= edges, oomodel.show(prog)
            assert entered <= reach


def test_nested_inside_rta_inside_cha():
    smaller = 0
    for _, prog in programs(7, 300):
        cha = oomodel.cha_spec(prog)
        rta = oomodel.rta_spec(prog)
        vta = variable_type_analysis(prog, rta)
        assert vta[0] <= rta[0] <= cha[0]
        assert vta[1] <= rta[1] <= cha[1]
        smaller += vta[1] != rta[1]
    assert smaller > 0


def test_monotone_in_the_initial_graph():
    for _, prog in programs(8, 300):
        from_rta = variable_type_analysis(prog, oomodel.rta_spec(prog))
        from_cha = variable_type_analysis(prog, oomodel.cha_spec(prog))
        assert from_rta[0] <= from_cha[0] and from_rta[1] <= from_cha[1]
