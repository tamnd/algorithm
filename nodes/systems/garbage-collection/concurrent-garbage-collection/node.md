---
tag: 0GJMF8
kind: technique
slug: concurrent-garbage-collection
name: Concurrent garbage collection
aliases:
- concurrent GC
- mostly concurrent collection
- mostly concurrent mark-sweep
area: systems/garbage-collection
level: advanced
summary: "Run marking or sweeping on collector threads while the mutator runs. A barrier records changes, and a short remark pause rescans what changed before memory is freed."
history:
  year: 1978
  people: [Edsger W. Dijkstra, Hans-J. Boehm, Alan J. Demers, Scott Shenker, Tony Printezis, David Detlefs]
  note: Dijkstra et al. (1978) gave the first collector proved correct while it runs at the same time as the program. Boehm, Demers and Shenker (1991) made marking mostly concurrent with dirty pages and a short final pause. Printezis and Detlefs (2000) used the card table and added concurrent precleaning; this became the CMS collector of the HotSpot JVM.
prereqs: [incremental-garbage-collection, tricolor-marking, write-barrier, card-marking]
see_also: [incremental-update-barrier, snapshot-at-the-beginning, on-the-fly-garbage-collection, parallel-garbage-collection, garbage-first-collector, shenandoah-collector, z-garbage-collector, c4-collector]
sources:
  - paper: doi:10.1145/113445.113459
    title: "Hans-J. Boehm, Alan J. Demers and Scott Shenker, Mostly parallel garbage collection, PLDI 1991, 157-164"
    locator: Concurrent marking, then a stop-the-world remark from the roots and the pages that the virtual-memory hardware marked dirty
  - paper: doi:10.1145/362422.362480
    title: "Tony Printezis and David Detlefs, A generational mostly-concurrent garbage collector, ISMM 2000, 143-154"
    locator: The phases initial mark, concurrent marking, concurrent precleaning, remark and concurrent sweeping, with the card table as the record of changes
  - paper: doi:10.1145/359642.359655
    title: "Edsger W. Dijkstra, Leslie Lamport, A. J. Martin, C. S. Scholten and E. F. M. Steffens, On-the-fly garbage collection, an exercise in cooperation, Communications of the ACM 21(11), 966-975, 1978"
    locator: The collector that marks and appends to the free list while the mutator runs, and its correctness argument
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 15 (concurrent garbage collection, correctness and barriers) and Chapter 16 (concurrent mark-sweep)
---

A concurrent garbage collector does its work on its own threads while the threads of the program, the [mutator](/mutator-and-collector/), keep running. The collector and the mutator touch the same heap at the same time, so the collector must learn about the pointer changes that the mutator makes behind it. A [write barrier](/write-barrier/) records them, and the collector keeps a [tricolor invariant](/tricolor-marking/) with this record. Most production collectors are *mostly* concurrent: they do the bulk of the marking concurrently and stop the mutator for two short pauses, one to mark the roots at the start and one to *remark*, to finish the marking with the changes that the barrier recorded. The sweep then runs concurrently again.

## In plain words

A simple collector stops the program while it cleans memory. A concurrent collector cleans on another processor while the program keeps working.

The difficulty is that the program changes its data while the collector looks at it. The collector could check an item, and then the program could hide an item that is still in use behind the checked one. The collector would then think the hidden item is not used, and free it.

So each time the program changes a pointer, a small piece of code marks the changed area as dirty. At the end, the collector stops the program for a short time and checks the dirty areas again. The collector can also check most dirty areas before this stop, so the stop is shorter.

## When it applies

**Heap model.** The heap has $H$ cells with $p$ pointer fields each, grouped into *cards* of $C$ consecutive cells. The mutator holds $r$ root registers and runs loads, stores, register clears and allocations, with at most $L$ reachable cells at a time. The collector runs on another processor. We model this as an interleaving: at each tick one mutator operation or one collector step happens. A mutator operation together with its barrier is atomic, and a collector step (scan one cell, clean one card, sweep one cell) is atomic. Two steps are pauses, in which the mutator does not run.

