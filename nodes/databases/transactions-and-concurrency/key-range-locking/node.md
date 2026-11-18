---
tag: VVNHG6
kind: algorithm
slug: key-range-locking
name: Key-range locking
aliases:
- next-key locking
- ARIES/KVL
area: databases/transactions-and-concurrency
level: advanced
summary: Locking for ordered indexes where a lock on a key also covers the gap below it, so range scans see no phantom inserts. Next-key locking is the usual form.
solves: [concurrency-control]
model: word-ram
complexity:
  vars: {n: the number of keys in the index, r: the number of keys that a scan returns, k: the number of active transactions, l: the number of locks that are held}
  time: {per-point-operation: "O(log n + k) expected", per-scan: "O(log n + (r + 1) k) expected"}
  space: {extra: "O(l)"}
properties: {deterministic: true, online: true}
prereqs: [phantom-problem, strict-two-phase-locking, b-plus-tree]
see_also: [predicate-locking, multiple-granularity-locking, lock-table, isolation-levels, aries-recovery, blink-tree, serializable-snapshot-isolation, two-phase-locking-theorem]
sources:
  - paper: "C. Mohan, ARIES/KVL: a key-value locking method for concurrency control of multiaction transactions operating on B-tree indexes, Proceedings of the 16th International Conference on Very Large Data Bases (VLDB), 1990, pages 392 to 405"
    locator: next-key locking on the key values of a B-tree index, with instant and commit-duration locks for inserts and deletes
  - paper: "David B. Lomet, Key range locking strategies for improved concurrency, Proceedings of the 19th International Conference on Very Large Data Bases (VLDB), 1993, pages 655 to 664"
    locator: locks on key ranges as resources, and lock modes for a key and the gap beside it
  - paper: doi:10.1145/1806907.1806908
    title: Goetz Graefe, A survey of B-tree locking techniques, ACM Transactions on Database Systems 35(3), 2010, article 16
    locator: the sections on key-range locking, next-key locking and the protection of gaps against phantoms
---

Key-range locking protects the gaps between the keys of an ordered index, not only the keys. Without it, [strict two-phase locking](/strict-two-phase-locking/) on the rows that a scan returns cannot stop the [phantom problem](/phantom-problem/): another transaction inserts a new key into the range, and a second scan sees it. In next-key locking, the usual form, a lock on a key that exists covers the key and the gap below it, down to the previous key, and a special key EOF covers the gap after the last key. A scan locks every key that it returns and also the next key after the range, and an insert must first test a lock on the next key above the new key, so it waits while somebody has read that gap. Mohan's ARIES/KVL (1990) is a well-known form for B-tree indexes. With locks held to the end, next-key locking gives serializable schedules, phantoms included, at the cost of one more lock per scan and per insert.

## In plain words

Think of a row of numbered seats in a theatre, where some seats are taken. You want to know who sits between seats 3 and 6, and you want nobody to sit down there until you leave. Putting your hand on each taken seat in that part is not enough: a new person could sit in an empty seat between them.

So each taken seat also guards the empty seats just before it. You put your hand on every taken seat in your part and on the first taken seat after it. Somebody who wants to sit in an empty seat must first touch the next taken seat to the right. If your hand is on it, they wait. At the end of the row, a sign marked "end" plays the part of the next seat.

## The problem

The input is a set of transactions that run operations on an index over an ordered set of keys: a range scan that returns the keys in $[lo, hi]$, a point lookup, an insert and a delete. A transaction sees the index through these operations only, and the schedule must be serializable with respect to their results: each committed transaction must get the same answers as in some serial run. Locks on the keys that exist do not give this, because the answer of a scan, or of a lookup that finds nothing, depends on keys that do not exist yet. [Predicate locking](/predicate-locking/) solves the problem in general, but testing whether two predicates overlap is expensive. In an ordered index, a range of key values is a predicate that is easy to cover with locks on keys that exist.

The model here is one index in main memory, a [lock table](/lock-table/) with S and X locks, and locks held to the end of the transaction, as in strict two-phase locking. Each operation runs as one step once it has its locks; in a real B-tree a short latch on the page plays this part.

## The algorithm

