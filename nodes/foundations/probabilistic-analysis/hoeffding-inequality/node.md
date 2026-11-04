---
tag: WABANV
kind: theorem
slug: hoeffding-inequality
name: Hoeffding's inequality
aliases:
- Hoeffding bound
area: foundations/probabilistic-analysis
level: core
summary: For independent X_i in [a_i, b_i], the sum exceeds its mean by t with probability at most exp(-2t^2 / sum (b_i - a_i)^2); the proof goes through Hoeffding's lemma.
prereqs: [markov-inequality, moment-generating-function, independent-random-variables, convex-function]
see_also: [chernoff-bound, binomial-tail-bounds, azuma-inequality, concentration-of-measure, chebyshev-inequality, pac-learning, random-sampling, median-trick]
sources:
  - paper: doi:10.1080/01621459.1963.10500830
    title: Wassily Hoeffding, Probability inequalities for sums of bounded random variables, Journal of the American Statistical Association 58(301), 1963
    locator: pages 13 to 30; Theorem 2 (sums of independent bounded variables) and its proof (the bound on the moment generating function); Section 6 (sampling without replacement)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 4, Section 4.5, The Hoeffding Bound (Theorem 4.12)
  - book: isbn:9780521884273
    title: Devdatt P. Dubhashi and Alessandro Panconesi, Concentration of Measure for the Analysis of Randomized Algorithms
    locator: Chapter 1, Section 1.5, The Hoeffding extension, and Section 1.6, Useful forms of the bound
  - book: isbn:9780199535255
    title: Stéphane Boucheron, Gábor Lugosi and Pascal Massart, Concentration Inequalities, A Nonasymptotic Theory of Independence
    locator: Chapter 2, Basic inequalities (Hoeffding's lemma and inequality, Bernstein's inequality)
  - paper: doi:10.2748/tmj/1178243286
    title: Kazuoki Azuma, Weighted sums of certain dependent random variables, Tohoku Mathematical Journal 19(3), 1967
    locator: pages 357 to 367
---

Hoeffding's inequality bounds the probability that a sum of [independent](/independent-random-variables/) bounded random variables exceeds its mean: if $a_i \le X_i \le b_i$, the sum $S$ satisfies $\Pr[S - \mathbb{E}S \ge t] \le \exp\bigl(-2t^2/\sum_i(b_i - a_i)^2\bigr)$. The bound depends only on the widths of the ranges, not on the distributions. The key step is Hoeffding's lemma, a bound on the [moment generating function](/moment-generating-function/) of one bounded variable with mean zero. It is the standard tool for sample sizes: to estimate a mean in $[0, 1]$ within $\varepsilon$ with confidence $1 - \delta$, about $\ln(2/\delta)/(2\varepsilon^2)$ samples suffice.

## Statement

**Hoeffding's lemma.** Let $Y$ be a random variable with $a \le Y \le b$ almost surely and $\mathbb{E}[Y] = 0$. Then for each real $s$,
$$ \mathbb{E}[e^{sY}] \le \exp\left(\frac{s^2(b-a)^2}{8}\right). $$

**Hoeffding's inequality.** Let $X_1, \ldots, X_n$ be independent random variables with $a_i \le X_i \le b_i$ almost surely, where $a_i \le b_i$ are real numbers with $\sum_i (b_i - a_i)^2 > 0$. Let $S = \sum_{i=1}^n X_i$. Then for each $t > 0$,
$$ \Pr[S - \mathbb{E}S \ge t] \le \exp\left(-\frac{2t^2}{\sum_{i=1}^n(b_i - a_i)^2}\right), \qquad \Pr[S - \mathbb{E}S \le -t] \le \exp\left(-\frac{2t^2}{\sum_{i=1}^n(b_i - a_i)^2}\right), $$
and so $\Pr[|S - \mathbb{E}S| \ge t] \le 2\exp\bigl(-2t^2/\sum_i(b_i - a_i)^2\bigr)$.

**Mean form.** If all $X_i \in [0, 1]$ and $\bar X = S/n$, then for each $\varepsilon > 0$,
$$ \Pr[\bar X - \mathbb{E}\bar X \ge \varepsilon] \le e^{-2n\varepsilon^2}, \qquad \Pr[|\bar X - \mathbb{E}\bar X| \ge \varepsilon] \le 2e^{-2n\varepsilon^2}. $$

## In plain words

Average many independent measurements, each known to lie between two fixed limits. The average is unlikely to be far from its expected value, and the chance of a given error falls exponentially in the number of measurements times the square of the error. The bound uses only the limits of each measurement. It does not need to know the distribution, the variance, or even whether the measurements have the same distribution.

The price of this generality is that the bound assumes the worst spread that the limits allow. When the measurements are almost always near one value, for example rare events, other bounds that use the actual spread are much sharper.

