---
tag: MY1GV3
kind: technique
slug: contention-management
name: Contention management
aliases:
- contention manager
area: concurrency/transactional-memory
level: advanced
summary: The policy of a transactional memory that decides, at a conflict, which transaction aborts, whether to wait and how long to back off. It controls progress, not safety.
prereqs: [transaction, obstruction-freedom, livelock]
see_also: [greedy-contention-manager, karma-contention-manager, polite-contention-manager, polka-contention-manager, dstm, transaction-conflict, eager-conflict-detection, lazy-conflict-detection]
sources:
  - paper: doi:10.1145/872035.872048
    title: "Maurice Herlihy, Victor Luchangco, Mark Moir and William N. Scherer III, Software transactional memory for dynamic-sized data structures, PODC 2003, pp. 92 to 101"
    locator: the contention manager as a separate module of DSTM, and the Aggressive and Polite managers in the experiments
  - paper: doi:10.1145/1073814.1073861
    title: "William N. Scherer III and Michael L. Scott, Advanced contention management for dynamic software transactional memory, PODC 2005, pp. 240 to 248"
    locator: Section 3.1 (the DSTM manager interface), Sections 3.2 and 3.3 (the managers), Section 4.3.5 (summary of the results)
  - paper: doi:10.1145/1073814.1073863
    title: "Rachid Guerraoui, Maurice Herlihy and Bastian Pochon, Toward a theory of transactional contention managers, PODC 2005, pp. 258 to 264"
    locator: Section 1 (the choice between waiting and aborting), Section 3 (Greedy) and Section 6 (no deterministic guarantee for the earlier managers)
  - paper: doi:10.1145/1504176.1504199
    title: "Michael F. Spear, Luke Dalessandro, Virendra J. Marathe and Michael L. Scott, A comprehensive strategy for contention management in software transactional memory, PPoPP 2009, pp. 141 to 150"
    locator: the definition of contention management, and a strategy for an STM with invisible reads
  - paper: doi:10.1145/1250662.1250674
    title: "Jayaram Bobba, Kevin E. Moore, Haris Volos, Luke Yen, Mark D. Hill, Michael M. Swift and David A. Wood, Performance pathologies in hardware transactional memory, ISCA 2007, pp. 81 to 91"
    locator: conflict resolution as a design dimension of HTM, and the pathologies that follow from it
---

**Contention management** is the part of a transactional memory that decides what happens when two transactions conflict: which one aborts, whether the other waits, and how long a loser backs off before it tries again. It is a separate question from *when* conflicts are found ([eager](/eager-conflict-detection/) or [lazy conflict detection](/lazy-conflict-detection/)) and from *how* tentative values are kept. In [DSTM](/dstm/), Herlihy, Luchangco, Moir and Scherer made it a module of its own, the **contention manager**, which the STM asks at each conflict. Any answer is safe, because the STM guarantees atomicity whatever the manager says; the answers decide progress: throughput, fairness, and freedom from [livelock](/livelock/) and starvation.

## In plain words

Two transactions want the same data, and at least one of them writes it. Both cannot go on. Someone must decide: stop the other one, wait for it, or give up and start again.

The STM can make each of these choices safely. But a bad rule can make the program slow or stuck. If every transaction always kills the other, two of them can keep killing each other for ever. If every transaction always waits, two of them can wait for each other for ever. If a short transaction always wins, a long one may never finish.

A contention manager is the rule that makes this choice. It can use what it knows about the two transactions: their age, how much work they did, how often they failed. Good rules make sure that someone finishes and that nobody loses for ever.

## When it applies

A contention manager is needed when the TM has a real choice at a conflict.

