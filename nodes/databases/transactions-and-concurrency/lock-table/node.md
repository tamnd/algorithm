---
tag: J4XAN4
kind: data-structure
slug: lock-table
name: Lock table
aliases:
- lock manager
- lock compatibility matrix
area: databases/transactions-and-concurrency
level: intro
summary: "A hash table from each locked item to its granted group and a FIFO queue of waiting requests, with a compatibility matrix of lock modes. It is the core of a lock manager."
model: word-ram
complexity:
  vars: {g: the number of holders of the item, q: the number of requests that wait on the item, a: the number of waiting requests that a release grants, k: the number of active transactions, L: the number of granted and waiting requests in the table}
  time: {request: "O(1 + g + q) expected", release: "O(1 + (1 + a) g) expected", wait-for-graph: "O(k^2)"}
  space: {extra: "O(L)"}
prereqs: [hash-table, readers-writer-lock, two-phase-locking]
see_also: [strict-two-phase-locking, wait-for-graph, deadlock-detection, multiple-granularity-locking, key-range-locking, conservative-two-phase-locking, wait-die-and-wound-wait, starvation]
sources:
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: Chapter 7 (lock modes and the compatibility matrix) and Chapter 8 (lock implementation, the lock table with its granted and waiting requests, conversions, and deadlock detection)
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 3 (the implementation of a two-phase locking scheduler with a lock table, and deadlock detection with the waits-for graph)
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 4 (locking schedulers, lock conversions and deadlock handling)
---

A lock table is the data structure inside the lock manager of a database system. It is a [hash table](/hash-table/) keyed by the name of a data item. The entry of an item holds the *granted group*, the transactions that hold a lock on the item with their modes, and a FIFO *wait queue* of requests that cannot be granted yet. A *compatibility matrix* tells which modes can be held together by different transactions. A scheduler such as [two-phase locking](/two-phase-locking/) calls the table for every read and write, and the [wait-for graph](/wait-for-graph/) for deadlock detection is read from it.

## In plain words

Think of a desk with one card for each file in use. The card lists who uses the file now and how: reading, which many people can do at the same time, or writing, which needs the file alone. Below them, the card lists the people who wait, in the order they came.

When a person asks for a file, the clerk finds its card. If nobody waits and the new use goes with the current uses, the person gets the file. If not, the name goes at the end of the waiting list. When a person gives the file back, the clerk lets in people from the top of the list while each one goes with the uses that remain. A reader who wants to write goes to the front of the list.

If the waiting people make a closed circle, the clerk sends one away.

## The abstract type

The table holds locks of transactions on items. A lock has a mode from a finite set $M$. The modes come with:

- a *compatibility* relation: $\mathit{compat}(h, m)$ is true when a transaction can be granted mode $m$ on an item while another transaction holds mode $h$ on it;
- a *supremum* $\sup(a, b)$, the weakest mode that is at least as strong as $a$ and $b$, with $\mathit{compat}(\sup(a, b), m)$ true exactly when $\mathit{compat}(a, m)$ and $\mathit{compat}(b, m)$ are both true.

For shared (S) and exclusive (X) locks, the matrix is:

| held \ requested | S | X |
|---|---|---|
| S | yes | no |
| X | no | no |

and $\sup(S, X) = X$. The matrix of [multiple granularity locking](/multiple-granularity-locking/) has five modes, IS, IX, S, SIX and X, and the same table serves it.

The operations are:

- `request(T, x, m)`: ask for mode $m$ on $x$. The result is *granted* or *waits*. A request by a transaction that already holds mode $h$ on $x$ is a *conversion* to $\sup(h, m)$.
- `release(T, x)`: give up the lock of $T$ on $x$. The result is the list of waiting requests that this grants.
- `cancel(T)`: take back the waiting request of $T$, if there is one. A transaction that aborts while it waits needs this.
- `release_all(T)`: `cancel(T)` and then release every lock of $T$. Strict two-phase locking calls it at commit or abort.
- `waits_for()`: the edges $T \to U$ of the wait-for graph.

A transaction has at most one waiting request at a time, because it stops when a request waits.

## Representation

- **The hash table.** It maps an item to its *entry*. An item with no holder and no waiter has no entry, so the table holds only the items in use. Its size is $O(L)$ for $L$ granted and waiting requests.
- **The entry of an item.** It has the granted group, a map from a transaction to its mode; the *group mode*, the supremum of the granted modes, or none if the group is empty; and the wait queue, a list of requests $(T, m, \mathit{conversion})$ in which every conversion comes before every new request.
- **The lists of a transaction.** A map from each transaction to the set of items it holds locks on, and a map from each waiting transaction to the item it waits on. With them, `release_all` and `cancel` do not scan the whole table.