## Proof

**Proof of Hoeffding's lemma.** If $a = b$, then $Y = 0$ almost surely and both sides equal 1. Assume $a < b$. Since $\mathbb{E}Y = 0$ and $a \le Y \le b$, we have $a \le 0 \le b$.

*Step 1 (convexity).* The function $y \mapsto e^{sy}$ is convex. Each $y \in [a, b]$ is the convex combination $y = \frac{b - y}{b - a}a + \frac{y - a}{b - a}b$, so
$$ e^{sy} \le \frac{b - y}{b - a}e^{sa} + \frac{y - a}{b - a}e^{sb}. $$
Put $y = Y$ and take expectations. Since $\mathbb{E}Y = 0$,
$$ \mathbb{E}[e^{sY}] \le \frac{b}{b - a}e^{sa} - \frac{a}{b - a}e^{sb}. $$

*Step 2 (a two-point variable).* Let $\theta = -a/(b - a)$, so $\theta \in [0, 1]$ and $b/(b - a) = 1 - \theta$. Let $u = s(b - a)$, so $sa = -\theta u$ and $sb = (1-\theta)u$. The right side of Step 1 is
$$ (1 - \theta)e^{-\theta u} + \theta e^{(1 - \theta)u} = e^{-\theta u}\bigl(1 - \theta + \theta e^u\bigr) = e^{\psi(u)}, \qquad \psi(u) = -\theta u + \ln\bigl(1 - \theta + \theta e^u\bigr). $$
The argument of the logarithm is positive, since $1 - \theta \ge 0$, $\theta \ge 0$, they are not both zero, and $e^u > 0$. The function $\psi$ is the logarithm of the generating function of $W - \theta$, where $W$ takes the value 1 with probability $\theta$ and 0 otherwise. This two-point law is the worst case: Step 1 replaced $Y$ by a variable on $\{a, b\}$ with the same mean.

*Step 3 (derivatives).* Write $\rho(u) = \dfrac{\theta e^u}{1 - \theta + \theta e^u} \in [0, 1]$. Then
$$ \psi(0) = 0, \qquad \psi'(u) = -\theta + \rho(u), \quad \psi'(0) = -\theta + \theta = 0, $$
$$ \psi''(u) = \frac{\theta e^u(1 - \theta + \theta e^u) - \theta e^u\cdot\theta e^u}{(1 - \theta + \theta e^u)^2} = \frac{\theta e^u(1 - \theta)}{(1 - \theta + \theta e^u)^2} = \rho(u)\bigl(1 - \rho(u)\bigr) \le \frac14, $$
because $x(1 - x) \le 1/4$ for every real $x$. (The value $\psi''(u)$ is the variance of a 0/1 variable with mean $\rho(u)$.)

*Step 4 (Taylor).* By Taylor's theorem with the Lagrange remainder, for each $u$ there is $\xi$ between $0$ and $u$ with
$$ \psi(u) = \psi(0) + \psi'(0)u + \tfrac12\psi''(\xi)u^2 \le \frac{u^2}{8} = \frac{s^2(b - a)^2}{8}. $$
With Step 2, $\mathbb{E}[e^{sY}] \le e^{\psi(u)} \le e^{s^2(b-a)^2/8}$. $\square$

**Proof of the inequality.** Let $Y_i = X_i - \mathbb{E}X_i$. Then $\mathbb{E}Y_i = 0$, $Y_i \in [a_i - \mathbb{E}X_i,\ b_i - \mathbb{E}X_i]$, an interval of width $b_i - a_i$, and the $Y_i$ are independent. Let $W = \sum_i(b_i - a_i)^2$ and $s > 0$.

