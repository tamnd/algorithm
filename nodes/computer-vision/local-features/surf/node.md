---
tag: RH1WJP
kind: algorithm
slug: surf
name: Speeded up robust features
aliases:
- SURF
area: computer-vision/local-features
level: core
summary: A scale-invariant detector and descriptor that approximates Hessian filters and Haar wavelet responses with box filters on an integral image.
solves: [feature-matching]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, n: the number of keypoints}
  time: {worst: O(W H + n), average: O(W H + n), best: O(W H + n)}
  space: {extra: O(W H + n)}
properties: {deterministic: true, exact: false, rotation_invariant: true, scale_invariant: true, heuristic: true}
history:
  year: 2006
  people: [Herbert Bay, Tinne Tuytelaars, Luc Van Gool]
  note: Bay, Tuytelaars and Van Gool presented SURF at ECCV 2006. The journal version with Andreas Ess appeared in Computer Vision and Image Understanding in 2008.
prereqs: [integral-image, determinant-of-hessian-detector]
see_also: [sift, haar-wavelet, scale-space-representation, automatic-scale-selection, feature-matching, orb-features, kaze-features, image-stitching]
sources:
  - paper: doi:10.1007/11744023_32
    title: Herbert Bay, Tinne Tuytelaars and Luc Van Gool, SURF, speeded up robust features, European Conference on Computer Vision (ECCV), Lecture Notes in Computer Science 3951, 404-417, 2006
    locator: the sections on the Fast-Hessian detector (box filters of size 9 for sigma 1.2, the weight 0.9, the filter sizes per octave) and on the descriptor (orientation within 6s, Gaussian 2.5s, the 4 x 4 subregions and the 64 values)
  - paper: doi:10.1016/j.cviu.2007.09.014
    title: Herbert Bay, Andreas Ess, Tinne Tuytelaars and Luc Van Gool, Speeded-up robust features (SURF), Computer Vision and Image Understanding 110(3), 346-359, 2008
    locator: the sections on interest point detection (integral images, the Hessian with box filters, the scale space, the localization) and on description and matching (orientation, the Haar sums, the sign of the Laplacian)
  - paper: doi:10.1109/CVPR.2001.990517
    title: Paul Viola and Michael Jones, Rapid object detection using a boosted cascade of simple features, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), vol. 1, 511-518, 2001
    locator: the section on the integral image
  - paper: doi:10.1023/B:VISI.0000029664.99615.94
    title: David G. Lowe, Distinctive image features from scale-invariant keypoints, International Journal of Computer Vision 60(2), 91-110, 2004
    locator: Section 4 (the quadratic fit of the keypoint position and scale) and Section 6 (the SIFT descriptor that SURF follows)
---

Speeded up robust features (SURF) find keypoints in an image and describe each one by 64 numbers. The detector looks for blobs, at the maxima of the determinant of the Hessian over space and scale, like the [determinant of Hessian detector](/determinant-of-hessian-detector/). The trick is that SURF replaces the Gaussian second derivatives by box filters, sums over rectangles that an [integral image](/integral-image/) gives in four lookups. So each filter costs the same at every scale, and SURF never builds an image pyramid. The descriptor sums [Haar wavelet](/haar-wavelet/) responses, also box filters, over a grid of $4 \times 4$ squares around the keypoint, turned to a dominant direction. Bay, Tuytelaars and Van Gool designed SURF in 2006 as a faster relative of [SIFT](/sift/) with a shorter descriptor.

## In plain words

A blob is a small bright spot on a dark ground, or a dark spot on a bright ground. To find blobs of every size, SURF slides patterns of black and white rectangles over the image, a small pattern for small blobs and larger ones for large blobs. A table of running sums gives the sum of any rectangle with four reads, so a large pattern costs no more than a small one. Where the pattern answers more strongly than at all nearby places and sizes, SURF puts a keypoint. Around each keypoint it measures how the brightness changes to the right and downward, finds the main direction of the change, and turns a square grid to that direction. In each of 16 squares it adds up the changes and their sizes. The 64 sums, scaled to length 1, describe the keypoint.

## The problem

The input is a gray image $I$ with $W$ columns and $H$ rows. A pixel is $(u, v)$, with $u$ the column (to the right) and $v$ the row (down), and angles are measured from the $u$ axis toward the $v$ axis. The output is a set of keypoints $(u, v, s, \theta)$, with a position, a scale $s$ and an orientation $\theta$, each with a vector of 64 values. The goal, as for SIFT, is that the same scene point in two views gives a keypoint in both, at corresponding positions and scales, with descriptors that are near in the Euclidean distance, which is the input to [feature matching](/feature-matching/).

