---
tag: 2J4Z4N
kind: theorem
slug: count-min-error-bound
name: Count-min sketch error bound
area: data-structures/probabilistic-structures
level: advanced
summary: With width e/eps and depth ln(1/delta), count-min overestimates by at most eps times the total weight with probability 1 - delta.
prereqs: [frequency-estimation, markov-inequality, universal-hash-family]
see_also: [count-min-sketch, count-sketch, spectral-bloom-filter, misra-gries-summary, linear-sketch, turnstile-model]
sources:
  - paper: doi:10.1016/j.jalgor.2003.12.001
    title: Graham Cormode and S. Muthukrishnan, An improved data stream summary, the count-min sketch and its applications, Journal of Algorithms 55(1), 2005
    locator: pages 58 to 75, Section 4.1 (the point query bound with width e over eps and depth ln of 1 over delta, and the median estimator for the general turnstile case)
  - paper: doi:10.1016/s0304-3975(03)00400-6
    title: Moses Charikar, Kevin Chen and Martin Farach-Colton, Finding frequent items in data streams, Theoretical Computer Science 312(1), 2004
    locator: pages 3 to 15 (the count sketch, with an error in terms of the second norm)
  - paper: doi:10.1145/964725.633056
    title: Cristian Estan and George Varghese, New directions in traffic measurement and accounting, SIGCOMM 2002
    locator: pages 323 to 336 (multistage filters and conservative update)
---