- **Eager conflict detection.** The STM finds the conflict when a transaction $A$ tries to access an object that an active transaction $B$ holds. $A$ can abort $B$, abort itself, or wait. This is the setting of DSTM and of the classic managers. In an obstruction-free STM, the manager must eventually let $A$ abort $B$, because $B$ may belong to a thread that has stopped.
- **Lazy conflict detection.** Conflicts are found at commit time. The usual rule is that the committer wins, and the manager decides little more than how long an aborted transaction waits before it restarts. A lazy STM can still starve a long reader that keeps being invalidated by short writers, so the policy for retries still matters.
- **Hardware TM.** In a best-effort [HTM](/hardware-transactional-memory/), the hardware resolves a conflict in the cache coherence protocol, and software sees only an abort. The software policy is the retry policy: how often to retry, and when to take a fallback path. Bobba et al. treat conflict resolution as one of three design dimensions of an HTM, with conflict detection and version management, and show performance pathologies that come from bad combinations.

Spear, Dalessandro, Marathe and Scott define contention management as "the mechanisms used to ensure forward progress", "to avoid livelock and starvation, and to promote throughput and fairness". Which manager works best depends on the conflict detection policy and on whether reads are visible (see Variations), so it is best to choose them together.

## The template

```pseudo id=main
OPEN(A, o)                                  ▷ the STM calls this at each access of A to object o
L1  loop
L2      B ← the active transaction that holds o in a conflicting mode, or none
L3      if B = none then
L4          take o for A; CM(A).OPENED(A, o); return
L5      d ← CM(A).RESOLVE(A, B)              ▷ the one decision of the manager
L6      if d = ABORT-ENEMY then CAS(status(B), ACTIVE, ABORTED)
L7      else if d = ABORT-SELF then abort A; CM(A).ABORTED(A); restart A
L8      else wait as d says                  ▷ a backoff, or until B ends
COMMIT(A)
L9  if CAS(status(A), ACTIVE, COMMITTED) then CM(A).COMMITTED(A)
L10 else CM(A).ABORTED(A); wait CM(A).RESTART-DELAY(A); restart A
```

This is the shape of the DSTM interface as Scherer and Scott describe it: notification methods ("hooks") for events such as begin, commit, abort, and the attempt and success of an access, plus two request methods that ask the manager whether a transaction should (re)start and whether an enemy should be aborted. Each thread has its own manager object, so management is distributed: a manager builds its view from the hooks of its own thread and from the public fields of the enemy, such as a timestamp or a priority. The compare-and-swap on L6 can fail if $B$ commits first; then the loop reads the owner again.

*Example.* $T_0$ opens $x$ then $y$, and $T_1$ opens $y$ then $x$. $T_0$ has opened $x$, and $T_0$ is older.

| step | Aggressive | Greedy |
|---|---|---|
| 1 | $T_0$ opens $y$ and is ready to commit | the same |
| 2 | $T_1$ wants $y$; it aborts $T_0$ and takes $y$ | $T_1$ wants $y$; $T_0$ is older and active, so $T_1$ waits |
| 3 | $T_0$ restarts; $T_1$ opens $x$, now free | $T_0$ commits |
| 4 | $T_0$ wants $x$; it aborts $T_1$ and takes $x$ | $T_1$ opens $y$ and $x$, and commits |
| 5 | $T_1$ restarts; the state is the one after step 0 | |

With Aggressive, the schedule can repeat steps 1 to 5 for ever, and no transaction commits, although both threads take steps: a livelock. The pages on the managers check runs of this kind in a small model. Greedy, which keeps timestamps across aborts, has no such run.

## Classic examples

- **Aggressive.** Always abort the enemy. It keeps obstruction freedom but can livelock, as in the example. In the DSTM experiments, one integer set benchmark livelocked with Aggressive as soon as more than one thread ran.
- **[Polite](/polite-contention-manager/).** Back off with exponentially growing random intervals, and abort the enemy after $m$ rounds. It came with DSTM.
- **[Karma](/karma-contention-manager/).** The priority of a transaction is the number of objects it has opened, over all its attempts. Abort the enemy when the number of tries exceeds the priority gap. Scherer and Scott, 2004.
- **[Polka](/polka-contention-manager/).** Karma's priorities with Polite's exponential backoff. Scherer and Scott proposed it as a default manager in 2005.
- **[Greedy](/greedy-contention-manager/).** Give each transaction a timestamp at its first start and keep it across aborts. Abort an enemy that is younger or that is waiting; otherwise wait. Guerraoui, Herlihy and Pochon proved that every transaction commits and that the makespan is within a factor $s(s + 1) + 2$ of the best, for $s$ shared objects.
- **Others from Scherer and Scott.** Eruption gives the priority of a blocked transaction to the enemy that blocks it; Kindergarten makes transactions take turns: it aborts an enemy that is on its list of enemies in favour of which it has already aborted, and otherwise adds the enemy to the list, backs off, and then aborts itself if it is still blocked; Timestamp aborts younger enemies and waits for older ones, which it marks as possibly dead and aborts later.

