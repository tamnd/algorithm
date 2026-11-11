---
tag: Z33CZD
kind: algorithm
slug: greedy-contention-manager
name: Greedy contention manager
aliases:
- Greedy CM
area: concurrency/transactional-memory
level: research
summary: A contention manager that gives each transaction a timestamp kept across aborts; the older one wins a conflict, and a waiting one can be aborted. Every transaction commits.
complexity:
  vars: {n: the number of transactions, s: the number of shared objects}
  steps: {decision: Θ(1)}
  space: {shared: Θ(n)}
properties: {deterministic: true, livelock_free: true, starvation_free: true, pending_commit: true}
history:
  year: 2005
  people: [Rachid Guerraoui, Maurice Herlihy, Bastian Pochon]
  note: Guerraoui, Herlihy and Pochon gave the Greedy manager at PODC 2005 as the first contention manager with both a progress guarantee and a bound on the makespan.
prereqs: [contention-management, starvation-freedom]
see_also: [karma-contention-manager, polite-contention-manager, polka-contention-manager, dstm, livelock, competitive-ratio, list-scheduling, priority-scheduling]
sources:
  - paper: doi:10.1145/1073814.1073863
    title: "Rachid Guerraoui, Maurice Herlihy and Bastian Pochon, Toward a theory of transactional contention managers, PODC 2005, pp. 258 to 264"
    locator: Section 3 (the two rules), Section 4 (Theorem 1, the pending commit property, Theorem 9 and the example with s + 1), Section 6 (time-outs for halted transactions)
  - paper: doi:10.1145/1146381.1146429
    title: "Rachid Guerraoui, Maurice Herlihy and Bastian Pochon, Towards a theory of transactional contention managers, PODC 2006 (brief announcement), pp. 316 to 317"
    locator: the short follow-up of the same authors
  - paper: doi:10.1007/s00453-008-9195-x
    title: "Hagit Attiya, Leah Epstein, Hadas Shachnai and Tami Tamir, Transactional contention management as a non-clairvoyant scheduling problem, Algorithmica 57(1), 2010, pp. 44 to 61 (first at PODC 2006)"
    locator: the O(s) upper bound for Greedy and the matching lower bound for deterministic work-conserving managers
  - paper: doi:10.1145/1073814.1073861
    title: "William N. Scherer III and Michael L. Scott, Advanced contention management for dynamic software transactional memory, PODC 2005, pp. 240 to 248"
    locator: Section 3 (the DSTM contention manager interface and the Timestamp manager, a forerunner of Greedy)
---

The **Greedy contention manager** decides conflicts between transactions in an obstruction-free STM such as [DSTM](/dstm/). Each transaction takes a **timestamp** when it begins and keeps it when it restarts after an abort; an older timestamp means a higher priority. When transaction $A$ finds that active transaction $B$ holds an object it needs, $A$ aborts $B$ if $B$ is younger or is itself waiting; otherwise $A$ waits. Guerraoui, Herlihy and Pochon proved in 2005 that with Greedy every transaction commits after a bounded delay, and that the time for $n$ transactions that share $s$ objects is within a factor of $s(s+1)+2$ of an optimal off-line schedule.

## In plain words

Two transactions want the same object, and only one can have it. Greedy settles this by age: the one that started first wins. The younger one either loses the object (it is aborted and starts again) or, if it is the one asking, it waits.

Two details make it work. First, a transaction keeps its age when it is aborted and starts again, so it can only get older relative to newcomers; after enough commits it is the oldest, and the oldest always wins. Second, a transaction that is waiting may lose its objects even to a younger one. A transaction that is stuck waiting must not also block others, so chains of waiting cannot grow and stall the system.

## The problem

In an STM with eager conflict detection, such as DSTM, a transaction opens objects one by one. If it wants an object that another active transaction owns, there is a conflict, and the STM asks the [contention manager](/contention-management/) what to do: abort the other transaction (the enemy), or wait and ask again. The STM stays correct with any answer; the manager only affects progress. A bad manager can [livelock](/livelock/): transactions keep aborting each other and none commits. We want a manager under which every transaction commits, as long as no thread stops for ever.

We use this model. There are $n$ threads, each running one transaction at a time; a transaction opens objects for writing (exclusive access). Threads are asynchronous, and the scheduler is fair: every thread whose transaction is not done takes infinitely many steps. GHP assume that "transaction delays are bounded"; a thread that halts for ever is treated under Pitfalls. Each transaction has a public status (active, committed or aborted), changed by compare-and-swap, and a public `waiting` flag. The timestamps come from a shared counter, so they are distinct.

## The algorithm

