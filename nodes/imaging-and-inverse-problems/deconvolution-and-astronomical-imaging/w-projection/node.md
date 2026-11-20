---
tag: 0A2NXG
kind: algorithm
slug: w-projection
name: W-projection
aliases:
- w-term correction
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: research
summary: Correct the non-coplanar baseline term in wide field radio imaging by convolving each visibility with a w-dependent Fresnel kernel during gridding.
model: real-ram
complexity:
  vars: {N: the number of pixels, m: the number of visibilities, S: the half-width of the kernel in cells, P: the number of distinct w values}
  time: {worst: Θ(m S^2 + P N log N), average: Θ(m S^2 + P N log N), best: Θ(m S^2 + P N log N)}
  space: {extra: Θ(N + P S^2)}
properties: {deterministic: true, iterative: false, linear: true, exact_with_full_kernel: true, gridding_is_adjoint_of_degridding: true}
history:
  year: 2008
  people: [Tim J. Cornwell, Kumar Golap, Sanjay Bhatnagar]
  note: "Cornwell, Golap and Bhatnagar (2008) wrote the w term of the measurement equation as a convolution in the uv plane, so that one 2D FFT images a wide field from a non-coplanar array."
prereqs: [aperture-synthesis, dirty-image, convolution-theorem, fast-fourier-transform]
see_also: [cotton-schwab-clean, hogbom-clean, multiscale-clean, van-cittert-zernike-theorem, nonuniform-fft, discrete-fourier-transform, parseval-theorem]
sources:
  - paper: doi:10.1109/JSTSP.2008.2005290
    title: "T. J. Cornwell, K. Golap and S. Bhatnagar, The noncoplanar baselines effect in radio interferometry, the W-projection algorithm, IEEE Journal of Selected Topics in Signal Processing 2(5), 2008"
    locator: "pp. 647 to 657 (the w term as a convolution in the uv plane, the kernel, its support and the comparison with faceting)"
  - paper: doi:10.1093/mnras/stu1368
    title: "A. R. Offringa et al., WSClean, an implementation of a fast, generic wide-field imager for radio astronomy, Monthly Notices of the Royal Astronomical Society 444(1), 2014"
    locator: "pp. 606 to 619 (w-stacking, the image-space alternative to w-projection)"
  - book: isbn:9783319444314
    title: "A. Richard Thompson, James M. Moran and George W. Swenson Jr., Interferometry and Synthesis in Radio Astronomy, third edition, Springer, 2017"
    locator: "Chapter 3, Analysis of the Interferometer Response (the measurement equation with the w term and the small-field approximation that drops it)"
---

W-projection makes the [dirty image](/dirty-image/) of a wide field from an array whose baselines do not lie in one plane, so that each visibility depends on its height $w$ as well as on $(u, v)$. It writes the $w$ term of the measurement equation as a convolution in the $uv$ plane by a kernel that depends only on $w$, applies that kernel while it puts the visibilities on the grid, and then images the whole field with one 2D [FFT](/fast-fourier-transform/). The plain dirty image of [aperture synthesis](/aperture-synthesis/) drops the $w$ term and is correct only for a small field. W-projection is not a deconvolution method: [Cotton-Schwab CLEAN](/cotton-schwab-clean/) calls it, and its adjoint, in each major cycle.

## In plain words

A radio array measures the sky through pairs of antennas. When the antennas do not lie in one plane, each measurement also carries a focus error that depends on the height difference of the pair, its w value. The error is zero at the center of the image and grows toward the edges, so a plain image blurs and weakens sources far from the center. W-projection removes the error before the image is made. It spreads each measurement over a small patch of grid cells, with a pattern that undoes the focus error for that w. Measurements with the same w use the same pattern, so each pattern is computed once. Then one Fourier transform makes the whole image. A larger patch gives a more accurate image and costs more time. The same patterns, used the other way, turn a sky model into predicted measurements.

## The problem

For an incoherent sky with brightness $I(l, m)$ in the direction cosines $(l, m)$, a baseline $(u, v, w)$ in wavelengths measures the visibility

$$V(u, v, w) = \iint \frac{I(l, m)}{\nu(l, m)}\, e^{-2\pi i\,(ul + vm + w(\nu - 1))}\, dl\, dm, \qquad \nu = \sqrt{1 - l^2 - m^2}.$$

