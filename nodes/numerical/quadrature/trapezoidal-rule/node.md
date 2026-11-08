---
tag: K7MAWR
kind: algorithm
slug: trapezoidal-rule
name: Trapezoidal rule
aliases:
- trapezoid rule
- composite trapezoidal rule
- trapezium rule
area: numerical/quadrature
level: intro
summary: Integrate the piecewise linear interpolant of f; error is O(h^2).
solves: [numerical-integration]
model: real-ram
complexity:
  vars: {m: "the number of subintervals, at least 1"}
  time: {worst: Θ(m), average: Θ(m), best: Θ(m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false}
prereqs: [quadrature-rule, piecewise-linear-interpolation]
see_also: [midpoint-rule, simpsons-rule, composite-quadrature, euler-maclaurin-formula, romberg-integration, tanh-sinh-quadrature, sinc-quadrature, kahan-summation]
sources:
  - paper: doi:10.1137/130932132
    title: Lloyd N. Trefethen and J. A. C. Weideman, The exponentially convergent trapezoidal rule, SIAM Review 56(3), 2014, 385-458
    locator: Section 2 (the Euler-Maclaurin view), Section 3 (periodic integrands, Theorem 3.2 with the bound 4 pi M/(e^(aN) - 1)) and Section 5 (integrals over the real line)
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Section 2.1, Primitive rules; Section 2.4, Compound rules; Section 2.9, Integration of periodic functions
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Section 5.1, The trapezoidal rule and Simpson's rule (the error formula), and Section 5.4 (the Euler-MacLaurin formula)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 7, Numerical integration I (the composite trapezium rule and the Euler-Maclaurin expansion)
  - paper: doi:10.1126/science.aad8085
    title: Mathieu Ossendrijver, Ancient Babylonian astronomers calculated Jupiter's position from the area under a time-velocity graph, Science 351(6272), 2016, 482-484
    locator: the trapezoid procedure on the cuneiform tablets
---

The trapezoidal rule approximates $\int_a^b f(x)\,dx$ by the integral of the [piecewise linear interpolant](/piecewise-linear-interpolation/) of $f$ on $m$ equal subintervals. It is a [quadrature rule](/quadrature-rule/) with $m + 1$ nodes, weights $h/2, h, \ldots, h, h/2$ and [degree of exactness](/degree-of-precision/) 1, and its error is $-(b - a) h^2 f''(\xi)/12$ for $f \in C^2[a, b]$. For a periodic analytic integrand over a full period, the same rule converges geometrically, which makes it one of the best rules known for that case.

## In plain words

Cut the interval into equal pieces. On each piece, draw a straight line from the value of the function at the left end to its value at the right end. The area under each line is a trapezoid, and the sum of the trapezoids approximates the area under the curve.

Each inner point is shared by two trapezoids, so its value counts in full, and the two end values count half. If you double the number of pieces, the error of a smooth function drops by about four. If the function repeats itself, like a wave, and you integrate over one full period, the errors of the pieces cancel almost completely, and a few dozen points can give full machine accuracy.

## The problem

The input is a function $f$ that can be evaluated at any point of $[a, b]$, the ends $a$ and $b$, and an integer $m \ge 1$. The output is the composite trapezoidal sum

$$T_m(f) = h \Big( \tfrac12 f(x_0) + \sum_{i=1}^{m-1} f(x_i) + \tfrac12 f(x_m) \Big), \qquad h = \frac{b - a}{m},\; x_i = a + i h,$$

an approximation to $I(f) = \int_a^b f(x)\,dx$ (weight $w = 1$). Here $m$ counts subintervals; the rule has $n = m + 1$ nodes. The error is $E_m(f) = I(f) - T_m(f)$. The cost is counted in evaluations of $f$.

## The algorithm

```pseudo id=main
TRAPEZOID(f, a, b, m)                      ▷ m ≥ 1 subintervals
L1  h ← (b − a) / m
L2  s ← (f(a) + f(b)) / 2                  ▷ the two ends get half weight
L3  for i ← 1 to m − 1 do
L4      s ← s + f(a + i · h)               ▷ inner nodes, each computed from a, not by x ← x + h
L5  return h · s
```

Line L2 adds the end values with weight one half. The loop of lines L3 and L4 adds each inner value once. Line L5 scales by the width $h$. If $a = b$, then $h = 0$ and the result is 0. If $b < a$, then $h < 0$ and the result is $-T_m$ on $[b, a]$, which matches the convention $\int_a^b = -\int_b^a$.

## Example

Take $f(x) = e^x$ on $[0, 1]$ with $m = 4$, so $h = 0.25$. The exact value is $e - 1 = 1.7182818285$.

| step | node $x_i$ | $f(x_i)$ | $s$ after the step |
|---|---|---|---|
| L2 | $0$ and $1$ | $1$ and $2.7182818285$ | $1.8591409142$ |
| L4, $i = 1$ | $0.25$ | $1.2840254167$ | $3.1431663309$ |
| L4, $i = 2$ | $0.5$ | $1.6487212707$ | $4.7918876016$ |
| L4, $i = 3$ | $0.75$ | $2.1170000166$ | $6.9088876182$ |
| L5 | | | $T_4 = 0.25 \cdot s = 1.7272219046$ |

The error is $E_4 = -8.940 \times 10^{-3}$. The asymptotic formula $-\frac{h^2}{12}(f'(b) - f'(a)) = -\frac{0.0625}{12}(e - 1) = -8.949 \times 10^{-3}$ predicts it to three digits. When $m$ doubles, the error drops by a factor close to 4:

| $m$ | 1 | 2 | 4 | 8 | 16 | 32 | 64 |
|---|---|---|---|---|---|---|---|
| $E_m$ | $-1.409 \times 10^{-1}$ | $-3.565 \times 10^{-2}$ | $-8.940 \times 10^{-3}$ | $-2.237 \times 10^{-3}$ | $-5.593 \times 10^{-4}$ | $-1.398 \times 10^{-4}$ | $-3.496 \times 10^{-5}$ |
| ratio | | 3.951 | 3.988 | 3.997 | 3.999 | 4.000 | 4.000 |

For the periodic $f(x) = e^{\cos x}$ on $[0, 2\pi]$, with $I = 2\pi I_0(1) = 7.954926521$, the errors are $-1.74$ for $m = 2$, $-3.44 \times 10^{-2}$ for $m = 4$, $-1.25 \times 10^{-6}$ for $m = 8$, $-6.5 \times 10^{-12}$ for $m = 12$ and below $10^{-15}$ for $m = 16$. The number of correct digits grows linearly with $m$.

## Correctness

The algorithm returns $T_m(f)$: line L2 and the loop add each node once with the right weight. The key facts are two error theorems, proved in full below.

- **Smooth case.** If $f \in C^2[a, b]$, then $E_m(f) = -\frac{(b - a) h^2}{12} f''(\xi)$ for some $\xi \in [a, b]$. The proof applies the interpolation error formula on each panel, uses that $(x - x_j)(x - x_{j+1})$ has one sign on the panel, and averages the panel errors with the intermediate value theorem. So the degree of exactness is 1, and $|E_m(f)| \le \frac{(b - a) h^2}{12} \max |f''|$ is a proved bound.
- **Asymptotic expansion.** If $f \in C^{2K+2}[a, b]$, the [Euler-Maclaurin formula](/euler-maclaurin-formula/) gives $T_m(f) - I(f) = \sum_{k=1}^{K} \frac{B_{2k}}{(2k)!} h^{2k} \big(f^{(2k-1)}(b) - f^{(2k-1)}(a)\big) + O(h^{2K+2})$, with the Bernoulli numbers $B_2 = \tfrac16$, $B_4 = -\tfrac{1}{30}$. The first term is the estimate $-\frac{h^2}{12}(f'(b) - f'(a))$ for $E_m$ used in the example. This expansion is the base of [Romberg integration](/romberg-integration/).
- **Periodic case.** If $f$ is $2\pi$-periodic and analytic with $|f| \le M$ in the strip $|\operatorname{Im} z| < \alpha$, then on $[0, 2\pi]$, $|E_m(f)| \le 4\pi M/(e^{\alpha m} - 1)$ (Trefethen and Weideman 2014, Theorem 3.2). The proof writes $T_m$ through aliasing as $2\pi \sum_\ell c_{\ell m}$, where $c_k$ are the Fourier coefficients, and bounds $|c_k| \le M e^{-\alpha |k|}$ by shifting the contour. For $e^{\cos x}$, $M = e^{\cosh \alpha}$ for every $\alpha > 0$, and the bound is $9.0 \times 10^{-6}$ at $m = 8$, above the observed $1.25 \times 10^{-6}$.

## Complexity

- **Evaluations.** Exactly $m + 1$ values of $f$: two in line L2 and $m - 1$ in line L4. This is the cost that matters when $f$ is expensive.
- **Arithmetic.** $\Theta(m)$ additions and multiplications, and $\Theta(1)$ extra memory. With the exact sum of the implementation (Python's `math.fsum`), the summation still takes $O(m)$ time.
- **Work for a tolerance.** For $f \in C^2$ with $f'' \ne 0$ somewhere, the error is $\Theta(m^{-2})$, so $\Theta(\tau^{-1/2})$ evaluations reach an error $\tau$. For a periodic analytic $f$ over a period, $O(\log(1/\tau))$ evaluations suffice.
- **Floating point.** In line L4, recursive summation adds a rounding error of up to about $(m - 1) u \sum_i |f(x_i)|$, so with $h \sum |f(x_i)| \approx (b - a) \max |f|$ the floor grows like $m u$ while the truncation error falls like $m^{-2}$. The total error of recursive summation is smallest near $m \approx u^{-1/3} \approx 2 \times 10^5$ in double precision. With [pairwise](/pairwise-summation/) or [Kahan summation](/kahan-summation/), or a correctly rounded sum, this floor disappears, and the limit of attainable accuracy is set by the errors in the values $f(x_i)$ and in the nodes $a + i h$: about $(b - a)$ times the largest error of one value.

## Properties

- **Degree of exactness 1.** It integrates every linear function exactly, and $E_m(x^2) = -(b - a) h^2/6$.
- **Positive weights.** All weights are positive and sum to $b - a$, so the rule is stable: errors $\delta$ in the data change the result by at most $(b - a)\delta$.
- **Closed and nested.** It uses both endpoints. The nodes of $T_m$ are among the nodes of $T_{2m}$, and $T_{2m} = \tfrac12 T_m + \tfrac{h}{2} \sum_{j=1}^{m} f(a + (j - \tfrac12) h) = \tfrac12 (T_m + M_m)$, where $M_m$ is the [midpoint rule](/midpoint-rule/). So halving $h$ costs only $m$ new values.
- **Error sign.** For a convex $f$ ($f'' \ge 0$) the rule overestimates: $E_m \le 0$. The midpoint rule then underestimates, and $I$ lies between $M_m$ and $T_m$.
- **Exact for trigonometric polynomials.** On a full period, $T_m$ integrates $e^{ikx}$ exactly for $|k| < m$, so it has trigonometric degree $m - 1$. This is the reason for the geometric convergence in the periodic case.

## Variants and improvements

- **Periodic trapezoidal rule.** For $f$ with period $b - a$, use $h \sum_{i=0}^{m-1} f(a + i h)$: the two ends are the same point. This is the rule behind the [discrete Fourier transform](/discrete-fourier-transform/) and its error is geometric for analytic $f$.
- **Trapezoidal rule on the real line.** $h \sum_{k=-\infty}^{\infty} f(kh)$ converges geometrically for $f$ analytic in a strip and decaying fast. After a change of variable this gives [sinc quadrature](/sinc-quadrature/) and [tanh-sinh quadrature](/tanh-sinh-quadrature/).
- **End corrections.** Adding $\frac{h^2}{12}(f'(a) - f'(b))$ cancels the $h^2$ term of the expansion and gives an $O(h^4)$ rule that uses derivative data. Gregory's rule does the same with differences of function values.
- **Extrapolation.** $\frac{4 T_{2m} - T_m}{3}$ is [Simpson's rule](/simpsons-rule/), and repeating the step gives [Romberg integration](/romberg-integration/). See [Richardson extrapolation](/richardson-extrapolation/).
- **Nonuniform nodes.** For tabulated data at points $t_0 < \cdots < t_n$, use $\sum_j \frac{t_{j+1} - t_j}{2}(f(t_j) + f(t_{j+1}))$. The error per panel is still $-\frac{(t_{j+1} - t_j)^3}{12} f''(\eta_j)$.

## When to use it

Use the trapezoidal rule for a periodic integrand over a full period: there it beats Gauss rules with the same number of points, as the example of $e^{\cos x}$ shows. Use it for tabulated data at equally spaced points, and as the base of Romberg integration or of a change of variable for endpoint singularities. For a smooth non-periodic integrand on a finite interval, [Simpson's rule](/simpsons-rule/), [Gaussian quadrature](/gaussian-quadrature/) or [Clenshaw-Curtis quadrature](/clenshaw-curtis-quadrature/) reach the same accuracy with far fewer evaluations. For an integrand with a kink or a jump inside the interval, put a node at that point, or split the interval there.

## Pitfalls

- **Full weight at the ends.** Writing line L2 as $s \leftarrow f(a) + f(b)$ adds $\frac{h}{2}(f(a) + f(b))$ too much and makes the error $O(h)$ instead of $O(h^2)$. The ends need the factor $\tfrac12$.
- **Accumulated nodes.** Computing the nodes in line L4 as $x \leftarrow x + h$ adds one rounding error per step, so the last node can be off by about $m u |b|$. Compute $a + i \cdot h$ (or $a + (b - a) i/m$) as line L4 does.
- **Both ends in the periodic case.** For a periodic integrand, $h \sum_{i=0}^{m} f(x_i)$ with full weights counts the point $a = b$ twice. Use half weights at both ends, or the sum from $0$ to $m - 1$.
- **Assuming $O(h^2)$ without smoothness.** For $f(x) = \sqrt{x}$ on $[0, 1]$, $f''$ is unbounded and the error falls like $h^{3/2}$ (observed order 1.50 between $m = 256$ and $m = 2048$). For a jump inside the interval the error is $O(h)$. Theorem 1 needs $f \in C^2[a, b]$.
- **Long sums.** For very large $m$, plain recursive summation in line L4 lets the rounding error grow like $m u$. Use a compensated or pairwise sum, as the implementation does with `math.fsum`.

## Implementations

## History

The rule is much older than calculus. Ossendrijver (2016) showed that Babylonian astronomers computed the distance travelled by Jupiter as the area of a trapezoid under a time-velocity graph. In the modern form it is the closed Newton-Cotes rule with two points. Its error expansion in even powers of $h$ is the Euler-Maclaurin formula of Euler and Maclaurin (1730s and 1740s), which Romberg used in 1955 for his extrapolation method. Trefethen and Weideman (2014) survey the geometric convergence for periodic integrands and for integrals over the real line, and trace it back to Poisson (1827).

## References
