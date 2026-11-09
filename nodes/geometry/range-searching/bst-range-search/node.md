---
tag: JZANN9
kind: algorithm
slug: bst-range-search
name: Binary search tree range search
aliases:
- BST range query
- BST range reporting
- pruned in-order traversal
area: geometry/range-searching
level: intro
summary: In-order traversal of a BST pruned to the subtrees that can contain keys in [lo, hi], in O(log n + k) time.
solves: [one-dimensional-range-search]
model: comparison-model
complexity:
  vars: {n: the number of keys, k: the number of reported keys, h: the height of the tree}
  time: {query: O(h + k) worst case, balanced: O(log n + k) worst case}
  space: {extra: O(h) worst case}
properties: {online: true, deterministic: true, recursive: true, static: false}
history:
  year: 1979
  people: [Jon Louis Bentley, Jerome H. Friedman]
  note: The pruned traversal is folklore of the 1960s and 1970s; Bentley and Friedman's 1979 survey of range searching gives it as the one-dimensional base case of the multidimensional structures.
prereqs: [one-dimensional-range-search, binary-search-tree, inorder-traversal]
see_also: [balanced-binary-search-tree, red-black-tree, order-statistic-tree, floor-and-ceiling-in-ordered-set, kd-tree-range-search, range-tree-query, orthogonal-range-searching, interval-tree-search]
sources:
  - paper: doi:10.1145/356789.356797
    title: Jon Louis Bentley and Jerome H. Friedman, Data structures for range searching, ACM Computing Surveys 11(4), 1979, pages 397 to 409
    locator: the one-dimensional case with sorted arrays and binary search trees
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 5, Section 5.1, 1-Dimensional Range Searching (the leaf-based variant with the split node, Theorem 5.2)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition, Addison-Wesley, 2011
    locator: Section 3.2, Binary Search Trees, range queries (the keys(lo, hi) method and its analysis)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.2
---

Binary search tree range search reports every key of a [binary search tree](/binary-search-tree/) that lies in a closed interval $[lo, hi]$. It is an [in-order traversal](/inorder-traversal/) that skips each subtree whose keys are all below $lo$ or all above $hi$. It reports the $k$ keys in sorted order in $O(h + k)$ time, where $h$ is the height of the tree, so in $O(\log n + k)$ time on a [balanced tree](/balanced-binary-search-tree/). It answers the [one-dimensional range search](/one-dimensional-range-search/) problem and is the base case of the multidimensional structures.

## In plain words

A search tree keeps smaller keys to the left of each key and larger ones to the right. To list all keys between a low and a high value, walk the tree in sorted order, but do not enter a part of the tree when every key there is too small or too large.

At each key, look left only if the key is larger than the low value, since otherwise everything on the left is too small. Write the key down if it lies between the two values. Look right only if the key is at most the high value. The keys that are written down come out in sorted order. Besides the answers, the walk touches only the keys along two paths: the path where the low value would be stored and the path where the high value would be stored.

## The problem

**Notation.** $P$ is the set of $n$ keys (points on a line, so $d = 1$), $k$ the output size, the number of keys reported, and $h$ the height of the tree, counted in nodes. The predicates $\mathrm{orient}$ and $\mathrm{incircle}$ are not used; the only predicate is the comparison of two keys.

The input is a binary search tree that holds the multiset $P$ and obeys the order rule

$$\text{every key in } x.\mathit{left} < x.\mathit{key} \le \text{every key in } x.\mathit{right},$$

so equal keys go to the right. A query is a pair $lo, hi$, and the range is closed: the answer is every stored key $x$ with $lo \le x \le hi$, once per copy. If $lo > hi$ the answer is empty. Duplicates and keys equal to $lo$ or $hi$ are the only degenerate cases, and the closed comparisons of lines L2, L4 and L6 handle them.

## The algorithm

```pseudo id=main
RANGE-SEARCH(x, lo, hi)
L1  if x = nil then return
L2  if lo < x.key then
L3      RANGE-SEARCH(x.left, lo, hi)
L4  if lo ≤ x.key ≤ hi then
L5      report x.key
L6  if x.key ≤ hi then
L7      RANGE-SEARCH(x.right, lo, hi)
```

- **Line L2.** Every key in the left subtree is smaller than $x.key$. If $x.key \le lo$, those keys are $< lo$, so the left subtree holds no answer and is skipped.
- **Lines L4 and L5.** The node's own key is tested against the closed range.
- **Line L6.** Every key in the right subtree is at least $x.key$. If $x.key > hi$, those keys are $> hi$, and the right subtree is skipped.
- **Order of output.** The three steps run in the order left, node, right, so the output is the in-order sequence restricted to the range: sorted, with duplicates kept.

The code replaces the recursion by an explicit stack of frames (node, stage), so that a degenerate tree of height $n$ does not exhaust the call stack.

## Example

The keys $2, 5, 9, 12, 15, 19, 23, 27, 31$ are stored in the balanced tree with root $15$, left child $9$ (children $5$ and $12$, and $2$ left of $5$) and right child $27$ (children $23$ and $31$, and $19$ left of $23$). The query is $[lo, hi] = [10, 24]$.

