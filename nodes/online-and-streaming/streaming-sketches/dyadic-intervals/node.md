---
tag: G0NHYJ
kind: concept
slug: dyadic-intervals
name: Dyadic intervals
aliases:
- dyadic decomposition
- binary intervals
- canonical dyadic decomposition
area: online-and-streaming/streaming-sketches
level: core
summary: Intervals of the form [k 2^j, (k+1) 2^j − 1]; every range of a universe of size U splits into at most 2 log2 U of them, which turns range and quantile queries into point queries.
prereqs: [binary-search, frequency-vector]
see_also: [count-min-sketch, q-digest, quantile-summary-problem, segment-tree, fenwick-tree, trie, count-sketch, linear-sketch]
sources:
  - paper: doi:10.1016/j.jalgor.2003.12.001
    title: Graham Cormode and S. Muthukrishnan, An improved data stream summary, the count-min sketch and its applications, Journal of Algorithms 55(1), 2005
    locator: pp. 58 to 75, the sections on range queries and on quantiles (one sketch for each dyadic level)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 4, Summaries for Ordered Data (the Q-Digest of Section 4.1 and the dyadic Count Sketch)
  - book: isbn:9781933019147
    title: S. Muthukrishnan, Data Streams, Algorithms and Applications, Foundations and Trends in Theoretical Computer Science 1(2), 2005
    locator: the sections on range sums and quantiles over the dyadic decomposition
---

A dyadic interval of the universe $[0, U)$, with $U = 2^L$, is a block of the form $[k 2^j, (k+1)2^j - 1]$ for a level $j$ with $0 \le j \le L$ and an index $k$. Every range $[a, b]$ of the universe is a disjoint union of at most $2L = 2\log_2 U$ dyadic intervals, and a prefix $[0, b]$ is a union of at most $L + 1$. So a summary that can count the items in each dyadic interval can count the items in any range with $O(\log U)$ lookups. Streaming algorithms use this to answer range queries, quantile queries and hierarchical heavy-hitter queries with point-query sketches such as [Count-Min](/count-min-sketch/). On this page $U$ is the universe size, a power of two, and $n$ is the number of items, or $\|f\|_1$ in the [turnstile model](/turnstile-model/).

## In plain words

Think of a ruler from 0 to 15. Mark it in halves, quarters, eighths and single steps. Each mark gives a block whose length is a power of two and that starts at a multiple of its length. These are the dyadic blocks. Any stretch of the ruler, such as 3 to 12, can be laid out from a few of these blocks: one small block at each end and a few larger ones in the middle. You never need more than two blocks of each size. So if you keep a count for every block, you can count any stretch by adding a handful of counts, and you can find the median by walking down from the big blocks to the small ones.

## The idea

**The tree.** The dyadic intervals form a complete binary tree of height $L$. The root is $[0, U - 1]$ at level $L$. A node $(j, k)$ at level $j \ge 1$ has the children $(j - 1, 2k)$ and $(j - 1, 2k + 1)$, its two halves, and the leaves at level 0 are the single points. A point $x$ lies in exactly one interval of each level, the one with $k = \lfloor x / 2^j \rfloor$, so it lies in $L + 1$ intervals in all. Two dyadic intervals are either disjoint or one contains the other.

**The decomposition.** For $0 \le a \le b < U$, call a dyadic interval inside $[a, b]$ maximal if its parent is not inside $[a, b]$. The canonical decomposition of $[a, b]$ is the set of its maximal dyadic intervals.

**Theorem.** The maximal dyadic intervals of $[a, b]$ are disjoint, their union is $[a, b]$, and there are at most $2L$ of them for $L \ge 1$. No other set of dyadic intervals with union $[a, b]$ is smaller.

*Proof.* Suppose that a maximal interval $I$ is strictly inside another maximal interval $I'$. Then $I'$ is an ancestor of $I$, so the parent of $I$ is inside $I'$ and therefore inside $[a, b]$, and $I$ is not maximal. So two maximal intervals are never nested, and dyadic intervals that are not nested are disjoint. For each $x \in [a, b]$, the point interval $\{x\}$ is inside $[a, b]$. Go up from it while the parent stays inside $[a, b]$; the last interval reached is maximal and contains $x$. So the union is $[a, b]$.

For the count, suppose that three maximal intervals $I_1 < I_2 < I_3$ have the same level $j < L$. The sibling $I'_2$ of $I_2$ is the other half of its parent, and it has the same length and is adjacent to $I_2$. It is not $I_1$ or $I_3$, since then the parent would be inside $[a, b]$. As dyadic intervals of level $j$ do not overlap, $I'_2$ lies between $I_1$ and $I_3$, so inside $[a, b]$, which is an interval. Then the parent $I_2 \cup I'_2$ is inside $[a, b]$, and $I_2$ is not maximal. So each level $j < L$ has at most 2 maximal intervals. If the root is maximal, it is the only one. Otherwise only the levels 0 to $L - 1$ count, which gives at most $2L$.

For the last claim, take any set $D$ of disjoint dyadic intervals with union $[a, b]$. Each interval of $D$ lies inside a maximal one, and each maximal interval is a disjoint union of intervals of $D$, since the intervals of $D$ inside it cover it and no interval of $D$ sticks out of it (a dyadic interval that meets a maximal one and is not inside it would contain it, and would then be inside $[a, b]$ and larger, which is not possible). So $D$ has at least as many intervals as the canonical set. $\square$

