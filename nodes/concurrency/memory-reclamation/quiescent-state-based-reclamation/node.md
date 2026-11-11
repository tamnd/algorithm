---
tag: RNB9XT
kind: algorithm
slug: quiescent-state-based-reclamation
name: Quiescent-state-based reclamation
aliases: [QSBR]
area: concurrency/memory-reclamation
level: core
summary: Each thread reports quiescent states, points where it holds no shared references. A node is freed once every thread has passed a quiescent state after its unlink. Reads cost nothing.
solves: [safe-memory-reclamation]
complexity:
  vars: {n: the number of processes, R: the limbo list length that starts an attempt to advance}
  space: {counters: Θ(n)}
  steps: {quiescent_state: O(1), node_read: O(1), advance_attempt: O(n)}
properties: {robust: false, bounded_garbage: false, read_side_cost_free: true, wait_free_reclamation: true}
history:
  year: 1998
  people: [Paul E. McKenney, John D. Slingwine]
  note: McKenney and Slingwine described quiescent states as the basis of read-copy update in 1998. Hart, McKenney, Demke Brown and Walpole named and measured QSBR as a reclamation scheme in 2007.
prereqs: [quiescent-state, epoch-based-reclamation]
see_also: [read-copy-update, grace-period, debra, hazard-pointers, neutralization-based-reclamation, interval-based-reclamation]
sources:
  - paper: "Paul E. McKenney and John D. Slingwine, Read-copy update, using execution history to solve concurrency problems, Parallel and Distributed Computing and Systems (PDCS) 1998, pages 509-518"
  - paper: doi:10.1016/j.jpdc.2007.04.010
    title: Thomas E. Hart, Paul E. McKenney, Angela Demke Brown and Jonathan Walpole, Performance of memory reclamation for lockless synchronization, Journal of Parallel and Distributed Computing 67(12), 2007, pages 1270-1285
    locator: the description of quiescent-state-based reclamation, its fuzzy barrier, and its cost compared with EBR, hazard pointers and lock-free reference counting
  - paper: doi:10.1109/TPDS.2011.159
    title: Mathieu Desnoyers, Paul E. McKenney, Alan S. Stern, Michel R. Dagenais and Jonathan Walpole, User-level implementations of read-copy update, IEEE Transactions on Parallel and Distributed Systems 23(2), 2012, pages 375-382
    locator: the quiescent-state-based user-space RCU, in which threads report quiescent states and go offline when they block
---

Quiescent-state-based reclamation (QSBR) is a [safe memory reclamation](/safe-memory-reclamation/) method in which threads do nothing at all when they read shared nodes. Instead, each thread reports a [quiescent state](/quiescent-state/) from time to time, at a point where it holds no reference to any shared node, for example between two operations. A node that is unlinked waits on a private list until every thread has reported a quiescent state after the unlink. Then no thread can still hold it, and it is freed. The reads are as fast as in a program with no reclamation, but one thread that stops reporting stops all reclamation.

## In plain words

Workers in a warehouse take parcels off a belt. Now and then, each worker puts both hands up to show that they hold nothing, and ticks a box with today's number.

A parcel that is taken off the belt is not shredded at once. It goes into a bin labelled with today's number.

When every worker has ticked today's number, the number goes up by one. A bin is shredded when the number is two past its label. Every worker has shown empty hands since the parcel left the belt, so nobody holds it.

If one worker never puts their hands up, the number stops, and the bins pile up.

## The problem

[Safe memory reclamation](/safe-memory-reclamation/) for a lock-free structure such as the [Treiber stack](/treiber-stack/) or the [Michael and Scott queue](/michael-scott-queue/). A node that one thread unlinks may still be read by another, so an immediate free gives a [use after free](/use-after-free/). QSBR frees the node after a [grace period](/grace-period/), here a time in which every thread passed a quiescent state.

The model: $n$ asynchronous processes that may stop forever between any two steps, on a sequentially consistent shared memory with reads, writes and [compare-and-swap](/compare-and-swap/). $G$ is the global counter. $C[p]$ is the value of $G$ that process $p$ saw at its last quiescent state. Each process keeps a private limbo list of pairs (node, counter). $R$ is the limbo length that starts an attempt to advance. The client reports a quiescent state only where it holds no reference to a shared node.

