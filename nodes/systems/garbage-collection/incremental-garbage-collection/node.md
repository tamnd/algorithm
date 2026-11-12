---
tag: RV18E3
kind: technique
slug: incremental-garbage-collection
name: Incremental garbage collection
aliases:
- incremental GC
- incremental collector
- incremental tracing collection
area: systems/garbage-collection
level: advanced
summary: "Interleave small slices of collector work with the mutator, for example k units of work per allocation, so that each pause is bounded and the cycle ends before memory runs out."
history:
  year: 1975
  people: [Guy L. Steele Jr., Edsger W. Dijkstra, Henry G. Baker]
  note: Steele (1975) and Dijkstra et al. (1978) gave collectors that mark while the program runs. Baker (1978) bounded the work of each step by doing k units of copying per allocation. Yuasa (1990) did the same for mark-and-sweep with a deletion barrier.
prereqs: [tracing-garbage-collection, tricolor-marking, mutator-and-collector, stop-the-world-collection]
see_also: [incremental-update-barrier, snapshot-at-the-beginning, baker-real-time-collector, concurrent-garbage-collection, on-the-fly-garbage-collection, lazy-sweeping, read-barrier, train-algorithm]
sources:
  - paper: doi:10.1145/359460.359470
    title: "Henry G. Baker Jr., List processing in real time on a serial computer, Communications of the ACM 21(4), 280-294, 1978"
    locator: The incremental collector that does k units of scanning at each CONS, and the choice of k from the size of the semispaces
  - paper: doi:10.1016/0164-1212(90)90084-Y
    title: "Taiichi Yuasa, Real-time garbage collection on general-purpose machines, Journal of Systems and Software 11(3), 181-198, 1990"
    locator: Incremental mark-and-sweep with a fixed amount of marking and sweeping at each allocation
  - paper: doi:10.1007/BFb0017182
    title: "Paul R. Wilson, Uniprocessor garbage collection techniques, International Workshop on Memory Management (IWMM 1992), LNCS 637, 1-42"
    locator: Section 3 (incremental tracing collectors, the coherence problem and the barrier families)
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 15 (concurrent and incremental collection, correctness and barriers) and Chapter 19 (real-time garbage collection, work-based scheduling)
  - paper: doi:10.1145/604131.604155
    title: "David F. Bacon, Perry Cheng and V. T. Rajan, A real-time garbage collector with low overhead and consistent utilization, POPL 2003, 285-298"
    locator: Time-based scheduling of collector slices and minimum mutator utilization
---

Incremental garbage collection splits one collection cycle into many small slices of work and runs them between the operations of the [mutator](/mutator-and-collector/), instead of in one [stop-the-world](/stop-the-world-collection/) pause. The usual pacing rule is a *tax* on allocation: each allocation first does $k$ units of collector work. A [barrier](/write-barrier/) keeps the [tricolor invariant](/tricolor-marking/) while the mutator changes the heap between slices, so no reachable object is freed. The two design questions are how to keep the collector correct while the heap changes, and how to choose $k$ so that each pause is short and the cycle still ends before the free memory runs out.

## In plain words

A simple collector stops the program, cleans the whole memory, and then lets the program go on. On a large memory this pause can be long.

An incremental collector cleans a little at a time. Each time the program asks for new memory, the collector first does a small fixed amount of cleaning. So no single request waits long.

Two problems follow. First, the program changes its data between the small steps, and the collector must not miss data that the program moved. A small check on each pointer write, called a barrier, tells the collector about such moves. Second, the collector must finish its round before the program uses up the free memory. If it does too little work per request, it falls behind. The amount of work per request must be large enough for the amount of live data and the size of memory.

## When it applies

**Heap model.** The heap has $H$ cells with $p$ pointer fields each. The mutator holds $r$ root registers and runs loads, stores, register clears and allocations. At every moment at most $L$ cells are [reachable](/heap-reachability/). Time is counted in *units* of collector work: one unit scans one gray cell, or sweeps one cell.

