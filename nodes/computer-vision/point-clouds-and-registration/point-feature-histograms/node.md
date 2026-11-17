---
tag: 4N5YX7
kind: algorithm
slug: point-feature-histograms
name: Fast point feature histograms
aliases:
- FPFH
- PFH
- point feature histograms
area: computer-vision/point-clouds-and-registration
level: core
summary: Describe a point by histograms of angles between its normal and its neighbors' normals in a Darboux frame, made fast by reusing per-point partial histograms.
model: real-ram
complexity:
  vars: {n: the number of points, k: the number of neighbors per point}
  time: {worst: O(n^2), average: O(n (log n + k)), best: Ω(n k)}
  space: {extra: Θ(n k)}
properties: {deterministic: true, exact: true, online: false, recursive: false, rigid_motion_invariant: true, needs_normals: true}
history:
  year: 2009
  people: [Radu Bogdan Rusu, Nico Blodow, Michael Beetz]
  note: "Rusu and his coauthors described points by histograms of angle features of point pairs (PFH) in 2008, and in 2009 made the descriptor fast (FPFH) by histogramming only the pairs of a point with its neighbors and adding the neighbors' histograms with weights."
prereqs: [point-cloud-normal-estimation, nearest-neighbor-search]
see_also: [shot-descriptor, spin-images, shape-context, feature-matching, fast-global-registration, teaser-registration, point-cloud-registration, iterative-closest-point]
sources:
  - paper: doi:10.1109/ROBOT.2009.5152473
    title: "Radu Bogdan Rusu, Nico Blodow and Michael Beetz, Fast point feature histograms (FPFH) for 3D registration, IEEE International Conference on Robotics and Automation 2009, 3212-3217"
    locator: "The Darboux frame and the angle features of a point pair, the simplified point feature histogram SPFH, and the FPFH as the SPFH of the point plus the distance weighted SPFH of its neighbors"
  - paper: "Radu Bogdan Rusu, Nico Blodow, Zoltan Csaba Marton and Michael Beetz, Aligning point cloud views using persistent feature histograms, IEEE/RSJ International Conference on Intelligent Robots and Systems 2008"
    locator: "The point feature histogram over all pairs of a neighborhood, and the selection of persistent features over several radii"
---

Fast point feature histograms (FPFH) describe the shape of a point cloud around one point by a short vector of numbers, for matching points between two scans. For two points with normals, three angles describe how one normal is turned relative to the other and to the line between the points, in a frame fixed at one of them, the Darboux frame. The angles do not change when the cloud is moved or rotated. The point feature histogram (PFH) counts these angles over all pairs of points in a neighborhood, which costs $O(k^2)$ pairs for $k$ neighbors. FPFH, by Rusu, Blodow and Beetz (2009), counts only the pairs of the point with its own neighbors, a simplified histogram, and adds the simplified histograms of the neighbors with weights, which costs $O(k)$ pairs per point. The result is a 33-value descriptor with three 11-bin parts, one per angle. It needs [normals](/point-cloud-normal-estimation/), and it is a standard descriptor for the coarse alignment of scans, as in [fast global registration](/fast-global-registration/).

## In plain words

Take a point and the points near it, each with a short arrow that sticks out of the surface. For two of them, ask how the second arrow is tilted, seen from the first one and the line between them. Three angles answer this, and they stay the same however the object is turned.

On a flat part all arrows are the same, so all angles are zero. On a ball, a pipe, an edge or a corner the angles take other typical values. Count how often each angle falls in each of a few ranges. The counts are the description of the point.

Counting all pairs of near points is slow. The fast version counts only the pairs that include the point itself, then adds in the counts of its neighbors, with more weight for the closer ones.

## The problem

The input is a cloud of $n$ points with unit normals, a radius $r$ and a number of bins $b$. For each point $p_i$ the output is a vector $F_i$ of $3b$ numbers, in three parts that each sum to 1, so that points on surfaces of the same local shape get close vectors, and the vector does not change when the cloud is moved by a rotation and a translation. Point descriptors have no single correct output; the requirement is that the descriptor is invariant, cheap, and discriminative for the matching that follows.

## The algorithm

The pair features first. For two points with normals:

```pseudo id=pair
PAIR-FEATURES(p_a, n_a, p_b, n_b)
P1  d ← (p_b - p_a) / ‖p_b - p_a‖
P2  if |n_b · d| > |n_a · d| then swap a and b, and set d ← -d
P3  u ← n_a; v ← (u × d) / ‖u × d‖; w ← u × v
P4  α ← v · n_b; φ ← u · d; θ ← atan2(w · n_b, u · n_b)
P5  return (α, φ, θ, ‖p_b - p_a‖)
```

