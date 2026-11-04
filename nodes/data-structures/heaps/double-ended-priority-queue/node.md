---
tag: 9MCHAX
kind: abstract-type
slug: double-ended-priority-queue
name: Double-ended priority queue
aliases:
- DEPQ
- double-ended heap
area: data-structures/heaps
level: core
summary: Priority queue supporting extraction of both the minimum and the maximum.
prereqs: [priority-queue, total-order]
see_also: [priority-queue, min-max-heap, interval-heap, deap, balanced-binary-search-tree, deque, comparison-sort-lower-bound, beam-search]
sources:
  - book: isbn:9781584884354
    title: Dinesh P. Mehta and Sartaj Sahni (editors), Handbook of Data Structures and Applications
    locator: the chapter Double-ended priority queues, by Sartaj Sahni
  - paper: "M. D. Atkinson, J.-R. Sack, N. Santoro and Th. Strothotte, Min-max heaps and generalized priority queues, Communications of the ACM 29(10), 1986"
    locator: the definition of the double-ended priority queue and the min-max heap
  - paper: "Svante Carlsson, The deap, a double-ended heap to implement double-ended priority queues, Information Processing Letters 26(1), 1987"
    locator: the whole paper
  - paper: "Jan van Leeuwen and Derick Wood, Interval heaps, The Computer Journal 36(3), 1993"
    locator: the whole paper
  - paper: "Ira Pohl, A sorting problem and its complexity, Communications of the ACM 15(6), 1972"
    locator: the bound of 3n/2 minus 2 comparisons to find both the minimum and the maximum
---

A double-ended priority queue, or DEPQ, is an abstract data type that holds a finite multiset of items with keys from a [total order](/total-order/), and supports `insert`, `find-min`, `find-max`, `extract-min` and `extract-max`. It is a [priority queue](/priority-queue/) that can be served from both ends, as a [deque](/deque/) is a queue that can be served from both ends. A balanced search tree gives each operation in $O(\log n)$ time, and the array structures made for it, the [min-max heap](/min-max-heap/), the [deap](/deap/) and the [interval heap](/interval-heap/), give $O(1)$ for the two finds and $O(\log n)$ for the other operations, in place and with small constants. It is used to keep the best $k$ items of a stream, to run branch and bound or [beam search](/beam-search/) with a memory limit, and in external sorting.

## In plain words

A normal priority queue lets you take out only the smallest item, or only the largest. Sometimes you need both. Think of a list of job applicants that you must keep short: you always want the best one next, and when the list is too long, you drop the worst one.

A double-ended priority queue holds a group of items with keys and lets you look at or take out the smallest and the largest, and add new items at any time. Two separate heaps do not work well, because an item taken out of one heap is still in the other. The structures for this type keep one shared set of items with quick access to both ends.

## Operations

Let $(U, \le)$ be a totally ordered set of keys. A DEPQ value $Q$ is a finite multiset of items, compared by their keys. Write $\min Q$ and $\max Q$ for the smallest and the largest key when $Q$ is not empty.

| operation | signature | what it does |
|---|---|---|
| `new` | $\text{new}() \to Q$ | the empty queue $\emptyset$ |
| `insert` | $\text{insert}(Q, x) \to Q$ | $Q$ becomes $Q \uplus \{x\}$ |
| `find-min` | $\text{find-min}(Q) \to x$ | for $Q \ne \emptyset$: an item with key $\min Q$; $Q$ does not change |
| `find-max` | $\text{find-max}(Q) \to x$ | for $Q \ne \emptyset$: an item with key $\max Q$; $Q$ does not change |
| `extract-min` | $\text{extract-min}(Q) \to (x, Q)$ | for $Q \ne \emptyset$: an item $x$ with key $\min Q$, and $Q$ becomes $Q \setminus \{x\}$ |
| `extract-max` | $\text{extract-max}(Q) \to (x, Q)$ | for $Q \ne \emptyset$: an item $x$ with key $\max Q$, and $Q$ becomes $Q \setminus \{x\}$ |
| `size` | $\text{size}(Q) \to \mathbb{N}$ | returns $|Q|$ |

The finds and extracts on the empty queue are errors. Some uses also need `meld`, or `delete` and `change-key` through a handle, as for a plain priority queue.

### Example

Start with the empty queue. The multiset is written in sorted order.

| step | operation | result | queue after |
|---|---|---|---|
| 1 | insert 5, 2, 8, 6 | | $\{2, 5, 6, 8\}$ |
| 2 | extract-max | 8 | $\{2, 5, 6\}$ |
| 3 | extract-min | 2 | $\{5, 6\}$ |
| 4 | insert 1 | | $\{1, 5, 6\}$ |
| 5 | find-max | 6 | $\{1, 5, 6\}$ |
| 6 | extract-max | 6 | $\{1, 5\}$ |
| 7 | extract-max | 5 | $\{1\}$ |
| 8 | find-min, find-max | 1, 1 | $\{1\}$ |

