---
tag: 6YVCN1
kind: algorithm
slug: polite-contention-manager
name: Polite contention manager
aliases:
- exponential backoff contention manager
area: concurrency/transactional-memory
level: research
summary: A contention manager that backs off for a random time with exponentially growing mean when it meets an enemy, and aborts the enemy after m rounds. It has no progress guarantee.
complexity:
  vars: {n: the number of transactions, m: the number of backoff rounds before an abort}
  steps: {decision: Θ(1), wait: Θ(2^m)}
  space: {shared: Θ(n)}
properties: {deterministic: false, obstruction_free: true, livelock_free: false, starvation_free: false}
history:
  year: 2003
  people: [Maurice Herlihy, Victor Luchangco, Mark Moir, William N. Scherer III]
  note: DSTM came with two simple managers, Aggressive and Polite; Scherer and Scott studied Polite again in 2004 and 2005, and joined it with Karma as Polka.
prereqs: [contention-management, exponential-backoff]
see_also: [karma-contention-manager, polka-contention-manager, greedy-contention-manager, binary-exponential-backoff, dstm, livelock, obstruction-freedom, spin-lock]
sources:
  - paper: doi:10.1145/1073814.1073861
    title: "William N. Scherer III and Michael L. Scott, Advanced contention management for dynamic software transactional memory, PODC 2005, pp. 240 to 248"
    locator: Section 3.2 (Polite, with mean 2^(n+k) ns, k = 4 and m = 22)
  - paper: "William N. Scherer III and Michael L. Scott, Contention management in dynamic software transactional memory, PODC Workshop on Concurrency and Synchronization in Java Programs (CSJP), 2004"
    locator: a comparison of many DSTM contention managers, among them Polite and Karma
  - paper: doi:10.1145/872035.872048
    title: "Maurice Herlihy, Victor Luchangco, Mark Moir and William N. Scherer III, Software transactional memory for dynamic-sized data structures, PODC 2003, pp. 92 to 101"
    locator: the contention manager module, and the Aggressive and Polite managers used in the experiments
  - paper: doi:10.1145/1073814.1073863
    title: "Rachid Guerraoui, Maurice Herlihy and Bastian Pochon, Toward a theory of transactional contention managers, PODC 2005, pp. 258 to 264"
    locator: Section 6 (managers with time-outs and randomized managers give no deterministic guarantee)
  - paper: doi:10.1145/103727.103729
    title: "John M. Mellor-Crummey and Michael L. Scott, Algorithms for scalable synchronization on shared-memory multiprocessors, ACM Transactions on Computer Systems 9(1), 1991, pp. 21 to 65"
    locator: exponential backoff for spin locks, the idea that Polite applies to transactions
---

The **Polite contention manager** resolves a conflict between transactions with **randomized exponential backoff**. When transaction $A$ finds that an active enemy $B$ owns an object it needs, $A$ spins for a random time whose mean doubles each time it meets the conflict again; after $m$ rounds it aborts $B$. Scherer and Scott give the mean as $2^{n+k}$ nanoseconds in round $n$, with $k = 4$ and $m = 22$ on their machine. Polite is simple and often fast, but it gives no guarantee of progress.

## In plain words

Two people meet in a narrow corridor. Polite says: step aside for a short time and look again; if the other is still there, wait twice as long; after a fixed number of tries, push through. Usually the other person has passed by then, and nobody had to turn back.

For transactions, waiting gives the enemy time to commit, which is cheaper than aborting it. The time grows quickly, so that a conflict that does not go away does not make the threads fight at full speed. Because the waits are random, two transactions that meet often do not keep making the same choice at the same moment. After $m$ rounds Polite gives up waiting and aborts the enemy, so it never waits for ever behind a transaction whose thread has stopped.

## The problem

The setting is the one of [contention management](/contention-management/): an STM with eager conflict detection, such as [DSTM](/dstm/), finds that transaction $A$ wants an object that active transaction $B$ owns, and asks the manager whether to abort $B$ or to wait. Any answer is safe. Obstruction freedom requires that a thread that runs alone eventually gets the object, so the manager must abort the enemy at some point.

We use this model on the page and in the code. There are $n$ threads, each running transactions that open objects for writing. Threads are asynchronous. In the code, round $i$ of backoff is exactly $2^i$ steps of the waiting thread, which stands for the random time of the paper; the scheduler decides what the other threads do meanwhile.

## The algorithm

```pseudo id=main
RESOLVE(A, B)                               ▷ A wants an object that active transaction B owns
L1  if tries(A) ≥ m then                    ▷ m rounds of backoff are over
L2      return ABORT-ENEMY                  ▷ A aborts B by CAS on its status
L3  spin for a random time with mean 2^(tries(A) + k) ns
L4  tries(A) ← tries(A) + 1
L5  return WAIT                             ▷ A calls RESOLVE again after the spin
OPENED(A)                                   ▷ A got an object
L6  tries(A) ← 0
```

The counter is per object: it counts the conflicts "encountered so far for an object" in the words of the paper, and it is reset when the transaction gets the object. Polite keeps nothing across aborts: a restarted transaction starts again with no advantage.

## Example

