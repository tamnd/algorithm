---
tag: JSXC11
kind: algorithm
slug: global-structure-from-motion
name: Global structure from motion
aliases:
- global SfM
area: computer-vision/structure-from-motion
level: advanced
summary: Solve for all camera rotations at once by rotation averaging, then all positions by translation averaging, then triangulate and bundle adjust once.
solves: [structure-from-motion-problem]
model: real-ram
complexity:
  vars: {N: "the number of images", m: "the number of observations", E: "the number of edges of the view graph"}
  time: {total: "O(N m + N^3)"}
  space: {extra: "O(N^2 + m)"}
properties: {deterministic: false, iterative: true, local: true, recursive: false, monotone: false}
history:
  year: 2013
  people: [Venu Madhav Govindu, Daniel Martinec, Tomas Pajdla, Pierre Moulon, Kyle Wilson, Noah Snavely]
  note: Govindu (2001) and Martinec and Pajdla (2007) first solved for all motions at once from the pairwise ones. Robust rotation and translation averaging made the scheme practical around 2013 and 2014.
prereqs: [structure-from-motion-problem, rotation-averaging, translation-averaging, bundle-adjustment]
see_also: [incremental-structure-from-motion, lie-algebraic-rotation-averaging, view-graph, essential-matrix-decomposition, point-triangulation, sparse-bundle-adjustment, ransac, feature-track]
sources:
  - paper: doi:10.1109/CVPR.2001.990963
    title: "Venu Madhav Govindu, Combining two-view constraints for motion estimation, IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2001), vol. 2, 218-225"
    locator: "the whole paper (the global estimation of all rotations and translations from the pairwise motions)"
  - paper: doi:10.1109/CVPR.2007.383115
    title: "Daniel Martinec and Tomas Pajdla, Robust rotation and translation estimation in multiview reconstruction, IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2007), 1-8"
    locator: "the whole paper (the linear rotation step and the translation step on all cameras at once)"
  - paper: doi:10.1109/ICCV.2013.403
    title: "Pierre Moulon, Pascal Monasse and Renaud Marlet, Global fusion of relative motions for robust, accurate and scalable structure from motion, IEEE International Conference on Computer Vision (ICCV 2013), 3248-3255"
    locator: "the whole paper (the rejection of wrong rotations by cycles, robust rotation averaging and the translation step on triplets)"
  - paper: doi:10.1007/978-3-319-10578-9_5
    title: "Kyle Wilson and Noah Snavely, Robust global translations with 1DSfM, Computer Vision ECCV 2014, Lecture Notes in Computer Science, Springer, 2014, 61-75"
    locator: "the whole paper (the outlier filter for the directions and the translation step of a global pipeline)"
  - paper: doi:10.1109/ICCV.2013.70
    title: "Avishek Chatterjee and Venu Madhav Govindu, Efficient and robust large-scale rotation averaging, IEEE International Conference on Computer Vision (ICCV 2013), 521-528"
    locator: "the robust rotation averaging used as the first step"
  - paper: doi:10.1007/978-3-031-73661-2_4
    title: "Linfei Pan, Dániel Baráth, Marc Pollefeys and Johannes L. Schönberger, Global structure-from-motion revisited, Computer Vision ECCV 2024, Lecture Notes in Computer Science, Springer, 2024, 58-77"
    locator: "the whole paper (the joint estimation of cameras and points in place of a separate translation step)"
  - paper: doi:10.1017/S096249291700006X
    title: "Onur Özyeşil, Vladislav Voroninski, Ronen Basri and Amit Singer, A survey of structure from motion, Acta Numerica 26, 2017, 305-364"
    locator: "the sections on the global pipeline, rotation estimation and location estimation"
---

Global structure from motion solves the [structure from motion problem](/structure-from-motion-problem/) for calibrated cameras by estimating all cameras at once, instead of one at a time as [incremental structure from motion](/incremental-structure-from-motion/) does. It first estimates the relative pose of every image pair with enough matches, which gives the [view graph](/view-graph/). Then it splits the camera poses into two parts. [Rotation averaging](/rotation-averaging/) finds all absolute rotations from the relative rotations of the edges. With the rotations known, each relative translation gives the direction from one camera center to another, and [translation averaging](/translation-averaging/) finds all centers from these directions. Finally it [triangulates](/point-triangulation/) every track with the fixed cameras and runs one [bundle adjustment](/bundle-adjustment/). Each step treats all images the same way, so the errors spread evenly over the scene, and the method needs only a few large solves, which makes it much faster than the incremental method on large photo collections. The weak step is translation averaging, which is sensitive to wrong edges and to cameras on a line.

## In plain words

The incremental method builds the model one photo at a time. The global method looks at all photos together. First, for every pair of photos that overlap, it works out how the two cameras stand compared with each other. Then it answers the question in two parts. Which way does each camera point? It picks the directions that agree best with all the pairs at once. Where does each camera stand? With the directions known, each pair says in which direction one camera sees the other, and the method picks the positions that agree best with these directions. Last, it places the points in 3D and polishes everything once.

