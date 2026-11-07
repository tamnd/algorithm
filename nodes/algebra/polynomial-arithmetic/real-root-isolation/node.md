---
tag: GQA31F
kind: problem
slug: real-root-isolation
name: Real root isolation
aliases:
- isolating intervals for real roots
- isolating real roots
- isolating real roots of polynomials
- real root isolation problem
area: algebra/polynomial-arithmetic
level: advanced
summary: Find disjoint intervals each containing exactly one real root of a polynomial.
model: multitape-turing-machine
complexity:
  vars: {n: the degree of f, L: the number of binary digits of the largest absolute value of a coefficient of f}
  time: {worst: O(n^5 (L + log n)^2)}
prereqs: [descartes-rule-of-signs, sturm-theorem, square-free-polynomial]
see_also: [vincent-collins-akritas, sturm-theorem, sturm-sequence, vincent-theorem, descartes-rule-of-signs, real-root-counting, polynomial-root-finding, cylindrical-algebraic-decomposition]
sources:
  - book: doi:10.1007/3-540-33099-2
    title: Saugata Basu, Richard Pollack and Marie-Francoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Chapter 10, Real Roots (Section 10.2, isolation of real roots with the Bernstein basis)
  - book: isbn:9780195125160
    title: Chee K. Yap, Fundamental Problems of Algorithmic Algebra, Oxford University Press, 2000
    locator: Chapter VII, Sturm Theory; Section 6.2 (root bounds) and Section 6.6 (root separation)
  - paper: doi:10.1145/800205.806346
    title: George E. Collins and Alkiviadis G. Akritas, Polynomial real root isolation using Descartes' rule of signs, SYMSAC 1976
    locator: pp. 272 to 275
  - paper: doi:10.1145/1145768.1145786
    title: Arno Eigenwillig, Vikram Sharma and Chee K. Yap, Almost tight recursion tree bounds for the Descartes method, ISSAC 2006
    locator: Corollary 3.5 and Theorems 4.1 and 4.2
  - paper: doi:10.1307/mmj/1028999140
    title: Kurt Mahler, An inequality for the discriminant of a polynomial, Michigan Mathematical Journal 11(3), 1964
    locator: pp. 257 to 262
  - paper: doi:10.1145/800206.806395
    title: Maurice Mignotte, Some inequalities about univariate polynomials, SYMSAC 1981
    locator: pp. 195 to 199
  - paper: doi:10.1006/jsco.2002.0531
    title: Victor Y. Pan, Univariate polynomials, nearly optimal algorithms for numerical factorization and root-finding, Journal of Symbolic Computation 33(5), 2002
    locator: pp. 701 to 733
  - paper: doi:10.1016/j.jsc.2015.03.004
    title: Michael Sagraloff and Kurt Mehlhorn, Computing real roots of real polynomials, Journal of Symbolic Computation 73, 2016
    locator: pp. 46 to 86
---

Real root isolation asks for a list of disjoint intervals with rational endpoints, one for each real root of a polynomial, such that each interval holds exactly one root. Such a list is an exact description of the real roots: each root is the unique root of $f$ in its interval, and the interval can be shrunk to any width afterwards. The classic exact methods use [Sturm's theorem](/sturm-theorem/) or [Descartes' rule of signs](/descartes-rule-of-signs/) to count roots in an interval and bisect until each count is $0$ or $1$; the size of the work depends on how close the roots are.

## In plain words

You are given a polynomial with whole-number or fraction coefficients, and you want to know where its real roots are, with no doubt and no rounding. You do not need the roots to many digits. You need, for each root, a small interval with simple fraction endpoints that holds that root and no other. From such intervals you can count the roots, sort them, compare them with other numbers, and make each interval as small as you like. The hard case is when two roots are very close together, because the intervals must then be very short to keep them apart.

## Definition

**Input.** A nonzero polynomial $f \in \mathbb{Q}[x]$ of degree $n$; after clearing denominators, $f \in \mathbb{Z}[x]$ with coefficients of at most $L$ binary digits.

**Output.** A list of items $J_1, \ldots, J_r$, where each item is either an open interval $(a_j, b_j)$ with rational $a_j < b_j$ or a single rational point $\{a_j\}$, such that

