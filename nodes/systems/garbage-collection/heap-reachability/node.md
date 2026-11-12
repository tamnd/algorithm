---
tag: M6KJ0E
kind: definition
slug: heap-reachability
name: Reachability in the heap
aliases:
- live object
- heap reachability
- reachable object
area: systems/garbage-collection
level: intro
summary: "An object is reachable, or live in the collector's sense, if a chain of pointers leads to it from a root. Unreachable objects stay unreachable."
prereqs: [gc-roots, graph-reachability]
see_also: [garbage, breadth-first-search, depth-first-search, multi-source-bfs, tracing-garbage-collection, tricolor-marking, weak-reference, ephemeron]
sources:
  - book: isbn:9781032218038
    title: "Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook: The Art of Automatic Memory Management, second edition, CRC Press, 2023"
    locator: Section 1.6 (liveness, correctness and reachability; the definition of the reachable set from the roots) and Chapter 2 (marking as a traversal of the reachable graph)
  - paper: doi:10.1145/367177.367199
    title: "John McCarthy, Recursive functions of symbolic expressions and their computation by machine, Part I, Communications of the ACM 3(4) (1960), 184-195"
    locator: the part on the free-storage list, where registers accessible to the program are traced and the cells that they do not reach are returned to free storage
  - paper: doi:10.1145/1028976.1028982
    title: "David F. Bacon, Perry Cheng and V. T. Rajan, A unified theory of garbage collection, OOPSLA 2004, 50-68"
    locator: the formulation of tracing as the least fixed point of the reference count equations
---

An object of the heap is *reachable* if a chain of [pointers](/pointer/) leads to it from a [root](/gc-roots/). A garbage collector calls a reachable object *live* and an unreachable one [garbage](/garbage/), because a program that cannot forge pointers can never touch an unreachable object again. The reachable set is the set of vertices that a [graph search](/graph-reachability/) from all the roots visits, and every [tracing collector](/tracing-garbage-collection/) computes it.

## Definition

Use the heap model of [mutator and collector](/mutator-and-collector/). The *heap graph* $G = (H, E)$ has a vertex for each object of the heap $H$ and an edge $x \to y$ for each field of $x$ that holds a reference to $y$. Let $\mathrm{Roots} \subseteq H$ be the objects that some root location refers to.

**Definition.** The *reachable set* is

$$\mathrm{Reach} = \{\, y \in H : \text{there is a path } x_0 \to x_1 \to \cdots \to x_k = y \text{ in } G \text{ with } x_0 \in \mathrm{Roots},\ k \ge 0 \,\}.$$

An object in $\mathrm{Reach}$ is *reachable*. In the language of collectors it is *live*; the next section explains why this word is an approximation.

**As a fixed point.** Let $\mathrm{succ}(S) = \{ y : x \to y \text{ for some } x \in S \}$ and $\Phi(S) = \mathrm{Roots} \cup \mathrm{succ}(S)$. The map $\Phi$ is monotone on the subsets of $H$, and $\mathrm{Reach}$ is its least fixed point: it is the smallest set that holds the roots and is closed under the edges. Iterating $\Phi$ from the empty set reaches it in at most $|H| + 1$ steps, because each step before the fixed point adds at least one object. Bacon, Cheng and Rajan (2004) use this view to show that tracing computes the least fixed point of a set of equations, and reference counting computes a larger one; see [automatic memory reclamation](/automatic-memory-reclamation/).

**Reachability is a safe test.** Call an object *semantically live* at a moment if the rest of the run accesses it. The mutator can only use references that it got from a root, from $\mathrm{New}$ or from a $\mathrm{Read}$ of an object that it already holds. So it can only access objects of $\mathrm{Reach}$, and every semantically live object is reachable. The converse is false: a reachable object may never be used again. The collector frees only unreachable objects, so it is safe, but it may keep some dead objects.

**Proposition (garbage stays garbage).** Assume that the mutator cannot forge pointers and that a new object has only null fields. If an object is unreachable at some moment, it is unreachable at every later moment.

