---
tag: 7MW0CV
kind: algorithm
slug: brisk-features
name: BRISK features
aliases:
- binary robust invariant scalable keypoints
area: computer-vision/local-features
level: advanced
summary: Scale-space AGAST keypoints with a binary descriptor from a fixed concentric sampling pattern, with long pairs giving the orientation and short pairs the bits.
solves: [feature-matching]
model: word-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, n: the number of keypoints, q: the number of pixels under the largest smoothing window of a pattern point}
  time: {worst: O(W H + n q), average: O(W H + n q), best: O(W H + n q)}
  space: {extra: O(W H + n)}
properties: {deterministic: true, exact: false, rotation_invariant: true, scale_invariant: true, heuristic: true}
history:
  year: 2011
  people: [Stefan Leutenegger, Margarita Chli, Roland Y. Siegwart]
  note: Leutenegger, Chli and Siegwart presented BRISK at ICCV 2011, at the same conference as ORB.
prereqs: [fast-corner-detector, brief-descriptor]
see_also: [orb-features, hamming-distance, scale-space-representation, image-pyramid, non-maximum-suppression, feature-matching, surf, superpoint]
sources:
  - paper: doi:10.1109/ICCV.2011.6126542
    title: Stefan Leutenegger, Margarita Chli and Roland Y. Siegwart, BRISK, binary robust invariant scalable keypoints, IEEE International Conference on Computer Vision (ICCV), 2548-2555, 2011
    locator: the section on scale-space keypoint detection (octaves and intra-octaves, the FAST 9-16 score, the FAST 5-8 mask for the layer below c0, the fits in position and scale) and the section on keypoint description (the sampling pattern, short and long pairs, the gradient, the 512 bits)
  - paper: doi:10.1007/978-3-642-15552-9_14
    title: Elmar Mair, Gregory D. Hager, Darius Burschka, Michael Suppa and Gerhard Hirzinger, Adaptive and generic corner detection based on the accelerated segment test, European Conference on Computer Vision (ECCV), Lecture Notes in Computer Science 6312, 183-196, 2010
    locator: the whole paper (AGAST, the segment test with an adaptive decision tree)
  - paper: doi:10.1007/11744023_34
    title: Edward Rosten and Tom Drummond, Machine learning for high-speed corner detection, European Conference on Computer Vision (ECCV), Lecture Notes in Computer Science 3951, 430-443, 2006
    locator: the section on the segment test
  - paper: doi:10.1109/CVPR.2012.6247715
    title: Alexandre Alahi, Raphael Ortiz and Pierre Vandergheynst, FREAK, fast retina keypoint, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 510-517, 2012
    locator: the whole paper (a retina-like pattern in the style of BRISK, orientation from symmetric pairs)
---

BRISK (binary robust invariant scalable keypoints) finds corners at many scales and describes each one by a string of 512 bits. The detector runs the [FAST](/fast-corner-detector/) segment test, in the faster AGAST form, on a pyramid of octaves and intra-octaves, and keeps the points whose FAST score is larger than at all neighbors in space and scale. The descriptor reads 60 smoothed intensities on four rings around the keypoint. Pairs of distant points give the direction of the local gradient, which turns the pattern; pairs of near points give the bits, one comparison each, as in [BRIEF](/brief-descriptor/). Descriptors are compared with the [Hamming distance](/hamming-distance/). Unlike [ORB](/orb-features/), whose tests are learned, BRISK uses a fixed, hand-designed pattern.

## In plain words

Look for corners in the image, and in smaller copies of the image so that large corners are found too. A corner is a point where many of the pixels on a small ring around it are all much brighter or all much darker. Keep a corner only where it is stronger than its neighbors and than the same place in the copies just smaller and just larger. Around each corner, read the brightness at 60 points on four circles, each blurred a little. Points that are far apart show which way the brightness rises, and that gives a direction. Turn the circles to that direction, and then compare each pair of nearby points: the brighter one gives a 1 or a 0. The 512 answers are the description of the corner.

## The problem

The input is a gray image $I$ with $W$ columns and $H$ rows; a pixel is $(u, v)$, with $u$ the column and $v$ the row, and angles grow from the $u$ axis toward the $v$ axis. The output is a set of keypoints $(u, v, t, \alpha)$ with a scale $t$ and an orientation $\alpha$, each with 512 bits, for [feature matching](/feature-matching/) by the Hamming distance.

**Scale space.** The pyramid has octaves $c_0, c_1, \dots$, each half the size of the one before, and intra-octaves $d_0, d_1, \dots$ between them. The layer $d_0$ is $c_0$ downsampled by $1.5$, and each next $d_i$ is half of $d_{i-1}$. So the scales are $t(c_i) = 2^i$ and $t(d_i) = 1.5 \cdot 2^i$.

