---
tag: 8H8C9B
kind: data-structure
slug: interval-tree
name: Interval tree
aliases:
- Augmented interval tree
- Centered interval tree
- Interval search tree
- centered interval tree
- interval search tree
area: data-structures/range-query-structures
level: core
summary: Balanced tree over intervals that reports all intervals containing a query point or overlapping a query interval.
implements: [range-query-structure]
model: comparison-model
complexity:
  vars: {n: the number of stored intervals, k: the number of reported intervals (0 for updates and single searches)}
  time: {worst: O((k + 1) log n)}
  space: {extra: Θ(n)}
prereqs: [balanced-binary-search-tree, augmenting-data-structures]
see_also: [interval-overlap-query, interval-stabbing-query, interval-tree-search, treap, red-black-tree, segment-tree, range-tree, sweep-line-technique]
sources:
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition, MIT Press (2022)
    locator: Chapter 17, Augmenting Data Structures, Section 17.3 Interval trees (INTERVAL-SEARCH, Theorem 17.2), and Exercise 17.3-4 (listing all overlapping intervals)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer (2008)
    locator: Chapter 10, More Geometric Data Structures, Section 10.1 Interval Trees (the centered tree and its query bound), and the Notes and Comments of Chapter 10
  - url: https://cp-algorithms.com/data_structures/treap.html
    title: cp-algorithms, Treap (Cartesian tree)
    locator: the operations split and merge, used here for insertion and deletion
---

An interval tree stores a set of closed intervals $[lo, hi]$ and finds the intervals that overlap a query interval $[a, b]$, or that contain a query point $p = [p, p]$. The form in this page is the *augmented* interval tree: a [balanced binary search tree](/balanced-binary-search-tree/) keyed by the left end $lo$, in which each node also stores $\mathit{max}$, the largest right end in its subtree. With this field one overlapping interval is found in $O(\log n)$ time, all $k$ of them in $O((k + 1) \log n)$ time, and intervals are inserted and deleted in $O(\log n)$ time. The *centered* interval tree of Edelsbrunner and McCreight is a static variant that reports in $O(\log n + k)$ time.

## In plain words

You keep a calendar of meetings, each with a start and an end time, and you want to know which meetings clash with a new one. A list sorted by start time is not enough: a meeting that started long ago may still be running.

The tree sorts the meetings by their start time, and every node also remembers the latest end time of all the meetings below it. When you look for a clash with a new meeting, you can skip a whole branch if its latest end is before your meeting starts, because nothing there is still running. You can also skip everything that starts after your meeting ends. What is left is a short walk down the tree.

## The abstract type

A dynamic set $S$ of closed intervals $[lo, hi]$ with $lo \le hi$, with duplicates allowed. Two intervals $[lo, hi]$ and $[a, b]$ *overlap* when $lo \le b$ and $a \le hi$. The operations are:

- $\textsc{insert}([lo, hi])$ and $\textsc{delete}([lo, hi])$, which removes one copy;
- $\textsc{search}([a, b])$: return one interval of $S$ that overlaps $[a, b]$, or nil;
- $\textsc{report}([a, b])$: return all intervals of $S$ that overlap $[a, b]$;
- the stabbing query $\textsc{report}([p, p])$: all intervals that contain the point $p$.

These are the [interval overlap query](/interval-overlap-query/) and the [interval stabbing query](/interval-stabbing-query/).

## Representation

Each node $x$ holds one interval $x.lo, x.hi$, two children, the balance data of the underlying tree, and

$$ x.\mathit{max} = \max(x.hi, \; x.\mathit{left}.\mathit{max}, \; x.\mathit{right}.\mathit{max}), $$

with $\mathit{nil}.\mathit{max} = -\infty$. The nodes are in search tree order by $lo$, with ties broken by any fixed rule. The field $\mathit{max}$ depends only on the node and its two children, so by the rule for [augmenting a data structure](/augmenting-data-structures/) it is kept in $O(1)$ time per changed node, including rotations, and every operation of the balanced tree keeps its $O(\log n)$ cost. This page uses a [treap](/treap/) with split and merge; a [red-black tree](/red-black-tree/) works the same way.

## Operations

