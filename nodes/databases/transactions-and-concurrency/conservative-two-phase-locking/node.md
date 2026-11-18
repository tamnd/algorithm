---
tag: CS6AB2
kind: algorithm
slug: conservative-two-phase-locking
name: Conservative two-phase locking
aliases:
- static 2PL
- conservative 2PL
area: databases/transactions-and-concurrency
level: core
summary: "Two-phase locking in which a transaction declares its read and write sets and gets all its locks at once before its first action. A waiting transaction holds nothing, so there is no deadlock."
solves: [concurrency-control]
model: word-ram
complexity:
  vars: {s: the number of items that one transaction declares, w: the number of waiting transactions, k: the number of active transactions}
  time: {per-admission-pass: "O(w s k) expected"}
  space: {extra: "O(k s)"}
properties: {deterministic: true, online: true}
prereqs: [two-phase-locking, lock-table, deadlock-prevention]
see_also: [two-phase-locking-theorem, strict-two-phase-locking, coffman-conditions, wait-for-graph, wait-die-and-wound-wait, lock-ordering, calvin-deterministic-transactions, starvation]
sources:
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 3 (conservative 2PL with predeclared read and write sets, and strict 2PL)
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 4 (variants of two-phase locking, among them conservative 2PL)
  - paper: "J. W. Havender, Avoiding deadlock in multitasking systems, IBM Systems Journal 7(2), 1968, pages 74 to 84"
    locator: the rule that a task requests all its resources together, which prevents deadlock
---

Conservative two-phase locking, also called static 2PL, is a form of [two-phase locking](/two-phase-locking/) in which each transaction declares, when it begins, the items it will read and the items it will write. The scheduler then grants all its locks in one step, or none of them. A transaction that cannot get all its locks waits and holds nothing. So no transaction ever waits while it holds a lock, one of the four [Coffman conditions](/coffman-conditions/) never holds, and there are no deadlocks. Every transaction takes its last lock before its first action, so it is two-phase, and the schedule is conflict serializable in the order in which the transactions got their locks. The price is that the read and write sets must be known in advance, and that locks are held from the start.

## In plain words

Think of a kitchen where each cook must say, before starting a dish, which pots and knives the dish needs. The cook gets all of them at once, or waits with empty hands until all of them are free. A cook never holds one pot while waiting for another, so two cooks can never each hold what the other one wants.

A cook who waits keeps a place in a line. A new cook who wants one of the same tools may not take it first, so nobody waits forever. Because each cook has every tool before the first step, the kitchen works as if the cooks had cooked one after the other, in the order in which they got their tools.

## The problem

The input is a set of transactions, each given as a program of reads $r_i(x)$ and writes $w_i(x)$ followed by a commit $c_i$ or an abort $a_i$. The actions arrive interleaved, and the scheduler decides when each transaction may start. The scheduler must make the committed projection of the output schedule [conflict serializable](/conflict-serializability/), and it should avoid deadlocks, so that it never has to abort a transaction to break one.

Here the scheduler knows the whole read set and write set of a transaction when the transaction begins. This is the main assumption of the method, and it is what basic two-phase locking does not need. The model is one site with a [lock table](/lock-table/) in main memory, with S (shared) and X (exclusive) locks: two locks of different transactions on the same item conflict unless both are S.

## The algorithm

```pseudo id=main
BEGIN(T, program)
L1  L(T) ← {(x, X) : T writes x} ∪ {(x, S) : T reads x and does not write it}
L2  append T to the wait list W
L3  ADMIT()

ADMIT()                                          ▷ after each begin and each release
L4  for each T in W, in order of arrival do
L5      if each (x, m) in L(T) conflicts with no lock that another transaction holds,
           and with no lock that a transaction before T in W wants then
L6          remove T from W; grant all of L(T) to T     ▷ the lock point of T
        else remember the locks of T as wanted

ACCESS(T, p(x))                                 ▷ p is r or w
L7  check that T holds a lock on x that covers p, then run p(x)
L8  if not strict and T has no later access to x then release x; ADMIT()

END(T)                                          ▷ c or a
L9  release all locks of T; ADMIT()
```

