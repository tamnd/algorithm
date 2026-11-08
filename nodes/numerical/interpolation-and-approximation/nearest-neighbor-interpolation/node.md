---
tag: JNZ01E
kind: algorithm
slug: nearest-neighbor-interpolation
name: Nearest-neighbour interpolation
aliases:
- Nearest-neighbor interpolation
- Piecewise constant interpolation
area: numerical/interpolation-and-approximation
level: intro
summary: Give each query point the value of the closest data point. In one dimension the result is piecewise constant, a query costs O(log n), and the error for Lipschitz f is at most L h/2.
solves: [interpolation-problem]
model: real-ram
complexity:
  vars: {n: "the number of intervals, with n + 1 sorted nodes", d: the dimension, N: the number of scattered points}
  time: {query_1d: Θ(log n), query_brute_force: Θ(N d)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, exact_on_polynomials: degree 0, continuous: false, local: true}
prereqs: [interpolation-problem, binary-search]
see_also: [piecewise-linear-interpolation, bilinear-interpolation, voronoi-diagram, nearest-neighbor-search, kd-tree, image-resampling, scattered-data-interpolation, shepard-interpolation]
sources:
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter III, Piecewise linear approximation (with the piecewise constant case as the splines of order 1)
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 18, Interpolation by piecewise polynomials
  - paper: "Philippe Thévenaz, Thierry Blu and Michael Unser, Interpolation revisited, IEEE Transactions on Medical Imaging 19(7) (2000) 739-758"
    locator: the nearest-neighbor kernel among the interpolation kernels for images, with its approximation order 1
  - paper: "Erik Meijering, A chronology of interpolation: from ancient astronomy to modern signal and image processing, Proceedings of the IEEE 90(3) (2002) 319-342"
    locator: the section on interpolation in signal and image processing (nearest-neighbor, linear and cubic kernels)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 7, Voronoi diagrams (the cells of nearest-neighbor regions and point location in them)
---

Nearest-neighbor interpolation gives each query point $t$ the value $y_j$ of the data point $x_j$ closest to it. In one dimension the result is a step function that jumps halfway between consecutive nodes; in several dimensions it is constant on each cell of the [Voronoi diagram](/voronoi-diagram/) of the data. It needs no setup, it reproduces only constants, and its error is $O(h)$, one order worse than [piecewise linear interpolation](/piecewise-linear-interpolation/). It is used where speed and the exact preservation of data values matter more than accuracy: image scaling of labels and masks, lookup tables, and categorical data.

## In plain words

You know the temperature at a few weather stations, and someone asks for the temperature at their house. The simplest answer is the reading of the closest station. That is nearest-neighbor interpolation.

On a line, every place between two stations takes the reading of whichever station is nearer, so the answer is flat and then jumps at the halfway point. The method never invents a value that was not measured, which is good when the values are labels such as colors or land types. But it is crude for smooth quantities: the error shrinks only in proportion to the spacing between stations.

## The problem

Notation on the interpolation pages: the nodes are $x_0 < x_1 < \cdots < x_n$, the data are $y_j = f(x_j)$, $h_j = x_{j+1} - x_j$ and $h = \max_j h_j$. The nearest-neighbor interpolant is
$$s(t) = y_{j(t)}, \qquad j(t) = \operatorname*{arg\,min}_{0 \le j \le n} |t - x_j|,$$
with a fixed rule for ties. On this page a tie at a midpoint $m_j = (x_j + x_{j+1})/2$ goes to the left node $x_j$, so $s = y_j$ on $(m_{j-1}, m_j]$. In $\mathbb{R}^d$ the nodes are points $x_1, \ldots, x_N$ with no order, $|\cdot|$ is the Euclidean norm, and ties go to the lowest index. The input of a query is the nodes, the data and a point $t$; the output is $s(t)$.

## The algorithm

```pseudo id=main
NN-INTERPOLATE(x, y, t)          ▷ x[0] < … < x[n], x[0] ≤ t ≤ x[n]
L1  if n = 0 then return y[0]
L2  lo ← 0, hi ← n               ▷ invariant: x[lo] ≤ t ≤ x[hi]
L3  while hi − lo > 1 do
L4      mid ← lo + ⌊(hi − lo) / 2⌋
L5      if x[mid] ≤ t then lo ← mid else hi ← mid
L6  if t − x[lo] ≤ x[lo + 1] − t then return y[lo]
L7  else return y[lo + 1]
```

Lines L2 to L5 are the binary search of piecewise linear interpolation: they find an interval $[x_{lo}, x_{lo+1}]$ that contains $t$. Every node outside this interval is farther from $t$ than one of its two ends, so the nearest node is one of them. Line L6 compares the two distances and breaks a tie toward the left. For $t$ outside $[x_0, x_n]$, the nearest node is $x_0$ or $x_n$; the implementation handles this by clamping.

In $\mathbb{R}^d$ the brute-force version computes $|t - x_i|^2$ for all $i$ and keeps the smallest, in $\Theta(Nd)$ time. A [k-d tree](/kd-tree/) or another structure for [nearest-neighbor search](/nearest-neighbor-search/) reduces the cost per query after a setup.

## Example

The nodes are $0, 1, 3, 4, 6$ with data $0, 2, 3, 1, 4$. The midpoints are $0.5, 2, 3.5, 5$.

