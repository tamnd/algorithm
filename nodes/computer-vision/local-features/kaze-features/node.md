---
tag: VCC3TB
kind: algorithm
slug: kaze-features
name: KAZE features
aliases:
- KAZE
- AKAZE
- accelerated KAZE
area: computer-vision/local-features
level: advanced
summary: Detect and describe features in a nonlinear scale space built by anisotropic diffusion, which blurs within regions but keeps their boundaries.
solves: [feature-matching]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, N: the number of levels, n: the number of keypoints}
  time: {worst: O(N W H + n), average: O(N W H + n), best: O(N W H + n)}
  space: {extra: O(N W H + n)}
properties: {deterministic: true, exact: false, rotation_invariant: true, scale_invariant: true, heuristic: true}
history:
  year: 2012
  people: [Pablo F. Alcantarilla, Adrien Bartoli, Andrew J. Davison]
  note: Alcantarilla, Bartoli and Davison presented KAZE at ECCV 2012 and named it for the Japanese word for wind, in tribute to Iijima.
prereqs: [anisotropic-diffusion, surf]
see_also: [sift, thomas-algorithm, scale-space-representation, determinant-of-hessian-detector, heat-equation, orb-features, brisk-features, feature-matching]
sources:
  - paper: doi:10.1007/978-3-642-33783-3_16
    title: Pablo F. Alcantarilla, Adrien Bartoli and Andrew J. Davison, KAZE features, European Conference on Computer Vision (ECCV), Lecture Notes in Computer Science 7577, 214-227, 2012
    locator: Section 3 (the conductivities g1, g2 and g3, the contrast k as the 70 percent point, the semi-implicit scheme), Section 4.1 (Equations 7 to 9), Section 4.2 (Equation 10 and the Scharr filters), Section 4.3 (the orientation and the M-SURF descriptor), Section 5 (O = 4 and S = 3 in the experiments, the repeatability of g2, Table 1 for the times)
  - paper: doi:10.1109/83.661190
    title: Joachim Weickert, Bart M. ter Haar Romeny and Max A. Viergever, Efficient and reliable schemes for nonlinear diffusion filtering, IEEE Transactions on Image Processing 7(3), 398-410, 1998
    locator: the whole paper (the AOS scheme and its properties)
  - paper: doi:10.1016/j.cviu.2007.09.014
    title: Herbert Bay, Andreas Ess, Tinne Tuytelaars and Luc Van Gool, Speeded-up robust features (SURF), Computer Vision and Image Understanding 110(3), 346-359, 2008
    locator: the section on orientation assignment (the sliding window of pi/3)
  - paper: doi:10.5244/C.27.13
    title: Pablo F. Alcantarilla, Jesus Nuevo and Adrien Bartoli, Fast explicit diffusion for accelerated features in nonlinear scale spaces, British Machine Vision Conference (BMVC), 13.1-13.11, 2013
    locator: the whole paper (AKAZE, a different method that follows KAZE)
---

KAZE finds and describes keypoints in a nonlinear scale space. [SIFT](/sift/) and [SURF](/surf/) build their scales with a Gaussian blur, which smooths edges as much as noise, so the position of a large structure moves and its outline fades. KAZE builds the scales with [anisotropic diffusion](/anisotropic-diffusion/) of the Perona and Malik type: the blur is strong inside flat regions and weak across strong edges. Each level comes from the one before by one step of an implicit scheme, the AOS scheme of Weickert, ter Haar Romeny and Viergever, which is stable for any step and needs only tridiagonal solves. On these levels KAZE finds the maxima of the scale-normalized [determinant of the Hessian](/determinant-of-hessian-detector/), gives each one an orientation as SURF does, and describes it with the 64 values of the M-SURF descriptor. AKAZE, by the same first author, is a different and faster method; see the variants below.

## In plain words

