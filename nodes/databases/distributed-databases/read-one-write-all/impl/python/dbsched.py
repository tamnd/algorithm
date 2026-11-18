# SPDX-License-Identifier: MIT
# Shared helper of the databases pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Schedules of transactions, and their classes checked by definition.

This is the reference that the tests of the concurrency pages compare
against. Every class test here follows its definition directly. The
serializability tests try every serial order of the committed transactions;
there is no conflict graph and no cycle test here. Do not use it as a
scheduler.

Actions and schedules
    An action is a tuple (kind, txn, item). kind is "r" (read), "w" (write),
    "c" (commit) or "a" (abort). txn is a transaction id (an int after
    parse). item is a string for r and w, and None for c and a.
    A schedule is a tuple of actions. In a well-formed schedule each
    transaction has at most one c or a, and it is the last action of that
    transaction. A schedule may be a prefix: a transaction with no c or a
    is active.

    parse("r1(x) w2(x) c1 a2")    the schedule as a tuple of actions
    format(s)                     the inverse of parse (also format_schedule)
    validate(s)                   raise ValueError if s is not well formed
    transactions(s)               the ids in the order of their first action
    committed(s), aborted(s)      the ids with a c, or with an a, in s
    actions_of(s, t)              the actions of t, in order
    committed_projection(s)       the r, w and c actions of the committed
                                  transactions, in the order of s
    conflicts(p, q)               different transactions, the same item, and
                                  at least one write
    serial_schedule(s, order)     the actions of the transactions of order,
                                  one transaction after the other

Equivalence and serializability (on the committed projection)
    conflict_equivalent(s1, s2)   same actions, and every pair of conflicting
                                  actions in the same order
    reads_from(s)                 {read: write it reads from}, see below
    final_writes(s)               {item: the last write on the item}
    view_equivalent(s1, s2)       same actions, same reads_from and the same
                                  final_writes
    conflict_serializable_orders(s), view_serializable_orders(s)
                                  every serial order of the committed
                                  transactions that is equivalent, as tuples,
                                  in lexicographic order of the sorted ids
    is_conflict_serializable(s), is_view_serializable(s)
    These raise ValueError when s has more than MAX_BRUTE_FORCE committed
    transactions. is_view_serializable uses the plain definition (view
    equivalence of C(s) to a serial schedule), with no condition on prefixes.

Recovery classes (on the full schedule, with its aborts), as in Bernstein,
Hadzilacos and Goodman (1987), Section 1.2
    is_recoverable(s)             if T_i reads x from T_j (i != j) and c_i is
                                  in s, then c_j < c_i
    avoids_cascading_aborts(s)    if T_i reads x from T_j (i != j), then
                                  c_j < r_i(x)
    is_strict(s)                  if w_j(x) < o_i(x) (i != j, o in r and w),
                                  then a_j < o_i(x) or c_j < o_i(x)

Reads-from
    An action is named by its occurrence id (txn, kind, item, k): the k-th
    action of that kind on that item by that transaction, from 0. A read
    r_i(x) reads from w_j(x) when w_j(x) comes before r_i(x), a_j does not
    come before r_i(x), and every write w_k(x) between them has its a_k
    before r_i(x). If no write qualifies, the read reads the initial value,
    shown as None. The writer is a write occurrence, not only a transaction,
    so a read between two writes of the same transaction on the same item
    is told apart from a read after both.

Generators
    interleavings(txns)           every schedule that merges the sequences
                                  of txns and keeps the order inside each
    random_schedule(rng, txns)    one of them, chosen uniformly with the
                                  random.Random rng
    Each element of txns is a sequence of actions or a string for parse.
