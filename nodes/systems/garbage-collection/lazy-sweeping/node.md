---
tag: 60PT1Y
kind: technique
slug: lazy-sweeping
name: Lazy sweeping
aliases:
- lazy sweep
- sweeping on allocation
area: systems/garbage-collection
level: advanced
summary: "A mark-sweep collector that only marks in the pause. The allocator sweeps the heap later, one block at a time, when it needs free cells."
prereqs: [mark-and-sweep]
see_also: [mark-and-sweep, stop-the-world-collection, incremental-garbage-collection, boehm-gc, segregated-free-lists, gc-space-time-tradeoff, deferred-coalescing]
sources:
  - paper: doi:10.1002/spe.4380121108
    title: R. John M. Hughes, A semi-incremental garbage collection algorithm, Software, Practice and Experience 12(11), 1081 ff., 1982
    locator: the algorithm in which the allocator sweeps the heap after a mark phase, so the delay of a collection depends on the heap in use
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 2, Section 2.5 (lazy sweeping) and Section 2.4 (bitmap marking)
  - paper: Hans-J. Boehm, Reducing garbage collector cache misses, Proceedings of the International Symposium on Memory Management (ISMM 2000), ACM, 2000
    locator: lazy sweeping of the blocks of one size class in the Boehm-Demers-Weiser collector
---

Lazy sweeping is a change to [mark-and-sweep](/mark-and-sweep/) collection: the collection pause only marks, and the sweep is done later by the allocator, one block at a time, when it runs out of free cells. The total sweep work in a cycle is the same, but it leaves the pause, which then costs time in the live data and not in the heap size. Hughes described it in 1982, and the Boehm-Demers-Weiser collector sweeps lazily, one block of a size class at a time. It is correct because a cell that was unmarked at the end of the mark is [garbage](/garbage/), and garbage stays garbage.

## In plain words

A mark-and-sweep collector stops the program twice as long as it must. The marking has to happen while the program waits, but the sweep does not: it only collects cells that nobody can reach, and those cells will not come back to life.

So the collector marks and returns at once. The heap is cut into blocks. When the program asks for a cell and the free list is empty, the allocator sweeps just the next block: it clears the marks of the cells in use and puts the others on the free list. Then it hands out one of them. When every block is swept and no cell is free, it is time for the next mark.

The work moves from one long stop into many small steps that come with the allocations.

## When it applies

- A [mark-and-sweep](/mark-and-sweep/) or mark-region collector with a heap much larger than the live data, so that the sweep, which costs time in the heap size, is a large part of the pause.
- The pause matters more than the total work: interactive programs, servers with response-time limits.
- The heap is divided into blocks, often one size class per block, as with [segregated free lists](/segregated-free-lists/); the allocator then sweeps only blocks of the size it needs.
- The mark bits can stay valid from one mark to the time of the sweep. A collector that must reuse the mark bits for something else in between, or that moves objects, cannot defer the sweep this way.

## The template

The heap has $B$ blocks of $S$ cells. Each cell has $k$ fields and a mark bit. The value $\mathit{next}$ is the first block not yet swept in this cycle; the blocks $\mathit{next}, \ldots, B - 1$ still carry the marks of the last mark phase.

```pseudo id=main
COLLECT()                                      ▷ the pause: mark only
L1  clear the marks of the blocks next .. B − 1    ▷ stale marks from the last cycle
L2  mark all cells reachable from the roots
L3  next ← 0, free ← empty                     ▷ every block now waits for a sweep

ALLOCATE()
L4  while free is empty do
L5      if next = B then
L6          if this call has already collected then fail: every cell is reachable
L7          COLLECT()
L8      else SWEEP-BLOCK(next), next ← next + 1
L9  a ← take a cell from free, clear its fields, return a

SWEEP-BLOCK(b)
L10 for each cell a of block b do
L11     if a is marked then clear the mark of a
L12     else put a on free
```

The holes of the template are the mark of line L2 (a stack marker, [pointer reversal](/schorr-waite-marking/), or a parallel marker), the unit of line L8 (a block, a page, or the next block of the right size class), and the free structure (a list per block, or a bump pointer over a run of free cells). Line L1 matters only if the program forces a collection before the last sweep ended: a live cell in an unswept block still carries its old mark, and if it is not cleared, the new mark would see the cell as done and never trace its fields.

