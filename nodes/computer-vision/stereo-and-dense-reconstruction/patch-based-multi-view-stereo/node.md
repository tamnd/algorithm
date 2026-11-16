---
tag: 22G2KD
kind: algorithm
slug: patch-based-multi-view-stereo
name: Patch-based multi-view stereo
aliases:
- PMVS
- Furukawa-Ponce MVS
area: computer-vision/stereo-and-dense-reconstruction
level: advanced
summary: Match features into small oriented patches, expand them into neighboring image cells and filter those that break visibility or have few neighbors, giving a dense set of patches on the surface.
solves: [multi-view-stereo]
model: real-ram
complexity:
  vars: {N: the number of images, F: the number of features per image, M: the number of image cells, s: the number of samples per patch, E: the cost evaluations per refinement, R: the rounds of expansion and filtering, k: the largest number of patches in one cell}
  time: {worst: O(N^3 F^2 E s + R M N (N E s + k)), average: O(N^3 F^2 E s + R M N (N E s + k)), best: Ω(N F)}
  space: {extra: O(M N)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2007
  people: [Yasutaka Furukawa, Jean Ponce]
  note: Furukawa and Ponce presented the method at CVPR 2007 and in IEEE TPAMI in 2010. It reconstructs a set of small oriented patches, with no initial shape, and had top results on the Middlebury multi-view benchmark of that time.
prereqs: [photo-consistency, normalized-cross-correlation, midpoint-triangulation, epipolar-geometry]
see_also: [multi-view-stereo, plane-sweep-stereo, patchmatch-stereo, depth-map-fusion, poisson-surface-reconstruction, incremental-structure-from-motion, point-cloud, space-carving]
sources:
  - paper: doi:10.1109/TPAMI.2009.161
    title: Yasutaka Furukawa and Jean Ponce, Accurate, dense, and robust multiview stereopsis, IEEE Transactions on Pattern Analysis and Machine Intelligence 32(8), pages 1362 to 1376, 2010
    locator: the patch model with its reference image and visible images, the photometric discrepancy by normalized cross-correlation, the image cells, and the three steps of matching, expansion and filtering
  - paper: doi:10.1561/0600000052
    title: "Yasutaka Furukawa and Carlos Hernández, Multi-view stereo: a tutorial, Foundations and Trends in Computer Graphics and Vision 9(1-2), pages 1 to 148, 2015"
    locator: the chapter on multi-view stereo algorithms (point cloud reconstruction by patch expansion)
  - paper: doi:10.1109/CVPR.2006.19
    title: Steven M. Seitz, Brian Curless, James Diebel, Daniel Scharstein and Richard Szeliski, A comparison and evaluation of multi-view stereo reconstruction algorithms, IEEE Conference on Computer Vision and Pattern Recognition 2006
    locator: the benchmark data sets and the accuracy and completeness measures
---

Patch-based multi-view stereo, or PMVS, turns calibrated images into a dense set of small oriented squares, called patches, that lie on the surface of the scene. It starts from a few reliable patches made from matched features. Then it grows the set: each patch tries to put new patches in the neighboring image cells, on its own tangent plane, and keeps those that look the same in several images. A filter step removes patches that break visibility or that do not fit their neighbors. Expansion and filtering alternate a few times. The method of Furukawa and Ponce (2007, 2010) needs no initial shape, no bounding volume and no depth range, and it handles outliers and occlusion well. The result is a quasi-dense oriented point set, which a surface method such as [Poisson surface reconstruction](/poisson-surface-reconstruction/) can turn into a mesh. It is one answer to the [multi-view stereo](/multi-view-stereo/) problem.

## In plain words

Think of covering a statue with small square stickers. You first put a few stickers where you are sure: points that look very distinct and that you can find in several photos. Then, next to every sticker, you try a new one that leans the same way as its neighbor, and you nudge it until it looks the same from all cameras. If the nudged sticker looks right in enough photos, it stays. You keep doing this until the stickers cover the statue. Now and then you walk around and pull off stickers that float in front of the statue or that do not line up with the stickers next to them.

## The problem

**Input.**

- $N$ gray images $I_1, \dots, I_N$ with known cameras $(K_i, R_i, t_i)$. A point $X$ maps to the camera frame by $R_i X + t_i$.
- Feature points in each image (the paper detects Harris and difference of Gaussian features; the code takes them as input).
- Parameters: the grid size $\mu$, the cell size $\beta$ in pixels, the least number $\gamma$ of images that must agree, the threshold $\alpha$ of the discrepancy, the number of rounds $R$.

**Output.** A set of patches. A patch $p$ has a center $c(p)$, a unit normal $n(p)$ that points toward the cameras, a reference image $R(p)$, the set $V(p)$ of images that may see it, and the set $V^*(p) \subseteq V(p)$ of images in which it is photo-consistent. The aim is at least one patch in every cell of $\beta \times \beta$ pixels of every image where the surface is seen, with each patch close to the surface.

**Discrepancy.** Lay a $\mu \times \mu$ grid on the patch, with one step about one pixel of $R(p)$. Project the grid into an image $I$ and read the image by bilinear interpolation. The discrepancy $h(p, I, R(p))$ is one minus the [normalized cross-correlation](/normalized-cross-correlation/) of these values with those of $R(p)$. The score of a patch is

$$g^*(p) = \frac{1}{|V^*(p) \setminus \{R(p)\}|} \sum_{I \in V^*(p) \setminus \{R(p)\}} h(p, I, R(p)),$$

and $V^*(p)$ holds $R(p)$ and the images of $V(p)$ with $h \le \alpha$. This is a [photo-consistency](/photo-consistency/) measure in scene space.

## The algorithm

```pseudo id=main
PMVS(images, cameras, features, R)
L1  for each image I_i and each feature f of I_i do                          ▷ matching
L2      if the cell of f in I_i already holds a patch then skip f
L3      F ← the features of other images within 2 pixels of the epipolar line of f
L4      triangulate f with each f' in F and sort the points by distance from the center of I_i
L5      for each point X in that order do p ← patch(c = X, n = unit(O_i - X), R = I_i)
L6          if ACCEPT(p) then
L7              register p in its cells; go to the next feature
L8  repeat R times
L9      for each patch p, then each new patch, do                              ▷ expansion
L10         for each I in V*(p) and each cell C next to the cell of p in I that holds no patch do
L11             X ← the point where the ray through the center of C meets the plane of p
L12             q ← patch(c = X, n = n(p), R = R(p))
L13             if ACCEPT(q) and I ∈ V*(q) and q projects into C then
L14                 register q in its cells; add q to the queue
L15     for each patch p do                                                    ▷ filtering
L16         remove p if fewer than a fraction of the patches in the 3 × 3 cells around p, in the images of V*(p), are neighbors of p
L17 return the patches

ACCEPT(p): V(p) ← the images that see c(p) at an angle below a limit; V*(p) ← R(p) and the images of V(p) with h ≤ α;
           refine c(p) along the ray of R(p) and the two angles of n(p) to minimize g*(p); recompute V(p) and V*(p);
           return |V*(p)| ≥ γ
```

**Matching (L1 to L7).** For a feature $f$ of $I_i$, the candidate matches in the other images lie near its epipolar line ([epipolar geometry](/epipolar-geometry/)). Each candidate gives a 3D point by [triangulation](/midpoint-triangulation/). The points are tried from the nearest to the farthest from the optical center $O_i$, and the first one that ACCEPT keeps becomes a patch. The normal starts pointing at $O_i$. Line L2 skips features in cells that are already covered, which saves time.

**Refinement.** ACCEPT moves the patch to lower $g^*(p)$ with three free values: the depth of $c(p)$ along the ray of $R(p)$ and two angles of $n(p)$. The paper uses a conjugate gradient method. The code uses a pattern search: it tries a step up and down in each value, keeps any step that helps, and halves the steps when none does. Moving $c(p)$ along the ray of $R(p)$ keeps its pixel in $R(p)$ fixed.

**Expansion (L9 to L14).** Real surfaces are smooth at the scale of a few pixels, so the plane of a patch is a good guess for its neighbors. Line L11 puts the new patch where the ray of the neighboring cell meets that plane, and ACCEPT corrects it. The test in line L13 that $q$ still projects into $C$ keeps one new patch per empty cell; it is a choice of the code. The paper has its own rules for which cells to skip. For example, it skips a cell that already holds a patch which is a neighbor of $p$, and it does not expand across a depth discontinuity.

**Filtering (L15 and L16).** Two patches $p$ and $p'$ are neighbors when $|(c(p) - c(p')) \cdot n(p)| + |(c(p) - c(p')) \cdot n(p')| < 2 \rho$, so each lies close to the plane of the other. The paper has three filters. Two of them use visibility: one removes patches that lie outside the surface, in front of patches that the same images see, and one removes patches that too few images see as the nearest surface. The third, of the regularization kind, removes a patch when few of the patches in the cells around it are its neighbors. The code has only a filter of the third kind, with the fraction 0.25 and $\rho$ equal to two pixels of $R(p)$, and the page gives the paper's filters only in outline.

## Example

The test file builds a textured plane $Z = 4 + 0.15 X - 0.1 Y$ and three $24 \times 24$ images with focal length 40, from cameras at $(0, 0, 0)$, $(0.5, 0, 0)$ and $(0.1, 0.45, 0)$. One pixel at depth 4 covers 0.1 units of the plane. Each image has 8 features: the projections of the 6 points with $X \in \{-0.5, 0, 0.5\}$ and $Y \in \{-0.4, 0.4\}$ on the plane, and 2 random points. The parameters are $\mu = 5$, $\beta = 3$, $\gamma = 2$, $\alpha = 0.3$ (NCC at least 0.7) and $R = 3$.

1. **Matching.** All 6 true points become patches at the true depth. The random features find no partner that passes ACCEPT. For example, the feature at $(16.36, 7.61)$ of image 1 has a match in image 2 at $(11.5, 7.61)$ on its epipolar line, which triangulates to $(0.5, -0.4, 4.115)$, a point of the plane. After refinement its normal is $(0.127, -0.089, -0.988)$, close to the true $(0.148, -0.098, -0.984)$, and $g^* = 0.001$.
2. **Expansion.** The first round grows the 6 patches to 60. The cells of image 1 that the other cameras also see are covered, except one: 35 of the 36 inner cells hold a patch. The largest distance of a patch center from the plane is 0.074 (under one pixel), and the median is 0.009.
3. **Filtering.** The filter removes nothing from this clean set. A patch put by hand at $(0, 0, 3.6)$, 0.4 in front of the plane, has no neighbor among the patches in the cells around it and is removed. The next two rounds add nothing.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It proves what the procedure guarantees, not that the output is the true surface.

1. **Acceptance.** Every patch in the output has $|V^*(p)| \ge \gamma$, $R(p) \in V^*(p)$, and $h(p, I, R(p)) \le \alpha$ for every $I \in V^*(p)$, as computed at the time it was accepted. Refinement never increases $g^*$.
2. **Cells.** Every patch is registered in the cell of its projection in each image of $V^*(p)$, and each new patch fills a cell that was empty.
3. **Termination.** Every accepted patch fills an empty cell, a filter round only removes patches, and the number of cells is finite. So each expansion ends after at most $M$ new patches, and the whole run ends after $R$ rounds.
4. **Exact data.** On a textured plane with exact images, a patch on the plane with the true normal has $h = 0$ in every image that sees all of its grid. So the truth passes ACCEPT. The bilinear sampling of the code makes $h$ small but not zero, as the example shows.

## Complexity

The model is the real RAM. Let $s = \mu^2$, let $E$ bound the cost evaluations of one refinement, and let $M$ be the total number of cells in all images, about $N W H / \beta^2$.

- **One ACCEPT.** $V(p)$ takes $O(N)$, one $g^*$ takes $O(N s)$, and the refinement takes $O(E N s)$.
- **Matching.** Each of the $N F$ features gets up to $(N - 1) F$ candidates in the worst case, so matching takes $O(N^3 F^2 E s)$. In practice the epipolar test leaves a few candidates per image and the first good one stops the loop.
- **Expansion.** Each accepted patch fills an empty cell, so a round has at most $M$ patches. Each patch tries at most 4 cells in each of at most $N$ images, so a round takes $O(M N^2 E s)$.
- **Filtering.** Each patch looks at 9 cells in at most $N$ images, with at most $k$ patches each, so a round takes $O(M N k)$.
- **Space.** The patches and their registrations take $O(M N)$, besides the images.

The constants are large, and most of the time goes to the cost evaluations of refinement.

## Properties

- **No initial shape.** Matching needs no bounding box, visual hull or depth range, unlike many volumetric methods in the survey of Seitz et al. (2006).
- **Local and robust.** Each patch is tested against the images on its own. Outliers fail ACCEPT or the filters, and occluded images leave $V^*(p)$.
- **Uniform density.** The cells set the density: about one patch per $\beta \times \beta$ pixels of each image.
- **Output is oriented points.** The output is not a surface. A mesh needs another step.
- **Deterministic.** Given the features and the order of the images, the result does not depend on random numbers.

## Variants and improvements

- **Software.** The PMVS2 program of Furukawa uses by default a window of 7 by 7 samples, a cell size of 2 pixels, an NCC threshold of 0.7 that drops by 0.05 per round, and at least 3 images per patch.
- **Clustering for large scenes.** CMVS splits a large photo collection into overlapping clusters of views that PMVS can handle one at a time.
- **Depth map methods.** Many later systems compute a depth map per image, for example with [PatchMatch stereo](/patchmatch-stereo/) in its multi-view form or with a [plane sweep](/plane-sweep-stereo/), and merge them by [depth map fusion](/depth-map-fusion/). The tutorial of Furukawa and Hernández (2015) compares the two approaches.
- **Mesh refinement.** A mesh made from the patches can be refined further with photo-consistency, which gives a smooth surface with finer detail.

## When to use it

Use PMVS when you have calibrated images, for example from [structure from motion](/incremental-structure-from-motion/), and want a dense, oriented point set with few outliers and no prior shape. It is a good input to Poisson surface reconstruction. For large photo collections or for a depth map per image, a depth map method with fusion is usually faster and easier to run in parallel.

## Pitfalls

- **Normal direction.** The normal must point toward the cameras. If refinement lets it turn away, the patch fails the angle test and is lost. Keep it in the half space that faces $R(p)$, for example with the slope form the code uses.
- **Patch scale.** The grid step must match about one pixel of $R(p)$ at the depth of the patch. A fixed step in scene units gives patches that are too large near the cameras and too small far away.
- **Flat texture.** NCC is undefined where the image is flat. Treat a zero variance as a failed match, not as a perfect one.
- **Grid outside an image.** If a grid point projects outside an image, that image cannot score the patch. Drop it from $V(p)$, do not compare a part of the grid.
- **Cells and drift.** Refinement can move a new patch out of the cell it was made for. Without a test like line L13, expansion can make patch after patch for the same empty cell.
- **Filter thresholds.** A distance $\rho$ that is too small removes good patches on curved surfaces; one that is too large keeps outliers.

## Implementations

## History

Furukawa and Ponce presented the method at CVPR 2007 and gave the full version in IEEE TPAMI in 2010. The TPAMI paper reports results on the Middlebury multi-view benchmark of Seitz et al. (2006), with its accuracy and completeness measures, and on other scenes. In that report the method was at the top for four of the six data sets of the benchmark. This is a benchmark result of that time, and the ranking depends on the version of the benchmark and on the methods submitted. The software, PMVS and later PMVS2 with CMVS for large collections, became a standard tool for dense reconstruction from photo collections.

## References
