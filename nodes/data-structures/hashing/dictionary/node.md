---
tag: P48ZRM
kind: abstract-type
slug: dictionary
name: Dictionary
aliases:
- associative array
- map
- symbol table
area: data-structures/hashing
level: intro
summary: Abstract type supporting insert, search and delete of keyed items.
prereqs: [dictionary-problem]
see_also: [hash-table, predecessor-problem, ordered-symbol-table, ordered-set, red-black-tree, skip-list, trie, direct-address-table]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: the introduction to Part III (Data Structures), the operations on dynamic sets, and Chapter 11 (Hash tables)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.1 (Symbol tables), the API and its conventions
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Chapter 6 (Searching), the introduction, and Section 6.2.1 (Searching an ordered table), the lower bound on comparisons
  - paper: doi:10.1145/322261.322274
    title: Andrew Chi-Chih Yao, Should tables be sorted?, Journal of the ACM 28(3), 1981
    locator: pages 615 to 628 (the lower bound for tables that store the keys in some order)
---

A dictionary is an abstract data type that stores a finite map from keys to values, with distinct keys, and supports insert, search and delete by key. It is the type behind the `dict` of Python, the `Map` of Java and the symbol table of a compiler, and it is the interface of the [dictionary problem](/dictionary-problem/). The main implementations are the [hash table](/hash-table/), with $O(1)$ expected time per operation, and the balanced search trees, such as the [red-black tree](/red-black-tree/), with $O(\log n)$ worst-case time and ordered queries.

## In plain words

A dictionary is a box of labelled cards. Each card has a label, the key, and some data, the value. No two cards have the same label. You can put a card in, take the card with a given label out, or look up the data of a label. If you put in a card with a label that is already in the box, the new card replaces the old one.

The word names what the box does, not how it is built. A hash table, a search tree and a plain list are all ways to build it. They give the same answers, but they differ in speed and in the extra things they can do, such as listing the labels in order.

## Operations

Let $K$ be the set of keys, with an equality test, and $V$ the set of values. A dictionary value $D$ is a finite partial function from $K$ to $V$. We write $\mathrm{dom}(D)$ for its set of keys and $|D| = |\mathrm{dom}(D)|$. The special result NIL means "no value", and it is not in $V$.

| operation | signature | meaning |
|---|---|---|
| `empty` | `() → D` | the dictionary with no key |
| `insert` | `(D, k, v) → D` | map $k$ to $v$; replace the old value if $k \in \mathrm{dom}(D)$ |
| `search` | `(D, k) → V ∪ {NIL}` | the value of $k$, or NIL if $k \notin \mathrm{dom}(D)$ |
| `delete` | `(D, k) → D` | remove $k$ and its value; no change if $k \notin \mathrm{dom}(D)$ |
| `size` | `(D) → ℕ` | the number of keys $|D|$ |
| `keys` | `(D) → set of K` | the set $\mathrm{dom}(D)$, in an order that the implementation chooses |

A **set** (or dynamic set) is a dictionary in which the values carry no information; then search is a membership test. A **multimap** allows several values per key. An **ordered dictionary** adds operations that use a total order on $K$: minimum, maximum, predecessor, successor, rank and range queries. These need an [ordered symbol table](/ordered-symbol-table/) or an [ordered set](/ordered-set/), not a plain dictionary.

Many libraries also have variants of the operations: `insert` that fails or returns the old value when the key is present, `delete` that returns the removed value, and `get` with a default value instead of NIL. Each is defined from the six operations above.

## Laws

For all dictionaries $D$, keys $k \ne k'$ in $K$ and values $v, v' \in V$:

$$\mathrm{search}(\mathrm{empty}, k) = \mathrm{NIL}$$

$$\mathrm{search}(\mathrm{insert}(D, k, v), k) = v \qquad \mathrm{search}(\mathrm{insert}(D, k, v), k') = \mathrm{search}(D, k')$$

$$\mathrm{search}(\mathrm{delete}(D, k), k) = \mathrm{NIL} \qquad \mathrm{search}(\mathrm{delete}(D, k), k') = \mathrm{search}(D, k')$$

$$\mathrm{size}(\mathrm{empty}) = 0 \qquad \mathrm{size}(\mathrm{insert}(D, k, v)) = \mathrm{size}(D) + [\mathrm{search}(D, k) = \mathrm{NIL}]$$

$$\mathrm{size}(\mathrm{delete}(D, k)) = \mathrm{size}(D) - [\mathrm{search}(D, k) \ne \mathrm{NIL}]$$

$$\mathrm{keys}(D) = \{k \in K : \mathrm{search}(D, k) \ne \mathrm{NIL}\}$$