**Why it is safe.** After line L2, a cell is unmarked exactly when it is not [reachable](/heap-reachability/). A cell that is not reachable can never become reachable again, because the mutator can only store pointers that it can already reach. During the cycle, ALLOCATE takes cells only from blocks that it has already swept, so no new cell appears in an unswept block. So at any time, an unmarked cell in an unswept block is garbage, and line L12 frees only garbage. A marked cell may become garbage after the mark; it is then not freed in this cycle, which an eager sweep right after the mark would also keep until the next cycle.

**Cost.** In the model with $r$ roots and $L$ reachable cells, the pause is $O(r + kL)$ for the mark, plus the clearing of line L1 for the blocks that the last cycle left unswept. The sweep still visits all $n = BS$ cells in a cycle, but each call of ALLOCATE does at most the sweep of the blocks it needs, and a block costs $O(S)$. If a fraction $f$ of the cells of every block is live, a block gives $(1 - f) S$ free cells, so the sweep cost per allocated cell is $S / ((1 - f) S) = 1 / (1 - f)$ cell visits. For example, with $B = 3$ blocks of $S = 2$ cells and three of the six cells live, a collection with an eager sweep visits 6 cells in the pause, and with lazy sweeping the pause visits none: the next three allocations visit 2 cells each.

**Worked trace.** Take $B = 3$, $S = 2$, $k = 1$, all six cells allocated, the fields $0 \to 3$, $3 \to 5$, $1 \to 2$, $2 \to 1$, $4 \to$ nil, and the root $0$. The live cells are $0, 3, 5$. The next ALLOCATE finds no free cell and $\mathit{next} = B$, so it runs COLLECT, which marks $0, 3, 5$ and sets $\mathit{next} = 0$. It then sweeps block 0 (cells 0 and 1): it clears the mark of 0 and frees 1, and it returns 1. The next call sweeps block 1, clears the mark of 3, frees 2 and returns it. The third call sweeps block 2, clears the mark of 5, frees 4 and returns it. The garbage cycle $1 \leftrightarrow 2$ was reclaimed by two separate allocations.

## Classic examples

- **[Mark-and-sweep](/mark-and-sweep/).** The eager form, where lines L8 to L12 run for all blocks at the end of COLLECT. Lazy sweeping changes only when the sweep runs.
- **Hughes's semi-incremental collector (1982).** The allocator sweeps the heap in small parts after a mark, so the delay at a collection is in proportion to the heap in use and not to the full heap.
- **The [Boehm collector](/boehm-gc/).** A mark-sweep collector for C with blocks of one size class; the allocator sweeps a block of the size it needs when its free list for that size is empty.
- **Mark-region collectors such as [Immix](/immix-collector/).** The allocator finds free lines in a block from the mark bits of the lines, at allocation time, which is the same idea at the level of lines.

## Variations

- **Size-class blocks.** Keep one list of unswept blocks per size class, and sweep only a block of the size that the request needs. Blocks with no live cell, found from a per-block live count kept by the marker, go back whole to the block allocator without a sweep.
- **Sweeping with the mark bitmap.** With the mark bits in a side bitmap, a sweep can skip a word of the bitmap that is all ones (all live) or find a run of zero bits (free cells) with one machine instruction.
- **Background sweeping.** A collector thread sweeps the blocks that the allocator has not reached yet, so the sweep runs in parallel with the program; the allocator and the sweeper must then take blocks in a safe way.
- **Sweeping as part of incremental collection.** In an [incremental collector](/incremental-garbage-collection/), the sweep is one more phase that the allocator drives in small steps.

## Pitfalls

- **Stale marks in unswept blocks.** If a new mark starts while some blocks still hold the marks of the last mark, a live cell there looks done, its fields are never traced, and a cell reachable only through it is freed. Clear those marks first (line L1), or finish the sweep before the mark.
- **Allocating into an unswept block.** If the allocator hands out a cell of a block that it has not swept, that new cell is unmarked, and the later sweep of the block frees it while it is live. Take cells only from swept blocks, or allocate new cells already marked ("allocate black").
- **Calling COLLECT too early.** Line L7 must run only when all blocks are swept. A collection while free cells still wait in unswept blocks throws away work and makes the next cycle start early.
- **Hidden cost in the allocator.** One allocation can sweep many blocks in a row if they are all full of live cells. Lazy sweeping bounds the pause of the collection, not the worst time of a single allocation.

## Exercises

1. With $B$ blocks of $S$ cells and a fixed fraction $f$ of live cells in every block, show that one cycle of $(1 - f) B S$ allocations does exactly $BS$ cell visits in SWEEP-BLOCK.
2. Construct a run in which a forced collection without line L1 frees a reachable cell, with two blocks of two cells.

## References