**What is measured.** The pause: the largest amount of collector work done between two mutator operations. The tax $k$: the collector work per allocation. The space: the heap size $H$ that is needed for a given $L$ and $k$ so that no allocation finds the heap full. Also the barrier cost per operation and the floating garbage.

Use it when the pause of a stop-the-world collection is too long for the application and there is one processor for both the program and the collector, or when the collector must not depend on spare processors. If spare processors exist, a [concurrent collector](/concurrent-garbage-collection/) runs the slices on another thread instead. The two share the barriers and the invariants; they differ in what is atomic. In an incremental collector a mutator operation and its barrier are one step for the collector, so the order of the instructions inside a barrier does not matter. In a concurrent collector it does.

## The template

This is an incremental mark-and-sweep collector with a [snapshot-at-the-beginning](/snapshot-at-the-beginning/) barrier and an allocation tax, in the style of Yuasa (1990). The phases are idle, mark and sweep; $W$ is the gray stack and $s$ the sweep pointer.

```pseudo id=main
ALLOCATE()
L1  if phase = idle and |free| ≤ F then BEGIN-CYCLE()
L2  if phase ≠ idle then COLLECT-WORK(k)          ▷ the tax
L3  if free is empty then fail
L4  x ← pop free, clear the fields of x
L5  if phase = mark, or phase = sweep and x ≥ s, then
L6      mark x                                    ▷ allocate black; return x

BEGIN-CYCLE()                                     ▷ a pause of r steps
L7  for each root r do SHADE(r); phase ← mark

COLLECT-WORK(k)
L8  u ← 0
L9  while u < k and phase ≠ idle do
L10     if phase = mark and W is not empty then
L11         x ← pop W, SHADE each field of x, u ← u + 1
L12     else if phase = mark then phase ← sweep, s ← 0
L13     else if s < H then
L14         if s is marked then clear the mark of s
L15         else if s is not free then push s on free
L16         s ← s + 1, u ← u + 1
L17     else phase ← idle

WRITE(x, f, y)                                    ▷ the deletion barrier
L18 if phase = mark then SHADE(x.f)
L19 x.f ← y
```

SHADE$(y)$ sets the mark of a non-nil unmarked $y$ and pushes it on $W$. Lines L5 and L6 allocate black: a cell allocated during marking is marked, and a cell allocated during the sweep is marked only if the sweep has not yet passed it, so that the sweep keeps it and clears its mark.

### Why it is correct

The barrier at line L18 is the deletion barrier of [snapshot-at-the-beginning](/snapshot-at-the-beginning/), so every cell that is reachable when line L7 runs, and every cell allocated after it, is marked when $W$ empties. The sweep frees only unmarked cells, and those were garbage at line L7, so they are garbage forever. The [incremental update barrier](/incremental-update-barrier/) is the other choice; it needs a final rescan of the roots.

### The pacing theorem

**Theorem.** Let $m = \lceil (L + H)/k \rceil$. If the heap starts empty, the trigger is $F \ge m$, and $H \ge L + 2m$, then no allocation finds the free list empty, and each allocation does at most $k$ units of collector work.

The reason is a count. One cycle does at most $L$ scans (only cells that were reachable at the start are pushed) and $H$ sweep steps, so it ends within $m$ allocations. The cycle starts with at least $m$ free cells, so these allocations succeed. At its end, the cells in use are those that were live at the start (at most $L$) and those allocated in the cycle (at most $m$), so at least $H - L - m \ge m$ cells are free for the next cycle. The full proof is in the proofs section.

Solved for $k$, the condition is about $k \ge 2(L + H)/(H - L)$. When the heap is twice the live data, $H = 2L$, this is $k \ge 6$; the tax falls toward 2 as the heap grows, and grows without bound as $H$ comes near $L$.

### Cost

- **Pause.** At most $k$ units per allocation, plus one pause of $r$ steps to shade the roots at the start of a cycle. Both are independent of $H$ and $L$.
- **Total work.** At most $L + H$ units per cycle, the same as a stop-the-world mark-and-sweep. The incremental collector adds the barrier, $O(1)$ per pointer store during marking, and the flag test of line L18 at other times.
- **Space.** The heap must hold $L$ live cells plus room for $2m$ more, against about $L$ plus a margin for a stop-the-world collector. The floating garbage is the price of the snapshot.