| query $t$ | interval found | $t - x_{lo}$ | $x_{lo+1} - t$ | $s(t)$ |
|---|---|---|---|---|
| 0.4 | $[0, 1]$ | 0.4 | 0.6 | 0 |
| 2 | $[1, 3]$ | 1 | 1 | 2 (tie, left node) |
| 2.1 | $[1, 3]$ | 1.1 | 0.9 | 3 |
| 5 | $[4, 6]$ | 1 | 1 | 1 (tie, left node) |
| 6 | $[4, 6]$ | 2 | 0 | 4 |

For $f = \sin$ on $[0, \pi]$ with $n$ equal intervals, the maximum error on a grid of 20001 points is $0.383$, $0.0980$ and $0.0245$ for $n = 4, 16, 64$, against the bound $\tfrac{h}{2}\max|f'| = 0.393, 0.0982, 0.0245$. The error falls by 4 when $n$ grows by 4, so it is first order. For Runge's function $1/(1 + 25x^2)$ on $[-1, 1]$, with $\max |f'| \approx 3.248$, the errors are $0.610$, $0.192$ and $0.0506$ for the same $n$.

## Correctness

The search of lines L2 to L5 ends with $x_{lo} \le t \le x_{lo+1}$, by the invariant proved for [piecewise linear interpolation](/piecewise-linear-interpolation/). For a node $x_k$ with $k < lo$, $t - x_k > t - x_{lo} \ge 0$, and for $k > lo + 1$, $x_k - t > x_{lo+1} - t \ge 0$, so only $x_{lo}$ and $x_{lo+1}$ can be nearest. Line L6 picks the nearer one, and the left one on a tie. The full proof is in the correctness proof below.

**Error bound.** If $f$ is Lipschitz on $[x_0, x_n]$ with constant $L$, then
$$|f(t) - s(t)| = |f(t) - f(x_{j(t)})| \le L\, |t - x_{j(t)}| \le L\, \frac{h}{2}.$$
For $f \in C^1$ take $L = \max|f'|$. The bound is sharp: for $f(t) = t$ the error at the midpoint of the widest interval is exactly $h/2$. For a merely continuous $f$, the error is at most the modulus of continuity $\omega_f(h/2)$, so $s \to f$ uniformly as $h \to 0$.

## Complexity

- **Query in one dimension.** The search takes $\lceil \log_2 n \rceil$ passes, and lines L6 and L7 take two subtractions and one comparison: $\Theta(\log n)$ in the worst case. On a uniform grid $x_j = a + jh$, the index is $\operatorname{round}((t - a)/h)$, in $O(1)$.
- **Query in $d$ dimensions.** Brute force costs $\Theta(Nd)$. A k-d tree costs $O(N \log N)$ to build; its query time is $O(\log N)$ on average for random points in a fixed low dimension, but it degrades toward $\Theta(N)$ as $d$ grows.
- **Space.** $O(1)$ beyond the data for the search.

## Properties

- **Preserves data values.** Every output is one of the $y_j$. Labels, class indices and integer masks stay valid.
- **Not continuous.** $s$ jumps at each midpoint; in images this shows as blocky pixels when enlarging.
- **Perfectly conditioned.** $|s(t)| \le \max_j |y_j|$ and the Lebesgue constant is 1.
- **Exact only on constants.** Linear data are not reproduced, so the approximation order is 1.
- **Order dependent on ties only.** Away from midpoints, the result does not depend on the tie rule.

## Variants and improvements

- **Previous-neighbor (zero-order hold).** Take the value of the node at or before $t$, as a sample-and-hold circuit does. The error bound becomes $L h$.
- **k nearest neighbors.** Average the values of the $k$ nearest data points. This is a regression method, not an interpolant, unless $k = 1$.
- **Inverse distance weighting.** [Shepard interpolation](/shepard-interpolation/) weights all data by an inverse power of the distance; as the power tends to infinity it tends to nearest-neighbor interpolation away from the Voronoi edges.
- **Higher order.** [Piecewise linear](/piecewise-linear-interpolation/) and [bilinear interpolation](/bilinear-interpolation/) give $O(h^2)$ errors on the same data.

## When to use it

Use nearest-neighbor interpolation for categorical data, for masks and labels in [image resampling](/image-resampling/), for lookups where a measured value must be returned unchanged, and as the cheapest fallback in high dimensions. Do not use it for smooth quantities when a linear scheme is possible: it needs about the square of the number of points to reach the same accuracy.

## Pitfalls

- **Searching the whole array.** A linear scan over all nodes at each query costs $\Theta(n)$. With sorted nodes, the binary search of lines L2 to L5 suffices.
- **Rounding a midpoint in floating point.** Writing the test as $t \le (x_{lo} + x_{lo+1})/2$ rounds the midpoint and can send a point just left of the true midpoint to the right node. Line L6 compares the two distances instead; ties then depend only on the rounding of $t - x_{lo}$ and $x_{lo+1} - t$.
- **Undefined tie rule.** Image libraries differ on whether a tie rounds up or down, which shifts the image by half a pixel. Fix the rule and document it.
- **Aliasing when shrinking images.** Picking one sample per output pixel ignores the others; reducing an image needs a low-pass filter first. See [aliasing](/aliasing/).

## Implementations

## History

Rounding a table argument to the nearest entry is the oldest way to read a table. In signal and image processing the nearest-neighbor kernel became the standard zero-order scheme, and the surveys of Thévenaz, Blu and Unser (2000) and Meijering (2002) place it as the method of approximation order 1, below the linear and cubic kernels. In several dimensions its regions are the cells of the Voronoi diagram.

## References
