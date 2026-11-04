---
tag: QC61E4
kind: theorem
slug: chebyshev-inequality
name: Chebyshev's inequality
aliases:
- Chebyshev inequality
area: foundations/probabilistic-analysis
level: intro
summary: For X with finite variance and a > 0, P(|X - E[X]| >= a) <= Var(X)/a^2; Markov's inequality applied to the squared deviation, valid for sums of pairwise independent variables.
prereqs: [markov-inequality, variance, expected-value]
see_also: [chernoff-bound, hoeffding-inequality, binomial-tail-bounds, pairwise-independence, median-trick, law-of-large-numbers, central-limit-theorem, high-probability-bounds]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.2, Variance and Moments of a Random Variable, and Section 3.3, Chebyshev's Inequality; Chapter 15, Section 15.1.1, A Construction of Pairwise Independent Bits, and Section 15.2, Chebyshev's Inequality for Pairwise Independent Variables
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Section 3.2, The Markov and Chebyshev Inequalities (Theorem 3.3), and Section 3.4, Two-Point Sampling
  - book: isbn:9780521884273
    title: Devdatt P. Dubhashi and Alessandro Panconesi, Concentration of Measure for the Analysis of Randomized Algorithms, Cambridge University Press, 2009
    locator: Chapter 1, Section 1.7, A Variance Bound
  - url: "https://en.wikipedia.org/wiki/Chebyshev%27s_inequality"
    locator: section History (Bienaymé 1853, Chebyshev 1867, Markov 1884), and section Sharpened bounds, Cantelli's inequality
---

Chebyshev's inequality says that a [random variable](/random-variable/) $X$ with mean $\mu$ and finite [variance](/variance/) $\sigma^2$ satisfies $\Pr(|X - \mu| \ge a) \le \sigma^2/a^2$ for each $a > 0$. It is [Markov's inequality](/markov-inequality/) applied to $(X - \mu)^2$. The variance of a sum is the sum of the variances already when the terms are [pairwise independent](/pairwise-independence/), so the inequality bounds sums of variables that are far from independent. This makes it the tool for sampling with few random bits, while the [Chernoff bound](/chernoff-bound/) gives much smaller tails when the terms are fully independent.

## Statement

**Theorem (Chebyshev).** Let $X$ be a random variable with $\mathbb{E}[X^2] < \infty$, mean $\mu = \mathbb{E}[X]$ and variance $\sigma^2 = \mathrm{Var}(X) = \mathbb{E}[(X - \mu)^2]$. For each $a > 0$,
$$ \Pr(|X - \mu| \ge a) \le \frac{\sigma^2}{a^2}. $$
When $\sigma > 0$, the substitution $a = k\sigma$ gives $\Pr(|X - \mu| \ge k\sigma) \le 1/k^2$ for each $k > 0$.

**Lemma (variance of a sum).** Let $X_1, \ldots, X_n$ have finite variances, and let them be pairwise independent: $X_i$ and $X_j$ are independent for each pair $i \ne j$. Then
$$ \mathrm{Var}\Big(\sum_{i=1}^n X_i\Big) = \sum_{i=1}^n \mathrm{Var}(X_i). $$
The same holds when the variables are only pairwise uncorrelated, $\mathbb{E}[X_i X_j] = \mathbb{E}[X_i]\,\mathbb{E}[X_j]$ for $i \ne j$.

**Corollary (sample mean).** If $X_1, \ldots, X_n$ are pairwise independent with common mean $\mu$ and variance $\sigma^2$, and $\bar X = \frac1n \sum_i X_i$, then for each $\varepsilon > 0$
$$ \Pr(|\bar X - \mu| \ge \varepsilon) \le \frac{\sigma^2}{n\varepsilon^2}. $$
This is the weak [law of large numbers](/law-of-large-numbers/) with a rate.

**Variation (Cantelli, one-sided).** Under the hypothesis of the theorem, for each $a > 0$,
$$ \Pr(X - \mu \ge a) \le \frac{\sigma^2}{\sigma^2 + a^2}, \qquad \Pr(X - \mu \le -a) \le \frac{\sigma^2}{\sigma^2 + a^2}. $$

## In plain words

