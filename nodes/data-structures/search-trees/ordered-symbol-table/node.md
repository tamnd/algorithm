---
tag: 0MHJ3V
kind: abstract-type
slug: ordered-symbol-table
name: Ordered symbol table
area: data-structures/search-trees
level: core
summary: Abstract type for key-value storage with ordered keys, adding operations such as min, max, floor, ceiling, rank, select and range queries.
prereqs: [dictionary, total-order]
see_also: [ordered-set, binary-search-tree, binary-search-symbol-table, red-black-tree, skip-list, floor-and-ceiling-in-ordered-set, order-statistic-tree, predecessor-problem]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.1 (Symbol tables), the ordered symbol table API, and Sections 3.2 and 3.3 for its implementations
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: the introduction to Part III (operations on dynamic sets), Chapter 12, and Section 17.1 (dynamic order statistics)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.1 (minimum-comparison sorting), the lower bound on comparisons, and Section 6.2 (Searching by comparison of keys)
---

An ordered symbol table is a [dictionary](/dictionary/) whose keys come from a [total order](/total-order/), and which uses that order in its operations: besides put, get and delete, it answers minimum, maximum, floor, ceiling, rank, select, and counts and lists of the keys in a range. The name and the interface are those of Sedgewick and Wayne, Section 3.1. Balanced search trees such as the [red-black tree](/red-black-tree/) implement each operation in $O(\log n)$ time, and in the [comparison model](/comparison-model/) no implementation can do much better.

## In plain words

A phone book is an ordered symbol table. Each entry has a name and a number, and the names are in alphabetical order. You can look up a name, add one, or remove one. Because of the order you can also answer other questions: what is the first name, what is the last, which name comes just before "Miller" if there is no "Miller", how many names come before "Nguyen", which name is the hundredth, and which names lie between "King" and "Lee".

A plain dictionary, such as a hash table, can only answer the first kind of question. The ordered version costs a little more per operation, but it answers all of them.

## Operations

Let $(K, <)$ be a total order and $V$ a set of values. A table $S$ is a finite partial function from $K$ to $V$, and $\mathrm{keys}(S)$ is its domain, with $n = |\mathrm{keys}(S)|$. NIL is a value that is not in $V$. All keys below are in $K$, and $lo \le hi$ in the range operations.

| operation | signature | meaning |
|---|---|---|
| `put` | `(S, k, v) → S` | map $k$ to $v$; replace the old value if $k$ is a key |
| `get` | `(S, k) → V ∪ {NIL}` | the value of $k$, or NIL |
| `delete` | `(S, k) → S` | remove $k$ if it is a key |
| `size` | `(S) → ℕ` | $n$ |
| `min`, `max` | `(S) → K ∪ {NIL}` | the smallest and the largest key, NIL if $S$ is empty |
| `floor` | `(S, k) → K ∪ {NIL}` | the largest key $\le k$ |
| `ceiling` | `(S, k) → K ∪ {NIL}` | the smallest key $\ge k$ |
| `rank` | `(S, k) → ℕ` | the number of keys $< k$ ($k$ need not be a key) |
| `select` | `(S, i) → K` | the key of rank $i$, for $0 \le i < n$ |
| `delete_min`, `delete_max` | `(S) → S` | remove the smallest or the largest key |
| `size_range` | `(S, lo, hi) → ℕ` | the number of keys in $[lo, hi]$ |
| `keys_range` | `(S, lo, hi) → list of K` | the keys in $[lo, hi]$, in increasing order |

The [ordered set](/ordered-set/) has the same order queries without values, and it names floor and ceiling as predecessor and successor queries. The problem of answering floor and ceiling alone is [floor and ceiling in an ordered set](/floor-and-ceiling-in-ordered-set/); for integer keys it is the [predecessor problem](/predecessor-problem/). Some libraries also give strict versions: `lower(k)`, the largest key $< k$, and `higher(k)`, the smallest key $> k$.

## Laws

Write $D = \mathrm{keys}(S)$. Put, get and delete follow the laws of the [dictionary](/dictionary/). The order operations are defined from $D$ alone, so they satisfy, for each table $S$, each $k, lo, hi \in K$ and each integer $i$ with $0 \le i < n$:

$$\mathrm{min}(S) = \min D, \qquad \mathrm{max}(S) = \max D \qquad (\text{NIL if } D = \emptyset)$$

$$\mathrm{floor}(S, k) = \max\{x \in D : x \le k\}, \qquad \mathrm{ceiling}(S, k) = \min\{x \in D : x \ge k\}$$

$$\mathrm{rank}(S, k) = |\{x \in D : x < k\}|$$

$$\mathrm{rank}(S, \mathrm{select}(S, i)) = i, \qquad \mathrm{select}(S, \mathrm{rank}(S, k)) = k \ \text{ for each } k \in D$$

$$\mathrm{size\_range}(S, lo, hi) = \mathrm{rank}(S, hi) - \mathrm{rank}(S, lo) + [hi \in D]$$

$$\mathrm{keys\_range}(S, lo, hi) = \text{the elements of } D \cap [lo, hi] \text{ in increasing order}$$

$$\mathrm{delete\_min}(S) = \mathrm{delete}(S, \mathrm{min}(S)) \quad \text{for } D \ne \emptyset$$