**What is measured.** The length of the pauses, the throughput lost to the barrier and to the collector threads, the floating garbage, and how often the collector falls behind.

Use it when the pauses of a [stop-the-world](/stop-the-world-collection/) collector are too long and the machine has processor time to spare for the collector. It differs from [incremental collection](/incremental-garbage-collection/) in two ways. The collector needs no allocation tax, since it has its own processor; instead it must start early enough to finish before memory runs out. And a barrier is no longer atomic with respect to the collector: the order of the instructions inside the barrier, and the memory order between processors, now matter.

## The template

The template is mostly concurrent mark-sweep, as in Printezis and Detlefs (2000). The phases are idle, mark, preclean and sweep. $W$ is the gray stack, and each card has a dirty bit. SHADE$(y)$ marks a non-nil unmarked $y$ and pushes it on $W$.

```pseudo id=main
INITIAL-MARK()                                      ▷ pause
L1  clean every card; for each root r do SHADE(r); phase ← mark

MARK-STEP()                                         ▷ concurrent, while W is not empty
L2  x ← pop W
L3  for each field f of x do SHADE(x.f)

PRECLEAN-STEP(c)                                    ▷ concurrent, card c is dirty
L4  clean c
L5  for each marked cell x on c do for each field f of x do SHADE(x.f)

REMARK()                                            ▷ pause
L6  for each root r do SHADE(r)
L7  for each dirty card c do clean c and rescan its marked cells as in L5
L8  while W is not empty do MARK-STEP()
L9  phase ← sweep; s ← 0

SWEEP-STEP()                                        ▷ concurrent
L10 if s is marked then clear the mark of s
L11 else if s is not free then put s on the free list
L12 s ← s + 1; if s = H then phase ← idle

WRITE(x, f, y)
L13 x.f ← y
L14 dirty the card of x

ALLOCATE()
L15 if the free list is empty then finish the cycle in a pause   ▷ concurrent mode failure
L16 x ← pop the free list; mark x if phase is mark or preclean, or phase is sweep and x ≥ s
```

The collector runs MARK-STEP until $W$ is empty, then PRECLEAN-STEP on dirty cards for a while, then REMARK. A new cycle starts with INITIAL-MARK when the free list falls to a trigger $F$.

### Why it is correct

This is the [incremental update](/incremental-update-barrier/) scheme of Steele, at the size of a card. When MARK-STEP scans a cell $x$, $x$ has no white child. A white child can appear in $x$ later only by a store into $x$, and line L14 then dirties the card of $x$. So at every moment, each black cell with a white child lies on a dirty card. Line L4 cleans a card before line L5 rescans it, so a store that comes during the rescan dirties the card again. At the remark the mutator is stopped: line L6 shades the roots, line L7 removes every black-to-white edge, and line L8 closes the marked set under the fields. So every cell reachable at the remark is marked. Cells allocated during marking are marked by line L16. The sweep frees only unmarked cells, which were unreachable at the remark and stay unreachable. The full proof is in the proofs section.

### Cost

- **Pauses.** The initial mark costs $r$ steps. The remark costs $r$ steps, plus a rescan of the marked cells on dirty cards, plus the marking that this rescan causes. Precleaning moves most of this work out of the pause, but the remark has no constant bound: a mutator that writes fast can dirty many cards just before it.
- **Barrier.** $O(1)$ per pointer store: one store into the card table. It is the same barrier that a [generational collector](/generational-garbage-collection/) already uses, which is why the card table is a natural choice.
- **Total work.** The marking of an atomic collector, plus the rescans of dirty cards.
- **Space.** One mark bit per cell, one bit or byte per card, and the floating garbage: cells allocated in the cycle, and cells that die after they were marked, stay until the next cycle.

## Classic examples

