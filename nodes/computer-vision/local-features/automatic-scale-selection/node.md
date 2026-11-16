---
tag: D3NE89
kind: technique
slug: automatic-scale-selection
name: Automatic scale selection
aliases:
- Lindeberg scale selection
- scale-normalized derivatives
area: computer-vision/local-features
level: advanced
summary: Pick the scale of a feature at the extremum over scale of a derivative normalized by a power of the scale, so that the chosen scale follows the size of the structure.
prereqs: [scale-space-representation, laplacian-of-gaussian]
see_also: [difference-of-gaussians-detector, determinant-of-hessian-detector, harris-laplace-detector, harris-affine-detector, invariant-local-features, sift, surf, gaussian-pyramid]
sources:
  - paper: doi:10.1023/A:1008045108935
    title: Tony Lindeberg, Feature detection with automatic scale selection, International Journal of Computer Vision 30(2), 79-116, 1998
    locator: the sections on gamma-normalized derivatives, the scale invariance of their extrema, and blob detection with the Laplacian and the determinant of the Hessian
  - book: isbn:978-0-7923-9418-1
    title: Tony Lindeberg, Scale-Space Theory in Computer Vision, Kluwer Academic Publishers, 1994
    locator: the chapter on scale selection and blob detection over scale
  - paper: doi:10.1023/B:VISI.0000027790.02288.f2
    title: Krystian Mikolajczyk and Cordelia Schmid, Scale and affine invariant interest point detectors, International Journal of Computer Vision 60(1), 63-86, 2004
    locator: Section 2 (the characteristic scale and the comparison of the measures used to select it)
  - paper: doi:10.1023/B:VISI.0000029664.99615.94
    title: David G. Lowe, Distinctive image features from scale-invariant keypoints, International Journal of Computer Vision 60(2), 91-110, 2004
    locator: Section 3 (the DoG as an approximation of the scale-normalized Laplacian)
  - paper: doi:10.1561/0600000017
    title: Tinne Tuytelaars and Krystian Mikolajczyk, Local invariant feature detectors, a survey, Foundations and Trends in Computer Graphics and Vision 3(3), 177-280, 2008
    locator: the part on scale invariant detectors
---

Automatic scale selection picks, for each feature of an image, the scale $t = \sigma^2$ at which a normalized derivative of the [scale space](/scale-space-representation/) has a local extremum over scale. Plain derivatives of a smoothed image fall as the scale grows, so their maximum is always at the finest scale. Lindeberg multiplied each derivative of order $m$ by $t^{m\gamma/2}$. With this factor, a structure that is $s$ times larger has its extremum at a scale $s^2$ times larger, so the selected scale follows the size of the structure. The [DoG detector](/difference-of-gaussians-detector/), the [determinant of Hessian detector](/determinant-of-hessian-detector/), the [Harris-Laplace detector](/harris-laplace-detector/) and the scale step of [SIFT](/sift/) and [SURF](/surf/) all use this rule.

## In plain words

To measure how big a spot in an image is, look at it through a range of blurs, from weak to strong. A weak blur leaves the spot sharp but small compared to the blur window; a very strong blur washes it out. In between there is one blur that fits the spot best, and there a well chosen response is at its peak. Scale selection computes the response for each blur and keeps the blur where it peaks. The response must be corrected for the blur first, because blur alone makes every response smaller. With the right correction, a spot twice as large peaks at a blur twice as wide, so the chosen size grows with the spot.

## When it applies

The setting is the scale space $L(\mathbf x, t) = g_t \ast f$ of an image, where $g_t$ is the Gaussian of variance $t$. A $\gamma$-normalized derivative of order $m$ is

$$\partial_{\xi}^{m} L = t^{m\gamma/2} \, \partial_x^{m} L, \qquad \text{that is} \quad \partial_\xi = t^{\gamma/2} \partial_x .$$

Scale selection applies when the feature is measured by a differential expression $D$ that is homogeneous: each term is a product of derivatives with the same total order $M$. Examples are the Laplacian $\nabla^2 L$ ($M = 2$), the determinant of the Hessian $L_{xx} L_{yy} - L_{xy}^2$ ($M = 4$), the gradient magnitude ($M = 1$) and the Harris measure ($M = 4$). The normalized measure is $t^{M\gamma/2} D$.

