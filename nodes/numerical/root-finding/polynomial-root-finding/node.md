---
tag: R6FW33
kind: problem
slug: polynomial-root-finding
name: Polynomial root finding
aliases:
- polynomial zeros
- computing polynomial roots
- polynomial factorization over C
area: numerical/root-finding
level: core
summary: Given the coefficients of a polynomial of degree n, find all or some of its n complex roots, counted with multiplicity, to a stated accuracy.
prereqs: [root-finding-problem, fundamental-theorem-of-algebra, horner-rule]
see_also: [companion-matrix-method, aberth-ehrlich-method, jenkins-traub-algorithm, laguerre-method, polynomial-deflation, root-conditioning, wilkinson-polynomial, real-root-counting]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 5.1, Horner's method (the running error bound of a computed polynomial value)
  - book: "J. H. Wilkinson, Rounding Errors in Algebraic Processes, Prentice-Hall, 1963 (reprinted by Dover, 1994)"
    locator: Chapter 2, Computations involving polynomials (the sensitivity of the zeros and the perturbation of the twentieth-degree polynomial)
  - paper: doi:10.1137/S0036144595288554
    title: V. Y. Pan, Solving a polynomial equation, some history and recent progress, SIAM Review 39(2) (1997) 187-220
    locator: the survey of methods and of their complexity
  - paper: "A. Edelman and H. Murakami, Polynomial roots from companion matrix eigenvalues, Mathematics of Computation 64 (1995) 763-776"
    locator: the backward error of the companion matrix method in terms of the coefficients
  - paper: "D. A. Bini and G. Fiorentino, Design, analysis, and implementation of a multiprecision polynomial rootfinder, Numerical Algorithms 23 (2000) 127-173"
    locator: the Aberth iteration with inclusion discs in MPSolve
---

