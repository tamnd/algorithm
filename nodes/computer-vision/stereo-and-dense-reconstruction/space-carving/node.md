---
tag: TB513P
kind: algorithm
slug: space-carving
name: Space carving
aliases:
- Kutulakos-Seitz space carving
- photo hull
area: computer-vision/stereo-and-dense-reconstruction
level: advanced
summary: "Remove voxels that fail a photo-consistency test until none fails. The result is the photo hull, the largest shape that explains all the calibrated input images."
solves: [multi-view-stereo]
model: real-ram
complexity:
  vars: {N: the number of images, W: the image width in pixels, H: the image height in pixels, n: the number of voxels along each side of the grid}
  time: {worst: O(N W H n^4), average: O(N W H n^4), best: O(N W H n)}
  space: {extra: O(N W H n + n^3)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2000
  people: [Kiriakos N. Kutulakos, Steven M. Seitz]
  note: "Kutulakos and Seitz defined the photo hull, proved that carving inconsistent voxels in any order converges to it, and gave a multi-sweep implementation for cameras at arbitrary positions."
prereqs: [photo-consistency, visual-hull, pinhole-camera-model]
see_also: [voxel-coloring, visual-hull, multi-view-stereo, plane-sweep-stereo, amanatides-woo-traversal, octree, marching-cubes, depth-map-fusion]
sources:
  - paper: doi:10.1023/A:1008191222954
    title: "Kiriakos N. Kutulakos and Steven M. Seitz, A theory of shape by space carving, International Journal of Computer Vision 38(3), 2000, pages 199 to 218"
    locator: "Section 2 (photo-consistency, Definitions 1 to 3, the background constraint in 2.1 and the monotone consistency check in 2.2), Section 3 (Lemma 1, Theorem 1 the Subset Theorem, Theorem 2 the Photo Hull Theorem), Section 4 (the Space Carving Algorithm and Proposition 1) and Section 5 (the multi-sweep implementation)"
  - paper: doi:10.1023/A:1008176507526
    title: "Steven M. Seitz and Charles R. Dyer, Photorealistic scene reconstruction by voxel coloring, International Journal of Computer Vision 35(2), 1999, pages 151 to 173"
    locator: Section 3.1 (the ordinal visibility constraint that space carving removes) and Section 4.3 (the single-pass layered algorithm)
  - paper: doi:10.1109/34.273735
    title: "Aldo Laurentini, The visual hull concept for silhouette-based image understanding, IEEE Transactions on Pattern Analysis and Machine Intelligence 16(2), 1994, pages 150 to 162"
    locator: "the definition of the visual hull, which is the result of carving with background pixels only"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 12.7.2, Volumetric and 3D surface reconstruction"
---

Space carving reconstructs a 3D shape from many calibrated photographs. It starts with a block of voxels that surely contains the scene and removes, one by one or in batches, every voxel whose visible pixels do not agree in color. When no voxel can be removed, the remaining voxels form the photo hull: the largest shape that explains every input image. The [visual hull](/visual-hull/) is the special case that uses only the silhouettes, so the photo hull is always inside it. [Voxel coloring](/voxel-coloring/) is the earlier single-pass algorithm for the same task, which needs all cameras on one side of the scene. Space carving drops that restriction and works for cameras that surround the object.

## In plain words

Think of a sculptor with a block of stone and a set of photographs of the statue from all around. For each small cube of stone on the surface, the sculptor asks every camera that can see that cube which color it saw there. If the cameras disagree, or if some camera saw only background there, the cube cannot be part of the statue, so the sculptor removes it. Removing a cube uncovers the cubes behind it, which then get the same question. The sculptor stops when every visible cube gets the same color from all cameras that see it. The stone that remains is the biggest statue that looks exactly like all the photographs. It can be bigger than the real statue where the real statue has plain, untextured parts.

## The problem

**Input.**

- $N$ images of size $W \times H$. Each pixel has a gray value or the mark $\bot$ for background.
- The cameras, as $K$, $R$, $t$ with $X_c = R X + t$ (see [pinhole camera model](/pinhole-camera-model/)).
- A volume $U$: a grid of voxels that contains the scene. The code uses an $n \times n \times n$ grid of unit cubes.
- A threshold $\tau \ge 0$ for the color test.

The model reduces each pixel to the ray through its center, and each ray to the ordered list of voxels that it crosses. For a set of voxels $V$, the voxel of $V$ that a pixel sees, its *owner*, is the first voxel of its ray that is in $V$.

**The test.** A voxel $v \in V$ passes if none of the pixels that $v$ owns is background and if the largest and smallest values of these pixels differ by at most $\tau$. A voxel that owns no pixel passes. This is a form of [photo-consistency](/photo-consistency/) for a Lambertian scene.

**Output.** The largest set $V \subseteq U$ in which every voxel passes, and a flag that tells if $V$ explains every non-background pixel. If some photo-consistent shape lies in $U$, the flag is true and $V$ is the photo hull.

## The algorithm

```pseudo id=main
SPACE-CARVE(U, rays, images, τ)
L1  V ← U
L2  repeat
L3      for each pixel p of each image do owner(p) ← the first voxel of V on the ray of p, or none
L4      bad ← the voxels v ∈ V whose owned pixels include background or have max - min > τ
L5      if bad is empty then exit the loop
L6      V ← V \ bad
L7  return V, and whether every non-background pixel has an owner
```

**Line L3, visibility.** The owners change as voxels go away, because a removed voxel uncovers the voxels behind it. The code walks the precomputed voxel list of each ray, which comes from a 3D grid traversal in the style of [Amanatides and Woo](/amanatides-woo-traversal/). A real implementation keeps a depth buffer per image and updates it only where the shape changed.

**Line L4, the test.** The test must be monotone: if a set of colors passes, every subset passes. The range test $\max - \min \le \tau$ is monotone. A background pixel among the owned pixels fails the test at once, so carving with $\tau = \infty$ gives the visual hull of the grid.

**Line L6, removal.** All failing voxels go at once. The proof shows that the order of removal does not change the result, so a sweep order, a priority queue or a random order all give the same set.

## Example

**A plus-shaped prism.** The test file builds a $5 \times 5 \times 5$ grid (125 voxels) and a true scene of 27 voxels: a plus sign three voxels high, with random gray values from $\{20, 120, 220\}$. Six cameras on a ring around the grid render $10 \times 10$ images, and 158 of the 600 pixels see the object.

| $\tau$ | voxels left | rounds | extra voxels |
|---|---|---|---|
| $\infty$ (silhouettes only) | 33 | 4 | 6 |
| 200 | 33 | 4 | 6 |
| 100 | 30 | 4 | 3 |
| 0 | 27 | 4 | 0 |

With $\tau = \infty$ the result is the visual hull of the grid: the silhouettes do not show the four inner corners of the plus, so 6 voxels in those corners remain. As $\tau$ goes down, the color test removes more of them, and at $\tau = 0$ the result is the true scene. In every row the result contains the true scene and is photo-consistent. The test file also compares the result with the union of all photo-consistent subsets, found by brute force over all $2^8$ subsets of a $2 \times 2 \times 2$ grid and all $2^9$ subsets of a $3 \times 3 \times 1$ grid.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It rests on two facts.

1. **Visibility can only grow.** If $V' \subseteq V$, every pixel that a voxel $v \in V'$ owns in $V$ it also owns in $V'$, because the voxels in front of it are gone in both sets.
2. **The test is monotone.** A subset of a passing set of values passes.

Together they give the Subset Theorem of Kutulakos and Seitz: a voxel that fails in $V$ fails in every subset of $V$ that contains it. So carving never removes a voxel of a consistent shape inside $V$, and when it stops, the result is the largest set in which every voxel passes. If some photo-consistent shape exists in $U$, this set contains it, so it explains every pixel, and it is the photo hull. The order of removal plays no part in the argument.

## Complexity

The model is the real RAM. Let $M = n^3$ be the number of voxels. Each ray crosses at most $3n$ voxels.

- **One round.** Line L3 walks at most $3n$ voxels for each of the $N W H$ pixels, so $O(N W H n)$. Line L4 reads each pixel value once, $O(N W H)$, and line L6 costs $O(M)$.
- **Rounds.** Each round except the last removes at least one voxel, so there are at most $M + 1 = n^3 + 1$ rounds. The worst case is $O(N W H n^4)$. One round suffices when $U$ is already consistent, which gives the best case $O(N W H n)$.
- **Space.** The ray lists take $O(N W H n)$ and the voxel set takes $O(n^3)$.

The bound with many rounds is loose. Kutulakos and Seitz count photo-consistency checks instead and bound them by $N M$. With depth buffers that are updated incrementally, the work per removed voxel is the area of its projection in the images.

## Properties

- **Exact for its model.** The result is the photo hull of the grid under the given test, independent of the order of removal.
- **Outer bound.** The photo hull contains every photo-consistent shape, so it contains the true scene whenever the true scene passes the test. It can be larger than the scene.
- **Any camera positions.** Unlike [voxel coloring](/voxel-coloring/), it needs no ordering of the voxels by distance to the cameras.
- **No regularization.** It has no smoothness term. Noise that makes a true voxel fail the test cuts a hole that the next rounds can widen.
- **Deterministic.** It has no random choices.

## Variants and improvements

- **Multi-sweep space carving.** Kutulakos and Seitz sweep a plane through the grid along each of the six principal directions. During a sweep they test each voxel against only the cameras on the side that the plane has already passed, for which the visibility order is known. After the six sweeps, a final check uses all cameras, and the sweeps repeat until no voxel is removed.
- **Voxel coloring.** When no scene point lies inside the convex hull of the camera centers, [voxel coloring](/voxel-coloring/) does one pass in order of distance and needs no repetition.
- **Visual hull.** With $\tau = \infty$, only the background test remains, and carving gives the [visual hull](/visual-hull/) of the grid. Image-based and polyhedral methods compute it much faster.
- **Probabilistic carving.** Later work replaces the hard test with probabilities of occupancy, which makes the result less sensitive to noise.
- **Adaptive grids.** An [octree](/octree/) refines the grid only near the surface, which cuts the number of voxels for a given resolution.
- **Surface extraction.** The carved set is a set of cubes. A mesh comes from [marching cubes](/marching-cubes/) on its occupancy.

## When to use it

Use space carving when you have many calibrated images all around a small object, good silhouettes, and textured surfaces, and you want a result with a clear meaning: the largest shape that is consistent with the data. It is a good teaching example of how visibility and photo-consistency interact. For real scenes with noise, specular highlights and little texture, modern [multi-view stereo](/multi-view-stereo/) pipelines based on depth maps and [depth map fusion](/depth-map-fusion/) give better surfaces.

## Pitfalls

- **A test that is not monotone.** A threshold on the standard deviation of the colors is common but not monotone: $\{0, 10\}$ has a standard deviation of 5, and $\{0, 10, 5, 5, 5\}$ has $\sqrt{10} \approx 3.16$. With such a test the Subset Theorem fails and the result can lose true voxels.
- **Holes from noise.** If the threshold is too tight, a true surface voxel fails, the voxel behind it becomes visible and also fails, and the hole grows through the object.
- **Too loose a threshold.** If it is too loose, the result stays close to the visual hull. Textureless regions always bulge outward.
- **Stale visibility.** After a removal, the owners of the pixels change. Testing a voxel with old visibility can remove a voxel that is consistent.
- **Calibration errors.** A small error in a camera pose makes a true voxel see different colors in different images, and it gets carved. Silhouettes must also be accurate, since one wrong background pixel removes every voxel on its ray.

## Implementations

## History

Seitz and Dyer introduced voxel coloring in 1997 for cameras that satisfy the ordinal visibility constraint. Kutulakos and Seitz removed that constraint. Their paper in the International Journal of Computer Vision (2000) defined photo-consistency, proved the Subset Theorem and the Photo Hull Theorem, and showed that carving in any order converges to the photo hull. They implemented it with plane sweeps in the six principal directions. Later work added probabilistic tests and better handling of noise, but depth-map based multi-view stereo replaced voxel carving in most practical systems.

## References
