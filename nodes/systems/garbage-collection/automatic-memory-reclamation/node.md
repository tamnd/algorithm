---
tag: ZV73X1
kind: problem
slug: automatic-memory-reclamation
name: Automatic memory reclamation
aliases:
- garbage identification and reclamation
- automatic dynamic memory management
area: systems/garbage-collection
level: intro
summary: "Free the heap objects that the program can no longer reach, with no explicit free, while the program runs. Tracing and reference counting are the two families."
prereqs: [garbage, mutator-and-collector]
see_also: [tracing-garbage-collection, reference-counting, cycle-collection, gc-space-time-tradeoff, generational-garbage-collection, concurrent-garbage-collection, safe-memory-reclamation, robson-bound]
sources:
  - book: isbn:9781032218038
    title: "Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook: The Art of Automatic Memory Management, second edition, CRC Press, 2023"
    locator: Chapter 1 (Sections 1.2 and 1.3, automatic dynamic memory management and the criteria to compare collectors), Chapter 5 (reference counting) and Chapter 6 (comparing garbage collectors)
  - paper: doi:10.1145/1028976.1028982
    title: "David F. Bacon, Perry Cheng and V. T. Rajan, A unified theory of garbage collection, OOPSLA 2004, 50-68"
    locator: the reference count equations, tracing as the least fixed point and reference counting as the greatest fixed point, and hybrid collectors as combinations of the two
  - paper: doi:10.1145/367177.367199
    title: "John McCarthy, Recursive functions of symbolic expressions and their computation by machine, Part I, Communications of the ACM 3(4) (1960), 184-195"
    locator: the part on the free-storage list and the reclamation of cells that the program's registers do not reach (tracing)
  - paper: doi:10.1145/367487.367501
    title: "George E. Collins, A method for overlapping and erasure of lists, Communications of the ACM 3(12) (1960), 655-657"
    locator: the whole paper (a count of references in each list cell, and erasure when it drops to zero)
  - paper: doi:10.1007/BFb0017182
    title: Paul R. Wilson, Uniprocessor garbage collection techniques, International Workshop on Memory Management (IWMM 1992), LNCS 637, 1-42
    locator: Section 1 (the two-phase abstraction) and Section 2 (reference counting, mark-sweep, mark-compact and copying)
---

Automatic memory reclamation is the problem of freeing the heap objects that a running program can no longer use, without any explicit `free` in the program. A solution, called a *garbage collector*, must never free an object that the program can still reach, and it should free unreachable objects soon, with small cost in time, pauses and memory. Two families of algorithms solve it: *tracing*, which finds the live objects by a search from the [roots](/gc-roots/), and [reference counting](/reference-counting/), which finds dead objects by counting the references to each object. Bacon, Cheng and Rajan (2004) showed that the two are duals: they compute the least and the greatest fixed point of the same equations.

## In plain words

A program creates objects and links them with references. Over time, many objects lose every link from the running code. They are garbage, and their memory should be used again. The programmer does not say when an object dies; the system must find out.

There are two ways to find out. The first way starts from the variables of the program, follows every reference and marks what it reaches. Everything that it does not mark is garbage. The second way keeps a counter in each object: the number of references to it. When the counter drops to zero, the object is garbage at once.

The first way finds all garbage but must look at all live objects. The second way works in small steps but misses groups of dead objects that refer to each other in a loop.

## Definition

**The heap model.** A heap $H$ of objects with fields, a root set, and a [mutator](/mutator-and-collector/) that runs an online sequence of operations $\mathrm{New}(f)$, $\mathrm{Read}(x, i)$, $\mathrm{Write}(x, i, v)$ and root assignments, and that cannot forge pointers. Objects have sizes in words; the heap has a fixed capacity in words.

**The task.** The collector interleaves actions $\mathrm{free}(x)$ with the mutator's operations. Let $\mathrm{Reach}_t$ be the [reachable](/heap-reachability/) set at time $t$.

- **Safety (required).** If $\mathrm{free}(x)$ happens at time $t$, then $x \notin \mathrm{Reach}_t$.
- **Completeness (desired).** Each object that becomes [garbage](/garbage/) is freed at some later time. A collector is *incomplete* if some garbage is never freed.
- **Promptness.** The delay between the time an object becomes garbage and the time it is freed.

**The costs.** The quality of a solution is stated in these measures, with the heap size, the live size $L$ (the most words in $\mathrm{Reach}_t$ at any time) and the allocation volume as variables:

