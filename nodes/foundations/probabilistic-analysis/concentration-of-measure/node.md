---
tag: 7F5YJ1
kind: concept
slug: concentration-of-measure
name: Concentration of measure
aliases:
- concentration inequalities
area: foundations/probabilistic-analysis
level: advanced
summary: A function of many independent random variables, none of which has much influence on it, takes a value close to its mean with probability exponentially close to 1.
prereqs: [independent-random-variables, expected-value, chernoff-bound, hoeffding-inequality, martingale]
see_also: [azuma-inequality, chernoff-bound, hoeffding-inequality, binomial-tail-bounds, balls-into-bins, johnson-lindenstrauss-lemma, chromatic-number, high-probability-bounds]
sources:
  - book: isbn:9780521884273
    title: Devdatt P. Dubhashi and Alessandro Panconesi, Concentration of Measure for the Analysis of Randomized Algorithms
    locator: Section 1.1 (What is concentration of measure); Chapter 5 (Martingales and the method of bounded differences); Chapter 6 (The simple method of bounded differences in action); Chapter 9 (the upper tail)
  - paper: doi:10.1017/CBO9781107359949.008
    title: Colin McDiarmid, On the method of bounded differences, in Surveys in Combinatorics 1989, London Mathematical Society Lecture Note Series 141
    locator: pages 148 to 188 (the bounded differences inequality)
  - book: isbn:9781119061953
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, fourth edition
    locator: Chapter 7, Martingales and Tight Concentration (the vertex exposure martingale and the chromatic number)
  - book: isbn:9780199535255
    title: Stéphane Boucheron, Gábor Lugosi and Pascal Massart, Concentration Inequalities, A Nonasymptotic Theory of Independence
    locator: Chapter 1 (the bounded differences inequality); Section 5.4, The Tsirelson-Ibragimov-Sudakov inequality (Gaussian concentration)
  - paper: doi:10.1007/BF02579208
    title: Eli Shamir and Joel Spencer, Sharp concentration of the chromatic number on random graphs G(n, p), Combinatorica 7(1), 1987
    locator: pages 121 to 129
  - paper: doi:10.1007/BF02122551
    title: Béla Bollobás, The chromatic number of random graphs, Combinatorica 8(1), 1988
    locator: pages 49 to 55
  - paper: "Keith Ball, An elementary introduction to modern convex geometry, in Flavors of Geometry, MSRI Publications 31, Cambridge University Press, 1997"
    locator: Lecture 2, Lemma 2.2 (upper bound for spherical caps); Lecture 8, Concentration of measure in geometry
---

