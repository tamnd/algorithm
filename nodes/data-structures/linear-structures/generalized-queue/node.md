---
tag: JGQ2VZ
kind: abstract-type
slug: generalized-queue
name: Generalized queue
area: data-structures/linear-structures
level: intro
summary: A data type that stores items and supports insertion and deletion of the kth oldest item, generalizing stacks and queues.
prereqs: [stack, queue]
see_also: [randomized-queue, priority-queue, order-statistic-tree, fenwick-tree, implicit-treap, deque, list, bag]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3, exercise 1.3.38 (Delete kth element), with an array implementation and a linked-list implementation
  - book: isbn:9780201314526
    title: Robert Sedgewick, Algorithms in C, Parts 1 to 4, third edition
    locator: Chapter 4 (Abstract data types), the section on FIFO queues and generalized queues, where stacks, FIFO queues and randomized queues are cases of one interface with insert and remove
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 17.1 (Dynamic order statistics), OS-SELECT and OS-RANK
---

A generalized queue is the abstract type of a collection that remembers the order in which its items arrived and can remove the $k$-th oldest item for any $k$. Insert adds an item as the newest one, and `delete(k)` removes and returns the item that is $k$-th in the order of arrival. With $k = 1$ it is a [queue](/queue/), with $k = n$ it is a [stack](/stack/), and with $k$ chosen uniformly at random it is a [randomized queue](/randomized-queue/). An array or a linked list gives delete in $\Theta(n)$ time, and an [order-statistic tree](/order-statistic-tree/) or a [Fenwick tree](/fenwick-tree/) over the arrival times gives both operations in $O(\log n)$.

## In plain words

Picture a line of people, each with a ticket that shows when they arrived. New people always join at the end. A normal line serves the person at the front. A pile of papers serves the newest one. A generalized queue lets you say "serve the third oldest" or "serve the oldest but two", and the line closes the gap when that person leaves.

So one type covers the line, the pile and many rules in between. The cost is that the computer must find the $k$-th person fast, which a plain line of people cannot do without counting from the front.

## Operations

The state is a finite sequence $G = \langle x_1, \ldots, x_n \rangle$ in the order of arrival, so $x_1$ is the oldest. Positions start at 1, as in the usual statement of the type.

| operation | signature | result |
|---|---|---|
| new | $() \to G$ | $\langle\rangle$ |
| is_empty | $(G) \to \text{bool}$ | $n = 0$ |
| size | $(G) \to \mathbb{N}$ | $n$ |
| insert | $(G, x) \to G$ | $\langle x_1, \ldots, x_n, x \rangle$ |
| delete | $(G, k) \to (T, G)$ | $x_k$ and $\langle x_1, \ldots, x_{k-1}, x_{k+1}, \ldots, x_n \rangle$, for $1 \le k \le n$ |

Delete with $k$ out of range is an error. Some versions add `get(k)`, which returns $x_k$ without removing it.

## Laws

For each generalized queue $G$ of size $n$, each item $x$ and each $k$ with $1 \le k \le n$:

$$\begin{aligned}
&(\text{G1})\quad \text{size}(\text{new}()) = 0, \qquad \text{size}(\text{insert}(G, x)) = n + 1,\\
&(\text{G2})\quad \text{delete}(\text{insert}(G, x), n + 1) = (x, G),\\
&(\text{G3})\quad \text{if } \text{delete}(G, k) = (y, G'), \text{ then } \text{delete}(\text{insert}(G, x), k) = (y, \text{insert}(G', x)).
\end{aligned}$$

Law (G2) says the newest item is at position $n + 1$, and law (G3) says that a later insert does not move the older items. Together they compute every delete: by induction on the number of inserts, a delete either takes the newest item (G2) or is pushed down past it (G3). Deletes on terms that contain earlier deletes are computed from the resulting sequence, since every value of the type equals the term of inserts that spells its sequence.

**Special cases.**

- With every delete at $k = 1$, the laws become the laws of a [queue](/queue/): the item that leaves is always the oldest.
- With every delete at $k = n$, they become the laws of a [stack](/stack/): law (G2) is the stack law $\text{pop}(\text{push}(S, x)) = (x, S)$.
- With $k$ uniform in $\{1, \ldots, n\}$ and independent of the past, delete is the dequeue of a [randomized queue](/randomized-queue/). Since its order of service does not depend on the order of arrival, a randomized queue does not need the full type: it swaps the chosen item with the last one and removes it in $O(1)$ time.
- A [priority queue](/priority-queue/) also removes from the middle, but chooses by key, not by age.

## Implementations

| implementation | insert | delete($k$) | space |
|---|---|---|---|
| [dynamic array](/dynamic-array/), shift on delete | $O(1)$ amortized | $\Theta(n - k + 1)$ | $\Theta(n)$ |
| [linked list](/linked-list/) with a tail pointer | $O(1)$ | $\Theta(k)$ | $n$ nodes |
| [doubly linked list](/doubly-linked-list/), walk from the nearer end | $O(1)$ | $\Theta(\min(k, n - k + 1))$ | $n$ nodes |
| [order-statistic tree](/order-statistic-tree/) keyed by arrival time | $O(\log n)$ | $O(\log n)$ | $\Theta(n)$ |
| [implicit treap](/implicit-treap/) or other tree with subtree sizes | $O(\log n)$ expected | $O(\log n)$ expected | $\Theta(n)$ |
| [Fenwick tree](/fenwick-tree/) of 0/1 marks over at most $m$ arrival times | $O(\log m)$ | $O(\log m)$ | $\Theta(m)$ |

In the tree forms, each item gets an arrival number $t = 1, 2, 3, \ldots$ when it is inserted. Since arrival numbers only increase, insert is always at the right end of the tree. Delete($k$) is the select operation OS-SELECT of CLRS Section 17.1: walk down from the root and use the subtree sizes to find the $k$-th smallest arrival number.

The Fenwick form keeps a 0/1 array $M$ over the arrival numbers, with $M[t] = 1$ while the item of arrival $t$ is still present. Delete($k$) finds the least $t$ with $M[1] + \cdots + M[t] = k$ by a binary descent in the tree in $O(\log m)$ steps, then sets $M[t] = 0$. The bound $m$ on the number of inserts must be known in advance, or the tree must be rebuilt by doubling.

Sedgewick and Wayne pose the array and the linked-list versions as an exercise. A two-pointer trick does not help: the array version must shift, or leave a hole that later deletes must count, and counting the holes is what the Fenwick tree does in logarithmic time.

## References
