---
tag: 8T28XX
kind: problem
slug: non-rigid-registration
name: Non-rigid point set registration
aliases:
- deformable point set registration
area: computer-vision/point-clouds-and-registration
level: advanced
summary: "Find a deformation, not just a rigid motion, that maps one point set or surface onto another, with a regularizer for smoothness."
prereqs: [point-cloud-registration, tikhonov-regularization]
see_also: [coherent-point-drift, robust-point-matching, as-rigid-as-possible-deformation, iterative-closest-point, image-registration, radial-basis-function-interpolation, gaussian-mixture-model, point-set-chamfer-distance]
sources:
  - paper: doi:10.1109/TVCG.2012.310
    title: "Gary K. L. Tam, Zhi-Quan Cheng, Yu-Kun Lai, Frank C. Langbein, Yonghuai Liu, David Marshall, Ralph R. Martin, Xian-Fang Sun and Paul L. Rosin, Registration of 3D point clouds and meshes: a survey from rigid to nonrigid, IEEE Transactions on Visualization and Computer Graphics 19(7), 2013, 1199-1217"
    locator: "The survey of non-rigid registration: the deformation models, the regularizers, and the methods for point sets and meshes"
  - paper: doi:10.1109/TPAMI.2010.46
    title: "Andriy Myronenko and Xubo Song, Point set registration: Coherent point drift, IEEE Transactions on Pattern Analysis and Machine Intelligence 32(12), 2010, 2262-2275"
    locator: "Non-rigid registration as the fit of a Gaussian mixture with a motion coherence regularizer, and the fast Gauss transform and low-rank approximations for large sets"
  - paper: doi:10.1016/S1077-3142(03)00009-2
    title: "Haili Chui and Anand Rangarajan, A new point matching algorithm for non-rigid registration, Computer Vision and Image Understanding 89(2-3), 2003, 114-141"
    locator: "Soft correspondences with a thin-plate spline map and deterministic annealing"
  - paper: doi:10.1109/TPAMI.2010.223
    title: "Bing Jian and Baba C. Vemuri, Robust point set registration using Gaussian mixture models, IEEE Transactions on Pattern Analysis and Machine Intelligence 33(8), 2011, 1633-1645"
    locator: "Registration by the L2 distance between two Gaussian mixtures, with thin-plate spline and Gaussian radial basis function maps"
  - paper: doi:10.1109/CVPR.2007.383165
    title: "Brian Amberg, Sami Romdhani and Thomas Vetter, Optimal step nonrigid ICP algorithms for surface registration, Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2007)"
    locator: "Non-rigid ICP with an affine map per vertex of a template mesh and a stiffness term that is lowered step by step"
  - paper: doi:10.1109/34.24792
    title: "Fred L. Bookstein, Principal warps: thin-plate splines and the decomposition of deformations, IEEE Transactions on Pattern Analysis and Machine Intelligence 11(6), 1989, 567-585"
    locator: "The thin-plate spline map through given landmark pairs, its bending energy, and its closed form"
---

Non-rigid point set registration asks for a deformation that maps a source point set $Y$ onto a target point set $X$, when a rotation and a translation are not enough: a face changes its expression, an organ moves with breathing, a hand bends its fingers, or two scans show two different objects of the same kind. It is the non-rigid form of [point cloud registration](/point-cloud-registration/). As in the rigid case, the correspondences are usually not known. Unlike the rigid case, the space of maps is huge, so any set can be bent onto any other. A useful problem needs a regularizer: a term that prefers smooth or nearly rigid deformations, in the sense of [Tikhonov regularization](/tikhonov-regularization/). The problem is a trade-off between how well the deformed source fits the target and how much the deformation costs.

## In plain words

You have two clouds of dots that show the same kind of thing, but one is bent, stretched or squashed compared with the other. Turning and sliding is not enough to lay one on the other.

So we let every dot of the first cloud move on its own. But if dots could move freely, we could pile them all onto any dots we like, and the result would mean nothing. So we ask for a smooth move: dots that start close together should move in nearly the same way, like a rubber sheet.

The task is to find the smooth move that brings the first cloud closest to the second. A stiff sheet fits less well but keeps the shape; a soft one fits better but may tear the shape apart.

## Definition

