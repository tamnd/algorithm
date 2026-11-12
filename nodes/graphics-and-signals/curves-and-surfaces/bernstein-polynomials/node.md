---
tag: HJJM56
kind: definition
slug: bernstein-polynomials
name: Bernstein polynomials
aliases:
- Bernstein basis
area: graphics-and-signals/curves-and-surfaces
level: intro
summary: The n + 1 polynomials C(n, i) t^i (1 - t)^(n - i) of degree n. On [0, 1] they are nonnegative and sum to 1, and they are the basis of Bezier curves.
prereqs: [polynomial, binomial-coefficient]
see_also: [bezier-curve, de-casteljau-algorithm, bernstein-approximation-theorem, b-spline, partition-of-unity, binomial-distribution, chebyshev-polynomials, polynomial-evaluation]
sources:
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 5, The Bernstein Form of a Bezier Curve (the basis, its properties, derivatives and the conversion to the power form)
  - book: isbn:9783540437611
    title: Hartmut Prautzsch, Wolfgang Boehm and Marco Paluszny, Bezier and B-Spline Techniques, Springer, 2002
    locator: Section 2.1, Bernstein polynomials (page 9), and Sections 2.8 and 2.9 on the conversion between the Bernstein and the monomial form
  - paper: "Sergei N. Bernstein, Démonstration du théorème de Weierstrass fondée sur le calcul des probabilités, Communications de la Société Mathématique de Kharkow, series 2, 13 (1912) 1-2"
    locator: the polynomials C(n, k) x^k (1 - x)^(n - k) as binomial probabilities, used to approximate a continuous function
  - paper: doi:10.1016/j.cagd.2012.03.001
    title: Rida T. Farouki, The Bernstein polynomial basis, a centennial retrospective, Computer Aided Geometric Design 29(6), 379-419 (2012)
    locator: the history of the basis from Bernstein to Bezier and de Casteljau, its properties, and its numerical stability
  - paper: doi:10.1016/0167-8396(87)90012-4
    title: Rida T. Farouki and V. T. Rajan, On the numerical condition of polynomials in Bernstein form, Computer Aided Geometric Design 4(3), 191-216 (1987)
    locator: the condition numbers of values and roots of a polynomial in the Bernstein and in the power form on [0, 1]
---

The Bernstein polynomials of degree $n$ are the $n + 1$ [polynomials](/polynomial/) $B_i^n(t) = \binom{n}{i} t^i (1 - t)^{n - i}$ for $i = 0, \dots, n$. They form a basis of the polynomials of degree at most $n$. On $[0, 1]$ they are nonnegative and their sum is 1, so a sum $\sum_i P_i B_i^n(t)$ of points is a weighted average of the points. This is why they are the basis of [Bézier curves](/bezier-curve/), and why Bernstein could use them in 1912 for a proof of the Weierstrass theorem by probability.

## Definition

For an integer $n \ge 0$ and $i \in \{0, \dots, n\}$, the Bernstein polynomial of degree $n$ and index $i$ is

$$B_i^n(t) = \binom{n}{i} t^i (1 - t)^{n - i},$$

with the [binomial coefficient](/binomial-coefficient/) $\binom{n}{i}$ and the convention $0^0 = 1$. Set $B_i^n = 0$ when $i < 0$ or $i > n$. The variable $t$ is real; the interesting domain is $[0, 1]$. For an interval $[a, b]$ with $a < b$, use $B_i^n((x - a)/(b - a))$.

A polynomial $p$ of degree at most $n$ in the form $p(t) = \sum_{i=0}^n c_i B_i^n(t)$ is in Bernstein form of degree $n$, and $c_0, \dots, c_n$ are its Bernstein coefficients. A curve $\sum_i P_i B_i^n(t)$ with points $P_i$ is a Bézier curve with [control points](/control-points/) $P_i$.

The basis has these properties. Each proof uses only the definition, the [binomial theorem](/binomial-theorem/) and Pascal's rule.

