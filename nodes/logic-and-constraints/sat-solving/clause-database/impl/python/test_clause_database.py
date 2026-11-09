# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clause-database/. The authors are listed in prov/K9N1A5.jsonl.

import random

import pytest

from clause_database import ClauseDatabase


def test_page_example() -> None:
    db = ClauseDatabase(5)
    a = db.add([1, 2, 3])
    b = db.add([-1, 4], learned=True, lbd=2)
    c = db.add([-2, -4, 5], learned=True, lbd=3)
    assert (a, b, c) == (0, 6, 11)
    assert db.arena == [3, 0, 0, 1, 2, 3, 2, 1, 2, -1, 4, 3, 1, 3, -2, -4, 5]
    assert db.watchers(-4) == [11] and db.watchers(4) == [6]
    db.swap_watch(c, 1, 2)
    assert db.literals(c) == [-2, 5, -4]
    assert db.watchers(-4) == [] and db.watchers(5) == [11]
    db.delete(b)
    assert db.wasted == 5 and db.check_invariant()
    assert list(db.refs()) == [0, 11]
    moved = db.collect_garbage()
    assert moved == {0: 0, 11: 6}
    assert db.arena == [3, 0, 0, 1, 2, 3, 3, 1, 3, -2, 5, -4]
    assert db.watchers(5) == [6] and db.watchers(4) == [] and db.watchers(-1) == []
    assert db.wasted == 0 and db.check_invariant()


def test_errors() -> None:
    db = ClauseDatabase(3)
    with pytest.raises(ValueError):
        db.add([1])
    with pytest.raises(ValueError):
        db.add([1, -1])
    with pytest.raises(ValueError):
        db.add([1, 4])
    r = db.add([1, 2])
    with pytest.raises(ValueError):
        db.swap_watch(r, 0, 2)
    db.delete(r)
    with pytest.raises(ValueError):
        db.delete(r)
    assert db.collect_garbage() == {} and db.arena == []


def test_random_operations_against_model() -> None:
    rng = random.Random(2003)
    checks = 0
    for _ in range(600):
        n = rng.randint(2, 8)
        db = ClauseDatabase(n)
        # model: name -> [literals, learned, lbd]; ref maps names to references
        model: dict[int, list] = {}
        ref: dict[int, int] = {}
        fresh = 0
        for _ in range(rng.randint(1, 40)):
            op = rng.random()
            if op < 0.4 or not model:
                vs = rng.sample(range(1, n + 1), rng.randint(2, n))
                lits = [v if rng.random() < 0.5 else -v for v in vs]
                learned = rng.random() < 0.5
                g = rng.randint(1, len(lits))
                ref[fresh] = db.add(lits, learned, g)
                model[fresh] = [lits, learned, g]
                fresh += 1
            elif op < 0.6:
                name = rng.choice(sorted(model))
                db.delete(ref.pop(name))
                del model[name]
            elif op < 0.8:
                name = rng.choice(sorted(model))
                lits = model[name][0]
                if len(lits) > 2:
                    i, k = rng.randint(0, 1), rng.randint(2, len(lits) - 1)
                    db.swap_watch(ref[name], i, k)
                    lits[i], lits[k] = lits[k], lits[i]
            elif op < 0.9:
                name = rng.choice(sorted(model))
                g = rng.randint(1, 9)
                db.set_lbd(ref[name], g)
                model[name][2] = g
            else:
                before = len(db.arena)
                wasted = db.wasted
                moved = db.collect_garbage()
                assert len(db.arena) == before - wasted
                assert sorted(moved) == sorted(ref.values())
                ref = {name: moved[r] for name, r in ref.items()}
            assert db.check_invariant()
            # every stored clause matches the model
            assert sorted(db.refs()) == sorted(ref.values())
            for name, (lits, learned, g) in model.items():
                r = ref[name]
                assert db.literals(r) == lits and db.is_learned(r) == learned and db.lbd(r) == g
                assert not db.is_deleted(r)
            # watch lists match the first two literals of the model clauses
            for v in range(1, n + 1):
                for lit in (v, -v):
                    want = sorted(ref[name] for name, (lits, _, _) in model.items() if lit in lits[:2])
                    assert sorted(db.watchers(lit)) == want
                    checks += 1
    assert checks > 10000