## The algorithm

```pseudo id=main
QUIESCENT()                          ▷ only where the caller holds no references
L1  e ← G
L2  C[me] ← e
RETIRE(x)                            ▷ x is already unlinked
L3  limbo ← limbo ∪ {(x, G)}         ▷ tag x with the counter after the unlink
    if |limbo| < R then return
L4  e ← G
L5  if every q has C[q] = e then
L6      CAS(G, e, e + 1)             ▷ g is the counter after this attempt
L7  for each (y, r) in limbo with g ≥ r + 2
L8      remove (y, r) from limbo; FREE(y)
```

Compared with [epoch-based reclamation](/epoch-based-reclamation/), there is no BEGIN and no END. A process never says that it is inside an operation; it only says, now and then, that it is outside one. So reads need no shared writes and no fences. The cost moves to the client: it must place QUIESCENT at points where it holds nothing, and it must call it often enough.

The counter $G$ moves from $e$ to $e + 1$ only when every process reported $e$, so between two quiescent states of $p$ that saw $e$, $G$ can go to at most $e + 1$. A node that $p$ can reach in that interval was retired after the first of them, so its tag is at least $e$, and L7 waits until $G \ge e + 2$. That can happen only after $p$ reports again, and by then $p$ has dropped the reference. One step of distance is not enough, for the same reason as in EBR.

Every process counts, including one that has finished its work. Real implementations let a thread go *offline* before it blocks or exits: an offline thread is skipped at L5, and it must come back online, with a fresh counter, before it touches shared nodes.

## Example

A stack $top \to A \to B$, two processes, $R = 1$, and a quiescent state after each operation. At the start $G = 0$ and $C[p] = C[q] = 0$. Process $p$ pops once and process $q$ pops twice.

| step | process | line | action | state after |
|---|---|---|---|---|
| 1 | $p$ | pop | reads $top = A$ | |
| 2 | $q$ | pop | reads $A.next = B$, CAS $top$ from $A$ to $B$ | $top \to B$ |
| 3 | $q$ | L3 | puts $(A, 0)$ in its limbo list | |
| 4 | $q$ | L4 to L6 | $C[p] = C[q] = 0$, so CAS $G$ from 0 to 1 | $G = 1$ |
| 5 | $q$ | L7 | $1 < 0 + 2$, so $A$ stays | limbo $= \{(A, 0)\}$ |
| 6 | $q$ | L1, L2 | quiescent state after the pop | $C[q] = 1$ |
| 7 | $q$ | pop, L3 | pops $B$, puts $(B, 1)$ in its list | $top =$ nil |
| 8 | $q$ | L4, L5 | $C[p] = 0 \ne 1$, so no advance; nothing is freed | $G = 1$ |
| 9 | $p$ | pop | reads $A.next$ and $A.val$ safely; its CAS fails; it reads $top =$ nil | |
| 10 | $p$ | L1, L2 | quiescent state after the pop | $C[p] = 1$ |

With one step of distance, step 5 frees $A$, and $p$ reads a freed node at step 9; the test file finds this run. After step 10 the next attempts of $q$ move $G$ to 2, which frees $A$, and to 3, which frees $B$, once $q$ has reported again.

## Correctness

The full proof is in proofs/correctness.md. It assumes that a process accesses only nodes that were not retired before its last quiescent state, that each node is retired once after it is unlinked, and that an unlinked node is not linked again.

- **Key fact.** If the last quiescent state of $p$ read $G = e$, then $G \le e + 1$ until $p$ reports again, because the advance from $e + 1$ to $e + 2$ needs $C[p] = e + 1$.
- **Safety.** A node that $p$ accesses has a tag $r \ge e$, and it is freed only when $G \ge r + 2 \ge e + 2$, so after $p$ reports again and drops the reference. No node is freed twice.
- **Progress.** If every process reports quiescent states again and again, $G$ grows and every retired node is freed.
- **Not robust.** A process that stops, or stops reporting, holds $G$ at most one above its last report forever.