| manager | decision at a conflict | guarantee |
|---|---|---|
| Aggressive | abort the enemy | obstruction freedom only |
| Polite | back off $m$ times, then abort | none beyond obstruction freedom |
| Karma | wait until tries exceed the priority gap | none beyond obstruction freedom |
| Polka | back off the gap times, exponentially | none beyond obstruction freedom |
| Greedy | abort a younger or waiting enemy, else wait | every transaction commits; bounded makespan |

## Variations

- **Who decides.** In DSTM each thread has its own manager, and managers agree only through public fields. Other designs use a central scheduler that serializes transactions that keep conflicting.
- **Abort self or abort enemy.** Some managers abort the requester rather than the holder. With lazy detection the committer wins, and the only policy is the delay before a restart.
- **Priorities.** A priority can be a timestamp (age), the work done (objects opened), the number of aborts, or a base priority given by the programmer. Scherer and Scott give prioritized variants that add the base priority of the thread at each open, to share throughput in proportion.
- **Visible and invisible reads.** With invisible reads, a writer cannot see the readers it conflicts with, so a manager can resolve only write conflicts, and readers find out at validation. Scherer and Scott found little difference between managers with invisible reads in some benchmarks, and large differences with visible reads.
- **Escalation.** Many systems combine a cheap policy with a fallback: back off a few times, then raise the priority of a transaction that keeps failing, or run it alone, for example as an [irrevocable transaction](/transaction-irrevocability/).

## Pitfalls

- **Always waiting.** If transactions only wait, two transactions that each hold an object the other needs wait for ever. GHP note that if a manager "never allows one transaction to abort another, then deadlock can happen".
- **Always aborting.** Aggressive avoids deadlock but allows livelock, as in the example.
- **Trusting backoff and priorities.** Polite, Karma and Polka make livelock unlikely in practice but do not exclude it. In the words of GHP, aborting enemies after a time-out "diminishes the probability of livelocks without however canceling it".
- **Waiting for a stopped thread.** In an obstruction-free STM, a manager that waits without limit behind an enemy loses obstruction freedom, because the enemy's thread may never run again. Greedy waits only for active enemies and assumes that delays are finite.
- **Forgetting the restart.** A policy that decides well at the conflict but restarts the loser at once can make the same conflict happen again right away. A delay before the restart is part of the policy.
- **Mixing up safety and progress.** A contention manager cannot fix an unsafe STM, and a safe STM does not make a manager correct. Zombie transactions, for example, are a problem of validation ([opacity](/opacity/)), not of contention management.

## Exercises

1. Show that a manager that always waits can deadlock, with two transactions and two objects. Then show that a manager that always aborts the enemy can livelock with the same two transactions.
2. In the example, give a schedule in which Karma does not commit either transaction in the first 20 steps. *Hint.* Look at how the priorities change in each round.
3. Prove that with Greedy, the oldest active transaction is never aborted. Why does this imply that some transaction commits whenever transactions keep taking steps?
4. With lazy conflict detection and the rule that the committer wins, construct a run in which one long read-only transaction never commits. Propose a manager rule that prevents it.
5. A manager for an HTM sees only the abort code. Design a retry policy that takes a fallback lock after a bounded number of conflict aborts, and argue that it gives progress if the fallback path always completes.

## References
