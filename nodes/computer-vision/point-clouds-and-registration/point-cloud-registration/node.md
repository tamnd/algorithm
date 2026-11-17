---
tag: AQNFQ0
kind: problem
slug: point-cloud-registration
name: Point cloud registration
aliases:
- point set registration
- scan matching
- scan alignment
area: computer-vision/point-clouds-and-registration
level: core
summary: "Find the transformation, often a rigid motion, that best aligns one point cloud to another when the point correspondences are not known."
prereqs: [point-cloud]
see_also: [iterative-closest-point, go-icp, teaser-registration, fast-global-registration, coherent-point-drift, non-rigid-registration, normal-distributions-transform, correlative-scan-matching]
sources:
  - paper: doi:10.1109/34.121791
    title: "Paul J. Besl and Neil D. McKay, A method for registration of 3-D shapes, IEEE Transactions on Pattern Analysis and Machine Intelligence 14(2), 1992, 239-256"
    locator: "The statement of rigid registration with unknown correspondences and the ICP algorithm"
  - paper: doi:10.1109/34.88573
    title: "Shinji Umeyama, Least-squares estimation of transformation parameters between two point patterns, IEEE Transactions on Pattern Analysis and Machine Intelligence 13(4), 1991, 376-380"
    locator: "The closed form least squares rotation, translation and scale when the correspondences are known"
  - paper: doi:10.1109/TPAMI.2015.2513405
    title: "Jiaolong Yang, Hongdong Li, Dylan Campbell and Yunde Jia, Go-ICP: A globally optimal solution to 3D ICP point-set registration, IEEE Transactions on Pattern Analysis and Machine Intelligence 38(11), 2016, 2241-2254"
    locator: "The global minimization of the ICP cost over all rigid motions by branch and bound"
  - paper: doi:10.1109/TPAMI.2010.46
    title: "Andriy Myronenko and Xubo Song, Point set registration: Coherent point drift, IEEE Transactions on Pattern Analysis and Machine Intelligence 32(12), 2010, 2262-2275"
    locator: "The probabilistic form of the problem, with rigid, affine and non-rigid transformations"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 13.2.1, Range data merging (ICP and its variants)"
---

Point cloud registration is the problem of finding the transformation that best aligns a source [point cloud](/point-cloud/) to a target point cloud of the same scene, when it is not known which source point corresponds to which target point. The transformation is usually a rigid motion, a rotation and a translation, but it can also be a similarity, an affine map or a smooth deformation. This page states the general problem and compares the methods. [Iterative closest point](/iterative-closest-point/) and its variants refine a pose from a start; [Go-ICP](/go-icp/) searches all poses with a proof of optimality; feature-based methods such as [TEASER](/teaser-registration/) and [fast global registration](/fast-global-registration/) need no start pose. [Real-time correlative scan matching](/correlative-scan-matching/) is one method for a special case from robotics: it aligns a 2D laser scan to a map by a search over a grid of poses on a rasterized likelihood table. When the correspondences are known, the problem becomes [optimal superposition](/optimal-superposition/), which has a closed-form solution.

## In plain words

Two scans of the same object are taken from different places. Each scan is a set of 3D points in the coordinates of its own sensor. To combine them, we must find how to turn and slide one scan so that it lies on top of the other.

The hard part is that we do not know which point in one scan is the same physical spot as which point in the other. The two scans also see different parts of the object and have noise. So registration has to find the pairs and the motion together.

## Definition

**Input.** A source point set $P = (p_1, \ldots, p_n)$ and a target point set $Q = \{q_1, \ldots, q_m\}$ in $\mathbb{R}^3$ (or $\mathbb{R}^2$), sometimes with normals, colors or other attributes per point. A class $\mathcal{T}$ of transformations, by default the rigid motions $x \mapsto R x + t$ with $R \in SO(3)$ and $t \in \mathbb{R}^3$ (the [special Euclidean group](/special-euclidean-group/)). A cost that measures how badly a transformed source fits the target.

**Output.** A transformation $T \in \mathcal{T}$ of least cost, or a good one when the least cost is too expensive to find.

The usual cost is the sum of squared distances from each transformed source point to its closest target point,

$$E(T) = \sum_{i=1}^n \min_j |T(p_i) - q_j|^2 .$$

Other costs replace the squared distance by the distance to the tangent plane of the target ([point-to-plane ICP](/point-to-plane-icp/)), by a Mahalanobis distance ([generalized ICP](/generalized-icp/)), by a robust function of the distance, or by a sum over only part of the points ([trimmed ICP](/trimmed-icp/)). Probabilistic forms model the target as a Gaussian mixture ([coherent point drift](/coherent-point-drift/)) or as Gaussians per voxel (the [normal distributions transform](/normal-distributions-transform/)) and maximize a likelihood.

