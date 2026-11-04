---
tag: 9NS9WP
kind: data-structure
slug: circular-buffer
name: Circular buffer
aliases:
- ring buffer
- circular queue
area: data-structures/linear-structures
level: intro
summary: Fixed-size array used as a wrap-around FIFO buffer.
implements: [queue, deque]
prereqs: [array, queue]
see_also: [deque, dynamic-array-resizing, circular-linked-list, sliding-window, two-stacks-queue, dynamic-array, monotonic-deque, real-time-queue]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.1 (Simple array-based data structures), the queue in an array with head and tail indices that wrap around, ENQUEUE and DEQUEUE
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.2 (Sequential allocation), the queue kept in a circular area of memory and the tests for overflow and underflow
  - paper: "Leslie Lamport, Specifying concurrent program modules, ACM Transactions on Programming Languages and Systems 5(2) (1983)"
    locator: the bounded queue shared by one producer and one consumer without locks
---

A circular buffer is an [array](/array/) of fixed capacity $N$ used as a [queue](/queue/), with the cell after the last one taken to be the first. The structure keeps the index $h$ of the front item and the count $n$, and the items are in cells $h, h + 1, \ldots, h + n - 1$, each taken modulo $N$. Enqueue writes at index $(h + n) \bmod N$ and dequeue reads at $h$ and moves $h$ forward, so no item is ever shifted. Each operation at either end, and access by position, costs $O(1)$ worst-case time with no allocation. It is the standard queue of device drivers, audio and network buffers, and producer-consumer channels, and with [resizing](/dynamic-array-resizing/) it becomes the array [deque](/deque/) of many libraries.

## In plain words

Picture a round table with a fixed number of seats. People sit down in the next free seat going clockwise, and the person who came first leaves first. You keep track of two things: where the first person sits, and how many people there are. When someone leaves, the "first" seat moves one place clockwise. When the seats at the end of the row are used up, new people go back to the seats at the start, which are free again.

Nobody ever has to change seats. The only limit is the number of seats: when all of them are taken, a new person cannot sit down, or, in some uses, takes the seat of the person who came first.

## The abstract type

The structure implements the bounded [queue](/queue/) type: `enqueue(B, x)` at the back and `dequeue(B)` at the front, with `size(B)`, `is_empty(B)` and `is_full(B)`. It also gives the [deque](/deque/) operations `push_front` and `pop_back`, and `get(B, i)` for the item at position $i$ from the front. The capacity $N$ is fixed when the buffer is made, so enqueue on a full buffer fails, unless the buffer is set to overwrite or to grow.

## Representation

An array $A[0..N-1]$, an index $h$ and a count $n$.

**Invariant.** $0 \le h < N$ and $0 \le n \le N$, and the queue from the front to the back is

$$\langle A[h], A[(h + 1) \bmod N], \ldots, A[(h + n - 1) \bmod N] \rangle.$$

The other $N - n$ cells hold no item of the queue; they may hold old values. Keeping $n$, not a second index $t$ for the back, makes "empty" ($n = 0$) and "full" ($n = N$) different states. With two indices only, $h = t$ means both, which is why some books leave one cell unused.

## Operations

```pseudo id=main
ENQUEUE(B, x)
L1  if B.n = N then error "overflow"
L2  A[(B.h + B.n) mod N] ← x
L3  B.n ← B.n + 1
DEQUEUE(B)
L4  if B.n = 0 then error "underflow"
L5  x ← A[B.h]
L6  B.h ← (B.h + 1) mod N, B.n ← B.n − 1
L7  return x
PUSH-FRONT(B, x)                           ▷ B is not full
L8  B.h ← (B.h − 1) mod N, A[B.h] ← x, B.n ← B.n + 1
POP-BACK(B)                                ▷ B is not empty
L9  B.n ← B.n − 1
L10 return A[(B.h + B.n) mod N]
GET(B, i)                                  ▷ 0 ≤ i < B.n
L11 return A[(B.h + i) mod N]
```

The modulo is the whole trick: index $N$ is read as index 0, so the occupied run of cells can wrap past the end of the array. In line L8, $(h - 1) \bmod N$ is $N - 1$ when $h = 0$; in languages where `%` can return a negative value, write $(h + N - 1) \bmod N$. When $N$ is a power of two, `mod N` is `& (N − 1)`, a single machine instruction.

## Example

Take $N = 4$. The column $A$ shows the four cells, with $\cdot$ for a cell never written. Cells outside the queue keep their old values.

| operation | $A$ | $h$ | $n$ | queue | result |
|---|---|---|---|---|---|
| enqueue(1) | 1 $\cdot$ $\cdot$ $\cdot$ | 0 | 1 | 1 | |
| enqueue(2) | 1 2 $\cdot$ $\cdot$ | 0 | 2 | 1 2 | |
| enqueue(3) | 1 2 3 $\cdot$ | 0 | 3 | 1 2 3 | |
| dequeue | 1 2 3 $\cdot$ | 1 | 2 | 2 3 | 1 |
| enqueue(4) | 1 2 3 4 | 1 | 3 | 2 3 4 | |
| enqueue(5) | 5 2 3 4 | 1 | 4 | 2 3 4 5 | |
| enqueue(6) | 5 2 3 4 | 1 | 4 | 2 3 4 5 | overflow |
| dequeue | 5 2 3 4 | 2 | 3 | 3 4 5 | 2 |
| push_front(9) | 5 9 3 4 | 1 | 4 | 9 3 4 5 | |
| pop_back | 5 9 3 4 | 1 | 3 | 9 3 4 | 5 |
| get(2) | 5 9 3 4 | 1 | 3 | 9 3 4 | 4 |

