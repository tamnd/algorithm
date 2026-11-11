---
tag: GCR25F
kind: algorithm
slug: karma-contention-manager
name: Karma contention manager
aliases:
- Karma
area: concurrency/transactional-memory
level: research
summary: A contention manager that ranks a transaction by the objects it has opened, over all its attempts; it aborts an enemy once its tries exceed the priority gap. It has no progress guarantee.
complexity:
  vars: {n: the number of transactions, d: "the enemy's priority minus the caller's, at the first conflict", l: the number of objects the enemy still opens}
  steps: {decision: Θ(1), wait: O(d + l)}
  space: {shared: Θ(n)}
properties: {deterministic: true, obstruction_free: true, livelock_free: false, starvation_free: false}
history:
  year: 2004
  people: [William N. Scherer III, Michael L. Scott]
  note: Scherer and Scott gave Karma among the managers for DSTM in 2004 and described it again at PODC 2005, where it led to Polka.
prereqs: [contention-management, livelock]
see_also: [greedy-contention-manager, polite-contention-manager, polka-contention-manager, dstm, obstruction-freedom, exponential-backoff, transaction-abort, starvation]
sources:
  - paper: doi:10.1145/1073814.1073861
    title: "William N. Scherer III and Michael L. Scott, Advanced contention management for dynamic software transactional memory, PODC 2005, pp. 240 to 248"
    locator: Section 3.1 (the DSTM manager interface) and Section 3.2 (Karma, and its variant Eruption)
  - paper: "William N. Scherer III and Michael L. Scott, Contention management in dynamic software transactional memory, PODC Workshop on Concurrency and Synchronization in Java Programs (CSJP), 2004"
    locator: a comparison of many DSTM contention managers, among them Karma and Polite
  - paper: doi:10.1145/1073814.1073863
    title: "Rachid Guerraoui, Maurice Herlihy and Bastian Pochon, Toward a theory of transactional contention managers, PODC 2005, pp. 258 to 264"
    locator: Section 6 (why Karma gives no worst-case guarantee)
  - paper: doi:10.1145/872035.872048
    title: "Maurice Herlihy, Victor Luchangco, Mark Moir and William N. Scherer III, Software transactional memory for dynamic-sized data structures, PODC 2003, pp. 92 to 101"
    locator: DSTM and its contention manager module
---

The **Karma contention manager** resolves conflicts in an obstruction-free STM such as [DSTM](/dstm/) by the amount of work each transaction has invested. The **priority** of a transaction is the number of objects it has opened, summed over all its attempts: it grows by one at each open, it is kept when the transaction is aborted, and it is reset to zero when the transaction commits. When transaction $A$ meets an active enemy $B$, $A$ aborts $B$ once the number of times $A$ has tried to open this object exceeds the difference $\mathrm{prio}(B) - \mathrm{prio}(A)$; until then it backs off for a fixed interval. Scherer and Scott designed Karma in 2004; it works well in practice but gives no guarantee of progress.

## In plain words

When two transactions want the same object, Karma lets the one that has done more work win, because aborting it would waste more. Work is counted in objects opened. A transaction that is aborted keeps its count, so each time it fails it starts the next attempt with more weight. A short transaction that keeps losing to a long one therefore builds up priority and wins in the end.

The loser does not wait for ever. Each time it asks and is told to wait, it gets one more point for this conflict. When its points plus its priority are more than the enemy's priority, it aborts the enemy. This keeps the manager obstruction-free: a transaction never waits for ever for an enemy that has stopped.

## The problem

The setting is the one of [contention management](/contention-management/): an STM with eager conflict detection finds that transaction $A$ wants an object that active transaction $B$ owns, and asks the manager whether $A$ should abort $B$ or wait. Any answer is safe. The goal is good throughput, with no thread able to block others for ever (obstruction freedom requires that the manager eventually lets $A$ abort $B$).

We use this model on the page and in the code. There are $n$ threads, each running transactions that open objects for writing. Threads are asynchronous. A backoff interval is a number of steps of the waiting thread, and the scheduler decides how many steps the other threads take meanwhile.

## The algorithm

```pseudo id=main
OPENED(A)                                   ▷ A has opened one more object
L1  prio(A) ← prio(A) + 1
L2  tries(A) ← 0
RESOLVE(A, B)                               ▷ A wants an object that active transaction B owns
L3  if prio(A) + tries(A) > prio(B) then
L4      return ABORT-ENEMY                  ▷ A aborts B by CAS on its status
L5  tries(A) ← tries(A) + 1
L6  back off for a fixed interval
L7  return WAIT                             ▷ A calls RESOLVE again after the interval
RESTARTED(A)                                ▷ A was aborted
L8  keep prio(A)                            ▷ the work done counts for the next attempt
COMMITTED(A)
L9  prio(A) ← 0
```

The test on L3 is the rule of the paper, "aborting an enemy transaction when the number of times a transaction has attempted to open an object exceeds the difference in priorities between the enemy and itself". Scherer and Scott count objects that are read and objects that are written; the model on this page has writes only.

## Example

$T_0$ opens $x$ then $y$, and $T_1$ opens $y$ then $x$; the backoff interval is one step. The priorities in the table are absolute.

