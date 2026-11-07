---
tag: 4AF992
kind: technique
slug: polynomial-deflation
name: Polynomial deflation
aliases:
- deflation
- root deflation
- synthetic division by a computed root
area: numerical/root-finding
level: advanced
summary: Divide a computed root out of a polynomial to lower its degree before finding the next root. Stable in the right direction and order; polish every root on the original polynomial.
prereqs: [polynomial-root-finding, horner-rule, polynomial-division]
see_also: [laguerre-method, newton-raphson-method, muller-method, bairstow-method, jenkins-traub-algorithm, aberth-ehrlich-method, root-conditioning, wilkinson-polynomial]
sources:
  - book: "J. H. Wilkinson, Rounding Errors in Algebraic Processes, Prentice-Hall, 1963 (reprinted by Dover, 1994)"
    locator: Chapter 2, Computations involving polynomials (the stability of deflation and the order in which roots should be removed)
  - paper: doi:10.1093/imamat/8.1.16
    title: "G. Peters and J. H. Wilkinson, Practical problems arising in the solution of polynomial equations, IMA Journal of Applied Mathematics 8(1) (1971) 16-35"
    locator: forward, backward and composite deflation, and implicit deflation in Newton's method
  - book: isbn:9780521880688
    title: W. H. Press, S. A. Teukolsky, W. T. Vetterling and B. P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 5.1, Polynomials and rational functions (synthetic division); Section 9.5, Roots of polynomials (deflation, its order, and polishing)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 5.1, Horner's method (synthetic division as the intermediate quantities of Horner's rule)
  - paper: "H. J. Maehly, Zur iterativen Auflösung algebraischer Gleichungen, Zeitschrift für angewandte Mathematik und Physik 5 (1954) 260-263"
    locator: Newton's method with the found roots removed implicitly
---

Polynomial deflation finds all the roots of a polynomial one at a time. After a root $z$ of $p$ has been computed, $p$ is divided by $x - z$, and the next root is sought in the quotient, which has degree one lower and no longer has $z$ as a root, so the search cannot return to it. The division is synthetic division, the intermediate values of [Horner's rule](/horner-rule/) at $z$, and costs $n$ multiply-adds. Since $z$ is only approximate and the division is done in floating point, each deflation perturbs the remaining roots. Done in the right direction and with the roots removed in increasing order of modulus, the perturbation is of the order of the rounding error of the coefficients. Polishing each root by a few steps of an iterative method on the original polynomial then removes the remaining error.

## In plain words

If you know one root of a polynomial, you can split that factor off and keep a smaller polynomial with the other roots, just as dividing 12 by 3 leaves 4. Then you look for a root of the smaller one, split it off, and go on until nothing is left. This stops the root finder from finding the same root again and again. The catch is that the root you split off is not exact, so the smaller polynomial is a little wrong. If you split off the smallest roots first and dividing works from the right end, the error stays tiny. At the end, each root is cleaned up by a few steps on the original polynomial.

## When it applies

Deflation applies to any method that finds one root at a time: [Newton's method](/newton-raphson-method/), [Laguerre's method](/laguerre-method/), [Muller's method](/muller-method/), the [Jenkins-Traub algorithm](/jenkins-traub-algorithm/), and [Bairstow's method](/bairstow-method/) with quadratic factors. It needs the polynomial as coefficients, and a root found to near the limiting accuracy. It is not needed by methods that find all roots at once, such as the [companion matrix method](/companion-matrix-method/) and the [Aberth-Ehrlich method](/aberth-ehrlich-method/).

Notation on the root-finding pages: $p(x) = a_n x^n + \cdots + a_0$ has roots $x_1, \ldots, x_n$; $z$ is a computed root; $u$ is the unit roundoff. Dividing $p$ by $x - z$ gives $p(x) = (x - z)q(x) + p(z)$, where the remainder $p(z)$ is tiny when $z$ is a good root, and is dropped.

## The template

```pseudo id=main
ALL-ROOTS-BY-DEFLATION(p, FIND, POLISH)
L1  q ← p;  Z ← empty list
L2  for i ← 1 to n do
L3      z ← FIND(q, start 0)                ▷ any one-root method; start at 0 to get small roots first
L4      z ← POLISH(p, z)                    ▷ a few steps of the same method on the original p
L5      append z to Z
L6      if |z| ≤ 1 then q ← FORWARD(q, z) else q ← BACKWARD(q, z)
L7  return Z

FORWARD(a_n..a_0, z)                         ▷ from the leading coefficient
F1  b_{n-1} ← a_n
F2  for j ← n − 1 down to 1 do b_{j-1} ← a_j + z · b_j
F3  return b_{n-1}..b_0                      ▷ the remainder a_0 + z b_0 = p(z) is dropped

BACKWARD(a_n..a_0, z)                        ▷ from the constant term, z ≠ 0
B1  b_0 ← −a_0 / z
B2  for j ← 1 to n − 1 do b_j ← (b_{j-1} − a_j) / z
B3  return b_{n-1}..b_0                      ▷ the dropped remainder is a_n − b_{n-1}
```

Both divisions compute the same exact quotient when $p(z) = 0$; they differ in which coefficient equation they skip, and so in how rounding errors propagate. Forward division multiplies by $z$ at each step, so errors grow when $|z|$ is large compared with the remaining roots. Backward division divides by $z$ at each step, so errors grow when $|z|$ is small compared with them. The test in line L6 is a simple stand-in for the choice made in practice (Peters and Wilkinson, 1971): forward deflation of the root of smallest modulus, or backward deflation of the root of largest modulus, is stable. A complex root $z$ of a real polynomial is removed together with $\bar z$ by dividing by the real quadratic $x^2 - 2\operatorname{Re}(z)\,x + |z|^2$, which keeps the arithmetic real.

## Classic examples

**Which direction (computed).** Let $p$ be the monic polynomial of degree 12 with roots $1.9^j$, $j = 0, \ldots, 11$, rounded to binary64, from $1$ to about $1164$. Divide out one root exactly and measure the quality of the quotient $\hat q$ by its largest relative backward error $|\hat q(x_i)| / \sum_j |\hat q_j||x_i|^j$ at the remaining true roots $x_i$, computed in rational arithmetic:

| division | root removed | largest backward error at the other roots |
|---|---|---|
| forward | smallest, $1$ | $7.0 \cdot 10^{-17}$ |
| forward | largest, $1.9^{11}$ | $9.9 \cdot 10^{-1}$ |
| backward | smallest, $1$ | $8.4 \cdot 10^{-1}$ |
| backward | largest, $1.9^{11}$ | $7.3 \cdot 10^{-17}$ |

In the stable cases the quotient is as good as the rounded coefficients; in the unstable ones it has nothing to do with the true quotient.

**All roots with Laguerre's method.** `laguerre_all_roots` in the [Laguerre's method](/laguerre-method/) implementation runs the template with Laguerre's method started at $0$, forward deflation, and up to 10 polishing steps on the original polynomial. On 500 random monic polynomials of degree at most 10 with roots in the square $[-1, 1]^2$ of the complex plane, every root is recovered to within $10^{-8}$ and has a residual below $10^{-12}$ relative to $\sum_j |a_j||z|^j$ (observed in the tests).

