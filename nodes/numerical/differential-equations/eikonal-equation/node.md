---
tag: 4XFGHE
kind: problem
slug: eikonal-equation
name: Eikonal equation
aliases:
- eikonal PDE
- travel-time equation
- static Hamilton-Jacobi equation |grad T| = s
area: numerical/differential-equations
level: advanced
summary: "Find the travel time T(x) with |∇T| = s(x) and T = 0 on a source set, where s = 1/c is the slowness. The answer is the viscosity solution, the minimal path cost from the sources, which has kinks."
prereqs: [pde-classification, method-of-characteristics, upwind-scheme]
see_also: [fast-marching-method, level-set-method, dijkstra, shortest-path, distance-transform, dial-algorithm, godunov-method, a-star-search]
sources:
  - book: isbn:9780821849743
    title: Lawrence C. Evans, Partial Differential Equations, second edition, American Mathematical Society, 2010
    locator: Section 3.2 (characteristics for nonlinear first-order equations), Chapter 10 (Hamilton-Jacobi equations and viscosity solutions; the control formula and uniqueness)
  - book: isbn:9780521645577
    title: J. A. Sethian, Level Set Methods and Fast Marching Methods, second edition, Cambridge University Press, 1999
    locator: Part II (the eikonal equation, upwind schemes for it, the fast marching method and its applications)
  - paper: doi:10.1090/S0002-9947-1983-0690039-8
    title: Michael G. Crandall and Pierre-Louis Lions, Viscosity solutions of Hamilton-Jacobi equations, Transactions of the American Mathematical Society 277(1) (1983) 1-42
    locator: definition of viscosity solutions, existence and uniqueness
  - paper: doi:10.1090/S0025-5718-04-01678-3
    title: Hongkai Zhao, A fast sweeping method for eikonal equations, Mathematics of Computation 74(250) (2005) 603-627
    locator: Gauss-Seidel sweeps in alternating orderings with the Godunov upwind update, convergence in a finite number of sweeps
  - paper: doi:10.1109/9.412624
    title: John N. Tsitsiklis, Efficient algorithms for globally optimal trajectories, IEEE Transactions on Automatic Control 40(9) (1995) 1528-1538
    locator: the Dijkstra-like single-pass algorithm for the discretized minimum-time problem
---

