---
tag: 02511Y
kind: technique
slug: parallel-garbage-collection
name: Parallel garbage collection
aliases:
- multi-threaded GC
- parallel collector
- parallel marking
- work-stealing garbage collection
area: systems/garbage-collection
level: advanced
summary: "Run one collection on several collector threads in a pause. Work stealing spreads the gray objects, atomic marks keep work single, and a termination protocol ends the phase."
history:
  year: 1997
  people: [Toshio Endo, Kenjiro Taura, Akinori Yonezawa, Christine H. Flood, David Detlefs, Nir Shavit, Xiaolan Zhang]
  note: Halstead's Multilisp (1984) already copied in parallel. Endo, Taura and Yonezawa (1997) balanced parallel marking with work stealing on a shared-memory machine, and Flood, Detlefs, Shavit and Zhang (2001) used work-stealing deques for parallel copying and parallel mark-compact in a Java virtual machine.
prereqs: [mark-and-sweep, stop-the-world-collection, work-stealing, compare-and-swap]
see_also: [chase-lev-deque, arora-blumofe-plaxton-deque, termination-detection, concurrent-garbage-collection, cheney-copying-collector, garbage-first-collector, tricolor-marking, work-span-model]
sources:
  - paper: doi:10.1145/509593.509641
    title: "Toshio Endo, Kenjiro Taura and Akinori Yonezawa, A scalable mark-sweep garbage collector on large-scale shared-memory machines, Supercomputing 1997"
    locator: Parallel marking with a mark stack per processor, stealing of work, and the split of large objects
  - paper: "Christine H. Flood, David Detlefs, Nir Shavit and Xiaolan Zhang, Parallel garbage collection for shared memory multiprocessors, USENIX Java Virtual Machine Research and Technology Symposium (JVM 2001)"
    title: "Christine H. Flood, David Detlefs, Nir Shavit and Xiaolan Zhang, Parallel garbage collection for shared memory multiprocessors, JVM 2001"
    locator: Work-stealing deques for parallel copying and parallel mark-compact, and the termination protocol
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 14 (parallel garbage collection, load balancing, termination, parallel marking, copying, sweeping and compaction)
---

A parallel garbage collector runs one collection on several collector threads at the same time, while the program is stopped. It does not shorten the total work; it divides the work of the [stop-the-world pause](/stop-the-world-collection/) among $P$ processors, so the pause can be up to $P$ times shorter. This is a different axis from [concurrent collection](/concurrent-garbage-collection/), in which the collector runs while the program runs; a collector can be parallel, concurrent, both, or neither. Three problems come with parallel tracing. The work must be balanced, because the heap graph is not known in advance; *work stealing* solves this. No object may be processed twice; an atomic test-and-set of the mark bit, or a [compare-and-swap](/compare-and-swap/) on the forwarding pointer, solves this. And the threads must agree that the work is finished, which is a [termination detection](/termination-detection/) problem.

## In plain words

When memory is cleaned with the program stopped, the stop can be shortened by using several helpers at once.

The helpers follow pointers from item to item. No one knows in advance how much work hides behind each pointer, so a fixed split leaves some helpers with nothing to do. Instead, each helper keeps its own pile of items to visit, and a helper with an empty pile takes an item from the pile of another helper.

Two helpers could reach the same item. A single machine instruction lets only one of them claim it. At the end, the helpers must all agree that every pile is empty before they stop.

## When it applies

**Heap model.** A heap of $n$ cells with $p$ pointer fields each, and a set of roots. The program is stopped. $P$ collector threads share the heap and a mark bit per cell. The *work* $T_1$ is the number of reachable cells (each is scanned once), and the *span* $T_\infty$ is the length of the longest chain of cells that must be scanned one after another, that is, the depth of the reachable graph in the order of discovery. By the [work-span model](/work-span-model/), no schedule marks in fewer than $\max(T_1/P, T_\infty)$ steps.

**What is measured.** The pause, the speedup over one thread, the balance of scanned cells per thread, the number of steals, and the cost of atomic operations.

Use it when the machine has several processors and the collector stops the program anyway. Almost every production collector for a multiprocessor marks, copies or compacts in parallel during its pauses.

## The template

Parallel marking with work stealing, in the style of Endo, Taura and Yonezawa and of Flood et al. Each worker $i$ owns a deque $D_i$ of gray cells and works at its bottom; thieves take from its top, as in [work stealing](/work-stealing/). *active* is a shared count of workers that are not trying to stop; it starts at $P$. The roots are marked and spread over the deques first.

```pseudo id=main
WORKER(i)
L1  while worker i has not stopped do
L2      if D_i is not empty then x ← POP-BOTTOM(D_i)
L3          for each field y of x do
L4              if y ≠ nil and TEST-AND-SET(mark[y]) then PUSH-BOTTOM(D_i, y)
L5      else v ← a random other worker whose deque is not empty
L6          if v exists then
L7              PUSH-BOTTOM(D_i, STEAL-TOP(D_v))
L8          else                                          ▷ offer to stop
L9              atomically active ← active − 1
L10             spin: if some deque is not empty then atomically active ← active + 1, and go to L1
L11                   if active = 0 then stop
```

