---
tag: XGZ50G
kind: algorithm
slug: cardano-formula
name: Cardano's formula
aliases:
- Cardano's method
- cubic formula
- del Ferro-Tartaglia-Cardano formula
area: numerical/root-finding
level: intro
summary: The three roots of a cubic in closed form. Shift to remove the square term, solve a quadratic for u^3, take one cube root u, and form the roots u - p/(3u) with the three choices of u.
solves: [polynomial-root-finding]
model: real-ram
complexity:
  vars: {n: "the degree, fixed at 3"}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, closed_form: true, complex_arithmetic: true}
prereqs: [quadratic-formula, polynomial, fundamental-theorem-of-algebra]
see_also: [ferrari-method, abel-ruffini-theorem, vieta-formulas, discriminant, newton-raphson-method, polynomial-root-finding, catastrophic-cancellation, companion-matrix-method]
sources:
  - book: "Girolamo Cardano, Ars Magna, or The Rules of Algebra, 1545, translated by T. Richard Witmer, MIT Press, 1968 (Dover reprint, 1993)"
    locator: Chapter XI, On the cube and first power equal to the number (the rule for x^3 + 6x = 20)
  - book: isbn:9781482245820
    title: Ian Stewart, Galois Theory, fourth edition, CRC Press, 2015
    locator: Chapter 1, Classical algebra (the solution of the cubic and its history from del Ferro and Tartaglia to Cardano)
  - book: isbn:9780521880688
    title: William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 5.6, Quadratic and Cubic Equations (the trigonometric form for three real roots and the stable choice of sign)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 1.8, Solving a quadratic equation (the cancellation that the choice of sign avoids, which Cardano's formula inherits)
---

Cardano's formula gives the three roots of a cubic $ax^3 + bx^2 + cx + d$ with $a \ne 0$ in closed form. A shift $x = t - b/(3a)$ removes the square term and leaves $t^3 + pt + q = 0$. With $t = u + v$ and $uv = -p/3$, the cube $u^3$ is a root of a [quadratic](/quadratic-formula/), and the roots are $t = \omega^k u - p/(3\omega^k u)$ for the three cube roots of unity $\omega^k$. The formula needs complex numbers even when all three roots are real, the case that Cardano called irreducible. It costs a fixed number of operations, but in floating point it needs care with signs and with roots of very different sizes, and an iterative step often makes it more accurate.

## In plain words

An equation with a cube, a square, a plain unknown and a number can always be solved by a recipe. First move the unknown by a fixed amount so that the square term goes away. Then split the unknown into two parts whose product you fix. The cube of one part then solves an ordinary quadratic equation, which the school formula solves. Take a cube root of that answer to get the first part, get the second part from the fixed product, and add them. That gives one root. The other two roots come from the other two cube roots, which are the first one turned by a third of a circle in the complex plane. Surprisingly, when all three roots are real, the recipe must pass through complex numbers on the way.

## The problem

The input is $a, b, c, d \in \mathbb{C}$ with $a \ne 0$. The output is the three roots $x_0, x_1, x_2 \in \mathbb{C}$ of $f(x) = ax^3 + bx^2 + cx + d$, with multiplicity, so that $f(x) = a(x - x_0)(x - x_1)(x - x_2)$. By the [fundamental theorem of algebra](/fundamental-theorem-of-algebra/) these roots exist. This is the case $n = 3$ of [polynomial root finding](/polynomial-root-finding/).

The notation of the root-finding pages is used where it applies: $f$ is the function, $x^*$ a root, $m$ its [multiplicity](/multiplicity-of-roots/). A closed form has no iterates; its cost is a fixed count of arithmetic operations and radicals, and its accuracy in floating point is measured against $u$, the [unit roundoff](/machine-epsilon/).

## The algorithm

All arithmetic is complex. $\sqrt{\cdot}$ and $\sqrt[3]{\cdot}$ are the principal roots, and $\omega = e^{2\pi i/3} = -\tfrac12 + \tfrac{\sqrt 3}{2} i$.

```pseudo id=main
CARDANO(a, b, c, d)                         ▷ a ≠ 0
L1  s ← b/(3a), C ← c/a, D ← d/a
L2  p ← C − 3s², q ← D − sC + 2s³          ▷ x = t − s gives t³ + pt + q = 0
L3  r ← √(q²/4 + p³/27)
L4  w ← −q/2 + r; if |−q/2 − r| > |w| then w ← −q/2 − r
L5  if w = 0 then return (−s, −s, −s)      ▷ then p = q = 0
L6  u ← ∛w
L7  for k ← 0, 1, 2 do
L8      uk ← ω^k · u
L9      tk ← uk − p/(3 uk)
L10     xk ← tk − s
L11 return (x0, x1, x2)
```

Lines L1 and L2 make the cubic monic and shift it: with $x = t - s$ and $s = b/(3a)$, the square term cancels. Line L3 is the square root of the quadratic $z^2 + qz - p^3/27 = 0$, whose two roots are $-q/2 \pm r$; one of them is $u^3$ and the other is $v^3$. Line L4 takes the root of larger modulus, as in the stable [quadratic formula](/quadratic-formula/): the other choice can cancel to zero. Line L5 handles the only case where both roots of the quadratic are zero. Lines L6 to L9 take one cube root and get the partner $v = -p/(3u)$ from the product $uv = -p/3$, so the two parts always match. Line L10 undoes the shift.

The quantity $\Delta = -(4p^3 + 27q^2) = -108\, r^2$ is the [discriminant](/discriminant/) of the depressed cubic. For real coefficients, $\Delta > 0$ means three distinct real roots, $\Delta = 0$ a multiple root, and $\Delta < 0$ one real root and two conjugate roots.

## Example

**Cardano's own example.** $x^3 + 6x = 20$, that is $(a, b, c, d) = (1, 0, 6, -20)$. Here $s = 0$, $p = 6$, $q = -20$, $r = \sqrt{100 + 8} = 10.392304845$, and $w = 10 + 10.392304845 = 20.392304845$. The cube root is $u = 2.732050808 = 1 + \sqrt 3$, and $v = -6/(3u) = -0.732050808 = 1 - \sqrt 3$.

| k | $u_k = \omega^k u$ | $t_k = u_k - p/(3u_k)$ | $x_k$ |
|---|---|---|---|
| 0 | 2.7320508 | 2 | 2 |
| 1 | −1.3660254 + 2.3660254 i | −1 + 3 i | −1 + 3 i |
| 2 | −1.3660254 − 2.3660254 i | −1 − 3 i | −1 − 3 i |

So $x^3 + 6x - 20 = (x - 2)(x^2 + 2x + 10)$.

**Three real roots.** $x^3 - 6x^2 + 11x - 6 = (x - 1)(x - 2)(x - 3)$. Here $s = -2$, $p = -1$, $q = 0$, and $r = \sqrt{-1/27} = 0.19245\,i$ is imaginary. Then $w = 0.19245\,i$ and $u = 0.5 + 0.28868\,i$, a complex number with $|u|^2 = 1/3$. Since $-p/(3u) = 1/(3u) = \bar u$, each $t_k = 2\operatorname{Re}(\omega^k u)$ is real: $t_0 = 1$, $t_1 = -1$, $t_2 = 0$, so $x_0 = 3$, $x_1 = 1$, $x_2 = 2$. In binary64 the computed roots have imaginary parts of about $10^{-16}$, the trace of the complex detour.

**A double root.** $x^3 - 3x + 2 = (x - 1)^2(x + 2)$ has $p = -3$, $q = 2$, $r = 0$ and $w = -1$. The principal cube root is $u = e^{i\pi/3} = 0.5 + 0.86603\,i$, and the roots are $t_0 = u + 1/u = 1$, $t_1 = -2$, $t_2 = 1$.

## Correctness

Let $v_k = -p/(3u_k)$, so $u_k v_k = -p/3$ for each $k$, and $v_k = \omega^{-k} v_0$. The key identity is

$$(u + v)^3 + p(u + v) + q = u^3 + v^3 + q + (3uv + p)(u + v),$$

so $t = u + v$ solves the depressed cubic when $uv = -p/3$ and $u^3 + v^3 = -q$. Line L4 makes $w = u^3$ a root of $z^2 + qz - p^3/27$, and then $v^3 = (-p/3)^3/u^3$ is the other root, so $u^3 + v^3 = -q$. Vieta's formulas then show that $t_0, t_1, t_2$ are exactly the three roots with multiplicity. The full proof, with the case $w = 0$, is in [the correctness proof](proofs/correctness.md).

## Complexity

In the [real RAM](/real-ram/) with complex arithmetic, where each field operation, each square root and each cube root costs one step, the method does a fixed number of steps: about 20 multiplications and divisions, one square root and one cube root. So the time and the space are $\Theta(1)$. A complex cube root costs a logarithm and an exponential, or a polar form, in a real library.

### Floating point

The formula is exact in exact arithmetic, but not backward stable in floating point.

- **The shift.** If the roots have very different sizes, the shift $s$ and the step $x_k = t_k - s$ cancel for the small roots. For $(x - 10^{-6})(x - 1)(x - 1000)$ in binary64, the computed small root has relative error $1.27 \times 10^{-5}$, although the root is well conditioned. Vieta's formula $x_{\text{small}} = -d/(a\, x_{\text{big},1}\, x_{\text{big},2})$ recovers it to full accuracy.
- **Multiple roots.** Near a root of multiplicity $m$, a perturbation of size $u$ in the coefficients moves the root by about $u^{1/m}$. So any method, Cardano's included, gives about 8 correct digits for a double root and about 5 for a triple root in binary64. This is the [conditioning of the root](/root-conditioning/), not a defect of the formula.
- **Polishing.** One or two steps of [Newton's method](/newton-raphson-method/) on the original cubic, from each computed root, bring a simple root to nearly full accuracy.

## Properties

- **Closed form.** A fixed number of operations, no iteration and no starting point.
- **Complex arithmetic is needed.** For three distinct real roots ($\Delta > 0$), every expression in real radicals fails: the square root in line L3 is of a negative number. This is the *casus irreducibilis*, and it is a theorem: no formula with real radicals can give these roots in general.
- **All roots at once.** The three choices of the cube root give the three roots, so no [deflation](/polynomial-deflation/) is needed.
- **Real roots stay real only in exact arithmetic.** In floating point, real roots of a real cubic come out with tiny imaginary parts in the irreducible case. Round them away only after a test against the discriminant.

## Variants and improvements

- **Viète's trigonometric form.** For real $p < 0$ and $\Delta \ge 0$, the roots are $t_k = 2\sqrt{-p/3}\cos\big(\tfrac13 \arccos\big(\tfrac{3q}{2p}\sqrt{-3/p}\big) - \tfrac{2\pi k}{3}\big)$ for $k = 0, 1, 2$. It uses only real arithmetic. For $p = -1$, $q = 0$ it gives $t_k = \tfrac{2}{\sqrt 3}\cos(\pi/6 - 2\pi k/3)$, which is $1, 0, -1$.
- **Hyperbolic forms.** For one real root, $\cosh$ or $\sinh$ of a third of an inverse hyperbolic function gives the real root without complex numbers.
- **Stable real solvers.** Numerical Recipes (Section 5.6) gives a real version with the stable choice of sign. Careful solvers scale the coefficients first, to avoid overflow in $s^3$ and $q^2$.
- **Iterative alternatives.** For a single real root, [Newton's method](/newton-raphson-method/) from a good start or a bracketing method is simpler and as accurate. For all roots of higher degree, use the [companion matrix method](/companion-matrix-method/) or the [Aberth-Ehrlich method](/aberth-ehrlich-method/).

## When to use it

Use Cardano's formula when you need the roots of many cubics fast with no loop and no branch on convergence, for example in geometry kernels (intersections of curves, eigenvalues of $3 \times 3$ symmetric matrices), and polish each root with one Newton step if full accuracy matters. Use Viète's form for real cubics with three real roots. For a cubic whose roots differ greatly in size, or for exact symbolic work, prefer an iterative method or exact arithmetic.

## Pitfalls

- **Two independent cube roots.** Computing $u = \sqrt[3]{-q/2 + r}$ and $v = \sqrt[3]{-q/2 - r}$ separately, as principal roots, can give a pair with $uv \ne -p/3$. For $x^3 + 6x - 20$, $v = \sqrt[3]{-0.3923}$ is $0.36603 + 0.63397\,i$ as a principal complex root, and $u + v = 3.09808 + 0.63397\,i$ is not a root. Line L9 takes $v = -p/(3u)$ instead.
- **The wrong sign in line L4.** Always taking $w = -q/2 + r$ cancels when $q > 0$ and $|p|$ is small. For $x^3 + 10^{-8}x + 1$, binary64 gives $r = 0.5$ exactly, so $w = 0$, and the method returns the triple root 0 although the roots are $-1$ and $0.5 \pm 0.86603\,i$. Line L4 takes the root of larger modulus.
- **Real cube roots in the irreducible case.** A real-only program with `cbrt` fails when $q^2/4 + p^3/27 < 0$. Use complex arithmetic, as lines L3 to L9 do, or Viète's form.
- **Discarding imaginary parts.** Taking the real part of each root of a real cubic is wrong when $\Delta < 0$: two of the roots are truly complex.
- **The shift for roots of different sizes.** Line L10 loses the small roots, as shown above. Recover them from Vieta's formula or by a Newton step.

## Implementations

## History

Scipione del Ferro solved the depressed cubic $x^3 + px = q$ around 1515 and did not publish. Niccolò Tartaglia found the solution again in 1535 and told it to Girolamo Cardano, who published it, with the general cubic and the irreducible case, in the Ars Magna of 1545 (Stewart, Chapter 1). Cardano's Chapter XI solves the example $x^3 + 6x = 20$. The irreducible case led Bombelli to compute with complex numbers. Viète gave the trigonometric solution for three real roots.

## References
