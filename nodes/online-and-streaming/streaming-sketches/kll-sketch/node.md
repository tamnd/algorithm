---
tag: 1FW1M3
kind: data-structure
slug: kll-sketch
name: KLL sketch
aliases:
- Karnin-Lang-Liberty sketch
- KLL quantile sketch
area: online-and-streaming/streaming-sketches
level: advanced
summary: Randomized mergeable quantile sketch built from a stack of compactors with geometrically shrinking capacities; with the right top levels it reaches the optimal O((1/ε) log log(1/δ)) items.
model: word-ram
complexity:
  vars: {n: the stream length, ε: the rank accuracy, δ: the failure probability, k: the capacity of the top compactor, H: the number of levels}
  time: {worst: O(k log k + H), amortized: O(log k)}
  space: {extra: O(k + log(n/k))}
properties: {online: true, deterministic: false, mergeable: true}
history:
  year: 2016
  people: [Zohar Karnin, Kevin Lang, Edo Liberty]
  note: Karnin, Lang and Liberty gave the sketch at FOCS 2016 with the matching lower bound for randomized comparison-based algorithms. It builds on the one-pass collapse of Munro and Paterson (1980) and of Manku, Rajagopalan and Lindsay (1998), and on the randomized compactors of Agarwal et al. (2012).
prereqs: [quantile-summary-problem, azuma-inequality, hoeffding-inequality]
see_also: [greenwald-khanna-summary, munro-paterson-algorithm, q-digest, t-digest, mergeable-summaries, reservoir-sampling, median-trick, epsilon-delta-guarantee]
sources:
  - url: https://arxiv.org/abs/1603.05346
    title: Zohar Karnin, Kevin Lang and Edo Liberty, Optimal quantile approximation in streams, FOCS 2016
    locator: Section 3 (compactors and Theorem 1), Section 4 (samplers, Theorem 2 and Corollary 1), Section 5 (Theorem 3, Theorem 4 with equal top capacities, Theorem 5 with GK on the top levels), Section 6 (Theorem 6, the lower bound)
  - paper: doi:10.1145/2213556.2213562
    title: Pankaj K. Agarwal, Graham Cormode, Zengfeng Huang, Jeff M. Phillips, Zhewei Wei and Ke Yi, Mergeable summaries, PODS 2012
    locator: the section on quantiles (random halving of sorted buffers)
  - paper: doi:10.1145/276304.276342
    title: Gurmeet Singh Manku, Sridhar Rajagopalan and Bruce G. Lindsay, Approximate medians and other quantiles in one pass and with limited memory, SIGMOD 1998
    locator: the buffer collapse scheme and its analysis
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 4, Summaries for Ordered Data (the KLL summary)
---

The KLL sketch is a randomized summary for the [quantile summary problem](/quantile-summary-problem/). It keeps a stack of compactors: level $h$ holds stream items that each stand for $2^h$ original items. When a level fills up, it is sorted and halved at random, and the surviving half moves up one level with twice the weight. Each halving changes any rank by $0$ or $\pm 2^h$ with equal chance, so the rank estimates are unbiased, and the capacities shrink geometrically down the stack so that the low levels, which make many small errors, take little space. The basic sketch answers a rank query within $\varepsilon n$ with probability $1 - \delta$ using $O((1/\varepsilon)\sqrt{\log(1/\delta)} + \log(\varepsilon n))$ items; with changes at the top it uses $O((1/\varepsilon)\log\log(1/\delta))$ items, which is optimal for randomized comparison-based summaries. On this page $n$ is the stream length, and the stream $\sigma$ is insertion only.

## In plain words

Imagine a pile of sorted cards that is getting too tall. You throw away every second card, and you choose at random whether to keep the cards in the odd places or in the even places. Each card you keep now counts for two. Any question of the form "how many cards are below this value?" is off by at most one card's worth after this step, and it is too high or too low with the same chance. The KLL sketch repeats this on many piles stacked on top of each other. The cards that reach the top have been halved many times and count for a lot, so the top piles get the most room. The errors from many small halvings mostly cancel out.

