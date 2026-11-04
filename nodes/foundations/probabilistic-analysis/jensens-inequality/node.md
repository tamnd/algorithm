---
tag: B08BEG
kind: theorem
slug: jensens-inequality
name: Jensen's inequality
aliases:
- Jensen inequality
area: foundations/probabilistic-analysis
level: intro
summary: For a convex function f, f(E[X]) <= E[f(X)].
prereqs: [convex-function, random-variable, expected-value, linearity-of-expectation]
see_also: [variance, random-binary-search-tree, comparison-sort-lower-bound, kraft-inequality, shannon-entropy, moment-generating-function, markov-inequality, hash-collision]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 2.1.2, Jensen's Inequality
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.3, Discrete random variables (Jensen's inequality for a convex function)
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume 1, third edition
    locator: Chapter IX, Random Variables; Expectation
  - paper: doi:10.1007/BF02418571
    title: J. L. W. V. Jensen, Sur les fonctions convexes et les inégalités entre les valeurs moyennes, Acta Mathematica 30 (1906), pages 175 to 193
    locator: the inequality for convex functions and weighted means
  - url: "https://en.wikipedia.org/wiki/Jensen%27s_inequality"
    locator: lead section (Jensen 1906, and the earlier proof of Hölder 1889 for twice differentiable functions)
---

Jensen's inequality says that for a [convex function](/convex-function/) $f$ and a [random variable](/random-variable/) $X$ with a finite mean, $f(\mathrm{E}[X]) \le \mathrm{E}[f(X)]$. For a concave function the inequality turns the other way. It is how a bound on $\mathrm{E}[f(X)]$ becomes a bound on $\mathrm{E}[X]$, as in the $O(\log n)$ bound on the expected height of a [random binary search tree](/random-binary-search-tree/), and it gives the facts $\mathrm{E}[X]^2 \le \mathrm{E}[X^2]$, $\mathrm{E}[1/X] \ge 1/\mathrm{E}[X]$ and the average-case [lower bound for comparison sorting](/comparison-sort-lower-bound/).

## Statement

A function $f : I \to \mathbb{R}$ on an interval $I \subseteq \mathbb{R}$ is *convex* when
$$ f(\lambda x + (1 - \lambda) y) \le \lambda f(x) + (1 - \lambda) f(y) \qquad \text{for all } x, y \in I \text{ and } \lambda \in [0, 1], $$
and *strictly convex* when the inequality is strict for all $x \ne y$ and $\lambda \in (0, 1)$. It is *concave* when $-f$ is convex.

**Theorem.** Let $X$ be a discrete random variable whose values lie in $I$ with probability $1$, and with $\mathrm{E}[|X|] < \infty$. Let $f$ be convex on $I$. Then $\mathrm{E}[X] \in I$, the expectation $\mathrm{E}[f(X)]$ is defined (finite or $+\infty$), and
$$ f(\mathrm{E}[X]) \le \mathrm{E}[f(X)]. $$
If $f$ is strictly convex, equality holds if and only if $X = \mathrm{E}[X]$ with probability $1$. If $f$ is concave, $f(\mathrm{E}[X]) \ge \mathrm{E}[f(X)]$.

**Finite form.** For $x_1, \ldots, x_n \in I$ and weights $\lambda_i \ge 0$ with $\sum_i \lambda_i = 1$,
$$ f\Big(\sum_{i=1}^n \lambda_i x_i\Big) \le \sum_{i=1}^n \lambda_i f(x_i). $$
This is the theorem for the $X$ that takes the value $x_i$ with probability $\lambda_i$. The theorem also holds for a general random variable, with the same proof and the Lebesgue integral as the expectation.

## In plain words

A convex function curves upward, like a bowl. Pick some points on the bowl and take their average. The average of the heights is at least the height of the bowl above the average position, because the straight chords of a bowl lie above the bowl.

So for an upward-curving cost, the average cost is at least the cost of the average input. For a downward-curving function, like the logarithm, the average of the function is at most the function of the average. The rule is useful in both directions. If you know that the average of a fast-growing function of the running time is small, the average running time is small too.

## Proof

**Lemma (three slopes).** Let $f$ be convex on $I$ and $x < y < z$ in $I$. Then
$$ \frac{f(y) - f(x)}{y - x} \le \frac{f(z) - f(x)}{z - x} \le \frac{f(z) - f(y)}{z - y}. $$
If $f$ is strictly convex, both inequalities are strict.

*Proof.* Write $y = \lambda x + (1 - \lambda) z$ with $\lambda = (z - y)/(z - x) \in (0, 1)$, so $1 - \lambda = (y - x)/(z - x)$. Convexity gives $f(y) \le \lambda f(x) + (1 - \lambda) f(z)$. Subtract $f(x)$ from both sides: $f(y) - f(x) \le (1 - \lambda)(f(z) - f(x))$, and divide by $y - x > 0$ to get the left inequality. Subtract $f(z)$ instead: $f(y) - f(z) \le \lambda (f(x) - f(z))$, so $f(z) - f(y) \ge \lambda (f(z) - f(x))$, and divide by $z - y > 0$ to get the right inequality. For strict convexity every step is strict. $\square$

**Lemma (supporting line).** Let $f$ be convex on $I$ and let $\mu$ be an interior point of $I$. There is a real number $c$ such that
$$ f(x) \ge f(\mu) + c\,(x - \mu) \qquad \text{for all } x \in I. $$
If $f$ is strictly convex, the inequality is strict for each $x \ne \mu$.

*Proof.* For $x \in I \setminus \{\mu\}$ let $s(x) = (f(x) - f(\mu))/(x - \mu)$, the slope of the chord from $\mu$ to $x$. We show that $s$ is non-decreasing. Take $x < x'$ in $I \setminus \{\mu\}$. If $x < x' < \mu$, the three-slope lemma on $x < x' < \mu$ gives $s(x) \le s(x')$ (compare its middle and right terms). If $x < \mu < x'$, the lemma on $x < \mu < x'$ gives $s(x) \le s(x')$ (its left and right terms). If $\mu < x < x'$, the lemma on $\mu < x < x'$ gives $s(x) \le s(x')$ (its left and middle terms). Since $\mu$ is interior, there is some $x' > \mu$ in $I$, and $s(x) \le s(x')$ for each $x < \mu$. So $c = \sup_{x < \mu} s(x)$ is a finite real number, with $s(x) \le c$ for $x < \mu$ and $s(x) \ge c$ for $x > \mu$. For $x > \mu$, multiply $s(x) \ge c$ by $x - \mu > 0$. For $x < \mu$, multiply $s(x) \le c$ by $x - \mu < 0$, which turns the inequality around. Both give $f(x) - f(\mu) \ge c(x - \mu)$. For strict convexity $s$ is strictly increasing. Then for $x > \mu$ we pick $x' \in (\mu, x)$ and get $s(x) > s(x') \ge c$, and for $x < \mu$ we pick $x'' \in (x, \mu)$ and get $s(x) < s(x'') \le c$. So the inequality is strict. $\square$