$T_0$ opens $x$ then $y$, and $T_1$ opens $y$ then $x$, with $m = 2$. The schedule is $T_0$, then seven steps of $T_1$, then $T_0, T_1, T_0, T_0, T_0$.

| step | who | event | tries of $T_1$ | backoff left |
|---|---|---|---|---|
| 1 | $T_0$ | opens $x$ | 0 | |
| 2 | $T_1$ | opens $y$ | 0 | |
| 3 | $T_1$ | wants $x$; $0 < 2$, so it waits (round 0, 1 step) | 1 | 1 |
| 4 | $T_1$ | backs off | 1 | 0 |
| 5 | $T_1$ | wants $x$; $1 < 2$, so it waits (round 1, 2 steps) | 2 | 2 |
| 6, 7 | $T_1$ | backs off | 2 | 0 |
| 8 | $T_1$ | wants $x$; $2 \ge 2$, aborts $T_0$ and takes $x$ | 0 | |
| 9 | $T_0$ | restarts | | |
| 10 | $T_1$ | commits | | |
| 11 to 13 | $T_0$ | opens $x$, opens $y$, commits | | |

In this schedule $T_0$ took no step while $T_1$ waited, so the waits did not help. If the scheduler had run $T_0$ during step 4, $T_0$ would have met $T_1$ on $y$ and waited too, and with random times one of them would usually have got through first.

## Correctness

Polite does not affect safety, which is the job of the STM. Its progress properties, proved in `proofs/correctness.md`, are:

1. **Each conflict ends.** If the same enemy keeps the object, $A$ aborts it after exactly $m$ waits and $2^m - 1$ steps of backoff in the model.
2. **Obstruction freedom is kept.** A transaction that runs alone commits after a bounded number of its own steps, even if a stopped transaction holds objects it needs.
3. **No livelock freedom.** There is a fair run with two transactions in which neither commits: each one, after its $m$ rounds of backoff, aborts the other just before the other can commit. The implementation finds such a cycle in the state graph for $m = 2$ and replays it.

In real time, a cycle of this kind needs the enemy to be idle during the whole backoff, and random backoff makes repeated bad timing unlikely. GHP put it in this way: aborting enemies after a time-out "diminishes the probability of livelocks without however canceling it", and "none of the polite or randomized managers provide any deterministic guarantee".

## Complexity

A decision takes $\Theta(1)$ steps. A conflict with an enemy that does not finish costs $m$ decisions and a total expected spin time of $\sum_{i=0}^{m-1} 2^{i+k} = (2^m - 1) 2^k$ ns, so $\Theta(2^m)$; with $k = 4$ and $m = 22$ this is about 67 ms. The space is one counter per transaction. There is no worst-case bound on the time until a transaction commits, by claim 3.

## Properties

- Obstruction-free: after $m$ rounds it always aborts the enemy.
- Randomized and not livelock-free; not starvation-free.
- Keeps no state across transactions, so it is cheap and needs no shared counters.
- Two tuning constants, $k$ and $m$, which depend on the machine.

## Variants and improvements

- **Karma** and **Polka.** [Karma](/karma-contention-manager/) replaces the fixed number of rounds by a priority difference based on work done; [Polka](/polka-contention-manager/) keeps the exponential backoff of Polite and takes the number of rounds from Karma's priorities.
- **Backoff after an abort.** Many STMs also back off before restarting an aborted transaction, which is the same idea applied at a different point.
- **Spin locks with backoff.** The same rule, a spin that doubles on each failure, is the standard way to reduce contention on a [spin lock](/spin-lock/); see [exponential backoff](/exponential-backoff/).

## When to use it

Polite is a good simple default when conflicts are short and rare: most conflicts end during the first rounds, and nobody is aborted. It is weak when one long transaction conflicts with many short ones, because the long one keeps being aborted after the same fixed number of rounds and never gets an advantage. Scherer and Scott found that Karma and Polite were often among the best managers of their 2004 study, but that neither did well on all benchmarks.

## Pitfalls

- **Assuming backoff prevents livelock.** It makes livelock less likely, not impossible; the run in the proof is a fair livelock.
- **Tuning for one machine.** The constants $k = 4$ and $m = 22$ were chosen for the test machine of the paper. With $m = 22$ a conflict with a stopped enemy costs tens of milliseconds before the abort.
- **Not resetting the counter.** If tries are not reset when an object is obtained, a later conflict aborts the enemy at once, and Polite behaves like the aggressive manager.
- **Fixed instead of random waits.** With equal fixed waits, two symmetric transactions can keep repeating the same decisions in step; the randomness is what breaks the symmetry in practice.

## Implementations

## History

Exponential backoff is an old idea for networks and spin locks. Herlihy, Luchangco, Moir and Scherer made contention management a separate module of DSTM in 2003. Their experiments used two managers: Aggressive, which always aborts the enemy, and Polite, which backs off a few times before it does. Scherer and Scott compared Polite with Karma and many other managers in 2004, and in 2005 they gave the version described here and merged Polite and Karma into Polka. Guerraoui, Herlihy and Pochon pointed out the same year that randomized managers like Polite give no deterministic guarantee, and gave the Greedy manager, which does.

## References