| measure | what it counts |
|---|---|
| throughput | total collector work, often per word allocated |
| pause time | the longest stretch in which the mutator cannot run |
| space overhead | heap size needed divided by $L$, including fragmentation and metadata |
| barrier cost | extra work in each $\mathrm{Read}$ or $\mathrm{Write}$ |
| completeness | which garbage is never freed |

Safety is a hard rule, so the other measures trade against each other. No single collector is best in all of them.

## Variants

- **Complete or incomplete.** Tracing collectors are complete. Plain reference counting is incomplete, because it never frees cyclic garbage; the subproblem of freeing it is [cycle collection](/cycle-collection/). A [conservative collector](/conservative-garbage-collection/) is complete only up to false retention from ambiguous roots.
- **Moving or non-moving.** A moving collector ([copying](/copying-collection/), [mark-compact](/mark-compact/)) can remove fragmentation but must update every reference to a moved object. A non-moving collector ([mark-and-sweep](/mark-and-sweep/), reference counting) must live with the fragmentation of its allocator.
- **Whole heap or partial.** A [generational collector](/generational-garbage-collection/) collects a young part of the heap often and the rest rarely.
- **How the work is placed.** [Stop-the-world](/stop-the-world-collection/), [incremental](/incremental-garbage-collection/), [concurrent](/concurrent-garbage-collection/) and [parallel](/parallel-garbage-collection/) collection differ in when the collector runs relative to the mutator.
- **Distributed heaps.** References cross machines, and the count updates are messages. [Weighted reference counting](/weighted-reference-counting/) removes the message on a copy.
- **Weak and conditional references.** With [weak references](/weak-reference/), [ephemerons](/ephemeron/) and [finalization](/finalization/), the program can observe when an object becomes garbage, and the collector must clear or notify in a defined order.

## Examples

A heap with roots $r_0$ and $r_1$ runs eight operations. Objects $A$, $B$, $C$ are made by $\mathrm{New}$:

1. $r_0 \leftarrow A$.
2. $A[0] \leftarrow B$.
3. $B[0] \leftarrow C$.
4. $A[1] \leftarrow C$.
5. $r_1 \leftarrow B$.
6. $r_0 \leftarrow \text{null}$. Now $A$ is garbage; $B$ and $C$ are reachable through $r_1$.
7. $C[0] \leftarrow B$. Now $B$ and $C$ form a cycle.
8. $r_1 \leftarrow \text{null}$. Now $B$ and $C$ are garbage.

The answers of the two families differ:

| collector | after step 6 | after step 8 |
|---|---|---|
| reference counting | frees $A$ at once; counts $B = 1$, $C = 1$ | counts $B = 1$, $C = 1$; frees nothing |
| a tracing collection | would free $A$ | would free $B$ and $C$ (and $A$, if still there) |

Reference counting frees $A$ in step 6 with no search, but it never frees the cycle $B \leftrightarrow C$. A tracing collection frees everything that is garbage at the time it runs, but only at that time, and at the price of a search of the live objects.

## Known algorithms

