---
tag: EE82ME
kind: algorithm
slug: mostly-copying-collection
name: Mostly-copying collection
aliases:
- Bartlett mostly-copying
- mostly-copying garbage collection
- Bartlett's mostly-copying collector
area: systems/garbage-collection
level: research
summary: "A copying collector for ambiguous roots: pages that a root word may point into are promoted in place and keep their objects; all other live objects are copied."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {r: the number of root words, L: the words of the retained objects, N: the number of pages}
  time: {worst: O(r + L + N), best: O(r + N)}
  space: {extra: O(N + L)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1988
  people: [Joel F. Bartlett]
  note: Bartlett described the collector in a DEC Western Research Laboratory report in 1988, for a Scheme system that compiled to C and so had no precise information about the stack.
prereqs: [conservative-garbage-collection, copying-collection]
see_also: [cheney-copying-collector, precise-garbage-collection, boehm-gc, heap-compaction, generational-garbage-collection, immix-collector]
sources:
  - paper: "Joel F. Bartlett, Compacting garbage collection with ambiguous roots, DEC Western Research Laboratory, Research Report 88/2, February 1988"
    locator: the division of the heap into pages with a space identifier, the promotion of pages that ambiguous roots point into, and the copying of all other reachable objects
  - paper: doi:10.1002/spe.4380180902
    title: Hans-Juergen Boehm and Mark Weiser, Garbage collection in an uncooperative environment, Software Practice and Experience 18(9), 807-820, 1988
    locator: the fully conservative, non-moving alternative for the same setting
  - book: isbn:9781032218038
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, second edition, CRC Press, 2023
    locator: Chapter 11, Section 11.2 (Finding pointers), on conservative roots, pinning and Bartlett's mostly-copying collector
---

Mostly-copying collection lets a copying collector work when the roots are ambiguous: the stack and the registers hold words that may be pointers or may be numbers, as in a program compiled to C. The heap is divided into pages, and each page carries a *space number*. A collection first *promotes* every page that a root word points into: it changes the page's space number to the new space, so the page and all its objects become part of to-space without moving. Then it copies all other reachable objects, as a [Cheney](/cheney-copying-collector/) collector would, starting from the objects on the promoted pages. The objects that the roots may point to never move, so the root words are never changed; every other object is compacted. The heap objects must have a precise layout, so that the collector knows which fields to update.

## In plain words

A copying collector moves live objects to a new area and fixes every pointer to them. But some values on the stack might be pointers or might be plain numbers, and the collector cannot tell. If it changed such a value and it was really a number, the program would break.

Bartlett's answer is to leave those objects where they are. The heap is cut into pages. If any value on the stack points into a page, the whole page is kept in place, and is simply relabelled as part of the new area. Everything else that is still in use is copied. So the objects on the stack's pages stay put, and the rest is compacted.

## The problem

Collect a heap of objects whose fields are known precisely, given a set of *ambiguous* roots: words that may or may not be pointers and that the collector must not change. Free every page that holds no object the program can reach, keep the object graph intact, and move as many objects as possible, to compact the heap and allow fast allocation.

## The algorithm

Each page $g$ has a space number $space[g]$; the pages of the current space hold all objects. Allocation takes free pages, marks them with the current space, and fills them by bumping a pointer.

```pseudo id=main
COLLECT(roots)
L1  next ← current + 1
L2  for each root word w do
L3      if w points into a page g with space[g] = current then
L4          space[g] ← next; append every object of g to the scan queue      ▷ promote g in place
L5  for each object o in the scan queue, in order, and each pointer field i of o do
L6      o.f[i] ← COPY(o.f[i])
L7  current ← next; every page whose space is not current is free

COPY(x)
L8  if x is null or the page of x has space[page] = next then return x      ▷ promoted, or a copy
L9  if x has a forwarding address then return it
L10 x' ← a copy of x in a fresh page of space next; give x the forwarding address x'; append x' to the scan queue; return x'
```

Lines L2 to L4 handle the ambiguous roots. A root word that points into a page of the current space promotes the page, whatever object, or part of an object, the word points to. A word that points outside the heap, or into a free page, is ignored. The scan queue starts with all objects of the promoted pages: they are all kept, since any of them could be the target of a root, so their fields must be traced and updated. Lines L5 and L6 are a Cheney scan: COPY copies each object once, leaves objects on promoted pages and copies in place (line L8), and returns the forwarding address of an object that is already copied (line L9). Line L7 frees all pages still in the old space in one step, by changing a number: no page is swept.

## Example

Pages hold 4 words and start at address 100, so page 0 is $[100, 104)$. The objects, with their pointer fields first:

| page | objects |
|---|---|
| 0 | $A$ at 100: $[C, 7]$; $B$ at 102: $[E, 0]$ |
| 1 | $C$ at 104: $[D, 5]$; $F$ at 106: two data words |
| 2 | $D$ at 108: $[\text{null}, 9]$; $E$ at 110: $[3]$, all data |

The roots are the words $100$ (a pointer to $A$) and $3$ (a small integer). The program can reach $A$, $C$ and $D$.

| step | action | effect |
|---|---|---|
| L2 to L4 | 100 points into page 0; 3 is outside the heap | page 0 is promoted; queue: $A$, $B$ |
| scan $A$ | $C$ is on page 1 | copy $C$ to 112 on a new page 3; $A.f_0 \gets 112$ |
| scan $B$ | $E$ is on page 2 | copy $E$ to 114 on page 3; $B.f_0 \gets 114$ |
| scan $C'$ | $D$ is on page 2 | $D$ does not fit on page 3: copy it to 116 on page 4 |
| scan $E'$, $D'$ | no pointers | |
| L7 | | pages 1 and 2 are free; $F$ is gone |

The root word 100 is unchanged and still points to $A$. $B$ is garbage, but it shares a page with $A$, so it is kept, and so is $E$, which $B$ points to. This is the price of promoting whole pages. The tests run this example.

## Correctness

**Claim.** After COLLECT: (1) no object on a promoted page has moved, and no root word has changed; (2) every object that the program can reach from a root word that is a real pointer, by real pointers, is retained; (3) each pointer field of a retained object points to the retained image of its original target, so the graph that the program sees is the same.

**Proof sketch.** (1) Promotion changes only a space number, and line L7 frees only pages whose space is not $next$. Root words are only read. (2) A real pointer root points into the page of its object, which is then in the current space and is promoted at line L4. Each object in the scan queue has its pointer fields processed once at line L6. A target is either on a promoted page or a copy (kept by line L8), or is copied and enqueued at line L10. By induction along a path of pointers, every reachable object is on a promoted page or has a copy that is enqueued, and line L7 keeps both. (3) Line L6 replaces each field with the result of COPY, which is the object itself if it does not move, and its unique copy otherwise: line L9 makes the copy unique. Fields of objects that are not in the queue do not matter, since those objects are freed. The proof file below gives the full argument, and the tests check all three claims against the true pointer graph on random heaps with random noise words in the roots.

## Complexity

Lines L2 to L4 take $O(r)$ time for $r$ root words, with $O(1)$ to find the page of an address. The scan and the copying take time linear in the words of the retained objects, $L$, including the garbage on promoted pages. Freeing the old space is a pass over the page table, $O(N)$, or $O(1)$ if the pages of each space are kept in a list. Space: the page table, and a forwarding address per copied object, which can be stored in the old copy.

## Properties

- **Mostly copying.** Only objects on promoted pages stay; in practice, few pages are promoted, because the stack is small compared with the heap.
- **Conservative for roots only.** The heap must be precise: the collector must know which fields of an object are pointers, so that it can update them.
- **Compacting.** Copied objects are packed into fresh pages, so allocation can bump a pointer.
- **Not incremental.** One collection processes all reachable objects in one pause.

## Variants and improvements

- **Generations.** Bartlett extended the collector with generations in 1989: pages of older spaces are not collected at each collection, and a remembered set covers pointers into the young pages.
- **Conservative heap objects.** Objects whose layout is unknown can also pin their targets: their words are treated as ambiguous, and the pages they point into are promoted.
- **Pinning single objects.** Instead of whole pages, a collector can pin single objects and mark the rest of the page free for reuse, as the [Immix](/immix-collector/) collector does with its lines. This wastes less space but needs a mark structure inside each page.
- **Mostly-copying for multiprocessors.** Later work made the collector concurrent and parallel, again with pages pinned by ambiguous roots.

## When to use it

Use mostly-copying collection when the runtime knows the layout of heap objects but cannot give exact stack maps: a language implementation that compiles to C, an interpreter whose C stack holds object pointers, or a runtime that calls into foreign code. It keeps most of the benefits of copying (compaction, fast allocation) without needing [precise roots](/precise-garbage-collection/). If the heap layout is also unknown, as for plain C programs, use a fully conservative, non-moving collector such as the [Boehm-Demers-Weiser collector](/boehm-gc/).

## Pitfalls

- **False retention by page.** All objects on a promoted page survive, with everything they reach. Large pages and dense stacks retain more garbage.
- **Large objects.** An object that spans several pages must promote all of them together when any is pinned.
- **Root words that point into free pages.** A word that points into a free page, or into a page of another space, must be ignored, or a free page would be resurrected.
- **Hidden pointers in the heap.** The heap must be precise. A pointer kept in a data field is not updated when its target moves.
- **Updating roots by mistake.** Root words must never be written, even when they look like valid pointers: they may be numbers.

## Implementations

## History

Bartlett introduced the collector in a 1988 report of the DEC Western Research Laboratory, for his Scheme-to-C compiler, and called it compacting garbage collection with ambiguous roots. Boehm and Weiser published a fully conservative collector for C the same year. Bartlett added generations in 1989, and the technique was used in several runtimes that compile to C or call C code, and studied further in comparisons of mostly-copying and conservative mark-sweep collection.

## References
