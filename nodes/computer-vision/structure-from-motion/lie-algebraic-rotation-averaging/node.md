---
tag: XFRXH0
kind: algorithm
slug: lie-algebraic-rotation-averaging
name: Lie-algebraic rotation averaging
aliases:
- Govindu rotation averaging
area: computer-vision/structure-from-motion
level: advanced
summary: Average rotations by repeated linear least squares on their logarithms in the Lie algebra so(3). Robust versions start from an L1 solution and then run IRLS with a robust cost.
solves: [rotation-averaging]
model: real-ram
complexity:
  vars: {N: "the number of cameras", E: "the number of edges of the view graph", k: "the number of iterations"}
  time: {per_iteration: "O(E + N^3)", total: "O(k (E + N^3))"}
  space: {extra: "O(E + N^2)"}
properties: {deterministic: true, iterative: true, local: true, recursive: false, monotone: false}
history:
  year: 2004
  people: [Venu Madhav Govindu, Avishek Chatterjee]
  note: Govindu averaged motions on a graph of views in 2001 and gave the iterative Lie-algebraic method in 2004. Chatterjee and Govindu (2013, 2018) made it robust with an L1 start and iteratively reweighted least squares.
prereqs: [rotation-averaging, so3-logarithm-map, laplacian-matrix, iteratively-reweighted-least-squares]
see_also: [global-structure-from-motion, view-graph, translation-averaging, gauss-newton-algorithm, m-estimator, se-sync, pose-graph-optimization, special-orthogonal-group]
sources:
  - paper: doi:10.1109/CVPR.2004.1315098
    title: "Venu Madhav Govindu, Lie-algebraic averaging for globally consistent motion estimation, IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2004), vol. 1, 684-691"
    locator: "the whole paper (the averaging of relative motions in the Lie algebra, the linear update and the iteration)"
  - paper: doi:10.1109/CVPR.2001.990963
    title: "Venu Madhav Govindu, Combining two-view constraints for motion estimation, IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2001), vol. 2, 218-225"
    locator: "the averaging of relative rotations over a graph of views"
  - paper: doi:10.1109/ICCV.2013.70
    title: "Avishek Chatterjee and Venu Madhav Govindu, Efficient and robust large-scale rotation averaging, IEEE International Conference on Computer Vision (ICCV 2013), 521-528"
    locator: "the whole paper (the L1 averaging in the Lie algebra and the reweighted refinement)"
  - paper: doi:10.1109/TPAMI.2017.2693984
    title: "Avishek Chatterjee and Venu Madhav Govindu, Robust relative rotation averaging, IEEE Transactions on Pattern Analysis and Machine Intelligence 40(4), 2018, 958-972"
    locator: "the robust cost functions, the iteratively reweighted least squares method and the experiments"
  - paper: doi:10.1007/s11263-012-0601-0
    title: "Richard Hartley, Jochen Trumpf, Yuchao Dai and Hongdong Li, Rotation averaging, International Journal of Computer Vision 103(3), 2013, 267-305"
    locator: "the sections on the Lie-algebraic and the L1 methods for multiple rotation averaging"
---

Lie-algebraic rotation averaging is an iterative algorithm for [rotation averaging](/rotation-averaging/): given measured relative rotations $R_{ij} \approx R_j R_i^{\mathsf T}$ on the edges of a [view graph](/view-graph/), it finds absolute rotations $R_k$ that fit them. Rotations do not form a vector space, so the algorithm works in the tangent space, the Lie algebra $\mathfrak{so}(3)$, which is $\mathbb{R}^3$. At each step it measures the disagreement of each edge as a rotation vector with the [logarithm map](/so3-logarithm-map/), solves one linear least squares problem for a small rotation of every camera, which is a system with the [graph Laplacian](/laplacian-matrix/), and applies the small rotations. With unit weights this is the Gauss-Newton method for the squared geodesic cost, as given by Govindu (2004). Chatterjee and Govindu made it robust: they start from an $L_1$ solution and then run [iteratively reweighted least squares](/iteratively-reweighted-least-squares/) with a robust cost, which removes the effect of wrong edges. It is the rotation step of many [global structure from motion](/global-structure-from-motion/) systems.

