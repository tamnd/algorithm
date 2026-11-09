# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/faro-shuffle/. The authors are listed in prov/0P38K0.jsonl.

from faro_shuffle import elmsley_moves, faro_shuffle, shuffle_order


def order_by_simulation(n: int, out: bool) -> int:
    start = list(range(n))
    a = faro_shuffle(start, out)
    k = 1
    while a != start:
        a = faro_shuffle(a, out)
        k += 1
    return k


def group_order(n: int) -> int:
    start = tuple(range(n))
    seen = {start}
    todo = [start]
    while todo:
        a = todo.pop()
        for out in (True, False):
            b = tuple(faro_shuffle(list(a), out))
            if b not in seen:
                seen.add(b)
                todo.append(b)
    return len(seen)


def test_example_eight_cards() -> None:
    a = list(range(8))
    assert faro_shuffle(a, out=True) == [0, 4, 1, 5, 2, 6, 3, 7]
    assert faro_shuffle(a, out=False) == [4, 0, 5, 1, 6, 2, 7, 3]
    states = [a]
    for _ in range(3):
        states.append(faro_shuffle(states[-1], out=True))
    assert states[2] == [0, 2, 4, 6, 1, 3, 5, 7]
    assert states[3] == a


def test_edges() -> None:
    assert faro_shuffle([]) == []
    assert faro_shuffle(["x", "y"], out=True) == ["x", "y"]
    assert faro_shuffle(["x", "y"], out=False) == ["y", "x"]
    try:
        faro_shuffle([1, 2, 3])
    except ValueError:
        pass
    else:
        raise AssertionError("odd decks must be rejected")


def test_orders_match_simulation() -> None:
    for n in range(2, 202, 2):
        assert shuffle_order(n, True) == order_by_simulation(n, True)
        assert shuffle_order(n, False) == order_by_simulation(n, False)


def test_table_values() -> None:
    table = {
        2: (1, 2), 4: (2, 4), 6: (4, 3), 8: (3, 6), 10: (6, 10), 12: (10, 12),
        20: (18, 6), 32: (5, 10), 50: (21, 8), 52: (8, 52), 54: (52, 20),
        64: (6, 12), 100: (30, 100), 1024: (10, 20),
    }
    for n, (o, i) in table.items():
        assert (shuffle_order(n, True), shuffle_order(n, False)) == (o, i)
        assert (order_by_simulation(n, True), order_by_simulation(n, False)) == (o, i)


def test_position_maps() -> None:
    for n in range(2, 60, 2):
        a = list(range(n))
        o, i = faro_shuffle(a, True), faro_shuffle(a, False)
        for p in range(n):
            assert o.index(p) == (2 * p % (n - 1) if p < n - 1 else n - 1)
            assert i.index(p) == (2 * p + 1) % (n + 1)


def test_26_in_shuffles_reverse_52_cards() -> None:
    a = list(range(52))
    for _ in range(26):
        a = faro_shuffle(a, out=False)
    assert a == list(range(51, -1, -1))


def test_elmsley_binary_trick() -> None:
    assert elmsley_moves(6) == "IIO"
    for n in (8, 16, 52, 64):
        for p in range(n):
            a = list(range(n))
            for move in elmsley_moves(p):
                a = faro_shuffle(a, out=(move == "O"))
            assert a.index(0) == p


def test_group_of_power_of_two_decks() -> None:
    for k in range(1, 5):
        assert group_order(2**k) == k * 2**k
