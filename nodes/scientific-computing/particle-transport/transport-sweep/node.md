---
tag: WZRH6P
kind: algorithm
slug: transport-sweep
name: Transport sweep
area: scientific-computing/particle-transport
level: core
summary: "Solves for each direction cell by cell in upwind order, so a source iteration needs no matrix inversion; parallel versions pipeline the sweeps."
solves: [linear-boltzmann-transport-equation]
model: real-ram
complexity:
  vars: {M: the number of cells, F: the number of faces, N: the number of directions}
  time: {worst: O(N (M + F))}
  space: {extra: O(M + F)}
properties: {deterministic: true, randomized: false, exact: true, iterative: false}
prereqs: [discrete-ordinates-method, topological-sort, upwind-scheme]
see_also: [source-iteration, directed-acyclic-graph, strongly-connected-components, method-of-characteristics-transport, domain-decomposition, gauss-seidel-method]
sources:
  - book: isbn:9780471092452
    title: E. E. Lewis and W. F. Miller, Jr., Computational Methods of Neutron Transport, Wiley, 1984
    locator: the sections on the sweep of the discrete ordinates equations in slab and in x-y geometry with diamond difference
  - paper: doi:10.1016/S0149-1970(01)00023-3
    title: Marvin L. Adams and Edward W. Larsen, Fast iterative methods for discrete-ordinates particle transport calculations, Progress in Nuclear Energy 40(1), 2002, 3-159
    locator: the discussion of the transport sweep as the exact inversion of the streaming and collision operator
  - paper: "H. Edelsbrunner, An acyclicity theorem for cell complexes in d dimensions, Combinatorica 10(3), 1990, 251-260"
    locator: the theorem that regular cell complexes, among them Delaunay triangulations, have no cycle in the in-front relation for any direction
  - paper: "L. J. Guibas and F. F. Yao, On translating a set of rectangles, Proceedings of the 12th ACM Symposium on Theory of Computing, 1980, 154-160"
    locator: the result that disjoint convex objects in the plane can be ordered for every direction
  - paper: "K. R. Koch, R. S. Baker and R. E. Alcouffe, Solution of the first-order form of three-dimensional discrete ordinates equations on a massively parallel machine, Transactions of the American Nuclear Society 65, 1992, 198-199"
    locator: the KBA pipelined parallel sweep
---

A transport sweep solves the discrete [transport equation](/linear-boltzmann-transport-equation/) $\Omega\cdot\nabla\psi + \Sigma_t\psi = q$ for one direction of flight $\Omega$ when the source $q$ is known. Particles that fly along $\Omega$ only depend on what lies behind them, so the cells can be solved one at a time in the order in which the particles reach them. Each cell takes its inflow from cells that are already solved. This is the exact inverse of the streaming and collision operator, in a number of operations proportional to the size of the mesh, and it is the inner step of [source iteration](/source-iteration/) and of the [discrete ordinates method](/discrete-ordinates-method/). On an unstructured mesh the order is a [topological sort](/topological-sort/) of the upwind graph, which exists only when the graph has no cycle.

## In plain words

Think of rain that falls at a slant through a grid of boxes. A box only gets water from the boxes upwind of it. So you start with the boxes at the edge where the rain comes in, and every time all the boxes that feed a box are done, you can do that box.

Each box needs one small calculation: what comes in, what is made inside, and what is lost, gives what goes out. You never need to solve a big system of equations.

If the boxes feed each other in a ring, there is no box to start with, and the method must cut the ring. Many boxes that do not feed each other can be done at the same time, which is how parallel computers do sweeps.

## The problem

Fix a direction $\Omega$ and a source $q_c$ in every cell. The mesh has cells $c$ with volumes $V_c$ and the total cross section $\Sigma_{t,c}$ in $\mathrm{cm}^{-1}$, and faces $f$ with the area $A_f$ and a unit normal $n_f$ that points out of one of its cells. For a face, $g_f = (\Omega\cdot n_f)A_f$ is the flow of particles through it per unit angular flux. The incoming angular flux is given on the boundary faces where $g_f < 0$, with the normal pointing out of the domain.

The step (upwind finite volume) scheme takes the angular flux on each face equal to the value of the cell upstream of it. Its balance in cell $c$ is
$$\Sigma_{t,c}V_c\,\psi_c + \sum_{\text{out faces}} g_f\,\psi_c - \sum_{\text{in faces}} |g_f|\,\psi_{\mathrm{up}} = q_c V_c .$$
The problem is to solve these equations for all cells. The upwind graph has an edge from cell $a$ to cell $b$ when particles flow from $a$ into $b$ through a shared face.

## The algorithm

