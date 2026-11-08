---
tag: BNE6XG
kind: algorithm
slug: neville-algorithm
name: Neville's algorithm
aliases:
- Neville-Aitken interpolation
- Neville's scheme
- Aitken-Neville algorithm
area: numerical/interpolation-and-approximation
level: core
summary: Evaluates the interpolating polynomial at one point by a triangular recursion that combines interpolants on fewer nodes, in Θ(n^2) operations and without forming coefficients.
solves: [polynomial-interpolation]
model: real-ram
complexity:
  vars: {n: "the degree bound, with n + 1 nodes"}
  time: {evaluate_one_point: Θ(n^2), add_node: Θ(n)}
  space: {extra: Θ(n)}
  flops: {evaluate_one_point: "5n(n+1)/2 + n + 1"}
properties: {deterministic: true, recursive: false, exact_on_polynomials: true, incremental: true, needs_distinct_nodes: true}
history:
  year: 1934
  people: [Eric Harold Neville, Alexander Aitken]
  note: Aitken (1932) gave an iterated scheme of linear interpolations, and Neville (1934) the symmetric variant that combines neighbouring sub-interpolants.
prereqs: [polynomial-interpolation, lagrange-interpolation]
see_also: [newton-interpolation, barycentric-interpolation, richardson-extrapolation, romberg-integration, sequence-extrapolation, divided-differences, polynomial-interpolation-error-theorem, thiele-continued-fraction-interpolation]
sources:
  - paper: "Eric H. Neville, Iterative interpolation, Journal of the Indian Mathematical Society 20 (1934) 87-120"
    locator: the scheme that combines interpolants on consecutive nodes
  - paper: "Alexander C. Aitken, On interpolation and extrapolation by proportional parts, without the use of differences, Proceedings of the Edinburgh Mathematical Society 3(1) (1932) 56-76"
    locator: the iterated linear interpolation that Neville's scheme rearranges
  - book: isbn:9780387954523
    title: Josef Stoer and Roland Bulirsch, Introduction to Numerical Analysis, third edition, Springer, 2002
    locator: Section 2.1.2, Neville's algorithm, and Chapter 3 on extrapolation methods for quadrature
  - book: isbn:9780521880688
    title: William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 3.2, Polynomial interpolation and extrapolation (Neville's algorithm with the error estimate from the last column)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 3, Interpolation theory (the recursive construction of interpolants from interpolants on fewer nodes)
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 5, Barycentric interpolation formula (the O(n) per point alternative)
---

Neville's algorithm computes the value $p_n(t)$ of the interpolating polynomial at a single point $t$. It never forms coefficients. It starts from the data, which are interpolants of degree 0, and repeatedly merges two interpolants on overlapping sets of $k$ nodes into one on $k + 1$ nodes by a weighted average. After $n$ rounds one value is left, and it is $p_n(t)$. A point costs $\Theta(n^2)$ operations, the whole triangle of partial results comes for free, and adding a node costs $\Theta(n)$. These properties make it the standard tool for polynomial extrapolation, as in [Richardson extrapolation](/richardson-extrapolation/), [Romberg integration](/romberg-integration/) and the Bulirsch-Stoer method.

## In plain words

Two points determine a line, and the line through two neighbouring data points gives a first guess at the value you want. Neville's idea is to combine two such guesses into a better one. Each guess is right at its own points, and the combination is weighted so that it stays right at all of them.

Then you combine neighbouring improved guesses again, and so on, building a triangle. Each layer uses one more data point, and the tip of the triangle is the value of the curve through all the points. You never write down the curve itself, only its value at the one place you asked about. The last two guesses before the tip also tell you roughly how accurate the answer is.

## The problem

Notation on the interpolation pages: the nodes $x_0, \ldots, x_n$ are distinct real numbers, in any order, with data $y_i = f(x_i)$; $p_n$ is the polynomial of degree at most $n$ with $p_n(x_i) = y_i$; $\omega(x) = \prod_i (x - x_i)$. For $i \le j$ let $p_{i, j}$ be the interpolant of degree at most $j - i$ of the data at $x_i, \ldots, x_j$, so $p_{i, i} = y_i$ and $p_{0, n} = p_n$. The input is the nodes, the data and a point $t$; the output is $p_n(t)$.

The algorithm rests on one identity, the **Neville recurrence**: for $i < j$,
$$p_{i, j}(t) = \frac{(t - x_i)\, p_{i+1, j}(t) - (t - x_j)\, p_{i, j-1}(t)}{x_j - x_i}.$$

## The algorithm

```pseudo id=main
NEVILLE(x, y, t)                 ▷ distinct nodes x[0..n], data y[0..n]
L1  for i ← 0 to n do P[i] ← y[i]
L2  for k ← 1 to n do
L3      for i ← 0 to n − k do    ▷ ascending, so P[i + 1] still holds level k − 1
L4          P[i] ← ((t − x[i]) · P[i + 1] − (t − x[i + k]) · P[i]) / (x[i + k] − x[i])
L5  return P[0]
```

After round $k$, $P[i] = p_{i, i+k}(t)$ for $0 \le i \le n - k$. Line L4 is the Neville recurrence with $j = i + k$. Because $i$ runs upward, the old value $P[i + 1] = p_{i+1, i+k}(t)$ is read before it is overwritten in the next step, so one array of $n + 1$ numbers suffices. Written out, the values form a triangle (the **Neville tableau**), with the data in column 0 and $p_n(t)$ at the tip.

## Example

The nodes are $0, 1, 2, 4, 5$, the data are $y = 2^x$, that is $1, 2, 4, 16, 32$, and $t = 3$. Entry $(k, i)$ of the tableau is $p_{i, i+k}(3)$:

| $i$ | $k = 0$ | $k = 1$ | $k = 2$ | $k = 3$ | $k = 4$ |
|---|---|---|---|---|---|
| 0 | 1 | 4 | 7 | 33/4 | **79/10** |
| 1 | 2 | 6 | 26/3 | 23/3 | |
| 2 | 4 | 10 | 20/3 | | |
| 3 | 16 | 0 | | | |
| 4 | 32 | | | | |

For example $p_{2,3}(3) = \big((3 - 2) \cdot 16 - (3 - 4) \cdot 4\big)/(4 - 2) = 10$, the value at 3 of the line through $(2, 4)$ and $(4, 16)$, and the tip is $\big((3 - 0) \cdot \tfrac{23}{3} - (3 - 5) \cdot \tfrac{33}{4}\big)/5 = \tfrac{79}{10}$, the same value as the [Newton form](/newton-interpolation/) gives. The true value is $2^3 = 8$. The two entries of column 3 differ by $7/12$, a pessimistic estimate of the actual error $1/10$.

## Correctness

The recurrence holds because its right side $R(t)$ is a polynomial of degree at most $j - i$ (each product has degree at most $1 + (j - i - 1)$) that interpolates the data at $x_i, \ldots, x_j$:

- at $t = x_i$, $R = \dfrac{0 - (x_i - x_j)\, y_i}{x_j - x_i} = y_i$, since $p_{i, j-1}(x_i) = y_i$;
- at $t = x_j$, $R = \dfrac{(x_j - x_i)\, y_j - 0}{x_j - x_i} = y_j$, since $p_{i+1, j}(x_j) = y_j$;
- at $t = x_m$ with $i < m < j$, both sub-interpolants equal $y_m$, so $R = y_m\,\dfrac{(x_m - x_i) - (x_m - x_j)}{x_j - x_i} = y_m$.

By uniqueness of the interpolant on $j - i + 1$ distinct nodes, $R = p_{i, j}$. Induction on $k$ then shows that after round $k$, $P[i] = p_{i, i+k}(t)$, and the loops end after $n(n+1)/2$ updates. The full proof, including the in-place update order, is in the correctness proof below. Exactness for polynomials of degree at most $n$ follows: if $y_i = q(x_i)$ with $\deg q \le n$, then $p_n = q$.

## Complexity

- **One point.** The differences $t - x_i$ cost $n + 1$ subtractions. Each of the $n(n+1)/2$ updates costs two multiplications, two subtractions and one division. The total is $\tfrac{5}{2} n(n+1) + n + 1$ operations, $\Theta(n^2)$.
- **Many points.** Each new $t$ costs $\Theta(n^2)$ again. For $m$ points this is $\Theta(m n^2)$, against $\Theta(n^2 + m n)$ for the [Newton form](/newton-interpolation/) or the [barycentric formula](/barycentric-interpolation/), which do the quadratic work once. So Neville's algorithm is for one point, or a few.
- **Adding a node.** Keeping the last diagonal of the tableau, a new node $x_{n+1}$ adds one row and one diagonal at a cost of $\Theta(n)$.
- **Space.** $n + 1$ numbers for the in-place version; $\Theta(n^2)$ to keep the whole tableau.

## Properties

- **Exact on polynomials** of degree at most $n$, in exact arithmetic.
- **Independent of node order.** The result is $p_n(t)$ for any ordering of the nodes, though the intermediate entries change. Ordering the nodes by distance from $t$ makes the early columns the most useful approximations.
- **Built-in error estimate.** The difference of the two entries of column $n - 1$ is $p_{1,n}(t) - p_{0,n-1}(t)$. It is a common, heuristic estimate of the error of $p_{0,n-1}(t)$, and so a pessimistic one for $p_n(t)$ when the interpolants converge. Nothing guarantees it, and it fails when the interpolants do not converge.
- **No division by small quantities in $t$.** Only node differences appear in denominators, so $t$ equal to a node is no special case, unlike the barycentric formula.
- **Rounding.** Observed in double precision for $e^x$ on $[-1, 1]$, comparing with the exact interpolant of the stored data at 30 random points: at Chebyshev points the error stays below $3 \times 10^{-15}$ for $n$ up to 60, as for the barycentric formula; at equispaced points both formulas lose accuracy together, with errors $4 \times 10^{-8}$ for $n = 40$ and about $0.02$ to $0.05$ for $n = 60$. The loss comes from the conditioning of equispaced interpolation, measured by the [Lebesgue constant](/lebesgue-constant/), and not from the formula.

## Variants and improvements

- **Aitken's scheme.** Aitken (1932) combines each new node with the same fixed sub-interpolant instead of with a neighbour: $p_{0..k-1, j}$ from $p_{0..k-1}$ and $p_{0..k-2, j}$. It computes the same final value with the same cost; Neville's arrangement uses consecutive nodes and is the one in current use.
- **Differences form.** Numerical Recipes keeps the differences $C_{k,i} = p_{i,i+k} - p_{i,i+k-1}$ and $D_{k,i} = p_{i,i+k} - p_{i+1,i+k}$ instead of the values; the final value is a sum of corrections, and the last correction is the error estimate.
- **Extrapolation.** To estimate $A = \lim_{h \to 0} A(h)$ from values $A(h_0), \ldots, A(h_n)$, run Neville's algorithm with nodes $h_i$ (or $h_i^2$ when the error expansion has only even powers) at $t = 0$. This is polynomial extrapolation, one of the methods of [sequence extrapolation](/sequence-extrapolation/), and with $h_i = h_0 2^{-i}$ and the trapezoidal rule it is [Romberg integration](/romberg-integration/). For $A(h) = \sin(h)/h$ with $h = 0.5, 0.25, \ldots, 0.03125$ and nodes $h^2$, the extrapolated value equals 1 to all digits of double precision, while the best single value is off by $1.6 \times 10^{-4}$.
- **Rational extrapolation.** Replacing the linear combination by a continued-fraction recurrence gives the Bulirsch-Stoer rational scheme, related to [Thiele interpolation](/thiele-continued-fraction-interpolation/).
- **Hermite data.** With repeated nodes the denominator vanishes; a variant uses derivative data in the first columns, as divided differences do. In practice the [Newton form](/newton-interpolation/) handles Hermite data more simply.

## When to use it

Use Neville's algorithm to evaluate an interpolant at one point or to extrapolate to a limit, especially when the error estimate from the tableau is wanted, as in Romberg integration and Bulirsch-Stoer integration. For many evaluation points, use the [barycentric formula](/barycentric-interpolation/) or the Newton form. For high degree, choose good nodes such as [Chebyshev nodes](/chebyshev-nodes/) first; no evaluation scheme rescues equispaced nodes.

## Pitfalls

- **Repeated nodes.** Two equal nodes give a division by zero in line L4. Check that the nodes are distinct, or use Hermite divided differences.
- **Wrong loop direction in the in-place version.** If $i$ runs downward in line L3, $P[i + 1]$ is already overwritten with level $k$ and the result is wrong.
- **Trusting the error estimate.** The column difference estimates the error only when the interpolants are converging; at equispaced nodes for Runge's function both are large and meaningless.
- **Using it for many points.** Calling it once per output point costs $\Theta(n^2)$ per point; precompute barycentric weights instead.
- **Extrapolating too far.** At $t$ far outside the nodes, $|\omega(t)|$ is large and the [interpolation error](/polynomial-interpolation-error-theorem/) grows quickly.

## Implementations

## History

Aitken (1932) published an iterated scheme of linear interpolations, designed for hand computation without differences. Neville (1934) gave the symmetric arrangement that combines interpolants on neighbouring nodes, and the two are often named together. The scheme became a standard tool of numerical extrapolation in the 1960s with Romberg integration and the extrapolation methods of Bulirsch and Stoer, which is how it appears in Stoer and Bulirsch's textbook and in Numerical Recipes.

## References
