---
tag: RGY2FY
kind: algorithm
slug: indyk-p-stable-sketch
name: Indyk p-stable sketch
aliases:
- p-stable sketch
- Indyk sketch
- stable random projection sketch
area: online-and-streaming/streaming-sketches
level: advanced
summary: Estimates F_p for 0 < p <= 2 by projecting onto p-stable random variables.
solves: [frequency-moment-problem]
model: streaming-model
complexity:
  vars: {}
  time: {worst: O((1/ε²) log(1/δ))}
  space: {extra: O((1/ε²) log(1/δ))}
properties: {online: true, deterministic: false, comparison: false, recursive: false}
prereqs: [p-stable-distribution, frequency-vector, turnstile-model, linear-sketch, median-trick, hoeffding-inequality]
see_also: [ams-sketch, count-sketch, frequency-moment-lower-bounds, johnson-lindenstrauss-lemma, e2lsh, entropy-estimation-problem, join-size-estimation-problem, random-projection]
sources:
  - paper: doi:10.1145/1147954.1147955
    title: Piotr Indyk, Stable distributions, pseudorandom generators, embeddings, and data stream computation, Journal of the ACM 53(3), 2006 (FOCS 2000)
    locator: the median estimator for the l_1 and l_p norms, its analysis, and the use of Nisan's generator (section numbers to check)
  - paper: doi:10.1007/BF01305237
    title: Noam Nisan, Pseudorandom generators for space-bounded computation, Combinatorica 12(4), 1992
    locator: the generator used to make the random matrix storable
  - paper: "Daniel M. Kane, Jelani Nelson and David P. Woodruff, On the exact space complexity of sketching and streaming small norms, Proceedings of the 21st ACM-SIAM Symposium on Discrete Algorithms (SODA), 2010"
    locator: the optimal space bound for 0 < p < 2 with limited independence (to check)
  - paper: "Ping Li, Estimators and tail bounds for dimension reduction in l_alpha (0 < alpha <= 2) using stable random projections, Proceedings of the 19th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2008"
    locator: the geometric mean and harmonic mean estimators (to check)
  - paper: doi:10.1080/01621459.1976.10480344
    title: J. M. Chambers, C. L. Mallows and B. W. Stuck, A method for simulating stable random variables, Journal of the American Statistical Association 71(354), 1976
    locator: the sampler used for the matrix entries
---

The Indyk p-stable sketch estimates the $\ell_p$ norm $\|f\|_p = (\sum_i |f_i|^p)^{1/p}$ of a [frequency vector](/frequency-vector/), and so the moment $F_p = \|f\|_p^p$, for any $0 < p \le 2$, in the [turnstile model](/turnstile-model/). It is due to Piotr Indyk (FOCS 2000, journal 2006). The sketch keeps $k$ counters $y_j = \sum_i X_{j,i} f_i$, where the $X_{j,i}$ are independent [p-stable](/p-stable-distribution/) random variables. Each $y_j$ then has the law of $\|f\|_p$ times one p-stable variable, so the median of $|y_1|, \ldots, |y_k|$, divided by the median of that law, is a $(1 \pm \varepsilon)$ estimate of $\|f\|_p$ with probability $1 - \delta$ when $k = O(\varepsilon^{-2}\log(1/\delta))$. For $p = 2$ it is a Gaussian projection, close to the [AMS sketch](/ams-sketch/); for $p = 1$ it uses Cauchy variables and estimates the $\ell_1$ norm, which the AMS sketch cannot do.

## In plain words

Give every possible item a list of random numbers of a special kind, one number for each of several counters. When an item arrives, add its random numbers, times its count, to the counters.

The special kind is chosen so that each counter behaves like one random number of the same kind, scaled by the size of the whole frequency vector. So each counter is a noisy reading of that size. The noise is wild: some readings are far too large. An average would follow them, but the middle reading does not.

Sort the sizes of the readings, take the middle one, and divide by the known middle value of the special numbers. With enough counters, this is close to the true size with high probability. Deletions work too, because the counters are sums.

## The problem

The input is a stream of updates $(x, c)$ that add $c$ to $f_x$, for items $x \in [n]$ and integers $c$ of any sign. At the end, output $\hat F$ with $(1 - \varepsilon) F_p \le \hat F \le (1 + \varepsilon) F_p$ with probability at least $1 - \delta$, where $F_p = \sum_i |f_i|^p$. This is the case $0 < p \le 2$ of the [frequency moment problem](/frequency-moment-problem/). For $p > 2$ no sketch of this kind exists, since there is no p-stable law, and every algorithm needs polynomial space by the [frequency moment lower bounds](/frequency-moment-lower-bounds/).

## The algorithm