The count-min sketch keeps $d$ rows of $w$ counters, adds each update to one counter in each row, and estimates the count of an item by the smallest of its $d$ counters. In the strict turnstile model the estimate is never too small, and with $w = \lceil e/\varepsilon \rceil$ and $d = \lceil \ln(1/\delta) \rceil$ it is too large by more than $\varepsilon$ times the total weight with probability at most $\delta$. The proof needs only pairwise independent hash functions and [Markov's inequality](/markov-inequality/). This bound, by Cormode and Muthukrishnan (2005), is why the sketch solves the [frequency estimation problem](/frequency-estimation/) in $O(\varepsilon^{-1} \log(1/\delta))$ counters.

## Statement

Let $f \in \mathbb{Z}^U$ be the frequency vector of a stream in the strict turnstile model, so $f_y \ge 0$ for each $y$, and let $N = \|f\|_1 = \sum_y f_y$. Let $h_1, \ldots, h_d : U \to \{0, \ldots, w-1\}$ be drawn independently from a [universal hash family](/universal-hash-family/), so that $\Pr[h_j(x) = h_j(y)] \le 1/w$ for each $x \ne y$. The sketch holds the counters
$$ C[j][b] = \sum_{y : h_j(y) = b} f_y, $$
and the estimate of $f_x$ is $\hat f_x = \min_{1 \le j \le d} C[j][h_j(x)]$.

**Theorem.** For each item $x$:
1. $\hat f_x \ge f_x$.
2. If $w \ge e/\varepsilon$ and $d \ge \ln(1/\delta)$, then $\Pr\big[\hat f_x > f_x + \varepsilon (N - f_x)\big] \le \delta$, and so $\Pr[\hat f_x > f_x + \varepsilon N] \le \delta$.

**Theorem (general turnstile).** If $f$ may have negative entries, let $\tilde f_x$ be the median of the $d$ values $C[j][h_j(x)]$. If $w \ge e/\varepsilon$, then $\Pr\big[|\tilde f_x - f_x| > 3\varepsilon \|f\|_1\big] \le 2^{-d/2}$.

## In plain words

Each row of the sketch is a short list of counters. Each item is sent to one counter in each row, and adds its count there. So the counter of an item also holds the counts of other items that landed in the same place. It can only be too large, never too small.

In one row, the extra amount is small on average: about the total count divided by the number of counters. It is rarely much larger than its average. With enough counters per row, one row is too far off only about one time in three.

The rows are independent. The estimate takes the smallest counter, so it is too far off only if every row is. Each new row makes this about three times less likely.

## Proof

Fix $x$ and a row $j$. Let $I_y = [h_j(y) = h_j(x)]$ for $y \ne x$, and
$$ Z_j = C[j][h_j(x)] - f_x = \sum_{y \ne x} f_y I_y. $$

**Part 1.** In the strict turnstile model $f_y \ge 0$ and $I_y \ge 0$, so $Z_j \ge 0$ for each $j$, and $\hat f_x = f_x + \min_j Z_j \ge f_x$.

**Part 2.** By [linearity of expectation](/linearity-of-expectation/) and universality,
$$ \mathbb{E}[Z_j] = \sum_{y \ne x} f_y \Pr[h_j(y) = h_j(x)] \le \frac{N - f_x}{w} \le \frac{\varepsilon (N - f_x)}{e}. $$
If $N = f_x$, then $Z_j = 0$ and there is nothing to prove. Otherwise $Z_j \ge 0$ and Markov's inequality gives
$$ \Pr[Z_j > \varepsilon(N - f_x)] \le \Pr[Z_j \ge \varepsilon(N - f_x)] \le \frac{\mathbb{E}[Z_j]}{\varepsilon(N - f_x)} \le \frac{1}{e}. $$
The estimate is too large by more than $\varepsilon(N - f_x)$ only if $Z_j > \varepsilon(N - f_x)$ for each $j$. The hash functions are independent, so the $Z_j$ are independent, and
$$ \Pr\big[\hat f_x > f_x + \varepsilon(N - f_x)\big] = \prod_{j=1}^{d} \Pr[Z_j > \varepsilon(N - f_x)] \le e^{-d} \le \delta. $$
Since $N - f_x \le N$, the second form follows.

**General turnstile.** Now $Z_j$ can be negative, but $|Z_j| \le \sum_{y \ne x} |f_y| I_y$, so $\mathbb{E}|Z_j| \le \|f\|_1 / w \le \varepsilon\|f\|_1/e$. Markov's inequality gives $\Pr[|Z_j| > 3\varepsilon\|f\|_1] \le 1/(3e) < 1/8$ (if $\|f\|_1 = 0$ all counters are 0). The median is off by more than $3\varepsilon\|f\|_1$ only if at least $\lceil d/2 \rceil$ of the independent rows are, which has probability at most
$$ \binom{d}{\lceil d/2 \rceil} \left(\frac18\right)^{\lceil d/2 \rceil} \le 2^d \cdot 2^{-3d/2} = 2^{-d/2}. \qquad \blacksquare $$

## Consequences

**Space.** The sketch has $\lceil e/\varepsilon \rceil \cdot \lceil \ln(1/\delta) \rceil$ counters. For $\varepsilon = 0.001$ and $\delta = 0.01$ this is $w = 2719$ and $d = 5$, so 13595 counters, about 53 KB with 4-byte counters. On a stream of $N = 10^9$ updates, each fixed query is then within $10^6$ of the truth with probability at least 0.99.

**Why $e$.** The proof works with any width $w = c/\varepsilon$ for $c > 1$: each row fails with probability at most $1/c$, so $d = \ln(1/\delta)/\ln c$ rows suffice. The total $w d = \frac{c}{\ln c} \cdot \frac{1}{\varepsilon}\ln\frac{1}{\delta}$ is smallest at $c = e$. The difference is small: $c = 2$ or $c = 4$ costs 6 percent more.

**All items at once.** The bound is for one fixed query. For a set of $Q$ queries chosen before the hash functions, the [union bound](/union-bound/) with $\delta/Q$ in place of $\delta$ costs only an additive $\ln Q$ in the depth.

**Heavy hitters.** An item with $f_x \ge \phi N$ has $\hat f_x \ge \phi N$ always, and an item with $f_x < (\phi - \varepsilon) N$ has $\hat f_x < \phi N$ with probability at least $1 - \delta$. So the threshold $\phi N$ separates the [frequent items](/frequent-items-problem/) with few errors.

**Products.** The estimate of an inner product $\sum_x f_x g_x$ from the row-wise products of two sketches, minimized over the rows, is too large by at most $\varepsilon \|f\|_1 \|g\|_1$ with probability $1 - \delta$, by the same argument.

## Tightness

**The width $1/\varepsilon$ is needed.** Take $N$ distinct items of weight 1, with $N$ large, and query a further item $x$. With fully random hash functions, the error in a row is a binomial count with mean $N/w$. If $w = c/\varepsilon$ with $c < 1$, the mean is $\varepsilon N/c > \varepsilon N$, and the error exceeds $\varepsilon N$ in each row with probability tending to 1 as $N$ grows. So the width must be at least about $1/\varepsilon$.

**The depth $\log(1/\delta)$ is needed.** Take $t = 1/\varepsilon$ items of weight $\varepsilon N$ each and query an absent $x$. A row errs by more than $\varepsilon N$ when at least two of the $t$ items share the counter of $x$. With $w = e/\varepsilon$ and fully random hashing this count is close to a [Poisson](/poisson-distribution/) variable with mean $1/e$, which is at least 2 with probability about $0.053$. The rows are independent, so the error probability is about $0.053^d$, and $\delta$ needs $d \ge \ln(1/\delta)/\ln(19)$ rows.

**Markov's inequality is not tight here.** On many inputs the true error is much smaller than the bound, because the colliding weight is a sum of many small terms. The bound $e^{-d}$ is for the worst input.

**The problem itself.** The [frequency estimation problem](/frequency-estimation/) needs $\Omega(1/\varepsilon)$ bits by a reduction from the index problem, so the width of the sketch is optimal up to a constant factor and the size of the counters.

## History

Cormode and Muthukrishnan introduced the count-min sketch and this bound at LATIN 2004, with the journal version in 2005. Similar ideas were older: the multistage filters of Estan and Varghese (2002) kept several hashed arrays of counters and took the minimum, and their conservative update increases only the smallest counters. The [count sketch](/count-sketch/) of Charikar, Chen and Farach-Colton (2002) uses random signs and a median for an error in terms of $\|f\|_2$. The contribution of the count-min paper was the simple analysis with pairwise independence and the many reductions to point queries.

## References