Make many blurred copies of the image, each more blurred than the one before. The blur is not the same everywhere: it is strong where the image is flat and weak where the brightness jumps, so outlines stay sharp while small noise goes away. In each copy, look for round spots where the brightness curves strongly in two directions, and keep a spot when it is stronger than its neighbors in the same copy and in the copies before and after. Around each spot, find the direction in which the brightness changes most. Then lay a grid around the spot in that direction, and in each of its 16 cells add up how the brightness changes. These 64 sums are the description.

## The problem

The input is a gray image with $W$ columns and $H$ rows, with values in $[0, 1]$; a pixel is $(u, v)$, with $u$ the column and $v$ the row, and angles grow from the $u$ axis toward the $v$ axis. The output is a set of keypoints $(u, v, \sigma, \theta)$ with a scale $\sigma$, an orientation $\theta$ and 64 values each, for [feature matching](/feature-matching/).

**Diffusion.** The levels $L$ evolve by the equation $\partial L / \partial t = \operatorname{div}(c \nabla L)$ with the conductivity $c = g(|\nabla L_\sigma|)$, where $L_\sigma$ is $L$ blurred by a small Gaussian. KAZE uses

$$g_2 = \frac{1}{1 + |\nabla L_\sigma|^2 / k^2},$$

one of the two functions of Perona and Malik. The contrast $k$ is the 70 percent point of the gradient magnitudes of the smoothed image: about 30 percent of the pixels have a gradient above $k$, and the diffusion across those edges is slow.

**Levels.** With $O$ octaves and $S$ sublevels, the level $i = o S + s$ has

$$\sigma_i = \sigma_0 2^{o + s / S}, \qquad t_i = \frac{1}{2} \sigma_i^2,$$

since a Gaussian blur of $\sigma$ is a linear diffusion for the time $\sigma^2 / 2$. All levels keep the full image size. The first level is the image blurred with a Gaussian of $\sigma_0$, and each next level is one implicit step of time $\tau = t_{i+1} - t_i$:

$$L^{i+1} = \left( I - \tau \sum_{l=1}^{m} A_l(L^i) \right)^{-1} L^i,$$

where $A_l$ is the diffusion along the axis $l$, with the weights $(c_j + c_n) / 2$ between neighbors. The AOS scheme replaces the inverse by $\frac{1}{m} \sum_l (I - m \tau A_l)^{-1}$, with $m = 2$, so that every system is tridiagonal and is solved by the [Thomas algorithm](/thomas-algorithm/).

**Detection.** The response is $L_\text{Hessian} = \sigma_i^2 (L_{uu} L_{vv} - L_{uv}^2)$, with the derivatives from $3 \times 3$ Scharr filters whose step grows with $\sigma_i$. Keypoints are the maxima over space and the two neighboring levels, above a threshold.

**Description.** The orientation is found as in SURF: the gradients at the points of a disk of radius $6 \sigma$, sampled with the step $\sigma$ and weighted by a Gaussian, are summed in a window of $\pi / 3$ that slides around the circle, and the longest sum gives $\theta$. The descriptor is M-SURF: a grid of $24 \sigma$ turned by $\theta$, cut into $4 \times 4$ subregions of $9 \sigma$ that overlap by $2 \sigma$. In each subregion, the turned gradients $(d_u, d_v)$ are weighted by a Gaussian of $2.5 \sigma$ around its center and summed into $(\sum d_u, \sum d_v, \sum |d_u|, \sum |d_v|)$; each of these four values is weighted by a Gaussian of 1.5 subregions around the keypoint, and the 64 values are scaled to unit length.

## The algorithm

