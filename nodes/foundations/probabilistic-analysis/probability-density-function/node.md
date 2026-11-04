---
tag: AH9E2G
kind: definition
slug: probability-density-function
name: Probability density function
area: foundations/probabilistic-analysis
level: intro
summary: A function whose integral over an interval gives the probability that a continuous random variable falls in that interval.
prereqs: [probability-distribution, random-variable]
see_also: [discrete-probability-distribution, uniform-distribution, inverse-transform-sampling, bucket-sort, geometric-distribution, central-limit-theorem]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 8.1, Continuous Random Variables; Section 8.2, The Uniform Distribution; Section 8.3, The Exponential Distribution
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.2 (continuous uniform probability distribution), and Section 8.4, Bucket sort
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume I, third edition
    locator: Chapter VII, The Normal Approximation to the Binomial Distribution (the normal density)
---

A probability density function is a nonnegative function $f$ whose integral over an interval gives the probability that a continuous [random variable](/random-variable/) falls in that interval. It plays the role for continuous variables that the mass function plays for [discrete distributions](/discrete-probability-distribution/), with integrals in place of sums. In algorithms it appears when keys are random real numbers, as in [bucket sort](/bucket-sort/), when hash values are modeled as uniform reals in $[0, 1)$, and when waiting times are modeled as exponential.

## Definition

A function $f : \mathbb{R} \to [0, \infty)$ is a **probability density function** (pdf) when it is integrable and

$$\int_{-\infty}^{\infty} f(x)\,dx = 1.$$

A real [random variable](/random-variable/) $X$ **has density** $f$ when, for all $a \le b$,

$$\Pr(a \le X \le b) = \int_a^b f(x)\,dx.$$

Then $X$ is called (absolutely) **continuous**. An equivalent condition is $F_X(x) = \int_{-\infty}^x f(t)\,dt$ for all $x$, where $F_X(x) = \Pr(X \le x)$ is the CDF (see [probability distribution](/probability-distribution/)). The integral is a Riemann integral for the densities on this page, and a Lebesgue integral in general.

**Properties.** Let $X$ have density $f$.

1. **Single points have probability 0.** With $a = b = x$, $\Pr(X = x) = \int_x^x f = 0$. So $\Pr(a < X < b) = \Pr(a \le X \le b)$: the endpoints do not change the value.
2. **The CDF is continuous**, because it has no jumps, by property 1 and the jump formula $\Pr(X = x) = F_X(x) - F_X(x^-)$.
3. **The density is the derivative of the CDF** at each point $x$ where $f$ is continuous. This is the fundamental theorem of calculus applied to $F_X(x) = \int_{-\infty}^x f$. For small $h > 0$, $\Pr(x \le X \le x + h) \approx f(x)\,h$.
4. **The density is not unique.** If $g = f$ except at finitely many points, then $\int_a^b g = \int_a^b f$ for all $a, b$, so $g$ is also a density of $X$.
5. **Expectation.** If $\int |x| f(x)\,dx < \infty$, then $\mathbb{E}[X] = \int x f(x)\,dx$. For $X \ge 0$, $\mathbb{E}[X] = \int_0^\infty \Pr(X > x)\,dx$, the continuous form of the tail sum on the [expected value](/expected-value/) page.

**Change of variables.** Let $g$ be strictly increasing and differentiable on an open interval that holds the values of $X$, and let $Y = g(X)$. Then $F_Y(y) = \Pr(g(X) \le y) = \Pr(X \le g^{-1}(y)) = F_X(g^{-1}(y))$. If $f$ is continuous at $g^{-1}(y)$ and $g' > 0$ there, the chain rule gives

$$f_Y(y) = f_X\big(g^{-1}(y)\big) \cdot \frac{d}{dy} g^{-1}(y).$$

For a strictly decreasing $g$, the same steps with $\Pr(X \ge g^{-1}(y))$ give the absolute value of the derivative.

**Joint density.** A pair $(X, Y)$ has joint density $f(x, y) \ge 0$ when $\Pr((X, Y) \in R) = \iint_R f$ for each rectangle $R$. The variables are [independent](/independent-random-variables/) exactly when there is a joint density of the form $f_X(x) f_Y(y)$.

## Examples and non-examples

**Uniform on an interval.** On $[a, b)$ the density is $f(x) = 1/(b - a)$ on the interval and 0 elsewhere. Then $\Pr(c \le X \le d) = (d - c)/(b - a)$ for $a \le c \le d \le b$. See [uniform distribution](/uniform-distribution/). For $[0, 1/2)$ the density is $f = 2$ on the interval. A density can be larger than 1. Only its integral is a probability.

**Bucket sort.** [Bucket sort](/bucket-sort/) assumes $n$ independent keys with the uniform density on $[0, 1)$. Bucket $i$ holds the keys in $[i/n, (i+1)/n)$, so each key lands in it with probability $\int_{i/n}^{(i+1)/n} 1\,dx = 1/n$. The number of keys in one bucket is then [binomial](/binomial-distribution/)$(n, 1/n)$, and this gives the expected linear time in CLRS, Section 8.4.

