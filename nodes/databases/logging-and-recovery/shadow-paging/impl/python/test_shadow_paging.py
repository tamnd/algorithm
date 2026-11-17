# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shadow-paging/. The authors are listed in prov/951MHG.jsonl.

import random

from shadow_paging import Crash, Disk, InPlaceDb, ShadowDb

N_SLOTS, N_PAGES = 40, 6


def workload(rng: random.Random, txns: int) -> list[list[tuple]]:
    out, val = [], 0
    for _ in range(txns):
        ops = []
        for _ in range(rng.randrange(1, 6)):
            val += 1
            ops.append(("write", rng.randrange(N_PAGES), val))
        ops.append(("commit",) if rng.random() < 0.75 else ("abort",))
        out.append(ops)
    return out


def run(db: ShadowDb, txns: list[list[tuple]], model: list, committed: list) -> None:
    """Run the transactions. `committed` gets the model state after each
    commit, with the disk write count at the end of the commit."""
    for ops in txns:
        db.begin()
        local = list(model)
        for op in ops:
            if op[0] == "write":
                db.write(op[1], op[2])
                local[op[1]] = op[2]
                assert db.read(op[1]) == op[2]
            elif op[0] == "commit":
                db.commit()
                model[:] = local
                committed.append((db.disk.writes, tuple(model)))
            else:
                db.abort()


def crash_test(cls, seeds: int) -> list[tuple]:
    """Crash before every disk write. Returns the failures."""
    bad = []
    for seed in range(seeds):
        txns = workload(random.Random(seed), 25)
        full = Disk(N_SLOTS, N_PAGES)
        run(cls(full), txns, [0] * N_PAGES, [])
        for k in range(full.writes + 1):
            disk = Disk(N_SLOTS, N_PAGES)
            disk.limit = k
            committed = [(0, (0,) * N_PAGES)]
            try:
                run(cls(disk), txns, [0] * N_PAGES, committed)
            except Crash:
                pass
            want = max(c for c in committed if c[0] <= k)[1]
            after = ShadowDb(disk)  # restart: only recompute the free slots
            if after.state() != want:
                bad.append((seed, k))
                continue
            # no garbage survives restart: free + reachable = all slots
            used = {disk.root, *disk.slots[disk.root]}
            assert after.free | used == set(range(N_SLOTS)) and not (after.free & used)
            # the database keeps working after restart
            disk.limit = None
            after.begin()
            after.write(0, -1)
            after.commit()
            assert ShadowDb(disk).state() == (-1,) + want[1:]
    return bad


def test_crash_before_every_disk_write() -> None:
    assert crash_test(ShadowDb, 30) == []


def test_in_place_writes_break_atomicity() -> None:
    assert crash_test(InPlaceDb, 5)


def test_shadow_pages_are_untouched_until_commit() -> None:
    disk = Disk(N_SLOTS, N_PAGES)
    db = ShadowDb(disk)
    db.begin()
    db.write(2, 7)
    db.write(2, 8)
    db.write(4, 9)
    assert ShadowDb(disk).state() == (0,) * N_PAGES  # a crash now loses all
    assert db.read(2) == 8
    db.commit()
    assert db.state() == (0, 0, 8, 0, 9, 0)
    # Slots 0 (old table) and 1..6 (old pages) are the shadow. Page 2 goes to
    # slot 7, then to slot 8 (slot 7 is freed), page 4 reuses slot 7, and the
    # new table goes to slot 9. After the root switch, slots 0, 3 and 5 are free.
    assert disk.root == 9 and disk.slots[9] == (1, 2, 8, 4, 7, 6)
    assert db.free == set(range(N_SLOTS)) - {9, 1, 2, 8, 4, 7, 6}


def test_scattering() -> None:
    # After random updates the logical pages no longer sit in slot order.
    disk = Disk(N_SLOTS, N_PAGES)
    db = ShadowDb(disk)
    rng = random.Random(3)
    for _ in range(30):
        db.begin()
        db.write(rng.randrange(N_PAGES), rng.random())
        db.commit()
    table = disk.slots[disk.root]
    assert list(table) != sorted(table) or max(table) - min(table) > N_PAGES
