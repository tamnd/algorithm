---
tag: 1NZA21
kind: algorithm
slug: voxel-coloring
name: Voxel coloring
aliases:
- Seitz-Dyer voxel coloring
area: computer-vision/stereo-and-dense-reconstruction
level: advanced
summary: "Visit voxels in layers of growing distance from the cameras and color each one whose still unexplained pixels agree. Needs no scene point inside the convex hull of the cameras."
solves: [multi-view-stereo]
model: real-ram
complexity:
  vars: {N: the number of images, W: the image width in pixels, H: the image height in pixels, n: the number of voxels along each side of the grid}
  time: {worst: Θ(N W H n), average: Θ(N W H n), best: Θ(N W H n)}
  space: {extra: O(N W H n + n^3)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1997
  people: [Steven M. Seitz, Charles R. Dyer]
  note: "Seitz and Dyer presented voxel coloring at CVPR 1997 and in a longer journal version in 1999. It was the first method to reconstruct a colored voxel scene from many views in one pass, with visibility handled exactly."
prereqs: [photo-consistency, pinhole-camera-model]
see_also: [space-carving, visual-hull, photo-consistency, multi-view-stereo, plane-sweep-stereo, convex-hull, octree, depth-map-fusion]
sources:
  - paper: doi:10.1023/A:1008176507526
    title: "Steven M. Seitz and Charles R. Dyer, Photorealistic scene reconstruction by voxel coloring, International Journal of Computer Vision 35(2), 1999, pages 151 to 173"
    locator: "Section 3.1 (the ordinal visibility constraint), Section 3.2 (the consistent scene that is closest to the cameras), Section 4.1 (layers), Section 4.2 (the voxel consistency test), Section 4.3 (the single-pass algorithm) and Section 4.4 (the cost)"
  - paper: doi:10.1023/A:1008191222954
    title: "Kiriakos N. Kutulakos and Steven M. Seitz, A theory of shape by space carving, International Journal of Computer Vision 38(3), 2000, pages 199 to 218"
    locator: "Section 2.2 (monotone consistency checks) and Section 5 (plane sweeps for cameras in general position)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 12.7.2, Volumetric and 3D surface reconstruction"
---

Voxel coloring reconstructs a colored 3D scene from many calibrated images in a single pass over a voxel grid. It needs one condition on the cameras: no point of the scene may lie inside the convex hull of the camera centers. Then the voxels can be visited in layers of growing distance from the cameras, so that a voxel is always visited before every voxel it can hide. A voxel is kept and colored when the pixels that see it, and that no nearer kept voxel explains, agree in color. [Space carving](/space-carving/) solves the same task without the condition on the cameras, but must repeat its passes until nothing changes. Voxel coloring returns the consistent scene that is nearest to the cameras, while space carving returns the largest one, the photo hull.

## In plain words

Imagine several cameras that all look at a scene from one side, for example from above a table. Cut the space into thin slices, from the slice nearest to the cameras to the slice farthest away. Walk through the slices in that order. In each slice, look at each small cube and ask the cameras what color they see in its direction. Ignore the camera pixels that a cube in an earlier slice already explains, because those pixels show that earlier cube. If the remaining pixels all show the same color, keep the cube with that color and tick off those pixels. A cube is never seen through another cube, so one walk through the slices is enough.

## The problem

**Input.**

- $N$ images of size $W \times H$. Each pixel has a gray value or the mark $\bot$ for background.
- The cameras, as $K$, $R$, $t$ with $X_c = R X + t$ (see [pinhole camera model](/pinhole-camera-model/)).
- A grid of voxels that contains the scene, with $n$ voxels along each side, and a threshold $\tau \ge 0$.

**The ordinal visibility constraint.** There must be a function $D$ on the points of the scene such that $D(P) < D(Q)$ whenever $P$ can hide $Q$ from some camera. Seitz and Dyer show that the distance to the convex hull of the camera centers is such a function when no scene point lies inside that hull. The code takes the simplest case: all camera centers lie below the plane $z = 0$, the grid lies above it, and $D = z$. The voxels with the same $z$ form a layer, and each pixel ray meets each layer in at most one voxel, at its point on the middle plane of the layer.

**The test.** A set of pixels passes if it has no background pixel and its largest and smallest values differ by at most $\tau$. This is a monotone form of [photo-consistency](/photo-consistency/) for a Lambertian scene.

**Output.** A set of colored voxels in which each voxel passes the test on the pixels that see it, and that explains every non-background pixel. The code also returns a flag that is false if some non-background pixel stays unexplained.

## The algorithm

```pseudo id=main
VOXEL-COLOR(rays, images, L, τ)
L1  S ← ∅; mark no pixel
L2  for k ← 0 to L - 1 do                     ▷ layers, nearest first
L3      for each voxel v of layer k do
L4          π(v) ← the unmarked pixels whose ray meets layer k at v
L5          if π(v) is not empty and passes the test then add v to S with the mean color of π(v)
L6      mark every pixel of π(v) for each voxel v added in this layer
L7  return S, and whether every non-background pixel is marked
```

**Line L4, the footprint.** The pixels that see $v$ are those whose rays meet $v$. Marked pixels already show a voxel of an earlier layer, which hides $v$ from them, so they are left out. The code finds all footprints of a layer in one pass over the unmarked pixels, by grouping them by the voxel their ray meets.

**Line L6, marking after the layer.** The pixels are marked only after the whole layer is done. Two voxels of the same layer never hide each other along a ray, so the order inside a layer does not matter.

**Line L5, the test.** Seitz and Dyer use the standard deviation of the colors, or a chi-square form of it with the noise level of the camera. The code uses the range of the colors, which is monotone, so that the proof holds exactly.

## Example

**A floor with blocks in front.** The test file uses a $4 \times 4 \times 3$ grid and four cameras below it with $10 \times 10$ images. The true scene is the whole far layer (16 voxels), which acts as a floor, and 11 voxels in the two nearer layers, with gray values from $\{0, 100, 200\}$. The images have 207 pixels that are not background.

With $\tau = 0$, voxel coloring keeps 21 voxels: 5 in the nearest layer, 13 in the middle layer and 3 in the far layer. Seven of them are empty in the true scene, and 13 true voxels are missing. Still, the result is photo-consistent, and every pixel sees a voxel at the same layer as in the true scene or at a nearer one. This is the meaning of the output: of all scenes that explain the images, it is the one nearest to the cameras. The true voxels that are missing are hidden in all four views, or are replaced by a nearer voxel that the images cannot tell apart from them.

The test file also checks the theorem by brute force. On grids of 8 and 12 voxels it lists every consistent scene, computes for each pixel the nearest voxel that any of them lets the pixel see, and compares this set with the output.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). For each pixel $p$, let $\ell(p)$ be the nearest layer at which some consistent scene gives $p$ an owner, and let $V_p$ be the voxel of the ray of $p$ at that layer. The set $\bar S$ of all $V_p$ is the scene of Seitz and Dyer.