**Exponential waiting times.** For a rate $\lambda > 0$, $f(x) = \lambda e^{-\lambda x}$ for $x \ge 0$ and 0 for $x < 0$. Its integral is $[-e^{-\lambda x}]_0^\infty = 1$, and $F(x) = 1 - e^{-\lambda x}$ for $x \ge 0$. By property 5, $\mathbb{E}[X] = \int_0^\infty e^{-\lambda x}\,dx = 1/\lambda$. By parts, $\mathbb{E}[X^2] = \int_0^\infty 2x e^{-\lambda x}\,dx = 2/\lambda^2$, so the variance is $2/\lambda^2 - 1/\lambda^2 = 1/\lambda^2$. For $\lambda = 2$: the mean is $0.5$, the variance is $0.25$, and $\Pr(X > 1) = e^{-2} \approx 0.1353$. The exponential law has no memory: $\Pr(X > s + t \mid X > s) = e^{-\lambda(s+t)} / e^{-\lambda s} = \Pr(X > t)$.

**Sampling it.** Let $U$ be uniform on $[0, 1)$ and $X = -\ln(1 - U)/\lambda$. For $x \ge 0$, $\Pr(X \le x) = \Pr(U \le 1 - e^{-\lambda x}) = 1 - e^{-\lambda x}$, so $X$ is exponential with rate $\lambda$. This is [inverse transform sampling](/inverse-transform-sampling/).

**From continuous to discrete.** If $X$ is exponential with rate $\lambda$, then $\lceil X \rceil$ is [geometric](/geometric-distribution/) with success probability $q = 1 - e^{-\lambda}$. For $k \ge 1$: $\Pr(\lceil X \rceil = k) = \Pr(k - 1 < X \le k) = e^{-\lambda(k-1)} - e^{-\lambda k} = (e^{-\lambda})^{k-1}(1 - e^{-\lambda})$. For $\lambda = 2$, the first values are $0.86466$, $0.11702$ and $0.01584$.

**The minimum of uniform hash values.** Let $U_1, \ldots, U_n$ be independent and uniform on $[0, 1)$, as in a model of hash values of $n$ distinct items, and let $M = \min_i U_i$. Then $\Pr(M > x) = (1 - x)^n$ for $0 \le x \le 1$, so $M$ has density $n(1 - x)^{n-1}$ on $[0, 1]$ by property 3, and $\mathbb{E}[M] = \int_0^1 (1 - x)^n\,dx = \frac{1}{n+1}$. For $n = 9$ this is $0.1$. Sketches that count distinct items, such as [MinHash](/minhash/) and [HyperLogLog](/hyperloglog/), use the fact that small hash values carry information about the number of distinct items.

**The normal density.** $\varphi(x) = \frac{1}{\sqrt{2\pi}} e^{-x^2/2}$ is the density of the standard normal law. It is the limit shape in the [central limit theorem](/central-limit-theorem/) and in the normal approximation of the [binomial distribution](/binomial-distribution/) (Feller, Chapter VII).

**Non-example: not integrable.** $f(x) = 1/x$ on $[1, \infty)$ is nonnegative, but its integral diverges, so no scaling makes it a density. In contrast, $f(x) = 1/x^2$ on $[1, \infty)$ is a density. A variable with this density has an infinite mean, because $\int_1^\infty x \cdot x^{-2}\,dx$ diverges.

**Non-example: a discrete variable.** A fair bit $B$ has no density. If $f$ were one, then $\Pr(B = 0) = \int_0^0 f = 0$, but $\Pr(B = 0) = 1/2$.

**Non-example: continuous but with no density.** Write a number in base 3 with digits chosen independently and uniformly from $\{0, 2\}$. The result $C$ has a continuous CDF (the Cantor function), so each point has probability 0. But $C$ lies with probability 1 in the Cantor set, which is covered for each $k$ by $2^k$ intervals of total length $(2/3)^k$. If $C$ had a density $f$, then $\Pr(C \text{ in those intervals}) = \int f$ over them, which tends to 0 as $k \to \infty$ (the integral of an integrable $f$ over sets whose length tends to 0 tends to 0). That contradicts the probability 1.

### Pitfalls

- **A density value is not a probability.** $f(x) = 2$ is fine, and $\Pr(X = x) = 0$ for every $x$. To get a probability, integrate over an interval.
- **Floating point is discrete.** A generator that returns a double in $[0, 1)$ returns one of finitely many values, for example multiples of $2^{-53}$. So $U = 0$ has a positive probability, about $1.1 \times 10^{-16}$ in that case, and $-\ln(U)$ then fails. Use $-\ln(1 - U)$, which is finite for $U \in [0, 1)$. A model with a density is an approximation of such a generator.
- **Forget the derivative and the density is wrong.** If $X$ is uniform on $[0, 1)$, then $Y = X^2$ is not uniform. The change of variables gives $f_Y(y) = \frac{1}{2\sqrt{y}}$ on $(0, 1)$, so $\Pr(Y \le 1/4) = \Pr(X \le 1/2) = 1/2$, not $1/4$.

## Related definitions

- The [probability distribution](/probability-distribution/) page defines the CDF and the kinds of distribution.
- A [discrete probability distribution](/discrete-probability-distribution/) has a mass function in place of a density.
- The [uniform distribution](/uniform-distribution/) has a constant density on an interval.
- The [geometric distribution](/geometric-distribution/) is the discrete analogue of the exponential law, with the same lack of memory.

## References
