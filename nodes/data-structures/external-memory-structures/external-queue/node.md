---
tag: HQ3Q31
kind: data-structure
slug: external-queue
name: External queue
aliases:
- disk-based queue
- external FIFO
area: data-structures/external-memory-structures
level: intro
summary: FIFO queue that buffers its head and tail blocks in memory, giving O(1/B) amortized I/Os per operation.
implements: [queue]
model: external-memory-model
prereqs: [queue, external-memory-model, external-stack]
see_also: [external-stack, amortized-cost, buffer-tree, external-memory-priority-queue, time-forward-processing, disk-striping]
sources:
  - book: isbn:9783540008835
    title: Ulrich Meyer, Peter Sanders and Jop Sibeyn (editors), Algorithms for Memory Hierarchies, Lecture Notes in Computer Science 2625, Springer (2003)
    locator: Chapter 2, Rasmus Pagh, Basic external memory data structures, Section 2.1 (stacks and queues)
  - book: isbn:9783540779773
    title: Kurt Mehlhorn and Peter Sanders, Algorithms and Data Structures, The Basic Toolbox, Springer (2008)
    locator: Section 3.4, stacks and queues, and its exercises on stacks and queues in external memory
  - book: isbn:9781601981066
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4) (2008)
    locator: Chapter 3, the bound Scan(N) and the parallel disk model that the analysis uses
---

An external queue is a [queue](/queue/) that keeps most of its items on disk, in blocks of $B$ items, and only its two ends in memory: a *head* buffer with the oldest items and a *tail* buffer with the newest ones, each of at most $B$ items. A full tail is written to disk as one block, and an empty head is refilled with the oldest block on disk, or with the tail itself when no block is on disk. Each item is written at most once and read at most once, and every transfer moves $B$ items, so $n$ operations make at most $2n/B$ I/Os: $O(1/B)$ amortized per operation in the [external memory model](/external-memory-model/). Unlike the [external stack](/external-stack/), the queue needs no extra slack against thrashing, because its two ends are in different places.

## In plain words

Think of a long line of letters waiting to be answered. New letters go on one end, and you answer letters from the other end. The line is too long for your desk, so you keep two trays on the desk: one for the newest letters and one for the next letters to answer.

When the tray of new letters is full, you put them in a box and send the box to the storeroom. When the tray of letters to answer is empty, you fetch the oldest box. If the storeroom is empty, you just take the tray of new letters.

Each letter goes to the storeroom at most once and comes back at most once, always in a full box. So the trips are few.

## The abstract type

The external queue implements the [queue](/queue/): `enqueue(Q, x)` puts $x$ at the back, `dequeue(Q)` removes and returns the front item, and `front(Q)`, `size(Q)` and `is-empty(Q)` read without a change. Dequeuing an empty queue is an error.

## Representation

There is a block size $B \ge 1$, and memory has room for $2B$ items.

- A *head* buffer $H$ in memory: at most $B$ items, the front of the queue, with the front item first.
- A *disk part*: a sequence of full blocks $D_1, \ldots, D_k$ of $B$ items each, oldest first. On a real disk this is a file used as a ring, or a list of blocks; memory keeps only the positions of the first and the last block.
- A *tail* buffer $T$ in memory: fewer than $B$ items, the back of the queue, with the newest item last.

The queue, from the front to the back, is $H \cdot D_1 \cdots D_k \cdot T$.

## Operations

```pseudo id=main
ENQUEUE(Q, x)
L1  append x to Q.T
L2  if |Q.T| = B then                         ▷ the tail is a full block
L3      WRITE-BLOCK Q.T as the new last block of the disk part
L4      Q.T ← empty

DEQUEUE(Q)
L5  if Q.H is empty then
L6      if the disk part has a block then
L7          Q.H ← READ-BLOCK of the first block, and remove that block from the disk part
L8      else if Q.T is empty then error "the queue is empty"
L9      else Q.H ← Q.T, Q.T ← empty            ▷ no I/O
L10 remove and return the first item of Q.H
```

`front` is a dequeue followed by putting the item back at the front of $H$. `size` is $|H| + Bk + |T|$.

## Example

Take $B = 3$. Enqueue $1, \ldots, 7$, dequeue once, enqueue 8, then dequeue until the queue is empty.

| operation | head | disk | tail | I/Os |
|---|---|---|---|---|
| enqueue 1, 2, 3 | | [1 2 3] | | 1 write |
| enqueue 4 to 7 | | [1 2 3] [4 5 6] | [7] | 2 writes |
| dequeue, returns 1 | [2 3] | [4 5 6] | [7] | 2 writes, 1 read |
| enqueue 8 | [2 3] | [4 5 6] | [7 8] | |
| dequeue 2, 3 | | [4 5 6] | [7 8] | |
| dequeue 4, 5, 6 | | | [7 8] | 2 writes, 2 reads |
| dequeue, returns 7 | [8] | | | the tail moves to the head, no I/O |
| dequeue, returns 8 | | | | 4 I/Os in total |