## In plain words

Each camera has an unknown direction, and for many pairs you have measured how much one camera is turned compared with the other. Start with a guess for every camera, for example by chaining the measurements along a tree. For each pair, compute how far the guess is from the measurement, as a small turn. Then ask: what small extra turn of every camera would make all these differences as small as possible together? That question has a straight answer from one set of linear equations, because small turns behave almost like ordinary vectors. Apply the turns and repeat. To stop a few bad measurements from pulling everything, give each pair a weight that gets smaller when its difference is large, and recompute the weights each time.

## The problem

**Input.** A connected graph on the cameras $1, \dots, N$ with $E$ edges, a measured rotation $R_{ij} \in SO(3)$ for each edge $(i, j)$, in the convention $X_j = R_{ij} X_i + t_{ij}$, a loss (squared, $L_1$ or Geman-McClure), its scale $\sigma$, a floor $\delta$ for the $L_1$ weights, a start (optional), a tolerance $\varepsilon$ and an iteration limit $k_{\max}$.

**Output.** Rotations $R_1, \dots, R_N$ with $R_1 = I$ at a stationary point of
$$F(R) = \sum_{(i,j)} \rho(\|r_{ij}\|), \qquad r_{ij} = \log\big(R_j^{\mathsf T} R_{ij} R_i\big) \in \mathbb{R}^3,$$
where $\log$ returns the rotation vector of angle in $[0, \pi]$. The residual $r_{ij}$ is zero when the edge agrees with the estimate, and $\|r_{ij}\|$ is the geodesic distance between $R_{ij}$ and $R_j R_i^{\mathsf T}$. The losses are $\rho(x) = x^2$, $\rho(x) = x$ and $\rho(x) = x^2 / (x^2 + \sigma^2)$.

**Update.** Each camera gets a small rotation $\omega_k$ applied on the right, $R_k \leftarrow R_k \exp([\omega_k]_\times)$. Then the residual of the edge $(i, j)$ becomes $\log(\exp(-[\omega_j]_\times) \exp([r_{ij}]_\times) \exp([\omega_i]_\times)) \approx r_{ij} + \omega_i - \omega_j$, to first order in all three vectors. So the linear model asks for $\omega_j - \omega_i \approx r_{ij}$ on every edge.

## The algorithm

```pseudo id=main
LIE-AVERAGE(G, {R_ij}, loss, σ, δ, ε, k_max)
L1  R <- the start, or the rotations chained from R_1 = I along a breadth-first spanning tree
L2  for it <- 1 to k_max
L3      for each edge (i, j): r_ij <- log(R_j^T R_ij R_i)
L4      w_ij <- 1 (squared), 1 / max(||r_ij||, δ) (L1), or σ² / (||r_ij||² + σ²)² (Geman-McClure)
L5      solve L ω = b with ω_1 = 0, where L is the weighted graph Laplacian without row and column 1, and b_k = Σ_(i,k) w_ik r_ik - Σ_(k,j) w_kj r_kj
L6      for each camera k: R_k <- R_k exp([ω_k]_x)
L7      if max_k ||ω_k|| < ε then stop
L8  return R
```

Line L1 gives a start that fits the tree edges exactly. Lines L3 and L4 compute the residuals and the weights of iteratively reweighted least squares: the weight $\rho'(x) / (2x)$ of the loss, up to a constant factor. Line L5 is the normal equation of $\min_\omega \sum w_{ij} \|\omega_j - \omega_i - r_{ij}\|^2$ with $\omega_1 = 0$. Its matrix is the same $(N - 1) \times (N - 1)$ Laplacian for the three coordinates of $\omega$, so one factorization serves three right-hand sides. Line L6 applies the step on the right, which matches the linear model. The robust run of Chatterjee and Govindu is LIE-AVERAGE with the $L_1$ loss from the tree start, followed by LIE-AVERAGE with a robust loss from its result. The reference code runs 30 iterations of each, with Geman-McClure as the robust loss.

