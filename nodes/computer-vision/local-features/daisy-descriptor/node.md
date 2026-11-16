---
tag: HGVST3
kind: algorithm
slug: daisy-descriptor
name: DAISY descriptor
aliases:
- DAISY
area: computer-vision/local-features
level: advanced
summary: A dense descriptor that samples convolved orientation maps on concentric rings of points, so that it can be computed at every pixel quickly.
solves: [feature-matching]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, B: the number of orientation bins, Q: the number of rings, T: the number of points on a ring, R: the radius of the outer ring in pixels}
  time: {worst: O(W H B Q (R + T)), average: O(W H B Q (R + T)), best: O(W H B Q (R + T))}
  space: {extra: O(W H B Q)}
properties: {deterministic: true, exact: true, dense: true, rotation_invariant: false}
history:
  year: 2008
  people: [Engin Tola, Vincent Lepetit, Pascal Fua]
  note: Tola, Lepetit and Fua presented DAISY at CVPR 2008 and gave the full form in IEEE TPAMI in 2010.
prereqs: [feature-descriptor, gaussian-filter]
see_also: [sift, stereo-matching, feature-matching, histogram-of-oriented-gradients, surf, convolution, bilinear-interpolation, census-transform]
sources:
  - paper: doi:10.1109/TPAMI.2009.77
    title: Engin Tola, Vincent Lepetit and Pascal Fua, DAISY, an efficient dense descriptor applied to wide-baseline stereo, IEEE Transactions on Pattern Analysis and Machine Intelligence 32(5), 815-830, 2010
    locator: Section III (the orientation maps, the incremental convolution, Equation 1 for the histograms, the definition of the descriptor, Equation 2 for the sigma values, the ring radii, the rotation by shifting, Table I for the parameters, Table II for the times)
  - paper: doi:10.1109/CVPR.2008.4587673
    title: Engin Tola, Vincent Lepetit and Pascal Fua, A fast local descriptor for dense matching, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 1-8, 2008
    locator: the whole paper (the first form of the descriptor)
  - paper: doi:10.1023/B:VISI.0000029664.99615.94
    title: David G. Lowe, Distinctive image features from scale-invariant keypoints, International Journal of Computer Vision 60(2), 91-110, 2004
    locator: the section on the local image descriptor (the SIFT histograms that DAISY replaces by convolutions)
---

DAISY is a [feature descriptor](/feature-descriptor/) made to be computed at every pixel of an image. Like [SIFT](/sift/), it is built from histograms of gradient orientations, but it gets them in a different way. It first makes one map per orientation, which holds the positive part of the derivative in that direction. It then blurs each map with [Gaussian filters](/gaussian-filter/) of a few sizes. The value of a blurred map at a point is then a histogram bin, so a histogram is a read of $B$ maps at one point. The descriptor of a pixel reads such histograms at the pixel and at points on concentric rings around it, with more blur on the outer rings. All the work that nearby descriptors share is done once, in the convolutions, so a dense field of descriptors costs little more than the blur. Tola, Lepetit and Fua built it for [stereo matching](/stereo-matching/) with a wide baseline.

## In plain words

At each pixel, the brightness changes in some direction. Make 8 copies of the image, one for each of 8 directions, and in each copy keep only how much the brightness rises in that direction. Blur each copy a little, more, and much more. Now one blurred copy holds, at each point, how strong the edges near that point are in its direction. To describe a pixel, read the 8 copies at the pixel itself and at 8 points on each of 3 circles around it. The far circles read the copies that are blurred more. Each group of 8 values is scaled to the same length. The 25 groups together are the description.

## The problem

The input is a gray image $I$ with $W$ columns and $H$ rows; a pixel is $(u, v)$, with $u$ the column and $v$ the row, and angles grow from the $u$ axis toward the $v$ axis. The output is a descriptor $D(u, v)$ for every pixel on a grid, which can be compared by the Euclidean distance, as in [feature matching](/feature-matching/) or in dense stereo.

**Orientation maps.** For $B$ directions $\theta_o = 2 \pi o / B$, the orientation map is the positive part of the directional derivative,

$$G_o = \left( \cos \theta_o \frac{\partial I}{\partial u} + \sin \theta_o \frac{\partial I}{\partial v} \right)^+, \qquad (a)^+ = \max(a, 0).$$

