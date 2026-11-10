# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dotted-version-vectors/. The authors are listed in prov/Q366JY.jsonl.

import random

from dotted_version_vectors import DottedVersionVector as DVV
from dotted_version_vectors import Server, random_schedule


def maximal(events: set, hist: dict) -> set:
    """Ground truth siblings: the events whose history no other event's history strictly contains."""
    return {e for e in events if not any(hist[e] < hist[f] for f in events)}


def run(servers: list[str], clients: int, ops: list[tuple]) -> None:
    """Run DVV servers and a ground-truth model side by side and compare them after each step."""
    srv = {r: Server(r) for r in servers}
    truth: dict[str, set] = {r: set() for r in servers}
    hist: dict = {}
    ctx: list[dict] = [{} for _ in range(clients)]
    seen: list[frozenset] = [frozenset() for _ in range(clients)]
    for op in ops:
        if op[0] == "get":
            _, c, r = op
            values, ctx[c] = srv[r].get()
            seen[c] = frozenset().union(*(hist[v] for v in truth[r]))
            assert set(values) == truth[r]
            # The context covers exactly the union of the histories read.
            assert {(i, k) for i, m in ctx[c].items() for k in range(1, m + 1)} == seen[c]
        elif op[0] == "put":
            _, c, r = op
            u = srv[r].put(ctx[c], None)
            event = u.dot if u.dot is not None else (r, u.vv[r])
            assert event not in hist  # each write gets a fresh event
            hist[event] = seen[c] | {event}
            assert u.history() == hist[event]
            srv[r].siblings = {(cl, event if cl == u else v) for cl, v in srv[r].siblings}
            truth[r] = maximal(truth[r] | {event}, hist)
        else:
            _, a, b = op
            srv[a].sync_with(srv[b])
            truth[a] = truth[b] = maximal(truth[a] | truth[b], hist)
        for r in servers:
            assert {v for _, v in srv[r].siblings} == truth[r]
            for cl, v in srv[r].siblings:
                assert cl.history() == hist[v]
            for x, _ in srv[r].siblings:
                for y, _ in srv[r].siblings:
                    assert x.leq(y) == (x.history() <= y.history())


def test_semantics_and_order() -> None:
    a = DVV({"r": 4})
    b = DVV({"r": 3}, ("r", 5))
    assert b.history() == {("r", 1), ("r", 2), ("r", 3), ("r", 5)}
    assert not a.leq(b) and not b.leq(a)  # {(r,4)} || {(r,3,5)}
    assert DVV({"r": 2}, ("r", 3)) == DVV({"r": 3})  # normal form


def test_blind_writes_then_read() -> None:
    # Two clients write at server b with empty contexts, then a client that read both writes at a.
    b = Server("b")
    u1 = b.put({}, "v1")
    u2 = b.put({}, "v2")
    assert u1 == DVV({"b": 0}, ("b", 1)) and u2 == DVV({"b": 0}, ("b", 2))
    assert u2.dot == ("b", 2) and u2.vv == {}
    assert len(b.siblings) == 2  # concurrent, both kept
    values, ctx = b.get()
    assert ctx == {"b": 2}
    a = Server("a")
    a.siblings = set(b.siblings)
    u3 = a.put(ctx, "v3")
    assert u3.vv == {"a": 1, "b": 2} and u3.dot is None
    assert [v for _, v in a.siblings] == ["v3"]


def test_per_server_vv_loses_update() -> None:
    # Section 3.2: with one plain version vector per sibling and server ids only,
    # the second blind write gets {(b,2)}, which dominates {(b,1)}: v1 is lost.
    def vv_leq(x: dict, y: dict) -> bool:
        return all(m <= y.get(i, 0) for i, m in x.items())

    sibs: list[tuple[dict, str]] = []
    for value in ("v1", "v2"):
        top = max((c.get("b", 0) for c, _ in sibs), default=0)
        new = {"b": top + 1}
        sibs = [(c, v) for c, v in sibs if not vv_leq(c, new)] + [(new, value)]
    assert [v for _, v in sibs] == ["v2"]  # v1 lost although nobody read it
    # The same writes with DVV keep both.
    s = Server("b")
    s.put({}, "v1")
    s.put({}, "v2")
    assert sorted(v for _, v in s.siblings) == ["v1", "v2"]


def test_sibling_explosion() -> None:
    # Two clients alternate get and put, and each put misses the other client's last put.
    # One version vector per object cannot tell which siblings a context covers.
    obj_vv: dict = {}
    obj_sibs: list = []
    ctx = [dict(obj_vv), dict(obj_vv)]
    dvv = Server("r")
    dctx = [{}, {}]
    for k in range(1, 9):
        c = k % 2
        # single version vector per object
        if all(obj_vv.get(i, 0) <= ctx[c].get(i, 0) for i in obj_vv):
            obj_sibs = [k]
        else:
            obj_sibs = obj_sibs + [k]
        for i, m in ctx[c].items():
            obj_vv[i] = max(obj_vv.get(i, 0), m)
        obj_vv["r"] = obj_vv.get("r", 0) + 1
        ctx[c] = dict(obj_vv)
        # dotted version vectors
        dvv.put(dctx[c], k)
        dctx[c] = dvv.get()[1]
        assert len(obj_sibs) == k
        assert len(dvv.siblings) == min(k, 2)


def test_random_against_causal_histories() -> None:
    rng = random.Random(2010)
    for _ in range(500):
        servers = ["a", "b", "c"][: rng.randint(1, 3)]
        clients = rng.randint(1, 4)
        run(servers, clients, random_schedule(servers, clients, rng.randint(0, 25), rng))
