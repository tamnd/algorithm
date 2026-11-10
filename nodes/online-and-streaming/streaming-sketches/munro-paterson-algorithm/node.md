---
tag: T3177E
kind: algorithm
slug: munro-paterson-algorithm
name: Munro-Paterson algorithm
aliases:
- Munro-Paterson multipass selection
area: online-and-streaming/streaming-sketches
level: advanced
summary: Exact selection of the k-th smallest of n items in p passes over a stream with O(n^(1/p) (log n)^(2 - 2/p)) storage, by samples that are merged and thinned. Its one-pass form led to KLL.
solves: [selection-problem]
model: comparison-model
complexity:
  vars: {n: the stream length, p: the number of passes, s: the sample size}
  time: {worst: O(p n log s)}
  space: {extra: O(n^(1/p) (log n)^(2 - 2/p))}
properties: {online: false, deterministic: true, comparison: true, exact: true, multi_pass: true}
history:
  year: 1980
  people: [J. Ian Munro, Mike S. Paterson]
  note: Munro and Paterson gave the multi-pass selection algorithm and the matching lower bound Ω(n^(1/p)) in Theoretical Computer Science in 1980, after a FOCS 1978 version.
prereqs: [selection-problem, order-statistic, streaming-model, merge-sort]
see_also: [kll-sketch, greenwald-khanna-summary, quantile-summary-problem, median-of-medians, quickselect, mergeable-summaries, comparison-model, dyadic-intervals]
sources:
  - paper: doi:10.1016/0304-3975(80)90061-4
    title: J. Ian Munro and Mike S. Paterson, Selection and sorting with limited storage, Theoretical Computer Science 12(3), 1980
    locator: pp. 315 to 323; Section 3.1 (the sample scheme, Lemma 2 with L_ij = j 2^i - 1 and M_ij = (i + j - 1) 2^i, the choice of filters, Lemma 1, Theorem 2), Section 4 (Theorem 4, Corollaries 1 and 2, Lemma 3)
  - paper: doi:10.1145/276304.276342
    title: Gurmeet Singh Manku, Sridhar Rajagopalan and Bruce G. Lindsay, Approximate medians and other quantiles in one pass and with limited memory, SIGMOD 1998
    locator: the one-pass framework of buffers that are collapsed, and its O((1/ε) log^2(εn)) space bound
  - url: https://arxiv.org/abs/1603.05346
    title: Zohar Karnin, Kevin Lang and Edo Liberty, Optimal quantile approximation in streams, FOCS 2016
    locator: Section 1 (the history from Munro and Paterson to MRL and Agarwal et al.), Section 2 (compactors)
---

The Munro-Paterson algorithm finds the exact $k$-th smallest of $n$ items that can only be read in order, one pass after the other, with small storage. In each pass it builds a sample by merging and thinning sorted blocks, and the sample gives two filters with the answer between them and few items between them. With $p$ passes it needs $O(n^{1/p}(\log n)^{2 - 2/p})$ storage, and Munro and Paterson proved that $\Omega(n^{1/p})$ is necessary. On this page $n$ is the stream length, the items come from a totally ordered set, and a pass reads the whole stream once.

## In plain words

Think of a long tape of numbers that you can read from start to end many times, but you can keep only a few numbers in memory. You want the number that has exactly a given place in sorted order. On each read you keep two fences, and you know that the answer lies between them. You ignore the numbers outside the fences, and only count how many lie below the lower fence. From the numbers between the fences you build a small, well spread sample: you sort short pieces, keep every second number of each, and join pieces two at a time. The sample tells you where to put two new fences that are much closer together. After a few reads so few numbers lie between the fences that you can keep them all and pick the answer directly.

## The problem

The input is a stream $\sigma = x_1, \ldots, x_n$ of items from a totally ordered set and a rank $k$ with $1 \le k \le n$. The algorithm may read $\sigma$ from start to end $p$ times and may compare items, but it cannot write to the stream. The output is the $k$-th smallest item, as in the [selection problem](/selection-problem/). The cost measure is the storage, counted in items: the number of items that the algorithm holds at one time.

The paper counts from the top (the $K$-th highest). This page counts from the bottom, which is the same up to a reversal of the order. Equal values are kept apart by their position in the stream, so all keys are distinct.

## The algorithm

Fix an even sample size $s$. A *sample at level $i$* is a sorted list of $s$ items taken from a set of $2^i s$ items, its *population*, by this rule.