Markov's rule bounds how often a quantity that is never negative can be large, using only its average. Chebyshev's rule applies the same idea to a better quantity: the squared distance of a value from its average. The average of that squared distance is the variance, a number that says how spread out the values are. The result is that a value is rarely many spreads away from the average: it is two spreads or more away at most a quarter of the time, and ten spreads or more away at most one time in a hundred.

The rule is useful for averages of many measurements. The spread of an average shrinks as you take more measurements, and this stays true when the measurements are only independent two at a time. So a few random bits can drive many measurements.

## Proof

**The theorem.** Let $Y = (X - \mu)^2$. Then $Y \ge 0$, and $\mathbb{E}[Y] = \sigma^2$ is finite because $\mathbb{E}[X^2] < \infty$ (this also makes $\mu$ finite, since $|X| \le (1 + X^2)/2$).

1. For $a > 0$, the events $\{|X - \mu| \ge a\}$ and $\{Y \ge a^2\}$ are equal, because $t \mapsto t^2$ is increasing on $[0, \infty)$ and $|X - \mu| \ge 0$.
2. Markov's inequality applies to $Y$, since $Y \ge 0$ and $a^2 > 0$: $\Pr(Y \ge a^2) \le \mathbb{E}[Y]/a^2 = \sigma^2/a^2$. $\square$

**The lemma.** Let $\mu_i = \mathbb{E}[X_i]$ and $D_i = X_i - \mu_i$. Each product $D_i D_j$ has a finite mean, since $|D_i D_j| \le (D_i^2 + D_j^2)/2$.

1. Expand the square: $\mathrm{Var}(\sum_i X_i) = \mathbb{E}[(\sum_i D_i)^2] = \sum_i \mathbb{E}[D_i^2] + \sum_{i \ne j} \mathbb{E}[D_i D_j]$, by [linearity of expectation](/linearity-of-expectation/).
2. For $i \ne j$, $X_i$ and $X_j$ are independent, so $D_i$ and $D_j$ are independent, and $\mathbb{E}[D_i D_j] = \mathbb{E}[D_i]\,\mathbb{E}[D_j] = 0$. Under the weaker hypothesis, $\mathbb{E}[D_i D_j] = \mathbb{E}[X_i X_j] - \mu_i\mu_j = 0$ directly.
3. So $\mathrm{Var}(\sum_i X_i) = \sum_i \mathbb{E}[D_i^2] = \sum_i \mathrm{Var}(X_i)$. Only pairs of variables enter the expansion, so independence of pairs is all that the proof uses. $\square$

**The corollary.** By the lemma and $\mathrm{Var}(cZ) = c^2\,\mathrm{Var}(Z)$, $\mathrm{Var}(\bar X) = n\sigma^2/n^2 = \sigma^2/n$, and $\mathbb{E}[\bar X] = \mu$. Apply the theorem to $\bar X$ with $a = \varepsilon$. $\square$

**Cantelli.** Write $D = X - \mu$, so $\mathbb{E}[D] = 0$ and $\mathbb{E}[D^2] = \sigma^2$. Fix $u \ge 0$.

1. If $D \ge a$, then $D + u \ge a + u > 0$, so $(D + u)^2 \ge (a + u)^2$. Hence $\{D \ge a\} \subseteq \{(D + u)^2 \ge (a + u)^2\}$.
2. Markov's inequality on the nonnegative variable $(D + u)^2$ gives $\Pr(D \ge a) \le \mathbb{E}[(D + u)^2]/(a + u)^2 = (\sigma^2 + u^2)/(a + u)^2$, because $\mathbb{E}[D] = 0$.
3. Choose $u = \sigma^2/a$. The bound becomes $\dfrac{\sigma^2 + \sigma^4/a^2}{(a + \sigma^2/a)^2} = \dfrac{\sigma^2(a^2 + \sigma^2)/a^2}{(a^2 + \sigma^2)^2/a^2} = \dfrac{\sigma^2}{\sigma^2 + a^2}$.
4. The lower tail is the upper tail of $-X$, which has the same variance. $\square$

## Consequences

**Coin flips.** Let $X$ be the number of heads in $n$ fair flips, so $\mu = n/2$ and $\sigma^2 = n/4$. The table compares Chebyshev's two-sided bound with the exact two-sided [binomial](/binomial-distribution/) tail, and Cantelli's one-sided bound with the exact upper tail $\Pr(X - n/2 \ge d)$.

