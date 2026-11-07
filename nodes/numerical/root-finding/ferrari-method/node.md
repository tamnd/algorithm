---
tag: 82X66E
kind: algorithm
slug: ferrari-method
name: Ferrari's method
aliases:
- Ferrari's quartic formula
- quartic formula
- Ferrari's solution of the quartic
area: numerical/root-finding
level: intro
summary: Closed form for quartic roots by reduction to a resolvent cubic. Shift away the cube term, solve a cubic for m, and split the quartic into two quadratics with the root m of largest modulus.
solves: [polynomial-root-finding]
model: real-ram
complexity:
  vars: {n: "the degree, fixed at 4"}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, closed_form: true, complex_arithmetic: true}
prereqs: [cardano-formula, quadratic-formula, polynomial]
see_also: [abel-ruffini-theorem, fundamental-theorem-of-algebra, vieta-formulas, newton-raphson-method, polynomial-root-finding, catastrophic-cancellation, companion-matrix-method, multiplicity-of-roots]
sources:
  - book: "Girolamo Cardano, Ars Magna, or The Rules of Algebra, 1545, translated by T. Richard Witmer, MIT Press, 1968 (Dover reprint, 1993)"
    locator: Chapter XXXIX, the rule of Lodovico Ferrari for a square square, squares and number equal to first powers, worked on x^4 + 6x^2 + 36 = 60x
  - book: isbn:9781482245820
    title: Ian Stewart, Galois Theory, fourth edition, CRC Press, 2015
    locator: Chapter 1, Classical algebra (the solution of the quartic by Ferrari and the resolvent cubic)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 1.8, Solving a quadratic equation (the choice of sign that the two quadratic factors use)
  - book: isbn:9780521880688
    title: William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 5.6, Quadratic and Cubic Equations, and Section 9.5, Roots of Polynomials (polishing closed form roots by Newton steps)
---

Ferrari's method gives the four roots of a quartic $ax^4 + bx^3 + cx^2 + dx + e$ with $a \ne 0$ in closed form. A shift $x = y - b/(4a)$ removes the cube term and leaves $y^4 + py^2 + qy + r$. Adding a free term $m$ inside a square turns the equation into a difference of two squares exactly when $m$ is a root of a cubic, the *resolvent cubic*, which [Cardano's formula](/cardano-formula/) solves. The quartic then splits into two quadratics, and the [quadratic formula](/quadratic-formula/) gives the four roots. It is the last general formula in radicals: from degree 5 on there is none ([Abel-Ruffini theorem](/abel-ruffini-theorem/)). The cost is a fixed number of operations, but in floating point the choice of $m$ and the shift need care.

## In plain words

An equation with a fourth power can be solved by a recipe that calls the recipe for cubes. First move the unknown by a fixed amount so that the cube term goes away. Then try to write the left side as one square minus another square. That works only for special values of a helper number, and those values solve a cubic equation. Pick one of them, the largest one, and the fourth-degree equation breaks into two ordinary quadratic equations. Each quadratic gives two roots, so you get all four. The three possible helper values match the three ways to sort the four roots into two pairs.

## The problem

Given complex $a, b, c, d, e$ with $a \ne 0$, find the four roots $x_1, \ldots, x_4$, with [multiplicity](/multiplicity-of-roots/), of $ax^4 + bx^3 + cx^2 + dx + e$. By the [fundamental theorem of algebra](/fundamental-theorem-of-algebra/) there are exactly four. The method is direct, not iterative, so there are no iterates and no order of convergence; the cost is a fixed count of arithmetic operations, square roots and cube roots. The relevant measure of quality is the error of each computed root in floating point, which we compare with the error of a [Newton](/newton-raphson-method/) step on the original quartic.

## The algorithm

Divide by $a$ and put $s = b/(4a)$, $C = c/a$, $D = d/a$, $E = e/a$. With $x = y - s$ the quartic becomes $y^4 + py^2 + qy + r$ with

$$p = C - 6s^2, \qquad q = D - 2Cs + 8s^3, \qquad r = E - Ds + Cs^2 - 3s^4.$$

For any $m$, $y^4 + py^2 + qy + r = 0$ is the same as $(y^2 + \tfrac{p}{2} + m)^2 = 2my^2 - qy + (m^2 + pm + \tfrac{p^2}{4} - r)$. The right side is a perfect square in $y$ when its discriminant is zero, that is when $m$ is a root of the resolvent cubic

$$R(m) = 8m^3 + 8pm^2 + (2p^2 - 8r)m - q^2.$$

