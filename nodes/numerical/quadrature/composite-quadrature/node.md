---
tag: QB75MX
kind: technique
slug: composite-quadrature
name: Composite quadrature rules
aliases:
- composite rules
- panel method
- compound quadrature rule
- repeated quadrature rule
area: numerical/quadrature
level: intro
summary: Cut [a, b] into m panels of width h = (b - a)/m, apply one basic rule on each panel and add the results. A basic rule of degree d gives an error O(h^(d+1)) for f in C^(d+1)[a, b].
prereqs: [quadrature-rule, degree-of-precision]
see_also: [trapezoidal-rule, simpsons-rule, midpoint-rule, gauss-legendre-quadrature, romberg-integration, adaptive-quadrature, euler-maclaurin-formula, pairwise-summation]
sources:
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 2, Approximate integration over a finite interval (the compound rules and their error terms)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Sections 5.1 (the trapezoidal and Simpson rules and their composite forms) and 5.2 (Newton-Cotes integration formulas)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 7, Numerical integration I (the composite trapezium and Simpson rules and their error bounds)
  - paper: doi:10.1137/130932132
    title: "Lloyd N. Trefethen and J. A. C. Weideman, The exponentially convergent trapezoidal rule, SIAM Review 56(3) (2014) 385-458"
    locator: Section 3 (geometric convergence of the trapezoidal rule for periodic analytic integrands)
---

A composite quadrature rule cuts the interval $[a, b]$ into $m$ panels of equal width $h = (b - a)/m$, applies one fixed basic [quadrature rule](/quadrature-rule/) on each panel, and adds the $m$ results. If the basic rule has [degree of precision](/degree-of-precision/) $d$, the composite rule has error $O(h^{d+1})$ for each $f \in C^{d+1}[a, b]$, so the error goes to zero as the panels shrink, with no need for high-degree interpolation. The composite [trapezoidal rule](/trapezoidal-rule/) and the composite [Simpson rule](/simpsons-rule/) are the standard examples, and the same idea is the base step of [adaptive quadrature](/adaptive-quadrature/) and [Romberg integration](/romberg-integration/).

## In plain words

To find the area under a curve, you can fit one simple shape to the whole curve, such as one trapezoid or one parabola. That works badly when the curve bends a lot. A composite rule cuts the interval into many short pieces of the same width. On each short piece the curve is almost a straight line or almost a parabola, so the simple shape fits well. You compute the area of each piece with the same small formula and add the areas. When you double the number of pieces, the error drops by a fixed factor that depends on the formula: about 4 for trapezoids and about 16 for parabolas. The cost is the number of times you evaluate the function.

## When it applies

- The integrand $f$ can be evaluated at any point of a bounded interval $[a, b]$, and the cost is counted in function evaluations.
- $f$ is smooth on the whole interval, or at least on each panel. The rate $h^{d+1}$ needs $f \in C^{d+1}[a, b]$. With less smoothness the rate drops to what $f$ allows.
- You want a method whose cost and error are predictable before you run it, or a building block for an [adaptive](/adaptive-quadrature/) or an extrapolation method such as [Richardson extrapolation](/richardson-extrapolation/).
- A single high-degree rule is not an option: equally spaced [Newton-Cotes rules](/newton-cotes-formulas/) of high degree have large negative weights and diverge for some analytic functions, while a composite rule of low degree converges for every continuous $f$ whose basic rule has positive weights.

## The template

**Notation.** We write $I(f) = \int_a^b f(x)\,dx$ (the weight is $w = 1$ on this page), a rule as $Q(f) = \sum_i w_i f(x_i)$, and the error as $E(f) = I(f) - Q(f)$. The basic rule has $n$ nodes $t_1, \ldots, t_n$ in $[0, 1]$ and weights $v_1, \ldots, v_n$ with $\sum_i v_i = 1$, and degree of precision $d$: it is exact on $\int_0^1 g(t)\,dt$ for each polynomial $g$ of degree at most $d$. Here $n$ counts nodes and $m$ counts panels, and $h = (b - a)/m$ is the panel width.

