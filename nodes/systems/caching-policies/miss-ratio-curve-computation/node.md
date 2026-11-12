---
tag: XPW03J
kind: problem
slug: miss-ratio-curve-computation
name: Miss ratio curve computation
aliases:
- MRC computation
- miss ratio curve construction
area: systems/caching-policies
level: advanced
summary: "Compute the miss ratio of a cache for every size from one trace. For LRU, exact tree methods take O(n log m) time; sampling and models trade a small error for less work."
prereqs: [miss-ratio-curve, reuse-distance, fenwick-tree]
see_also: [mattson-stack-algorithm, shards, order-statistic-tree, balanced-binary-search-tree, inclusion-property, reservoir-sampling, cache-hit-ratio, lru]
sources:
  - paper: doi:10.1147/sj.92.0078
    title: "R. L. Mattson, J. Gecsei, D. R. Slutz and I. L. Traiger, Evaluation techniques for storage hierarchies, IBM Systems Journal 9(2) (1970), 78-117"
    locator: stack processing, which gives the success function of a stack algorithm for all capacities in one pass
  - paper: doi:10.1147/rd.194.0353
    title: "B. T. Bennett and V. J. Kruskal, LRU stack processing, IBM Journal of Research and Development 19(4) (1975), 353-357"
    locator: the computation of LRU stack distances with a tree over the positions of the trace in O(n log n) time
  - paper: "Frank Olken, Efficient methods for calculating the success function of fixed space replacement policies, Lawrence Berkeley Laboratory report LBL-12370, 1981"
    title: "Frank Olken, Efficient methods for calculating the success function of fixed space replacement policies, LBL-12370, 1981"
    locator: a balanced tree keyed by the time of last use, which gives O(n log m) time and O(m) space
  - paper: "Carl A. Waldspurger, Nohhyun Park, Alexander Garthwaite and Irfan Ahmad, Efficient MRC construction with SHARDS, 13th USENIX Conference on File and Storage Technologies (FAST 15), 2015, 95-110"
    title: "Waldspurger, Park, Garthwaite and Ahmad, Efficient MRC construction with SHARDS, FAST 2015"
    locator: Section 2.2, the cost O(N log M) time and O(M) space of exact methods, and sampling by a hash of the location
  - paper: "Xiameng Hu, Xiaolin Wang, Lan Zhou, Yingwei Luo, Chen Ding and Zhenlin Wang, Kinetic modeling of data eviction in cache, USENIX Annual Technical Conference (ATC 16), 2016, 351-364"
    title: "Hu, Wang, Zhou, Luo, Ding and Wang, Kinetic modeling of data eviction in cache, USENIX ATC 2016"
    locator: Section 2.2, the average eviction time (AET) model, with P(t) from the reuse time histogram and the miss ratio P(AET(c))
---

Miss ratio curve computation asks for the miss ratio of a cache at each size, from one trace of requests. The output is the [miss ratio curve](/miss-ratio-curve/) $m(c)$ for $c = 0, 1, \ldots$. Simulating a cache at each size separately is too slow for long traces and many sizes. For [LRU](/lru/) and other policies with the [inclusion property](/inclusion-property/), one pass gives all sizes at once. The exact methods take $O(n \log m)$ time on a trace of $n$ requests with $m$ distinct items. Sampling methods such as [SHARDS](/shards/) and models such as AET are faster, use less memory, and have a small error.

## In plain words

You have a long log of which items a program asked for. You want to know, for each possible cache size, how often the cache would miss. You could replay the log once for each size, but a storage trace may have a billion requests and a million useful sizes.

For LRU there is a shortcut. For each request, count how many different items were used since the last time this item was used. An LRU cache hits the request exactly when this count is less than its size. So one pass that finds these counts, and a table of how often each count occurs, gives the answer for all sizes. The hard part is to find the counts fast, without a long scan for each request.

## Definition

**Input.** A trace $\sigma_1 \cdots \sigma_n$ over a set of $m$ distinct items, and a largest size $C$ (often $C = m$).

**Output.** For each $c = 0, 1, \ldots, C$, the miss ratio $m(c)$ of an LRU cache of size $c$ that starts empty.

The [reuse distance](/reuse-distance/) $d_t$ of request $t$ is the number of distinct other items requested since the previous request for $\sigma_t$, or $\infty$ if there is none. An LRU cache of size $c$ hits request $t$ exactly when $d_t < c$. So with $h(d) = |\{t : d_t = d\}|$,

$$m(c) = 1 - \frac{1}{n} \sum_{d < c} h(d),$$

and the problem is the same as computing the histogram $h$. Mattson's stack distance is $d_t + 1$.

## Variants

- **Other stack algorithms.** For a policy with the inclusion property, the [Mattson stack algorithm](/mattson-stack-algorithm/) gives the curve from the depth of each item in a priority stack. LFU and Belady's MIN fit here; the tree methods below are for LRU.
- **Policies without inclusion.** For FIFO, CLOCK, ARC and most modern policies the cache content at one size says nothing about another size. The curve needs one simulation per size, often on a sampled trace.
- **Byte sizes.** With objects of different sizes, $c$ is in bytes. The LRU stack still works, but the distance is the total size of the distinct objects since the last use, not their number.
- **Online.** A system computes the curve while it runs, with bounded memory, to resize or partition its caches every few minutes.
- **Approximate.** The curve only needs to be close, for example with a mean absolute error below $0.01$ over all sizes.