**FAST score.** On each layer, the FAST 9-16 test asks whether 9 contiguous pixels of the circle of 16 are all brighter than $I(p) + T$ or all darker than $I(p) - T$. The score $s$ of a pixel is the largest threshold for which it is still a corner. A keypoint is a pixel with $s > T$ that is larger than the scores of its 8 neighbors and of the layers above and below near the same place. The paper fits a 2D quadratic to the scores in each of the three layers and a parabola along the log of the scale to refine the position and the scale. For $c_0$ it makes the scores of a virtual layer $d_{-1}$ below it with the FAST 5-8 mask on $c_0$.

**Pattern.** The 60 points $p_i$ lie on a center point and on four rings. In the OpenCV pattern, the radii are $0.85 \cdot (0, 2.9, 4.9, 7.4, 10.8)$, with $1, 10, 14, 15$ and $20$ points, all scaled by $t$. Each point is read after smoothing with a Gaussian whose $\sigma_i$ grows with the spacing of the points on its ring, so that the smoothed areas do not overlap much. Write $I(p_i, \sigma_i)$ for the smoothed value.

**Pairs.** Of the $60 \cdot 59 / 2 = 1770$ pairs, the short pairs $\mathcal{S}$ have $\lVert p_j - p_i \rVert < \delta_{\max}$ and the long pairs $\mathcal{L}$ have $\lVert p_j - p_i \rVert > \delta_{\min}$. The paper gives $\delta_{\max} = 9.75 t$ and $\delta_{\min} = 13.67 t$ for its pattern; in the units of the radii above the thresholds are $5.85 t$ and $8.2 t$, which give 512 short and 870 long pairs. The local gradient of a long pair, and their mean, are

$$g(p_i, p_j) = (p_j - p_i) \frac{I(p_j, \sigma_j) - I(p_i, \sigma_i)}{\lVert p_j - p_i \rVert^2}, \qquad g = \frac{1}{|\mathcal{L}|} \sum_{(p_i, p_j) \in \mathcal{L}} g(p_i, p_j),$$

and the orientation is $\alpha = \operatorname{atan2}(g_v, g_u)$. With the pattern turned by $\alpha$, the bit of a short pair is $b = [I(p_j^\alpha, \sigma_j) > I(p_i^\alpha, \sigma_i)]$.

## The algorithm

```pseudo id=main
BRISK(I, T)
L1  build the layers c_0, d_0, c_1, d_1, ...; compute the FAST 9-16 score s on each
L2  keep the points with s > T that beat their 8 neighbors and the layers above and below; refine the scale t
L3  for each keypoint (u, v, t), read the 60 pattern points scaled by t, each smoothed with σ_i t
L4      g ← the mean of (p_j - p_i)(I(p_j) - I(p_i)) / ‖p_j - p_i‖² over the 870 long pairs
L5      α ← atan2(g_v, g_u)
L6      read the 60 points again with the pattern turned by α
L7      for each of the 512 short pairs (i, j), bit ← [I(p_j) > I(p_i)]
L8  return the keypoints with their 512-bit descriptors
```

Our code simplifies the detector. It computes the FAST score on all layers without AGAST, compares a point with the largest score in a $3 \times 3$ neighborhood of the layers above and below, refines only the scale by the parabola, and has no layer $d_{-1}$; a missing layer counts as the score 0. The smoothing is a Gaussian-weighted mean of the pixels within $3\sigma$ of the point, and $\sigma \approx 1.3\, r \sin(\pi / n)$ for a ring of radius $r$ with $n$ points (0.5 for the center), which is our choice. The descriptor is the one of the paper.

## Example

**A square.** In a $64 \times 64$ image that is 30 everywhere except a square of value 200 with the corners $(20, 20)$ and $(43, 43)$, the pixel $(20, 20)$ is the corner pixel of the square. On its circle of 16 pixels, 11 contiguous pixels are outside the square and darker by $170$, so its FAST score is $170$; the pixel $(19, 19)$ outside the square has the score 0. Some neighbors along the edges have the same score 170, and the code keeps the first in raster order. The detector finds all four corners of the square at the scale $t \approx 1.22$, and again in the coarser layers. At $(20, 20)$ the long pairs give $\alpha \approx 44.5°$: the mean gradient points from the corner into the bright square, toward the lower right.

**The pattern.** The radii are $0, 2.47, 4.17, 6.29$ and $9.18$ pixels at $t = 1$, and our $\sigma$ values are $0.5, 0.99, 1.21, 1.70$ and $1.87$. The two outer rings are about 2.9 pixels apart, so the smoothed areas of neighboring points touch but do not cover each other.

**Rotation by 90 degrees.** On a $64 \times 64$ image turned by 90 degrees, the orientation of a point grows by about $\pi/2$, and the tests find fewer than 40 of the 512 bits different between the point and its turned copy, while two points about 6 pixels apart differ in more than 40 bits. The pattern has 10, 14 and 15 points on three rings, which are not multiples of 4, so a turned pattern does not fall on the same points, and the match is close but not exact.