The test on line L6 compares the new mode with one group mode, not with each holder, because of the property of $\sup$. A conversion of $T$ must be compared with the supremum of the *other* holders, without the old mode of $T$, since a lock is never in conflict with another lock of the same transaction.

## Operations

```pseudo id=main
REQUEST(T, x, m)                              ▷ granted or waits
L1  e ← the entry of x; make an empty one if x has none
L2  if T holds mode h on x then                 ▷ a conversion
L3      if sup(h, m) = h then return granted     ▷ the lock T holds is enough
L4      if compat(the sup of the modes of the other holders, sup(h, m)) then
            set the mode of T to sup(h, m); return granted
L5      put (T, sup(h, m), conversion) into the queue after the last conversion
        return waits
L6  if the queue of e is empty and compat(group mode of e, m) then
        add (T, m) to the granted group; return granted
L7  append (T, m) to the queue of e; return waits

RELEASE(T, x)
L8  remove T from the granted group of x
L9  group mode ← the sup of the modes that are left
    WAKE(x)

WAKE(x)
L10 while the queue of x is not empty do
L11     r ← the head; if r.mode is not compatible with the group (without r.T, for a conversion) then stop
L12     remove r from the queue; grant r.mode to r.T; tell r.T to continue
L13 if x has no holder and no waiter then remove the entry of x
```

`cancel(T)` removes the request of $T$ from its queue and then calls WAKE, because the request it removes can be the head that blocks the others. `release_all(T)` calls `cancel(T)` and then RELEASE for each item of $T$.

**The wait-for graph.** For each waiting request of $T$ on $x$, add an edge $T \to U$ for each holder $U \ne T$ of $x$ whose mode is not compatible with the mode that $T$ waits for, and for each transaction $U$ with a request ahead of $T$ in the queue of $x$. The second kind of edge comes from FIFO order: $T$ cannot pass $U$, even if the modes of $T$ and $U$ are compatible. A cycle in this graph is a deadlock (see Correctness), and the detector finds it with [depth-first search](/depth-first-search/).

## Example

Take S and X modes on one item $x$.

| step | call | result | granted group of $x$ | queue of $x$ |
|---|---|---|---|---|
| 1 | request(1, x, S) | granted (L6) | 1:S | |
| 2 | request(2, x, S) | granted (L6) | 1:S, 2:S | |
| 3 | request(3, x, X) | waits (L7) | 1:S, 2:S | 3:X |
| 4 | request(4, x, S) | waits (L7) | 1:S, 2:S | 3:X, 4:S |
| 5 | request(1, x, X) | waits (L5) | 1:S, 2:S | 1:X, 3:X, 4:S |
| 6 | release(2, x) | grants 1:X | 1:X | 3:X, 4:S |
| 7 | release(1, x) | grants 3:X | 3:X | 4:S |
| 8 | release(3, x) | grants 4:S | 4:S | |

At step 4, S is compatible with the group mode S, but $T_4$ still waits, because $T_3$ waits ahead of it. If $T_4$ could pass, a stream of readers could keep $T_3$ out forever. At step 5, $T_1$ asks to convert its S lock to X. The conversion goes to the front of the queue, so it waits only for $T_2$. After step 5, the wait-for graph has the edges

$$1 \to 2, \quad 3 \to 1, \quad 3 \to 2, \quad 4 \to 1, \quad 4 \to 3.$$

There is no cycle. There is no edge $4 \to 2$: when $T_2$ leaves and nothing else changes, $T_4$ still waits for $T_1$ and $T_3$.

A conversion deadlock: $T_1$ and $T_2$ both hold S on $x$, and both ask for X. Each conversion waits for the S lock of the other one, so the graph has the cycle $1 \to 2 \to 1$. If the detector aborts $T_2$, `release_all(2)` releases its S lock, and WAKE grants X to $T_1$.

## Correctness

The table keeps three invariants after each operation:

1. **Safety.** The modes of two different transactions in a granted group are compatible.
2. **No lost wake-up.** If the queue of $x$ is not empty, its head cannot be granted now: some other holder has a mode that is not compatible with the mode of the head.
3. **Bookkeeping.** Each waiting transaction is in exactly one queue, at the item that it waits on.

Lines L4 and L6, and the grant in L12, add a mode only when it is compatible with the other holders, so they keep invariant 1. WAKE stops only when the queue is empty or the head does not fit, which gives invariant 2 after each release and cancel. A new request that waits at L7 or a conversion that waits at L5 becomes the head only when it does not fit.

