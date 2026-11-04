---
tag: B3VZVD
kind: technique
slug: segment-tree-maximum-subsegment-sum
name: Segment tree for the maximum sum subsegment
aliases:
- Segment tree for finding the maximum sum subsegment
area: data-structures/range-query-structures
level: core
summary: Stores in each node the sum, best prefix, best suffix and best subsegment, so merges answer maximum subarray sum queries with updates.
prereqs: [segment-tree, maximum-subarray-problem]
see_also: [kadane-algorithm, maximum-subarray-divide-and-conquer, monoid, lazy-propagation, range-query-problem, heavy-light-decomposition, divide-and-conquer-paradigm, range-assignment-query]
sources:
  - url: https://cp-algorithms.com/data_structures/segment_tree.html
    title: cp-algorithms, Segment Tree
    locator: section Finding subsegments with the maximal sum
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8 (Algorithm Design Techniques), the divide-and-conquer algorithm for the maximum subvector
---

This technique answers the [maximum subarray problem](/maximum-subarray-problem/) on any range $[l, r]$ of an array, with point updates, by a [segment tree](/segment-tree/) whose nodes store four numbers: the sum, the best prefix sum, the best suffix sum and the best subsegment sum of the node's range. Two such records merge in $O(1)$ time into the record of the joined range, so a query and an update each cost $O(\log n)$. The merge is the combine step of the [divide-and-conquer algorithm](/maximum-subarray-divide-and-conquer/) for the maximum subarray, and the records with this merge form a [monoid](/monoid/).

## In plain words

You have a list of daily gains and losses. A question names a stretch of days and asks for the best run of consecutive days inside it, the run with the largest total. The list also changes from time to time.

The best run of a stretch cannot be found from the best runs of its two halves alone, because the best run may cross the middle. So each piece of the list keeps four numbers: its total, the best run that starts at its first day, the best run that ends at its last day, and its best run anywhere. A run that crosses the middle is a run that ends the left half joined to a run that starts the right half. With the four numbers of both halves, the four numbers of the whole piece take a few additions and comparisons.

## When it applies

