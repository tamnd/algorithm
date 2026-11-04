---
tag: 2MFT4K
kind: concept
slug: moment-generating-function
name: Moment generating function
aliases:
- MGF
- exponential moment
area: foundations/probabilistic-analysis
level: advanced
summary: E[e^(tX)] as a function of t; its exponential-moment bounds drive Chernoff-type tail bounds.
prereqs: [expected-value, random-variable, independent-random-variables, markov-inequality]
see_also: [chernoff-bound, hoeffding-inequality, binomial-tail-bounds, variance, central-limit-theorem, generating-functions, poisson-distribution, geometric-distribution]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 4.1, Moment Generating Functions; Section 4.2, Deriving and Applying Chernoff Bounds (4.2.1, sums of Poisson trials); Section 9.1.3, the moment generating function of the normal distribution
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 4, Tail Inequalities (Section 4.1, the Chernoff bound)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.5, The tails of the binomial distribution
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume 1, third edition
    locator: Chapter XI, Integral-Valued Variables. Generating Functions
---

The moment generating function (MGF) of a [random variable](/random-variable/) $X$ is the function $M_X(t) = \mathrm{E}[e^{tX}]$ of a real parameter $t$, with values in $(0, \infty]$. When it is finite near $t = 0$, its derivatives at 0 are the moments $\mathrm{E}[X^k]$, and it fixes the distribution of $X$. The MGF of a sum of [independent random variables](/independent-random-variables/) is the product of their MGFs. With [Markov's inequality](/markov-inequality/) applied to $e^{tX}$, this gives the exponentially small tails of the [Chernoff bound](/chernoff-bound/), the main tool for "with high probability" claims about randomized algorithms.

## In plain words

Markov's inequality bounds how often a non-negative quantity is far above its average. It is weak: it only says that a quantity is at least ten times its average at most one time in ten.

The trick behind the moment generating function is to apply Markov's inequality not to the quantity itself but to an exponential of it. The exponential turns a moderate excess into a huge one, so the same weak inequality gives a very strong bound. There is a free knob, the rate of the exponential, and you turn it to get the best bound.

The exponential also has a second gift. The exponential of a sum is a product, and the average of a product of independent parts is the product of their averages. So for a sum of many independent coin flips, the computation splits into one small computation for each flip.

## The idea

### Definition and domain

For a real random variable $X$, let

$$M_X(t) = \mathrm{E}\big[e^{tX}\big] \in (0, \infty], \qquad t \in \mathbb{R}.$$

The value is well defined because $e^{tX} > 0$. Always $M_X(0) = 1$. The set $D = \{t : M_X(t) < \infty\}$ is an interval that holds 0: if $a, b \in D$ and $0 \le \lambda \le 1$, then $e^{(\lambda a + (1-\lambda)b)x} \le \lambda e^{ax} + (1-\lambda)e^{bx}$ for each $x$, because $s \mapsto e^{sx}$ is a [convex function](/convex-function/), so $\lambda a + (1-\lambda)b \in D$. The interval can be all of $\mathbb{R}$ (a bounded $X$), a half-line, or only $\{0\}$.

For a variable with values in $\{0, 1, 2, \ldots\}$, the probability generating function $G_X(z) = \mathrm{E}[z^X] = \sum_k \Pr[X = k]z^k$ carries the same information, and $M_X(t) = G_X(e^t)$. Feller, Chapter XI, works with $G_X$. See also [generating functions](/generating-functions/).

### Moments from derivatives

**Claim.** If $M_X(t) < \infty$ for all $t$ in $(-\delta, \delta)$ for some $\delta > 0$, then $\mathrm{E}[|X|^k] < \infty$ for each $k \ge 0$, and for $|t| < \delta$

$$M_X(t) = \sum_{k \ge 0} \frac{\mathrm{E}[X^k]}{k!}\,t^k, \qquad \text{so} \qquad M_X^{(k)}(0) = \mathrm{E}[X^k].$$

*Proof.* Fix $s$ with $0 < s < \delta$. Since $e^{s|x|} \le e^{sx} + e^{-sx}$, we get $\mathrm{E}[e^{s|X|}] \le M_X(s) + M_X(-s) < \infty$. All terms of $e^{s|X|} = \sum_k s^k|X|^k/k!$ are non-negative, so the mean of the sum is the sum of the means: $\sum_k s^k\,\mathrm{E}[|X|^k]/k! < \infty$. Each term is finite, so $\mathrm{E}[|X|^k] < \infty$. For $|t| \le s$, the partial sums of $\sum_k t^kX^k/k!$ are bounded in absolute value by $e^{s|X|}$, which has a finite mean. By dominated convergence, $\mathrm{E}[e^{tX}] = \sum_k t^k\mathrm{E}[X^k]/k!$. This is a power series in $t$ that converges on $(-s, s)$, and a power series can be differentiated term by term inside its interval of convergence, so its $k$-th derivative at 0 is $\mathrm{E}[X^k]$. Since $s < \delta$ was arbitrary, the claim holds on $(-\delta, \delta)$. $\square$

In particular $\mathrm{E}[X] = M_X'(0)$ and the [variance](/variance/) is $M_X''(0) - M_X'(0)^2$. The function $\ln M_X(t)$ is often easier: its first two derivatives at 0 are the mean and the variance.

### Sums of independent variables

**Claim.** If $X$ and $Y$ are independent, then $M_{X+Y}(t) = M_X(t)\,M_Y(t)$ for each real $t$ (with $\infty \cdot c = \infty$ for $c > 0$). By induction, $M_{X_1 + \cdots + X_n} = \prod_i M_{X_i}$ for mutually independent $X_1, \ldots, X_n$.

*Proof.* $e^{t(X+Y)} = e^{tX}e^{tY}$. The variables $e^{tX}$ and $e^{tY}$ are functions of $X$ and of $Y$, so they are independent, and they are non-negative. For independent non-negative variables, $\mathrm{E}[UV] = \mathrm{E}[U]\,\mathrm{E}[V]$, with the value $\infty$ allowed; this product rule is proved on the page [independent random variables](/independent-random-variables/). For the induction, $X_1 + \cdots + X_{n-1}$ is independent of $X_n$ when the $X_i$ are mutually independent. $\square$

### Uniqueness

If $M_X(t) = M_Y(t) < \infty$ for all $t$ in an open interval around 0, then $X$ and $Y$ have the same distribution. Mitzenmacher and Upfal state this in Section 4.1 and do not prove it; we also only cite it. For variables with values in $\{0, 1, \ldots, m\}$ it is elementary: then $M_X(t) = G_X(e^t)$, and a polynomial $G_X$ that is known on an interval determines its coefficients $\Pr[X = k]$. Uniqueness lets you identify a distribution from its MGF: for example, a sum of independent Poisson variables with means $\lambda_1$ and $\lambda_2$ has MGF $e^{(\lambda_1 + \lambda_2)(e^t - 1)}$, so it is Poisson with mean $\lambda_1 + \lambda_2$.

### The Chernoff method

For each $t > 0$ and each real $a$, the map $x \mapsto e^{tx}$ is increasing, so $\{X \ge a\} = \{e^{tX} \ge e^{ta}\}$. Markov's inequality for the non-negative variable $e^{tX}$ gives

$$\Pr[X \ge a] \le \frac{M_X(t)}{e^{ta}} \quad (t > 0), \qquad \Pr[X \le a] \le \frac{M_X(t)}{e^{ta}} \quad (t < 0).$$

The bound holds for each $t$, so one takes the $t$ that makes it smallest, or a $t$ that makes it simple.

**Theorem (Chernoff bound for Poisson trials).** Let $X = \sum_{i=1}^n X_i$, where the $X_i$ are mutually independent, $X_i \in \{0, 1\}$ and $\Pr[X_i = 1] = p_i$. Let $\mu = \mathrm{E}[X] = \sum_i p_i > 0$. Then for each $\delta > 0$,

$$\Pr[X \ge (1 + \delta)\mu] \le \left(\frac{e^{\delta}}{(1 + \delta)^{1 + \delta}}\right)^{\mu},$$

and for each $0 < \delta < 1$,

$$\Pr[X \le (1 - \delta)\mu] \le \left(\frac{e^{-\delta}}{(1 - \delta)^{1 - \delta}}\right)^{\mu}.$$

*Proof.*

1. For each real $t$, $M_{X_i}(t) = 1 - p_i + p_ie^t = 1 + p_i(e^t - 1)$.
2. The inequality $1 + x \le e^x$ holds for each real $x$: the function $e^x - 1 - x$ has derivative $e^x - 1$, which is negative for $x < 0$ and positive for $x > 0$, so its minimum is its value 0 at $x = 0$. With $x = p_i(e^t - 1)$, $M_{X_i}(t) \le e^{p_i(e^t - 1)}$.
3. By the product rule for independent variables, $M_X(t) = \prod_i M_{X_i}(t) \le \prod_i e^{p_i(e^t - 1)} = e^{\mu(e^t - 1)}$.
4. Upper tail. Take $t = \ln(1 + \delta) > 0$. The Chernoff method gives $\Pr[X \ge (1+\delta)\mu] \le e^{\mu(e^t - 1)}e^{-t(1+\delta)\mu} = e^{\mu\delta}(1+\delta)^{-(1+\delta)\mu}$, which is the first bound.
5. Lower tail. Take $t = \ln(1 - \delta) < 0$. The Chernoff method for $t < 0$ gives $\Pr[X \le (1-\delta)\mu] \le e^{\mu(e^t - 1)}e^{-t(1-\delta)\mu} = e^{-\mu\delta}(1-\delta)^{-(1-\delta)\mu}$, which is the second bound. $\blacksquare$

The choice of $t$ in step 4 minimizes $\mu(e^t - 1) - t(1+\delta)\mu$, the exponent of the bound of step 3. The page [Chernoff bound](/chernoff-bound/) derives the simpler forms such as $e^{-\mu\delta^2/3}$ for $0 < \delta \le 1$, and the page [Hoeffding's inequality](/hoeffding-inequality/) treats bounded variables that are not 0 or 1.

## Examples

**Common MGFs.** Each one follows from the definition by a sum or an integral.

| distribution of $X$ | $M_X(t)$ | where finite |
|---|---|---|
| Bernoulli($p$) | $1 - p + pe^t$ | all $t$ |
| [binomial](/binomial-distribution/)($n, p$) | $(1 - p + pe^t)^n$ | all $t$ |
| [Poisson](/poisson-distribution/)($\lambda$) | $e^{\lambda(e^t - 1)}$ | all $t$ |
| [geometric](/geometric-distribution/)($p$) on $\{1, 2, \ldots\}$, $p < 1$ | $\dfrac{pe^t}{1 - (1-p)e^t}$ | $t < -\ln(1 - p)$ |
| standard normal | $e^{t^2/2}$ | all $t$ |
| normal($\mu, \sigma^2$) | $e^{\mu t + \sigma^2t^2/2}$ | all $t$ |

- *Binomial.* It is a sum of $n$ independent Bernoulli($p$) variables, so the product rule gives the $n$-th power.
- *Poisson.* $\sum_{k \ge 0} e^{tk}e^{-\lambda}\lambda^k/k! = e^{-\lambda}\sum_k (\lambda e^t)^k/k! = e^{-\lambda}e^{\lambda e^t}$.
- *Geometric.* $\sum_{k \ge 1} e^{tk}(1-p)^{k-1}p = pe^t\sum_{j \ge 0}\big((1-p)e^t\big)^j$, a geometric series that converges exactly when $(1-p)e^t < 1$.
- *Normal.* $\frac1{\sqrt{2\pi}}\int e^{tx - x^2/2}\,dx = e^{t^2/2}\cdot\frac1{\sqrt{2\pi}}\int e^{-(x-t)^2/2}\,dx = e^{t^2/2}$, by completing the square. For $\mu + \sigma Z$ use $M_{\mu + \sigma Z}(t) = e^{\mu t}M_Z(\sigma t)$.

**Moments of the binomial.** With $M(t) = (q + pe^t)^n$ and $q = 1 - p$: $M'(t) = npe^t(q + pe^t)^{n-1}$, so $M'(0) = np$. Then $M''(t) = npe^t(q + pe^t)^{n-1} + n(n-1)p^2e^{2t}(q + pe^t)^{n-2}$, so $M''(0) = np + n(n-1)p^2$. The variance is $np + n(n-1)p^2 - n^2p^2 = np(1-p)$.

**A tail of 100 fair coins.** Let $X$ be the number of heads in 100 fair flips, so $\mu = 50$, and bound $\Pr[X \ge 75]$.

| method | bound on $\Pr[X \ge 75]$ |
|---|---|
| [Markov](/markov-inequality/), $\mu/75$ | $0.667$ |
| [Chebyshev](/chebyshev-inequality/), $\mathrm{Var}[X]/25^2 = 25/625$ | $0.04$ |
| Poisson-trials bound above, $\delta = \frac12$: $(e^{0.5}/1.5^{1.5})^{50}$ | $4.47 \times 10^{-3}$ |
| Hoeffding, $e^{-2 \cdot 25^2/100} = e^{-12.5}$ | $3.73 \times 10^{-6}$ |
| best Chernoff bound for this binomial, $2^{100}/3^{75}$ | $2.08 \times 10^{-6}$ |
| exact value, $2^{-100}\sum_{k=75}^{100}\binom{100}{k}$ | $2.82 \times 10^{-7}$ |

The best Chernoff bound minimizes $e^{-75t}\big(\frac{1 + e^t}2\big)^{100}$ over $t > 0$. Setting the derivative of the logarithm to 0 gives $100\,e^t/(1 + e^t) = 75$, so $e^t = 3$ and the bound is $3^{-75}2^{100}$. The Poisson-trials bound is weaker here because step 2 of its proof replaces $1 + x$ by $e^x$, which loses much when $p_i = \frac12$ is not small. The bounds that use the MGF fall exponentially in the number of flips, while Markov and Chebyshev fall at most polynomially.

**Independence is needed for the product.** Let $X$ be a fair bit and $Y = X$. Then $M_{X+Y}(1) = \frac{1 + e^2}2 = 4.19$, but $M_X(1)M_Y(1) = \big(\frac{1 + e}2\big)^2 = 3.46$. The sum $2X$ has a heavier tail than a sum of two independent bits, and a Chernoff bound that assumes independence would be wrong for it.

## Where it is used

- **Tail bounds.** The [Chernoff bound](/chernoff-bound/), the [binomial tail bounds](/binomial-tail-bounds/) and [Hoeffding's inequality](/hoeffding-inequality/) all start from the Chernoff method. They give the [high-probability bounds](/high-probability-bounds/) of randomized algorithms.
- **Balls into bins and load balancing.** The maximum load of $n$ balls in $n$ bins is $O(\log n/\log\log n)$ with high probability, by the Poisson-trials bound for one bin and a [union bound](/union-bound/) over the bins; see [the maximum load of balls into bins](/balls-into-bins-max-load/).
- **Randomized rounding.** The rounded solution of [randomized rounding](/randomized-rounding/) breaks each constraint by only a small factor with high probability, by the Chernoff bound for each constraint.
- **Amplification.** The [median trick](/median-trick/) runs an estimator $O(\log(1/\epsilon))$ times and takes the median. A Chernoff bound on the number of bad runs gives the failure probability $\epsilon$.
- **Limit theorems.** The MGF of a sum of independent variables is a product, so the MGF of a normalized sum is easy to track. One classical proof of the [central limit theorem](/central-limit-theorem/), for variables with an MGF, shows that these MGFs converge to $e^{t^2/2}$.

### Pitfalls

- **The MGF may be infinite.** A finite mean, or even all finite moments, does not give a finite MGF for $t > 0$. For $\Pr[X = k] = c/k^3$ with $k \ge 1$, $\mathrm{E}[X]$ is finite but $M_X(t) = \sum_k ce^{tk}/k^3 = \infty$ for each $t > 0$. The lognormal distribution has all moments finite and still has $M_X(t) = \infty$ for each $t > 0$. For such heavy tails, use the characteristic function $\mathrm{E}[e^{itX}]$, which always exists, or truncate the variable.
- **Moments need an open interval around 0.** The formula $M_X^{(k)}(0) = \mathrm{E}[X^k]$ needs $M_X$ finite on both sides of 0. A one-sided domain is not enough.
- **Independence.** The product rule, and so each Chernoff bound for sums, needs mutual independence of the terms, or a weaker property such as negative association that the bound proves separately. Pairwise independence, which is enough for the variance of a sum, is not enough here.
- **The sign of $t$.** The upper tail uses $t > 0$ and the lower tail uses $t < 0$. Using $t > 0$ for $\Pr[X \le a]$ is wrong, because $e^{tx}$ is then increasing and $\{X \le a\}$ is not $\{e^{tX} \ge e^{ta}\}$.
- **A loose step costs a lot.** The step $1 + x \le e^x$ is tight only for small $x$. For fair coins, it raises the bound in the table from $2.08 \times 10^{-6}$ to $4.47 \times 10^{-3}$. When the $p_i$ are not small, compute or bound $M_X$ directly.

## References