- A sample at level 0 is its whole population of $s$ items, sorted.
- A sample at level $i + 1$ comes from a population split into two halves of $2^i s$ items. Take a sample at level $i$ of each half, *thin* each one by keeping only its 2nd, 4th, 6th, ... smallest items, and merge the two thinned halves into one sorted list of $s$ items.

In one pass the items arrive in order, so the samples are built bottom up, like a binary counter. Each full block of $s$ items is a sample at level 0. When a new sample at level $i$ is ready and a thinned sample of level $i$ waits, the two are merged into a sample at level $i + 1$. So at most one thinned sample waits at each level. At the end the pass adds imaginary items $+\infty$ until there are $2^r s$ items for some $r$.

The filters $lo$ and $hi$ start at $-\infty$ and $+\infty$. In each pass the *population* is the set of items $x$ with $lo \le x \le hi$, and $k'$ is the rank of the answer in it.

```pseudo id=main
MP-SELECT(σ, k, s, M)
L1  lo ← −∞; hi ← +∞; B ← ∞
L2  repeat, with one new pass over σ each time
L3      final ← (B ≤ M)
L4      for each x in σ: if x < lo then below ← below + 1, else if x ≤ hi then SAMPLE-ADD(x), or store x if final
L5      k' ← k − below
L6      if final then sort the stored items and return the k'-th of them
L7      (Q, r) ← SAMPLE-FINISH
L8      u ← ⌊(k' − 1)/2^r⌋ − r + 1; v ← ⌈k'/2^r⌉
L9      if u ≥ 1 then lo ← Q[u]; if Q[v] is not imaginary then hi ← Q[v]; if lo = hi then return lo
L10     B ← min((2r − 1)·2^r + 2, the population size)

SAMPLE-ADD(x)
L11 append x to the block; when the block holds s items, sort it and CARRY it as a sample at level 0

CARRY(Q)
L12 i ← 0; while a thinned sample T waits at level i: Q ← merge(T, thin(Q)); remove T; i ← i + 1
L13 let thin(Q) wait at level i

SAMPLE-FINISH
L14 pad the block, then add blocks of +∞, until there are 2^r blocks; the last CARRY gives the sample Q at level r
```

Here $M$ is the storage for the last pass. Line L10 is a proven bound on the size of the next population, so the last pass never stores more than $M$ items.

## Example

Take the 32 items $14, 3, 25, 9, 30, 1, 18, 22, 7, 27, 12, 5, 20, 31, 16, 0, 29, 10, 24, 2, 13, 26, 8, 19, 4, 28, 11, 23, 6, 17, 15, 21$, which are the numbers 0 to 31 in some order, with $s = 8$, $M = 16$ and $k = 11$. The answer is 10. Here the number of items below a value $x$ is $x$ itself.

**Pass 1.** The population is all 32 items. The four blocks of 8, sorted and thinned, are these.

| block | sorted (a sample at level 0) | thinned |
|---|---|---|
| 1 | 1, 3, 9, 14, 18, 22, 25, 30 | 3, 14, 22, 30 |
| 2 | 0, 5, 7, 12, 16, 20, 27, 31 | 5, 12, 20, 31 |
| 3 | 2, 8, 10, 13, 19, 24, 26, 29 | 8, 13, 24, 29 |
| 4 | 4, 6, 11, 15, 17, 21, 23, 28 | 6, 15, 21, 28 |

Blocks 1 and 2 merge into the level 1 sample $3, 5, 12, 14, 20, 22, 30, 31$, and blocks 3 and 4 into $6, 8, 13, 15, 21, 24, 28, 29$. These thin to $5, 14, 22, 31$ and $8, 15, 24, 29$, which merge into the level 2 sample $Q = 5, 8, 14, 15, 22, 24, 29, 31$, so $r = 2$.

Lemma 2 below says that the $j$-th item of $Q$ has between $4j - 1$ and $4(j + 1)$ items below it. For $j = 3$ that is between 11 and 16, and indeed 14 has 14 items below it. With $k' = 11$, line L8 gives $u = \lfloor 10/4 \rfloor - 2 + 1 = 1$ and $v = \lceil 11/4 \rceil = 3$, so $lo = Q[1] = 5$ and $hi = Q[3] = 14$. Line L10 gives the bound $B = 3 \cdot 4 + 2 = 14 \le M$.

