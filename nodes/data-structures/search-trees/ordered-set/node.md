---
tag: 0J86VT
kind: abstract-type
slug: ordered-set
name: Ordered set
aliases:
- ordered dictionary
- sorted set
area: data-structures/search-trees
level: core
summary: Dictionary extended with min, max, predecessor, successor, rank and select.
prereqs: [dictionary, total-order]
see_also: [ordered-symbol-table, binary-search-tree, floor-and-ceiling-in-ordered-set, predecessor-problem, order-statistic-tree, skip-list, red-black-tree, priority-queue]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: the introduction to Part III (operations on dynamic sets), Chapter 12, and Section 17.1 (dynamic order statistics)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.1 (Symbol tables), ordered operations
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.1 (minimum-comparison sorting), the lower bound on comparisons
---

An ordered set is a [dictionary](/dictionary/) of keys from a [total order](/total-order/) that also answers questions about the order: the minimum and the maximum, the predecessor and the successor of a key, and the [rank](/rank/) of a key and the key of a given rank. These are the operations on dynamic sets of CLRS, Part III, with rank and select added. Balanced search trees such as the [red-black tree](/red-black-tree/) give each operation in $O(\log n)$ time, and in the [comparison model](/comparison-model/) no structure does better by more than a constant factor.

## In plain words

An ordered set is a box of distinct items that can be lined up from smallest to largest. You can add an item, remove one, and ask if one is there. Because the items have an order, you can also ask which item is first and which is last, which item comes just before or just after a given one, at which position an item stands in the line, and which item stands at a given position.

A set that only answers "is it there?" can be faster, as a hash table is. The ordered set gives up a little speed to answer all the order questions too.

## Operations

Let $(K, <)$ be a total order. A value of the type is a finite set $S \subseteq K$ with $n = |S|$. NIL is not in $K$.

| operation | signature | meaning |
|---|---|---|
| `insert` | `(S, k) → S` | $S \cup \{k\}$ |
| `delete` | `(S, k) → S` | $S \setminus \{k\}$ |
| `contains` | `(S, k) → bool` | $k \in S$ |
| `size` | `(S) → ℕ` | $n$ |
| `min`, `max` | `(S) → K ∪ {NIL}` | $\min S$, $\max S$ |
| `predecessor` | `(S, k) → K ∪ {NIL}` | $\max\{s \in S : s < k\}$ |
| `successor` | `(S, k) → K ∪ {NIL}` | $\min\{s \in S : s > k\}$ |
| `floor`, `ceiling` | `(S, k) → K ∪ {NIL}` | $\max\{s \in S : s \le k\}$, $\min\{s \in S : s \ge k\}$ |
| `rank` | `(S, k) → ℕ` | $\lvert\{s \in S : s < k\}\rvert$ |
| `select` | `(S, i) → K` | the element of rank $i$, for $0 \le i < n$ |
| `iterate` | `(S) → sequence of K` | the elements in increasing order |

The maximum or minimum of an empty set is NIL. In CLRS, PREDECESSOR and SUCCESSOR take an element of the set; here they take any key of $K$, which makes them the queries of [floor and ceiling in an ordered set](/floor-and-ceiling-in-ordered-set/). Some texts define rank as the number of elements $\le k$ or count from 1; the laws below fix the 0-based form. An [ordered symbol table](/ordered-symbol-table/) is an ordered set with a value for each key.

## Laws

For all $S$, all $k, k' \in K$ and all integers $0 \le i < n$:

