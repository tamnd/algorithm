---
tag: VEDYF0
kind: algorithm
slug: lucas-kanade-method
name: Lucas-Kanade method
aliases:
- Lucas-Kanade optical flow
area: graphics-and-signals/image-processing
level: advanced
summary: Find the shift of a small window between two frames by least squares on the brightness constancy constraint, a 2 by 2 system per window, and refine it by warping and repeating.
solves: [optical-flow]
model: real-ram
complexity:
  vars: {m: the number of pixels in the window, k: the number of iterations}
  time: {worst: Θ(k m), average: Θ(k m), best: Θ(m)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: false, dense: false, local: true, iterative: true}
history:
  year: 1981
  people: [Bruce D. Lucas, Takeo Kanade]
  note: Lucas and Kanade registered images by Newton-Raphson steps on the squared difference over a region, using the image gradient, with a stereo application.
prereqs: [optical-flow, least-squares-problem, normal-equations, bilinear-interpolation]
see_also: [horn-schunck-method, harris-corner-detector, image-pyramid, image-registration, template-matching, newton-method-for-systems, eigenvalue, corner-detection]
sources:
  - paper: "Bruce D. Lucas and Takeo Kanade, An iterative image registration technique with an application to stereo vision, Proceedings of the 7th International Joint Conference on Artificial Intelligence (IJCAI), Vancouver, 1981, volume 2, pages 674 to 679"
    locator: the whole paper (the linearization of the difference, the one-dimensional and two-dimensional updates, the weighting, the iteration and the coarse-to-fine use of smoothed images)
  - paper: doi:10.1023/B:VISI.0000011205.11775.fd
    title: Simon Baker and Iain Matthews, Lucas-Kanade 20 years on, a unifying framework, International Journal of Computer Vision 56(3), 2004, 221 to 255
    locator: Section 2 (the forwards additive algorithm, its derivation as Gauss-Newton and its cost per iteration) and Section 3 (the compositional and inverse compositional forms)
  - paper: doi:10.1007/BF01420984
    title: John L. Barron, David J. Fleet and Steven S. Beauchemin, Performance of optical flow techniques, International Journal of Computer Vision 12(1), 1994, 43 to 77
    locator: the section on differential techniques (the local least-squares method, its eigenvalue threshold and its measured errors)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 9, Motion estimation (translational alignment, incremental refinement and optical flow)
---

The Lucas-Kanade method finds the shift $d = (u, v)$ of a small window between two frames as the least-squares solution of the brightness constancy constraint $I_x u + I_y v + I_t = 0$ over all pixels of the window. This is a 2 by 2 linear system $G d = b$ whose matrix $G = \sum \nabla I\, \nabla I^{\mathsf T}$ is the structure tensor of the window. The system is well posed when both [eigenvalues](/eigenvalue/) of $G$ are large, that is when the window has texture in two directions, which is the same test that [corner detectors](/harris-corner-detector/) use. Iterating the solve on the warped second frame, as Lucas and Kanade did, gives a Gauss-Newton method that recovers shifts of a few pixels to high accuracy, and an [image pyramid](/image-pyramid/) extends it to larger motions.

## In plain words

Pick a small square of pixels in the first frame, for example around a corner of an object, and ask where that square went in the next frame. At each pixel, the change of brightness in time and the slope of brightness in space give one equation for the two unknown parts of the motion. A square has many pixels, so you have many equations for two unknowns. They do not agree exactly, so you take the motion that fits all of them best in the least-squares sense, which needs only the solution of two equations in two unknowns. If the square holds only a straight edge, the equations cannot tell a slide along the edge, and the method must report failure. To handle larger motions, move the second frame by the current guess and solve again for the small rest, a few times.

## The problem

The input is two gray frames $E^1$ and $E^2$ with real values, a window $\Omega$ of $m$ pixels of $E^1$ (often a square of side $2r + 1$ around a chosen point), an iteration limit $k$ and a tolerance $\tau$. Pixel $x = (x_1, x_2)$ has integer indices and its center at $x + (1/2, 1/2)$. Off-grid values $E^2(x + d)$ come from [bilinear interpolation](/bilinear-interpolation/) with the indices clamped at the border. The output is a shift $d$ that minimizes

$$
\varepsilon(d) = \sum_{x \in \Omega} \big( E^2(x + d) - E^1(x) \big)^2,
$$

the sum of squared differences between the window and its shifted copy, or a report that the window has too little texture. Every pixel of the window is assumed to move by the same $d$. The linearization $E^2(x + d + \Delta) \approx E^2(x + d) + \nabla E^2(x + d) \cdot \Delta$ turns each step into a linear [least-squares problem](/least-squares-problem/) with the [normal equations](/normal-equations/)