1. **$\bar S$ is consistent.** No voxel of $\bar S$ lies in front of $V_p$ on the ray of $p$, and the pixels that a voxel owns in $\bar S$ are a subset of those it owns in a consistent scene. The monotone test then carries over.
2. **The invariant.** Before layer $k$, the unmarked pixels are exactly those with $\ell(p) \ge k$. A voxel of layer $k$ passes if and only if it is in $\bar S$. If it is in $\bar S$, its footprint is a subset of its pixels in a consistent scene. If it is not in $\bar S$ but passed, adding it to $\bar S$ would give a consistent scene in which some pixel has an owner nearer than $\ell(p)$.

So the output is $\bar S$ whenever any consistent scene exists. With a test that is not monotone, such as a threshold on the standard deviation, the argument breaks and the method is a heuristic.

## Complexity

The model is the real RAM. With $n$ layers, each layer costs one pass over all $N W H$ pixels plus the test on the footprints, which together have at most $N W H$ pixels. The total is $\Theta(N W H n)$ in every case.

The code stores the voxel of each layer for each pixel, $O(N W H n)$, and the colored voxels, $O(n^3)$. Seitz and Dyer compute the footprints on the fly and store only the images and one bit per pixel for the marks, which is $O(N W H)$ besides the output. They count the cost per voxel as the size of its footprint and state a bound linear in the number of voxels and the number of images.

## Properties

- **One pass.** Each voxel is tested once. No voxel is changed after its layer.
- **Exact visibility.** Under the ordinal visibility constraint, the marks give the exact set of pixels that see each voxel.
- **Nearest consistent scene.** The result is consistent, and at each pixel its surface is as near to the cameras as any consistent scene allows. It is contained in the photo hull of [space carving](/space-carving/), but it is usually smaller.
- **Restricted camera positions.** No scene point may lie inside the convex hull of the camera centers. Cameras all around an object break this.
- **No smoothness term.** Each voxel is judged only by its colors.

## Variants and improvements

- **Space carving.** Kutulakos and Seitz drop the camera condition by plane sweeps in six directions, each using only the cameras on one side of the plane, and repeat them until no voxel changes.
- **Generalized voxel coloring.** Culbertson, Malzbender and Slabaugh keep exact visibility for any camera positions with item buffers that record, for each pixel, which surface voxel it sees.
- **Other layer shapes.** The layers need not be planes. Any layers work if the distance to the convex hull of the camera centers grows from layer to layer, for example shells around a region from which the cameras look outward.
- **Adaptive grids.** An [octree](/octree/) refines the grid near the surface, which saves memory at high resolution.
- **Probabilistic tests.** Later methods replace the hard threshold with a probability of occupancy, which makes the result less sensitive to noise.

## When to use it

Use voxel coloring when the cameras are all on one side of the scene, for example a camera that moves along a path in front of a room or above a table, and you want a colored model in one fast pass with exact visibility. If the cameras surround the object, use [space carving](/space-carving/) or a method based on depth maps. For high quality surfaces of real objects, modern [multi-view stereo](/multi-view-stereo/) with [depth map fusion](/depth-map-fusion/) is better.

## Pitfalls

- **Cameras around the object.** If a scene point is inside the convex hull of the camera centers, no layer order respects visibility, and voxels are tested against pixels that do not see them.
- **Bulges in textureless areas.** Where the surface has no texture, voxels in front of it also pass the test, and the result bulges toward the cameras. This follows from the output being the nearest consistent scene.
- **A tight threshold.** One noisy pixel can make a true voxel fail. Its pixels stay unmarked, and a wrong voxel farther away may then take them.
- **The standard deviation test.** It is not monotone, so the proof does not hold for it, and adding pixels can make a failing voxel pass.
- **Coarse footprints.** A voxel covers several pixels in each image. Treating each pixel as one ray, as the code does, misses voxels that cover only part of a pixel.

## Implementations

## History

Seitz and Dyer presented voxel coloring at CVPR 1997 and in a longer journal version in the International Journal of Computer Vision in 1999. They introduced the ordinal visibility constraint and showed that, under it, a single pass over the voxels in order of distance gives a consistent scene with exact visibility. Kutulakos and Seitz then generalized the idea to space carving for any camera positions, and Culbertson, Malzbender and Slabaugh gave generalized voxel coloring with item buffers.

## References