- **The answer for a range does not merge, but a small record does.** The best subsegment of a union is not a function of the two best subsegments, and adding the sum, the best prefix and the best suffix makes the record closed under the merge.
- **The array changes between the queries.** For a single query on a fixed array, [Kadane's algorithm](/kadane-algorithm/) is simpler and takes $O(n)$ time.
- **Many queries on arbitrary ranges.** Each query costs $O(\log n)$ merges instead of a scan of its range.
- **The same pattern fits other "best run" queries.** The longest run of equal or of good items, and the matching of brackets, use records of the same shape.

## The template

Let $A[0 \ldots n-1]$ be an array of numbers. A record is $(s, p, x, b)$: for a nonempty range $[a, c]$, $s$ is $\sum_{i=a}^{c} A[i]$, $p$ is the largest sum of a nonempty prefix $A[a \ldots j]$, $x$ is the largest sum of a nonempty suffix $A[j \ldots c]$, and $b$ is the largest sum of a nonempty subsegment $A[i \ldots j]$ with $a \le i \le j \le c$. The tree is the recursive segment tree with node $1$ for $[0, n-1]$ and the children $2v$ and $2v + 1$.

```pseudo id=main
LEAF(y)                                                     ▷ hole: the record of one item
L1  return (y, y, y, y)

MERGE(L, R)                                                 ▷ L for [a, m], R for [m + 1, c]
L2  s ← L.s + R.s
L3  p ← max(L.p, L.s + R.p)
L4  x ← max(R.x, R.s + L.x)
L5  b ← max(L.b, R.b, L.x + R.p)
L6  return (s, p, x, b)

QUERY(v, lo, hi, l, r)                                      ▷ [l, r] meets [lo, hi]
L7  if l ≤ lo and hi ≤ r then return T[v]
L8  mid ← ⌊(lo + hi)/2⌋
L9  if r ≤ mid then return QUERY(2v, lo, mid, l, r)
L10 if l > mid then return QUERY(2v + 1, mid + 1, hi, l, r)
L11 return MERGE(QUERY(2v, lo, mid, l, r), QUERY(2v + 1, mid + 1, hi, l, r))

UPDATE(v, lo, hi, i, y)
L12 if lo = hi then T[v] ← LEAF(y); return
L13 mid ← ⌊(lo + hi)/2⌋
L14 if i ≤ mid then UPDATE(2v, lo, mid, i, y) else UPDATE(2v + 1, mid + 1, hi, i, y)
L15 T[v] ← MERGE(T[2v], T[2v + 1])
```

The holes are the record of one item and the merge. The build is the usual one of a segment tree, with LEAF at the leaves and MERGE at the inner nodes, in $O(n)$ time. The answer to the range query $(l, r)$ is the field $b$ of QUERY$(1, 0, n - 1, l, r)$.

**Why the merge is correct.** Let $L$ and $R$ be the records of $[a, m]$ and $[m + 1, c]$. A nonempty prefix of $[a, c]$ either ends at some $j \le m$, and then it is a prefix of $[a, m]$, or it ends at $j > m$, and then it is all of $[a, m]$ followed by the nonempty prefix $A[m + 1 \ldots j]$ of $[m + 1, c]$. The best one of the first kind has the sum $L.p$, and the best one of the second kind has the sum $L.s + R.p$, so line L3 is right. Line L4 is the mirror image. A nonempty subsegment $[i, j]$ of $[a, c]$ lies inside $[a, m]$, or inside $[m + 1, c]$, or has $i \le m < j$. In the last case it is the nonempty suffix $A[i \ldots m]$ followed by the nonempty prefix $A[m + 1 \ldots j]$, and the two parts can be chosen apart, so the best sum is $L.x + R.p$. This gives line L5, and line L2 is clear. For one item, each of the four fields is the item itself, which is line L1.

**Why the query is correct.** By induction on the depth, QUERY$(v, lo, hi, l, r)$ returns the record of $[\max(l, lo), \min(r, hi)]$, which is nonempty because the two ranges meet. Line L7 returns the stored record when $[lo, hi]$ lies inside $[l, r]$. Lines L9 and L10 recurse only into the child that meets $[l, r]$, and line L11 runs when both children meet it, so the two parts are adjacent and nonempty and MERGE is right for them. The left part is always the first argument: the merge is not commutative.

**Cost.** MERGE costs $O(1)$. As in the [segment tree](/segment-tree/), a query visits at most four nodes per level, so it does $O(\log n)$ merges; an update rebuilds the $\lceil \lg n \rceil + 1$ records on the path from the leaf to the root. The space is at most $4n$ records of four numbers.

### A worked run

Let $A = [2, -1, 3, -5, 4, -2, 3, -1]$, with $n = 8$. The records $(s, p, x, b)$ of the tree are:

| node | range | items | record |
|---|---|---|---|
| 1 | $[0, 7]$ | the whole array | $(3, 4, 4, 5)$ |
| 2 | $[0, 3]$ | 2, −1, 3, −5 | $(-1, 4, -1, 4)$ |
| 3 | $[4, 7]$ | 4, −2, 3, −1 | $(4, 5, 4, 5)$ |
| 4 | $[0, 1]$ | 2, −1 | $(1, 2, 1, 2)$ |
| 5 | $[2, 3]$ | 3, −5 | $(-2, 3, -2, 3)$ |
| 6 | $[4, 5]$ | 4, −2 | $(2, 4, 2, 4)$ |
| 7 | $[6, 7]$ | 3, −1 | $(2, 3, 2, 3)$ |

At the root, line L5 gives $b = \max(4, 5, -1 + 5) = 5$, the run $4, -2, 3$ of the right half.

1. The query $(1, 6)$ covers $-1, 3, -5, 4, -2, 3$. It returns the record $(2, 2, 5, 5)$: the best prefix is $-1 + 3 = 2$, the best suffix is $4 - 2 + 3 = 5$, and the best subsegment is also $4, -2, 3$ with the sum 5.
2. The query $(3, 5)$ covers $-5, 4, -2$ and returns $(-3, -1, 2, 4)$, so the answer is 4, the single item 4.
3. The update $A[3] \leftarrow 5$ makes node 5 the record $(8, 8, 8, 8)$, node 2 the record $(9, 9, 9, 9)$, and the root the record $(13, 14, 13, 14)$. The best subsegment of the whole array is now $A[0 \ldots 6]$ with the sum 14.

## Classic examples

- **Maximum subarray sum on a range, with point updates.** The template itself.
- **Range assignment.** Add a lazy tag "set every item to $c$", as in [range assignment queries](/range-assignment-query/). A node of length $k$ that gets the tag has the record $(kc, t, t, t)$ with $t = kc$ if $c > 0$ and $t = c$ otherwise, since the best nonempty run of equal items is the whole range or one item. See [lazy propagation](/lazy-propagation/).
- **The longest run of ones.** For a 0-1 array, store the length of the range, the longest run of ones at the start, at the end and anywhere. The merge is the same, with "the left part is all ones" in place of the sum: the prefix of the union is $L.p + R.p$ if $L.p$ equals the length of the left part, and $L.p$ otherwise.
- **Brackets.** For a string of brackets, store the number of unmatched closing and of unmatched opening brackets of a range. The merge matches the open brackets of the left part with the closing ones of the right part, which answers "is this substring balanced" and "the longest balanced subsequence".
- **Paths in trees.** With [heavy-light decomposition](/heavy-light-decomposition/), a path is $O(\log n)$ ranges, and the records of these ranges are merged in the order of the path. The records of the ranges that the path goes up must be reversed first, by an exchange of $p$ and $x$.

## Variations

- **Empty subsegments allowed.** If the empty run with the sum 0 counts, use the leaf $(y, \max(0, y), \max(0, y), \max(0, y))$; the merge stays the same. Then an array of only negative items has the answer 0.
- **The position of the best subsegment.** Store with $p$ the end of the best prefix, with $x$ the start of the best suffix, and with $b$ both ends, and carry them along in each $\max$ of lines L3 to L5.
- **An iterative tree.** A bottom-up segment tree also works, but the query must keep two partial results, one for the left side and one for the right side, and merge them as $\mathrm{MERGE}(\mathit{left}, \mathit{right})$ at the end, because the merge is not commutative.
- **An identity element.** The record $(0, -\infty, -\infty, -\infty)$ is a two-sided identity of MERGE, so a query may start from it and merge every covered node in order, without the cases of lines L9 and L10.
- **Other semirings.** The merge uses only $+$ and $\max$, and it stays correct when $(\max, +)$ is replaced by another pair in which $+$ distributes over $\max$, such as $(\min, +)$ for the minimum sum subsegment.

## Pitfalls

- **Merging in the wrong order.** $\mathrm{MERGE}(R, L)$ is the record of the range "$R$ then $L$", not of "$L$ then $R$". A query that merges its parts in the order it finds them, as an iterative tree does, gives wrong answers.
- **A wrong identity.** The record $(0, 0, 0, 0)$ is not an identity for nonempty runs: it turns the answer for an array of negative items into 0. Use $-\infty$ in the last three fields, or the case split of lines L9 and L10.
- **Infinite values in sums.** With $-\infty$ stored as a large negative integer, $L.s + R.p$ can overflow in fixed-width arithmetic. Keep the sentinel far from the limit, or avoid it by the case split.
- **Only two fields.** Storing only the sum and the best subsegment, or adding the best prefix but not the best suffix, gives a merge that misses the runs that cross the middle.
- **Lazy tags on the four fields.** A range add of $c$ is not a simple tag of this record: after the add, the best subsegment of a node can be a run of another length, so the new $b$ does not follow from the old record and $c$ alone. For $[1, -5, 1]$ the best run is one item with the sum 1, and after adding 3 to each item it is the whole range with the sum 6. Range assignment works with a tag, range add does not.

## Exercises

1. Prove that $(0, -\infty, -\infty, -\infty)$ is a two-sided identity of MERGE and that MERGE is associative, so that the records form a [monoid](/monoid/).
2. Change the records so that the query also returns the leftmost pair $(i, j)$ of a best subsegment, and prove that the ties are broken the right way.
3. Write the bracket version: store, for each range, the number of unmatched opening and closing brackets, and answer the length of the longest balanced subsequence of $s[l \ldots r]$ in $O(\log n)$ time.
4. For $A = [-3, -1, -2]$, compute the records of the tree by hand and check that the root is $(-6, -3, -2, -1)$. Then give the root for the variation with empty subsegments allowed.

## References
