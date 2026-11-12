---
tag: CGRV4H
kind: technique
slug: tracing-garbage-collection
name: Tracing garbage collection
aliases:
- tracing collector
- tracing GC
area: systems/garbage-collection
level: intro
summary: "Find the live objects by following pointers from the roots, as a graph search does, and reclaim every object that the search does not reach. Mark-sweep, mark-compact and copying all do this."
prereqs: [gc-roots, heap-reachability]
see_also: [mark-and-sweep, copying-collection, mark-compact, reference-counting, tricolor-marking, stop-the-world-collection, generational-garbage-collection, conservative-garbage-collection]
sources:
  - paper: doi:10.1145/367177.367199
    title: John McCarthy, Recursive functions of symbolic expressions and their computation by machine, Part I, Communications of the ACM 3(4), 184-195, 1960
    locator: Section 4, the free-storage list and the reclamation of registers that cannot be reached from the base registers
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 1 (the mutator, the collector, roots and reachability) and Chapters 2 to 4 (mark-sweep, mark-compact and copying)
  - paper: Paul R. Wilson, Uniprocessor garbage collection techniques, International Workshop on Memory Management (IWMM 1992), LNCS 637, Springer, 1992
    locator: the sections on the two-phase abstraction (liveness detection and reclamation) and on tracing collectors
  - book: isbn:9780471941484
    title: Richard Jones and Rafael Lins, Garbage Collection, Algorithms for Automatic Dynamic Memory Management, Wiley, 1996
    locator: Chapter 2, the classical algorithms
---

Tracing garbage collection finds the objects that a program can still use by following pointers. It starts at the *roots*, the references that the program holds in its registers, stack and global variables, and visits every object it can reach, as a [depth-first](/depth-first-search/) or [breadth-first search](/breadth-first-search/) of a graph does. Every object that the search does not reach is [garbage](/garbage/), because no sequence of pointer loads can ever lead to it, and its memory is reclaimed. McCarthy introduced the idea for LISP in 1960. [Mark-and-sweep](/mark-and-sweep/), [mark-compact](/mark-compact/) and [copying](/copying-collection/) collectors are the three classic ways to reclaim what the search leaves behind. The other great family, [reference counting](/reference-counting/), finds garbage locally instead.

## In plain words

Think of a set of balloons tied together with strings, some of them tied to your hand. Pull your hand and see which balloons come with it: those are the ones you can still reach. All the other balloons, even if they are tied to each other, are lost to you, and can be taken away.

A tracing collector does exactly this with the objects of a program. It starts from the references that the program holds, follows every pointer, and marks what it finds. What is not found is junk. Then it takes the junk back, either by listing the free places, by packing the found objects together, or by copying them to a fresh area.

## When it applies

- **The heap is a graph that the collector can read.** The runtime can tell which words of an object are pointers, or it can guess safely, as a [conservative collector](/conservative-garbage-collection/) does.
- **The roots are known.** The collector can find every reference the program holds outside the heap: in registers, on the stacks of all threads, and in globals ([GC roots](/gc-roots/)).
- **Reachability is a good stand-in for liveness.** An object that is not reachable is surely dead. An object that is reachable may still be dead, if the program will never use it again, but a collector cannot know the future, so it keeps it.
- **Garbage can contain cycles.** Tracing reclaims a cycle of garbage objects as easily as any other garbage, which reference counting cannot do alone.
- **Pauses or barriers are acceptable.** The collector either stops the program ([stop the world](/stop-the-world-collection/)) or uses barriers to run beside it.

## The template

```pseudo id=main
TRACE-AND-RECLAIM(roots, heap)
L1  W ← empty worklist; clear all marks                ▷ hole: mark bits, bitmap, or a second space
L2  for each root r do SHADE(r)
L3  while W is not empty do
L4      x ← take an object from W                       ▷ hole: stack (depth-first) or queue (breadth-first)
L5      for each pointer field f of x do SHADE(f)
L6  RECLAIM every object that is not marked            ▷ hole: sweep, compact, or drop the old space

SHADE(p)
L7  if p ≠ nil and p is not marked then
L8      mark p and put p in W                           ▷ a copying collector copies p here
```

