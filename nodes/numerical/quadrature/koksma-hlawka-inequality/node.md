---
tag: F9GMY1
kind: theorem
slug: koksma-hlawka-inequality
name: Koksma-Hlawka inequality
aliases:
- Koksma-Hlawka theorem
- Koksma inequality
- Hlawka-Zaremba identity
area: numerical/quadrature
level: research
summary: Bounds quasi-Monte Carlo error by the star discrepancy times the variation of the integrand.
prereqs: [discrepancy]
see_also: [quasi-monte-carlo-integration, discrepancy, halton-sequence, sobol-sequence, monte-carlo-integration, multidimensional-integration, peano-kernel-theorem, quadrature-error]
sources:
  - book: isbn:9780898712957
    title: Harald Niederreiter, Random Number Generation and Quasi-Monte Carlo Methods, SIAM, CBMS-NSF Regional Conference Series in Applied Mathematics 63, 1992
    locator: Chapter 2, Section 2.1 (Theorem 2.6, the exact formula for the one-dimensional star discrepancy) and Section 2.2 (Theorem 2.9, Koksma's inequality; Theorem 2.11, the Koksma-Hlawka inequality)
  - book: isbn:9780521191593
    title: Josef Dick and Friedrich Pillichshammer, Digital Nets and Sequences, Cambridge University Press, 2010
    locator: Chapter 2, Quasi-Monte Carlo integration, discrepancy and reproducing kernel Hilbert spaces (the Hlawka-Zaremba identity and the Koksma-Hlawka inequality); Chapter 3 (the lower bound of Roth)
  - paper: "J. F. Koksma, Een algemeene stelling uit de theorie der gelijkmatige verdeeling modulo 1, Mathematica B (Zutphen) 11, 1942, 7-11"
    locator: the one-dimensional inequality
  - paper: "Edmund Hlawka, Funktionen von beschränkter Variation in der Theorie der Gleichverteilung, Annali di Matematica Pura ed Applicata 54, 1961, 325-333"
    locator: the inequality in s dimensions with the Hardy-Krause variation
  - paper: "S. K. Zaremba, Some applications of multidimensional integration by parts, Annales Polonici Mathematici 21, 1968, 85-96"
    locator: the integration by parts identity and its L^2 form
  - paper: "Art B. Owen, Multidimensional variation for quasi-Monte Carlo, in Contemporary Multivariate Analysis and Design of Experiments, World Scientific, 2005, 49-74"
    locator: the Vitali and Hardy-Krause variations, and integrands of infinite variation
  - paper: "K. F. Roth, On irregularities of distribution, Mathematika 1, 1954, 73-79"
    locator: the lower bound of order (log N)^((s-1)/2) / N for the L^2 and star discrepancy
---

## Statement

For points $P = \{x_1, \ldots, x_N\} \subset [0, 1)^s$ and $t \in [0, 1]^s$, let $A(t) = \#\{i : x_i \in [0, t)\}$ with $[0, t) = \prod_k [0, t_k)$, let the *local discrepancy* be $\Delta(t) = A(t)/N - t_1 t_2 \cdots t_s$, and let the *star discrepancy* be $D_N^*(P) = \sup_{t \in [0,1]^s} |\Delta(t)|$. For a nonempty $u \subseteq \{1, \ldots, s\}$ and $t \in [0,1]^s$ write $(t_u, 1)$ for the point with coordinates $t_k$ for $k \in u$ and $1$ otherwise, and $\partial^u f = \partial^{|u|} f / \prod_{k \in u} \partial x_k$.

**Theorem (Koksma 1942 for $s = 1$, Hlawka 1961).** Let $f : [0, 1]^s \to \mathbb{R}$ have continuous mixed partial derivatives $\partial^u f$ for every $u \subseteq \{1, \ldots, s\}$. Then the *Hlawka-Zaremba identity*

$$\frac{1}{N}\sum_{i=1}^N f(x_i) - \int_{[0,1]^s} f(x)\,dx = \sum_{\emptyset \ne u \subseteq \{1..s\}} (-1)^{|u|} \int_{[0,1]^{|u|}} \Delta(t_u, 1)\, \partial^u f(t_u, 1)\,dt_u$$

holds, and consequently

$$\Big|\frac{1}{N}\sum_{i=1}^N f(x_i) - \int_{[0,1]^s} f\Big| \le V_{HK}(f)\, D_N^*(P), \qquad V_{HK}(f) = \sum_{\emptyset \ne u} \int_{[0,1]^{|u|}} \big|\partial^u f(t_u, 1)\big|\,dt_u .$$

$V_{HK}(f)$ is the variation of $f$ in the sense of Hardy and Krause (anchored at $1$), written here for smooth $f$. The inequality holds, with the general definition of $V_{HK}$, for every $f$ of bounded Hardy-Krause variation (Niederreiter 1992, Theorem 2.11). The result is a deterministic bound; it is **proved** below for smooth $f$ and cited for general $f$.

For $s = 1$ it reads $|\frac1N \sum f(x_i) - \int_0^1 f| \le D_N^* \int_0^1 |f'|$, with $\int_0^1 |f'|$ the total variation of $f$.

## In plain words

Quasi-Monte Carlo replaces random points by points that are spread out as evenly as possible. This theorem explains why that works and how well. It splits the error into two factors that have nothing to do with each other.

One factor measures the points: look at every box that has a corner at the origin, compare the fraction of points inside it with the box's volume, and take the worst mismatch. The other factor measures the function: how much it wiggles, added up along every coordinate and every combination of coordinates. The error is at most the product. So well-spread points give a small error for every function that does not wiggle too much, and the bound is the best possible of its kind.

## Proof

**Step 1 (one dimension).** Let $s = 1$ and $f \in C^1[0, 1]$. For $x \in [0, 1]$, $f(x) = f(1) - \int_x^1 f'(t)\,dt = f(1) - \int_0^1 \mathbf{1}[x < t]\, f'(t)\,dt$. Average this over the points and, separately, integrate it over $x \in [0, 1]$, using Fubini's theorem (the integrand is bounded):

$$\frac1N\sum_i f(x_i) = f(1) - \int_0^1 \frac{A(t)}{N} f'(t)\,dt, \qquad \int_0^1 f = f(1) - \int_0^1 t\, f'(t)\,dt,$$

because $\frac1N \#\{i : x_i < t\} = A(t)/N$ and $\int_0^1 \mathbf{1}[x < t]\,dx = t$. Subtracting, the error is $-\int_0^1 \Delta(t) f'(t)\,dt$, which is the identity for $s = 1$, and $|\int \Delta f'| \le \sup|\Delta| \int |f'| = D_N^* \int|f'|$.

**Step 2 (the anchored expansion).** For $f$ as in the theorem and every $x \in [0, 1]^s$,

$$f(x) = \sum_{u \subseteq \{1..s\}} (-1)^{|u|} \int_{[0,1]^{|u|}} \Big(\prod_{k \in u} \mathbf{1}[x_k < t_k]\Big)\, \partial^u f(t_u, 1)\,dt_u, \tag{1}$$

where the term $u = \emptyset$ is $f(1, \ldots, 1)$. *Proof by induction on $s$.* For $s = 1$ this is the formula of Step 1. For $s > 1$, apply the one-dimensional formula in the last coordinate: $f(x) = f(x', 1) - \int_0^1 \mathbf{1}[x_s < t_s]\, \partial_s f(x', t_s)\,dt_s$ with $x' = (x_1, \ldots, x_{s-1})$. Apply the induction hypothesis in $x'$ to the function $f(\cdot, 1)$ and, for each fixed $t_s$, to $\partial_s f(\cdot, t_s)$; both have continuous mixed derivatives in $x'$. The first gives the terms of (1) with $s \notin u$; the second, after moving the $t_s$ integral inside (Fubini, all integrands bounded), gives those with $s \in u$, the extra minus sign supplying the factor for $s$. $\square$

**Step 3 (the identity).** Average (1) over the points and integrate it over $[0,1]^s$, exchanging sums and integrals as in Step 1. For a fixed $u$ and $t_u$, the average of $\prod_{k \in u} \mathbf{1}[x_{i,k} < t_k]$ over $i$ is $A(t_u, 1)/N$, because a coordinate $x_{i,k} \in [0, 1)$ always satisfies $x_{i,k} < 1$; and the integral of the same product over $x \in [0, 1]^s$ is $\prod_{k \in u} t_k$, the volume of $[0, (t_u, 1))$. The difference is $\Delta(t_u, 1)$. The terms with $u = \emptyset$ are $f(1)$ in both and cancel. This is the identity.

**Step 4 (the inequality).** Each $|\Delta(t_u, 1)| \le D_N^*$ since $(t_u, 1) \in [0, 1]^s$, so the absolute value of the right side is at most $D_N^* \sum_{u \ne \emptyset} \int |\partial^u f(t_u, 1)|\,dt_u = D_N^*\, V_{HK}(f)$. $\blacksquare$

## Consequences

- **Rates for quasi-Monte Carlo.** The first $N$ points of the [Halton sequence](/halton-sequence/) in $s$ dimensions have $D_N^* = O((\log N)^s / N)$ (Halton 1960), and [Sobol](/sobol-sequence/) and other $(t, s)$-sequences have the same order (Niederreiter 1992, Chapter 4). So for every $f$ with $V_{HK}(f) < \infty$, [quasi-Monte Carlo integration](/quasi-monte-carlo-integration/) has deterministic error $O((\log N)^s/N)$, against the probabilistic $\sigma N^{-1/2}$ of [Monte Carlo](/monte-carlo-integration/).
- **Separation of concerns.** Point sets are designed and compared by $D_N^*$ alone, independently of the integrand, and integrands by $V_{HK}$ alone.
- **A numerical check.** For $f(x, y) = e^{x + y}$ on $[0, 1]^2$, $V_{HK}(f) = 2e(e - 1) + (e - 1)^2 = (e - 1)(3e - 1) = 12.29$. With the first $N$ points of the Halton sequence in bases 2 and 3 (indices $1..N$) and with $N$ pseudo-random points (seed 1), computed exactly by checking all boxes with corners at point coordinates:

| $N$ | points | $D_N^*$ | error | bound $V_{HK} D_N^*$ |
|---|---|---|---|---|
| 100 | Halton | 0.0502 | $7.1 \times 10^{-2}$ | 0.62 |
| 100 | random | 0.1057 | $7.4 \times 10^{-2}$ | 1.30 |
| 1000 | Halton | 0.0068 | $8.9 \times 10^{-3}$ | 0.084 |
| 1000 | random | 0.0359 | $1.8 \times 10^{-2}$ | 0.44 |

The bound holds and is pessimistic by a factor of about 10, as is typical: the identity integrates $\Delta$ against $\partial^u f$, and $\Delta$ changes sign.

- **The $L^2$ form (Zaremba).** By Cauchy-Schwarz in the identity, $|E| \le \sum_u \|\Delta(\cdot_u, 1)\|_{L^2} \|\partial^u f(\cdot_u, 1)\|_{L^2}$, which involves the $L^2$ discrepancy, computable in $O(s N^2)$ by Warnock's formula, instead of the star discrepancy, which is hard to compute in high dimension.
- **Kernel view.** The identity says that the worst-case error in a reproducing kernel Hilbert space with a suitable kernel is a discrepancy; this is the starting point of weighted spaces and of tractability results where the error bound does not grow with $s$ (Dick and Pillichshammer 2010, Chapter 2).

## Tightness

- **The constant 1 is optimal (proved for $s = 1$).** For any points and any $t \in (0, 1]$, the step function $f = \mathbf{1}_{[0, t)}$ has total variation 1 and error $A(t)/N - t = \Delta(t)$. Taking $t$ where $|\Delta|$ is nearly maximal gives an error arbitrarily close to $D_N^*\, V(f)$. In $s$ dimensions the indicator of $[0, t)$ with all $t_k < 1$ has Hardy-Krause variation 1 in the general definition, and the same argument applies. Smooth approximations of these step functions show that the bound is also sharp within the smooth class.
- **The point factor cannot be made small faster than about $1/N$.** In one dimension $D_N^* = \frac{1}{2N} + \max_i |x_{(i)} - \frac{2i - 1}{2N}|$ for the sorted points $x_{(i)}$ (Niederreiter 1992, Theorem 2.6), so $D_N^* \ge \frac{1}{2N}$ with equality exactly for the midpoint set. In $s \ge 2$ dimensions every $N$-point set has $D_N^* \ge c_s (\log N)^{(s-1)/2}/N$ (Roth 1954). So no point set makes the Koksma-Hlawka bound decay faster than $N^{-1}$ times a logarithmic factor.
- **The function factor is often infinite.** $V_{HK}(f) = \infty$ for many simple integrands in $s \ge 2$: the indicator of the triangle $\{x_1 + x_2 \le 1\}$, and, in $s = 3$, functions with a kink along a plane that is not parallel to the axes, such as $\max(x_1 + x_2 + x_3 - 1, 0)$, whose third mixed derivative is the derivative of a point mass on the plane (Owen 2005). For these the inequality says nothing, although quasi-Monte Carlo may still beat Monte Carlo.
- **Pessimism in high dimension.** $(\log N)^s/N$ increases with $N$ until $N \approx e^s$, so for $s = 50$ the bound is useless at every practical $N$, even though quasi-Monte Carlo often works well there. Weighted discrepancies explain this when later coordinates matter less.

## History

Jurjen Koksma proved the one-dimensional inequality in 1942, in the theory of uniform distribution modulo 1. Edmund Hlawka extended it to $s$ dimensions in 1961, using the variation of Hardy and Krause, which had been introduced for double Fourier series early in the twentieth century. Stanisław Zaremba (1968) gave the integration by parts identity behind it and its $L^2$ version. Klaus Roth's 1954 lower bound and the constructions of Halton (1960), Sobol (1967) and Niederreiter (1980s) set the achievable rates, and Niederreiter's 1992 monograph made the inequality the standard justification of quasi-Monte Carlo methods.

## References