| $n$ | $d$ | Chebyshev $\frac{n/4}{d^2}$ | exact $\Pr(\lvert X - n/2\rvert \ge d)$ | Cantelli | exact $\Pr(X - n/2 \ge d)$ |
| --- | --- | --- | --- | --- | --- |
| 100 | 10 | 0.25 | 0.0569 | 0.2 | 0.0284 |
| 100 | 15 | 0.111 | 0.00352 | 0.1 | 0.00176 |
| 100 | 20 | 0.0625 | $7.85 \times 10^{-5}$ | 0.0588 | $3.93 \times 10^{-5}$ |
| 100 | 25 | 0.04 | $5.64 \times 10^{-7}$ | 0.0385 | $2.82 \times 10^{-7}$ |
| 1000 | 50 | 0.1 | 0.00173 | 0.0909 | 0.000865 |
| 1000 | 100 | 0.025 | $2.73 \times 10^{-10}$ | 0.0244 | $1.36 \times 10^{-10}$ |

At $d = 2\sigma$ (the rows $n = 100, d = 10$) Chebyshev is off by a factor of about 4. Further out the true one-sided tail is at most $e^{-2d^2/n}$ by the [Hoeffding inequality](/hoeffding-inequality/), while Chebyshev falls only like $1/d^2$. The [Chernoff bound](/chernoff-bound/) and the [binomial tail bounds](/binomial-tail-bounds/) capture the exponential decay. They need full independence, and Chebyshev does not.

**Sample size for estimating a proportion.** To estimate an unknown probability $p$ by the fraction $\bar X$ of successes in $n$ pairwise independent trials, so that $\Pr(|\bar X - p| \ge \varepsilon) \le \delta$, the corollary with $\sigma^2 = p(1-p) \le \frac14$ shows that
$$ n \ge \frac{1}{4\varepsilon^2\delta} $$
suffices. For $\varepsilon = 0.01$ and $\delta = 0.05$ this is $n = 50{,}000$. With full independence, the Hoeffding inequality needs only $n \ge \ln(2/\delta)/(2\varepsilon^2) = 18{,}445$. The difference grows as $\delta$ shrinks: Chebyshev pays $1/\delta$, Hoeffding pays $\ln(1/\delta)$.

**The median trick.** Chebyshev's dependence on $1/\delta$ can be repaired with independent repetition, as in the [median trick](/median-trick/). Use groups of $n_0 = 1/\varepsilon^2$ trials. By the corollary, the estimate of one group is off by $\varepsilon$ or more with probability at most $p(1-p)/(n_0\varepsilon^2) \le \frac14$. Take $m$ independent groups, $m$ odd, and output the median of the $m$ estimates. The median is above $p + \varepsilon$ only if at least $(m+1)/2$ estimates are above $p + \varepsilon$, and similarly below. So the median fails only if at least $(m+1)/2$ groups fail. The groups are independent and each fails with probability at most $\frac14$, so this probability is at most $\Pr(\mathrm{Bin}(m, \frac14) \ge (m+1)/2)$. For $\varepsilon = 0.01$ and $\delta = 10^{-6}$:

| method | trials |
| --- | --- |
| Chebyshev alone, $n = 1/(4\varepsilon^2\delta)$ | $2.5 \times 10^9$ |
| median of $m = 79$ groups of $10^4$ | $790{,}000$ |

The exact value $\Pr(\mathrm{Bin}(79, \frac14) \ge 40) = 8.65 \times 10^{-7}$ is below $10^{-6}$, and $m = 77$ gives $1.17 \times 10^{-6}$, which is above it. The number of groups grows like $\ln(1/\delta)$.

**Pairwise independent bits.** Take three independent fair bits $b_1, b_2, b_3$, and for each nonempty set $S \subseteq \{1, 2, 3\}$ let $Y_S$ be the XOR of the bits in $S$. This gives 7 bits $Y_S$, each fair, and any two of them are independent, but they are not independent as a set (Mitzenmacher and Upfal, Section 15.1.1). For their sum $X = \sum_S Y_S$, the lemma gives $\mathrm{Var}(X) = 7 \cdot \frac14 = \frac74$, the same as for 7 independent bits, and $\mu = \frac72$. Chebyshev gives $\Pr(|X - \frac72| \ge \frac72) \le \frac{7/4}{49/4} = \frac17 = 0.143$. The exact value is $\frac18 = 0.125$: when the seed is $000$ all 7 bits are 0, and for each other seed exactly 4 of the 7 bits are 1, so $X \in \{0, 4\}$. For 7 fully independent bits the same event, $X \in \{0, 7\}$, has probability $\frac{2}{128} = 0.0156$. Chebyshev is nearly tight here, and no bound with exponential decay can hold for these bits.