TEST-AND-SET sets the mark bit and returns true only to the thread that set it, so each reachable cell is pushed and scanned exactly once.

### Why it is correct

**Marking.** The argument of [mark-and-sweep](/mark-and-sweep/) holds with many deques. Every marked cell is in some deque or has been scanned. A scanned cell has all its fields marked. When all deques are empty, the marked set contains the roots and is closed under the fields, so it is the reachable set.

**Termination.** A worker pushes only to its own deque, and it offers to stop only when its own deque is empty. So a non-empty deque belongs to a worker that is counted in *active*. If a worker sees $\textit{active} = 0$ at line L11, every deque is empty, no worker can push again, and marking is complete. A worker that sees work at line L10 adds itself back before it steals, so *active* never reaches 0 while work remains.

### Cost

- **Steps.** In a simulation of $P$ workers in rounds, marking a complete binary tree of 1023 cells takes 1025, 516, 270 and 167 rounds for $P = 1, 2, 4, 8$; the scanned cells per worker differ by at most 8. Without stealing, one worker scans all 1023 cells.
- **Span.** A linked list of 200 cells has span 200 and no parallelism. With 4 workers it takes 822 rounds, more than one worker's 202, because the only gray cell moves from thief to thief.
- **Atomics.** One test-and-set per field that points to an unmarked cell. A test of the bit before the atomic operation avoids most of them.
- **Steals.** Each steal is a synchronized operation on another worker's deque, but it happens only when a worker runs out of work. With randomized stealing on a [Chase-Lev](/chase-lev-deque/) or [Arora-Blumofe-Plaxton](/arora-blumofe-plaxton-deque/) deque, the expected number of steals is $O(P\,T_\infty)$.

## Classic examples

**Parallel copying.** Several threads run [Cheney's scan](/cheney-copying-collector/) on separate parts of to-space. Two threads may try to copy the same object; each copies it into its own buffer and tries to install the forwarding pointer with compare-and-swap. The loser discards its copy and uses the winner's. Flood et al. use work-stealing deques for the objects still to scan.

**Parallel mark-compact.** Mark in parallel as above, then split the heap into regions, compute the new address of each live object per region with a prefix sum, and move the regions in parallel. Flood et al. did this for the old generation of the HotSpot JVM.

**Parallel sweeping.** Split the heap into chunks and give one chunk at a time to each thread; there is no dependence between chunks.

**Systems.** The parallel collector of the HotSpot JVM, the young-generation pauses of [Garbage-First](/garbage-first-collector/), and the marking threads of most concurrent collectors all use work stealing.

## Variations

- **Steal half.** Take half of the victim's deque in one steal, which cuts the number of steals when deques are long.
- **Split large objects.** An array of a million references is one unit of work; push it as several ranges so that others can steal the parts. Endo, Taura and Yonezawa split large objects this way.
- **Overflow.** A deque of fixed size can fill. Mark the overflowing objects and find them again later by a scan of the heap, or link them on a list.
- **Termination protocols.** The counter above is simple. Other protocols use a status word with one bit per thread, or the distributed algorithms of [termination detection](/termination-detection/) when the threads do not share memory.
- **Parallel and concurrent.** A [concurrent collector](/concurrent-garbage-collection/) can run several marking threads; the barriers of the mutator then push to the same work lists.

## Pitfalls

- **Marking without an atomic operation.** If two threads test the bit and then set it, both may push the cell, and it is scanned twice. For marking this only wastes work; for copying it makes two copies of one object, which is wrong.
- **Termination when a steal is in flight.** A thief that has removed a cell from a deque but not yet pushed it holds work that no deque shows. The protocol must count the thief as active while it steals: here, a worker leaves *active* only after its failed steal, and re-enters it before it steals.
- **Too fine a balance.** Stealing single cells on a deep, narrow graph moves the only work around and makes the pause longer, as the list example shows.
- **False sharing.** Mark bits of nearby objects share a cache line. Atomic updates on them by several threads slow each other down.
- **Serial phases.** Root scanning, reference processing or a final serial step limit the speedup, as [Amdahl's law](/amdahls-law/) says.

## Exercises

1. Prove that in the template, each reachable cell is scanned exactly once, for any interleaving of atomic steps.
2. Give a heap with $T_1 = n$ cells and span $T_\infty = \sqrt{n}$, and estimate the rounds for $P = \sqrt{n}$.
3. Change the template to steal half of the victim's deque. How does the list example change?
4. Write the parallel copying step with compare-and-swap on the forwarding word, and explain what the losing thread does with its copy.

## References
