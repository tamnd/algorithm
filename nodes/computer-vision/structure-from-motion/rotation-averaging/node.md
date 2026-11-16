---
tag: YMV3VT
kind: problem
slug: rotation-averaging
name: Rotation averaging
aliases:
- multiple rotation averaging
- rotation synchronization
area: computer-vision/structure-from-motion
level: advanced
summary: Find absolute rotations of many cameras that best agree with measured relative rotations on the edges of a view graph.
prereqs: [special-orthogonal-group, view-graph]
see_also: [lie-algebraic-rotation-averaging, translation-averaging, global-structure-from-motion, so3-logarithm-map, pose-graph-optimization, se-sync, semidefinite-programming, laplacian-matrix]
sources:
  - paper: doi:10.1007/s11263-012-0601-0
    title: "Richard Hartley, Jochen Trumpf, Yuchao Dai and Hongdong Li, Rotation averaging, International Journal of Computer Vision 103(3), 2013, 267-305"
    locator: "the whole survey (the metrics on SO(3), single and multiple rotation averaging, convexity, and the algorithms)"
  - paper: doi:10.1109/CVPR.2004.1315098
    title: "Venu Madhav Govindu, Lie-algebraic averaging for globally consistent motion estimation, IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2004), vol. 1, 684-691"
    locator: "the statement of motion averaging on a graph and the iterative Lie-algebraic solution"
  - paper: doi:10.1109/CVPR.2007.383115
    title: "Daniel Martinec and Tomas Pajdla, Robust rotation and translation estimation in multiview reconstruction, IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2007), 1-8"
    locator: "the linear method for the rotations (a least squares problem in the matrix entries followed by a projection onto the rotations)"
  - paper: doi:10.1109/TPAMI.2017.2693984
    title: "Avishek Chatterjee and Venu Madhav Govindu, Robust relative rotation averaging, IEEE Transactions on Pattern Analysis and Machine Intelligence 40(4), 2018, 958-972"
    locator: "the robust formulation and the comparison of the cost functions"
  - paper: doi:10.1007/978-3-319-46478-7_16
    title: "Kyle Wilson, David Bindel and Noah Snavely, When is rotations averaging hard?, Computer Vision ECCV 2016, Lecture Notes in Computer Science, Springer, 2016, 255-270"
    locator: "the local convexity analysis in terms of the graph Laplacian"
  - paper: doi:10.1109/cvpr.2018.00021
    title: "Anders Eriksson, Carl Olsson, Fredrik Kahl and Tat-Jun Chin, Rotation averaging and strong duality, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2018), 127-135"
    locator: "the Lagrangian dual of chordal rotation averaging and the condition for strong duality"
---

Rotation averaging is the problem of finding the absolute orientations $R_1, \dots, R_N$ of $N$ cameras from noisy measurements of some of their relative orientations $R_{ij} \approx R_j R_i^{\mathsf T}$. The measured pairs are the edges of a [view graph](/view-graph/), and the relative rotations come from the [essential matrices](/essential-matrix/) of the image pairs. Each absolute rotation appears in many edges, so the edges are redundant, and the problem asks for the rotations that agree with all of them as well as possible under a chosen distance on the [rotation group](/special-orthogonal-group/) and a chosen loss. The answer is fixed only up to one common rotation, the gauge. Rotation averaging is the first step of [global structure from motion](/global-structure-from-motion/), before [translation averaging](/translation-averaging/), and the rotation part of [pose graph optimization](/pose-graph-optimization/) in SLAM. The name multiple rotation averaging separates it from single rotation averaging, the mean of several measurements of one rotation. The best known algorithm in vision is [Lie-algebraic rotation averaging](/lie-algebraic-rotation-averaging/).

## In plain words

Each camera in a set of photos points in some direction, and you want to know all these directions. For pairs of photos that overlap, you can measure how much the second camera is turned compared with the first. These pair measurements have small errors, and some are completely wrong. Rotation averaging finds one direction per camera so that the pair measurements fit as well as possible. If you only chain the measurements from one camera to the next along a path, the errors add up, and different paths give different answers. Averaging uses all pairs together and spreads the errors over them. Turning all cameras together by the same amount does not change any pair, so one camera is fixed as the reference.

## Definition

**Input.** A connected graph $G = (V, E)$ with $V = \{1, \dots, N\}$, and for each edge $(i, j) \in E$ a measured rotation $R_{ij} \in SO(3)$. The convention is $X_j = R_{ij} X_i + t_{ij}$ for the coordinates of a point in the frames of cameras $i$ and $j$, so with absolute rotations $X_c = R_k X + t_k$ the exact relation is $R_{ij} = R_j R_i^{\mathsf T}$.

