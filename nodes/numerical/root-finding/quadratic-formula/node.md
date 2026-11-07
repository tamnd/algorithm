---
tag: CQ88BP
kind: algorithm
slug: quadratic-formula
name: Quadratic formula
aliases:
- quadratic equation solution
- stable quadratic formula
- citardauq formula
area: numerical/root-finding
level: intro
summary: Closed form for the roots of a x^2 + b x + c. Take the larger root without cancellation and the other from the product c/a; with an accurate discriminant both are accurate.
solves: [polynomial-root-finding]
model: real-ram
complexity:
  vars: {}
  time: {all: Θ(1)}
  space: {extra: Θ(1)}
  evaluations: {square_roots: "1"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: true, local: false}
prereqs: [floating-point-arithmetic, catastrophic-cancellation, discriminant]
see_also: [cardano-formula, ferrari-method, root-conditioning, polynomial-root-finding, fused-multiply-add, multiplicity-of-roots, abel-ruffini-theorem, newton-raphson-method]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 1.8, Solving a quadratic equation
  - book: isbn:9780521880688
    title: W. H. Press, S. A. Teukolsky, W. T. Vetterling and B. P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 5.6, Quadratic and cubic equations
  - paper: "G. E. Forsythe, Pitfalls in computation, or why a math book isn't enough, American Mathematical Monthly 77 (1970) 931-956"
    locator: the section on the quadratic equation
  - paper: "D. Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991) 5-48"
    locator: Section 1.4, Cancellation (the quadratic formula)
  - paper: "W. Kahan, On the cost of floating-point computation without extra-precise arithmetic, manuscript, University of California at Berkeley, 2004"
    locator: the accurate discriminant
---

The quadratic formula gives the two roots of $a x^2 + b x + c = 0$, $a \ne 0$, as $x = (-b \pm \sqrt{b^2 - 4ac})/(2a)$. In exact arithmetic that is the whole story. In floating point the textbook form fails twice: when $b^2 \gg |4ac|$ one of the two signs subtracts nearly equal numbers and loses most digits of the small root, and when the roots are close the discriminant itself cancels. The stable form computes the root of larger magnitude with no cancellation, takes the other from the product of the roots $c/a$, and computes the discriminant with a single rounding. Then both roots are accurate to a few units in the last place.

## In plain words

The school formula adds or subtracts a square root from $-b$. If $b$ is large and the square root is almost equal to $|b|$, one of the two choices subtracts two nearly equal numbers, and the digits that agree cancel and leave only rounding noise. The fix is to use only the sign that adds, which gives the bigger root safely. The two roots multiply to $c/a$, so the smaller root is $c/a$ divided by the bigger one, with no subtraction at all. A second problem appears when the two roots are nearly equal: then $b^2$ and $4ac$ are nearly equal, and their difference must be computed with extra care.

## The problem

The input is three real numbers $a, b, c$ with $a \ne 0$, given as floating-point numbers. The output is the two roots of $p(x) = a x^2 + b x + c$, counted with [multiplicity](/multiplicity-of-roots/): two real roots, or a pair of complex conjugate roots. The goal in floating point is that each computed root has a small relative error with respect to the exact roots of the stored coefficients.

Notation on the root-finding pages: $x^*$ is a root and $u = 2^{-53}$ the unit roundoff of binary64. Here we write $h = b/2$ and $D = h^2 - ac = (b^2 - 4ac)/4$, so the roots are $(-h \pm \sqrt D)/a$.

## The algorithm

```pseudo id=main
QUADRATIC(a, b, c)
L1  if a, b or c is not finite then return "invalid"; if a = 0 then return "not quadratic"
L2  scale a, b, c by one power of 2 so that the largest magnitude lies in [1/2, 1)
L3  h ← b/2; D ← h·h − a·c, computed exactly and rounded once
L4  if D < 0 then
L5      re ← −h/a; im ← sqrt(−D)/a
L6      return (re + i·|im|, re − i·|im|)
L7  s ← sqrt(D); if h ≥ 0 then q ← −(h + s) else q ← s − h
L8  if q = 0 then return (0, 0)
L9  return (q/a, c/q)
```