Concentration of measure is the fact that a function of many [independent](/independent-random-variables/) random variables, when no single variable can change it by much, is almost constant: it stays close to its mean, except with a probability that is exponentially small in the square of the distance. The [Chernoff bound](/chernoff-bound/) and [Hoeffding's inequality](/hoeffding-inequality/) are the case of a sum. The method of bounded differences of McDiarmid, proved with a [martingale](/martingale/) and the [Azuma inequality](/azuma-inequality/), extends them to functions that are not sums, such as the number of empty bins or the chromatic number of a random graph. The same phenomenon appears in geometry: on a sphere of high dimension, almost all the area lies near each equator.

## In plain words

Think of a quantity that depends on many independent random choices: the number of empty bins after throwing many balls, the number of colors that a random graph needs, the length of a random vector. If changing one choice can move the quantity only a little, then the quantity is very predictable. It is not exactly fixed, but large departures from its average are extremely rare, and they get rarer exponentially fast as the departure grows.

The reason is that a large departure needs many of the choices to push in the same direction at the same time, and independent choices rarely do this. This is why random algorithms often behave as if they were deterministic, and why a quick analysis of the average is often enough.

## The idea

**Bounded differences.** Let $X_1, \ldots, X_n$ be independent random variables, $X_i$ with values in a set $\Omega_i$. Let $f: \Omega_1 \times \cdots \times \Omega_n \to \mathbb{R}$ have *bounded differences* $c_1, \ldots, c_n$: for each $i$ and all $x, x'$ that differ only in coordinate $i$,
$$ |f(x) - f(x')| \le c_i. $$
Then $Z = f(X_1, \ldots, X_n)$ satisfies, for each $t > 0$,
$$ \Pr[Z - \mathbb{E}Z \ge t] \le \exp\left(-\frac{2t^2}{\sum_i c_i^2}\right), \qquad \Pr[|Z - \mathbb{E}Z| \ge t] \le 2\exp\left(-\frac{2t^2}{\sum_i c_i^2}\right). $$
This is McDiarmid's inequality (1989), also called the bounded differences inequality. The proof writes $Z - \mathbb{E}Z$ as the sum of the differences of the Doob martingale $Z_k = \mathbb{E}[Z \mid X_1, \ldots, X_k]$, shows that each difference lies, given the past, in an interval of length $c_k$, and applies Hoeffding's lemma to each step. The [Azuma inequality](/azuma-inequality/) page gives the proof; the plain Azuma argument with $|Z_k - Z_{k-1}| \le c_k$ gives the weaker exponent $t^2/(2\sum_i c_i^2)$.

The sum $f(x) = \sum_i x_i$ with $x_i \in [a_i, b_i]$ has $c_i = b_i - a_i$, and the inequality becomes Hoeffding's inequality. So the bounded differences inequality loses nothing on sums, and it needs no structure of $f$ besides the $c_i$.

**The scale.** If each $c_i \le c$, then $Z$ deviates from its mean by more than $\lambda c\sqrt n$ with probability at most $2e^{-2\lambda^2}$. A function such as a count over $n$ items can have a range of size $cn$; its typical fluctuation is only of order $c\sqrt n$.

**Mean and median.** Concentration around the mean gives concentration around each median $M$ of $Z$. If $M - \mathbb{E}Z \ge t > 0$, then $\Pr[Z - \mathbb{E}Z \ge t] \ge \Pr[Z \ge M] \ge 1/2$, and the bound gives $1/2 \le e^{-2t^2/\sum c_i^2}$, so $t \le \sqrt{\ln 2\cdot\sum_i c_i^2/2}$. The same holds below the mean. So $|M - \mathbb{E}Z| \le \sqrt{\ln 2\cdot\sum_i c_i^2/2}$, which is $0.59$ times the fluctuation scale $\sqrt{\sum_i c_i^2}$.

**Geometry.** The same phenomenon holds for Lipschitz functions of a Gaussian vector and on the sphere. Let $G$ be a standard Gaussian vector in $\mathbb{R}^n$, and let $f: \mathbb{R}^n \to \mathbb{R}$ be $L$-Lipschitz for the Euclidean distance ([Lipschitz condition](/lipschitz-condition/)). Then $\Pr[f(G) - \mathbb{E}f(G) \ge t] \le e^{-t^2/(2L^2)}$ for each $t > 0$, with no dependence on $n$ (the Tsirelson-Ibragimov-Sudakov inequality; Boucheron, Lugosi and Massart, Section 5.4). For the uniform measure on the unit sphere $S^{n-1}$ in $\mathbb{R}^n$ and a unit vector $u$, the cap $\{x : \langle x, u\rangle \ge \varepsilon\}$ has measure at most $e^{-n\varepsilon^2/2}$ for $0 \le \varepsilon < 1$ (Ball, Lemma 2.2). So almost all of the sphere lies within distance of order $1/\sqrt n$ of the equator orthogonal to $u$, for every $u$ at once.

### Pitfalls

- **Worst case differences.** The $c_i$ must bound the change for all values of the other coordinates, not only for typical values. When a rare configuration gives a large $c_i$, the bound becomes weak even though the function is well concentrated. The number of triangles in a random graph is the standard example below.
- **Independence of the inputs.** The $X_i$ must be independent. The function $f$ itself may combine them in any way, and the quantities that $f$ counts, such as the indicators of empty bins, may be dependent; what matters is the independence of the underlying choices.
- **Mean, not a known value.** The bound is around $\mathbb{E}Z$. To use it you still need $\mathbb{E}Z$, or a bound on it, from another argument such as [linearity of expectation](/linearity-of-expectation/).
- **Absolute, not relative.** The window $\lambda\sqrt{\sum c_i^2}$ is absolute. When $\mathbb{E}Z$ is smaller than $\sqrt{\sum c_i^2}$, the bound says nothing useful.

## Examples

### Empty bins

Throw $m$ balls into $n$ bins, each ball into a uniform random bin, independently. Let $Z$ be the number of empty bins. By linearity, $\mathbb{E}Z = n(1 - 1/n)^m$. The empty bin indicators are dependent, but $Z$ is a function of the $m$ independent positions of the balls, and moving one ball changes $Z$ by at most 1. So $c_i = 1$ and
$$ \Pr[|Z - \mathbb{E}Z| \ge t] \le 2e^{-2t^2/m}. $$
For $n = m = 10^4$: $\mathbb{E}Z = 3678.6$, the exact standard deviation is $31.18$, and with probability at least $0.99$ the number of empty bins lies within $162.8$ of the mean. Chebyshev's inequality with the exact variance gives the window $311.8$ at the same level, and needs the variance.

For $n = m = 100$ the exact distribution of $Z$ follows from a recurrence on the number of occupied bins: $\mathbb{E}Z = 36.603$ and the variance is $9.740$.

| $t$ | exact $\Pr[\lvert Z - \mathbb{E}Z\rvert \ge t]$ | McDiarmid $2e^{-2t^2/100}$ | Chebyshev with exact variance |
| --- | --- | --- | --- |
| 5 | $1.079 \times 10^{-1}$ | $1.213$ (no information) | $0.390$ |
| 8 | $9.974 \times 10^{-3}$ | $0.556$ | $0.152$ |
| 10 | $1.258 \times 10^{-3}$ | $0.271$ | $0.0974$ |
| 15 | $1.175 \times 10^{-6}$ | $0.0222$ | $0.0433$ |
| 20 | $7.426 \times 10^{-11}$ | $6.709 \times 10^{-4}$ | $0.0244$ |

The bounded differences inequality ignores the variance, so it is weak near the mean. In the far tail its exponential decay wins over Chebyshev. Both are far above the truth, because $\sum c_i^2 = 100$ is about ten times the true variance.

### Chromatic number of a random graph

Let $G$ be the random graph $G(n, 1/2)$ of the [Erdős-Rényi model](/erdos-renyi-model/), and let $\chi$ be its [chromatic number](/chromatic-number/). For $i = 2, \ldots, n$ let $Y_i$ be the set of edges from vertex $i$ to the vertices $1, \ldots, i-1$. The $Y_i$ are independent and determine $G$. If only $Y_i$ changes, the old proper coloring stays proper on the other vertices, because no edge between them changes; give vertex $i$ a new color. So $\chi$ changes by at most 1, in each direction, and the bounded differences inequality with $n - 1$ coordinates gives
$$ \Pr\left[|\chi - \mathbb{E}\chi| \ge \lambda\sqrt{n-1}\right] \le 2e^{-2\lambda^2}. $$
Alon and Spencer (Chapter 7) derive the bound $2e^{-\lambda^2/2}$ by this vertex exposure martingale with the Azuma inequality, and attribute the result to Shamir and Spencer (1987). The bound holds without any knowledge of the value of $\mathbb{E}\chi$. Bollobás (1988) later proved that $\chi \sim n/(2\log_2 n)$ with high probability. For $n = 10^6$, $n/(2\log_2 n) = 25086$, while the window that holds with probability $0.99$ is $\pm 1628$.

### The length of a Gaussian vector

The Euclidean norm is 1-Lipschitz. For a standard Gaussian vector $G$ in $\mathbb{R}^n$, $\mathbb{E}\|G\| = \sqrt2\,\Gamma(\frac{n+1}{2})/\Gamma(\frac n2)$, which is $9.975$ for $n = 100$ and $99.9975$ for $n = 10^4$. Gaussian concentration gives $\Pr[|\|G\| - \mathbb{E}\|G\|| \ge 3.255] \le 0.01$ for every $n$. So for $n = 10^4$ the vector lies in a shell of radius about 100 and width about 6.5, with probability at least $0.99$. This is the effect behind the [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/) and [random projection](/random-projection/): the length of a random projection of a fixed vector is close to its expected value.

### Caps of a sphere

For the uniform measure on $S^{n-1}$, the fraction of the sphere with first coordinate at least $\varepsilon$ is $\int_\varepsilon^1(1-x^2)^{(n-3)/2}dx \big/ \int_{-1}^1(1-x^2)^{(n-3)/2}dx$. Its values, and Ball's bound $e^{-n\varepsilon^2/2}$:

| $n$ | $\varepsilon = 0.1$ | $\varepsilon = 0.2$ | $\varepsilon = 0.3$ | bound at $0.1$, $0.2$, $0.3$ |
| --- | --- | --- | --- | --- |
| 10 | $0.385$ | $0.278$ | $0.185$ | $0.951$, $0.819$, $0.638$ |
| 100 | $0.160$ | $0.0225$ | $1.152 \times 10^{-3}$ | $0.607$, $0.135$, $0.0111$ |
| 1000 | $7.679 \times 10^{-4}$ | $8.602 \times 10^{-11}$ | $1.448 \times 10^{-22}$ | $6.738 \times 10^{-3}$, $2.061 \times 10^{-9}$, $2.863 \times 10^{-20}$ |

In dimension 1000, less than one part in $10^{10}$ of the sphere has a coordinate above $0.2$ in a given direction.

### Where the method is weak: triangles

Let $T$ be the number of triangles in $G(n, 1/2)$, as a function of the $\binom n2$ independent edges. Changing one edge changes $T$ by up to $n - 2$, so $\sum c_e^2 = \binom n2(n-2)^2$. For $n = 1000$: $\mathbb{E}T = \binom{n}{3}/8 = 20770875$ and the exact standard deviation is $88226$. The bounded differences inequality gives the window $\pm 1148027$ at probability $0.99$, which is 5.5 percent of the mean but 13 standard deviations. The worst case change $n - 2$ is far above the typical change, which is about $n/4$. For sparse graphs, where $\mathbb{E}T$ is small, the method fails, and the upper tail of $T$ needs other tools (Dubhashi and Panconesi, Chapter 9).

## Where it is used

- **Analysis of randomized algorithms.** Load in [balls into bins](/balls-into-bins/) and in hashing, the running time of [randomized quicksort](/randomized-quicksort/) with [high probability](/high-probability-bounds/), [randomized rounding](/randomized-rounding/), and the number of rounds of distributed algorithms. Dubhashi and Panconesi is a book of such applications.
- **Random graphs.** Concentration of the chromatic number, the independence number and the clique number of $G(n, p)$, by vertex and edge exposure martingales (Alon and Spencer, Chapter 7).
- **Learning theory.** In [PAC learning](/pac-learning/) and [empirical risk minimization](/empirical-risk-minimization/), the largest gap between empirical and true error over a class is a function of the independent samples with bounded differences $1/m$. The bounded differences inequality makes it concentrate around its mean, which is then bounded with the [VC dimension](/vc-dimension/) or Rademacher averages.
- **High-dimensional geometry and data.** Random projections and the [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/), [nearest neighbor search](/nearest-neighbor-search/) in high dimension (where the distances to most points are nearly equal), and Dvoretzky's theorem on almost spherical sections of convex bodies (Ball, Lecture 9).
- **Probabilistic method.** Showing that a random structure has a property with probability close to 1, not only positive probability; see the [probabilistic method](/probabilistic-method/).

## References
