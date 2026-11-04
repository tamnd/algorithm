---
tag: F277W6
kind: theorem
slug: central-limit-theorem
name: Central limit theorem
aliases:
- CLT
area: foundations/probabilistic-analysis
level: intro
summary: Normalized sums of i.i.d. variables with finite variance converge in distribution to the normal distribution.
prereqs: [random-variable, expected-value, variance, independent-random-variables, law-of-large-numbers]
see_also: [binomial-distribution, chernoff-bound, hoeffding-inequality, expected-number-of-inversions, moment-generating-function, quicksort-expected-running-time, concentration-of-measure]
sources:
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume 1, third edition
    locator: Chapter VII, The Normal Approximation to the Binomial Distribution (the de Moivre-Laplace theorem); Chapter X, Laws of Large Numbers (the central limit theorem for identically distributed and for non-identical variables)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 9.1, The Normal Distribution; Section 9.2, Limit of the Binomial Distribution; Section 9.3, The Central Limit Theorem
  - book: isbn:9781118122372
    title: Patrick Billingsley, Probability and Measure, Anniversary edition
    locator: Section 26, Characteristic Functions (the Taylor bound and the continuity theorem); Section 27, The Central Limit Theorem (identically distributed summands, the Lindeberg and Lyapounov theorems)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1, Inversions (the inversion table, and the mean and variance of the number of inversions)
  - paper: "Uwe Rösler, A limit theorem for 'Quicksort', RAIRO Informatique Théorique et Applications 25(1) (1991), pages 85 to 100"
    locator: the limit law of the number of comparisons of quicksort
  - url: "https://en.wikipedia.org/wiki/Central_limit_theorem"
    locator: section History (de Moivre 1733, Laplace 1812, Lyapunov 1901, Lindeberg, Pólya's name of 1920)
  - url: "https://en.wikipedia.org/wiki/Berry%E2%80%93Esseen_theorem"
    locator: the i.i.d. statement, the bound C < 0.4748 (Shevtsova 2011) and the lower bound C >= 0.40973 (Esseen 1956)
---

The central limit theorem says that the sum of many [independent](/independent-random-variables/), identically distributed random variables with finite [variance](/variance/), after you subtract its mean and divide by its standard deviation, has a distribution close to the standard normal distribution. The [law of large numbers](/law-of-large-numbers/) says that the average converges to the mean; the central limit theorem says how the error is spread: it is about $\sigma/\sqrt n$ in size, with a bell-shaped law. It explains the shape of the [binomial distribution](/binomial-distribution/), the sample sizes of Monte Carlo estimates, and the distribution of many costs of algorithms, such as the number of [inversions](/inversion/) of a random permutation.

## Statement

Let $\Phi(x) = \frac{1}{\sqrt{2\pi}}\int_{-\infty}^{x} e^{-u^2/2}\,du$ be the distribution function of the standard normal distribution $N(0,1)$.

**Theorem (Lindeberg-Lévy).** Let $X_1, X_2, \ldots$ be independent and identically distributed (i.i.d.) random variables with $\mathrm{E}[X_1] = \mu$ and $0 < \mathrm{Var}[X_1] = \sigma^2 < \infty$. Let $S_n = X_1 + \cdots + X_n$ and
$$ Z_n = \frac{S_n - n\mu}{\sigma\sqrt n}. $$
Then for each real $x$,
$$ \lim_{n\to\infty}\Pr[Z_n \le x] = \Phi(x), $$
and the convergence is uniform in $x$: $\sup_{x\in\mathbb R}\,|\Pr[Z_n \le x] - \Phi(x)| \to 0$.

Equivalent forms: $\sqrt n(\bar X_n - \mu)/\sigma$ tends in distribution to $N(0,1)$, and $\Pr[a \le Z_n \le b] \to \Phi(b) - \Phi(a)$ for all $a \le b$. The special case of [Bernoulli trials](/bernoulli-trials/) is the de Moivre-Laplace theorem.

**Lindeberg's theorem.** The variables need not have the same distribution. Let $X_1, X_2, \ldots$ be independent with means $\mu_k$ and finite variances $\sigma_k^2$, and let $s_n^2 = \sigma_1^2 + \cdots + \sigma_n^2 > 0$. If for each $\varepsilon > 0$
$$ \lim_{n\to\infty}\frac{1}{s_n^2}\sum_{k=1}^{n}\mathrm{E}\bigl[(X_k - \mu_k)^2\, I\{|X_k - \mu_k| > \varepsilon s_n\}\bigr] = 0, $$
then $(S_n - \sum_{k\le n}\mu_k)/s_n$ tends in distribution to $N(0,1)$. This is cited from Billingsley, Section 27; we use it in the example of inversions.

**Berry-Esseen bound.** If, in addition, $\rho = \mathrm{E}[|X_1 - \mu|^3] < \infty$, then there is an absolute constant $C$ with
$$ \sup_{x}\,\bigl|\Pr[Z_n \le x] - \Phi(x)\bigr| \le \frac{C\rho}{\sigma^3\sqrt n} \quad \text{for each } n \ge 1. $$
The best known value is $C < 0.4748$ (Shevtsova, 2011), and $C \ge 0.40973$ is necessary (Esseen, 1956).

## In plain words

Add up many small random amounts that do not depend on each other. The total is random too. The central limit theorem says that the shape of its distribution is almost always the same bell curve, whatever the shape of the small amounts was, as long as none of them is wildly large. Only two numbers matter: the mean of the total and its spread.

The spread grows like the square root of the number of terms, not like the number itself. So with a hundred times more coin flips, the typical gap between the count of heads and half the flips grows only ten times.

The bell curve is good for questions near the center, such as "is the count within two spreads of the mean". It is bad for questions about rare events far in the tail. For those, use a tail bound.

## Proof

We prove the Lindeberg-Lévy theorem with characteristic functions. The proof uses three standard facts of Fourier analysis, which we cite from Billingsley, Section 26.

- **(F1)** For each real $x$, $|e^{ix} - 1 - ix + x^2/2| \le \min(|x|^3/6,\ x^2)$.
- **(F2)** The characteristic function of $N(0,1)$ is $e^{-t^2/2}$.
- **(F3) Continuity theorem.** If $\mathrm{E}[e^{itZ_n}] \to \mathrm{E}[e^{itZ}]$ for each real $t$, then $\Pr[Z_n \le x] \to \Pr[Z \le x]$ at each $x$ where the distribution function of $Z$ is continuous.

**Step 1: reduce to mean 0 and variance 1.** Let $Y_k = (X_k - \mu)/\sigma$. The $Y_k$ are i.i.d. with $\mathrm{E}[Y_k] = 0$, $\mathrm{E}[Y_k^2] = 1$, and $Z_n = (Y_1 + \cdots + Y_n)/\sqrt n$. Let $\varphi(t) = \mathrm{E}[e^{itY_1}]$.

**Step 2: $\varphi(t) = 1 - t^2/2 + o(t^2)$ as $t \to 0$.** Apply (F1) with $x = tY_1$ and take expectations. Since $\mathrm{E}[Y_1] = 0$ and $\mathrm{E}[Y_1^2] = 1$,
$$ \Bigl|\varphi(t) - 1 + \frac{t^2}{2}\Bigr| \le \mathrm{E}\Bigl[\min\Bigl(\frac{|t|^3|Y_1|^3}{6},\ t^2Y_1^2\Bigr)\Bigr] = t^2\,\mathrm{E}\Bigl[\min\Bigl(\frac{|t|\,|Y_1|^3}{6},\ Y_1^2\Bigr)\Bigr]. $$
The variable inside the last expectation is at most $Y_1^2$, which has a finite mean, and it tends to 0 pointwise as $t \to 0$. By dominated convergence its expectation tends to 0. So the error is $o(t^2)$. This step uses only $\mathrm{E}[Y_1^2] < \infty$; no third moment is needed.

**Step 3: a product lemma.** If $z_1, \ldots, z_n$ and $w_1, \ldots, w_n$ are complex numbers of modulus at most 1, then $|z_1\cdots z_n - w_1\cdots w_n| \le \sum_k |z_k - w_k|$. *Proof by induction on $n$.* The case $n = 1$ is an equality. For $n \ge 2$, write $z_1\cdots z_n - w_1\cdots w_n = z_1(z_2\cdots z_n - w_2\cdots w_n) + (z_1 - w_1)w_2\cdots w_n$. The moduli of $z_1$ and of $w_2\cdots w_n$ are at most 1, and the induction hypothesis bounds the first bracket. $\square$

**Step 4: the characteristic function of $Z_n$.** Fix $t$. By independence, the expectation of a product of functions of the $Y_k$ is the product of the expectations, so
$$ \mathrm{E}[e^{itZ_n}] = \prod_{k=1}^n \mathrm{E}[e^{i(t/\sqrt n)Y_k}] = \varphi(t/\sqrt n)^n. $$
Let $w_n = 1 - t^2/(2n)$. For $n \ge t^2/4$ we have $-1 \le w_n \le 1$, and $|\varphi| \le 1$ always. Step 3 with all $z_k = \varphi(t/\sqrt n)$ and all $w_k = w_n$ gives
$$ \bigl|\varphi(t/\sqrt n)^n - w_n^n\bigr| \le n\,\bigl|\varphi(t/\sqrt n) - 1 + t^2/(2n)\bigr|. $$
By Step 2, the right side is $n \cdot o(t^2/n)$, which tends to 0 as $n \to \infty$. Also $w_n^n = (1 - t^2/(2n))^n \to e^{-t^2/2}$. So $\mathrm{E}[e^{itZ_n}] \to e^{-t^2/2}$ for each real $t$.

**Step 5: convergence of the distribution functions.** By (F2) the limit is the characteristic function of $N(0,1)$. Its distribution function $\Phi$ is continuous everywhere, so by (F3), $\Pr[Z_n \le x] \to \Phi(x)$ for each real $x$.

**Step 6: the convergence is uniform.** Let $F_n(x) = \Pr[Z_n \le x]$ and fix $\varepsilon > 0$. Since $\Phi$ is continuous and increases from 0 to 1, there are points $x_0 < x_1 < \cdots < x_m$ with $\Phi(x_0) < \varepsilon$, $\Phi(x_m) > 1 - \varepsilon$, and $\Phi(x_{j+1}) - \Phi(x_j) < \varepsilon$ for each $j$. By Step 5 there is an $N$ such that $|F_n(x_j) - \Phi(x_j)| < \varepsilon$ for all $j$ and all $n \ge N$. Take $n \ge N$ and any $x$.
- If $x_j \le x \le x_{j+1}$, then since $F_n$ and $\Phi$ are non-decreasing, $F_n(x) \le F_n(x_{j+1}) < \Phi(x_{j+1}) + \varepsilon < \Phi(x) + 2\varepsilon$, and $F_n(x) \ge F_n(x_j) > \Phi(x_j) - \varepsilon > \Phi(x) - 2\varepsilon$.
- If $x < x_0$, then $0 \le F_n(x) \le F_n(x_0) < 2\varepsilon$ and $0 \le \Phi(x) < \varepsilon$, so $|F_n(x) - \Phi(x)| < 2\varepsilon$. The case $x > x_m$ is symmetric.

So $\sup_x |F_n(x) - \Phi(x)| < 2\varepsilon$ for all $n \ge N$. $\blacksquare$

When the [moment generating function](/moment-generating-function/) of $X_1$ is finite near 0, the same computation works with $\mathrm{E}[e^{tZ_n}] \to e^{t^2/2}$ in place of the characteristic function, and a continuity theorem for moment generating functions. The proof above needs no such hypothesis.

## Consequences

### Coin flips and the binomial distribution

The number of heads in $n$ fair flips is $S_n \sim \mathrm{Bin}(n, \frac12)$, with mean $n/2$ and standard deviation $\sqrt n/2$. Since $S_n$ takes only integer values, the normal approximation is better with the continuity correction: $\Pr[S_n \le k] \approx \Phi((k + \frac12 - n/2)/(\sqrt n/2))$.

| event | exact | normal, with correction | normal, without correction |
| --- | --- | --- | --- |
| $n = 100$: $45 \le S \le 55$ | 0.72875 | 0.72867 | 0.68269 |
| $n = 1000$: $S \ge 530$ | 0.03101 | 0.03104 | 0.02889 |
| $n = 1000$: $S \ge 550$ | 0.000865 | 0.000872 | 0.000783 |
| $n = 1000$: $S \ge 600$ | $1.364 \times 10^{-10}$ | $1.558 \times 10^{-10}$ | $1.270 \times 10^{-10}$ |

Near the center the approximation is accurate to about 4 decimal places at $n = 100$.

### Sample sizes for Monte Carlo estimates

To estimate a probability $p$ to within $\pm\varepsilon$, the theorem suggests that $\hat p$ is about normal with standard deviation $\sqrt{p(1-p)/n} \le 1/(2\sqrt n)$. With $\Phi(1.96) = 0.975$, the choice $n = 1.96^2/(4\varepsilon^2)$ gives a miss probability of about $0.05$. For $\varepsilon = 0.01$ this is $n = 9604$, against the 18445 samples that [Hoeffding's inequality](/hoeffding-inequality/) needs and the 50000 that Chebyshev's inequality needs (see the [law of large numbers](/law-of-large-numbers/)). The number 9604 is an approximation, not a guarantee: the theorem holds in the limit and says nothing exact about a fixed $n$. The Berry-Esseen bound makes it exact up to an additive error of at most $0.4748\,\rho/(\sigma^3\sqrt n)$.

### The number of inversions of a random permutation

Let $I_n$ be the number of [inversions](/inversion/) of a uniformly random permutation of $n$ distinct keys. It is the number of shifts of [insertion sort](/insertion-sort/) and the number of swaps of [bubble sort](/bubble-sort/). By the [inversion table](/inversion-table/) (Knuth, Section 5.1.1), each permutation corresponds to exactly one sequence $(b_1, \ldots, b_n)$ with $0 \le b_j \le n - j$, and $I_n = b_1 + \cdots + b_n$. A uniform permutation gives a uniform sequence, so the $b_j$ are independent and $b_j$ is uniform on $\{0, \ldots, n-j\}$. Renamed, $I_n$ has the distribution of $Y_1 + \cdots + Y_n$, where the $Y_k$ are independent and $Y_k$ is uniform on $\{0, \ldots, k-1\}$. So
$$ \mathrm{E}[I_n] = \sum_{k=1}^n \frac{k-1}{2} = \frac{n(n-1)}{4}, \qquad \mathrm{Var}[I_n] = \sum_{k=1}^n \frac{k^2-1}{12} = \frac{n(n-1)(2n+5)}{72}. $$
The variance uses the sum rule for independent variables from the page on [variance](/variance/) and $\mathrm{Var}[Y_k] = (k^2-1)/12$. The mean is also derived on the page on the [expected number of inversions](/expected-number-of-inversions/).

The $Y_k$ do not have the same distribution, so we use Lindeberg's theorem. Each $|Y_k - \mathrm{E}[Y_k]| \le (k-1)/2 < n$, and $s_n^2 = n(n-1)(2n+5)/72$ grows like $n^3/36$. For each $\varepsilon > 0$ there is an $N$ with $\varepsilon s_n > n$ for $n \ge N$, and then each indicator in Lindeberg's condition is 0. So the condition holds, and $(I_n - n(n-1)/4)/s_n$ tends in distribution to $N(0, 1)$.

The exact distribution, computed by convolving the uniform distributions, shows how fast this happens. Here $F$ is the distribution function of $I_n$, and the normal approximation uses the continuity correction.

| $n$ | mean | standard deviation | $\sup_x \lvert F(x) - \text{normal}\rvert$ | $\Pr[I_n \le \text{mean} - \text{sd}]$ | normal value |
| --- | --- | --- | --- | --- | --- |
| 10 | 22.5 | 5.590 | 0.0050 | 0.1456 | 0.1416 |
| 20 | 95 | 15.411 | 0.0025 | 0.1594 | 0.1573 |
| 50 | 612.5 | 59.774 | 0.00099 | 0.1586 | 0.1577 |

So the number of swaps of insertion sort on random input is $n^2/4 \pm O(n^{3/2})$, and for large $n$ about 68 percent of inputs fall within one standard deviation of the mean.

### Where the theorem does not apply

Not every cost of a randomized algorithm is asymptotically normal. The number of comparisons $C_n$ of [randomized quicksort](/randomized-quicksort/) has mean $2n\ln n + O(n)$ and standard deviation of order $n$, but $(C_n - \mathrm{E}[C_n])/n$ converges to a limit law that is not normal (Rösler, 1991). The reason is that the large terms of the recursion, the sizes of the first few partitions, are not small compared with the total. The analysis of the mean is on the page on [quicksort's expected running time](/quicksort-expected-running-time/).

## Tightness

**The rate $1/\sqrt n$ cannot be improved.** For a fair coin, $S_n$ is integer-valued, so $\Pr[Z_n \le 0] = \Pr[S_n \le n/2] = \frac12 + \frac12\Pr[S_n = n/2]$ for even $n$. By [Stirling's approximation](/stirling-approximation/), $\Pr[S_n = n/2] = \binom{n}{n/2}2^{-n} \sim \sqrt{2/(\pi n)}$, so the error at $x = 0$ is about $1/\sqrt{2\pi n}$. At $n = 100$ it is 0.039795 against $1/\sqrt{200\pi} = 0.039894$; at $n = 10000$ it is 0.0039893 against 0.0039894. For the coin, $\rho/\sigma^3 = (1/8)/(1/8) = 1$, so the Berry-Esseen bound at $n = 100$ is below $0.04748$, and the true largest error is at least 0.0398. A jump of a lattice distribution always forces an error of the order $1/\sqrt n$.

**Finite variance is needed.** If the $X_i$ are i.i.d. standard Cauchy, then $S_n/n$ has the standard Cauchy distribution for every $n$, so $S_n/\sqrt n = \sqrt n\,(S_n/n)$ spreads out without limit and no normalization by $\sqrt n$ gives a normal limit. The characteristic function of the Cauchy law is $e^{-|t|}$, which has no expansion $1 - t^2/2 + o(t^2)$, so Step 2 fails.

**The tails are wrong far from the center.** The theorem controls the absolute error $|\Pr[Z_n \le x] - \Phi(x)|$, not the relative error of a tiny tail. For $n = 1000$ fair flips, the normal value of $\Pr[S \ge 700]$ is $8.46 \times 10^{-37}$, about 10 times the exact value $8.83 \times 10^{-38}$; for $\Pr[S \ge 750]$ it is $2.14 \times 10^{-56}$, about 318 times the exact $6.74 \times 10^{-59}$. For a skewed variable the error goes the other way. For $S \sim \mathrm{Bin}(1000, 0.01)$, with mean 10, the exact $\Pr[S \ge 25]$ is $4.20 \times 10^{-5}$ and the normal value is $2.03 \times 10^{-6}$, about 21 times too small; for $\Pr[S \ge 30]$ the exact value $2.06 \times 10^{-7}$ is 718 times the normal value. For rare events, such as the largest load of a hash bucket, use a [Chernoff bound](/chernoff-bound/): for $\Pr[S \ge 600]$ with $n = 1000$ fair flips, it gives the guaranteed bound $1.80 \times 10^{-9}$, and Hoeffding's inequality gives $2.06 \times 10^{-9}$.

### Pitfalls

- **Approximation is not a bound.** "About normal" gives no guarantee at a fixed $n$. For a proof, use the Berry-Esseen bound with its constant, or a tail bound such as [Hoeffding's inequality](/hoeffding-inequality/).
- **The continuity correction.** For an integer-valued sum, compare $\Pr[S \le k]$ with $\Phi$ at $k + \frac12$, not at $k$. At $n = 100$, omitting it changes the value of $\Pr[45 \le S \le 55]$ from 0.7287 to 0.6827.
- **Dependence.** The theorem needs independence or a substitute (martingale and mixing versions exist). A sum of identical copies, $S_n = nX_1$, keeps the shape of $X_1$ for every $n$.
- **Small means.** For $\mathrm{Bin}(n, p)$ with $np$ small, the law is skewed and close to a [Poisson distribution](/poisson-distribution/), and the normal approximation is poor even near the center.
- **Normal does not mean bounded.** A normal limit says nothing about the maximum of the cost. The worst case of insertion sort is $n(n-1)/2$ swaps, far beyond the mean plus a few standard deviations.

## History

Abraham de Moivre found the normal approximation to the number of heads in many flips of a fair coin in 1733. Laplace extended it to the binomial distribution with any success probability in his Théorie analytique des probabilités of 1812; Feller, Chapter VII, gives this de Moivre-Laplace theorem. Lyapunov proved a general form for independent variables in 1901, under a condition on higher moments. Lindeberg proved the theorem under his weaker condition in 1922, and Lévy also contributed to the general theory. Pólya named it the central limit theorem ("zentraler Grenzwertsatz") in 1920. Berry (1941) and Esseen (1942) independently proved the bound on the rate that carries both names.

## References