Line L2 multiplies all three coefficients by the same power of two, which is exact and does not change the roots; afterwards $h^2$ and $ac$ cannot overflow. Line L3 needs $D$ to a small relative error. The implementation forms $D$ exactly in rational arithmetic and rounds once; Kahan's method gets the same accuracy in floating point with a fused multiply-add (see [fused multiply-add](/fused-multiply-add/)). In line L7, $q = -(h + \operatorname{sign}(h)\sqrt D)$ adds two numbers of the same sign, so it has no cancellation, and $q/a$ is the root of larger magnitude. Line L9 gets the second root from $x_1 x_2 = c/a$: it is $(c/a)/(q/a) = c/q$. Line L8 handles $q = 0$, which happens only when $h = 0$ and $D = 0$, that is $b = c = 0$.

## Example

All in binary64.

| equation | textbook formula | QUADRATIC | exact roots |
|---|---|---|---|
| $x^2 - 10^8 x + 1$ | $7.450580596923828 \cdot 10^{-9}$, $10^8$ | $10^{-8}$, $10^8$ | $1.0000000000000000100 \cdot 10^{-8}$, $99999999.99999999$ |
| $x^2 - (2 + 2^{-26}) x + (1 + 2^{-26})$ | $1 + 2^{-27}$ twice | $1$, $1 + 2^{-26}$ | $1$, $1 + 2^{-26}$ |
| $2^{-1000}(x^2 - 3x + 2)$ | $1.5$ twice | $1$, $2$ | $1$, $2$ |
| $2^{1000}(x^2 - 3x + 2)$ | NaN | $1$, $2$ | $1$, $2$ |
| $x^2 + x + 1$ | $-0.5 \mp 0.8660254037844386\,i$ | $-0.5 \pm 0.8660254037844386\,i$ | $-\tfrac12 \pm \tfrac{\sqrt 3}{2} i$ |

In the first row $\sqrt{b^2 - 4} $ rounds to $10^8 - 1.49 \cdot 10^{-8}$, and $10^8$ minus that leaves one rounding error, so the small root is 25 percent wrong. In the second row the coefficients are exact floating-point numbers, but $h^2 = 1 + 2^{-26} + 2^{-54}$ rounds to $1 + 2^{-26} = ac$, the computed textbook discriminant is $0$, and both roots come out as the average; the exact $D = 2^{-54}$ gives both roots exactly. In the third row $b^2$ underflows, and in the fourth it overflows.

## Correctness

All claims are proved in [the correctness proof](proofs/correctness.md).

- **Exact arithmetic.** QUADRATIC returns the two roots of $p$ with multiplicity: $q/a$ and $c/q$ when $D \ge 0$, and $(-h \pm i\sqrt{-D})/a$ when $D < 0$. The case of a double root ($D = 0$) returns it twice.
- **Floating point (proved).** In binary64 with round to nearest, if no intermediate result underflows or overflows after the scaling of line L2, then $D < 0$ exactly when the computed $D$ is negative, and each computed real root, and each computed real and imaginary part, equals the exact value for the stored coefficients times $1 + \theta$ with $|\theta| \le \tfrac72 u + O(u^2)$.
- **The textbook formula (estimate).** When $|4ac| \ll b^2$, the root computed with cancellation is near $-c/b$ but carries the absolute error $u |b| / |a|$ of the square root, so its relative error is of order $u\, b^2 / |ac|$, with no bound as $ac \to 0$; the first row of the example shows $25$ percent.