## Variants

- **Rigid, similarity and affine.** The class $\mathcal{T}$ can add a global scale (Umeyama 1991) or allow any affine map.
- **Non-rigid.** [Non-rigid registration](/non-rigid-registration/) finds a deformation with a regularizer for smoothness, for example for faces or bodies.
- **Partial overlap and outliers.** Only part of each cloud has a partner in the other. Trimmed costs, robust costs and rejection of far pairs handle this.
- **Many clouds.** Registration of many scans at once spreads the error over all of them; it leads to [pose graph optimization](/pose-graph-optimization/) and [bundle adjustment](/bundle-adjustment/).
- **2D scans to maps.** In robotics, a 2D laser scan is aligned to a map or to the previous scan, for example by [real-time correlative scan matching](/correlative-scan-matching/) or the normal distributions transform.

## Known algorithms

| Method | Needs a start pose | Guarantee | Notes |
|---|---|---|---|
| [ICP](/iterative-closest-point/) | yes | cost never rises; a fixed point | the standard refinement step |
| [Point-to-plane ICP](/point-to-plane-icp/) | yes | local; fast near a solution | needs target normals |
| [Generalized ICP](/generalized-icp/) | yes | local | covariance per point |
| [Trimmed ICP](/trimmed-icp/) | yes | trimmed cost never rises | partial overlap |
| [Normal distributions transform](/normal-distributions-transform/) | yes | local | Gaussians per voxel, no closest points |
| [Coherent point drift](/coherent-point-drift/) | yes, but a wide basin | local (EM) | also non-rigid |
| [Go-ICP](/go-icp/) | no | within $\epsilon$ of the global minimum | slow; small clouds |
| [RANSAC](/ransac/) on feature matches | no | probabilistic | descriptors such as [FPFH](/point-feature-histograms/) |
| [4PCS](/four-points-congruent-sets/) | no | probabilistic | four-point bases, no descriptors |
| [Fast global registration](/fast-global-registration/) | no | local in a robust cost | feature matches, no closest points |
| [TEASER](/teaser-registration/) | no | certifiable under its noise model | many outliers |

A common pipeline uses two stages. A global method, usually feature matching with [RANSAC](/ransac/), gives a coarse pose, and ICP or one of its variants refines it. The [taxonomy of ICP variants](/icp-variants-taxonomy/) lists the choices inside the refinement step.

## Bounds

What is known about the solutions:

- **Known pairs.** If the pairs $(p_i, q_{c(i)})$ are given, the least squares rigid motion has a closed form by the SVD ([Kabsch algorithm](/kabsch-algorithm/)) or by a unit quaternion ([quaternion superposition](/quaternion-superposition/)), in $\Theta(n)$ time. Umeyama (1991) adds the scale and the sign fix that keeps a proper rotation.
- **A minimum exists.** For the rigid cost $E$ above with finite $Q$, $E$ is continuous and grows without bound as $|t|$ grows, and $SO(3)$ is compact, so a least cost motion exists.
- **It need not be unique.** A symmetric shape, such as a cube, has many motions of the same cost. A plane, a sphere or a long cylinder leaves directions of motion that the points do not fix at all.
- **The cost is not convex.** $E$ has many local minima in the rotation, and it is not differentiable where a closest point changes. So local methods such as ICP find the global minimum only from a good start (see the [ICP convergence theorem](/icp-convergence-theorem/)).
- **Global search is possible but slow.** [Go-ICP](/go-icp/) finds a motion within a given gap $\epsilon$ of the global minimum by branch and bound, but its time grows quickly as $\epsilon$ falls and as the clouds grow.
- **Exact copies are easy.** If the source is an exact rigid copy of the target, with the same number of points, testing this and finding the motion is a problem of exact congruence, which algorithms of computational geometry solve in $O(n \log n)$ time in 3D. Noise, partial overlap and different sampling, which real scans always have, make this result inapplicable.

## Applications

- Merging range scans into one model, before [surface reconstruction](/surface-reconstruction/).
- Odometry and mapping for robots and cars with lidar.
- Tracking of a depth camera, as in KinectFusion, which aligns each depth frame to a model by point-to-plane ICP.
- Inspection: alignment of a scanned part to its CAD model.
- Medical imaging: alignment of surfaces from different scans of a patient.

## References
