---
tag: 2DWA9Q
kind: problem
slug: pose-graph-optimization
name: Pose graph optimization
aliases:
- pose graph SLAM
area: robotics/localization-and-slam
level: core
summary: Find the poses that minimize the sum of squared Mahalanobis errors of all relative pose constraints in a pose graph.
prereqs: [pose-graph, nonlinear-least-squares]
see_also: [graphslam, se-sync, isam2, square-root-sam, gauss-newton-algorithm, levenberg-marquardt, switchable-constraints, rotation-averaging]
sources:
  - paper: doi:10.1023/A:1008854305733
    title: "Feng Lu and Evangelos Milios, Globally consistent range scan alignment for environment mapping, Autonomous Robots 4(4), 1997, pages 333 to 349"
    locator: "the joint estimation of all scan poses from a network of relative pose constraints"
  - paper: doi:10.1109/MITS.2010.939925
    title: "Giorgio Grisetti, Rainer Kümmerle, Cyrill Stachniss and Wolfram Burgard, A tutorial on graph-based SLAM, IEEE Intelligent Transportation Systems Magazine 2(4), 2010, pages 31 to 43"
    locator: "the error of a constraint, the least squares cost, and its minimization by Gauss-Newton on the manifold of poses"
  - paper: doi:10.1177/0278364918784361
    title: "David M. Rosen, Luca Carlone, Afonso S. Bandeira and John J. Leonard, SE-Sync: a certifiably correct algorithm for synchronization over the special Euclidean group, International Journal of Robotics Research 38(2-3), 2019, pages 95 to 125"
    locator: "the nonconvexity of pose graph optimization, its semidefinite relaxation, and the exact recovery guarantee for small noise"
  - paper: doi:10.1109/TRO.2016.2624754
    title: "Cesar Cadena, Luca Carlone, Henry Carrillo, Yasir Latif, Davide Scaramuzza, Jose Neira, Ian Reid and John J. Leonard, Past, present, and future of simultaneous localization and mapping: toward the robust-perception age, IEEE Transactions on Robotics 32(6), 2016, pages 1309 to 1332"
    locator: "the maximum a posteriori formulation of the SLAM back end and the open problems of convergence and robustness"
---

Pose graph optimization is the back end problem of graph-based SLAM. The input is a [pose graph](/pose-graph/): poses as vertices and measured relative poses with information matrices as edges. The output is the set of poses that best agrees with all edges, in the sense of the least sum of squared Mahalanobis errors. With Gaussian noise this is the maximum likelihood estimate of the poses. The problem is a [nonlinear least squares](/nonlinear-least-squares/) problem on a product of the groups $SE(2)$ or $SE(3)$. It is nonconvex because of the rotations, so local methods such as [Gauss-Newton](/gauss-newton-algorithm/) can stop at a local minimum that is not global. [SE-Sync](/se-sync/) certifies a global optimum when its semidefinite relaxation is tight, which Rosen et al. prove for noise below a level that depends on the graph. The pose graph is the data, this page is the question, and [GraphSLAM](/graphslam/) is a method that solves a version with landmarks.

## In plain words

A robot recorded where it stood many times, and for many pairs of those places it measured how far apart they are and how they are turned. The measurements do not fit together exactly, because each one has some error. The problem asks for one set of places that fits all the measurements as well as possible. A measurement that the robot trusts more counts more. When the robot drives a loop, the small errors of each step add up, and the measurement at the end of the loop shows the total. A good answer spreads that total over the whole loop. The turning part makes the problem hard, because a search can get stuck in an answer that is good near by but not the best overall.

## Definition

**Input.** A connected graph with vertices $1, \dots, n$ and an edge set $E$. Each edge $(i, j) \in E$ has a measured relative pose $Z_{ij} \in SE(d)$, with $d = 2$ or $3$, and a symmetric positive definite information matrix $\Omega_{ij}$ of size 3 or 6.

**Error of an edge.** For poses $X_i, X_j \in SE(d)$, the error is
$$e_{ij}(X_i, X_j) = \mathrm{Log}\big(Z_{ij}^{-1} X_i^{-1} X_j\big),$$
the vector of the transformation that is left when the measured relative pose is removed from the estimated one. In the plane, many systems use the simpler form $e_{ij} = \big(R_i^\top (t_j - t_i) - t_{ij},\ \mathrm{wrap}(\theta_j - \theta_i - \theta_{ij})\big)$. See [pose compounding operators](/pose-compounding-operators/).

**The question.** Find
$$X^\star = \arg\min_{X_1, \dots, X_n} \sum_{(i,j) \in E} e_{ij}^\top \Omega_{ij}\, e_{ij}.$$
The cost does not change when all poses are multiplied on the left by one pose, so one pose is fixed, usually $X_1 = I$. Without this gauge the minimizer is not unique.

**Nonconvexity.** Even with exact measurements on a cycle, the cost has local minima that are not global. See the second example below.

## Variants

- **Planar and spatial.** $SE(2)$ with 3 parameters per pose, or $SE(3)$ with 6.
- **Chordal cost.** Replace the geodesic rotation error by the Frobenius distance $\kappa_{ij} \|R_j - R_i \tilde R_{ij}\|_F^2$, and the translation error by $\tau_{ij} \|t_j - t_i - R_i \tilde t_{ij}\|^2$. This is the form that [SE-Sync](/se-sync/) relaxes. For small errors it is close to the geodesic form.
- **Rotations only.** Without translations the problem is rotation synchronization, also called [rotation averaging](/rotation-averaging/) in structure from motion.
- **Translations only.** With known rotations the cost is a linear least squares problem in the translations and is convex.
- **With landmarks.** If landmark positions are also unknowns, the problem is [full SLAM](/full-slam/) on a [factor graph](/factor-graph/). Marginalizing the landmarks gives a pose graph again, with denser edges.
- **Robust versions.** With wrong loop closures, a robust kernel or [switchable constraints](/switchable-constraints/) replace the squared error for the doubtful edges.
- **Online.** The graph grows over time, and the estimate must be updated after each new edge, as in [iSAM](/isam/) and [iSAM2](/isam2/).

