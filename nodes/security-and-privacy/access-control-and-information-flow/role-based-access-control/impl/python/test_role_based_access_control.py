# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/role-based-access-control/. The authors are listed in prov/VWXVF2.jsonl.

import itertools
import random

from role_based_access_control import RBAC

READ_HANDBOOK = ("read", "handbook")
WRITE_ACCOUNT = ("write", "account")
READ_LOG = ("read", "log")
APPROVE_LOAN = ("approve", "loan")
READ_STATEMENT = ("read", "statement")


def build_bank() -> RBAC:
    """The example of the page."""
    b = RBAC()
    for x in ["employee", "teller", "auditor", "manager", "customer"]:
        b.add_role(x)
    assert b.add_inheritance("teller", "employee")
    assert b.add_inheritance("auditor", "employee")
    assert b.add_inheritance("manager", "teller")
    b.grant_permission(READ_HANDBOOK, "employee")
    b.grant_permission(WRITE_ACCOUNT, "teller")
    b.grant_permission(READ_LOG, "auditor")
    b.grant_permission(APPROVE_LOAN, "manager")
    b.grant_permission(READ_STATEMENT, "customer")
    assert b.add_ssd({"teller", "auditor"}, 2)
    assert b.add_dsd({"teller", "customer"}, 2)
    assert b.assign_user("alice", "manager")
    assert b.assign_user("bob", "teller")
    assert b.assign_user("bob", "customer")
    assert b.assign_user("carol", "auditor")
    return b


def test_page_example() -> None:
    b = build_bank()
    b.check_invariant()
    assert b.authorized_roles("alice") == {"manager", "teller", "employee"}
    assert b.user_permissions("alice") == {APPROVE_LOAN, WRITE_ACCOUNT, READ_HANDBOOK}
    assert b.user_permissions("carol") == {READ_LOG, READ_HANDBOOK}
    # Static separation of duty.
    assert not b.assign_user("carol", "teller")
    assert not b.assign_user("alice", "auditor")  # alice is a teller through manager
    assert not b.add_inheritance("auditor", "teller")  # would make carol a teller
    # Sessions and dynamic separation of duty.
    b.create_session("bob", 1)
    assert b.add_active_role(1, "teller")
    assert not b.add_active_role(1, "customer")
    assert not b.add_active_role(1, "manager")  # not authorized
    assert b.check_access(1, WRITE_ACCOUNT)
    assert b.check_access(1, READ_HANDBOOK)  # inherited from employee
    assert not b.check_access(1, READ_STATEMENT)
    b.drop_active_role(1, "teller")
    assert b.add_active_role(1, "customer")
    assert b.check_access(1, READ_STATEMENT)
    assert not b.check_access(1, WRITE_ACCOUNT)
    b.create_session("alice", 2)
    assert b.add_active_role(2, "employee")
    assert not b.check_access(2, APPROVE_LOAN)  # least privilege: only employee is active
    assert b.add_active_role(2, "manager")
    assert b.check_access(2, APPROVE_LOAN)
    b.check_invariant()


def test_edge_cases() -> None:
    b = RBAC()
    b.add_role("a")
    b.add_role("b")
    assert not b.add_inheritance("a", "a")
    assert b.add_inheritance("a", "b")
    assert not b.add_inheritance("b", "a")
    assert not b.assign_user("u", "missing")
    assert not b.add_ssd({"a"}, 2)
    assert not b.add_ssd({"a", "b"}, 3)
    assert b.assign_user("u", "a")
    assert not b.add_ssd({"a", "b"}, 2)  # u is authorized for a and b
    b.create_session("u", "s")
    assert b.add_active_role("s", "a")
    assert b.add_active_role("s", "b")
    assert not b.add_dsd({"a", "b"}, 2)
    b.deassign_user("u", "a")
    assert b.active_roles("s") == set()
    assert not b.check_access("s", "p")
    b.check_invariant()


def closure_oracle(n: int, edges: set[tuple[int, int]]) -> list[list[bool]]:
    """The reflexive and transitive closure of the hierarchy, by Warshall's method."""
    ge = [[i == j or (i, j) in edges for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            if ge[i][k]:
                for j in range(n):
                    if ge[k][j]:
                        ge[i][j] = True
    return ge


def test_random_states_against_flattened_relation() -> None:
    rng = random.Random(1996)
    objects = ["o1", "o2", "o3", "o4"]
    rights = ["r", "w", "x"]
    perms = list(itertools.product(rights, objects))
    users = ["u1", "u2", "u3", "u4"]
    for trial in range(600):
        n = rng.randint(1, 5)
        b = RBAC()
        for x in range(n):
            b.add_role(x)
        edges: set[tuple[int, int]] = set()
        ua: set[tuple[str, int]] = set()
        pa: set[tuple[tuple[str, str], int]] = set()
        ssd: list[tuple[frozenset[int], int]] = []
        for _ in range(rng.randint(0, 25)):
            op = rng.random()
            if op < 0.3:
                i, j = rng.randrange(n), rng.randrange(n)
                ge = closure_oracle(n, edges)
                trial_ge = closure_oracle(n, edges | {(i, j)})
                ok = not ge[j][i] and all(
                    len({x for x in range(n) if any(trial_ge[y][x] for u2, y in ua if u2 == u)} & rs) < k
                    for u in users
                    for rs, k in ssd
                )
                assert b.add_inheritance(i, j) == ok
                if ok:
                    edges.add((i, j))
            elif op < 0.55:
                u, x = rng.choice(users), rng.randrange(n)
                ge = closure_oracle(n, edges)
                auth = {z for z in range(n) if any(ge[y][z] for u2, y in ua | {(u, x)} if u2 == u)}
                ok = all(len(auth & rs) < k for rs, k in ssd)
                assert b.assign_user(u, x) == ok
                if ok:
                    ua.add((u, x))
            elif op < 0.65:
                u, x = rng.choice(users), rng.randrange(n)
                b.deassign_user(u, x)
                ua.discard((u, x))
            elif op < 0.9:
                p, x = rng.choice(perms), rng.randrange(n)
                b.grant_permission(p, x)
                pa.add((p, x))
            else:
                rs = frozenset(rng.sample(range(n), rng.randint(1, n)))
                k = rng.randint(1, 3)
                ge = closure_oracle(n, edges)
                ok = 2 <= k <= len(rs) and all(
                    len({z for z in range(n) if any(ge[y][z] for u2, y in ua if u2 == u)} & rs) < k for u in users
                )
                assert b.add_ssd(rs, k) == ok
                if ok:
                    ssd.append((rs, k))
            b.check_invariant()
        # The flattened relation UA o RH* o PA, against sessions with every authorized role.
        ge = closure_oracle(n, edges)
        for u in users:
            flat = {p for (p, x) in pa if any(ge[y][x] for u2, y in ua if u2 == u)}
            assert b.user_permissions(u) == flat
            sid = (trial, u)
            b.create_session(u, sid)
            for x in b.authorized_roles(u):
                assert b.add_active_role(sid, x)
            for p in perms:
                assert b.check_access(sid, p) == (p in flat)
