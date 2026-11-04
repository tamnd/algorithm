---
tag: Y5EVC6
kind: data-structure
slug: sloppy-counter
name: Sloppy counter
aliases:
- approximate counter
- scalable counter
area: data-structures/concurrent-structures
level: advanced
summary: Per-core local counters periodically flushed to a global counter, trading exactness for scalability.
prereqs: [lock-striping, mutex, lock-ordering]
see_also: [combining-tree, counting-network, fetch-and-add, reference-counting, relaxed-priority-queue, linearization-point, quiescent-consistency, approximate-counting]
sources:
  - url: https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Boyd-Wickizer.pdf
    title: Silas Boyd-Wickizer, Austin T. Clements, Yandong Mao, Aleksey Pesterev, M. Frans Kaashoek, Robert Morris and Nickolai Zeldovich, An analysis of Linux scalability to many cores, OSDI 2010
    locator: Section 4.3 (Sloppy counters) and Figure 2
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/threads-locks-usage.pdf
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces, Chapter 29 (Lock-based Concurrent Data Structures)
    locator: Section 29.1 (Concurrent Counters), the part Scalable Counting, Figures 29.3 and 29.4
  - book: isbn:9780123973375
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, revised reprint
    locator: Chapter 12, Section 12.2 (Shared Counting), for the problem of a contended shared counter
---

A sloppy counter is a shared counter split into one local count per core and one global count. An increment changes only the local count of its core, under the lock of that core, and moves the local count to the global count when it reaches a threshold $S$. A read of the global count is cheap but may be up to $p(S - 1)$ below the true value for $p$ cores; an exact read takes every lock. Boyd-Wickizer and others named it in 2010, when they used it to remove contention on reference counts in the Linux kernel, and the textbook of Arpaci-Dusseau calls the same design an approximate counter. It is [lock striping](/lock-striping/) applied to one integer.

## In plain words

Picture a stadium with four gates and one main counter in the office. If every gate sends a runner to the office for each fan who comes in, the runners crowd the office door. Instead, each gate keeps its own tally on a sheet. When a sheet reaches five fans, the gate sends one runner with the number five and starts a new sheet.

The office number is now a little behind the truth, by at most four fans for each gate, but the office door is quiet. If the exact number is needed, someone stops all gates for a moment and adds the office number and all sheets.

A sloppy counter does this inside a computer. Each core counts on its own, and only now and then touches the shared total.

## The abstract type

The object holds an integer $N$, at first some value $N_0$, and has three operations.

- inc() changes $N$ to $N + 1$.
- exact() returns $N$.
- approximate() returns some $v$ with $N - p(S - 1) \le v \le N$.

The third operation is a relaxed specification: it is nondeterministic, with a bound that depends on the number $p$ of cores and the threshold $S$. The concurrent object is [linearizable](/linearizability/) with respect to this relaxed sequential type. It is not linearizable with respect to an exact counter whose read always returns $N$, unless $S = 1$.

## Representation

- $C.local[0..p-1]$: one count per core, each with a [mutex](/mutex/) $C.lock[i]$.
- $C.global$: the global count, with a mutex $C.glock$.
- $S \ge 1$: the threshold.

A call on core $i$ uses stripe $i$; several threads on one core share it, and take turns at $C.lock[i]$.

**Invariant.** At a moment when no lock is held, $N = C.global + \sum_i C.local[i]$ and $0 \le C.local[i] \le S - 1$ for each $i$. So $N - p(S - 1) \le C.global \le N$.

## Operations

```pseudo id=main
INC(C, i)                                 ▷ i is the core of the caller
L1  acquire(C.lock[i])
L2  C.local[i] ← C.local[i] + 1           ▷ linearization point if no move follows
L3  if C.local[i] ≥ S then
L4      acquire(C.glock)
L5      C.global ← C.global + C.local[i]  ▷ linearization point of a move
L6      release(C.glock)
L7      C.local[i] ← 0
L8  release(C.lock[i])

APPROXIMATE(C)
L9  acquire(C.glock)
L10 v ← C.global                          ▷ linearization point
L11 release(C.glock)
L12 return v

EXACT(C)
L13 for i ← 0 to p − 1 do acquire(C.lock[i])
L14 acquire(C.glock)
L15 v ← C.global + C.local[0] + ... + C.local[p − 1]   ▷ linearization point
L16 release C.glock, then all C.lock[i]
L17 return v
```

**Increment.** The common case is lines L1, L2 and L8: a lock that only this core uses, and a count in a cache line that stays in the cache of this core. Once in $S$ increments, the call also takes the global lock and moves the local count (lines L4 to L7).

**Approximate read.** One read of the global count. Lines L9 and L11 are there for symmetry with the textbook code; a single atomic load gives the same guarantee.

**Exact read.** It takes all locks in one order: the local locks in increasing index, then the global lock. An increment takes a local lock and then the global lock, which agrees with this order, so no cycle of waits can form ([lock ordering](/lock-ordering/)).

## Example

Two cores, $S = 3$, the count starts at 0. Core 0 increments three times and core 1 twice; then reads come in while the third increment of core 0 is moving its count. $N$ is the true count at the linearization points.