The guarantee is about the stored coefficients. When the roots are close, they are ill conditioned: a relative change $\epsilon$ in $c$ can move a double root by about $\sqrt{\epsilon}$ times its size, so coefficients that were rounded before the call can make the roots inaccurate whatever the formula ([root conditioning](/root-conditioning/)).

## Complexity

- **Operations.** A fixed number of arithmetic operations, one square root and, for $D$, one exact product of two pairs of binary64 numbers. So the cost is $\Theta(1)$.
- **Space.** $\Theta(1)$.

### Floating point

The three risks and their fixes are cancellation in $-b \pm \sqrt{\cdot}$ (fixed by lines L7 and L9), cancellation in $b^2 - 4ac$ when the roots are close (fixed by the accurate $D$ of line L3), and overflow or underflow of $b^2$ (fixed by the scaling of line L2). Without an accurate $D$, the absolute error in the computed $D$ is about $u(h^2 + |ac|)$, and two close roots then come out with relative errors of order $\sqrt u \approx 10^{-8}$, as the second row of the example shows. A root can still overflow if it is larger than the largest finite number, and the scaling can turn a coefficient subnormal when the coefficients differ by a factor of more than about $2^{1000}$.

## Properties

- **Closed form.** No iteration, no stopping rule.
- **Accurate.** With the accurate discriminant every computed root has a relative error of a few $u$ with respect to the stored coefficients, in the sense of the bound above.
- **Order of the outputs.** The implementation returns real roots in increasing order, and complex roots with the positive imaginary part first.

## Variants and improvements

- **Kahan's discriminant.** Compute $p = \operatorname{fl}(h^2)$, $r = \operatorname{fl}(ac)$ and their exact errors with fused multiply-add, and add the error terms when $p$ and $r$ are close; this gives $D$ to within a few units in the last place without wider arithmetic (Kahan, 2004).
- **Citardauq formula.** The form $x = 2c/(-b \mp \sqrt{b^2 - 4ac})$ is the textbook formula turned upside down; line L9 uses it for one root.
- **Higher degree.** The [Cardano formula](/cardano-formula/) and [Ferrari's method](/ferrari-method/) give the roots of cubics and quartics in radicals; by the [Abel-Ruffini theorem](/abel-ruffini-theorem/) there is no such formula in degree five or more, and [polynomial root finding](/polynomial-root-finding/) uses iterative methods.
- **Polishing.** One step of [Newton's method](/newton-raphson-method/) on $p$ from a computed root can reduce its residual further if $p$ is evaluated accurately.

## When to use it

Use the stable form whenever a quadratic must be solved in floating point, including inside other algorithms: ray and sphere intersection, the eigenvalues of a $2 \times 2$ matrix, the parabola step of [Muller's method](/muller-method/), and the quadratic factors in [Bairstow's method](/bairstow-method/). The textbook form is fine only in exact or symbolic arithmetic.

## Pitfalls

- **Both signs of the textbook formula.** One of them cancels whenever $|4ac| \ll b^2$.
- **The naive discriminant.** It hides close roots: in the second row of the example two distinct roots come out equal.
- **Testing $D = 0$ with a tolerance.** Deciding "double root" when $|D|$ is small changes a well-defined answer into a guess; the computed sign of an accurately computed $D$ is the exact sign.
- **Dividing by $a$ first.** Forming $b/a$ and $c/a$ before the formula adds two roundings and can overflow when $a$ is tiny.
- **The case $a = 0$.** The formula divides by zero; the equation is linear and needs its own code.

## Implementations

## History

Babylonian tablets from about 1800 BC solve quadratic problems by completing the square, and Brahmagupta (628) and al-Khwarizmi (about 820) state general rules in words. The formula with the square root of $b^2 - 4ac$ is the modern symbolic form. The numerical failure of the textbook formula and the fix through the product of the roots are standard in the literature on rounding error; Forsythe (1970) used it as his first example of a pitfall in computation, and Kahan (2004) gave a way to compute the discriminant accurately without extra precision.

## References