Line P2 picks as the source the point whose normal makes the smaller angle with the line of the pair, so the result does not depend on the order of the two points. Line P3 builds the Darboux frame: $u$ is the source normal, $v$ is orthogonal to both the normal and the line, and $w$ completes the frame. Line P4 reads off $\phi$, the cosine of the angle between the normal and the line; $\alpha$, how far the target normal leans out of the plane of $u$ and the line; and $\theta$, the turn of the target normal in that plane. The values lie in $[-1, 1]$, $[-1, 1]$ and $[-\pi, \pi]$.

Then the descriptor:

```pseudo id=main
FPFH(P, N, r, b)
L1  for each point p_i of P do
L2      K_i ← the points of P within distance r of p_i, other than p_i
L3      for each p_j in K_i do
L4          (α, φ, θ) ← PAIR-FEATURES(p_i, n_i, p_j, n_j)
L5          add 1 to the bin of α, of φ and of θ in the three b-bin parts of SPFH(p_i)
L6      scale each part of SPFH(p_i) to sum 1
L7  for each point p_i of P do
L8      F_i ← SPFH(p_i) + (1/|K_i|) Σ_{p_j ∈ K_i} SPFH(p_j) / ‖p_j - p_i‖
L9      scale each part of F_i to sum 1
L10 return F
```

Lines L1 to L6 compute the simplified point feature histogram (SPFH) of every point, from its own $k$ pairs. Line L8 is the FPFH formula of the 2009 paper: the point's own SPFH plus the mean of the neighbors' SPFHs, each divided by its distance, so near neighbors count more. Line L9 is a common last step. The usual choice is $b = 11$, for 33 values. The PFH counts the pairs among all points of $\{p_i\} \cup K_i$, with the three features binned jointly, $b^3$ bins; with $b = 5$ this is 125 values.

## Example

A pair: $p_a = (0, 0, 0)$ with $n_a = (0, 0, 1)$, and $p_b = (1, 0, 0)$ with $n_b = (0.6, 0, 0.8)$, a normal tilted by 36.87°.

| step | value |
|---|---|
| P1: $d$ | $(1, 0, 0)$ |
| P2: $\lvert n_a \cdot d \rvert$, $\lvert n_b \cdot d \rvert$ | 0 and 0.6, so $b$ becomes the source and $d = (-1, 0, 0)$ |
| P3: $u$ | $(0.6, 0, 0.8)$ |
| P3: $u \times d$ | $(0, -0.8, 0)$, so $v = (0, -1, 0)$ |
| P3: $w = u \times v$ | $(0.8, 0, -0.6)$ |
| P4: $\alpha = v \cdot (0, 0, 1)$ | 0 |
| P4: $\phi = u \cdot d$ | $-0.6$ |
| P4: $\theta = \operatorname{atan2}(-0.6, 0.8)$ | $-0.6435$, that is $-36.87°$ |

The two normals and the line lie in the $xz$ plane, so $\alpha = 0$, and $\theta$ is the angle between the normals. Given in the other order, the pair gives the same three numbers.

On a plane, every normal is the same and orthogonal to every line of a pair, so every pair gives $\alpha = \phi = \theta = 0$. With 11 bins, all the mass of each part falls in the middle bin, bin 5, and the FPFH of every point of a plane is the same: 1 in bins 5, 16 and 27 and 0 elsewhere. On a sphere, the two normals and the line of a pair lie in one plane through the center, so again $\alpha = 0$, but $\phi$ and $\theta$ move away from 0 as the curvature grows. On a cylinder, $\alpha$ is not 0 for most pairs. This is how the three parts tell surfaces apart.

## Correctness

The frame of line P3 is right handed and orthonormal whenever the source normal is not along the line of the pair. In this frame, the line is $\phi u - \sqrt{1 - \phi^2}\, w$ and the target normal is $\alpha v + \sqrt{1 - \alpha^2} (\cos\theta\, u + \sin\theta\, w)$. So the four numbers $(\alpha, \phi, \theta, \lVert p_b - p_a \rVert)$ fix the pair of oriented points up to a rotation and a translation, and two pairs have the same four numbers exactly when a rigid motion maps one onto the other. The rule of line P2 makes the features independent of the order of the pair, except when both normals make the same angle with the line. A rigid motion keeps all distances and all features, so the neighbor sets, the bins and the weights stay the same, and so does every histogram, up to rounding at bin borders. FPFH counts the pairs of $p_i$ with its neighbors and the pairs of each neighbor with its own neighbors: it misses pairs of two neighbors that are not neighbors of each other and adds pairs that reach out to $2r$. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/), with $n$ points and $k$ neighbors per point.