$$
\underbrace{\sum_{x} g(x)\, g(x)^{\mathsf T}}_{G}\ \Delta = -\sum_{x} g(x)\, e(x), \qquad g = \nabla E^2(x + d),\ e = E^2(x + d) - E^1(x).
$$

## The algorithm

```pseudo id=main
LUCAS-KANADE(E¹, E², Ω, k, τ)
L1  d ← (0, 0)                                          ▷ or a guess from a coarser pyramid level
L2  repeat up to k times
L3      G ← the 2 × 2 zero matrix;  b ← (0, 0)
L4      for each pixel x of Ω do
L5          g ← ((E²(x+d+e₁) − E²(x+d−e₁))/2, (E²(x+d+e₂) − E²(x+d−e₂))/2)   ▷ central differences
L6          e ← E²(x + d) − E¹(x)
L7          G ← G + g gᵀ;  b ← b − g e
L8      if det G ≤ ε then return NOT ENOUGH TEXTURE
L9      Δ ← G⁻¹ b;  d ← d + Δ                           ▷ G⁻¹ b by the 2 × 2 closed form
L10     if |Δ| < τ then return d
L11 return d
```

With $G = \begin{pmatrix} a & b_{12} \\ b_{12} & c \end{pmatrix}$ and $b = (p, q)$, line L9 is $\Delta = \big( (cp - b_{12} q),\ (aq - b_{12} p) \big) / (ac - b_{12}^2)$. One pass of lines L3 to L9 with $d = 0$ is the classic one-step flow of a window. The loop of lines L2 to L10 is the iteration of Lucas and Kanade: the second frame is resampled at the new shift, so each step solves only for the residual motion. The threshold $\varepsilon$ in line L8 is usually a bound on the smaller eigenvalue of $G$ rather than on the determinant, which also rejects windows with one strong and one weak direction.

## Example

**One solve by hand.** A window of three pixels has gradients $g = (1, 0)$, $(0, 1)$ and $(1, 1)$ and time differences $e = -2$, $1$ and $-1$. Then $G = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ and $b = -\big(1 \cdot (-2) + 0 + 1 \cdot (-1),\ 0 + 1 \cdot 1 + 1 \cdot (-1)\big) = (3, 0)$. The determinant is $3$, so $\Delta = \big( (2 \cdot 3 - 1 \cdot 0)/3,\ (2 \cdot 0 - 1 \cdot 3)/3 \big) = (2, -1)$. Each pixel's constraint $g \cdot \Delta + e = 0$ holds: $2 - 2 = 0$, $-1 + 1 = 0$ and $2 - 1 - 1 = 0$. The eigenvalues of $G$ are 3 and 1, so the window has texture in both directions.

**A translated blob.** Frame 1 is the $24 \times 24$ image $100 \exp(-|x - c|^2 / 18)$, a Gaussian blob with $\sigma = 3$ centered at $c = (11.5, 11.5)$. Frame 2 is the same blob moved by the integer shift $(2, -1)$, so that $E^2(x + (2, -1)) = E^1(x)$ at every pixel. With the $13 \times 13$ window around pixel $(11, 11)$, the one-step solve from $d = 0$ gives $(1.8826, -0.9148)$, an error of $0.145$ pixels, because the linearization does not hold over two pixels. The iteration then gives errors of $0.00245$, $1.09 \times 10^{-5}$ and $4.87 \times 10^{-8}$ after steps 2, 3 and 4, and it reaches $(2, -1)$ to about $10^{-15}$ in 7 steps. At $d = (2, -1)$ the bilinear samples fall on pixels, $e = 0$ at every pixel, and the correction is 0, so the true shift is a fixed point.

**A straight edge.** If $E^1 = 3x_1 + 5x_2$, every gradient is $(3, 5)$, $G = m \begin{pmatrix} 9 & 15 \\ 15 & 25 \end{pmatrix}$ has determinant 0, and line L8 reports that the window has no texture across the edge direction. This is the aperture problem.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows three facts. First, line L9 solves the normal equations of the linear least-squares problem of the step, and when $G$ is nonsingular this is the unique minimizer of $\sum_x (g(x) \cdot \Delta + e(x))^2$; the residual is orthogonal to both columns. Second, $G$ is positive semidefinite, and it is singular exactly when all gradients in the window are parallel or zero, the aperture case. Third, if $E^2$ is an exact translation of $E^1$ by an integer shift $t$ on the pixels that the window reads, then $d = t$ is a fixed point of lines L3 to L9: every $e(x)$ is 0, so $b = 0$ and $\Delta = 0$. Whether the iteration reaches $t$ from $d = 0$ depends on the image; it is a Gauss-Newton method, which converges when the start is close enough and $G$ stays well conditioned, but has no global guarantee.

## Complexity

