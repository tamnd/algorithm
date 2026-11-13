---
tag: P120H7
kind: algorithm
slug: laplacian-of-gaussian
name: Laplacian of Gaussian
aliases:
- LoG
- Marr-Hildreth edge detector
area: graphics-and-signals/image-processing
level: advanced
summary: Filter an image with the Laplacian of a Gaussian, the sum of two separable filters, and mark the zero crossings of the result as edges. This is the edge detector of Marr and Hildreth.
solves: [edge-detection]
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, r: radius ceil(4 sigma) of the kernel}
  time: {worst: Θ(W H r), best: Θ(W H r)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, linear: true, separable: false, exact: false, in_place: false}
history:
  year: 1980
  people: [David Marr, Ellen Hildreth]
  note: Marr and Hildreth proposed in 1980 to find edges as the zero crossings of the Laplacian of a Gaussian smoothed image, as a model of early human vision.
prereqs: [gaussian-filter, edge-detection]
see_also: [canny-edge-detector, separable-filter, marching-squares, laplacian-pyramid, unsharp-masking, sift, continuous-wavelet-transform, finite-difference-method]
sources:
  - paper: doi:10.1098/rspb.1980.0020
    title: David Marr and Ellen Hildreth, Theory of edge detection, Proceedings of the Royal Society of London B 207, 187 to 217, 1980
    locator: the definition of the operator as the Laplacian of a Gaussian, the zero crossings as edges, and the approximation by a difference of two Gaussians
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 10.2, the subsection The Marr-Hildreth Edge Detector
  - paper: "Vincent Torre and Tomaso A. Poggio, On edge detection, IEEE Transactions on Pattern Analysis and Machine Intelligence 8(2), 147 to 163, 1986"
    locator: the analysis of zero crossings of second derivative filters, and the false edges at points where the gradient magnitude is at a minimum
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 7.2, Edges and contours (the Laplacian of Gaussian and its zero crossings)
---

The Laplacian of Gaussian, or LoG, is the filter that applies the Laplacian $\nabla^2 = \partial^2/\partial x^2 + \partial^2/\partial y^2$ to an image after smoothing with a Gaussian of scale $\sigma$. Since both operations are linear, they combine into one kernel, $\nabla^2 G_\sigma$. At an edge, the first derivative has a maximum, so the second derivative crosses zero. David Marr and Ellen Hildreth used this in 1980: their [edge detector](/edge-detection/) marks the pixels where the LoG output changes sign. The kernel is not separable, but it is the sum of two separable kernels, so the filter costs $\Theta(r)$ per pixel for a kernel of radius $r$. The zero crossings form closed curves, and the detector needs only one threshold.

## In plain words

Blur the image, then measure at each pixel how the brightness curves. On the dark side of an edge the brightness bends up, and on the bright side it bends down. So the curvature is positive on one side and negative on the other, and it passes through zero exactly at the edge. The detector looks for pairs of next pixels where the sign changes, and it marks the one that is nearer to zero. The amount of blur decides which edges you see: a small blur shows fine detail, a large blur shows only large shapes. A sign change with only a very small jump is probably noise, so it is not marked.

## The problem

The input is a gray image $I$ with $H$ rows and $W$ columns, a scale $\sigma > 0$ and a threshold $t \ge 0$. Pixel $(x, y)$ is a point sample at integer coordinates, with $x$ to the right and $y$ downward. There is one channel, with values that we treat as linear. A read outside the image returns the nearest border pixel (the clamp rule). There are two outputs. The first is the filtered image $L = I \star K$, the [correlation](/cross-correlation/) with a sampled LoG kernel $K$. The second is the mask of its zero crossings.

## The algorithm

**The kernel.** Let $r = \lceil 4\sigma \rceil$. The 1D Gaussian is $g[k] = e^{-k^2/(2\sigma^2)} / Z$ for $|k| \le r$, with $Z$ chosen so that the sum is 1. Let $\mu_2 = \sum_k k^2 g[k]$ and $\mu_4 = \sum_k k^4 g[k]$. The 1D second derivative kernel is

$$d_2[k] = a\, (k^2 - \mu_2)\, g[k], \qquad a = \frac{2}{\mu_4 - \mu_2^2}.$$

So $\sum_k d_2[k] = 0$ and $\sum_k k^2 d_2[k] = 2$, which makes $d_2$ return exactly 2 on the samples of $x^2$. The 2D kernel is

$$K[u, v] = d_2[u]\, g[v] + g[u]\, d_2[v] = a\, (u^2 + v^2 - 2\mu_2)\, g[u]\, g[v].$$

