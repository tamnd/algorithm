---
tag: NTSNHM
kind: algorithm
slug: streaming-k-median
name: Streaming k-median
aliases:
- Guha et al. streaming k-median
- Small-Space algorithm
- divide-and-conquer streaming k-median
area: machine-learning/clustering
level: research
summary: One-pass constant-factor approximation for k-median over a data stream.
solves: [k-median-problem]
model: streaming-model
complexity:
  vars: {n: the number of points in the stream, k: the number of medians, m: "the buffer size (k < m)", L: the number of levels, s: the most swaps in one call of the local solver}
  time: {worst: "O((n + L^2 m) m k^2 (s + 1))"}
  space: {extra: "O(L^2 m^2)"}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2000
  people: [Sudipto Guha, Nina Mishra, Rajeev Motwani, Liadan O'Callaghan]
  note: Guha, Mishra, Motwani and O'Callaghan gave the divide and conquer method at FOCS 2000; the journal version of 2003 with Meyerson adds a randomized version and experiments.
prereqs: [k-median-problem, streaming-model, local-search, divide-and-conquer-paradigm]
see_also: [partitioning-around-medoids, k-median-problem, meyerson-algorithm, online-facility-location-problem, coreset, birch, bfr-algorithm, mini-batch-k-means]
sources:
  - paper: "S. Guha, N. Mishra, R. Motwani and L. O'Callaghan, Clustering data streams, Proceedings of FOCS 2000, pp. 359-366"
    title: Guha, Mishra, Motwani and O'Callaghan 2000
    locator: the Small-Space algorithm and the one-pass stream algorithm
  - paper: "S. Guha, A. Meyerson, N. Mishra, R. Motwani and L. O'Callaghan, Clustering data streams: theory and practice, IEEE Transactions on Knowledge and Data Engineering 15(3), 2003, pp. 515-528"
    title: Guha et al. 2003
    locator: "Theorems 1 to 4 (the factor 2c(1 + 2b) + 2b of one level), Theorem 5 (more levels) and Theorem 6 (time O(n^(1+ε)), memory n^ε, factor 2^O(1/ε))"
  - paper: "V. Arya, N. Garg, R. Khandekar, A. Meyerson, K. Munagala and V. Pandit, Local search heuristics for k-median and facility location problems, SIAM Journal on Computing 33(3), 2004, pp. 544-562"
    title: Arya et al. 2004
    locator: the factor 5 of single-swap local search, used here as the solver
  - paper: "M. Charikar, L. O'Callaghan and R. Panigrahy, Better streaming algorithms for clustering problems, Proceedings of STOC 2003, pp. 30-39"
    title: Charikar, O'Callaghan and Panigrahy 2003
    locator: a constant factor with memory polynomial in k and log n
  - paper: "L. O'Callaghan, N. Mishra, A. Meyerson, S. Guha and R. Motwani, Streaming-data algorithms for high-quality clustering, Proceedings of ICDE 2002, pp. 685-694"
    title: O'Callaghan et al. 2002
    locator: the LSEARCH local solver and experiments with the STREAM method
---

Streaming k-median is the one-pass method of Guha, Mishra, Motwani and O'Callaghan for the [k-median problem](/k-median-problem/) when the points arrive as a stream and do not fit in memory. It reads the points into a buffer of size $m$. When the buffer is full, it replaces the $m$ points by $k$ medians, each with the number of points that it serves as a weight, and puts the medians into the buffer of the next level. At the end it clusters all the weighted points that are left. Each level loses at most a constant factor, so with a constant number of levels the result is a constant-factor approximation that uses about $n^{\varepsilon}$ memory.

## In plain words

Suppose you must choose $k$ meeting points for a very long list of addresses, but you can keep only a few hundred addresses in memory. Read a few hundred addresses, choose $k$ good meeting points for them, and keep only these meeting points, each with a count of the addresses it stands for. Forget the addresses. Do the same with the next few hundred, and so on.

When you have kept many meeting points, treat them as addresses with counts and summarize them again. At the end, choose $k$ meeting points for everything you still keep.

Each summary moves every address a little. The moves add up, but each level of summaries can make the result worse only by a fixed factor. So the final choice is still within a fixed factor of the best choice.

## The problem

The input is a stream of $n$ points $x_1, x_2, \ldots$ of a [metric space](/metric-space/) $(X, d)$, read once in this order, and an integer $k$. The output is a set $C$ of $k$ points with a small cost $\sum_i d(x_i, C)$, where $d(x, C) = \min_{c \in C} d(x, c)$. The memory must be much smaller than $n$; this is the [streaming model](/streaming-model/). The local problems are weighted: a point $y$ with weight $w$ costs $w\, d(y, C)$.

## The algorithm

```pseudo id=main
STREAM-K-MEDIAN(stream, k, m, SOLVE)        ▷ k < m; SOLVE is a weighted k-median solver
L1  for each point x of the stream do
L2      add (x, 1) to buffer B[0];  i ← 0
L3      while B[i] holds m weighted points do
L4          C ← SOLVE(B[i], k); give each c ∈ C the total weight of the points it serves
L5          empty B[i]; add the weighted medians of C to B[i + 1];  i ← i + 1
L6  F ← the union of all buffers B[0], B[1], ...
L7  return SOLVE(F, k)
```

A median at level $i + 1$ stands for all the original points that its points stand for, so the weights always add up to the number of points read. The solver chooses its medians among the weighted points that it gets. The implementation here uses weighted local search with single swaps, like [PAM](/partitioning-around-medoids/), and an exact solver by enumeration for tests.

## Example

Take points on a line with $d(x, y) = |x - y|$, $k = 2$, $m = 4$ and the exact solver. The stream is $1, 2, 10, 11, 3, 12, 2, 13, 30, 1, 31, 11$. Weights are in brackets; ties go to the first pair in input order.

| after reading | reduction | medians (weight) | cost of the step | buffers after the step |
|---|---|---|---|---|
| $11$ | level 0: $1, 2, 10, 11$ | $1\,(2)$, $10\,(2)$ | 2 | $B[1] = 1(2), 10(2)$ |
| $13$ | level 0: $3, 12, 2, 13$ | $3\,(2)$, $12\,(2)$ | 2 | $B[1] = 1(2), 10(2), 3(2), 12(2)$ |
| $13$ | level 1: $1(2), 10(2), 3(2), 12(2)$ | $1\,(4)$, $10\,(4)$ | 8 | $B[1]$ empty, $B[2] = 1(4), 10(4)$ |
| $11$ | level 0: $30, 1, 31, 11$ | $30\,(2)$, $1\,(2)$ | 11 | $B[1] = 30(2), 1(2)$ |

The final pool is $30(2), 1(2), 1(4), 10(4)$. The exact solver chooses $\{1, 30\}$, with pool cost $4 \cdot 9 = 36$. On the 12 original points these medians cost 57. The best two medians, $2$ and $12$, cost 45. Here $L = 2$ levels did a reduction, so the bound with the exact solver is $(3^{3} - 1) \cdot 45$; the true ratio is $57/45 \approx 1.27$. The loss comes from the last level-0 buffer: it had to serve $11$ from $1$, and at level 1 the medians $3$ and $12$ were merged into $1$ and $10$.

## Correctness

Each original point is represented by exactly one buffered point at all times. When it is moved to a median, the move costs $d(y_i, y_{i+1})$, and by the triangle inequality the final distance of a point is at most the sum of its moves plus the distance of its last representative to the final medians.

If the solver is a $b$-approximation for each buffer and a $c$-approximation at the end, each level multiplies the sum $\mathrm{OPT} + (\text{cost of all moves so far})$ by at most $1 + 2b$. The factor 2 is the price of choosing medians among the buffered points and not anywhere in the space. The final result costs at most $\big((1 + 2c)(1 + 2b)^L - 1\big)\,\mathrm{OPT}$ for $L$ levels with a reduction. For $L = 1$ this is the factor $2c(1 + 2b) + 2b$ of Guha et al. The full proof is on the correctness page.

**The constant of this implementation.** Single-swap local search is a 5-approximation in a metric, so $b = c = 5$ and the factor is $11^{L+1} - 1$: 120 for one level and 1330 for two. With the exact solver ($b = c = 1$) it is $3^{L+1} - 1$, which is 8 for one level. These are worst-case bounds; on real data the ratio is usually close to 1.

## Complexity

- **Levels.** Level $i$ receives at most $n (k/m)^i$ weighted points, so $L \le \lceil \log(n/m) / \log(m/k) \rceil + 1$. With $m = n^{\varepsilon}$ and $k \le \sqrt{m}$, there are $O(1/\varepsilon)$ levels and the factor is $2^{O(1/\varepsilon)}$.
- **Memory.** Each buffer holds fewer than $m$ points, so the buffers take $O(Lm)$ points. The local solver keeps the distance matrix of the points it gets: $m^2$ entries for one buffer and $(Lm)^2$ at the end. The memory does not depend on $n$ except through $L$.
- **Time.** There are at most $2n/m$ reductions if $m \ge 2k$. One call of this local search on $m$ points takes $O(k^2 m^2)$ time per swap pass, because it computes the cost of each of the $k(m - k)$ trial sets. So the time is $O(n m k^2 (s + 1))$ for the levels, where $s$ is the most swaps in one call, plus the final call. Guha et al. reach $O(n^{1 + \varepsilon})$ time with faster solvers.

## Properties

- **One pass.** Each point is read once and then forgotten.
- **Constant factor.** For a fixed number of levels the factor does not depend on $n$.
- **Any metric.** Only distances are needed, and the medians are input points.
- **Order matters.** The buffers depend on the order of the stream, so the medians do too; the bound holds for every order.
- **Weights add up.** The weights in the buffers always sum to the number of points read, so the summary can be used at any time.

## Variants and improvements

- **Small-Space.** The two-level version: split the data into pieces, solve each, then solve the weighted medians. With the local search here its factor is 120.
- **Bicriteria solvers.** Guha et al. allow the solver to return $O(k)$ medians per buffer, for example from a facility location algorithm, which makes the levels faster and the factor better.
- **Randomized version.** Guha et al. (2003) sample and use [online facility location](/online-facility-location-problem/) ideas to get $\tilde{O}(nk)$ time. [Meyerson's algorithm](/meyerson-algorithm/) is the online part of such methods.
- **Polylog memory.** Charikar, O'Callaghan and Panigrahy (2003) get a constant factor with memory polynomial in $k$ and $\log n$.
- **Coresets.** In Euclidean space, merge-and-reduce of [coresets](/coreset/) gives a $(1 + \varepsilon)$ factor with polylogarithmic memory.
- **LSEARCH.** O'Callaghan et al. (2002) use a facility location local search as the solver, which works well in experiments.

## When to use it

Use streaming k-median when the data comes as a stream or is too large to keep, and only distances are available. If the data is Euclidean, coreset methods, [BIRCH](/birch/) or [mini-batch k-means](/mini-batch-k-means/) are often more practical. If the data fits in memory, run a k-median algorithm on all of it.

## Pitfalls

- **Large constants.** The proven factor grows fast with the number of levels. Choose $m$ large so that there are only one or two levels.
- **Weights.** The solver must use the weights. A solver that treats a median of weight 1000 like a single point gives a poor result.
- **Buffer size.** The method needs $m > k$, and if $m$ is close to $k$ each level removes few points and there are many levels.
- **Duplicates.** Two medians at the same place both stay in the buffer. This is correct but wastes memory; they can be merged.

## Implementations

## History

Guha, Mishra, Motwani and O'Callaghan gave the divide and conquer method and its analysis at FOCS 2000, with the analysis of discrete and continuous medians that gives the factor 2 per level. The journal version of 2003 with Meyerson adds a randomized version in $\tilde{O}(nk)$ time and experiments with the LSEARCH solver of O'Callaghan et al. Later work by Charikar, O'Callaghan and Panigrahy, and by Har-Peled and Mazumdar with coresets, reduced the memory to polylogarithmic in $n$.

## References