## The abstract type

- **Insert(x)** adds one item from a totally ordered set.
- **Rank(x)** returns $\tilde R(x)$, an estimate of $R(x)$, the number of items at most $x$. For each fixed $x$, $\mathbb{E}[\tilde R(x)] = R(x)$, and $\Pr[|\tilde R(x) - R(x)| > \varepsilon n] \le \delta$.
- **Query(r)** returns a stored item at which the estimated rank first reaches $r$.
- **Merge(S₁, S₂)** returns a sketch of the two streams together, with the same guarantee for $n = n_1 + n_2$.

The guarantee is for each query, in the [(ε, δ) form](/epsilon-delta-guarantee/) with additive error $\varepsilon n$. For all quantiles at once, apply it to the $O(1/\varepsilon)$ ranks at multiples of $\varepsilon n$ with $\delta$ replaced by $\delta\varepsilon$ and use a [union bound](/union-bound/). The sketch is comparison-based: it stores items and only compares them.

## Representation

The sketch has $H$ levels $B_0, \ldots, B_{H-1}$. An item in $B_h$ has weight $w_h = 2^h$. With a parameter $k$ and a ratio $c \in (1/2, 1)$, here $c = 2/3$, level $h$ has the capacity
$$k_h = \max\big(2, \lceil k\,c^{H-1-h} \rceil\big),$$
so the top level has capacity $k$ and each level below has about $c$ times the capacity of the one above. The capacities depend on $H$, so they shrink when a new level is added. The sketch also stores $n$ and one fair random bit per compaction. The total weight $\sum_h 2^h |B_h|$ is always $n$.

## Operations

```pseudo id=main
KLL-INSERT(S, x)
L1  append x to B_0; n ← n + 1
L2  while some level h has |B_h| ≥ k_h do
L3      COMPACT(the lowest such h)

COMPACT(h)
L4  sort B_h; if |B_h| is odd, set aside its largest item
L5  b ← a fair random bit
L6  if h = H − 1 then add an empty level B_H; H ← H + 1
L7  append the items at the positions b + 1, b + 3, b + 5, ... of B_h to B_(h+1)
L8  B_h ← the item set aside, if any; all other items of B_h are dropped

KLL-RANK(S, x)
L9  return the sum over h of 2^h · |{y ∈ B_h : y ≤ x}|

KLL-QUERY(S, r)
L10 sort all stored items, each with its weight; return the first item at which the running weight reaches r
```

A merge appends the levels of the two sketches level by level and then runs the loop of lines L2 and L3. A compaction of $2s$ items at level $h$ keeps $s$ items of twice the weight, so the total weight stays $n$.

## Example

Take $k = 5$ and the 16 items 9, 2, 14, 5, 11, 7, 1, 16, 4, 12, 6, 15, 3, 10, 8, 13. The random bits are 0, 1, 0, 1, 0 in order. Positions count from 1, so bit 0 keeps the odd positions and bit 1 keeps the even ones.

| after item | compacted level | $H$ before, capacities | sorted buffer | bit | moved up |
|---|---|---|---|---|---|
| 11 | 0 | 1, (5) | 2, 5, 9, 11, 14 | 0 | 2, 9 (14 stays) |
| 16 | 0 | 2, (4, 5) | 1, 7, 14, 16 | 1 | 7, 16 |
| 15 | 0 | 2, (4, 5) | 4, 6, 12, 15 | 0 | 4, 12 |
| 15 | 1 | 2, (4, 5) | 2, 4, 7, 9, 12, 16 | 1 | 4, 9, 16 |
| 8 | 0 | 3, (3, 4, 5) | 3, 8, 10 | 0 | 3 (10 stays) |

