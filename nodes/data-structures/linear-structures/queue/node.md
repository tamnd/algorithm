---
tag: Q8RNN3
kind: abstract-type
slug: queue
name: Queue
aliases:
- FIFO queue
area: data-structures/linear-structures
level: intro
summary: Collection with enqueue and dequeue in first-in first-out order.
prereqs: [asymptotic-notation]
see_also: [stack, deque, circular-buffer, randomized-queue, steque, min-queue, priority-queue, breadth-first-search]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.1 (Simple array-based data structures), the part on stacks and queues, with the queue in an array that wraps around
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.2.1 (Stacks, queues, and deques) and Section 2.2.2 (Sequential allocation), the circular queue
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3 (Bags, Queues, and Stacks), the FIFO queue API and the linked-list implementation with first and last
  - url: https://opendatastructures.org/
    title: Pat Morin, Open Data Structures
    locator: Section 2.3 (ArrayQueue) and Section 3.1 (SLList)
  - paper: John V. Guttag, Abstract data types and the development of data structures, Communications of the ACM 20(6) (1977)
    locator: the algebraic axioms of the type Queue
---

A queue is an abstract data type that holds a finite sequence of items, adds items at one end, the *back*, and removes them at the other end, the *front*. So the item that comes out is always the one that has waited longest, which is the *first in, first out* (FIFO) rule. A [circular buffer](/circular-buffer/) or a [singly linked list](/singly-linked-list/) with a tail pointer gives each operation in $O(1)$ time. Queues order the vertices of [breadth-first search](/breadth-first-search/), the jobs of a round-robin scheduler, and the data in a buffer between a producer and a consumer.

## In plain words

Think of a line of people at a ticket desk. A new person joins at the end of the line. The desk serves the person at the head of the line. Nobody jumps ahead, so people are served in the order in which they came.

A queue in a program works the same way. One action adds an item at the end. Another action takes the item at the head. You can also look at the item at the head without taking it, and ask if the line is empty. A good queue keeps a marker at each end of the line, so each action takes the same short time, however long the line is.

## Operations

A queue over a set $T$ of items is a value $Q$. Its state is a finite sequence $\langle x_1, x_2, \dots, x_k \rangle$ of items of $T$, with $x_1$ at the front, $x_k$ at the back, and $k \ge 0$.

| operation | signature | what it does |
|---|---|---|
| `new` | $\text{new}() \to Q$ | the empty queue $\langle \rangle$ |
| `enqueue` | $\text{enqueue}(Q, x) \to Q$ | $\langle x_1, \dots, x_k \rangle$ becomes $\langle x_1, \dots, x_k, x \rangle$ |
| `dequeue` | $\text{dequeue}(Q) \to (x, Q)$ | for $k \ge 1$: returns $x_1$, and the queue becomes $\langle x_2, \dots, x_k \rangle$ |
| `front` | $\text{front}(Q) \to x$ | for $k \ge 1$: returns $x_1$ and does not change $Q$ (also called `peek`) |
| `is_empty` | $\text{is\_empty}(Q) \to \text{bool}$ | true when $k = 0$ |
| `size` | $\text{size}(Q) \to \mathbb{N}$ | returns $k$ |

`dequeue` and `front` on the empty queue are errors (underflow). An implementation with a fixed capacity $N$ also has overflow: an `enqueue` when $k = N$.

### Example

Start with the empty queue. The front is on the left.

| step | operation | result | queue after |
|---|---|---|---|
| 1 | enqueue 5 | | $\langle 5 \rangle$ |
| 2 | enqueue 2 | | $\langle 5, 2 \rangle$ |
| 3 | enqueue 8 | | $\langle 5, 2, 8 \rangle$ |
| 4 | dequeue | 5 | $\langle 2, 8 \rangle$ |
| 5 | front | 2 | $\langle 2, 8 \rangle$ |
| 6 | enqueue 7 | | $\langle 2, 8, 7 \rangle$ |
| 7 | size | 3 | $\langle 2, 8, 7 \rangle$ |
| 8 | dequeue | 2 | $\langle 8, 7 \rangle$ |
| 9 | dequeue | 8 | $\langle 7 \rangle$ |
| 10 | dequeue | 7 | $\langle \rangle$ |
| 11 | is_empty | true | $\langle \rangle$ |

The items came out as 5, 2, 8, 7, the order in which they went in. The same operations on a [stack](/stack/) give 8 at step 4 and 7, 2, 5 at steps 8 to 10.

## Laws

Each implementation meets these equations, for each queue $Q$ and each item $x$:

$$\begin{aligned}
&(\text{Q1})\quad \text{is\_empty}(\text{new}()) = \text{true}, \qquad \text{is\_empty}(\text{enqueue}(Q, x)) = \text{false},\\
&(\text{Q2})\quad \text{front}(\text{enqueue}(Q, x)) = \begin{cases} x & \text{if } \text{is\_empty}(Q),\\ \text{front}(Q) & \text{else,} \end{cases}\\
&(\text{Q3})\quad \text{dequeue}(\text{enqueue}(Q, x)) = \begin{cases} (x, \text{new}()) & \text{if } \text{is\_empty}(Q),\\ (y, \text{enqueue}(Q', x)) & \text{else, where } (y, Q') = \text{dequeue}(Q), \end{cases}\\
&(\text{Q4})\quad \text{size}(\text{new}()) = 0, \qquad \text{size}(\text{enqueue}(Q, x)) = \text{size}(Q) + 1.
\end{aligned}$$

The terms $\text{dequeue}(\text{new}())$ and $\text{front}(\text{new}())$ are not defined. Compare these laws with the laws of the [stack](/stack/): there, a pop right after a push returns the new item, and here a dequeue returns the new item only when the queue was empty. Laws (Q2) and (Q3) need a case split on the inner queue, which is why a queue is harder than a stack to build from one end of a list.

**Canonical form.** Each queue that a program can build from $\text{new}()$ by valid calls of enqueue and dequeue equals exactly one term $E(y_1, \dots, y_k) = \text{enqueue}(\cdots\text{enqueue}(\text{new}(), y_1)\cdots, y_k)$ with $k \ge 0$, and then $\text{dequeue}(E(y_1, \dots, y_k)) = (y_1, E(y_2, \dots, y_k))$ for $k \ge 1$.

*Proof.* First the formula for dequeue, by induction on $k$. For $k = 1$ it is the first case of (Q3). For $k \ge 2$, $E(y_1, \dots, y_k) = \text{enqueue}(E(y_1, \dots, y_{k-1}), y_k)$ with a nonempty inner queue by (Q1). The induction hypothesis gives $\text{dequeue}(E(y_1, \dots, y_{k-1})) = (y_1, E(y_2, \dots, y_{k-1}))$, and the second case of (Q3) gives $(y_1, \text{enqueue}(E(y_2, \dots, y_{k-1}), y_k)) = (y_1, E(y_2, \dots, y_k))$. Existence of the canonical form then follows by induction on the number of calls: enqueue appends to the term, and a valid dequeue needs $k \ge 1$ and gives a term with $k - 1$ items. Uniqueness, by induction on $k$: equal terms have the same $k$ by (Q4), the same first item $y_1$ by (Q2) and the formula, and equal rests $E(y_2, \dots, y_k)$, which have the same items by the induction hypothesis. $\square$

So the state is exactly the sequence $\langle y_1, \dots, y_k \rangle$, and two implementations that meet (Q1) to (Q4) agree on each sequence of operations.

**Order of removal.** If $x$ is enqueued before $y$, then $x$ is dequeued before $y$. So a queue cannot reorder its input: if the items $1, 2, \dots, n$ pass through a queue, they come out as $1, 2, \dots, n$ in each interleaving of the operations. This is the opposite of a stack, which can make $C_n = \frac{1}{n+1}\binom{2n}{n}$ different outputs.

## Implementations

| implementation | enqueue | dequeue and front | space for $n$ items |
|---|---|---|---|
| [circular buffer](/circular-buffer/) with a fixed capacity $N$ | $\Theta(1)$ worst case | $\Theta(1)$ worst case | $N$ cells, so $n \le N$ |
| circular buffer in a [dynamic array](/dynamic-array/) | $\Theta(1)$ amortized, $\Theta(n)$ worst case | $\Theta(1)$ amortized | $\Theta(n)$ |
| [singly linked list](/singly-linked-list/) with head and tail pointers | $\Theta(1)$ worst case | $\Theta(1)$ worst case | $n$ nodes, one item and one [pointer](/pointer/) each |
| two [stacks](/stack/), an inbox and an outbox | $\Theta(1)$ worst case | $\Theta(1)$ amortized, $\Theta(n)$ worst case | $\Theta(n)$ |

The circular buffer keeps the index $h$ of the front and the count $k$ in an array $A[0 \ldots N-1]$. The front is $A[h]$, and enqueue writes $A[(h + k) \bmod N]$. The linked list removes at the head and adds after the tail. A plain [array](/array/) with a front index that only moves right also works, but it wastes the cells before the front.

The two-stack queue pushes each new item on the inbox. A dequeue pops the outbox; when the outbox is empty, it first moves all items of the inbox to the outbox, which reverses them. Each item is pushed at most twice and popped at most twice, so a sequence of $m$ operations costs $O(m)$ in total, which is $O(1)$ amortized by the [accounting method](/accounting-method/).

Related types: a [deque](/deque/) adds and removes at both ends, a [steque](/steque/) is a stack that also adds at the bottom, a [randomized queue](/randomized-queue/) removes a random item, a [min-queue](/min-queue/) adds a `min` operation, and a [priority queue](/priority-queue/) removes the item with the least key, not the oldest one.

## References