Two opposite directions hold the two signs of the same derivative, so DAISY keeps the polarity of the edges.

**Convolved maps.** For $i = 0, \dots, Q - 1$, the layer $i$ is $G_o^{\Sigma_i} = G_{\Sigma_i} * G_o$, where $G_\Sigma$ is a Gaussian of standard deviation $\Sigma$ and

$$\Sigma_i = \frac{R (i + 1)}{2 Q}.$$

Since the convolution of two Gaussians is a Gaussian whose variances add, the layer $i + 1$ is the layer $i$ convolved with a Gaussian of standard deviation $\sqrt{\Sigma_{i+1}^2 - \Sigma_i^2}$.

**Descriptor.** Let $h_\Sigma(p) = (G_1^\Sigma(p), \dots, G_B^\Sigma(p))$ be the histogram at the point $p$, and $\tilde h$ the same vector scaled to unit length. The ring $i$ has radius $r_i = R (i + 1) / Q$ and the $T$ points $l_j = p + r_i (\cos \theta_j, \sin \theta_j)$ with $\theta_j = 2 \pi j / T$. Then

$$D(p) = \left( \tilde h_{\Sigma_0}(p), \tilde h_{\Sigma_0}(l_0(r_0)), \dots, \tilde h_{\Sigma_0}(l_{T-1}(r_0)), \dots, \tilde h_{\Sigma_{Q-1}}(l_{T-1}(r_{Q-1})) \right),$$

with $1 + Q T$ histograms of $B$ values. The center reads the first layer. The defaults are $R = 15$, $Q = 3$, $T = 8$ and $B = 8$, which give $25 \cdot 8 = 200$ values.

## The algorithm

```pseudo id=main
DAISY(I, R, Q, T, B, step)
L1  (g_u, g_v) ← the image gradient
L2  for o = 0, ..., B - 1: G_o ← max(0, cos θ_o g_u + sin θ_o g_v)
L3  for i = 0, ..., Q - 1: layer_i ← layer_{i-1} convolved with the Gaussian of σ = sqrt(Σ_i² - Σ_{i-1}²), with layer_{-1} = G and Σ_{-1} = 0
L4  for each pixel p on the grid of the given step
L5      the center histogram ← the B values of layer_0 at p, scaled to unit length
L6      for each ring i and each j: the histogram ← the B values of layer_i at p + r_i (cos θ_j, sin θ_j), scaled to unit length
L7      D(p) ← the 1 + Q T histograms in order
L8  return all D(p)
```

The paper takes the gradient with the kernels $[1, -1]$; our code uses central differences, repeats the border pixels for the gradient and the convolutions, and reads the maps between pixels by [bilinear interpolation](/bilinear-interpolation/). The paper notes that rounding the points to the nearest pixel works about as well. Our code also builds the descriptor turned by $k$ steps of $2 \pi / T$, as the paper describes: the ring points move by $k$ places and, when $B$ is a multiple of $T$, the bins of each histogram move by $k B / T$.

## Example

**The sigma values.** With $R = 15$ and $Q = 3$, the layers have $\Sigma = 2.5, 5$ and $7.5$, and the rings have the radii $5, 10$ and $15$. The incremental convolutions use $\sigma = 2.5$, then $\sqrt{25 - 6.25} \approx 4.33$, then $\sqrt{56.25 - 25} \approx 5.59$. The last kernel is smaller than a direct one of $\sigma = 7.5$, and it starts from maps that are already smooth.

**A ramp.** On the ramp $I(u, v) = 3 u + 2 v$, away from the border, the gradient is $(3, 2)$ at every pixel, so each orientation map is constant and the blur does not change it. With $B = 8$ the maps are

$$(3,\ 3.5355,\ 2,\ 0,\ 0,\ 0,\ 0,\ 0.7071),$$

since for example $(3 + 2)/\sqrt{2} \approx 3.5355$ for $\theta = 45°$ and $(3 - 2)/\sqrt{2} \approx 0.7071$ for $\theta = 315°$. The squared length is $9 + 12.5 + 4 + 0.5 = 26$, so every one of the 25 histograms is $(0.588, 0.693, 0.392, 0, 0, 0, 0, 0.139)$.

**A quarter turn.** When the image turns by 90 degrees, the gradient turns by 90 degrees, and the map $o$ of the turned image is the map $o - 2$ of the original. The descriptor of the turned image, read with $k = 2$, is equal to the descriptor of the original at the same point, within rounding.

