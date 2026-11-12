---
tag: CWN22Y
kind: algorithm
slug: cheney-copying-collector
name: Cheney's copying collector
aliases:
- Cheney's algorithm
- breadth-first copying
- Cheney scan
area: systems/garbage-collection
level: core
summary: "A copying collector with no stack and no recursion. Two pointers into to-space, scan and free, make the copied objects themselves a breadth-first queue."
solves: [automatic-memory-reclamation]
variant_of: copying-collection
model: word-ram
complexity:
  vars: {L: the number of words in reachable objects, r: the number of roots}
  time: {worst: O(r + L)}
  space: {extra: O(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1970
  people: [C. J. Cheney]
  note: Cheney's two-page paper in Communications of the ACM replaced the recursion of earlier copying collectors by a scan of to-space.
prereqs: [copying-collection, breadth-first-search]
see_also: [copying-collection, tricolor-marking, baker-real-time-collector, generational-garbage-collection, mark-and-sweep, queue, bump-pointer-allocation, schorr-waite-marking]
sources:
  - paper: doi:10.1145/362790.362798
    title: C. J. Cheney, A nonrecursive list compacting algorithm, Communications of the ACM 13(11), 677-678, 1970
    locator: the whole paper; the two pointers into the new space and the breadth-first copy of the list structure
  - paper: doi:10.1145/363269.363280
    title: Robert R. Fenichel and Jerome C. Yochelson, A LISP garbage-collector for virtual-memory computer systems, Communications of the ACM 12(11), 611-612, 1969
    locator: the semispace scheme with a recursive copy that Cheney's scan replaces
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 4, Section 4.1 (Cheney scanning, Algorithm 4.2 with the scan and free pointers) and Section 4.2 (breadth-first order and locality)
---

Cheney's copying collector is the standard way to implement a [semispace copying collector](/copying-collection/). It copies the objects reachable from the roots into to-space with no stack and no recursion. Two pointers into to-space do all the work: everything below $\mathit{scan}$ is fully processed, and the objects between $\mathit{scan}$ and $\mathit{free}$ have been copied but their fields still point into from-space. So to-space itself is the [queue](/queue/) of a [breadth-first search](/breadth-first-search/), and the objects end in breadth-first order. C. J. Cheney published it in 1970, in a two-page paper.

## In plain words

You move the things you still use from an old room to an empty new room. First carry over the things you hold, and line them up along the wall of the new room. Now walk along that line, one thing at a time. For each thing, look at what it needs from the old room. If something needed is still in the old room, carry it over and put it at the end of the line, and leave a note in its old place. If there is already a note, it was carried before, so just write down its new place.

You stop when your walk reaches the end of the line. The line itself was your to-do list, so you never needed a separate one.

## The problem

**Heap model.** As for [copying collection](/copying-collection/): two semispaces of $S$ words; each object has a header word with its size and then its pointer fields, each an object or nil; the program allocates in to-space with a [bump pointer](/bump-pointer-allocation/); the mutator holds its references in $r$ root slots and is stopped during a collection.

**Task.** Move the reachable objects, which take $L$ words, into the other semispace, and update every root and every field, with only a constant amount of space beside the two semispaces. A recursive copy needs a stack as deep as the longest chain of objects, which can be as large as the heap; a collector runs exactly when memory is short, so it cannot count on that space.

**What is measured.** Time, extra space, and the order of the copies.

## The algorithm

```pseudo id=main
COLLECT()
L1  swap from-space and to-space; scan ← free ← start of to-space
L2  for each root slot s do s ← FORWARD(s)
L3  while scan < free do
L4      for each field f of the object at scan do f ← FORWARD(f)
L5      scan ← scan + size(object at scan)

FORWARD(p)
L6  if p = nil then return nil; if p is forwarded then return its forwarding address
L7  b ← free; copy the size(p) words of p to b; free ← free + size(p)
L8  header of p ← "forwarded to b"
L9  return b
```

FORWARD is the same as in the [semispace collector](/copying-collection/), except that it pushes nothing: copying an object to $\mathit{free}$ is enough to put it at the end of the queue. The loop of lines L3 to L5 takes the object at $\mathit{scan}$, the front of the queue, and forwards its fields. It stops when the queue is empty, $\mathit{scan} = \mathit{free}$. In the colors of [tricolor marking](/tricolor-marking/), the objects below $\mathit{scan}$ are black, the objects between $\mathit{scan}$ and $\mathit{free}$ are gray, and the objects still in from-space are white.

## Example

A semispace has 11 words. The objects are $A \to (B, C)$, $B \to (D)$, $C \to (E)$, $D$ and $E$ with no fields, and $G \to (A)$, which is garbage. The root is $A$. In from-space they lie at $A = 0$ (size 3), $B = 3$, $C = 5$ (size 2), $D = 7$, $E = 8$ (size 1), $G = 9$ (size 2). To-space starts at 11.

| step | action | scan | free | queue (scan to free) |
|---|---|---|---|---|
| L2 | copy $A$ to 11 | 11 | 14 | $A$ |
| scan $A$ | copy $B$ to 14 and $C$ to 16; fields of $A$ become 14, 16 | 14 | 18 | $B, C$ |
| scan $B$ | copy $D$ to 18; field of $B$ becomes 18 | 16 | 19 | $C, D$ |
| scan $C$ | copy $E$ to 19; field of $C$ becomes 19 | 18 | 20 | $D, E$ |
| scan $D$ | no fields | 19 | 20 | $E$ |
| scan $E$ | no fields | 20 | 20 | empty |

The words 11 to 19 are $[3, 14, 16 \mid 2, 18 \mid 2, 19 \mid 1 \mid 1]$ and the root is 11. The order $A, B, C, D, E$ is the breadth-first order from $A$. A copy with a stack, as on the [copying collection](/copying-collection/) page, gives $A, B, C, E, D$ on this heap, because it scans $C$ before $B$. The garbage $G$ was never visited.

## Correctness

At line L3, the copies fill to-space from its start to $\mathit{free}$; the copies below $\mathit{scan}$ have all their fields forwarded, and the copies from $\mathit{scan}$ to $\mathit{free}$ still hold their original fields; and the originals of the copies, in address order, are a prefix of the breadth-first list of the reachable objects. Scanning the copy at $\mathit{scan}$ forwards its fields in order and appends the objects not yet copied, which is one step of breadth-first search. Each object is copied once, because its header becomes a forwarding address, so $\mathit{free}$ is bounded and $\mathit{scan}$ catches up. At the end every copy is scanned, every reachable object is copied, and every pointer holds the new address. The full proof is in the proofs section.

## Complexity

The model is the [word RAM](/word-ram/) with the heap model above.

- **Time.** Each root is forwarded once. Each reachable object is copied once and scanned once, and each field is forwarded once. So a collection takes $O(r + L)$ time. The garbage is never visited.
- **Space.** The two pointers $\mathit{scan}$ and $\mathit{free}$, so $O(1)$ beside the second semispace, whatever the shape of the data.
- **Amortized.** As for every semispace collector, the cost per allocated word is about $cL/(S - L)$; see [the space-time tradeoff](/gc-space-time-tradeoff/).

## Properties

- **Iterative, constant extra space.** No stack, no recursion, no extra queue. This is the main point of the algorithm.
- **Breadth-first order.** The copies end in breadth-first order. This is simple and deterministic, but it can place an object far from the objects it points to: the cells of a long list are spread out when each cell also points to other data. For the cache, a depth-first order is often better.
- **Compacting.** The copies are packed at the start of to-space, and allocation continues at $\mathit{free}$.
- **A natural incremental form.** The scan can be cut into steps. [Baker's real-time collector](/baker-real-time-collector/) does a few steps of the scan at each allocation.

## Variants and improvements

- **Approximately depth-first copying.** Moon (1984) scans the last partly filled page of to-space before going on, so that children land near their parents more often, still with no stack.
- **Hierarchical decomposition.** Wilson, Lam and Moher (1991) improve the locality of the copies by a two-level scan.
- **Generational scavenging.** In a [generational collector](/generational-garbage-collection/), a Cheney scan copies the survivors of the young generation; the remembered set adds roots from the old generation.
- **Parallel scanning.** Several threads scan to-space at once, each with its own block for copies, and they steal work from each other.

## When to use it

Use Cheney's algorithm whenever you implement a copying collector and want it simple and safe: it needs no extra memory at a time when memory is short, and its loop is short. It is the usual scavenger for the young generation. If the cache behavior of the copies matters a lot, consider a variant that copies in a more depth-first order.

## Pitfalls

- **Scanning by objects, not by words.** The scan must step by the size of each object, which needs a header that tells the size and which words are pointers.
- **The forwarding test.** FORWARD must test for a forwarding address before it copies, or an object with two pointers to it is copied twice.
- **Overwriting the header first.** The forwarding address goes into the old header after the copy, or the copy reads the forwarding address as the size.
- **Roots in from-space after the flip.** Every root must go through FORWARD at line L2, including the roots of every thread and the values held by the allocator during a collection.

## Implementations

## History

Fenichel and Yochelson (1969) introduced semispace copying with a recursive copy. Cheney (1970) showed that the recursion is not needed: the new space itself, read from left to right, holds all the work that remains. The algorithm became the basis of later copying collectors, such as Baker's incremental collector (1978) and the generation scavenging of Ungar (1984).

## References