| step | thread | what it does | local | global | $N$ |
|---|---|---|---|---|---|
| 1 | core 0 | inc, L1 to L8 | [1, 0] | 0 | 1 |
| 2 | core 1 | inc | [1, 1] | 0 | 2 |
| 3 | core 0 | inc | [2, 1] | 0 | 3 |
| 4 | core 1 | inc | [2, 2] | 0 | 4 |
| 5 | reader | approximate() returns 0 | [2, 2] | 0 | 4 |
| 6 | core 0 | inc, L1 to L3: local[0] is 3 | [3, 2] | 0 | 4 |
| 7 | core 0 | L4, L5: holds glock, global is 3 | [3, 2] | 3 | 5 |
| 8 | reader | approximate(), L9: glock is taken, spins | [3, 2] | 3 | 5 |
| 9 | core 0 | L6, L7: releases glock, local[0] is 0 | [0, 2] | 3 | 5 |
| 10 | reader | L9 to L12: returns 3 | [0, 2] | 3 | 5 |
| 11 | other | exact(), L13: lock 0 is taken, spins | [0, 2] | 3 | 5 |
| 12 | core 0 | L8: releases lock 0; inc returns | [0, 2] | 3 | 5 |
| 13 | other | L13 to L17: returns 3 + 0 + 2 = 5 | [0, 2] | 3 | 5 |

At step 5 the error is $4 = p(S - 1)$, the largest possible. At step 7 the true count becomes 5 at the move, not at step 6: the increment of step 6 is counted from the moment its unit reaches the global count, so the sum of global and local counts would count it twice between steps 7 and 9, but no reader can see that sum then, because the exact read needs lock 0.

## Correctness

Linearize an increment at line L2 if its new local count is below $S$, and at line L5 if it moves the count; the case is fixed at line L2, because only the holder of $C.lock[i]$ changes $C.local[i]$. Linearize the reads at lines L10 and L15. Define for each stripe the *pending* amount $c_i$: $C.local[i]$, minus 1 while the holder is between lines L2 and L5 of a moving increment, and 0 while it is between lines L5 and L7. The key invariant is $N = C.global + \sum_i c_i$ with $0 \le c_i \le S - 1$, where $N$ counts the increments whose points have passed. From it, an approximate read returns a value in $[N - p(S - 1), N]$, and an exact read, which holds every lock and so sees $c_i = C.local[i]$, returns $N$. The lock order makes the counter [deadlock-free](/deadlock-freedom/), and with [starvation-free](/starvation-freedom/) locks each call returns. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | steps | contention |
|---|---|---|
| inc | $O(1)$; the global lock once per $S$ calls of a core | the local lock of its core; the global lock at rate $1/S$ |
| approximate | $O(1)$ | the global lock |
| exact | $O(p)$ | all locks |
| space | $p + 1$ counts and $p + 1$ locks | |

With one shared counter, all $m$ increments pass through one lock or one cache line, so they are serial. With a sloppy counter, the global lock sees about $m/S$ calls, and the local locks are uncontended when each thread stays on its core. The price is the error bound $p(S - 1)$ of the approximate read, and the cost $\Theta(p)$ of an exact read. Arpaci-Dusseau report that with $S = 1024$, four million updates on four processors take hardly more time than one million updates on one processor.

## Variants

- **Reference counts with spare references.** The Linux version of Boyd-Wickizer and others supports increments and decrements of any amount $V$. A core keeps *spare references* in its local count: a decrement adds $V$ to the local count, and an increment takes $V$ from the local count if it has enough, and otherwise adds $V$ to the central count. The invariant is that the central count equals the sum of the local counts plus the references in use. Deciding that the object can be freed needs the reconciling, expensive, exact read.
- **Lock-free stripes.** Replace each local lock by an atomic [fetch-and-add](/fetch-and-add/) on a padded word. Java's `LongAdder` keeps a base and an array of cells, adds cells under contention, and gives an exact sum only in a quiet state.
- **Scalable nonzero indicators (SNZI).** A tree of counters that answers only the question whether the count is zero, which is what many reference counts need.
- **Combining instead of splitting.** A [combining tree](/combining-tree/) or a [counting network](/counting-network/) gives each increment a distinct value, which a sloppy counter cannot do.
- **Probabilistic counting.** The [Morris counter](/morris-counter/) and other [approximate counting](/approximate-counting/) methods save memory, not contention; they are a different kind of approximation.

## When to use it

Use a sloppy counter when updates far outnumber reads and reads can be a little stale: statistics, quotas checked against a soft limit, the memory use of a network protocol, reference counts of objects that are rarely freed. Do not use it when each increment needs the new value, as in a ticket or a sequence number, or when a read must be exact and frequent, because each exact read stops all updates for $\Theta(p)$ lock steps.

## Pitfalls

- **Expecting an exact read from the global count.** The approximate read can miss up to $p(S - 1)$ increments. Code that tests the global count against zero or against a hard limit must use the exact read.
- **A threshold of one.** With $S = 1$ every increment takes the global lock, and the counter is slower than a plain counter.
- **A wrong lock order.** An exact read that takes the global lock first, then the local locks, can deadlock with an increment that holds a local lock and waits for the global lock at line L4.
- **False sharing.** If the local counts of different cores share a cache line, each increment still moves that line between cores, and most of the gain is lost. Pad each count, and each lock, to its own line.
- **Threads that move between cores.** If threads migrate, the per-core lock is still correct but becomes contended. The stripe index must be read once per call (line L1 uses $i$ throughout).

## Implementations

The Python class follows the pseudocode line by line. The operations are generators that yield after each shared step, and each lock is taken by repeated tries, so the tests replay the example, show that cores do not wait for each other, and check random interleavings with a linearizability search against the relaxed counter type above. The plain methods also run under real threads.

## History

Shared counters as a bottleneck are an old theme of parallel computing; combining networks and counting networks attack it by combining or spreading the calls. Boyd-Wickizer, Clements, Mao, Pesterev, Kaashoek, Morris and Zeldovich introduced sloppy counters in their 2010 study of Linux on 48 cores, for the reference counts of directory entries, mount points and routing entries. The textbook of Arpaci-Dusseau presents the simpler version with a threshold, under the name approximate counter.

## References
