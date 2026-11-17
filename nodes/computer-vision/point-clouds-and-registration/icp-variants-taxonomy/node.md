---
tag: 8V9XQH
kind: concept
slug: icp-variants-taxonomy
name: Efficient variants of ICP
aliases:
- Rusinkiewicz-Levoy ICP taxonomy
area: computer-vision/point-clouds-and-registration
level: advanced
summary: "The six stages of ICP (selection, matching, weighting, rejection, error metric, minimization) and the choices at each, which trade speed per iteration against convergence and robustness."
prereqs: [iterative-closest-point]
see_also: [point-to-plane-icp, trimmed-icp, generalized-icp, kd-tree, voxel-grid-downsampling, range-image, m-estimator, point-cloud-registration]
sources:
  - paper: doi:10.1109/IM.2001.924423
    title: "Szymon Rusinkiewicz and Marc Levoy, Efficient variants of the ICP algorithm, Proceedings of the Third International Conference on 3-D Digital Imaging and Modeling (3DIM), 2001, 145-152"
    locator: "The division of ICP into stages, the comparison of the choices at each stage, normal-space sampling, projection-based matching, and the combined high-speed variant"
  - paper: doi:10.1109/34.121791
    title: "Paul J. Besl and Neil D. McKay, A method for registration of 3-D shapes, IEEE Transactions on Pattern Analysis and Machine Intelligence 14(2), 1992, 239-256"
    locator: "The original ICP: all points, closest-point matching, point-to-point error and the closed-form minimization"
  - paper: doi:10.1016/0262-8856(92)90066-C
    title: "Yang Chen and Gérard Medioni, Object modelling by registration of multiple range images, Image and Vision Computing 10(3), 1992, 145-155"
    locator: "The point-to-plane error metric"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 13.2.1, Range data merging (ICP and its variants)"
---

The taxonomy of Rusinkiewicz and Levoy (2001) splits [iterative closest point](/iterative-closest-point/) (ICP) into six stages and treats each stage as a choice: which points to select, how to match them, how to weight the pairs, which pairs to reject, which error metric to use, and how to minimize it. Most ICP variants change only one or two of these stages, so the taxonomy is a map of the variants. Rusinkiewicz and Levoy compared the choices at each stage on test meshes, proposed normal-space sampling for the selection stage, and combined the fastest choices into a variant that aligns two range images in a few tens of milliseconds on the hardware of 2001. This page explains the stages and where the other ICP pages fit in them.

## In plain words

ICP is a loop: pick some points, find their partners, decide how much each pair counts, throw away bad pairs, measure how far apart the pairs are, and move the cloud to make that measure smaller.

Each of these six steps can be done in several ways. Some ways make one round of the loop cheap. Some ways make the loop need fewer rounds. Some ways make the loop safe against bad data. A good ICP picks one way for each step so that the whole loop is fast and safe for the data at hand.

## The idea

One iteration of ICP has these stages. The choices listed are those of the paper and of common practice.

1. **Selection.** Which source points (or points of both clouds) take part. Choices: all points; a uniform subsample; a new random sample in each iteration; points with a high intensity gradient; and **normal-space sampling**, which picks points so that their normals spread as evenly as possible over the sphere of directions. Normal-space sampling keeps the few points on small features, such as grooves on a flat surface, that fix the motion along the surface; uniform sampling can miss them.
2. **Matching.** Which target point each selected point pairs with. Choices: the closest point, found with a [k-d tree](/kd-tree/); normal shooting, the intersection of the line along the source normal with the target surface; and **projection**, which projects the source point into the [range image](/range-image/) of the target and takes the point in that pixel. Projection costs $O(1)$ per point but gives worse pairs, so it needs more iterations; the paper found it the fastest overall when combined with point-to-plane.
3. **Weighting.** How much each pair counts. Choices: equal weights; weights that fall with the distance of the pair; weights from the agreement of the normals; and weights from the noise model of the scanner. A robust [M-estimator](/m-estimator/) is a weighting rule.
4. **Rejection.** Which pairs to drop. Choices: pairs farther apart than a fixed distance; the worst fixed fraction of pairs, as in [trimmed ICP](/trimmed-icp/); pairs farther than a multiple of the standard deviation of the distances; pairs that do not agree with their neighbors; and pairs with a point on the boundary of a mesh. Boundary rejection matters for scans that overlap in part, since points beyond the overlap otherwise all match the edge of the other scan.
5. **Error metric.** What distance the fit sums. Choices: the squared point-to-point distance of [ICP](/iterative-closest-point/); the squared point-to-plane distance of [point-to-plane ICP](/point-to-plane-icp/); and distances that add color. [Generalized ICP](/generalized-icp/) later added a metric with a covariance for each point.
6. **Minimization.** How the pose is found for the chosen metric. Choices: the closed form for point-to-point pairs; a linearized least squares step for point-to-plane pairs; extrapolation of the pose sequence, as in Besl and McKay; and stochastic search.

The paper measured the speed of convergence of each choice with the other stages fixed. Its main findings were these. Point-to-plane converged in far fewer iterations than point-to-point. Normal-space sampling helped on scenes where a few small features fix the alignment. Projection-based matching gave the fastest total time, because each iteration was cheap. Weighting and rejection had small effects on the speed of convergence in its tests; their main role is robustness to noise and outliers. These are results on the test meshes and machines of 2001, not general laws.

## Examples

- **The original ICP.** Besl and McKay (1992): all points, closest point, equal weights, no rejection, point-to-point, closed form with extrapolation.
- **Chen and Medioni.** Selected points, normal shooting, point-to-plane, linearized least squares (see [point-to-plane ICP](/point-to-plane-icp/)).
- **The fast variant of the paper.** Random sampling, projection-based matching, equal weights, rejection of far pairs, point-to-plane, linearized least squares.
- **Real-time depth tracking.** KinectFusion (Newcombe et al., 2011) uses projection matching on depth images, rejection by distance and normal angle, and point-to-plane, close to the fast variant.
- **Partial overlap.** [Trimmed ICP](/trimmed-icp/) changes only the rejection stage: it keeps the fraction $\xi$ of pairs with the least distances.
- **Lidar clouds.** [Voxel grid downsampling](/voxel-grid-downsampling/) for selection, a k-d tree for matching, distance rejection, and point-to-plane or generalized ICP.

## Where it is used

- **Design of an ICP.** The six stages are a checklist: for each, choose the cheapest option that the data allows, then test.
- **Comparison of variants.** A new variant is easiest to understand by the stages it changes. Benchmarks of ICP often fix five stages and vary one.
- **Software.** Libraries for point clouds build ICP from parts that follow these stages, so that the user can swap the sampler, the matcher, the rejectors and the error metric.
- **Limits.** The taxonomy is about local refinement. It does not cover the start pose; for that, see the global methods on the [point cloud registration](/point-cloud-registration/) page.

## References