Polynomial root finding asks for the roots of $p(x) = a_n x^n + \cdots + a_1 x + a_0$, $a_n \ne 0$, given its coefficients. By the [fundamental theorem of algebra](/fundamental-theorem-of-algebra/) there are exactly $n$ complex roots counted with multiplicity, and by the [Abel-Ruffini theorem](/abel-ruffini-theorem/) there is no formula in radicals for $n \ge 5$, so for large $n$ the roots are computed numerically. Two facts shape every method. The roots are continuous functions of the coefficients but can be extremely sensitive to them, as [Wilkinson's polynomial](/wilkinson-polynomial/) shows. And because all $n$ roots are wanted, the methods either find them one at a time and divide them out, or iterate on all of them at once, or compute them as the eigenvalues of a matrix.

## In plain words

A polynomial is a sum of powers of $x$ with given numbers in front. Its roots are the values of $x$ that make it zero, and a polynomial of degree $n$ has exactly $n$ of them if complex numbers and repeats are allowed. For degree two there is the school formula, and for three and four there are longer formulas, but from degree five on no such formula exists. So computers find the roots by iteration. The hard part is that tiny changes in the numbers in front can move some roots a long way, so the best one can ask is the exact roots of a polynomial whose coefficients are very close to the given ones.

## Definition

**Input.** The coefficients $a_0, \ldots, a_n$ of $p$, real or complex, with $a_n \ne 0$; in exact versions they are integers or rationals.

**Output.** Approximations $\hat x_1, \ldots, \hat x_n$ of the roots $x_1, \ldots, x_n$ with multiplicity, so that $p(x) = a_n \prod (x - x_i)$. Accuracy is stated in one of three ways: forward, $|\hat x_i - x_{\pi(i)}| \le \tau$ for a matching $\pi$; backward, the $\hat x_i$ are the exact roots of a polynomial with coefficients $a_j(1 + \epsilon_j)$, $|\epsilon_j| \le \eta$; or certified, with discs that each provably contain a stated number of roots.

**Partial versions.** Find the real roots only, the roots in a region, the root of largest modulus, or one root near a starting point.

Notation on the root-finding pages: $x^*$ is a root, $m$ its multiplicity, and $u$ the unit roundoff. For a simple root, the relative condition number with respect to relative changes in the coefficients is
$$\kappa(x^*) = \frac{\sum_j |a_j|\,|x^*|^j}{|x^*|\,|p'(x^*)|},$$
see [root conditioning](/root-conditioning/).

## Variants

- **Real roots of real or integer polynomials.** Count and isolate them exactly with [Sturm sequences](/sturm-sequence/), [Descartes' rule of signs](/descartes-rule-of-signs/) and the [Vincent-Collins-Akritas method](/vincent-collins-akritas/); see [real root counting](/real-root-counting/) and [real root isolation](/real-root-isolation/).
- **Rational roots of integer polynomials.** The [rational root theorem](/rational-root-theorem/) gives a finite list of candidates.
- **Roots in a region.** Count the roots in the unit disc with the [Schur-Cohn test](/schur-cohn-test/), or in any disc, and search by subdivision ([Lehmer-Schur method](/lehmer-schur-method/)).
- **Other bases.** Polynomials given in the Chebyshev or Bernstein basis or by values at points are often better conditioned, and have their own colleague and comrade matrices.
- **Multiple roots.** Compute the [square-free factorization](/square-free-factorization/) first in exact arithmetic, or find clusters numerically.

## Examples

| polynomial | roots | remark |
|---|---|---|
| $x^2 - 2$ | $\pm\sqrt 2$ | well conditioned; the [quadratic formula](/quadratic-formula/) in its stable form gives both to full accuracy |
| $x^n - 1$ | $e^{2\pi i k/n}$, $k = 0, \ldots, n-1$ | all simple and well conditioned |
| $(x - 1)^4$ with $a_0$ changed from $1$ to $1 - 10^{-16}$ | $1 \pm 10^{-4}$ and $1 \pm 10^{-4} i$ | a change of $10^{-16}$ moves a root of multiplicity 4 by $10^{-16/4} = 10^{-4}$ |
| $\prod_{k=1}^{20} (x - k)$ | $1, 2, \ldots, 20$ | changing $a_{19} = -210$ by $2^{-23}$ turns ten of the roots complex, among them $16.73 \pm 2.81 i$ (Wilkinson, 1963) |
| $x^5 - x - 1$ | one real root $1.1673039782614187$ and two complex pairs | not solvable in radicals |

## Known algorithms

| method | finds | cost | notes |
|---|---|---|---|
| [companion matrix](/companion-matrix-method/) and the [QR algorithm](/qr-algorithm/) | all roots | $O(n^3)$ flops, $O(n^2)$ memory; structured QR variants $O(n^2)$ | backward stable as an eigenvalue problem; normwise backward stable in the coefficients when they are scaled (Edelman and Murakami, 1995); used by `roots` in MATLAB and NumPy |
| [Aberth-Ehrlich](/aberth-ehrlich-method/) | all roots at once | $O(n^2)$ per sweep | cubic local convergence for simple roots; with multiprecision and inclusion discs in MPSolve |
| [Durand-Kerner](/durand-kerner-method/) (Weierstrass) | all roots at once | $O(n^2)$ per sweep | quadratic local convergence |
| [Jenkins-Traub](/jenkins-traub-algorithm/) | one root at a time, with deflation | $O(n^2)$ overall in practice | the classic black-box polynomial solver (RPOLY, CPOLY) |
| [Laguerre's method](/laguerre-method/) with [deflation](/polynomial-deflation/) | one root at a time | $O(n)$ per step | cubic convergence to simple roots, converges from almost any start in practice |
| [Newton's method](/newton-raphson-method/) with deflation | one root at a time | $O(n)$ per step | quadratic; needs good starts; polish roots against the original $p$ |
| [Muller's method](/muller-method/) | one root, possibly complex | $O(n)$ per step | order $1.84$; no derivative |
| [Bairstow's method](/bairstow-method/) | quadratic factors in real arithmetic | $O(n)$ per step | complex pairs without complex arithmetic |
| [Graeffe's method](/graeffe-method/), [Bernoulli's method](/bernoulli-method/) | moduli of the roots, the dominant root | | historical; Graeffe's squaring is used in modern splitting methods |
| [Lehmer-Schur](/lehmer-schur-method/) | all roots, by subdivision | | guaranteed, slow |

## Bounds

- **Existence and count (proved).** Exactly $n$ roots in $\mathbb{C}$ with multiplicity. All lie in $|x| \le 1 + \max_{j < n} |a_j/a_n|$ ([Cauchy's bound](/cauchy-root-bound/)).
- **No radicals (proved).** For $n \ge 5$ there is no general formula in radicals; $x^5 - x - 1$ is a concrete example whose roots are not expressible in radicals.
- **Sensitivity (proved).** A root of multiplicity $m$ moves by about $(\epsilon\,m!\,|a_j x^{*j}| / |p^{(m)}(x^*)|)^{1/m}$ under a change $\epsilon a_j$ in one coefficient, so its forward accuracy in floating point is about $u^{1/m}$; a simple root has forward error about $\kappa(x^*)\,u\,|x^*|$ at best.
- **Limiting accuracy of evaluation.** Horner's rule computes $p(x)$ with an error at most $\gamma_{2n} \sum_j |a_j|\,|x|^j$, $\gamma_{2n} = 2nu/(1 - 2nu)$ (Higham, Section 5.1); no root test based on computed values can resolve $|p(x)|$ below this level.
- **Complexity (proved).** All $n$ roots can be approximated to $b$ digits with a number of bit operations within polylogarithmic factors of $n^2 (n + b)$, close to the lower bound given by the size of the output and of the input needed (Pan, 1997 and later work).

## Reductions

- **To eigenvalues.** The roots of $p$ are the eigenvalues of its companion matrix; conversely the characteristic polynomial is a poor way to compute eigenvalues, because its roots are more sensitive than the eigenvalues of the matrix.
- **To one-variable root finding.** Each root can be found by a scalar method, and the rest from the deflated polynomial $p(x)/(x - \hat x)$ ([polynomial deflation](/polynomial-deflation/)).
- **From exact factorization.** Over $\mathbb{Q}$, [factorization over the integers](/polynomial-factorization-over-integers/) splits $p$ into irreducible factors, each with simple roots, before any numerical work.
- **To real root isolation.** For real roots only, isolate exactly first and refine numerically.

## Applications

- **Eigenvalues of small matrices** and characteristic equations of linear recurrences and of linear differential equations with constant coefficients.
- **Control and signal processing.** The poles and zeros of rational transfer functions; stability tests count roots in a half-plane or a disc ([Schur-Cohn test](/schur-cohn-test/), [z-transform](/z-transform/)).
- **Computer algebra and geometry.** Real algebraic numbers, ray tracing of algebraic surfaces, intersections of curves via [resultants](/resultant/).
- **Quadrature.** The nodes of Gaussian quadrature are roots of orthogonal polynomials.

## References