## Examples

Take the trace $a\,b\,c\,b\,a\,d\,a\,c$, so $n = 8$ and $m = 4$.

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| request | $a$ | $b$ | $c$ | $b$ | $a$ | $d$ | $a$ | $c$ |
| reuse distance | $\infty$ | $\infty$ | $\infty$ | 1 | 2 | $\infty$ | 1 | 3 |

The histogram is $h(1) = 2$, $h(2) = 1$, $h(3) = 1$. So $m(0) = m(1) = 1$, $m(2) = 6/8$, $m(3) = 5/8$ and $m(c) = 4/8$ for each $c \ge 4$.

**The tree method on this trace.** Keep a mark at the time of the last use of each item. Before $t = 8$ the last uses are $a$ at 7, $b$ at 4, $c$ at 3 and $d$ at 6, so the marks are at $3, 4, 6, 7$. The previous use of $c$ is at time 3, and the marks after time 3 are at $4, 6, 7$, so $d_8 = 3$. Then the mark moves from 3 to 8. Each mark stands for one distinct item, which is why the count of marks is the count of distinct items. A [Fenwick tree](/fenwick-tree/) over the times $1..n$ gives the count, and the move, in $O(\log n)$ time each.

**A model.** On a trace of 100,000 requests drawn with Zipf weights $1/i^{0.9}$ from 10,000 items, the AET model below differs from the exact curve by $0.0008$ on average over the sizes 0 to 3000, and by at most about $0.007$.

## Known algorithms

| method | time | space | exact |
|---|---|---|---|
| one LRU simulation per size | $O(nC)$ | $O(C)$ | yes |
| Mattson's LRU stack (Mattson et al. 1970) | $O(nm)$ | $O(m)$ | yes |
| tree over positions (Bennett and Kruskal 1975) | $O(n \log n)$ | $O(n)$ | yes |
| balanced tree of last-use times (Olken 1981) | $O(n \log m)$ | $O(m)$ | yes |
| SHARDS, fixed rate $R$ (Waldspurger et al. 2015) | $O(n + Rn \log(Rm))$ | $O(Rm)$ | no |
| SHARDS, fixed size $s$ | $O(n + n_s \log s)$, with $n_s$ the sampled requests | $O(s)$ | no |
| AET model (Hu et al. 2016) | $O(n)$ | $O(n)$, less with sampling | no |

- **Mattson's stack.** Keep the items in a list in the order of last use. The position of the requested item is its distance; move it to the front. A scan can take $\Theta(m)$ time.
- **Tree methods.** Mark the time of the last use of each item. The distance of request $t$ to an item last used at time $p$ is the number of marks in $(p, t)$. Bennett and Kruskal kept counts in a tree over the positions of the trace. Olken kept only the $m$ live marks in a balanced tree keyed by time, with subtree sizes, an [order statistic tree](/order-statistic-tree/); this gives $O(n \log m)$ time and $O(m)$ space. The code below uses a Fenwick tree over all $n$ times.
- **SHARDS.** Keep only the items whose hash falls below a threshold, a fraction $R$ of all items, and run a tree method on them. Each distance found is scaled by $1/R$. See [SHARDS](/shards/).
- **AET.** Hu et al. use only reuse times, which are easy to count. Let $P(t)$ be the fraction of requests whose reuse time is greater than $t$, with first uses counted as $\infty$. The average eviction time $\mathrm{AET}(c)$ of a cache of size $c$ solves $\sum_{t < \mathrm{AET}(c)} P(t) = c$, and the model gives $m(c) = P(\mathrm{AET}(c))$. It is exact for a loop and close for traces where the items are requested independently.
- **Counter Stacks.** Wires et al. (OSDI 2014) estimate the distances with probabilistic counters of distinct items, in sublinear space.

## Bounds

- The exact tree methods take $O(n \log m)$ time and $O(m)$ space. The SHARDS paper cites this cost as the reason exact methods are too expensive to run online on storage traces.
- Mattson's list takes $\Theta(nm)$ time in the worst case, for example on a loop over $m$ items.
- SHARDS with a fixed size uses constant memory. The paper reports a median mean absolute error of $0.0072$ for a sample of 8,000 items over 124 traces, and less with a small correction.
- No lower bound for exact computation above $\Omega(n)$ is stated in these sources.

## Reductions

- **Curve and histogram.** The LRU curve and the histogram of reuse distances give each other: one is the running sum of the other, and $h(d) = n\,(m(d) - m(d + 1))$.
- **Distinct elements in a range.** A reuse distance is the number of distinct values in a range of the trace. The marks reduce it to counting marked positions in a range, a prefix sum query.
- **Sampling.** Hashing the item, not the request, keeps all requests to each sampled item. The distances among sampled items are then about $R$ times the true distances, which is why scaling by $1/R$ works.

## Applications

- **Cache sizing and partitioning** in storage arrays, hypervisors, key-value caches and shared processor caches, where a curve per tenant decides how much space each tenant gets.
- **Workload study.** The curve shows the working sets of a trace as drops.
- **Removing cliffs.** Talus needs the curve to find the convex hull; see [miss ratio curve](/miss-ratio-curve/).
- **Choosing a policy.** Curves of several policies on one trace show where one policy wins.

## References