- **Per step.** Lines L4 to L7 do a constant number of bilinear samples and products per pixel, so one step costs $\Theta(m)$ for a window of $m$ pixels. Line L9 is $O(1)$.
- **Total.** $k$ steps cost $\Theta(km)$ in the [real RAM](/real-ram/); the best case is one step, $\Theta(m)$.
- **Space.** The five sums of $G$ and $b$ are running totals, so the extra space is $\Theta(1)$ beyond the frames.
- **Many windows.** For flow at $n$ points with windows of $m$ pixels, the cost is $\Theta(nkm)$. For a dense flow at every pixel with a square window, the sums $\sum I_x^2$, $\sum I_x I_y$, $\sum I_y^2$, $\sum I_x I_t$ and $\sum I_y I_t$ come from five [integral images](/integral-image/) or a [box blur](/box-blur/) in $O(1)$ per pixel, so one step of dense flow costs $\Theta(WH)$.
- **Inverse compositional form.** Baker and Matthews show that computing the gradients and $G$ once on the first frame, and composing the inverse of each update, gives the same first-order steps with the per-step cost reduced to the image differences and one product per pixel.

## Properties

- **Local.** The flow of a window depends only on the pixels that it reads.
- **Sparse by nature.** It gives a reliable answer only at points with texture in two directions; the matrix $G$ says where.
- **Equal to a corner measure.** $G$ is the structure tensor of the [Harris corner detector](/harris-corner-detector/). Shi and Tomasi chose points to track by the size of its smaller eigenvalue.
- **Subpixel.** The answer is a real shift, not limited to the pixel grid.
- **Translation only, as written.** The same scheme works for an affine or projective warp, with more parameters and a larger normal matrix, as in the original paper.

## Variants and improvements

- **Pyramidal Lucas-Kanade.** Run the iteration on a [Gaussian pyramid](/gaussian-pyramid/) from the top level down, doubling $d$ from one level to the next. A shift of 40 pixels is 5 pixels at level 3, inside the range of the linearization.
- **Weighted windows.** Weight each pixel, for example with a Gaussian, so that the center counts more. Lucas and Kanade allow a weight per pixel.
- **Affine and projective warps.** Solve for 6 or 8 parameters with the same Gauss-Newton step; this is the form used in [image registration](/image-registration/) and in tracking of planar patches.
- **Inverse compositional.** Precompute the gradient and $G$ on the template, as described by Baker and Matthews.
- **Robust losses.** Replace the squared difference with a robust function and solve by reweighted least squares, so that occluded pixels have less influence.
- **Dense flow.** Solve at every pixel with box sums, or combine the local data term with the global smoothness of the [Horn-Schunck method](/horn-schunck-method/).

## When to use it

Use Lucas-Kanade to track a set of well-chosen points through a video, as in feature tracking for structure from motion and video stabilization, and to refine a coarse estimate of a translation or a warp to subpixel accuracy. Pick the points with a [corner detector](/corner-detection/), and use a pyramid when the motion can exceed a pixel or two. Use [template matching](/template-matching/) or [phase correlation](/phase-correlation/) when the motion is large and no pyramid is available, and the [Horn-Schunck method](/horn-schunck-method/) when a flow is needed at every pixel, including flat regions.

## Pitfalls

- **Flat or straight windows.** A window with no texture or with a single edge direction gives a singular or nearly singular $G$, and the solve returns noise. Test the smaller eigenvalue, not only the determinant, against a threshold that is scaled to the image contrast.
- **Large motion without a pyramid.** The step is a linearization; beyond about one cycle of the dominant image frequency, it can move the wrong way.
- **Gradient of the wrong image.** The step needs the gradient of the image that is being shifted, at the shifted position, or a precomputed gradient with the inverse compositional rule. Mixing them gives a wrong sign or a biased step.
- **Brightness changes.** A gain or offset between frames enters $e$ and biases the shift. Subtract the window means, or add gain and bias to the unknowns.
- **Windows at the border.** Samples outside the image are clamped values, which do not move with the scene. Keep the window and its shift inside the image.
- **Many moving objects.** A window across a motion boundary has no single shift, and the solution is a blend of both.

## Implementations

## History

Lucas and Kanade published the method in 1981 at IJCAI as an image registration technique, with stereo matching as the application. They linearized the difference between an image and a shifted copy, derived the update from the gradient in one and in two dimensions, iterated it in the manner of Newton-Raphson, allowed weights per pixel, and suggested starting on smoothed images. Shi and Tomasi in 1994 chose the windows to track by the smaller eigenvalue of $G$. Barron, Fleet and Beauchemin found the local least-squares method among the most accurate in their 1994 comparison of optical flow techniques. Baker and Matthews in 2004 put the forwards additive form of Lucas and Kanade and its later variants into one framework and analyzed their cost.

## References