Since $g[u] g[v]$ is the sampled 2D Gaussian, $K$ is the sampled $\nabla^2 G_\sigma = (u^2 + v^2 - 2\sigma^2)\, G_\sigma / \sigma^4$, with the constants $2\sigma^2$ and $1/\sigma^4$ replaced by their discrete values $2\mu_2$ and $a$. Each of the two terms is an outer product, a [separable filter](/separable-filter/).

**Zero crossings.** For each pair of 4-neighbors $p$ and $q$, if $L(p)$ and $L(q)$ have opposite signs and $|L(p) - L(q)| \ge t$, the zero lies between them, and we mark the one of the two nearer to the zero, that is, the one with the smaller $|L|$. On a tie, we mark $p$, the first in scan order. A pixel with $L(p) = 0$ exactly is marked when its two neighbors along one axis have opposite signs and differ by at least $t$.

```pseudo id=main
LOG(I, σ)
L1  (g, d_2, r) ← the kernels above
L2  A ← I ⋆ d_2 along x, then ⋆ g along y
L3  B ← I ⋆ d_2 along y, then ⋆ g along x
L4  return L = A + B

ZERO-CROSSINGS(L, t)                        ▷ mark starts as all false
L5  for each pixel p and each q ∈ {p + (1, 0), p + (0, 1)} inside the image do
L6      if L(p) L(q) < 0 and |L(p) − L(q)| ≥ t then mark the one of p, q with smaller |L|, p on a tie
L7      if L(p) = 0 and L(p − (q − p)) L(q) < 0 and |L(p − (q − p)) − L(q)| ≥ t then mark p
L8  return mark
```

The detector of Marr and Hildreth is ZERO-CROSSINGS(LOG($I$, $\sigma$), $t$).

## Example

Take 6 rows of 16 pixels, each row $0, \ldots, 0, 100, \ldots, 100$ with 8 zeros, so the step is at $x = 7.5$. Let $\sigma = 1.5$, so $r = 6$. The image does not depend on $y$, so line L3 gives $B = 0$, and line L2 gives the 1D second derivative of each row. Rounded to two places, the row of $L$ is

$$0, 0, 0.06, 0.52, 2.59, 7.40, 11.19, 5.92, -5.92, -11.19, -7.40, -2.59, -0.52, -0.06, 0, 0.$$

It is positive on the dark side, negative on the bright side, and odd about $x = 7.5$. The only sign change is between columns 7 and 8, with a jump of $11.84 \ge t = 1$. The two values have the same size, so line L6 marks column 7, the first. Each row has exactly one edge pixel, half a pixel from the true edge.

If the step goes through a pixel center instead, with the row $0, \ldots, 0, 50, 100, \ldots, 100$ and the 50 at column 8, then $L$ is about 0 at column 8, with $8.56$ on its left and $-8.56$ on its right. Column 8 is the only marked pixel in each row.

On a disk of radius 8 in a $33 \times 33$ image, with $\sigma = 1.5$ and $t = 5$, all the marked pixels are within 1 pixel of the circle of radius 8, and they form a closed ring.

## Correctness

The [proof](proofs/correctness.md) shows three facts. First, the separable form of lines L2 to L4 equals the correlation with the 2D kernel $K$. Second, away from the border, $L$ is exactly $I_{xx} + I_{yy}$ on every quadratic image $I = c_{20} x^2 + c_{11} x y + c_{02} y^2 + c_{10} x + c_{01} y + c_{00}$, so $L$ is 0 on affine images and 4 on $x^2 + y^2$. Third, on a vertical step between two pixels, $L$ is odd about the step and has exactly one sign change in each row, so each row has exactly one marked pixel next to the step. The marking rule is checked in the tests against a rule stated per pixel.

## Complexity

Lines L2 and L3 each do two 1D correlations with $2r + 1$ taps, so the filter costs $4(2r + 1) W H$ multiplications and additions, $\Theta(W H r)$ in the worst case and in the best case. The direct 2D correlation with $K$ costs $(2r + 1)^2 W H$, which is $\Theta(W H r^2)$. Lines L5 to L7 do a constant amount of work per pixel, $\Theta(W H)$. The images $A$, $B$ and the mask take $\Theta(W H)$ extra space. With $r = \lceil 4\sigma \rceil$, the cost grows linearly in $\sigma$. An image pyramid, as in the [Laplacian pyramid](/laplacian-pyramid/), or the FFT makes large scales cheaper.

## Properties