"""

import itertools
import re

MAX_BRUTE_FORCE = 6

READ, WRITE, COMMIT, ABORT = "r", "w", "c", "a"
_KINDS = (READ, WRITE, COMMIT, ABORT)
_TOKEN = re.compile(r"^([rwca])(\d+)(?:\(([A-Za-z_][A-Za-z0-9_]*)\))?$")


# ---------------------------------------------------------------- basics

def parse(text):
    """Parse "r1(x) w2(x) c1 a2" into a tuple of actions."""
    out = []
    for tok in text.split():
        m = _TOKEN.match(tok)
        if not m:
            raise ValueError("bad action %r" % tok)
        kind, txn, item = m.group(1), int(m.group(2)), m.group(3)
        if kind in (READ, WRITE) and item is None:
            raise ValueError("a read or write needs an item: %r" % tok)
        if kind in (COMMIT, ABORT) and item is not None:
            raise ValueError("a commit or abort has no item: %r" % tok)
        out.append((kind, txn, item))
    s = tuple(out)
    validate(s)
    return s


def format(schedule):
    """Write a schedule in the notation of parse."""
    parts = []
    for kind, txn, item in schedule:
        if item is None:
            parts.append("%s%s" % (kind, txn))
        else:
            parts.append("%s%s(%s)" % (kind, txn, item))
    return " ".join(parts)


format_schedule = format


def validate(schedule):
    """Raise ValueError unless each transaction ends at most once, at its end."""
    ended = set()
    for act in schedule:
        if len(act) != 3:
            raise ValueError("an action is (kind, txn, item): %r" % (act,))
        kind, txn, item = act
        if kind not in _KINDS:
            raise ValueError("bad kind %r" % (kind,))
        if (kind in (READ, WRITE)) != (item is not None):
            raise ValueError("item must be set exactly for r and w: %r" % (act,))
        if txn in ended:
            raise ValueError("action after the end of transaction %r" % (txn,))
        if kind in (COMMIT, ABORT):
            ended.add(txn)


def transactions(schedule):
    """The transaction ids in the order of their first action."""
    seen = []
    for _, txn, _ in schedule:
        if txn not in seen:
            seen.append(txn)
    return seen


def committed(schedule):
    """The set of ids that have a commit in the schedule."""
    return {txn for kind, txn, _ in schedule if kind == COMMIT}


def aborted(schedule):
    """The set of ids that have an abort in the schedule."""
    return {txn for kind, txn, _ in schedule if kind == ABORT}


def actions_of(schedule, txn):
    """The actions of one transaction, in order."""
    return tuple(a for a in schedule if a[1] == txn)


def committed_projection(schedule):
    """The actions of the committed transactions, in the order of the schedule."""
    validate(schedule)
    keep = committed(schedule)
    return tuple(a for a in schedule if a[1] in keep)


def conflicts(p, q):
    """True when p and q are reads or writes of different transactions on the
    same item, and at least one of them is a write."""
    return (p[0] in (READ, WRITE) and q[0] in (READ, WRITE)
            and p[1] != q[1] and p[2] == q[2]
            and (p[0] == WRITE or q[0] == WRITE))


def serial_schedule(schedule, order):
    """The serial schedule that runs the transactions of order one by one."""
    out = []
    for txn in order:
        out.extend(actions_of(schedule, txn))
    return tuple(out)


def _occurrences(schedule):
    """The occurrence id (txn, kind, item, k) of each action, by position."""
    count = {}
    ids = []
    for kind, txn, item in schedule:
        key = (txn, kind, item)
        k = count.get(key, 0)
        count[key] = k + 1
        ids.append((txn, kind, item, k))
    return ids


# ---------------------------------------------------------- equivalence

def _same_actions(s1, s2):
    return sorted(_occurrences(s1), key=repr) == sorted(_occurrences(s2), key=repr)


def _conflict_pairs(schedule):
    ids = _occurrences(schedule)
    pairs = set()
    for i in range(len(schedule)):
        for j in range(i + 1, len(schedule)):
            if conflicts(schedule[i], schedule[j]):
                pairs.add((ids[i], ids[j]))
    return pairs


def conflict_equivalent(s1, s2):
    """Same actions, and every pair of conflicting actions in the same order."""
    return _same_actions(s1, s2) and _conflict_pairs(s1) == _conflict_pairs(s2)


def reads_from(schedule):
    """Map the occurrence id of each read to the write occurrence it reads
    from, or to None for the initial value (see the module notes)."""
    ids = _occurrences(schedule)
    result = {}
    for q, (kind, txn, item) in enumerate(schedule):
        if kind != READ:
            continue
        ended_abort = {t for k, t, _ in schedule[:q] if k == ABORT}
        source = None
        for p in range(q - 1, -1, -1):
            pk, pt, pi = schedule[p]
            if pk == WRITE and pi == item and pt not in ended_abort:
                source = ids[p]
                break
        result[ids[q]] = source
    return result


def final_writes(schedule):
    """Map each written item to the occurrence id of its last write that is
    not followed by an abort of its transaction."""
    ids = _occurrences(schedule)
    gone = aborted(schedule)
    result = {}
    for p, (kind, txn, item) in enumerate(schedule):
        if kind == WRITE and txn not in gone:
            result[item] = ids[p]
    return result


def view_equivalent(s1, s2):
    """Same actions, the same reads-from map and the same final writes."""
    return (_same_actions(s1, s2) and reads_from(s1) == reads_from(s2)
            and final_writes(s1) == final_writes(s2))


# ------------------------------------------------------- serializability

def _orders(schedule, equivalent):
    cp = committed_projection(schedule)
    txns = sorted(committed(cp), key=repr)
    if len(txns) > MAX_BRUTE_FORCE:
        raise ValueError("brute force over %d committed transactions; at most %d"
                         % (len(txns), MAX_BRUTE_FORCE))
    return [order for order in itertools.permutations(txns)
            if equivalent(cp, serial_schedule(cp, order))]


def conflict_serializable_orders(schedule):
    """Every serial order of the committed transactions that is conflict
    equivalent to the committed projection."""
    return _orders(schedule, conflict_equivalent)


def view_serializable_orders(schedule):
    """Every serial order of the committed transactions that is view
    equivalent to the committed projection."""
    return _orders(schedule, view_equivalent)


def is_conflict_serializable(schedule):
    return bool(conflict_serializable_orders(schedule))


def is_view_serializable(schedule):
    return bool(view_serializable_orders(schedule))


# -------------------------------------------------------- recovery classes

def _position_of_end(schedule, kind):
    return {txn: p for p, (k, txn, _) in enumerate(schedule) if k == kind}


def _foreign_reads(schedule):
    """(position of the read, reader, writer txn) for each read from another
    transaction."""
    validate(schedule)
    ids = _occurrences(schedule)
    rf = reads_from(schedule)
    out = []
    for q, (kind, txn, _) in enumerate(schedule):
        if kind == READ:
            src = rf[ids[q]]
            if src is not None and src[0] != txn:
                out.append((q, txn, src[0]))
    return out


def is_recoverable(schedule):
    """If T_i reads from T_j (i != j) and c_i is in the schedule, then c_j < c_i."""
    commit_at = _position_of_end(schedule, COMMIT)
    for _, reader, writer in _foreign_reads(schedule):
        if reader in commit_at:
            if writer not in commit_at or commit_at[writer] > commit_at[reader]:
                return False
    return True


def avoids_cascading_aborts(schedule):
    """If T_i reads x from T_j (i != j), then c_j comes before the read."""
    commit_at = _position_of_end(schedule, COMMIT)
    for q, _, writer in _foreign_reads(schedule):
        if writer not in commit_at or commit_at[writer] > q:
            return False
    return True


def is_strict(schedule):
    """If w_j(x) < o_i(x) with i != j, then T_j ended (c_j or a_j) before o_i(x)."""
    validate(schedule)
    end_at = _position_of_end(schedule, COMMIT)
    end_at.update(_position_of_end(schedule, ABORT))
    for q, (kind, txn, item) in enumerate(schedule):
        if kind not in (READ, WRITE):
            continue
        for p in range(q):
            pk, pt, pi = schedule[p]
            if pk == WRITE and pi == item and pt != txn:
                if pt not in end_at or end_at[pt] > q:
                    return False
    return True


# ------------------------------------------------------------- generators

def _as_actions(txn):
    return parse(txn) if isinstance(txn, str) else tuple(txn)


def interleavings(txns):
    """Yield every interleaving of the sequences, keeping each one in order."""
    seqs = [_as_actions(t) for t in txns]
    pos = [0] * len(seqs)
    total = sum(len(s) for s in seqs)
    current = []

    def rec():
        if len(current) == total:
            yield tuple(current)
            return
        for i, seq in enumerate(seqs):
            if pos[i] < len(seq):
                current.append(seq[pos[i]])
                pos[i] += 1
                yield from rec()
                pos[i] -= 1
                current.pop()

    yield from rec()


def random_schedule(rng, txns):
    """One interleaving, uniform over all interleavings: the next action comes
    from a sequence with probability proportional to its remaining length."""
    seqs = [_as_actions(t) for t in txns]
    pos = [0] * len(seqs)
    left = sum(len(s) for s in seqs)
    out = []
    while left:
        r = rng.randrange(left)
        for i, seq in enumerate(seqs):
            rest = len(seq) - pos[i]
            if r < rest:
                out.append(seq[pos[i]])
                pos[i] += 1
                break
            r -= rest
        left -= 1
    return tuple(out)


# -------------------------------------------------------------- self-test

def _self_test():
    # A CSR schedule, equivalent to T1 T2 only.
    s = parse("r1(x) w1(x) r2(x) r1(y) w2(x) w1(y) c1 c2")
    assert format(s) == "r1(x) w1(x) r2(x) r1(y) w2(x) w1(y) c1 c2"
    assert conflict_serializable_orders(s) == [(1, 2)]
    assert is_view_serializable(s)
    # The lost update: neither CSR nor VSR.
    s = parse("r1(x) r2(x) w1(x) w2(x) c1 c2")
    assert not is_conflict_serializable(s) and not is_view_serializable(s)
    # Blind writes: VSR (as T1 T2 T3) but not CSR.
    s = parse("r1(x) w2(x) w1(x) w3(x) c1 c2 c3")
    assert not is_conflict_serializable(s)
    assert view_serializable_orders(s) == [(1, 2, 3)]
    # Not recoverable: T2 reads x from T1 and commits first.
    s = parse("w1(x) r2(x) c2 c1")
    assert not is_recoverable(s)
    # Recoverable but not ACA; ACA but not strict; strict.
    s = parse("w1(x) r2(x) c1 c2")
    assert is_recoverable(s) and not avoids_cascading_aborts(s)
    s = parse("w1(x) w2(x) c1 c2")
    assert avoids_cascading_aborts(s) and not is_strict(s)
    s = parse("w1(x) c1 r2(x) w2(x) c2")
    assert is_strict(s)
    # A read after an aborted write reads the initial value.
    s = parse("w1(x) a1 r2(x) c2")
    assert reads_from(s) == {(2, "r", "x", 0): None} and is_strict(s)
    # Committed projection, interleavings and random schedules.
    assert committed_projection(parse("r1(x) w2(x) a2 c1")) == parse("r1(x) c1")
    allx = list(interleavings(["r1(x) w1(x)", "r2(x) c2"]))
    assert len(allx) == 6 and len(set(allx)) == 6
    import random
    rng = random.Random(1)
    t = [parse("r1(x) w1(y) c1"), parse("w2(x) c2"), parse("r3(y) c3")]
    for _ in range(50):
        assert random_schedule(rng, t) in set(interleavings(t))
    return True


if __name__ == "__main__":
    _self_test()
