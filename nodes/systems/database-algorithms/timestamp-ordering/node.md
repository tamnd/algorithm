---
tag: X0WMGA
kind: algorithm
slug: timestamp-ordering
name: Timestamp ordering
aliases:
- basic timestamp ordering
- timestamp ordering concurrency control
area: systems/database-algorithms
level: core
summary: "Give each transaction a timestamp at start and keep, per item, the largest read and write timestamps. An action that arrives too late aborts its transaction. No locks, no deadlocks."
solves: [concurrency-control]
model: word-ram
complexity:
  vars: {d: the number of items, n: the number of actions}
  time: {per-action: "O(1)", total: "O(n)"}
  space: {extra: "O(d)"}
properties: {deterministic: true, online: true}
prereqs: [conflict-serializability, concurrency-control]
see_also: [thomas-write-rule, two-phase-locking, multiversion-concurrency-control, optimistic-concurrency-control, wait-die-and-wound-wait, conflict-graph, lamport-clocks, tl2]
sources:
  - paper: doi:10.1145/356842.356846
    title: Philip A. Bernstein and Nathan Goodman, Concurrency control in distributed database systems, ACM Computing Surveys 13(2), 1981, pages 185 to 221
    locator: the section on timestamp ordering (the basic T/O rules for reads and writes with read and write timestamps, and the variants built on them)
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 4 (basic timestamp ordering, strict TO, the Thomas write rule and conservative TO)
  - paper: doi:10.1145/320071.320076
    title: Robert H. Thomas, A majority consensus approach to concurrency control for multiple copy databases, ACM Transactions on Database Systems 4(2), 1979, pages 180 to 209
    locator: the use of timestamps on data items to order updates, and the rule that an obsolete update is ignored
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 4 (nonlocking schedulers, timestamp ordering)
---

Timestamp ordering (TO) is a [concurrency control](/concurrency-control/) method that fixes the serial order in advance: the order of the transactions' start timestamps. Each item $x$ remembers the largest timestamp of a transaction that read it, $\mathrm{rts}(x)$, and that wrote it, $\mathrm{wts}(x)$. A read or write that would break the timestamp order, because a younger transaction has already done a conflicting action on $x$, is rejected, and its transaction aborts and restarts with a new timestamp. Every accepted pair of conflicting actions is then in timestamp order, so the committed result is [conflict serializable](/conflict-serializability/) in timestamp order. TO takes no locks and so has no deadlocks. The basic rules are from the survey of Bernstein and Goodman (1981); the idea of timestamps on items goes back to Thomas (1979) and Reed (1978).

## In plain words

Every transaction gets a ticket number when it starts. The system promises that the result will look as if the transactions had run one at a time in ticket order.

Each piece of data remembers the highest ticket that has read it and the highest ticket that has written it. When a transaction with ticket 5 wants to read something that ticket 7 has already written, it is too late: in ticket order it should have read the old value, which is gone. So ticket 5 is cancelled and starts again with a new, higher ticket. The same happens when ticket 5 wants to write something that ticket 7 has already read or written. Nobody ever waits for a lock, so nobody can get stuck in a circle of waiting, but some work is thrown away.

## The problem

The input is a stream of actions $r_i(x)$ and $w_i(x)$ from concurrent transactions. The scheduler must accept, delay or reject each action so that the committed projection of the output is conflict serializable. Two actions conflict if they are in different transactions, touch the same item, and at least one is a write. TO solves it by choosing the equivalent serial order in advance and enforcing it item by item. Timestamps must be unique and increasing; in a distributed system they can be [Lamport clock](/lamport-clocks/) values with the site number as a tie breaker.

## The algorithm

When transaction $T_i$ starts, it gets $\mathrm{ts}(T_i)$ from a counter. For each item, $\mathrm{rts}(x)$ and $\mathrm{wts}(x)$ start at $0$.