Enqueue(5) writes at $(1 + 3) \bmod 4 = 0$: the queue wraps past the end, and cell 0, which held the dequeued 1, is used again. Push_front(9) moves $h$ back from 2 to 1. Get(2) reads cell $(1 + 2) \bmod 4 = 3$.

## Correctness

Write $c_i = (h + i) \bmod N$ for the cell of position $i$. ENQUEUE on a non-full buffer writes $x$ in cell $c_n$, which is not one of the cells $c_0, \ldots, c_{n-1}$ because $n < N$ and the $c_i$ for $0 \le i < N$ are distinct. So it does not overwrite an item, and with $n + 1$ the queue gains $x$ at the back. DEQUEUE returns $A[c_0]$, and moving $h$ to $c_1$ while lowering $n$ makes the queue start at the old position 1. PUSH-FRONT and POP-BACK are the mirror cases. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | memory writes |
|---|---|---|
| enqueue, push_front | $O(1)$ worst case | 1 cell and 2 words |
| dequeue, pop_back | $O(1)$ worst case | 2 words |
| get, set at position $i$ | $O(1)$ worst case | |
| insert or delete at position $i$ | $\Theta(\min(i, n - i) + 1)$ | |
| space | $N$ cells and 2 words | |

No operation allocates memory, which is why the circular buffer is used in interrupt handlers and real-time code. The occupied cells are contiguous, or in two contiguous runs when they wrap, so a walk through the queue has good cache behaviour.

## Variants

- **Overwrite when full.** Enqueue on a full buffer writes over the oldest item and moves $h$ forward. The buffer then keeps the last $N$ items of a stream, as in a log of recent events or the [sliding window](/sliding-window/) of a moving average.
- **Growable.** On a full enqueue, allocate an array of capacity $2N$ and copy the items in queue order to cells $0, \ldots, n - 1$, then set $h = 0$. By [dynamic array resizing](/dynamic-array-resizing/), each operation costs $O(1)$ amortized. Java's `ArrayDeque` and Rust's `VecDeque` are growable circular buffers.
- **Two indices.** Keep the front index $h$ and the back index $t$ instead of $n$, and leave one cell unused, so that the buffer is full when $(t + 1) \bmod N = h$. This is the form of CLRS Section 10.1. It is the form used between two threads, because each index is written by only one of them.
- **Free-running counters.** Keep two counters that never wrap modulo $N$, and take them modulo $N$ only to index the array. The count is their difference, so empty and full differ without a spare cell. This needs $N$ to be a power of two if the counters overflow.
- **Lock-free single producer, single consumer.** The producer writes only $t$ and the consumer writes only $h$. With the right memory ordering, no lock is needed. Lamport (1983) gave this queue as an example of a concurrent program.

## When to use it

Use a circular buffer for a queue or deque when the largest size is known, or when a bound on the size is acceptable and items may be dropped or rejected beyond it: buffers between a producer and a consumer, keyboard and network input, audio samples, the last $N$ events. Use the growable form as a general deque; it is faster than a linked list because it allocates rarely and keeps items next to each other. If the program needs constant-time insertion in the middle at a held position, use a [doubly linked list](/doubly-linked-list/). If one end is enough, a [dynamic array](/dynamic-array/) is simpler.

## Pitfalls

- **Full and empty look the same.** With only a front and a back index and no spare cell, $h = t$ in both states. Keep the count, leave one cell unused, or use free-running counters.
- **Negative modulo.** In C, Java and Go, `(h - 1) % N` is $-1$ when $h = 0$. Write `(h + N - 1) % N`.
- **Growing by a raw copy.** Copying $A[0..N-1]$ into the low half of a larger array breaks the queue when it wraps: the items in cells $0, \ldots, t - 1$ belong after those in cells $h, \ldots, N - 1$. Copy in queue order, or move the wrapped run to just after the old end.
- **Overflow of free-running counters.** If $N$ is not a power of two, a counter that wraps at $2^{32}$ jumps to a different cell modulo $N$.
- **Memory ordering between threads.** In the lock-free form, the producer must write the cell before it publishes the new $t$, and the consumer must read $t$ before it reads the cell. Plain stores and loads are not enough on most processors; use release and acquire operations.

## Implementations

## History

Knuth (Volume 1, Section 2.2.2) treats a queue kept in a circular area of memory, with the tests for overflow and underflow, as part of sequential allocation. Hardware buffers of the same form were used in input and output devices from the early days of computing. CLRS Section 10.1 gives the form with head and tail indices. Lamport (1983) used the buffer between one producer and one consumer to show a concurrent queue that needs no lock.

## References
