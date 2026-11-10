---
tag: 4BWT77
kind: data-structure
slug: count-min-sketch
name: Count-min sketch
aliases:
- CM sketch
- Cormode-Muthukrishnan sketch
area: online-and-streaming/streaming-sketches
level: core
summary: Counter arrays with min-of-rows queries that overestimate frequencies within epsilon times the L1 norm.
model: streaming-model
complexity:
  vars: {}
  time: {worst: O(log(1/δ))}
  space: {extra: O((1/ε) log(1/δ))}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [frequency-vector, turnstile-model, universal-hash-family, markov-inequality, epsilon-delta-guarantee]
see_also: [count-min-error-bound, frequency-estimation, count-sketch, linear-sketch, dyadic-intervals, space-saving, spectral-bloom-filter, join-size-estimation-problem]
sources:
  - paper: doi:10.1016/j.jalgor.2003.12.001
    title: Graham Cormode and S. Muthukrishnan, An improved data stream summary, the count-min sketch and its applications, Journal of Algorithms 55(1), 2005
    locator: pages 58 to 75, Section 4.1 (point queries with width e/ε and depth ln(1/δ), and the median for the general turnstile case), and the later parts on inner products, range queries and heavy hitters
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 3, Summaries for multisets (the Count-Min sketch, conservative update, and the comparison with the Count Sketch)
  - paper: doi:10.1145/964725.633056
    title: Cristian Estan and George Varghese, New directions in traffic measurement and accounting, Proceedings of ACM SIGCOMM 2002
    locator: pages 323 to 336, multistage filters and the conservative update
  - url: https://web.stanford.edu/class/cs168/l/l2.pdf
    title: Tim Roughgarden and Gregory Valiant, CS168 The Modern Algorithmic Toolbox, Lecture 2, Approximate heavy hitters and the count-min sketch, Stanford University
    locator: Section 3, the count-min sketch and its error analysis
---

The count-min sketch is a small array of counters that estimates the entries of the [frequency vector](/frequency-vector/) of a stream. It has $d$ rows of $w$ counters and one hash function for each row. An update adds to one counter in each row, and a query returns the smallest of the $d$ counters of the item. When all counts are non-negative, the estimate is never too small, and with $w = \lceil e/\varepsilon \rceil$ and $d = \lceil \ln(1/\delta) \rceil$ it is too large by more than $\varepsilon \|f\|_1$ with probability at most $\delta$. It is a [linear sketch](/linear-sketch/), so it handles deletions and two sketches can be added. This page is the streaming view of the sketch; the bound is also stated as the theorem [count-min sketch error bound](/count-min-error-bound/), and the problem it solves is [frequency estimation](/frequency-estimation/).

## In plain words

Take a few rows of boxes, each box with a tally. Each row has its own rule that sends every item to one box of that row. When an item arrives, add one to its box in each row. Other items share these boxes, so each box holds the count of the item plus the counts of some strangers.

To estimate the count of an item, look at its box in every row and take the smallest tally. The strangers can only add to a tally, so no tally is too small. A box with many strangers is rare, and it is very rare that all rows give the item a crowded box at once.

## The abstract type

The sketch stores an approximation of a vector $f \in \mathbb{Z}^n$ under the operations:

- **update$(x, c)$:** add $c$ to $f_x$. In the cash register model $c > 0$; in the [turnstile model](/turnstile-model/) $c$ can be negative.
- **query$(x)$:** return an estimate $\hat f_x$ of $f_x$.
- **merge:** given sketches of $f$ and $g$ with the same hash functions, return the sketch of $f + g$.

The guarantee is for the strict turnstile model, where every $f_x \ge 0$ at query time: $f_x \le \hat f_x$ always, and $\hat f_x \le f_x + \varepsilon \|f\|_1$ with probability at least $1 - \delta$ for each fixed query, in the sense of the [epsilon-delta guarantee](/epsilon-delta-guarantee/). Here $\|f\|_1 = \sum_y |f_y|$, which is the total count when all counts are non-negative.

## Representation

- A table $C$ of $d$ rows and $w$ columns of counters, all 0 at the start.
- Hash functions $h_1, \ldots, h_d : [n] \to \{0, \ldots, w - 1\}$, drawn independently from a [universal hash family](/universal-hash-family/), so that $\Pr[h_j(x) = h_j(y)] \le 1/w$ for $x \ne y$. A standard choice is $h_j(x) = ((a_j x + b_j) \bmod P) \bmod w$ with a prime $P > n$, $a_j \in \{1, \ldots, P - 1\}$ and $b_j \in \{0, \ldots, P - 1\}$, as in [universal hashing](/universal-hashing/). Each function is two numbers.

