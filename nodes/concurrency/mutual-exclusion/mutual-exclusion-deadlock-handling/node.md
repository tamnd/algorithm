---
tag: Z43BNF
kind: problem
slug: mutual-exclusion-deadlock-handling
name: Deadlock handling
aliases:
- deadlock prevention, avoidance, detection and recovery
- deadlock handling for locks
- wait-die
- wound-wait
area: concurrency/mutual-exclusion
level: core
summary: Keep programs that take several locks free of deadlock in practice, with lock order, trylock and back off, timeouts, a validator such as lockdep, or the wait-die and wound-wait rules.
history:
  year: 1978
  people: [Daniel J. Rosenkrantz, Richard E. Stearns, Philip M. Lewis II]
  note: Rosenkrantz, Stearns and Lewis gave the wait-die and wound-wait rules for distributed databases in 1978. Lock hierarchies go back to Havender (1968); run-time validators such as Linux lockdep are later practice.
prereqs: [lock-ordering, deadlock-detection, mutex]
see_also: [lock-ordering, deadlock-prevention, deadlock-detection, wait-for-graph, wait-die-and-wound-wait, two-phase-locking, livelock, deadlock]
sources:
  - paper: doi:10.1145/320251.320260
    title: Daniel J. Rosenkrantz, Richard E. Stearns and Philip M. Lewis II, System level concurrency control for distributed database systems, ACM Transactions on Database Systems 3(2), 1978, pages 178 to 198
    locator: the wait-die and wound-wait systems, which use transaction timestamps to decide whether a requester waits, dies or wounds the holder
  - url: "https://docs.kernel.org/locking/lockdep-design.html"
    title: The Linux kernel documentation, Runtime locking correctness validator
    locator: lock classes, the dependency rules between classes, and the report of a possible circular locking dependency
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems (1987)
    locator: Chapter 3, Two Phase Locking, the sections on deadlocks, with timeouts, detection on the waits-for graph and victim selection, and the timestamp based prevention schemes
  - book: isbn:9780321349606
    title: Brian Goetz and others, Java Concurrency in Practice (2006)
    locator: Chapter 10, Avoiding Liveness Hazards, the sections on lock-ordering deadlocks and on timed lock attempts
---