The eikonal equation $|\nabla T(x)| = s(x)$, with $T = 0$ on a source set $\Gamma$, describes the first arrival time $T(x)$ of a front that moves with speed $c(x) = 1/s(x)$ in the normal direction. With $s \equiv 1$ the solution is the distance to $\Gamma$. It is a nonlinear first-order PDE, a static Hamilton-Jacobi equation, and in general it has no smooth solution: the distance to two points has a kink on their bisector. The right solution concept is the viscosity solution, which equals the minimal travel cost along paths from $\Gamma$. Upwind discretizations solved in a causal order, as in the [fast marching method](/fast-marching-method/), compute it in about the time of [Dijkstra's algorithm](/dijkstra/).

## In plain words

Light a fire along a line in a field, and suppose the fire spreads at a known speed at each place: fast on dry grass, slowly on wet ground. The eikonal equation asks when the fire reaches each point. The answer is the time of the fastest route from the starting line to that point. It is the continuous version of finding shortest paths in a road network. Seismologists use it for the arrival times of earthquake waves, robots for the quickest way around obstacles, and image software for distances to the edges of a shape. The arrival time map usually has creases, where two routes of equal length meet. Methods that assume a smooth answer fail there, so solvers follow the fire outward from the source, using only information that has already arrived.

## Definition

**Notation.** Domain $\Omega \subset \mathbb{R}^n$, closed source set $\Gamma \subset \overline\Omega$, slowness $s : \overline\Omega \to [s_{\min}, s_{\max}]$ continuous with $s_{\min} > 0$. Grid spacing $h$, grid values $T_{ij} \approx T(x_{ij})$.

**Problem.** Find $T : \overline\Omega \to [0, \infty)$ with

$$|\nabla T(x)| = s(x) \ \text{in } \Omega \setminus \Gamma, \qquad T = 0 \ \text{on } \Gamma,$$

in the viscosity sense.

**Viscosity solution.** A continuous $T$ is a viscosity solution if for every smooth $\phi$ and every point $x_0$ where $T - \phi$ has a local maximum, $|\nabla\phi(x_0)| \le s(x_0)$, and where $T - \phi$ has a local minimum, $|\nabla\phi(x_0)| \ge s(x_0)$ (Crandall and Lions 1983; Evans, Chapter 10). Under the hypotheses above, for $\Omega = \mathbb{R}^n$ or a convex domain, the unique viscosity solution is the optimal control value

$$T(x) = \inf\Big\{\int_0^1 s(\gamma(\theta))\,|\gamma'(\theta)|\,d\theta \;:\; \gamma \text{ Lipschitz},\ \gamma(0) \in \Gamma,\ \gamma(1) = x\Big\}.$$

With $s \equiv 1$, $T(x) = \operatorname{dist}(x, \Gamma)$.

**Characteristics.** Where $T$ is smooth, it is constant speed propagation along rays: the characteristics of the Hamiltonian $H(x, p) = |p| - s(x)$ are the optimal paths, straight lines when $s$ is constant. Kinks form where rays from different parts of $\Gamma$ meet (the cut locus), and the viscosity solution keeps the first arrival.

## Variants

- **Anisotropic eikonal equation** $\sqrt{\nabla T^{\mathsf T}M(x)\nabla T} = 1$ with a positive definite matrix field $M$, and general static Hamilton-Jacobi equations $H(x, \nabla T) = 0$ with $H$ convex in $\nabla T$; characteristics and gradient no longer point the same way, which breaks the simple causal ordering.
- **Time-dependent form.** The level set equation $\phi_t + c(x)|\nabla\phi| = 0$; the zero level set of $\phi(\cdot, t)$ is the front at time $t$, so $\{T = t\}$ is the front ([level set method](/level-set-method/)).
- **Signed distance** to a closed curve or surface, used to reinitialize level set functions.
- **Geodesic distance on surfaces and meshes**, the eikonal equation on a manifold with $s \equiv 1$.
- **Multiple arrivals.** In seismics, later arrivals also matter; they are not given by the viscosity solution and need ray tracing or phase space methods.

## Examples

**Distance to a point.** $s \equiv 1$, $\Gamma = \{0\}$: $T(x) = |x|$. It is smooth except at the source, where it has a conical point.

**A kink.** On $[-1, 1]$ with $\Gamma = \{-1, 1\}$ and $s \equiv 1$, the viscosity solution is $T = 1 - |x|$. The zigzag functions with slope $\pm1$ that vanish at $\pm1$ also satisfy $|T'| = 1$ at almost every point, so "almost everywhere solution" does not single out one answer. The function $|x| - 1$ also satisfies the boundary values, but it fails the viscosity test at $x = 0$: $\phi \equiv -1$ touches $T - \phi$ from below there with $|\phi'| = 0 < 1$. The viscosity solution allows only concave kinks, where routes meet.

**A first-order upwind scheme near a point source.** On $[-1, 1]^2$ with $s \equiv 1$ and a source at the centre grid point, the Godunov upwind discretization $\big(\max(T_{ij} - a, 0)\big)^2 + \big(\max(T_{ij} - b, 0)\big)^2 = h^2$, with $a$ and $b$ the smaller neighbour values in $x$ and $y$, solved by fast sweeping, gives these maximum errors:

| $h$ | $\max|T_{ij} - |x_{ij}||$ | ratio to previous | error$/(h\log(1/h))$ |
|---|---|---|---|
| 0.1 | $8.21 \cdot 10^{-2}$ | | 0.357 |
| 0.05 | $5.12 \cdot 10^{-2}$ | 1.60 | 0.342 |
| 0.025 | $3.11 \cdot 10^{-2}$ | 1.65 | 0.336 |
| 0.0125 | $1.84 \cdot 10^{-2}$ | 1.69 | 0.335 |

The maximum is at the corners, along the diagonal. On the grid axes the scheme is exact to rounding. The observed rate is near $h\log(1/h)$ rather than $h$, because the point source makes the solution singular; this is an observation on this problem, consistent with the error analysis of first-order schemes for point sources.

**Non-example: graph distance on the grid.** [Dijkstra's algorithm](/dijkstra/) on the 4-neighbour grid graph with edge length $h$ computes Manhattan distance $|x_1| + |x_2|$. At the corner $(1, 1)$ it gives 2 instead of $\sqrt2 \approx 1.414$ for every $h$: refining the grid does not remove the error. The upwind scheme, which uses both neighbours in a single update, does converge.

## Known algorithms

- **[Fast marching method](/fast-marching-method/)** (Sethian 1996; Tsitsiklis 1995): Dijkstra-like single pass with the upwind update and a [priority queue](/priority-queue/), $O(N\log N)$ for $N$ grid points.
- **Fast sweeping** (Zhao 2005): Gauss-Seidel iteration of the same update in $2^n$ alternating orderings; $O(N)$ per round, and for constant $s$ a fixed number of rounds suffices.
- **Bucketed variants** with $O(N)$ total work, in the style of [Dial's algorithm](/dial-algorithm/), using the bounded ratio $s_{\max}/s_{\min}$ (Tsitsiklis 1995).
- **Ordered upwind methods** for anisotropic problems, which widen the update stencil so that causality holds.
- **Level set and time marching**: solve $\phi_t + c|\nabla\phi| = 0$ with an upwind or ENO/[WENO](/weno-scheme/) scheme and record crossing times; simple but slower.
- **Exact distance transforms** for $s \equiv 1$ on images ([distance transform](/distance-transform/)), which compute the Euclidean distance to a set of pixels in linear time without solving a PDE.

## Bounds

- **Convergence (proved).** Monotone, consistent and stable schemes converge to the viscosity solution, by the Barles-Souganidis theorem (1991); for the first-order upwind scheme the error is $O(\sqrt h)$ in general and $O(h)$ where the solution is smooth or semiconcave, with an extra logarithm at a point source as in the table.
- **Work.** Every algorithm must read all $N$ values of $s$, so $\Omega(N)$; fast marching takes $O(N\log N)$ with a binary heap, and bucketed or sweeping methods $O(N)$ for bounded slowness ratio or fixed geometry.
- **Higher order.** Higher-order upwind stencils, and the local factoring $T = |x - x_0|\,\tau$ near point sources, restore order 2 or more on smooth parts of the solution.

## Reductions

- **To shortest paths.** The discrete upwind equations are the Bellman equations of a stochastic shortest path problem on the grid; Dijkstra-type label setting applies because the update is monotone and causal (Tsitsiklis 1995).
- **From the level set equation.** A front moving with speed $c > 0$ that never changes sign reaches $x$ at time $T(x)$, so the evolution problem reduces to one eikonal solve.
- **From geometrical optics.** The high-frequency limit of the wave equation $u_{tt} = c^2\Delta u$ with the ansatz $u = A(x)e^{i\omega(T(x) - t)}$ gives $|\nabla T| = 1/c$ at leading order in $1/\omega$; hence the name, from the Greek for image.

## Applications

Seismic travel-time tomography and migration, geometrical optics, robot path planning around obstacles, image segmentation and geodesic active contours, distance functions and medial axes in computer graphics, the reinitialization step of level set methods, and wildfire and etching front propagation.

## References