**Proof of the theorem.** Let $\mu = \mathrm{E}[X]$, which is finite. Let $a = \inf I$ and $b = \sup I$.

*Step 1: $\mu \in I$, and the endpoint case.* Since $a \le X \le b$ with probability $1$, we have $a \le \mu \le b$. Suppose $\mu = a$ (so $a$ is finite). Then $X - a \ge 0$ with probability $1$ and $\mathrm{E}[X - a] = 0$. A non-negative discrete variable with mean $0$ is $0$ at each outcome of positive probability, so $X = a$ with probability $1$. In particular $a$ is a value of $X$, so $a \in I$, and $f(X) = f(\mu)$ with probability $1$, which gives equality in the theorem. The case $\mu = b$ is the same. In all other cases $\mu$ is an interior point of $I$.

*Step 2: the inequality.* Let $\mu$ be interior, and let $\ell(x) = f(\mu) + c(x - \mu)$ be the supporting line of the lemma. Then $f(X) \ge \ell(X)$ at each outcome. The variable $\ell(X)$ has the finite mean $\mathrm{E}[\ell(X)] = f(\mu) + c(\mathrm{E}[X] - \mu) = f(\mu)$, by [linearity of expectation](/linearity-of-expectation/). The variable $D = f(X) - \ell(X)$ is non-negative, so $\mathrm{E}[D]$ is defined and $\mathrm{E}[D] \ge 0$, possibly $+\infty$. Hence $\mathrm{E}[f(X)] = \mathrm{E}[D] + \mathrm{E}[\ell(X)]$ is defined, and
$$ \mathrm{E}[f(X)] = \mathrm{E}[D] + f(\mu) \ge f(\mu) = f(\mathrm{E}[X]). $$

