---
tag: 85F3S3
kind: algorithm
slug: bst-floor-and-ceiling
name: BST floor and ceiling
aliases:
- BST predecessor query
- BST successor query
area: data-structures/search-trees
level: core
summary: Queries on a binary search tree that find the largest key not above, or smallest key not below, a given key.
model: comparison-model
complexity:
  vars: {n: the number of keys, h: the height of the tree}
  time: {worst: Θ(h), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false, in_place: true}
prereqs: [binary-search-tree, bst-search]
see_also: [floor-and-ceiling-in-ordered-set, ordered-symbol-table, ordered-set, binary-search, predecessor-problem, order-statistic-tree, bst-range-search]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.2 (Binary search trees), order-based methods, floor() and ceiling()
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 12.2 (Querying a binary search tree), TREE-SEARCH and TREE-SUCCESSOR
---

The floor of a key $k$ in a [binary search tree](/binary-search-tree/) is the largest key of the tree that is at most $k$, and the ceiling is the smallest key that is at least $k$. Both are found by one descent from the root, as in [BST search](/bst-search/), that keeps the best candidate seen so far: for the floor, each node with a key below $k$ is a candidate, and the search continues to its right to find a larger one. The descent takes $O(h)$ time on a tree of height $h$, and $k$ itself need not be in the tree. These are the queries of the problem [floor and ceiling in an ordered set](/floor-and-ceiling-in-ordered-set/).

## In plain words

You want the largest number in the tree that is not bigger than your number. Walk down from the top as in an ordinary search. When the number at a node is bigger than yours, it is too big, so go left. When it is smaller, it could be the answer, so write it down, and then go right to look for a better one that is still not too big.

When the walk falls off the tree, the last number you wrote down is the answer. If you never wrote one down, every number in the tree is too big. The ceiling works the same way with left and right swapped.

## The problem

The input is a binary search tree with root $x$ and distinct keys from a total order, and a query key $k$. Let $D$ be the set of keys. The output of FLOOR is $\max\{d \in D : d \le k\}$, and the output of CEILING is $\min\{d \in D : d \ge k\}$; each is NIL when the set is empty. The tree is not changed.

## The algorithm

```pseudo id=main
FLOOR(x, k)
L1  best ← NIL
L2  while x ≠ NIL do
L3      if k = x.key then return k
L4      if k < x.key then x ← x.left          ▷ x.key is too large
L5      else best ← x; x ← x.right             ▷ x.key < k: a candidate
L6  return best.key if best ≠ NIL else NIL

CEILING(x, k)
L7  best ← NIL
L8  while x ≠ NIL do
L9      if k = x.key then return k
L10     if k > x.key then x ← x.right         ▷ x.key is too small
L11     else best ← x; x ← x.left              ▷ x.key > k: a candidate
L12 return best.key if best ≠ NIL else NIL
```

FLOOR walks the search path of $k$. Line L3 stops at an exact match. Line L4 skips a key that is too large; all keys of its right subtree are larger still, so only the left subtree can hold the floor. Line L5 records a key below $k$; the keys of its left subtree are smaller, so they cannot beat it, and the search goes right. CEILING is the mirror image.

## Example

Take the tree built by inserting 50, 30, 70, 20, 40, 60, 80, 35, 45 and 65.

```
              50
           /      \
         30        70
        /  \      /  \
      20    40   60   80
           /  \    \
         35    45   65
```

**Floor of 62.** The path is $50 \to 70 \to 60 \to 65 \to$ NIL.

| node | compare | action | best |
|---|---|---|---|
| 50 | $50 < 62$ | candidate, go right | 50 |
| 70 | $70 > 62$ | go left | 50 |
| 60 | $60 < 62$ | candidate, go right | 60 |
| 65 | $65 > 62$ | go left | 60 |
| NIL | | return | 60 |

**Ceiling of 62.** The same path records 70 and then 65, so the answer is 65. The keys 60 and 65 are the in-order neighbours of the gap that holds 62.

More queries: the floor of 49 is 45 and its ceiling is 50; the floor of 36 is 35 and its ceiling is 40; the floor and the ceiling of 45 are both 45; the floor of 10 is NIL and its ceiling is 20; the floor of 90 is 80 and its ceiling is NIL.

## Correctness

