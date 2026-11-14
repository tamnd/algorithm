---
tag: 0AP7M8
kind: algorithm
slug: floating-random-walk-capacitance
name: Floating random walk capacitance extraction
aliases:
- random walk capacitance extraction
- FRW capacitance extraction
area: eda/timing-and-verification
level: research
summary: Le Coz and Iverson's Monte Carlo method that estimates capacitance by random walks that jump between maximal empty cubes around conductors.
solves: [parasitic-extraction]
model: real-ram
complexity:
  vars: {N: the number of walks, T: the mean number of jumps per walk, M: the number of conductor boxes, G: the size of the sampling table}
  time: {expected: O(N T (M + log G))}
  space: {extra: O(M + G)}
properties: {deterministic: false, recursive: false, exact: false}
history:
  year: 1992
  people: [Yannick L. Le Coz, Ralph B. Iverson]
  note: Le Coz and Iverson published the floating random walk for integrated circuit capacitance in Solid-State Electronics in 1992. It builds on the walk on spheres of Muller (1956). RWCap by Yu, Zhuang, Zhang, Hu and Liu (2013) added fast transition tables for layered dielectrics and parallel walks.
prereqs: [monte-carlo-integration, poisson-equation, martingale]
see_also: [importance-sampling, central-limit-theorem, optional-stopping-theorem, finite-difference-method, finite-element-method, markov-chain, rc-tree, elmore-delay]
sources:
  - paper: doi:10.1016/0038-1101(92)90332-7
    title: Y. L. Le Coz and R. B. Iverson, A stochastic algorithm for high speed capacitance extraction in integrated circuits, Solid-State Electronics 35(7), 1005 to 1012, 1992
    locator: the floating random walk on the largest empty cubes, with the surface Green's function of the cube as the transition density, applied to the capacitance of integrated circuit conductors (general locator)
  - paper: doi:10.1214/aoms/1177728169
    title: Mervin E. Muller, Some continuous Monte Carlo methods for the Dirichlet problem, Annals of Mathematical Statistics 27(3), 569 to 589, 1956
    locator: the walk on spheres, the jump to the boundary of the largest empty sphere, and the stopping layer of width epsilon
  - paper: doi:10.1109/TCAD.2012.2224346
    title: Wenjian Yu, Hao Zhuang, Chao Zhang, Gang Hu and Zhi Liu, RWCap, a floating random walk solver for 3-D capacitance extraction of very-large-scale integration interconnects, IEEE Transactions on Computer-Aided Design 32(3), 353 to 366, 2013
    locator: the precomputed transition and weight tables for cubes in layered dielectrics, the variance reduction, and the parallel walks
  - paper: doi:10.1109/43.97624
    title: K. Nabors and J. White, FastCap, a multipole accelerated 3-D capacitance extraction program, IEEE Transactions on Computer-Aided Design 10(11), 1447 to 1459, 1991
    locator: the boundary element method with which floating random walk results are usually compared
---

Floating random walk capacitance extraction estimates the capacitance between the wires of a chip by random walks through the space between them. Each walk starts on a closed surface around one conductor and jumps, again and again, to a random point on the boundary of the largest empty cube around its position, with the probabilities given by the Green's function of the cube. It stops when it lands on a conductor, and the conductor where it stops, with a weight from the first jump, is one sample of the charge. Yannick Le Coz and Ralph Iverson published it in 1992. It needs no mesh, it gives an error bar with each result, and its cost per coefficient grows only slowly with the size of the layout, so it is used for reference-quality [parasitic extraction](/parasitic-extraction/) on large structures.

## In plain words

The voltage at a point of empty space is the average of the voltages on any box of empty space around it. So you can find the voltage at a point by a game: jump to a random point on the biggest empty box around you, then to a random point on the biggest empty box around that point, and so on, until you land on a wire. The voltage of that wire is your answer, and the average over many games is the true voltage.

The charge on a wire depends on how fast the voltage changes just next to it. The method starts each game on a ring around the wire, gives the first jump a weight that measures that change, and adds the weighted answers. The result is a sum of random numbers, so it carries an error bar. More games give a smaller error.

## The problem