1. $\mathrm{contains}(\mathrm{insert}(S, k), k') = (k' = k \text{ or } \mathrm{contains}(S, k'))$, and $\mathrm{contains}(\mathrm{delete}(S, k), k') = (k' \ne k \text{ and } \mathrm{contains}(S, k'))$. These are the laws of a set.
2. $\mathrm{size}(\mathrm{insert}(S, k)) = n + [k \notin S]$ and $\mathrm{size}(\mathrm{delete}(S, k)) = n - [k \in S]$.
3. $\mathrm{rank}(S, \mathrm{select}(S, i)) = i$, and $\mathrm{select}(S, \mathrm{rank}(S, s)) = s$ for each $s \in S$.
4. $\mathrm{min}(S) = \mathrm{select}(S, 0)$ and $\mathrm{max}(S) = \mathrm{select}(S, n - 1)$ for $n \ge 1$.
5. For $s = \mathrm{select}(S, i)$: $\mathrm{successor}(S, s) = \mathrm{select}(S, i + 1)$ if $i + 1 < n$, else NIL; and $\mathrm{predecessor}(S, s) = \mathrm{select}(S, i - 1)$ if $i \ge 1$, else NIL.
6. $\mathrm{predecessor}(S, k) = \mathrm{select}(S, \mathrm{rank}(S, k) - 1)$ if $\mathrm{rank}(S, k) \ge 1$, else NIL.
7. $\mathrm{floor}(S, k) = k$ if $k \in S$, else $\mathrm{predecessor}(S, k)$; and $\mathrm{ceiling}(S, k) = k$ if $k \in S$, else $\mathrm{successor}(S, k)$.
8. $\mathrm{iterate}(S) = (\mathrm{select}(S, 0), \ldots, \mathrm{select}(S, n - 1))$, a strictly increasing sequence.
9. $\mathrm{rank}(S, k) \le \mathrm{rank}(S, k')$ whenever $k \le k'$.

Here $[P]$ is 1 if $P$ holds and 0 otherwise.

*Proof of laws 3 to 6.* List $S$ as $s_0 < s_1 < \cdots < s_{n-1}$. The elements smaller than $s_i$ are $s_0, \ldots, s_{i-1}$, so $\mathrm{rank}(S, s_i) = i$ and $\mathrm{select}(S, i) = s_i$; this gives laws 3 and 4. The elements larger than $s_i$ are $s_{i+1}, \ldots$, and the smallest of them is $s_{i+1}$, which gives law 5. For law 6 let $r = \mathrm{rank}(S, k)$: the elements smaller than $k$ are exactly $s_0, \ldots, s_{r-1}$, because the list is sorted, and the largest is $s_{r-1}$. $\square$

## Implementations

Costs for a set of $n$ keys. "Sizes" means that each node stores the size of its subtree, as in an [order statistic tree](/order-statistic-tree/).

| implementation | insert, delete | contains, predecessor, successor | min, max | rank, select | iterate |
|---|---|---|---|---|---|
| sorted array | $O(n)$ | $O(\log n)$ | $O(1)$ | $O(\log n)$, $O(1)$ | $O(n)$ |
| [binary search tree](/binary-search-tree/) | $O(h)$ | $O(h)$ | $O(h)$ | $O(h)$ with sizes | $O(n)$ |
| [red-black tree](/red-black-tree/), [AVL tree](/avl-tree/) | $O(\log n)$ worst | $O(\log n)$ worst | $O(\log n)$ | $O(\log n)$ with sizes | $O(n)$ |
| [treap](/treap/) | $O(\log n)$ expected | $O(\log n)$ expected | $O(\log n)$ expected | $O(\log n)$ expected with sizes | $O(n)$ |
| [skip list](/skip-list/) | $O(\log n)$ expected | $O(\log n)$ expected | $O(1)$, $O(\log n)$ expected | $O(\log n)$ expected with widths | $O(n)$ |
| [splay tree](/splay-tree/) | $O(\log n)$ amortized | $O(\log n)$ amortized | $O(\log n)$ amortized | $O(\log n)$ amortized with sizes | $O(n)$ |
| [B-tree](/b-tree/) | $O(\log_B n)$ block reads | $O(\log_B n)$ block reads | $O(\log_B n)$ | $O(\log_B n)$ with counts | $O(n/B)$ block reads |
| [fusion tree](/fusion-tree/), $w$-bit integers | static | $O(\log_w n)$ | $O(1)$ | $O(\log_w n)$ | $O(n)$ |

A [hash table](/hash-table/) gives insert, delete and contains in $O(1)$ expected time but has no fast order operations. For integer keys, the structures of the [predecessor problem](/predecessor-problem/) beat the comparison bounds.

## Lower bounds

In the [comparison model](/comparison-model/):

- **Queries.** Contains, predecessor and rank need $\lceil \lg(n+1) \rceil$ comparisons in the worst case on a set of $n$ keys, since rank has $n + 1$ possible answers and each leaf of a decision tree gives one answer. See the [sorted search lower bound](/sorted-search-lower-bound/).
- **Updates with queries.** An ordered set sorts: insert $n$ keys, then iterate (or call select for each $i$, or call min and delete $n$ times). Sorting $n$ keys needs $\lg(n!) = n \lg n - O(n)$ comparisons in the worst case (Knuth, Section 5.3.1). If iterate costs no comparisons, as in a search tree, the $n$ inserts must make them, so insert costs $\Omega(\log n)$ amortized. If the inserts are cheap, as in an unsorted list, then iterate or min must pay.
- **Min and delete.** The same reduction shows that a structure cannot do both insert and delete-min in $o(\log n)$ amortized comparisons. A [priority queue](/priority-queue/) meets the same bound.

On the [word RAM](/word-ram/) with $w$-bit integer keys, predecessor queries in linear space can be faster; their limits are those of the [predecessor lower bound](/predecessor-lower-bound/).

## References