- **Linear and rotation invariant.** The continuous operator $\nabla^2 G_\sigma$ is linear and does not depend on the direction of the axes, so it needs no direction for each pixel, unlike [Canny's detector](/canny-edge-detector/).
- **Sum zero.** $\sum K = 0$, so the output is 0 on a flat image and does not change when a constant is added to $I$.
- **Exact on quadratics.** The discrete kernel gives the exact Laplacian of every quadratic image.
- **Closed contours.** The zero set of a smooth function is made of closed curves or curves that end at the border, so the marked pixels form closed rings around regions. Canny edges, in contrast, stop at corners.
- **False edges.** A zero crossing of the Laplacian also occurs where the gradient magnitude has a minimum along the gradient, for example between two parallel edges. These crossings have a small slope of $L$, so a threshold on the jump removes most of them.
- **Edges move at corners.** Where an edge curves, the zero crossing of the Laplacian is not on the maximum of the gradient. At a corner of a square, the zero crossings round the corner off.
- **Band pass.** The frequency response of $\nabla^2 G_\sigma$ is $-|\omega|^2 e^{-\sigma^2 |\omega|^2 / 2}$, which is 0 at frequency 0 and has its peak at $|\omega| = \sqrt{2}/\sigma$.

## Variants and improvements

- **Difference of Gaussians.** Marr and Hildreth noted that the difference of two Gaussians with scales in the ratio of about 1.6 is close to the LoG. The difference of Gaussians costs two Gaussian filters, and [SIFT](/sift/) uses it at many scales.
- **Scale normalized LoG for blobs.** The response $\sigma^2 \nabla^2 G_\sigma \star I$ has its extreme value at the scale of a blob of the size of the scale, so the local extrema over position and scale detect blobs. This is a [feature detection](/feature-detection/) method, not an edge detector.
- **Subpixel contours.** Run [marching squares](/marching-squares/) on $L$ at the level 0, and the contour has a position between the pixels by linear interpolation.
- **Second derivative along the gradient.** Robert Haralick in 1984, and the definition of an edge in Canny's work, use the zero crossings of the second derivative along the gradient direction, not of the Laplacian. These lie on the maxima of the gradient magnitude, also where an edge curves.
- **Discrete Laplacian of a smoothed image.** Smooth with a [Gaussian filter](/gaussian-filter/), then apply a $3 \times 3$ Laplacian mask, such as the [finite difference](/finite-difference-method/) stencil with the center $-4$. This is simpler, but less exact than the kernel here.
- **Sharpening.** Subtracting a multiple of the Laplacian from an image sharpens it, which is a form of [unsharp masking](/unsharp-masking/).

## When to use it

Use the LoG detector when you want closed contours around regions, when you want a detector that has no direction step, or when you want blob or texture features at a chosen scale. Its output is also a good input for subpixel contours. If you need edges at the right place near corners and junctions, or one response per edge with a good rejection of noise, [Canny's detector](/canny-edge-detector/) is usually better. For the detection of edges at several scales at low cost, use a difference of Gaussians on a pyramid.

## Pitfalls

- **No threshold.** With $t = 0$, every sign change of the noise is a zero crossing, and a flat noisy region is full of them. In the tests, noise of standard deviation 5 gives crossings at $t = 0$ and none at $t = 4$.
- **Floating point zeros.** On a flat image, the floating point output is not exactly 0 but a tiny value of random sign. A threshold of at least a small positive value is needed.
- **Truncated kernel.** If you sample the continuous formula and cut it at a small radius, the sum of the kernel is not 0, and the filter responds to a flat image. Fix the moments after the truncation, as the kernel here does with $\mu_2$ and $a$, and use a radius of about $4\sigma$.
- **Both pixels of a crossing.** Marking both $p$ and $q$ gives edges 2 pixels wide.
- **The sign convention.** Some texts use $-\nabla^2 G$ (the Mexican hat, as a [wavelet](/continuous-wavelet-transform/)), which flips the signs. The zero crossings do not change, but code that uses the sign must agree on the convention.

## Implementations

## History

David Marr and Ellen Hildreth published "Theory of edge detection" in the Proceedings of the Royal Society of London in 1980. They argued that the smoothing should be a Gaussian, because it is the filter that is best localized in space and in frequency at the same time, and that the Laplacian is the lowest order derivative that does not depend on the direction. They related the operator to the receptive fields of cells in the retina and noted the approximation by a difference of two Gaussians. In 1986 Torre and Poggio analyzed the zero crossings of second derivative filters and showed the false edges at minima of the gradient. Canny's detector of the same year used the maxima of the gradient along its direction, and replaced the LoG as the most used edge detector.

## References