```pseudo id=main
SWEEP(mesh, Σt, q, Ω, inflow values)
L1  for each interior face f between cells a and b, with g_f = (Ω·n_f) A_f
L2      if g_f > 0 then add the edge a → b and indeg(b) ← indeg(b) + 1;  if g_f < 0 the same for b → a
L3  Q ← the cells with indeg = 0
L4  while Q is not empty do
L5      c ← pop Q;  ψ_c ← (q_c V_c + Σ over the in faces of |g_f| ψ_up) / (Σt_c V_c + Σ over the out faces of g_f)
L6      for each edge c → d do  indeg(d) ← indeg(d) − 1;  if indeg(d) = 0 then push d on Q
L7  if some cell was not solved then report a cycle and the cells it blocks
```

Lines L1 to L3 and L6 are Kahn's algorithm for the [topological sort](/topological-sort/) of the upwind graph. Line L5 is the cell solve: when it runs, every upstream value $\psi_{\mathrm{up}}$ is a boundary value or the value of a cell that is already done. The order depends only on $\Omega$ and the mesh, so a code computes it once per direction and keeps it for all iterations.

On a rectangle grid the order is simply row by row and cell by cell in the direction of flight, and the implementation also has the diamond difference sweep of the [discrete ordinates](/discrete-ordinates-method/) page in two dimensions: $\psi_c = (q + a\psi_L + b\psi_B)/(\Sigma_t + a + b)$ with $a = 2|\mu|/\Delta x$ and $b = 2|\eta|/\Delta y$, and then $\psi_R = 2\psi_c - \psi_L$, $\psi_T = 2\psi_c - \psi_B$.

## Example

**A two by two grid by hand.** Take cells of $1 \times 1$ cm, $\Sigma_t = 1\ \mathrm{cm}^{-1}$, $q = 1$, vacuum inflow and $\Omega = (0.6, 0.8)$. Number the cells 0 (lower left), 1 (lower right), 2 (upper left) and 3 (upper right). The faces have $g = 0.6$ in $x$ and $g = 0.8$ in $y$, so every denominator in line L5 is $1 + 0.6 + 0.8 = 2.4$.

- Line L3: only cell 0 has no upstream cell. $\psi_0 = 1/2.4 = 0.416667$.
- Line L6 frees cells 1 and 2. $\psi_1 = (1 + 0.6 \cdot 0.416667)/2.4 = 0.520833$ and $\psi_2 = (1 + 0.8 \cdot 0.416667)/2.4 = 0.555556$.
- Cell 3 gets $0.6\psi_2 + 0.8\psi_1 = 0.75$, so $\psi_3 = 1.75/2.4 = 0.729167$.

The outflow through the right and top sides is $0.6(\psi_1 + \psi_3) + 0.8(\psi_2 + \psi_3) = 1.777778$. The absorption is $\psi_0 + \psi_1 + \psi_2 + \psi_3 = 2.222222$, and the two add to the total source 4. The cells form 3 wavefronts: $\{0\}$, $\{1, 2\}$ and $\{3\}$.

**First order on triangles.** On the unit square cut into $2n^2$ triangles, a pure absorber with $\Sigma_t = 1$, $q = 1$, vacuum inflow and $\Omega = (\cos 0.4, \sin 0.4)$ has the exact solution $\psi = 1 - e^{-s}$, where $s$ is the distance back to the inflow side along $\Omega$. The error of the step sweep, summed over the cells with the cell areas, is:

| $n$ | triangles | error | ratio | outflow |
|---|---|---|---|---|
| 8 | 128 | $2.036 \times 10^{-2}$ | | 0.642776 |
| 16 | 512 | $1.192 \times 10^{-2}$ | 1.71 | 0.649119 |
| 32 | 2048 | $6.617 \times 10^{-3}$ | 1.80 | 0.652428 |

The ratio tends to 2, the first order of the step scheme; the exact outflow is 0.655832. The balance of absorption, outflow and source holds to $5 \times 10^{-16}$ on every mesh.

**Second order with diamond difference.** For $\mu = 0.6$, $\eta = 0.3$, $\Sigma_t = 2$ on the unit square, the source $q = (\Sigma_t - \mu - \eta)e^{-(x + y)}$ and the matching inflow have the solution $\psi = e^{-(x + y)}$. The largest error of the cell values on an $n \times n$ grid is $1.010 \times 10^{-3}$, $2.860 \times 10^{-4}$, $7.624 \times 10^{-5}$ and $1.969 \times 10^{-5}$ for $n = 8, 16, 32, 64$. The ratios $3.53$, $3.75$ and $3.87$ tend to 4, which is second order (a measurement).

**A negative value.** One cell of $1 \times 1$ cm with $\Sigma_t = 1$, no source, $\mu = \eta = 0.1$ and the inflow 1 on both sides gives the cell value $2/7$ and the outgoing values $-3/7$ on both sides with diamond difference.

## Correctness

