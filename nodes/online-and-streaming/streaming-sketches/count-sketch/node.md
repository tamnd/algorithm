---
tag: 2S6HW2
kind: data-structure
slug: count-sketch
name: Count sketch
aliases:
- CCFC sketch
- Charikar-Chen-Farach-Colton sketch
- CountSketch
area: online-and-streaming/streaming-sketches
level: core
summary: Signed counter arrays giving unbiased frequency estimates with error in the L2 norm.
model: streaming-model
complexity:
  vars: {}
  time: {worst: O(log(1/δ))}
  space: {extra: O((1/ε²) log(1/δ))}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [frequency-vector, turnstile-model, universal-hash-family, pairwise-independence, chebyshev-inequality, median-trick]
see_also: [count-min-sketch, ams-sketch, frequency-estimation, frequent-items-problem, linear-sketch, frequency-moment-problem, join-size-estimation-problem, johnson-lindenstrauss-lemma]
sources:
  - paper: doi:10.1016/s0304-3975(03)00400-6
    title: Moses Charikar, Kevin Chen and Martin Farach-Colton, Finding frequent items in data streams, Theoretical Computer Science 312(1), 2004 (ICALP 2002)
    locator: the sections on the count sketch, its variance bound in terms of the tail of the frequency vector, and the top-k algorithm (to check)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 3, Summaries for multisets (the Count Sketch and its comparison with the Count-Min sketch)
  - paper: doi:10.1016/j.jalgor.2003.12.001
    title: Graham Cormode and S. Muthukrishnan, An improved data stream summary, the count-min sketch and its applications, Journal of Algorithms 55(1), 2005
    locator: pages 58 to 75, the comparison of the count-min sketch with the count sketch of Charikar, Chen and Farach-Colton
  - url: https://web.stanford.edu/class/cs168/l/l2.pdf
    title: Tim Roughgarden and Gregory Valiant, CS168 The Modern Algorithmic Toolbox, Lecture 2, Approximate heavy hitters and the count-min sketch, Stanford University
    locator: the remarks on the count sketch as the variant with random signs
---

The count sketch estimates the entries of the [frequency vector](/frequency-vector/) of a stream, with an error in terms of the second norm $\|f\|_2$. It is due to Charikar, Chen and Farach-Colton (2002). Like the [count-min sketch](/count-min-sketch/), it has $d$ rows of $w$ counters and one bucket hash for each row. Unlike it, each row also has a random sign $\pm 1$ for each item, an update adds the signed count, and a query takes the median of the signed row values. Each row is an unbiased estimate with variance at most $\|f\|_2^2 / w$. With $w = \lceil 3/\varepsilon^2 \rceil$ and $d = O(\log(1/\delta))$, the estimate is within $\varepsilon \|f\|_2$ of the true count with probability at least $1 - \delta$, in the general [turnstile model](/turnstile-model/), with negative counts allowed. It is a [linear sketch](/linear-sketch/).

## In plain words

Use rows of boxes as in the count-min sketch, but give each item a random sign in each row, plus or minus. When an item arrives, add its count to its box with its sign. To read an item, look at its box in a row and multiply by its sign.

The other items in the box have random signs, so on average they cancel. The reading is right on average, but it can be too high or too low. Each row gives one reading. The middle reading of all rows is far from the truth only if half the rows are bad, and that is very rare.

The noise comes from the other counts, and a few large counts matter much more than many small ones. When the data has a few large items, their partners in a box are small, and the error is small.

## The abstract type

The sketch stores an approximation of a vector $f \in \mathbb{Z}^n$ under three operations:

- **update$(x, c)$:** add $c$ to $f_x$, for any integer $c$, positive or negative.
- **query$(x)$:** return an estimate $\hat f_x$ of $f_x$.
- **merge:** given sketches of $f$ and $g$ with the same hash functions, return the sketch of $f + g$.

The guarantee is two-sided. For each fixed query, $|\hat f_x - f_x| \le \varepsilon \|f\|_2$ with probability at least $1 - \delta$, where $\|f\|_2 = (\sum_y f_y^2)^{1/2} = \sqrt{F_2}$. A stronger form bounds the error by the norm of the tail of $f$, the vector without its largest entries.

