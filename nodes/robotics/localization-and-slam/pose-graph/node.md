---
tag: 4A941D
kind: data-structure
slug: pose-graph
name: Pose graph
aliases:
- pose constraint graph
area: robotics/localization-and-slam
level: core
summary: A graph whose vertices are robot poses and whose edges are measured relative poses with information matrices, from odometry, scan matching and loop closures.
model: real-ram
complexity:
  vars: {p: the number of poses, E: the number of edges, d: the number of edges at one vertex}
  time: {add_vertex: O(1), add_edge: O(1), neighbors: O(d), residual: O(1), initialize: O(p + E), assemble: O(p + E)}
  space: {total: O(p + E)}
history:
  year: 1997
  people: [Feng Lu, Evangelos Milios]
  note: Lu and Milios kept all scan poses as a network of relative pose constraints and solved for them jointly, which is the pose graph used by graph-based SLAM.
prereqs: [special-euclidean-group, pose-compounding-operators]
see_also: [pose-graph-optimization, factor-graph, graphslam, loop-closure-detection, se-sync, switchable-constraints, correlative-scan-matching, iterative-closest-point]
sources:
  - paper: doi:10.1023/A:1008854305733
    title: "Feng Lu and Evangelos Milios, Globally consistent range scan alignment for environment mapping, Autonomous Robots 4(4), 1997, pages 333 to 349"
    locator: "the network of poses linked by relative pose constraints from scan matching and odometry"
  - paper: doi:10.1109/MITS.2010.939925
    title: "Giorgio Grisetti, Rainer Kümmerle, Cyrill Stachniss and Wolfram Burgard, A tutorial on graph-based SLAM, IEEE Intelligent Transportation Systems Magazine 2(4), 2010, pages 31 to 43"
    locator: "the graph of poses and constraints, the error of an edge with its information matrix, and the sparse structure of the linear system"
  - paper: doi:10.1561/2300000043
    title: "Frank Dellaert and Michael Kaess, Factor graphs for robot perception, Foundations and Trends in Robotics 6(1-2), 2017"
    locator: "pose graphs as factor graphs with between factors, and the retraction on the pose manifold"
---

A pose graph stores the result of the front end of a SLAM system in a form that a back end can optimize. Each vertex is a robot pose $X_i$ in $SE(2)$ or $SE(3)$. Each edge $(i, j, Z_{ij}, \Omega_{ij})$ says that a sensor measured the pose of $j$ in the frame of $i$ as $Z_{ij}$, with the information matrix $\Omega_{ij}$, the inverse of the covariance of the measurement. Edges between consecutive poses come from odometry. Edges between poses far apart in time come from scan matching or [loop closure detection](/loop-closure-detection/). The graph holds no landmarks; they were used to make the edges and are then dropped. The structure supports adding vertices and edges, computing the error of each edge, building a first guess from a spanning tree, and assembling the sparse linear system that [pose graph optimization](/pose-graph-optimization/) solves. It is a special case of a [factor graph](/factor-graph/), with one factor per edge and one prior factor that fixes the gauge.

## In plain words

Think of the places where the robot stood as pins on a board, and each measurement as a rubber band between two pins. A band has a natural length and a stiffness. Bands between neighbors in time come from the wheel counts. Bands between distant pins come from the robot seeing the same place again. The pose graph is the list of pins and bands. It can say how much each band is stretched, give a first layout by following one chain of bands from a start pin, and write down the equations that an optimizer needs to relax all the bands at once.

## The abstract type

A pose graph holds:

- a set of vertices, each with an identifier and a pose $X_i$;
- a list of edges, each with two distinct vertex identifiers $i$ and $j$, a measured relative pose $Z_{ij}$, and an information matrix $\Omega_{ij}$ (symmetric positive semidefinite, $3 \times 3$ in the plane).

The operations are ADD-VERTEX, ADD-EDGE, NEIGHBORS, RESIDUAL, COST, INITIALIZE and ASSEMBLE. The error of an edge is

$$e_{ij} = \mathrm{Log}\big(Z_{ij}^{-1} X_i^{-1} X_j\big),$$

the vector in the Lie algebra that takes the measured pose of $j$ to the predicted one. It is zero when the poses agree with the measurement. The cost is $F = \sum e_{ij}^\top \Omega_{ij} e_{ij}$. Derivatives use the right perturbation $X \exp(\delta)$, so $\delta$ is expressed in the frame of the pose. The code is planar: a pose is $(x, y, \theta)$, and $\mathrm{Log}$ returns $(\rho_x, \rho_y, \theta)$ with $\theta \in [-\pi, \pi)$, where $(\rho_x, \rho_y) = V(\theta)^{-1}(x, y)$ and $V(\theta) = \frac{1}{\theta}\begin{bmatrix} \sin\theta & -(1 - \cos\theta) \\ 1 - \cos\theta & \sin\theta \end{bmatrix}$.