Deadlock handling, for a program or a system built on [mutexes](/mutex/) and other exclusive locks, is the practical problem of choosing a way to make sure that a group of processes that take several locks never ends in a [deadlock](/deadlock/), or that a deadlock that does happen is broken. The general theory, with the four [Coffman conditions](/coffman-conditions/), [prevention](/deadlock-prevention/), the [banker's algorithm](/banker-algorithm/) for avoidance, and [detection](/deadlock-detection/), is on those pages. This page is about the tools that lock code really uses: lock hierarchies, trylock with back off, timeouts, run-time validators, detection with abort, and the two timestamp rules of Rosenkrantz, Stearns and Lewis, wait-die and wound-wait, which are proved deadlock free below.

## In plain words

Programs that take two or more locks can get stuck: each one holds a lock that another one needs. There are a few common ways to stop this.

One way is to agree on an order and take locks only in that order. Another is to try a lock without waiting, and if it is busy, give back what you hold and start again. Another is to wait only for a limited time. Debug tools can watch the order in which a program takes locks and warn before anything gets stuck.

Databases often use a different rule. Each job gets a ticket number when it starts. When two jobs want the same lock, the ticket numbers decide who waits and who gives up and starts again. Because the older job always wins in the end, every job finishes.

## Definition

The model has $n$ asynchronous processes (threads, or transactions) in a sequentially consistent memory. A process may crash between steps. The shared objects are $m$ exclusive locks with the operations lock, unlock and trylock, and for transactions an abort that undoes the work of the process, releases all its locks and lets it restart. A process blocks only in a lock operation.

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ or $T_i, T_j$ | process (transaction) names; $i, j$ are indices |
| $m$ | the number of locks (the shared objects) |
| $k$ | the contention: the number of processes that ask for the same lock at the same time |
| $\mathit{ts}(T)$ | the timestamp of transaction $T$; a smaller timestamp is older |

**The problem.** Give a rule for lock requests (and perhaps for aborts) such that every execution has [deadlock freedom](/deadlock-freedom/) among the locks: there is never a set of processes each blocked on a lock held by another process of the set. A strong solution also gives [starvation freedom](/starvation-freedom/): every process that keeps trying eventually holds all the locks it needs. The cost of a solution is measured in the restrictions it puts on the code, the work done at each request, and the work thrown away by aborts and retries.

A wait among locks is an edge of the [wait-for graph](/wait-for-graph/), and with exclusive locks there is a deadlock exactly when that graph has a cycle. So every method below either keeps the graph acyclic or finds a cycle and breaks it.

## Variants

- **Threads with locks, no rollback.** Kernel and application code cannot undo its work, so it must prevent deadlock: a lock order, or trylock with a release of the locks it holds.
- **Transactions with rollback.** A database can abort a transaction and run it again. This allows detection with recovery, timeouts, and the timestamp rules.
- **Known lock sets.** If a process knows all its locks at the start, it can take them in order, or all at once (conservative locking).
- **Unknown lock sets.** If locks are found one at a time, as in a transaction that reads a row and then decides which other row to lock, a static order may be impossible, and the system needs aborts or a back off.
- **Distributed locks.** The wait-for graph is spread over sites. Detection then needs messages, as in the probe algorithm of Chandy, Misra and Haas on the [wait-for graph](/wait-for-graph/) page; the timestamp rules need no messages beyond the requests themselves, which was the motive of Rosenkrantz, Stearns and Lewis.

## Examples

**The basic case.** $T_1$ takes lock $x$ then $y$; $T_2$ takes $y$ then $x$. If each takes its first lock, each waits for the other. The simulator of the implementation confirms the deadlock with plain waiting, and also for three transactions with the cyclic lock lists $(x, y)$, $(y, z)$, $(z, x)$. With $\mathit{ts}(T_1) = 1 < \mathit{ts}(T_2) = 2$, the methods handle it as follows.

| method | what happens when $T_1$ holds $x$, $T_2$ holds $y$, and both ask for the other lock |
|---|---|
| lock order $x \prec y$ | cannot happen: $T_2$ must take $x$ first, so it waits for $T_1$ before it holds anything |
| trylock and back off | a trylock fails; that process releases its lock, waits a little and tries again |
| timeout | one of the waits times out; that process releases its locks and retries or reports an error |
| detection | the detector finds the cycle $T_1 \to T_2 \to T_1$ and aborts a victim |
| wait-die | $T_1$ (older) waits for $T_2$; $T_2$ (younger) asks for $x$, held by an older transaction, and dies |
| wound-wait | $T_1$ (older) wounds $T_2$, which aborts and releases $y$; $T_2$ restarts and waits for $T_1$ |

In both timestamp rules the younger transaction is the one that restarts, and it keeps its old timestamp.

**The timestamp rules.** A lock manager runs the following code for each request, commit and abort. A transaction asks for its locks one at a time and releases them all at its end, as in [strict two phase locking](/strict-two-phase-locking/).

```pseudo id=main
REQUEST(T, ℓ, rule)                   ▷ T asks for the exclusive lock ℓ
L1  if T is wounded then return ABORT
L2  if ℓ is free then give ℓ to T; return GOT
L3  H ← the holder of ℓ
L4  if rule = wait-die and ts(T) > ts(H) then return ABORT       ▷ the younger requester dies
L5  if rule = wound-wait and ts(T) < ts(H) then mark H wounded    ▷ H must abort
L6  T waits until it holds ℓ, or until it is wounded

RELEASE-ALL(T)                        ▷ at the end of T, by commit or abort
L7  for each lock ℓ held by T do
L8      give ℓ to its oldest waiter W that is not wounded, or free ℓ if there is none
L9      if rule = wait-die then mark wounded each other waiter of ℓ younger than W

COMMIT(T)
L10 if T is wounded then ABORT(T) else RELEASE-ALL(T)

ABORT(T)
L11 undo T; RELEASE-ALL(T); clear the mark of T; restart T with the same ts(T)
```

Line 9 applies the wait-die rule again for the waiters that now wait for a new holder: a waiter younger than the new holder would be waiting for an older transaction, which wait-die forbids, so it dies. Lines 4 and 9 together keep the invariant used in the proof.

**What the tests check.** For both rules, over all interleavings of the examples with two and with three transactions, there is no deadlock, every run commits all the transactions, and the wait-for graph keeps the shape of the proof in every state: under wait-die every edge goes from an older to a younger transaction, and under wound-wait every edge goes from a younger transaction to an older one, or to a wounded holder. Over 150 seeded random runs for each rule, with 2 to 4 transactions and random lock lists, every run commits all its transactions, and aborts do happen.

## Known algorithms

- **Lock hierarchies.** Rank the locks and take them in increasing rank; see [lock ordering](/lock-ordering/), which proves that no cycle of waits can form. Costs: a design rule that all the code must keep, and no help for locks found late.
- **Trylock and back off.** Take the first lock with lock, and each further one with trylock. On failure, release everything, wait for a short time, and start again. A process never waits while it holds a lock, so no cycle of waits can form. Costs: work is repeated, and processes that back off in lock step can retry forever, which is [livelock](/livelock/); a random delay, or [exponential backoff](/exponential-backoff/), makes this unlikely but does not exclude it. Trylock is also the tool for a late lock that goes against the order (the ACQUIRE-LATE template on the lock ordering page).
- **Timeouts.** Wait for a lock for at most a fixed time, as with a timed lock in Java or `pthread_mutex_timedlock` in POSIX threads, and treat a timeout as a failure: release and retry, or abort. A timeout also ends a wait for a process that has crashed while it holds a lock, which no graph method can see. Costs: a timeout does not show that there was a deadlock; a short limit aborts processes that were only slow, and a long one leaves a real deadlock in place for that long.
- **Run-time validators.** A validator such as Linux lockdep records, for each pair of lock classes, that one was taken while the other was held, and reports a dependency that closes a cycle, even in a run that did not deadlock. It finds wrong orders in testing; it does not resolve a deadlock at run time. The [lock ordering](/lock-ordering/) page has a small validator of this kind.
- **Detection and recovery.** Keep the wait-for graph, look for a cycle when a process waits or at intervals, and abort a victim on the cycle: for example the youngest transaction, or the one that has done the least work. See [deadlock detection](/deadlock-detection/). Costs: the graph and the check, and the lost work of the victim; a victim chosen badly again and again starves.
- **Wait-die.** When $T$ asks for a lock held by $H$: if $T$ is older, it waits; if it is younger, it dies (aborts and later restarts with its old timestamp). Older transactions wait for younger ones only.
- **Wound-wait.** When $T$ asks for a lock held by $H$: if $T$ is older, it wounds $H$ ($H$ aborts and releases its locks, and $T$ waits until then); if $T$ is younger, it waits. Younger transactions wait for older ones only, apart from short waits for a wounded holder.
- **Avoidance.** The [banker's algorithm](/banker-algorithm/) grants a request only if the state stays safe. It needs the maximum claim of each process in advance, so lock code almost never uses it.

### Wait-die and wound-wait are deadlock free

**Theorem 1 (wait-die).** Under wait-die, in every reachable state, every edge $T \to H$ of the wait-for graph has $\mathit{ts}(T) < \mathit{ts}(H)$. Hence the graph has no cycle, and there is no deadlock.

*Proof.* An edge $T \to H$ means that $T$ waits at line 6 for a lock $\ell$ that $H$ holds. The edge appears in one of two ways. If $T$ asked for $\ell$ while $H$ held it, then line 4 did not abort $T$, so $\mathit{ts}(T) < \mathit{ts}(H)$. If $T$ was already waiting for $\ell$ and $\ell$ passed to a new holder $W$ at line 8, then either $\mathit{ts}(T) < \mathit{ts}(W)$, or line 9 marked $T$ wounded; a wounded waiter leaves line 6 and aborts, so it is not blocked and its edge does not count. Timestamps do not change, so the inequality holds as long as the edge exists. Along any path of the graph the timestamps strictly increase, so no path returns to its start, and the graph is acyclic. With exclusive locks a deadlock would give a cycle of the wait-for graph, so there is none. $\square$

**Theorem 2 (wound-wait).** Under wound-wait, in every reachable state, every edge $T \to H$ whose holder $H$ is not wounded has $\mathit{ts}(T) > \mathit{ts}(H)$. Hence no set of blocked processes can be deadlocked.

*Proof.* Take an edge $T \to H$ for the lock $\ell$. If $T$ asked for $\ell$ while $H$ held it and $T$ was older, line 5 marked $H$ wounded, and the mark stays until $H$ aborts and releases $\ell$. If $T$ was younger, $\mathit{ts}(T) > \mathit{ts}(H)$. If $\ell$ passed to a new holder $W$ at line 8, $W$ is the oldest waiter, so every other waiter is younger than $W$. Now suppose a set $D$ of processes is deadlocked: every process of $D$ is blocked at line 6, and the holder of the lock it waits for is in $D$. A wounded process is never blocked, since line 6 ends when the process is wounded, so no process of $D$ is wounded. So every edge inside $D$ goes from a younger to an older transaction, timestamps strictly decrease along every path in $D$, and the edges of $D$ cannot form the cycle that a deadlock needs. $\square$

**Theorem 3 (no starvation).** Assume a fair scheduler, a finite number of transactions at any time, timestamps that grow with the start time and do not change on restart, and that a transaction that holds all its locks reaches its commit. Then under both rules every transaction commits.

*Proof sketch.* The oldest live transaction $T_0$ is never aborted: under wait-die it is older than every holder, so line 4 never fires for it and line 9 never marks it; under wound-wait only an older transaction can wound, and there is none. Each wait of $T_0$ is for a younger holder (wait-die) or for a wounded one (wound-wait), and by Theorems 1 and 2 the chain of waits from that holder ends at a process that can step; with a fair scheduler, and since the system is deadlock free, the holder ends, by commit or abort, in finite time, and $T_0$ gets the lock by line 8. So $T_0$ commits. New transactions are younger, so after $T_0$ the next oldest becomes the oldest, and so on: every transaction becomes the oldest after finitely many commits, and then commits. $\square$

The fairness assumption matters. A scheduler that always runs the youngest transaction under wait-die can keep it dying and restarting forever while the older one never gets a step; the test of the implementation uses a round robin order for this reason.

## Bounds

| method | work per lock request | can abort | can livelock | needs |
|---|---|---|---|---|
| lock order | $O(1)$, or $O(\log m)$ to sort a known set | no | no | a rank on the locks |
| trylock and back off | $O(1)$ per try | releases and retries | yes, unless delays are random | nothing |
| timeout | $O(1)$ plus a timer | yes, also with no deadlock | possible | a time limit |
| detection on wait | $O(n + e)$ for a search from the new edge, $e$ the number of edges | the victim | no | the wait-for graph |
| wait-die, wound-wait | $O(1)$: one comparison of timestamps | yes, also with no deadlock | no, with a fair scheduler | timestamps, rollback |

With exclusive locks each blocked process waits for one holder, so the wait-for graph has at most $n$ edges and a search from a new edge takes $O(n)$ time. The timestamp rules pay for their constant cost in aborts: they abort when a wait would only go against the timestamp order, not only when it would close a cycle. Under wait-die a young transaction can die many times on the same lock while the older holder runs, once per attempt; under wound-wait a younger requester waits instead, and a transaction is aborted only when an older one asks for a lock it holds.

## Reductions

- Every method maps to the [wait-for graph](/wait-for-graph/). Prevention keeps it acyclic for all executions, detection keeps it acyclic by removing a vertex when a cycle appears, and timeouts remove long waits without looking at the graph.
- Lock ordering and the timestamp rules are two forms of one idea: fix a strict order and allow only waits that respect it. Lock ordering orders the locks, statically; wait-die and wound-wait order the transactions, by timestamp, and turn each wait against the order into an abort.
- Trylock and back off removes the hold and wait condition, and timeouts and the wounds of wound-wait add preemption; see the [Coffman conditions](/coffman-conditions/) and [deadlock prevention](/deadlock-prevention/).
- Checking that a given program cannot deadlock, over all its interleavings, is [deadlock freedom checking](/deadlock-freedom-checking/), a model checking problem; the simulator of the implementation does this by brute force for small cases.

## Applications

- **Operating system kernels.** Locks follow a documented order, and lockdep checks it in debug builds of Linux. Kernel code cannot roll back, so it relies on prevention.
- **Application code.** Java code orders locks by a key, or uses a timed tryLock and backs off; see [lock ordering](/lock-ordering/).
- **Database systems.** Lock managers for [two phase locking](/two-phase-locking/) usually detect deadlocks on a wait-for graph and abort a victim, often after a wait has lasted some time, and many also have a lock wait timeout. Wait-die and wound-wait suit distributed databases, where a global wait-for graph is expensive; the [wait-die and wound-wait](/wait-die-and-wound-wait/) page treats them as database algorithms.
- **Transactional memory.** [Contention management](/contention-management/) in [software transactional memory](/software-transactional-memory/) faces the same choice between waiting and aborting, and some contention managers use timestamps in the same way.

### History

Havender (1968) proposed ordered resource classes for OS/360, the root of lock hierarchies. Coffman, Elphick and Shoshani (1971) and Holt (1972) set out prevention, avoidance and detection for operating systems. For distributed databases, Rosenkrantz, Stearns and Lewis (1978) gave the wait-die and wound-wait systems, in which a timestamp fixed at the start of a transaction decides every conflict, so that no site needs a global view of the waits. Run-time validators of lock order, such as lockdep in the Linux kernel, came later.

## References
