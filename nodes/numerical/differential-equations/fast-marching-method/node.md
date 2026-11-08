---
tag: XZFJD7
kind: algorithm
slug: fast-marching-method
name: Fast marching method
aliases:
- FMM
- Sethian's fast marching method
area: numerical/differential-equations
level: advanced
summary: "Solves the eikonal equation |∇T| = s on a grid like Dijkstra's algorithm: accept points in increasing T with a heap, each updated by the first-order upwind formula. O(N log N) for N points."
solves: [eikonal-equation]
model: real-ram
complexity:
  vars: {N: "the number of grid points"}
  time: {worst: "Θ(N log N)"}
  space: {extra: "Θ(N)"}
  evaluations: {worst: "4N"}
properties: {deterministic: true, single_pass: true, order: "1", monotone: true, label_setting: true}
history:
  year: 1996
  people: [James A. Sethian, John N. Tsitsiklis]
  note: Sethian (1996) introduced fast marching for front propagation using the upwind discretization of Rouy and Tourin (1992); Tsitsiklis (1995) had given an equivalent Dijkstra-like algorithm for continuous shortest paths in optimal control.
prereqs: [eikonal-equation, dijkstra, priority-queue]
see_also: [level-set-method, dial-algorithm, binary-heap, distance-transform, shortest-path, upwind-scheme, godunov-method, a-star-search]
sources:
  - paper: doi:10.1073/pnas.93.4.1591
    title: J. A. Sethian, A fast marching level set method for monotonically advancing fronts, Proceedings of the National Academy of Sciences USA 93(4) (1996) 1591-1595
    locator: the algorithm (Known, Trial and Far points, heap of Trial values) and the O(N log N) count
  - paper: doi:10.1109/9.412624
    title: John N. Tsitsiklis, Efficient algorithms for globally optimal trajectories, IEEE Transactions on Automatic Control 40(9) (1995) 1528-1538
    locator: the Dijkstra-like label-setting method for the discretized continuous shortest path problem and its causality property
  - paper: doi:10.1137/0729053
    title: Elisabeth Rouy and Agnès Tourin, A viscosity solutions approach to shape-from-shading, SIAM Journal on Numerical Analysis 29(3) (1992) 867-884
    locator: the monotone upwind discretization of the eikonal equation and its convergence to the viscosity solution
  - book: isbn:9780521645577
    title: J. A. Sethian, Level Set Methods and Fast Marching Methods, second edition, Cambridge University Press, 1999
    locator: Chapter 8 (fast marching methods, the update formula, heap implementation, higher-order versions)
  - book: isbn:9780387954820
    title: Stanley Osher and Ronald Fedkiw, Level Set Methods and Dynamic Implicit Surfaces, Springer, 2003
    locator: Chapter 7 (constructing signed distance functions; the fast marching method)
  - paper: doi:10.1090/S0025-5718-04-01678-3
    title: Hongkai Zhao, A fast sweeping method for eikonal equations, Mathematics of Computation 74(250) (2005) 603-627
    locator: the same discrete equations solved by Gauss-Seidel sweeps, used as the test oracle; error O(h log(1/h)) for a point source
---

