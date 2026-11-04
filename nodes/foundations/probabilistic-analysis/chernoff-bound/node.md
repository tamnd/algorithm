---
tag: D7FZ82
kind: theorem
slug: chernoff-bound
name: Chernoff bound
aliases:
- Chernoff-Hoeffding bound
- Chernoff inequality
area: foundations/probabilistic-analysis
level: core
summary: A sum of independent 0/1 variables with mean mu exceeds (1+delta)mu or falls below (1-delta)mu with probability exponentially small in mu, proved with the moment generating function.
prereqs: [markov-inequality, moment-generating-function, independent-random-variables, expected-value]
see_also: [binomial-tail-bounds, hoeffding-inequality, chebyshev-inequality, union-bound, high-probability-bounds, azuma-inequality, concentration-of-measure, balls-into-bins]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 4, Chernoff and Hoeffding Bounds, Sections 4.1 to 4.3 (Theorem 4.4 upper tail, Theorem 4.5 lower tail, Corollary 4.6 two-sided form)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 4, Tail Inequalities, Section 4.1, The Chernoff bound
  - book: isbn:9780521884273
    title: Devdatt P. Dubhashi and Alessandro Panconesi, Concentration of Measure for the Analysis of Randomized Algorithms
    locator: Chapter 1, Chernoff-Hoeffding Bounds, Sections 1.3 to 1.6; Chapter 3 for dependent settings (negative association)
  - paper: doi:10.1214/aoms/1177729330
    title: Herman Chernoff, A measure of asymptotic efficiency for tests of a hypothesis based on the sum of observations, Annals of Mathematical Statistics 23(4), 1952
    locator: pages 493 to 507
  - url: "https://en.wikipedia.org/wiki/Chernoff_bound"
    locator: lead section (Chernoff attributed the bound to Herman Rubin; Cramér 1938)
---

