---
tag: 3SPGGR
kind: algorithm
slug: lloyds-algorithm
name: Lloyd's algorithm
aliases:
- Lloyd's relaxation
- Voronoi relaxation
- Lloyd iteration
area: geometry/voronoi-and-delaunay
level: advanced
summary: Iteratively moves each site to its cell centroid, converging to a centroidal Voronoi tessellation.
model: real-ram
complexity:
  vars: {n: the number of sites, k: the number of steps}
  time: {worst: O(k n log n)}
  space: {extra: O(n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1957
  people: [Stuart P. Lloyd]
  note: Lloyd described the method in a Bell Labs report of 1957 on the quantization of signals; it was published in 1982.
prereqs: [voronoi-diagram, voronoi-cell, centroidal-voronoi-tessellation, centroid]
see_also: [k-means, k-means-problem, fortunes-algorithm, mesh-generation, fixed-point-iteration, gradient-descent, power-diagram, delaunay-triangulation]
sources:
  - paper: doi:10.1109/TIT.1982.1056489
    title: S. P. Lloyd, Least squares quantization in PCM, IEEE Transactions on Information Theory 28(2), 1982
    locator: Method I, the iteration between nearest-neighbour cells and centroids, and the fact that the error does not increase
  - paper: doi:10.1137/S0036144599352836
    title: Q. Du, V. Faber and M. Gunzburger, Centroidal Voronoi tessellations, applications and algorithms, SIAM Review 41(4), 1999
    locator: Lloyd's method for centroidal Voronoi tessellations with a density, its energy descent and its convergence
  - paper: "Q. Du, M. Emelianenko and L. Ju, Convergence of the Lloyd algorithm for computing centroidal Voronoi tessellations, SIAM Journal on Numerical Analysis 44(1), 2006"
    locator: the global convergence results and the linear rate in one dimension
---

Lloyd's algorithm moves a set of $n$ sites in a region toward a [centroidal Voronoi tessellation](/centroidal-voronoi-tessellation/). In each step it computes the [Voronoi cells](/voronoi-cell/) of the sites inside the region and moves every site to the [centroid](/centroid/) of its cell. Each step never increases the *quantization energy*, the integral of the squared distance from a point of the region to its nearest site, and the fixed points of a step are exactly the centroidal tessellations. With an $O(n \log n)$ Voronoi algorithm a step costs $O(n \log n)$ time. The same iteration on a finite set of data points is the [k-means](/k-means/) algorithm.

## In plain words

Put some sites in a room. Split the room so that each part holds the points nearest to one site. Each part has a balance point. Move every site to the balance point of its part, split the room again, and repeat.

Each round makes the average squared walk from a point of the room to its nearest site shorter, or keeps it the same. It stays the same only when every site already sits on its balance point; then the rounds change nothing more.

After many rounds the sites are spread evenly. Their parts have about the same size, and in a large room they look like a honeycomb.

## The problem

The input is a list of $n$ sites $p = (x, y)$, here with integer coordinates, inside an axis-parallel box $B = [x_0, x_1] \times [y_0, y_1]$ with $x_0 < x_1$ and $y_0 < y_1$, and a number $k$ of steps. Repeated sites are merged. The density is uniform on $B$. The output is the list of sites after $k$ steps, as exact rational points.

Notation: $n$ is the number of distinct sites and $z_i$ is site $i$. $V_i$ is the Voronoi cell of $z_i$ clipped to $B$, $m_i$ its area, and $z_i^*$ its centroid. The energy is

$$\mathcal{E}(z) = \sum_{i=1}^{n} \int_{V_i} |x - z_i|^2 \, dx.$$

The cells are built from the bisectors of pairs of sites, so the only predicate is the sign of an affine function, $2 (z_j - z_i) \cdot x - (|z_j|^2 - |z_i|^2)$, which is an $\mathrm{orient}$-type test; $\mathrm{incircle}$ is not used. No general position is assumed: collinear and cocircular sites are allowed.

## The algorithm

```pseudo id=main
LLOYD(Z, B, k)
L1  repeat k times
L2      compute the Voronoi cell V_i of each site z_i, clipped to B
L3      for each site z_i do
L4          z_i' ← the centroid of V_i
L5      Z ← Z'
L6  return Z
```

- **Line L2.** Any Voronoi algorithm works, followed by clipping to the box. The code clips the box by the $n - 1$ half-planes $|x - z_i| \le |x - z_j|$, in exact rational arithmetic, which is simple and costs $O(n^2)$ per cell.
- **Line L4.** For a polygon with counterclockwise vertices $p_0, \ldots, p_{s-1}$, the area is $A = \frac{1}{2} \sum_t p_t \times p_{t+1}$ and the centroid is $\frac{1}{6A} \sum_t (p_t + p_{t+1}) (p_t \times p_{t+1})$, indices mod $s$.
- **Line L5.** All sites move at once, from the old cells. Moving one site at a time and recomputing the cells is a different method.

## Example

Take the box $[0, 4] \times [0, 2]$ and the two sites $(0, 0)$ and $(1, 0)$. Their bisector is the line $x = 1/2$.

| step | sites | energy |
| --- | --- | --- |
| 0 | $(0, 0)$, $(1, 0)$ | $173/6$ |
| 1 | $(1/4, 1)$, $(9/4, 1)$ | $91/12$ |
| 2 | $(5/8, 1)$, $(21/8, 1)$ | $283/48$ |
| 3 | $(13/16, 1)$, $(45/16, 1)$ | $1051/192$ |

- Step 1: the cells are $[0, 1/2] \times [0, 2]$ and $[1/2, 4] \times [0, 2]$, with centroids $(1/4, 1)$ and $(9/4, 1)$.
- From then on the two sites are $2$ apart and their bisector is the vertical line through their midpoint $s/2$, where $s$ is the sum of their $x$-coordinates. The new sum is $s/2 + 2$, so $s - 4$ halves at every step. The sites after step $j \ge 1$ are $(1 - 3/2^{j+1}, 1)$ and $(3 - 3/2^{j+1}, 1)$, and the energy is $16/3 + 9/4^j$.

The sites tend to $(1, 1)$ and $(3, 1)$, the centers of the two squares, which is a centroidal tessellation with energy $16/3$. The rectangle has a second centroidal tessellation, the sites $(2, 1/2)$ and $(2, 3/2)$ with energy $34/3$, as shown on the [centroidal Voronoi tessellation page](/centroidal-voronoi-tessellation/). A start on the vertical line $x = 2$ stays on it and goes to that one.

## Correctness

**Theorem.** Let the sites be distinct points of the box $B$. Then every step is well defined: every cell is a convex polygon of positive area, and the new sites are distinct points of the interior of $B$. The energy satisfies

$$\mathcal{E}(z^*) \le \mathcal{E}(z) - \sum_{i=1}^{n} m_i |z_i - z_i^*|^2,$$

so it never increases and stays the same only when $z^* = z$. The fixed points of a step are exactly the centroidal Voronoi tessellations of $B$.

The proof has two halves, one for each part of a step. For fixed cells, the parallel axis rule $\int_W |x - z|^2 = \int_W |x - c|^2 + m |z - c|^2$ shows that the centroid $c$ is the best point for the cell, and gives the decrease $m_i |z_i - z_i^*|^2$. For fixed sites, the Voronoi cells are the best partition, because every point then pays its smallest squared distance. The full proof is in [the correctness proof](proofs/correctness/).

**What is proved and what is cited.** The decrease of the energy and the fixed points are proved. That the sites converge, and how fast, is not proved here. Du, Emelianenko and Ju proved global convergence results and a linear rate in one dimension for log-concave densities. In general a limit can be a centroidal tessellation that is not a minimum of the energy, such as the second tessellation of the example.

## Complexity

- **One step.** $O(n \log n)$ time with [Fortune's algorithm](/fortunes-algorithm/) and clipping, since the diagram has $O(n)$ edges by the [Voronoi complexity theorem](/voronoi-complexity-theorem/), and $O(n)$ space. So $k$ steps take $O(k n \log n)$ time in the worst case. Proved in [the complexity proof](proofs/complexity/).
- **This code.** $O(n^3)$ time per step, from $n$ cells times $n - 1$ clips of polygons with $O(n)$ vertices, and $O(n)$ space.
- **Number of steps.** No bound is given here. In the example the distance to the limit halves at every step and the energy gap shrinks by $4$; this is observed for that input only.
- **Exact numbers.** With rationals the numerators and denominators grow from step to step; the real RAM does not count this.

## Properties

- **Descent.** The energy never increases; it is a Lyapunov function of the iteration.
- **Fixed point method.** A step is the map $z \mapsto z^*$, and a CVT is a fixed point. In terms of the energy, the gradient is $\partial \mathcal{E} / \partial z_i = 2 m_i (z_i - z_i^*)$, so a step is a [gradient descent](/gradient-descent/) step with step size $1 / (2 m_i)$ for site $i$.
- **Deterministic.** The result depends only on the start.
- **Local.** Every site moves only with the shape of its own cell.

## Variants and improvements

- **Densities.** With a density $\rho$, use the weighted centroid $\int_{V_i} x \rho / \int_{V_i} \rho$. Stippling and blue-noise sampling use an image as the density.
- **Discrete data.** With the density a sum of point masses at data points, the step is the [k-means](/k-means/) step, and the energy is the [k-means](/k-means-problem/) cost. Then there are finitely many partitions and the energy strictly decreases until it stops, so the iteration ends after finitely many steps, but the number of steps can be exponential in the worst case.
- **Faster methods.** Quasi-Newton methods on the energy, such as L-BFGS, often need far fewer steps than Lloyd's iteration near the limit.
- **Constrained cells.** With a capacity for each cell, the cells become those of a [power diagram](/power-diagram/), and the iteration alternates between weights and centroids.
- **On surfaces and in meshes.** The same step on a surface, or with the dual [Delaunay triangulation](/delaunay-triangulation/), smooths meshes in [mesh generation](/mesh-generation/).

## When to use it

Use it to spread points evenly over a region, for sampling, stippling, sensor placement or mesh smoothing, when a few dozen steps are enough and a simple method is wanted. For a precise optimum of the energy, follow it with a faster method. Do not use it to find the best placement: it stops at the first centroidal tessellation it reaches, which may be a saddle point or a local minimum.

## Pitfalls

- **Coincident sites in line L2.** Two equal sites have no bisector. Merge them first, as the code does; distinct sites stay distinct.
- **Moving sites one by one in line L5.** Updating a site and then using the new site for the next cell is a different iteration. Compute all cells first.
- **Unclipped cells in line L2.** Cells on the boundary of the diagram are unbounded. Clip them to the region before taking centroids.
- **Expecting a global minimum.** The iteration can stop at a saddle point, as the strips of the example show; a start on the line $x = 2$ stays there.
- **Slow convergence.** The energy gap can shrink slowly. Stop on a small change of the energy, not on a fixed small step size alone.
- **Growing rationals.** Exact arithmetic is good for tests and small examples; for many steps the numbers become very long, so use floating point.

## Implementations

## History

Stuart Lloyd described the method in a Bell Labs report in 1957, for the design of the quantizer of pulse-code modulation. The report circulated for many years and was published in the IEEE Transactions on Information Theory in 1982. The same iteration was found again in statistics as k-means, by Forgy and others. Du, Faber and Gunzburger made centroidal Voronoi tessellations a common tool in 1999, with Lloyd's method as the basic algorithm, and later work by Du, Emelianenko and Ju studied its convergence.

## References