## Classic examples

**A queue at the limit.** $H = 48$ cells and $L = 16$. The mutator is a FIFO queue of 16 cells: each step allocates a cell at the tail and drops the head, so each allocation makes one cell garbage. With $k = 4$, $m = \lceil 64/4 \rceil = 16$ and $L + 2m = 48 = H$, so the theorem applies with the trigger $F = 16$. A run of 3000 allocations completes 175 cycles, and no allocation does more than 4 units. With $k = 3$ ($m = 22$) the condition fails, yet this workload still runs, since the sweep returns cells during the cycle. With $k = 2$ ($m = 32$) the collector falls behind and an allocation finds the free list empty in the second cycle.

**Random mutators.** With $H = 64$, $L = 16$ and $k = 4$ ($m = 20$, $L + 2m = 56 \le 64$), six seeded random mutators of 3000 steps each never find the heap full, and no reachable cell is ever on the free list.

**Systems.**

- [Baker's real-time collector](/baker-real-time-collector/) is the incremental form of [copying collection](/copying-collection/), with a [read barrier](/read-barrier/) and $k$ units of copying per allocation.
- Yuasa's collector is incremental mark-and-sweep with a deletion barrier, as in the template.
- The [train algorithm](/train-algorithm/) bounds the pauses for the old generation by collecting one car at a time.
- Many interpreters, such as Lua since version 5.1, use an incremental mark-and-sweep with a step size that the program can tune.

## Variations

- **Time-based pacing.** Instead of $k$ units per allocation, run the collector for a fixed slice of time in each period. Bacon, Cheng and Rajan's Metronome collector does this to give a minimum mutator utilization in each time window.
- **Lazy sweeping only.** Do the mark in one pause and the sweep incrementally, inside the allocator. See [lazy sweeping](/lazy-sweeping/).
- **Incremental update.** Use the [incremental update barrier](/incremental-update-barrier/), allocate white, and end each cycle with a rescan of the roots. This frees more garbage per cycle but has a final pause with no constant bound.
- **Incremental copying.** Move objects in small steps. The mutator may then see an object in two places, which needs a [read barrier](/read-barrier/) or a forwarding pointer; see [Baker's collector](/baker-real-time-collector/).
- **Generational.** Collect a small young generation in short pauses, and the old generation incrementally; see [generational garbage collection](/generational-garbage-collection/).

## Pitfalls

- **A tax that is too small.** If $k$ is below what the live data and the heap need, the collector falls behind and must finish the cycle in one long pause, or fail. The queue example shows it with $k = 2$.
- **Live data above the bound.** The tax is computed from $L$. If the program keeps more live data than $L$, the guarantee is gone. A real system must measure the live data and raise $k$.
- **Work that is not counted.** Large objects, long arrays and root sets of variable size make one unit of work unbounded. Split the scan of a large object into pieces, and bound the roots.
- **Forgetting the barrier on some stores.** A store done by the runtime (array copy, object clone, reflection) must use the barrier too.
- **Allocating white with a snapshot barrier.** A cell allocated white during marking has no snapshot path, and the sweep frees it while it is in use.
- **Ignoring the barrier cost.** The barrier runs on every pointer store; it costs throughput even when the pauses are short.

## Exercises

1. Find the smallest integer tax that meets the theorem for $L = 16$ and $H = 32$, and for $L = 16$ and $H = 128$.
2. Change the template to allocate white during marking and add a final rescan of the roots. Where does the pacing proof break?
3. Show that if the sweep is not counted (the cells are freed in one step at the end), the work per cycle is at most $L$ and the condition becomes $H \ge L + 2 \lceil L/k \rceil$. What does the pause become?
4. Find the largest pause of the template when one cell has $p$ fields and $p$ is not bounded, and change the unit of work so the pause is bounded again.

## References