```pseudo id=main
NEXT(k)
L1  return the smallest key in the index above k, or EOF if there is none

SCAN(T, lo, hi)
L2  S-lock each key v of the index with lo ≤ v ≤ hi, and S-lock NEXT(hi)
L3  return the keys v of the index with lo ≤ v ≤ hi

FETCH(T, k)
L4  if k is in the index then S-lock k else S-lock NEXT(k); return whether k is in the index

INSERT(T, k)
L5  if k is in the index then S-lock k; return false          ▷ a duplicate key
L6  test an instant X lock on NEXT(k)                         ▷ nobody else holds a lock on the gap
L7  X-lock k; insert k; return true

DELETE(T, k)
L8  if k is not in the index then S-lock NEXT(k); return false
L9  X-lock k and NEXT(k); delete k; return true

END(T)
L10 on abort, undo the inserts and deletes of T in reverse order; release all locks of T
```

Every lock may have to wait. After a wait, the operation computes its locks again, since the next key may have changed; locks that it got before the wait stay. Except for the instant lock of line L6, every lock is held until line L10. The instant lock is granted only when no other transaction holds any lock on the next key, and it is released at once. If the transaction already holds the next key, it keeps its lock.

The lock on $\mathrm{NEXT}(k)$ in a delete keeps the gap closed after the key is gone: the deleted key leaves a larger gap, which the next key now covers, and nobody may insert into it or read it until the deleting transaction ends. The X lock on the deleted key keeps readers of the key itself away.

## Example

**A phantom that waits.** The index holds the keys 2, 5 and 7. $T_1$ scans $[3, 6]$ twice, and $T_2$ inserts 4.

| step | event | locks after the step |
|---|---|---|
| 1 | $T_1$ scans $[3, 6]$: it S-locks 5, and NEXT(6) = 7; the result is (5) | 1: S 5, S 7 |
| 2 | $T_2$ inserts 4: the instant X lock on NEXT(4) = 5 conflicts with $T_1$, so $T_2$ waits | 1: S 5, S 7 |
| 3 | $T_1$ scans $[3, 6]$ again; the result is (5) again; $c_1$ | |
| 4 | $T_2$ gets the instant lock on 5, X-locks 4, and inserts it; $c_2$ | |

If the scan locked only the key 5 that it returned, then the insert of 4 would need only its own X lock on 4. It would run at step 2, and the second scan would return (4, 5): a phantom. The schedule would not be serializable, since $T_1$ would come both before and after $T_2$.

**A gap after a delete.** With the same keys, $T_1$ deletes 5: it X-locks 5 and NEXT(5) = 7. Now $T_2$ looks up 6. The key 6 is not there, so $T_2$ S-locks NEXT(6), which is now 7, and waits. If $T_1$ aborts, 5 comes back; if $T_1$ commits, 5 is gone. In both cases $T_2$ sees a state that a serial run gives.

**A deadlock.** $T_1$ and $T_2$ both scan $[3, 6]$, so both hold S on 5 and 7. Then $T_1$ inserts 4 and waits for the S lock of $T_2$ on 5, and $T_2$ inserts 6 and waits for the S lock of $T_1$ on 7. The lock manager must abort one of them.

## Correctness

The proof is on [the proof page](proofs/correctness.md). Each key value $v$ of the domain is a *slot*, which may be empty. A scan reads all slots in its range, a lookup reads one slot, and a successful insert or delete writes one slot. The *cover* of $v$ is $v$ if it is in the index, and $\mathrm{NEXT}(v)$ if it is not.

- **The cover invariant.** At every moment, each active transaction holds a lock on the current cover of every slot that it has used, and an X lock if it wrote the slot. Lines L2, L4, L5 and L8 lock the cover when an operation reads a slot, and lines L7 and L9 lock the new cover after a write. A cover can move only by an insert into the gap below it, which needs the instant X lock on it (line L6), or by a delete of the cover itself, which needs an X lock on it (line L9). So it can move only under a transaction that holds it in X, and that is never another holder.
- **No phantoms.** If two transactions use the same slot, one of them for a write, then both would hold a lock on its cover, one of them X. So the first one has ended before the second one uses the slot. The schedule of slot reads and writes is strict and conflict serializable in commit order, and every committed transaction gets the same results as in the serial run in commit order.

## Complexity

