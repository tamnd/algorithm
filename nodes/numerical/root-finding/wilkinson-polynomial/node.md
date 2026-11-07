---
tag: BPAVN8
kind: concept
slug: wilkinson-polynomial
name: Wilkinson's polynomial
aliases:
- Wilkinson's example
- perfidious polynomial
area: numerical/root-finding
level: advanced
summary: The degree-20 polynomial with roots 1, 2, ..., 20. Its roots are well separated yet extremely ill-conditioned in the monomial coefficients, as Wilkinson found in the 1950s.
prereqs: [root-conditioning, polynomial-root-finding]
see_also: [root-conditioning, multiplicity-of-roots, polynomial-deflation, laguerre-method, horner-rule, condition-number, vieta-formulas, stopping-criteria]
sources:
  - paper: doi:10.1007/BF01386381
    title: "J. H. Wilkinson, The evaluation of the zeros of ill-conditioned polynomials, Part I, Numerische Mathematik 1 (1959) 150-166"
    locator: the polynomial with zeros 1, ..., 20 and the effect of the perturbation 2^(-23) of the coefficient of x^19
  - book: "J. H. Wilkinson, Rounding Errors in Algebraic Processes, Prentice-Hall, 1963 (reprinted by Dover, 1994)"
    locator: Chapter 2, Computations involving polynomials (the polynomial with zeros 1, 2, ..., 20, and the polynomial with zeros 2^(-1), ..., 2^(-20))
  - paper: "J. H. Wilkinson, The perfidious polynomial, in G. H. Golub (editor), Studies in Numerical Analysis, MAA Studies in Mathematics 24, 1984, 1-28"
    locator: the account of the discovery on the Pilot ACE and the analysis of the sensitivities
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 5, Polynomials (error analysis of Horner's method and the notes and references on Wilkinson's polynomial)
---

*Wilkinson's polynomial* is
$$w(x) = \prod_{j=1}^{20} (x - j) = x^{20} - 210x^{19} + 20615x^{18} - \cdots - 8752948036761600000\,x + 2432902008176640000.$$
Its roots are the integers $1, \ldots, 20$, spaced one apart, so nothing about them looks difficult. Yet J. H. Wilkinson found in the 1950s, while testing root finders on the Pilot ACE computer, that some of them are extraordinarily sensitive to the coefficients: changing the coefficient $-210$ of $x^{19}$ by $2^{-23} \approx 1.2 \times 10^{-7}$ turns ten of the real roots into five complex pairs, one of them $16.73 \pm 2.81i$. The example showed that [ill-conditioning](/root-conditioning/) of polynomial roots is not caused by close or [multiple roots](/multiplicity-of-roots/) only, and it ended the practice of computing eigenvalues through the characteristic polynomial.

## In plain words

Multiply out $(x-1)(x-2)\cdots(x-20)$ and you get a polynomial with gigantic coefficients, up to about $1.4 \times 10^{19}$. Near $x = 15$ its value is a small number left over after adding and subtracting terms of size $10^{27}$, so a tiny change in any coefficient changes the value by far more than the value itself. Nudge a coefficient by one part in a billion and many roots jump far away, some off the real line. The roots were easy to state; the coefficients are a terrible way to describe them.

## The idea

Notation on the root-finding pages: $w$ is Wilkinson's polynomial with coefficients $a_i$ of $x^i$, $x^* = j$ a root, $u = 2^{-53}$ the unit roundoff, and $\kappa(w, j) = \sum_i |a_i| j^i / (j\,|w'(j)|)$ the relative condition number of the root $j$, as on the [root conditioning](/root-conditioning/) page.

**Sensitivity to one coefficient (exact).** Differentiating $w(x^*) = 0$ gives $\partial x^*/\partial a_{19} = -j^{19}/w'(j)$ with $w'(j) = \prod_{k \ne j}(j - k) = (-1)^{20-j}(j-1)!\,(20-j)!$. So
$$\left|\frac{\partial x^*}{\partial a_{19}}\right| = \frac{j^{19}}{(j-1)!\,(20-j)!},$$
which is $8.2 \times 10^{-18}$ at $j = 1$ and $2.4 \times 10^{9}$ at $j = 16$, the maximum. A change of $2^{-23}$ in $a_{19}$ therefore moves the root at 16 by about 290 to first order, which means only that the first-order theory has broken down and the roots have moved a long way.

