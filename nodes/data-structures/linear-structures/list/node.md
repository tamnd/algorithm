---
tag: Z9DNWF
kind: abstract-type
slug: list
name: List
aliases:
- sequence
- abstract list
area: data-structures/linear-structures
level: intro
summary: Ordered collection with positional access, insertion and deletion.
prereqs: [asymptotic-notation]
see_also: [array, dynamic-array, linked-list, doubly-linked-list, gap-buffer, rope, order-statistic-tree, stack]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2 (Linear lists), the list of operations at the start of the section, and Sections 2.2.2 and 2.2.3 for the sequential and linked representations
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 10 (Elementary data structures), Sections 10.1 and 10.2
  - paper: "Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of the 21st ACM Symposium on Theory of Computing (1989)"
    locator: the lower bound for list indexing and for dynamic prefix problems
  - paper: "Paul F. Dietz, Optimal algorithms for list indexing and subset rank, Workshop on Algorithms and Data Structures (WADS 1989), Lecture Notes in Computer Science 382 (1989)"
    locator: the upper bound of order log n / log log n for list indexing
---

A list is the abstract type of a finite sequence $\langle x_0, x_1, \ldots, x_{n-1} \rangle$ that a program reads and changes by position: it can get or set the item at position $i$, insert an item before position $i$, and delete the item at position $i$. The type fixes only what the operations do, not how fast they are, so its implementations make different trade-offs: an [array](/array/) reads by position in $O(1)$ time but inserts in $\Theta(n)$, a [linked list](/linked-list/) inserts at a held node in $O(1)$ but reaches position $i$ in $\Theta(i)$, and a balanced tree does both in $O(\log n)$. In the cell-probe model no implementation does all of them in $o(\log n / \log \log n)$ time.

## In plain words

A list is a row of items in a fixed order, like the lines of a text or the songs of a playlist. Each item has a position: the first, the second, and so on. You can ask for the item at a position, replace it, put a new item in between two others, or take an item out. When you put an item in or take one out, the items after it change their position by one, but their order stays the same.

The list type says only what these actions do. It does not say how the computer stores the row. Different ways of storing it make different actions fast, and the right choice depends on which actions a program uses most.

## Operations

A list over a set $T$ of items has as its state a finite sequence $L = \langle x_0, \ldots, x_{n-1} \rangle$ with $n \ge 0$. Positions start at 0.

| operation | signature | result |
|---|---|---|
| new | $() \to L$ | the empty list $\langle\rangle$ |
| length | $(L) \to \mathbb{N}$ | $n$ |
| get | $(L, i) \to T$ | $x_i$, for $0 \le i < n$ |
| set | $(L, i, x) \to L$ | $\langle x_0, \ldots, x_{i-1}, x, x_{i+1}, \ldots, x_{n-1} \rangle$, for $0 \le i < n$ |
| insert | $(L, i, x) \to L$ | $\langle x_0, \ldots, x_{i-1}, x, x_i, \ldots, x_{n-1} \rangle$, for $0 \le i \le n$ |
| delete | $(L, i) \to (T, L)$ | $x_i$ and $\langle x_0, \ldots, x_{i-1}, x_{i+1}, \ldots, x_{n-1} \rangle$, for $0 \le i < n$ |
| search | $(L, x) \to \mathbb{N} \cup \{\text{NIL}\}$ | the least $i$ with $x_i = x$, or NIL |

Insert at $i = n$ is *append*. Many libraries add iteration in order, concatenation and slicing, which are compositions of these operations. An implementation based on nodes also offers operations at a *position handle*, such as "insert after this node", which a pure index interface does not have.

## Laws

For each list $L$ of length $n$, each item $x$ and each index in the stated range:

$$\begin{aligned}
&(\text{L1})\quad \text{length}(\text{new}()) = 0, \qquad \text{length}(\text{insert}(L, i, x)) = n + 1 \quad (0 \le i \le n),\\
&(\text{L2})\quad \text{get}(\text{insert}(L, i, x), j) = \begin{cases} \text{get}(L, j) & j < i, \\ x & j = i, \\ \text{get}(L, j - 1) & i < j \le n, \end{cases}\\
&(\text{L3})\quad \text{delete}(\text{insert}(L, i, x), i) = (x, L),\\
&(\text{L4})\quad \text{length}(\text{set}(L, i, x)) = n, \qquad \text{get}(\text{set}(L, i, x), j) = \begin{cases} x & j = i, \\ \text{get}(L, j) & j \ne i, \end{cases}\\
&(\text{L5})\quad \text{if } \text{length}(L) = \text{length}(L') \text{ and } \text{get}(L, j) = \text{get}(L', j) \text{ for all } j, \text{ then } L = L'.
\end{aligned}$$