The bound is close to tight: for $L \ge 2$, the range $[1, U - 2]$ needs $2L - 2$ intervals, and the tests check, over all ranges for $U$ up to 64, that $2L - 2$ is the exact maximum.

**Prefixes.** The prefix $[0, b]$ has one maximal interval for each 1 bit of $b + 1$: if $b + 1 = \sum_{j \in J} 2^j$, the intervals are laid down from the largest $j$ to the smallest. So a prefix needs at most $L + 1$ intervals, and at most $L$ when $b < U - 1$. This is the rule of the [Fenwick tree](/fenwick-tree/).

**Computing the decomposition.** The bottom-up loop below is the query loop of an iterative [segment tree](/segment-tree/). It works on the half-open range $[lo, hi)$ in units of $2^j$.

```pseudo id=main
DYADIC-DECOMPOSE(a, b)                        ▷ 0 ≤ a ≤ b < U = 2^L
L1  lo ← a; hi ← b + 1; j ← 0
L2  while lo < hi do
L3      if lo is odd then output the block (j, lo); lo ← lo + 1
L4      if hi is odd then hi ← hi − 1; output the block (j, hi)
L5      lo ← ⌊lo / 2⌋; hi ← ⌊hi / 2⌋; j ← j + 1
L6  return the blocks from the left side in order, then those from the right side in reverse
```

Each pass of the loop outputs at most two blocks and goes up one level, so it runs $O(L)$ steps.

**Range counts.** Keep a count $c(j, k)$ for each dyadic interval. An update of $x$ by $\Delta$ adds $\Delta$ to the $L + 1$ counts on the path from the leaf $x$ to the root. A range count is the sum of the counts of the canonical decomposition, at most $2L$ terms. In a stream, the counts of level $j$ form a [frequency vector](/frequency-vector/) over $U/2^j$ items, and one replaces it by a sketch.

**Quantiles.** To find the item of rank $r$, start at the root. At a node, look at the count $c$ of the left child: if $r \le c$, go left; else subtract $c$ from $r$ and go right. After $L$ steps the leaf is the answer. With approximate counts the walk returns an approximate quantile.

## Examples

**A range.** With $U = 16$ ($L = 4$), the range $[3, 12]$ splits into $[3, 3]$, $[4, 7]$, $[8, 11]$ and $[12, 12]$, four intervals. The loop of lines L1 to L6 starts with $lo = 3$, $hi = 13$. At level 0 both are odd, so it outputs $[3, 3]$ and $[12, 12]$ and moves to $lo = 2$, $hi = 6$ at level 1. Both are even, so it moves to $lo = 1$, $hi = 3$ at level 2. Both are odd, so it outputs $[4, 7]$ and $[8, 11]$, and then $lo = hi = 1$ ends the loop.

**The worst case.** The range $[1, 14]$ needs six intervals: $[1, 1]$, $[2, 3]$, $[4, 7]$, $[8, 11]$, $[12, 13]$, $[14, 14]$. That is $2L - 2 = 6$.

**A prefix.** For $[0, 12]$, $b + 1 = 13 = 8 + 4 + 1$, so the intervals are $[0, 7]$, $[8, 11]$ and $[12, 12]$.

**A quantile with Count-Min.** Let $U = 2^{32}$ and take one [Count-Min sketch](/count-min-sketch/) for each of the 33 levels, each with additive error $\varepsilon' \|f\|_1$ with probability $1 - \delta'$. A prefix count adds at most 32 sketch answers, so its error is at most $32 \varepsilon' \|f\|_1$. With $\varepsilon' = \varepsilon/32$ the error is $\varepsilon n$. A [binary search](/binary-search/) for the smallest $x$ with estimated prefix count at least $r$ makes 32 prefix queries, so a union bound over the $32 \cdot 32$ point queries needs $\delta' = \delta/1024$. In general this gives width $O(\log U/\varepsilon)$ and depth $O(\log(\log U/\delta))$ per level, and $O((1/\varepsilon)\log^2 U \log(\log U/\delta))$ counters in all, as in Cormode and Muthukrishnan (2005). It works in the turnstile model, where summaries that store items fail.

## Where it is used

- **Range sums and quantiles in turnstile streams.** Dyadic [Count-Min](/count-min-sketch/) and dyadic [Count Sketch](/count-sketch/), as above. Both are [linear sketches](/linear-sketch/), so they handle deletions and merge by addition.
- **The q-digest.** Each node of a [q-digest](/q-digest/) is a dyadic interval, and its error bound comes from the fact that a prefix meets at most $\log U$ levels.
- **Hierarchical heavy hitters.** Find the dyadic intervals, such as IP prefixes, whose count is above a threshold, by descending only into heavy nodes.
- **Range structures.** [Segment trees](/segment-tree/) and [Fenwick trees](/fenwick-tree/) store aggregates of dyadic intervals; a binary [trie](/trie/) over the bits of the keys has the dyadic intervals as its nodes.
- **The [quantile summary problem](/quantile-summary-problem/)** for integer universes, where the dyadic tree replaces comparisons.

## References
