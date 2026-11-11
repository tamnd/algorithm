---
tag: D8YGK7
kind: algorithm
slug: polka-contention-manager
name: Polka contention manager
aliases:
- Polka
area: concurrency/transactional-memory
level: research
summary: A contention manager that joins Karma and Polite. It backs off for as many intervals as the priority gap, with intervals that grow exponentially, then aborts the enemy. No progress guarantee.
complexity:
  vars: {n: the number of transactions, d: "the enemy's priority minus the caller's, at the first conflict"}
  steps: {decision: Θ(1), wait: Θ(2^d)}
  space: {shared: Θ(n)}
properties: {deterministic: false, obstruction_free: true, livelock_free: false, starvation_free: false}
history:
  year: 2005
  people: [William N. Scherer III, Michael L. Scott]
  note: Scherer and Scott combined the priorities of Karma with the exponential backoff of Polite and proposed the result, Polka, as a default manager for DSTM.
prereqs: [karma-contention-manager, polite-contention-manager]
see_also: [contention-management, greedy-contention-manager, dstm, exponential-backoff, livelock, obstruction-freedom, transaction-abort, spin-lock]
sources:
  - paper: doi:10.1145/1073814.1073861
    title: "William N. Scherer III and Michael L. Scott, Advanced contention management for dynamic software transactional memory, PODC 2005, pp. 240 to 248"
    locator: Section 3.3 (Polka), Section 3.4 (prioritized Polka) and Section 4.3.5 (Polka as a default manager)
  - paper: doi:10.1145/1073814.1073863
    title: "Rachid Guerraoui, Maurice Herlihy and Bastian Pochon, Toward a theory of transactional contention managers, PODC 2005, pp. 258 to 264"
    locator: Section 6 (managers with time-outs and randomized managers give no deterministic guarantee)
  - paper: doi:10.1145/872035.872048
    title: "Maurice Herlihy, Victor Luchangco, Mark Moir and William N. Scherer III, Software transactional memory for dynamic-sized data structures, PODC 2003, pp. 92 to 101"
    locator: DSTM and its contention manager module
---

The **Polka contention manager** of Scherer and Scott (2005) joins two older managers for obstruction-free STM. From [Karma](/karma-contention-manager/) it takes the **priority**: the number of objects a transaction has opened, summed over all its attempts, kept on abort and reset on commit. From [Polite](/polite-contention-manager/) it takes **randomized exponential backoff**. When transaction $A$ meets an active enemy $B$, Polka "backs off for a number of intervals equal to the difference in priorities", and the intervals grow exponentially; then it aborts $B$. Scherer and Scott found that no manager was best on all their benchmarks, but that Polka had good throughput even where others beat it, and they proposed it as a default. Like its parents, Polka gives no guarantee of progress.

## In plain words

Two transactions want the same object. The one that has done less work steps back, because aborting the other would waste more. How many times it steps back depends on how far behind it is: one time for each object of difference. Each wait is twice as long as the one before, so a transaction far behind waits a long time and gives the leader a good chance to finish.

The waits do two jobs. They let the more invested transaction commit. They also keep losing threads off the memory bus, in the same way that backoff helps a [spin lock](/spin-lock/). If the leader still has not finished after all the waits, the follower aborts it, so a stopped thread never blocks others for ever.

## The problem

The setting is the one of [contention management](/contention-management/): an STM with eager conflict detection, such as [DSTM](/dstm/), finds that transaction $A$ wants an object that active transaction $B$ owns, and asks the manager whether to abort $B$ or to wait. Any answer is safe. Obstruction freedom requires that a thread that runs alone eventually gets the object, so the manager must abort the enemy at some point.

We use this model on the page and in the code. There are $n$ threads, each running transactions that open objects for writing. Threads are asynchronous. In the code, backoff interval $i$ of a conflict is exactly $2^i$ steps of the waiting thread, which stands for the random time of the paper; the scheduler decides what the other threads do meanwhile. Priorities are kept as differences, since Polka compares only differences.

## The algorithm

```pseudo id=main
OPENED(A)                                   ▷ A got an object
L1  prio(A) ← prio(A) + 1
L2  tries(A) ← 0
RESOLVE(A, B)                               ▷ A wants an object that active transaction B owns
L3  if tries(A) ≥ prio(B) − prio(A) then    ▷ A has backed off once for each unit of the gap
L4      return ABORT-ENEMY                  ▷ A aborts B by CAS on its status
L5  spin for a random time with mean 2^(tries(A) + k) ns
L6  tries(A) ← tries(A) + 1
L7  return WAIT                             ▷ A calls RESOLVE again after the spin
RESTARTED(A)                                ▷ A was aborted and starts again
L8  keep prio(A)
COMMITTED(A)
L9  prio(A) ← 0
```

The test on L3 reads the priority of $B$ again at each call, so if $B$ opens more objects while $A$ waits, $A$ must wait more. If $A$ already has at least the priority of $B$, the gap is at most zero and $A$ aborts $B$ at once. The constant $k$ sets the length of the first interval; the paper uses the same backoff as Polite.

Two details of the paper are not in the block. Polka "unconditionally aborts a group of (visible) readers that hold an object needed for read-write access", because the authors found writes more important than reads in their benchmarks; our model has only writes. In the prioritized version, each open adds the base priority of the thread instead of 1.

## Example

$T_0$ opens objects $0, 1, 2$, and $T_1$ opens object $2$. The schedule runs $T_0$ three times, then $T_1$ alone until it gets object 2.