Then with $\sigma^2 = 2m$ the right side is $(\sigma y - q/(2\sigma))^2$, and the quartic is the product of $y^2 - \sigma y + A$ and $y^2 + \sigma y + B$ with $A, B = \tfrac{p}{2} + m \pm \tfrac{q}{2\sigma}$.

```pseudo id=main
FERRARI(a, b, c, d, e):                      // a != 0
L1   s <- b/(4a);  C <- c/a;  D <- d/a;  E <- e/a
L2   p <- C - 6s^2;  q <- D - 2Cs + 8s^3;  r <- E - Ds + Cs^2 - 3s^4
L3   (m1, m2, m3) <- CARDANO(8, 8p, 2p^2 - 8r, -q^2)
L4   m <- the mi of largest modulus
L5   if m = 0 then return (-s, -s, -s, -s)
L6   sigma <- sqrt(2m)
L7   A <- p/2 + m + q/(2 sigma);  B <- p/2 + m - q/(2 sigma)
L8   (y1, y2) <- QUAD(-sigma, A);  (y3, y4) <- QUAD(sigma, B)
L9   return (y1 - s, y2 - s, y3 - s, y4 - s)

QUAD(beta, gamma):                           // roots of y^2 + beta y + gamma
L10  w <- sqrt(beta^2 - 4 gamma);  t <- the one of -(beta + w)/2, -(beta - w)/2 of larger modulus
L11  if t = 0 then return (0, 0) else return (t, gamma/t)
```

Line L1 normalizes and L2 removes the cube term. Line L3 solves the resolvent cubic by Cardano's formula and L4 takes its root of largest modulus. Line L5 handles the case where all three roots of $R$ are zero, which happens exactly when $p = q = r = 0$, so the quartic is $(x + s)^4$. Lines L6 and L7 form the two quadratic factors, L8 solves them and L9 undoes the shift. QUAD is the stable quadratic formula: it computes the root of larger modulus without cancellation and gets the other from the product $\gamma$.

## Example

Take Ferrari's own equation $x^4 + 6x^2 - 60x + 36 = 0$ (Ars Magna, Chapter XXXIX). There is no cube term, so $s = 0$, $p = 6$, $q = -60$, $r = 36$, and $R(m) = 8m^3 + 48m^2 - 216m - 3600$. Its three roots give three factorizations:

| root $m$ of $R$ | $\lvert m \rvert$ | $\sigma = \sqrt{2m}$ | roots of $y^2 - \sigma y + A$ | roots of $y^2 + \sigma y + B$ |
|---|---|---|---|---|
| $7.0097912285$ | 7.0098 | $3.7442732882$ | $3.0998744240$, $0.6443988642$ | $-1.8721366441 \pm 3.8101353368i$ |
| $-6.5048956143 + 4.6778470995i$ | 8.0122 | $1.2277377799 + 3.8101353368i$ | $-1.8721366441 + 3.8101353368i$, $3.0998744240$ | $-1.8721366441 - 3.8101353368i$, $0.6443988642$ |
| $-6.5048956143 - 4.6778470995i$ | 8.0122 | $1.2277377799 - 3.8101353368i$ | $-1.8721366441 - 3.8101353368i$, $3.0998744240$ | $-1.8721366441 + 3.8101353368i$, $0.6443988642$ |

Each choice of $m$ gives the same four roots, sorted into pairs in a different way: $\sigma$ is the sum of the pair in the first factor, so $2m = (y_1 + y_2)^2$. In the first row, $3.0998744240 + 0.6443988642 = 3.7442732882 = \sigma$ and $A = 1.9975555581$ is their product. Line L4 takes a complex root of modulus 8.0122, and the computed roots have residuals $|p(x_i)|$ below $10^{-13}$. The real roots are $3.0998744240$ and $0.6443988642$.

## Correctness

The invariant is that the depressed quartic equals $(y^2 - \sigma y + A)(y^2 + \sigma y + B)$ whenever $m \ne 0$ is a root of $R$; expanding the product and using $R(m) = 0$ checks it, and the shift of L1 and L2 maps the roots of the depressed quartic to those of the original. The full proof, with the zero case and the stable quadratic formula, is in [the correctness proof](proofs/correctness.md).

## Complexity