*Step 3: equality for strictly convex $f$.* If $X = \mu$ with probability $1$, both sides equal $f(\mu)$. Otherwise $\Pr[X \ne \mu] > 0$, so $\mu$ is interior by step 1, and some outcome $\omega$ of positive probability has $X(\omega) \ne \mu$. By the strict form of the lemma, $D(\omega) > 0$, so $\mathrm{E}[D] \ge D(\omega)\Pr[\{\omega\}] > 0$ and the inequality is strict.

*Concave case.* Apply the theorem to the convex function $-f$. $\blacksquare$

## Consequences

**Second moment.** With $f(x) = x^2$, $\mathrm{E}[X]^2 \le \mathrm{E}[X^2]$. This is the statement that the [variance](/variance/) $\mathrm{E}[X^2] - \mathrm{E}[X]^2$ is never negative. It is also why a bound $\mathrm{E}[X^2] \le B$ gives $\mathrm{E}[X] \le \sqrt B$.

**Reciprocals.** $f(x) = 1/x$ is strictly convex on $(0, \infty)$, so $\mathrm{E}[1/X] \ge 1/\mathrm{E}[X]$ for a positive $X$. For $X$ uniform on $\{1, 2, 3\}$, $\mathrm{E}[X] = 2$ and $\mathrm{E}[1/X] = 11/18 \approx 0.611$, against $1/2$. So the expected speed of a run is not the inverse of the expected time.

**Means.** $\ln$ is concave on $(0, \infty)$. For positive $x_1, \ldots, x_n$ the finite form with $\lambda_i = 1/n$ gives $\frac1n \sum_i \ln x_i \le \ln\big(\frac1n \sum_i x_i\big)$, which is the inequality of the arithmetic and geometric means, $(x_1 \cdots x_n)^{1/n} \le \frac1n \sum_i x_i$. For $1, 2, 4, 8$ the geometric mean is $2.828$ and the arithmetic mean is $3.75$.

**Height of a random binary search tree.** Let $X_n$ be the height of a [binary search tree](/binary-search-tree/) built by inserting $n$ distinct keys in a uniform random order. The analysis bounds the exponential height $Y_n = 2^{X_n}$ instead, because $Y_n$ obeys a simple recurrence, and it shows $\mathrm{E}[Y_n] \le C n^3$ for a constant $C$. The function $x \mapsto 2^x$ is convex, so Jensen gives $2^{\mathrm{E}[X_n]} \le \mathrm{E}[2^{X_n}] \le C n^3$, and taking $\lg$ gives $\mathrm{E}[X_n] \le 3\lg n + \lg C = O(\log n)$. Without Jensen, a bound on $\mathrm{E}[2^{X_n}]$ says nothing direct about $\mathrm{E}[X_n]$. See the [random binary search tree](/random-binary-search-tree/).

**Average-case lower bound for sorting.** A comparison sort on $n$ distinct keys is a [decision tree](/decision-tree-model/) with at least $L = n!$ reachable leaves. Let $d$ be the depth of the leaf reached on a uniform random input; each of the $L$ leaves has probability $1/L$. The [Kraft inequality](/kraft-inequality/) for a binary tree gives $\sum_{\text{leaves}} 2^{-d(\ell)} \le 1$ (it holds for a single leaf, and the sum for a tree is half the sum of the sums for its two subtrees). With the convex function $x \mapsto 2^{-x}$,
$$ 2^{-\mathrm{E}[d]} \le \mathrm{E}[2^{-d}] = \frac1L \sum_{\ell} 2^{-d(\ell)} \le \frac1L, $$
so $\mathrm{E}[d] \ge \lg L = \lg n!$. Every comparison sort makes at least $\lg n!$ comparisons on average over random inputs, not only in the worst case. For $n = 3$ the best tree has two leaves at depth $2$ and four at depth $3$, with mean depth $16/6 \approx 2.667$, and $\lg 6 \approx 2.585$.

