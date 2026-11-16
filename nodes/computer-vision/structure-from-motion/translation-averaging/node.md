---
tag: B6KXJE
kind: problem
slug: translation-averaging
name: Translation averaging
aliases:
- camera location estimation from directions
area: computer-vision/structure-from-motion
level: advanced
summary: Find camera positions from known rotations and measured pairwise translation directions, which fix them only up to a global scale and offset.
prereqs: [rotation-averaging, view-graph]
see_also: [global-structure-from-motion, rotation-averaging, generic-rigidity, laman-theorem, rigidity-matrix, eigenvalue-problem, iteratively-reweighted-least-squares, robust-model-fitting]
sources:
  - paper: doi:10.1109/CVPR.2015.7298883
    title: "Onur Özyeşil and Amit Singer, Robust camera location estimation by convex programming, IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2015), 2674-2683"
    locator: "the whole paper (parallel rigidity, the least unsquared deviations formulation and its solution)"
  - paper: doi:10.1007/978-3-319-10578-9_5
    title: "Kyle Wilson and Noah Snavely, Robust global translations with 1DSfM, Computer Vision ECCV 2014, Lecture Notes in Computer Science, Springer, 2014, 61-75"
    locator: "the whole paper (the outlier filter by one-dimensional projections and the chordal cost on the directions)"
  - paper: doi:10.1109/ICCV.2013.66
    title: "Nianjuan Jiang, Zhaopeng Cui and Ping Tan, A global linear method for camera pose registration, IEEE International Conference on Computer Vision (ICCV 2013), 481-488"
    locator: "the linear constraints on the camera positions from triplets of cameras"
  - paper: doi:10.1109/CVPR.2001.990963
    title: "Venu Madhav Govindu, Combining two-view constraints for motion estimation, IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2001), vol. 2, 218-225"
    locator: "the linear estimation of the translations from the pairwise directions"
  - paper: doi:10.1017/S096249291700006X
    title: "Onur Özyeşil, Vladislav Voroninski, Ronen Basri and Amit Singer, A survey of structure from motion, Acta Numerica 26, 2017, 305-364"
    locator: "the section on location estimation (the formulations, parallel rigidity and the robust methods)"
---

Translation averaging is the problem of finding the positions of $N$ cameras when their rotations are known and, for some pairs of cameras, the direction from one camera center to the other has been measured. The pairs are the edges of a [view graph](/view-graph/). The direction of an edge comes from the relative translation of the pair, which two-view geometry gives only up to scale, rotated into the world frame with the result of [rotation averaging](/rotation-averaging/). Directions say nothing about distances, so the positions are fixed at best up to one common shift and one common positive scale, and only if the graph is parallel rigid, a condition on the graph similar to [generic rigidity](/generic-rigidity/). It is the second step of [global structure from motion](/global-structure-from-motion/), and usually the weakest one: directions are noisy for pairs with a short baseline, wrong pairs give wrong directions, and some natural cost functions collapse the cameras into clusters.

## In plain words

You know which way every camera points, and for pairs of cameras you know in which direction one stands as seen from the other, but not how far away it is. Translation averaging finds where all the cameras stand. Picture a map with pins and, for some pairs of pins, an arrow that shows the direction from one pin to the other. You must place the pins so that the arrows fit. You can never learn the size of the map, or where it sits, from directions alone. If the pins are linked only in a chain, each link can still stretch or shrink, so you need loops of arrows, enough of them, to fix the shape. Some arrows are wrong, so a good method must not let them pull the whole map apart.

## Definition

**Input.** A connected graph $G = (V, E)$ with $V = \{1, \dots, N\}$, the camera rotations $R_k$, and for each edge $(i, j) \in E$ a relative translation $t_{ij}$, known up to a positive scale, with the convention $X_j = R_{ij} X_i + t_{ij}$.

**Directions.** With $X_c = R_k X + t_k$ and the center $c_k = -R_k^{\mathsf T} t_k$, the exact relative translation is $t_{ij} = t_j - R_{ij} t_i = -R_j (c_j - c_i)$. So the unit direction of the edge in the world frame is
$$v_{ij} = \frac{-R_j^{\mathsf T} t_{ij}}{\|t_{ij}\|}, \qquad c_j - c_i = \lambda_{ij} v_{ij} \text{ with } \lambda_{ij} > 0.$$

**Output.** Centers $c_1, \dots, c_N$ such that $c_j - c_i$ points along $v_{ij}$ as well as possible, with the gauge fixed, for example by $c_1 = 0$ and $\sum_k \|c_k\|^2 = 1$. Common costs are:

- the linear cost $\sum_{(i,j)} \| (I - v_{ij} v_{ij}^{\mathsf T}) (c_j - c_i) \|^2 = \sum \| v_{ij} \times (c_j - c_i) \|^2$, the squared distance of $c_j - c_i$ from the line of $v_{ij}$;
- the chordal cost $\sum \| v_{ij} - (c_j - c_i) / \|c_j - c_i\| \|^2$, which compares unit vectors;
- the least unsquared deviations (LUD) cost $\sum \| c_j - c_i - d_{ij} v_{ij} \|$ over the centers and scales $d_{ij} \ge 1$.

