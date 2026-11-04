---
tag: EEZKV7
kind: theorem
slug: binomial-tail-bounds
name: Tails of the binomial distribution
area: foundations/probabilistic-analysis
level: core
summary: For X ~ Bin(n, p) and k = an above the mean, the tail P(X >= k) lies between exp(-n D(a||p))/(n+1) and exp(-n D(a||p)), where D is the relative entropy; simpler bounds follow from it.
prereqs: [binomial-distribution, chernoff-bound, binomial-coefficient-bounds, shannon-entropy]
see_also: [chernoff-bound, hoeffding-inequality, chebyshev-inequality, union-bound, stirling-approximation, central-limit-theorem, binary-entropy-function, balls-into-bins]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 4, Section 4.2 (Chernoff bounds for sums of Poisson trials); Chapter 10, Entropy, Randomness, and Information (entropy and binomial coefficients)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition
    locator: Chapter 11, Information Theory and Statistics, Section 11.1 (the method of types, the size of a type class) and Section 11.4 (large deviation theory)
  - paper: doi:10.1080/01621459.1963.10500830
    title: Wassily Hoeffding, Probability inequalities for sums of bounded random variables, Journal of the American Statistical Association 58(301), 1963
    locator: pages 13 to 30, Theorem 1 (the relative entropy bound for variables in [0, 1])
  - book: isbn:9780521884273
    title: Devdatt P. Dubhashi and Alessandro Panconesi, Concentration of Measure for the Analysis of Randomized Algorithms
    locator: Chapter 1, Sections 1.2 (the binomial distribution) and 1.3 (the Chernoff bound)
  - paper: doi:10.1214/aoms/1177729330
    title: Herman Chernoff, A measure of asymptotic efficiency for tests of a hypothesis based on the sum of observations, Annals of Mathematical Statistics 23(4), 1952
    locator: pages 493 to 507
---