There are $M$ conductors in a uniform dielectric with permittivity $\varepsilon$, inside a grounded box, which is conductor 0. For a conductor $j$ let $\phi_j$ be the potential that solves the Laplace equation (the [Poisson equation](/poisson-equation/) with no charge) in the free space, equals 1 on conductor $j$ and 0 on every other conductor. The *capacitance coefficient* $C_{ij}$ is the charge on conductor $i$ under $\phi_j$. With a closed surface $\Gamma$ around conductor $i$ only, with length (or area) $L$ and outward normal $n$, Gauss's law gives

$$C_{ij} = -\varepsilon \oint_\Gamma \nabla \phi_j \cdot n \, ds.$$

The diagonal coefficient $C_{ii}$ is positive, the coupling coefficients $C_{ij}$ with $i \ne j$ are negative, and each row sums to zero when the box is counted. The task is to estimate one row $C_{i0}, C_{i1}, \ldots, C_{iM}$ to a given relative error. This page works in two dimensions with squares, so that the code and the tests stay small. Le Coz and Iverson work in three dimensions with cubes, and every step below is the same there.

## The algorithm

```pseudo id=main
FRW-ROW(conductors, i, Γ, N)
    C[0..M] ← 0
L1  for each of N walks do
L2      r, n ← a uniform point of Γ and the outward normal there
L3      h ← the distance from r to the nearest conductor          ▷ the largest empty square around r has half width h
L4      q ← a point of that square's boundary drawn with the Green's function density K(r, ·)
L5      w ← (∇_r K(r, q) · n) / K(r, q)                          ▷ the weight of the first jump
        repeat
L6          h, k ← the distance from q to the nearest conductor, and that conductor
L7          if h ≤ δ then stop the walk at conductor k
L8          q ← a point of the boundary of the empty square of half width h around q, drawn with the density K
L9      C[k] ← C[k] − ε L w
    return C / N, with the standard error of each entry from the sample variance
```

The first jump estimates the gradient and the rest of the walk estimates the potential. Lines L6 to L8 are the floating random walk proper: the square "floats" with the walker and is always as large as the free space allows, so the walk takes long jumps far from the conductors and short jumps near them. The density $K$ is the same for every square up to scaling, so the code tabulates it once for the unit square: a side chosen uniformly, then a position on the side from a table of its cumulative distribution. In three dimensions the tables are for one face of the unit cube. The stopping layer $\delta$ is one grid unit in the code, which works on integer coordinates.

## Example

The conductor is the square $[-1, 1]^2$ inside the grounded box $[-3, 3]^2$, a square coaxial line, with $\varepsilon = 1$. The surface $\Gamma$ is the square $[-1.5, 1.5]^2$, with $L = 12$. The reference is a [finite difference](/finite-difference-method/) solution with the five-point stencil. Its discrete energy is that of a piecewise linear [finite element](/finite-element-method/) field, so by the Dirichlet principle it is an upper bound on $C_{11}$, and it decreases as the grid gets finer: 6.305, 6.251 and 6.229 on grids of spacing 1/4, 1/8 and 1/16.

One walk with seed 2 of the code:

| step | point | distance $h$ | nearest |
| --- | --- | --- | --- |
| L2 | $(-0.595, -1.5)$, normal $(0, -1)$ | 0.5 | conductor 1 |
| L4 | $(-0.898, -2.0)$ on the bottom side, $w = 2.947$ | 1.0 | box and conductor 1, a tie |
| L8 | $(0.102, -1.703)$ | 0.703 | conductor 1 |
| L8 | $(0.323, -1.0)$ | 0 | conductor 1, stop |

The walk ends on conductor 1, so it adds $-\varepsilon L w = -35.4$ to $C_{11}$ and 0 to $C_{10}$. A single sample is large and has either sign. Only the mean is meaningful:

| walks $N$ | $C_{11}$ | $C_{10}$ |
| --- | --- | --- |
| 1000 | $5.83 \pm 0.78$ | $-5.73 \pm 0.55$ |
| 10000 | $6.36 \pm 0.25$ | $-6.16 \pm 0.18$ |
| 100000 | $6.33 \pm 0.08$ | $-6.15 \pm 0.06$ |