**Output.** Rotations $R_1, \dots, R_N \in SO(3)$ that minimize
$$F(R_1, \dots, R_N) = \sum_{(i, j) \in E} \rho\big( d(R_{ij}, R_j R_i^{\mathsf T}) \big),$$
with $R_1 = I$ to fix the gauge.

**Distances.** For a rotation $Q$ by the angle $\theta \in [0, \pi]$, $\operatorname{trace} Q = 1 + 2 \cos \theta$. The angular, or geodesic, distance is $d_\angle(A, B) = \arccos\big((\operatorname{trace}(A^{\mathsf T} B) - 1)/2\big)$, the angle of $A^{\mathsf T} B$, which is also $\|\log(A^{\mathsf T} B)\|$ with the [logarithm map](/so3-logarithm-map/). The chordal distance is $d_F(A, B) = \|A - B\|_F = 2 \sqrt 2 \sin(\theta / 2)$. The quaternion distance uses $\min(\|q_A - q_B\|, \|q_A + q_B\|)$ for unit quaternions in the Hamilton convention. All three are close to $\theta$ times a constant for small angles.

**Losses.** $\rho(d) = d^2$ gives the least squares problems, which are the maximum likelihood problems for small Gaussian noise. $\rho(d) = d$ gives the $L_1$ problem, which is less affected by wrong edges. Bounded losses such as Geman-McClure, $\rho(d) = d^2 / (d^2 + \sigma^2)$, ignore large residuals almost completely.

**Gauge.** If $R_k$ solves the problem, so does $R_k Q$ for any fixed $Q \in SO(3)$, since $(R_j Q)(R_i Q)^{\mathsf T} = R_j R_i^{\mathsf T}$. Fixing $R_1 = I$ removes this freedom.

## Variants

- **Single rotation averaging.** One rotation, many measurements of it: find the mean of $R^{(1)}, \dots, R^{(k)}$. With the chordal $L_2$ cost, the answer is the arithmetic mean projected onto $SO(3)$ by the [singular value decomposition](/singular-value-decomposition/) (theorem). With the geodesic $L_2$ cost, it is the Karcher mean, found by iteration.
- **Rotations in the plane.** In $SO(2)$, rotations are angles, and the problem becomes angular synchronization: find angles $\theta_k$ with $\theta_j - \theta_i \approx \theta_{ij}$ modulo $2\pi$. Singer (2011) solved it by an eigenvector of a Hermitian matrix.
- **Robust averaging.** A fraction of the edges are outliers. The loss is $L_1$ or bounded, or the outliers are removed first by cycle tests on the [view graph](/view-graph/).
- **Weighted averaging.** Each edge has a weight or a full covariance, for example from the number of inliers of its pair.
- **Pose averaging.** The edges carry full relative poses in $SE(3)$ with known translation scales. This is [pose graph optimization](/pose-graph-optimization/); with the chordal cost it can be solved with a certificate by [SE-Sync](/se-sync/).

## Examples

- **A tree.** If $G$ is a tree, every edge can be met exactly: fix $R_1 = I$ and set $R_j = R_{ij} R_i$ along the tree. The cost is 0, and the solution is unique up to the gauge. There is no redundancy, so the noise of each edge goes straight into the result.
- **A triangle of rotations about one axis.** Take rotations about the $Z$ axis with $R_{12}$ by $10^\circ$, $R_{23}$ by $20^\circ$ and $R_{13}$ by $33^\circ$. Going around the cycle gives $10 + 20 - 33 = -3$ degrees, so no choice fits all three edges. With $R_1 = I$, the squared geodesic cost $(\theta_2 - 10)^2 + (\theta_3 - \theta_2 - 20)^2 + (\theta_3 - 33)^2$ has its minimum at $\theta_2 = 11^\circ$, $\theta_3 = 32^\circ$, with a residual of $1^\circ$ on each edge. The $L_1$ cost has the value $3^\circ$ at every split of the $3^\circ$ among the three edges with the same sign, so its minimizer is not unique; one minimizer puts all of it on one edge.
- **One wrong edge.** On a complete graph of 6 cameras with exact edges, replace one edge by a rotation $0.5$ rad away. The least squares solution spreads this error over all cameras. The robust run of the [Lie-algebraic algorithm](/lie-algebraic-rotation-averaging/) in the reference code of [global structure from motion](/global-structure-from-motion/) returns rotations within $2 \cdot 10^{-3}$ rad of the truth, and the edge test then removes exactly the wrong edge (a benchmark result on this test).