## Example

Take three cameras and rotations about the $Z$ axis: $R_{12}$ by $10^\circ$, $R_{23}$ by $20^\circ$ and $R_{13}$ by $33^\circ$. The cycle does not close: $10 + 20 - 33 = -3$ degrees. Write $\theta_k$ for the angle of $R_k$.

- **Start (line L1).** The breadth-first tree from camera 1 uses the edges $(1, 2)$ and $(1, 3)$, so $\theta_2 = 10^\circ$ and $\theta_3 = 33^\circ$. The residual of the edge $(2, 3)$ is $20 - 23 = -3$ degrees, and the other two residuals are 0.
- **Squared loss.** All rotations share one axis, so they commute, the linear model is exact, and line L5 solves $2\omega_2 - \omega_3 = 3$, $-\omega_2 + 2\omega_3 = -3$ (in degrees): $\omega_2 = 1$, $\omega_3 = -1$. After one step, $\theta_2 = 11^\circ$ and $\theta_3 = 32^\circ$, each edge has a residual of $1^\circ$ in size, and the cost drops from $9$ to $3$ square degrees ($0.00091$ rad squared). The second iteration finds $\omega = 0$ and stops.
- **$L_1$ loss.** From the start, the two exact edges get the weight $1/\delta = 10^6$ and the third gets $1 / (3^\circ)$, so the solve keeps the exact edges almost fixed, and the iteration stays within $10^{-4}$ degrees of the start. The start is one of the $L_1$ minimizers, with the cost $3^\circ = 0.05236$ rad, but the whole error sits on one edge.
- **Geman-McClure loss, $\sigma = 0.1$ rad.** All residuals are small compared with $\sigma$, so the loss behaves like the squared loss, and the run ends at $\theta_2 = 11^\circ$, $\theta_3 = 32^\circ$ after 13 iterations.

The reference code gives these numbers. On a larger test with 15 cameras and 62 edges, with $0.01$ rad of noise and about 15% of the edges replaced by random rotations, the squared loss ends with a largest relative rotation error of $1.90$ rad, worse than the tree start, and the robust run ends with $0.022$ rad (a benchmark result on this test).

## Correctness

The update is exact to first order: for the squared loss, line L5 solves the Gauss-Newton system of $F$ in the local coordinates $\omega$ (theorem). The gradient of $\sum \|r_{ij}\|^2$ with respect to $\omega_k$ at $\omega = 0$ is exactly $-2 b_k$, because the derivative of $\|\log Q\|^2$ along a small rotation $u$ is $2 \langle \log Q, u \rangle$ (theorem). The grounded Laplacian of a connected graph with positive weights is positive definite, so line L5 has a unique solution, and $\omega$ is a descent direction whenever $b \ne 0$ (theorem). The solution is $\omega = 0$ if and only if $b = 0$, which is the stationarity condition, so a stop at line L7 with $\varepsilon \to 0$ means a stationary point (theorem). On exact data, the tree start already has all residuals 0, so the algorithm returns the true rotations up to the gauge after one iteration (theorem). The full step has no line search, so the cost need not decrease at every step; in practice it does from a good start (heuristic). The proof file below gives the details.

## Complexity

In the real RAM model, line L3 costs $O(E)$: one logarithm and two $3 \times 3$ products per edge. Line L5 assembles the Laplacian in $O(E)$ and solves it. The reference code uses a dense solve, $O(N^3)$ per iteration. The Laplacian has one nonzero block per edge, so a sparse Cholesky factorization with a fill-reducing order, or the [conjugate gradient method](/conjugate-gradient-method/), makes the solve close to linear in $E$ for the view graphs of SfM. Line L6 costs $O(N)$. So one iteration costs $O(E + N^3)$ dense or about $O(E)$ sparse, and $k$ iterations cost $k$ times that. The squared loss usually stops in a handful of iterations; the reweighted runs need tens. The space is $O(E)$ for the residuals plus the space of the solver, $O(N^2)$ dense.