```pseudo id=main
BEGIN(A)                                    ▷ a new transaction, not a restart
L1  ts(A) ← fetch-and-add(clock, 1)
L2  waiting(A) ← false
RESOLVE(A, B)                               ▷ A needs an object that active transaction B owns
L3  if ts(B) > ts(A) or waiting(B) then     ▷ rule 1: B is younger, or B is waiting
L4      return ABORT-ENEMY                  ▷ A changes status(B) from active to aborted by CAS
L5  waiting(A) ← true                       ▷ rule 2: B is older and is not waiting
L6  return WAIT                             ▷ A calls RESOLVE again at its next step
OPENED(A)                                   ▷ the object is now A's
L7  waiting(A) ← false
RESTARTED(A)                                ▷ A was aborted; it starts again
L8  waiting(A) ← false                      ▷ ts(A) is kept
```

These are the two rules of the paper: "If B is lower priority than A, or if B is waiting for another transaction, then A aborts B. If B is higher priority than A and is not waiting, then A waits until B commits, aborts, or starts waiting." Waiting is not a blocking call: $A$ checks again at each step, so it sees at once when $B$ commits, is aborted, or starts to wait itself.

## Example

Two transactions: $T_0$ opens $x$ then $y$, and $T_1$ opens $y$ then $x$. $T_0$ has timestamp 0, so it is older. The schedule is $T_0, T_1, T_1, T_0, T_0, T_1, T_1, T_1, T_1$; each row is one step. The state of a transaction is its status, the number of objects it has opened, and its waiting flag.

| step | who | event | owner of $x$ | owner of $y$ | $T_0$ | $T_1$ |
|---|---|---|---|---|---|---|
| 1 | $T_0$ | opens $x$ | $T_0$ | none | active, 1 | active, 0 |
| 2 | $T_1$ | opens $y$ | $T_0$ | $T_1$ | active, 1 | active, 1 |
| 3 | $T_1$ | wants $x$; $T_0$ is older and not waiting (L5) | $T_0$ | $T_1$ | active, 1 | active, 1, waiting |
| 4 | $T_0$ | wants $y$; $T_1$ is younger (L3, L4): abort $T_1$, take $y$ | $T_0$ | $T_0$ | active, 2 | aborted |
| 5 | $T_0$ | commits | none | none | committed | aborted |
| 6 | $T_1$ | restarts with timestamp 1 (L8) | none | none | committed | active, 0 |
| 7 | $T_1$ | opens $y$ | none | $T_1$ | committed | active, 1 |
| 8 | $T_1$ | opens $x$ | $T_1$ | $T_1$ | committed | active, 2 |
| 9 | $T_1$ | commits | none | none | committed | committed |

Compare the Aggressive manager, which always aborts the enemy. After $T_0$ opens $x$, the six steps $T_0, T_1, T_0, T_1, T_0, T_1$ give: $T_0$ opens $y$; $T_1$ aborts $T_0$ and takes $y$; $T_0$ restarts; $T_1$ opens $x$; $T_0$ aborts $T_1$ and takes $x$; $T_1$ restarts. The system is back in the state after the first step, both threads took steps, and nobody committed, so this cycle can repeat for ever. The implementation checks both runs.

## Correctness

Greedy does not affect safety: the STM decides what a transaction reads and when it commits, and the manager only picks who is aborted. The claims are about progress. The full proof is in `proofs/correctness.md`. Its key step is this:

**Lemma.** Let $A$ be the transaction with the smallest timestamp among those that are not committed. After $A$ takes one more step, it never waits again and no transaction aborts it.

$A$ never waits, because rule 2 needs an older enemy that is still active, and there is none. Another transaction $C$ can abort $A$ only by rule 1, which needs $A$ to be younger than $C$ (false) or waiting (false once $A$ has taken a step, since each step of $A$ either clears the flag on L7 or L8 or runs RESOLVE against a younger enemy and aborts it). So, from then on, each step of $A$ opens an object, possibly after aborting its owner, or commits. If $A$ opens $\ell$ objects, it commits within $\ell + 2$ of its own steps after it becomes the oldest: at most one restart (if it was aborted while its flag was still set), at most $\ell$ opens, and the commit. This is the **pending commit property** of GHP: at any time, some running transaction will run without interruption until it commits.

**No livelock.** By the lemma, the oldest transaction that is not done commits within a bounded number of its own steps, and fairness gives it those steps. Then another transaction is the oldest, and so on.

**No starvation.** A transaction keeps its timestamp across aborts, and every transaction that begins later gets a larger one. When $A$ begins, at most $n - 1$ other transactions are running, so at most $n - 1$ transactions are older than $A$ for ever. Each of them commits by the argument above, and then $A$ is the oldest. GHP state this as Theorem 1: "Every transaction commits after a bounded delay."