1. **Partition of unity.** $\sum_{i=0}^n B_i^n(t) = (t + (1 - t))^n = 1$ for all real $t$, by the binomial theorem. See [partition of unity](/partition-of-unity/).
2. **Sign.** $B_i^n(t) \ge 0$ for $t \in [0, 1]$, and $B_i^n(t) > 0$ for $t \in (0, 1)$, because each factor is nonnegative there.
3. **End values.** $B_i^n(0) = 1$ if $i = 0$ and 0 otherwise; $B_i^n(1) = 1$ if $i = n$ and 0 otherwise.
4. **Symmetry.** $B_i^n(t) = B_{n-i}^n(1 - t)$, because $\binom{n}{i} = \binom{n}{n-i}$.
5. **Recursion.** $B_i^n(t) = (1 - t) B_i^{n-1}(t) + t B_{i-1}^{n-1}(t)$ for $n \ge 1$. Proof: by Pascal's rule $\binom{n}{i} = \binom{n-1}{i} + \binom{n-1}{i-1}$, and $\binom{n-1}{i} t^i (1-t)^{n-i} = (1 - t) B_i^{n-1}(t)$, $\binom{n-1}{i-1} t^i (1 - t)^{n-i} = t B_{i-1}^{n-1}(t)$. This recursion is the [de Casteljau algorithm](/de-casteljau-algorithm/) read backwards.
6. **Derivative.** $\frac{d}{dt} B_i^n(t) = n \left(B_{i-1}^{n-1}(t) - B_i^{n-1}(t)\right)$ for $n \ge 1$. Proof: the product rule gives $\binom{n}{i}\left(i t^{i-1}(1-t)^{n-i} - (n - i) t^i (1-t)^{n-i-1}\right)$, and $\binom{n}{i} i = n \binom{n-1}{i-1}$, $\binom{n}{i}(n - i) = n \binom{n-1}{i}$.
7. **Basis and change of basis.** Expanding $(1 - t)^{n-i}$ by the binomial theorem and using $\binom{n}{i}\binom{n-i}{k-i} = \binom{n}{k}\binom{k}{i}$ gives
$$B_i^n(t) = \sum_{k=i}^{n} (-1)^{k-i} \binom{n}{k} \binom{k}{i} t^k.$$
In the other direction, $t^k = t^k (t + (1 - t))^{n-k}$, and the same identity gives
$$t^k = \sum_{i=k}^{n} \frac{\binom{i}{k}}{\binom{n}{k}} B_i^n(t), \qquad 0 \le k \le n.$$
So the $n + 1$ polynomials span all polynomials of degree at most $n$, a space of dimension $n + 1$, and they are a basis. The case $k = 1$ gives $t = \sum_i \frac{i}{n} B_i^n(t)$ (linear precision).
8. **Maximum.** For $0 < i < n$, $\frac{d}{dt}\, t^i (1 - t)^{n-i} = t^{i-1} (1 - t)^{n-i-1} (i - n t)$, so on $[0, 1]$ the polynomial $B_i^n$ rises up to $t = i/n$ and falls after it. Its unique maximum on $[0, 1]$ is at $t = i/n$. For $i = 0$ and $i = n$ the maximum is at the end point $0$ or $1$.
9. **Integral.** $\int_0^1 B_i^n(t)\,dt = \frac{1}{n+1}$. Proof: for $1 \le i \le n$, property 3 gives $B_i^{n+1}(1) - B_i^{n+1}(0) = 0$, and by property 6 this difference is $(n + 1)\left(\int_0^1 B_{i-1}^n - \int_0^1 B_i^n\right)$. So all $n + 1$ integrals are equal, and by property 1 they sum to 1.
10. **Degree elevation.** $B_i^n = \frac{n + 1 - i}{n + 1} B_i^{n+1} + \frac{i + 1}{n + 1} B_{i+1}^{n+1}$. Proof: write $B_i^n = (1 - t) B_i^n + t B_i^n$. Then $(1 - t) B_i^n = \binom{n}{i} t^i (1 - t)^{n+1-i} = \frac{\binom{n}{i}}{\binom{n+1}{i}} B_i^{n+1}$, and $\binom{n}{i} / \binom{n+1}{i} = \frac{n + 1 - i}{n + 1}$. In the same way $t B_i^n = \frac{\binom{n}{i}}{\binom{n+1}{i+1}} B_{i+1}^{n+1}$ with ratio $\frac{i+1}{n+1}$.
11. **Probability.** For $t \in [0, 1]$, $B_i^n(t)$ is the probability of exactly $i$ successes in $n$ independent trials with success probability $t$. So $(B_0^n(t), \dots, B_n^n(t))$ is the [binomial distribution](/binomial-distribution/) with parameters $n$ and $t$. This is Bernstein's view of 1912.

The cost model is the real RAM with exact arithmetic, and the unit is one arithmetic operation. All $n + 1$ values $B_i^n(t)$ at one $t$ cost $O(n^2)$ operations by the recursion of property 5, or $O(n)$ by the ratio $B_{i+1}^n(t) / B_i^n(t) = \frac{n - i}{i + 1} \cdot \frac{t}{1 - t}$ for $t \ne 1$. To evaluate a polynomial in Bernstein form, see [curve evaluation](/curve-evaluation/).

