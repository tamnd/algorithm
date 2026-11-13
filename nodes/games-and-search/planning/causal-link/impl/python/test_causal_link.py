# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/causal-link/. The authors are listed in prov/3AWZJ1.jsonl.

import random
from itertools import permutations

from causal_link import FINISH, START, Link, Plan, make_action, possibly_between, protected, resolutions, threats, valid

FACTS = ["p", "q", "r"]


def random_plan(rng):
    plan = Plan(rng.sample(FACTS, rng.randint(0, 3)), rng.sample(FACTS, rng.randint(0, 2)))
    for k in range(rng.randint(1, 4)):
        plan.add_step(make_action(f"s{k}", rng.sample(FACTS, rng.randint(0, 2)), rng.sample(FACTS, rng.randint(0, 2)),
                                  rng.sample(FACTS, rng.randint(0, 2))))
    n = len(plan.steps)
    for _ in range(rng.randint(0, 3)):
        i, j = rng.randrange(2, n), rng.randrange(2, n)
        plan.add_ordering(i, j)
    for j in range(n):
        for p in plan.steps[j].pre:
            producers = [i for i in range(n) if p in plan.steps[i].add and i != j]
            if producers and rng.random() < 0.7:
                plan.add_link(rng.choice(producers), p, j)
    return plan


def brute_orders(plan):
    """Every permutation of the steps that keeps all ordering constraints."""
    n = len(plan.steps)
    for perm in permutations(range(n)):
        pos = {k: i for i, k in enumerate(perm)}
        if all(pos[i] < pos[j] for i, s in plan.after.items() for j in s):
            yield perm


def test_threat_check_agrees_with_brute_force():
    rng = random.Random(81)
    found = 0
    for _ in range(300):
        plan = random_plan(rng)
        orders = list(brute_orders(plan))
        for systematic in (False, True):
            got = set(threats(plan, systematic))
            expected = set()
            for link in plan.links:
                for k, step in enumerate(plan.steps):
                    touches = link.fact in step.delete or (systematic and link.fact in step.add)
                    if k in (link.producer, link.consumer) or not touches:
                        continue
                    if any(o.index(link.producer) < o.index(k) < o.index(link.consumer) for o in orders):
                        expected.add((k, link))
            assert got == expected
            found += len(got)
    assert found > 100


def test_no_threat_means_protected_in_every_linearization():
    rng = random.Random(82)
    for _ in range(300):
        plan = random_plan(rng)
        orders = list(plan.linearizations())
        threatened = {link for _, link in threats(plan)}
        for link in plan.links:
            assert (link not in threatened) == all(protected(plan, o, link) for o in orders)


def test_resolutions_keep_exactly_the_safe_linearizations():
    rng = random.Random(83)
    checked = 0
    for _ in range(300):
        plan = random_plan(rng)
        for k, link in threats(plan):
            safe = {o for o in plan.linearizations()
                    if not o.index(link.producer) < o.index(k) < o.index(link.consumer)}
            union = set()
            for child in resolutions(plan, k, link):
                assert not possibly_between(child, k, link)
                union |= set(child.linearizations())
            assert union == safe
            checked += 1
    assert checked > 100


def test_links_without_threats_and_open_conditions_give_valid_plans():
    rng = random.Random(84)
    complete = 0
    for _ in range(3000):
        plan = random_plan(rng)
        linked = {(link.fact, link.consumer) for link in plan.links}
        if any((p, j) not in linked for j, s in enumerate(plan.steps) for p in s.pre) or threats(plan):
            continue
        complete += 1
        assert all(valid(plan, o) for o in plan.linearizations())
    assert complete > 50


def test_sussman_threats():
    on, clear, table = (lambda b, x: ("on", b, x)), (lambda b: ("clear", b)), (lambda b: ("ontable", b))
    plan = Plan([on("c", "a"), table("a"), table("b"), clear("c"), clear("b")], [on("a", "b"), on("b", "c")])
    c_off = plan.add_step(make_action("move(c,a,table)", [on("c", "a"), clear("c")], [table("c"), clear("a")], [on("c", "a")]))
    b_on = plan.add_step(make_action("move(b,table,c)", [table("b"), clear("b"), clear("c")], [on("b", "c")], [table("b"), clear("c")]))
    a_on = plan.add_step(make_action("move(a,table,b)", [table("a"), clear("a"), clear("b")], [on("a", "b")], [table("a"), clear("b")]))
    plan.add_link(START, clear("c"), c_off)
    plan.add_link(START, clear("b"), b_on)
    plan.add_link(c_off, clear("a"), a_on)
    assert set(threats(plan)) == {(b_on, Link(START, clear("c"), c_off)), (a_on, Link(START, clear("b"), b_on))}
    first = resolutions(plan, b_on, Link(START, clear("c"), c_off))
    assert len(first) == 1                     # demotion before START is impossible
    second = resolutions(first[0], a_on, Link(START, clear("b"), b_on))
    assert [list(p.linearizations()) for p in second] == [[(START, c_off, b_on, a_on, FINISH)]]


def test_link_rules():
    plan = Plan(["p"], ["q"])
    try:
        plan.add_link(START, "q", FINISH)
        assert False
    except ValueError:
        pass
    k = plan.add_step(make_action("k", ["p"], ["q"], []))
    assert plan.add_link(k, "q", FINISH) and Link(k, "q", FINISH) in plan.links
    other = plan.add_step(make_action("o", ["q"], ["p"], []))
    plan.add_link(k, "q", other)
    assert not plan.add_link(other, "p", k)    # k already comes before other