```pseudo id=main
COMPOSITE(f, a, b, m, BASIC)          ▷ BASIC = (t[1..n], v[1..n]) on [0, 1], exact to degree d
L1  h ← (b − a) / m
L2  S ← 0
L3  for j ← 0 to m − 1 do
L4      x0 ← a + j · h                ▷ left end of panel j; do not form it by repeated addition
L5      P ← 0
L6      for i ← 1 to n do
L7          P ← P + v[i] · f(x0 + h · t[i])
L8      S ← SUM(S, h · P)             ▷ hole: plain, pairwise or compensated summation
L9  return S
```

The two holes are the basic rule BASIC and the summation SUM. Lines L4 to L7 apply the basic rule on panel $j$, mapped from $[0, 1]$ to $[x_j, x_j + h]$ by $x = x_j + h t$; the factor $h$ in line L8 is the Jacobian of that map. When the basic rule uses both ends of its interval (trapezoid, Simpson, closed Newton-Cotes), the value at the right end of panel $j$ is the value at the left end of panel $j + 1$; a careful program evaluates it once, which gives $m(n - 1) + 1$ evaluations in place of $mn$.

**The basic rules.** On $[0, 1]$:

| basic rule | nodes $t_i$ | weights $v_i$ | $d$ | composite error, $f$ smooth enough |
|---|---|---|---|---|
| midpoint | $\tfrac12$ | $1$ | 1 | $\tfrac{(b-a)h^2}{24} f''(\xi)$ |
| trapezoid | $0, 1$ | $\tfrac12, \tfrac12$ | 1 | $-\tfrac{(b-a)h^2}{12} f''(\xi)$ |
| Simpson | $0, \tfrac12, 1$ | $\tfrac16, \tfrac46, \tfrac16$ | 3 | $-\tfrac{(b-a)h^4}{2880} f^{(4)}(\xi)$ |
| 2-point Gauss-Legendre | $\tfrac12 \mp \tfrac{1}{2\sqrt3}$ | $\tfrac12, \tfrac12$ | 3 | $\tfrac{(b-a)h^4}{4320} f^{(4)}(\xi)$ |

Each $\xi$ is some point of $(a, b)$. The midpoint and trapezoid lines need $f \in C^2[a, b]$, the other two need $f \in C^4[a, b]$. The constants follow from the one-panel errors $\tfrac{h^3}{24}f''$, $-\tfrac{h^3}{12}f''$, $-\tfrac{h^5}{2880}f^{(4)}$ and $\tfrac{h^5}{4320}f^{(4)}$ (Atkinson, Sections 5.1 and 5.3) and the lemma below. In the Simpson line $h$ is the panel width, and each panel holds three nodes. Many books write $h$ for the node spacing $h/2$; then the same error reads $-\tfrac{(b-a)h^4}{180}f^{(4)}(\xi)$.

**Theorem (the rate of a composite rule).** Let the basic rule have degree of precision $d$ and let $L = \sum_i |v_i|$. For each $f \in C^{d+1}[a, b]$,

$$|E(f)| \le \frac{1 + L}{(d+1)!}\,(b - a)\,h^{d+1}\,\max_{[a, b]} |f^{(d+1)}|.$$

*Proof.* Fix a panel $[x_j, x_j + h]$ and set $g(t) = f(x_j + h t)$ for $t \in [0, 1]$. Then $g^{(d+1)}(t) = h^{d+1} f^{(d+1)}(x_j + ht)$, and the exact integral and the rule on the panel are $h \int_0^1 g$ and $h \sum_i v_i g(t_i)$. Let $p$ be the Taylor polynomial of $g$ of degree $d$ at $0$. Taylor's theorem with the Lagrange remainder gives $|g(t) - p(t)| \le \max|g^{(d+1)}|\,t^{d+1}/(d+1)! \le \max|g^{(d+1)}|/(d+1)!$ on $[0, 1]$. The basic rule is exact for $p$, so its error on $g$ equals its error on $r = g - p$, which is $\int_0^1 r - \sum_i v_i r(t_i)$, of absolute value at most $(1 + L)\max|r|$. So the error on the panel is at most $h (1 + L) h^{d+1} \max|f^{(d+1)}|/(d+1)!$. There are $m$ panels and $mh = b - a$, so the sum of the panel errors is at most the bound of the theorem. $\square$