## Correctness

DAISY is a definition, and its use for matching is a benchmark result. The proof in `proofs/correctness.md` shows that:

- The orientation maps are the positive parts of the directional derivatives, and two opposite maps are never both positive.
- In the continuous case the incremental convolutions give the same layers as direct ones; in the discrete code they agree to about $10^{-3}$ of the largest value away from the border.
- Each of the $1 + Q T$ histograms has unit length unless it is 0, and the descriptor has $(1 + Q T) B$ values.
- A constant offset of the image does not change the descriptor, and a positive gain does not change it either, since each histogram is scaled to unit length.
- A turn of the image by 90 degrees, with $B = T = 8$, maps the descriptor to the descriptor of the turned image read with $k = 2$.

## Complexity

The model is the [real RAM](/real-ram/).

- Lines L1 and L2 take $O(B)$ time per pixel.
- Line L3 does $B Q$ separable convolutions. The kernel of a step has radius $\lceil 4 \sigma \rceil = O(R)$, so each takes $O(W H R)$ time.
- Lines L4 to L7 read $(1 + Q T) B$ values per pixel, each by a bilinear read in $O(1)$ time, and scale $1 + Q T$ histograms.

The total time is $O(W H B Q (R + T))$ for a step of 1. The layers take $O(W H B Q)$ space. A dense field of descriptors takes $(1 + Q T) B$ values per pixel, so the paper keeps the layers and reads a descriptor only when it is needed. The paper reports 3.8 seconds for DAISY against 252 seconds for SIFT for the descriptors at every pixel of an $800 \times 600$ image.

## Properties

- **Dense.** The cost of the shared work is paid once per image and not once per descriptor.
- **Polarity.** The rectified maps keep the sign of the derivative, unlike a histogram of $|\nabla I|$ over angles modulo $\pi$.
- **Normalization per histogram.** Each histogram is scaled on its own, so that a part of the descriptor that falls on an occluding object does not change the scale of the other parts.
- **Isotropic kernels.** The blur is circular, so a turned descriptor needs no new convolutions, only a turn of the sampling points and a shift of the bins.
- **Not invariant by default.** For stereo, the descriptor is read without a turn; a rotation invariant form needs an orientation from elsewhere.

## Variants and improvements

- **Turned descriptors.** The paper computes the descriptor in several orientations by shifting, which is cheap since the layers stay the same.
- **Occlusion masks.** For stereo, the paper uses masks that switch off the parts of the descriptor that may be hidden, and it chooses the masks with the depth estimates.
- **Other normalizations.** The authors note that, outside stereo, a normalization of the whole descriptor may be better.
- **Dense SIFT and HOG.** [SIFT](/sift/) descriptors on a dense grid, and the [histogram of oriented gradients](/histogram-of-oriented-gradients/), give related dense features, with box or triangle weights in place of the Gaussian layers.

## When to use it

Use DAISY when a descriptor is needed at every pixel, as in wide-baseline stereo, dense correspondence, or optical flow with large motions. For sparse keypoints, [SIFT](/sift/) or [SURF](/surf/) give a scale and an orientation as well; for short, very fast codes, binary descriptors are better.

## Pitfalls

- **The center layer.** The center histogram reads the first, least blurred layer, not a layer of its own.
- **Border.** The outer ring reaches $R$ pixels from the pixel and its blur about $4 \Sigma_{Q-1}$ more; near the border the replicated pixels change the values.
- **Flat regions.** A histogram with no gradient is 0 and stays 0, and a weak one is scaled up to unit length, which makes noise look like structure.
- **Turning with few bins.** A turn by $k$ ring steps shifts the bins exactly only when $B$ is a multiple of $T$.
- **Memory.** Storing all dense descriptors takes $(1 + Q T) B$ values per pixel, 200 by default.

## Implementations

## History

Tola, Lepetit and Fua, at EPFL, presented DAISY at CVPR 2008 as a fast local descriptor for dense matching and gave the full form, with the stereo method and its occlusion handling, in IEEE TPAMI in 2010. They named it for its shape, which looks like a flower. The design takes the histograms of SIFT and GLOH and replaces the sums over cells by Gaussian convolutions of orientation maps, with larger kernels away from the center, as the geometric blur of Berg and Malik recommends.

## References