Law (L5) says that a list is determined by its length and its items, so two lists built in different ways are equal when they spell the same sequence. With (L5), law (L2) also fixes delete: for $0 \le i < n$, $\text{delete}(L, i)$ returns $\text{get}(L, i)$ and the list $L'$ of length $n - 1$ with $\text{get}(L', j) = \text{get}(L, j)$ for $j < i$ and $\text{get}(L, j + 1)$ for $j \ge i$.

**Every list is built by appends.** Each list $L = \langle x_0, \ldots, x_{n-1} \rangle$ equals $\text{insert}(\cdots\text{insert}(\text{new}(), 0, x_0)\cdots, n - 1, x_{n-1})$.

*Proof.* By induction on $n$. For $n = 0$ the list is $\text{new}()$ by (L1) and (L5). For $n \ge 1$, let $L'$ be the term for $\langle x_0, \ldots, x_{n-2} \rangle$, which exists by the induction hypothesis. By (L1), $\text{insert}(L', n - 1, x_{n-1})$ has length $n$. By (L2) with $i = n - 1$, its item at $j < n - 1$ is $\text{get}(L', j) = x_j$ and its item at $n - 1$ is $x_{n-1}$. By (L5) it equals $L$. $\square$

**Search.** $\text{search}(L, x) = i$ exactly when $\text{get}(L, i) = x$ and $\text{get}(L, j) \ne x$ for all $j < i$, and it is NIL exactly when no position holds $x$.

**Special cases.** A [stack](/stack/) is a list used only with insert and delete at position $n$ (or only at 0). A [queue](/queue/) inserts at $n$ and deletes at 0. A [deque](/deque/) uses both ends. These restrictions allow implementations with $O(1)$ time for each operation.

## Implementations

| implementation | get, set at $i$ | insert, delete at $i$ | insert, delete at the ends | space |
|---|---|---|---|---|
| [array](/array/), capacity $N$ | $\Theta(1)$ | $\Theta(n - i + 1)$ | $\Theta(1)$ at the back, $\Theta(n)$ at the front | $N$ |
| [dynamic array](/dynamic-array/) | $\Theta(1)$ | $\Theta(n - i + 1)$ amortized | $\Theta(1)$ amortized at the back | $\Theta(n)$ |
| [circular buffer](/circular-buffer/), growable | $\Theta(1)$ | $\Theta(\min(i, n - i) + 1)$ amortized | $\Theta(1)$ amortized at both | $\Theta(n)$ |
| [singly linked list](/singly-linked-list/) | $\Theta(i + 1)$ | $\Theta(i + 1)$; $\Theta(1)$ after a held node | $\Theta(1)$ at the front | $n$ nodes |
| [doubly linked list](/doubly-linked-list/) | $\Theta(\min(i, n - i) + 1)$ | the same; $\Theta(1)$ at a held node | $\Theta(1)$ at both | $n$ nodes |
| [gap buffer](/gap-buffer/) | $\Theta(1)$ | $\Theta(\lvert i - g \rvert + 1)$ amortized, $g$ the gap | as for a general $i$ | $\Theta(n)$ |
| [unrolled linked list](/unrolled-linked-list/), blocks of $B$ | $\Theta(n/B + 1)$ | $\Theta(n/B + B)$ | $\Theta(B)$ | $\Theta(n)$ |
| [rope](/rope/) or [order-statistic tree](/order-statistic-tree/) | $\Theta(\log n)$ | $\Theta(\log n)$ | $\Theta(\log n)$ | $\Theta(n)$ |

Search costs $\Theta(n)$ in each of them, since the list type keeps the order of insertion and not the order of the items. To search faster, a program keeps a separate index, such as a hash table from items to nodes.

## Lower bounds

In the [cell-probe model](/cell-probe-model/) with words of $\Theta(\log n)$ bits, Fredman and Saks (1989) proved that any implementation of a list with insert, delete and get by position needs $\Omega(\log n / \log \log n)$ amortized time per operation, for some sequences of operations. Dietz (1989) gave a structure that meets this bound. So the $\Theta(1)$ access of an array and the $\Theta(1)$ insert of a linked list cannot be combined: a structure that is fast at one of them is slow at the other, or both are $\Omega(\log n / \log \log n)$. Balanced trees reach $O(\log n)$, which is within a factor of $\log \log n$ of the bound.

## References