```pseudo id=main
TO-READ(T_i, x)
L1  if ts(T_i) < wts(x) then reject: a younger transaction wrote x; go to L5
L2  run r_i(x); rts(x) ← max(rts(x), ts(T_i))

TO-WRITE(T_i, x)
L3  if ts(T_i) < rts(x) or ts(T_i) < wts(x) then reject: a younger transaction read or wrote x; go to L5
L4  run w_i(x); wts(x) ← ts(T_i)

ON-REJECT(T_i)
L5  abort T_i, undo its writes, and restart it with a new timestamp
```

A transaction that reads and then writes the same item passes its own read, since $\mathrm{ts}(T_i) = \mathrm{rts}(x)$ is not smaller. The restart must use a new timestamp: with the old one, the same late action would be rejected again. The [Thomas write rule](/thomas-write-rule/) changes one case of line L3: a write that is late only because of a younger *write* (and not a younger read) is skipped instead of rejected.

## Example

**A schedule that TO accepts and 2PL cannot produce.** Let the transactions start in the order $T_3, T_1, T_2$, so $\mathrm{ts}(T_3) = 1$, $\mathrm{ts}(T_1) = 2$ and $\mathrm{ts}(T_2) = 3$, and take $S = r_3(z)\ r_1(x)\ w_2(x)\ w_3(y)\ w_1(y)$.

| action | test | result | stamps after |
|---|---|---|---|
| $r_3(z)$ | $1 \ge \mathrm{wts}(z) = 0$ | accept | $\mathrm{rts}(z) = 1$ |
| $r_1(x)$ | $2 \ge \mathrm{wts}(x) = 0$ | accept | $\mathrm{rts}(x) = 2$ |
| $w_2(x)$ | $3 \ge \mathrm{rts}(x) = 2$, $3 \ge \mathrm{wts}(x) = 0$ | accept | $\mathrm{wts}(x) = 3$ |
| $w_3(y)$ | $1 \ge 0$, $1 \ge 0$ | accept | $\mathrm{wts}(y) = 1$ |
| $w_1(y)$ | $2 \ge \mathrm{rts}(y) = 0$, $2 \ge \mathrm{wts}(y) = 1$ | accept | $\mathrm{wts}(y) = 2$ |

All actions pass, and $S$ is conflict equivalent to $T_3 T_1 T_2$, the timestamp order. Under [two-phase locking](/two-phase-locking/), $T_1$ would have to release $x$ before $w_2(x)$ and lock $y$ after $w_3(y)$, which breaks the two-phase rule.

**A schedule that 2PL accepts and TO rejects.** $S' = r_2(z)\ w_1(x)\ c_1\ r_2(x)\ c_2$, where $T_2$ starts first. Under 2PL, $T_1$ locks $x$, writes and commits, and then $T_2$ reads $x$; the result is serial, $T_1 T_2$. Under TO, $\mathrm{ts}(T_2) = 1 < \mathrm{wts}(x) = 2$ at $r_2(x)$, so $T_2$ is rejected: in timestamp order it should have read $x$ before $T_1$ wrote it. So 2PL and TO accept incomparable sets of schedules.

**A late write.** In $r_1(y)\ r_2(x)\ w_1(x)$ with $T_1$ older, the write $w_1(x)$ finds $\mathrm{rts}(x) = 2 > 1$: the younger $T_2$ has read the old value, which would be wrong in the order $T_1 T_2$. $T_1$ is rejected and restarts as a new, youngest transaction.

## Correctness

The proof file has the details. The stamps $\mathrm{rts}(x)$ and $\mathrm{wts}(x)$ never decrease, and they bound the timestamps of all accepted reads and writes of $x$. So when an action $q_j(x)$ passes the test, every earlier accepted action $p_i(x)$ of another transaction that conflicts with it has $\mathrm{ts}(T_i) < \mathrm{ts}(T_j)$. Every edge of the [conflict graph](/conflict-graph/) of the committed projection goes from a smaller to a larger timestamp, so the graph is acyclic and the timestamp order is an equivalent serial order. Conversely, if timestamps are given at start, TO passes a schedule unchanged exactly when all its conflicts follow the start order.

## Complexity

- **Per action.** One or two comparisons and one update of a stamp: $O(1)$ time, with a hash table from items to stamps.
- **Space.** Two stamps per item, $O(d)$. Systems keep stamps only for recently used items and use a lower bound for the rest.
- **Work lost.** The real cost is in restarts. A rejected transaction loses everything it did, and under heavy conflict TO restarts much more than locking, especially for long transactions, which have the oldest timestamps when they finish.