With $w = 0$, or with $l^2 + m^2$ small, the last phase vanishes and $V$ is the 2D Fourier transform of $I / \nu$, which is the [Van Cittert-Zernike theorem](/van-cittert-zernike-theorem/). The dropped phase is $2\pi w(\nu - 1) \approx -\pi w (l^2 + m^2)$. It is small only when $|w|\,(l^2 + m^2) \ll 1$ over the field, which fails for long baselines, low frequencies and wide fields.

The discrete form used on this page has $n \times n$ pixels with signed offsets $p = (a, b)$, $-n/2 \le a, b < n/2$, and $l = b\,\Delta l$, $m = a\,\Delta l$. The grid cell in the $uv$ plane is $\Delta u = 1/(n\,\Delta l)$, and a visibility sits on the grid point $k = (k_v, k_u)$ with any real $w$. With $N = n^2$, the real sky $x$ and $y_p = x_p / \nu_p$, the model is

$$V(k, w) = \sum_p y_p\, G_w(p)\, e^{-2\pi i\, k \cdot p / n}, \qquad G_w(p) = e^{-2\pi i w (\nu_p - 1)} .$$

Measured visibilities $V_j$ at $(k_j, w_j)$ come with weights $\omega_j > 0$, and $\Omega = \sum_j \omega_j$. The exact dirty image is the adjoint of this model, $D_p = \frac1\Omega \sum_j \omega_j\, \mathrm{Re}\big(V_j\, \overline{a_{jp}}\big)$ with $a_{jp} = G_{w_j}(p)\, e^{-2\pi i\, k_j \cdot p/n} / \nu_p$. The direct sum costs $\Theta(mN)$ for $m$ visibilities. The task is to compute $D$, and the model visibilities of a given sky, with FFTs.

Real visibilities do not sit on grid points; a gridding kernel spreads each one onto the grid, as in the [nonuniform FFT](/nonuniform-fft/). Grid points here keep the $w$ step apart from that interpolation.

## The algorithm

On the grid, $V(\cdot, w)$ is the [DFT](/discrete-fourier-transform/) of the product $y \cdot G_w$. By the [convolution theorem](/convolution-theorem/), the DFT of a product is the circular convolution of the DFTs divided by $N$, so

$$V(k, w) = \sum_q K_w(q)\, V(k - q, 0), \qquad K_w = \frac1N\, \mathrm{DFT}(G_w).$$

The visibility at height $w$ is the visibility at $w = 0$ convolved with the kernel $K_w$. The kernel is a Fresnel pattern: $G_w$ is a pure phase, and $K_w$ spreads over a few cells for small $|w|$ and over more cells for large $|w|$. Gridding with the conjugate kernel is the adjoint operation, and it gives the dirty image.

```pseudo id=main
W-PROJECTION-IMAGE(vis, n, Δl, S)        ▷ vis: tuples (k, w, V, ω), offsets mod n
L1  F ← n × n grid of zeros
L2  for each visibility (k, w, V, ω) in vis do
L3      K ← W-KERNEL(n, Δl, w, S)          ▷ cached for each distinct w
L4      F[k - q] ← F[k - q] + ω · conj(K_q) · V for every offset q of K
L5  E ← N · IDFT2(F)
L6  return D_p ← Re(E_p) / (Ω · ν_p) for every pixel p

W-KERNEL(n, Δl, w, S)
L7  G_p ← exp(-2πi w (ν_p - 1)) for every pixel p
L8  Ĝ ← DFT2(G)
L9  return K_q ← Ĝ_q / N for the offsets q with |q_v|, |q_u| ≤ S
```

The prediction of model visibilities is the same steps in the other order: $V_0 = \mathrm{DFT2}(x/\nu)$ with one FFT, then $V_j = \sum_q K_{w_j}(q)\, V_0[k_j - q]$ for each visibility. This degridding step is the adjoint of lines L1 to L4, for every support $S$.