## Representation

- A table $C$ of $d$ rows and $w$ columns of counters, all 0 at the start.
- For each row $j$, a bucket hash $h_j : [n] \to \{0, \ldots, w - 1\}$ from a [universal hash family](/universal-hash-family/), with $\Pr[h_j(x) = h_j(y)] \le 1/w$ for $x \ne y$.
- For each row $j$, a sign hash $s_j : [n] \to \{-1, +1\}$ from a pairwise independent family: for $x \ne y$, the pair $(s_j(x), s_j(y))$ is uniform on $\{-1, +1\}^2$, as in [pairwise independence](/pairwise-independence/).
- All $2d$ hash functions are drawn independently.

A pairwise independent sign family: draw a random bit vector $a$ and a random bit $b$, and set $s(x) = (-1)^{\langle a, x \rangle \oplus b}$, where $\langle a, x \rangle$ is the parity of the bits that $a$ and $x$ share. For $x \ne y$, the parity $\langle a, x \oplus y \rangle$ is a fair bit, and $b$ makes each sign a fair bit, so the two signs are independent.

For error $\varepsilon$ and failure probability $\delta$, take $w = \lceil 3/\varepsilon^2 \rceil$ and $d = \lceil 18 \ln(1/\delta) \rceil$. The constant 18 comes from the Hoeffding bound in the proof. It is loose, and in practice $d$ between 5 and 10 is common.

## Operations

```pseudo id=main
CS-UPDATE(C, x, c)                       ▷ add c to f_x, c of any sign
L1  for j ← 1 to d do
L2      C[j][h_j(x)] ← C[j][h_j(x)] + s_j(x) · c

CS-QUERY(C, x)
L3  for j ← 1 to d do e_j ← s_j(x) · C[j][h_j(x)]
L4  return the median of e_1, …, e_d

CS-MERGE(C, C′)                          ▷ same w, d and hash functions
L5  return the table C + C′, counter by counter
```

For an even $d$, the code returns the lower median, the value at position $\lceil d/2 \rceil$ in sorted order. The proof holds for it as well.

**Top-$k$ items.** Charikar, Chen and Farach-Colton keep a heap of the $k$ items with the largest estimates next to the sketch. When an item arrives, the algorithm updates the sketch, estimates the item, and puts it in the heap if its estimate is larger than the smallest one there. This finds the approximate top $k$ items of an insertion-only stream in one pass. In the turnstile model, heavy items are found with a search over [dyadic intervals](/dyadic-intervals/), as with the count-min sketch.

## Example

Take $w = 3$, $d = 3$ and $P = 31$. The bucket hashes are $h_1(x) = x \bmod 3$, $h_2(x) = (2x \bmod 31) \bmod 3$ and $h_3(x) = (13 x \bmod 31) \bmod 3$. The signs are $s_1(x) = (-1)^{x_0}$, $s_2(x) = (-1)^{x_1}$ and $s_3(x) = -(-1)^{x_0}$, where $x_0$ and $x_1$ are the two lowest bits of $x$. The counts are $f_1 = 5$, $f_2 = 3$, $f_3 = 1$ and $f_4 = 1$, so $\|f\|_2 = \sqrt{36} = 6$.

| $x$ | $f_x$ | $h_1, h_2, h_3$ | $s_1, s_2, s_3$ |
|---|---|---|---|
| 1 | 5 | 1, 2, 1 | $-, +, +$ |
| 2 | 3 | 2, 1, 2 | $+, -, -$ |
| 3 | 1 | 0, 0, 2 | $-, -, +$ |
| 4 | 1 | 1, 2, 0 | $+, +, -$ |
| 7 | 0 | 1, 2, 2 | $-, -, +$ |

The table is row 1: $[-1, -4, 3]$, row 2: $[-1, -3, 6]$ and row 3: $[-1, 5, -2]$. For example, box 1 of row 1 holds $-5$ from item 1 and $+1$ from item 4.