Here $\max \emptyset = \min \emptyset = $ NIL, and $[P]$ is 1 if $P$ holds and 0 else. These laws have useful consequences that tests can check:

- **Floor and ceiling bracket the query.** If both exist, $\mathrm{floor}(S, k) \le k \le \mathrm{ceiling}(S, k)$, with equality on both sides exactly when $k \in D$, and no key of $D$ lies strictly between them.
- **Rank and floor.** $\mathrm{floor}(S, k)$ is NIL if $\mathrm{rank}(S, k) = 0$ and $k \notin D$; else it is $k$ if $k \in D$, and $\mathrm{select}(S, \mathrm{rank}(S, k) - 1)$ if $k \notin D$.
- **Select is the sorted list.** $\mathrm{select}(S, 0), \ldots, \mathrm{select}(S, n-1)$ is $D$ in increasing order, and $\mathrm{keys\_range}(S, \min D, \max D)$ is the same list.

*Proof of the rank and select laws.* List $D$ in increasing order as $x_0 < x_1 < \cdots < x_{n-1}$. The keys smaller than $x_i$ are exactly $x_0, \ldots, x_{i-1}$, so $\mathrm{rank}(S, x_i) = i$, and the key of rank $i$ is $x_i$. Both laws follow. For the size law, the keys in $[lo, hi]$ are the keys $< hi$ that are not $< lo$, plus $hi$ itself if it is a key, and $\{x < lo\} \subseteq \{x < hi\}$ because $lo \le hi$. $\square$

## Implementations

The costs are for a table with $n$ keys, in the [comparison model](/comparison-model/). The range operations cost the stated time plus $O(r)$ for $r$ reported keys.

| implementation | get | put, delete | min, max | floor, ceiling | rank, select | keys in range |
|---|---|---|---|---|---|---|
| [unordered linked list](/sequential-search-symbol-table/) | $O(n)$ | $O(n)$ | $O(n)$ | $O(n)$ | $O(n)$, $O(n)$ expected with quickselect | $O(n + r \log r)$ |
| [sorted array](/binary-search-symbol-table/) | $O(\log n)$ | $O(n)$ | $O(1)$ | $O(\log n)$ | $O(\log n)$, $O(1)$ | $O(\log n + r)$ |
| [binary search tree](/binary-search-tree/) | $O(h)$ | $O(h)$ | $O(h)$ | $O(h)$ | $O(h)$ with subtree sizes | $O(h + r)$ |
| [red-black tree](/red-black-tree/), [AVL tree](/avl-tree/) | $O(\log n)$ worst | $O(\log n)$ worst | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ with sizes ([order statistic tree](/order-statistic-tree/)) | $O(\log n + r)$ |
| [skip list](/skip-list/) | $O(\log n)$ expected | $O(\log n)$ expected | $O(1)$, $O(\log n)$ | $O(\log n)$ expected | $O(\log n)$ expected with widths | $O(\log n + r)$ expected |
| [treap](/treap/) | $O(\log n)$ expected | $O(\log n)$ expected | $O(\log n)$ expected | $O(\log n)$ expected | $O(\log n)$ expected with sizes | $O(\log n + r)$ expected |
| [splay tree](/splay-tree/) | $O(\log n)$ amortized | $O(\log n)$ amortized | $O(\log n)$ amortized | $O(\log n)$ amortized | $O(\log n)$ amortized with sizes | $O(\log n + r)$ amortized |
| [B-tree](/b-tree/) of order $b$ | $O(\log_b n)$ block reads | $O(\log_b n)$ block reads | $O(\log_b n)$ | $O(\log_b n)$ | $O(\log_b n)$ with counts | $O(\log_b n + r/b)$ block reads |

A [hash table](/hash-table/) is not on the list: it gives $O(1)$ expected get and put, but each order query needs a scan of all keys. For integer keys of $w$ bits, structures of the [predecessor problem](/predecessor-problem/), such as the [fusion tree](/fusion-tree/), beat the comparison bounds below.

## Lower bounds

**Search.** In the comparison model, get, floor, ceiling and rank on a table of $n$ keys need $\lceil \lg(n+1) \rceil$ comparisons in the worst case. For rank this is a counting argument: the $n + 1$ possible answers $0, 1, \ldots, n$ must be at different leaves of the decision tree, so the tree has height at least $\lceil \lg(n+1) \rceil$. The same holds for get, see the [sorted search lower bound](/sorted-search-lower-bound/).

**Updates and queries together.** An ordered symbol table sorts: put $n$ distinct keys, then call `select` for $i = 0, 1, \ldots, n - 1$ (or call `delete_min` $n$ times). Each sort in the comparison model needs $\lg(n!) = n \lg n - O(n)$ comparisons in the worst case (Knuth, Section 5.3.1). So for each implementation, a sequence of $2n$ operations of these kinds costs $\Omega(n \log n)$ comparisons, and the amortized cost per operation is $\Omega(\log n)$. A structure cannot have both $o(\log n)$ amortized put and $o(\log n)$ amortized delete_min. The same reduction holds for a [priority queue](/priority-queue/).

**Beyond comparisons.** On the [word RAM](/word-ram/) with integer keys, the bounds of the [predecessor problem](/predecessor-problem/) apply instead; see the [predecessor lower bound](/predecessor-lower-bound/).

## References
