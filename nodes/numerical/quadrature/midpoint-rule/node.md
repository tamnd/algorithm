---
tag: YFXF32
kind: algorithm
slug: midpoint-rule
name: Midpoint rule
aliases:
- rectangle rule
- midpoint rectangle rule
- composite midpoint rule
area: numerical/quadrature
level: intro
summary: Sample f at subinterval midpoints; error is O(h^2).
solves: [numerical-integration]
model: real-ram
complexity:
  vars: {m: "the number of subintervals, at least 1"}
  time: {worst: Θ(m), average: Θ(m), best: Θ(m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false}
prereqs: [quadrature-rule]
see_also: [trapezoidal-rule, simpsons-rule, composite-quadrature, newton-cotes-formulas, gauss-legendre-quadrature, improper-integration, explicit-midpoint-method]
sources:
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Section 2.1, Primitive rules (the rectangle and midpoint rules); Section 2.4, Compound rules; Section 2.6, Integration formulas of open type
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Sections 5.1 and 5.2 (the midpoint rule as the simplest open Newton-Cotes and Gauss rule)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 7, Numerical integration I (error estimates and composite formulae)
  - paper: doi:10.1137/130932132
    title: Lloyd N. Trefethen and J. A. C. Weideman, The exponentially convergent trapezoidal rule, SIAM Review 56(3), 2014, 385-458
    locator: Section 3 (the midpoint and trapezoidal sums of a periodic function are both equispaced sums and converge at the same geometric rate)
---

The midpoint rule approximates $\int_a^b f(x)\,dx$ by cutting $[a, b]$ into $m$ equal subintervals and adding the areas of rectangles whose heights are the values of $f$ at the midpoints. It is an open [quadrature rule](/quadrature-rule/) with $m$ nodes, all weights equal to $h$, [degree of exactness](/degree-of-precision/) 1, and error $(b - a) h^2 f''(\xi)/24$ for $f \in C^2[a, b]$. That error is half the size of the [trapezoidal rule](/trapezoidal-rule/) error and of the opposite sign, and the rule never evaluates $f$ at the ends of the interval.

## In plain words

Cut the interval into equal pieces. In each piece, look at the function only once, in the middle. Pretend the function is flat at that height across the piece, and add up the areas of the flat boxes.

A straight line through the middle point tilts up on one side and down on the other, so its area is the same as the flat box. So the box is right for every straight line, not only for flat ones. For a curved function, the error of each box is small and the errors of a bent curve all point the same way. Doubling the number of pieces cuts the error by about four. Because the ends are never touched, the rule still works when the function blows up at an end, though slowly.

## The problem

The input is a function $f$ that can be evaluated at the interior points of $[a, b]$, the ends $a$ and $b$, and an integer $m \ge 1$. The output is the composite midpoint sum

$$M_m(f) = h \sum_{i=1}^{m} f\big(a + (i - \tfrac12) h\big), \qquad h = \frac{b - a}{m},$$

an approximation to $I(f) = \int_a^b f(x)\,dx$ (weight $w = 1$). Here $m$ counts subintervals and also nodes: the rule has $n = m$ nodes. The error is $E_m(f) = I(f) - M_m(f)$, and the cost is the number of evaluations of $f$.

## The algorithm

```pseudo id=main
MIDPOINT(f, a, b, m)                       ▷ m ≥ 1 subintervals
L1  h ← (b − a) / m
L2  s ← 0
L3  for i ← 1 to m do
L4      s ← s + f(a + (i − 1/2) · h)       ▷ the midpoint of subinterval i
L5  return h · s
```

Line L1 fixes the width. The loop of lines L3 and L4 adds the value of $f$ at the middle of each subinterval, and line L5 multiplies by the common weight $h$. If $a = b$ the result is 0, and if $b < a$ it is minus the rule on $[b, a]$.

## Example

Take $f(x) = e^x$ on $[0, 1]$ with $m = 4$, so $h = 0.25$ and the midpoints are $0.125, 0.375, 0.625, 0.875$. The exact value is $e - 1 = 1.7182818285$.

| step | midpoint | $f$ at the midpoint | $s$ after the step |
|---|---|---|---|
| L4, $i = 1$ | $0.125$ | $1.1331484531$ | $1.1331484531$ |
| L4, $i = 2$ | $0.375$ | $1.4549914146$ | $2.5881398677$ |
| L4, $i = 3$ | $0.625$ | $1.8682459574$ | $4.4563858251$ |
| L4, $i = 4$ | $0.875$ | $2.3988752940$ | $6.8552611191$ |
| L5 | | | $M_4 = 0.25 \cdot s = 1.7138152798$ |

The error is $E_4 = 4.4665 \times 10^{-3}$. The asymptotic estimate $\frac{h^2}{24}(f'(b) - f'(a)) = 4.4747 \times 10^{-3}$ agrees to three digits, and the trapezoidal rule with the same $m$ has error $-8.9401 \times 10^{-3}$, about $-2$ times as large. When $m$ doubles from 1 to 64 the errors are $6.956 \times 10^{-2}$, $1.777 \times 10^{-2}$, $4.467 \times 10^{-3}$, $1.118 \times 10^{-3}$, $2.796 \times 10^{-4}$, $6.992 \times 10^{-5}$ and $1.748 \times 10^{-5}$, with ratios $3.915, 3.978, 3.995, 3.999, 4.000, 4.000$.

## Correctness

The algorithm returns $M_m(f)$, since the loop adds each midpoint value once. The main result, proved in full below, is:

- **Error theorem.** If $f \in C^2[a, b]$, then $E_m(f) = \frac{(b - a) h^2}{24} f''(\xi)$ for some $\xi \in [a, b]$. On one panel with midpoint $c$, Taylor's theorem gives $f(x) = f(c) + f'(c)(x - c) + \tfrac12 g(x)(x - c)^2$ with a continuous $g$ whose values are values of $f''$. The linear term integrates to 0 by symmetry, which is why the rule is exact for linear functions. The weight $(x - c)^2$ has one sign, so the mean value theorem for integrals gives $\frac{h^3}{24} f''(\eta)$ per panel, and the intermediate value theorem combines the $m$ panels.
- **Bound and degree.** So $|E_m(f)| \le \frac{(b - a) h^2}{24} \max |f''|$, the rule is exact for degree 1, and $E_m(x^2) = (b - a) h^2/12 \ne 0$.
- **Asymptotic expansion.** For $f \in C^{2K+2}[a, b]$, the [Euler-Maclaurin formula](/euler-maclaurin-formula/) for midpoint sums gives $E_m(f) = \frac{h^2}{24}(f'(b) - f'(a)) - \frac{7 h^4}{5760}(f'''(b) - f'''(a)) + \cdots + O(h^{2K+2})$, an expansion in even powers of $h$ like that of the trapezoidal rule. For a cubic $p$ the first term is exact: $E_m(p) = \frac{h^2}{24}(p'(b) - p'(a))$.

## Complexity

- **Evaluations.** Exactly $m$ values of $f$, one per subinterval, none at $a$ or $b$.
- **Arithmetic and memory.** $\Theta(m)$ operations and $\Theta(1)$ extra memory.
- **Work for a tolerance.** For $f \in C^2$, $\Theta(\tau^{-1/2})$ evaluations reach an error $\tau$, with half the constant of the trapezoidal rule: $m \ge \sqrt{(b - a)^3 \max|f''| / (24 \tau)}$ suffices by the theorem.
- **Floating point.** As for the trapezoidal rule, recursive summation in line L4 adds an error of up to about $(m - 1) u \sum_i |f(c_i)|$. The implementation sums with `math.fsum`, which rounds once, so the remaining error comes from the values $f(c_i)$ and from the computed midpoints.

## Properties

- **Open.** The nodes are interior points, so the rule applies to $\int_0^1 x^{-1/2}\,dx$, where $f(0)$ is infinite. The convergence is then slow: the error falls like $h^{1/2}$ for $x^{-1/2}$ and like $h$ for $\log x$, where the observed error is close to $-0.347 h$.
- **Positive and stable.** All weights equal $h > 0$ and sum to $b - a$.
- **Degree of exactness 1 with one node per panel.** On one panel it is the 1-point [Gauss-Legendre rule](/gauss-legendre-quadrature/), so it reaches the largest degree $2n - 1 = 1$ that one node allows.
- **Opposite error to the trapezoidal rule.** For $f \in C^2$, $E(M_m) \approx -\tfrac12 E(T_m)$. For convex $f$, $M_m(f) \le I(f) \le T_m(f)$. The combination $\frac{2 M_m + T_m}{3}$ is the composite [Simpson's rule](/simpsons-rule/) with $2m$ subintervals.
- **Nesting by thirds.** The midpoints of $M_m$ are among those of $M_{3m}$, not of $M_{2m}$. Halving $h$ needs all new values, while tripling reuses the old ones.

## Variants and improvements

- **Left and right rectangle rules.** $h \sum_{i=0}^{m-1} f(a + i h)$ uses the left ends. Its degree of exactness is 0 and its error is $O(h)$. These are the Riemann sums of calculus courses and are not a substitute for the midpoint rule.
- **Open Newton-Cotes rules.** The midpoint rule is the open [Newton-Cotes formula](/newton-cotes-formulas/) with one node. Open rules with more nodes have higher degree but soon get negative weights.
- **Gauss rules.** [Gauss-Legendre quadrature](/gauss-legendre-quadrature/) with $n$ nodes per panel generalizes the midpoint rule to degree $2n - 1$.
- **Periodic integrands.** For a periodic $f$ over a full period, the midpoint sum is an equispaced sum like the periodic trapezoidal rule, and it converges at the same geometric rate (Trefethen and Weideman 2014, Section 3).
- **Explicit midpoint method.** Applied to $y' = f(x)$, the [explicit midpoint method](/explicit-midpoint-method/) for ODEs reduces to the midpoint rule.

## When to use it

Use the midpoint rule when the integrand cannot be evaluated at the ends, when a simple rule of second order is enough, or inside a larger scheme such as a step of an ODE solver or a cell average of a finite volume method. It has half the error of the trapezoidal rule for one fewer evaluation. Prefer the [trapezoidal rule](/trapezoidal-rule/) when you want to halve $h$ and reuse old values, as in [Romberg integration](/romberg-integration/). For high accuracy on a smooth integrand, use [Gaussian quadrature](/gaussian-quadrature/), and for an endpoint singularity use a change of variable such as [tanh-sinh quadrature](/tanh-sinh-quadrature/) instead of many midpoints.

## Pitfalls

- **Nodes at the left ends.** Writing line L4 as $f(a + (i - 1) h)$ gives the left rectangle rule. Its error is $O(h)$, not $O(h^2)$. The node must be the midpoint $a + (i - \tfrac12) h$.
- **Accumulated nodes.** Computing the midpoints by $x \leftarrow x + h$ in line L4 lets rounding errors in the nodes grow with $i$. Compute each midpoint from $a$, as line L4 does.
- **Halving $h$ with reuse.** Code that refines $M_m$ to $M_{2m}$ cannot reuse any old value, because no old midpoint is a new midpoint. Refine by a factor of 3, or use $T_{2m} = \tfrac12 (T_m + M_m)$.
- **Trusting the $h^2$ rate near a singularity.** For $x^{-1/2}$ on $[0, 1]$ the error with $m = 2048$ is still $1.3 \times 10^{-2}$. The theorem needs $f \in C^2[a, b]$, which fails here.

## Implementations

## History

The midpoint rule is the oldest form of the rectangle sums that define the Riemann integral, and it is the open Newton-Cotes rule with one node. Davis and Rabinowitz (Section 2.1) list it among the primitive rules, with the trapezoidal and Simpson rules. Its error constant $1/24$ and the opposite sign of the trapezoidal error are classical and appear in all the textbooks cited here.

## References