```pseudo id=main
SEARCH(T, a, b)                          ▷ one interval of T that overlaps [a, b], or nil
L1  x ← T.root
L2  while x ≠ nil and not (x.lo ≤ b and a ≤ x.hi) do
L3      if x.left ≠ nil and x.left.max ≥ a then x ← x.left
L4      else x ← x.right
L5  return x
```

The report walks the tree and prunes two kinds of subtree: a subtree whose $\mathit{max}$ is below $a$, where every interval ends too early, and the right subtree of a node with $lo > b$, where every interval starts too late.

```pseudo id=report
REPORT(x, a, b, out)                     ▷ the call is REPORT(T.root, a, b, out)
L6  if x = nil or x.max < a then return
L7  REPORT(x.left, a, b, out)
L8  if x.lo ≤ b and a ≤ x.hi then append [x.lo, x.hi] to out
L9  if x.lo ≤ b then REPORT(x.right, a, b, out)
```

INSERT and DELETE are the operations of the balanced tree, with $\mathit{max}$ recomputed at each node whose children change. With a treap, INSERT splits the tree at the key of the new interval and merges the three parts; DELETE splits out the nodes with the key of the interval and merges the two subtrees of one of them.

## Example

Insert $[16, 21]$, $[8, 9]$, $[25, 30]$, $[5, 10]$, $[15, 23]$, $[17, 19]$, $[26, 26]$, $[0, 3]$, $[6, 7]$ and $[19, 20]$ into a plain search tree by $lo$, in this order. The nodes, with their $\mathit{max}$ fields, are:

| node | left child | right child | $\mathit{max}$ |
|---|---|---|---|
| $[16, 21]$ (root) | $[8, 9]$ | $[25, 30]$ | 30 |
| $[8, 9]$ | $[5, 10]$ | $[15, 23]$ | 23 |
| $[5, 10]$ | $[0, 3]$ | $[6, 7]$ | 10 |
| $[15, 23]$ | | | 23 |
| $[25, 30]$ | $[17, 19]$ | $[26, 26]$ | 30 |
| $[17, 19]$ | | $[19, 20]$ | 20 |
| $[26, 26]$ | | | 26 |
| $[0, 3]$, $[6, 7]$, $[19, 20]$ | | | 3, 7, 20 |

$\textsc{search}(22, 25)$: the root $[16, 21]$ ends before 22, and its left child has $\mathit{max} = 23 \ge 22$, so go left. $[8, 9]$ does not overlap, and its left child has $\mathit{max} = 10 < 22$, so go right. $[15, 23]$ overlaps $[22, 25]$, and the search returns it.

$\textsc{report}(22, 25)$ goes into the subtree of $[8, 9]$, skips $[5, 10]$ at once because $10 < 22$, and outputs $[15, 23]$. At the root it goes right, skips $[17, 19]$ because $20 < 22$, outputs $[25, 30]$, and at $[26, 26]$ it stops, because $26 > 25$ means that this interval and its right subtree start too late. The answer is $[15, 23]$ and $[25, 30]$. The stabbing query $\textsc{report}(9, 9)$ returns $[5, 10]$ and $[8, 9]$.

## Correctness

SEARCH keeps the invariant "if some interval of $T$ overlaps $[a, b]$, then one is in the subtree of $x$". When line L3 goes left, the left subtree has an interval $[lo', hi']$ with $hi' = x.\mathit{left}.\mathit{max} \ge a$. If it does not overlap, then $lo' > b$, and every interval in the right subtree has an even larger left end, so none of them overlaps either; so going left loses nothing. When line L4 goes right, the left subtree is empty or all its intervals end before $a$, so none overlaps, and $x$ itself does not overlap. So when the loop ends with $x = \mathit{nil}$, no interval overlaps. This is the argument of CLRS, Theorem 17.2.

REPORT outputs exactly the overlapping intervals of the subtree of $x$: line L6 skips a subtree only when all its right ends are below $a$, line L9 skips a right subtree only when all its left ends are at least $x.lo > b$, and line L8 tests each other node. The [proof](proofs/correctness.md) gives both arguments and the bound on the visited nodes.

## Complexity