The support $S$ is the only accuracy setting. With $S \ge n/2$ the kernel is complete and both outputs are exact. In practice $S$ is a few cells, and it grows with $|w|$: the phase of $G_w$ has the local frequency $w\, l / \nu$ in $u$, so the kernel reaches about $|w|\, l_{\max} / \Delta u$ cells from its center. Production codes compute the kernels on an oversampled grid for a list of $w$ values, and take the kernel of the nearest listed $w$ for each visibility.

## Example

Take $n = 16$ and $\Delta l = 0.05$, so $|l|, |m| \le 0.4$ and $\Delta u = 1.25$ wavelengths. The sky has a point of flux 1 at the center pixel and one at the offset $(a, b) = (-7, 6)$, where $l = 0.3$, $m = -0.35$ and $\nu = 0.8874$. There are 40 visibilities with $k_u, k_v$ drawn from $\{-5, \dots, 5\}$ and $w$ drawn from $\{-6, -3, 0, 3, 6\}$, with seed 1 and unit weights. At the corner source and $w = 6$, the dropped phase is $2\pi \cdot 6 \cdot (1 - 0.8874) = 4.25$ radians, far from small.

The kernel for $w = 6$ has $|K(0,0)| = 0.380$ and $|K(q)| = 0.294$ at the four nearest offsets. Its total energy $\sum_q |K(q)|^2$ is 1. The part of the energy with $|q_v|, |q_u| \le S$ is 0.145 for $S = 0$, 0.717 for $S = 1$, 0.916 for $S = 2$, 0.983 for $S = 4$ and 0.995 for $S = 6$.

The table gives the largest error of the predicted visibilities, divided by the largest $|V_j|$, and the dirty image at the two sources. The exact dirty image has 1.1541 at the center and 1.4240 at the corner source.

| method | prediction error | image at center | image at corner source |
|---|---|---|---|
| no $w$ term | 0.925 | 1.1541 | -0.3269 |
| $S = 0$ | 1.235 | 0.2715 | 0.1634 |
| $S = 1$ | 0.545 | 1.6268 | 1.1433 |
| $S = 2$ | 0.321 | 1.0297 | 1.1408 |
| $S = 4$ | 0.134 | 1.1331 | 1.3394 |
| $S = 6$ | 0.060 | 1.1439 | 1.4378 |
| full kernel ($16 \times 16$) | 0 to rounding | 1.1541 | 1.4240 |

Without the $w$ term, the center source is exact, because $\nu = 1$ there, but the corner source comes out negative. A kernel of one cell is worse than no correction: it scales every visibility by $K(0, 0)$ and drops the rest of the kernel. From $S = 1$ on, the prediction error falls as the support grows, and the image values at the sources come close to the exact ones from $S = 4$ on.

## Correctness

On the grid the identity $V(k, w) = \sum_q K_w(q)\, V(k - q, 0)$ is exact, by the convolution theorem for the DFT. So degridding with the full kernel gives the exact model visibilities. Line L4 adds $\omega_j \overline{K_w(q)}\, V_j$ at $k_j - q$, and the inverse DFT turns this into $\omega_j V_j \nu_p \overline{a_{jp}}$ at pixel $p$, because $\overline{G_w(p)} = \sum_q \overline{K_w(q)}\, e^{-2\pi i\, q \cdot p/n}$. Line L6 divides by $\Omega \nu_p$ and takes the real part, so with the full kernel the output is the exact dirty image.