Fix $k$ and a $k \times n$ matrix $X$ of independent standard p-stable variables, with characteristic function $e^{-|t|^p}$. Let $\mu_p$ be the median of $|X_{j,i}|$: $\mu_1 = 1$ for the Cauchy law, $\mu_2 = \sqrt{2}\,\Phi^{-1}(3/4) \approx 0.95387$ for $N(0, 2)$, and a numerical value for other $p$. The matrix is not stored; column $x$ is made again from a short seed whenever item $x$ arrives.

```pseudo id=main
STABLE-UPDATE(y, x, c)                     ▷ add c to f_x
L1  for j ← 1 to k do
L2      y[j] ← y[j] + c · X[j][x]          ▷ X[j][x] made again from the seed

STABLE-ESTIMATE(y)
L3  N ← median(|y[1]|, …, |y[k]|) / μ_p    ▷ estimate of ‖f‖_p
L4  return N^p                             ▷ estimate of F_p

STABLE-MERGE(y, y′)                        ▷ both sketches use the same seed
L5  return y + y′
```

The median is the lower median, the $\lceil k/2 \rceil$-th smallest value. For $p = 1$, the proof gives $k = \lceil \ln(2/\delta) \cdot 25\pi^2 / (8\varepsilon^2) \rceil$ for a $(1 \pm \varepsilon)$ estimate of $\|f\|_1$; for $F_p$ with $p \le 2$, use $\varepsilon/3$ in place of $\varepsilon$.

## Example

Take $p = 1$, $n = 3$ items $0, 1, 2$, and $k = 5$. The matrix comes from a seeded Cauchy sampler, rounded to two places:

| row | $X_{j,0}$ | $X_{j,1}$ | $X_{j,2}$ |
|---|---|---|---|
| 1 | $-0.15$ | $0.19$ | $4.12$ |
| 2 | $-0.11$ | $0.02$ | $0.28$ |
| 3 | $-1.53$ | $0.04$ | $0.43$ |
| 4 | $1.31$ | $-3.28$ | $-0.71$ |
| 5 | $-3.42$ | $1.47$ | $0.70$ |

The stream is $(0, +2), (2, +2), (1, -1), (0, +1)$, with a deletion in the third update. At the end $f = (3, -1, 2)$ and $\|f\|_1 = 6$. By line L2, each counter is the row times $f$:

| row | $y_j$ | $\lvert y_j \rvert$ |
|---|---|---|
| 1 | $-0.45 - 0.19 + 8.24 = 7.60$ | $7.60$ |
| 2 | $-0.33 - 0.02 + 0.56 = 0.21$ | $0.21$ |
| 3 | $-4.59 - 0.04 + 0.86 = -3.77$ | $3.77$ |
| 4 | $3.93 + 3.28 - 1.42 = 5.79$ | $5.79$ |
| 5 | $-10.26 - 1.47 + 1.40 = -10.33$ | $10.33$ |

The sorted absolute values are $0.21, 3.77, 5.79, 7.60, 10.33$. The median is $5.79$, and $\mu_1 = 1$, so the estimate of $\|f\|_1 = F_1$ is $5.79$, about 3.5% below the true value 6. The single readings range from $0.21$ to $10.33$: each one alone is a poor estimate, and the large entries $4.12$ and $-3.42$ show the heavy tails of the Cauchy law. Five rows are far too few for a guarantee; the example only shows the steps.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). By induction on the updates, $y_j = \sum_i X_{j,i} f_i$. Since the rows are independent and the entries are p-stable, the $y_j$ are independent copies of $\|f\|_p X$. So $|y_j| / \|f\|_p$ falls below $(1 - \varepsilon)\mu_p$ with probability at most $\frac12 - \eta$ and above $(1 + \varepsilon)\mu_p$ with probability at most $\frac12 - \eta$, where $\eta$ is of order $\varepsilon$ because the density of $|X|$ is positive near $\mu_p$. The median is wrong only if at least half the rows land on one wrong side, and Hoeffding's inequality bounds each side by $e^{-2\eta^2 k}$. For the Cauchy law, $\Pr[|X| \le x] = \frac{2}{\pi}\arctan x$ gives $\eta \ge \frac{2\varepsilon}{5\pi}$, and $k \ge \frac{\ln(2/\delta)}{2\eta^2}$ gives failure probability at most $\delta$. Raising to the power $p \le 2$ at most triples the relative error.

## Complexity

- **Update:** $k = O(\varepsilon^{-2}\log(1/\delta))$ additions, plus the cost of making $k$ matrix entries from the seed.
- **Query:** $O(k)$ time with a linear-time median.
- **Space:** $k$ counters and the seed. Each counter needs $O(\log(nm/\varepsilon))$ bits of precision when the entries are rounded and truncated. With Nisan's generator, Indyk's version uses $O(\varepsilon^{-2}\log(1/\delta))$ counters plus a seed polylogarithmic in $n$. Kane, Nelson and Woodruff (2010) reached the optimal $O(\varepsilon^{-2}\log(nm))$ bits for $0 < p < 2$ with a different estimator.
- **Merge:** $O(k)$, for two sketches built from the same seed.