For error $\varepsilon$ and failure probability $\delta$, take $w = \lceil e/\varepsilon \rceil$ and $d = \lceil \ln(1/\delta) \rceil$. For example, $\varepsilon = 0.01$ and $\delta = 0.01$ give $272 \times 5$ counters.

## Operations

```pseudo id=main
CM-UPDATE(C, x, c)                       ▷ add c to f_x
L1  for j ← 1 to d do
L2      C[j][h_j(x)] ← C[j][h_j(x)] + c

CM-QUERY(C, x)
L3  return min over j of C[j][h_j(x)]

CM-CONSERVATIVE-UPDATE(C, x, c)          ▷ only for c > 0
L4  v ← CM-QUERY(C, x) + c
L5  for j ← 1 to d do
L6      C[j][h_j(x)] ← max(C[j][h_j(x)], v)

CM-MERGE(C, C′)                          ▷ same w, d and hash functions
L7  return the table C + C′, counter by counter
```

**Conservative update.** In the cash register model, a counter needs to be at least the count of each item that maps to it. Lines L4 to L6 raise each counter of $x$ only to the new estimate of $x$, not by the full $c$. Each counter then stays at most the counter of CM-UPDATE, so the error bound still holds and the estimates are often much better. This rule is from the multistage filters of Estan and Varghese (2002). It is not linear: it does not allow deletions, and a sketch built this way cannot be subtracted.

**Range queries.** For a range $[\ell, r]$ of items, keep one sketch for each level of [dyadic intervals](/dyadic-intervals/): level $k$ counts the item $\lfloor x / 2^k \rfloor$. A range splits into at most $2 \log_2 n$ dyadic intervals, and the answer is the sum of their estimates. It is never too small, and it is too large by more than $2 \varepsilon \|f\|_1 \log_2 n$ with probability at most $2\delta \log_2 n$.

**Heavy hitters.** In the cash register model, keep a heap of the items whose estimate is at least $\phi \|f\|_1$, and check each item when it arrives. In the turnstile model, search down the dyadic levels and open only the intervals whose estimate is at least $\phi \|f\|_1$. This solves the [frequent items problem](/frequent-items-problem/) with deletions.

## Example

Take $w = 4$, $d = 2$, the prime $P = 31$, $h_1(x) = x \bmod 4$ and $h_2(x) = (7x \bmod 31) \bmod 4$. The updates are $(1, 3)$, $(2, 2)$, $(5, 1)$ and $(6, 4)$, so $\|f\|_1 = 10$.

| $x$ | $c$ | $h_1(x)$ | $h_2(x)$ |
|---|---|---|---|
| 1 | 3 | 1 | $7 \bmod 4 = 3$ |
| 2 | 2 | 2 | $14 \bmod 4 = 2$ |
| 5 | 1 | 1 | $(35 \bmod 31) \bmod 4 = 0$ |
| 6 | 4 | 2 | $(42 \bmod 31) \bmod 4 = 3$ |

The table is row 1: $[0, 4, 6, 0]$ and row 2: $[1, 0, 2, 7]$.

| $x$ | $f_x$ | $C[1][h_1(x)]$ | $C[2][h_2(x)]$ | $\hat f_x$ |
|---|---|---|---|---|
| 1 | 3 | 4 | 7 | 4 |
| 2 | 2 | 6 | 2 | 2 |
| 5 | 1 | 4 | 1 | 1 |
| 6 | 4 | 6 | 7 | 6 |
| 9 | 0 | 4 | 0 | 0 |

Row 1 puts 1 with 5 and 2 with 6. Row 2 separates 2 and 5 from the others, so the minimum is exact for them and for the absent item 9. Item 6 collides in both rows, so its estimate is too large by 2. Each estimate is at least the true count.

## Correctness

**Theorem.** In the strict turnstile model, for each item $x$, $f_x \le \hat f_x$, and with $w = \lceil e/\varepsilon \rceil$ and $d = \lceil \ln(1/\delta) \rceil$,
$$ \Pr\left[\hat f_x > f_x + \varepsilon \|f\|_1\right] \le \delta . $$

