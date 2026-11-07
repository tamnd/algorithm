---
tag: MGFY99
kind: concept
slug: root-conditioning
name: Conditioning of a root
aliases:
- condition number of a root
- sensitivity of roots
- root sensitivity
- pseudozeros
area: numerical/root-finding
level: advanced
summary: How much a root moves when the function or the coefficients change slightly. A simple root has condition 1/|f'(x*)|; a root of multiplicity m moves like the m-th root of the change.
prereqs: [root-finding-problem, multiplicity-of-roots, condition-number]
see_also: [wilkinson-polynomial, polynomial-root-finding, stopping-criteria, newton-raphson-method, horner-rule, polynomial-deflation, multiplicity-of-roots, square-free-factorization]
sources:
  - book: "J. H. Wilkinson, Rounding Errors in Algebraic Processes, Prentice-Hall, 1963 (reprinted by Dover, 1994)"
    locator: Chapter 2, Computations involving polynomials (sensitivity of the zeros to changes in the coefficients, the polynomial with zeros 1, 2, ..., 20)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 5, Polynomials (the running error bound for Horner's method and the condition of evaluation); Section 1.6 for condition numbers in general
  - paper: "W. Gautschi, On the condition of algebraic equations, Numerische Mathematik 21 (1973) 405-424"
    locator: condition numbers of roots with respect to coefficient perturbations, and their growth for real roots
  - paper: "K.-C. Toh and L. N. Trefethen, Pseudozeros of polynomials and pseudospectra of companion matrices, Numerische Mathematik 68 (1994) 403-425"
    locator: pseudozero sets and the componentwise backward error of an approximate root
  - paper: "J. H. Wilkinson, The perfidious polynomial, in G. H. Golub (editor), Studies in Numerical Analysis, MAA Studies in Mathematics 24, 1984, 1-28"
    locator: the history and analysis of the ill-conditioning of polynomial zeros
---

The *conditioning* of a root measures how far the root moves when the equation is changed slightly. It is a property of the problem, not of any method: no algorithm working in floating point can deliver a root more accurately than its condition number allows, because the rounding errors in evaluating $f$ already act as a change of $f$. A simple root $x^*$ of $f$ has absolute condition number $1/|f'(x^*)|$. A root of a polynomial with respect to relative changes in its coefficients has condition number $\sum_i |a_i||x^*|^i \big/ \bigl(|x^*||p'(x^*)|\bigr)$, which can be enormous for roots that are perfectly separated, as [Wilkinson's polynomial](/wilkinson-polynomial/) shows. A root of [multiplicity](/multiplicity-of-roots/) $m > 1$ has infinite condition number: a change of size $\varepsilon$ moves it by about $\varepsilon^{1/m}$.

## In plain words

Imagine the graph of $f$ crossing the axis. If the crossing is steep, raising or lowering the graph a little hardly moves the crossing point. If the graph is nearly flat there, the same small shift slides the crossing a long way, and if the graph only touches the axis, a shift can make the crossing vanish or split in two. Computers always shift the graph a little, because every evaluation is rounded. So the steepness at the root, compared with the size of that rounding noise, decides how many digits of the root anyone can hope to get, however clever the method.

## The idea

Notation on the root-finding pages: $f$ is the function, $x^*$ a root of multiplicity $m$, $p(x) = \sum_{i=0}^n a_i x^i$ a polynomial of degree $n$, $u$ the unit roundoff ($2^{-53}$ in double precision), and $\delta$ the size of a perturbation.

**Simple roots of a function (first order, proved).** Let $f$ be $C^1$ near a simple root $x^*$ and perturb it to $f + \delta g$ with $g$ continuous. By the implicit function theorem the perturbed equation has, for small $\delta$, a unique nearby root $x^*(\delta)$, and
$$x^*(\delta) = x^* - \delta\,\frac{g(x^*)}{f'(x^*)} + o(\delta).$$
For perturbations with $|g| \le 1$ the absolute condition number is $1/|f'(x^*)|$. For systems the same argument gives $\delta x \approx -J(x^*)^{-1}\delta g(x^*)$, with condition number $\|J(x^*)^{-1}\|$.

**Polynomial roots and coefficients (first order, proved).** Differentiating $p(x^*) = 0$ with respect to a coefficient gives $\partial x^*/\partial a_i = -(x^*)^i/p'(x^*)$. If every coefficient is changed by a relative amount at most $\delta$, so $|\Delta a_i| \le \delta |a_i|$, the root moves by at most
$$|\Delta x^*| \lesssim \delta\,\frac{\sum_i |a_i||x^*|^i}{|p'(x^*)|}, \qquad \kappa(p, x^*) = \frac{\sum_i |a_i||x^*|^i}{|x^*|\,|p'(x^*)|},$$
where $\kappa$ is the relative componentwise condition number. The numerator is the sum of the absolute values of the terms of $p(x^*)$: a large $\kappa$ means that $p(x^*) = 0$ is the result of heavy cancellation.

**Backward error of an approximate root (proved).** A number $z$ is an exact root of some polynomial $\tilde p$ with $|\tilde a_i - a_i| \le \eta |a_i|$ for all $i$ if and only if $\eta \ge |p(z)| / \sum_i |a_i||z|^i$ (Toh and Trefethen, 1994, following Rigal and Gaches for linear systems). Combined with the first-order bound this gives the rule of thumb
$$\text{relative forward error} \lesssim \kappa(p, z) \times \text{backward error}.$$

**Multiple roots (proved).** If $f = (x - x^*)^m h$ with $h(x^*) \ne 0$ and the perturbation is $f - \delta$ with $\delta$ small, the perturbed roots near $x^*$ satisfy $(x - x^*)^m \approx \delta / h(x^*)$, so there are $m$ of them (counted in $\mathbb{C}$), at distance about $|\delta/h(x^*)|^{1/m}$ along the $m$-th roots of $\delta/h(x^*)$. The derivative $\partial x^*/\partial\delta$ is unbounded, so the condition number is infinite; the useful statement is the Hölder bound $|\Delta x^*| = O(\delta^{1/m})$. A cluster of $m$ close simple roots behaves the same way for perturbations larger than the cluster width.

**Limiting accuracy in floating point.** Horner's rule in floating point returns the exact value at $x$ of a polynomial whose coefficients have relative errors at most $\gamma_{2n} = 2nu/(1 - 2nu)$ (Higham, Chapter 5). So, whatever the iteration, the computed values near a simple root are noise once $|x - x^*| \lesssim \gamma_{2n}\,\kappa(p, x^*)\,|x^*|$, and near a root of multiplicity $m$ once $|x - x^*| \lesssim \bigl(\gamma_{2n} \sum_i|a_i||x^*|^i\, m!/|p^{(m)}(x^*)|\bigr)^{1/m}$. A [stopping rule](/stopping-criteria/) that asks for more than this cannot be met; tests that compare $|p(x)|$ with $\gamma_{2n}\sum_i |a_i||x|^i$ stop exactly when the noise level is reached.

**Dependence on representation (observed and proved).** Conditioning depends on how the problem is given. The roots of $\prod_j (x - r_j)$ given by the $r_j$ need no computation; the same polynomial given by its monomial coefficients can be very ill-conditioned. Likewise the eigenvalues $1, \ldots, 20$ of $\operatorname{diag}(1, \ldots, 20)$ are perfectly conditioned for the matrix, while the same numbers as roots of the characteristic polynomial in monomial form are not. This is why eigenvalue problems are not solved through the characteristic polynomial.

## Examples

**A simple root.** For $f(x) = \cos x - x$ at $x^* = 0.739085$, $|f'(x^*)| = 1 + \sin x^* = 1.674$, so the root is well conditioned: an evaluation error of $10^{-16}$ moves it by about $6 \times 10^{-17}$.

**A double root.** $(x - 1)^2 - \delta$ has roots $1 \pm \sqrt\delta$. In double precision the evaluation error of $(x-1)^2$ expanded as $x^2 - 2x + 1$ near $x = 1$ is a few multiples of $u$, so the root is determined only to about $\sqrt{u} \approx 10^{-8}$, half the digits.

**Wilkinson's polynomial (computed exactly in rational arithmetic).** For $w(x) = \prod_{j=1}^{20}(x - j)$, with $|a_{19}| = 210$ and $a_0 = 20!$:

| root $j$ | $\lvert \partial x^*/\partial a_{19} \rvert$ | $\kappa(w, j)$ |
|---|---|---|
| 1 | $8.2 \times 10^{-18}$ | $4.2 \times 10^{2}$ |
| 5 | $6.1 \times 10^{-1}$ | $8.2 \times 10^{8}$ |
| 10 | $7.6 \times 10^{6}$ | $5.6 \times 10^{12}$ |
| 14 | $1.3 \times 10^{9}$ | $5.4 \times 10^{13}$ |
| 16 | $2.4 \times 10^{9}$ | $3.5 \times 10^{13}$ |
| 20 | $4.3 \times 10^{7}$ | $1.4 \times 10^{11}$ |

Merely storing the coefficients in double precision changes five of them ($a_3$ to $a_7$ are not representable) and moves the root at 13 to $12.99938$; the first-order prediction $-\sum_i \Delta a_i\, 13^i / w'(13) = -6.193 \times 10^{-4}$ matches the exact change $-6.193 \times 10^{-4}$. Changing $a_{19}$ by $2^{-23}$, as Wilkinson did, turns ten of the roots into five complex pairs, the widest being $16.7307 \pm 2.8126i$: there the first-order theory no longer applies at all.

**A well-conditioned polynomial.** The polynomial with roots $2^{-1}, 2^{-2}, \ldots, 2^{-20}$, also Wilkinson's, has all $\kappa \le 136$ (computed exactly): roots of very different sizes are well determined by relative changes in the coefficients.

## Where it is used

- **Choosing a target accuracy.** Stopping rules for [Newton's method](/newton-raphson-method/), the [Laguerre method](/laguerre-method/) and [polynomial deflation](/polynomial-deflation/) compare the residual with the noise level $\gamma_{2n}\sum|a_i||x|^i$.
- **Interpreting results.** A computed root with small backward error is as good as the data allow; a large forward error then signals ill-conditioning, not a bad method.
- **Multiple roots.** Ill-conditioning at multiple roots motivates computing the [square-free factorization](/square-free-factorization/) exactly first, or using methods that know the multiplicity.
- **Representation choice.** Ill-conditioning in the monomial basis motivates working with eigenvalue formulations, Chebyshev or Bernstein bases, or factored forms.
- **Pseudozero sets.** The set of points with backward error at most $\eta$, plotted as level curves of $|p(z)|/\sum|a_i||z|^i$, shows at once which roots are reliable.

## References