The implementation for this page checks these claims on every reachable state of small workloads (two or three transactions, up to three objects each, all orders of the timestamps; 1643 states in all). It finds no fair cycle without a commit, it checks the lemma on every edge of the state graph, and it shows that the only state without a step is the one where all transactions committed. Code cannot prove the claim for all workloads; the proof does that.

## Complexity

A decision costs $\Theta(1)$ steps: read the timestamp, the status and the waiting flag of the enemy, and do one compare-and-swap on its status. The manager needs one timestamp and one flag per transaction, and one shared counter. The timestamps grow without bound, so a real system uses a 64-bit counter.

The paper also bounds the **makespan**, the time until the last of $n$ transactions that start at time 0 commits, against an optimal off-line list scheduler that knows the objects each transaction will use. The exact statement is Theorem 9: "Any contention manager that satisfies the pending commit property produces a makespan within a factor of $s(s+1)+2$ of optimal", where $s$ is the number of shared objects. (The abstract uses the same factor; one sentence in Section 4 says $s(s+1)/2$, but the theorem and the abstract give $s(s+1)+2$.) The paper also shows a run that needs $s + 1$ time units where 2 are enough: transactions $T_0, \ldots, T_s$ in a chain over objects $X_1, \ldots, X_s$, where each one aborts the one before it.

The ratio $O(s)$ is not from this paper. Attiya, Epstein, Shachnai and Tamir (PODC 2006, Algorithmica 2010) improved the analysis of Greedy to $O(s)$, and showed that any deterministic work-conserving manager has ratio $\Omega(s)$ in the worst case, so the order $s$ is the best possible in that class.

## Properties

- Livelock free and starvation free, under fair scheduling and with no halted threads.
- Pending commit property: the oldest transaction that has taken a step since it became the oldest is never aborted and never waits.
- Deterministic. It needs no tuning constants, unlike the managers based on backoff.
- Works with eager conflict detection, where conflicts appear while transactions run. The paper notes that managers of this kind do not fit STMs that find conflicts only at commit time.

## Variants and improvements

- **Time-outs for halted threads.** GHP extend the rule so that $A$ waits for an older $B$ only until a time-out, after which $A$ aborts $B$; the time-out doubles each time $A$ has had to abort $B$ in this way. The Timestamp manager of Scherer and Scott also uses ages, and it too aborts an enemy that seems to be inactive. GHP note that priorities by timestamp are an old idea, going back at least to 1978 in databases.
- **Window-based Greedy.** Later work (Sharma and Busch, 2010) groups the transactions of each thread into windows and uses random priorities inside a window, to get better bounds for threads that run many transactions.
- **Global timestamps from other clocks.** Any source of distinct, increasing timestamps works; the paper names logical clocks. What matters is that a transaction with timestamp $t$ has only a bounded number of older transactions.

## When to use it

Use Greedy when a guarantee of progress matters, for example in a system where a long transaction must not starve. The managers based on backoff, such as [Polka](/polka-contention-manager/), have no such guarantee but are tuned for throughput; GHP give benchmark results for Greedy in Section 5 of their paper. In STMs with lazy conflict detection, such as [TL2](/tl2/), a transaction that validates successfully at commit always wins, so a timestamp manager is less useful there.

## Pitfalls

- **Halted transactions.** Without time-outs, a transaction waits for ever for an older one whose thread has stopped (for example, it was descheduled for a long time or crashed). The guarantee needs bounded delays.
- **New timestamp on restart.** If a restarted transaction takes a fresh timestamp, it can lose every conflict again, and starvation freedom is lost. The timestamp must survive aborts.
- **A private waiting flag.** Rule 1 needs to see that the enemy is waiting. If the flag is not visible, a waiting transaction can block a younger one, which blocks another, and the chain makes the system slow; the bound of Theorem 9 also uses the pending commit property, which the flag keeps.
- **Reading the bound as O(s).** The ratio in the 2005 paper is $s(s+1)+2$; the $O(s)$ bound is a later result of a different paper.

## Implementations

## History

Herlihy, Luchangco, Moir and Scherer introduced contention managers with DSTM in 2003, and Scherer and Scott compared many of them in 2004 and 2005, including a Timestamp manager that also favours older transactions. None of those managers had a worst-case guarantee: as GHP note, aborting enemies after a time-out "diminishes the probability of livelocks without however canceling it". Guerraoui, Herlihy and Pochon gave Greedy at PODC 2005, with Theorem 1 (bounded delay) and Theorem 9 (the makespan bound). Attiya, Epstein, Shachnai and Tamir then treated contention management as non-clairvoyant scheduling and proved the $O(s)$ bound.

## References
