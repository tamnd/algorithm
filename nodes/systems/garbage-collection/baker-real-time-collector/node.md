---
tag: DE61E5
kind: algorithm
slug: baker-real-time-collector
name: Baker's real-time collector
aliases:
- Baker copying collector
- Baker's incremental copying collector
- Baker read barrier
area: systems/garbage-collection
level: advanced
summary: "An incremental semispace copying collector. A read barrier keeps the mutator in to-space, and each allocation scans k cells, so the scan ends before to-space fills."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {S: the number of cells in one semispace (the time bounds are per mutator operation), L: the most cells reachable at any moment, k: the cells scanned per allocation, p: the number of pointer fields in a cell, r: the number of roots}
  time: {worst: O(k p^2 + r p), best: Θ(1)}
  space: {extra: O(S)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1978
  people: [Henry G. Baker Jr.]
  note: Baker made Cheney's copying collector incremental. A read barrier moves each from-space cell that the program touches, every CONS does a fixed amount of scanning, and new cells go to the top of to-space. Brooks (1984) replaced the test in the barrier with an indirection word.
prereqs: [cheney-copying-collector, incremental-garbage-collection, read-barrier]
see_also: [copying-collection, tricolor-marking, incremental-update-barrier, snapshot-at-the-beginning, shenandoah-collector, c4-collector, z-garbage-collector, train-algorithm]
sources:
  - paper: doi:10.1145/359460.359470
    title: "Henry G. Baker Jr., List processing in real time on a serial computer, Communications of the ACM 21(4), 280-294, 1978"
    locator: The incremental copying collector for list cells, with the CAR and CDR barrier, k scan steps at each CONS, and new cells at the top of to-space
  - paper: doi:10.1145/800055.802042
    title: "Rodney A. Brooks, Trading data space for reduced time and code space in real-time garbage collection on stock hardware, ACM Symposium on LISP and Functional Programming, 256-262, 1984"
    locator: The indirection word in each object that replaces the conditional read barrier
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 17 (concurrent copying and compaction, Baker's algorithm and the Brooks indirection barrier)
  - paper: doi:10.1007/BFb0017182
    title: "Paul R. Wilson, Uniprocessor garbage collection techniques, International Workshop on Memory Management (IWMM 1992), LNCS 637, 1-42"
    locator: Section 3 (incremental tracing collectors, Baker's incremental copying)
---

Baker's real-time collector is the incremental form of [Cheney's copying collector](/cheney-copying-collector/). The heap has two semispaces. At a *flip* the roles of the spaces swap and the roots are copied to the new to-space. After that, the program and the collector share the time: each allocation first scans $k$ gray cells of to-space, and a [read barrier](/read-barrier/) copies each from-space cell that the program is about to load. So the program only ever holds to-space addresses, the *to-space invariant*. New cells are put at the top of to-space and count as black. Baker published the method in 1978 for LISP list cells. If $k$ is chosen from a bound $L$ on the live data, the scan ends before to-space fills, so each pause is bounded and no allocation fails.

## In plain words

Memory has two halves. The program uses one half. When that half is full, the collector starts to move the data that is still in use into the other half, and the old half is then free again.

A simple copying collector moves all the data in one long stop. Baker's collector moves only the data that the program points to at once, and then moves the rest a little at a time. Each time the program asks for new memory, the collector first moves a few more items.

The program can still try to read an item that has not moved yet. A small check on each read catches this: it moves the item first and gives the program the new place. So the program never sees the old half. If the collector moves enough items per request, it finishes before the new half is full.

## The problem

**Heap model.** Two semispaces of $S$ cells each. A cell has $p$ pointer fields, each holding an address or nil. The mutator holds $r$ root registers and runs four kinds of operation: load a field of a held cell into a register, store a register into a field of a held cell, clear or copy a register, and allocate a cell. At every moment at most $L$ cells are [reachable](/heap-reachability/) from the registers.

**Goal.** Reclaim the unreachable cells while the mutator runs, so that each mutator operation waits for at most a constant amount of collector work, and no allocation fails while at most $L$ cells are live. The collector must keep the mutator's view of the heap: the graph of cells reachable from the registers, with cells named by identity and not by address, must be the same as with no collector.

## The algorithm

To-space is the range $[\textit{base}, \textit{base} + S)$. Copied cells grow up from the bottom: the cells below *scan* are scanned (black), and the cells in $[\textit{scan}, \textit{copy})$ are copied but not yet scanned (gray). New cells grow down from *top*; the cells at or above *top* are black too. To-space is full when $\textit{copy} = \textit{top}$. A from-space cell that has been copied holds a forwarding address.

```pseudo id=main
FLIP()
L1  swap the semispaces; scan ← copy ← base; top ← base + S
L2  for each root register r do r ← EVACUATE(r)

EVACUATE(a)                                ▷ return the to-space copy of a
L3  if a = nil or a is in to-space then return a
L4  if a has a forwarding address then return it
L5  b ← copy; copy ← copy + 1; copy the fields of a into b
L6  set the forwarding address of a to b
L7  return b

LOAD(x, f)                                 ▷ the read barrier; x is in to-space
L8  y ← EVACUATE(x.f); x.f ← y; return y

SCAN(k)
L9  while fewer than k cells are scanned and scan < copy do
L10     for each field f of scan do scan.f ← EVACUATE(scan.f)
L11     scan ← scan + 1

ALLOCATE()
L12 if copy = top then                     ▷ to-space is full
L13     if scan < copy then fail           ▷ the collector fell behind
L14     FLIP()
L15 SCAN(k)                                ▷ the tax
L16 if copy = top then fail
L17 top ← top − 1; clear the fields of top
L18 return top                             ▷ above top, so black
```

A store needs no barrier. The value stored comes from a register, so by the to-space invariant it is a to-space address, and the store cannot hide a from-space cell from the collector. Line L8 writes the new address back into the field, so a second load of the same field does not need the forwarding address.

In the terms of [tricolor marking](/tricolor-marking/), from-space cells that are not copied are white, gray cells are $[\textit{scan}, \textit{copy})$, and all other to-space cells are black. The mutator holds only black or gray cells and stores only such addresses, so it never writes a white pointer anywhere. That is a stronger invariant than either barrier family of mark-and-sweep needs.

## Example

One semispace has $S = 8$ cells with $p = 2$ fields, and $k = 1$. The first to-space is $[0, 8)$. The mutator allocates $a = 7$ and $b = 6$, keeps $a$ in register 0, and sets $a.f_0 = b$ and $b.f_1 = a$, a cycle. It then allocates six cells $5, \ldots, 0$ that it drops at once. Now $\textit{copy} = \textit{top} = 0$ and to-space is full; $\textit{scan} = \textit{copy}$, so no gray cell remains.

| step | line | event | scan, copy, top | forwarding |
|---|---|---|---|---|
| 1 | L12, L14 | the next allocation finds to-space full and flips; to-space is $[8, 16)$ | 8, 8, 16 | |
| 2 | L2 | register 0 holds 7; EVACUATE copies $a$ to 8 | 8, 9, 16 | 7 → 8 |
| 3 | L15, L10 | SCAN(1) scans 8: field $f_0 = 6$ is copied to 9 | 9, 10, 16 | 7 → 8, 6 → 9 |
| 4 | L17 | the new cell is 15, black | 9, 10, 15 | |
| 5 | L8 | the mutator loads $b = 8.f_0 = 9$, then $9.f_1$: it is 7, which forwards to 8 | 9, 10, 15 | |

After step 5, cell 9 holds $(\text{nil}, 8)$. The next allocation scans 9, finds only to-space addresses, and the scan has ended: $\textit{scan} = \textit{copy} = 10$. The six dropped cells were never touched. The cycle $a \leftrightarrow b$ is kept with the same shape at new addresses.

## Correctness

The proof in the proofs section has four steps.

1. **To-space invariant.** Registers hold only to-space addresses. Line L2 evacuates the roots at the flip, LOAD returns an evacuated address, and ALLOCATE returns a to-space cell.
2. **Only gray cells hold from-space addresses.** A scanned cell has all fields evacuated, a new cell starts with nil fields, and stores write only to-space values. From-space cells are never written after the flip.
3. **The view is kept.** Each from-space cell is copied at most once (line L4), its copy gets the same fields, and every later use of the old address is mapped to the copy. So the graph that the mutator reaches is unchanged, cell by cell.
4. **At most $L$ copies per cycle.** A from-space cell is copied only if a root or a gray cell points to it, and by the second step those pointers are fields as they were at the flip. So every copied cell was reachable at the flip, and there are at most $L$.

When $\textit{scan} = \textit{copy}$, no cell that the mutator can reach is in from-space, so the next flip may reuse it.

**Theorem (the pacing bound).** If $S \ge L + \lceil L/k \rceil$, no allocation fails, and no evacuation finds to-space full.

The reason is a count. Let $c \le L$ be the number of cells copied in a cycle. Each allocation that leaves gray cells behind has scanned $k$ cells, so the scan ends within the first $\lceil c/k \rceil \le \lceil L/k \rceil$ allocations after the flip. Up to then, to-space holds at most $L$ copies and at most $\lceil L/k \rceil$ new cells, which fits. Once no gray cell remains, no from-space address is reachable, so nothing more is copied in this cycle, and line L13 cannot fail at the next flip.

## Complexity

The model is the [word RAM](/word-ram/) with the heap model above.

- **Allocation.** At most $k$ cells scanned, each with $p$ evacuations, and each evacuation copies at most $p$ words, so $O(k p^2)$ word operations. At a flip there is also a pause of $r$ evacuations for the roots.
- **Load.** A test of the address, and at most one copy of $p$ words. A load of a to-space address costs $O(1)$; this is the common case, but the test runs on every load.
- **Store.** $O(1)$, with no barrier.
- **Total work.** A cycle copies and scans at most $L$ cells, as in a stop-the-world semispace collector. Dead cells cost nothing.
- **Space.** $2S$ cells with $S \ge L + \lceil L/k \rceil$. A larger $k$ shrinks the heap toward $2L$; $k = 1$ needs $S = 2L$, so a heap of $4L$.

## Properties

- **Bounded pauses.** Each operation does a bounded amount of collector work, which is why Baker called it real time. The bound counts work, not time; see the pitfalls.
- **Moving and compacting.** Survivors are packed at the bottom of to-space, so there is no fragmentation and allocation is a pointer decrement.
- **No write barrier.** The read barrier carries the whole invariant.
- **Floating garbage.** A cell that is copied or allocated in a cycle stays until the next flip, even if it dies before then. A from-space cell whose last pointer is overwritten in a gray cell before the scan reaches it is not copied at all.
- **Incremental, not concurrent.** One processor runs both parts. A barrier and its copy are one step for the collector.

## Variants and improvements

- **Brooks indirection.** Brooks (1984) gave every object an extra word that points to the current copy: to itself, or to its to-space copy. Every access goes through this word with no test. In this form the mutator may hold from-space addresses, and writes must go to the to-space copy. The [Shenandoah collector](/shenandoah-collector/) first used this layout.
- **Page-protection barrier.** Appel, Ellis and Li (1988) protected the unscanned pages of to-space with virtual memory, so the trap of the first access scans a whole page. The barrier then costs nothing in the common case, but the pause of a trap is a page of work.
- **Non-copying form.** Baker's Treadmill (1992) keeps the same colors as four segments of a doubly linked list and moves cells between lists, not between spaces.
- **Concurrent copying.** Modern collectors such as [C4](/c4-collector/), [Shenandoah](/shenandoah-collector/) and [ZGC](/z-garbage-collector/) keep a to-space invariant for the mutator with a load barrier, but the collector runs on its own threads and races with the mutator for each copy.

## When to use it

Use it when each operation of the program must have a bounded delay, there is one processor, and twice the live data plus a margin fits in memory. It suits LISP-like systems with small cells of one size. Prefer [incremental mark-and-sweep](/incremental-garbage-collection/) with a write barrier when loads are much more frequent than stores, when memory is tight, or when objects must not move. Prefer a [stop-the-world](/stop-the-world-collection/) [copying collector](/copying-collection/) when throughput matters more than pauses.

## Pitfalls

- **A tax that is too small.** If $k$ is smaller than the bound needs for the actual live data, to-space fills while gray cells remain, and the collector must stop the program to finish the scan or fail. A queue of 16 live cells with $S = 24$ runs with $k = 2$ but fails in its first cycle with $k = 1$.
- **The cost of every load.** The barrier tests every pointer load. Without hardware help, this costs much more throughput than a write barrier, since loads are more common than stores.
- **Large objects.** Copying a large object in the barrier is a long pause. Copy large objects lazily, or keep them in a separate space that is not copied.
- **The root pause.** The flip copies all roots at once. A deep stack makes this pause long; scan the stack incrementally too.
- **Pointer comparison with Brooks indirection.** If the mutator can hold both a from-space and a to-space address of one object, an equality test must compare the forwarded addresses.

## Implementations

## History

Minsky (1963) and Fenichel and Yochelson (1969) gave copying collectors, and Cheney (1970) made the copy breadth-first with no stack. Baker's paper of 1978 made the copy incremental for a LISP system on a serial computer. It also treated vectors and the stack. Lieberman and Hewitt (1983) built a generational collector on the same mechanism. Brooks (1984) reduced the barrier cost with the indirection word, and Appel, Ellis and Li (1988) moved the barrier into the virtual-memory hardware. The to-space invariant returned in the concurrent compacting collectors of the 2000s and 2010s.

## References