| step | who | event | prio $T_0$ | prio $T_1$ | tries |
|---|---|---|---|---|---|
| 1 | $T_0$ | opens $x$ | 1 | 0 | |
| 2 | $T_1$ | opens $y$ | 1 | 1 | |
| 3 | $T_1$ | wants $x$: $1 + 0 > 1$ is false, wait | 1 | 1 | $T_1$: 1 |
| 4 | $T_0$ | wants $y$: $1 + 0 > 1$ is false, wait | 1 | 1 | $T_0$: 1, $T_1$: 1 |
| 5 | $T_1$ | backs off | 1 | 1 | |
| 6 | $T_1$ | wants $x$: $1 + 1 > 1$, aborts $T_0$, takes $x$ | 1 | 2 | |
| 7 | $T_0$ | restarts and keeps priority 1 | 1 | 2 | |
| 8 | $T_1$ | commits; its priority goes back to 0 | 1 | 0 | |
| 9 to 11 | $T_0$ | opens $x$, opens $y$, commits | 0 | 0 | |

**A livelock.** Karma cannot stop an adversarial scheduler. Start with $T_0$ owning $x$, priorities $1$ and $0$. Then: $T_0$ opens $y$ (priorities 2 and 0); $T_1$ wants $y$ and waits three times, since it needs $0 + 3 > 2$; meanwhile the scheduler does not run $T_0$, which is ready to commit; $T_1$ aborts $T_0$ and takes $y$ (2 and 1); $T_0$ restarts; $T_1$ opens $x$ (2 and 2); $T_0$ wants $x$, waits once, then aborts $T_1$ and takes $x$ (3 and 2); $T_1$ restarts. The state is the same as at the start, except that both priorities grew by 2, and the decisions depend only on the difference. Both threads took steps and nobody committed, so the round can repeat for ever. The implementation finds this cycle by a search of the state graph and replays it.

## Correctness

Karma does not affect safety, which is the job of the STM. The progress claims, proved in `proofs/correctness.md`, are:

1. **Each wait is bounded.** While the same attempt of $B$ owns the object, $A$ waits at most $d + \ell + 1$ intervals, where $d$ is the priority difference at the first conflict and $\ell$ is the number of objects $B$ can still open (each open raises the priority of $B$ by one).
2. **Obstruction freedom is kept.** A transaction that runs alone from some time on commits after a bounded number of its own steps, even if other transactions stopped while they owned objects it needs.
3. **No livelock freedom.** The run above is a fair run in which no transaction commits.

GHP explain why priority by work cannot give a worst-case guarantee: "any transaction A might get repeatedly aborted due to newcomer transactions that, between two aborts of A, get aborted more often and access more objects". The [Greedy manager](/greedy-contention-manager/) uses timestamps instead, and it has a proof of progress.

## Complexity

A decision takes $\Theta(1)$ steps: read the priority of the enemy, compare, and either back off or do one compare-and-swap on its status. The space is one priority and one counter per transaction. A transaction with priority $d$ below its enemy, where the enemy's priority does not change, waits exactly $\max(0, d + 1)$ intervals before it aborts the enemy; the tests check this for all $d$ from $-3$ to 5. The time until all transactions commit has no bound in the worst case, by claim 3.

## Properties

- Obstruction-free: no transaction waits for ever behind a stopped enemy.
- Not livelock-free and not starvation-free in the worst case.
- Deterministic as described here; the backoff interval is fixed, not random.
- The priority is cumulative: it is not reset on abort, only on commit.

## Variants and improvements

- **Eruption** (Scherer and Scott) adds the priority of a blocked transaction to the enemy that blocks it, so that a transaction that holds an object many others need finishes sooner.
- **Polka** combines Karma's priorities with the randomized exponential backoff of Polite: it backs off for a number of intervals equal to the priority difference, and the intervals grow exponentially. See [Polka](/polka-contention-manager/).
- **Kindergarten** and **Timestamp** are other managers of the same study. Timestamp gives priority to the older transaction, as [Greedy](/greedy-contention-manager/) does, but it has no waiting rule and no proof of progress.

## When to use it

Karma is a reasonable heuristic for workloads where transactions of very different lengths conflict, because a long transaction is protected by its priority, and a short one that keeps losing gains priority. Scherer and Scott found that Karma and Polite were often among the best managers of their 2004 study, but that neither did well on all benchmarks; that was the reason for Polka. Use [Greedy](/greedy-contention-manager/) when a guarantee of progress is needed.

## Pitfalls

- **Assuming it prevents livelock.** It reduces the chance of livelock in practice; under an adversarial schedule two transactions can abort each other for ever, as shown above.
- **Resetting the priority on abort.** Then a short transaction that loses to long ones never builds up priority, and the main idea of Karma is lost.
- **Counting tries across objects.** The counter is per object: it is reset when the transaction opens an object. If it is not reset, a transaction that waited for one object aborts the owner of the next one at once.
- **Priority overflow.** A transaction that is aborted many times has a growing priority; use a wide counter.

## Implementations

## History

Herlihy, Luchangco, Moir and Scherer made the contention manager a separate module of DSTM in 2003. DSTM itself came with two simple managers, Aggressive and Polite. Scherer and Scott proposed many more in 2004, among them Karma, Eruption and Kindergarten, and compared them with Polite; in 2005 they described them again and added Polka and the prioritized variants. Guerraoui, Herlihy and Pochon noted in 2005 that none of these managers gives a worst-case guarantee, and proposed Greedy.

## References