**Hash collisions.** Hash $n$ keys into $m$ slots, and let $\ell_j$ be the number of keys in slot $j$. The number of colliding pairs is $\sum_j \binom{\ell_j}{2}$, and $g(x) = x(x - 1)/2$ is convex. The finite form with $\lambda_j = 1/m$ gives $\frac1m \sum_j g(\ell_j) \ge g(n/m)$, so any [hash function](/hash-collision/) has at least $m\, g(n/m) = \frac{n(n - m)}{2m}$ colliding pairs on any set of keys. For $n = 1000$ and $m = 100$ this is $4500$ pairs.

**Entropy.** For a random variable $X$ with at most $k$ values of positive probability, $\mathrm{E}[\lg(1/p(X))] \le \lg \mathrm{E}[1/p(X)] \le \lg k$ by concavity of $\lg$. So the [Shannon entropy](/shannon-entropy/) of $X$ is at most $\lg k$, with equality for the uniform distribution.

**Moments and tails.** For $t$ real, $e^{tx}$ is convex, so $\mathrm{E}[e^{tX}] \ge e^{t\mathrm{E}[X]}$: the [moment generating function](/moment-generating-function/) is at least the exponential of the mean. For $1 \le p \le q$, Jensen with the convex $x \mapsto x^{q/p}$ on $|X|^p$ gives $\mathrm{E}[|X|^p]^{1/p} \le \mathrm{E}[|X|^q]^{1/q}$.

## Tightness

**Equality.** For an affine $f(x) = \alpha x + \beta$, equality holds for each $X$, by linearity. For a strictly convex $f$, equality holds only for a constant $X$, by the theorem. So no inequality of the form $f(\mathrm{E}[X]) + \delta \le \mathrm{E}[f(X)]$ with a fixed $\delta > 0$ holds for all $X$.

**The gap can be unbounded.** Let $X = k$ with probability $1/k$ and $X = 0$ otherwise, for an integer $k \ge 1$. Then $\mathrm{E}[X] = 1$ and $\mathrm{E}[X^2] = k$. So $f(\mathrm{E}[X]) = 1$, while $\mathrm{E}[f(X)]$ is as large as we like. Jensen gives a direction, not a size. The size of the gap for $f(x) = x^2$ is the variance.

**Convexity is needed.** For $f(x) = \sqrt{x}$, which is concave, and $X$ uniform on $\{0, 4\}$, $f(\mathrm{E}[X]) = \sqrt 2 \approx 1.414$ and $\mathrm{E}[f(X)] = 1$. The convex direction fails.

### Pitfalls

- **The direction.** For convex $f$ the function of the mean is the smaller side. A common slip is $\mathrm{E}[X^2] \le \mathrm{E}[X]^2$. Check with a two-point example before using the inequality.
- **Concave functions of costs.** $\mathrm{E}[\lg T] \le \lg \mathrm{E}[T]$ for a positive running time $T$. A bound on $\mathrm{E}[\lg T]$ therefore does not bound $\mathrm{E}[T]$, and the mean of the logarithms of measured times is not the logarithm of the mean time.
- **Convex on the right set.** $f$ must be convex on an interval that holds all values of $X$. $1/x$ is convex on $(0, \infty)$ but not on $\mathbb{R} \setminus \{0\}$. For $X$ uniform on $\{-1, 1\}$ the mean is $0$ and $1/\mathrm{E}[X]$ is not defined.
- **Finite mean.** The theorem needs $\mathrm{E}[|X|] < \infty$. If the mean is infinite, the left side $f(\mathrm{E}[X])$ has no meaning.
- **A product is not a convex function of one variable.** $\mathrm{E}[XY]$ against $\mathrm{E}[X]\,\mathrm{E}[Y]$ is a question of correlation, not of Jensen. See [independent random variables](/independent-random-variables/).

## History

Jensen published the inequality for convex functions and weighted means in Acta Mathematica in 1906. The Wikipedia article records an earlier proof by Otto Hölder in 1889 for twice differentiable functions. In the analysis of algorithms it appears in the standard texts: Mitzenmacher and Upfal, Section 2.1.2, and CLRS, Appendix C.3.

## References
