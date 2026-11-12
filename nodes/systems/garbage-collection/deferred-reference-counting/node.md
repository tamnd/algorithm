---
tag: 0A4SH2
kind: algorithm
slug: deferred-reference-counting
name: Deferred reference counting
aliases:
- deferred RC
- Deutsch-Bobrow reference counting
area: systems/garbage-collection
level: core
summary: "Reference counting that does not count references from roots. Objects whose count drops to zero wait in a zero count table, and a scan of the roots decides which to free."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {r: the number of roots, z: the number of entries in the zero count table, k: the number of fields of the objects that a collection frees}
  time: {worst: O(r + z + k), amortized: O(1)}
  space: {extra: O(z)}
properties: {online: true, deterministic: true, recursive: false, complete: false, moving: false}
history:
  year: 1976
  people: [L. Peter Deutsch, Daniel G. Bobrow]
  note: "Deutsch and Bobrow described an incremental reference counting collector for Lisp that does not count references from local variables, with a table of the objects whose count is zero."
prereqs: [reference-counting, gc-roots]
see_also: [reference-counting, weighted-reference-counting, cycle-collection, trial-deletion, write-barrier, stop-the-world-collection, tracing-garbage-collection, automatic-memory-reclamation]
sources:
  - paper: doi:10.1145/360336.360345
    title: "L. Peter Deutsch and Daniel G. Bobrow, An efficient, incremental, automatic garbage collector, Communications of the ACM 19(9) (1976), 522-526"
    locator: the whole paper (references from variables are not counted, and objects with a zero count are kept in a table until the variables are scanned)
  - book: isbn:9781032218038
    title: "Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook: The Art of Automatic Memory Management, second edition, CRC Press, 2023"
    locator: Section 5.3 (deferred reference counting and the zero count table)
  - book: isbn:9780471941484
    title: "Richard Jones and Rafael Lins, Garbage Collection: Algorithms for Automatic Dynamic Memory Management, Wiley, 1996"
    locator: Chapter 3 (deferred reference counting)
---

Deferred reference counting is a form of [reference counting](/reference-counting/) that counts only the references from heap objects and ignores the references from the [roots](/gc-roots/): registers, stack slots and, in many systems, global variables. Most pointer writes in a program change local variables, so most count updates disappear. The price is that a count of zero no longer proves that an object is dead, because a root may still refer to it. Such an object goes into a *zero count table* (ZCT), and from time to time the collector scans the roots and frees the entries of the table that no root refers to. Deutsch and Bobrow (1976) introduced the method for Lisp.

## In plain words

Plain reference counting updates a counter each time the program copies or drops a reference. Most of these changes happen in local variables, which come and go very fast.

Deferred counting stops counting the local variables. It counts only the references that are stored inside objects. When an object's counter drops to zero, it is not freed at once, because a local variable may still hold it. It goes on a waiting list instead.

From time to time, the program stops for a short time. The collector looks at all local variables and marks the objects that they hold as safe. Every object on the waiting list that is not safe and still has a counter of zero is freed.

## The problem

Solve [automatic memory reclamation](/automatic-memory-reclamation/) in the heap model of [mutator and collector](/mutator-and-collector/), with the roots $r_1, \ldots, r_m$ kept apart from the heap. Writes to roots must cost nothing extra, and writes to heap fields may cost $O(1)$.

## The algorithm

Each object $x$ has a count $\mathrm{rc}(x)$ of the heap fields that refer to it. The set ZCT holds every object whose count is zero, and possibly some others.

```pseudo id=main
NEW(n)
L1  x ← allocate an object with n null fields; rc(x) ← 0
L2  add x to ZCT
L3  return x

WRITE-ROOT(i, y)
L4  rᵢ ← y                                 ▷ no count changes

WRITE(p, i, y)                             ▷ p[i] ← y for a heap object p
L5  if y ≠ null then rc(y) ← rc(y) + 1
L6  z ← p[i]; p[i] ← y
L7  if z ≠ null then DEC(z)

DEC(z)
L8  rc(z) ← rc(z) − 1
L9  if rc(z) = 0 then add z to ZCT

COLLECT()                                  ▷ the mutator is stopped
L10 for each root rᵢ ≠ null do rc(rᵢ) ← rc(rᵢ) + 1
L11 while ZCT is not empty do
L12     x ← remove some object from ZCT
L13     if rc(x) = 0 then
L14         for each field x[j] ≠ null do DEC(x[j])
L15         free(x)
L16 for each root rᵢ ≠ null do DEC(rᵢ)
```

Line L10 counts the roots for the time of the collection, so an object that a root refers to has a positive count and stays. Line L14 can add the children of a freed object to the ZCT, and the loop frees them in the same collection. Line L16 removes the root counts again; an object that only roots refer to drops back to zero and returns to the ZCT for the next collection.

## Example

Roots $r_0$ and $r_1$. Object $a$ and object $b$ have one field each, and $c$ has none.