## Properties

- **Deadlock-free.** Basic TO never waits, so there is no [deadlock](/deadlock/). Strict TO waits only for older transactions, so it also cannot deadlock.
- **Fixed serial order.** The order is chosen at start, not discovered during the run. This is easy to use across sites, since each site enforces the same order without talking to the others.
- **Not recoverable in the basic form.** Basic TO lets a transaction read a value written by a transaction that has not committed. If the writer aborts later, the reader must abort too, and if the reader has already committed, the schedule is not recoverable.
- **Starvation is possible.** A restart gets a new timestamp, so a long transaction can be rejected again and again by shorter, younger ones. Locking schemes such as [wait-die and wound-wait](/wait-die-and-wound-wait/) keep the old timestamp on restart for exactly this reason; TO cannot, because its timestamps are the serial order.
- **Incomparable with 2PL.** Each accepts schedules that the other rejects (see the examples and the [concurrency control](/concurrency-control/) page).

## Variants and improvements

- **Strict TO.** Delay $r_i(x)$ and $w_i(x)$ while the transaction that wrote $\mathrm{wts}(x)$ has not committed or aborted. Schedules become strict, and waits go only from younger to older transactions, so no deadlock forms.
- **Thomas write rule.** Skip a write that is older than $\mathrm{wts}(x)$ but not older than $\mathrm{rts}(x)$, instead of rejecting it. It accepts more schedules, which are view serializable but not always conflict serializable. See [Thomas write rule](/thomas-write-rule/).
- **Multiversion TO.** Keep the old versions of each item. A read with timestamp $t$ reads the version with the largest write timestamp at most $t$, so reads are never rejected; a write is rejected only if a younger transaction has already read the version it would replace. Reed's 1978 thesis gave this scheme; see [multiversion concurrency control](/multiversion-concurrency-control/).
- **Conservative TO.** Each site waits until it has seen all older operations from every other site before it runs an operation, so nothing is ever rejected. It needs the operations to arrive in timestamp order on each channel.
- **Transactional memory.** [TL2](/tl2/) and other STMs with a [global version clock](/global-version-clock/) give each transaction a read timestamp at start and check that every location it reads has a version no larger than that timestamp. This is the read rule of TO. The write side differs: TL2 locks its write set at commit and validates its read set, so it decides at commit time like [optimistic concurrency control](/optimistic-concurrency-control/).

## When to use it

Use TO when deadlocks must be impossible, when an order fixed at start is useful (for example across sites with synchronized clocks), and when conflicts are rare enough that restarts are cheap. In modern systems the plain form is rare; its ideas live on in multiversion TO, in timestamp-based [optimistic](/optimistic-concurrency-control/) schemes, and in transactional memory.

## Pitfalls

- **Restarting with the old timestamp.** The late action would be rejected again forever. TO must give a new timestamp on restart; contrast wait-die and wound-wait, which must keep the old one.
- **Dirty reads.** Basic TO accepts a read of an uncommitted write. Add the strict rule, or the recovery system has to handle cascading aborts.
- **Two stamps, not one.** Checking writes only against $\mathrm{wts}(x)$ misses the case where a younger transaction has read $x$; that read would then see a value that the serial order says it should not have seen.
- **Timestamps are not wall clocks.** Two transactions must never get the same timestamp; break ties by site or thread number.
- **The name "TO".** The short name is used for other things as well; in a text about databases it means this method.

## Implementations

## History

Thomas (1979) used timestamps on data items in a majority consensus protocol for replicated databases, with the rule that an update older than the current value is ignored. Reed's 1978 MIT thesis built multiversion timestamp ordering. Bernstein and Goodman's 1981 survey of distributed concurrency control organized the methods into locking, timestamp ordering and combinations, and stated the basic T/O rules with read and write timestamps that are used here. Bernstein, Hadzilacos and Goodman (1987) gave the textbook treatment with strict TO and conservative TO.

## References