```pseudo id=main
KAZE(I, σ_0, O, S, threshold)
L1  L_0 ← I blurred with σ_0; k ← the 70 percent point of |∇L_0|
L2  for i = 1, ..., O S - 1: c ← g_2(|∇ (L_{i-1} blurred with σ = 1)|, k)
L3      L_i ← one AOS step of time t_i - t_{i-1} from L_{i-1} with the conductivity c
L4  for each level i: the response σ_i² (L_uu L_vv - L_uv²) and the derivatives L_u, L_v, by Scharr filters
L5  keypoints ← the strict maxima of the response over 3 × 3 × 3, above the threshold, on the levels 1 to O S - 2
L6  for each keypoint (u, v, σ): θ ← the longest sum of the gradients in a window of π/3 over the disk of radius 6σ
L7      d ← the 64 values of M-SURF on the grid of 24σ turned by θ, scaled to unit length
L8  return the keypoints with their descriptors
```

Our code takes the exact 70 percent point of the sorted nonzero gradient magnitudes in place of a histogram, blurs with $\sigma = 1$ before the conductivity, and uses the step $\operatorname{round}(\sigma_i)$ for the Scharr filters. The paper searches for maxima in a window of $\sigma_i \times \sigma_i$ after a quick $3 \times 3$ check and refines the position to subpixel accuracy; our code uses the $3 \times 3 \times 3$ window only and keeps the pixel. The Gaussian of the orientation has $2.5 \sigma$, which is our choice, and the threshold $10^{-4}$ is our default for images in $[0, 1]$.

## Example

**One implicit step.** On the row $(0, 0, 1, 1)$ with $c = 1$ everywhere and $\tau = 0.5$, the system $(I - \tau A) x = f$ gives $x = (1/14, 3/14, 11/14, 13/14)$. The sum stays 2, and every value stays in $[0, 1]$. The step is stable however large $\tau$ is: on the two pixels $(0, 1)$ with $\tau = 1$, the result is $(1/3, 2/3)$, not an overshoot.

**The levels.** With $\sigma_0 = 1.6$ and $S = 3$, the levels have $\sigma = 1.6, 2.02, 2.54, 3.2, 4.03, 5.08, 6.4, \dots$ and the times $t = 1.28, 2.03, 3.23, 5.12, \dots$; the octave $o$ starts at $\sigma = 1.6 \cdot 2^o$.

**An edge.** On an $8 \times 24$ image with the values 40 and 200 on the two sides of a vertical edge, scaled to $[0, 1]$, and with $O = 2$ and $S = 2$, the jump between the two middle pixels is $0.157$ on the first level and still $0.111$ on the last level, of $\sigma \approx 4.53$. A Gaussian blur with the same $\sigma$ leaves a jump of only $0.055$. The total of the image does not change.

**A blob.** In a $32 \times 32$ image with a bright disk of radius 3 centered at $(15, 16)$, with $O = 2$ and $S = 3$, the detector finds the center $(15, 16)$ on the levels of $\sigma \approx 2.02$ and $\sigma = 3.2$.

## Correctness

KAZE is a heuristic, and its repeatability and matching quality are benchmark results. The proof in `proofs/correctness.md` shows that:

- The Thomas algorithm solves the tridiagonal systems of the implicit step, whose matrices are strictly diagonally dominant.
- Each implicit step, and so each AOS step, keeps the sum of the image, and every new value is a weighted mean of the old values, so the values stay between the old minimum and maximum, for every step size.
- For a small step, the implicit step agrees with the explicit step of the diffusion up to a term of order $\tau^2$.
- The keypoints are exactly the strict maxima of the response over $3 \times 3 \times 3$ above the threshold.
- A positive gain of the image does not change the levels apart from the same gain, nor the orientation, nor the descriptor, since $k$ scales with the image.
- A quarter turn of the image turns the levels, adds $\pi / 2$ to the orientation and does not change the descriptor.

## Complexity

The model is the [real RAM](/real-ram/). Let $N = O S$.

- Line L1 takes $O(W H \log(W H))$ time in our code, for the sort; a histogram, as in the paper, takes $O(W H)$.
- Lines L2 and L3 take $O(W H)$ time per level: a blur with a fixed kernel, and one tridiagonal solve of length $W$ for each row and of length $H$ for each column, each in linear time.
- Line L4 takes $O(W H)$ time per level, with five Scharr filters, and line L5 takes $O(W H)$ time per level with 26 comparisons per pixel.
- Lines L6 and L7 read a fixed number of samples per keypoint: 113 points for the orientation and $16 \cdot 81$ for the descriptor.