**Lemma (the mean value form).** If each panel error has the form $c\, h^{d+2} f^{(d+1)}(\xi_j)$ with the same constant $c$ and some $\xi_j$ in panel $j$, then $E(f) = c\,(b - a)\,h^{d+1} f^{(d+1)}(\xi)$ for some $\xi \in (a, b)$.

*Proof.* $E(f) = c h^{d+2} \sum_j f^{(d+1)}(\xi_j) = c h^{d+2} m \cdot \mu$, with $\mu = \frac1m \sum_j f^{(d+1)}(\xi_j)$. The mean $\mu$ lies between the smallest and the largest of the values $f^{(d+1)}(\xi_j)$, and $f^{(d+1)}$ is continuous, so the intermediate value theorem gives $\xi$ with $f^{(d+1)}(\xi) = \mu$. Then use $hm = b - a$. $\square$

**Floating point.** In line L8 a plain running sum of $m$ positive terms has a worst-case relative rounding error of about $(m-1)u$, with $u = 2^{-53}$ the unit roundoff ([floating-point summation](/floating-point-summation/)). [Pairwise summation](/pairwise-summation/) lowers the bound to about $u \log_2 m$, and [Kahan summation](/kahan-summation/) to about $2u$, independent of $m$. The truncation error falls like $h^{d+1}$ but the rounding error does not, so the total error has a floor near $u \cdot \int_a^b |f|$ at best, and the floor rises with plain summation as $m$ grows.

## Classic examples

The test integral is $\int_0^1 e^x\,dx = e - 1 = 1.718281828\ldots$, with $m$ panels.

| $m$ | trapezoid error | ratio | Simpson error | ratio | 2-point Gauss error | ratio |
|---|---|---|---|---|---|---|
| 1 | $-1.409 \times 10^{-1}$ | | $-5.793 \times 10^{-4}$ | | $3.855 \times 10^{-4}$ | |
| 2 | $-3.565 \times 10^{-2}$ | 3.95 | $-3.701 \times 10^{-5}$ | 15.65 | $2.466 \times 10^{-5}$ | 15.63 |
| 4 | $-8.940 \times 10^{-3}$ | 3.99 | $-2.326 \times 10^{-6}$ | 15.91 | $1.551 \times 10^{-6}$ | 15.91 |
| 8 | $-2.237 \times 10^{-3}$ | 4.00 | $-1.456 \times 10^{-7}$ | 15.98 | $9.706 \times 10^{-8}$ | 15.98 |
| 32 | $-1.398 \times 10^{-4}$ | | $-5.690 \times 10^{-10}$ | | $3.793 \times 10^{-10}$ | |

The errors match the table of the template: at $m = 32$, $\tfrac{1}{12}(1/32)^2 (e - 1) = 1.398 \times 10^{-4}$ and $\tfrac{1}{2880}(1/32)^4 (e - 1) = 5.690 \times 10^{-10}$, because the mean of $f'' = f^{(4)} = e^x$ over $[0, 1]$ is $e - 1$. The ratio 4 for each halving of $h$ is the rate $h^2$, and 16 is the rate $h^4$. The Gauss and Simpson errors have opposite signs and a ratio near $-2/3$, which is $2880/4320$ with the sign change.