**The lost object.** The register $r_0$ holds $A$, and $A.f_0 = B$, $B.f_0 = Z$. The mutator copies $Z$ into $A.f_1$, clears $B.f_0$, and drops its register copies of $B$ and $Z$. If the collector has scanned $A$ but not $B$, nothing points to $Z$ from a gray cell any more. Over all 4978 interleavings of this program with one cycle of the template without line L14, 18 free $Z$ while it is reachable. With line L14, none of 7147 interleavings does (with precleaning; 4978 without it).

**Precleaning.** A random mutator with 16 live cells on a heap of 48 cells, cards of 4 cells and 4 registers, runs for 3000 ticks with the collector on half the ticks, over 20 seeds. Without precleaning, the 297 remark pauses do 1984 units of work, at most 12 in one pause. With precleaning, the 296 remark pauses do 1184 units: each pause only shades the 4 roots.

**A slow collector.** With the collector on only 15 percent of the ticks, the same runs hit 483 concurrent mode failures. Each one finishes the cycle in a pause. No run frees a reachable cell.

**Systems.**

- The CMS collector of the HotSpot JVM followed Printezis and Detlefs. It was deprecated in JDK 9 and removed in JDK 14.
- The [Boehm collector](/boehm-gc/) has a mostly concurrent mode that uses the dirty bits of the virtual-memory system, as in Boehm, Demers and Shenker (1991).
- The [Garbage-First collector](/garbage-first-collector/) marks concurrently with a [snapshot-at-the-beginning](/snapshot-at-the-beginning/) barrier and compacts in pauses.
- [Shenandoah](/shenandoah-collector/), [ZGC](/z-garbage-collector/) and [C4](/c4-collector/) also move objects concurrently, with a load barrier.

## Variations

- **Snapshot barrier.** Use the [snapshot-at-the-beginning](/snapshot-at-the-beginning/) deletion barrier instead of dirty cards. The remark then only drains the buffers of the barrier and has no card rescan; the price is more floating garbage.
- **Dirty pages from the hardware.** Boehm, Demers and Shenker read the dirty bits of the virtual-memory system, so the mutator code needs no barrier at all.
- **No global pause.** An [on-the-fly collector](/on-the-fly-garbage-collection/) replaces the pauses with handshakes, in which each thread stops by itself for a moment to give its roots.
- **Parallel phases.** The pauses and the concurrent phases can each use several collector threads; see [parallel garbage collection](/parallel-garbage-collection/).
- **Concurrent compaction.** Mark-sweep fragments the heap. Concurrent copying needs a [read barrier](/read-barrier/) or forwarding, as in [Baker's collector](/baker-real-time-collector/) and its concurrent heirs.

## Pitfalls

- **Card mark before the store.** If the barrier dirties the card first and the collector cleans and rescans the card between the two instructions, the new pointer is missed. Store first, then dirty the card, and make sure that a collector that sees the dirty card also sees the store.
- **Clean after the rescan.** If precleaning rescans a card and then cleans it, a store that came during the rescan is lost. Clean first, as at line L4.
- **Starting too late.** The collector must finish before the free memory runs out. If it does not, the result is a concurrent mode failure and a long pause. The trigger must use the allocation rate and the marking rate, not only the heap size.
- **Allocating ahead of the sweep.** A cell allocated during the sweep at an address that the sweep has not reached yet must be marked, or the sweep frees it while it is in use. Line L16 does this.
- **Forgetting stores by the runtime.** Array copies, object clones and native code must run the barrier too.

## Exercises

1. Show an interleaving of the lost-object program in which $Z$ is freed when line L14 is removed.
2. The remark of the template rescans the roots. Change the template so that the registers are treated as a card that is always dirty, and show that the proof still holds.
3. Replace the card barrier by the deletion barrier of [snapshot-at-the-beginning](/snapshot-at-the-beginning/). Which lines of the remark can be removed?
4. Model a barrier that dirties the card before the store, with the two instructions as separate steps. Find an interleaving with precleaning that loses an object.

## References