For a [binomial](/binomial-distribution/) variable $X \sim \mathrm{Bin}(n, p)$ and a level $k = an$ above the mean, the tail $\Pr[X \ge k]$ is $e^{-nD(a\|p)}$ up to a factor between $1/(n+1)$ and $1$, where $D(a\|p)$ is the relative entropy of two coins. So the tail falls exponentially in $n$, at a rate that is known exactly. The other usual estimates, the [Chernoff bound](/chernoff-bound/), [Hoeffding's inequality](/hoeffding-inequality/), the bound $\binom{n}{k}p^k$ and the ratio bound, are weaker forms of this one, and each has its own range where it is close to the truth.

## Statement

Let $n \ge 1$, $0 < p < 1$ and $X \sim \mathrm{Bin}(n, p)$, so $\Pr[X = j] = \binom{n}{j}p^j(1-p)^{n-j}$ for $j = 0, \ldots, n$. The exact tail is
$$ \Pr[X \ge k] = \sum_{j=k}^{n}\binom{n}{j}p^j(1-p)^{n-j}. $$
For $a \in [0, 1]$ the *relative entropy* (Kullback-Leibler divergence) of a coin with bias $a$ from a coin with bias $p$, and the [binary entropy](/binary-entropy-function/) in nats, are
$$ D(a\|p) = a\ln\frac{a}{p} + (1-a)\ln\frac{1-a}{1-p}, \qquad H(a) = -a\ln a - (1-a)\ln(1-a), $$
with $0\ln 0 = 0$.

1. **Upper bound.** For each real $a$ with $p \le a \le 1$: $\Pr[X \ge an] \le e^{-nD(a\|p)}$. For each real $a$ with $0 \le a \le p$: $\Pr[X \le an] \le e^{-nD(a\|p)}$.
2. **Lower bound.** For each integer $k$ with $0 \le k \le n$: $\Pr[X \ge k] \ge \Pr[X = k] \ge \dfrac{e^{-nD(k/n\|p)}}{n+1}$.
3. **Ratio bound.** For each integer $k$ with $k + 1 > (n+1)p$, in particular each $k \ge np$:
$$ \Pr[X \ge k] \le \Pr[X = k]\cdot\frac{(k+1)(1-p)}{k+1-(n+1)p}. $$
4. **Subset bound.** For each integer $1 \le k \le n$: $\Pr[X \ge k] \le \binom nk p^k \le \left(\dfrac{enp}{k}\right)^k$.
5. **Quadratic bound.** $D(a\|p) \ge 2(a-p)^2$ for all $a \in [0, 1]$. Hence $\Pr[X \ge np + t] \le e^{-2t^2/n}$ for $t \ge 0$.

By 1 and 2, for each integer $k$ with $np \le k \le n$,
$$ \frac{e^{-nD(k/n\|p)}}{n+1} \le \Pr[X \ge k] \le e^{-nD(k/n\|p)}. $$

## In plain words

Toss a biased coin many times and count the heads. The chance to see many more heads than expected is tiny, and this page says exactly how tiny. It is a fixed number raised to the power of the number of tosses. That fixed number depends only on how biased the coin is and on the fraction of heads you ask for. It is measured by how different the two coins are: the real coin, and an imagined coin whose bias equals the fraction you ask for.

The bound is exact up to a factor that grows only as fast as the number of tosses, which is small next to an exponential. The simpler bounds that people use in algorithms, such as those of Chernoff and Hoeffding, are easier to compute but always a little weaker.

## Proof

Write $q = 1 - p$ and $b_j = \Pr[X = j]$.

**Part 1.** Let $p \le a \le 1$. If $a = 1$, then $\Pr[X \ge n] = p^n = e^{-n\ln(1/p)} = e^{-nD(1\|p)}$. Let $p \le a < 1$. The variable $X$ is a sum of $n$ independent Bernoulli($p$) variables, so for each $t \ge 0$ the method of the [Chernoff bound](/chernoff-bound/) (Markov's inequality applied to $e^{tX}$, then independence) gives the bound with the exact generating function:
$$ \Pr[X \ge an] \le e^{-tan}\,\mathbb{E}[e^{tX}] = e^{-tan}(q + pe^t)^n. $$
Choose $e^t = \dfrac{a q}{p(1-a)}$. Since $a \ge p$ we have $aq \ge p(1-a)$, so $e^t \ge 1$ and $t \ge 0$. Then
$$ q + pe^t = q + \frac{aq}{1-a} = \frac{q}{1-a}, \qquad e^{-tan} = \left(\frac{p(1-a)}{aq}\right)^{an}, $$
and the product is
$$ \left(\frac pa\right)^{an}\left(\frac{1-a}{q}\right)^{an}\left(\frac{q}{1-a}\right)^{n} = \left(\frac pa\right)^{an}\left(\frac{q}{1-a}\right)^{(1-a)n} = e^{-nD(a\|p)}. $$
For the lower tail, $n - X \sim \mathrm{Bin}(n, q)$, and $X \le an$ holds exactly when $n - X \ge (1-a)n$, with $1 - a \ge q$. The upper bound for $n - X$ gives $e^{-nD(1-a\|q)}$, and $D(1-a\|1-p) = D(a\|p)$ by the definition.

**Part 2.** Let $a = k/n$ and consider the binomial law with parameter $a$: $c_j = \binom nj a^j(1-a)^{n-j}$ for $j = 0, \ldots, n$. If $a \in \{0, 1\}$, then $c_k = 1$. Otherwise, for $0 \le j < n$,
$$ \frac{c_{j+1}}{c_j} = \frac{(n-j)a}{(j+1)(1-a)} \ge 1 \iff (n-j)a \ge (j+1)(1-a) \iff j \le na + a - 1 = k - (1 - a). $$
So the ratio is at least 1 for $j \le k - 1$ and less than 1 for $j \ge k$, since $0 < 1 - a < 1$. Hence $c_k$ is the largest of the $n+1$ numbers $c_0, \ldots, c_n$, which sum to 1, and $c_k \ge 1/(n+1)$. Now $a^k(1-a)^{n-k} = e^{n(a\ln a + (1-a)\ln(1-a))} = e^{-nH(a)}$, so
$$ \binom nk \ge \frac{e^{nH(a)}}{n+1}. $$
Next, $p^k q^{n-k} = e^{n(a\ln p + (1-a)\ln q)}$, and from the definitions $a\ln p + (1-a)\ln q = -H(a) - D(a\|p)$. So
$$ \Pr[X = k] = \binom nk e^{-nH(a)}e^{-nD(a\|p)} \ge \frac{e^{-nD(a\|p)}}{n+1}. $$
Finally $\Pr[X \ge k] \ge \Pr[X = k]$.

**Part 3.** For $0 \le j < n$ the ratio $b_{j+1}/b_j = \dfrac{(n-j)p}{(j+1)q}$ decreases as $j$ grows. Let $r = \dfrac{(n-k)p}{(k+1)q}$. Then $b_j \le r^{j-k}b_k$ for each $j \ge k$. The condition $r < 1$ reads $(n-k)p < (k+1)q$, that is $np - kp < k + 1 - kp - p$, that is $k + 1 > (n+1)p$. So
$$ \Pr[X \ge k] = \sum_{j \ge k} b_j \le b_k\sum_{i \ge 0}r^i = \frac{b_k}{1-r} = b_k\,\frac{(k+1)q}{(k+1)q - (n-k)p} = b_k\,\frac{(k+1)q}{k+1-(n+1)p}. $$
If $k \ge np$ then $k + 1 > np + p = (n+1)p$ because $p < 1$.

**Part 4.** Write $X = \sum_{i=1}^n X_i$ with independent Bernoulli($p$) variables. If $X \ge k$, then some set $S$ of $k$ indices has $X_i = 1$ for all $i \in S$. Each such event has probability $p^k$, and there are $\binom nk$ sets, so the [union bound](/union-bound/) gives $\binom nk p^k$. Next, $\binom nk \le n^k/k!$, and $e^k = \sum_{j \ge 0}k^j/j! \ge k^k/k!$ gives $k! \ge (k/e)^k$. So $\binom nk \le (en/k)^k$, see [binomial coefficient bounds](/binomial-coefficient-bounds/).

**Part 5.** Fix $p$ and let $g(a) = D(a\|p) - 2(a-p)^2$ on $(0, 1)$. Then $g(p) = 0$,
$$ g'(a) = \ln\frac ap - \ln\frac{1-a}{q} - 4(a - p), \qquad g'(p) = 0, \qquad g''(a) = \frac1a + \frac1{1-a} - 4 = \frac{1}{a(1-a)} - 4 \ge 0, $$
since $a(1-a) \le 1/4$. So $g$ is convex with $g'(p) = 0$, its minimum on $(0,1)$ is $g(p) = 0$, and $g \ge 0$. At $a \in \{0, 1\}$ the inequality follows by continuity, since $D(\cdot\|p)$ is continuous on $[0,1]$. With $a = p + t/n$, Part 1 gives $\Pr[X \ge np + t] \le e^{-nD(a\|p)} \le e^{-2t^2/n}$ (and the probability is 0 when $a > 1$). $\square$

## Consequences

**The exponent is exact.** For each fixed $a$ with $p < a < 1$,
$$ \lim_{n \to \infty} -\frac1n\ln\Pr[X \ge an] = D(a\|p). $$
The upper bound gives $\ge$. For $\le$, let $k = \lceil an\rceil$; then $\Pr[X \ge an] = \Pr[X \ge k] \ge e^{-nD(k/n\|p)}/(n+1)$, and $k/n \to a$, $D(\cdot\|p)$ is continuous, and $\ln(n+1)/n \to 0$. This is the binomial case of Chernoff's 1952 theorem.

**The relative entropy bound beats the Chernoff bound.** The Chernoff bound (U) for $\mu = np$ and $a = (1+\delta)p$ comes from the same Markov step, after the relaxation $q + pe^t \le e^{p(e^t-1)}$. The function $\phi(t) = -tan + n\ln(q + pe^t)$ is convex, since $\phi''(t) = n\,s(1-s) \ge 0$ with $s = pe^t/(q+pe^t)$, and Part 1 picks the point where $\phi'(t) = 0$, which is its minimum. So $e^{-nD(a\|p)} = \min_t e^{\phi(t)} \le e^{\phi(t_C)} \le$ (U), where $t_C = \ln(1+\delta)$ is Chernoff's choice. The gap is large when $p$ is not small: for $n = 1000$, $p = 1/2$ and $k = 600$, the relative entropy bound is $1.800 \times 10^{-9}$ and (U) is $8.331 \times 10^{-5}$. When $p$ is small, $q + pe^t$ is close to $e^{p(e^t - 1)}$ and the two bounds are close.

**Hoeffding's bound for coins.** Part 5 is the binomial case of [Hoeffding's inequality](/hoeffding-inequality/). It loses when $p$ is small: for $p = 0.01$ and $a = 0.02$, $D(a\|p) = 0.003914$, but $2(a-p)^2 = 0.0002$.

**Counting.** Part 2 and its proof give $e^{nH(k/n)}/(n+1) \le \binom nk \le e^{nH(k/n)}$, because $c_k \le 1$. With $n = 100$ and $k = 10$:

| quantity | value |
| --- | --- |
| $e^{nH(k/n)}/(n+1)$ | $1.300 \times 10^{12}$ |
| $\binom nk$ | $1.731 \times 10^{13}$ |
| $n^k/k!$ | $2.756 \times 10^{13}$ |
| $e^{nH(k/n)}$ | $1.313 \times 10^{14}$ |
| $(en/k)^k$ | $2.203 \times 10^{14}$ |

**Rare events.** Part 4 is the form used for [balls into bins](/balls-into-bins/), where $p = 1/n$ and $k$ is small. For $\mathrm{Bin}(1000, 0.001)$: $\Pr[X \ge 5] = 3.637 \times 10^{-3}$, $\binom{1000}{5}10^{-15} = 8.250 \times 10^{-3}$ and $(e/5)^5 = 4.749 \times 10^{-2}$; $\Pr[X \ge 10] = 1.074 \times 10^{-7}$, $\binom{1000}{10}10^{-30} = 2.634 \times 10^{-7}$ and $(e/10)^{10} = 2.203 \times 10^{-6}$.

## Tightness

**The exact-type bounds.** The first table is for $n = 1000$. The lower bound is $e^{-nD}/(n+1)$, the KL bound is $e^{-nD}$ with $D = D(k/n\|p)$, the ratio bound is Part 3, and "normal" is the normal approximation with continuity correction, $1 - \Phi\bigl((k - \frac12 - np)/\sqrt{np(1-p)}\bigr)$, which is an estimate and not a bound.

| $p$ | $k$ | exact $\Pr[X \ge k]$ | $\Pr[X = k]$ | lower bound | KL bound | ratio bound | normal |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.5 | 520 | $1.087 \times 10^{-1}$ | $1.134 \times 10^{-2}$ | $4.488 \times 10^{-4}$ | $4.492 \times 10^{-1}$ | $1.441 \times 10^{-1}$ | $1.087 \times 10^{-1}$ |
| 0.5 | 550 | $8.653 \times 10^{-4}$ | $1.694 \times 10^{-4}$ | $6.675 \times 10^{-6}$ | $6.682 \times 10^{-3}$ | $9.241 \times 10^{-4}$ | $8.721 \times 10^{-4}$ |
| 0.5 | 600 | $1.364 \times 10^{-10}$ | $4.634 \times 10^{-11}$ | $1.798 \times 10^{-12}$ | $1.800 \times 10^{-9}$ | $1.386 \times 10^{-10}$ | $1.558 \times 10^{-10}$ |
| 0.5 | 700 | $8.833 \times 10^{-38}$ | $5.066 \times 10^{-38}$ | $1.839 \times 10^{-39}$ | $1.841 \times 10^{-36}$ | $8.856 \times 10^{-38}$ | $8.457 \times 10^{-37}$ |
| 0.01 | 15 | $8.241 \times 10^{-2}$ | $3.454 \times 10^{-2}$ | $3.343 \times 10^{-4}$ | $3.347 \times 10^{-1}$ | $9.134 \times 10^{-2}$ | $7.633 \times 10^{-2}$ |
| 0.01 | 20 | $3.288 \times 10^{-3}$ | $1.792 \times 10^{-3}$ | $1.995 \times 10^{-5}$ | $1.997 \times 10^{-2}$ | $3.390 \times 10^{-3}$ | $1.267 \times 10^{-3}$ |
| 0.01 | 30 | $2.060 \times 10^{-7}$ | $1.418 \times 10^{-7}$ | $1.921 \times 10^{-9}$ | $1.923 \times 10^{-6}$ | $2.073 \times 10^{-7}$ | $2.868 \times 10^{-10}$ |
| 0.01 | 50 | $8.306 \times 10^{-20}$ | $6.751 \times 10^{-20}$ | $1.167 \times 10^{-21}$ | $1.168 \times 10^{-18}$ | $8.315 \times 10^{-20}$ | $1.891 \times 10^{-36}$ |

**The simpler bounds.** The second table is for the same cases. Chernoff (U) uses $\mu = np$ and $\delta = k/\mu - 1$, the simple form is $e^{-\delta^2\mu/3}$ (only for $\delta \le 1$), Hoeffding is $e^{-2(k - np)^2/n}$, and Chebyshev is $np(1-p)/(k - np)^2$.

| $p$ | $k$ | exact | KL bound | Chernoff (U) | $e^{-\delta^2\mu/3}$ | Hoeffding | Chebyshev |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.5 | 520 | $1.087 \times 10^{-1}$ | $4.492 \times 10^{-1}$ | $6.738 \times 10^{-1}$ | $7.659 \times 10^{-1}$ | $4.493 \times 10^{-1}$ | $0.625$ |
| 0.5 | 550 | $8.653 \times 10^{-4}$ | $6.682 \times 10^{-3}$ | $8.887 \times 10^{-2}$ | $1.889 \times 10^{-1}$ | $6.738 \times 10^{-3}$ | $0.100$ |
| 0.5 | 600 | $1.364 \times 10^{-10}$ | $1.800 \times 10^{-9}$ | $8.331 \times 10^{-5}$ | $1.273 \times 10^{-3}$ | $2.061 \times 10^{-9}$ | $0.025$ |
| 0.5 | 700 | $8.833 \times 10^{-38}$ | $1.841 \times 10^{-36}$ | $3.709 \times 10^{-16}$ | $2.623 \times 10^{-12}$ | $1.805 \times 10^{-35}$ | $0.00625$ |
| 0.01 | 15 | $8.241 \times 10^{-2}$ | $3.347 \times 10^{-1}$ | $3.389 \times 10^{-1}$ | $4.346 \times 10^{-1}$ | $9.512 \times 10^{-1}$ | $0.396$ |
| 0.01 | 20 | $3.288 \times 10^{-3}$ | $1.997 \times 10^{-2}$ | $2.101 \times 10^{-2}$ | $3.567 \times 10^{-2}$ | $8.187 \times 10^{-1}$ | $0.099$ |
| 0.01 | 30 | $2.060 \times 10^{-7}$ | $1.923 \times 10^{-6}$ | $2.356 \times 10^{-6}$ | not valid | $4.493 \times 10^{-1}$ | $0.0248$ |
| 0.01 | 50 | $8.306 \times 10^{-20}$ | $1.168 \times 10^{-18}$ | $2.650 \times 10^{-18}$ | not valid | $4.076 \times 10^{-2}$ | $0.00619$ |

Three things show in the tables. The ratio bound is within 2 percent of the exact tail when $k$ is about 6 standard deviations above the mean, and within 7 percent at about 3. The KL bound is too large by a factor of 4 to 21 in these rows, and the lower bound is too small by a factor of 48 to 246; the truth is in between. Hoeffding is close to the KL bound when $p = 1/2$ and nearly useless when $p = 0.01$, while Chernoff (U) is the other way round.

**The polynomial factor.** For fixed $p < a < 1$ and $k = an$ an integer, $\Pr[X \ge k] = \Theta\bigl(e^{-nD(a\|p)}/\sqrt n\bigr)$. Neither factor $1$ nor $1/(n+1)$ of the statement is the truth, but each is off only by a polynomial. Proof: by the sharp form of [Stirling's approximation](/stirling-approximation/), $c_k = \binom nk a^k(1-a)^{n-k} \sim 1/\sqrt{2\pi n a(1-a)}$, so $\Pr[X = k] = c_k e^{-nD(a\|p)}$ is of this order. The ratio bound multiplies $\Pr[X = k]$ by $1/(1-r)$, and $r \to (1-a)p/(a(1-p)) < 1$, a constant. So the tail is between $\Pr[X = k]$ and a constant times it.

### Pitfalls

- **The normal approximation is not a bound.** In the first table it is too small by 16 orders of magnitude at $p = 0.01$, $k = 50$, and too large by a factor of about 10 at $p = 1/2$, $k = 700$. The [central limit theorem](/central-limit-theorem/) controls the absolute error of the distribution function, about $1/\sqrt n$, which says nothing about tails smaller than that.
- **Chebyshev is polynomial.** Its bound decays as $1/t^2$, not exponentially. It is the right tool only when the variables are not fully independent.
- **Direction of the bound.** The KL upper bound needs $a \ge p$ for the upper tail and $a \le p$ for the lower tail. For $a$ on the wrong side, $e^{-nD(a\|p)}$ is less than 1 but the probability tends to 1.
- **Floating point.** For large $n$ the terms $\binom nj p^j(1-p)^{n-j}$ underflow, and $1 - \Pr[X < k]$ loses all digits when the tail is small. Sum the tail terms from $k$ upward, in log space or with exact integers.

## History

Chernoff (1952) showed that for sums of independent identically distributed variables, and so for the binomial, the tail $\Pr[X \ge an]$ decays as $e^{-n\rho}$ with $\rho$ given by the optimized moment generating function; for the binomial $\rho = D(a\|p)$. Hoeffding (1963), Theorem 1, proved the non-asymptotic bound $e^{-nD(a\|p)}$ for the mean of independent variables in $[0, 1]$, and from it the bound $e^{-2nt^2}$. The lower bound by the largest term of the binomial law with parameter $k/n$ is the method of types of information theory; see Cover and Thomas, Chapter 11.

## References
