---
tag: 4N1MDY
kind: definition
slug: mutator-and-collector
name: Mutator and collector
area: systems/garbage-collection
level: intro
summary: "The mutator runs the program and changes the heap through New, Read and Write. The collector finds objects that the mutator cannot reach and reclaims them."
prereqs: [pointer]
see_also: [gc-roots, heap-reachability, garbage, write-barrier, read-barrier, stop-the-world-collection, concurrent-garbage-collection, automatic-memory-reclamation]
sources:
  - paper: doi:10.1145/359642.359655
    title: "Edsger W. Dijkstra, Leslie Lamport, A. J. Martin, C. S. Scholten and E. F. M. Steffens, On-the-fly garbage collection: an exercise in cooperation, Communications of the ACM 21(11) (1978), 966-975"
    locator: the introduction, which splits the system into the mutator and the collector, and the operations of the mutator on the graph of nodes
  - book: isbn:9781032218038
    title: "Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook: The Art of Automatic Memory Management, second edition, CRC Press, 2023"
    locator: Chapter 1, Section 1.6 (terminology and notation, the mutator and the collector, the allocator, mutator read and write operations New, Read and Write)
  - paper: doi:10.1007/BFb0017182
    title: Paul R. Wilson, Uniprocessor garbage collection techniques, International Workshop on Memory Management (IWMM 1992), LNCS 637, 1-42
    locator: Section 1, the two-phase abstraction (garbage detection and garbage reclamation) and the use of the term mutator
---

The *mutator* and the *collector* are the two parts of a program that runs with automatic memory management. The mutator executes the program: it allocates objects and reads and writes their [pointer](/pointer/) fields, and so it changes the graph of the heap. The collector finds the objects that the mutator can no longer reach and gives their memory back to the allocator. The names come from Dijkstra, Lamport, Martin, Scholten and Steffens (1978), who treated the two parts as cooperating processes.

## Definition

**The heap model.** The heap $H$ is a finite set of objects. Each object $x$ has a fixed number of fields $x[0], \ldots, x[f_x - 1]$. A field holds a reference to an object of $H$, the value null, or a value that is not a pointer. The *roots* are a finite set $R$ of locations outside the heap (registers, stack slots, global variables) that also hold references; see [root set](/gc-roots/). The heap is a directed graph with an edge $x \to y$ for each field of $x$ that refers to $y$.

**The mutator** is the code of the program. Under the abstraction of the Jones, Hosking and Moss handbook, it changes the heap only through three operations:

- $\mathrm{New}(f)$ returns a fresh object with $f$ fields, all null, and adds it to $H$. The allocator serves this request.
- $\mathrm{Read}(x, i)$ returns the value of $x[i]$.
- $\mathrm{Write}(x, i, v)$ sets $x[i] \leftarrow v$.

It also reads and writes its roots. A mutator in this model cannot forge a pointer: each reference that it holds came from $\mathrm{New}$, from a root, or from a $\mathrm{Read}$ of an object that it already reached. Programs in Java, C#, Lisp or Python meet this rule. C with pointer arithmetic does not.

**The collector** is the code that removes objects from $H$. Its one hard rule is *safety*: it may free $x$ only if no sequence of mutator operations from the present state can access $x$. Because the mutator cannot forge pointers, an object that no path from a root reaches is safe to free (see [reachability in the heap](/heap-reachability/)). A collector is *complete* if each such object is freed in the end. Plain [reference counting](/reference-counting/) is safe but not complete, because it never frees a cycle.

**Barriers.** A collector may attach code to $\mathrm{Read}$ or $\mathrm{Write}$. This code is a [read barrier](/read-barrier/) or a [write barrier](/write-barrier/). It is collector work that runs on the mutator's thread, inside the mutator's operations.

**What is measured.** The two parts share the processor and the memory, so the costs of a collector are stated as costs to the mutator:

| measure | what it counts |
|---|---|
| throughput | the fraction of the total run time that the mutator runs |
| pause time | the longest time that the mutator is stopped by one action of the collector |
| mutator utilization | the fraction of a time window of a given length in which the mutator runs; the minimum over all windows is the minimum mutator utilization |
| space overhead | the heap size that the collector needs, divided by the largest amount of live data |
| barrier cost | the extra instructions in each $\mathrm{Read}$ or $\mathrm{Write}$ |

## Examples and non-examples

**A stop-the-world collector.** The mutator runs until $\mathrm{New}$ fails. Then all mutator threads stop, the collector runs to the end, and the mutator resumes. The two parts never run at the same time. This is [stop-the-world collection](/stop-the-world-collection/). The pause is the full time of one collection.

**Reference counting.** The collector work runs inside the mutator's own writes. Each $\mathrm{Write}(x, i, v)$ adds 1 to the count of $v$ and subtracts 1 from the count of the old value of $x[i]$, and frees an object whose count drops to zero. The write barrier is the whole collector.

**A short trace.** Let the roots be $r_0$ and $r_1$. The mutator runs:

1. $a \leftarrow \mathrm{New}(1)$, $r_0 \leftarrow a$.
2. $b \leftarrow \mathrm{New}(1)$, $\mathrm{Write}(a, 0, b)$.
3. $r_1 \leftarrow b$.
4. $r_0 \leftarrow \text{null}$.

After step 4, no root and no reachable object refers to $a$, so $a$ is [garbage](/garbage/), and a collector may free it. The object $b$ is still reachable through $r_1$, although the edge $a \to b$ still exists. The edge from a dead object does not keep its target alive.

**Concurrent collection.** In a [concurrent collector](/concurrent-garbage-collection/), the collector runs on its own thread while the mutator threads run. The mutator can move a reference while the collector traces, so the two must cooperate through barriers. The paper of Dijkstra and others is a classic study of this case: it gives a collector that runs in parallel with the mutator and a proof that the two do not interfere.

**Non-example: explicit deallocation.** A C program that calls `free` has no collector. The program itself decides when an object is dead, and an error gives a [use-after-free](/use-after-free/) or a leak.

**Non-example: safe memory reclamation in lock-free code.** In [hazard pointers](/hazard-pointers/) or [epoch-based reclamation](/epoch-based-reclamation/), the program tells the scheme which node it has unlinked, and the scheme only decides when the free is safe for other threads. No part of the system traces a heap or counts the references of the program, so there is no collector in this sense. The page [safe memory reclamation](/safe-memory-reclamation/) treats that problem.

## Related definitions

- **Allocator.** The part that serves $\mathrm{New}$. The collector returns freed memory to it. The pages in memory allocation, such as [bump-pointer allocation](/bump-pointer-allocation/), describe allocators.
- **Root set.** The locations that the mutator can access without a $\mathrm{Read}$: [GC roots](/gc-roots/).
- **Reachability and garbage.** The collector's safe test for liveness: [reachability in the heap](/heap-reachability/) and [garbage](/garbage/).
- **Barriers.** [Write barrier](/write-barrier/) and [read barrier](/read-barrier/): the code that the collector adds to the mutator's operations.
- **Modes of cooperation.** [Stop-the-world](/stop-the-world-collection/), [incremental](/incremental-garbage-collection/), [concurrent](/concurrent-garbage-collection/) and [on-the-fly](/on-the-fly-garbage-collection/) collection differ in how the work of the collector is placed among the mutator's operations.

## References