**Why it works.** Let $f'(\mathbf x) = f(s\mathbf x)$ be a copy of $f$ made smaller by the factor $s$. Its scale space is $L'(\mathbf x, t) = L(s\mathbf x, s^2 t)$, and each derivative of order $m$ gets the factor $s^m$. So

$$t^{M\gamma/2} D'(\mathbf x, t) = s^{M(1 - \gamma)} \, (s^2 t)^{M\gamma/2} D(s\mathbf x, s^2 t).$$

The factor $s^{M(1-\gamma)}$ does not depend on $t$. So a local extremum over scale at $(\mathbf x_0, t_0)$ for $f$ is a local extremum at $(\mathbf x_0 / s, t_0 / s^2)$ for $f'$, for every $\gamma$. With $\gamma = 1$ the values at the two extrema are also equal, which lets a detector compare the strength of features of different sizes with one threshold.

It does not apply to structures with no size of their own. An ideal step edge or the corner of an infinite wedge looks the same at every magnification, so with $\gamma = 1$ its normalized response is constant over scale and there is no extremum.

## The template

```pseudo id=main
SELECT-SCALES(f, x, D, M, γ, t_1 < t_2 < ... < t_K)
L1  for k ← 1 to K do
L2      L_k ← g_{t_k} * f                       ▷ the scale-space level t_k
L3      R_k ← t_k^{M γ / 2} · D(L_k)(x)          ▷ the normalized measure at x
L4  S ← empty list
L5  for k ← 2 to K - 1 do
L6      if |R_k| > |R_{k-1}| and |R_k| > |R_{k+1}| then
L7          append t_k to S                     ▷ a characteristic scale of x
L8  return S
```

A detector runs the same test over position and scale at once: it keeps the points where $\lvert R \rvert$ is larger than at all 26 neighbours in the stack of levels, or it finds points in space at each level first and then tests them over scale, as Harris-Laplace does. The levels are usually spaced by a constant factor in $\sigma$, such as $2^{1/3}$, and a parabola through the three values around the extremum refines the scale.

## Classic examples

- **A Gaussian blob and the Laplacian.** For $f(\mathbf x) = \exp(-\lvert\mathbf x\rvert^2/(2t_0))$ the scale space at the center is $L = t_0/(t_0 + t)$ and $\nabla^2 L = -2t_0/(t_0+t)^2$. With $\gamma = 1$,
$$t \, \lvert\nabla^2 L\rvert = \frac{2 t t_0}{(t_0 + t)^2},$$
whose derivative in $t$ is zero at $t = t_0$. The selected scale is the variance of the blob, and the value there is $1/2$ for every $t_0$.
- **A Gaussian blob and the determinant of the Hessian.** At the center $L_{xx} = L_{yy} = -t_0/(t_0 + t)^2$ and $L_{xy} = 0$, so $t^2 \det H = t_0^2 t^2 / (t_0 + t)^4$. Its maximum is again at $t = t_0$, with the value $1/16$.
- **An elongated blob.** For a blob with the variances $a$ and $b$ along its two axes, $t^2 \det H$ at the center is $t^2 ab / ((a + t)^2 (b + t)^2)$, which is largest at $t = \sqrt{ab}$. The normalized Laplacian picks a different scale. For $a = 1$ and $b = 4$ the determinant picks $t = 2$ and the Laplacian $t \approx 1.75$; for $a = 1$ and $b = 9$ they pick $t = 3$ and $t \approx 2.08$.
- **A difference of Gaussians.** The DoG between the scales $t$ and $k^2 t$ is close to $(k^2 - 1) \, t \nabla^2 L / 2$, a normalized Laplacian times a constant. For the Gaussian blob, the DoG at the center is $t_0/(t_0 + t) - t_0/(t_0 + k^2 t)$, which is largest at $t = t_0 / k$, where the geometric mean $k t$ of the two variances is $t_0$. For $t_0 = 4$ and $k = 2^{1/3}$ the peak is at $t = 3.175$.
- **A sine wave.** For $f(x) = \sin(\omega_0 x)$ the derivative of order $m$ has the amplitude $\omega_0^m e^{-\omega_0^2 t / 2}$ in scale space. The normalized amplitude $t^{m\gamma/2} \omega_0^m e^{-\omega_0^2 t/2}$ is largest at $t = m\gamma / \omega_0^2$. The selected $\sigma$ is proportional to the wavelength $2\pi/\omega_0$; for $\omega_0 = 0.5$ and $\gamma = 1$ it is $t = 4$ for $m = 1$ and $t = 8$ for $m = 2$.
- **A blurred edge.** A step edge smoothed with variance $t_0$ has the gradient $1/\sqrt{2\pi(t_0 + t)}$ at the edge in scale space. With $\gamma = 1$ the normalized gradient grows with $t$ and has no maximum. With $\gamma = 1/2$ it is $t^{1/4}/\sqrt{2\pi(t_0 + t)}$, which is largest at $t = t_0$: the selected scale is the width of the edge. This is why $\gamma = 1/2$ is the usual choice for edges and $\gamma = 1$ for blobs.