## Properties

- **Linear.** The sketch is a [linear sketch](/linear-sketch/): $y = Xf$. Sketches of two streams with the same seed add, and the difference of two sketches estimates $\|f - g\|_p$, a distance between two streams.
- **Turnstile.** Negative updates and negative final counts are allowed; the guarantee depends only on the final $f$.
- **Randomized, with an oblivious adversary.** The stream must not depend on the matrix. An adaptive adversary that sees the estimates can make linear sketches fail.
- **Two-sided error.** The estimate can be above or below $\|f\|_p$.
- **Not an average.** For $p < 2$, $|y_j|$ has infinite variance, and for $p \le 1$ infinite mean, so the method of the [median trick](/median-trick/) with group averages does not apply; the median works on single rows.

## Variants and improvements

- **Other estimators.** Li (2008) studied the geometric mean $\prod_j |y_j|^{1/k}$ and the harmonic mean, rescaled by known constants, which have smaller error for the same $k$ and simple tail bounds. A fractional power estimator averages $|y_j|^{\lambda}$ for $\lambda < p/2$, where the variance is finite.
- **Optimal space.** Kane, Nelson and Woodruff (2010) used limited independence and an estimator based on the empirical characteristic function, the mean of $\cos(t y_j)$, which reaches $O(\varepsilon^{-2}\log(nm))$ bits for $0 < p < 2$, matching a lower bound.
- **$p = 2$.** Gaussian entries give the Johnson-Lindenstrauss projection, and $\frac{1}{k}\sum_j y_j^2$, an average, works because the variance is finite. Random signs, as in the [AMS sketch](/ams-sketch/), give the same guarantee with 4-wise independent bits and are simpler.
- **Entropy and moments near 1.** Estimates of $F_p$ for $p$ close to 1 give estimates of the [empirical entropy](/entropy-estimation-problem/) through the derivative of $F_p$ at $p = 1$; Harvey, Nelson and Onak (2008) used stable sketches this way.
- **Embeddings.** The same projection embeds $\ell_p$ into a space where distances are read off by medians, and Datar, Immorlica, Indyk and Mirrokni used p-stable projections for [locality-sensitive hashing](/e2lsh/) in $\ell_p$.

## When to use it

Use it for the $\ell_1$ norm or $F_p$ with $p < 2$ in a turnstile stream: the total volume $\sum_i |f_i|$ when counts can be negative, or the $\ell_1$ distance between two streams through the difference of their sketches. For $p = 2$, the [AMS sketch](/ams-sketch/) is simpler and needs only random signs. For insertion-only streams and $p = 1$, a single counter of the stream length gives $F_1$ exactly. For $p > 2$, use the algorithms built on [count sketches](/count-sketch/), with polynomial space.

## Pitfalls

- **Averaging the rows.** For $p = 1$ the mean of $|y_j|$ is infinite, and a sample mean is ruled by its largest value. Use the median, or one of the estimators made for heavy tails.
- **The wrong scale constant.** The median of $|X|$ depends on the parametrization. With characteristic function $e^{-|t|^p}$, $\mu_1 = 1$ and $\mu_2 \approx 0.954$; for $N(0, 1)$ entries, the constant is $0.6745$ instead.
- **Storing the matrix.** A stored $k \times n$ matrix defeats the purpose. Make the entries again from a seed, and use the same seed for sketches that must be merged.
- **Pseudorandom entries.** The proof assumes independent entries. Seeded generators work in practice, but the proven guarantee needs Nisan's generator or the limited independence analysis of Kane, Nelson and Woodruff.
- **Numerical range.** Stable samplers can return huge values, from $\cos\Theta$ near 0. Clip or round the entries with care, since one huge entry for a frequent item swamps a row; the median tolerates a few such rows, not many.
- **Small $k$.** The constant $\frac{25\pi^2}{8}$ is large; with $k = 5$, as in the example, the estimate is a rough guess.

## Implementations

## History

Indyk introduced the sketch at FOCS 2000, in a paper that also gave embeddings of $\ell_p$ and pseudorandom matrices for streaming through Nisan's generator; the journal version appeared in 2006. It answered the question of estimating $\ell_1$ distances between streams, studied by Feigenbaum, Kannan, Strauss and Viswanathan (1999) for $p = 1$ with a different method. Gaussian projections for $p = 2$ go back to the Johnson-Lindenstrauss lemma (1984), and the sampler for stable variables to Chambers, Mallows and Stuck (1976). Li (2008) gave estimators with better constants, and Kane, Nelson and Woodruff (2010) settled the space complexity for $0 < p < 2$.

## References