Let $h$ be the height of the tree, which is $O(\log n)$ for a balanced tree and $O(\log n)$ in expectation for a treap. SEARCH makes one step per level, $O(h)$. INSERT and DELETE are $O(h)$, with $O(1)$ extra work per changed node for $\mathit{max}$.

REPORT visits $O((k + 1) h)$ nodes, and never more than $2n + 1$ calls. The reason is that each node that passes line L6 either has an output in its subtree, so it lies on one of the $k$ paths from the root to an output, or it lies on the search path of $b$. Indeed, a called node off that path has an ancestor where the walk went left at a node with $lo \le b$, so all intervals below it have $lo \le b$; if it also passes line L6, the interval that gives its $\mathit{max} \ge a$ overlaps $[a, b]$ and is reported. The other calls stop at line L6 and are at most twice the calls that pass it, plus one. So the report costs $O(\min(n, (k + 1) \log n))$, which is the bound of CLRS, Exercise 17.3-4. The space is one node per interval, $\Theta(n)$.

## Variants

- **Centered interval tree.** Pick the median $x_{\mathrm{mid}}$ of the $2n$ endpoints. The intervals that contain $x_{\mathrm{mid}}$ stay at the root, in two lists, one sorted by left end and one by right end; the intervals left and right of $x_{\mathrm{mid}}$ go to the two subtrees. A stabbing query at $p < x_{\mathrm{mid}}$ scans the list by left end until $lo > p$ and recurses left. It uses $O(n)$ space, $O(n \log n)$ build time and $O(\log n + k)$ query time (de Berg et al., Section 10.1), but it is static.
- **Segment tree over the endpoints.** Store each interval at the $O(\log n)$ canonical nodes of a [segment tree](/segment-tree/) over the sorted endpoints. Stabbing queries take $O(\log n + k)$ time with $O(n \log n)$ space, and the structure extends to counting and to higher dimensions.
- **Priority search tree.** McCreight's structure answers stabbing queries in $O(\log n + k)$ time with $O(n)$ space, and also supports insertion and deletion in $O(\log n)$ time.
- **Report and delete.** Another way to list all overlaps is to run SEARCH, output and delete the found interval, and repeat; then insert the intervals back. This also costs $O((k + 1) \log n)$.
- **Counting.** The number of intervals that contain $p$ is the number with $lo \le p$ minus the number with $hi < p$, which two [order statistic trees](/order-statistic-tree/) or two Fenwick trees answer in $O(\log n)$ time.

## When to use it

Use the augmented interval tree when intervals arrive and leave online and the queries ask for overlaps with a point or an interval, as in calendars, genome annotations and memory allocators. For a static set, the centered tree or a sorted array of endpoints with a sweep is simpler and faster. If all queries are known in advance, a [sweep line](/sweep-line-technique/) over the sorted endpoints answers them in $O((n + q) \log n + k)$ time without a tree. For axis-parallel rectangles, use a [range tree](/range-tree/) or a segment tree of interval trees.

## Pitfalls

- **Open and closed ends.** The overlap test $lo \le b$ and $a \le hi$ is for closed intervals. For half-open intervals $[lo, hi)$ it is $lo < b$ and $a < hi$, and lines L3, L6 and L9 change in the same way.
- **Forgetting $\mathit{max}$ in rotations.** Each rotation or split changes two or three nodes, and their $\mathit{max}$ must be recomputed from the bottom up. A wrong $\mathit{max}$ makes SEARCH miss intervals silently.
- **Pruning only by $\mathit{max}$.** Without the test $x.lo \le b$ on line L9, REPORT still returns the right intervals but can visit the whole tree, $\Theta(n)$, for a query near the left end.
- **Duplicate intervals.** If the tree allows equal keys, DELETE must remove one node with this exact interval, not any node with the same left end.
- **Unbalanced trees.** On a plain search tree, inserting intervals in order of $lo$ makes a path, and every operation becomes $\Theta(n)$.

## Implementations

## History

Edelsbrunner (1980) and McCreight (1980) introduced the centered interval tree in two technical reports, and McCreight also gave the priority search tree in 1985; de Berg et al. give this history in the notes of their Chapter 10. The augmented form, a red-black tree keyed by the left end with the field $\mathit{max}$, is the example that Cormen, Leiserson, Rivest and Stein use to teach the augmentation of search trees.

## References