**Why.** The values $j^{19}$ grow far faster than $(j-1)!(20-j)!$ shrinks in the middle range. Equivalently, near $x = 14$ to $16$ the terms $|a_i| x^i$ of $w(x)$ add up to about $10^{27}$ while $|w'(x)|$ is about $10^{12}$: the value of $w$ is the result of cancellation of almost 15 decimal digits. Any relative perturbation of size $\delta$ in the coefficients shifts the value by up to $\delta \cdot 10^{27}$, and dividing by the slope gives the shift of the root.

**Floating point (proved bound, observed values).** Horner's rule in double precision evaluates $w$ with error up to about $\gamma_{40}\sum_i|a_i||x|^i$; at $x = 14.5$ this is about $2.3 \times 10^{13}$, while $|w(14.5)| = 2.1 \times 10^{12}$. So the computed sign of $w$ near the middle roots is not reliable, and no iterative method applied to the double-precision coefficients can locate the root at 15 to better than roughly $10^{-3}$ to $10^{-2}$, whatever its convergence order.

**Separation does not help.** All roots are at distance 1 from their neighbours. The polynomial with roots $2^{-1}, 2^{-2}, \ldots, 2^{-20}$, which Wilkinson also studied, has roots that are much closer together, yet every root has $\kappa \le 136$. Ill-conditioning comes from the relation between the roots and the monomial coefficients, not from the spacing.

## Examples

All figures below were computed with exact rational coefficients and an 80-digit Aberth iteration.

**The $2^{-23}$ perturbation.** The roots of $w(x) - 2^{-23}x^{19}$ are

| real roots | complex pairs |
|---|---|
| 1.000000, 2.000000, 3.000000, 4.000000, 5.000000 | $10.095266 \pm 0.643501i$ |
| 6.000007, 6.999697, 8.007268, 8.917250 | $11.793634 \pm 1.652330i$ |
| 20.846908 | $13.992358 \pm 2.518830i$ |
| | $16.730737 \pm 2.812625i$ |
| | $19.502439 \pm 1.940330i$ |

These agree with Wilkinson's 1959 and 1963 values.

**Just storing the coefficients.** In double precision the coefficients $a_3, \ldots, a_7$ are not representable and are rounded, by relative amounts below $u$. The exact roots of the rounded polynomial include $9.99980$, $12.99938$, $14.00055$ and $16.00019$: about three to four correct digits in the middle range before any arithmetic is done. The first-order formula $-\sum_i \Delta a_i\, j^i / w'(j)$ predicts these shifts to four digits.

**Condition numbers.** For selected roots, $\kappa(w, j)$ is $4.2 \times 10^2$ at $j = 1$, $5.6 \times 10^{12}$ at $j = 10$, $5.4 \times 10^{13}$ at $j = 14$ (the largest) and $1.4 \times 10^{11}$ at $j = 20$. With $u = 1.1 \times 10^{-16}$, the product $u\,\kappa \cdot j$ predicts errors up to about $0.1$ in the worst case, consistent with the observed errors of order $10^{-3}$, since most coefficients are stored exactly.

**As a matrix problem.** The eigenvalues of $\operatorname{diag}(1, 2, \ldots, 20)$, or of any symmetric matrix with these eigenvalues, change by at most $\|E\|_2$ under a symmetric perturbation $E$ (Weyl's inequality): the same twenty numbers are perfectly conditioned there. The companion matrix of $w$ has the same eigenvalues but inherits the ill-conditioning of the coefficients.

## Where it is used

- **Testing polynomial root finders.** It is the standard hard case for [Laguerre](/laguerre-method/), Jenkins-Traub, Aberth and companion-matrix solvers, and for the order of [deflation](/polynomial-deflation/).
- **Teaching conditioning.** It separates the conditioning of a problem from the stability of an algorithm: a backward-stable method returns roots of a nearby polynomial, which here are far from $1, \ldots, 20$.
- **Eigenvalue algorithms.** It is the classic argument against computing eigenvalues as roots of the characteristic polynomial.
- **Choice of basis.** It motivates representing polynomials by values, by Chebyshev or Bernstein coefficients, or in factored form.

## References