1. the items are pairwise disjoint;
2. each item contains exactly one real root of $f$;
3. every real root of $f$ lies in some item.

So $r$ is the number of distinct real roots. A point item is a rational root found exactly. Some methods return closed intervals instead, with the same conditions.

**Square-free reduction.** The roots of $f$ and of $f / \gcd(f, f')$ are the same, and the second polynomial is [square-free](/square-free-polynomial/). So it is enough to solve the problem for square-free inputs, and most algorithms assume this.

**Cost model.** Algorithms are compared by their bit cost on a [multitape Turing machine](/multitape-turing-machine/), as a function of $n$ and $L$, because the numbers grow during the computation. The bound in the front matter is the proved bound for the Descartes method with classical arithmetic; better bounds are listed under Bounds.

## Variants

- **Isolation in an interval.** Only the roots in a given interval $(a, b)$ are wanted. The Descartes method starts from $(a, b)$ instead of a root bound.
- **Refinement.** Each isolating interval must be shrunk below a width $2^{-\kappa}$. This is root approximation with a certified result, by bisection or by Newton steps on the isolated root.
- **Counting.** Only the number of real roots in an interval is wanted: [real root counting](/real-root-counting/), solved exactly by one Sturm count.
- **Complex root isolation.** Disjoint discs or boxes, one for each complex root; see [polynomial root finding](/polynomial-root-finding/).
- **Real coefficients.** The coefficients are real numbers given by approximations to any requested precision. Exact methods do not apply directly; Sagraloff and Mehlhorn (2016) solve this version for square-free inputs.
- **Systems and multivariate input.** The roots of a system, or the cells of [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/), reduce to isolating roots of univariate polynomials with real algebraic coefficients.

## Examples

- $f = x^3 - 3x + 1$: one answer is $(-4, 0)$, $(0, 1)$, $(1, 2)$. The roots are $2\cos(8\pi/9)$, $2\cos(4\pi/9)$ and $2\cos(2\pi/9)$, near $-1.879$, $0.347$ and $1.532$.
- $f = x^2 - 2$: one answer is $(-4, 0)$, $(0, 4)$, for $-\sqrt 2$ and $\sqrt 2$.
- $f = x^3 - x$: one answer is $(-2, 0)$, $\{0\}$, $(0, 2)$. The root $0$ is a midpoint, so it is reported exactly.
- $f = x^2 + 1$: the answer is the empty list, since there are no real roots.
- $f = x^2(x - 1)$: the square-free part is $x(x - 1)$, and one answer is $\{0\}$, $(0, 2)$. The double root is reported once.
- **Close roots.** Mignotte's polynomial $f = x^7 - 2(10x - 1)^2 = x^7 - 200x^2 + 40x - 2$ has two roots near $0.0999777$ and $0.1000224$, only about $4.5 \cdot 10^{-5}$ apart, and a third near $2.844$. The [Vincent-Collins-Akritas](/vincent-collins-akritas/) method returns $(819/8192, 3277/32768)$, $(3277/32768, 1639/16384)$ and $(2, 4)$. The first two intervals have length about $3 \cdot 10^{-5}$.

All outputs above are those of the implementation on the Vincent-Collins-Akritas page, checked by its tests.

## Known algorithms

| algorithm | count used | idea |
|---|---|---|
| Sturm bisection | [Sturm sequence](/sturm-sequence/), exact | bisect until each count is $0$ or $1$ |
| [Vincent-Collins-Akritas](/vincent-collins-akritas/) (Descartes method) | Descartes' rule after a Möbius map, an upper bound | bisect until each count is $0$ or $1$ |
| continued fraction method (VAS) | Descartes' rule | follow the [continued fraction](/continued-fraction/) of each root, with [Vincent's theorem](/vincent-theorem/) for termination |
| Bernstein basis method | Descartes' rule in the Bernstein basis | de Casteljau subdivision instead of Taylor shifts |
| numerical methods with certification | complex root approximation | Pan (2002) approximates all complex roots with nearly optimal cost, then the real ones are selected |
| Descartes with Newton steps | Descartes' rule | Sagraloff and Mehlhorn (2016) speed up the convergence to clusters of roots |