## The problem

**Input.** An intrinsic matrix $K$ shared by all images, the [feature tracks](/feature-track/) of $N$ images, a threshold $\tau$ on the reprojection error in pixels, a threshold $\alpha$ on the disagreement of a relative rotation, a minimum number of inliers per edge, and a random seed.

**Output.** A pose $(R_i, t_i)$ with $X_c = R_i X + t_i$ for each image of the largest connected part of the view graph, and a point $X_j$ for each track that could be triangulated. The first image has $R = I$ and $t = 0$, and the scale is arbitrary, set by the normalization of the centers.

**Conventions.** The relative pose of an edge $(i, j)$ is $X_j = R_{ij} X_i + t_{ij}$, so $R_{ij} = R_j R_i^{\mathsf T}$ and $t_{ij} = -R_j (c_j - c_i)$ for the centers $c_i = -R_i^{\mathsf T} t_i$. With known rotations, the unit direction from $c_i$ to $c_j$ is $v_{ij} = -R_j^{\mathsf T} t_{ij} / \|t_{ij}\|$.

## The algorithm

```pseudo id=main
GLOBAL-SFM(K, tracks, τ, α)
L1  for each image pair with enough common tracks: (R_ij, t_ij) <- RANSAC on the essential matrix; keep it as an edge if it has enough inliers
L2  R <- robust Lie-algebraic rotation averaging on the edges of the largest connected part (an L1 start, then Geman-McClure weights)
L3  remove each edge with angle(R_ij, R_j R_i^T) > α, and stop if the graph is no longer connected
L4  for each edge: v_ij <- -R_j^T t_ij / ||t_ij||
L5  c <- the eigenvector of the smallest eigenvalue of the matrix of Σ ||(I - v_ij v_ij^T)(c_j - c_i)||², with c_1 = 0 and the sign that makes Σ v_ij · (c_j - c_i) > 0
L6  for each image k: t_k <- -R_k c_k
L7  triangulate each track from its registered views; keep the views with error below 10 τ, refit once, keep it if 2 views remain
L8  bundle adjust all cameras and points with the first camera fixed
L9  drop observations with error above τ and points with fewer than 2 observations, then bundle adjust again
L10 return the cameras, the points and the kept observations
```

Line L1 builds the view graph with the [eight-point algorithm](/eight-point-algorithm/) inside [RANSAC](/ransac/) and the [essential matrix decomposition](/essential-matrix-decomposition/), as in the first step of the incremental method. Line L2 is [Lie-algebraic rotation averaging](/lie-algebraic-rotation-averaging/) from a breadth-first tree start, 30 iterations with $L_1$ weights and 30 with Geman-McClure weights. Line L3 removes the edges whose relative rotations disagree with the averaged ones, since these edges likely have wrong translations too. Line L5 is the linear form of translation averaging: the matrix is a block Laplacian of size $3(N - 1)$ after the row and column of $c_1$ are removed, and the constraint $\sum \|c_k\|^2 = 1$ makes the minimum an eigenvector. Line L7 uses a loose gate of $10 \tau$, because the cameras are not yet refined. Lines L8 and L9 use [Levenberg-Marquardt](/levenberg-marquardt/) with the points eliminated by the [Schur complement](/schur-complement/).

## Example

The reference test uses 5 cameras on a sphere of radius 3, all looking at the origin, with $f = 800$ px, and 40 points in a cube of size 2. Each point is seen by each camera with probability 0.8. Gaussian noise of 0.5 px is added, and 5% of the observations are replaced by random pixels. With $\tau = 3$ px and $\alpha = 0.1$ rad:

- There are 161 observations. Line L1 finds all 10 image pairs as edges, with 18 to 27 inliers each.
- Line L3 keeps all 10 edges.
- After line L9, the result has 5 cameras, 35 points and 134 kept observations. The largest reprojection error is 1.05 px and the root mean square error is 0.47 px.
- After the best similarity to the truth, the largest point error is 0.027 units, the largest center error is 0.0025 units, and the largest rotation error is 0.0019 rad.

A second test shows the edge filter. Six cameras form a complete graph with exact relative poses, and the relative rotation of the edge $(1, 4)$ is turned by an extra 0.5 rad. Robust averaging still finds all rotations within $2 \cdot 10^{-3}$ rad, and line L3 removes the edge $(1, 4)$ and only that edge. A third test shows why the graph needs loops: for 4 cameras on a path, the matrix of line L5 has 3 zero eigenvalues, so the centers are not fixed, and closing the path into a cycle leaves 1, the scale. These are benchmark results of the reference tests.

## Correctness

