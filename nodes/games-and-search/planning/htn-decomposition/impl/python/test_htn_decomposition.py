# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/htn-decomposition/. The authors are listed in prov/NW29JR.jsonl.

import random

from htn_decomposition import (Domain, Method, TaskNetwork, all_plans, chain, find_plan, method, operator, run_plan, shop,
                               travel_domain)

CHECK = "?check"


def expansions(network, domain, depth):
    """Every fully primitive network reachable by decomposition within the depth bound.
    A marker node carries the method precondition; it inherits the orderings of the
    decomposed node and comes before every subtask."""
    compound = [n for n, (t, _) in network.nodes.items() if not t.startswith(CHECK) and not domain.is_primitive(t)]
    if not compound:
        yield network
        return
    n = min(compound)
    task, d = network.nodes[n]
    if d >= depth:
        return
    for m in domain.methods.get(task, []):
        marker = Method(m.name, task, m.pre, (CHECK + str(sorted(m.pre)),) + m.subtasks,
                        frozenset((0, j + 1) for j in range(len(m.subtasks))) | {(i + 1, j + 1) for i, j in m.order})
        expanded = network.decompose(n, marker)
        yield from expansions(expanded, domain, depth)


def brute_plans(init, network, domain, depth):
    pre_of = {CHECK + str(sorted(m.pre)): m.pre for ms in domain.methods.values() for m in ms}
    plans = set()

    def simulate(net, done, state, plan):
        """Walk every linearization of net; a prefix that fails is cut, since every
        linearization that extends it fails too."""
        if len(done) == len(net.nodes):
            plans.add(tuple(plan))
            return
        for n in net.nodes:
            if n in done or any(v == n and u not in done for u, v in net.order):
                continue
            task = net.nodes[n][0]
            if task.startswith(CHECK):
                if pre_of[task] <= state:
                    simulate(net, done | {n}, state, plan)
            else:
                op = domain.operators[task]
                if op.pre <= state:
                    simulate(net, done | {n}, (state - op.delete) | op.add, plan + [task])

    for net in expansions(network, domain, depth):
        simulate(net, frozenset(), frozenset(init), [])
    return plans


def random_domain(rng, total_order):
    facts = [f"f{i}" for i in range(4)]
    ops = []
    for k in range(3):
        ops.append(operator(f"o{k}", rng.sample(facts, rng.randint(0, 1)), rng.sample(facts, rng.randint(1, 2)),
                            rng.sample(facts, rng.randint(0, 1))))
    methods = []
    for task in ("T", "U"):
        for k in range(rng.randint(1, 2)):
            size = rng.randint(0, 2)
            subtasks = [rng.choice(["o0", "o1", "o2", "T", "U"]) for _ in range(size)]
            if total_order or size < 2:
                order = None
            else:
                order = rng.choice([[], [(0, 1)], [(1, 0)]])
            methods.append(method(f"{task}{k}", task, rng.sample(facts, rng.randint(0, 1)), subtasks, order))
    init = frozenset(f for f in facts if rng.random() < 0.5)
    return init, Domain(ops, methods)


def initial_network(rng, total_order):
    tasks = [rng.choice(["T", "U", "o0", "o1"]) for _ in range(rng.randint(1, 2))]
    order = None if total_order or len(tasks) < 2 else rng.choice([[], [(0, 1)]])
    return TaskNetwork.of(tasks, order)


def test_partial_order_plans_equal_brute_force():
    rng = random.Random(51)
    nonempty = 0
    for _ in range(250):
        init, domain = random_domain(rng, total_order=False)
        network = initial_network(rng, total_order=False)
        plans = all_plans(init, network, domain, 3)
        assert plans == brute_plans(init, network, domain, 3)
        nonempty += bool(plans)
    assert nonempty > 60


def test_every_plan_is_a_valid_primitive_plan():
    rng = random.Random(52)
    for _ in range(250):
        init, domain = random_domain(rng, total_order=False)
        network = initial_network(rng, total_order=False)
        for plan in all_plans(init, network, domain, 3):
            assert all(domain.is_primitive(t) for t in plan)
            assert run_plan(init, plan, domain) is not None


def test_shop_agrees_with_the_partial_order_planner_on_total_order():
    rng = random.Random(53)
    for _ in range(250):
        init, domain = random_domain(rng, total_order=True)
        network = initial_network(rng, total_order=True)
        tasks = [network.nodes[n] for n in sorted(network.nodes)]
        assert set(shop(init, tasks, domain, 3)) == all_plans(init, network, domain, 3)
        assert set(shop(init, tasks, domain, 3)) == brute_plans(init, network, domain, 3)


def test_travel_backtracks_from_the_bus_to_the_taxi():
    init, domain = travel_domain()
    network = TaskNetwork.of(["travel"])
    assert find_plan(init, network, domain, 1) == ("call-taxi", "ride-taxi", "pay-driver")
    assert all_plans(init, network, domain, 1) == {("call-taxi", "ride-taxi", "pay-driver")}
    assert find_plan(init | {"park-is-near"}, network, domain, 1) == ("walk",)
    assert find_plan(init | {"have-coin"} - {"have-cash"}, network, domain, 1) == ("go-to-stop", "buy-ticket", "ride-bus")
    assert find_plan(init - {"have-cash"}, network, domain, 1) is None
    assert find_plan(init, network, domain, 0) is None


def test_method_precondition_is_tested_in_the_current_state():
    # The method for T needs g. Task o makes g. With o before T a plan exists;
    # with T before o it does not, and unordered the planner finds o, then T.
    ops = [operator("o", [], ["g"]), operator("p", [], ["done"])]
    domain = Domain(ops, [method("m", "T", ["g"], ["p"])])
    assert all_plans([], TaskNetwork.of(["o", "T"]), domain, 1) == {("o", "p")}
    assert all_plans([], TaskNetwork.of(["T", "o"]), domain, 1) == set()
    assert all_plans([], TaskNetwork.of(["T", "o"], []), domain, 1) == {("o", "p")}


def test_shop_rejects_a_partially_ordered_method():
    domain = Domain([operator("a"), operator("b")], [method("m", "T", [], ["a", "b"], [])])
    try:
        list(shop(frozenset(), [("T", 0)], domain, 2))
        assert False
    except ValueError:
        pass