## Examples

**A one-dimensional loop.** Three poses on a line, $x_0 = 0$ fixed. Odometry says $x_1 - x_0 = 1$ and $x_2 - x_1 = 1$. A loop closure says $x_2 - x_0 = 1.7$. All weights are 1. The cost is $(x_1 - 1)^2 + (x_2 - x_1 - 1)^2 + (x_2 - 1.7)^2$. Setting the two derivatives to zero gives $2x_1 - x_2 = 0$ and $2x_2 - x_1 = 2.7$, so $x_1 = 0.9$ and $x_2 = 1.8$. The three errors are $-0.1$, $-0.1$ and $0.1$, and the cost is $0.03$. The disagreement of 0.3 between odometry and the loop closure is spread equally over the three edges. Without rotations the problem is linear and convex, and this is the global optimum.

**A wrong local minimum.** Take $n$ rotations in the plane on a cycle, with every measurement equal to the identity and every weight 1. In the chordal cost, an edge whose two angles differ by $\delta$ costs $\|\mathrm{Rot}(\delta) - I\|_F^2 = 4 - 4\cos\delta$. The global minimum puts all angles equal, with cost 0. Now put $\theta_i = 2\pi i / n$. Each edge has $\delta = 2\pi / n$, and the cost is $n (4 - 4\cos(2\pi/n))$. The derivative with respect to $\theta_i$ is $4 \sin\delta - 4 \sin\delta = 0$, so this is a critical point. The Hessian in the angles is $4 \cos(2\pi/n)$ times the [Laplacian matrix](/laplacian-matrix/) of the cycle. For $n \ge 5$, $\cos(2\pi/n) > 0$, so the Hessian is positive semidefinite, and its only null direction turns all angles together, which does not change the cost. So the twisted state is a local minimum that is not global. For $n = 5$ its cost is $5(4 - 4\cos 72°) = 13.82$. A Gauss-Newton solver started there does not move. The [SE-Sync](/se-sync/) page shows how its certificate finds the way out of this state.

## Known algorithms

- **Gauss-Newton and Levenberg-Marquardt on the manifold.** Linearize each error at the current poses, solve the sparse normal equations, and update each pose by a retraction. This is the method of Lu and Milios and of the tutorial of Grisetti et al., and the core of general solvers such as g2o, Ceres and GTSAM. See [Gauss-Newton](/gauss-newton-algorithm/), [Levenberg-Marquardt](/levenberg-marquardt/) and [Powell's dog leg](/powell-dogleg/). Each step costs one sparse solve. They find a local minimum and depend on the initial guess.
- **Square root methods.** [Square root SAM](/square-root-sam/) factors the measurement Jacobian by QR or Cholesky with a fill-reducing order. [iSAM](/isam/) and [iSAM2](/isam2/) update the factor as the graph grows. They solve the same linearized systems, faster.
- **Initialization.** A [spanning tree](/spanning-tree/) of odometry edges, or chordal relaxation of the rotations followed by a linear solve for the translations, gives a starting point that often lies in the basin of the global minimum.
- **Stochastic gradient and tree parameterizations.** Olson, Leonard and Teller, and later Grisetti and colleagues in TORO, used incremental pose parameterizations that converge from poor initial guesses.
- **Certifiable methods.** [SE-Sync](/se-sync/) solves a semidefinite relaxation by a low rank Riemannian method and returns a certificate of global optimality when the relaxation is tight.
- **Information filters.** [GraphSLAM](/graphslam/) and the [extended information filter](/extended-information-filter/) work with the same information form, with landmarks.

## Bounds

No closed form solution is known for the general problem. A Gauss-Newton step costs one solve of a sparse positive definite system of size $3n$ or $6n$. Its cost depends on the fill-in of the factor; see [elimination ordering](/elimination-ordering/). For a graph that is mostly a chain with few loops, the fill is small and a step takes close to linear time. The number of steps depends on the initial guess and the noise.

SE-Sync gives a global optimum in polynomial time when the relaxation is exact. Rosen et al. prove that it is exact when the noise is below a level that depends on the graph. Above that level the relaxation can have a gap, and then it gives only a lower bound. This page gives no complexity result for the general problem, because none was confirmed from a source.

## Reductions

- **Translations from rotations.** For fixed rotations the cost is a linear least squares problem in the translations. So the problem reduces to a problem over the rotations alone, with a modified data matrix. SE-Sync uses this step.
- **Full SLAM to a pose graph.** Eliminating the landmarks from the information matrix of [full SLAM](/full-slam/) leaves a pose graph whose edges are the marginal constraints. This is the step of [GraphSLAM](/graphslam/) after the landmarks are eliminated.
- **Linear least squares.** Each Gauss-Newton step is a [least squares problem](/least-squares-problem/) with a sparse Jacobian.

## Applications

- The back end of lidar SLAM systems that build pose graphs from scan matching, such as [LOAM](/lidar-odometry-and-mapping/) with a loop closure module, or systems based on [correlative scan matching](/correlative-scan-matching/).
- The loop closing step of visual SLAM, for example the essential graph optimization of [ORB-SLAM](/orb-slam/).
- Multi-robot mapping, where the graphs of several robots are joined by inter-robot edges.
- [Rotation averaging](/rotation-averaging/) and the initialization of [bundle adjustment](/bundle-adjustment/) in structure from motion.

## References