- **[Composite trapezoidal rule](/trapezoidal-rule/).** Rate $h^2$ for $f \in C^2$. For a periodic analytic $f$ over a full period it converges geometrically: on $\int_0^{2\pi} e^{\cos x}\,dx = 2\pi I_0(1) = 7.954926521\ldots$ the errors for $m = 4, 8, 12, 16$ are $-3.4 \times 10^{-2}$, $-1.3 \times 10^{-6}$, $-6.5 \times 10^{-12}$ and $-8.9 \times 10^{-16}$. The reason is the [Euler-Maclaurin formula](/euler-maclaurin-formula/): all its correction terms cancel for a periodic $f$ (Trefethen and Weideman 2014, Section 3).
- **[Composite Simpson rule](/simpsons-rule/).** Rate $h^4$ for $f \in C^4$, with $2m + 1$ evaluations.
- **Composite [Gauss-Legendre rules](/gauss-legendre-quadrature/).** With $n$ nodes per panel the degree is $2n - 1$ and the rate is $h^{2n}$; the nodes are inside the panels, so no evaluation is shared and the cost is $mn$ evaluations.
- **Endpoint singularity.** On $\int_0^1 \sqrt{x}\,dx = 2/3$ the hypothesis $f \in C^2$ fails at $0$. The trapezoid errors for $m = 4, 16, 64, 256$ are $2.34 \times 10^{-2}$, $3.09 \times 10^{-3}$, $3.96 \times 10^{-4}$, $5.01 \times 10^{-5}$, and Simpson gives $3.59 \times 10^{-3}$, $4.49 \times 10^{-4}$, $5.61 \times 10^{-5}$, $7.01 \times 10^{-6}$. Both rates are $h^{1.5}$: the first panel, where $f$ is not smooth, sets the error, and a higher-degree basic rule gains only a constant. See [improper integration](/improper-integration/) for the cures.
- **Rounding.** Composite Simpson on $\int_0^1 e^x\,dx$ with $m = 2^{21}$ panels has a truncation error below $10^{-25}$. A plain left-to-right sum of the panel values has error $1.75 \times 10^{-14}$; `math.fsum` of the same panel values gives the correctly rounded sum, with error $0$ at that precision.

## Variations

- **Non-uniform panels.** Panel $j$ has its own width $h_j$, and the bound becomes $\frac{1+L}{(d+1)!}\sum_j h_j^{d+2}\max_{\text{panel } j}|f^{(d+1)}|$. Graded meshes, with panels that shrink geometrically toward a singular endpoint, restore the full rate for integrands like $\sqrt{x}$.
- **[Adaptive quadrature](/adaptive-quadrature/).** Choose the panels from the data: split a panel when an error estimate is large.
- **Extrapolation.** Composite trapezoid values for $h, h/2, h/4, \ldots$ combine into [Romberg integration](/romberg-integration/), which uses the even-power error expansion of the [Euler-Maclaurin formula](/euler-maclaurin-formula/).
- **End corrections.** Gregory's rules change only the weights near the two ends of the composite trapezoid rule and raise the order, with all inner weights equal to $h$.

## Pitfalls

- **Which $h$.** Simpson's error is $(b-a)h^4 f^{(4)}/2880$ with $h$ the panel width and $(b-a)h^4 f^{(4)}/180$ with $h$ the node spacing. Mixing the two conventions gives a factor 16 error in the predicted error.
- **Odd number of intervals for Simpson.** The textbook form needs an even number of node intervals. With the panel form of this page each panel has its own midpoint, so any $m$ works.
- **Evaluating shared endpoints twice.** A closed basic rule shares the end values of adjacent panels. Code that calls $f$ at both ends of each panel pays $mn$ evaluations instead of $m(n-1)+1$.
- **Expecting the rate without the smoothness.** The rate $h^{d+1}$ needs $f \in C^{d+1}$ on all of $[a, b]$. A kink, a jump, or an endpoint singularity lowers the rate to the one that the worst panel allows.
- **Nodes by repeated addition.** Computing $x_{j+1} = x_j + h$ in a loop accumulates an error of order $j u |x|$ in the nodes; compute $a + j h$ as in line L4.
- **Asking for more than the floor.** Past the point where the truncation error falls below the rounding error, a larger $m$ makes the result worse, not better.

## Exercises

1. Show that the composite midpoint rule and the composite trapezoidal rule on the same panels satisfy $T_{2m} = \tfrac12(T_m + M_m)$, and use it to reuse all old values when $m$ doubles.
2. Show that $\tfrac13(4T_{2m} - T_m)$ is the composite Simpson rule on $m$ panels.
3. For $f(x) = |x - 1/3|$ on $[0, 1]$, find the rate of the composite trapezoidal rule when $1/3$ is never a panel end, and explain why it does not drop below $h^2$.

## References