The error bar is one standard error, and it falls by $\sqrt{10}$ for each factor of 10 in $N$. With 100000 walks both estimates are within two standard errors of the finite difference values. The walks in this example took 5.0 jumps on average, with at most 41 in a sample of 5000 walks.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). A harmonic function at the centre of an empty square equals the integral of its boundary values against the Poisson kernel $K$, and its gradient equals the integral against $\nabla K$. So the potential at the walker is a [martingale](/martingale/) along the walk. The walk reaches the stopping layer with probability 1, because each jump halves the distance to the nearest conductor with a probability that does not depend on the scale, and the [optional stopping theorem](/optional-stopping-theorem/) then says that the indicator "the walk ends on conductor $j$" has mean $\phi_j(q)$. Weighting the first jump by $\nabla K \cdot n / K$ is [importance sampling](/importance-sampling/) of the gradient integral with the density $K$, so each sample has mean $C_{ij}$, up to the stopping layer and the grid. The weight is bounded because $\Gamma$ stays away from the conductors, so the variance is finite and the error falls as $\sigma / \sqrt{N}$.

## Complexity

Each jump finds the nearest conductor and draws a point. A scan of the $M$ conductor boxes costs $O(M)$, and the draw costs $O(\log G)$ with a table of $G$ points, so $N$ walks of $T$ jumps on average cost $O(N T (M + \log G))$ time, with $O(M + G)$ space. What is proved is that $T$ is finite and that the error after $N$ walks is $\sigma / \sqrt{N}$, so $N$ grows as $\sigma^2 / \eta^2$ for an error $\eta$. What is measured is the size of $T$ and $\sigma$: in the example $T$ was about 5 and the relative standard deviation $\sigma / C$ of one sample was about 4. Production tools replace the scan with a spatial index over the conductor boxes, so the cost of a jump grows only slowly with $M$. Unlike a [quadtree](/quadtree/) or [uniform grid](/uniform-grid/) that stores a solid in mechanical CAD, this index only has to answer one query: the distance from a point to the nearest box.

## Properties

- Randomized and unbiased up to the stopping layer. Each estimate comes with a standard error, so the user can stop when the error is small enough.
- No mesh and no linear system. The memory is the geometry plus the tables.
- Local. The cost of one row depends on the region the walks visit, not on the total size of the layout, so the method suits a few critical nets in a large chip.
- Each walk is independent, so the walks run in parallel with no communication.
- The estimated matrix is not exactly symmetric, and the coupling coefficients of far conductors have a large relative error, because few walks reach them.

## Variants and improvements

- **Three dimensions.** The original method uses cubes and the surface Green's function of a cube, tabulated once.
- **Layered dielectrics.** The jump domain may cross the interface of two dielectrics if the transition table is computed for that case. RWCap uses tables for cubes cut by a planar interface.
- **Variance reduction.** The sample variance of the gradient weight is large. Importance sampling of the first jump, stratified sampling of the start point, and antithetic pairs of walks reduce it.
- **Non-Manhattan conductors.** Jump domains then need the distance to slanted or curved shapes. Xu, Zhang and Yu extended the walks to conductors of general shape in 2017.
- **Walk on spheres.** Muller's method uses spheres instead of cubes, with the uniform distribution on the sphere as the transition density, which needs no table. Cubes fit Manhattan wiring better, because a face of the cube can lie flat against a wire.

## When to use it

Use it for a few nets with high accuracy, for checking a fast rule-based or table-based extractor, and for structures too large for a boundary element solver such as FastCap. For the full chip, extractors use precomputed capacitance tables per pattern, which are faster but less accurate. Use a deterministic solver when the result must be repeatable to all digits, or when the whole matrix of a small structure is needed, since the walk costs grow with the number of rows.

## Pitfalls

- Do not start walks on the conductor itself. The weight has a $1/h$ factor, and $h$ near 0 gives an unbounded variance. The Gaussian surface must keep a positive distance from every conductor.
- A sample is large and of either sign. Report the standard error, and do not trust a few hundred walks.
- The fixed seed in a test gives a repeatable result, but the tolerance must come from the standard error, not from one lucky run.
- A coupling coefficient smaller than its standard error is not resolved. Report it as such and do not round it to zero without saying so.
- The stopping layer and the rounding of jumps add a small bias. Keep the layer far below the smallest feature.

## Implementations

## History

Muller introduced the walk on spheres for the Dirichlet problem in 1956. Le Coz and Iverson adapted it to integrated circuit capacitance in 1992, with cubes that fit Manhattan wiring and a weighted first jump for the charge. Yu and his group made it fast for layered dielectrics and parallel machines with RWCap in 2013, and later extended it to conductors of general shape.

## References
