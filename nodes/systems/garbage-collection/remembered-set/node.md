---
tag: ASEXAM
kind: data-structure
slug: remembered-set
name: Remembered set
aliases:
- remembered sets
- remset
- sequential store buffer
area: systems/garbage-collection
level: core
summary: "The set of old-to-young slots (or objects) that a minor collection treats as roots. Often a sequential store buffer drained into a hash set."
model: word-ram
complexity:
  vars: {b: the capacity of the store buffer, r: the number of remembered entries}
  time: {expected: O(1), worst: O(b)}
  space: {extra: Θ(b + r)}
prereqs: [generational-garbage-collection, write-barrier, hash-table]
see_also: [card-marking, generational-hypothesis, train-algorithm, generational-collector-beltway, garbage-first-collector, gc-roots]
sources:
  - paper: doi:10.1145/800020.808261
    title: David Ungar, Generation scavenging, a non-disruptive high performance storage reclamation algorithm, ACM SIGSOFT/SIGPLAN Software Engineering Symposium on Practical Software Development Environments, 157-167, 1984
    locator: the remembered set of old objects that hold pointers to new objects, and the store check that fills it
  - paper: doi:10.1145/141936.141946
    title: Antony L. Hosking, J. Eliot B. Moss and Darko Stefanovic, A comparative performance evaluation of write barrier implementations, OOPSLA 1992, 92-109
    locator: the sequential store buffer, the remembered sets kept in hash tables, card marking with several card sizes, and their measured costs
  - book: isbn:9781032218038
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, second edition, CRC Press, 2023
    locator: Section 9.8 (Inter-generational pointers, remembered sets and pointer direction) and Section 11.8 (precision of write barriers, hash tables, sequential store buffers, overflow action)
  - paper: doi:10.1002/spe.4380190206
    title: Andrew W. Appel, Simple generational garbage collection and fast allocation, Software Practice and Experience 19(2), 171-183, 1989
    locator: the list of stored-into locations that the barrier appends to, scanned at each minor collection
---

A remembered set is the record that a [generational collector](/generational-garbage-collection/) keeps of the pointers from the old generation into the young one. It holds slots $(o, i)$, field $i$ of an old object $o$, or whole objects $o$, and a minor collection treats each remembered slot as one more [root](/gc-roots/). The [write barrier](/write-barrier/) adds entries when the mutator stores a young pointer into an old object. A common representation is a *sequential store buffer*, an array that the barrier appends to in $O(1)$ time, drained into a [hash set](/hash-table/) that removes the duplicates. With it, a minor collection costs time proportional to the remembered entries and the survivors, not to the size of the old generation.

## In plain words

The collector wants to clean only the young part of the heap. But an old object can point to a young one, and the collector does not look at old objects. So the program keeps a list. Each time it stores a pointer to a young object into an old object, it writes the place of that store on the list. When the collector runs, it reads the list and treats each place on it as a starting point.

Writing to the end of a list is very fast, so the program does that on each store. When the list is full, the program moves its items into a table that keeps each place once, and the list starts again empty.

## The abstract type

A remembered set is a set of heap places with these operations.

- `record(o, i)`: the barrier reports that field $i$ of old object $o$ now holds a young pointer.
- `roots()`: at a minor collection, list each remembered slot that still holds a young pointer, once.
- `retain(keep)`: after a collection, drop the entries that no longer hold young pointers.
- `forget(D)`: after a major collection, drop the entries of the freed old objects $D$.

The contract is the invariant (I) below: each old-to-young slot of the heap is covered by an entry. Entries may be stale (the slot was overwritten later) or duplicated; `roots()` filters them. So the set may be larger than the exact set of old-to-young slots, but never smaller.

## Representation

- $B[0 \ldots b-1]$, the sequential store buffer, and $top$, the number of entries in it.
- $H$, a hash set of entries.
- For object precision, a *remembered* bit in the header of each old object.
- An entry is the slot $(o, i)$ with slot precision, or the object $o$ with object precision.

**Invariant (I).** Between operations, for each old object $o$ and each field $i$ of $o$ that holds a young object: with slot precision, $(o, i) \in H \cup B[0 \ldots top-1]$; with object precision, $o \in H \cup B[0 \ldots top-1]$ and $o$ has its remembered bit set.

## Operations

```pseudo id=main
RECORD(o, i)                         ▷ called by the write barrier
L1  e ← (o, i) with slot precision, or o with object precision
L2  if object precision and o.remembered then return
L3  if object precision then o.remembered ← true
L4  B[top] ← e; top ← top + 1
L5  if top = b then DRAIN()

DRAIN()
L6  for j ← 0 to top − 1 do H ← H ∪ {B[j]}
L7  top ← 0

ROOTS()                              ▷ at a minor collection
L8  DRAIN()
L9  for each entry e in H do
L10     for each slot s of e that holds a young object do yield s

RETAIN(keep)                         ▷ after a minor collection
L11 H ← {e ∈ H : keep(e)}; clear the remembered bit of each dropped object
```

**RECORD** is the barrier's slow path. With object precision, the header bit makes a second store into the same object free (line L2), which is the scheme of Ungar's scavenger. The append of line L4 is one store and one increment. Line L5 drains a full buffer. Some systems put a protected page after the buffer, so that the overflow test is a hardware trap and the fast path has no branch.

**DRAIN** moves the buffer into $H$ and so removes the duplicates. It takes $O(top)$ expected time with a hash set.

**ROOTS** drains first, so that $H$ holds all entries. For a slot entry it yields the slot if it still holds a young pointer. For an object entry it scans all fields of the object. Each slot is yielded at most once, because $H$ has no duplicates and the slots of distinct objects differ.