| step | node | line L2: go left? | line L4: report? | line L6: go right? | output so far |
|---|---|---|---|---|---|
| 1 | 15 | yes, $10 < 15$ | (after the left subtree) | | |
| 2 | 9 | no, $10 \ge 9$ | no | yes, $9 \le 24$ | |
| 3 | 12 | yes, child is nil | yes | yes, child is nil | 12 |
| 4 | 15 | | yes | yes, $15 \le 24$ | 12, 15 |
| 5 | 27 | yes, $10 < 27$ | (after the left subtree) | | 12, 15 |
| 6 | 23 | yes | (after the left subtree) | | 12, 15 |
| 7 | 19 | yes, child is nil | yes | yes, child is nil | 12, 15, 19 |
| 8 | 23 | | yes | yes, $23 \le 24$, child is nil | 12, 15, 19, 23 |
| 9 | 27 | | no | no, $27 > 24$ | 12, 15, 19, 23 |

The search enters $6$ nodes: $15, 9, 12, 27, 23, 19$. The two that are not reported, $9$ and $27$, lie on the search path of $10$ (nodes $15, 9, 12$) and on the search path of $24$ (nodes $15, 27, 23$). The subtrees of $5$ and $31$ are never entered.

## Correctness

**Invariant.** When RANGE-SEARCH is called on a node $x$, the keys of the whole tree that lie in $[lo, hi]$ and have not been reported are exactly those of the subtree of $x$ that lie in $[lo, hi]$, followed by those that come after the subtree in in-order. Lines L2 and L6 skip only subtrees that contain no key of $[lo, hi]$, by the order rule, and the traversal order left, node, right is in-order. So the output is exactly $P \cap [lo, hi]$ in sorted order. The proof, with the visit bound, is in [the correctness proof](proofs/correctness/).

## Complexity

- **Query time.** Each entered node costs $O(1)$ comparisons. A node that is entered but not reported has its key below $lo$ or above $hi$, and the proof shows that it then lies on the search path of $lo$ or on the search path of $hi$. Each path has at most $h$ nodes, so the search enters at most $k + 2h$ nodes and takes $O(h + k)$ time in the worst case. Calls on nil children add at most $2(k + 2h)$ constant steps.
- **Balanced trees.** In a [red-black tree](/red-black-tree/) or any other balanced tree $h = O(\log n)$, so the query takes $O(\log n + k)$ time in the worst case. In a tree built by random insertions the expected height is $O(\log n)$.
- **Space.** The explicit stack holds $O(h)$ frames.
- **Optimality.** In the comparison model, the emptiness case $lo = hi$ is a membership test, which needs $\Omega(\log n)$ comparisons, and reporting needs $\Omega(k)$ steps to write the output. So $O(\log n + k)$ is optimal.

## Properties

- **Output sensitive.** The cost depends on $k$, not on the size of the subtrees that are skipped.
- **Sorted output.** Keys come out in non-decreasing order, which a hash table cannot give.
- **Dynamic.** The tree may change between queries; the search only reads it.
- **Comparison based.** Only the key comparison is used, so the keys can be any totally ordered type.

## Variants and improvements

- **Counting.** If every node stores the size of its subtree, as in an [order statistic tree](/order-statistic-tree/), the count $|P \cap [lo, hi]|$ is the rank of $hi$ minus the rank of $lo$, computed in $O(h)$ time without visiting the answers.
- **Leaf-based trees.** de Berg et al. store the keys in the leaves and route with copies in the internal nodes. The query finds the split node where the paths to $lo$ and $hi$ separate, then reports whole subtrees hanging off the two paths. This form gives the canonical subsets used by the [range tree](/range-tree/).
- **Sorted array.** For a static set, two [binary searches](/binary-search/) find the first and last index in the range, and the answer is a slice. This uses less memory and has better cache behavior.
- **Higher dimensions.** The [kd-tree range search](/kd-tree-range-search/) and the [range tree query](/range-tree-query/) apply the same pruning in two or more dimensions.

## When to use it

Use the tree search when the key set changes over time and range queries must return keys in order, for example an ordered map in a standard library. For a static key set, a sorted array with two binary searches is simpler and faster. For many queries with large outputs on disk, use a [B-tree](/b-tree/), which reads $O(\log_B n + k/B)$ blocks.

## Pitfalls

- **Strict versus non-strict test on line L2.** Writing `if lo ≤ x.key then go left` is safe but enters the left subtree when $x.key = lo$, where every key is $< lo$; it wastes a path. Writing `if lo < x.key` with the opposite order rule ("left $\le$ key $<$ right") misses copies of $lo$ stored on the left. The test of line L2 must match the order rule: with equal keys going right, go left exactly when $lo < x.key$.
- **Skipping the right side too early.** Writing `if x.key < hi then go right` on line L6 loses the copies of $hi$ in the right subtree, which exist when $hi$ has duplicates. The right line is `if x.key ≤ hi`.
- **Testing only the node.** A search that stops at the first node outside $[lo, hi]$ misses answers below it: a node with key below $lo$ can have answers in its right subtree. Line L6 must be checked even when line L4 fails.
- **Recursion depth.** An unbalanced tree built from sorted input has height $n$, and a recursive implementation then overflows the call stack. Use an explicit stack or a balanced tree.

## Implementations

## History

Binary search trees go back to the late 1950s and 1960s, and the pruned traversal was part of the folklore of searching before it was named. Jon Bentley and Jerome Friedman's 1979 survey in ACM Computing Surveys treated it as the one-dimensional base case of range searching, from which kd-trees, range trees and the other multidimensional structures are built. The leaf-based form with a split node is the version in de Berg et al., Section 5.1, where it serves as the first level of the range tree.

## References