The first compaction creates level 1, and the fourth creates level 2, which shrinks the capacity of level 0 to $\lceil 5 \cdot (2/3)^2 \rceil = 3$. At the end, $B_0 = \{10, 13\}$ with weight 1, $B_1 = \{3\}$ with weight 2, and $B_2 = \{4, 9, 16\}$ with weight 4. The total weight is $2 + 2 + 12 = 16$, using 6 stored items.

The rank estimates for $x = 1, \ldots, 16$ are 0, 0, 2, 6, 6, 6, 6, 6, 10, 11, 11, 11, 12, 12, 12, 16, against the true ranks 1 to 16. The largest error is 2. For instance, Rank(4) $= 2 \cdot 1 + 4 \cdot 1 = 6$. Query(8) runs over 3 (weight 2), 4 (4) and 9 (4), with running weights 2, 6, 10, and returns 9, whose true rank is 9. There were four compactions at level 0 and one at level 1, so the variance proxy of the proof is $V = 4 \cdot 1^2 + 1 \cdot 2^2 = 8$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has four steps.

1. **One compaction.** Let $a$ be the number of compacted items at most $x$. They form a prefix of the sorted buffer, and $\lceil a/2 \rceil$ of them are at odd positions and $\lfloor a/2 \rfloor$ at even positions. So the compaction changes $\tilde R(x)$ by $2w\lceil a/2 \rceil - wa$ or $2w\lfloor a/2 \rfloor - wa$, which is $0$ if $a$ is even and $+w$ or $-w$ with probability $1/2$ each if $a$ is odd.
2. **The schedule is fixed.** The sizes of the levels, the number $H$ and the number $m_h$ of compactions of each level depend only on $n$ (and on the merge order), not on the random bits. So the error $\tilde R(x) - R(x)$ is a sum of martingale differences with fixed bounds $w_h$.
3. **Counting compactions.** Each compaction of level $h$ consumes at least $k_h - 1 \ge k_h/2$ items of weight $2^h$, and at most $n$ weight ever passes through a level, so $m_h \le 2n/(k_h 2^h)$. A new top level appears only when a level of capacity $k$ is compacted, so $2^{H-1} \le 2n/k$.
4. **Azuma.** These give $V = \sum_h m_h 4^h \le (8c/(2c - 1))\,n^2/k^2$, which is $16n^2/k^2$ for $c = 2/3$, and the Azuma-Hoeffding inequality gives $\Pr[|\tilde R(x) - R(x)| \ge \varepsilon n] \le 2\exp(-\varepsilon^2 k^2/32)$.

So $k = \lceil \sqrt{32\ln(2/\delta)}/\varepsilon \rceil$ gives error $\varepsilon n$ with probability $1 - \delta$. The improvements to $O((1/\varepsilon)\log\log(1/\delta))$ are only sketched in the proof file.

## Complexity

**Space.** At most $\sum_h k_h \le \sum_h (k c^{H-1-h} + 1) + H \le k/(1 - c) + 2H = 3k + 2H$ items for $c = 2/3$, and $H \le \log_2(n/k) + 2$. With the $k$ above this is $O((1/\varepsilon)\sqrt{\log(1/\delta)} + \log(\varepsilon n))$ items, which is Theorem 1 of the paper. The sketch needs one random bit per compaction, so $O(n/k)$ random bits in all, and no hash functions.

**Better bounds from the paper.** Theorem 2 and Corollary 1 replace the many lowest levels, whose capacity is 2, by a sampler of one item, which gives $O((1/\varepsilon)\sqrt{\log(1/\delta)})$ items and stays mergeable. Theorem 4 gives the top $s = O(\log\log(1/\delta))$ levels the same capacity $k$, which gives $O((1/\varepsilon)\log^2\log(1/\delta))$ items and stays mergeable. Theorem 5 feeds the top levels into a [GK summary](/greenwald-khanna-summary/) instead, which gives $O((1/\varepsilon)\log\log(1/\delta))$ items but is not mergeable.

