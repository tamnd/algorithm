---
tag: B3NX9Z
kind: technique
slug: left-right-consistency-check
name: Left-right consistency check
aliases:
- left-right check
- cross-checking of disparities
area: computer-vision/stereo-and-dense-reconstruction
level: core
summary: Compute disparity maps with each image as reference and invalidate the pixels whose two disparities do not map back to each other, which marks occlusions and many mismatches.
prereqs: [disparity, stereo-matching]
see_also: [cost-volume, semi-global-matching, block-matching-stereo, subpixel-disparity-refinement, forward-backward-error, mutual-nearest-neighbor-matching, depth-map-fusion, optical-flow]
sources:
  - paper: "Pascal Fua, A parallel stereo algorithm that produces dense depth maps and preserves image features, Machine Vision and Applications 6(1), 1993, 35-49"
    locator: the validity test that keeps a match only if the correlation from the left and from the right image gives the same pair
  - paper: doi:10.1109/TPAMI.2007.1166
    title: Heiko Hirschmüller, Stereo processing by semiglobal matching and mutual information, IEEE Transactions on Pattern Analysis and Machine Intelligence 30(2), 2008, 328-341
    locator: the part on the consistency check, the right disparity map from the same cost volume, and the separation of occlusions from mismatches
  - paper: doi:10.1023/A:1014573219977
    title: Daniel Scharstein and Richard Szeliski, A taxonomy and evaluation of dense two-frame stereo correspondence algorithms, International Journal of Computer Vision 47(1-3), 2002, 7-42
    locator: the part on refinement and on occlusion detection by cross-checking
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (cross-checking of disparity maps and the handling of occlusions)
---

The left-right consistency check computes a [disparity](/disparity/) map $d_L$ with the left image as reference and a map $d_R$ with the right image as reference, and keeps the left pixel $(u, v)$ only if the right pixel it points to points back: $|d_L(u, v) - d_R(u - d_L(u, v), v)| \le \tau$ for a small threshold $\tau$, usually 1 pixel or 0 for integer maps. A pixel whose scene point is hidden in the right image has no true match, so its two disparities seldom agree, and many plain mismatches in flat or repeated areas fail the test too. Fua (1993) used the test to keep only reliable matches. With a [cost volume](/cost-volume/), the right map comes almost free from the same costs, so [semi-global matching](/semi-global-matching/) and most local methods use the check before they fill the invalid pixels. The same idea appears in tracking as the [forward-backward error](/forward-backward-error/) and in feature matching as [mutual nearest neighbors](/mutual-nearest-neighbor-matching/).

## In plain words

Match each pixel of the left image into the right image. Then do the same thing the other way, from the right image back into the left. If a left pixel goes to some right pixel, and that right pixel comes back to the same left pixel, the match is probably right. If it comes back somewhere else, something is wrong: either the left pixel sees a part of the scene that the right camera cannot see, or the matcher was confused. Mark such pixels as unknown, and fill them later from good neighbors.

## When it applies

- The method can compute a disparity map with either image as reference. With a cost volume this costs only a second winner-takes-all on the sheared volume; with other methods it costs a second full run.
- Wrong disparities are worse than missing ones, as in 3D reconstruction, robot navigation or [depth map fusion](/depth-map-fusion/), where an invalid pixel is skipped but a wrong one creates a false surface.
- The scene has depth edges, so that some pixels are half occluded: seen by one camera only. These are the pixels next to the left side of a near object in the left image.

## The template

```pseudo id=main
LR-CHECK(d_L, d_R, τ)
L1  for each left pixel (u, v) do
L2      x ← u - round(d_L(u, v))
L3      if x < 0 or x ≥ W then valid(u, v) ← false
L4      else valid(u, v) ← |d_L(u, v) - d_R(x, v)| ≤ τ
L5  return valid
```

The right map uses the same sign: the right pixel $(x, v)$ matches the left pixel $(x + d_R(x, v), v)$. The holes are the threshold $\tau$ and what happens to the invalid pixels afterwards. A common fill takes, for each invalid pixel, the valid disparities nearest to it on its row to the left and to the right, and keeps the smaller one, because a half occluded pixel belongs to the background, which has the smaller disparity. A [median filter](/median-filter/) of the result removes the streaks this fill leaves. Hirschmüller (2008) also separates the two kinds of failure: an invalid pixel is a mismatch if some other disparity of its column would be consistent, and an occlusion otherwise, and the two kinds are filled differently.