The test file checks every interleaving of small stack and queue runs with two and three processes, runs with explicit quiescent states, 150 seeded random runs of each kind, and three unsafe variants: one step of distance, a quiescent state reported in the middle of a pop, and an immediate free. It also measures the garbage with and without a stalled process.

## Complexity

| measure | value |
|---|---|
| shared space | $G$ and $n$ counters |
| read of a node | no extra steps |
| QUIESCENT | 2 steps |
| attempt to advance | $O(n)$ reads |
| retired but unfreed nodes | not bounded if a process stops reporting |

**Cost per operation.** QSBR adds no work to the read side at all, not even a store or a fence, which is why the Linux kernel uses it for RCU in non-preemptible builds. The cost is two shared steps per quiescent state, and the client may report less often than once per operation to make it smaller.

**Garbage.** The garbage is the nodes retired since the slowest process last reported, plus two periods. In the test with three processes and 400 operations each and no stall, the peak is at most 30 nodes over ten seeds: it is larger than with EBR because a process that has finished its program never reports again. With process 0 stopped inside its first pop, no node is ever freed, and the peak equals the number of retirements, 50 or 400.

## Properties

- Not robust: one thread that stops reporting stops all reclamation.
- The read side is free: no writes, no fences, no retries.
- The client must know where its quiescent states are; a wrong report gives a use after free that no test of the scheme itself can catch.
- QUIESCENT, RETIRE and the attempt to advance are wait free.
- Idle and blocked threads need an offline mode, or they stop reclamation too.

## Variants and improvements

- **[Epoch-based reclamation](/epoch-based-reclamation/).** Threads announce when they enter and leave an operation, so idle threads do not block anything, at the cost of a write and a fence per operation.
- **[Read-copy-update](/read-copy-update/).** The same grace-period wait packaged as `synchronize_rcu` and `call_rcu`; the Linux kernel uses context switches as quiescent states, and the user-space library liburcu has a QSBR flavour with explicit reports and offline threads.
- **[DEBRA](/debra/).** Brown (2015) reports quiescence at the start of each operation and checks one other thread per operation, so the advance attempt costs $O(1)$.
- **Robust variants.** [Neutralization-based reclamation](/neutralization-based-reclamation/) forces a slow thread to a quiescent state with a signal, and [interval-based reclamation](/interval-based-reclamation/) bounds what a stalled thread can hold.

## When to use it

Use QSBR when the program has natural quiescent points, such as the end of each event or request in a loop of worker threads, or a context switch in a kernel, and when read speed is what matters. It is the fastest scheme for read-mostly data. Avoid it in a library that cannot see its caller's loop, and wherever threads can block for a long time without going offline.

## Pitfalls

**Freeing one period too early.** The wrong code is L7 with $g \ge r + 1$. A process that reported $r$ may still hold a node retired at counter $r$ while $G = r + 1$; the test finds the use after free at once. The right code is $g \ge r + 2$.

**A quiescent state while holding a node.** The wrong code calls QUIESCENT (L1 and L2) inside an operation, after it read a pointer and before it is done with it. Once it reports, its reference is no longer counted, and the node can be freed under it. The test shows this with a report placed between the read of $top$ and the read of $top.next$. The right code reports only between operations.

**Forgetting idle threads.** A thread that finishes its work, or waits on a lock or for I/O, never moves its counter, and the garbage grows. Mark the thread offline before it blocks and online after.

**Reporting too rarely.** A thread that reports once a second keeps a second's worth of garbage alive. Report at least once per bounded amount of work.

## Implementations

## History

McKenney and Slingwine described read-copy update in 1998, with quiescent states such as context switches and a grace period after which every CPU has passed one; the idea had been in the DYNIX/ptx kernel since the early 1990s. Hart, McKenney, Demke Brown and Walpole (2007) used the name QSBR for this reclamation scheme and measured it against epochs, hazard pointers and reference counting: it was the fastest for reads when no thread stalls. Desnoyers and others (2012) gave user-level RCU a QSBR flavour with explicit reports and offline threads, and the Linux kernel still uses quiescent states for non-preemptible RCU.

## References