**Newton with implicit deflation (Maehly).** Instead of forming the quotient, apply Newton's method to $p(x)/\prod_{i < k}(x - z_i)$, whose Newton step is
$$x \leftarrow x - \frac{1}{p'(x)/p(x) - \sum_{i < k} 1/(x - z_i)}.$$
The original coefficients are used throughout, so no deflation error accumulates, at the cost of $k - 1$ extra divisions per step.

## Variations

- **Composite deflation.** Find the roots of the quotient in both directions, forward for the roots smaller than $|z|$ and backward for the larger ones, and splice the two halves of the quotient together; this is stable for any root $z$ (Peters and Wilkinson, 1971).
- **Quadratic deflation.** Divide by a real quadratic factor, as in [Bairstow's method](/bairstow-method/) and in the real version of [Jenkins-Traub](/jenkins-traub-algorithm/).
- **Deflation of matrices.** The same idea for eigenvalues removes a found eigenvalue from a matrix, as in [power iteration](/power-iteration/) or the splitting of a Hessenberg matrix in the [QR algorithm](/qr-algorithm/).
- **Deflation of functions.** For a general $f$, search for zeros of $f(x)/(x - z)$ after finding $z$; this is the analogue of Maehly's method.

## Pitfalls

- **Wrong order.** Removing large roots first by forward division destroys the small roots, as the table shows. Starting each search at $0$ makes the small roots come out first.
- **Unpolished roots.** Roots found in deflated polynomials carry all earlier errors. Always polish them on the original $p$, and check that the polished roots are distinct: two of them may converge to the same root of $p$.
- **Ill-conditioned polynomials.** Deflation cannot be better than the conditioning of the roots allows; for [Wilkinson's polynomial](/wilkinson-polynomial/) the rounding of the coefficients alone moves the roots far, see [root conditioning](/root-conditioning/).
- **Multiple roots.** A root of multiplicity $m$ is computed only to about $u^{1/m}$, and dividing by an inaccurate factor perturbs the other copies; group clustered roots and deflate them together.
- **Remainder not checked.** A large dropped remainder $p(z)$ means $z$ was not a root; deflate only after convergence.

## Exercises

1. Show that the $b_j$ of FORWARD are the intermediate values of Horner's rule at $z$, and that the dropped remainder is $p(z)$.
2. Show that if $p(z) = 0$ exactly, FORWARD and BACKWARD return the same quotient in exact arithmetic.
3. Let $p(x) = (x - 1)(x - 10^6)$. Deflate by $z = 10^6(1 + 10^{-10})$ forward and backward and compare the remaining root with $1$.
4. Derive Maehly's step from Newton's method applied to $p(x)/\prod_{i<k}(x - z_i)$.
5. Explain why starting each search at $0$ makes the roots come out roughly in increasing order of modulus for Newton's and Laguerre's methods.

## References
