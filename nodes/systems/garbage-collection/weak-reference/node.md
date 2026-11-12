---
tag: HJH8A4
kind: definition
slug: weak-reference
name: Weak reference
aliases:
- weak pointer
- weakref
area: systems/garbage-collection
level: intro
summary: "A reference that does not keep its target alive. When no chain of ordinary references reaches the target, the collector may free it and clears the weak reference."
prereqs: [heap-reachability, garbage]
see_also: [ephemeron, finalization, reference-counting, cycle-collection, heap-reachability, garbage, tracing-garbage-collection, gc-roots]
sources:
  - book: isbn:9781032218038
    title: "Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook: The Art of Automatic Memory Management, second edition, CRC Press, 2023"
    locator: Section 12.2 (weak references, their uses, the strengths of references and their support in tracing and reference counting collectors)
  - url: https://docs.oracle.com/javase/8/docs/api/java/lang/ref/package-summary.html
    title: Java Platform SE 8 API, package java.lang.ref
    locator: the package description, section on reachability (strongly, softly, weakly and phantom reachable objects) and the notification by reference queues
  - url: https://docs.python.org/3/library/weakref.html
    title: Python documentation, weakref module
    locator: the introduction (weak references, callbacks, WeakKeyDictionary and WeakValueDictionary)
---

A *weak reference* is a reference that the garbage collector ignores when it decides which objects are live. If the only paths to an object pass through weak references, the object is [garbage](/garbage/): the collector may free it, and then it *clears* every weak reference to it, so that a later read returns null. Ordinary references, which keep their targets alive, are then called *strong*. Weak references let a program refer to an object, for a cache, a table of canonical objects or a back pointer, without being the reason that the object stays in memory.

## Definition

Use the heap model of [mutator and collector](/mutator-and-collector/), with two kinds of fields: *strong* and *weak*. The heap graph has a strong edge $x \to y$ for each strong field of $x$ that refers to $y$, and a weak edge for each weak field.

**Strong reachability.** An object is *strongly reachable* if a path of strong edges leads to it from a [root](/gc-roots/). [Reachability in the heap](/heap-reachability/) for a collector with weak references means strong reachability: weak edges are left out of the search.

**Weak reachability.** An object is *weakly reachable* if it is not strongly reachable, but a path that uses at least one weak edge leads to it from a root.

**Semantics.** A weak field holds a target or null. The mutator can:

- create a weak reference to an object that it holds;
- *get* the target: the result is the object, now held by a strong reference of the mutator, or null if the reference was cleared.

The collector guarantees:

- **No retention.** A weak edge never makes its target live.
- **Clearing.** When the collector finds that an object $x$ is not strongly reachable, it clears all weak references to $x$ at once, before or when it frees $x$. A get that comes after the clearing returns null.
- **Atomic view.** A get that returns $x$ makes $x$ strongly reachable again. So the collector must clear weak references in a step that no get can split: either the mutator sees $x$ and $x$ stays, or it sees null.

The collector is not required to clear at the first moment that $x$ becomes weakly reachable. It clears when a collection finds this, which can be much later.

**Strengths.** Some languages offer more than one kind of non-strong reference. In Java, a *soft* reference is like a weak one, but the collector clears it only when it needs memory, which suits caches. A *phantom* reference never returns its target. It only tells the program, through a queue, that the object has been collected, and it is used to release outside resources after an object dies. The collector checks the strengths in order: strong, then soft, then weak, then [finalization](/finalization/), then phantom.

**With reference counting.** A weak reference does not add to the count. When the count drops to zero, the object is freed even if weak references exist, so the runtime must find and clear them, for example with a list of the weak references of each object, or with a side record that outlives the object and that each weak reference checks.

## Examples and non-examples

**A small heap.** The root refers to $A$. The object $A$ has a strong field to $B$ and a weak field to $C$, and $B$ has a weak field back to $A$. No other reference to $C$ exists.

- $A$ and $B$ are strongly reachable. $C$ is only weakly reachable, so the next collection frees $C$ and clears the weak field of $A$.
- If the root is set to null, $A$ and $B$ become garbage. With [reference counting](/reference-counting/), the count of $A$ drops from 1 to 0, because the back pointer of $B$ is weak, so $A$ is freed, and then $B$. If the back pointer were strong, $A$ and $B$ would form a cycle that reference counting never frees.

**A cache.** A program maps file names to their parsed contents, through weak references to the contents. While some part of the program uses a parsed file, the cache returns it. When no part uses it any more, the collector frees it and the cache entry reads as null, so the cache does not keep all files in memory.

**A canonicalizing table.** A table maps each value to the one object that represents it, with the objects held weakly, as in a table of interned strings. Objects that the program no longer uses leave the table.

**Non-example: a strong value in a weak-keyed table.** A table with weak keys and strong values keeps each value alive as long as the table lives. If a value refers to its own key, the key stays strongly reachable through the table, and the entry is never removed. This is the problem that [ephemerons](/ephemeron/) solve.

**Non-example: a reference that the program forgets to read.** A weak reference does not tell the program when to stop using an object. A program that reads the target, stores it in a strong field, and keeps it there makes the object live again, and the weak reference has no effect.

## Related definitions

- **Ephemeron.** A key and a value where the value is reachable through the pair only if the key is reachable from elsewhere: [ephemeron](/ephemeron/).
- **Finalization.** Code that runs after an object is found not to be strongly reachable, and that can make it reachable again: [finalization](/finalization/).
- **Reachability and garbage.** Weak references change the edges that the collector follows: [reachability in the heap](/heap-reachability/) and [garbage](/garbage/).
- **Breaking cycles.** In a reference counting system, weak back pointers are the usual way to avoid the cycles that [cycle collection](/cycle-collection/) must otherwise find.
- **Weak pointers in lock-free code.** A counted pointer that can be upgraded to a strong one only while the count is positive, as in `weak_ptr` of C++, follows the same idea in manual memory management; see [lock-free reference counting](/lock-free-reference-counting/).

## References
