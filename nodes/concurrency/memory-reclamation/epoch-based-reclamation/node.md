---
tag: E1V1VX
kind: algorithm
slug: epoch-based-reclamation
name: Epoch-based reclamation
aliases: [EBR, epoch-based memory reclamation]
area: concurrency/memory-reclamation
level: core
summary: Each operation announces the global epoch. The epoch advances when all active operations have seen it, and a node retired in epoch r is freed once the epoch reaches r + 2.
solves: [safe-memory-reclamation]
complexity:
  vars: {n: the number of processes, R: the limbo list length that starts an attempt to advance}
  space: {announcements: Θ(n)}
  steps: {begin_try: O(1), end: O(1), advance_attempt: O(n)}
properties: {robust: false, bounded_garbage: false, per_node_cost: false, wait_free_reclamation: true}
history:
  year: 2004
  people: [Keir Fraser]
  note: Fraser described epoch-based reclamation in his 2004 Cambridge PhD thesis, Practical lock-freedom. Hart, McKenney, Demke Brown and Walpole compared it with QSBR and hazard pointers in 2007.
prereqs: [safe-memory-reclamation, grace-period]
see_also: [quiescent-state-based-reclamation, read-copy-update, debra, hazard-pointers, hazard-eras, interval-based-reclamation, neutralization-based-reclamation, hyaline]
sources:
  - url: https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-579.pdf
    title: Keir Fraser, Practical lock-freedom, PhD thesis, University of Cambridge, Technical Report UCAM-CL-TR-579, 2004
    locator: the section on epoch-based garbage collection, with the global epoch, the per-thread epoch and the three limbo lists
  - paper: doi:10.1016/j.jpdc.2007.04.010
    title: Thomas E. Hart, Paul E. McKenney, Angela Demke Brown and Jonathan Walpole, Performance of memory reclamation for lockless synchronization, Journal of Parallel and Distributed Computing 67(12), 2007, pages 1270-1285
    locator: the description of epoch-based reclamation and its measured cost next to QSBR, hazard pointers and lock-free reference counting, including the effect of a preempted thread
  - paper: doi:10.1145/2767386.2767436
    title: Trevor Brown, Reclaiming memory for lock-free data structures, there has to be a better way, PODC 2015, pages 261-270
    locator: the survey of reclamation schemes and the account of why a thread that stops inside an operation stops epoch-based reclamation
---

Epoch-based reclamation (EBR) is a [safe memory reclamation](/safe-memory-reclamation/) method that works per operation, not per node. A shared counter, the global epoch, numbers the phases of the run. Each operation first writes the current epoch into its own announcement slot and clears the slot at the end. A node that is unlinked is put on a private limbo list with the epoch at that time. The epoch moves forward only when every active operation has announced the current one, and a node retired in epoch $r$ is freed once the epoch reaches $r + 2$. By then every operation that could have seen the node has ended. Reads cost nothing extra, but one thread that stops inside an operation stops all reclamation.

## In plain words

A library has a big clock on the wall that shows a day number. When you come in, you write today's number on your own card. When you leave, you wipe the card.

When a book is withdrawn, the librarian does not destroy it at once. She puts it in a box marked with today's number.

The clock moves to the next day only when every card on the wall shows today's number or is empty. A box is destroyed when the clock is two days past its number. Anyone who could have touched those books came in at least two days ago and has left by now.

If one reader falls asleep inside, the clock stops, and the boxes pile up.

## The problem

[Safe memory reclamation](/safe-memory-reclamation/) for a lock-free structure such as the [Treiber stack](/treiber-stack/) or the [Michael and Scott queue](/michael-scott-queue/). A node that one process unlinks may still be read by another process, so an immediate free gives a [use after free](/use-after-free/). EBR waits for a [grace period](/grace-period/): a time after which every operation that was running at the unlink has ended.

The model: $n$ asynchronous processes that may stop forever between any two steps, on a sequentially consistent shared memory with reads, writes and [compare-and-swap](/compare-and-swap/). $G$ is the global epoch. $A[p]$ is the announcement of process $p$: $\bot$ outside an operation, or an epoch. Each process keeps a private limbo list of pairs (node, epoch). $R$ is the limbo length that starts an attempt to advance.

## The algorithm

