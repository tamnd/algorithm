---
tag: C1KCSN
kind: algorithm
slug: interval-tree-search
name: Interval tree search
aliases:
- Interval tree stabbing and overlap search
area: sequences/interval-problems
level: core
summary: Descend an interval tree, pruning subtrees by their maximum endpoint, to report overlaps.
solves: [interval-overlap-query, interval-stabbing-query]
model: comparison-model
complexity:
  vars: {n: the number of stored intervals, k: the number of reported intervals, h: the height of the tree}
  time:
    worst: "O(min(n, (k + 1) h))"
    average: "O(min(n, (k + 1) h))"
    best: "Θ(1)"
  space: {extra: Θ(h)}
properties: {deterministic: true, comparison: true, recursive: true, in_place: true, online: true}
prereqs: [interval-tree, interval-overlap-query, interval-stabbing-query, binary-search-tree]
see_also: [bst-search, augmenting-data-structures, priority-search-tree, segment-tree, sweep-line-technique, allens-interval-algebra, interval-list-intersection, range-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 17.3, Interval trees (INTERVAL-SEARCH and Theorem 17.2), and Exercise 17.3-4 (listing all overlapping intervals)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 10, More Geometric Data Structures, Section 10.1 Interval Trees (stabbing queries and their cost)
---

Interval tree search answers overlap and stabbing queries on a binary search tree of intervals ordered by left end, in which every node also stores the largest right end in its subtree. It reports all $k$ matching intervals by a walk that skips a subtree when its largest right end is too small and skips everything right of a node whose left end is too large, which costs $O(\min(n, (k + 1) h))$ time on a tree of height $h$; a single match is found in $O(h)$ time. This page states the search for any query given by two monotone tests, one on right ends and one on left ends, which covers closed, half-open and open intervals and both kinds of query with the same code. The tree itself, with insertion and deletion, is the [interval tree](/interval-tree/) data structure; here it is a static balanced tree built from a sorted array.

## In plain words

Sort the intervals by where they start and put them in a balanced tree, so that each branch holds a run of neighbours in that order. At each branch, write down the latest end of any interval in it.

To find the intervals that meet a query, walk the tree from the top. If the latest end in a branch is still too early, nothing in that branch reaches the query, so skip it. If an interval starts too late, everything after it in the sorted order starts too late as well, so stop going right.

What counts as "too early" and "too late" depends on whether intervals include their ends. That is the only part that changes between closed and half-open intervals.

## The problem

The input is a set of $n$ intervals $\langle l_j, r_j \rangle$, stored once, and a sequence of queries. An [overlap query](/interval-overlap-query/) $\langle a, b \rangle$ asks for the intervals that share a point with it, and a [stabbing query](/interval-stabbing-query/) $p$ asks for the intervals that contain $p$. Each query is turned into two tests:

- $\mathrm{reach}(r)$, a test on right ends that is *upward closed*: if it holds for $r$, it holds for every $r' \ge r$;
- $\mathrm{start}(l)$, a test on left ends that is *downward closed*: if it holds for $l$, it holds for every $l' \le l$.

An interval matches when $\mathrm{reach}(r_j)$ and $\mathrm{start}(l_j)$ both hold. The tests for each type are:

| query | $\mathrm{reach}(r)$ | $\mathrm{start}(l)$ |
|---|---|---|
| overlap, closed $[a, b]$ | $r \ge a$ | $l \le b$ |
| overlap, half-open $[a, b)$ or open $(a, b)$ | $r > a$ | $l < b$ |
| stab $p$, closed $[l, r]$ | $r \ge p$ | $l \le p$ |
| stab $p$, half-open $[l, r)$ | $r > p$ | $l \le p$ |
| stab $p$, open $(l, r)$ | $r > p$ | $l < p$ |

The overlap tests are proved on the [overlap query](/interval-overlap-query/) page, and the stabbing tests are the definitions of the three types. Each row is a pair of monotone tests, so the search below is correct for all of them.

## The algorithm

The tree is a binary search tree whose in-order sequence is the intervals sorted by left end, with $x.\mathit{max}$ the largest right end in the subtree of $x$ and $\mathrm{nil}.\mathit{max} = -\infty$. The implementation builds it implicitly from the sorted array: the node of positions $[lo, hi)$ is $mid = \lfloor (lo + hi) / 2 \rfloor$, with children $[lo, mid)$ and $[mid + 1, hi)$, so $h = \lfloor \log_2 n \rfloor + 1$.

```pseudo id=main
REPORT(x, reach, start, out)                 ▷ call REPORT(T.root, reach, start, out)
L1  if x = nil or not reach(x.max) then return     ▷ every interval below ends too early
L2  REPORT(x.left, reach, start, out)
L3  if not start(x.l) then return                  ▷ x and its right subtree start too late
L4  if reach(x.r) then append x to out
L5  REPORT(x.right, reach, start, out)
```

```pseudo id=search
SEARCH(T, reach, start)                      ▷ one matching interval, or nil
L6  x ← T.root
L7  while x ≠ nil and not (reach(x.r) and start(x.l)) do
L8      if x.left ≠ nil and reach(x.left.max) then x ← x.left else x ← x.right
L9  return x
```

Line L1 uses $\mathit{max}$: if the largest right end below $x$ fails the upward closed test, all right ends below $x$ fail it. Line L3 uses the order: every interval in the right subtree of $x$ starts at or after $x.l$, so if $x.l$ fails the downward closed test, they all fail it. Line L3 comes after line L2, because the left subtree may hold matches even when $x$ starts too late. Line L8 is the rule of CLRS, INTERVAL-SEARCH, with the comparison $\mathit{max} \ge a$ replaced by the test $\mathrm{reach}$.

## Example

Store the intervals with end points $(1, 3), (2, 5), (3, 4), (5, 8), (6, 7), (8, 9), (7, 10)$. Sorted by left end and built as above, the tree has root $(5, 8)$; its left child $(2, 5)$ has children $(1, 3)$ and $(3, 4)$; its right child $(7, 10)$ has children $(6, 7)$ and $(8, 9)$. The $\mathit{max}$ fields are 10 at the root, 5 at $(2, 5)$, 10 at $(7, 10)$, and the right end at each leaf.

**Closed overlap query $[4, 6]$**, with $\mathrm{reach}(r) = (r \ge 4)$ and $\mathrm{start}(l) = (l \le 6)$:

| call on | L1: $\mathrm{reach}(\mathit{max})$ | L3: $\mathrm{start}(l)$ | L4: $\mathrm{reach}(r)$ | output |
|---|---|---|---|---|
| $(5, 8)$ | $10 \ge 4$ | | | |
| $(2, 5)$ | $5 \ge 4$ | | | |
| $(1, 3)$ | $3 \ge 4$ fails, return | | | |
| $(2, 5)$ | | $2 \le 6$ | $5 \ge 4$ | $(2, 5)$ |
| $(3, 4)$ | $4 \ge 4$, a touch | $3 \le 6$ | $4 \ge 4$ | $(3, 4)$ |
| $(5, 8)$ | | $5 \le 6$ | $8 \ge 4$ | $(5, 8)$ |
| $(7, 10)$ | $10 \ge 4$ | | | |
| $(6, 7)$ | $7 \ge 4$ | $6 \le 6$, a touch | $7 \ge 4$ | $(6, 7)$ |
| $(7, 10)$ | | $7 \le 6$ fails, return | | |

The output is $(2, 5), (3, 4), (5, 8), (6, 7)$, and the leaf $(8, 9)$ is never visited. **As half-open intervals**, $[4, 6)$ uses $r > 4$ and $l < 6$: the call on $(3, 4)$ stops at L1, since $4 > 4$ fails, and the call on $(6, 7)$ stops at L3, since $6 < 6$ fails. The output is $(2, 5), (5, 8)$. The touches at 4 and 6 are the difference.

**Half-open stabbing query $p = 7$**, with $r > 7$ and $l \le 7$: the root passes, $(2, 5)$ fails L1 since $5 > 7$ fails, the root is reported, $(7, 10)$ passes, $(6, 7)$ fails L1 since $7 > 7$ fails, $(7, 10)$ is reported since $7 \le 7$, and $(8, 9)$ stops at L3. The output is $[5, 8), [7, 10)$.

**SEARCH for the closed query $[9, 9]$.** At the root, $8 \ge 9$ fails, and the left child has $\mathit{max} = 5 < 9$, so go right. $(7, 10)$ has $10 \ge 9$ and $7 \le 9$, so it is returned. For $[11, 12]$ the walk goes right, right, and falls off the tree: no interval reaches 11.

## Correctness

REPORT appends exactly the matching intervals of the subtree of $x$, by induction on the subtree. Line L1 returns only when every right end below $x$ fails $\mathrm{reach}$, line L3 returns only when $x$ and every interval of its right subtree fail $\mathrm{start}$, and line L4 tests $x$ itself. SEARCH keeps the invariant "if some interval matches, one lies below $x$": going left at line L8 is safe because a left interval with $\mathrm{reach}$ that does not match must fail $\mathrm{start}$, and then so does every interval right of it. The [proof](proofs/correctness.md) gives the details and the bound on the visited nodes.

## Complexity

- **REPORT.** Call a node *expanded* if a call on it passes line L1. An expanded node either has an output below it, or lies on the path from the root to the first interval, in sorted order, that fails $\mathrm{start}$. So at most $(k + 1) h$ nodes are expanded, and each expanded node makes at most two calls. With at most $n$ expanded nodes, the cost is $O(\min(n, (k + 1) h))$.
- **SEARCH.** One step per level, $O(h)$.
- **Space.** The recursion of REPORT has depth $h$. The tree takes $\Theta(n)$ space and is built in $O(n \log n)$ time by sorting and one bottom-up pass for $\mathit{max}$.
- **Not $O(\log n + k)$.** The bound has the factor $h$ on $k$. REPORT expands every ancestor of every output. If the outputs are $k$ leaves spread evenly over the tree, for example long intervals at the leaves and short intervals that end early at the inner nodes, their ancestors number $\Theta(k \log (n / k))$, which for $k = \sqrt{n}$ is $\Theta(\sqrt{n} \log n)$. Structures with $O(\log n + k)$ queries exist, the centered interval tree and the [priority search tree](/priority-search-tree/), see the [overlap query](/interval-overlap-query/) page.

## Properties

- **Any monotone pair of tests.** The search uses only that $\mathrm{reach}$ is upward closed and $\mathrm{start}$ is downward closed. Mixed end point types, such as a closed query on half-open intervals, need only the right pair of tests.
- **Output order.** REPORT outputs the matches in the order of the tree, by left end.
- **Any binary search tree.** The argument needs only the search tree order and the $\mathit{max}$ field, so it works on red-black trees, AVL trees and treaps, where $h = O(\log n)$, and on the static tree here.
- **Online.** Each query is answered when it arrives, unlike the offline sweep.

## Variants and improvements

- **Dynamic sets.** Keep the tree balanced under insertion and deletion and update $\mathit{max}$ along the changed paths, as in the [interval tree](/interval-tree/) page. The search is unchanged.
- **Counting.** For the count alone, two sorted arrays and [binary search](/binary-search/) give $O(\log n)$ time, as on the [stabbing query](/interval-stabbing-query/) page; the tree is not needed.
- **Report by repeated SEARCH.** Find one match, report and delete it, repeat, and insert the matches back. This also costs $O((k + 1) \log n)$ on a balanced dynamic tree.
- **Batch queries.** With all queries known, sort them with the end points and [sweep](/sweep-line-technique/), in $O((n + q) \log (n + q) + k)$ time.

## When to use it

Use it when queries arrive one at a time, especially in a dynamic set, and the answers are small. Use the count formula when only the number of matches is needed, a sweep when all queries are known in advance, and a priority search tree or a centered interval tree when answers are large and the extra factor of $h$ matters.

## Pitfalls

- **One test for all types.** Using $r \ge a$ and $l \le b$ for half-open intervals reports intervals that only touch the query, such as $[3, 4)$ for $[4, 6)$. The tests must change at both ends, in lines L1, L3 and L4.
- **Half-open stabbing is not an overlap query.** The half-open query $[p, p)$ is empty and meets nothing. Stabbing a half-open interval at $p$ uses $r > p$ and $l \le p$, which is neither the closed nor the half-open overlap rule.
- **Pruning before the left subtree.** Placing line L3 before line L2 loses matches in the left subtree of a node that starts too late.
- **A stale $\mathit{max}$.** After an update, $\mathit{max}$ must be recomputed from the bottom up on every changed node; a value that is too small makes line L1 skip matches.
- **Equal left ends.** Ties may be in any order, but the in-order sequence must be sorted by left end; a tree keyed by some other field breaks line L3.

## Implementations

## History

The search with the field $\mathit{max}$ is the example that CLRS use to teach the augmentation of search trees, with INTERVAL-SEARCH for one overlap and an exercise for listing all of them, for closed intervals. Edelsbrunner and McCreight proposed the centered interval tree around 1980, which de Berg et al. present with stabbing queries in $O(\log n + k)$ time.

## References