1. *Markov.* Since $x \mapsto e^{sx}$ is increasing and $e^{s(S - \mathbb{E}S)} > 0$, [Markov's inequality](/markov-inequality/) gives $\Pr[S - \mathbb{E}S \ge t] \le e^{-st}\,\mathbb{E}\bigl[e^{s\sum_i Y_i}\bigr]$.
2. *Independence.* The $e^{sY_i}$ are independent, so $\mathbb{E}[e^{s\sum_i Y_i}] = \prod_i\mathbb{E}[e^{sY_i}]$.
3. *Lemma.* Each factor is at most $e^{s^2(b_i - a_i)^2/8}$, so the probability is at most $\exp(-st + s^2W/8)$.
4. *Choice of $s$.* The exponent $-st + s^2W/8$ is smallest at $s = 4t/W > 0$, where it equals $-4t^2/W + 2t^2/W = -2t^2/W$.

For the lower tail apply the same argument to the variables $-X_i \in [-b_i, -a_i]$, which have the same widths. The two-sided form follows by the [union bound](/union-bound/). The mean form is the case $a_i = 0$, $b_i = 1$, $t = n\varepsilon$, where $W = n$ and $2t^2/W = 2n\varepsilon^2$. $\square$

## Consequences

**Sample size for estimating a mean.** Let $X_1, \ldots, X_n$ be independent samples of a variable with values in $[0, 1]$ and unknown mean $p$, for example the indicator that a random input makes a program fail. To get $\Pr[|\bar X - p| \ge \varepsilon] \le \delta$ it suffices that $2e^{-2n\varepsilon^2} \le \delta$, that is
$$ n \ge \frac{\ln(2/\delta)}{2\varepsilon^2}. $$
For $\varepsilon = 0.01$ and $\delta = 0.05$: Hoeffding needs $n \ge 18444.4$, so $n = 18445$. [Chebyshev's inequality](/chebyshev-inequality/) with the variance bound $1/4$ needs $1/(4n\varepsilon^2) \le \delta$, so $n \ge 50000$. The normal approximation suggests $n \approx 1.96^2/(4\varepsilon^2) = 9604$, but it is not a guarantee. The sample size grows only like $\ln(1/\delta)$ in the confidence and like $1/\varepsilon^2$ in the accuracy. For Bernoulli samples the exact error probability $\Pr[|\bar X - p| \ge 0.01]$ is:

| $n$ | exact, $p = 1/2$ | exact, $p = 1/10$ | Hoeffding $2e^{-2n\varepsilon^2}$ | Chebyshev $1/(4n\varepsilon^2)$ |
| --- | --- | --- | --- | --- |
| 9604 | $4.890 \times 10^{-2}$ | $1.096 \times 10^{-3}$ | $0.293$ | $0.260$ |
| 18445 | $6.734 \times 10^{-3}$ | $6.488 \times 10^{-6}$ | $0.0500$ | $0.136$ |
| 50000 | $7.903 \times 10^{-6}$ | $1.252 \times 10^{-13}$ | $9.080 \times 10^{-5}$ | $0.0500$ |

The case $p = 1/2$ has the largest variance and is the hardest; the bound must hold for it. At $p = 1/10$ the bound is far too pessimistic, because it does not see the smaller variance.

**Learning and sampling.** In [PAC learning](/pac-learning/), Hoeffding's inequality for one hypothesis and the union bound over a finite class $\mathcal H$ give that $n \ge \ln(2|\mathcal H|/\delta)/(2\varepsilon^2)$ samples make every empirical error within $\varepsilon$ of the true error, with probability at least $1 - \delta$. The same argument sets the number of trials of a [Monte Carlo algorithm](/monte-carlo-algorithm/) that estimates a probability, and the size of a [random sample](/random-sampling/) for estimating a fraction.

**Martingales.** Step 2 of the proof is the only use of independence. When $X_i$ is only bounded given the past, and has conditional mean 0, Hoeffding's lemma still applies to each conditional generating function, and the tower property replaces the product. This gives the [Azuma inequality](/azuma-inequality/) and the bounded differences inequality of [concentration of measure](/concentration-of-measure/).

## Tightness

**Hoeffding against Chernoff and the exact tail.** The table uses $X \sim \mathrm{Bin}(1000, p)$, a sum of 1000 variables in $[0, 1]$. Chernoff (U) is the multiplicative [Chernoff bound](/chernoff-bound/) $(e^\delta/(1+\delta)^{1+\delta})^{\mu}$ with $\mu = 1000p$ and $(1+\delta)\mu = k$; Hoeffding is $e^{-2(k - \mu)^2/1000}$.

| $p$ | event | exact | Hoeffding | Chernoff (U) | Chebyshev |
| --- | --- | --- | --- | --- | --- |
| 0.5 | $X \ge 520$ | $1.087 \times 10^{-1}$ | $4.493 \times 10^{-1}$ | $6.738 \times 10^{-1}$ | $0.625$ |
| 0.5 | $X \ge 550$ | $8.653 \times 10^{-4}$ | $6.738 \times 10^{-3}$ | $8.887 \times 10^{-2}$ | $0.100$ |
| 0.5 | $X \ge 600$ | $1.364 \times 10^{-10}$ | $2.061 \times 10^{-9}$ | $8.331 \times 10^{-5}$ | $0.025$ |
| 0.5 | $X \ge 700$ | $8.833 \times 10^{-38}$ | $1.805 \times 10^{-35}$ | $3.709 \times 10^{-16}$ | $0.00625$ |
| 0.01 | $X \ge 15$ | $8.241 \times 10^{-2}$ | $9.512 \times 10^{-1}$ | $3.389 \times 10^{-1}$ | $0.396$ |
| 0.01 | $X \ge 20$ | $3.288 \times 10^{-3}$ | $8.187 \times 10^{-1}$ | $2.101 \times 10^{-2}$ | $0.099$ |
| 0.01 | $X \ge 30$ | $2.060 \times 10^{-7}$ | $4.493 \times 10^{-1}$ | $2.356 \times 10^{-6}$ | $0.0248$ |
| 0.01 | $X \ge 50$ | $8.306 \times 10^{-20}$ | $4.076 \times 10^{-2}$ | $2.650 \times 10^{-18}$ | $0.00619$ |

For $p = 1/2$ Hoeffding is much better than Chernoff (U), which pays for replacing a coin by a Poisson variable. For $p = 0.01$ Hoeffding is nearly useless: the deviation $t = 40$ in the last row is large next to the standard deviation $3.15$, but $2t^2/n = 3.2$ is small, because the bound charges each variable for the full width 1 of its range while its variance is only $0.0099$. The sharp exponent for both cases is the relative entropy of [binomial tail bounds](/binomial-tail-bounds/).

**The constant 1/8 in the lemma is best possible.** Let $Y = \pm 1$ with probability $1/2$ each, so $b - a = 2$ and the lemma gives $\mathbb{E}[e^{sY}] = \cosh s \le e^{s^2/2}$. Since $\ln\cosh s = s^2/2 - s^4/12 + O(s^6)$, the ratio $\ln\cosh s/(s^2/2)$ tends to 1 as $s \to 0$, so no constant below $1/8$ works. Numerically $\ln\cosh s$ is $0.0049917$ against $0.005$ at $s = 0.1$, and $0.4338$ against $0.5$ at $s = 1$.

**The constant 2 in the inequality is best possible.** Suppose the bound held with $e^{-ct^2/n}$ for some $c > 2$, for all sums of $n$ fair coins. For a fair coin the exponent of the exact tail is $D(\frac12 + \varepsilon\|\frac12) = \sum_{k \ge 1}(2\varepsilon)^{2k}/(2k(2k-1)) = 2\varepsilon^2 + O(\varepsilon^4)$, so we can fix $\varepsilon > 0$ with $D(\frac12 + \varepsilon\|\frac12) < c\varepsilon^2$; for $\varepsilon = 0.05$ the two exponents are $0.0050084$ and $0.005$. The lower bound of [binomial tail bounds](/binomial-tail-bounds/) gives $\Pr[S - n/2 \ge \varepsilon n] \ge e^{-nD}/(n+1)$ whenever $(\frac12 + \varepsilon)n$ is an integer, and this exceeds $e^{-c\varepsilon^2 n}$ for all large such $n$. So $c \le 2$. For fixed $t/n$ the bound still misses a factor of order $1/\sqrt n$, as every bound obtained from the generating function does.

### Pitfalls

- **Independence.** The proof multiplies generating functions. For dependent variables use a martingale version ([Azuma](/azuma-inequality/)) and check its hypotheses. With $n$ copies of one fair coin the sum is $0$ or $n$, and $\Pr[S - n/2 \ge n/2] = 1/2$, against the claimed $e^{-n/2}$.
- **Bounded almost surely.** The variables must lie in $[a_i, b_i]$ with probability 1. A bound on the mean or the variance is not enough. For unbounded variables, such as geometric or exponential ones, Hoeffding does not apply; truncate them first, or use a bound for that distribution.
- **Range, not variance.** For rare events the variance $p(1-p)$ is far below the worst case $1/4$ of the range, and Hoeffding gives a much weaker bound than the Chernoff bound or Bernstein's inequality, which uses the variance (Boucheron, Lugosi and Massart, Chapter 2). To estimate a small $p$ within a relative error, use the multiplicative Chernoff bound, which needs about $3\ln(2/\delta)/(\varepsilon^2 p)$ samples instead of a number in $1/(\varepsilon p)^2$.
- **Additive error.** The mean form controls $|\bar X - p|$, not $|\bar X - p|/p$. An additive error of $0.01$ says nothing about a probability of $0.001$.
- **The constant.** The exponent is $2t^2/\sum(b_i - a_i)^2$, with the squared widths. Writing $t^2/(2\sum(b_i - a_i)^2)$, the Azuma constant, is valid but four times weaker in the exponent; writing $2t^2/n$ for variables in $[-1, 1]$ is wrong, since the width there is 2 and the correct exponent is $t^2/(2n)$.

## History

Wassily Hoeffding proved the inequality in 1963, in a paper on sums of bounded random variables, together with the sharper relative entropy form for variables in $[0, 1]$ and versions for U-statistics and for sampling without replacement from a finite population. The method, Markov's inequality applied to an exponential, is the one of Chernoff (1952). Azuma (1967) extended the bound to martingales with bounded differences. In computer science the inequality is often stated together with the Chernoff bounds, as in Mitzenmacher and Upfal, Section 4.5.

## References
