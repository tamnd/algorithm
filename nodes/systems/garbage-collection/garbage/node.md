---
tag: 9XJ1PN
kind: definition
slug: garbage
name: Garbage
aliases:
- dead object
- syntactic garbage
- semantic garbage
area: systems/garbage-collection
level: intro
summary: "Syntactic garbage is a heap object that no root reaches. Semantic garbage is an object that the program never uses again. Collectors free the first kind."
prereqs: [heap-reachability]
see_also: [automatic-memory-reclamation, gc-roots, cycle-collection, weak-reference, finalization, snapshot-at-the-beginning, use-after-free, rice-theorem]
sources:
  - book: isbn:9781032218038
    title: "Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook: The Art of Automatic Memory Management, second edition, CRC Press, 2023"
    locator: Chapter 1, Sections 1.1 and 1.2 (explicit deallocation, dangling pointers and leaks, automatic dynamic memory management) and Section 1.6 (liveness, correctness and reachability)
  - book: isbn:9780471941484
    title: "Richard Jones and Rafael Lins, Garbage Collection: Algorithms for Automatic Dynamic Memory Management, Wiley, 1996"
    locator: Chapter 1 (the definition of garbage and of liveness by reachability)
  - book: isbn:9781133187790
    title: "Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage, 2013"
    locator: Chapter 5 (undecidable problems and reducibility from the halting problem)
---

*Garbage* is heap memory that the program will not use again and that a collector may therefore reclaim. Two definitions are in use. An object is *syntactic garbage* if no chain of [pointers](/pointer/) from the [roots](/gc-roots/) reaches it, and *semantic garbage* if the rest of the run never accesses it. Every syntactic garbage object is semantic garbage, but not the reverse, and semantic garbage cannot be decided in general. So collectors free syntactic garbage, and the word "garbage" without a qualifier means that kind.

## Definition

Use the heap model of [mutator and collector](/mutator-and-collector/): a heap $H$, root locations, and a mutator that uses $\mathrm{New}$, $\mathrm{Read}$ and $\mathrm{Write}$ and cannot forge pointers. Let $\mathrm{Reach}_t$ be the set of objects that are [reachable](/heap-reachability/) from the roots after operation $t$.

**Syntactic garbage.** An object $x \in H$ is *syntactic garbage* at time $t$ if $x \notin \mathrm{Reach}_t$. A collector that frees only such objects is *safe*.

**Semantic garbage.** An object $x \in H$ is *semantically live* at time $t$ if some operation after $t$ reads or writes a field of $x$, and *semantic garbage* at time $t$ otherwise. This depends on the future of the run, so it is a property of the program and its input, not of the heap state.

**Proposition 1.** Each syntactic garbage object is semantic garbage.

*Proof.* The mutator accesses an object only through a reference that it holds, and it holds only references from the roots, from $\mathrm{New}$, or from a $\mathrm{Read}$ of an object that it holds. By the proposition on [reachability in the heap](/heap-reachability/), an unreachable object stays unreachable, so no later operation can obtain a reference to it. $\square$

**Proposition 2.** No algorithm decides, for every program $P$, input $w$ and point of the run, whether a given object is semantically live.

*Proof.* Assume a decider $D$ exists. Given a Turing machine $M$ and an input $u$, build the program $P$: "$x \leftarrow \mathrm{New}(1)$; store $x$ in a root; simulate $M$ on $u$; then $\mathrm{Read}(x, 0)$". The simulation uses only objects other than $x$. Right after the first line, $x$ is semantically live if and only if $M$ halts on $u$. So $D$ decides the [halting problem](/halting-problem/), which is undecidable. $\square$

The same argument, in the general form of [Rice's theorem](/rice-theorem/), shows that every exact notion of "the program still needs this object" is undecidable. Reachability is the standard safe approximation. In the other direction, a compiler can shrink the roots by leaving out dead variables, which moves reachability closer to semantic liveness.

**Garbage over time.** An object becomes garbage at the moment the last path to it is cut, by a $\mathrm{Write}$ or a root assignment. Some kinds of garbage have names:

- *Cyclic garbage* is a set of unreachable objects that refer to each other in a cycle. [Reference counting](/reference-counting/) cannot free it: see [cycle collection](/cycle-collection/).
- *Floating garbage* is an object that becomes garbage while a concurrent or incremental collection runs, and that this collection does not free. For example, a collector with a [snapshot at the beginning](/snapshot-at-the-beginning/) treats each object reachable at the start as live until the next cycle.

## Examples and non-examples

**A simple case.** The program runs `a = New(1); b = New(1); a.f = b; a = null; b = null`. After the last statement, no root refers to either object, so both are syntactic garbage. The edge $a \to b$ remains in the heap, but it starts at a dead object, so it does not keep $b$ alive.

**Semantic garbage that is reachable.** A server stores each request in a global map for a cache and never looks up the old ones. The old entries are reachable from a global variable, so they are not syntactic garbage, and no collector frees them. They are semantic garbage. This is a leak in a collected language, and the usual tool to avoid it is a [weak reference](/weak-reference/) or an [ephemeron](/ephemeron/) table, whose entries do not keep their keys alive.

**A dead local variable.** A function holds a large buffer in a local variable, uses it once, then runs for a long time. The buffer is semantic garbage after its last use. It is syntactic garbage only if the stack map at the safe point leaves the slot out; with a conservative or type-only scan of the stack, it stays reachable until the function returns.

**Non-example: an object that a weak reference refers to.** If the only path to an object passes through a weak reference, the object is syntactic garbage, because weak edges do not count. A program that reads the weak reference before the collector clears it gets a strong reference back, and then the object is live again. Weak references are the one place where a program can observe the moment an object becomes garbage.

**Non-example: a freed object that the program still uses.** In a program with explicit `free`, the opposite error exists: an object is freed while it is still semantically live, and a later access is a [use-after-free](/use-after-free/). A safe collector never makes this error, because it frees only syntactic garbage.

## Related definitions

- **Reachability.** Garbage is the complement of the reachable set: [reachability in the heap](/heap-reachability/).
- **Roots.** The locations from which reachability is measured: [GC roots](/gc-roots/).
- **The reclamation problem.** Finding and freeing garbage, with its costs and the two families of algorithms: [automatic memory reclamation](/automatic-memory-reclamation/).
- **Finalization.** Code that runs after an object is found to be garbage, and that can make it reachable again: [finalization](/finalization/).
- **Garbage in lock-free code.** In [safe memory reclamation](/safe-memory-reclamation/), a node that a thread has unlinked is often called garbage too. There, the program itself declares the node dead, and the scheme only waits until no other thread can still hold a pointer to it.

## References