The fast marching method solves the [eikonal equation](/eikonal-equation/) $|\nabla T(x)| = s(x)$, $T = 0$ on a source set, on a uniform grid. It discretizes the equation with the first-order upwind (Godunov) formula and computes the discrete solution in a single pass, accepting grid points in increasing order of $T$ exactly as [Dijkstra's algorithm](/dijkstra/) accepts vertices in increasing order of distance. With a binary heap the cost is $O(N \log N)$ for $N$ grid points. $T(x)$ is the first arrival time of a front that starts at the sources and moves with speed $1/s$, so the same computation gives distance functions, travel times and shortest path lengths in continuous media.

## In plain words

Picture a fire lit at some points in a field, where the grass burns at different speeds in different places. The method records, for every point of a grid laid over the field, the moment the fire reaches it. It keeps a list of points next to the burned region with a tentative arrival time each. The point with the earliest tentative time cannot be reached sooner by any other route, so it is declared burned for good. Its unburned neighbours then get their tentative times improved, using a small formula that looks at the burned neighbours on either side, and the process repeats until the whole field is done. It is the same idea as finding shortest routes on a road map, but the formula lets the front cut diagonally through grid cells instead of moving only along grid lines.

## The problem

Given a rectangular grid $x_{ij} = (jh, ih)$ with spacing $h > 0$, a slowness $s_{ij} > 0$ at each point ($s_{ij} = \infty$ marks an obstacle) and a nonempty set of source points, find values $T_{ij}$ with $T = 0$ at sources and, at every other reachable point,

$$\big(\max(T_{ij} - a_{ij}, 0)\big)^2 + \big(\max(T_{ij} - b_{ij}, 0)\big)^2 = (s_{ij}h)^2,$$

where $a_{ij} = \min(T_{i,j-1}, T_{i,j+1})$ and $b_{ij} = \min(T_{i-1,j}, T_{i+1,j})$ are the smaller neighbour values in the two grid directions (neighbours outside the grid or on obstacles count as $\infty$). Points that no path of non-obstacle points connects to a source get $T = \infty$. This is the Godunov upwind discretization of $|\nabla T| = s$ (Rouy and Tourin 1992). Its solution is unique (see Correctness) and converges to the viscosity solution of the eikonal equation as $h \to 0$.

The local solve has a closed form. For $c = s_{ij}h$ and $a \le b$,

$$U(c, a, b) = \begin{cases} a + c & \text{if } b - a \ge c, \\ \tfrac12\big(a + b + \sqrt{2c^2 - (b - a)^2}\big) & \text{otherwise,} \end{cases}$$

the largest root of the quadratic; it uses $b$ only when $b < U$. That is the upwind property: a point's value depends only on smaller neighbour values.

## The algorithm

Every grid point is Far, Trial or Known. Known values are final. A min-heap holds Trial points keyed by their tentative value; instead of a decrease-key operation, an improved value is pushed again and stale heap entries are skipped when popped.

```pseudo id=main
FAST-MARCHING(s, h, sources)
L1  for each grid point x do T[x] ← ∞, state[x] ← FAR
L2  for each source x do T[x] ← 0, state[x] ← TRIAL, PUSH(heap, (0, x))
L3  while heap is not empty do
L4      (τ, x) ← POP-MIN(heap)
L5      if state[x] = KNOWN or τ > T[x] then continue      ▷ stale entry
L6      state[x] ← KNOWN
L7      for each grid neighbour y of x with state[y] ≠ KNOWN and s[y] < ∞ do
L8          t ← U(s[y] h, a_y, b_y)     ▷ a_y, b_y: smallest KNOWN neighbour in each direction
L9          if t < T[y] then T[y] ← t, state[y] ← TRIAL, PUSH(heap, (t, y))
L10 return T
```

Line L8 uses only Known neighbours. Known values are final and never exceed the value being computed, so the update at line L8 is the same as the full discrete equation once the point is accepted.

## Example

A $3 \times 3$ grid with $h = 1$, $s = 1$ everywhere and one source at the corner $(0, 0)$. Points are accepted in this order (ties broken by grid index):

| step | accepted | T | update applied to its neighbours |
|---|---|---|---|
| 1 | (0,0) | 0 | (0,1), (1,0): one-sided, $0 + 1 = 1$ |
| 2 | (0,1) | 1 | (0,2): $1 + 1 = 2$; (1,1): one-sided $1 + 1 = 2$ |
| 3 | (1,0) | 1 | (1,1): $a = b = 1$, $U = 1 + \sqrt2/2 = 1.7071$; (2,0): 2 |
| 4 | (1,1) | 1.7071 | (1,2), (2,1): $\tfrac12(1.7071 + 2 + \sqrt{2 - 0.0858}) = 2.5453$ |
| 5, 6 | (0,2), (2,0) | 2 | (1,2), (2,1) unchanged |
| 7, 8 | (1,2), (2,1) | 2.5453 | (2,2): $2.5453 + \sqrt2/2 = 3.2524$ |
| 9 | (2,2) | 3.2524 | none |

The exact distances are $\sqrt2 = 1.4142$, $\sqrt5 = 2.2361$ and $2\sqrt2 = 2.8284$; the first-order scheme overestimates most along the diagonal, where the front direction is furthest from the grid axes. On the square $[-1, 1]^2$ with a point source at the centre and $s = 1$, the maximum error against $|x|$ is

| points per side | $h$ | max error | ratio |
|---|---|---|---|
| 21 | 0.1 | 8.21e-2 | |
| 41 | 0.05 | 5.12e-2 | 1.60 |
| 81 | 0.025 | 3.11e-2 | 1.65 |
| 161 | 0.0125 | 1.84e-2 | 1.69 |

The ratios stay below 2 and creep upwards, consistent with the error $O(h \log(1/h))$ observed for a point source (Zhao 2005); the singularity of $|x|$ at the source spoils plain first order. A plane wave from a whole grid column is reproduced exactly.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Three facts carry it. First, $U$ is monotone (smaller neighbour values give a smaller result) and causal ($U > \min(a, b)$, and $U$ ignores any neighbour value $\ge U$). Second, as in Dijkstra's algorithm, these make the accepted values nondecreasing, so a point's value is final when it is popped: every neighbour accepted later has a value at least as large and would not change $U$. Third, the discrete system has only one solution, by a comparison argument at the point where the difference of two solutions is largest. So the output is the unique solution of the discrete equations, and in particular equal to what the fast sweeping method computes. Convergence of that discrete solution to the viscosity solution of the eikonal equation follows from the Barles and Souganidis theorem for monotone, consistent, stable schemes (Rouy and Tourin 1992); it is an asymptotic result without a rate in general.

## Complexity

Each grid point is accepted at most once, and each acceptance updates at most 4 neighbours, so there are at most $4N$ evaluations of $U$ and at most $N + 4N$ heap pushes, each costing $O(\log N)$. Total time $\Theta(N \log N)$ in the worst case, space $\Theta(N)$ for $T$, the states and the heap. In $d$ dimensions the update solves a quadratic with up to $d$ terms and the bound becomes $O(dN \log N)$. The $\log N$ comes only from the heap: a bucket queue with bucket width at most $\min(s)h/\sqrt{2}$ gives $O(N)$ time when the ratio $\max s / \min s$ is bounded, by the same causality bound (accepting a point raises any neighbour at least $\min(s)h/\sqrt2$ above the smaller neighbour used), as in [Dial's algorithm](/dial-algorithm/) (Tsitsiklis 1995). The fast sweeping method needs $O(N)$ work per sweep and a number of sweeps that grows with the number of times characteristics turn.

## Properties

- **Label setting.** Every value is computed once and frozen, like Dijkstra and unlike fast sweeping or Bellman-Ford style label correcting.
- **Monotone acceptance.** Known values come out in nondecreasing order, which also yields the zero level sets of $T(x) - t$ for all $t$ in order: the front positions in time.
- **Deterministic and exact on its discrete problem.** The output does not depend on tie-breaking in the heap.
- **First order.** Smooth solutions converge at rate $O(h)$; point sources lose a logarithm.
- **Isotropic speed only.** The update assumes the front speed does not depend on its direction.

## Variants and improvements

- **Second-order fast marching.** Replace the one-sided difference by the second-order one $\frac{3T_{ij} - 4T_{i,j-1} + T_{i,j-2}}{2h}$ when both upwind points are Known (Sethian 1999). The causality argument no longer holds exactly but works well in practice.
- **Initialization near interfaces.** For level set reinitialization the Known set starts as the grid points next to the zero contour with exact distances computed locally (Osher and Fedkiw 2003, Chapter 7).
- **Unstructured meshes.** Kimmel and Sethian (1998) extended the update to acute triangulations; obtuse triangles need a virtual splitting to keep causality.
- **Ordered upwind methods.** Sethian and Vladimirsky (2003) handle anisotropic speeds, where the simple update loses causality.
- **Fast sweeping.** Zhao (2005) solves the same discrete equations by Gauss-Seidel sweeps in $2^d$ alternating orders, $O(N)$ per sweep and no heap.
- **Untidy and bucketed queues.** Approximate or bucket queues reach $O(N)$ time, as in Dial's algorithm, sometimes accepting small ordering errors.

## When to use it

Use it for distance functions, arrival times and geodesic distances on grids: reinitializing [level set](/level-set-method/) functions, seismic travel times, path planning around obstacles, and image segmentation with geodesic active contours. It is the method of choice when characteristics curve a lot, since it needs one pass regardless of geometry. Prefer fast sweeping when many queries reuse a simple medium, and use graph algorithms such as [A*](/a-star-search/) when only one target matters. For time-dependent or non-monotone front motion use the level set method, since fast marching requires a front that moves in one direction only.

## Pitfalls

- **Using non-Known neighbours in the update.** Tentative Trial values can be too large and later decrease; mixing them in breaks the proof and can give wrong values.
- **Taking the wrong root or ignoring the one-sided case.** When $b - a \ge c$, the two-sided formula gives a value at most $b$ (or a negative discriminant), contradicting upwinding; use $a + c$.
- **Negative discriminant from rounding.** $2c^2 - (b - a)^2$ can come out slightly negative when $b - a \approx c$; the branch $b - a \ge c$ must be tested first.
- **Expecting first order near a point source.** The error is $O(h \log(1/h))$ there; initialize the exact distance in a small ball around the source for full first order.
- **Diagonal neighbours.** The standard update uses only the $2d$ axis neighbours; including diagonals without changing the formula is inconsistent.
- **Stale heap entries.** With lazy deletion, the check at line L5 is required; without it points are accepted twice.

## Implementations

## History

Rouy and Tourin (1992) wrote down the monotone upwind discretization of the eikonal equation and proved convergence to the viscosity solution by iteration. Tsitsiklis (1995) observed that a discretized continuous optimal control problem with this structure can be solved in one Dijkstra-like pass and also gave a Dial-like bucketed version. Sethian (1996) introduced the fast marching method for monotonically advancing fronts in the level set setting, with the heap of Trial points, and developed its extensions in his book (Sethian 1999). Zhao (2005) analyzed the fast sweeping alternative.

## References