```pseudo id=main
BEGIN()                              ▷ at the start of each operation
L1  e ← G
L2  A[me] ← e                        ▷ announce the epoch
L3  if G ≠ e then goto L1            ▷ the epoch moved: announce again
END()                                ▷ at the end of each operation
L4  A[me] ← ⊥
RETIRE(x)                            ▷ x is already unlinked
L5  limbo ← limbo ∪ {(x, G)}         ▷ tag x with the epoch after the unlink
    if |limbo| < R then return
L6  e ← G
L7  if every q has A[q] = ⊥ or A[q] = e then
L8      CAS(G, e, e + 1)             ▷ g is the epoch after this attempt
L9  for each (y, r) in limbo with g ≥ r + 2
L10     remove (y, r) from limbo; FREE(y)
```

An operation that announced $e$ holds the epoch at $e$ or $e + 1$: to go from $e + 1$ to $e + 2$, the check at L7 must see $A[p] = e + 1$ or $\bot$, and $p$ writes neither until it ends. A node that this operation can reach is retired after the operation began, so its tag is at least $e$, and L9 waits for $e + 2$. The two steps of distance are both needed. One step only says that the node was unlinked in epoch $r$, and an operation that announced $r$ may still hold it while the epoch is $r + 1$.

L3 closes a race in BEGIN. Without it, a process could read $G = e$, pause while the epoch moves twice, and then announce the old $e$ and read nodes that were retired after it read $G$ and already freed. The re-read makes the announced value the current epoch at the moment the operation starts.

Fraser's original keeps three limbo lists per thread, one for each epoch modulo 3, and frees a whole list when the thread sees the epoch move. The version above keeps one list with the tag in each entry; it frees the same nodes at the same times.

## Example

A stack $top \to A \to B$, two processes, and $R = 1$, so every RETIRE tries to advance. Process $p$ pops once and process $q$ pops twice.

| step | process | line | action | state after |
|---|---|---|---|---|
| 1 | $p$ | L1 to L3 | reads $G = 0$, announces 0 | $A[p] = 0$ |
| 2 | $p$ | pop | reads $top = A$ | |
| 3 | $q$ | L1 to L3 | announces 0 | $A[q] = 0$ |
| 4 | $q$ | pop | reads $A.next = B$, CAS $top$ from $A$ to $B$ | $top \to B$ |
| 5 | $q$ | L5 | puts $(A, 0)$ in its limbo list | |
| 6 | $q$ | L6 to L8 | every announcement is 0, so CAS $G$ from 0 to 1 | $G = 1$ |
| 7 | $q$ | L9 | $1 < 0 + 2$, so $A$ stays | limbo $= \{(A, 0)\}$ |
| 8 | $q$ | L4 | ends the pop | $A[q] = \bot$ |
| 9 | $q$ | L1 to L3, pop, L5 | announces 1, pops $B$, puts $(B, 1)$ in its list | $top =$ nil |
| 10 | $q$ | L6, L7 | $A[p] = 0 \ne 1$, so no advance; nothing is freed | $G = 1$ |
| 11 | $p$ | pop | reads $A.next$ and $A.val$ safely; its CAS fails; it reads $top =$ nil | |
| 12 | $p$ | L4 | ends; the stack was empty for it | $A[p] = \bot$ |

At step 7 a test with one epoch of distance, $g \ge r + 1$, frees $A$, and $p$ reads a freed node at step 11. The test file finds this run when L9 uses $r + 1$. After step 12, the next attempt of $q$ advances to 2 and then to 3, and frees $A$ and then $B$.

## Correctness

The full proof is in proofs/correctness.md. It assumes that a process touches nodes only inside BEGIN and END, that every node it reaches was not retired before its BEGIN, that each node is retired once after it is unlinked, and that an unlinked node is not linked again.

- **Key fact.** An operation that announced $e$ keeps $G \le e + 1$ until it ends, because the check at L7 that would move $G$ from $e + 1$ to $e + 2$ reads its announcement after the epoch reached $e + 1$ and sees $e$.
- **Safety.** A node it accesses has a tag $r \ge e$, and L9 waits for $G \ge r + 2 \ge e + 2$, which happens only after the operation ends. No node is freed twice.
- **Progress.** If no operation runs forever, the epoch keeps moving and every retired node is freed.
- **Not robust.** If one process stops inside an operation that announced $e$, the epoch never passes $e + 1$, and no node retired after that is freed.

The test file checks every interleaving of small stack and queue runs with two and three processes, 150 seeded random runs of each kind, the use after free with one epoch of distance or with an immediate free, and the growth of garbage under a stall.

## Complexity