The Sturm method needs a remainder sequence with large coefficients; the Descartes method needs only Taylor shifts and is usually faster in practice. Eigenwillig, Sharma and Yap (2006) show that the Descartes method has the same bound on the number of bisection steps as Sturm bisection.

## Bounds

- **Root bound.** Every root satisfies $|\alpha| < 1 + \max_{i<n} |f_i/f_n|$ ([Cauchy's bound](/cauchy-root-bound/)), so a starting interval of length $2^{O(L)}$ holds all real roots. Yap, Section 6.2, gives this and sharper bounds.
- **Root separation.** For a square-free $f$ of degree $n \ge 2$ with discriminant $\operatorname{disc}(f)$ and Mahler measure $\mathrm{M}(f)$, Mahler (1964) proved $\operatorname{sep}(f) > \sqrt{3 |\operatorname{disc}(f)|}\; n^{-(n+2)/2}\, \mathrm{M}(f)^{-(n-1)}$. For integer $f$, $|\operatorname{disc}(f)| \ge 1$ and $\mathrm{M}(f) \le \|f\|_2 \le \sqrt{n+1}\, 2^L$, so $\log_2(1/\operatorname{sep}(f)) = O(n(L + \log n))$. The endpoints of an isolating list need about this many binary digits in the worst case.
- **Close roots exist.** Mignotte (1981) gave the family $x^n - 2(ax - 1)^2$ with two real roots at distance less than $2a^{-(n+2)/2}$, so the separation can be exponentially small in $n$ and the bound above is close to the truth.
- **Tree size.** The Descartes method and Sturm bisection both use $O(n(L + \log n))$ subdivisions for square-free integer polynomials, and this is tight for $L = \Omega(\log n)$ (Eigenwillig, Sharma and Yap, 2006, Corollary 3.5).
- **Bit cost.** The Descartes method costs $O(n^5 (L + \log n)^2)$ bit operations with classical arithmetic (Eigenwillig, Sharma and Yap, Theorem 4.1), and $n^4 (L + \log n)^2$ up to logarithmic factors with a fast Taylor shift (their Theorem 4.2). Numerical methods built on Pan's algorithm, and the method of Sagraloff and Mehlhorn, have lower bounds still, close to the size of the output in the worst case.
- **Lower bound.** Any method must read the input, of size about $nL$ binary digits. For Mignotte's family the two close roots force an endpoint with about $(n/2)\log_2 a$ binary digits, so the output can also have size $\Omega(n L)$. No lower bound that matches the upper bounds above is known for the exact methods.

## Reductions

- **To square-free inputs.** Replace $f$ by $f / \gcd(f, f')$ with the [polynomial gcd](/polynomial-gcd/); the roots and the answer are the same.
- **To positive roots.** The roots of $f$ in $(a, b)$ are the images of the positive roots of $(y + 1)^n f((ay + b)/(y + 1))$, so counting in an interval reduces to counting positive roots, which is where Descartes' rule applies.
- **From counting.** An exact root count for intervals, such as Sturm's, gives isolation by bisection, and the number of steps is bounded by the separation bound.
- **From complex root isolation.** Certified discs for all complex roots, small enough to be disjoint and to decide which meet the real line, give real root isolation.
- **To refinement.** Isolating intervals turn root approximation into a safe local problem: in an isolating interval with a sign change, bisection or Newton steps converge to the one root.

## Applications

- [Cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) and [quantifier elimination](/quantifier-elimination/) over the reals: the sample points of the cells are real algebraic numbers given by isolating intervals.
- Exact representation of real algebraic numbers: a pair of a square-free polynomial and an isolating interval names one root, and comparisons and signs are computed by refining the intervals.
- Exact geometric computation: the intersections of curves, the topology of a plane curve and the arrangement of algebraic curves need certified roots of univariate polynomials.
- Solving polynomial systems: after elimination with [resultants](/resultant/) or Gröbner bases, the real solutions come from isolating the real roots of univariate polynomials.

## References
