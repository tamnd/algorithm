---
tag: 8EH0Z3
kind: algorithm
slug: plane-sweep-stereo
name: Plane sweep stereo
aliases:
- Collins plane sweep
- space-sweep stereo
area: computer-vision/stereo-and-dense-reconstruction
level: core
summary: Warp the other images onto a series of planes through the scene by homographies, score photo-consistency at each, and give every pixel the depth of its best plane.
solves: [multi-view-stereo, stereo-matching]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, N: the number of images, D: the number of planes}
  time: {worst: Θ(D N W H), average: Θ(D N W H), best: Θ(D N W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1996
  people: [Robert T. Collins]
  note: Collins (CVPR 1996) swept a plane through space and counted at each position how many back-projected features met there, which matched many images at once without rectification. Later work made it dense and ran it on the GPU.
prereqs: [homography, pinhole-camera-model, photo-consistency]
see_also: [multi-view-stereo, cost-volume, block-matching-stereo, patchmatch-stereo, depth-map-fusion, space-carving, stereo-rectification, semi-global-matching]
sources:
  - paper: doi:10.1109/CVPR.1996.517097
    title: Robert T. Collins, A space-sweep approach to true multi-image matching, IEEE Conference on Computer Vision and Pattern Recognition 1996, pages 358 to 363
    locator: the space-sweep method (a plane swept through the scene, back-projected features counted on each plane)
  - paper: doi:10.1109/CVPR.2007.383245
    title: David Gallup, Jan-Michael Frahm, Philippos Mordohai, Qingxiong Yang and Marc Pollefeys, Real-time plane-sweeping stereo with multiple sweeping directions, IEEE Conference on Computer Vision and Pattern Recognition 2007
    locator: Section 3 (the planes, the plane-induced homography of Eq. 3, the cost of Eq. 5 with a window and a gain ratio, best-cost selection and the depth of Eq. 7, the left and right camera subsets against occlusion) and Section 4.2 (the spacing of the planes)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (plane sweep and multi-view stereo)
---

Plane sweep stereo computes a depth map for one reference image from any number of calibrated images. It moves a plane through the scene in small steps. For each position of the plane, it maps every other image onto the reference image with the [homography](/homography/) that the plane induces, and compares the colors pixel by pixel. Where the plane passes through the true surface, the mapped images agree with the reference, so the cost is low. Each pixel takes the plane with the lowest cost over a small window, and its depth is where its ray meets that plane. The costs for all planes form a [cost volume](/cost-volume/), the same object that [block matching](/block-matching-stereo/) builds for a rectified pair. Plane sweep needs no rectification and uses all images at once, which is why it is a standard first step of [multi-view stereo](/multi-view-stereo/).

## In plain words

Hold a large glass sheet in front of a camera at some distance, and imagine that every camera projects its photo onto the sheet. Where a real object touches the sheet, all the projected photos show the same color at that spot, because they all saw the same point. Where the object is in front of or behind the sheet, the photos land in different places and disagree. Now move the sheet away from the camera step by step and note, for each pixel, the distance at which the photos agreed best. That distance is the depth of the pixel. The work is the same for every step, so a graphics card can do it very fast.

## The problem

**Input.**

- A reference image $I_0$ and other images $I_1, \dots, I_{N-1}$, all $W \times H$ gray images. Pixel $(u, v)$ is `img[v][u]`.
- The cameras. Camera 0 is $K_0 [I \mid 0]$, so its frame is the frame of the scene. Camera $k$ maps a point $X$ to $X_k = R_k X + t_k$ and has the intrinsic matrix $K_k$ (see [pinhole camera model](/pinhole-camera-model/)).
- A unit normal $n$ and offsets $d_1, \dots, d_D > 0$. Plane $j$ is the set of points with $n^\top X = d_j$. For fronto-parallel planes $n = (0, 0, 1)$ and $d_j$ is a depth.
- A window radius $r$.

**Output.** For each reference pixel $p$, the index $j^*(p)$ of the plane with the least window cost, and the depth $Z(p)$ of the point where the ray of $p$ meets that plane.

The window cost of plane $j$ at $p$ is $S_j(p) = \sum_{q} e_j(q)$ over the pixels $q$ of the $(2r+1) \times (2r+1)$ window of $p$ that lie inside the image, where $e_j(q)$ is the mean of $|I_0(q) - I_k(H_{jk} q)|$ over the cameras $k \ge 1$ in which $H_{jk} q$ falls inside the image. This is a [photo-consistency](/photo-consistency/) measure that assumes Lambertian surfaces. Other measures, such as [normalized cross-correlation](/normalized-cross-correlation/), fit in the same place.

## The algorithm

```pseudo id=main
PLANE-SWEEP(I_0, ..., I_{N-1}, cameras, n, d_1..d_D, r)
L1  for each pixel p do best[p] ← ∞
L2  for j ← 1 to D do
L3      for k ← 1 to N - 1 do H_k ← K_k (R_k + t_k n^T / d_j) K_0^-1
L4      for each pixel p = (u, v) do
L5          e(p) ← mean over the cameras k with H_k p inside I_k of |I_0(p) - I_k(H_k p)|, or a fixed cost if no camera sees p
L6      S ← the sum of e over the (2r+1) × (2r+1) window of each pixel
L7      for each pixel p do
L8          if S(p) < best[p] then best[p] ← S(p); index[p] ← j
L9  for each pixel p do depth[p] ← d_index[p] / (n^T K_0^-1 p̃)
L10 return index, depth
```

**Line L3, the homography.** A point $X$ on plane $j$ satisfies $n^\top X / d_j = 1$, so $X_k = R_k X + t_k = (R_k + t_k n^\top / d_j) X$. The reference pixel of $X$ is $\tilde p \sim K_0 X$, so $X$ is a multiple of $K_0^{-1} \tilde p$, and the pixel of $X$ in camera $k$ is $H_k \tilde p$. Here $\tilde p = (u, v, 1)$ and $\sim$ means equal up to a scale. The sign of the term $t_k n^\top / d_j$ depends on how the plane is written: with $n^\top X + d = 0$ it becomes a minus. Check the sign with one point before you trust a formula from another source.

**Line L5, the warp.** $H_k \tilde p$ has fractional coordinates, so $I_k$ is read by [bilinear interpolation](/bilinear-interpolation/). On a GPU the whole image $I_k$ is drawn onto the reference view with the texture unit, which is why this step is fast there. The code divides the sum by the number of cameras that see the point. Gallup et al. sum over all cameras and also multiply each image by a gain ratio, to allow for changes of exposure.

**Line L6, the window.** The window sum takes $O(1)$ per pixel with an [integral image](/integral-image/). The window is what makes the result stable: a single pixel matches many wrong planes by chance.

**Line L8, the choice.** This is winner-takes-all over the cost volume. The strict test keeps the first of two equal costs. A global method, such as [semi-global matching](/semi-global-matching/) or [graph cuts](/graph-cut-stereo/), can replace it.

**Line L9, the depth.** The ray of $p$ is the set of points $s K_0^{-1} \tilde p$. It meets $n^\top X = d$ at $s = d / (n^\top K_0^{-1} \tilde p)$, and the third entry of $K_0^{-1} \tilde p$ is 1, so $s$ is the depth $Z$.

**Plane spacing.** For a camera at the baseline $b$ from the reference, a fronto-parallel plane at depth $Z$ shifts pixels by the disparity $f b / Z$. Planes that are equally spaced in depth are too dense near the cameras and too sparse far away. Gallup et al. space them so that the image of a point moves by at most one pixel from one plane to the next, which for this case means equal steps of $1 / (f b)$ in $1 / Z$.

## Example

**One camera shift.** Take $f_x = f_y = 50$ and a second camera at the center $(0.2, 0, 0)$ with $R = I$, so $t = (-0.2, 0, 0)$. For $n = (0, 0, 1)$ the homography is $H = K (I + t n^\top / Z) K^{-1}$, which moves every pixel by $-50 \cdot 0.2 / Z = -10 / Z$ in $u$ and does not change $v$. The four planes at $Z = 2, 2.5, 5, 10$ move the pixel $(7, 3)$ to $(2, 3)$, $(3, 3)$, $(5, 3)$ and $(6, 3)$. If the pixel $(3, 3)$ of the second image shows the same point as $(7, 3)$ of the reference, the plane at $Z = 2.5$ wins at that pixel.

**Plane spacing.** With $f = 500$ pixels and $b = 0.1$ m, the disparity is $50 / Z$. From $Z = 1$ m (disparity 50) to $Z = 10$ m (disparity 5), steps of one pixel in disparity need 46 planes: $Z = 1, 1.0204, 1.0417, \dots, 10$. Equal steps in depth with the same step at 1 m, which is about 0.02 m, would need about 440 planes.

**Two planes.** The test file ray-casts a $24 \times 20$ scene for three cameras with $f = 40$: a textured back plane at $Z = 4$ and a textured rectangle at $Z = 2.5$ in front of it. One camera moves 0.4 to the right, one moves to the left and down (the $Y$ axis points down) and turns slightly. A sweep over the 9 depths $\{2, 2.25, 2.5, 2.8, 3.2, 3.6, 4, 4.5, 5\}$ with a $3 \times 3$ window gives the true depth at 453 of the 480 pixels; this map shows the index of the winning plane per pixel (2 is $Z = 2.5$, 6 is $Z = 4$):

```text
000666666666666666666666
666666666666666666666666
666666666666666666666666
666666666666666666666666
666666666666066666666666
666666666666333666666666
666666122222222366666666
666666122222222236666666
666666632222222220666666
666666632222222200666666
666666642222222226666666
666666641222222216666666
666666641222222211666666
666666666222221016666666
666666666666666666666666
```

(The last five rows are all 6 and are not shown.) The errors lie on the edges of the rectangle, where the window covers both depths and one camera sees the back plane behind the edge, and in the top left corner, which no other camera sees, so all planes tie and the first one wins. With a window of one pixel ($r = 0$), 113 pixels get a wrong plane.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has two parts.

1. **The homography lemma.** If $X$ lies on the plane $n^\top X = d$ and $\tilde p \sim K_0 X$, then $H \tilde p \sim K_k (R_k X + t_k)$, the image of $X$ in camera $k$. So $e_j(p)$ compares the reference with exactly the pixels that see the point where the ray of $p$ meets plane $j$, and line L9 returns the depth of that point.
2. **The choice.** After the iteration for plane $j$, $best[p] = \min_{i \le j} S_i(p)$ and $index[p]$ is the first index that reaches it. So the output is the winner-takes-all minimizer of the cost volume, with ties to the first plane.

The method is exact for the cost it defines. Whether the cost has its minimum at the true depth is a property of the scene: it needs texture, Lambertian surfaces, a point that all used cameras see, a window on which the surface is close to the swept plane, and a true depth close to one of the $d_j$. None of this is guaranteed, and the example shows the errors when it fails.

## Complexity

The model is the real RAM: the homography, the bilinear sample and the absolute difference each cost $O(1)$.

- **One plane.** Line L3 costs $O(N)$. Lines L4 and L5 cost $\Theta(N W H)$. Line L6 costs $\Theta(W H)$ with an integral image, independent of $r$. Lines L7 and L8 cost $\Theta(W H)$.
- **All planes.** $\Theta(D N W H)$ time in every case, since no step depends on the data.
- **Space.** The arrays best, index, $e$ and $S$ take $\Theta(W H)$. The code never stores the whole cost volume, which would take $\Theta(D W H)$; keep it only if a later step, such as [subpixel refinement](/subpixel-disparity-refinement/) or a global method, needs it.

The work for one plane is a texture warp and a box filter for each image, which a GPU does for every pixel in parallel. This is how Yang and Pollefeys, and later Gallup et al., ran the sweep in real time.

## Properties

- **Any number of images, no rectification.** The homography handles any camera pose. Adding an image adds one warp per plane.
- **Deterministic and data independent.** The same steps run for every plane and pixel.
- **Discrete depths.** The output depth is one of the planes. The error is at most half the spacing of the planes, unless a refinement step follows.
- **Fronto-parallel bias.** The window assumes that the surface is parallel to the plane over the window. A slanted surface makes the window cost high at every plane. Sweeping planes with the normal of the surface removes this bias.
- **No occlusion model.** A pixel that one camera does not see adds a high cost for the right plane.

## Variants and improvements

- **Feature space sweep.** Collins (1996) swept a plane through the scene and, at each position, back-projected the features of all images onto the plane and counted how many met in each cell. Cells with many votes are 3D features. It was made for sparse features.
- **Dense sweep on the GPU.** Yang and Pollefeys made the dense version above run in real time by doing the warps with graphics hardware, as Gallup et al. describe.
- **Several sweep directions.** Gallup et al. (2007) find the main surface normals of an urban scene (ground and facades) from sparse 3D points of [structure from motion](/structure-from-motion-problem/), sweep once for each normal, and pick per pixel the best depth and normal over all sweeps, with best cost or with a graph cut. This removes the fronto-parallel bias on planar scenes.
- **Occlusion.** Following Kang et al., Gallup et al. compute the cost once with the cameras on the left and once with those on the right of the reference, and keep the lower one, since the visibility of a point usually changes only once along a row of cameras.
- **Plane priors.** Gallup et al. also use the sparse points to sweep planes only near depths where the points suggest a surface, which saves time and helps on textureless walls.
- **Per-pixel planes.** [PatchMatch stereo](/patchmatch-stereo/) and its multi-view successors give every pixel its own plane and search the planes at random instead of sweeping a fixed set.
- **Fusion.** One sweep gives one depth map. [Depth map fusion](/depth-map-fusion/) combines the maps of many reference views into one model.

## When to use it

Use plane sweep when you have several calibrated images, for example frames of a video with known poses, and need a depth map fast, in particular on a GPU. It is the multi-view form of [block matching](/block-matching-stereo/) and fails in the same places: textureless areas, occlusions and slanted surfaces. For a rectified pair, block matching on the disparity is the same computation with a cheaper warp. When quality matters more than speed, use a per-pixel plane search such as [PatchMatch stereo](/patchmatch-stereo/) or a global method on the cost volume.

## Pitfalls

- **Plane sign convention.** $n^\top X = d$ and $n^\top X + d = 0$ give opposite signs in the homography. Test the homography by mapping one point of the plane before you sweep.
- **Which frame.** The plane must be given in the frame of the reference camera, and $R_k, t_k$ must map that frame to camera $k$. If the poses are given in a world frame, convert them first.
- **Equal steps in depth.** They waste planes near the cameras and miss depths far away. Space the planes in inverse depth, or by the pixel motion they cause.
- **Points behind a camera.** A homography also maps points behind camera $k$ into the image. Skip a sample when the third coordinate of $H_k \tilde p$ is not positive.
- **Cameras that do not see the point.** Averaging over only the cameras that see the sample, as the code does, keeps the cost comparable between pixels. A plain sum gives low costs to pixels near the border that few cameras see.
- **Gain changes.** The absolute difference assumes equal exposure. Use a gain ratio, as Gallup et al. do, or a measure like NCC.

## Implementations

## History

Collins (1996) introduced the space sweep as a way to match features across many images at once without rectification: a plane moves through the scene and features vote for the cells where their back-projected rays meet it. Yang and Pollefeys then made the sweep dense and ran it on graphics hardware, which turned plane sweep into a real-time depth method. Gallup, Frahm, Mordohai, Yang and Pollefeys (2007) swept planes in several directions found from sparse structure from motion, to handle the slanted ground and facades of street-level video in real time.

## References