With one item left, the minimum and the maximum are the same item.

## Laws

For each queue $Q$ and items $x, y$, with the laws (P1) to (P6) of the [priority queue](/priority-queue/) for `insert`, `find-min`, `extract-min` and `size`, and in (D3) and (D4) the queue $R$ not empty:

$$\begin{aligned}
&(\text{D1})\quad \text{key}(\text{find-max}(\text{insert}(Q, x))) = \max(\text{key}(x), \max Q), \qquad \text{key}(\text{find-max}(\text{insert}(\text{new}(), x))) = \text{key}(x),\\
&(\text{D2})\quad (z, R') = \text{extract-max}(R) \implies \text{insert}(R', z) = R \text{ and } \text{key}(z) = \text{key}(\text{find-max}(R)),\\
&(\text{D3})\quad \text{key}(\text{find-min}(R)) \le \text{key}(\text{find-max}(R)),\\
&(\text{D4})\quad \text{size}(R) = 1 \implies \text{key}(\text{find-min}(R)) = \text{key}(\text{find-max}(R)).
\end{aligned}$$

(D1) and (D2) are the max laws of a max-priority queue, and they hold on the same value $Q$ as the min laws: the two ends see one multiset. (D3) and (D4) follow from the multiset meaning. With the laws, every sequence of operations gives the same keys in every implementation, since each extract removes one item of the extreme key on its side.

**Bounded queue.** To keep the $k$ smallest keys of a stream, insert each key, and when the size becomes $k + 1$, call `extract-max`. After each step the queue holds the $k$ smallest keys seen so far: an extracted key is larger than $k$ other keys, so it is not among the $k$ smallest, and it stays so as more keys arrive. A max-heap alone also does this; the DEPQ adds `find-min` and `extract-min` for the best key at any time.

**Sorting from both ends.** Insert $n$ items, then alternate `extract-min` and `extract-max`. The outputs fill the sorted order from both ends at once.

## Implementations

| implementation | insert | find-min, find-max | extract-min, extract-max | notes |
|---|---|---|---|---|
| unsorted array | $\Theta(1)$ | $\Theta(n)$ | $\Theta(n)$ | |
| sorted array | $\Theta(n)$ | $\Theta(1)$ | $\Theta(1)$ | extract from both ends with two indices |
| [balanced search tree](/balanced-binary-search-tree/) | $O(\log n)$ | $O(1)$ with pointers to the ends | $O(\log n)$ | also supports search and delete of any key |
| [min-max heap](/min-max-heap/) | $O(\log n)$ | $O(1)$ | $O(\log n)$ | one array; min levels and max levels alternate |
| [deap](/deap/) | $O(\log n)$ | $O(1)$ | $O(\log n)$ | one array; an empty root, a min-heap on the left, a max-heap on the right |
| [interval heap](/interval-heap/) | $O(\log n)$ | $O(1)$ | $O(\log n)$ | one array; each node holds two keys, an interval |
| two heaps with a correspondence | $O(\log n)$ | $O(1)$ | $O(\log n)$ | a min-heap and a max-heap, each item linked to its twin |
| two heaps with [lazy deletion](/lazy-deletion/) | $O(\log n)$ | $O(1)$ amortized | $O(\log n)$ amortized | dead entries are skipped at the root |

The times are worst case unless marked. The three array structures are in place, need no pointers, and are built in $O(n)$ time from $n$ keys. Of them, the interval heap is the simplest to code and has the shortest paths, since its tree has about $n/2$ nodes. Melding needs other structures, for example two [leftist heaps](/leftist-heap/) with links between twins.

## Lower bounds

**Comparison model.** A DEPQ is a priority queue with more operations, so the bound of the [priority queue](/priority-queue/) carries over: some mix of `insert` and `extract-min` costs $\Omega(\log n)$ amortized comparisons per operation, because $n$ inserts and $n$ extracts sort $n$ keys, see the [comparison sort lower bound](/comparison-sort-lower-bound/).

**Both ends at once.** After $n$ inserts, a `find-min` and a `find-max` together give the smallest and the largest of $n$ keys. Pohl (1972) showed that this needs at least $\lceil 3n/2 \rceil - 2$ comparisons in the worst case, and that this many suffice. So a DEPQ whose finds make no comparisons must spend at least $\lceil 3n/2 \rceil - 2$ comparisons over the $n$ inserts or the build, which is more than the $n - 1$ that finding only the minimum needs. The pairing of the keys in an interval heap is the same idea as Pohl's algorithm: compare the keys in pairs, then the smaller ones for the minimum and the larger ones for the maximum.

## References