| step | operation | counts | ZCT |
|---|---|---|---|
| 1 | $a \leftarrow$ NEW(1), $r_0 \leftarrow a$ | $a = 0$ | $\{a\}$ |
| 2 | $b \leftarrow$ NEW(1), $a[0] \leftarrow b$ | $a = 0$, $b = 1$ | $\{a, b\}$ |
| 3 | $c \leftarrow$ NEW(0), $b[0] \leftarrow c$ | $a = 0$, $b = 1$, $c = 1$ | $\{a, b, c\}$ |
| 4 | $r_1 \leftarrow c$ | no change | $\{a, b, c\}$ |
| 5 | $r_0 \leftarrow \text{null}$ | no change | $\{a, b, c\}$ |
| 6 | COLLECT, line L10 | $a = 0$, $b = 1$, $c = 2$ | $\{a, b, c\}$ |
| 7 | take $a$: count 0, free it | $b = 0$, $c = 2$ | $\{b, c\}$ |
| 8 | take $b$: count 0, free it | $c = 1$ | $\{c\}$ |
| 9 | take $c$: count 1, keep it | $c = 1$ | $\{\}$ |
| 10 | line L16 | $c = 0$ | $\{c\}$ |

Steps 4 and 5 are root writes, so they change no count, although in plain reference counting step 5 would free $a$ at once. In step 1, $a$ has count 0 while $r_0$ holds it, and the ZCT keeps it safe until a collection proves it dead. The collection frees $a$ and $b$. The object $c$ survives with count 0, because only the root $r_1$ refers to it, and it waits in the ZCT.

## Correctness

Between collections, two invariants hold: (I1) $\mathrm{rc}(x)$ is the number of heap fields of unfreed objects that refer to $x$, and (I2) every unfreed object with count 0 is in the ZCT. During COLLECT, line L10 makes each count equal to the number of heap fields and roots that refer to the object, and line L13 frees an object only when this number is 0, so no reachable object is freed. When the loop ends, the ZCT is empty, so every unfreed object has a heap or root reference. After COLLECT, as with plain reference counting, the unfreed garbage is exactly the garbage that a cycle of garbage reaches, and the ZCT holds exactly the objects that only roots refer to. The full proof is below.

## Complexity

- **Mutator.** A root write costs nothing extra. A heap write costs $O(1)$: two count updates and at most one insertion into the ZCT.
- **Collection.** COLLECT takes $O(r + z + k)$ time, where $r$ is the number of roots, $z$ the number of objects that pass through the ZCT, and $k$ the number of fields of the freed objects. Each entry is removed once, and each freed object is handled once.
- **Amortized.** Charge the ZCT entry of an object to the NEW or the DEC that made it, and the freeing of an object to its NEW. The roots are scanned once per collection, so if collections run after a fixed amount of allocation, all costs are $O(1)$ amortized per operation.
- **Space.** The ZCT holds at most one entry per object. Systems often bound its size and run COLLECT when it is full.

## Properties

- **Delayed freeing.** An object becomes free only at the next collection, not at the write that kills it.
- **Short, bounded pauses.** A collection scans the roots and the ZCT, not the heap. The pause depends on the size of the stacks and on the garbage that it frees.
- **Not complete.** Like plain reference counting, it never frees a cycle of garbage.
- **A stop for the roots.** The mutator must be at a safe point during COLLECT, because the collector reads its registers and stack.

## Variants and improvements

- **Globals as heap fields.** Some systems count references from global variables and treat only registers and stacks as roots. This keeps the root scan small.
- **Coalesced reference counting.** Log the first change of each heap field between two collections, and apply only the net count changes at the collection. This removes most of the remaining heap count updates.
- **Deferral with a log.** Instead of a ZCT, log each decrement and process the log at the collection. Many high-performance reference counting collectors combine deferral, coalescing and a cycle collector.
- **Cycle collection.** [Trial deletion](/trial-deletion/) or a backup tracing collector frees the cycles: see [cycle collection](/cycle-collection/). Trial deletion needs only the heap counts, so it works with deferred counts too, once the roots are taken into account.
- **Plain counting.** Without deferral, each count is exact and freeing is immediate: [reference counting](/reference-counting/).

## When to use it

Use deferred reference counting when you want reference counting but cannot pay for count updates on every write to a local variable, which is the case in most compiled languages. The runtime must be able to stop threads at safe points and to find their roots, as a tracing collector must. If you need memory back at the exact moment an object dies, for example to close a file, use plain counting for those objects.

## Pitfalls

- **Freeing at count zero.** An object with count zero may still be held by a root. Only COLLECT, after the root scan, may free it.
- **Forgetting new objects.** A new object has count 0 and lives only in roots at first. If NEW does not put it in the ZCT, a later collection does not see it, and if it dies before any heap field refers to it, it leaks.
- **Missing roots.** Every root must be counted at line L10. A root that the scan misses, such as a value in a register that the stack map does not list, causes a wrong free.
- **Unbalanced root counts.** Line L16 must undo exactly what line L10 did, on the same root values. If the mutator runs between the two lines, the counts become wrong.

## Implementations

## History

Deutsch and Bobrow (1976) designed the method for an incremental collector for Lisp. They observed that most count changes come from local variables, stopped counting those references, and kept the objects with a zero count in a table that a scan of the variables checks. Later high-performance reference counting collectors, described in Chapter 5 of the Jones, Hosking and Moss handbook, keep this deferral and add coalesced counting and cycle collection.

## References
