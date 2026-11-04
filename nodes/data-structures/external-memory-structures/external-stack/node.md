---
tag: A69Z23
kind: data-structure
slug: external-stack
name: External stack
aliases:
- disk-based stack
area: data-structures/external-memory-structures
level: intro
summary: Stack that keeps one block of its top in memory so that push and pop cost O(1/B) I/Os amortized.
implements: [stack]
model: external-memory-model
prereqs: [stack, external-memory-model, amortized-cost]
see_also: [external-queue, dynamic-array, potential-method, buffer-tree, external-memory-priority-queue, time-forward-processing]
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

An external stack is a [stack](/stack/) that holds most of its items on disk, in blocks of $B$ items, and keeps only its top part in memory. The top part is a buffer of at most $2B$ items. A push into a full buffer first writes the $B$ oldest items of the buffer to disk as one block, and a pop from an empty buffer first reads the last block back. After each block transfer the buffer holds exactly $B$ items, so at least $B$ operations come between two transfers, and $n$ pushes and pops cost at most $n/B$ I/Os: $O(1/B)$ amortized per operation in the [external memory model](/external-memory-model/). This is optimal, and it is the reason that a stack, a scan and a [queue](/external-queue/) are the cheapest structures of external memory.

## In plain words

Think of a tall pile of papers, too tall for your desk. You keep the top of the pile on the desk and put the rest in boxes in a storeroom, one box for each fixed number of papers.

When the papers on the desk get too many, you pack the lower ones into a box and carry it away. When the desk is empty and you need another paper, you bring back the last box you stored. Each trip moves a whole box.

The trick is to keep room for two boxes of papers on the desk. After each trip, the desk is half full, so many papers must come or go before the next trip. With room for only one box, you could be forced to walk to the storeroom for every single paper.

## The abstract type

The external stack implements the [stack](/stack/): `push(S, x)` puts $x$ on top, `pop(S)` removes and returns the top item, and `top(S)`, `size(S)` and `is-empty(S)` read without a change. Popping an empty stack is an error.

## Representation

There is a block size $B \ge 1$, and memory has room for at least $2B$ items, so $M \ge 2B$.

- A *disk part*: an array of $k$ full blocks $D[0], \ldots, D[k-1]$, each of $B$ items, in the order of the stack from the bottom. On a real disk these are $k$ consecutive blocks of a file, so a counter $k$ is all that memory needs.
- A *buffer* $buf$ in memory, a list of at most $2B$ items: the top of the stack, in order, with the top item last.

The stack, read from the bottom to the top, is $D[0] \cdot D[1] \cdots D[k-1] \cdot buf$. The invariants are that each disk block is full and $|buf| \le 2B$.

## Operations

```pseudo id=main
PUSH(S, x)
L1  if |S.buf| = 2B then                       ▷ the buffer is full
L2      WRITE-BLOCK the first B items of S.buf as S.D[S.k], S.k ← S.k + 1
L3      remove those B items from S.buf          ▷ B items remain
L4  append x to S.buf

POP(S)
L5  if S.buf is empty then
L6      if S.k = 0 then error "the stack is empty"
L7      S.k ← S.k − 1, S.buf ← READ-BLOCK S.D[S.k]   ▷ B items
L8  remove and return the last item of S.buf
```

`top` is a pop followed by putting the item back. `size` is $Bk + |buf|$.

## Example

Take $B = 2$, so the buffer holds up to 4 items. Push $1, 2, \ldots, 7$, then pop 4 times, push 8, and pop until the stack is empty.

| operation | disk | buffer | I/Os so far |
|---|---|---|---|
| push 1, 2, 3, 4 | | [1 2 3 4] | 0 |
| push 5 | [1 2] | [3 4 5] | 1 write |
| push 6 | [1 2] | [3 4 5 6] | 1 |
| push 7 | [1 2] [3 4] | [5 6 7] | 2 |
| pop 7, 6, 5 | [1 2] [3 4] | [ ] | 2 |
| pop | [1 2] | [3], returns 4 | 2 writes, 1 read |
| push 8 | [1 2] | [3 8] | 3 |
| pop 8, 3 | [1 2] | [ ] | 3 |
| pop 2, 1 | | [ ], after reading [1 2] | 4 |

There are 16 operations and 4 block transfers, within the bound $16/B = 8$.

## Correctness