Lines L1 to L5 are a graph search from the roots: the marked objects are the visited vertices, and the worklist is the frontier. In the terms of [tricolor marking](/tricolor-marking/), unmarked objects are white, objects in $W$ are gray, and marked objects not in $W$ are black. When $W$ is empty, the marked objects are exactly the objects reachable from the roots. Line L6 is where the families differ. The search costs $O(r + L)$ for $r$ roots and $L$ live words; the cost of reclaiming depends on the family.

## Classic examples

- **[Mark-and-sweep](/mark-and-sweep/).** Mark with a stack, then sweep the whole heap and put each unmarked object on a [free list](/free-list/). Objects never move.
- **[Mark-compact](/mark-compact/).** Mark, then move the live objects together and rewrite the pointers ([two-finger](/two-finger-compaction/), [Lisp 2](/lisp2-compaction/)). The free space becomes one block.
- **[Copying collection](/copying-collection/).** The search and the reclaim are one step: SHADE copies each object to an empty space, and the old space is dropped whole. [Cheney's algorithm](/cheney-copying-collector/) uses the copies themselves as the queue.
- **[Schorr-Waite marking](/schorr-waite-marking/).** The worklist is stored in the objects themselves, by reversing pointers, so marking needs no extra memory.
- **[Generational collection](/generational-garbage-collection/).** Trace only the young objects often, with the pointers from old to young objects as extra roots.

## Variations

- **The worklist.** A stack gives depth-first order, a queue gives breadth-first order; pointer reversal keeps the stack inside the heap.
- **Where the marks live.** In a header bit, in a side bitmap, or as the forwarding address of a copy.
- **How to reclaim.** Sweep to free lists, sweep lazily on allocation ([lazy sweeping](/lazy-sweeping/)), compact in place, or copy to another space.
- **When it runs.** All at once with the program stopped, in small steps ([incremental](/incremental-garbage-collection/)), or beside the program ([concurrent](/concurrent-garbage-collection/)). The last two need barriers that keep the tricolor invariants.
- **How much of the heap.** The whole heap, one generation, or a set of regions, with the pointers into the set from outside as extra roots.
- **Precise or conservative.** A precise collector knows every pointer; a conservative one treats any word that looks like a pointer as one.

## Pitfalls

- **A missed root.** If one reference that the program holds is not scanned, the object it refers to may be reclaimed while it is still in use. Every register, stack slot and global must be found, for every thread.
- **Recursion in the marker.** A recursive mark can overflow the stack on a long list. Use an explicit worklist, a queue in to-space, or pointer reversal.
- **The program changes the heap during the trace.** If the collector runs while the program writes pointers, it can miss a live object; see the lost object problem in [tricolor marking](/tricolor-marking/).
- **Reachable but dead.** An object that is still referenced, for example from a cache or a list that is never emptied, is never reclaimed. This is a memory leak that a tracing collector cannot fix.
- **Finalizers and weak references.** Objects with [finalizers](/finalization/) or behind [weak references](/weak-reference/) need extra passes, and a finalizer can make an object reachable again.

## Exercises

1. Show that, when the worklist is empty, every object reachable from the roots is marked, whatever order the worklist uses.
2. Give a heap with a garbage cycle of three objects. Show that tracing reclaims it, and that plain reference counting does not.
3. The trace costs $O(r + L)$. Explain why the sweep of mark-and-sweep costs time in proportion to the whole heap, and why a copying collector does not.
4. Write the template with a queue, and show that it visits the objects in breadth-first order. Then write it with no worklist at all, using the copies in a second space as the queue.
5. Give an example of an object that is reachable but will never be used again. Can any collector reclaim it safely?

## References
