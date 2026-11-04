---
tag: 86006N
kind: problem
slug: dictionary-problem
name: Dictionary problem
aliases:
- dynamic set membership
- dynamic set problem
- membership problem
- symbol table problem
area: data-structures/hashing
level: intro
summary: Maintain a set of keyed records under insertions, deletions and lookups.
prereqs: [asymptotic-notation, comparison-model]
see_also: [dictionary, hash-table, static-dictionary-problem, element-distinctness, predecessor-problem, static-dictionary-lower-bound, red-black-tree, word-ram]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: the introduction to Part III (Data Structures), the operations on dynamic sets, and Chapter 11 (Hash tables)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Chapter 6 (Searching), the introduction, Section 6.2.1 (the comparison lower bound) and Section 6.4 (Hashing)
  - paper: doi:10.1137/S0097539791194094
    title: Martin Dietzfelbinger, Anna Karlin, Kurt Mehlhorn, Friedhelm Meyer auf der Heide, Hans Rohnert and Robert E. Tarjan, Dynamic perfect hashing, upper and lower bounds, SIAM Journal on Computing 23(4), 1994
    locator: pages 738 to 761 (the dynamic dictionary with O(1) worst-case lookup and O(1) expected amortized update)
  - paper: doi:10.1145/322261.322274
    title: Andrew Chi-Chih Yao, Should tables be sorted?, Journal of the ACM 28(3), 1981
    locator: pages 615 to 628 (the cell-probe lower bound for tables that store the keys in some order)
---

The dictionary problem asks to keep a set of records, each with a distinct key, under a sequence of insertions, deletions and searches by key, and to answer each search with the record of that key or with "absent". It is the problem behind the [dictionary](/dictionary/) abstract type. In the [comparison model](/comparison-model/), each search needs $\Omega(\log n)$ comparisons in the worst case, and balanced search trees reach this bound. On the [word RAM](/word-ram/), [hash tables](/hash-table/) solve it in $O(1)$ expected amortized time per operation.

## In plain words

You keep a collection of records, such as the names and phone numbers of your contacts. The records arrive and leave one at a time. At any moment someone can give you a name and ask for the number. The dictionary problem is to answer these questions quickly, while the collection keeps changing.

The answer to a question depends only on the history: the last record put in with that name, unless it was removed later. The hard part is speed. Looking through all the records each time is slow when there are millions of them.

## Definition

Let $K$ be a set of keys with an equality test, and $V$ a set of values. NIL is a symbol not in $V$.

**Input.** A sequence $\sigma_1, \sigma_2, \ldots, \sigma_s$ of operations, given online (each answer must be given before the next operation is read). Each operation is one of $\mathrm{insert}(k, v)$, $\mathrm{delete}(k)$ or $\mathrm{search}(k)$, with $k \in K$ and $v \in V$.

**Output.** For each search $\sigma_t = \mathrm{search}(k)$, the answer $a_t \in V \cup \{\mathrm{NIL}\}$ defined as follows. Let $t' < t$ be the largest index such that $\sigma_{t'}$ is $\mathrm{insert}(k, \cdot)$ or $\mathrm{delete}(k)$. Then

$$a_t = \begin{cases} v & \text{if } t' \text{ exists and } \sigma_{t'} = \mathrm{insert}(k, v), \\ \mathrm{NIL} & \text{if } t' \text{ does not exist, or } \sigma_{t'} = \mathrm{delete}(k). \end{cases}$$

Equivalently, define $D_0 = \emptyset$ and let $D_t$ be the finite map after $\sigma_1, \ldots, \sigma_t$, where insert sets $D(k) = v$ and delete removes $k$. Then $a_t = D_{t-1}(k)$ if $k \in \mathrm{dom}(D_{t-1})$, and $a_t = \mathrm{NIL}$ else. The size $n$ in a bound is the largest $|D_t|$ over the sequence, unless the bound says otherwise.

The cost of an algorithm is the cost of the whole sequence, or of each operation, in a named model and case: worst case per operation, amortized over the sequence, or expected over the random choices of the algorithm for each fixed sequence.

## Variants

- **Membership.** $V$ has one element, so a search answers yes or no. This is the dynamic set problem, and the [hash set](/hash-table/) is its usual solution.
- **Static dictionary.** All keys are given first, and then only searches follow. See the [static dictionary problem](/static-dictionary-problem/), which [perfect hashing](/perfect-hashing/) solves with $O(1)$ worst-case search.
- **Insert-only (incremental) dictionary.** No deletions. Many uses, such as a visited set in a graph search or [deduplication](/dedup/), need only this.
- **Ordered dictionary.** Keys are totally ordered, and the queries also ask for the minimum, the successor or the keys in a range. With successor queries this is the [predecessor problem](/predecessor-problem/), and hashing alone does not solve it.
- **Approximate membership.** Searches may answer "present" for an absent key with a small probability. A [Bloom filter](/bloom-filter/) solves it in fewer bits than any exact set.
- **External memory.** The keys live on disk, and the cost is the number of block transfers. [B-trees](/b-tree/), [extendible hashing](/extendible-hashing/) and [linear hashing](/linear-hashing/) are the classic solutions.