**Lower bound.** Theorem 6 of the paper: a randomized comparison-based algorithm that returns an $\varepsilon$-approximate quantile with probability $1 - \delta$ must store $\Omega((1/\varepsilon)\log\log(1/\delta))$ items. The proof takes streams of length $n = C\varepsilon^{-2}\log^2(1/\varepsilon)$ and $\delta = 1/(2\,n!)$. Then, with probability at least $1/2$, one string of random bits works for all $n!$ orders at once, and fixing it gives a deterministic algorithm. The deterministic lower bound $\Omega((1/\varepsilon)\log(1/\varepsilon))$ of Hung and Ting then applies, and $\log\log(1/\delta) = \Theta(\log(1/\varepsilon))$ here. So the bound is shown for this range of $\delta$, and Theorem 5 matches it.

**Time.** An insert that triggers no compaction is $O(1)$. A compaction of level $h$ sorts $k_h$ items, and level $h$ is compacted at most $2n/(k_h 2^h)$ times, so the total sorting work is $\sum_h (2n/(k_h 2^h))\,O(k_h\log k_h) = O(n\log k)$, that is $O(\log k)$ amortized per insert. One insert can cascade through all levels, which costs $O(k\log k + H)$ in the worst case. Rank is $O(\text{size})$; Query sorts the stored items once, $O(k\log k)$.

## Variants

- **Lazy compaction.** Practical versions compact only when the whole sketch exceeds its total capacity, and then compact the lowest full level. This uses the space better and keeps the same analysis.
- **Samplers at the bottom.** As in Theorem 2, levels with capacity 2 are replaced by one reservoir sample of weight $2^h$ (see [reservoir sampling](/reservoir-sampling/)).
- **Relative error.** The REQ sketch of Cormode, Karnin, Liberty, Thaler and Veselý (2021) compacts only the upper half of each buffer, so that small ranks are kept with relative error.
- **Deterministic halving.** Always keeping the odd positions gives a deterministic summary in the style of [Munro and Paterson](/munro-paterson-algorithm/), but the errors then add up instead of cancelling, and it needs $O((1/\varepsilon)\log^2(\varepsilon n))$ items.

## When to use it

Use the KLL sketch when you need quantiles over large or distributed data, a small and predictable size, and merges of sketches from many machines. Apache DataSketches and several databases ship it. If you need a guarantee on every query without randomness, use the [GK summary](/greenwald-khanna-summary/) or the [q-digest](/q-digest/). If you only need the tails with relative error, use a relative-error variant.

## Pitfalls

- **The guarantee is per query.** $\delta$ bounds the failure of one fixed rank query. A query whose value is chosen after looking at the sketch is not covered, and all quantiles at once need a union bound.
- **Fresh random bits.** Each compaction needs its own fair bit. Reusing one bit for all compactions makes the errors of a level add up.
- **Odd buffers.** Compact an even number of items. Promoting from an odd buffer breaks the conservation of weight and biases the ranks.
- **Capacities shrink.** When a level is added, the lower capacities drop, so the loop of lines L2 and L3 must keep running until no level is full.
- **Small $k$.** The bound $2\exp(-\varepsilon^2k^2/32)$ is loose. Apache DataSketches documents a normalized rank error of about 1.65 percent at 99 percent confidence for $k = 200$, an empirical figure. Size the sketch from such measurements or from the variance proxy $V$, not from the constant 32.
- **Weights in Query.** Sort items with their weights; counting stored items without weights gives badly wrong ranks.

## Implementations

## History

Munro and Paterson (1980) used samples that are merged and halved for multi-pass selection, and the [Munro-Paterson algorithm](/munro-paterson-algorithm/) page explains how its one-pass form already gives approximate quantiles. Manku, Rajagopalan and Lindsay (1998) turned the collapse of buffers into a one-pass quantile summary, and in 1999 added random sampling to remove the need to know $n$. Agarwal et al. (2012) showed that halving with a random offset makes the error unbiased and the summary mergeable. Karnin, Lang and Liberty (2016) used geometric capacities, so that the low levels are small, and proved the optimal bound with a matching lower bound.

## References