- **Tracing.** [Tracing garbage collection](/tracing-garbage-collection/) and its main forms: [mark-and-sweep](/mark-and-sweep/) (McCarthy 1960), [mark-compact](/mark-compact/) and [copying collection](/copying-collection/), with [Cheney's algorithm](/cheney-copying-collector/) as the standard breadth-first copier. Cost per collection: $\Theta(L)$ for the mark or copy, plus $\Theta(\text{heap size})$ for a sweep.
- **Reference counting.** [Reference counting](/reference-counting/) (Collins 1960): $O(1)$ work per pointer write, plus $O(1 + f)$ for each freed object with $f$ fields. Its variants cut the count traffic: [deferred reference counting](/deferred-reference-counting/) ignores the roots, and [weighted reference counting](/weighted-reference-counting/) removes the increment messages in a distributed heap.
- **Cycle collection for reference counting.** [Trial deletion](/trial-deletion/), as in the synchronous collector of Bacon and Rajan (2001), or a backup tracing collector: see [cycle collection](/cycle-collection/).
- **Hybrids.** [Generational collection](/generational-garbage-collection/) traces the young objects and can count or trace the old ones. Bacon, Cheng and Rajan describe such collectors as a choice, for each part of the heap, between the two fixed points below.

## Bounds

**The fixed point theorem.** Let $T \subseteq H$ be the objects that the roots refer to, $\mathrm{succ}(S)$ the objects that a field of an object of $S$ refers to, and $\Phi(S) = T \cup \mathrm{succ}(S)$, a monotone map on the subsets of $H$. Call an object *cycle-reachable* if a path leads to it from an object that lies on a cycle of the heap graph, and let $C$ be the set of these objects.

**Theorem.** (1) The least fixed point of $\Phi$ is $\mathrm{Reach}$. (2) The greatest fixed point of $\Phi$ is $\mathrm{Reach} \cup C$.

*Proof.* (1) is the definition of [reachability](/heap-reachability/) as the least closed set. For (2), let $\nu$ be the greatest fixed point; it exists by the [Knaster-Tarski theorem](/knaster-tarski-theorem/). Since $\nu = \Phi(\nu)$, each $x \in \nu$ is in $T$ or has a predecessor in $\nu$. Walk back from $x$ through predecessors in $\nu$. The heap is finite, so the walk reaches $T$, and then $x \in \mathrm{Reach}$, or it repeats an object, and then $x$ is reached from a cycle, so $x \in C$. Hence $\nu \subseteq \mathrm{Reach} \cup C$. Conversely, let $S = \mathrm{Reach} \cup C$. An object of $\mathrm{Reach} \setminus T$ has its predecessor on a path from $T$ in $\mathrm{Reach}$. An object of $C$ has its predecessor on the cycle or on the path from the cycle in $C$. So $S \subseteq \Phi(S)$. By Knaster-Tarski, $\nu$ is the union of all such sets, so $S \subseteq \nu$. $\square$

Tracing computes the least fixed point: it starts from nothing and adds what the roots reach. Reference counting keeps the greatest one: a count is positive as long as some object, dead or alive, refers to it, so an object stays while it has a predecessor in the kept set. The proof on the [reference counting](/reference-counting/) page shows that after each write the set of objects that it keeps is exactly the greatest fixed point of the current heap. The difference of the two fixed points is the garbage that a cycle of garbage reaches, which is exactly what plain reference counting leaks.

**Time.** A tracing collection costs $\Omega(L)$ work, because it must visit each live object to know that it is live; a mark-sweep collection adds a sweep linear in the heap size. Reference counting costs $\Theta(1)$ per counted pointer write, which no tracing collector pays, plus work proportional to the objects that it frees. For a copying collector with two semispaces of $S$ words each, one collection costs $c L$ and frees $S - L$ words, so the work per allocated word is $c L / (S - L)$: it falls as the heap grows. The page [GC space-time tradeoff](/gc-space-time-tradeoff/) treats this curve.

**Pauses.** A stop-the-world tracing collection pauses for $\Theta(L)$ time, and one write in plain reference counting can free a whole structure, which is a pause linear in its size. Incremental and real-time collectors, starting with [Baker's collector](/baker-real-time-collector/), bound the work per mutator operation.

**Space.** A non-moving collector frees objects in place, so its heap suffers the worst-case fragmentation of a non-moving allocator. The [Robson bound](/robson-bound/) shows that this can force a heap of order $L \log n$ words, where $n$ is the ratio of the largest to the smallest object size. A copying collector avoids fragmentation but needs room for a second copy of the live data.

## Reductions

- **To graph reachability.** On a frozen heap, finding the garbage is the complement of a multi-source [graph reachability](/graph-reachability/) query from the root objects, which a [breadth-first search](/breadth-first-search/) answers in linear time. The hard parts of the real problem are that the graph changes while the collector runs, and the cost measures above.
- **Cycle collection as a subproblem.** A reference counting collector solves the whole problem only together with a solution of [cycle collection](/cycle-collection/).
- **Not the same as safe memory reclamation.** In lock-free code, [safe memory reclamation](/safe-memory-reclamation/) (with [hazard pointers](/hazard-pointers/), [epoch-based reclamation](/epoch-based-reclamation/) or [lock-free reference counting](/lock-free-reference-counting/)) also frees memory without a race. There, the program declares which node it removed, and the scheme only decides when the free is safe for other threads. No heap is traced, and the program is not relieved of finding dead nodes.

## Applications

Every runtime of a memory-safe language solves this problem. Lisp systems used tracing from McCarthy's first implementation. The virtual machines of Java and .NET, and the runtimes of Go and of JavaScript engines, use tracing collectors, many of them generational and concurrent. CPython uses reference counting with a cycle detector as a backup. Swift and Objective-C use reference counting that the compiler inserts, and C++ and Rust offer library reference counting (`shared_ptr`, `Rc`, `Arc`) for the objects that the programmer chooses.

## References