**Input.** A target set $X = \{x_1, \ldots, x_n\}$ and a source set $Y = \{y_1, \ldots, y_m\}$ in $\mathbb{R}^d$, a class $\mathcal{T}$ of maps $T : \mathbb{R}^d \to \mathbb{R}^d$, a discrepancy $D$ between point sets that needs no correspondences, a regularizer $R : \mathcal{T} \to [0, \infty)$, and a weight $\lambda > 0$.

**Output.** A map

$$T^\star \in \arg\min_{T \in \mathcal{T}} \; D\bigl(T(Y), X\bigr) + \lambda\, R(T),$$

and often also a correspondence between $Y$ and $X$, either hard or as a soft match matrix.

Common choices:

- **Discrepancy.** The [chamfer distance between point sets](/point-set-chamfer-distance/); the negative log likelihood of $X$ under a [Gaussian mixture](/gaussian-mixture-model/) centred at $T(Y)$, as in [coherent point drift](/coherent-point-drift/); the softassign energy of [robust point matching](/robust-point-matching/); or the $L_2$ distance between two Gaussian mixtures (Jian and Vemuri).
- **Map and regularizer.** A thin-plate spline with its bending energy $\int \|\nabla^2 T\|^2$ (Bookstein); a sum of Gaussian [radial basis functions](/radial-basis-function-interpolation/) with a norm that penalizes high frequencies of the displacement, the motion coherence of CPD; an affine map per vertex of a mesh with a penalty on the difference between the maps of neighbours (Amberg et al.); or the [as-rigid-as-possible](/as-rigid-as-possible-deformation/) energy, which penalizes how far each local patch is from a rigid motion.

$D$ must not need correspondences; when the correspondences are given, $D$ is a sum of squared distances between pairs, and the problem becomes a smoothing or interpolation problem.

## Variants

- **Known correspondences.** With landmark pairs $(y_k, x_k)$, the problem is to interpolate or smooth a map through them. For the thin-plate spline it has a closed form, a linear system of size about $m$ (Bookstein).
- **Point sets or surfaces.** With meshes, the regularizer can use the mesh edges, and the discrepancy can use normals or point to plane distances.
- **Partial overlap and outliers.** Real scans see different parts. The discrepancy must allow points with no partner: a uniform outlier term in a mixture, or the slacks of softassign.
- **Articulated motion.** The deformation is a set of rigid parts joined at joints, as for a human body.
- **Isometric deformation.** The deformation keeps geodesic distances on the surface, as for cloth or a body in a new pose; the task is then mostly to find the correspondence.
- **Dense images.** For images and volumes, the analogue is deformable [image registration](/image-registration/), where the discrepancy compares intensities.
- **Groupwise registration.** Many sets are registered to a common template at once.

## Examples

**A bend that no rigid or affine map can fit.** Let $Y = \{(0, 0), (1, 0), (2, 0)\}$ and $X = \{(0, 0), (1, 0.5), (2, 0)\}$, with the pairs known. The centroids are $(1, 0)$ and $(1, 1/6)$. After the centring, the $y$ coordinates of $X$ are $-1/6$, $1/3$ and $-1/6$, while those of $Y$ are all 0, and the cross-covariance matrix is $\operatorname{diag}(2, 0)$, so the best rotation is the identity. The sum of squared residuals is $1/36 + 1/9 + 1/36 = 1/6$. An affine map cannot do better, because it sends the three collinear points of $Y$ to three collinear points, and the best line through $X$ in the least squares sense, $y = 1/6$, leaves the same residual $1/6$. A non-rigid map fits exactly, for example $T(u, w) = \bigl(u,\; w + 0.5 - 0.5 (u - 1)^2\bigr)$, which lifts the middle point by $0.5$ and leaves the end points in place. Its second derivatives are not zero, so a bending energy charges it a positive cost, and the weight $\lambda$ decides whether the exact fit is worth that cost.

**Collapse without a regularizer.** Let the discrepancy be the one-sided distance $\sum_k \min_j |T(y_k) - x_j|^2$, and let $T$ be any map. The map that sends every $y_k$ to $x_1$ has cost 0, so it is a minimizer, and it says nothing about the shapes. A two-sided discrepancy rules out this collapse, but not other wild maps: a map that sends each $y_k$ to some $x_j$ so that every $x_j$ is hit also has cost 0. Only the regularizer makes the problem well posed.

