---
tag: ND3TVB
kind: abstract-type
slug: priority-queue
name: Priority queue
aliases:
- PQ
- priority queue ADT
area: data-structures/heaps
level: intro
summary: Abstract collection supporting insert and extract-min (or extract-max).
prereqs: [queue, asymptotic-notation]
see_also: [binary-heap, heap, fibonacci-heap, pairing-heap, meldable-priority-queue, double-ended-priority-queue, heapsort, top-m-problem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 6.5 (Priority queues)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4 (Priority Queues), the API, the elementary implementations and the table of costs
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3 (Sorting by selection), the part on priority queues
  - paper: Mikkel Thorup, Equivalence between priority queues and sorting, Journal of the ACM 54(6), 2007
    locator: the main theorem, which turns a sorting algorithm on the word RAM into a priority queue
---

A priority queue is an abstract data type that holds a finite multiset of items with keys from a total order, and supports `insert` of an item and `extract-min`, which removes and returns an item with the smallest key. It is a [queue](/queue/) in which the order of removal is fixed by the keys and not by the order of arrival. The [binary heap](/binary-heap/) gives both operations in $O(\log n)$ time. Priority queues drive [Dijkstra's algorithm](/dijkstra/), [Prim's algorithm](/prim/), [Huffman coding](/huffman-coding/), [heapsort](/heapsort/), event simulation and the [top M](/top-m-problem/) items of a stream.

## In plain words

A hospital emergency room does not treat people in the order they arrive. Each patient gets a priority, and the doctor always takes the most urgent patient next. New patients come in at any time. A priority queue is this waiting room as a data type.

It has two main actions: add an item with its priority, and take out the item with the best priority. You can also look at the best item without taking it out, and ask how many items wait. Some versions let you change the priority of a waiting item, or join two waiting rooms into one. The type says only what these actions do. A heap, a sorted list or a search tree can build it, with different speeds.

## Operations

Let $(U, \le)$ be a totally ordered set of keys. An item is a pair of a key and some data, and we compare items by their keys only. A priority queue value $Q$ is a finite multiset of items. We write $|Q|$ for the number of items and $\min Q$ for the smallest key in $Q$ when $Q$ is not empty.

| operation | signature | what it does |
|---|---|---|
| `new` | $\text{new}() \to Q$ | the empty queue $\emptyset$ |
| `insert` | $\text{insert}(Q, x) \to Q$ | $Q$ becomes $Q \uplus \{x\}$ |
| `find-min` | $\text{find-min}(Q) \to x$ | for $Q \ne \emptyset$: returns an item $x \in Q$ with key $\min Q$, and does not change $Q$ |
| `extract-min` | $\text{extract-min}(Q) \to (x, Q)$ | for $Q \ne \emptyset$: returns an item $x$ with key $\min Q$, and $Q$ becomes $Q \setminus \{x\}$ |
| `is-empty` | $\text{is-empty}(Q) \to \text{bool}$ | true when $Q = \emptyset$ |
| `size` | $\text{size}(Q) \to \mathbb{N}$ | returns $|Q|$ |

Here $\uplus$ is the union of multisets, which keeps both copies of an item that occurs twice, and $Q \setminus \{x\}$ removes one copy of $x$. `find-min` and `extract-min` on the empty queue are errors. A *max-priority queue* has `find-max` and `extract-max` instead, with $\ge$ in place of $\le$. Each statement on this page holds for it with the order reversed.

**Optional operations.** Many uses need more than the base type. These operations need a *handle*: a reference to an item in the queue, which `insert` returns.

| operation | signature | what it does |
|---|---|---|
| `decrease-key` | $\text{decrease-key}(Q, h, k) \to Q$ | for $k \le$ the key of the item $h$: sets the key of $h$ to $k$ |
| `delete` | $\text{delete}(Q, h) \to Q$ | removes the item $h$ |
| `meld` | $\text{meld}(Q_1, Q_2) \to Q$ | returns $Q_1 \uplus Q_2$; the inputs are used up |

[Decrease-key](/decrease-key/) is the step of Dijkstra's and Prim's algorithms that lowers the distance of a vertex. A queue with `meld` is a [meldable priority queue](/meldable-priority-queue/). A queue with both `find-min` and `find-max` is a [double-ended priority queue](/double-ended-priority-queue/). An [indexed priority queue](/indexed-priority-queue/) uses small integers as the handles.

### Example

Start with the empty queue. The keys are integers, and the multiset is written in sorted order.

| step | operation | result | queue after |
|---|---|---|---|
| 1 | insert 5 | | $\{5\}$ |
| 2 | insert 2 | | $\{2, 5\}$ |
| 3 | insert 8 | | $\{2, 5, 8\}$ |
| 4 | extract-min | 2 | $\{5, 8\}$ |
| 5 | insert 1 | | $\{1, 5, 8\}$ |
| 6 | find-min | 1 | $\{1, 5, 8\}$ |
| 7 | extract-min | 1 | $\{5, 8\}$ |
| 8 | extract-min | 5 | $\{8\}$ |
| 9 | insert 7 | | $\{7, 8\}$ |
| 10 | extract-min | 7 | $\{8\}$ |
| 11 | extract-min | 8 | $\emptyset$ |

The item 1 arrives at step 5, after 5 and 8, and it leaves first. The item 8 arrives at step 3 and leaves last. A first-in first-out queue would return 5, 2, 8, 1, 7 in that order.

## Laws

Each implementation meets these equations, for each queue $Q$ and items $x, y$. In (P4) the queue $Q$ is not empty, and in (P5) the queue $R$ is not empty.

$$\begin{aligned}
&(\text{P1})\quad \text{is-empty}(\text{new}()) = \text{true}, \qquad (\text{P2})\quad \text{is-empty}(\text{insert}(Q, x)) = \text{false},\\
&(\text{P3})\quad \text{insert}(\text{insert}(Q, x), y) = \text{insert}(\text{insert}(Q, y), x),\\
&(\text{P4})\quad \text{key}(\text{find-min}(\text{insert}(Q, x))) = \min(\text{key}(x), \min Q), \qquad \text{key}(\text{find-min}(\text{insert}(\text{new}(), x))) = \text{key}(x),\\
&(\text{P5})\quad (z, R') = \text{extract-min}(R) \implies \text{insert}(R', z) = R \text{ and } \text{key}(z) = \text{key}(\text{find-min}(R)),\\
&(\text{P6})\quad \text{size}(\text{new}()) = 0, \qquad \text{size}(\text{insert}(Q, x)) = \text{size}(Q) + 1.
\end{aligned}$$

Each law holds in the multiset meaning of the table above. For (P3), both sides are $Q \uplus \{x, y\}$. For (P4), the smallest key of $Q \uplus \{x\}$ is the smaller of $\text{key}(x)$ and $\min Q$. For (P5), extract-min removes one copy of an item $z$ of smallest key, and putting $z$ back gives $R$ again. Conversely, two implementations that meet the laws give the same keys for each sequence of operations, because by (P5) the value after each extract-min is the old multiset less one item of smallest key.

Law (P3) says that the order of the inserts does not matter: a queue is a multiset, not a sequence. Law (P5) fixes the key of the item that comes out, but not the item itself. When two items share the smallest key, an implementation may return either one. So a priority queue is not *stable*: of two items with equal keys, the one inserted first need not come out first. To get first-in first-out order among equal keys, use the pair (key, insertion counter) as the key, compared in lexicographic order.

**Order of removal.** If $x$ and $y$ are both in the queue and $\text{key}(x) < \text{key}(y)$, then $x$ comes out before $y$. *Proof.* While $x$ is in the queue, $\min Q \le \text{key}(x) < \text{key}(y)$, so by (P5) no extract-min returns $y$. $\square$

**Sorting by a priority queue.** Insert $n$ items, then call extract-min $n$ times. By (P5), each extract-min returns an item of smallest key among the items that are left, so the outputs come in non-decreasing order of keys. With a binary heap this is [heapsort](/heapsort/). With an unsorted list it is [selection sort](/selection-sort/), and with a sorted list it is [insertion sort](/insertion-sort/).

## Implementations

| implementation | insert | find-min | extract-min | decrease-key | meld |
|---|---|---|---|---|---|
| unsorted [array](/array/) or list | $\Theta(1)$ | $\Theta(n)$ | $\Theta(n)$ | $\Theta(1)$ | $\Theta(1)$ (list) |
| sorted array or list | $\Theta(n)$ | $\Theta(1)$ | $\Theta(1)$ | $\Theta(n)$ | $\Theta(n)$ |
| [binary heap](/binary-heap/) | $O(\log n)$ | $\Theta(1)$ | $O(\log n)$ | $O(\log n)$ | $\Theta(n)$ |
| [d-ary heap](/d-ary-heap/) | $O(\log_d n)$ | $\Theta(1)$ | $O(d \log_d n)$ | $O(\log_d n)$ | $\Theta(n)$ |
| [leftist heap](/leftist-heap/) | $O(\log n)$ | $\Theta(1)$ | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ |
| [skew heap](/skew-heap/) | $O(\log n)$ amortized | $\Theta(1)$ | $O(\log n)$ amortized | | $O(\log n)$ amortized |
| [binomial heap](/binomial-heap/) | $O(1)$ amortized, $O(\log n)$ worst | $O(\log n)$, or $O(1)$ with a pointer | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ |
| [pairing heap](/pairing-heap/) | $O(1)$ | $\Theta(1)$ | $O(\log n)$ amortized | $o(\log n)$ amortized, not $O(1)$ | $O(1)$ |
| [Fibonacci heap](/fibonacci-heap/) | $O(1)$ | $\Theta(1)$ | $O(\log n)$ amortized | $O(1)$ amortized | $O(1)$ |
| [strict Fibonacci heap](/strict-fibonacci-heap/), [Brodal queue](/brodal-queue/) | $O(1)$ | $O(1)$ | $O(\log n)$ | $O(1)$ | $O(1)$ |
| [balanced search tree](/balanced-binary-search-tree/) | $O(\log n)$ | $O(1)$ with a pointer | $O(\log n)$ | $O(\log n)$ | $O(n)$ in general |
| [bucket queue](/bucket-queue/), keys in $\{0, \ldots, C\}$ | $O(1)$ | $O(C)$ | $O(C)$ | $O(1)$ | |
| [radix heap](/radix-heap/), monotone integer keys up to $C$ | $O(\log C)$ amortized | | $O(\log C)$ amortized, $O(1)$ with a word of flags | $O(1)$ amortized | |

The costs are worst case unless the table says otherwise; $n$ is the number of items. The bounds for the pairing heap are those of the [pairing heap](/pairing-heap/) page. The bucket queue and the radix heap are not comparison-based, and the radix heap needs the extracted keys to never decrease. A plain binary heap has no meld faster than building a new heap from both arrays in $\Theta(n)$ time.

For a small $n$, or for a program that inserts many items and extracts few, the unsorted list is often the fastest. For the general case, the binary heap in an array is the usual choice of the standard libraries: `heapq` of Python, `PriorityQueue` of Java and `std::priority_queue` of C++. The heaps with $O(1)$ decrease-key matter in theory for Dijkstra's algorithm on dense graphs, where they give $O(m + n \log n)$ time.

## Lower bounds

**Comparison model.** In the [comparison model](/comparison-model/), each priority queue needs $\Omega(\log n)$ amortized time per operation for some mix of insert and extract-min. The reason is the sort above: $n$ inserts followed by $n$ extract-mins sort $n$ items, and each comparison sort needs at least $\lceil \lg(n!) \rceil$ comparisons in the worst case (see the [comparison sort lower bound](/comparison-sort-lower-bound/)). Since $\lg(n!) = n \lg n - n \lg e + O(\log n)$, the $2n$ operations need $n \lg n - O(n)$ comparisons together, so the amortized cost of an insert plus an extract-min is at least $\lg n - O(1)$. For $n = 1000$ this is $\lceil \lg 1000! \rceil = 8530$ comparisons for 2000 operations.

The bound puts no limit on each operation alone. A Fibonacci heap does insert, find-min, meld and decrease-key in $O(1)$ amortized time. Then extract-min must pay: it costs $\Omega(\log n)$ amortized in each comparison-based queue with $O(1)$ amortized insert.

**Word RAM.** For integer keys on the [word RAM](/word-ram/) the comparison bound does not apply. Thorup proved that a priority queue and sorting are equivalent there: if $n$ keys can be sorted in $n \cdot S(n)$ time, then a priority queue can do insert and extract-min in $O(S(n))$ time per operation, and the converse is the sort above. With the integer sorting algorithms known today, this gives $O(\log \log n)$ time per operation.

## References