## Representation

The vertices are a hash map from the identifier to the pose. The edges are an array, and each vertex has an adjacency list of the indices of its edges. An edge is stored once, with its direction. Reading an edge from $j$ to $i$ uses $Z_{ij}^{-1}$ with the covariance $\mathrm{Ad}_{Z} \Omega^{-1} \mathrm{Ad}_{Z}^\top$ under the right perturbation, but the code never needs to reverse an edge, because the residual is always written from the first end. The linear system is a map from a pair of vertices to a $3 \times 3$ block, so a block exists only where an edge exists.

## Operations

```pseudo id=main
ADD-VERTEX(G, i, X)
L1  G.X[i] ← X;  G.adj[i] ← empty list
ADD-EDGE(G, i, j, Z, Ω)
L2  append (i, j, Z, Ω) to G.E;  let k be its index
L3  append k to G.adj[i] and to G.adj[j]
RESIDUAL(G, k)
L4  return Log(Z⁻¹ X_i⁻¹ X_j) for the edge k = (i, j, Z, Ω)
INITIALIZE(G, r)
L5  seen ← {r};  Q ← a queue that holds r
L6  while Q is not empty do
L7      i ← pop the front of Q
L8      for each edge k in G.adj[i] do
L9          j ← the other end of k
L10         if j is not in seen then
L11             X_j ← X_i Z if k goes from i to j, else X_i Z⁻¹
L12             add j to seen;  push j on Q
ASSEMBLE(G)
L13 H ← an empty map of 3 × 3 blocks;  g ← an empty map of 3-vectors
L14 for each edge k = (i, j, Z, Ω) do
L15     e ← RESIDUAL(G, k);  A ← ∂e/∂δ_i;  B ← ∂e/∂δ_j
L16     H_ii += AᵀΩA;  H_ij += AᵀΩB;  H_ji += BᵀΩA;  H_jj += BᵀΩB
L17     g_i += AᵀΩe;  g_j += BᵀΩe
L18 return H, g
```

NEIGHBORS($G$, $i$) reads the other end of each edge in $G.\mathit{adj}[i]$. COST sums $e^\top \Omega e$ over the edges.

INITIALIZE is a [breadth-first search](/breadth-first-search/) that composes the measurements along a spanning tree from the root $r$. It is the usual first guess for an optimizer: it gives a zero error on every tree edge, and all of the error of each loop sits on the edges outside the tree.

ASSEMBLE builds the Gauss-Newton system $H\,\delta = -g$ of the cost. The code computes $A$ and $B$ by central differences with the step $10^{-6}$ on the right perturbation. In the plane, closed forms exist: with $E = Z^{-1} X_i^{-1} X_j$, the Jacobian of $\mathrm{Log}(E)$ is $J_r^{-1}(e)$, and $\partial e / \partial \delta_j = J_r^{-1}(e)$ and $\partial e / \partial \delta_i = -J_r^{-1}(e)\,\mathrm{Ad}_{X_j^{-1} X_i}$. Many codes replace $J_r^{-1}(e)$ by the identity, which is close when the errors are small. The module does not solve the system; a solver such as [square root SAM](/square-root-sam/), [iSAM2](/isam2/) or a dense Cholesky does that.

## Example

**The square.** Four poses on a square of side 2 m, driven counterclockwise: $(0, 0, 0)$, $(2, 0, \pi/2)$, $(2, 2, \pi)$, $(0, 2, -\pi/2)$. The edges are $0 \to 1$, $1 \to 2$, $2 \to 3$ and the loop closure $3 \to 0$, each with the true relative pose $(2, 0, \pi/2)$ and $\Omega = \mathrm{diag}(100, 100, 400)$, which means standard deviations of 0.1 m and 0.05 rad. With these exact measurements, INITIALIZE from vertex 0 reproduces the four poses, and the cost is 0.

**With noise.** Add noise of standard deviation 0.05 to each component of each measurement (seed 7). The measurements become

| edge | $Z$ |
|---|---|
| $0 \to 1$ | (1.9872, 0.0256, 1.5595) |
| $1 \to 2$ | (1.9842, -0.0465, 1.5601) |
| $2 \to 3$ | (2.0556, 0.0212, 1.6226) |
| $3 \to 0$ | (2.0124, 0.0197, 1.5801) |