The scheduler runs actions of admitted transactions only. A transaction that reads and writes the same item gets X at once, so there are no lock conversions. The test of line L5 against the earlier waiters is a choice of this page that keeps the wait list fair: a new transaction can pass a waiter only when the two do not conflict. Without it, a stream of readers could keep a writer waiting forever.

The flag *strict* selects one of two release rules. With strict = true, every lock is held until commit or abort (line L9), which is conservative strict 2PL. With strict = false, a lock is released after the last access of the transaction to the item (line L8). The transaction is still two-phase, because its lock point came before its first action.

## Example

**Admission in order.** Let $T_1 = r_1(x)\, c_1$, $T_2 = r_2(y)\, w_2(x)\, c_2$, $T_3 = r_3(x)\, c_3$ and $T_4 = w_4(z)\, c_4$ begin in this order.

| step | event | locks held | wait list |
|---|---|---|---|
| 1 | $T_1$ begins and gets S on $x$ | 1: S $x$ | |
| 2 | $T_2$ begins; X on $x$ conflicts with $T_1$, so it gets nothing | 1: S $x$ | 2 |
| 3 | $T_3$ begins; S on $x$ fits $T_1$ but conflicts with the wanted X of $T_2$ | 1: S $x$ | 2, 3 |
| 4 | $T_4$ begins and gets X on $z$; it conflicts with nobody | 1: S $x$; 4: X $z$ | 2, 3 |
| 5 | $T_1$ ends; $T_2$ gets S on $y$ and X on $x$ | 2: S $y$, X $x$; 4: X $z$ | 3 |
| 6 | $T_2$ ends; $T_3$ gets S on $x$ | 3: S $x$; 4: X $z$ | |

At step 2, $T_2$ does not take S on $y$ while it waits for $x$. After step 4 the [wait-for graph](/wait-for-graph/) has the edges $2 \to 1$ (a held lock) and $3 \to 2$ (an earlier waiter). The lock points are in the order $T_1, T_4, T_2, T_3$.

**The deadlock of basic 2PL.** Let $T_1 = r_1(x)\, w_1(y)\, c_1$ and $T_2 = r_2(y)\, w_2(x)\, c_2$, with the actions offered in the order $1, 2, 1, 2, 1, 2$. Under basic 2PL, $T_1$ locks $x$, $T_2$ locks $y$, and each then waits for the other: a deadlock. Under conservative 2PL, $T_1$ gets S on $x$ and X on $y$ at once. $T_2$ needs X on $x$ and S on $y$, so it waits with nothing. The output is $r_1(x)\, w_1(y)\, c_1\, r_2(y)\, w_2(x)\, c_2$, a serial schedule.

**Early release.** Let $T_1 = w_1(x)\, r_1(y)\, c_1$ and $T_2 = r_2(x)\, c_2$, offered in the order $1, 2, 2, 1, 1$. With strict = false, $T_1$ releases $x$ right after $w_1(x)$, since it does not touch $x$ again. $T_2$ is admitted, and the output is $w_1(x)\, r_2(x)\, c_2\, r_1(y)\, c_1$. It is conflict serializable, but not [recoverable](/recoverable-schedule/): $T_2$ read from $T_1$ and committed first. With strict = true, $T_2$ waits until $c_1$, and the output is $w_1(x)\, r_1(y)\, c_1\, r_2(x)\, c_2$.

## Correctness

There are four claims. The proofs are on [the proof page](proofs/correctness.md).

- **Serializability.** Each transaction gets all its locks before its first action and releases none before then, so every transaction is two-phase, and its lock point is the moment of line L6. By the [two-phase locking theorem](/two-phase-locking-theorem/), the committed projection is conflict equivalent to the serial schedule in the order of the lock points, which is the order of admission.
- **No deadlock.** A waiting transaction holds no lock. An edge $T \to U$ of the wait-for graph goes from a waiter to a holder, or from a waiter to an earlier waiter. A holder has no edge out of it, because it does not wait, and the edges between waiters go back in the order of arrival. So the graph has no cycle.
- **No starvation.** The first waiter conflicts with no earlier waiter, so it waits only for holders. A new transaction that conflicts with it is not admitted before it. The holders never wait, so if every admitted transaction ends, the first waiter is admitted. By induction along the wait list, every transaction is admitted.
- **Strictness.** With strict = true, every X lock is held until the end of its transaction, so the output schedule is [strict](/strict-schedule/).