With a cut kernel, gridding and degridding stay exact adjoints of each other, so the image is the exact dirty image of the cut model. The kernel has unit energy by [Parseval's theorem](/parseval-theorem/), because $|G_w| = 1$. If $E_S$ is the energy kept by the cut, the error of each predicted visibility is at most $\sqrt{1 - E_S}\, \sqrt N\, \|y\|_2$ by the Cauchy-Schwarz inequality. This bound holds for every sky, and it is loose for a sky of a few points. The full proof is below.

## Complexity

One kernel costs a 2D FFT of $N$ pixels, $\Theta(N \log N)$, and there are $P$ distinct $w$ values, so the kernels cost $\Theta(P N \log N)$ and $\Theta(P S^2)$ space. Gridding $m$ visibilities with $(2S + 1)^2$ cells each costs $\Theta(m S^2)$, and the final FFT costs $\Theta(N \log N)$. The total is $\Theta(m S^2 + P N \log N)$, against $\Theta(m N)$ for the direct sum. In real use $m$ is in the millions and $S$ grows with $|w_{\max}|$, so the $m S^2$ term usually dominates, and the kernels are computed once for a list of $w$ values and kept.

## Properties

- **Linear.** Both outputs are linear in the data, and gridding is the exact adjoint of degridding for every support. This keeps the major cycles of Cotton-Schwab CLEAN consistent.
- **Exact with the full kernel.** On the grid model the only error is the cut of the kernel and, in practice, the rounding of $w$ to a listed value.
- **The kernel at $w = 0$ is a delta.** Then W-projection is plain gridding.
- **Symmetry in $w$.** $G_{-w} = \overline{G_w}$, so $K_{-w}(q) = \overline{K_w(-q)}$, and one kernel serves $\pm w$. A visibility with $w < 0$ can also be replaced by its conjugate at $(-u, -v, -w)$, because the sky is real.
- **Unit energy.** $\sum_q |K_w(q)|^2 = 1$ for every $w$.
- **The support grows with $|w|$ and with the field.** The kernel reaches about $|w|\, l_{\max} / \Delta u$ cells, which is $|w|\, n\, \Delta l\, l_{\max}$.

## Variants and improvements

- **Kernel with an anti-aliasing taper.** Real gridding uses a smooth kernel, often a prolate spheroidal function, to place off-grid visibilities. The w-projection kernel is then the transform of the taper times $G_w$, and the image is divided by the taper at the end. The taper also makes the kernel tails smaller.
- **W-stacking.** Offringa et al. (2014) grid the visibilities into several planes by $w$, transform each plane, multiply it by $\overline{G_w}$ in the image and add the planes. The error comes only from the spacing of the planes, and the cost does not grow with the kernel size.
- **Faceting.** The field is split into small facets, each imaged with its own tangent plane, where the small-field approximation holds. Cornwell, Golap and Bhatnagar (2008) compare it with w-projection.
- **Snapshots.** For a short time the baselines lie close to a tilted plane $w = \alpha u + \beta v$. The part of $w$ on that plane is a change of coordinates in the image, so the kernel corrects only the small distance of each baseline from the plane, and each snapshot image is regridded to common coordinates.
- **Other direction-dependent effects.** The same idea, a kernel in the $uv$ plane per baseline, also corrects the primary beams of the antennas.

## When to use it

Use W-projection when the dropped phase $\pi |w|\, (l^2 + m^2)$ is not small over the field: low frequencies, long baselines and wide fields, as for low-frequency arrays. Use it inside the major cycle of [Cotton-Schwab CLEAN](/cotton-schwab-clean/), which needs a matched pair of predict and image steps. When $|w|$ is very large, w-stacking or a mixed method can be cheaper, because the w-projection kernel grows with $|w|$. For a small field the plain dirty image is correct, and W-projection adds only cost.

## Pitfalls

- **A kernel that is too small.** The error falls slowly with $S$ because the kernel has tails from the sharp edge of the field. On the example, $S = 6$ still leaves 6 percent. Use a taper and an $S$ that grows with $|w|$.
- **A one-cell kernel.** Keeping only $K(0, 0)$ is worse than no correction, because it scales the visibility down.
- **Mismatched gridding and degridding.** If the predict step does not use the same kernels as the image step, the two are not adjoints, and the major cycles of CLEAN can stall or diverge.
- **The sign of $w$ and the conjugate.** Gridding uses $\overline{K_w}$ and degridding uses $K_w$. A sign error moves sources away from the center instead of correcting them.
- **The factor $1/\nu$.** The measurement equation divides by $\nu$, and the image step divides by $\nu$ again. Leaving it out gives wrong fluxes near the edge.
- **Memory.** Kernels for large $|w|$ on an oversampled grid are large, and there is one per listed $w$.

## Implementations

## History

The $w$ term was long handled by keeping the field small, or by splitting it into facets that each had their own tangent plane. Cornwell, Golap and Bhatnagar (2008) noted that the $w$ term is a multiplication in the image, so it is a convolution in the $uv$ plane, and they applied it while gridding. Their paper compared the method with faceting. Offringa et al. (2014) moved the correction back to the image in w-stacking, in the WSClean imager.

## References