The Bernstein form is better conditioned than the power form on $[0, 1]$. Farouki and Rajan (1987) compare the condition numbers of the value and of the roots in the two forms. They show that for $t \in [0, 1]$, the condition number of $p(t)$ in the Bernstein form is at most its condition number in the power form. The [de Casteljau algorithm](/de-casteljau-algorithm/) gives a matching small rounding error.

## Examples and non-examples

- **Degree 1.** $B_0^1(t) = 1 - t$ and $B_1^1(t) = t$. A curve $P_0 B_0^1 + P_1 B_1^1$ is the segment from $P_0$ to $P_1$, so linear interpolation is the Bernstein form of degree 1.
- **Degree 3 at $t = 1/2$ and $t = 1/4$.** At $t = 1/2$ the values are $1/8, 3/8, 3/8, 1/8$. At $t = 1/4$ they are $27/64, 27/64, 9/64, 1/64$. Each list sums to 1, and the first list is symmetric, as property 4 says.
- **Change of basis.** The cubic $p(t) = -9t^3 + 12t^2 - 1$ has the power coefficients $(a_0, a_1, a_2, a_3) = (-1, 0, 12, -9)$. By property 7, its Bernstein coefficient $c_i$ is $\sum_{k \le i} a_k \binom{i}{k} / \binom{3}{k}$. This gives $c_0 = -1$, $c_1 = -1$, $c_2 = -1 + 12/3 = 3$ and $c_3 = -1 + 12 - 9 = 2$. The coefficients change sign once, and $p$ has exactly one root in $[0, 1]$, at $t = 1/3$. The page on [Bézier clipping](/bezier-clipping/) finds this root from the coefficients $(-1, -1, 3, 2)$.
- **The maximum.** $B_1^2(t) = 2t(1 - t)$ has its maximum $1/2$ at $t = 1/2 = i/n$.
- **Non-example: outside $[0, 1]$.** $B_1^2(2) = 2 \cdot 2 \cdot (-1) = -4$. The partition of unity still holds ($B_0^2(2) + B_1^2(2) + B_2^2(2) = 1 - 4 + 4 = 1$), but a value is negative, so a sum $\sum P_i B_i^n(2)$ is not a weighted average of the points. The [convex hull property](/convex-hull-property/) holds only for $t \in [0, 1]$.
- **Non-example: not an interpolation basis.** $B_1^2(1/2) = 1/2$, not 1, and $B_0^2(1/2) = 1/4$, not 0. So the Bernstein coefficients of $p$ are not the values $p(i/n)$ in general, and a Bézier curve does not pass through its inner control points. The basis with $\ell_i(t_j) = \delta_{ij}$ is the Lagrange basis of [Lagrange interpolation](/lagrange-interpolation/).
- **Non-example: other objects with the same name.** The Bernstein operator $f \mapsto \sum_k f(k/n) B_k^n$ uses this basis, and it is the subject of the [Bernstein approximation theorem](/bernstein-approximation-theorem/). The Bernstein-Sato polynomial of algebraic analysis and Bernstein's inequality for derivatives of polynomials are different things.

## Related definitions

- A [Bézier curve](/bezier-curve/) is a Bernstein form with points as coefficients. A [rational Bézier curve](/rational-bezier-curve/) divides a weighted Bernstein form by the Bernstein form of the weights.
- The [B-spline](/b-spline/) basis is the piecewise generalization. On the knot vector with $n + 1$ knots at 0 and $n + 1$ knots at 1, the B-splines of degree $n$ are the Bernstein polynomials of degree $n$.
- The [partition of unity](/partition-of-unity/) and nonnegativity give the [convex hull property](/convex-hull-property/). The [variation diminishing property](/variation-diminishing-property/) is the statement that $\sum c_i B_i^n$ has no more roots in $(0, 1)$ than the sequence $c_i$ has sign changes; it is [Descartes' rule of signs](/descartes-rule-of-signs/) after the change of variable $s = t / (1 - t)$.
- The [Bernstein approximation theorem](/bernstein-approximation-theorem/) and the [Weierstrass approximation theorem](/weierstrass-approximation-theorem/) use the basis to approximate continuous functions.
- [Chebyshev polynomials](/chebyshev-polynomials/) are another basis of the same space. They are the better basis for minimax approximation, and the Bernstein basis is the better basis for geometric control.

## References