## Known algorithms

- **Spanning tree.** Chain the rotations along a [maximum spanning tree](/maximum-spanning-tree/) of the view graph. It costs $O(N)$ after the tree is built, but uses no redundancy. It is the usual start for the iterative methods.
- **Linear chordal relaxation.** Martinec and Pajdla (2007) drop the constraint $R_k \in SO(3)$, solve the linear least squares problem $R_j \approx R_{ij} R_i$ in the 9 entries of each matrix, and project each result onto $SO(3)$. A spectral form takes the top 3 eigenvectors of the $3N \times 3N$ matrix of the blocks $R_{ij}$, as in angular synchronization.
- **Lie-algebraic averaging.** [Govindu (2004)](/lie-algebraic-rotation-averaging/) linearizes the residuals in the Lie algebra $\mathfrak{so}(3)$, solves a sparse [Laplacian](/laplacian-matrix/) system for an update of all rotations, and repeats. Chatterjee and Govindu (2013, 2018) made it robust with an $L_1$ start and [iteratively reweighted least squares](/iteratively-reweighted-least-squares/).
- **Weiszfeld iterations.** Hartley, Aftab and Trumpf (2011) minimize the $L_1$ geodesic cost one rotation at a time with the Weiszfeld algorithm for the geometric median.
- **Semidefinite relaxation.** Fredriksson and Olsson (2012) and Eriksson, Olsson, Kahl and Chin (2018) solve the [Lagrangian dual](/lagrangian-duality/) of the chordal $L_2$ problem as a [semidefinite program](/semidefinite-programming/); when the dual is tight, the result is the global minimum with a certificate. Shonan averaging and rotation coordinate descent solve the same relaxation faster.

## Bounds

- **Identifiability (theorem).** With exact data on a connected graph, the solution is unique up to the gauge, because chaining along any spanning tree fixes every rotation. With a disconnected graph, each component has its own gauge, and the relative orientation of the components is not determined.
- **Non-convexity.** $SO(3)$ is not a convex set, and the multiple averaging cost has local minima that are not global, even for the $L_2$ geodesic cost. For single rotation averaging the picture is simpler: Hartley et al. (2013) show that the geodesic $L_2$ cost has a unique minimum when all measurements lie in a small enough ball, and they give the radius (theorem).
- **When it is easy.** Wilson, Bindel and Snavely (2016) bound the size of the region where the cost is locally convex in terms of the algebraic connectivity of the graph Laplacian and the noise level: well connected graphs with small noise are easy, and long chains with large noise are hard (theorem).
- **Strong duality (theorem).** Eriksson et al. (2018) prove that the semidefinite relaxation of chordal $L_2$ averaging is tight, so the global minimum can be found in polynomial time, when the residual angles at the optimum are below a bound that depends on the algebraic connectivity of the graph.
- **Cost of a step.** The iterative methods solve one sparse linear system with $3N$ unknowns per iteration. For the view graphs of SfM, a sparse Cholesky factorization or the conjugate gradient method makes a step close to linear in $|E|$.

## Reductions

- **From global SfM.** [Global structure from motion](/global-structure-from-motion/) reduces to rotation averaging, then [translation averaging](/translation-averaging/) with the rotations fixed, then triangulation.
- **From pose graph optimization.** Fixing the translations of a pose graph leaves rotation averaging; many pose graph solvers start from a rotation averaging solution.
- **To a linear problem by relaxation.** Dropping the orthogonality constraints gives a linear least squares problem (chordal relaxation); dropping the rank constraint of the lifted $3N \times 3N$ matrix gives a semidefinite program.
- **To angular synchronization.** For rotations about one common axis, the problem is synchronization over $SO(2)$, the unit complex numbers.

## Applications

- The rotation step of global SfM pipelines such as the method of Moulon, Monasse and Marlet (2013), 1DSfM (Wilson and Snavely 2014) and their successors.
- Rotation initialization for [pose graph optimization](/pose-graph-optimization/) after [loop closures](/loop-closure-detection/) in SLAM.
- Multi-camera rig calibration, where the relative rotations between the cameras of a rig come from many captures.
- Cryo-electron microscopy, where the orientations of many noisy projections of one molecule are found by synchronization of their relative rotations.

## References