## Correctness

BRISK is a heuristic; its matching quality is a benchmark result. The proof in `proofs/correctness.md` shows that:

- The FAST score of the code is the largest threshold for which the point is still a FAST 9-16 corner: the point is a corner for $T$ exactly when $T < s$.
- The kept points are those with $s > T$ that beat their neighbors in the layer and are not beaten by the layers above and below.
- On a linear ramp $a u + b v$ with exact smoothed values, each long pair gives the part of $(a, b)$ along the direction of the pair, and the mean is $M (a, b)$ for a fixed matrix $M$. For the pattern above $M \approx \operatorname{diag}(0.5014, 0.4986)$, so $\alpha$ is within 0.16 degrees of the direction of $(a, b)$.
- Multiplying the image by a positive number does not change the descriptor or the orientation, since every smoothed value is multiplied by it.

## Complexity

The model is the [word RAM](/word-ram/).

- Line L1 takes $O(1)$ time per pixel on each layer. The layers $c_i$ and $d_i$ have $W H / 4^i$ and $W H / (2.25 \cdot 4^i)$ pixels, so the sum is $O(W H)$.
- Line L2 takes $O(1)$ time per pixel, with 8 neighbors and 9 pixels in each of the two adjacent layers.
- Lines L3 and L6 take $O(q)$ time per keypoint for 60 smoothed values, where $q$ is the number of pixels under the largest Gaussian window. In the code $q$ grows with $t^2$; OpenCV approximates the Gaussians by box sums over an integral image, which makes the cost a constant.
- Lines L4, L5 and L7 take a constant time, with 870 long and 512 short pairs.

The total time is $O(W H + n q)$, and the space is $O(W H)$ for the layers and $O(n)$ words for the descriptors, 64 bytes each. The paper reports that BRISK is much faster than SURF while matching about as well on its benchmarks.

## Properties

- **Scale invariant.** The keypoint scale comes from the maximum of the FAST score over the layers, and the pattern scales with $t$.
- **Rotation invariant.** The pattern turns by $\alpha$, which is the direction of the mean gradient over the long pairs.
- **Contrast.** The bits compare two smoothed values, so a positive gain does not change them, and a constant offset changes none of the exact comparisons, only the rounding.
- **Fixed pattern.** There is no learning. The pattern is designed by hand, with dense short pairs near the center for the bits and long pairs across the whole pattern for the orientation.
- **Binary.** 512 bits are 64 bytes; the Hamming distance takes 8 XOR and popcount operations.

## Variants and improvements

- **AGAST.** Mair and his coauthors build the segment test as a decision tree that adapts to the image, which is faster than FAST and gives the same corners.
- **SU-BRISK.** A single-scale, upright form skips the scale space and the orientation, for speed when the camera does not turn or zoom.
- **FREAK.** Alahi, Ortiz and Vandergheynst use a retina-like pattern with more points near the center, learn the pairs, and compare the descriptor from coarse to fine.
- **ORB.** [ORB](/orb-features/) gets its orientation from the intensity centroid and learns its tests; it is the more common choice today.

## When to use it

Use BRISK for fast matching with binary descriptors when scale changes matter, for example in visual odometry with zoom or in mapping with large changes of distance. ORB is more common and usually just as good; [SIFT](/sift/) and learned features such as [SuperPoint](/superpoint/) match better when there is time.

## Pitfalls

- **The units of the thresholds.** The paper's $9.75 t$ and $13.67 t$ belong to the paper's pattern units; with the OpenCV radii above, the same split into 512 and 870 pairs comes from $5.85 t$ and $8.2 t$. Mixing the two gives a wrong number of bits.
- **Plateaus of the score.** At the corner of a sharp square, several pixels have the same FAST score. Without a rule for ties, a strict maximum test finds no keypoint at all.
- **Smoothing size.** Without smoothing, aliasing on the outer rings makes the bits unstable; with too much, neighboring points read the same value.
- **Border.** The outer ring at scale $t$ with its smoothing reaches about $16 t$ pixels; points nearer to the border have no descriptor.
- **Gradient on flat patches.** When $g$ is near 0 the orientation is unstable, and so are the bits.

## Implementations

## History

Leutenegger, Chli and Siegwart, at ETH Zurich, presented BRISK at ICCV 2011, the same conference where Rublee and his coauthors presented ORB. BRISK joined the AGAST corner test of Mair and his coauthors (2010) with a scale space search for the FAST score and a binary descriptor in the spirit of BRIEF, with a fixed pattern of rings. FREAK followed in 2012 with a retina-like pattern. BRISK is in OpenCV and was used in visual-inertial odometry, for example in the OKVIS system of Leutenegger and his coauthors.

## References