The search from vertex 0 first takes the edges $0 \to 1$ and $3 \to 0$, then $1 \to 2$. The edge $3 \to 0$ is read backward, so $X_3 = X_0 Z_{30}^{-1} = (-0.0011, 2.0125, -1.5801)$. The tree edges have zero error, and the edge $2 \to 3$ carries the whole loop error, $e = (0.0206, -0.0019, -0.0391)$, with $F = 0.6554$. ASSEMBLE returns 12 blocks: the 4 diagonal blocks and 2 for each of the 4 edges; the blocks $(0, 2)$ and $(1, 3)$ are absent. Eight Gauss-Newton steps on this system with $X_0$ fixed lower $F$ to $0.2600$ and spread the error over all four edges, whose costs become 0.031, 0.051, 0.111 and 0.067.

## Correctness

The [correctness proof](proofs/correctness.md) shows that INITIALIZE reaches exactly the connected component of the root, keeps the root pose, gives a zero error on every edge of the search tree, and leaves the other components alone. With consistent measurements, it recovers the true poses up to the root pose. It also shows that ASSEMBLE returns the sums $\sum J^\top \Omega J$ and $\sum J^\top \Omega e$ with a block only where an edge exists, and that $2g$ is the gradient of $F$ under the right perturbation. The tests check these facts, and check that Gauss-Newton with the assembled system drives the gradient below $10^{-7}$.

## Complexity

Let $p$ be the number of poses, $E$ the number of edges and $d$ the number of edges at a vertex.

- ADD-VERTEX and ADD-EDGE: $O(1)$ expected, with hash maps for the vertices.
- NEIGHBORS: $O(d)$.
- RESIDUAL: $O(1)$ in the plane and in 3D.
- INITIALIZE: $O(p + E)$, as for breadth-first search.
- ASSEMBLE: $O(p + E)$, and the system has at most $p + 2E$ nonzero blocks.
- Memory: $O(p + E)$.

A typical SLAM pose graph has $E$ a small multiple of $p$: one odometry edge per pose, plus loop closures. Solving the system is not part of the structure, and its cost depends on the fill-in of the factorization; see [elimination ordering](/elimination-ordering/).

## Variants

- **3D pose graphs.** The poses are in $SE(3)$, the errors have 6 components, and the blocks are $6 \times 6$.
- **Pose and landmark graphs.** Add landmark vertices and pose to landmark edges; the result is the graph of [GraphSLAM](/graphslam/) and [square root SAM](/square-root-sam/).
- **Robust edges.** Give loop closure edges a robust kernel, or a switch variable as in [switchable constraints](/switchable-constraints/), so that a wrong loop closure does not bend the map.
- **Other error forms.** Some codes use the plain difference of the coordinates with a wrapped angle, $Z_{ij} \ominus (X_i^{-1} X_j)$, instead of $\mathrm{Log}$. The two agree to first order for small errors.
- **Hierarchical graphs.** Group the poses into submaps and keep a coarse graph of submaps for speed.

## When to use it

Use a pose graph when a front end, such as scan matching or visual odometry, already turns the raw data into relative poses. It is the standard back end for 2D and 3D laser SLAM and for visual SLAM with keyframes, as in [ORB-SLAM](/orb-slam/). When landmarks must stay in the estimate, for example to reuse them for localization, use a factor graph with landmarks instead.

## Pitfalls

- **Wrong direction of an edge.** $Z_{ij}$ is the pose of $j$ in the frame of $i$. Storing $Z_{ji}$ in its place gives a wrong error that no optimizer can repair.
- **Unwrapped angles.** The angle part of the error must be wrapped to $[-\pi, \pi)$, and so must the difference of two angle errors in a finite difference.
- **The gauge.** The cost does not change if all poses move by the same rigid motion. Fix one pose, or add a prior, before solving.
- **Overconfident edges.** An information matrix that is too large on a wrong loop closure lets that edge win against all the odometry. Check loop closures before adding them.
- **Initialization by a long tree path.** On large loops, the spanning tree guess can be far from the optimum, because it stacks all the drift on the closing edges.

## Implementations

## History

Lu and Milios (1997) aligned laser scans by keeping all scan poses and the relative poses between them, and solving for all poses at once. This is the first pose graph. Gutmann and Konolige (1999) built such graphs incrementally with loop closures. Olson, Leonard and Teller (2006) and Grisetti and colleagues made the optimization fast on large graphs, and Grisetti, Kümmerle, Stachniss and Burgard (2010) wrote a tutorial on graph-based SLAM. Libraries such as g2o and GTSAM store the pose graph as a factor graph.

## References
