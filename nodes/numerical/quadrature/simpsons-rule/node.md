---
tag: CWAN1Z
kind: algorithm
slug: simpsons-rule
name: Simpson's rule
aliases:
- Simpson rule
- Simpson's 1/3 rule
- composite Simpson rule
- Kepler's barrel rule
area: numerical/quadrature
level: intro
summary: Integrate the quadratic interpolant over pairs of subintervals; error is O(h^4).
solves: [numerical-integration]
model: real-ram
complexity:
  vars: {m: "the number of subintervals, even and at least 2"}
  time: {worst: Θ(m), average: Θ(m), best: Θ(m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 1743
  people: [Thomas Simpson]
  note: Simpson published the rule in 1743; Kepler had used the same formula for the volume of wine barrels in 1615.
prereqs: [trapezoidal-rule, polynomial-interpolation]
see_also: [midpoint-rule, newton-cotes-formulas, composite-quadrature, adaptive-quadrature, romberg-integration, richardson-extrapolation, peano-kernel-theorem, gauss-legendre-quadrature]
sources:
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Section 2.2, Simpson's rule; Section 2.4, Compound rules
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Section 5.1, The trapezoidal rule and Simpson's rule (the error formula with f'''' and the composite rule)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 7, Numerical integration I (Simpson's rule, its error and the composite rule)
  - book: "Thomas Simpson, Mathematical Dissertations on a Variety of Physical and Analytical Subjects, London, 1743"
    locator: the rule for the area under a curve by parabolic arcs
  - book: "Johannes Kepler, Nova stereometria doliorum vinariorum, Linz, 1615"
    locator: the barrel rule for volumes
---

Simpson's rule approximates $\int_a^b f(x)\,dx$ by cutting $[a, b]$ into an even number $m$ of subintervals of width $h$ and replacing $f$ on each pair of subintervals by the parabola through its three points. The result is the weighted sum $\frac{h}{3}(f_0 + 4 f_1 + 2 f_2 + 4 f_3 + \cdots + 4 f_{m-1} + f_m)$. It is a [quadrature rule](/quadrature-rule/) with $m + 1$ nodes and [degree of exactness](/degree-of-precision/) 3, one more than its construction suggests, and its error is $-(b - a) h^4 f^{(4)}(\xi)/180$ for $f \in C^4[a, b]$.

## In plain words

Cut the interval into an even number of equal pieces and take them two at a time. On each pair you know the function at three points: the left end, the middle and the right end. Draw the parabola through these three points and take its exact area. Add up the areas of all the parabolas.

The area under one parabola is the width times a weighted average of the three heights, with weights 1, 4 and 1. So the whole rule is a weighted sum with the pattern 1, 4, 2, 4, 2, and so on, ending with 4 and 1. The middle point is symmetric, and this gives the rule a bonus: it is exact even for cubic curves. Doubling the number of pieces divides the error of a smooth function by about sixteen.

## The problem

The input is a function $f$ that can be evaluated on $[a, b]$, the ends $a$ and $b$, and an even integer $m \ge 2$. The output is the composite Simpson sum

$$S_m(f) = \frac{h}{3}\Big( f(x_0) + 4 \sum_{i \text{ odd}} f(x_i) + 2 \sum_{\substack{0 < i < m \\ i \text{ even}}} f(x_i) + f(x_m) \Big), \qquad h = \frac{b - a}{m},\; x_i = a + i h,$$

an approximation to $I(f) = \int_a^b f(x)\,dx$ (weight $w = 1$). Here $m$ counts subintervals; the rule has $n = m + 1$ nodes. The error is $E_m(f) = I(f) - S_m(f)$, and the cost is the number of evaluations of $f$.

## The algorithm

```pseudo id=main
SIMPSON(f, a, b, m)                        ▷ m ≥ 2 and m even
L1  h ← (b − a) / m
L2  s ← f(a) + f(b)                        ▷ the ends have coefficient 1
L3  for i ← 1 to m − 1 do
L4      if i is odd then s ← s + 4 · f(a + i · h)    ▷ centres of the double panels
L5      else s ← s + 2 · f(a + i · h)                ▷ shared ends of two double panels
L6  return h · s / 3
```

Each double panel $[x_{2j-2}, x_{2j}]$ contributes $\frac{h}{3}(f(x_{2j-2}) + 4 f(x_{2j-1}) + f(x_{2j}))$, the integral of the quadratic interpolant at its three nodes. An inner node with even index ends one double panel and starts the next, so it gets coefficient $1 + 1 = 2$ (line L5). Each odd node is a centre and gets 4 (line L4). The ends get 1 (line L2). If $a = b$ the result is 0, and if $b < a$ it is minus the rule on $[b, a]$.

## Example

Take $f(x) = e^x$ on $[0, 1]$ with $m = 4$, so $h = 0.25$. The exact value is $e - 1 = 1.7182818285$.

| step | node | coefficient | $f$ at the node | $s$ after the step |
|---|---|---|---|---|
| L2 | $0$ and $1$ | 1 and 1 | $1$ and $2.7182818285$ | $3.7182818285$ |
| L4, $i = 1$ | $0.25$ | 4 | $1.2840254167$ | $8.8543834952$ |
| L5, $i = 2$ | $0.5$ | 2 | $1.6487212707$ | $12.1518260366$ |
| L4, $i = 3$ | $0.75$ | 4 | $2.1170000166$ | $20.6198261031$ |
| L6 | | | | $S_4 = 0.25 \cdot s / 3 = 1.7183188419$ |

The error is $E_4 = -3.7013 \times 10^{-5}$, compared with $-8.94 \times 10^{-3}$ for the trapezoidal rule on the same five values. The asymptotic estimate $-\frac{h^4}{180}(f'''(b) - f'''(a)) = -3.7289 \times 10^{-5}$ agrees to two digits. For $m = 2, 4, \ldots, 128$ the errors are $-5.79 \times 10^{-4}$, $-3.70 \times 10^{-5}$, $-2.33 \times 10^{-6}$, $-1.46 \times 10^{-7}$, $-9.10 \times 10^{-9}$, $-5.69 \times 10^{-10}$ and $-3.56 \times 10^{-11}$. The ratios $15.65, 15.91, 15.98, 15.99, 16.00, 16.00$ approach $2^4 = 16$.

## Correctness

The algorithm returns $S_m(f)$, because the loop gives each inner node its coefficient 4 or 2. The full proof below has three steps.

- **Degree of exactness 3.** On a double panel centred at $c$, write $t = x - c$. The basic rule $\frac{h}{3}(f(c - h) + 4 f(c) + f(c + h))$ is exact for $1$ and $t^2$ by direct computation, and for $t$ and $t^3$ because both the integral and the rule of an odd function vanish. For $x^4$ the error is $-\frac{2 (b - a) h^4}{15} \ne 0$.
- **Error on one double panel.** Let $q$ be the cubic that matches $f$ at $c - h$, $c$, $c + h$ and matches $f'$ at $c$. The rule cannot see the difference between $f$ and $q$, and it is exact for $q$. The Hermite error is $f^{(4)}(\zeta)/24$ times $(t^2 - h^2) t^2 \le 0$, a factor of one sign. The mean value theorem for integrals gives the panel error $-\frac{h^5}{90} f^{(4)}(\eta)$.
- **Composite error.** Summing over the $m/2$ double panels and applying the intermediate value theorem gives, for $f \in C^4[a, b]$,

$$E_m(f) = -\frac{(b - a)\, h^4}{180} f^{(4)}(\xi), \qquad \xi \in [a, b].$$

So $|E_m(f)| \le \frac{(b - a) h^4}{180} \max |f^{(4)}|$ is a proved bound. For $f \in C^6$, the [Euler-Maclaurin formula](/euler-maclaurin-formula/) gives the asymptotic form $E_m(f) = -\frac{h^4}{180}(f'''(b) - f'''(a)) + O(h^6)$, which is exact for polynomials of degree at most 5. The [Peano kernel theorem](/peano-kernel-theorem/) gives the same constant $1/180$ and also the bound $\frac{(b - a) h^3}{72}\max|f'''|$ for $f \in C^3$ only.

## Complexity

- **Evaluations.** Exactly $m + 1$ values of $f$, as for the trapezoidal rule with the same nodes.
- **Arithmetic and memory.** $\Theta(m)$ operations and $\Theta(1)$ extra memory.
- **Work for a tolerance.** For $f \in C^4$, $m \ge \big((b - a)^5 \max|f^{(4)}| / (180 \tau)\big)^{1/4}$ subintervals give an error at most $\tau$. So the work is $\Theta(\tau^{-1/4})$, against $\Theta(\tau^{-1/2})$ for the trapezoidal rule.
- **Floating point.** The weights are positive and sum to $b - a$. Recursive summation adds an error of up to about $m u$ times $\sum$ of the absolute terms. The implementation uses `math.fsum`, so the attainable accuracy is set by the errors in the values of $f$, about $(b - a)$ times the largest error of one value. For $4/(1 + x^2)$ on $[0, 1]$, $S_{128}$ is already within $9 \times 10^{-15}$ of $\pi$, and more subintervals cannot improve on this level.

## Properties

- **Exact for cubics.** The degree of exactness is 3 although the rule integrates a quadratic interpolant. The reason is symmetry: the error functional vanishes on $t^3$.
- **Positive weights.** The weights $\frac{h}{3}(1, 4, 2, \ldots, 4, 1)$ are positive, so the rule is stable.
- **Extrapolated trapezoid.** $S_m = \frac{4 T_m - T_{m/2}}{3}$, where $T_m$ is the [trapezoidal rule](/trapezoidal-rule/). This is one step of [Richardson extrapolation](/richardson-extrapolation/) and the second column of [Romberg integration](/romberg-integration/). Also $S_{2m} = \frac{T_m + 2 M_m}{3}$ with the [midpoint rule](/midpoint-rule/) $M_m$.
- **Closed Newton-Cotes.** One double panel is the closed [Newton-Cotes formula](/newton-cotes-formulas/) with three nodes.
- **Sign of the error.** If $f^{(4)} \ge 0$ on $[a, b]$, then $S_m(f) \ge I(f)$.

## Variants and improvements

- **Simpson's 3/8 rule.** The 4-point closed Newton-Cotes rule $\frac{3h}{8}(f_0 + 3 f_1 + 3 f_2 + f_3)$ also has degree 3, with panel error $-\frac{3 h^5}{80} f^{(4)}(\eta)$. It is used when the number of subintervals is odd: apply it to three subintervals and Simpson's rule to the rest.
- **Adaptive Simpson.** [Adaptive quadrature](/adaptive-quadrature/) compares $S$ on a panel with the sum of $S$ on its two halves and subdivides where they differ by more than the local tolerance. The difference divided by 15 estimates the error of the finer value.
- **Boole's rule and Romberg.** One more extrapolation step, $\frac{16 S_{2m} - S_m}{15}$, gives the composite Boole rule of degree 5. Continuing gives [Romberg integration](/romberg-integration/).
- **Gauss rules.** The 2-point [Gauss-Legendre rule](/gauss-legendre-quadrature/) also has degree 3, but with 2 nodes per panel instead of 3 (2 shared). It cannot reuse values between panels.

## When to use it

Use Simpson's rule for smooth integrands given at equally spaced points, or when you want a simple rule of order 4 with positive weights. It is a good default for tabulated data with an odd number of points. For an integrand that you can evaluate anywhere, [Gaussian quadrature](/gaussian-quadrature/) or [Clenshaw-Curtis quadrature](/clenshaw-curtis-quadrature/) reaches the same accuracy with fewer evaluations, and [adaptive quadrature](/adaptive-quadrature/) handles integrands whose difficulty is local. Its $h^4$ rate needs $f \in C^4$: for $\sqrt{x}$ on $[0, 1]$ the observed order is 1.5, the same as for the trapezoidal rule, so the extra work buys nothing there.

## Pitfalls

- **An odd number of subintervals.** With odd $m$, the 1, 4, 2 pattern of lines L4 and L5 does not end with 4, 1, and the sum is not a Simpson rule. The implementation rejects odd $m$. Use the 3/8 rule on three subintervals.
- **Swapped coefficients.** Giving coefficient 4 to the even nodes and 2 to the odd ones (swapping lines L4 and L5) produces weights that are not those of any interpolatory rule, and the error becomes $O(h)$.
- **Counting $m$ as nodes.** Some texts write the rule with $2n$ subintervals or with $n$ "panels". Mixing these conventions changes $h$ by a factor 2 and the error estimate by a factor 16. On this page, $m$ is the number of subintervals and $h = (b - a)/m$.
- **Judging the order from one example.** For $4/(1 + x^2)$ on $[0, 1]$, $f'''(0) = f'''(1)$, so the $h^4$ term of the expansion vanishes and the observed error falls like $h^6$ (ratios near 64). This is a property of the integrand, not of the rule.

## Implementations

## History

The rule is named after Thomas Simpson, who published it in 1743 in his Mathematical Dissertations. It is older: Kepler used the same formula, with weights 1, 4, 1, for the volume of wine barrels in his Nova stereometria doliorum vinariorum of 1615, and in German it is still called the Keplersche Fassregel. Its error term with $f^{(4)}$ and the constant $1/180$ are classical and appear in all modern texts, for example in Davis and Rabinowitz, Section 2.2.

## References