- **Point operations.** A lookup, insert or delete finds its key and the next key with one search of the index, $O(\log n)$ in a [B+ tree](/b-plus-tree/), and asks for one or two locks. In the code, a lock request compares with the holders of the key, up to $k$ of them, so an operation costs $O(\log n + k)$ expected time. The code keeps the keys in a sorted list and scans it, which is simpler and slower.
- **Scans.** A scan that returns $r$ keys takes $r + 1$ locks, so $O(\log n + (r + 1) k)$ expected time.
- **Space.** The lock table holds the $l$ locks that are held, $O(l)$; one scan adds one lock more than plain row locking.
- **Concurrency.** A lock on a key also blocks inserts into the gap below it. This can block more than the range that a scan asked for: with the keys 2, 5 and 7, a scan of $[3, 6]$ locks the key 7, so it also blocks a delete of 7, which it did not read. With the keys 2, 5 and 9, it locks 9 and blocks inserts of 7 and 8, outside its range.

## Properties

- **Serializable with respect to the results.** With locks held to the end, the transactions see the index as in a serial run, phantoms included (shown above).
- **Strict.** Every write holds its X lock to the end, so the schedules are strict and an abort needs no cascade.
- **Not deadlock free.** Scans followed by inserts into the same range can deadlock, as in the example. A [wait-for graph](/wait-for-graph/) or a timeout finds them.
- **Locks only keys.** A lock is asked for only on a key that is in the index at that moment, on EOF, or on the key that is being inserted. The lock table tests keys for equality and needs no predicate test.

## Variants and improvements

- **ARIES/KVL.** Mohan's method for B-trees locks key values, and it refines the durations of the locks of inserts and deletes; it also handles indexes with duplicate keys, where a key value has a list of row ids.
- **Previous-key locking.** The same idea with the gaps above the keys: a lock on a key covers the gap up to the next key, and inserts test the previous key. A key below all others plays the part of EOF.
- **Range lock modes.** Lomet (1993) treats the key and the gap beside it as separate resources and gives modes that lock one without the other, so that an insert into a gap does not wait for a reader of the key, and a reader of a key does not block the gap. SQL Server, for example, has modes of this kind for its serializable level.
- **Gap locks.** MySQL InnoDB, for example, uses next-key locks under its default level, and has gap locks that cover only the gap without the key.
- **Coarser locks.** [Multiple granularity locking](/multiple-granularity-locking/) can instead lock the whole table in S for a scan. This also stops phantoms, but it blocks every writer of the table.

## When to use it

Use key-range locking when a lock-based system must give serializable range scans on a B-tree, or must make "not found" stay true for the rest of a transaction, for example for a check of a unique key. It is the standard answer to the phantom problem in systems with two-phase locking. Where most transactions only read, multiversion schemes, for example [serializable snapshot isolation](/serializable-snapshot-isolation/), avoid the read locks; where the range is not a range of one index, a predicate or table lock is needed.

## Pitfalls

- **Forgetting the next key after a range.** A scan that locks only the keys that it returns lets an insert into the last gap through, and a lookup that finds nothing and locks nothing lets the key appear later.
- **Releasing the next-key lock of a delete.** If a delete releases its lock on the next key before the commit, another transaction can read the larger gap and then see the key come back at an abort.
- **Locking the next key too late.** The next key must be computed and locked in the same step as the insert or the read, under the latch of the page. After a wait, it must be computed again: the old next key may have been deleted, or a new key may lie in between.
- **The gap is larger than the range.** A lock on the next key blocks inserts into the whole gap below it, so a short scan near a sparse part of the index can block many inserts. Range lock modes reduce this.
- **The EOF key.** The gap after the last key needs a lock too. An index that has no EOF key lets phantoms appear at the end of the key space.

## Implementations

## History

Eswaran, Gray, Lorie and Traiger (1976) described phantoms, which locks on single rows cannot stop, and proposed predicate locks, which are costly to test. For indexes, Mohan (1990) described ARIES/KVL, which locks key values in a B-tree and closes each gap with a lock on the next key, with locks of instant and commit duration. Lomet (1993) treated keys and the ranges between them as separate lockable resources, and Graefe (2010) surveyed these methods and their later forms. MySQL InnoDB, for example, uses next-key locks, and SQL Server has key-range locks for its serializable level.

## References