There are 16 operations and 4 transfers, within the bound $2 \cdot 16 / B \approx 10.7$.

## Correctness

Let $\sigma = H \cdot D_1 \cdots D_k \cdot T$. Line L1 appends $x$ to $\sigma$. Lines L3 and L4 move the whole tail to the end of the disk part, which does not change $\sigma$. In a dequeue, line L7 moves the first block into the empty head and line L9 moves the tail into the empty head when the disk part is empty; neither changes $\sigma$. Line L10 then removes the first item of $\sigma$. So $\sigma$ is always the queue, and a dequeue returns the oldest item not yet dequeued. Only full tails are written, so every block has $B$ items, and $|T| < B$ and $|H| \le B$ after every operation. The proof below gives the details and the I/O bound.

## Complexity

**I/O bound.** Each write moves a full tail of $B$ items that were enqueued since the last write, and an item never goes back to the tail, so it is written at most once: there are at most $\lfloor e/B \rfloor$ writes for $e$ enqueues. Each read takes a block that some write put on disk, and removes it, so there are at most as many reads as writes. So $n$ operations make at most $2\lfloor n/B \rfloor$ transfers, $2/B$ amortized per operation.

| quantity | cost |
|---|---|
| enqueue, dequeue | $O(1/B)$ amortized I/Os, at most 1 I/O in the worst case |
| front, size | no I/O beyond that of a dequeue |
| CPU time | $O(1)$ amortized, $O(B)$ in the worst case to copy a block |
| memory | $2B$ items |
| disk | $\lfloor N/B \rfloor$ blocks for $N$ items |

**No thrashing.** An item enters the disk part only as part of a full block and leaves it only in the same block, so no sequence of operations can make the queue read and write the same block again and again. This is the difference from a stack, whose single active end needs a buffer of two blocks.

**Optimality.** When more than $2B$ items wait in the queue, the others must be on disk, and each of them costs a share $1/B$ of a write and of a read. So $\Theta(1/B)$ amortized is the best possible for a queue that holds more than its memory.

## Variants

- **Larger buffers.** With buffers of $kB$ items, the transfers move $k$ blocks at once, which suits real disks better, and the bound stays $O(1/B)$.
- **Prefetching.** A library such as STXXL reads the next block of the disk part, and writes the old tail, while the program works on the buffers, so that it rarely waits for the disk.
- **Several disks.** Striping the blocks over $D$ disks gives $O(1/(DB))$ amortized I/Os. See [disk striping](/disk-striping/).
- **Deques.** A double-ended queue can be built the same way, with a buffer of two blocks at each end, for the reason given on the [external stack](/external-stack/) page.
- **Priority queues.** Queues in order of priority, not of arrival, need more: see the [external memory priority queue](/external-memory-priority-queue/) and the [buffer tree](/buffer-tree/).

## When to use it

Use an external queue when a FIFO grows beyond main memory: the frontier of a breadth-first search of a large graph, the input of a stream of jobs, or the passes of an external algorithm that writes a sequence once and reads it once later. Breadth-first search in external memory, for example, keeps its frontiers in files that are written and read in this way. When the queue fits in memory, a ring buffer is simpler.

## Pitfalls

- **Reading the wrong end.** The head must be refilled from the oldest block (line L7), and from the tail only when the disk part is empty (line L9). Taking the tail while older blocks are on disk returns items out of order.
- **Writing a partial tail.** Writing the tail before it is full gives blocks with fewer than $B$ items. The bound then fails, because a block may carry only one item.
- **A circular file.** On a real disk, the disk part is used at the front and grown at the back. Keeping it as a ring of blocks in one file, or freeing blocks at the front, keeps its space at $O(N/B)$ blocks and not $O(n/B)$ for $n$ operations.
- **Counting the move from tail to head as an I/O.** Line L9 only changes pointers in memory. Counting it as a transfer is not wrong for the bound, but it hides that a queue which fits in $2B$ items makes no I/O at all.

## Implementations

## History

Queues with buffered blocks at both ends are, with stacks, among the first structures of the external memory literature, and the parallel disk model of Vitter and Shriver is the usual model for their analysis. Pagh's chapter in the volume Algorithms for Memory Hierarchies of 2003 presents the external queue and its $O(1/B)$ amortized bound, and Mehlhorn and Sanders give it in their textbook of 2008. The STXXL library of Dementiev, Kettner and Sanders provides external queues of this kind.

## References