| $x$ | $f_x$ | $e_1, e_2, e_3$ | median |
|---|---|---|---|
| 1 | 5 | 4, 6, 5 | 5 |
| 2 | 3 | 3, 3, 2 | 3 |
| 3 | 1 | 1, 1, $-2$ | 1 |
| 4 | 1 | $-4$, 6, 1 | 1 |
| 7 | 0 | 4, $-6$, $-2$ | $-2$ |

Item 1 shares a box with item 4 in rows 1 and 2. Row 1 gives $4$, too low, because item 4 has the opposite sign there. Row 2 gives $6$, too high. Row 3 is clean, and the median is exact. The absent item 7 gets $-2$: the count sketch can return values below the true count, and even negative values. Each error here is at most 2, against $\|f\|_2 = 6$.

## Correctness

Fix an item $x$ and a row $j$. The row estimate is
$$ e_j = s_j(x) C[j][h_j(x)] = f_x + \sum_{y \ne x} f_y \, s_j(x) s_j(y) \, 1[h_j(y) = h_j(x)] , $$
because $s_j(x)^2 = 1$.

**Lemma (one row).** $\mathbb{E}[e_j] = f_x$ and $\mathrm{Var}[e_j] \le (\|f\|_2^2 - f_x^2)/w$.

For $y \ne x$, $s_j(x) s_j(y)$ has mean 0 by pairwise independence, and it is independent of $h_j$. So each error term has mean 0. For the variance, the cross terms for $y \ne z$ (both not $x$) contain $s_j(y) s_j(z)$, with mean 0. The square terms are $f_y^2 \Pr[h_j(y) = h_j(x)] \le f_y^2 / w$.

**Theorem.** With $w = \lceil 3/\varepsilon^2 \rceil$ and $d = \lceil 18 \ln(1/\delta) \rceil$, $\Pr[|\hat f_x - f_x| > \varepsilon \|f\|_2] \le \delta$, for every $f \in \mathbb{Z}^n$.