## Variations

- **The choice of measure.** The Laplacian and the [DoG](/difference-of-gaussians-detector/) respond to blobs and also along edges; the [determinant of the Hessian](/determinant-of-hessian-detector/) responds less along edges. Mikolajczyk and Schmid compared several measures for the selection of the characteristic scale and kept the Laplacian for Harris-Laplace.
- **Extrema in position and scale together.** [SIFT](/sift/) and [SURF](/surf/) look for extrema of one measure in the three dimensions $(x, y, t)$. [Harris-Laplace](/harris-laplace-detector/) uses one measure in space (the Harris measure) and another over scale (the Laplacian).
- **Affine shape.** [Harris-affine](/harris-affine-detector/) selects a scale and then adapts an elliptic window, because a single scale cannot fit an elongated structure.
- **Pyramids.** Instead of smoothing the full image at every level, a [Gaussian pyramid](/gaussian-pyramid/) halves the image size at each octave, and the scale of a level is computed from its octave and its index.
- **Other values of $\gamma$.** $\gamma$ trades how the selected scale depends on the shape of the structure; values below $1$ are used for edges and ridges.

## Pitfalls

- **The selected scale is proportional to the size, not equal to it.** The constant depends on the measure and on the dimension. In 1D, $t \lvert L_{xx} \rvert$ of a Gaussian of variance $t_0$ is $t \sqrt{t_0}/(t_0 + t)^{3/2}$ at the center, which is largest at $t = 2t_0$, not at $t_0$. On the pixel grid, with the discrete Gaussian kernel, a second difference and $t_0 = 4$, the peak is also at $t = 8$.
- **Scale sampling.** With levels spaced by a factor $k$ in $\sigma$, the true extremum can fall between two levels, and a structure near the first or the last level has no extremum because it has no neighbour on one side. Use a parabola over scale and extend the range by one level on each side.
- **Small scales on the pixel grid.** For $t$ below about $1$ the sampled Gaussian smooths less than it should, and derivatives by finite differences are biased. Features at the finest levels are less reliable. A sharp corner or a step edge has no scale of its own, so on the grid its extremum is often at the finest level the detector allows.
- **Many scales at one place.** Nested structures, such as a dark spot inside a bright disk, give several extrema over scale at one point. Keep all local extrema, not only the largest one.
- **Neighbouring structures.** At coarse scales two nearby blobs merge into one, and the selected scale of each is then pulled by the other.
- **Border effects.** At large scales the smoothing kernel reaches past the image border, and the measure near the border depends on the border rule.

## Exercises

1. In $D$ dimensions, a Gaussian blob of variance $t_0$ has $\nabla^2 L = -D t_0^{D/2}/(t_0 + t)^{D/2 + 1}$ at the center. Show that $t\,\lvert\nabla^2 L\rvert$ is largest at $t = 2t_0/D$, and check the cases $D = 1$ and $D = 2$ against the examples on this page.
2. Repeat the elongated blob example for the normalized Laplacian and show that the maximum solves a polynomial equation in $t$. Check the value $t \approx 1.75$ for $a = 1$ and $b = 4$.
3. Show that the normalized gradient with $\gamma = 1$ of an ideal step edge is $1/\sqrt{2\pi}$ at every scale.
4. For the sine wave, find $\gamma$ such that the selected $\sigma$ for $m = 2$ is equal to $1/\omega_0$.
5. Show that the DoG between $t$ and $k^2 t$ of the Gaussian blob is largest at $t = t_0/k$.

## References