**Two-point sampling.** The same idea lets a randomized algorithm draw $t$ pairwise independent sample points from only two truly random numbers, and still reduce its error to $O(1/t)$ by Chebyshev (Motwani and Raghavan, Section 3.4). Full independence would give an error exponentially small in $t$, but would cost $t$ random numbers.

## Tightness

The constant cannot be improved for a single variable. Let $a \ge \sigma > 0$ and let $X$ take the value $\mu - a$ with probability $\sigma^2/(2a^2)$, the value $\mu + a$ with the same probability, and the value $\mu$ otherwise. Then $\mathbb{E}[X] = \mu$, $\mathrm{Var}(X) = a^2 \cdot \sigma^2/a^2 = \sigma^2$, and $\Pr(|X - \mu| \ge a) = \sigma^2/a^2$, which is equality. For $a < \sigma$ the bound exceeds 1, and the variable equal to $\mu \pm \sigma$ with probability $\frac12$ each has $\Pr(|X - \mu| \ge a) = 1$.

Cantelli's bound is also exact. For $a > 0$, let $X = \mu + a$ with probability $\sigma^2/(\sigma^2 + a^2)$ and $X = \mu - \sigma^2/a$ with probability $a^2/(\sigma^2 + a^2)$. The mean is $\mu$, the variance is $(a^2\sigma^2 + \sigma^4)/(\sigma^2 + a^2) = \sigma^2$, and $\Pr(X - \mu \ge a) = \sigma^2/(\sigma^2 + a^2)$.

The extremal variables put their mass at a few points far from the mean. For sums of many independent terms the bound is loose by a factor that grows without limit, as the table of coin flips shows. For sums of only pairwise independent terms it is close to the truth, as the example of the XOR bits shows.

### Pitfalls

- **The variance must be finite.** For a Pareto variable with $\Pr(X > x) = x^{-3/2}$ for $x \ge 1$, the mean is 3 and the variance is infinite. Chebyshev says nothing, and the sample mean converges slowly.
- **Halving the two-sided bound needs symmetry.** For an asymmetric variable, $\Pr(X - \mu \ge a) \le \sigma^2/(2a^2)$ can be false. With $\sigma = 1$ and $a = 2$, Cantelli's extremal variable above has $\Pr(X - \mu \ge 2) = \frac15$, while $\sigma^2/(2a^2) = \frac18$. Use Cantelli's inequality for one tail.
- **Variances of dependent terms do not add.** If $X_1 = \cdots = X_n = X$, then $\mathrm{Var}(\sum_i X_i) = n^2\,\mathrm{Var}(X)$, not $n\,\mathrm{Var}(X)$. The lemma needs the covariances of all pairs to vanish.
- **Pairwise independence is enough for Chebyshev, but not for Chernoff.** The XOR example has the right variance, and its tail is $\frac18$ where full independence gives $\frac{1}{64}$. Do not apply a Chernoff bound to pairwise independent hash values.
- **Small failure probabilities are expensive.** Chebyshev needs a number of samples proportional to $1/\delta$. To reach $\delta = 1/n^c$ use the median trick or a Chernoff bound, which need a number proportional to $\ln(1/\delta)$.
- **Bounds with $k \le 1$ are empty.** $\Pr(|X - \mu| \ge k\sigma) \le 1/k^2$ says nothing for $k \le 1$.

## History

Irénée-Jules Bienaymé first proved the inequality in 1853, and Pafnuty Chebyshev proved it more generally in 1867. Andrey Markov, a student of Chebyshev, gave another proof in his thesis of 1884. The one-sided form is due to Francesco Paolo Cantelli. In computer science, the use of Chebyshev's inequality with pairwise independent samples to save random bits is presented by Motwani and Raghavan, Section 3.4, and by Mitzenmacher and Upfal, Chapter 15.

## References
