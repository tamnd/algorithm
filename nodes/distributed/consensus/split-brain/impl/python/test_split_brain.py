# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-brain/. The authors are listed in prov/Z2JAHA.jsonl.

from split_brain import LockService, Storage, run, stale_writes


def scripted(fencing: bool) -> Storage:
    """Client 1 gets token 33, pauses past its lease; client 2 gets token 34 and writes; client 1 wakes and writes."""
    lock, store = LockService(ttl=10), Storage(fencing)
    lock.token = 32
    t1, _ = lock.acquire(1, now=0)
    assert t1 == 33
    assert lock.acquire(2, now=5) is None  # the lease of client 1 is still valid
    # client 1 pauses from time 1 to time 20; its lease expires at time 10
    t2, _ = lock.acquire(2, now=12)
    assert t2 == 34
    assert store.write(t2, 2, "new")
    store.write(t1, 1, "stale")  # client 1 wakes and still thinks it holds the lease
    return store


def test_fencing_rejects_the_stale_holder() -> None:
    store = scripted(fencing=True)
    assert store.accepted == [(34, 2, "new")]


def test_without_fencing_the_stale_write_lands() -> None:
    store = scripted(fencing=False)
    assert store.accepted[-1] == (33, 1, "stale")
    assert stale_writes(store) == 1


def test_random_runs() -> None:
    unfenced_bad = 0
    for seed in range(300):
        fenced = run(seed, fencing=True)
        assert stale_writes(fenced) == 0
        tokens = [t for t, _, _ in fenced.accepted]
        assert tokens == sorted(tokens)  # the accepted writes are in token order
        unfenced = run(seed, fencing=False)
        unfenced_bad += stale_writes(unfenced) > 0
        assert len(fenced.accepted) > 0
    assert unfenced_bad > 30  # pauses and slow clocks cause split brain often


def test_one_token_per_grant() -> None:
    lock = LockService(ttl=5)
    seen = []
    for now in range(0, 60, 6):
        g = lock.acquire(now % 3, now)
        assert g is not None
        seen.append(g[0])
    assert seen == list(range(1, 11))