*Proof.* Let $\mathrm{Reach}_t$ be the reachable set after $t$ operations. We show $\mathrm{Reach}_{t+1} \subseteq \mathrm{Reach}_t \cup N$, where $N$ holds the object made by operation $t + 1$ if it is a $\mathrm{New}$, and is empty otherwise. A $\mathrm{Read}$ changes no edge and puts into a root a reference to an object that was already reachable. A root assignment stores a reference that the mutator holds, so its target is in $\mathrm{Reach}_t$. A $\mathrm{New}$ adds a fresh object with no outgoing edges. A $\mathrm{Write}(x, i, v)$ removes one edge and adds the edge $x \to v$, where $v$ is null or in $\mathrm{Reach}_t$, because the mutator holds it. Now take any $y \in \mathrm{Reach}_{t+1}$ with $y \notin N$, and a path to $y$ from a root object at time $t + 1$. Cut the path after its last new edge, or keep the whole path if it has no new edge. The cut point is a root object of time $t + 1$ or the target of a new edge, and in both cases it is in $\mathrm{Reach}_t$. The rest of the path uses only edges that existed at time $t$. So $y \in \mathrm{Reach}_t$. By induction, an object outside $\mathrm{Reach}_t$ is outside each later reachable set. $\square$

This property is what lets a collector work on a snapshot. Once an object is found unreachable, no later action of the mutator can make it reachable, so the collector can free it at any later time. Two features break it on purpose: [finalization](/finalization/), which makes a dead object reachable again to run its finalizer, and a [weak reference](/weak-reference/) whose target the program reads before the collector clears it.

**Cost of the test.** A [breadth-first](/breadth-first-search/) or [depth-first search](/depth-first-search/) that starts from all root objects at once computes $\mathrm{Reach}$ in $O(|R| + |\mathrm{Reach}| + e)$ time, where $|R|$ is the number of root locations and $e$ is the number of fields of the reachable objects. The search never visits an unreachable object, so the cost of marking depends on the live data, not on the heap size.

## Examples and non-examples

**A small heap.** The roots refer to $A$ and $D$. The edges are $A \to B$, $B \to C$, $C \to A$, $D \to E$, $F \to G$, $G \to F$ and $F \to E$.

- A breadth-first search with the queue $[A, D]$ visits $A, D, B, E, C$. So $\mathrm{Reach} = \{A, B, C, D, E\}$ and the garbage is $\{F, G\}$.
- The iteration of $\Phi$ gives $\{A, D\}$, then $\{A, B, D, E\}$, then $\{A, B, C, D, E\}$, and then no change.
- The cycle $A \to B \to C \to A$ is live because a root refers to $A$. The cycle $F \leftrightarrow G$ is garbage, and its edge into the live object $E$ does not matter: an edge from a dead object keeps nothing alive, and it does not make $E$ dead either.

**Reachable but dead.** A program puts each request into a global list for a debug log that it never reads. Every request object stays reachable through the global variable, so no collector frees it, although no later operation uses it. This is the usual memory leak of a collected program.

**Non-example: a weak reference.** If the only path to an object passes through a [weak reference](/weak-reference/), the object is not reachable in the sense of this page. Weak edges are left out of $G$ when the collector computes $\mathrm{Reach}$.

**Non-example: an ephemeron value.** The value of an [ephemeron](/ephemeron/) is reachable through the ephemeron only if its key is reachable by some other path. This is a conditional edge, and the reachable set is then the least fixed point of a larger map.

## Related definitions

- **Graph reachability.** The general problem of which vertices a search from a source reaches: [graph reachability](/graph-reachability/) and [reachability](/reachability/). Heap reachability is the case with many sources (the roots), a graph that the mutator changes while a concurrent collector searches it, and edge kinds (strong, weak, ephemeron) that a plain graph does not have.
- **Tricolor abstraction.** A collector that searches in steps colors each object white (not yet seen), gray (seen, fields not yet scanned) or black (scanned): [tricolor marking](/tricolor-marking/).
- **Garbage.** The complement of the reachable set: [garbage](/garbage/).
- **Root set.** The starting points of the search: [GC roots](/gc-roots/).
- **Cycles.** The strongly connected parts of the heap graph, the [strongly connected components](/strongly-connected-components/), matter for reference counting, which cannot free a cycle: see [cycle collection](/cycle-collection/).

## References
