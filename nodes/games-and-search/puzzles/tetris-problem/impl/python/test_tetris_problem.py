# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tetris-problem/. The authors are listed in prov/QESA6R.jsonl.

import random

from tetris_problem import BASE, drop, rotations, survive_count, survive_count_brute, survives_forever


def test_rotations() -> None:
    assert {name: len(rotations(name)) for name in BASE} == {
        'I': 2, 'O': 1, 'T': 4, 'S': 2, 'Z': 2, 'L': 4, 'J': 4}


def test_drop_and_clear() -> None:
    empty = (0, 0, 0, 0)
    flat_i = rotations('I')[0]
    board, lost = drop(empty, flat_i, 0, 4)
    assert board == empty and not lost  # one row filled and cleared
    board, lost = drop(empty, rotations('O')[0], 1, 4)
    assert board == (0b0110, 0b0110, 0, 0) and not lost
    assert drop(empty, flat_i, 1, 4) is None  # does not fit in the width


def test_dynamic_program_against_brute_force() -> None:
    rng = random.Random(9)
    for _ in range(40):
        width, height = rng.choice([(3, 4), (4, 3), (4, 4)])
        seq = ''.join(rng.choice('IOTSZLJ') for _ in range(rng.randint(1, 7)))
        assert survive_count(seq, width, height) == survive_count_brute(seq, width, height), seq


def test_periodic_sequences() -> None:
    # width a multiple of 4: alternating S and Z can go on forever
    assert survives_forever('SZ', 4, 4)
    # odd width: O pieces alone always lose, since no row can ever be filled
    assert not survives_forever('O', 3, 4) and not survives_forever('O', 5, 4)
    assert survives_forever('O', 4, 4)