- **Neighbor search.** Brute force costs $\Theta(n)$ per point, $\Theta(n^2)$ in total. A [k-d tree](/kd-tree/) on well-spread points costs $O(\log n + k)$ per radius query on average.
- **SPFH.** Lines L3 to L6 cost $O(k + b)$ per point.
- **FPFH.** Line L8 costs $O(k b)$ per point, which is $O(k)$ for a fixed $b$.
- **PFH.** All pairs of a neighborhood cost $O(k^2)$ per point, $O(n k^2)$ in total.
- **Space.** $\Theta(n k)$ for the neighbor lists and $\Theta(n b)$ for the histograms.

The total for FPFH is $O(n^2)$ with brute force and $O(n (\log n + k))$ with a tree, against $O(n k^2)$ for the PFH. With $k$ around 50, the pair count per point drops from about 1250 to 50.

## Properties

- **Rigid motion invariant.** Rotations and translations of the cloud do not change the descriptor.
- **Sensitive to normal signs.** The features use the normals with their signs, so flipping one normal changes the features of its pairs. Orient the normals, at least by a viewpoint, for repeatable results.
- **Depends on the density.** The weights of line L8 and the counts depend on the sampling. Downsample to an even density first, for example with a [voxel grid](/voxel-grid-downsampling/).
- **Scale dependent.** The radius $r$ fixes the scale of the shape that the descriptor sees.
- **Low dimension.** 33 values make matching with a [k-d tree](/kd-tree/) cheap.

## Variants and improvements

- **PFH.** The full histogram over all pairs, binned jointly. It is more descriptive and $O(k)$ times slower. The 2008 work also used the distance as a fourth feature and kept only the persistent points, whose histograms stand out from the mean at several radii.
- **Distance weights.** Implementations differ in the weight of line L8, for example the inverse of the distance or of its square, and in the scaling of the parts.
- **Color and other channels.** Extra parts for color or intensity differences of the pairs.
- **Viewpoint feature histogram.** A global descriptor for a whole object, built from the same angles between each point and the center, plus the viewing direction.
- **SHOT and spin images.** [SHOT](/shot-descriptor/) bins normal angles in a spherical grid around a local reference frame, and [spin images](/spin-images/) bin point positions around one normal. Both are common alternatives.
- **Learned descriptors.** Networks trained on scans give more discriminative descriptors at a higher cost.

## When to use it

Use FPFH for the coarse alignment of two scans: compute it on a downsampled cloud, match descriptors by nearest neighbors with a [ratio or mutual test](/feature-matching/), and pass the matches to a robust estimator such as [RANSAC](/ransac/), [fast global registration](/fast-global-registration/) or [TEASER](/teaser-registration/). Then refine with [ICP](/iterative-closest-point/). It is a good default when the scans are clean, the normals are reliable and speed matters. For noisy or cluttered scenes, SHOT is often more discriminative; for clouds without normals, use a descriptor that needs none.

## Pitfalls

- **v not normalized.** At line P3, $u \times d$ has length $\sqrt{1 - \phi^2}$, not 1. Without the division, $\alpha$ shrinks for pairs with large $|\phi|$ and the frame is not orthonormal.
- **No source rule.** Without line P2, the features of a pair depend on which point comes first, and the SPFH of $p_i$ is not consistent with the SPFH of $p_j$.
- **Degenerate pairs.** When the source normal lies along the line of the pair, line P3 has no frame. Skip the pair, as the code does, and do not divide by zero.
- **Duplicate points.** A point at distance 0 from $p_i$ gives an infinite weight at line L8. Remove duplicates first.
- **A radius for normals equal to the radius for features.** The normals of line L4 should come from a smaller neighborhood than $r$ at line L2; otherwise the features see almost the same normals for all pairs and lose detail.
- **Empty neighborhoods.** A point with no neighbor within $r$ gets an all-zero vector at line L9. Treat such points as having no descriptor.

## Implementations

## History

Rusu, Blodow, Marton and Beetz (2008) introduced point feature histograms for aligning point cloud views: angle features of all point pairs in a neighborhood, computed in a Darboux frame, binned into one histogram, together with a test that kept only the persistent features. The cost of $O(k^2)$ pairs per point made the method slow for dense clouds. Rusu, Blodow and Beetz (2009) proposed the fast version: the simplified histogram of the pairs of a point with its own neighbors, and the weighted sum of these histograms over the neighbors, which brings the cost down to $O(k)$ pairs per point. They used it for the initial alignment of scans with a sample consensus method. Both descriptors are part of the Point Cloud Library, and FPFH became the usual baseline for 3D local descriptors.

## References