Let $\sigma = D[0] \cdots D[k-1] \cdot buf$. A push in lines L1 to L3 moves the first $B$ items of $buf$ to the end of the disk part, which does not change $\sigma$, and line L4 appends $x$ to $\sigma$. A pop in line L7 moves the last disk block into the empty buffer, which does not change $\sigma$, and line L8 removes the last item of $\sigma$. So $\sigma$ is always the stack, and a pop returns the last item pushed and not yet popped. Line L2 writes exactly $B$ items, so each disk block is full, and line L4 runs on a buffer of at most $2B - 1$ items, so $|buf| \le 2B$. A pop from an empty buffer finds a full block when $k > 0$, so it never returns from an empty buffer except in the error case. The proof below also gives the I/O bound.

## Complexity

**I/O bound.** Any sequence of $n$ pushes and pops, starting from an empty stack, makes at most $\lfloor n/B \rfloor$ block transfers. Right after a transfer, before the operation that caused it changes the buffer, the buffer holds exactly $B$ items. The next transfer needs a buffer of $2B$ items or of 0 items, and each operation changes its size by one. So at least $B$ operations separate two transfers, and the first transfer, a write, comes only at the push number $2B + 1$. Amortized, each operation costs at most $1/B$ I/Os.

| quantity | cost |
|---|---|
| push, pop | $O(1/B)$ amortized I/Os, at most 1 I/O in the worst case |
| top, size | no I/O beyond that of a pop |
| CPU time | $O(1)$ amortized per operation, $O(B)$ in the worst case to copy a block |
| memory | $2B$ items |
| disk | $\lceil N/B \rceil$ blocks for $N$ items |

**Optimality.** A sequence of $N$ pushes must at some point keep about $N - M$ items on disk, and one write moves at most $B$ of them, so $\Omega((N - M)/B)$ I/Os are needed. The external stack matches this bound, the cost of a [scan](/external-memory-model/) of $N$ items.

**A potential function.** With $\Phi = \big|\,|buf| - B\,\big| / B$, an operation without I/O raises $\Phi$ by at most $1/B$, and an operation with one transfer lowers $\Phi$ from 1 to at most $1/B$. So with this potential the amortized cost of each operation is at most $1/B$. The potential starts at 1 and never goes below 0, so $n$ operations make at most $n/B + 1$ transfers. This is the [potential method](/potential-method/) form of the bound, one transfer weaker than the direct count.

## Variants

- **More than two blocks of buffer.** A larger buffer, say $kB$ items, transfers $(k-1)B$ items at a time when it is full. The bound stays $O(1/B)$, and the transfers become longer sequential reads and writes.
- **Prefetching and write-behind.** The STXXL library and similar libraries overlap the next block transfer with the work on the buffer, so that on a real disk the program rarely waits.
- **Several disks.** With $D$ disks, the blocks can be striped over the disks, and each transfer moves $D$ blocks at once, for $O(1/(DB))$ amortized I/Os. See [disk striping](/disk-striping/).
- **A queue.** The same buffering at both ends gives an [external queue](/external-queue/).
- **In main memory.** The same idea with a [dynamic array](/dynamic-array/) of chunks gives a stack that never copies all its items when it grows.

## When to use it

Use an external stack when a stack can grow beyond main memory: the depth-first search of a large graph, the stack of a recursion that has been made explicit, or undo logs. It is also a building block: the [buffer tree](/buffer-tree/), [time-forward processing](/time-forward-processing/) and external graph algorithms use stacks and queues of this form. When the stack fits in memory, a plain array is simpler.

## Pitfalls

- **A buffer of one block thrashes.** With a buffer of only $B$ items, which writes as soon as it is full and reads as soon as it is empty, a push followed by a pop at a block boundary makes one write and one read. An adversary that alternates push and pop there forces one I/O for every operation. The buffer of $2B$ items, which keeps $B$ items after each transfer, is what makes the bound amortized $O(1/B)$.
- **Writing the wrong half.** The items written to disk must be the oldest ones in the buffer, the first $B$ (line L2). Writing the newest ones puts the top of the stack on disk.
- **Partial blocks.** Each block on disk is full. Code that also writes partial blocks has to store their lengths, and a pop then reads blocks that hold few items.
- **Counting `top` as free.** In this implementation `top` on an empty buffer reads a block. The cost is still counted in the bound, but `top` is not free of I/O.

## Implementations

## History

Stacks and queues with buffered blocks are basic tools of the external memory literature from its start, and the parallel disk model of Vitter and Shriver is the usual model for their analysis. Pagh's chapter in the volume Algorithms for Memory Hierarchies of 2003 presents the stack with a buffer of two blocks and the $O(1/B)$ amortized bound, and Mehlhorn and Sanders give it in their textbook of 2008. The STXXL library of Dementiev, Kettner and Sanders provides external stacks of this kind.

## References