**RETAIN** runs after the copy. A slot whose target was promoted now holds an old pointer and is dropped; a slot whose target is still young (a survivor) stays. The collector also calls RECORD for each field of a newly promoted object that points to a young survivor.

## Example

Use slot precision and $b = 3$. Objects $A$ and $B$ are old; $x$ and $y$ are young.

| step | store | barrier action | $B$ | $H$ |
|---|---|---|---|---|
| 1 | $A.f_0 \gets x$ | RECORD$(A, 0)$ | $(A,0)$ | |
| 2 | $B.f_1 \gets y$ | RECORD$(B, 1)$ | $(A,0), (B,1)$ | |
| 3 | $A.f_0 \gets y$ | RECORD$(A, 0)$, buffer full, DRAIN | | $(A,0), (B,1)$ |
| 4 | $B.f_1 \gets$ nil | none: the value is not young | | $(A,0), (B,1)$ |
| 5 | $A.f_1 \gets x$ | RECORD$(A, 1)$ | $(A,1)$ | $(A,0), (B,1)$ |

At the minor collection, ROOTS drains the buffer, so $H = \{(A,0), (B,1), (A,1)\}$. It yields $(A, 0)$, which holds $y$, and $(A, 1)$, which holds $x$. The entry $(B, 1)$ is stale: the slot holds nil, so it is skipped. The duplicate of $(A, 0)$ from step 3 was removed by the drain. If the collection promotes both $x$ and $y$, RETAIN drops all three entries, and the set is empty again.

## Correctness

Each operation keeps (I), if the barrier calls RECORD on every store that puts a young pointer into an old object, and the collector calls RECORD for the young fields of each object it promotes. A store of any other kind cannot create an old-to-young slot. DRAIN moves entries from $B$ to $H$ and loses none. RETAIN drops only entries that hold no young pointer. So after any sequence of operations, ROOTS yields every old-to-young slot, exactly once each, and no other slot. The full proof is in the proof file below.

## Complexity

| operation | time | note |
|---|---|---|
| RECORD | $O(1)$ worst case without a drain; $O(b)$ expected with one | $O(1)$ amortized expected over a sequence, since each entry is drained once |
| DRAIN | $O(top)$ expected | hash set inserts |
| ROOTS | $O(r)$ expected for slots; $O(\sum \text{fields of remembered objects})$ for objects | plus the drain |
| RETAIN | $O(r)$ expected | |

The space is $\Theta(b + r)$ words, where $r = |H|$. The number of entries $r$ is at most the number of distinct old-to-young slots ever recorded since the last RETAIN, so a program that stores into the same few slots keeps $H$ small, while the buffer can still fill with duplicates. These bounds are in the [word RAM](/word-ram/) model with a hash set of expected $O(1)$ time per operation.

## Variants

- **Precision.** Slot precision records exactly the field; object precision records the object and scans all its fields at a collection; [card marking](/card-marking/) records a region of a fixed size, and scans every object on a dirty card. Coarser entries make the barrier cheaper and the collection more expensive. Hosking, Moss and Stefanovic measured these choices against each other in a Smalltalk system.
- **No filter in the barrier.** The barrier can append every pointer store into the heap, and leave the test "old object, young value" to the drain. The fast path is then two instructions, but the buffer fills faster.
- **Per-region remembered sets.** A collector that collects any region, not only the young one, keeps one set per region, holding the slots outside that region that point into it. [Garbage-First](/garbage-first-collector/), the [train algorithm](/train-algorithm/) and [Beltway](/generational-collector-beltway/) do this, and record a pointer only when its target is collected before its source.
- **Card queues.** A barrier can mark a card and append the card, not the slot, to a buffer, as in G1's dirty card queues. The buffer then holds cards to refine into per-region sets later.
- **Overflow handling.** When $H$ grows too large, a collector can promote the targets of the remembered slots, or switch to a card table for the hot region.

## When to use it

Use a slot or object remembered set when old-to-young stores are rare and spread over few places, because then $r$ is small and each entry is cheap to process. Use [card marking](/card-marking/) when stores are frequent and clustered, as in large arrays, because the barrier is an unconditional byte store and the space is fixed. A remembered set is not a list of all pointers into a region: it holds only the pointers whose source is not collected together with their target. It also differs from the dirty-page approach of conservative collectors, which needs no barrier code but finds changes only at page granularity.

## Pitfalls

- **Forgetting promoted objects.** An object that is promoted while it points to a young survivor creates an old-to-young slot without any mutator store. The collector must RECORD it; otherwise invariant (I) breaks and the next minor collection frees a live object.
- **Not filtering stale entries.** A remembered slot can hold nil or an old pointer by the time of the collection. Line L10 must read the slot again and skip it. Treating the recorded value as a root keeps garbage alive.
- **Entries of dead old objects.** After a major collection frees old objects, their entries must go. A stale entry then names freed memory, which the next minor collection would read.
- **Unbounded duplicates.** A loop that stores into one old slot fills the buffer with the same entry. Drain into a hash set, or use object precision with a header bit.
- **Nepotism.** An entry of a garbage old object still acts as a root and keeps its young targets alive until the next major collection.

## Implementations

## History

Ungar's generation scavenging of 1984 introduced the term: its remembered set held the old objects that pointed to new ones, with a bit in each object to avoid duplicates. Appel's collector of 1989 kept a list of the locations stored into. Hosking, Moss and Stefanovic compared sequential store buffers, remembered sets in hash tables and card marking in 1992, and found that the best choice depends on the store pattern of the program.

## References