## Complexity

- **Admission.** One pass of ADMIT looks at each of the $w$ waiters and each of its $s$ declared locks. In the code, each lock is compared with the holders of its item, up to $k$ of them, so a pass costs $O(w s k)$ expected time. With a count of the holders of each mode in each entry of the lock table, as in a real lock manager, each test costs $O(1)$ and a pass costs $O(w s)$.
- **Access.** A read or write costs $O(1)$ expected time for the check of line L7.
- **Space.** The declared lock sets of the active transactions take $O(k s)$.
- **Concurrency.** A transaction holds each lock from before its first action to its end (strict) or to its last access to the item. Basic 2PL takes each lock just before the first access to its item, so it holds locks for a shorter time, and conservative 2PL allows less concurrency. On the other side, it never wastes work on deadlock victims.

## Properties

- **Output class.** Conflict serializable, in the order of admission. With strict = true, also strict, so recoverable and free of cascading aborts.
- **Deadlock free and starvation free.** Shown above; no wait-for graph is needed, and no transaction is aborted by the scheduler.
- **Needs knowledge in advance.** The read and write sets must be known when the transaction begins.
- **Admits fewer schedules than basic 2PL.** Every schedule of conservative 2PL is a schedule of basic 2PL, since a transaction may always take its locks early. The converse is false: in the deadlock example, basic 2PL can also produce the serial output, but it lets $r_1(x)\, r_2(y)$ run concurrently first, which conservative 2PL never does.

## Variants and improvements

- **Conservative strict 2PL.** The form with strict = true. It is deadlock free and gives strict schedules.
- **Ordered locking.** Instead of all locks at once, a transaction takes its locks one at a time in a fixed global order of the items ([lock ordering](/lock-ordering/)). It also needs the lock set in advance and also prevents deadlock, because a cycle of waits would need an item order with a cycle. A transaction then waits while it holds locks, but it holds them for less time.
- **Deterministic databases.** [Calvin](/calvin-deterministic-transactions/) orders the transactions first and then gives each one its full lock set in that order. A transaction whose read set depends on the data first runs a reconnaissance step to find its set, and it restarts if the set changed.
- **Wait-free alternatives.** [Wait-die and wound-wait](/wait-die-and-wound-wait/) also prevent deadlocks, without the read and write sets, but they abort transactions instead.

## When to use it

Use conservative 2PL when the read and write sets are known when a transaction starts: stored procedures with fixed keys, batch jobs, and systems that order transactions in advance. It suits workloads in which a deadlock abort would be expensive, for example long transactions, or systems that cannot restart a transaction. Do not use it for interactive transactions whose next read depends on what they have read, or for queries whose sets come from a scan of an index: the scheduler would have to lock a superset, for example the whole table.

## Pitfalls

- **An undeclared access.** A transaction that touches an item it did not declare, or writes an item it declared only for reading, breaks the method. Line L7 must reject the access; an upgrade at that point could wait while holding locks and bring deadlocks back.
- **A superset of the real set.** If the sets are not known exactly, the transaction must declare a superset. This is safe but holds more locks for longer.
- **Starvation without the FIFO test.** If line L5 compares only with the holders, a transaction that needs many items can wait forever while smaller transactions keep one of its items busy.
- **Early release and recovery.** With strict = false the schedules are serializable but may not be recoverable, as in the example. Use strict = true when transactions can abort.
- **All or nothing must be atomic.** The test of line L5 and the grant of line L6 must be one step of the lock manager. If another transaction can take a lock between the test and the grant, a transaction ends up holding a part of its set while it waits.

## Implementations

## History

Havender (1968) proposed, for the OS/360 operating system, that a task should request all its resources together to prevent deadlock. In databases the same rule, with read and write sets declared in advance, became the static or conservative form of two-phase locking. Bernstein, Hadzilacos and Goodman (1987) present it as conservative 2PL beside basic and strict 2PL, and Weikum and Vossen (2001) list it among the variants of 2PL. Deterministic database systems such as Calvin (2012) use the same idea of taking the full lock set of a transaction in a fixed order.

## References