Row $j$ holds $C[j][h_j(x)] = f_x + X_j$, where $X_j = \sum_{y \ne x,\, h_j(y) = h_j(x)} f_y \ge 0$ is the count of the strangers in the box of $x$. By universality, $\mathbb{E}[X_j] \le \|f\|_1 / w \le (\varepsilon / e) \|f\|_1$. By [Markov's inequality](/markov-inequality/), $\Pr[X_j > \varepsilon \|f\|_1] \le 1/e$. The rows use independent hash functions, so all $d$ rows are bad with probability at most $e^{-d} \le \delta$, and the minimum is bad only then. The proof needs only universal hash functions, not stronger independence.

The full proof, with the conservative update, merges and range queries, is below. The same bound in theorem form, with its tightness, is on the [count-min sketch error bound](/count-min-error-bound/) page.

## Complexity

- **Space.** $wd = \lceil e/\varepsilon \rceil \lceil \ln(1/\delta) \rceil$ counters and $2d$ hash parameters, that is $O((1/\varepsilon) \log(1/\delta))$ words.
- **Update and query.** $d = O(\log(1/\delta))$ hash evaluations and counter operations each.
- **Merge.** $O(wd)$ additions.
- **Range query.** $O(\log n \log(1/\delta))$ time with $O(\log n)$ sketches.

## Variants

- **The general turnstile model.** If some counts can be negative, the minimum is no longer an upper bound. Cormode and Muthukrishnan use the median of the $d$ row values instead, with error at most $3\varepsilon \|f\|_1$ with probability $1 - \delta^{1/4}$.
- **Inner products.** For sketches of $f$ and $g$ with the same hash functions, $\min_j \sum_b C_f[j][b] \, C_g[j][b]$ estimates $\sum_x f_x g_x$ with error at most $\varepsilon \|f\|_1 \|g\|_1$, with probability $1 - \delta$, when all counts are non-negative. This estimates [join sizes](/join-size-estimation-problem/). The AMS estimator gives an error in terms of second norms instead.
- **Count-mean-min.** Subtract an estimate of the noise of each row, $(\|f\|_1 - C[j][h_j(x)])/(w - 1)$, and take the median of the rows. This helps on data with many small counts.
- **The count sketch.** The [count sketch](/count-sketch/) adds a random sign to each update and takes the median of the rows. Its error is $\varepsilon \|f\|_2$ with $O((1/\varepsilon^2) \log(1/\delta))$ counters and can be in both directions.

**Count-min against the count sketch.** With $k$ counters in each row, the count-min error is about $\|f\|_1 / k$ and the count-sketch error is about $\|f\|_2 / \sqrt{k}$. Since $\|f\|_2 \le \|f\|_1 \le \sqrt{n} \, \|f\|_2$, neither is always better. On very skewed data $\|f\|_2$ is close to the largest count, and the count sketch wins for small errors. On flat data $\|f\|_2$ is about $\|f\|_1/\sqrt{n}$, and both are poor for single items. The count-min sketch is one-sided and smaller for the same $\varepsilon$ when the guarantee in $\|f\|_1$ is enough.

## When to use it

Use the count-min sketch for frequency estimates with deletions, for summaries that must be added across machines or time windows, and for heavy hitters, range sums and quantiles over a turnstile stream. On insertion-only streams, a counter-based summary such as [Space-Saving](/space-saving/) gives a deterministic bound of the same order with fewer counters; prefer the count-min sketch there only when you need linearity or the fixed memory layout. Use the [count sketch](/count-sketch/) when you need an error in terms of $\|f\|_2$.

## Pitfalls

- **Negative counts.** With $f_x < 0$ allowed, the minimum can be far below the true count. Use the median, or keep the data in the strict turnstile model.
- **Correlated rows.** The bound $e^{-d}$ needs independent hash functions for the rows. Rows built from one hash value with different moduli are not independent.
- **A failure for each query.** The probability $\delta$ is for one fixed query. For $q$ queries at once, the union bound gives $q\delta$, so take $d = \lceil \ln(q/\delta) \rceil$.
- **Adaptive queries.** The bound assumes the stream and the queries do not depend on the hash functions. An adversary who sees the estimates can find colliding items.
- **Conservative update with deletions.** The conservative rule needs $c > 0$. Subtracting from such a sketch can make estimates too small.
- **Merging sketches with different seeds.** Two sketches add only if they share $w$, $d$ and the hash functions.

## Implementations

## History

Graham Cormode and S. Muthukrishnan presented the count-min sketch at LATIN 2004, and the journal version appeared in the Journal of Algorithms in 2005. It needs $O(1/\varepsilon)$ counters in each row, against $O(1/\varepsilon^2)$ for earlier sketches with an error in the same terms, and it gave one structure for point, range and inner product queries, heavy hitters and quantiles. Similar structures came before it: the multistage filters of Estan and Varghese (2002), which also introduced the conservative update, and the spectral Bloom filters of Cohen and Matias (2003). Its simple analysis and its linearity made it one of the most used sketches in networking, databases and machine learning.

## References