The loop of FLOOR keeps this invariant: *the floor of $k$ in the whole tree is the larger of best.key and the floor of $k$ in the subtree of $x$* (where NIL is smaller than each key). At the start, best is NIL and $x$ is the root. If $k < x.key$, then $x$ and its right subtree hold only keys $> k$, so the floor in the subtree of $x$ is the floor in its left subtree. If $x.key < k$, then $x.key$ is at most $k$, and each key of its left subtree is smaller than $x.key$; so the floor in the subtree of $x$ is the larger of $x.key$ and the floor in its right subtree, and each key in the right subtree that is at most $k$ is larger than $x.key$. When $x$ is NIL, the invariant says that best is the floor. A match in line L3 is the floor by definition. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Each run of the loop visits one node of a root-to-leaf path and takes $O(1)$ time. So the time is $\Theta(d + 1)$, where $d$ is the depth of the last node visited, and $O(h)$ in the worst case; on a chain it is $\Theta(n)$. The best case is a match at the root, $\Theta(1)$. The iterative form uses $O(1)$ extra space. In the [comparison model](/comparison-model/), $\lceil \lg(n+1) \rceil$ comparisons are needed in the worst case, because the $n + 1$ possible answers (NIL and each key) must be told apart; a tree of minimum height meets this bound up to a factor of 2 for the two tests per level.

## Properties

- **Same path as a search.** The nodes visited are the search path of $k$. The floor is the last node on the path where the search went right, and the ceiling is the last node where it went left.
- **No parent pointers.** Unlike TREE-SUCCESSOR, the descent never goes up.
- **Read only.** The tree does not change.
- **Comparison based.** It needs only $<$ on keys.

## Variants and improvements

- **Recursive form (Sedgewick and Wayne).** `floor(x, k)` returns NIL for NIL, $x$ on a match, `floor(x.left, k)` if $k < x.key$, and else `t = floor(x.right, k)`, returning $t$ if it is not NIL and $x$ otherwise. It does the same comparisons with $\Theta(d)$ stack space.
- **Strict versions.** The largest key $< k$ (lower) and the smallest key $> k$ (higher) drop the equality test: for lower, treat $k = x.key$ as "too large" and go left.
- **Through the successor.** Search for $k$; if it is absent, the place where the search fell off is a gap, and its in-order neighbours are the floor and the ceiling. With parent pointers, TREE-SUCCESSOR and TREE-PREDECESSOR from the last node visited give the same answers.
- **Rank and select.** With subtree sizes, the same descent also counts the keys below $k$, which gives rank; see the [order statistic tree](/order-statistic-tree/).
- **Range queries.** A [range search](/bst-range-search/) for $[lo, hi]$ starts at the ceiling of $lo$ and walks successors up to the floor of $hi$.
- **Integer keys.** For $w$-bit integers, the [predecessor problem](/predecessor-problem/) has faster structures than a comparison tree.

## When to use it

Use it for each query of the form "the nearest key at or below $k$" on an ordered map: the last event before a time, the price band of an amount, the free block of memory nearest an address, the interval that starts at or before a point. Use a balanced tree, such as a [red-black tree](/red-black-tree/), so that $h = O(\log n)$. For a static set, [binary search](/binary-search/) on a sorted array gives the same answer with less memory.

## Pitfalls

- **Going left after a candidate.** After recording $x$ as a floor candidate, the search must go right. Going left only finds smaller keys, which cannot beat the candidate.
- **Returning the last node visited.** The last node on the path is not the floor in general. In the example the floor of 62 is 60, but the last node visited is 65.
- **Mixing up floor and strict lower.** Code that returns the largest key $< k$ when the caller asked for $\le k$ (or the reverse) is wrong exactly on the keys that are in the tree. Test with a key that is present.
- **NIL versus a key.** When all keys exceed $k$, the floor is NIL. A caller that treats the result as a key dereferences NIL.

## Implementations

The Python functions follow the main block and need only `<` on keys; the equality test of lines L3 and L9 is written as two tests with `<`. The file has a small insert helper used by the tests.

## History

Floor and ceiling as named operations of an ordered table come from the ordered symbol table interface of Sedgewick and Wayne, Section 3.2. The queries themselves are as old as tree search: the nearest neighbours of a missing key are the two ends of the gap where a search for it stops.

## References