Here $[P]$ is 1 when $P$ is true and 0 else. Two consequences follow from the laws and are useful in tests:

- **Last write wins.** $\mathrm{insert}(\mathrm{insert}(D, k, v), k, v')$ and $\mathrm{insert}(D, k, v')$ answer each search the same way.
- **Insert then delete.** If $\mathrm{search}(D, k) = \mathrm{NIL}$, then $\mathrm{delete}(\mathrm{insert}(D, k, v), k)$ answers each search as $D$ does.

Both follow by applying the search laws to each key $k''$, in the two cases $k'' = k$ and $k'' \ne k$. The laws determine $\mathrm{search}(D, k)$ for each $D$ built from empty by inserts and deletes, by induction on the number of operations, so they pin down the type: two implementations that meet them give the same answers on each sequence of operations.

The laws say nothing about the order of `keys`, and nothing about time. A [hash table](/hash-table/) lists its keys in an order that depends on the hash function, and that order can change after a resize.

## Implementations

The costs are for a dictionary with $n$ keys, on the [word RAM](/word-ram/) with keys of one word. "Expected" is over the random choice of the hash function.

| implementation | search | insert | delete | ordered queries |
|---|---|---|---|---|
| [unsorted list](/sequential-search-symbol-table/) | $O(n)$ worst | $O(n)$ worst (with the check for a present key) | $O(n)$ worst | no |
| [sorted array](/binary-search-symbol-table/) | $O(\log n)$ worst | $O(n)$ worst | $O(n)$ worst | yes |
| [direct-address table](/direct-address-table/) | $O(1)$ worst | $O(1)$ worst | $O(1)$ worst | slow; space $\Theta(\lvert K \rvert)$ |
| [hash table](/hash-table/), [separate chaining](/separate-chaining/) | $O(1)$ expected | $O(1)$ expected amortized | $O(1)$ expected | no |
| [open addressing](/open-addressing/), [linear probing](/linear-probing/) | $O(1)$ expected | $O(1)$ expected amortized | $O(1)$ expected | no |
| [cuckoo hashing](/cuckoo-hashing/) | $O(1)$ worst | $O(1)$ expected amortized | $O(1)$ worst | no |
| [dynamic perfect hashing](/dynamic-perfect-hashing/) | $O(1)$ worst | $O(1)$ expected amortized | $O(1)$ expected amortized | no |
| [red-black tree](/red-black-tree/), [AVL tree](/avl-tree/) | $O(\log n)$ worst | $O(\log n)$ worst | $O(\log n)$ worst | yes |
| [skip list](/skip-list/), [treap](/treap/) | $O(\log n)$ expected | $O(\log n)$ expected | $O(\log n)$ expected | yes |
| [B-tree](/b-tree/) of order $b$ | $O(\log_b n)$ block reads | $O(\log_b n)$ block reads | $O(\log_b n)$ block reads | yes |
| [trie](/trie/) for strings of length $L$ | $O(L)$ worst | $O(L)$ worst | $O(L)$ worst | yes |

A [Bloom filter](/bloom-filter/) is not an implementation: it answers membership with false positives and cannot delete.

## Lower bounds

**Comparison model.** If an implementation may learn about keys only by comparing two keys with $<$, $=$ and $>$, then a search in a dictionary with $n$ keys needs at least $\lceil \lg(n + 1) \rceil$ comparisons in the worst case. The decision tree of the search must compare the query with each key $x$ of the dictionary at some node, else it cannot tell a query equal to $x$ from a query that is just above or below $x$. So the tree has at least $n$ internal nodes, and a binary tree with $n$ internal nodes has height at least $\lceil \lg(n+1) \rceil$ (Knuth, Section 6.2.1). So search trees cannot beat $\Theta(\log n)$ per search; see the [sorted search lower bound](/sorted-search-lower-bound/). Hash tables avoid this bound because they compute with the bits of the key, which the comparison model does not allow.

**Cell-probe model.** Yao showed that if a table of $n$ cells holds the $n$ keys, one per cell, in an order chosen by the implementation, and the universe is large enough, then some membership query needs $\lceil \lg(n + 1) \rceil$ probes; see the [static dictionary lower bound](/static-dictionary-lower-bound/). With a few extra cells the bound fails: [FKS perfect hashing](/fks-perfect-hashing/) answers each query with $O(1)$ probes in $O(n)$ cells.

**Ordered queries.** A dictionary that also answers predecessor queries solves the [predecessor problem](/predecessor-problem/), which has its own lower bounds in the cell-probe model.

## References