**Gauge.** If $c_k$ is a solution, so is $s c_k + d$ for any shift $d$ and scale $s > 0$, because $s (c_j - c_i)$ has the same direction. The scale $s < 0$ reverses every direction, so the sign of the directions fixes the mirror, but the linear cost does not see the sign.

## Variants

- **With points.** The tracks can enter the problem: with known rotations, each observation gives the constraint $\tilde x_{ij} \times (R_i X_j + t_i) = 0$, linear in points and translations. This uses all the data, not only one direction per pair, and handles collinear camera motion.
- **With triplets.** Jiang, Cui and Tan (2013) use triplets of cameras whose relative scales are fixed by the local geometry of the triangle, which gives linear equations that do not let the solution collapse.
- **Robust variants.** A fraction of the directions are outliers. The robust costs are LUD, the ShapeFit formulation, and losses that downweight long baselines or large residuals.
- **Known scales.** When the distances of the edges are known, as in SLAM with odometry or a stereo rig, the problem becomes linear least squares in the centers, the translation part of [pose graph optimization](/pose-graph-optimization/).

## Examples

- **A triangle.** Three cameras not on one line, with the three directions of the triangle: the triangle is fixed up to shift and scale, because its angles are fixed by the directions. This is the smallest parallel rigid graph.
- **A chain is not enough.** For 4 cameras on the path $1, 2, 3, 4$, each of the 3 edges can change its length independently, so the centers have a 3-parameter family of solutions, one of which is the global scale. With $c_1 = 0$, the $9 \times 9$ matrix of the linear cost has 3 zero eigenvalues. Closing the path into the cycle $1, 2, 3, 4, 1$ leaves a single zero eigenvalue, the scale, so the generic 4-cycle is parallel rigid in 3D. The reference code of [global structure from motion](/global-structure-from-motion/) checks both counts.
- **Exact directions on 6 cameras.** With 10 exact directions on 6 cameras in general position, the smallest eigenvector of the linear cost gives the true centers to $10^{-9}$ after the gauge is fixed (a benchmark result of the same test).
- **Collinear cameras.** A camera that moves forward along a straight line gives the same direction for every pair. The relative distances along the line cannot be found from the directions at all, so a video of forward motion needs the points or known scales.

## Known algorithms

- **Linear least squares.** Minimize the linear cost under the gauge constraint. The answer is the eigenvector of the smallest eigenvalue of a sparse $3N \times 3N$ matrix, a block Laplacian with the blocks $I - v_{ij} v_{ij}^{\mathsf T}$ (Govindu 2001; Brand, Antone and Teller 2004). It is fast, but it favors short baselines: pairs that are far apart cost more for the same angle error, so the minimum tends to pull cameras together into clusters (a known weakness, shown in many experiments).
- **1DSfM.** Wilson and Snavely (2014) project all directions onto many random one-dimensional axes, solve an ordering problem on each to find edges that disagree, remove these outliers and then minimize the chordal cost by nonlinear least squares.
- **LUD.** Özyeşil and Singer (2015) minimize the least unsquared deviations cost, a convex problem, by [iteratively reweighted least squares](/iteratively-reweighted-least-squares/). The constraint $d_{ij} \ge 1$ prevents the collapse to a point.
- **ShapeFit and its relatives.** Goldstein, Hand and coauthors minimize the sum of the unsquared distances to the lines under one linear normalization, a convex program with exact recovery guarantees under random corruption models.
- **Global linear method.** Jiang, Cui and Tan (2013) solve one sparse linear system built from camera triplets.

## Bounds

- **Parallel rigidity (theorem).** Exact directions determine the centers up to shift and scale if and only if the framework is parallel rigid. For centers in general position this depends only on the graph. In 3D each edge gives 2 independent constraints, and there are $3N - 4$ unknowns after the gauge, so $2|E| \ge 3N - 4$ is necessary (a counting argument). A random choice of directions and a rank test of the linear cost matrix decide generic parallel rigidity with probability 1.
- **The counting condition is not sufficient.** As for [Laman's theorem](/laman-theorem/) in rigidity theory, the edges must also be spread out: a dense part of the graph cannot make up for a part that is only a chain, because the extra edges of the dense part are redundant.
- **Exact recovery under corruption.** Under random models of corrupted directions, convex methods such as ShapeFit and LUD recover the exact locations with high probability when the fraction of outliers is below a constant (theorems of their authors, under the stated models).
- **Cost.** The linear method costs one sparse eigenvector computation of size $3N$. LUD costs a sequence of sparse weighted least squares problems.

## Reductions

- **From global SfM.** Global SfM reduces to rotation averaging, then translation averaging, then triangulation with fixed cameras.
- **To an eigenvalue problem.** With the linear cost and the constraint $\sum \|c_k\|^2 = 1$, the problem is the smallest [eigenvalue problem](/eigenvalue-problem/) of a symmetric positive semidefinite matrix (theorem).
- **To rigidity theory.** Parallel rigidity is the bearing version of the distance [rigidity](/generic-rigidity/) of frameworks, and the matrix of the linear cost plays the role of the [rigidity matrix](/rigidity-matrix/).
- **To sensor network localization.** Locating sensors from measured bearings is the same problem.

## Applications

- The location step of global SfM systems, after rotation averaging.
- Camera network calibration and sensor network localization from bearings.
- Merging partial reconstructions whose relative directions are known.

## References