| step | who | event | gap | tries of $T_1$ | backoff set |
|---|---|---|---|---|---|
| 1 to 3 | $T_0$ | opens 0, 1, 2; $\mathrm{prio}(T_0) = 3$ | 3 | 0 | |
| 4 | $T_1$ | wants 2; $0 < 3$, waits | 3 | 1 | 1 step |
| 5 | $T_1$ | backs off | 3 | 1 | |
| 6 | $T_1$ | wants 2; $1 < 3$, waits | 3 | 2 | 2 steps |
| 7, 8 | $T_1$ | backs off | 3 | 2 | |
| 9 | $T_1$ | wants 2; $2 < 3$, waits | 3 | 3 | 4 steps |
| 10 to 13 | $T_1$ | backs off | 3 | 3 | |
| 14 | $T_1$ | wants 2; $3 \ge 3$, aborts $T_0$ and takes 2 | | 0 | |
| 15 | $T_1$ | commits | | | |
| 16 to 20 | $T_0$ | restarts, opens 0, 1, 2, commits | | | |

$T_1$ backed off for three intervals of $1, 2, 4$ steps, one for each unit of the gap. Karma, with a fixed interval, would have waited about the same number of times but for a fixed time each. If the scheduler had run $T_0$ during the backoff, $T_0$ would have committed and $T_1$ would have found object 2 free.

## Correctness

Polka does not affect safety, which is the job of the STM. Its progress properties, proved in `proofs/correctness.md`, are:

1. **Each conflict ends.** If the same enemy keeps the object and its priority does not change, $A$ aborts it after exactly $d$ waits and $2^d - 1$ steps of backoff in the model, where $d$ is the priority gap. If the enemy keeps opening objects, it is no longer stopped, and it either commits or $A$ catches up.
2. **Obstruction freedom is kept.** A transaction that runs alone commits after a bounded number of its own steps, even if stopped transactions hold objects it needs.
3. **No livelock freedom.** There is a fair run with two transactions in which neither commits. In each round both priorities grow by 2, so the gap returns to the same value and the round repeats. The implementation finds such a cycle in the state graph and replays it.

In real time the bad run needs the enemy to be idle during the whole backoff, and random backoff makes repeated bad timing unlikely. GHP note that aborting enemies after a time-out "diminishes the probability of livelocks without however canceling it", and that "none of the polite or randomized managers provide any deterministic guarantee".

## Complexity

A decision takes $\Theta(1)$ steps. A conflict with a stopped enemy that leads by $d$ costs $d$ waits and a total expected spin time of $\sum_{i=0}^{d-1} 2^{i+k} = (2^d - 1)\,2^k$ ns, so $\Theta(2^d)$. The space is a priority and a counter per transaction. There is no worst-case bound on the time until a transaction commits, by claim 3.

## Properties

- Obstruction-free: the number of waits is bounded by the gap at each call.
- Randomized; not livelock-free and not starvation-free.
- Priorities survive aborts, so a transaction that keeps losing gains weight over time, as in Karma.
- The exponential intervals reduce memory traffic from threads that retry the same object.
- Priorities can grow without bound inside one long transaction; the gap, not the size, decides.

## Variants and improvements

- **Karma.** Fixed intervals, and one more try than the gap. Polka keeps the count and makes the intervals exponential.
- **Karmexp.** Scherer and Scott also tested a manager with fixed intervals, in which the number of intervals needed to overtake an enemy grows exponentially with the priority gap. They used it to check that the exponential backoff, not only the priorities, explains why Polka did well.
- **Prioritized Polka.** Each open adds the base priority $BP$ of the thread, so a thread with a larger $BP$ catches up faster. The aim is proportional sharing of throughput.
- **Greedy.** [Greedy](/greedy-contention-manager/) replaces work-based priorities by start-time timestamps that are kept across aborts. That gives a bound on the time to commit, which Polka does not have.

## When to use it

Polka was proposed as a default manager for an obstruction-free STM in which conflicts are usually short: it waits when waiting is likely to pay, and its backoff keeps contention low. It is a poor choice when a worst-case progress guarantee is needed, for example when a long transaction must not be aborted again and again by short ones; then a timestamp-based manager such as Greedy is safer. With invisible reads, the paper found little difference between managers, because a writer seldom sees the readers it conflicts with.

## Pitfalls

- **Assuming that priorities prevent livelock.** Both priorities can grow by the same amount in each round, as in the proof, so the gap never closes.
- **Long waits behind a stopped thread.** The total wait grows exponentially with the gap. A transaction far behind a stopped enemy spins for a long time before it aborts it.
- **Not resetting the priority on commit.** A thread that keeps its priority across transactions wins all its conflicts later, and others can starve.
- **Reading the gap only once.** The gap must be read at each call. If the enemy keeps opening objects, a gap read only at the first call lets $A$ abort a transaction that is now much further ahead.

## Implementations

## History

Herlihy, Luchangco, Moir and Scherer made contention management a separate module of DSTM in 2003, with two simple managers, Aggressive and Polite. In 2004 Scherer and Scott proposed many more, among them Karma, and compared them with Polite. They found that these two were often among the best, but that neither did well on all benchmarks. At PODC 2005 they combined them into Polka and proposed it as a default. At the same conference Guerraoui, Herlihy and Pochon showed that managers of this kind give no deterministic guarantee, and gave Greedy, which does.

## References
