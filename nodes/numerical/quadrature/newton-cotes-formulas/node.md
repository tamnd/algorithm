---
tag: BB06D0
kind: algorithm
slug: newton-cotes-formulas
name: Newton-Cotes formulas
aliases:
- Newton-Cotes rules
- closed Newton-Cotes formulas
- open Newton-Cotes formulas
- Newton-Cotes quadrature
area: numerical/quadrature
level: core
summary: Interpolatory rules on equally spaced nodes; trapezoid, Simpson and Boole's rules are members.
solves: [numerical-integration]
model: real-ram
complexity:
  vars: {n: "the number of nodes per panel", m: "the number of panels, at least 1"}
  time: {worst: Θ(m n + n^3), average: Θ(m n + n^3), best: Θ(m n + n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [interpolatory-quadrature]
see_also: [trapezoidal-rule, simpsons-rule, midpoint-rule, composite-quadrature, clenshaw-curtis-quadrature, runge-phenomenon, gaussian-quadrature, romberg-integration]
sources:
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Section 2.5, Integration formulas of interpolatory type (the closed Newton-Cotes rules, their weights and error terms); Section 2.6, Integration formulas of open type
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Sections 5.1 and 5.2 (the trapezoidal and Simpson rules, and the general Newton-Cotes formulas with their error theorem)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 7, Numerical integration I (Newton-Cotes formulae, error estimates, the Runge phenomenon revisited, composite formulae)
  - paper: "George Pólya, Über die Konvergenz von Quadraturverfahren, Mathematische Zeitschrift 37 (1933), 264-286"
    locator: divergence of the Newton-Cotes rules for analytic integrands
  - book: "Roger Cotes, Harmonia mensurarum, Cambridge, 1722"
    locator: De methodo differentiali Newtoniana (the coefficients of the closed rules with up to 11 points)
  - book: "Isaac Newton, Methodus differentialis, London, 1711"
    locator: interpolation through equally spaced points and the three-eighths rule
---

The Newton-Cotes formulas are the [interpolatory quadrature rules](/interpolatory-quadrature/) whose nodes are equally spaced. The closed rule with $n$ points uses both ends of the interval, the open rule uses only interior points, and their weights are rational numbers computed once from the moment equations. The [trapezoidal rule](/trapezoidal-rule/) ($n = 2$), [Simpson's rule](/simpsons-rule/) ($n = 3$), the three-eighths rule ($n = 4$) and Boole's rule ($n = 5$) are the closed members, and the [midpoint rule](/midpoint-rule/) is the open rule with one point. The $n$-point rule has degree of exactness $n - 1$ for even $n$ and $n$ for odd $n$. For large $n$ the weights take both signs and grow, and the rules can diverge even for analytic integrands, so in practice a rule of small $n$ is applied on $m$ panels.

## In plain words

Put a few equally spaced points on the interval, run a polynomial curve through the function values there, and take the exact area under that curve. Two points give a straight line and the trapezoid. Three points give a parabola and Simpson's rule. Any number of points gives a fixed recipe of weights: multiply each function value by its weight and add up.

A symmetric set of points with an odd count gets one degree of accuracy for free, which is why Simpson's rule with three points is as good as the rule with four. Many equally spaced points is a bad idea: the curve through them can swing wildly near the ends, some weights become negative and large, and the answer gets worse. The safe way to get more accuracy is to cut the interval into many pieces and use a small rule on each.

## The problem

The input is a function $f$, an interval $[a, b]$, the number of nodes $n$ per panel, whether the rule is closed or open, and the number of panels $m \ge 1$. With $H = (b - a)/m$, the output is the composite Newton-Cotes sum

$$Q(f) = H \sum_{j=0}^{m-1} \sum_{i=1}^{n} W_i\, f\big(a + (j + t_i) H\big),$$

an approximation to $I(f) = \int_a^b f(x)\,dx$, with weight $w = 1$. The reference nodes are $t_i = (i - 1)/(n - 1)$ for a closed rule ($n \ge 2$) and $t_i = i/(n + 1)$ for an open rule ($n \ge 1$), and $W_i = \int_0^1 \ell_i(t)\,dt$ are the integrals of the Lagrange basis polynomials. The node spacing inside a panel is $h = H/(n - 1)$ (closed) or $h = H/(n + 1)$ (open). The error is $E(f) = I(f) - Q(f)$ and the cost is counted in evaluations of $f$, plus the one-time cost of the weights.

## The algorithm

```pseudo id=main
NEWTON-COTES(f, a, b, n, open, m)
L1  t ← (i − 1)/(n − 1) for i = 1..n if closed, else i/(n + 1)     ▷ nodes on [0, 1]
L2  solve Σ_i W_i t_i^k = 1/(k + 1), k = 0..n − 1, exactly           ▷ moment equations
L3  H ← (b − a) / m
L4  s ← 0
L5  for j ← 0 to m − 1 do
L6      for i ← 1 to n do
L7          s ← s + W_i · f(a + (j + t_i) · H)
L8  return H · s
```

Lines L1 and L2 depend only on $n$ and the type, so a program computes them once, in rational arithmetic, and stores the table. Lines L3 to L8 map the reference rule to each panel. In a closed rule the last node of panel $j$ is the first node of panel $j + 1$, and the implementation evaluates it once with the two weights added, which turns the inner coefficients $W_n + W_1$ at shared nodes into the familiar $2$ of the composite trapezoidal and Simpson rules.

Weights of the low closed and open rules on $[0, 1]$, and the error on one panel for $f \in C^{d+1}$, with node spacing $h$ and some $\xi$ in the panel:

| rule | $n$ | weights $W_i$ | $d$ | error on one panel |
|---|---|---|---|---|
| trapezoidal | 2 | $\tfrac12, \tfrac12$ | 1 | $-\tfrac{1}{12} h^3 f''(\xi)$ |
| Simpson | 3 | $\tfrac16, \tfrac46, \tfrac16$ | 3 | $-\tfrac{1}{90} h^5 f^{(4)}(\xi)$ |
| three-eighths | 4 | $\tfrac18, \tfrac38, \tfrac38, \tfrac18$ | 3 | $-\tfrac{3}{80} h^5 f^{(4)}(\xi)$ |
| Boole | 5 | $\tfrac{7}{90}, \tfrac{32}{90}, \tfrac{12}{90}, \tfrac{32}{90}, \tfrac{7}{90}$ | 5 | $-\tfrac{8}{945} h^7 f^{(6)}(\xi)$ |
| midpoint (open) | 1 | $1$ | 1 | $\tfrac13 h^3 f''(\xi)$ |
| open, 2 points | 2 | $\tfrac12, \tfrac12$ | 1 | $\tfrac34 h^3 f''(\xi)$ |
| Milne (open) | 3 | $\tfrac23, -\tfrac13, \tfrac23$ | 3 | $\tfrac{14}{45} h^5 f^{(4)}(\xi)$ |

## Example

Boole's rule ($n = 5$, closed, $m = 1$) for $f(x) = e^x$ on $[0, 1]$, with nodes $0, \tfrac14, \tfrac12, \tfrac34, 1$:

| step | node | $f$ | $s$ after the step |
|---|---|---|---|
| L7, $i = 1$ | $0$ | $1.0000000000$ | $0.0777777778$ |
| L7, $i = 2$ | $0.25$ | $1.2840254167$ | $0.5343201482$ |
| L7, $i = 3$ | $0.5$ | $1.6487212707$ | $0.7541496509$ |
| L7, $i = 4$ | $0.75$ | $2.1170000166$ | $1.5068607679$ |
| L7, $i = 5$ | $1$ | $2.7182818285$ | $1.7182826879$ |

Line L8 multiplies by $H = 1$. The exact value is $e - 1 = 1.7182818285$, so $E = -8.595 \times 10^{-7}$, consistent with $-\tfrac{8}{945} h^7 e^{\xi}$ for $h = \tfrac14$ and $\xi \approx 0.51$. On one panel, the errors of the closed rules for $e^x$ on $[0, 1]$ fall quickly with $n$: $-1.41 \times 10^{-1}$ ($n = 2$), $-5.79 \times 10^{-4}$ ($n = 3$), $-2.58 \times 10^{-4}$ ($n = 4$), $-8.59 \times 10^{-7}$ ($n = 5$), $-1.06 \times 10^{-9}$ ($n = 7$), $-9.8 \times 10^{-13}$ ($n = 9$), and rounding level at $n = 11$. Each odd $n$ gains as much as the even $n$ above it, as the degree rule predicts. The function $e^x$ is entire, so high-degree interpolation converges; the Runge function below shows the opposite.

## Correctness

The full proof is in the correctness file; the main points are:

- **Interpolatory.** The moment matrix of line L2 is a transposed [Vandermonde matrix](/vandermonde-matrix/) of distinct nodes, so the weights are unique and equal $\int_0^1 \ell_i$. The rule is exact for every polynomial of degree at most $n - 1$.
- **Symmetry.** The nodes are symmetric about $\tfrac12$, so the weights are, and the rule integrates every function odd about $\tfrac12$ exactly.
- **Degree.** For odd $n$, the node polynomial $\omega$ is odd about the centre, so $\int \omega = 0$ and the degree rises to $n$; for even $n$, $\int \omega \ne 0$ and it stays at $n - 1$. A sign lemma shows that $\omega$ on unit spacing alternates in sign with strictly decreasing lobes toward the centre, which proves $\int \omega \ne 0$ for even $n$ and $\int (x - c)\omega \ne 0$ for odd $n$, so the degree is exactly as stated.
- **Composite.** Each panel is an affine image of $[0, 1]$, so the composite rule has the same degree.
- **Error term (cited).** For $f \in C^{d+1}$ on one panel, $E = C_n h^{d+2} f^{(d+1)}(\xi)$ (Steffensen's theorem, Davis and Rabinowitz Section 2.5), with the constants of the table. The composite error is then $C_n \frac{b - a}{n - 1} h^{d+1} f^{(d+1)}(\xi)$ for closed rules, so the order is $h^{d+1}$: $h^2$, $h^4$, $h^4$, $h^6$ for $n = 2, 3, 4, 5$.

## Complexity

- **Evaluations.** $m(n - 1) + 1$ for a closed rule, since adjacent panels share one node, and $m n$ for an open rule.
- **Weights.** Gauss-Jordan elimination on the $n \times n$ moment system costs $O(n^3)$ rational operations and $O(n^2)$ memory, once per $n$; the test sizes $n \le 11$ take milliseconds. Floating-point solution of the moment system is not advisable for large $n$, since the Vandermonde matrix is badly conditioned.
- **Work for a tolerance.** For a composite rule of order $p = d + 1$ and $f \in C^{p}$, an error $\tau$ needs $\Theta(\tau^{-1/p})$ evaluations.
- **Floating point.** With rounded weights and `math.fsum`, the rounding error is about $u \sum_i |W_i f(x_i)| H$ times a small constant. This is close to $u\,I(|f|)$ when the weights are positive, and up to $\sum |W_i|$ times larger otherwise.

## Properties

- **Weights are rational, symmetric and sum to 1** on $[0, 1]$.
- **Positivity.** All closed weights are positive for $n \le 8$ and $n = 10$; the 9-point rule and every closed rule with $n \ge 11$ have negative weights. Among open rules, the first negative weight appears at $n = 3$ (Milne). The sum $\sum |W_i|$ is 1.45 at $n = 9$, 3.06 at $n = 11$ and 544 at $n = 21$.
- **Divergence for large $n$.** For $f(x) = 1/(1 + 25 x^2)$ on $[-1, 1]$, the single-panel errors at $n = 5, 9, 13, 17, 21, 25$ are $0.075$, $0.25$, $0.61$, $1.8$, $5.9$ and $21$. Pólya (1933) proved that the closed Newton-Cotes rules diverge for some analytic integrands; the cause is the [Runge phenomenon](/runge-phenomenon/) of equispaced interpolation together with $\sum |W_i| \to \infty$. Composite rules with fixed $n$ converge for every Riemann integrable $f$: the 5-point rule on 64 panels gets this integral to better than $10^{-9}$.
- **Nesting.** The closed nodes for $n$ points are contained in those for $2n - 1$ points, which [Romberg integration](/romberg-integration/) uses: the second column of the Romberg table is Simpson's rule and the third is Boole's rule.

## Variants and improvements

- **Composite rules.** Apply a low-order rule on $m$ panels; see [composite quadrature](/composite-quadrature/). This is the standard use.
- **Open rules.** Use them when $f$ cannot be evaluated at the ends, or in predictor formulas for ODEs. The [midpoint rule](/midpoint-rule/) is the most useful one.
- **Clenshaw-Curtis and Fejér rules.** Interpolate at Chebyshev points instead of equispaced points: the weights stay positive and the rules converge for every continuous $f$. See [Clenshaw-Curtis quadrature](/clenshaw-curtis-quadrature/).
- **Gauss rules.** Free the nodes as well as the weights to reach degree $2n - 1$. See [Gaussian quadrature](/gaussian-quadrature/).
- **Rules with end corrections.** The Gregory rules keep the trapezoidal weights inside and correct a few weights near the ends, which gives a higher order on long equispaced grids without the large mixed-sign weights of a single high-degree rule.

## When to use it

Use a low-order Newton-Cotes rule when the data come on an equispaced grid, as tabulated values or samples, or when a simple composite rule is enough. Simpson's rule and Boole's rule on many panels are good defaults for smooth $f$ given on such a grid. Do not raise $n$ beyond about 8 for a single panel; use more panels, or move to [Gaussian quadrature](/gaussian-quadrature/) or [Clenshaw-Curtis quadrature](/clenshaw-curtis-quadrature/) when you can choose the nodes.

## Pitfalls

- **High degree on one panel.** The 11-point and higher rules amplify errors in $f$ through $\sum |W_i|$ and can diverge. More nodes on one panel is not more accuracy.
- **Wrong number of panels.** Composite Simpson needs an even number of subintervals, the composite three-eighths rule a multiple of 3, and Boole's rule a multiple of 4. Stating $m$ as panels, as here, avoids the confusion.
- **Expecting order $n$ from even $n$.** The 4-point rule has the same order $h^4$ as Simpson's rule with one more evaluation per panel. Odd $n$ is the better choice.
- **Floating-point weights from the moment system.** Solving the Vandermonde system in floating point loses digits quickly as $n$ grows. Use exact rational arithmetic, as the implementation does, or a table.
- **Kinks inside a panel.** The order $h^{d+1}$ needs $f \in C^{d+1}$. A kink inside a panel drops composite Simpson to order $h^2$; a kink at a panel end costs nothing.

## Implementations

## History

Newton described interpolation through equally spaced points in a letter of 1676 and in the Methodus differentialis (published 1711), and gave the three-eighths rule. Roger Cotes computed the weights of the closed rules up to 11 points; they were published after his death in Harmonia mensurarum (1722). Simpson's rule is older than both: Simpson stated it in 1743, and Cavalieri and Gregory knew it earlier. Boole's rule appears in Boole's Treatise on the Calculus of Finite Differences (1860). Steffensen proved the general error theorem in the 1920s, and Pólya (1933) showed that the closed rules need not converge as $n \to \infty$.

## References