## Examples

Start from the empty dictionary and run this sequence. The table shows the answer of each search and the map after each step.

| step | operation | answer | map after the step |
|---|---|---|---|
| 1 | insert(apple, 3) | | {apple: 3} |
| 2 | insert(pear, 5) | | {apple: 3, pear: 5} |
| 3 | search(apple) | 3 | {apple: 3, pear: 5} |
| 4 | insert(apple, 7) | | {apple: 7, pear: 5} |
| 5 | search(apple) | 7 | {apple: 7, pear: 5} |
| 6 | delete(pear) | | {apple: 7} |
| 7 | search(pear) | NIL | {apple: 7} |
| 8 | delete(fig) | | {apple: 7} |
| 9 | search(fig) | NIL | {apple: 7} |

Step 4 replaces the value of a present key. Step 8 deletes an absent key, which changes nothing.

## Known algorithms

- [Sequential search in an unsorted list](/sequential-search-symbol-table/): $O(n)$ per operation in the worst case.
- [Binary search in a sorted array](/binary-search-symbol-table/): $O(\log n)$ per search, $O(n)$ per update, in the worst case.
- [Red-black trees](/red-black-tree/) and [AVL trees](/avl-tree/): $O(\log n)$ per operation in the worst case, in the comparison model.
- [Skip lists](/skip-list/) and [treaps](/treap/): $O(\log n)$ expected per operation.
- [Hash tables](/hash-table/) with [separate chaining](/separate-chaining/) or [open addressing](/open-addressing/), and a hash function from a [universal family](/universal-hash-family/): $O(1)$ expected per operation, $O(1)$ expected amortized with resizing.
- [Cuckoo hashing](/cuckoo-hashing/) and [dynamic perfect hashing](/dynamic-perfect-hashing/): $O(1)$ worst-case search, $O(1)$ expected amortized update.
- [Direct-address tables](/direct-address-table/): $O(1)$ worst case per operation, but with space proportional to the size of the universe.

## Bounds

**Upper bound on the word RAM.** With keys of one word, the dictionary problem has an algorithm with $O(1)$ worst-case search and $O(1)$ expected amortized insert and delete, in $O(n)$ words of space: the dynamic perfect hashing of Dietzfelbinger, Karlin, Mehlhorn, Meyer auf der Heide, Rohnert and Tarjan (1994). Chaining with universal hashing gives $O(1)$ expected time for each operation, with the same space.

**Lower bound in the comparison model.** If the algorithm learns about keys only by comparing two of them, a search in a set of $n$ keys needs at least $\lceil \lg(n+1) \rceil$ comparisons in the worst case (Knuth, Section 6.2.1; see the [sorted search lower bound](/sorted-search-lower-bound/)). So each comparison-based solution takes $\Omega(\log n)$ time per search, and balanced search trees are optimal in that model. A whole sequence also has a lower bound: the [element distinctness](/element-distinctness/) problem on $n$ items reduces to $n$ searches and $n$ inserts (see Reductions), and it needs $\Omega(n \log n)$ comparisons, so some sequence of $2n$ operations costs $\Omega(n \log n)$ comparisons.

**Lower bound in the cell-probe model.** Yao (1981) showed that a table that stores the $n$ keys in $n$ cells, one per cell, with no other information, needs $\lceil \lg(n+1) \rceil$ probes for some search, when the universe is large enough. See the [static dictionary lower bound](/static-dictionary-lower-bound/). Hashing escapes this bound by using $O(n)$ extra cells.

**Why hashing is not limited by these bounds.** A hash table computes an address from the bits of the key, with arithmetic that the comparison model does not allow. The $O(1)$ expected bound needs the random choice of the hash function; for a fixed hash function an adversary can pick keys that all collide, and then the cost is $\Theta(n)$ per operation.

## Reductions

- **Element distinctness reduces to the dictionary problem.** For each item $x_i$ in turn, search for $x_i$; if it is present, answer "not distinct", else insert it. This uses at most $n$ searches and $n$ inserts. With a hash table it solves element distinctness in $O(n)$ expected time on the word RAM.
- **[Deduplication](/dedup/) and the [frequency counter](/frequency-counter/)** reduce to the dictionary problem in the same way, with $n$ operations: a set of the keys seen so far, or a map from each key to its count.
- **The dictionary problem reduces to the ordered dictionary problem** with no extra cost: an ordered structure answers each dictionary operation.

## Applications

- Symbol tables of compilers and interpreters, which map names to their declarations.
- Database indexes on equality, and the build side of a [hash join](/hash-join/).
- Caches, such as an [LRU cache](/lru-cache/), which find a cached item by its key.
- The visited set of a graph search, and the table of [memoization](/memoization/).
- [Deduplication](/dedup/), [frequency counting](/frequency-counter/) and [hash consing](/hash-consing/).

## References
