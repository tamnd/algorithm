---
tag: R2EVPC
kind: theorem
slug: law-of-large-numbers
name: Law of large numbers
aliases:
- weak law of large numbers
- strong law of large numbers
area: foundations/probabilistic-analysis
level: intro
summary: The sample average of i.i.d. variables converges to the expected value.
prereqs: [random-variable, expected-value, variance, chebyshev-inequality, independent-random-variables]
see_also: [central-limit-theorem, hoeffding-inequality, chernoff-bound, monte-carlo-integration, median-trick, markov-inequality, concentration-of-measure]
sources:
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume 1, third edition
    locator: Chapter X, Laws of Large Numbers (the weak law with only a finite mean by truncation, the strong law, the Petersburg game); Chapter IX, Random Variables; Expectation (variance of a sum, Chebyshev's inequality)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 3.2, Variance and Moments of a Random Variable; Section 3.3, Chebyshev's Inequality; Section 4.2.3, Application, Estimating a Parameter; Section 11.1, The Monte Carlo Method; Section 15.2, Chebyshev's Inequality for Pairwise Independent Variables
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.3, Discrete random variables (variance, Chebyshev's inequality), and Section C.5, The tails of the binomial distribution
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 3, Moments and Deviations (Section 3.2, The Markov and Chebyshev Inequalities); Chapter 4, Tail Inequalities
  - url: "https://en.wikipedia.org/wiki/Law_of_large_numbers"
    locator: sections History (Bernoulli 1713, Poisson 1837, Khinchin 1929, Kolmogorov 1930 and 1933) and Limitation (the Cauchy distribution)
---

The law of large numbers says that the average of many [independent](/independent-random-variables/) copies of a [random variable](/random-variable/) gets close to its [expected value](/expected-value/). The weak law says that, for each fixed tolerance, the probability of a miss tends to 0; with a finite [variance](/variance/) it holds with the explicit bound $\sigma^2/(n\varepsilon^2)$ of [Chebyshev's inequality](/chebyshev-inequality/). The strong law says that the averages converge with probability 1. The law is the reason that Monte Carlo estimates, random sampling and repeated runs of a [randomized algorithm](/randomized-algorithm/) give answers you can trust.

## Statement

Let $X_1, X_2, \ldots$ be random variables on one [probability space](/probability-space/), and let $\bar X_n = \frac1n(X_1 + \cdots + X_n)$ be the sample mean of the first $n$ of them.

**Weak law, with finite variance (Chebyshev form).** Assume that the $X_i$ are pairwise independent, that each has the mean $\mathrm{E}[X_i] = \mu$, and that each has the variance $\mathrm{Var}[X_i] = \sigma^2 < \infty$. Then for each integer $n \ge 1$ and each real $\varepsilon > 0$,
$$ \Pr\bigl[\,|\bar X_n - \mu| \ge \varepsilon\,\bigr] \le \frac{\sigma^2}{n\varepsilon^2}. $$
So $\Pr[|\bar X_n - \mu| \ge \varepsilon] \to 0$ as $n \to \infty$, for each $\varepsilon > 0$. This is convergence in probability, $\bar X_n \to \mu$.

**Weak law, with finite mean only (Khinchin, 1929).** If the $X_i$ are independent and identically distributed (i.i.d.) and $\mathrm{E}[|X_1|] < \infty$, then $\Pr[|\bar X_n - \mu| \ge \varepsilon] \to 0$ for each $\varepsilon > 0$, where $\mu = \mathrm{E}[X_1]$. There is no rate in this form. Feller proves it by truncation in Chapter X.

**Strong law (Kolmogorov, 1930).** If the $X_i$ are i.i.d. and $\mathrm{E}[|X_1|] < \infty$, then
$$ \Pr\Bigl[\,\lim_{n\to\infty} \bar X_n = \mu\,\Bigr] = 1. $$
Kolmogorov also showed (1933) that for i.i.d. variables the finite mean is necessary: if $\mathrm{E}[|X_1|] = \infty$, the averages do not converge to a finite limit with probability 1. Below we prove the strong law under the extra hypothesis $\mathrm{E}[X_1^4] < \infty$.

The strong law implies the weak law. The converse fails: the weak law controls each $\bar X_n$ alone, and the strong law controls the whole path $\bar X_1, \bar X_2, \ldots$ at once.

## In plain words

Flip a fair coin many times and count the share of heads. After ten flips the share can be far from one half. After ten thousand flips it is almost always close to one half. The law of large numbers makes this exact: the average of many independent tries of the same random experiment settles near the true mean, and the chance of a large error shrinks as the number of tries grows.

The weak form says that for each error size you fix in advance, the chance of an error that large goes to zero. Its simple proof also says how fast. The strong form says that, on a single long run, the running average converges.

The law does not say that early luck is balanced by later bad luck. The coin has no memory. A lead of heads is not taken back; the many later flips dilute it.

## Proof

### The weak law, with finite variance

We use two facts.

**Chebyshev's inequality.** For a random variable $Y$ with finite variance and each $a > 0$, $\Pr[|Y - \mathrm{E}[Y]| \ge a] \le \mathrm{Var}[Y]/a^2$. *Proof.* The variable $Z = (Y - \mathrm{E}[Y])^2$ is non-negative with $\mathrm{E}[Z] = \mathrm{Var}[Y]$. The event $|Y - \mathrm{E}[Y]| \ge a$ is the event $Z \ge a^2$. By [Markov's inequality](/markov-inequality/), $\Pr[Z \ge a^2] \le \mathrm{E}[Z]/a^2$. $\square$

**The variance of the mean.** For any random variables with finite variance, $\mathrm{Var}[X_1 + \cdots + X_n] = \sum_i \mathrm{Var}[X_i] + 2\sum_{i<j}\mathrm{Cov}(X_i, X_j)$; the proof is on the page on [variance](/variance/). If $X_i$ and $X_j$ are independent, then $\mathrm{E}[X_iX_j] = \mathrm{E}[X_i]\,\mathrm{E}[X_j]$, so $\mathrm{Cov}(X_i, X_j) = 0$. This uses only the independence of the pair, so pairwise independence is enough. Hence $\mathrm{Var}[X_1 + \cdots + X_n] = n\sigma^2$.

*Proof of the weak law.* By [linearity of expectation](/linearity-of-expectation/), $\mathrm{E}[\bar X_n] = \frac1n \cdot n\mu = \mu$. Since $\mathrm{Var}[cY] = c^2\,\mathrm{Var}[Y]$, we get $\mathrm{Var}[\bar X_n] = \frac{1}{n^2}\cdot n\sigma^2 = \sigma^2/n$. Chebyshev's inequality with $Y = \bar X_n$ and $a = \varepsilon$ gives
$$ \Pr\bigl[\,|\bar X_n - \mu| \ge \varepsilon\,\bigr] \le \frac{\mathrm{Var}[\bar X_n]}{\varepsilon^2} = \frac{\sigma^2}{n\varepsilon^2}. $$
The right side tends to 0 as $n \to \infty$ for each fixed $\varepsilon > 0$. $\blacksquare$

The proof needs only that the $X_i$ have the same mean, have variances at most $\sigma^2$, and are pairwise uncorrelated. It does not need full independence or the same distribution.

### The strong law, with a finite fourth moment

We assume that the $X_i$ are i.i.d. with $K = \mathrm{E}[(X_1 - \mu)^4] < \infty$.

**Lemma (first Borel-Cantelli lemma).** If $A_1, A_2, \ldots$ are events with $\sum_n \Pr[A_n] < \infty$, then with probability 1 only finitely many $A_n$ occur. *Proof.* The event "infinitely many $A_n$ occur" is a subset of $\bigcup_{n \ge m} A_n$ for each $m$. By the [union bound](/union-bound/) its probability is at most $\sum_{n \ge m}\Pr[A_n]$. This tail of a convergent series tends to 0 as $m \to \infty$, so the probability is 0. $\square$

*Proof of the strong law.* Let $Y_i = X_i - \mu$, so the $Y_i$ are i.i.d. with $\mathrm{E}[Y_i] = 0$, $\mathrm{E}[Y_i^2] = \sigma^2$ and $\mathrm{E}[Y_i^4] = K$. Let $T_n = Y_1 + \cdots + Y_n = n(\bar X_n - \mu)$.

1. *The fourth moment of $T_n$.* Expand $T_n^4 = \sum_{i,j,k,l} Y_iY_jY_kY_l$ over all $n^4$ ordered 4-tuples of indices. If one index of a tuple appears exactly once, say $i$, then $Y_i$ is independent of the product of the other three factors, so the expectation of the term is $\mathrm{E}[Y_i] \cdot \mathrm{E}[\cdots] = 0$. The tuples with no index that appears exactly once are of two types. The $n$ tuples $(i,i,i,i)$ give $\mathrm{E}[Y_i^4] = K$ each. The tuples with two distinct indices, each twice, number $3n(n-1)$: there are 3 ways to split the four positions into two pairs, and $n(n-1)$ ways to give the pairs distinct indices. Each gives $\mathrm{E}[Y_i^2]\,\mathrm{E}[Y_j^2] = \sigma^4$ by independence. So $\mathrm{E}[T_n^4] = nK + 3n(n-1)\sigma^4$.
2. *A bound by $K$.* The variance of $Y_1^2$ is $K - \sigma^4 \ge 0$, so $\sigma^4 \le K$. Hence $\mathrm{E}[T_n^4] \le nK + 3n^2K \le 4n^2K$.
3. *A summable tail.* Fix $\varepsilon > 0$ and let $A_n$ be the event $|\bar X_n - \mu| \ge \varepsilon$, which is the event $T_n^4 \ge n^4\varepsilon^4$. By Markov's inequality, $\Pr[A_n] \le \mathrm{E}[T_n^4]/(n^4\varepsilon^4) \le 4K/(n^2\varepsilon^4)$. Since $\sum_n 1/n^2$ converges, $\sum_n \Pr[A_n] < \infty$.
4. *Borel-Cantelli.* By the lemma, with probability 1 only finitely many $A_n$ occur. So, with probability 1, $|\bar X_n - \mu| < \varepsilon$ for all large $n$.
5. *All tolerances at once.* Let $B_k$ be the event that $|\bar X_n - \mu| \ge 1/k$ for infinitely many $n$. Step 4 with $\varepsilon = 1/k$ gives $\Pr[B_k] = 0$. The averages fail to converge to $\mu$ exactly when some $B_k$ occurs, and by the union bound over the countably many $k$, $\Pr[\bigcup_k B_k] = 0$. $\blacksquare$

The proof with only $\mathrm{E}[|X_1|] < \infty$ needs truncation and a finer argument; see Feller, Chapter X.

## Consequences

### Monte Carlo estimation of a probability

An algorithm wants $p = \Pr[E]$ for some event $E$ that it can sample, for example the chance that a random input makes a heuristic fail. It draws $n$ independent samples and returns the fraction $\hat p$ of samples in which $E$ occurs. Each sample is an [indicator variable](/indicator-random-variable/) with mean $p$ and variance $p(1-p) \le 1/4$, so $\hat p$ is the sample mean of [Bernoulli trials](/bernoulli-trials/). This is the base of [Monte Carlo integration](/monte-carlo-integration/) and of [random sampling](/random-sampling/).

The weak law in Chebyshev form gives $\Pr[|\hat p - p| \ge \varepsilon] \le 1/(4n\varepsilon^2)$, so $n \ge 1/(4\varepsilon^2\delta)$ samples make the failure probability at most $\delta$. For bounded samples, [Hoeffding's inequality](/hoeffding-inequality/) gives $\Pr[|\hat p - p| \ge \varepsilon] \le 2e^{-2n\varepsilon^2}$, so $n \ge \ln(2/\delta)/(2\varepsilon^2)$ is enough. With the error $\varepsilon = 0.01$:

| failure probability $\delta$ | samples by Chebyshev | samples by Hoeffding |
| --- | --- | --- |
| $0.05$ | 50000 | 18445 |
| $10^{-6}$ | 2500000000 | 72544 |

Chebyshev's bound grows like $1/\delta$; the exponential bound grows like $\ln(1/\delta)$. The [central limit theorem](/central-limit-theorem/) explains the true size of the error, but it gives an approximation, not a bound.

### An estimate of $\pi$

Draw $n$ points independently and uniformly in the unit square, and let $\hat p$ be the fraction of points with $x^2 + y^2 \le 1$. Then $\mathrm{E}[\hat p] = \pi/4 = 0.785398\ldots$, and $4\hat p$ estimates $\pi$. Each indicator has the variance $\frac\pi4(1 - \frac\pi4) = 0.168548\ldots$, so $\mathrm{Var}[4\hat p] = 16 \cdot 0.168548/n$. For $n = 10^6$ the standard deviation of $4\hat p$ is $0.001642$. Chebyshev's inequality gives $\Pr[|4\hat p - \pi| \ge 0.01] \le 0.02697$. Hoeffding's inequality, applied to $\hat p$ with the error $0.0025$, gives the much smaller bound $2e^{-12.5} = 7.45 \times 10^{-6}$. The error shrinks only like $1/\sqrt n$: each new correct decimal digit costs 100 times as many points.

### The median trick

When the samples are not bounded and only a bound on the variance is known, as in the [AMS sketch](/ams-sketch/), Chebyshev's inequality is the usual tool for one average. The [median trick](/median-trick/) then turns its $1/\delta$ cost into $\ln(1/\delta)$. Take $k$ independent groups. Make each group large enough that its mean misses by $\varepsilon$ or more with probability at most $1/4$; for the coin estimate above with $\varepsilon = 0.01$, that is $1/(4 \cdot 10^{-4} \cdot \frac14) = 10000$ samples. Return the median of the $k$ group means. If the median misses, then at least $(k+1)/2$ of the group means miss on the same side, and the number of misses is a sum of $k$ independent indicators with mean at most $1/4$. By Hoeffding's inequality, this has probability at most $e^{-2k(1/4)^2} = e^{-k/8}$. For $\delta = 10^{-6}$ this bound asks for $k = 111$ groups; the exact binomial tail shows that $k = 79$ groups already give $\Pr[\mathrm{Bin}(79, \frac14) \ge 40] = 8.6 \times 10^{-7}$. That is 790000 samples in total, against $2.5 \times 10^9$ by Chebyshev's inequality alone.

### Repeated runs of a randomized algorithm

The running time of a [Las Vegas algorithm](/las-vegas-algorithm/) on a fixed input is a random variable. Over many independent runs, the average time per run tends to the expected time, by the strong law. This is why the expected running time of [randomized quicksort](/randomized-quicksort/), about $2n\ln n$ comparisons, is also the long-run average that a benchmark sees.

## Tightness

**The rate of Chebyshev's bound.** The bound $\sigma^2/(n\varepsilon^2)$ uses only the variance. For bounded variables the true tail falls exponentially in $n$, as the [Chernoff bound](/chernoff-bound/) and Hoeffding's inequality show. For a fair coin and $\varepsilon = 0.01$:

| $n$ | exact $\Pr[\lvert\bar X_n - \frac12\rvert \ge 0.01]$ | Chebyshev bound | Hoeffding bound |
| --- | --- | --- | --- |
| 1000 | 0.548 | 2.5 | 1.64 |
| 10000 | 0.0466 | 0.25 | 0.271 |
| 100000 | $2.59 \times 10^{-10}$ | 0.025 | $4.12 \times 10^{-9}$ |

So the factor $1/n$ is far from the truth for coins. Chebyshev's inequality itself cannot be improved for a single variable: for $a \ge \sigma$, the variable that takes the values $\mu - a$ and $\mu + a$ with probability $\sigma^2/(2a^2)$ each, and $\mu$ otherwise, has the variance $\sigma^2$ and meets the bound with equality.

**Without a finite mean the law fails.** If $X_1, X_2, \ldots$ are i.i.d. with the standard Cauchy distribution, with density $1/(\pi(1+x^2))$, then $\mathrm{E}[|X_1|] = \infty$, and $\bar X_n$ has the same standard Cauchy distribution for every $n$. So $\Pr[|\bar X_n| \ge 1] = 1 - \frac2\pi\arctan 1 = \frac12$ for each $n$, and averaging does not help at all. Feller, Chapter X, treats a discrete example, the Petersburg game, whose payoff has an infinite mean.

**Without independence the law fails.** Let $X_1$ be a fair coin flip in $\{0, 1\}$ and let $X_i = X_1$ for each $i$. Each $X_i$ has the mean $\frac12$ and the variance $\frac14$, but $\bar X_n = X_1$, so $|\bar X_n - \frac12| = \frac12$ always. In the proof, the covariances are $\frac14$ instead of 0, and $\mathrm{Var}[\bar X_n] = \frac14$ does not shrink. A generator of pseudo-random numbers with correlated outputs breaks a Monte Carlo estimate in the same way.

**Weak does not give strong for free.** The strong law needs more than the bound $\sigma^2/(n\varepsilon^2)$: the series $\sum_n 1/n$ diverges, so step 3 of the strong proof does not work with the second moment alone. The fourth moment gives the summable bound $1/n^2$.

### Pitfalls

- **The gambler's fallacy.** After ten heads in a row, the next flip of a fair coin is still heads with probability $\frac12$. The law does not push the count back. The surplus of heads stays; it is the share that converges, because the surplus is divided by a growing $n$.
- **The sum does not converge.** $\bar X_n - \mu \to 0$, but $S_n - n\mu$ does not. For a fair coin, $\mathrm{E}[|S_n - n/2|]$ is 3.98 at $n = 100$, 39.89 at $n = 10^4$ and 398.94 at $n = 10^6$: it grows like $\sqrt{n/(2\pi)}$. The ratio $\mathrm{E}[|S_n - n/2|]/n$ falls like $1/\sqrt n$, from 0.0398 to 0.000399.
- **The limit says nothing about a fixed $n$.** Convergence in probability alone gives no sample size. For a guarantee, use the explicit Chebyshev form or an exponential tail bound, with the constants.
- **The variance must be known or bounded.** The bound $\sigma^2/(n\varepsilon^2)$ uses the true variance. Plugging in the sample variance from the same data gives an estimate, not a bound. For an indicator, $\sigma^2 \le \frac14$ is a safe bound.
- **Each sample must have the same mean.** An average of samples from a stream whose distribution drifts converges, if at all, to the average of the means, not to any one mean.

## History

Jacob Bernoulli proved the first law of large numbers, for the share of successes in repeated trials, in his Ars Conjectandi, published in 1713 after his death. Poisson gave the result the name "law of large numbers" in 1837. Chebyshev's inequality gave the short proof of the weak law for variables with finite variance. Khinchin showed in 1929 that a finite mean suffices for the weak law of i.i.d. variables. Kolmogorov proved the strong law for i.i.d. variables with a finite mean in 1930, and in 1933 showed that the finite mean is also necessary.

## References