The method uses a fixed number of operations: about 30 complex additions and multiplications for L1, L2 and L7, one Cardano solve (one square root and one cube root), one more square root at L6, and one square root and one division in each call of QUAD. So time and extra space are $\Theta(1)$ on the [real RAM](/real-ram/) with complex arithmetic. A [Newton](/newton-raphson-method/) polish of each root with [Horner's rule](/horner-rule/) costs 8 more multiplications and additions for each step.

## Properties

- **Exact in exact arithmetic.** In complex arithmetic with exact square and cube roots, the four outputs are the roots with multiplicity.
- **Any root of $R$ works in exact arithmetic.** Every nonzero root of $R$ gives a valid splitting. If $q \ne 0$, all three roots are nonzero, since their product is $q^2/8$.
- **Complex arithmetic.** As for the cubic, the method may pass through complex numbers even when all four roots are real.
- **No backward stability guarantee.** In floating point each step is a rounding of a well-defined expression, but the shift and the division by $\sigma$ can lose accuracy, so the outputs can be far from the roots of any nearby quartic. Polishing fixes this in practice.

## Variants and improvements

- **Descartes' factorization.** Write the depressed quartic as $(y^2 + uy + v)(y^2 - uy + w)$ and solve for $u^2$, a cubic again. It is the same method in different variables.
- **Euler's form.** The roots are $y = \tfrac12(\pm\sqrt{z_1} \pm \sqrt{z_2} \pm \sqrt{z_3})$, where $z_i = (y_1 + y_2)^2$ for the three pairings are the roots of $z^3 + 2pz^2 + (p^2 - 4r)z - q^2$ (that is $z = 2m$), and the product of the three square roots must equal $-q$. It is symmetric but needs this rule for the signs.
- **The biquadratic case.** When $q = 0$, the quartic is a quadratic in $y^2$ and needs no cubic. In exact arithmetic the general method also handles it, because $m = 0$ is then not chosen at L4 unless $p = r = 0$.
- **Polishing.** One or two [Newton](/newton-raphson-method/) steps on the original quartic, from each computed root, bring simple roots to full accuracy. Numerical Recipes (Section 9.5) recommends this for any closed form root.
- **Eigenvalues.** The [companion matrix method](/companion-matrix-method/) computes the four roots as eigenvalues, which is backward stable and often preferred in libraries.

## When to use it

Use it when a quartic must be solved in a fixed, small number of operations, with no loop: in geometry (intersection of two conics, ray and torus intersection in graphics, distance from a point to an ellipse) and in closed form solutions of mechanics problems. Follow it with Newton polishing when accuracy matters. When the roots may be clustered or of very different sizes, or when the code must be robust for all inputs, an eigenvalue solver or an iterative method with deflation is safer. For degree 5 and more there is no formula of this kind.

## Pitfalls

- **Taking a root of $R$ of small modulus (L4).** For the quartic with roots $1, 2, 3, 4 + 10^{-7}$, $q$ is about $10^{-7}$, and $R$ has a root near zero. Taking that root makes $\sigma$ tiny, $q/(2\sigma)$ at L7 is a ratio of two small inexact numbers, and the computed roots are wrong by 0.0118. The root of largest modulus gives an error of $2.1 \times 10^{-14}$.
- **Losing a small root to the shift (L1, L9).** For the roots $10^{-4}, 1, 2, 1000$ the shift is $s = 250.75$, and L9 computes the root $10^{-4}$ as $y - s$ with $y \approx s$: [catastrophic cancellation](/catastrophic-cancellation/). The computed value is $9.99965 \times 10^{-5}$, a relative error of $3.5 \times 10^{-5}$; the root 1 is also off by $7 \times 10^{-9}$. Two Newton steps on the original quartic bring both to relative error below $4 \times 10^{-16}$.
- **Dividing by $\sigma = 0$ (L7).** Without the test at L5, the quartic $(x + s)^4$ gives $m = 0$ and a division by zero. With $p, q, r$ small but nonzero after rounding, L5 is not taken and the division is fine, since $|m|$ is the largest root of $R$.
- **Using the naive quadratic formula (L10).** For a quadratic factor whose roots differ greatly in size, $-\beta/2 \pm w/2$ cancels in the small root ([quadratic formula](/quadratic-formula/)). L10 and L11 avoid this.
- **Multiple roots.** At a double root the roots of $R$ coincide in pairs, and the root is [ill conditioned](/root-conditioning/): for roots $1, 1, 2, 2$ the computed roots are off by $3 \times 10^{-13}$, and a perturbation of size $u$ in the coefficients moves a double root by about $\sqrt{u}$.

## Implementations

## History

Lodovico Ferrari, a student of Gerolamo Cardano, found the method around 1540, when a problem from Zuanne da Coi led to the equation $x^4 + 6x^2 + 36 = 60x$. Since the method needs the solution of a cubic, it could not be published before Cardano's formula, and both appeared in Cardano's Ars Magna in 1545. Descartes (1637) and Euler gave other forms of the reduction. Lagrange (1770) explained why the method works through the resolvent and the permutations of the roots, the analysis that led to the proof of the [Abel-Ruffini theorem](/abel-ruffini-theorem/).

## References