From invariant 2 and the FIFO rule, every waiting transaction has at least one edge out of it in the wait-for graph: to an incompatible holder if it is the head, and to the head otherwise. Every edge is real: while $U$ keeps the lock or the place in the queue that gives the edge $T \to U$, the request of $T$ is not granted. And the edges are complete: if every $U$ with an edge $T \to U$ leaves the item, then $T$ becomes the head with only compatible holders, and WAKE grants it. So a set of waiting transactions in which nobody can ever continue contains a cycle, and each cycle is such a set. A scheduler that runs [strict two-phase locking](/strict-two-phase-locking/) on this table produces only conflict serializable and strict schedules, by the [two-phase locking theorem](/two-phase-locking-theorem/). The full proofs are on [the proof page](proofs/correctness.md).

## Complexity

The hash table gives the entry of an item in $O(1)$ expected time. With $g$ holders and $q$ waiting requests on the item:

| operation | time | notes |
|---|---|---|
| request, new | $O(1)$ expected | L6 compares with the stored group mode |
| request, conversion | $O(1 + g + q)$ expected | the sup of the other holders, and the place after the last conversion |
| release | $O(1 + g)$ expected, plus $O(g)$ per request it grants | the new group mode is a sup over the holders |
| release_all | the sum over the items of the transaction | |
| wait-for graph | $O(k^2)$ | each of the $k$ waiting transactions gets at most $g + q \le 2k$ edges |

A real lock manager keeps a count of the holders of each mode in the entry. Then the group mode and the sup of the other holders come from the counts in $O(|M|)$ time, a constant, and a request that does not wait costs $O(1)$ expected. The space is $O(L)$ for $L$ granted and waiting requests, plus $O(k)$ for the lists of the transactions.

## Variants

- **Update mode.** Many systems add a mode U for a read that will probably be followed by a write. Two U locks are not compatible, so two transactions that read with intent to write cannot both hold the item and then deadlock in their conversions to X, as in the example. Systems differ in whether a new S request is compatible with a held U lock.
- **Intention modes.** The five modes IS, IX, S, SIX and X of [multiple granularity locking](/multiple-granularity-locking/) use the same table with a $5 \times 5$ matrix. Lock names for key ranges, as in [key-range locking](/key-range-locking/), are also entries of the same table.
- **Lock escalation.** When one transaction holds too many row locks in one table, the lock manager replaces them with one lock on the table. This saves memory and can cause new waits.
- **Other wait rules.** A system can let a compatible new request pass the queue. That gives more concurrency and can starve a writer. A system can also refuse to wait: [wait-die and wound-wait](/wait-die-and-wound-wait/) abort one side by timestamp instead, so no wait-for graph is needed. A timeout instead of a graph also breaks deadlocks, with false positives.
- **Latches on the table.** In a multithreaded system the lock table is itself shared, so each bucket of the hash table has a short-term [mutex](/mutex/) (a latch). The latch protects the entry for the time of one call only.
- **Locks without waiting.** [Conservative two-phase locking](/conservative-two-phase-locking/) asks for all the locks of a transaction in one call and grants all or none, so a waiting transaction holds nothing.

## When to use it

Use a lock table in any scheduler that locks named items: two-phase locking and its variants, locking for B+ tree pages and key ranges, and locks on schema objects. It is the standard choice when transactions conflict often enough that waiting is cheaper than an abort and a restart. Where conflicts are rare, [optimistic concurrency control](/optimistic-concurrency-control/) avoids the cost of a table call for each access, and multiversion systems avoid locks for reads.

## Pitfalls

- **A lost wake-up.** A transaction that aborts while it waits must leave the queue through `cancel`, and `cancel` must call WAKE. If the cancelled request was the head, the requests behind it can fit now, and without WAKE they wait forever although nothing blocks them.
- **Conversions at the end of the queue.** If $T_1$ holds S and $T_3$ waits for X, a conversion of $T_1$ to X at the end of the queue waits for $T_3$, which waits for $T_1$. This is a deadlock that the table itself made. Put conversions before new requests.
- **A conversion compared with its own lock.** If line L4 compares the new mode with the full group mode, a transaction that holds S alone can never convert to X, because X is not compatible with its own S.
- **Edges only to the holders.** A wait-for graph with edges only to holders misses waits that come from FIFO order. Then the detector can fail to see a deadlock in which some transaction waits behind another waiter.
- **Empty entries.** An entry with no holder and no waiter must leave the hash table (L13), or the table grows with every item that was ever locked.
- **Hashed lock names.** Some systems lock a hash of the key instead of the key. Two different keys with the same hash then conflict, which is safe but gives false waits.

## Implementations

## History

Shared and exclusive locks, the compatibility matrix and lock conversions come from the System R work at IBM in the 1970s, where Gray, Lorie, Putzolu and Traiger also gave the intention modes of multiple granularity locking. Bernstein, Hadzilacos and Goodman (1987) describe a two-phase locking scheduler with a lock table and deadlock detection with the waits-for graph. Gray and Reuter (1993) describe a full lock manager, with the lock table as a hash table of lock headers, the granted and waiting requests of each lock, conversions, and deadlock detection.

## References