The Chernoff bound says that a sum $X$ of [independent](/independent-random-variables/) 0/1 random variables is unlikely to be far from its mean $\mu$: the probability that $X \ge (1+\delta)\mu$ or $X \le (1-\delta)\mu$ falls exponentially in $\mu$. The proof applies [Markov's inequality](/markov-inequality/) to $e^{tX}$ and uses the [moment generating function](/moment-generating-function/) of $X$. It is the main tool behind [high probability bounds](/high-probability-bounds/) for randomized algorithms, from load balancing and [randomized rounding](/randomized-rounding/) to [balls into bins](/balls-into-bins/).

## Statement

Let $X_1, \ldots, X_n$ be independent random variables with $X_i \in \{0, 1\}$ and $\Pr[X_i = 1] = p_i$ (Poisson trials: the $p_i$ may differ). Let $X = \sum_{i=1}^n X_i$ and $\mu = \mathbb{E}[X] = \sum_i p_i$, and assume $\mu > 0$.

**Upper tail.** For each $\delta > 0$,
$$ \Pr[X \ge (1+\delta)\mu] \le \left(\frac{e^{\delta}}{(1+\delta)^{1+\delta}}\right)^{\mu}. \tag{U} $$

**Lower tail.** For each $0 < \delta < 1$,
$$ \Pr[X \le (1-\delta)\mu] \le \left(\frac{e^{-\delta}}{(1-\delta)^{1-\delta}}\right)^{\mu}. \tag{L} $$

**Simple forms.** From (U) and (L):

1. For each $\delta > 0$: $\Pr[X \ge (1+\delta)\mu] \le e^{-\delta^2\mu/(2+\delta)}$.
2. For $0 < \delta \le 1$: $\Pr[X \ge (1+\delta)\mu] \le e^{-\delta^2\mu/3}$. For $\delta \ge 1$: $\Pr[X \ge (1+\delta)\mu] \le e^{-\delta\mu/3}$.
3. For $0 < \delta < 1$: $\Pr[X \le (1-\delta)\mu] \le e^{-\delta^2\mu/2}$.
4. For $R \ge 6\mu$: $\Pr[X \ge R] \le 2^{-R}$.
5. Two-sided, for $0 < \delta < 1$: $\Pr[|X - \mu| \ge \delta\mu] \le 2e^{-\delta^2\mu/3}$.

**Bounds on the mean.** (U) and forms 1, 2 and 4 stay true when $\mu$ is replaced by any $\mu_H \ge \mathbb{E}[X]$. (L) and form 3 stay true when $\mu$ is replaced by any $0 < \mu_L \le \mathbb{E}[X]$.

## In plain words

Flip many coins, each with its own chance of heads, and count the heads. On average you get some number of heads. The Chernoff bound says that the count lands far above or far below the average only with a tiny probability, and the probability shrinks exponentially as the average grows. To be twice as far away, in relative terms, costs about four times as much in the exponent.

The trick of the proof is to look at an exponential of the count instead of the count itself. A large count makes the exponential huge, and Markov's inequality, which only knows the average, then gives a very small probability. The coins must not influence each other: for coins that are glued together the bound can fail.

## Proof

Fix the setting of the statement. The proof has three steps for (U) and (L), then one step for each simple form.

**Step 1 (the generating function of one trial).** For each real $t$,
$$ \mathbb{E}[e^{tX_i}] = (1 - p_i) + p_i e^t = 1 + p_i(e^t - 1) \le \exp\bigl(p_i(e^t - 1)\bigr). $$
The last step uses $1 + y \le e^y$ for each real $y$. This holds because $g(y) = e^y - 1 - y$ has $g(0) = 0$ and $g'(y) = e^y - 1$, which is negative for $y < 0$ and positive for $y > 0$, so $g \ge 0$.

**Step 2 (independence).** The variables $e^{tX_1}, \ldots, e^{tX_n}$ are independent, because the $X_i$ are. The expectation of a product of independent variables is the product of the expectations. So
$$ \mathbb{E}[e^{tX}] = \prod_{i=1}^n \mathbb{E}[e^{tX_i}] \le \prod_{i=1}^n \exp\bigl(p_i(e^t - 1)\bigr) = \exp\bigl(\mu(e^t - 1)\bigr). \tag{M} $$
This is the only place where independence is used.

**Step 3 (Markov on the exponential).** *Upper tail.* Let $t > 0$ and $a = (1+\delta)\mu$. The map $x \mapsto e^{tx}$ is increasing, so $X \ge a$ holds exactly when $e^{tX} \ge e^{ta}$. The variable $e^{tX}$ is positive, so Markov's inequality applies:
$$ \Pr[X \ge a] = \Pr[e^{tX} \ge e^{ta}] \le \frac{\mathbb{E}[e^{tX}]}{e^{ta}} \le \frac{\exp(\mu(e^t - 1))}{e^{t(1+\delta)\mu}}. $$
Choose $t = \ln(1+\delta)$, which is positive because $\delta > 0$. Then $e^t - 1 = \delta$ and $e^{t(1+\delta)\mu} = (1+\delta)^{(1+\delta)\mu}$, which gives (U).

*Lower tail.* Let $t < 0$ and $a = (1-\delta)\mu$. Now $x \mapsto e^{tx}$ is decreasing, so $X \le a$ holds exactly when $e^{tX} \ge e^{ta}$. By Markov's inequality and (M),
$$ \Pr[X \le a] \le \frac{\mathbb{E}[e^{tX}]}{e^{ta}} \le \frac{\exp(\mu(e^t - 1))}{e^{t(1-\delta)\mu}}. $$
Choose $t = \ln(1-\delta)$, which is negative because $0 < \delta < 1$. Then $e^t - 1 = -\delta$ and $e^{t(1-\delta)\mu} = (1-\delta)^{(1-\delta)\mu}$, which gives (L).

The choices of $t$ are the best ones: the exponent $\mu(e^t - 1) - t(1\pm\delta)\mu$ has derivative $\mu e^t - (1\pm\delta)\mu$, which is zero exactly at these values.

**Step 4 (form 1).** Take logarithms. Form 1 follows from (U) when $\mu(\delta - (1+\delta)\ln(1+\delta)) \le -\mu\delta^2/(2+\delta)$. We first show
$$ \ln(1+\delta) \ge \frac{2\delta}{2+\delta} \quad \text{for } \delta \ge 0. $$
Let $h(\delta) = \ln(1+\delta) - 2\delta/(2+\delta)$. Then $h(0) = 0$ and
$$ h'(\delta) = \frac{1}{1+\delta} - \frac{4}{(2+\delta)^2} = \frac{(2+\delta)^2 - 4(1+\delta)}{(1+\delta)(2+\delta)^2} = \frac{\delta^2}{(1+\delta)(2+\delta)^2} \ge 0, $$
so $h \ge 0$ on $[0, \infty)$. Hence
$$ \delta - (1+\delta)\ln(1+\delta) \le \delta - \frac{2\delta(1+\delta)}{2+\delta} = \frac{2\delta + \delta^2 - 2\delta - 2\delta^2}{2+\delta} = -\frac{\delta^2}{2+\delta}. $$
Multiply by $\mu > 0$ and exponentiate.

**Step 5 (form 2).** For $0 < \delta \le 1$ we have $2 + \delta \le 3$, so $\delta^2/(2+\delta) \ge \delta^2/3$, and form 1 gives $e^{-\delta^2\mu/3}$. For $\delta \ge 1$ we have $3\delta \ge 2 + \delta$, so $\delta^2/(2+\delta) \ge \delta/3$, and form 1 gives $e^{-\delta\mu/3}$.

**Step 6 (form 3).** Form 3 follows from (L) when $-\delta - (1-\delta)\ln(1-\delta) \le -\delta^2/2$ for $0 < \delta < 1$. For $|\delta| < 1$ the series $\ln(1-\delta) = -\sum_{k \ge 1}\delta^k/k$ converges absolutely, so we may multiply it by $1-\delta$ term by term:
$$ (1-\delta)\ln(1-\delta) = -\sum_{k\ge1}\frac{\delta^k}{k} + \sum_{k\ge1}\frac{\delta^{k+1}}{k} = -\delta + \sum_{k\ge2}\delta^k\left(\frac{1}{k-1} - \frac1k\right) = -\delta + \sum_{k\ge2}\frac{\delta^k}{k(k-1)}. $$
So $-\delta - (1-\delta)\ln(1-\delta) = -\sum_{k\ge2}\delta^k/(k(k-1)) \le -\delta^2/2$, because the term $k = 2$ is $\delta^2/2$ and all other terms are positive.

**Step 7 (form 4).** Let $R \ge 6\mu$ and set $\delta = R/\mu - 1 \ge 5$, so $R = (1+\delta)\mu$. From (U) and $e^\delta \le e^{1+\delta}$,
$$ \Pr[X \ge R] \le \left(\frac{e^{1+\delta}}{(1+\delta)^{1+\delta}}\right)^{\mu} = \left(\frac{e}{1+\delta}\right)^{(1+\delta)\mu} = \left(\frac{e}{1+\delta}\right)^{R} \le \left(\frac{e}{6}\right)^{R} \le 2^{-R}, $$
since $1 + \delta \ge 6$ and $e/6 = 0.453 < 1/2$.

**Step 8 (form 5).** The events $X \ge (1+\delta)\mu$ and $X \le (1-\delta)\mu$ cover the event $|X - \mu| \ge \delta\mu$. By the [union bound](/union-bound/), form 2 (valid since $\delta < 1$) and form 3, the probability is at most $e^{-\delta^2\mu/3} + e^{-\delta^2\mu/2} \le 2e^{-\delta^2\mu/3}$.

**Step 9 (bounds on the mean).** Let $\mu_H \ge \mu$. For $t > 0$ we have $e^t - 1 > 0$, so (M) gives $\mathbb{E}[e^{tX}] \le \exp(\mu_H(e^t - 1))$. Steps 3, 4, 5 and 7 then run with $\mu_H$ in place of $\mu$ and with the event $X \ge (1+\delta)\mu_H$. Let $0 < \mu_L \le \mu$. For $t < 0$ we have $e^t - 1 < 0$, so $\mu(e^t - 1) \le \mu_L(e^t - 1)$, and Steps 3 and 6 run with $\mu_L$. $\square$

## Consequences

**Variables in $[0, 1]$.** The statement holds for independent $X_i$ with values anywhere in $[0, 1]$ and $\mathbb{E}[X_i] = p_i$. Only Step 1 changes. For $x \in [0, 1]$ the convexity of $x \mapsto e^{tx}$ gives $e^{tx} \le (1 - x)e^{0} + x e^{t}$. Take expectations: $\mathbb{E}[e^{tX_i}] \le 1 + p_i(e^t - 1)$, and the rest of the proof is the same. For variables in a general interval $[a_i, b_i]$, see [Hoeffding's inequality](/hoeffding-inequality/).

**Load balancing.** Assign $m$ jobs to $n$ machines, each job to a machine chosen uniformly and independently. The load $X$ of one machine is a sum of $m$ independent trials with $p = 1/n$, so $\mu = m/n$. Fix $c > 0$ and assume $\mu \ge 3(c+1)\ln n$. Set $\delta = \sqrt{3(c+1)\ln n/\mu}$, so that $\delta \le 1$. Form 2 gives $\Pr[X \ge (1+\delta)\mu] \le e^{-\delta^2\mu/3} = n^{-(c+1)}$. The union bound over the $n$ machines gives
$$ \Pr\left[\max \text{load} \ge \mu + \sqrt{3(c+1)\mu\ln n}\right] \le n^{-c}. $$
So when each machine expects at least a logarithmic number of jobs, the maximum load is $\mu + O(\sqrt{\mu\log n})$ with high probability. When $m = n$, the expected load is 1 and the right answer is different: the maximum load is $\Theta(\log n/\log\log n)$, see [balls into bins](/balls-into-bins/).

Take $n = 1000$ machines, $m = 100000$ jobs, so $\mu = 100$, and ask for a load level $L$ that no machine reaches, except with probability at most $10^{-3}$. Each method below bounds $\Pr[\text{one machine} \ge L]$ by $10^{-6}$ and then takes the union bound over the 1000 machines.

| method | smallest $L$ |
| --- | --- |
| simple form 2, $\delta = \sqrt{3\ln(10^6)/100} = 0.644$ | 165 |
| full bound (U) | 157 |
| exact binomial tail of one machine | 152 |
| [Chebyshev](/chebyshev-inequality/), with variance $99.9$ | 10095 |

The exact tail of one machine is $7.910 \times 10^{-7}$ at $L = 152$ and $1.667 \times 10^{-9}$ at $L = 165$. Chebyshev needs a deviation of $9995$ because its bound decays only as the inverse square of the deviation. The Chernoff bounds ask for 5 to 13 more jobs than the exact tail. The deviation that Chebyshev needs is about 190 times the exact one, which is 52.

**Error reduction.** A [Monte Carlo algorithm](/monte-carlo-algorithm/) that answers a yes or no question correctly with probability $2/3$ can be run $k$ times, and the majority answer taken. The number of correct runs has mean $\mu = 2k/3$, and the majority is wrong only if it is at most $k/2 = (1 - 1/4)\mu$. Form 3 with $\delta = 1/4$ bounds this by $e^{-\mu/32} = e^{-k/48}$. See [error amplification](/error-amplification/) and the [median trick](/median-trick/).

## Tightness

The table compares the bounds for $X$ with the [binomial distribution](/binomial-distribution/) $\mathrm{Bin}(1000, 0.1)$, so $\mu = 100$ and the variance is $90$. Chebyshev is the two-sided bound $90/(\delta\mu)^2$, capped at 1. Markov is $1/(1+\delta)$.

| $\delta$ | event | exact | (U) | form 1 | form 2 | Chebyshev | Markov |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.1 | $X \ge 110$ | $1.583 \times 10^{-1}$ | $6.162 \times 10^{-1}$ | $6.211 \times 10^{-1}$ | $7.165 \times 10^{-1}$ | $0.900$ | $0.909$ |
| 0.2 | $X \ge 120$ | $2.200 \times 10^{-2}$ | $1.528 \times 10^{-1}$ | $1.623 \times 10^{-1}$ | $2.636 \times 10^{-1}$ | $0.225$ | $0.833$ |
| 0.3 | $X \ge 130$ | $1.341 \times 10^{-3}$ | $1.645 \times 10^{-2}$ | $1.998 \times 10^{-2}$ | $4.979 \times 10^{-2}$ | $0.100$ | $0.769$ |
| 0.5 | $X \ge 150$ | $4.489 \times 10^{-7}$ | $2.000 \times 10^{-5}$ | $4.540 \times 10^{-5}$ | $2.404 \times 10^{-4}$ | $0.036$ | $0.667$ |
| 1.0 | $X \ge 200$ | $2.928 \times 10^{-21}$ | $1.673 \times 10^{-17}$ | $3.338 \times 10^{-15}$ | $3.338 \times 10^{-15}$ | $0.009$ | $0.500$ |

For the lower tail of the same variable:

| $\delta$ | event | exact | (L) | form 3 | Chebyshev |
| --- | --- | --- | --- | --- | --- |
| 0.1 | $X \le 90$ | $1.582 \times 10^{-1}$ | $5.960 \times 10^{-1}$ | $6.065 \times 10^{-1}$ | $0.900$ |
| 0.2 | $X \le 80$ | $1.761 \times 10^{-2}$ | $1.167 \times 10^{-1}$ | $1.353 \times 10^{-1}$ | $0.225$ |
| 0.3 | $X \le 70$ | $5.745 \times 10^{-4}$ | $6.521 \times 10^{-3}$ | $1.111 \times 10^{-2}$ | $0.100$ |
| 0.5 | $X \le 50$ | $5.995 \times 10^{-9}$ | $2.172 \times 10^{-7}$ | $3.727 \times 10^{-6}$ | $0.036$ |

The exponents are close to the truth, and the bounds are off by a factor that grows slowly. Two facts explain the gap. First, Step 1 replaces $1 + p_i(e^t - 1)$ by $\exp(p_i(e^t - 1))$, which is the generating function of a [Poisson](/poisson-distribution/) variable. For a binomial variable the sharper exponent is the relative entropy $D(a \| p)$, see [binomial tail bounds](/binomial-tail-bounds/). Second, every bound of the form $\inf_t \mathbb{E}[e^{tX}]e^{-ta}$ misses a polynomial factor: for a binomial with fixed $p$ and $\delta$, the exact tail is smaller than the optimized bound by a factor of order $1/\sqrt{\mu}$.

**(U) cannot be improved by more than a factor $e\sqrt{k}$.** Let $Y$ have the Poisson distribution with mean $\mu$, and let $k = (1+\delta)\mu$ be an integer. By the weak form of [Stirling's approximation](/stirling-approximation/), $k! \le e\sqrt{k}\,(k/e)^k$, so
$$ \Pr[Y \ge k] \ge \Pr[Y = k] = \frac{e^{-\mu}\mu^k}{k!} \ge \frac{e^{-\mu + k}}{e\sqrt k}\left(\frac{\mu}{k}\right)^k = \frac{1}{e\sqrt k}\left(\frac{e^{\delta}}{(1+\delta)^{1+\delta}}\right)^{\mu}. $$
The binomial $\mathrm{Bin}(n, \mu/n)$ is a sum of Poisson trials with mean $\mu$, and its tails tend to those of $Y$ as $n \to \infty$. So no bound that depends only on $\mu$ and $\delta$ can beat (U) by more than the factor $e\sqrt{k}$. For $\mu = 10$ and $\delta = 1$: (U) gives $(e/4)^{10} = 0.0210$, the Poisson tail $\Pr[Y \ge 20]$ is $0.00345$, and the lower estimate is $0.00173$.

**Form 4 is loose but convenient.** For $\mathrm{Bin}(1000, 0.001)$, so $\mu = 1$, form 4 gives $\Pr[X \ge 6] \le 2^{-6} = 0.0156$; the exact value is $5.881 \times 10^{-4}$.

### Pitfalls

- **Independence is required.** Let $X_1 = X_2 = \cdots = X_n$ be one fair coin, copied. Then $\mu = n/2$ and $\Pr[X \ge 2\mu] = \Pr[X = n] = 1/2$ for each $n$, while form 2 claims $e^{-n/6}$. The proof fails in Step 2: the generating function of a sum of dependent variables is not the product.
- **Pairwise independence is not enough.** Take $k$ fair independent bits $b_1, \ldots, b_k$ and, for each nonempty set $S \subseteq \{1, \ldots, k\}$, the bit $Y_S = \bigoplus_{i \in S} b_i$. These $n = 2^k - 1$ bits are uniform and [pairwise independent](/pairwise-independence/): for $S \ne T$ the map $b \mapsto (Y_S, Y_T)$ is linear over GF(2) with two independent rows, so it takes each of the 4 values on $2^{k-2}$ inputs. If all $b_i = 0$, all $Y_S = 0$. For $k = 10$: $n = 1023$, $\mu = 511.5$, and $\Pr[X = 0] = 2^{-10} = 9.766 \times 10^{-4}$, while form 3 with $\delta = 0.99$ would claim at most $1.379 \times 10^{-109}$. For pairwise independent variables use [Chebyshev's inequality](/chebyshev-inequality/).
- **Negative dependence is allowed.** The bounds hold for negatively associated variables, for example the indicators that the bins are empty when balls are thrown at random; see Dubhashi and Panconesi, Chapter 3. Do not assume this for other dependent variables.
- **Form 2 needs $\delta \le 1$.** For $\mathrm{Bin}(1000, 0.001)$ and $\delta = 9$, the exact $\Pr[X \ge 10]$ is $1.074 \times 10^{-7}$, but $e^{-\delta^2\mu/3} = e^{-27} = 1.880 \times 10^{-12}$ is smaller than the truth. The correct bounds are (U), $8.103 \times 10^{-7}$, or form 2 for $\delta \ge 1$, $e^{-3} = 0.0498$.
- **Which way the mean may move.** An upper bound $\mu_H \ge \mathbb{E}[X]$ may replace $\mu$ in the upper tail, and a lower bound $\mu_L$ in the lower tail. The other way round is false: a smaller $\mu$ in the upper tail makes the event larger, not smaller.
- **The bound is relative.** For small $\mu$ the bound $e^{-\delta^2\mu/3}$ is near 1 for every $\delta \le 1$. When $\mu$ is a constant, use (U) with a large $\delta$, or form 4.
- **Union bound over too many events.** A per-event bound of $n^{-(c+1)}$ survives a union over $n$ events, not over $2^n$ events. The constant $c$ in "with high probability" depends on the constant in the threshold, as in the load balancing example.

## History

Herman Chernoff published the method in 1952, in a paper on the asymptotic efficiency of statistical tests. The paper bounds the tail of a sum of independent identically distributed variables by $\inf_t \mathbb{E}[e^{t(X - a)}]^n$ and shows that the exponent is asymptotically exact. Chernoff later attributed the bound itself to Herman Rubin, and Harald Cramér had proved a closely related result on large deviations in 1938 (see the Wikipedia article in the sources). Hoeffding's 1963 paper gave the versions for bounded variables. The multiplicative forms (U) and (L) for Poisson trials, with their simple forms, are the standard ones in computer science; they appear in this form in Motwani and Raghavan (1995), Chapter 4, and in Mitzenmacher and Upfal, Chapter 4.

## References