**Box Hessian.** The Hessian of the image smoothed at scale $\sigma$ has the entries $L_{uu}$, $L_{vv}$ and $L_{uv}$. SURF approximates them by box filters $D_{uu}$, $D_{vv}$ and $D_{uv}$ of odd size $L$. For $L = 9$ the filter $D_{vv}$ has three lobes, each 5 pixels wide and 3 pixels high, with the weights $+1, -2, +1$ along $v$; $D_{uu}$ is the same filter turned by 90 degrees; and $D_{uv}$ has four squares of $3 \times 3$ pixels with the weights $+1$ and $-1$, with a gap of one pixel between them. In general a lobe is $l_0 = L / 3$ pixels long and $2 l_0 - 1$ pixels wide. The filter of size 9 matches a Gaussian with $\sigma = 1.2$, and a filter of size $L$ matches the scale $s = 1.2 L / 9$. Each response is divided by $L^2$, so that responses at different sizes can be compared. The blob response is

$$\det(\mathcal{H}_{\text{approx}}) = D_{uu} D_{vv} - (0.9\, D_{uv})^2 .$$

The weight $0.9$ corrects for the box shapes: it is the ratio $\lVert L_{uv}(1.2) \rVert_F \lVert D_{vv}(9) \rVert_F / (\lVert L_{vv}(1.2) \rVert_F \lVert D_{uv}(9) \rVert_F) \approx 0.912$ of the Frobenius norms of the kernels.

**Octaves.** The first octave uses the sizes $9, 15, 21, 27$. Each next octave doubles the step between the sizes and the sampling step in the image: $15, 27, 39, 51$ with a step of 2 pixels, then $27, 51, 75, 99$ with a step of 4 pixels.

## The algorithm

```pseudo id=main
SURF(I)
L1  S ← the integral image of I
L2  for each octave, each filter size L and each sampled pixel (u, v), compute D_uu, D_vv, D_uv by box sums from S, divided by L^2
L3  d(u, v, L) ← D_uu D_vv - (0.9 D_uv)^2
L4  keep (u, v, L) if d > the threshold and d is larger than its 26 neighbors in (u, v, L); refine (u, v, L) by a quadratic fit; s ← 1.2 L / 9
L5  for each keypoint, take the Haar responses (dx, dy) of size 4s at the points of step s within a radius of 6s, weighted by a Gaussian with σ = 2.5s
L6  θ ← the direction of the largest sum of the responses whose angles lie in a window of π/3
L7  turn a square of side 20s to θ; in each of its 4 × 4 subregions, sum dx, dy, |dx| and |dy| of 5 × 5 Haar responses of size 2s, taken in the turned frame and weighted by a Gaussian with σ = 3.3s
L8  return the keypoints with their 64 sums, each vector divided by its length
```

The Haar response $dx$ of size $h$ is the sum of an $h \times h$ square on the right half minus the left half, and $dy$ the bottom half minus the top half. Each is two box sums. In line L7 the responses are taken with the axes of the image at the turned sample points and then turned into the frame of the keypoint, as Bay and his coauthors do; this is cheaper than turning the wavelets.

The sign of $D_{uu} + D_{vv}$, the sign of the Laplacian, tells bright blobs on a dark ground from dark blobs on a bright ground. SURF stores it with each keypoint, and a matcher compares only keypoints with the same sign.

## Example

**A disk.** A $64 \times 64$ image is 20 everywhere except a disk of radius 5 at $(32, 30)$ with the value 200. At the center, the filter of size 9 lies inside the disk, on a constant region, so all its responses are 0. The larger filters give $d = 2007.0$ for $L = 15$, $2165.1$ for $L = 21$ and $1483.7$ for $L = 27$, so the response peaks at $L = 21$, the middle layers of the first octave. This point is a maximum among its 26 neighbors, and the quadratic fit gives the scale $s \approx 2.55$, close to the scale $5 / \sqrt{2} \approx 3.5$ at which a Gaussian blob detector answers most strongly to a disk of radius 5. The sum $D_{uu} + D_{vv}$ is negative, so the sign of the Laplacian marks a bright blob. With the threshold 1, the detector also returns four much weaker points on the diagonals, about 11 pixels from the center, with a positive Laplacian; there, the dark ground next to the disk looks like a dark blob to the large filters.

**A ramp.** On the image $I(u, v) = 3u + 2v$, every Haar response of size $h$ is $(3, 2)$ times the same positive number, so every window that contains any response gives a sum in the direction $(3, 2)$, and $\theta = \operatorname{atan2}(2, 3) \approx 33.7°$.

**The weight 0.9.** With the Gaussian $\sigma = 1.2$ sampled on the $9 \times 9$ grid, the ratio of the Frobenius norms above is $0.9127$, which Bay and his coauthors round to $0.9$.

## Correctness

SURF is a heuristic; its claim of repeatability under changes of view is a benchmark result, not a theorem. The proof in `proofs/correctness.md` shows what the code computes:

- Each box sum from the integral image equals the sum of the pixels in the box, and the decomposition of each box filter into one or two large boxes equals the filter mask.
- Transposing the image swaps $D_{uu}$ and $D_{vv}$ and keeps $D_{uv}$, so the determinant map is transposed exactly. This is the discrete form of rotation invariance by 90 degrees.
- Line L4 returns exactly the strict local maxima above the threshold.
- On a ramp, the orientation is the direction of the ramp. Away from the border, the descriptor does not change when a constant is added to the image, has length 1, and does not change when the image is multiplied by a positive constant.

## Complexity

The model is the [real RAM](/real-ram/).

- Line L1 takes $O(W H)$ time.
- Lines L2 to L4 take $O(1)$ time per sample, since each box sum takes four reads, whatever the filter size. The first octave has $4 W H$ samples, and each next octave has a quarter as many, so the detector takes $O(W H)$ time for any number of octaves.
- Lines L5 to L7 take $O(1)$ time per keypoint, with 109 samples for the orientation and 400 for the descriptor, each a few box sums. The sliding window over the orientations takes $O(1)$ time for a fixed number of samples.

The total time is $O(W H + n)$ and the space is $O(W H + n)$. Because the integral image makes the cost of a filter independent of its size, large scales cost no more than small ones. This is the main source of the speed of SURF over SIFT, which smooths the image with ever larger Gaussians.

## Properties

- **Scale invariant.** The keypoint scale follows the blob size, and the sampling grid of the orientation and the descriptor scales with $s$.
- **Rotation invariant.** The descriptor is turned to $\theta$. The upright form U-SURF skips the orientation and is faster and more distinctive when the camera stays upright.
- **Contrast invariant.** The Haar responses do not change when a constant is added, and the final division removes a gain.
- **Approximate.** The box filters approximate Gaussian derivatives; they are not rotation invariant at angles other than multiples of 90 degrees, and the responses of the box filters are not exactly scale normalized.
- **Short descriptor.** 64 values, against 128 for SIFT, make the matching faster.

## Variants and improvements

- **U-SURF.** The upright form sets $\theta = 0$. Bay and his coauthors report that it is faster and works well for rotations up to about 15 degrees.
- **SURF-128.** It splits the sums of $dx$ and $|dx|$ by the sign of $dy$, and the sums of $dy$ and $|dy|$ by the sign of $dx$, which gives 128 values and is more distinctive.
- **SURF-36.** A $3 \times 3$ grid of subregions gives a shorter descriptor.
- **M-SURF.** The descriptor of [KAZE](/kaze-features/) uses overlapping subregions and two Gaussian weightings, which reduces the effects at the borders of the subregions.
- **Binary descriptors.** [ORB](/orb-features/) and [BRISK](/brisk-features/) use binary tests and the Hamming distance, and are much faster to compute and match.

## When to use it

SURF is a good choice when SIFT-like float descriptors are wanted at a lower cost, for [image stitching](/image-stitching/), recognition of objects and registration. SURF is patented, and OpenCV keeps it in its nonfree module, which led many users to ORB. On a phone or an embedded device, ORB is much faster: the ORB paper reports 15.3 ms for ORB, 217.3 ms for SURF and 5228.7 ms for SIFT on images of $640 \times 480$ pixels on one test computer. When accuracy matters more than speed, SIFT or [RootSIFT](/rootsift/) often matches better; [KAZE](/kaze-features/) keeps edges sharper in its scale space.

## Pitfalls

- **Filter size and scale.** The scale is $s = 1.2 L / 9$, not $L$. Mixing them breaks the sizes of the orientation and descriptor windows.
- **Normalization.** Without the division by $L^2$, larger filters always answer more strongly, and the scale selection fails.
- **Border.** A filter that leaves the image sees zeros (or copied edge pixels), and the responses near the border are not reliable. Keep the keypoints at least half the largest filter size away from the border.
- **Integer sizes.** Haar sizes of $4s$ and $2s$ must be rounded to even integers, and the sample points to pixels. These roundings make the descriptor change a little under rotation, even by 90 degrees.
- **Thresholds.** The threshold on the determinant depends on the range of the pixel values; a value that works for images in $[0, 1]$ finds almost everything in $[0, 255]$.
- **Gaussian weights.** The Gaussian for the orientation has $\sigma = 2.5s$ in the ECCV paper; implementations differ in this and other small choices, so descriptors from different libraries do not match each other.

## Implementations

## History

Bay, Tuytelaars and Van Gool presented SURF at ECCV 2006, and with Ess they gave the longer journal version in 2008. They combined three known parts: the [integral image](/integral-image/) that Viola and Jones had used for the Haar features of their face detector, the [determinant of the Hessian](/determinant-of-hessian-detector/) as a blob measure from the scale space work of Lindeberg, and the grid of local sums of the SIFT descriptor. SURF became one of the most used local features in the late 2000s. Faster binary features such as BRIEF, ORB and BRISK followed in 2010 and 2011, and the nonlinear scale space of KAZE in 2012 used a SURF-like descriptor.

## References