## Properties

- **Local (theorem).** The method converges to a stationary point near its start, not to the global minimum. A good start, such as a maximum spanning tree on the inlier counts, matters.
- **Not monotone.** There is no line search, so a step can raise the cost far from a minimum. A damping term with a test that rejects steps which raise the cost, as in [Levenberg-Marquardt](/levenberg-marquardt/), makes it monotone.
- **Gauge.** Fixing $\omega_1 = 0$ removes the gauge. Without it the Laplacian is singular, with the constant vector in its null space.
- **Exact on exact data (theorem).** A consistent set of edges is fitted exactly.
- **Robustness.** The $L_1$ start is less affected by wrong edges than the squared loss, and the bounded Geman-McClure weights almost ignore edges with large residuals. Both are heuristics with good benchmark results, not guarantees.

## Variants and improvements

- **Chordal and quaternion costs.** The same scheme works with other distances; the chordal cost leads to the linear relaxation of Martinec and Pajdla (2007).
- **$L_1$ by linear programming.** Chatterjee and Govindu (2013) solve the $L_1$ problem in the Lie algebra with a linear solver for $L_1$ problems, then refine with reweighted least squares. The reference code solves the $L_1$ part by reweighting too, which is simpler but can stall at the start, as in the example.
- **Weiszfeld iterations.** Hartley, Aftab and Trumpf (2011) update one rotation at a time towards the geodesic $L_1$ median of its neighbors.
- **Certifiable methods.** The [semidefinite](/semidefinite-programming/) relaxation of the chordal cost, solved directly or by Shonan averaging, gives a certificate of global optimality when it is tight.
- **Pose averaging.** The same linearization on $SE(3)$ averages full motions, as in [pose graph optimization](/pose-graph-optimization/).

## When to use it

Use it for the rotation step of global SfM, and for any rotation averaging problem on a sparse graph with a decent start. Use the robust form whenever the edges come from two-view geometry, since some of them are always wrong. If a certificate of global optimality is needed, use a semidefinite method such as [SE-Sync](/se-sync/) on the chordal cost. If the graph is a chain with few loops, there is little to average, and the result is close to the chained start.

## Pitfalls

- **Left and right updates.** The step $R_k \exp([\omega_k]_\times)$ must match the residual. With $r_{ij} = \log(R_j^{\mathsf T} R_{ij} R_i)$, the linear model is $r_{ij} + \omega_i - \omega_j$. With a left update or another residual, the signs or the frames of $\omega$ change.
- **Angles near $\pi$.** The logarithm is not smooth at angle $\pi$, and its axis is ambiguous there. Residuals that large mean a wrong edge or a bad start; a robust loss limits their effect.
- **The $L_1$ weight floor.** With weights $1/\|r\|$, an edge with a zero residual gets an infinite weight. The floor $\delta$ prevents a division by zero, but large weights freeze the start, as the example shows.
- **Disconnected graphs.** The grounded Laplacian is singular if the graph is not connected. Check the components of the view graph first; the reference code raises an error.
- **Units of $\sigma$.** The Geman-McClure scale is an angle in radians. Too small a value treats good edges as outliers, and too large a value gives the squared loss.

## Implementations

## History

Govindu (2001) combined the relative motions of many image pairs into consistent global motions, and in 2004 he formulated the averaging in the Lie algebra and gave the iterative scheme on this page, for rotations and for full motions. Martinec and Pajdla (2007) proposed a linear method for the rotations based on the chordal distance. Hartley, Aftab and Trumpf (2011) gave the Weiszfeld method for $L_1$ averaging, and Hartley, Trumpf, Dai and Li (2013) surveyed the field. Chatterjee and Govindu (2013) combined an $L_1$ start with reweighted least squares for large scale robust averaging, and extended the analysis of the robust costs in their 2018 journal paper.

## References