**What the check guarantees.** If $d_L$ and $d_R$ are the true integer disparity maps of a scene, every left pixel whose scene point is visible in the right image passes with $\tau = 0$, because the right pixel sees the same point at the same depth. A left pixel whose point is hidden points to a right pixel that sees a nearer point, with a larger disparity, so it fails if that disparity is larger by more than $\tau$. So with true maps and $\tau = 0$ the check flags exactly the half occluded pixels and the pixels whose match is outside the right image. With estimated maps there is no such guarantee: two maps can agree on the same wrong match, for example on a repeated pattern, and the check then passes a wrong pixel.

## Classic examples

**A step edge.** Take a row of 10 pixels. A background plane has disparity 1 and a near object, the left pixels 5 to 7, has disparity 3. Suppose the matcher returns the true disparity wherever there is one and the background disparity elsewhere:

| left pixel $u$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| $d_L(u)$ | 1 | 1 | 1 | 1 | 1 | 3 | 3 | 3 | 1 | 1 |
| $x = u - d_L(u)$ | $-1$ | 0 | 1 | 2 | 3 | 2 | 3 | 4 | 7 | 8 |
| $d_R(x)$ | | 1 | 1 | 3 | 3 | 3 | 3 | 3 | 1 | 1 |
| valid | no | yes | yes | no | no | yes | yes | yes | yes | yes |

The right map is $d_R = (1, 1, 3, 3, 3, 1, 1, 1, 1, 1)$: the right pixels 2 to 4 see the near object. The pixels 3 and 4 fail: their background is hidden behind the object in the right image, and the number of such pixels is the jump of disparity, $3 - 1 = 2$. Pixel 0 fails because its match is outside the right image. The fill gives pixels 3 and 4 the smaller of the nearest valid values 1 (pixel 2) and 3 (pixel 5), which is the true background disparity 1.

**In stereo methods.** [Semi-global matching](/semi-global-matching/) computes $d_R$ from the right view of the same cost volume and checks with $\tau = 1$. [Block matching](/block-matching-stereo/) implementations such as OpenCV's add the check as an option. Learned methods use it to mark pixels for which the network output should not be trusted.

**Beyond stereo.** In [optical flow](/optical-flow/) and tracking, a point is tracked forward and then backward, and a large [forward-backward error](/forward-backward-error/) marks it as unreliable. In feature matching, keeping only [mutual nearest neighbors](/mutual-nearest-neighbor-matching/) is the same test on discrete matches. In multi-view stereo and [depth map fusion](/depth-map-fusion/), a depth is kept only if other views confirm it by projecting it back.

## Variations

- **Threshold.** $\tau = 0$ for integer maps keeps only exact agreement; $\tau = 1$ allows rounding and subpixel differences. With subpixel maps, round $u - d_L(u, v)$ to the nearest pixel or interpolate $d_R$.
- **One-sided check from one volume.** Instead of a second map, test whether the right pixel $x$ has its least cost at $u$ among all left pixels that can match it. This is the same test written on the cost volume.
- **Uniqueness constraint.** Allow each right pixel to be the match of at most one left pixel. This is weaker: it does not test that the right pixel points back.
- **Occlusion in the model.** Graph cut and dynamic programming methods can label pixels as occluded inside the optimization instead of after it.

## Pitfalls

- **Sign of the right map.** The right pixel $(x, v)$ matches the left pixel $(x + d_R, v)$. Using $x - d_R$ makes almost every pixel fail.
- **Not a correctness proof.** Agreement does not prove a match. On repeated textures both maps can make the same mistake.
- **Twice the work.** Without a cost volume, the right map needs a second full run of the matcher.
- **Filling from the wrong side.** Filling a half occluded pixel with the larger, foreground disparity grows the near object. Use the smaller one, or the one on the background side.
- **Thin structures.** Objects narrower than the window are often matched in one direction only and are removed by the check, together with real occlusions.

## References
