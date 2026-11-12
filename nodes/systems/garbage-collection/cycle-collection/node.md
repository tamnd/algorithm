---
tag: ED15S9
kind: problem
slug: cycle-collection
name: Cycle collection
aliases:
- cyclic garbage collection
- cyclic reference counting
area: systems/garbage-collection
level: core
summary: "Find and free the garbage that reference counting leaves: dead objects that a cycle of dead objects reaches, whose counts never drop to zero."
prereqs: [reference-counting, heap-reachability]
see_also: [trial-deletion, reference-counting, deferred-reference-counting, weak-reference, tracing-garbage-collection, mark-and-sweep, strongly-connected-components, automatic-memory-reclamation]
sources:
  - paper: doi:10.1007/3-540-45337-7_12
    title: "David F. Bacon and V. T. Rajan, Concurrent cycle collection in reference counted systems, ECOOP 2001, LNCS 2072, 207-235"
    locator: the synchronous cycle collector (candidate roots, the phases MarkRoots, ScanRoots and CollectRoots, linear time), and the comparison with the earlier quadratic method
  - paper: doi:10.1016/0020-0190(90)90226-N
    title: "A. D. Martinez, R. Wachenchauzer and R. D. Lins, Cyclic reference counting with local mark-scan, Information Processing Letters 34(1) (1990), 31-35"
    locator: the whole paper (a local mark-scan of the subgraph below a pointer whose count is decremented to a nonzero value)
  - paper: doi:10.1016/0020-0190(92)90088-D
    title: "Rafael D. Lins, Cyclic reference counting with lazy mark-scan, Information Processing Letters 44(4) (1992), 215-220"
    locator: the whole paper (candidates are buffered and the local mark-scan is delayed)
  - book: isbn:9781032218038
    title: "Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook: The Art of Automatic Memory Management, second edition, CRC Press, 2023"
    locator: Section 5.5 (cyclic reference counting, trial deletion and backup tracing)
  - url: https://github.com/python/cpython/blob/main/InternalDocs/garbage_collector.md
    title: CPython developer documentation, Garbage collector design
    locator: the sections on identifying reference cycles (a copy of each reference count, from which the references inside the examined set are subtracted)
---

Cycle collection is the problem of freeing the garbage that [reference counting](/reference-counting/) cannot free. If dead objects refer to each other in a cycle, each of them keeps a count of at least one, so none is ever freed, and neither is any object that they refer to. A cycle collector finds this garbage and frees it, without freeing any object that the program can reach. The two main solutions are a backup tracing collector and *trial deletion*, which subtracts the references inside a group of objects and keeps only those that something outside the group still refers to.

## In plain words

Reference counting frees an object when nothing refers to it. Two dead objects that refer to each other each still have one reference, so the counter never reaches zero. The same holds for a longer loop of objects, and for everything that the loop refers to.

A cycle collector looks for such groups. One way is to search the whole heap from the program's variables, as a tracing collector does, and to free what the search does not find. A cheaper way looks only at a small group of suspect objects. It asks, for each object in the group, how many of its references come from outside the group. If no reference from outside leads into a part of the group, that part is dead.

## Definition

**Input.** A heap in the model of [mutator and collector](/mutator-and-collector/), run by reference counting, so each object $x$ has an exact count $\mathrm{rc}(x)$ of the references to it from roots and heap fields. Let $\mathrm{Reach}$ be the [reachable](/heap-reachability/) set.

**Cyclic garbage.** By the theorem on the [reference counting](/reference-counting/) page, after each write the objects that reference counting keeps are $\mathrm{Reach} \cup C$, where $C$ is the set of unreachable objects that a cycle of unreachable objects reaches. The set $C$ is the *cyclic garbage*. It can hold acyclic parts too: a dead list that hangs from a dead cycle.

**Task.** Run from time to time, possibly in steps between the mutator's operations, and free objects such that:

- **Safety.** No object of $\mathrm{Reach}$ is freed, and the counts of the remaining objects stay exact.
- **Completeness.** Each object of $C$ is freed by some later run. A method is *partial* if it frees only the cyclic garbage that it examines.

**Candidates.** Many methods look only at *candidate roots*: objects whose count was decremented to a nonzero value. A cycle can become garbage only at such a decrement, because the last external reference into it is removed by a decrement that leaves the count of its target positive.

**The internal-count test.** Let $S$ be a set of objects that contains every object that its members refer to, and that does not contain the root record. For $x \in S$, let the *external count* be $\mathrm{ext}(x) = \mathrm{rc}(x) - |\{(y, j) : y \in S, \ y[j] = x\}|$, the number of references to $x$ from outside $S$. Call $x \in S$ *externally held* if a path inside $S$ leads to $x$ from an object with $\mathrm{ext} > 0$.

**Proposition.** (1) Each object of $S$ that is not externally held is garbage. (2) If $S$ contains every unreachable object of the heap, then the objects of $S$ that are not externally held are exactly the garbage in $S$.

*Proof.* (1) Let $x \in S$ be reachable, by a path from a root. Take the first object $y$ of the path that is in $S$. All later objects are in $S$, because $S$ is closed under the edges. The edge into $y$ comes from a root or from an object outside $S$, so $\mathrm{ext}(y) > 0$, and the rest of the path shows that $x$ is externally held. (2) Assume that $S$ contains all garbage. If $\mathrm{ext}(y) > 0$, then a root or an object outside $S$ refers to $y$. An object outside $S$ is reachable, so $y$ is reachable, and so is each object that a path from $y$ reaches. So every externally held object is reachable, and with (1), the rest are exactly the garbage of $S$. $\square$

