---
tag: MNBT5P
kind: algorithm
slug: mark-and-sweep
name: Mark-and-sweep
aliases:
- mark and sweep
- McCarthy collector
- mark-sweep collection
area: systems/garbage-collection
level: intro
summary: "Mark every cell reachable from the roots, then sweep the whole heap and put each unmarked cell on the free list. Marking costs time in the live data, sweeping in the heap size."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {n: the number of cells in the heap, k: the number of pointer fields in a cell, L: the number of reachable cells, r: the number of roots}
  time: {worst: O(r + k L + n), best: Θ(n)}
  space: {extra: O(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1960
  people: [John McCarthy]
  note: McCarthy described the method for the free-storage list of LISP in 1960. Cells that no register reaches are found by marking the reachable ones and are returned to the free list in one pass over memory.
prereqs: [tracing-garbage-collection, depth-first-search, free-list]
see_also: [lazy-sweeping, schorr-waite-marking, tricolor-marking, mark-compact, copying-collection, reference-counting, gc-space-time-tradeoff, stop-the-world-collection]
sources:
  - paper: doi:10.1145/367177.367199
    title: John McCarthy, Recursive functions of symbolic expressions and their computation by machine, Part I, Communications of the ACM 3(4), 184-195, 1960
    locator: Section 4, the free-storage list and the reclamation of registers that are no longer accessible
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 2, Section 2.1 (the mark-sweep algorithm) and Section 2.7 (issues to consider)
  - book: isbn:9780471941484
    title: Richard Jones and Rafael Lins, Garbage Collection, Algorithms for Automatic Dynamic Memory Management, Wiley, 1996
    locator: Chapter 2 (the classical algorithms) and Chapter 4 (mark-sweep garbage collection)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.3.5, Lists and garbage collection
---

Mark-and-sweep is the first [tracing garbage collector](/tracing-garbage-collection/). When the [free list](/free-list/) is empty, it stops the program, *marks* every cell that the program can still reach from its [roots](/gc-roots/), and then *sweeps* the whole heap: each cell that has no mark is [garbage](/garbage/) and goes back on the free list. McCarthy described it for LISP in 1960. The mark phase costs time in proportion to the live data, and the sweep phase in proportion to the heap size. Cells never move, so it needs no change to the pointers of the program, but the free space can be [fragmented](/external-fragmentation/).

## In plain words

A program keeps its data in small cells that point to each other. Some cells are no longer reachable from anything the program holds, so the program can never use them again. The collector finds them in two steps.

First it marks. It starts from the cells that the program holds directly, puts a mark on each one, and follows every pointer to put a mark on each cell it finds. A cell that is already marked is not visited again, so loops in the data do no harm.

Then it sweeps. It walks over every cell of memory from one end to the other. A marked cell is in use: it loses its mark and stays. A cell with no mark is junk, and it goes on the list of free cells, ready for the next request.

## The problem

**Heap model.** The heap has $n$ cells with the addresses $0$ to $n-1$. Each cell has $k$ pointer fields, and each field holds an address or nil. Each cell also has one mark bit. The free cells form a [free list](/free-list/), linked through field 0. The mutator (the [program](/mutator-and-collector/)) holds its references in a set of root slots. It allocates cells, and it reads and writes the fields of cells that it reaches from the roots.

**Task.** This is the [automatic memory reclamation](/automatic-memory-reclamation/) problem for this model. When ALLOCATE finds the free list empty, find the set $R$ of cells [reachable](/heap-reachability/) from the roots, and put every cell outside $R$ on the free list, without changing a field of any cell in $R$.

**What is measured.** The time of one collection in field visits and cell visits, the extra space (mark bits and the mark stack), and the cells freed by each collection.

## The algorithm

```pseudo id=main
COLLECT(H)                                   ▷ mark, then sweep
L1  W ← an empty stack
L2  for each root r ≠ nil with r unmarked do mark r, push r on W
L3  while W is not empty do
L4      x ← pop W
L5      for each field y of x do
L6          if y ≠ nil and y is unmarked then mark y, push y on W
L7  free ← nil
L8  for a ← n − 1 downto 0 do                ▷ the sweep
L9      if a is marked then clear the mark of a
L10     else clear the fields of a, a.next ← free, free ← a

ALLOCATE(H)
L11 if free = nil then COLLECT(H)
L12 if free = nil then fail: every cell is reachable
L13 a ← free, free ← a.next, clear the fields of a
L14 return a
```

Lines L1 to L6 are a [depth-first search](/depth-first-search/) of the heap graph with an explicit [stack](/stack/). A cell is marked when it is pushed, not when it is popped, so it is pushed at most once even if many fields point to it. Lines L7 to L10 rebuild the free list from nothing: a cell that was already free is unmarked and goes back on the new list, so the old list needs no special case. The sweep runs from the top address down, so the new list is in increasing address order, which helps the locality of the next allocations.

## Example

The heap has $n = 8$ cells with $k = 2$ fields, and all of them are allocated. The roots are $0$ and $5$. The fields are $0 \to (1, 2)$, $1 \to (3, \text{nil})$, $2 \to (1, 0)$, $3 \to (\text{nil}, \text{nil})$, $4 \to (6, 7)$, $5 \to (\text{nil}, 5)$, $6 \to (4, \text{nil})$ and $7 \to (\text{nil}, \text{nil})$. So $0$ and $2$ form a cycle, $5$ points to itself, and $4$ and $6$ form a garbage cycle.

| step | line | popped | marked after the step | stack $W$ (top on the right) |
|---|---|---|---|---|
| 1 | L2 | | 0, 5 | 0, 5 |
| 2 | L4 | 5 | 0, 5 | 0 |
| 3 | L4 | 0 | 0, 1, 2, 5 | 1, 2 |
| 4 | L4 | 2 | 0, 1, 2, 5 | 1 |
| 5 | L4 | 1 | 0, 1, 2, 3, 5 | 3 |
| 6 | L4 | 3 | 0, 1, 2, 3, 5 | empty |

The field $5 \to 5$ in step 2 and the fields $2 \to 1$ and $2 \to 0$ in step 4 find marked cells, so the cycles stop the search. The sweep then visits $7, 6, \ldots, 0$. The cells $7$, $6$ and $4$ have no mark, so the free list becomes $4 \to 6 \to 7$. The marks of $0, 1, 2, 3, 5$ are cleared. The cycle $4 \leftrightarrow 6$ is freed even though each of its cells has a pointer to it, which [reference counting](/reference-counting/) alone cannot do. The mark phase did 5 pops and 10 field visits; the sweep did 8 cell visits.

## Correctness

The mark phase keeps three facts at line L3: every marked cell is reachable; every root is marked; and every marked cell that is not on the stack has all its fields marked. When the stack is empty, the marked set holds the roots and is closed under the fields, so it holds every reachable cell, and with the first fact it is exactly the reachable set. The sweep then puts each unmarked cell on the list one time and touches no field of a marked cell. So after COLLECT the free list holds exactly the unreachable cells, the reachable cells are unchanged, and all marks are clear. The full proof is in the proofs section.

## Complexity

The model is the [word RAM](/word-ram/) with the heap model above.

- **Mark.** Each reachable cell is pushed and popped exactly once, and each pop visits its $k$ fields. Line L2 looks at each of the $r$ roots. So the mark phase takes $\Theta(r + k L)$ time, where $L$ is the number of reachable cells. Unreachable cells are never visited.
- **Sweep.** Lines L8 to L10 visit all $n$ cells, with $O(1)$ work each (or $O(k)$ to clear the fields), so $\Theta(n)$.
- **One collection.** $O(r + kL + n)$ in the worst case and $\Omega(n)$ in every case.
- **Space.** One mark bit for each cell, and a stack of at most $L$ entries. Recursive marking would use the program stack instead, and can overflow it on a long list; [Schorr-Waite marking](/schorr-waite-marking/) removes the stack.
- **Cost per allocation.** One collection frees $n - L$ cells, so the next $n - L$ allocations take $O(1)$ time each. The collection cost spread over them is $(c_m L + c_s n) / (n - L)$ for constants $c_m$ and $c_s$. This grows without bound as $L$ comes near $n$, and it never falls below $c_s$, because of the sweep term. The page [GC space-time tradeoff](/gc-space-time-tradeoff/) derives this cost exactly and compares it with copying collection.

## Properties

- **Non-moving.** Cells keep their addresses, so the collector can work with pointers it cannot update, as in [conservative collection](/conservative-garbage-collection/).
- **Complete for cycles.** A garbage cycle is never reached from a root, so it is freed.
- **Stop-the-world.** In this form the mutator waits for the full collection; see [stop-the-world collection](/stop-the-world-collection/). The pause is $\Theta(r + kL + n)$.
- **Fragmenting.** Free cells are scattered over the heap. With cells of one size this does no harm. With objects of many sizes the free space can be cut into pieces too small for a request; [mark-compact](/mark-compact/) collectors fix this.

## Variants and improvements

- **Lazy sweeping.** Sweep a block at a time inside ALLOCATE, and not in the pause. See [lazy sweeping](/lazy-sweeping/).
- **Bitmap marking.** Keep the mark bits in a side table, so marking does not write to the objects and the sweep can skip whole words of the table.
- **Pointer reversal.** [Schorr-Waite marking](/schorr-waite-marking/) marks with $O(1)$ extra space by storing the return path in the fields of the cells.
- **Incremental and concurrent marking.** Mark in small steps that interleave with the mutator, with the [tricolor](/tricolor-marking/) invariant and a barrier. See [incremental garbage collection](/incremental-garbage-collection/).
- **Conservative marking.** Treat each word that looks like an address as a pointer. The [Boehm collector](/boehm-gc/) is a mark-sweep collector of this kind.

## When to use it

Use mark-and-sweep when objects must not move (C and C++ heaps, objects whose addresses are passed to foreign code) or when memory is too tight for the half-empty heap of [copying collection](/copying-collection/). Prefer copying when most objects die young and the live data is small, since copying does not touch dead objects at all. Prefer [reference counting](/reference-counting/) when memory must be freed at once, as soon as the last pointer goes, and add [cycle collection](/cycle-collection/) for the cycles.

## Pitfalls

- **Marking when popped.** If line L6 pushes $y$ without marking it and the mark is set only when $y$ is popped, a cell with many incoming fields is pushed many times, and the stack can grow to the number of fields, not of cells. Mark at the push, as in lines L2 and L6.
- **Forgetting to clear marks.** If line L9 does not clear the mark, the next collection sees every cell of this one as marked and frees nothing, or frees too little. Clear the mark in the sweep, or flip the meaning of the bit at each collection.
- **Recursion.** A recursive MARK on a long linked list overflows the stack. Use the explicit stack of line L1, or pointer reversal.
- **Hidden roots.** A pointer held only in a machine register or in a local variable that the collector does not scan makes a live cell look like garbage. The set of [roots](/gc-roots/) must be complete.

## Implementations

## History

McCarthy described the method in his 1960 paper on LISP. When the free-storage list ran out, the system marked the registers that it could reach from the base registers of the program, and a pass through memory returned the unmarked ones to the free list. In the same year Collins described [reference counting](/reference-counting/) as the alternative. Section 2.3.5 of Knuth's Volume 1 gives several marking algorithms, among them one with link inversion, which is [Schorr-Waite marking](/schorr-waite-marking/).

## References
