---
tag: QWB7ME
kind: abstract-type
slug: meldable-priority-queue
name: Meldable priority queue
aliases:
- mergeable heap
- mergeable priority queue
area: data-structures/heaps
level: core
summary: Priority queue that also supports merging two queues into one.
prereqs: [priority-queue, asymptotic-notation]
see_also: [leftist-heap, skew-heap, binomial-heap, pairing-heap, fibonacci-heap, brodal-queue, strict-fibonacci-heap, randomized-heap]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: the introduction to Chapter 19 (Fibonacci Heaps), which defines mergeable heaps and compares binary heaps with Fibonacci heaps
  - book: isbn:9780898711875
    title: Robert Endre Tarjan, Data Structures and Network Algorithms, SIAM, 1983
    locator: Chapter 3 (Heaps), the operations of a heap including meld
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3 (Sorting by selection), the part on merging priority queues
  - paper: Gerth Stølting Brodal, Worst-case efficient priority queues, Proceedings of the 7th ACM-SIAM Symposium on Discrete Algorithms (SODA), 1996
    locator: the main theorem, O(1) worst-case meld, insert, find-min and decrease-key with O(log n) delete-min
  - paper: David Cheriton and Robert Endre Tarjan, Finding minimum spanning trees, SIAM Journal on Computing 5(4), 1976
    locator: the use of mergeable heaps of edges in the minimum spanning tree algorithm
---

A meldable priority queue, also called a mergeable heap, is a [priority queue](/priority-queue/) with one more operation, `meld`, which joins two queues into one queue that holds the items of both. The array [binary heap](/binary-heap/) cannot meld fast, because the two arrays must be copied into one. Pointer-based heaps can: the [leftist heap](/leftist-heap/) and the [binomial heap](/binomial-heap/) meld in $O(\log n)$ worst-case time, and the [pairing heap](/pairing-heap/), the [Fibonacci heap](/fibonacci-heap/) and the [Brodal queue](/brodal-queue/) in $O(1)$. Meld is needed when sets of candidates merge, as in some algorithms for minimum spanning trees, and it is the base operation from which many heaps build insert and delete-min.

## In plain words

A priority queue is a waiting line in which the most urgent item always goes first. A meldable priority queue lets you also take two such lines and make one line from them, with no item lost, and with the most urgent item of both at the front.

Think of two hospitals that close one ward and move all its patients to the other. The joined ward still needs to know, at any time, who is the most urgent patient. A good meldable queue does this join with little work, without sorting all patients again.

## Operations

The type holds a finite multiset of items, each with a key from a total order. A queue is an object; meld takes two of them.

| operation | result |
|---|---|
| `make-heap()` | a new empty queue |
| `insert(Q, x)` | adds the item $x$ to $Q$; returns a handle to it |
| `find-min(Q)` | an item of smallest key in $Q$; $Q$ is not empty |
| `delete-min(Q)` | removes and returns an item of smallest key; $Q$ is not empty |
| `meld(Q1, Q2)` | a queue with the items of $Q_1$ and of $Q_2$; $Q_1$ and $Q_2$ are not used after it |
| `is-empty(Q)`, `size(Q)` | as for a priority queue |
| `decrease-key(Q, h, k)` | optional: makes the key of the item with handle $h$ equal to $k \le$ its key |
| `delete(Q, h)` | optional: removes the item with handle $h$ |

CLRS calls meld `UNION`. Most structures make meld *destructive*: the two input queues share nodes with the result, so they must not be used again. A persistent version, in which the inputs stay valid, is possible with a [purely functional](/purely-functional-data-structure/) [leftist heap](/leftist-heap/) or skew heap.

**Insert from meld.** `insert(Q, x)` is `meld(Q, single(x))`, where `single(x)` is a queue of one item. The leftist, skew and pairing heaps define insert in this way.

**Delete-min from meld.** In tree-based heaps, the root holds the minimum, and delete-min removes the root and melds its subtrees. The heaps differ in how they meld these subtrees: two of them in a leftist heap, a linear number with pairing in a pairing heap, and by rank in a binomial or Fibonacci heap.

### Example

Let $Q_1$ hold the keys 5, 9, 2 and $Q_2$ hold the keys 7, 1, 8.

| step | operation | result | $Q$ after, as a multiset |
|---|---|---|---|
| 1 | `find-min(Q1)` | 2 | $Q_1 = \{2, 5, 9\}$ |
| 2 | `find-min(Q2)` | 1 | $Q_2 = \{1, 7, 8\}$ |
| 3 | `Q ← meld(Q1, Q2)` | | $Q = \{1, 2, 5, 7, 8, 9\}$ |
| 4 | `find-min(Q)` | 1 | $Q = \{1, 2, 5, 7, 8, 9\}$ |
| 5 | `delete-min(Q)` | 1 | $Q = \{2, 5, 7, 8, 9\}$ |
| 6 | `insert(Q, 3)` | | $Q = \{2, 3, 5, 7, 8, 9\}$ |
| 7 | `delete-min(Q)`, twice | 2, then 3 | $Q = \{5, 7, 8, 9\}$ |

Step 4 follows from the laws below: the minimum of the meld is the smaller of the two minima of steps 1 and 2. After step 3, $Q_1$ and $Q_2$ are no longer valid queues.

## Laws

