---
tag: 30G9RA
kind: concept
slug: reuse-distance
name: Reuse distance
aliases:
- LRU stack distance
- Stack distance
- reuse distance
- stack distance
area: systems/caching-policies
level: intro
summary: "The number of distinct other items requested between two uses of the same item. An LRU cache of size k hits a request exactly when its reuse distance is less than k."
prereqs: [locality-of-reference, cache-hit-ratio]
see_also: [mattson-stack-algorithm, miss-ratio-curve, shards, lru, working-set-model, three-cs-model, fenwick-tree, miss-ratio-curve-computation]
sources:
  - paper: doi:10.1147/sj.92.0078
    title: "R. L. Mattson, J. Gecsei, D. R. Slutz and I. L. Traiger, Evaluation techniques for storage hierarchies, IBM Systems Journal 9(2) (1970), 78-117"
    locator: the stack distance of a reference and the distance distribution, from which the hit ratio of every cache size follows
  - paper: doi:10.1147/rd.194.0353
    title: "B. T. Bennett and V. J. Kruskal, LRU stack processing, IBM Journal of Research and Development 19(4) (1975), 353-357"
    locator: computing LRU stack distances in O(log n) time per reference with a tree over the positions of last uses
  - paper: "Chen Ding and Yutao Zhong, Predicting whole-program locality through reuse distance analysis, ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI 2003), 245-257"
    title: "Chen Ding and Yutao Zhong, Predicting whole-program locality through reuse distance analysis, PLDI 2003"
    locator: the use of the name reuse distance, approximate measurement with bounded relative error, and prediction across program inputs
---

The reuse distance of a request for item $x$ is the number of distinct items other than $x$ requested since the previous request for $x$. A first request has infinite reuse distance. It is the same number as the depth of $x$ in the LRU stack of Mattson, Gecsei, Slutz and Traiger (1970), counted from 0 at the top, which is why it is also called the LRU *stack distance*. Its main property is exact: an LRU cache of $k$ items hits a request if and only if the reuse distance of the request is less than $k$. So the histogram of reuse distances of a trace gives the LRU hit ratio of every cache size at once.

## In plain words

Each time a program asks for an item, look back to the last time it asked for the same item. Count how many other items it asked for in between, but count each item once, however often it came up. That count is the reuse distance.

A small count means the program came back to the item quickly, before many other things got in the way. A cache that keeps the items used most recently, and has room for more items than the count, still holds the item. So the count tells, for each request, which cache sizes would answer it. Count only the number of requests in between, with repeats, and you get a different number, the reuse time. The reuse time is easier to measure but does not tell what the cache holds.

## The idea

**Definition.** Let $\sigma_1 \cdots \sigma_n$ be a trace. For a request $\sigma_t = x$ whose previous request for $x$ is at time $p$,

$$\text{reuse time}(t) = t - p, \qquad \text{reuse distance}(t) = \bigl|\{ \sigma_s : p < s < t \}\bigr|.$$

If there is no earlier request for $x$, both are $\infty$. Always $\text{reuse distance}(t) \le \text{reuse time}(t) - 1$, with equality when the items between the two uses are all different.

**Equal to the LRU stack depth.** The LRU stack lists the items in order of their last use, most recent on top. Just before time $t$, the items above $x$ are exactly the items used after time $p$, which are the distinct items in $\sigma_{p+1} \cdots \sigma_{t-1}$. So the depth of $x$, counted from 0, is its reuse distance. Mattson and others count depth from 1; their stack distance is the reuse distance plus 1. Both conventions are common, so state which one you use.

**Why LRU hits exactly when the distance is small.** An LRU cache of $k$ items holds the top $k$ items of the LRU stack (this is the [inclusion property](/inclusion-property/) of LRU, proved on the [Mattson stack algorithm](/mattson-stack-algorithm/) page). So request $t$ hits if and only if $x$ is among the top $k$, that is, if and only if its reuse distance is less than $k$. If $N(d)$ is the number of requests with reuse distance $d$, the LRU cache of size $k$ has $\sum_{d < k} N(d)$ hits, and the [miss ratio curve](/miss-ratio-curve/) of LRU is $m(k) = 1 - \frac{1}{n}\sum_{d < k} N(d)$.

**Reuse distance and reuse time.** The two measures answer different questions. The reuse time is the age of the item; it decides hits for the [working set policy](/working-set-model/) and for cache rules based on time, such as expiry. The reuse distance is the number of competitors; it decides hits for LRU. Two requests with the same reuse time can have different reuse distances, as in the example below. The reuse time is easy to compute with one hash table of last-use times; the reuse distance needs more work.

**Computing it.** The direct way keeps the LRU stack as a list and searches it, which costs $O(M)$ time per request for $M$ distinct items. Bennett and Kruskal (1975) put a 1 at the position of the last use of each item in a tree over the positions, so that the reuse distance of request $t$ is the number of 1s strictly between $p$ and $t$. A [Fenwick tree](/fenwick-tree/) or a balanced search tree gives each answer in $O(\log n)$ time. For very long traces, Ding and Zhong measure distances approximately with bounded relative error, and [SHARDS](/shards/) samples a fixed fraction of the items by a hash of the key, see [miss ratio curve computation](/miss-ratio-curve-computation/).

**What it does not capture.** The reuse distance gives exact answers only for LRU and fully associative caches. For a set associative cache, the extra misses are the conflict misses of the [three Cs model](/three-cs-model/). For other policies, such as FIFO or ARC, the histogram is only an indication.

## Examples

Take the trace $a\,b\,c\,b\,b\,a\,d\,c\,a$.

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| request | $a$ | $b$ | $c$ | $b$ | $b$ | $a$ | $d$ | $c$ | $a$ |
| reuse time | $\infty$ | $\infty$ | $\infty$ | 2 | 1 | 5 | $\infty$ | 5 | 3 |
| reuse distance | $\infty$ | $\infty$ | $\infty$ | 1 | 0 | 2 | $\infty$ | 3 | 2 |

At $t = 6$, the requests between the two uses of $a$ are $b\,c\,b\,b$, which hold 2 distinct items, so the reuse distance is 2 while the reuse time is 5. At $t = 8$ the reuse time is also 5, but the requests between, $b\,b\,a\,d$, hold 3 distinct items.

The histogram has $N(0) = 1$, $N(1) = 1$, $N(2) = 2$, $N(3) = 1$ and 4 first requests. So LRU has $1, 2, 4, 5$ hits with $k = 1, 2, 3, 4$ items. A single simulation of LRU with $k = 3$ confirms 4 hits: at $t = 4, 5, 6, 9$.

A non-example: a cyclic scan over $M$ items repeated many times gives every repeated request the reuse distance $M - 1$. The histogram is a single spike, and the LRU miss ratio drops from 1 to almost 0 when $k$ reaches $M$. That cliff is invisible in a mean reuse distance, so use the whole histogram.

## Where it is used

- **Cache sizing.** The histogram gives the LRU miss ratio curve, which tells how much a larger cache would help. Storage systems and key-value caches compute it online with sampling.
- **Compilers and program analysis.** Reuse distance profiles show which loops and data structures cause misses, and they guide loop tiling and data layout. They also predict the locality of a program on larger inputs.
- **Policy design.** Policies such as [LIRS](/lirs/) rank items by their last reuse distance rather than by recency alone, to resist scans.
- **Models.** The distribution of reuse distances is a compact model of [locality of reference](/locality-of-reference/), used to generate synthetic traces.

## References
