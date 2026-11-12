---
tag: D0R5KM
kind: algorithm
slug: copying-collection
name: Copying garbage collection
aliases:
- copying collector
- semispace collector
- semispace copying collection
area: systems/garbage-collection
level: intro
summary: "Split the heap into two halves. To collect, copy every object reachable from the roots into the empty half, leave a forwarding address in each old copy, then drop the old half whole."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {L: the number of words in reachable objects, r: the number of roots, S: the size of one semispace in words}
  time: {worst: O(r + L)}
  space: {extra: O(S)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1969
  people: [Robert R. Fenichel, Jerome C. Yochelson]
  note: Fenichel and Yochelson split the memory into two semispaces and copied the reachable objects from one to the other; Cheney made the copy non-recursive in 1970.
prereqs: [tracing-garbage-collection, depth-first-search]
see_also: [cheney-copying-collector, mark-and-sweep, mark-compact, heap-compaction, bump-pointer-allocation, gc-space-time-tradeoff, generational-garbage-collection, baker-real-time-collector]
sources:
  - paper: doi:10.1145/363269.363280
    title: Robert R. Fenichel and Jerome C. Yochelson, A LISP garbage-collector for virtual-memory computer systems, Communications of the ACM 12(11), 611-612, 1969
    locator: the two semispaces, the copy of the reachable list structure, and the forwarding addresses left in the old space
  - paper: doi:10.1145/362790.362798
    title: C. J. Cheney, A nonrecursive list compacting algorithm, Communications of the ACM 13(11), 677-678, 1970
    locator: the copy without recursion, with the to-space itself as the queue
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 4, Section 4.1 (semispace copying collection, Algorithms 4.1 and 4.2, flip, forward and copy) and Section 4.2 (traversal order and locality)
  - book: isbn:9780471941484
    title: Richard Jones and Rafael Lins, Garbage Collection, Algorithms for Automatic Dynamic Memory Management, Wiley, 1996
    locator: Chapter 6, copying garbage collection
---

Copying garbage collection divides the heap into two equal halves, the *semispaces*. The program allocates in one of them, to-space, with a [bump pointer](/bump-pointer-allocation/). When it is full, the collector swaps the roles of the two halves and copies every object reachable from the roots out of the old half, now from-space, into the empty half. Each copied object leaves a *forwarding address* in its old place, so that every later pointer to it finds the copy. Then the whole of from-space is free at once; the garbage is never visited. Fenichel and Yochelson described the method for LISP in 1969. It is the base of [Cheney's algorithm](/cheney-copying-collector/) and of the young generation in most [generational collectors](/generational-garbage-collection/).

## In plain words

You have two rooms, and you live in one of them. When it is full of things, you do not look for the junk. You look for the things you still use: start with those you hold, and then each thing that one of them needs. Carry each one to the empty room, and put a note in its old place that says where it went, so you never carry it twice. When nothing more is needed, the old room holds only junk, so you clear it all at once.

The new room is now tidy: the things are packed at one end, and the rest of the room is free. The price is that one room is always kept empty.

## The problem

**Heap model.** The memory has two semispaces of $S$ words each. Each object has a header word with its size, and then its pointer fields, each the address of an object or nil. The program allocates in to-space by bumping a pointer $\mathit{free}$. The mutator holds its references in $r$ root slots and is stopped during a collection ([stop the world](/stop-the-world-collection/)).

**Task.** When to-space is full, move the objects reachable from the roots, which take $L \le S$ words, into the other semispace, and update the roots and fields so that the reachable graph is the same up to a renaming of addresses. The free space after a collection is one block of $S - L$ words.

**What is measured.** The time of a collection, which should depend on $L$ but not on the garbage, and the memory, $2S$ words.

## The algorithm

```pseudo id=main
COLLECT()
L1  swap from-space and to-space; free ← start of to-space; W ← empty stack
L2  for each root slot s do s ← FORWARD(s)
L3  while W is not empty do
L4      b ← pop W                               ▷ a copy whose fields still point to from-space
L5      for each field f of b do f ← FORWARD(f)

FORWARD(p)
L6  if p = nil then return nil; if p is forwarded then return its forwarding address
L7  b ← free; copy the size(p) words of p to b; free ← free + size(p)
L8  header of p ← "forwarded to b"
L9  push b on W; return b

ALLOCATE(n)
L10 if free + n > end of to-space then COLLECT(); if still free + n > end then fail
L11 a ← free; free ← free + n; return a
```

FORWARD copies an object the first time any pointer to it is seen, and returns the copy every later time, through the forwarding address in the old header. The stack $W$ holds the copies that have not been scanned yet; scanning a copy forwards each of its fields. Fenichel and Yochelson wrote the copy as a recursive procedure; the explicit stack does the same work in a [depth-first](/depth-first-search/) order with no recursion. [Cheney's algorithm](/cheney-copying-collector/) removes the stack too: the copies in to-space are themselves the queue.

The new object in ALLOCATE must not keep a pointer across COLLECT that the collector cannot see. In the implementation, the field values of a new object are held as extra roots during a collection.

## Example

A semispace has $S = 9$ words. Four objects sit in from-space; the size counts the header, and the root is $A$.

| object | address | size | fields |
|---|---|---|---|
| $A$ | 0 | 3 | $B$, $C$ |
| $B$ | 3 | 2 | $C$ |
| $C$ | 5 | 2 | $A$ |
| $D$ | 7 | 2 | $B$ |

To-space starts at 9.

| step | action | free | $W$ |
|---|---|---|---|
| L2 | copy $A$ to 9; $A$ forwarded to 9 | 12 | 9 |
| L4, L5 | scan 9: copy $B$ to 12, copy $C$ to 14 | 16 | 12, 14 |
| L4, L5 | scan 14 ($C$): $A$ is forwarded, so the field becomes 9 | 16 | 12 |
| L4, L5 | scan 12 ($B$): $C$ is forwarded, so the field becomes 14 | 16 | empty |

To-space now holds $[3, 12, 14 \mid 2, 14 \mid 2, 9]$ in the words 9 to 15, and the root is 9. The live data is 7 words, and the 11 words from 16 to 26 are free. $D$ was garbage, and the collector never looked at it.

## Correctness

The proof keeps an invariant at line L3: each from-space object is either not copied, or forwarded to a copy that holds its size and, for each field $v$, either $v$ (if the copy is still on the stack) or the address of the copy of $v$ (if it was scanned); the stack holds the unscanned copies once each; the copies fill to-space from its start to $\mathit{free}$; and only reachable objects are copied. Each object is copied at most once, because its header changes to a forwarding address, so the loop ends. Along any path from a root, each object is copied and its copy scanned, so the next object is copied too; so every reachable object is copied. When the stack is empty, every field holds the new address. The full proof is in the proofs section.

## Complexity

The model is the [word RAM](/word-ram/) with the heap model above.

- **Time.** Each root is forwarded once, each reachable object is copied once and scanned once, and each of its words is moved once. So a collection takes $O(r + L)$ time. The garbage is never touched, so the cost does not depend on the size of the heap.
- **Space.** The second semispace, $S$ words, is the main cost: at most half of the memory holds data. The stack $W$ needs up to one entry for each reachable object; Cheney's algorithm needs none.
- **Amortized cost.** A collection frees $S - L$ words for new objects, so the collection cost per allocated word is about $cL / (S - L)$ for a constant $c$. It falls as the semispaces grow; see [the space-time tradeoff of garbage collection](/gc-space-time-tradeoff/).

## Properties

- **Compacting.** The copies are packed at the start of to-space, so there is no fragmentation, and allocation is a bump of a pointer.
- **Cost proportional to the live data.** The best case for a copying collector is a heap that is mostly garbage, which is the usual case for young objects.
- **Half the memory in reserve.** A semispace collector can use only $S$ of its $2S$ words for data.
- **Moves objects.** The collector must know every pointer exactly; it cannot work with ambiguous roots unless it pins their targets, as [mostly-copying collection](/mostly-copying-collection/) does.
- **Traversal order.** The order of the copies follows the traversal: depth-first with a stack, breadth-first with Cheney's queue. Depth-first tends to place an object next to its first child, which is often better for the cache.

## Variants and improvements

- **[Cheney's algorithm](/cheney-copying-collector/).** A breadth-first copy with two pointers into to-space and no stack or recursion.
- **Generational copying.** Copy only the young objects, which mostly die young; see [generational garbage collection](/generational-garbage-collection/) and the [generational hypothesis](/generational-hypothesis/).
- **Incremental copying.** [Baker's real-time collector](/baker-real-time-collector/) copies a few objects at each allocation, with a read barrier that forwards every pointer the program loads.
- **Approximately depth-first copying.** Moon's and other variants change the scan order to place related objects together without a full stack.
- **Mostly-copying.** Pin the pages that ambiguous roots point to, and copy the rest.

## When to use it

Use a copying collector when most objects die young and memory is not tight: the cost is proportional to the survivors, and allocation is as cheap as it can be. This is why the young generation of most production collectors is a copying collector. Do not use a pure semispace collector for a large heap of long-lived data: it copies the same data at each collection and wastes half the memory. There, [mark-compact](/mark-compact/) or [mark-and-sweep](/mark-and-sweep/) is better.

## Pitfalls

- **Forgetting a root.** Every reference that the mutator holds, including those in registers and in a half-built object, must be forwarded. A missed root keeps a from-space address, and from-space will be reused.
- **Copying twice.** FORWARD must check the forwarding address first. Without it, an object with two pointers to it is copied twice, and the graph is not the same.
- **Overwriting the fields with the forwarding address.** The forwarding address goes into the old copy only after the object has been copied, and only into a word that the copy no longer needs.
- **To-space overflow.** A semispace collector must collect before the live data exceeds a semispace. A generational collector that promotes into an older space needs a fallback when that space is full.

## Implementations

## History

Minsky described a collector for LISP that copied the reachable list structure to secondary storage and back, in 1963. Fenichel and Yochelson (1969) introduced the two semispaces in main memory, for a LISP system with virtual memory, with a recursive copy. Cheney (1970) made the copy non-recursive with a breadth-first scan of to-space. Baker (1978) made it incremental, and Lieberman and Hewitt (1983) and Ungar (1984), whose generation scavenging gave the alias *scavenging*, used it for the young objects of a generational collector.

## References