**Pass 2.** The items below 5 are $0, \ldots, 4$, so $below = 5$ and $k' = 6$. The population is the 10 items $5, \ldots, 14$, at most $B$. The pass stores them, and the 6th smallest is 10.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has three steps.

1. **Samples are well spread (Lemma 2 of the paper).** Let $L_{ij}$ and $M_{ij}$ be the least and the largest number of population items that can lie below the $j$-th smallest item of a sample at level $i$. Then $L_{ij} = j 2^i - 1$ and $M_{ij} = (i + j - 1)2^i$. At level 0 both are $j - 1$. At level $i$, if $p$ of the first $j$ items come from one half and $q = j - p$ from the other, the $j$-th item is the $2p$-th item of one level $i - 1$ sample and lies between the $2q$-th and the $(2q + 2)$-th item of the other. This gives $L_{ij} = L_{i-1,2p} + L_{i-1,2q} + 1$ and $M_{ij} = M_{i-1,2p} + M_{i-1,2q+2}$, and induction gives the formulas.
2. **The filters keep the answer.** The answer has $k' - 1$ population items below it. The $u$-th item of $Q$ has at most $M_{ru} = (r + u - 1)2^r \le k' - 1$ items below it, so it is at most the answer. The $v$-th item has at least $L_{rv} = v 2^r - 1 \ge k' - 1$ below it, so it is at least the answer. Imaginary items are larger than all real items, so they never become $lo$.
3. **The population shrinks.** Since $\lceil k'/2^r \rceil = \lfloor (k' - 1)/2^r \rfloor + 1$, $v - u = r$. Between the $u$-th and the $v$-th item lie at most $M_{rv} - L_{ru} - 1 = (2r - 1)2^r$ items, so with the two filters the next population has at most $(2r - 1)2^r + 2$ items, the bound of line L10.

So every pass keeps the answer between the filters and $k'$ is its rank among them, and the last pass returns it.

## Complexity

**Storage of one pass.** One pass holds the filters, the block of at most $s$ items, and at most one thinned sample of $s/2$ items at each level below $r$. So it holds at most $rs/2 + s + 2$ items, the bound in the paper. The tests check this bound on every pass.

