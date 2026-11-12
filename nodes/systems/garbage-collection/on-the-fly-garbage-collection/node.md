---
tag: R73E8Z
kind: algorithm
slug: on-the-fly-garbage-collection
name: On-the-fly garbage collection
aliases:
- on-the-fly collector
- Doligez-Leroy-Gonthier collector
- DLG collector
area: systems/garbage-collection
level: research
summary: "Concurrent mark-sweep that never stops all threads at once. The collector posts a status, each thread answers alone at a safe point, and a barrier that depends on the status keeps marking safe."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {H: the number of cells in the heap, p: the number of pointer fields in a cell, L: the number of reachable cells, R: the number of registers of all threads together}
  time: {worst: O(R + p L + H), best: Θ(H)}
  space: {extra: O(H)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1978
  people: [Edsger W. Dijkstra, Leslie Lamport, Damien Doligez, Xavier Leroy, Georges Gonthier]
  note: Dijkstra, Lamport, Martin, Scholten and Steffens (1978) gave a collector that runs beside one mutator with no pause, as an exercise in proofs of concurrent programs. Doligez and Leroy (1993) and Doligez and Gonthier (1994) made it work for many threads with handshakes. Domani, Kolodner and Petrank (2000) built a generational version in a Java virtual machine.
prereqs: [concurrent-garbage-collection, snapshot-at-the-beginning]
see_also: [tricolor-marking, incremental-update-barrier, write-barrier, mutator-and-collector, stop-the-world-collection, parallel-garbage-collection, generational-garbage-collection]
sources:
  - paper: doi:10.1145/359642.359655
    title: "Edsger W. Dijkstra, Leslie Lamport, A. J. Martin, C. S. Scholten and E. F. M. Steffens, On-the-fly garbage collection, an exercise in cooperation, Communications of the ACM 21(11), 966-975, 1978"
    locator: The collector with three colors that runs beside one mutator, and its invariants
  - paper: doi:10.1145/579.587
    title: "Mordechai Ben-Ari, Algorithms for on-the-fly garbage collection, ACM Transactions on Programming Languages and Systems 6(3), 333-344, 1984"
    locator: A version with two colors and a simpler proof
  - paper: doi:10.1145/158511.158611
    title: "Damien Doligez and Xavier Leroy, A concurrent, generational garbage collector for a multithreaded implementation of ML, POPL 1993, 113-123"
    locator: The shared major heap collected on the fly, with handshakes between the collector and each thread
  - paper: doi:10.1145/174675.174673
    title: "Damien Doligez and Georges Gonthier, Portable, unobtrusive garbage collection for multiprocessor systems, POPL 1994, 70-83"
    locator: The collector with the statuses sync1, sync2 and async, its write barrier, and its correctness proof
  - paper: doi:10.1145/349299.349336
    title: "Tamar Domani, Elliot K. Kolodner and Erez Petrank, A generational on-the-fly garbage collector for Java, PLDI 2000, 274-284"
    locator: The adaptation of the handshake collector to Java threads, with generations
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 15 (concurrent collection and handshakes) and Chapter 16 (concurrent mark-sweep, on-the-fly marking)
---

An on-the-fly garbage collector is a [concurrent collector](/concurrent-garbage-collection/) that never stops all the threads of the program at the same moment. A mostly concurrent collector still has short global pauses, to mark the roots and to finish the marking. An on-the-fly collector replaces each of them by a *handshake*: the collector posts a request, and each thread answers it alone, at one of its own safe points, while the other threads keep running. In the collector of Doligez, Leroy and Gonthier (DLG), the collector posts three statuses in turn, sync1, sync2 and async. A thread shades its own roots when it answers async. A write barrier that depends on the status of the thread keeps every reachable cell visible to the collector while the threads answer at different times.

## In plain words

Many programs run several threads that share the same memory. To find the unused memory, a collector must first learn what each thread holds. A simple way is to stop all the threads together. With many threads, this stop costs time, because all must wait for the slowest one.

An on-the-fly collector never stops all the threads together. It posts a message, and each thread reads it when it is ready, does a small task, and goes on. One message asks each thread to tell the collector what it holds.

The risk is that the threads answer at different times. A thread that has already answered can take an item from a thread that has not. To prevent this, all threads first turn on extra checks on their pointer writes, and only then do they report what they hold.

## The problem

**Heap model.** One shared heap of $H$ cells with $p$ pointer fields each. There are several mutator threads. Each thread has its own registers, which are its roots, and it loads, stores, clears registers and allocates. A thread can reach a cell of another thread only through the heap. One collector thread marks and sweeps.

**Concurrency model.** The steps of the threads and of the collector interleave in any order. Each step is atomic. A store takes two steps: the thread first reads the collector's flag, then shades and writes; the collector can move between the two. A thread changes its status only at a *safe point*, between two of its own operations.

**Goal.** Free only cells that are unreachable from the registers of all threads, with no step that waits for all threads at once. Each thread pauses only for its own handshake work, which is the shading of its own registers.

## The algorithm

$W$ is the shared gray stack, and SHADE$(y)$ marks a non-nil unmarked $y$ and pushes it on $W$. The flag *marking* is true from the post of async until the trace ends. Each thread $m$ has a status, $\textit{status}_m$; outside a cycle it is async.

```pseudo id=main
COLLECTOR-CYCLE()
L1  for each status in sync1, sync2, async do post the status
L2      wait until every thread has answered it        ▷ no thread waits for this
L3  while W is not empty do x ← pop W
L4      for each field f of x do SHADE(x.f)
L5  s ← 0
L6  while s < H do if s is marked then clear the mark of s
L7      else if s is not free then put s on the free list
L8      s ← s + 1

ANSWER(m)                                               ▷ at a safe point of thread m
L9  status_m ← the posted status
L10 if status_m = async then for each register r of m do SHADE(r)

WRITE(m, x, f, y)                                       ▷ thread m stores y into x.f
L11 flag ← marking                                      ▷ the collector may move on here
L12 if status_m ∈ {sync1, sync2} then SHADE(x.f); SHADE(y)
L13 else if flag then SHADE(x.f)
L14 x.f ← y

ALLOCATE(m)
L15 take a free cell x; mark x if status_m = async and marking, or the sweep has not reached x
```

The three statuses have three roles.

- **sync1 and sync2.** While a thread is in one of these statuses, its barrier shades both the old and the new value of each field it writes. This is the deletion barrier of [snapshot-at-the-beginning](/snapshot-at-the-beginning/) and the insertion barrier of [incremental update](/incremental-update-barrier/) at once.
- **async.** When a thread answers async, it shades its registers. From then until the trace ends, its barrier shades the old value only, as in snapshot marking, and it allocates black.
- **The order.** The collector posts async only after every thread has answered the sync statuses. So when the first thread shades its roots, every thread already runs a barrier that shades deleted pointers.

The trace needs no termination protocol with the threads. When every thread has answered async and $W$ is empty, every reachable cell is marked, and a barrier can only shade the old value of a field of a reachable cell, which is then marked already.

## Example

$G$ is a shared cell in register 0 of two threads, $G.f_0 = B$ and $B.f_0 = Z$. Thread 0 loads $B$ and then $Z$ into its registers. Thread 1 loads $B$ and stores nil into $B.f_0$. Consider a collector that skips the sync statuses and posts async at once.

| step | who | action | effect |
|---|---|---|---|
| 1 | thread 1 | loads $B$ into register 1 | |
| 2 | thread 1 | starts the store into $B.f_0$ and reads the flag: false | |
| 3 | collector | posts async | the flag is now true |
| 4 | thread 0 | answers async (L10) | $G$ is gray |
| 5 | thread 0 | loads $B$, then $Z$ | $Z$ is white, in a register of thread 0 |
| 6 | thread 1 | ends the store (L13 with flag false) | $B.f_0$ = nil, $Z$ is not shaded |
| 7 | thread 1 | answers async | $B$ is gray |
| 8 | collector | traces $G$ and $B$, then sweeps | $Z$ is freed while thread 0 holds it |

With the sync statuses, the post at step 3 is sync1, and thread 1 cannot answer before its store ends. The collector waits for that answer, so the store ends before async is posted, and thread 0 shades its registers only after $B.f_0$ is nil. If thread 0 loaded $Z$ earlier, $Z$ is in its registers when it answers; if later, it cannot reach $Z$ at all. Over all schedules of these two programs with one collector cycle, the version with only async frees a reachable cell in 50 of 474461 schedules. The full protocol frees none in 8881776, and none in 7901664022 schedules of a longer program in which thread 0 also moves $Z$ into $G$ and drops its registers. Without the barrier, 112656 of 8431446 schedules of the short program fail.

## Correctness

The proof in the proofs section follows the snapshot argument, with one snapshot per thread.

1. **The barrier is on before any root is shaded.** The async post comes after every thread has answered sync1 and sync2. A thread changes status only at safe points, so a store that read the old flag ends before its thread answers sync1. From the answer of sync1 on, the thread's barrier shades every deleted pointer.
2. **Snapshot paths.** Call a cell *protected* if it is gray, or reachable from a gray cell through white cells. Let $t_m$ be the moment that thread $m$ answers async. Every white cell in the registers of a thread that has answered, and every white cell reachable from such a cell, stays protected: a path through white cells is cut only by a store, and that store shades the old value.
3. **Threads that have not answered.** A cell that such a thread moves into the heap is shaded by line L12, and a cell it holds in a register is shaded when it answers. So it cannot hand a white cell to an answered thread without shading it.
4. **End of the trace.** When all threads have answered and $W$ is empty, no cell is gray, so every protected cell is marked; each reachable cell is protected or marked. Cells allocated after the answers are black.

So the sweep frees only cells that are unreachable when the trace ends, and they stay unreachable.

## Complexity

The model is the [word RAM](/word-ram/) with the heap model above.

- **Collector work per cycle.** $O(R)$ for the shading of the registers, $O(pL)$ for the trace, and $\Theta(H)$ for the sweep: $O(R + pL + H)$, the same as a [stop-the-world](/stop-the-world-collection/) mark-sweep.
- **Pause per thread.** One handshake answer costs $O(1)$ for sync1 and sync2 and $O(r_m)$ for async, where $r_m$ is the number of registers of thread $m$. No step waits for the slowest thread, except the collector.
- **Barrier.** $O(1)$ per store: one or two SHADE calls. The barrier reads the status of the thread and the flag, and it is active only during a cycle.
- **Space.** One mark bit per cell, the stack $W$, and the floating garbage of a snapshot collector.

## Properties

- **No global pause.** Each thread stops only to shade its own registers.
- **Non-moving.** It is a mark-sweep collector; the heap can fragment.
- **Floating garbage.** As in snapshot marking, every cell reachable when its thread answered async, and every cell allocated during marking, survives the cycle.
- **A fine-grained design.** Doligez and Gonthier prove the algorithm with the steps of the barrier interleaved with the collector. The model on this page is coarser: a store is two steps, and a shade is one. In this model, sync1 and async alone already give no loss in the exhaustive test.

## Variants and improvements

- **One mutator.** The collector of Dijkstra et al. has one mutator and one collector and no handshake. The mutator shades the new target of each store; the order of the store and the shade inside the barrier matters, and Woodger found an error in an earlier version that had the opposite order. Ben-Ari (1984) gave a version with two colors and a simpler proof.
- **Thread-local young heaps.** Doligez and Leroy (1993) gave each thread its own young generation, collected by the thread alone, and collected only the shared old heap on the fly.
- **Generations in Java.** Domani, Kolodner and Petrank (2000) added generations to the handshake collector in a Java virtual machine.
- **Handshakes elsewhere.** Many production collectors replace some global pauses by per-thread handshakes, for example to scan the stacks of threads one at a time.
- **Parallel marking.** The trace can use several collector threads; see [parallel garbage collection](/parallel-garbage-collection/).

## When to use it

Use it when there are many threads and a global pause is too costly, even a short one: the time to stop every thread grows with the number of threads and with the slowest one. A [mostly concurrent collector](/concurrent-garbage-collection/) is simpler and gives short pauses when the threads reach safe points quickly. If objects must move, the collector also needs a read barrier or forwarding.

## Pitfalls

- **Shading roots before the barrier is on everywhere.** The example shows the loss when the sync statuses are skipped.
- **A status change inside a barrier.** A thread must not answer a handshake between the two steps of a store. Safe points lie between operations.
- **The order inside the barrier.** In a concurrent setting, the shade and the store are separate steps. With a deletion barrier, the old value must be read and shaded before the new value is written; with an insertion barrier, Woodger's scenario shows how the wrong order fails.
- **Stale shading after the cycle.** A barrier that read the flag during marking can shade a cell after the trace ends. If that mark is not cleared by the sweep, the cell looks black in the next cycle although it was never scanned. Shade only while marking, or use alternating colors.
- **Threads that do not reach a safe point.** A thread in a long loop with no safe point delays the handshake, and the collector cannot go on.

## Implementations

## History

Dijkstra, Lamport, Martin, Scholten and Steffens wrote their 1978 paper as an exercise in reasoning about concurrent programs. It introduced the three colors. Steele (1975) had given a concurrent collector with a different barrier. Ben-Ari (1984) simplified the algorithm and its proof. Doligez and Leroy (1993) built a concurrent collector for Concurrent Caml Light with handshakes between the collector and many threads, and Doligez and Gonthier (1994) refined the algorithm and proved it correct. Domani, Kolodner and Petrank (2000) brought the method to Java.

## References