The proofs are in the proof file. Kahn's algorithm outputs a cell only after all its upstream cells, and it outputs every cell exactly when the upwind graph has no cycle; otherwise the unsolved cells are those on a cycle or downstream of one, so line L7 detects cycles exactly. In the sweep order the matrix of the cell equations is lower triangular with a positive diagonal, so line L5 computes the one solution. Adding the cell balances cancels every interior face, so absorption plus outflow equals the source plus the inflow. With a source and inflow that are not negative, the step values are not negative. On a grid with both components of $\Omega$ nonzero, cell $(i, j)$ is on wavefront $i + j + 1$, so there are $n_x + n_y - 1$ wavefronts.

## Complexity

In the [real RAM](/real-ram/) model, lines L1 and L2 visit each face once, and lines L4 to L6 visit each cell once and each face at most twice, so one direction costs $O(M + F)$ operations and $N$ directions cost $O(N(M + F))$. If the order of each direction is stored, the later sweeps skip lines L1 to L3, but the storage is $O(NM)$. The extra memory of one sweep is $O(M + F)$ for the graph and the counters. On a grid this is $O(M)$, the same as the cell loop of the [discrete ordinates method](/discrete-ordinates-method/).

The sweep is sequential along each path of the graph. With $P$ processors the time of one direction is at least the number of wavefronts, $n_x + n_y - 1$ on a two-dimensional grid (Theorem 5 of the proof), and at least $M/P$.

## Properties

- **Direct and exact.** For a fixed source, one sweep solves the discrete equations of a direction exactly. No iteration and no matrix are needed.
- **Conservative.** Absorption plus outflow equals the source plus the inflow, for every direction and every mesh (Theorem 3 of the proof).
- **Positive for the step scheme.** Step values are never negative. Diamond difference is second order but can give negative values in thick cells.
- **Direction dependent order.** Each direction has its own order. Directions in the same octant on a grid share it.
- **Parallel only across wavefronts and directions.** Cells on one wavefront and different directions are independent; cells along a path are not.

## Variants and improvements

- **Higher order cell solves.** The same order works with diamond difference, linear discontinuous finite elements and the step characteristic scheme, which solve a small dense system per cell instead of one equation.
- **KBA pipelining.** Koch, Baker and Alcouffe (1992) split a three-dimensional grid into columns, one per processor, and pipeline blocks of cells and many directions through the processor grid, so that the processors downstream start before the first ones finish.
- **Cycles on unstructured meshes.** Curved or non-convex cells, and some meshes of convex cells in three dimensions, can give cycles. A code finds the [strongly connected components](/strongly-connected-components/) of the upwind graph, cuts an edge of each by using the value of the last iteration on that face, and sweeps the rest in order. This lags the inflow on the cut faces; as a rule of thumb, the iteration then converges more slowly, more so when many faces are cut.
- **Graph based scheduling.** Codes for unstructured meshes compute a priority for each cell, such as its depth in the graph, and give each processor a part of the mesh, so that many directions are in flight at the same time.

## When to use it

Use a sweep whenever a discrete ordinates or characteristics method needs the streaming and collision operator inverted for a known source: inside [source iteration](/source-iteration/), as the operator of a Krylov method, or as a preconditioner. It suits meshes where the cells can be ordered for each direction: rectangle grids, two-dimensional meshes of convex cells, and Delaunay or other regular meshes in any dimension (by the theorem of Edelsbrunner 1990). On meshes with cycles, or on very many processors with few cells each, plan for cut edges and for idle time at the start and end of each pipeline.

## Pitfalls

- **Faces with $\Omega\cdot n = 0$ (line L2).** Such a face carries no flow and must not add an edge. Rounding can make $g_f$ tiny with either sign; this still gives a valid order, but the code must not treat a tiny negative value as an inflow from a cell that is not done.
- **Normals with the wrong sign.** If a face normal points into the cell instead of out of it, the face gives the wrong edge, and the sweep can find a cycle or use a value that is not ready.
- **Silent cycles (line L7).** A sweep that walks through a fixed list without checking the counters uses zero or old values on the faces of a cycle, without any error.
- **Thick cells with diamond difference.** The outgoing values can be negative even when all data are positive, and a fixup makes the sweep nonlinear.
- **Storing all orders.** With many directions and a large mesh, the orders and the angular fluxes use most of the memory; directions that share an order should share storage.

## Implementations

## History

The sweep is as old as the discrete ordinates codes: Carlson's $S_n$ codes at Los Alamos in the 1950s solved the cells in the direction of flight on slab and rectangle meshes, and Lewis and Miller (1984) give the sweep in slab and x-y geometry with diamond difference. For parallel computers, Koch, Baker and Alcouffe (1992) introduced the pipelined KBA sweep. The question of when a mesh can be ordered for every direction comes from computational geometry: Guibas and Yao (1980) showed that disjoint convex objects in the plane can be ordered for any direction of translation, and Edelsbrunner (1990) proved that regular cell complexes, which include Delaunay triangulations, have no cycles in any dimension. Unstructured mesh codes compute the order by a topological sort of the upwind graph and break the cycles they find.

## References