**Shrinking.** In a pass with population $n'$, $r = \lceil \log_2(n'/s) \rceil$, so $2^r < 2n'/s$ and the next population is at most $(2r - 1)2^r + 2 < 4rn'/s$. With storage $S$, take $s \approx 2S/\log_2 n$ and $r \le \log_2 n$. Then the next population is $O(n' (\log n)^2 / S)$, which is Lemma 1 of the paper.

**Passes (Theorem 2 of the paper).** After $p - 1$ passes the population is $O(n((\log n)^2/S)^{p-1})$, and the last pass can store it if this is at most $S$. Solving gives the storage
$$S = O\big(n^{1/p}(\log n)^{2 - 2/p}\big)$$
for exact selection in $p$ passes. For two passes this is $O(\sqrt{n}\log n)$. The scheme needs $S = \Omega((\log n)^2)$, so that $s$ exceeds about $4r$; otherwise the filters do not move closer. The implementation stops with an error in that case.

**Lower bound (Theorem 4 of the paper).** Each $p$-pass algorithm that finds the median, or the $k$-th smallest for $k = \Theta(n)$, needs $\Omega(n^{1/p})$ storage. The key step (Lemma 3) is an adversary. After one pass with storage $S$ it leaves a set $X$ of at least $\lfloor n/(2S - 1) \rfloor$ items, none of them stored and no two of them compared, whose median is the median of the whole input. So each pass divides the size of the problem by $O(S)$ at best. Corollary 1 gives $\Omega(\sqrt{n}) \le S \le O(\sqrt{n}\log n)$ for two passes. Corollary 2: for $\log S = \Omega(\sqrt{\log n \log\log n})$ the number of passes needed is $\log n/\log S + O(1)$. The same paper shows that sorting in $p$ passes needs about $n/(4p)$ storage, by an argument on items that must be compared.

**Time.** Each pass sorts blocks of $s$ items, $O(n \log s)$, and the merges at level $i$ touch $n/2^i$ items, $O(n)$ in all. So the time is $O(n\log s)$ per pass and $O(pn\log s)$ in all.

## Properties

- **Exact and deterministic.** There is no error and no randomness. The answer is always the $k$-th smallest item.
- **Comparison based.** It uses only comparisons, so it works for any totally ordered set.
- **Read-only, multi-pass.** It never writes to the stream; it needs the stream again for each pass.
- **Counts as well as samples.** Items outside the filters are only counted, which fixes the rank of the answer inside the population.
- **One pass gives approximate ranks.** By Lemma 2, the $j$-th item of the final sample has rank between $j2^r$ and $(r + j - 1)2^r + 1$, so a single pass gives each rank within about $r 2^r \approx rn/s$.

## Variants and improvements

- **The one-pass collapse and MRL.** Take only the first pass and stop. The final sample is then an approximate quantile summary with rank error at most $r 2^r$, which is $\varepsilon n$ when $s \approx r/\varepsilon$. The storage is $r$ waiting halves of $s/2$ items, $O((1/\varepsilon)\log^2(\varepsilon n))$ items. Manku, Rajagopalan and Lindsay (1998) built their one-pass quantile summary on this idea, with buffers of $s$ items that are *collapsed* (merged, sorted, and thinned) when they are full. This step, from a pass of exact selection to a summary of one pass, is the root of all later sketches of this kind.
- **Random thinning and KLL.** Thinning always keeps the even positions, so the errors of all levels can add up, and the bound $r 2^r$ grows with $r$. If a fair coin chooses between the odd and the even positions, the error of each thinning has mean 0, and the errors of the levels cancel in the way of a random walk. Agarwal et al. (2012) used this to make the summary mergeable. The [KLL sketch](/kll-sketch/) of Karnin, Lang and Liberty (2016) keeps random thinning and also makes the lower levels smaller, with capacities that shrink by a factor $c < 1$ per level. That gives $O((1/\varepsilon)\log\log(1/\delta))$ space, which is optimal. A thinning step of KLL is called a *compaction*, and it is exactly the thin-and-merge step on this page.
- **Merging more than two.** Munro and Paterson remark that merging samples five at a time instead of two at a time saves a constant factor of storage.
- **Very small storage.** For $2 \le S \le O((\log n)^2)$, their Theorem 3 gives $O((\log n)^3/S)$ passes, by simulating one pass of the main scheme with several passes.
- **Random order.** If the stream comes in random order, far fewer passes are needed for the same storage; Guha and McGregor (2009) study this case.

## When to use it

Use it when the data is too large for memory, can be read many times in the same order (a file, a tape, a table scan), and the exact order statistic is needed. If an approximate rank is enough, one pass of a [GK summary](/greenwald-khanna-summary/) or a [KLL sketch](/kll-sketch/) is cheaper. A common practical scheme is a two-pass hybrid in this spirit: one approximate pass to choose filters and one counting pass to finish exactly.

## Pitfalls

- **Too small a sample.** If $s$ is about $2r$ or less, the bound $(2r - 1)2^r + 2$ is no smaller than the population and the filters do not move. The sample size must grow like $\log n$, so the storage must be at least of order $(\log n)^2$.
- **Equal values.** The analysis needs distinct keys. Break ties by position in the stream, or count the items equal to a filter, or the population can be wrong by the number of copies.
- **The rank inside the population.** The rank $k'$ must be updated from the count of items below $lo$ in the same pass. The filters are chosen at the end of a pass, so their ranks are only known in the next pass.
- **The imaginary items.** Padding with $+\infty$ must not move a filter to an imaginary item. With $k' \le n'$ the lower filter is always real, but the upper filter can be imaginary and must then stay where it was.
- **Ranks from the top.** The paper selects the $K$-th highest. Its formulas $u = \lfloor (k-1)/2^r \rfloor - r + 1$ and $v = \lceil k/2^r \rceil$ count from the top; on this page they count from the bottom.

## Implementations

## History

Munro and Paterson presented the work at FOCS 1978 and published it in Theoretical Computer Science in 1980. They proved the upper bound $O(n^{1/p}(\log n)^{2 - 2/p})$ and the lower bound $\Omega(n^{1/p})$ for $p$-pass selection, and bounds for sorting with limited storage. Pohl (1969) had studied the storage for the median in one pass. Manku, Rajagopalan and Lindsay (1998) took the sample scheme to one pass for approximate quantiles. Agarwal et al. (2012) and Karnin, Lang and Liberty (2016) added random thinning, which led to the optimal [KLL sketch](/kll-sketch/).

## References