| measure | value |
|---|---|
| shared space | $G$ and $n$ announcements |
| BEGIN | 3 steps per try; it retries only if the epoch moved |
| END | 1 step |
| attempt to advance | $O(n)$ reads, one per announcement |
| reads of nodes | no extra cost |
| retired but unfreed nodes | not bounded if a process stops inside an operation |

**Cost per node.** A read of a node costs nothing extra, which is the main gain over [hazard pointers](/hazard-pointers/). The cost is per operation: two writes and two reads of shared words, and on real hardware one store-load fence after L2. An attempt to advance reads $n$ announcements; with $R = n$ the cost per retired node is $O(1)$ amortized.

**Garbage.** With no stall, the garbage is the nodes retired in the last two or three epochs plus up to $R$ per limbo list. In the test with three processes and 400 operations each, the peak is at most 11 nodes over ten seeds. With process 0 stopped inside its first pop, the two others retire one node per two operations and none is ever freed: the peak is exactly 50 for runs of 50 operations and 400 for runs of 400, so the garbage grows with the run length.

## Properties

- Not robust: one stalled operation stops all reclamation, and the garbage can fill memory.
- BEGIN is lock free; END, RETIRE and the attempt to advance are wait free.
- No cost per node read, so long traversals are as fast as without reclamation.
- The client does not say which nodes it holds; it only marks the start and the end of each operation.
- Every operation writes a shared slot, so on real hardware BEGIN needs a store-load fence.

## Variants and improvements

- **[Quiescent-state-based reclamation](/quiescent-state-based-reclamation/).** Threads report quiescent states between operations instead of announcing epochs inside them; reads cost nothing at all, but the client must place the reports.
- **[DEBRA](/debra/).** Brown (2015) checks one other thread's announcement per operation instead of all of them, which makes the attempt to advance $O(1)$; DEBRA+ adds signals to make it robust.
- **Robust hybrids.** [Hazard eras](/hazard-eras/) and [interval-based reclamation](/interval-based-reclamation/) bound the garbage by letting a stalled thread hold back only the nodes alive in its announced epoch range. [Neutralization-based reclamation](/neutralization-based-reclamation/) restarts a stalled reader with a signal.
- **[Read-copy-update](/read-copy-update/).** The same grace-period idea as a programming interface, with readers in read-side critical sections and a synchronize call for writers.

## When to use it

Use EBR when operations are short and threads are not preempted for long, for example in a runtime with a fixed set of worker threads, and when reads dominate: it is the fastest of the general methods for traversals. Crossbeam in Rust and many research systems use it. Avoid it in a library whose callers can block or be descheduled inside an operation, or with oversubscribed cores; there [hazard pointers](/hazard-pointers/), [hazard eras](/hazard-eras/) or [interval-based reclamation](/interval-based-reclamation/) keep the memory bounded.

## Pitfalls

**Freeing one epoch too early.** The wrong code is L9 with $g \ge r + 1$. An operation that announced $r$ may still hold a node retired in epoch $r$ while $G = r + 1$; the test finds the use after free at once. The right code is $g \ge r + 2$.

**Announcing without the re-read.** The wrong code is L1 and L2 and then use nodes. If the epoch moves twice between L1 and L2, the announced value is stale, and nodes retired after the read of $G$ can be freed while the operation reads them. The right code re-reads $G$ at L3 and announces again if it moved.

**Tagging with an old epoch.** The tag at L5 must be read after the unlink. Reading $G$ at the start of the operation and using it as the tag can give a tag that is one epoch too small, which has the same effect as freeing one epoch too early.

**Holding a node across operations.** A pointer kept after END is not protected. The client must not cache node addresses between operations.

**Blocking inside an operation.** A thread that waits for I/O or a lock between BEGIN and END stops reclamation for everyone. Keep operations short and nonblocking.

## Implementations

## History

Keir Fraser described epoch-based reclamation in his 2004 Cambridge PhD thesis on practical lock-free data structures, with a global epoch, per-thread epochs and three limbo lists. The idea of waiting until every thread has passed a point goes back to the quiescent states of read-copy-update by McKenney and Slingwine (1998). Hart, McKenney, Demke Brown and Walpole measured EBR, QSBR, hazard pointers and lock-free reference counting in 2007 and showed that epochs are fast when no thread stalls. Brown's DEBRA (2015) made the epoch check cheap, and a line of work since then, hazard eras (2017), interval-based reclamation (2018), Hyaline (2019) and NBR (2021), keeps the speed of epochs while bounding the garbage.

## References
