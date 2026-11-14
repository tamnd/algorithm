---
tag: WRAPDK
kind: algorithm
slug: shape-diameter-function
name: Shape diameter function
aliases:
- Shapira-Shamir-Cohen-Or segmentation
area: cad/mesh-processing
level: advanced
summary: Shapira, Shamir and Cohen-Or's local thickness measure from rays cast inward in a cone, used to segment meshes into parts that stay stable under pose changes.
model: real-ram
complexity:
  vars: {F: the number of faces, r: the number of rays for each face}
  time: {worst: O(r F^2)}
  space: {extra: Θ(r)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2008
  people: [Lior Shapira, Ariel Shamir, Daniel Cohen-Or]
  note: They measured the thickness of a mesh at each face with a cone of rays cast inward, and used it to cut meshes into parts that are the same in different poses, and to build skeletons.
prereqs: [moller-trumbore, ray-casting, polygon-mesh]
see_also: [mesh-segmentation, medial-axis, gaussian-mixture-model, expectation-maximization, alpha-expansion, bounding-volume-hierarchy, watertight-ray-triangle-intersection, variational-shape-approximation]
sources:
  - paper: doi:10.1007/s00371-007-0197-5
    title: Lior Shapira, Ariel Shamir and Daniel Cohen-Or, Consistent mesh partitioning and skeletonisation using the shape diameter function, The Visual Computer 24(4), 2008, 249 to 259
    locator: the definition of the shape diameter function, the cone of rays and the removal of outliers, the normalization, the soft clustering with a Gaussian mixture and the hard clustering with graph cuts, and the use of the function for skeletons
  - paper: doi:10.1080/10867651.1997.10487468
    title: Tomas Möller and Ben Trumbore, Fast, minimum storage ray-triangle intersection, Journal of Graphics Tools 2(1), 1997, 21 to 28
    locator: the ray-triangle test that solves for the distance and the barycentric coordinates with triple products, without the plane equation
  - paper: doi:10.1109/34.969114
    title: Yuri Boykov, Olga Veksler and Ramin Zabih, Fast approximate energy minimization via graph cuts, IEEE Transactions on Pattern Analysis and Machine Intelligence 23(11), 2001, 1222 to 1239
    locator: the alpha-expansion move, the graph cut that computes the best move, and the bound on the energy of a local minimum for a metric smoothness term
---

The shape diameter function (SDF) gives each face of a closed triangle mesh a number that measures how thick the shape is at that face. From the centroid of the face, a few dozen rays go into the shape, inside a cone about the inward normal. Each ray stops where it leaves the shape on the other side. The lengths far from the median are dropped, and the mean of the rest is the SDF of the face. On a finger the value is small, on a torso it is large, and it changes little when an arm bends at the elbow, because the thickness of the arm does not change. Shapira, Shamir and Cohen-Or (2008) introduced the function and built a [mesh segmentation](/mesh-segmentation/) on it: cluster the values with a [Gaussian mixture](/gaussian-mixture-model/), then smooth the labels with a graph cut. The SDF is related to the [medial axis](/medial-axis/): it is meant to approximate the diameter of the largest ball inside the shape near the face, but it is computed from rays and needs no medial axis.

## In plain words

Stand inside a hollow statue, on the inner side of its skin, and look straight in. Measure how far it is to the skin on the other side. Do the same while looking a little to the left, to the right, up and down. Throw away the strange answers, and take the average of the rest. That number is the thickness of the statue at that spot.

In a thin part, such as a finger, all the answers are small. In a thick part, such as the body, they are large. When the statue raises its arm, the arm keeps its thickness, so the numbers on the arm stay almost the same.

Once every small piece of the skin has its number, the pieces with similar numbers are put in groups, and the groups become the parts: head, arms, legs, body.

## The problem

The input is a closed triangle mesh with outward normals, the boundary of a solid, and a face $f$ of it. The output is a positive number $\mathrm{SDF}(f)$ that measures the thickness of the solid near $f$, or nothing if no ray leaves the solid in a valid way. For a segmentation, the input also has a number $k$ of clusters, and the output is a label for each face.

There is no exact target value. For a slab of thickness $h$, a single ray along the normal gives $h$, and the cone of rays gives a fixed multiple of $h$. On other shapes the SDF is a measured quantity, and its use is to compare faces of the same mesh, or faces of meshes of the same object in different poses.

## The algorithm

```pseudo id=main
SDF(closed mesh with outward normals, face f, number of rays r, cone angle γ)
L1  o ← the centroid of f;  n ← the inward normal of f
L2  D ← n and r − 1 more directions in rings of 8 around n, at angles up to γ/2 from n
L3  for each direction d in D do
L4      (t, G) ← the smallest t > 0 with o + t d on a face other than f, and the faces G hit at that t
L5      if there is a hit and d · n_g > 0 for some g in G then append the length t |d| to ℓ
L6  m ← the median of ℓ;  s ← the standard deviation of ℓ
L7  K ← the lengths of ℓ with |ℓ_i − m| ≤ s
L8  return the mean of K, or nothing if ℓ is empty
```

Line L2 sets the cone. The CGAL implementation uses a cone with an opening of $120°$, so $\gamma / 2 = 60°$, and 25 rays by default. The code uses the axis and three rings of eight rays, at $20°$, $40°$ and $60°$. Line L4 is a [ray-triangle test](/moller-trumbore/) against every face. The code computes it with exact rational numbers: the coordinates, the centroid and the directions are turned into fractions, so the hit parameter $t$, the choice of the first face and the test of line L5 are decided without rounding. Only the length $t|d|$ is a float. Line L5 keeps a ray only if it leaves the solid at the first hit, that is if the ray goes in the direction of the outward normal of the face it hits. On a mesh with holes or with wrongly oriented faces, a ray can leave through a hole (no hit) or reach a face from its outer side; both rays are dropped. Lines L6 and L7 remove outliers. A ray that slips through a narrow gap into a far part of the mesh, or that hits the far end of a long part at a flat angle, gives a length far from the others.

**Normalization.** The values are then mapped to $[0, 1]$ with

$$\mathrm{nsdf}(f) = \frac{\log\bigl(\alpha\,(\mathrm{SDF}(f) - \min) / (\max - \min) + 1\bigr)}{\log(\alpha + 1)},$$

where $\min$ and $\max$ are taken over the faces of the mesh. A larger $\alpha$ spreads out the small values, which are the thin parts. The values do not depend on the scale of the mesh.

**Segmentation.** The paper then cuts the mesh into parts in two steps.

1. **Soft clustering.** Fit a mixture of $k$ Gaussians to the normalized values with the [EM algorithm](/expectation-maximization/). Each face gets a probability for each cluster. Thin parts and thick parts fall into different Gaussians.
2. **Hard clustering.** Choose one label for each face by minimizing an energy on the graph of faces, where two faces are adjacent when they share an edge. The data term of a face is $-\log$ of the probability of its label. The smoothness term charges each pair of adjacent faces with different labels, and the charge is small along concave edges, where parts usually meet. The minimization uses [alpha-expansion](/alpha-expansion/) graph cuts. A weight $\lambda$ between the two terms sets how smooth the borders are.

A part is then a connected set of faces with the same label. The SDF can be smoothed over the surface before the clustering, for example with a [bilateral filter](/bilateral-filter/) on the faces, as CGAL does. The code of this page computes the SDF and the normalization, not the segmentation.

## Example

**A slab.** Take the box $6 \times 6 \times 1$, with the big sides cut into unit squares and each square into two triangles, and a face of the top side near its center. All 25 rays reach the bottom side. Their lengths are $1$ (the axis), $1/\cos 20° = 1.0642$ (eight rays), $1/\cos 40° = 1.3054$ (eight rays) and $1/\cos 60° = 2$ (eight rays). The median is $1.3054$ and the standard deviation is $0.3989$, so line L7 drops the eight rays of length $2$, and

$$\mathrm{SDF} = \frac{1 + 8 \times 1.0642 + 8 \times 1.3054}{17} = 1.1739.$$

The SDF is 17% larger than the thickness, because the cone tilts the rays. For the slab of thickness $\tfrac12$ the value is $0.5870$, half as large. With one ray along the normal, the SDF is $1$, the thickness.

**A bar that bends.** Take the bar $6 \times 1 \times 1$, cut into 208 triangles. On the faces of the long sides, away from the ends, the SDF is between $1.014$ and $1.163$, with a mean of $1.092$. On the faces of the two ends it is $0.712$ on average, because the rays from an end hit the long sides soon. Now bend the bar into a quarter circle, with the same triangles: each vertex $(x, y, z)$ goes to the point at the arc length $x$ along a circle of radius $6/(\pi/2) = 3.82$. On the long sides away from the ends, the SDF now has a mean of $1.079$, between $1.000$ and $1.197$. The value of each such face changes by $3.4\%$ on average and by $9.4\%$ at most. The largest change on the whole mesh is $29\%$, at a face next to an end, where the SDF goes from $0.371$ to $0.478$. So the measure stays close to the thickness of the bar, not to its shape in space. This is the stability that the segmentation uses.

**Why the test is exact.** A ray aimed at a point of an edge shared by two triangles must hit one of them. In floating point, the computed barycentric coordinates can put the point just outside both triangles, and the ray then passes through the closed surface. In a search over random triangles with float coordinates, with each ray aimed at the exact midpoint of the shared edge, this happened in 1612 of 20000 trials. The exact test hits both triangles at the same $t$ in all of them.

## Correctness

The [proof](proofs/correctness.md) shows these facts about the code.

- **The ray-triangle test is exact.** The test solves $o + t d = a + u e_1 + v e_2$ by Cramer's rule and checks $u \ge 0$, $v \ge 0$, $u + v \le 1$ and $t > 0$ on rationals. It returns the hit exactly when the ray meets the closed triangle, and two faces that share the hit point are both found.
- **The exit test keeps the right rays.** On a closed mesh with outward normals, a ray that starts inside the face $f$ and goes inward, and whose first hit is inside a face $g$, has $d \cdot n_g > 0$. So line L5 keeps it. The choice on an edge or a vertex is not proved to be the right one in all cases.
- **The slab.** On a slab of thickness $h$, for a face far enough from the side walls, every ray is kept, a ray at the angle $\theta$ has length $h / \cos\theta$, one ray gives $h$, and the SDF is $h$ times a constant that depends only on the angles of the rays. For the 25 rays of the code the constant is $1.1739$.
- **It stops.** Each face needs $r$ times $F - 1$ ray-triangle tests.

The rest is measured, not proved. That the SDF is close to the local diameter on other shapes, that it changes little when the pose changes, and that the segmentation finds the parts a person would choose, are results of experiments, in the paper and in the example above.

## Complexity

For one face, line L4 tests each ray against every face, so the time is $\Theta(r F)$ tests on the [real RAM](/real-ram/), and the sort of line L6 adds $O(r \log r)$. For all faces the time is $O(r F^2)$. The extra space is $\Theta(r)$ for the lengths of one face. A [bounding volume hierarchy](/bounding-volume-hierarchy/) makes each ray cost about $O(\log F)$ tests on typical meshes, so all faces take about $O(r F \log F)$ time; the worst case stays $O(r F^2)$. Exact rational arithmetic is slower than floats by a large factor: the pure Python code took about 40 seconds for the 208 faces of the bar. A robust float test, such as a [watertight ray-triangle test](/watertight-ray-triangle-intersection/), is the usual choice for large meshes.

## Properties

- **Invariant under scaling, nearly invariant under rigid motions.** Scaling the mesh scales all lengths, and the normalized values do not change. A rigid motion moves the cone with the face, but the code may turn the rings of rays about the axis, so the values can change slightly, as on the rotated slab of the tests, where they agree to $10^{-9}$.
- **Nearly invariant under pose changes.** A bend at a joint changes the SDF mostly near the joint. This is measured, not proved.
- **Volume based.** The SDF looks at the solid, not only at the surface near the face. Two faces on opposite sides of a thin part get similar values.
- **Deterministic.** The directions are fixed, so the same mesh gives the same values.
- **Needs a closed, oriented mesh.** Holes and flipped faces make rays drop, and a face with no kept ray gets no value.

## Variants and improvements

- **Skeletons.** The paper also uses the SDF to build a skeleton of the parts: a point pushed inward from a face by half its SDF lies near the middle of the shape.
- **Smoothing on the surface.** CGAL smooths the SDF with a bilateral filter over the faces before the clustering, and gives faces with no value the mean of their neighbours.
- **Volumetric versions.** The thickness can also be computed from a voxel grid or from a medial axis, for example as the diameter of the largest inscribed ball that touches the point. This is more expensive but has no rays to choose.
- **Other ray descriptors.** [Ambient occlusion](/ambient-occlusion/) casts rays outward, not inward, and measures how hidden a point is. Both are per-face features that learning-based segmentation can use together.
- **Fewer faces.** The values of neighbouring faces are close, so the SDF can be computed on a subset of the faces and spread to the others.

## When to use it

Use the SDF when the parts of a shape differ in thickness, such as the limbs of an animal, the legs of a chair or the handle of a cup, and when the segmentation must be the same for the same object in different poses. It is a good feature for comparing shapes of articulated objects and for learning-based segmentation. For a segmentation into nearly flat patches, as for mechanical parts or buildings, a normal-based method such as [variational shape approximation](/variational-shape-approximation/) fits better. For a mesh that is not closed, repair it first, or expect missing values near the holes.

## Pitfalls

- **Float ray tests leak.** A float ray-triangle test can miss both faces at a shared edge, and the ray then finds a face far away or none. Use exact or watertight tests, or at least treat lengths far from the median as outliers.
- **Hitting the starting face.** A ray from the centroid of $f$ meets the plane of $f$ at $t = 0$. Skip $f$ itself and require $t > 0$, or the SDF is 0.
- **Wrong orientation.** With flipped faces, the exit test drops rays that should count, or keeps rays that reached a face from outside. Orient the mesh consistently first.
- **Too wide a cone.** At $60°$ from the normal a ray is twice as long as the thickness, and near the end of a part it can hit the far end. The outlier removal handles a few such rays, not most of them.
- **Not a distance.** The SDF of a slab is $1.17$ times its thickness with the cone of the code, and the factor changes with the number and the angles of the rays. Compare SDF values only when they come from the same settings.
- **Parts of equal thickness.** Two parts with the same thickness, such as the upper and the lower leg, fall into the same cluster. The graph cut separates them only where the surface has a concave edge between them.
- **Cost.** Without an acceleration structure the cost is quadratic in the number of faces.

## Implementations

## History

Shapira, Shamir and Cohen-Or defined the shape diameter function in a paper in The Visual Computer in 2008. They cast a cone of rays inward from each face, removed the outlier lengths, and used the result for two tasks: a segmentation of meshes into parts by a Gaussian mixture and graph cuts, which gave the same parts for the same object in different poses, and the construction of skeletons. The ray-triangle test they relied on goes back to Möller and Trumbore (1997), and the graph cut step to the alpha-expansion of Boykov, Veksler and Zabih (2001). The function was later included in the CGAL library, with the segmentation, and became a common feature for the segmentation of meshes.

## References