Write $C(Q)$ for the multiset of items of $Q$, $\uplus$ for the union of multisets, and $\emptyset$ for the result of `make-heap()`. The laws of the [priority queue](/priority-queue/) hold, and also:

- **(M1) Contents.** $C(\mathrm{meld}(Q_1, Q_2)) = C(Q_1) \uplus C(Q_2)$.
- **(M2) Identity.** $C(\mathrm{meld}(\emptyset, Q)) = C(\mathrm{meld}(Q, \emptyset)) = C(Q)$.
- **(M3) Commutative and associative.** $C(\mathrm{meld}(Q_1, Q_2)) = C(\mathrm{meld}(Q_2, Q_1))$, and $C(\mathrm{meld}(\mathrm{meld}(Q_1, Q_2), Q_3)) = C(\mathrm{meld}(Q_1, \mathrm{meld}(Q_2, Q_3)))$.
- **(M4) Minimum.** If $Q_1$ and $Q_2$ are not both empty, then the key of $\mathrm{find\text{-}min}(\mathrm{meld}(Q_1, Q_2))$ is the smaller of the keys of the minima of the nonempty ones.
- **(M5) Insert.** $C(\mathrm{insert}(Q, x)) = C(\mathrm{meld}(Q, \mathrm{single}(x)))$.
- **(M6) Handles.** A handle returned by insert on $Q_1$ or $Q_2$ stays valid for the result of a meld, until its item is deleted.

M2 and M3 follow from M1, because $\uplus$ is commutative and associative with identity $\emptyset$. M4 follows from M1 and the law of find-min: the smallest key of a union of two multisets is the smaller of their smallest keys. The laws state equal *contents*, not equal structure: two melds in a different order usually give different trees, and when keys are equal, find-min may return a different item.

A consequence of M1 and the priority queue laws: if $Q$ is the meld of $Q_1, \dots, Q_k$, then the sequence of keys that repeated delete-min returns from $Q$ is the sorted merge of the sequences that it returns from each $Q_i$. So a meldable queue can do a [k-way merge](/k-way-merge/) of sorted lists.

## Implementations

Bounds are worst case unless marked "am." for amortized or "exp." for expected. The value $n$ is the number of items after the operation.

| structure | insert | find-min | delete-min | meld | decrease-key |
|---|---|---|---|---|---|
| [binary heap](/binary-heap/) in an array | $O(\log n)$ | $O(1)$ | $O(\log n)$ | $\Theta(n)$ | $O(\log n)$ |
| [leftist heap](/leftist-heap/) | $O(\log n)$ | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ with parent pointers |
| [skew heap](/skew-heap/) | $O(\log n)$ am. | $O(1)$ | $O(\log n)$ am. | $O(\log n)$ am. | |
| [randomized heap](/randomized-heap/) | $O(\log n)$ exp. | $O(1)$ | $O(\log n)$ exp. | $O(\log n)$ exp. | $O(\log n)$ exp. |
| [binomial heap](/binomial-heap/) | $O(1)$ am., $O(\log n)$ | $O(1)$ with a min pointer | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ |
| [pairing heap](/pairing-heap/) | $O(1)$ | $O(1)$ | $O(\log n)$ am. | $O(1)$ | $o(\log n)$ am. |
| [Fibonacci heap](/fibonacci-heap/) | $O(1)$ | $O(1)$ | $O(\log n)$ am. | $O(1)$ | $O(1)$ am. |
| [rank-pairing heap](/rank-pairing-heap/), [hollow heap](/hollow-heap/) | $O(1)$ | $O(1)$ | $O(\log n)$ am. | $O(1)$ | $O(1)$ am. |
| [Brodal queue](/brodal-queue/), [strict Fibonacci heap](/strict-fibonacci-heap/) | $O(1)$ | $O(1)$ | $O(\log n)$ | $O(1)$ | $O(1)$ |

**Where meld is used.** Cheriton and Tarjan's 1976 algorithm for [minimum spanning trees](/minimum-spanning-tree/) keeps, for each tree of the forest, a heap of the edges that leave it, and melds the heaps when two trees join. Algorithms that contract parts of a graph, such as those for minimum branchings, do the same. A [k-way merge](/k-way-merge/) can meld the $k$ heaps of the lists. A purely functional meldable heap also gives persistent priority queues, which share structure between versions.

## Lower bounds

**Delete-min must cost $\Omega(\log n)$ in the comparison model if insert is fast.** With $n$ inserts and $n$ delete-mins, any priority queue sorts $n$ keys. In the [comparison model](/comparison-model/), [sorting needs](/comparison-sort-lower-bound/) $\lg(n!) = n \lg n - O(n)$ comparisons. So if insert and meld take $O(1)$ amortized comparisons, delete-min must take $\Omega(\log n)$ amortized comparisons. The Brodal queue and the strict Fibonacci heap meet this bound with $O(1)$ worst-case meld and $O(\log n)$ worst-case delete-min, so they are optimal in this model.

**Arrays.** An implicit heap stored in one array, such as the binary heap, keeps its items in fixed slots. To meld, the items of one array must move into the other, which takes $\Omega(\min(n_1, n_2))$ moves for two arrays of sizes $n_1$ and $n_2$ that are stored apart. This is why every fast meldable queue uses pointers.

## References