By [Chebyshev's inequality](/chebyshev-inequality/), one row is bad with probability at most $\|f\|_2^2 / (w \varepsilon^2 \|f\|_2^2) \le 1/3$. The median is bad only if at least half of the $d$ independent rows are bad. By the Hoeffding bound, this has probability at most $e^{-2d (1/2 - 1/3)^2} = e^{-d/18} \le \delta$. This is the [median trick](/median-trick/).

**Theorem (tail bound).** Let $f_{\mathrm{res}(k)}$ be $f$ with its $k$ largest entries in absolute value set to 0. If $k \le w/6$, then one row has $|e_j - f_x| \le \sqrt{6/w} \, \|f_{\mathrm{res}(k)}\|_2$ with probability at least $2/3$, and the median of $d = \lceil 18 \ln(1/\delta) \rceil$ rows has it with probability at least $1 - \delta$.

The idea is that the $k$ largest items land in the box of $x$ with probability at most $k/w \le 1/6$, and the rest of the noise has variance at most $\|f_{\mathrm{res}(k)}\|_2^2 / w$. On skewed data the tail norm is much smaller than $\|f\|_2$. The full proofs are below.

## Complexity

- **Space.** $wd$ counters and $4d$ hash parameters, that is $O((1/\varepsilon^2) \log(1/\delta))$ words. Each counter needs $O(\log(m n))$ bits for a stream of $m$ updates of bounded size.
- **Update.** $d$ bucket hashes and $d$ signs, $O(\log(1/\delta))$ time.
- **Query.** $d$ row values and a median: $O(d)$ time with linear-time selection, or $O(d \log d)$ by sorting.
- **Merge.** $O(wd)$ additions.

## Variants

- **Count-min and count sketch.** The table compares the two sketches with $w$ counters in each row and $d = O(\log(1/\delta))$ rows.

| | count-min sketch | count sketch |
|---|---|---|
| hash functions | one universal hash per row | one universal hash and one pairwise sign per row |
| row value | $C[j][h_j(x)]$ | $s_j(x) C[j][h_j(x)]$ |
| combine rows | minimum | median |
| error for $w$ columns | $\|f\|_1 \cdot e/w$, one-sided | $\|f\|_2 \cdot \sqrt{3/w}$, two-sided |
| width for error $\varepsilon \|f\|_1$ or $\varepsilon \|f\|_2$ | $\lceil e/\varepsilon \rceil$ | $\lceil 3/\varepsilon^2 \rceil$ |
| stream model | strict turnstile (minimum) | general turnstile |

Since $\|f\|_2 \le \|f\|_1$, an error of $\varepsilon \|f\|_2$ is never worse than $\varepsilon \|f\|_1$, but it costs $1/\varepsilon^2$ counters instead of $1/\varepsilon$. On skewed data, $\|f\|_2$ is much smaller than $\|f\|_1$, and the count sketch wins for the same space. On flat data the count-min sketch is smaller.

- **Second moment.** Each row gives $\sum_b C[j][b]^2$, an unbiased estimate of $F_2 = \|f\|_2^2$ when the signs are pairwise independent. With 4-wise independent signs, its variance is at most $2F_2^2$, as in the [AMS sketch](/ams-sketch/). This is the fast AMS sketch of Thorup and Zhang (2004): one counter update for each row instead of $w$.
- **Inner products.** For sketches of $f$ and $g$ with the same hash functions, $\sum_b C_f[j][b] \, C_g[j][b]$ is an unbiased estimate of $\langle f, g \rangle$, used for [join size estimation](/join-size-estimation-problem/).
- **Feature hashing.** One row of the count sketch, used to map a large sparse vector to $w$ dimensions, is the signed hashing trick of machine learning. The signs make inner products unbiased. It is a sparse random projection, in the spirit of the [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/).
- **Sparse recovery.** Keeping the $k$ largest estimates of a count sketch gives a $k$-sparse vector close to $f$ in the second norm. This is the base of many sparse recovery schemes.

## When to use it

Use the count sketch when the stream has deletions or negative weights, or when you need an error in terms of $\|f\|_2$ or of the tail of $f$, as for finding the top $k$ items of skewed data. Use it also when you need unbiased estimates, for example to sum estimates over many items. Use the [count-min sketch](/count-min-sketch/) when all counts are non-negative, a one-sided error in $\|f\|_1$ is enough, and space is tight. For an insertion-only stream with a deterministic guarantee, use [Space-Saving](/space-saving/) or the [Misra-Gries summary](/misra-gries-summary/).

## Pitfalls

- **Signs and buckets from one hash value.** The proof needs the sign independent of the bucket. Taking both from the bits of one hash value is fine only if the hash function is independent enough across those bits.
- **The mean instead of the median.** The mean of the rows has the same expectation, but it does not give the $\log(1/\delta)$ dependence; one bad row can spoil it.
- **Reading the estimate as a lower or upper bound.** The error can go either way, and absent items can get negative estimates. Clamp at 0 when counts are known to be non-negative.
- **Comparing widths.** For the same $\varepsilon$, the count sketch needs about $\varepsilon^{-2}$ columns, not $\varepsilon^{-1}$. Compare the two sketches at the same memory, not at the same $\varepsilon$.
- **Adaptive queries.** As with every randomized sketch, the bound is for a stream and queries chosen without knowledge of the hash functions.

## Implementations

## History

Moses Charikar, Kevin Chen and Martin Farach-Colton introduced the count sketch at ICALP 2002 in *Finding frequent items in data streams*, with a journal version in Theoretical Computer Science in 2004. Their goal was the top $k$ queries of a search engine log in one pass. The random signs come from the tug of war of Alon, Matias and Szegedy (1996), and the hashing of items to buckets lets each update touch one counter per row. Cormode and Muthukrishnan (2004) showed that dropping the signs and taking the minimum gives the [count-min sketch](/count-min-sketch/), with a one-sided error in $\|f\|_1$. Thorup and Zhang (2004) used the same structure with 4-wise independent signs to estimate $F_2$ quickly. The count sketch is also the basis of many sparse recovery schemes and of the hashing trick for features.

## References