On exact data, the method returns the true cameras and points up to a similarity, if each image pair of the view graph satisfies the conditions of the eight-point method, the graph is parallel rigid for the true centers, and each track is seen from two centers that are not on one line with its point (theorem). The steps are: line L1 gives exact relative poses with $\|t_{ij}\| = 1$; the tree start of line L2 fits every edge exactly, so the reweighted iterations do not move it; line L3 keeps every edge; the directions of line L4 are exact; under parallel rigidity the matrix of line L5 has a one-dimensional null space that holds the true centers; and triangulation and bundle adjustment then change nothing. The proof below gives the details. Each bundle adjustment never raises its cost (theorem). With noise and outliers there is no guarantee: rotation averaging and bundle adjustment find local minima, and the linear translation step can pull cameras together (heuristic).

## Complexity

In the real RAM model, with a fixed cap on the RANSAC samples, line L1 costs $O(N m)$, because a track seen in $d$ images belongs to $d^2 / 2$ pairs and $\sum d^2 \le N m$. Line L2 costs $O(E + N^3)$ per iteration with the dense solve of the reference code, and it runs a fixed number of iterations. Line L5 needs one symmetric eigenvalue problem of size $3N$, $O(N^3)$ with a dense method. Line L7 costs $O(m)$. Each bundle adjustment iteration costs $O(N m + N^3)$, as on the incremental page, and the number of iterations is capped. With $E \le N^2$, the total is $O(N m + N^3)$, against $O(N^2 m + N^4)$ for the incremental method, which runs a bundle adjustment after each new image. Sparse solvers make the averaging steps close to linear in $E$. The space is $O(N^2)$ for the dense matrices plus $O(m)$ for the data.

## Properties

- **Randomized.** RANSAC in line L1 samples at random; the reference code fixes the seed.
- **Order free.** No step depends on the order of the images, so the errors spread over the whole scene and there is no drift along a sequence.
- **Fast.** It has only a few large solves and one or two bundle adjustments (benchmark result in the cited papers).
- **Fragile translations.** The quality depends on the translation step, which is sensitive to wrong directions, short baselines and collinear cameras.
- **Fewer images registered.** Images that are only weakly connected may be lost by the filters, while the incremental method can still add them by PnP.

## Variants and improvements

- **Cycle checks.** Moulon, Monasse and Marlet (2013) reject wrong relative rotations with cycles of length 3 before averaging, and estimate translations from triplets of cameras.
- **Robust translations.** 1DSfM (Wilson and Snavely, 2014) removes wrong directions by one-dimensional projections, and LUD and ShapeFit use convex robust costs.
- **Points in the translation step.** Using the tracks directly, as the constraints $x \times (R_i X + t_i) = 0$, avoids collinear degeneracies.
- **Joint positioning.** GLOMAP (Pan, Baráth, Pollefeys and Schönberger, 2024) replaces the separate translation step by one robust estimation of camera centers and points together, with accuracy close to the incremental method on their benchmarks (benchmark result of the authors).
- **Hybrid methods.** Use global rotations with incremental registration of the centers, or merge incremental models with global averaging.

## When to use it

Use it for large unordered photo collections when speed matters and the view graph is dense, with many loops. Use it when the images have no natural order and drift is a concern. If the view graph is sparse, close to a chain, or the cameras move along a line, as in a video from a car, the translation step is weak; use [incremental structure from motion](/incremental-structure-from-motion/) or [visual odometry](/visual-odometry/) there.

## Pitfalls

- **Wrong edges.** Repetitive structures give wrong pairs that agree with each other. Robust losses and cycle checks reduce the risk but cannot remove it.
- **Collinear cameras.** If the cameras move along a line, the directions say nothing about the spacing along the line, and the linear step returns a poor answer.
- **Clustering.** The linear cost favors short distances, so the minimum can pull groups of cameras together. Use a robust or scale-aware cost, or the points.
- **Disconnected filters.** Removing edges can break the graph into parts, and a connected graph can still fail to be parallel rigid. Take the largest parallel rigid part. The reference code only checks connectivity and raises an error if it fails.
- **Sign of the directions.** The linear cost does not see the sign of $v_{ij}$, so the solution must be oriented, as line L5 does.

## Implementations

## History

Govindu (2001) proposed to combine the relative motions of all image pairs into consistent global motions by averaging, first the rotations and then the translations. Martinec and Pajdla (2007) built a full pipeline with linear rotation averaging and a robust translation step on all cameras. Around 2013 and 2014, robust rotation averaging (Chatterjee and Govindu), the global fusion of relative motions (Moulon, Monasse and Marlet) and robust translations by 1DSfM (Wilson and Snavely) made global SfM competitive on large Internet collections. The Acta Numerica survey of Özyeşil, Voroninski, Basri and Singer (2017) reviews the theory. GLOMAP (Pan, Baráth, Pollefeys and Schönberger, 2024) closed much of the accuracy gap with the incremental method.

## References