Part (1) is the safety argument of trial deletion. Part (2) explains why a collector that applies the test to all objects is complete, and why one that applies it to a part of the heap is only partial: a reference from dead objects outside $S$ looks like an external reference.

## Variants

- **Backup tracing.** Run a [tracing collector](/tracing-garbage-collection/), such as [mark-and-sweep](/mark-and-sweep/), from time to time over the whole heap. It frees all garbage, cyclic or not, and can also repair counts that overflowed.
- **Local trial deletion from candidates.** Apply the internal-count test to the subgraph that the candidate roots reach. This is the method of [trial deletion](/trial-deletion/).
- **Internal-count test over all tracked objects.** Apply the test to every object that can be part of a cycle, or to one generation of them, with references from older generations treated as external.
- **Concurrent cycle collection.** Run the cycle collector while the mutator runs. The mutator can change the subgraph during the test, so the collector must check its result again before it frees anything.
- **Avoiding cycles.** Use [weak references](/weak-reference/) for back pointers, or types that cannot form cycles, so that no cyclic garbage arises.

## Examples

**A dead two-cycle.** In the example of the [reference counting](/reference-counting/) page, $B$ and $C$ refer to each other and the root $r_1$ is set to null. The decrement leaves $\mathrm{rc}(B) = 1$, so $B$ becomes a candidate. With $S = \{B, C\}$, both internal references are subtracted: $\mathrm{ext}(B) = 1 - 1 = 0$ and $\mathrm{ext}(C) = 1 - 1 = 0$. Nothing in $S$ is externally held, so both objects are freed.

**A live cycle.** Objects $a \to b \to c \to a$ form a cycle, and a root refers to $b$, so $\mathrm{rc}(a) = 1$, $\mathrm{rc}(b) = 2$ and $\mathrm{rc}(c) = 1$. If $a$ is a candidate, $S = \{a, b, c\}$ and the external counts are $0$, $1$ and $0$. The object $b$ is externally held, and so are $c$ and $a$ through the path $b \to c \to a$. Nothing is freed. If the root then drops $b$, all external counts are 0, and all three objects are freed.

**A partial test.** Let $S = \{x\}$ hold one object $x$ with no fields, and let a dead cycle outside $S$ refer to $x$. Then $\mathrm{ext}(x) = 1$, and the test keeps $x$, although it is garbage. A test that includes the cycle in $S$ frees all of it.

## Known algorithms

- **[Trial deletion](/trial-deletion/).** The synchronous algorithm of Bacon and Rajan (2001) buffers the candidate roots, then, for all of them together, subtracts the internal counts (MarkGray), restores the counts of externally held objects (Scan), and frees the rest (CollectWhite). It runs in time linear in the size of the subgraph that the candidates reach.
- **Local mark-scan.** Martinez, Wachenchauzer and Lins (1990) ran the same kind of test on the subgraph below each pointer whose count is decremented to a nonzero value, at once. Lins (1992) delayed the test and kept the candidates in a buffer. Since each candidate is handled on its own, the total work can be quadratic in the size of the subgraph.
- **Backup [mark-and-sweep](/mark-and-sweep/).** A full trace frees everything that reference counting missed, in time linear in the live heap plus a sweep.
- **CPython's cycle detector.** It copies the reference count of each tracked container object, subtracts the references from the other tracked objects of the generation that it examines, and keeps every object that a positive copy reaches. This is the internal-count test over a whole generation.

## Bounds

- **Trial deletion.** Bacon and Rajan's synchronous collector does $O(N + E)$ work for the subgraph of $N$ objects and $E$ references that the buffered candidates reach, with at most three passes over that subgraph.
- **Per-candidate local tests.** If the test runs separately for each candidate, objects that many candidates reach are examined many times. Bacon and Rajan give a heap of nested cycles on which this takes quadratic time.
- **Tracing.** A backup trace costs time linear in the live data, and a sweep adds time linear in the heap, however little cyclic garbage exists.
- **No free lunch for a local method.** The subgraph that a candidate reaches can be large and live, for example when the candidate refers to a big live structure. A local method then does much work and frees nothing, which is why practical systems mark objects that cannot be part of a cycle and skip them.

## Reductions

- **To reachability.** On a frozen heap, cyclic garbage is the set $C$ above, which a [graph reachability](/graph-reachability/) search from the roots finds, together with all other garbage.
- **To strongly connected components.** An object is on a cycle exactly when its [strongly connected component](/strongly-connected-components/) has more than one object or a self-loop. So $C$ is the set of garbage objects that a search from the nontrivial components of the garbage reaches. No practical collector uses this, because finding the garbage already needs a reachability search.
- **From automatic memory reclamation.** Reference counting plus a complete cycle collector solves the full problem of [automatic memory reclamation](/automatic-memory-reclamation/).

## Applications

CPython combines reference counting with a cycle detector that runs from time to time and uses the internal-count test. Other runtimes with reference counting add a trial deletion collector or a backup tracing collector. Systems with no cycle collector, such as Swift and the `Rc` and `shared_ptr` types of Rust and C++, ask the programmer to break cycles with weak references.

## References