Apart from the sort, the total time is $O(N W H + n)$, and the space is $O(N W H)$ for the levels and their derivatives and $O(n)$ for the descriptors. All levels have the full size, while SIFT and SURF work on smaller octaves. The paper reports that KAZE takes more time than SURF and about the same time as SIFT, and that the nonlinear scale space is the most costly step.

## Properties

- **Edge preserving.** The diffusion is slow across edges with a gradient much larger than $k$, so the keypoints of large structures stay at the boundaries of objects.
- **Stable for any step.** The implicit AOS step keeps the range of the image for every $\tau$, so each level is one step, however long its time.
- **Scale invariant.** The scale of a keypoint comes from the maximum of the response over the levels, and the grid of the descriptor scales with $\sigma$.
- **Rotation invariant.** The grid and the gradients are turned by the orientation.
- **Contrast.** The descriptor is scaled to unit length and $k$ scales with the image, so a positive gain does not change it; the threshold of the detector is not invariant.

## Variants and improvements

- **Other conductivities.** The paper tests $g_1 = \exp(-|\nabla L_\sigma|^2 / k^2)$, $g_2$ and the function $g_3$ of Weickert, and reports that $g_2$ is slightly better for repeatability.
- **Upright descriptor.** Without the orientation step, the descriptor is faster, and the paper reports that it usually matches better when the images do not turn.
- **AKAZE.** Accelerated KAZE (Alcantarilla, Nuevo and Bartoli, BMVC 2013) is a different method. It builds the nonlinear scale space with fast explicit diffusion in place of AOS, with a pyramid that downsamples the octaves, and it describes the points by a binary descriptor (M-LDB). It is much faster than KAZE.
- **Gaussian scale space.** With $g = 1$, the diffusion is linear and the levels approach the Gaussian [scale space](/scale-space-representation/) of SIFT and SURF.

## When to use it

Use KAZE when the scenes have strong boundaries and much noise, or when the objects bend, and when time is not tight. On its benchmarks, the paper reports better repeatability than SIFT and SURF, with large gains under blur and noise. When speed matters, AKAZE, [ORB](/orb-features/) or [BRISK](/brisk-features/) are better choices.

## Pitfalls

- **AKAZE is not KAZE.** The two names are often mixed; the schemes, the pyramids and the descriptors are different.
- **The contrast $k$.** It depends on the image. A $k$ that is too small stops the diffusion at weak edges and keeps noise; a $k$ that is too large makes the space close to the Gaussian one.
- **The normalization.** The paper writes the factor $\sigma^2$. In the terms of Lindeberg this is the normalization with $\gamma = 1/2$: in the linear case, the response of a Gaussian blob of width $s$ peaks at $\sigma = s / \sqrt{3}$, where the factor $\sigma^4$ ($\gamma = 1$) gives $\sigma = s$. The keypoint scales are then smaller than the blob sizes.
- **The size of the step.** The AOS step is stable for any $\tau$, but its accuracy falls for long steps, since the splitting has an error of order $\tau^2$; the late levels of an octave are only rough approximations of the diffusion.
- **Cost.** Every level has the full image size, so the memory and the time grow with the number of levels.

## Implementations

## History

Perona and Malik introduced nonlinear diffusion with an edge-stopping conductivity in 1990. Weickert, ter Haar Romeny and Viergever gave the AOS scheme in 1998, which makes implicit steps cheap and stable. Alcantarilla, Bartoli and Davison joined the two with a detector and a descriptor in the style of SURF and presented KAZE at ECCV 2012. The name is the Japanese word for wind, in tribute to Iijima, the father of scale space. AKAZE followed at BMVC 2013 with fast explicit diffusion. OpenCV has both.

## References