**Faces.** A template face mesh is deformed onto a scan of a new face, so that every vertex of the template lands on the same part of the new face, for example the tip of the nose. The template has a fixed structure, so every scan then has the same vertices, which is the first step to build a statistical model of faces. Non-rigid ICP (Amberg et al.) was built for this use.

## Known algorithms

| Method | Discrepancy and correspondence | Deformation and regularizer |
|---|---|---|
| Thin-plate spline [robust point matching](/robust-point-matching/) (Chui and Rangarajan, 2003) | softassign with slacks, deterministic annealing | thin-plate spline, bending energy |
| [Coherent point drift](/coherent-point-drift/) (Myronenko and Song, 2010) | Gaussian mixture with a uniform outlier term, fitted by EM | Gaussian radial basis functions, motion coherence |
| Gaussian mixture $L_2$ registration (Jian and Vemuri, 2011) | $L_2$ distance between two mixtures | thin-plate spline or Gaussian radial basis functions |
| Non-rigid ICP (Amberg et al., 2007) | closest points, as in [ICP](/iterative-closest-point/) | affine map per vertex, stiffness lowered step by step |
| [As-rigid-as-possible](/as-rigid-as-possible-deformation/) registration | closest points | local rigidity of each patch |

Most methods alternate between a correspondence step and a deformation step with the correspondences fixed, which is then a regularized least squares problem. Tam et al. (2013) survey these methods for point clouds and meshes.

## Bounds

- **Without a regularizer the problem is trivial.** As the second example shows, for any $X$ and $Y$ and for the common discrepancies, a map of cost 0 exists. So all lower bounds and guarantees depend on the regularizer.
- **Not convex.** With unknown correspondences, the cost is not convex in $T$, even for linear classes of maps such as affine maps, because the discrepancy takes a minimum or a sum over the possible partners. The methods above find local minima. Annealing, as in RPM, or a large starting variance, as in CPD, widens the basin but gives no guarantee.
- **Cost per step.** The dense soft methods compute an $m \times n$ matrix in each step, so each step takes $\Theta(m n)$ time. CPD solves an $m \times m$ linear system for the Gaussian map, which costs $O(m^3)$ by a direct method; Myronenko and Song use the fast Gauss transform and a low-rank approximation of the kernel matrix to bring a step close to linear time in $m + n$.
- **Closest point methods.** With a [k-d tree](/kd-tree/) on $X$, the correspondence step of non-rigid ICP takes about $O(m \log n)$ time on well spread points, and the deformation step is a sparse linear system.

## Reductions

- **Rigid registration is a special case.** If $\mathcal{T}$ holds only rigid motions, or if the regularizer is 0 on rigid motions and infinite on all other maps, the problem is rigid [point cloud registration](/point-cloud-registration/).
- **Known correspondences reduce it to regression.** With the pairs fixed and the discrepancy a weighted sum of squared distances, a thin-plate spline or a Gaussian kernel map with a quadratic regularizer is found by one linear system, as in [radial basis function interpolation](/radial-basis-function-interpolation/) and in kernel ridge regression with the [kernel trick](/kernel-trick/).
- **Alternation.** RPM and CPD turn the problem into a sequence of such regressions with soft weights, one per step of softassign or of EM.
- **The correspondence part is an assignment problem.** For a fixed map and a one-to-one match, the best correspondence is an [assignment problem](/assignment-problem/), solved by the [Hungarian algorithm](/hungarian-algorithm/). If the regularizer depends on pairs of matches, such as the change of the distance between two points, the match becomes a [quadratic assignment problem](/quadratic-assignment-problem/), which is NP-hard in general.

## Applications

- **Medical imaging.** Register organs or anatomical landmarks between patients, between times, or between a scan and an atlas.
- **Faces and bodies.** Fit a template mesh to scans, to build statistical shape models and to transfer animation.
- **Shape analysis.** Find the correspondence between two shapes of the same class, and measure how they differ.
- **Tracking.** Follow deforming objects, such as cloth or soft tissue, in a sequence of depth scans.
- **Biology.** Align cells, nuclei or neurons between samples and between times.

## References
