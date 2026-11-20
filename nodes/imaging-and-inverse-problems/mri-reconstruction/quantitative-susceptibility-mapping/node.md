---
tag: 0BCC2T
kind: problem
slug: quantitative-susceptibility-mapping
name: Quantitative susceptibility mapping
aliases:
- QSM
- dipole inversion
area: imaging-and-inverse-problems/mri-reconstruction
level: advanced
summary: Recover the magnetic susceptibility map from the measured field map, which is its convolution with a dipole kernel that vanishes on a cone.
model: real-ram
prereqs: [mri-signal-equation, tikhonov-regularization]
see_also: [phase-unwrapping, image-deblurring, well-posed-problem, convolution-theorem, wiener-filter, total-variation-denoising, conjugate-gradient-method, poisson-equation]
sources:
  - paper: doi:10.1002/mrm.22187
    title: Ludovic de Rochefort, Tian Liu, Bryan Kressler, Jing Liu, Pascal Spincemaille, Vincent Lebon, Jianlin Wu and Yi Wang, Quantitative susceptibility map reconstruction from MR phase data using bayesian regularization, validation and application to brain imaging, Magnetic Resonance in Medicine 63(1), 2010
    locator: pages 194 to 206 (dipole inversion with a weighted data term and priors from regions of zero susceptibility and from the edges of the magnitude image; general locator for the details)
  - paper: doi:10.1002/mrm.21828
    title: Tian Liu, Pascal Spincemaille, Ludovic de Rochefort, Bryan Kressler and Yi Wang, Calculation of susceptibility through multiple orientation sampling (COSMOS), a method for conditioning the inverse problem from measured magnetic field map to susceptibility source image in MRI, Magnetic Resonance in Medicine 61(1), 2009
    locator: pages 196 to 204 (the field measured at several orientations of the object to B0, and the susceptibility from weighted linear least squares; general locator for the details)
---

Quantitative susceptibility mapping (QSM) is the problem of recovering the magnetic susceptibility $\chi(r)$ of tissue from the phase of MRI data. The tissue changes the main field $B_0$ a little, and the change is the convolution of $\chi$ with the field of a unit dipole. In Fourier space the convolution is a product with the kernel $D(k) = \frac13 - k_z^2 / |k|^2$, and $D$ is zero on a double cone at 54.7356 degrees to $B_0$. So the field does not see the frequencies of $\chi$ on that cone, and the inversion, called dipole inversion, is ill-posed. Methods fill the gap with a prior, as in other [deconvolution problems](/image-deblurring/), or measure the field at several orientations of the head (COSMOS, Liu et al. 2009). Iron in the brain, calcium and the oxygen in venous blood all change $\chi$, which is why the map is useful.

## In plain words

Every material becomes a weak magnet in a strong magnetic field. Iron becomes a slightly stronger magnet than water, and calcium a slightly weaker one. These small magnets change the field of the scanner nearby, and the change shows up in the phase of the MRI signal.

QSM works backward from the measured field change to the strength of the small magnets in each voxel. Each small magnet changes the field in a fixed pattern, with lobes along the field and a different sign to the sides. The measured field is the sum of all these patterns.

One family of patterns gives no field change at all, so the data cannot see it. QSM must guess that part, using prior knowledge, or rotate the head and scan again so that the hidden part changes.

## Definition

**The physical model.** Let $B_0$ point along $z$, and let $\delta(r) = (B_z(r) - B_0)/B_0$ be the relative field change. For an isotropic susceptibility with $|\chi| \ll 1$, to first order in $\chi$ and with the Lorentz sphere correction,

$$\delta = d * \chi, \qquad d(r) = \frac{3\cos^2\theta_r - 1}{4\pi |r|^3}, \qquad \hat\delta(k) = D(k)\, \hat\chi(k), \qquad D(k) = \frac13 - \frac{k_z^2}{|k|^2},$$

where $\theta_r$ is the angle between $r$ and $z$, and the [convolution theorem](/convolution-theorem/) turns the convolution into a product. $D(0)$ is not defined, so $\chi$ is determined at most up to a constant, and QSM gives values relative to a reference region. The model is an approximation: it ignores anisotropy of $\chi$ (white matter has some), effects of the microstructure, and terms of second order in $\chi$.

**From the data to the field.** The phase of the image at the echo time $\mathrm{TE}$ is $\varphi(r) = \varphi_0(r) \pm 2\pi \bar\gamma\, \Delta B(r)\, \mathrm{TE}$, with the sign set by the scanner convention. [Phase unwrapping](/phase-unwrapping/) removes the jumps of $2\pi$, and a fit over several echoes removes $\varphi_0$. The result is the total field. It is the sum of the local field, from $\chi$ inside the region of interest $\Omega$ (the brain), and the background field, from sources outside $\Omega$ such as the air in the sinuses. Background field removal estimates the local field $\delta$ inside $\Omega$.

**The discrete problem (dipole inversion).** On a grid of $N$ voxels with the periodic DFT $F$,

$$\delta = F^{-1} \operatorname{diag}(D)\, F \chi + e \quad \text{on } \Omega,$$

with noise $e$ whose variance depends on the magnitude of the image. Given $\delta$ on $\Omega$, find $\chi$. This page uses $D(0) = 0$ and real $\chi$.

## Variants

- **Single orientation.** One scan, the usual clinical case. A prior must fill the frequencies near the cone.
- **Several orientations (COSMOS).** The head is scanned at $n_o$ orientations to $B_0$. In the frame of the head each scan has its own kernel $D_i(k) = \frac13 - (k \cdot b_i)^2 / |k|^2$, where $b_i$ is the direction of $B_0$. The kernels have different cones, so the combined problem can be well conditioned.
- **Susceptibility tensor imaging.** For anisotropic tissue, $\chi$ is a symmetric $3 \times 3$ tensor in each voxel, with six unknowns, so at least six orientations are needed.
- **Total field inversion.** The background and local fields are fitted together, without a separate background removal step.
- **The field from several echoes.** A fit of phase against echo time gives the field and its noise variance, which become the weights of the data term.

## Examples

**The kernel by hand.** $D(1, 0, 0) = \frac13$, $D(0, 0, 1) = \frac13 - 1 = -\frac23$, $D(1, 0, 1) = \frac13 - \frac12 = -\frac16$ and $D(1, 1, 1) = \frac13 - \frac13 = 0$. Also $D(1, 7, 5) = \frac13 - \frac{25}{75} = 0$. The zero set is $3 k_z^2 = |k|^2$, that is $\cos^2\theta = \frac13$, the angle $\arccos(1/\sqrt3) = 54.7356$ degrees to the $z$ axis, the magic angle.

**A sphere (theorem under the model).** A ball of radius $a$ with uniform $\chi$ gives, outside the ball, the field of one dipole at its center: $\delta(r) = \chi a^3 (3\cos^2\theta - 1) / (3 |r|^3)$. This follows from the kernel, because $d$ is harmonic away from $0$ (see Reductions) and so its mean over a ball equals its value at the center. Inside the ball, with the Lorentz correction, $\delta = 0$. So the field outside the ball tells only $\chi a^3$, not $\chi$ and $a$ apart.

**A numerical example (measurement).** A $32^3$ phantom: an ellipsoid with $\chi = 0.02$ and three balls with $0.15$, $-0.1$ and $0.08$ (in arbitrary units), mean removed. The field is computed with the periodic model, and Gaussian noise with a standard deviation of 1 percent of the largest field value is added. The table gives $\|\hat\chi - \chi\|_2 / \|\chi\|_2$. The same model makes and inverts the data, so these errors are smaller than with real data.

| method | relative error |
|---|---|
| division by $D$ where $D \ne 0$, without noise | 0.246 |
| division by $D$ where $D \ne 0$, with noise | 3.08 |
| truncated k-space division, threshold 0.05, 0.1, 0.2, 0.3 | 0.482, 0.404, 0.401, 0.458 |
| Tikhonov in k-space, $\alpha = 10^{-4}, 10^{-3}, 10^{-2}, 0.03$ | 0.615, 0.422, 0.416, 0.510 |
| 3 orientations: $B_0$ tilted by 0, 25 degrees about $x$, 25 degrees about $y$ | 0.106 |
| 5 orientations: 0 and $\pm 25$ degrees about $x$ and about $y$ | 0.072 |

Without noise, all the error of the first row comes from the 153 grid frequencies (of $32^3$) where $D$ is exactly zero. They hold 6.1 percent of the energy of $\chi$, and $\sqrt{0.061} = 0.246$. The 8 low frequencies $(\pm1, \pm1, \pm1)$ alone hold 5.3 percent. With noise, division by the small values of $D$ near the cone makes the error 3.08. The single orientation methods trade this noise for a bias near the cone, and their best errors were 0.401 and 0.416. Three tilted orientations have no common zero on the grid; the smallest value of $\sum_i D_i(k)^2$ over $k \ne 0$ was 0.040.

## Known algorithms

| method | data | what it does |
|---|---|---|
| Truncated k-space division (TKD) | one orientation | divides by $D$ where $\lvert D \rvert > t$ and by $\pm t$ elsewhere; two FFTs, $O(N \log N)$; where $\lvert D \rvert < t$ it divides by $t$ in place of $\lvert D \rvert$, so it shrinks those frequencies, which gives streaks along the cone and values that are too small |
| Tikhonov in k-space | one orientation | $\hat\chi = F^{-1}[D \hat\delta / (D^2 + \alpha)]$, the closed form of [Tikhonov regularization](/tikhonov-regularization/) with the identity; $O(N \log N)$ |
| Weighted, Bayesian regularization (de Rochefort et al. 2010) | one orientation, the magnitude image | a data term weighted by the noise, with priors that regions of the background have zero susceptibility and that edges of $\chi$ match edges of the magnitude image; solved iteratively |
| Edge weighted $\ell_1$ and total variation | one orientation, the magnitude image | an $\ell_1$ penalty of the gradient, as in [total variation denoising](/total-variation-denoising/), with weights from the magnitude edges; solved by [conjugate gradients](/conjugate-gradient-method/) on a smoothed form or by [ADMM](/admm/) |
| COSMOS (Liu et al. 2009) | $n_o$ orientations | weighted linear least squares; with equal weights, $\hat\chi(k) = \sum_i D_i(k) \hat\delta_i(k) / \sum_i D_i(k)^2$ for each $k$, $O(n_o N \log N)$ |
| Learned methods | one orientation | a network trained on pairs of fields and maps; its accuracy is a measurement on its test data |

## Bounds

- **The forward operator (theorem).** In the continuous setting on $L^2(\mathbb{R}^3)$, the map $\chi \mapsto d * \chi$ is the Fourier multiplier $D$, with $-\frac23 \le D \le \frac13$, so its norm is $\frac23$, reached along $k_z$.
- **No bounded inverse (theorem).** $D$ is zero only on the cone, a set of measure zero, so the map is injective on $L^2$. But $|D|$ takes values as small as we like near the cone, and the inverse is the multiplier $1/D$, which is unbounded. So the solution does not depend continuously on the data, and the problem is not [well posed](/well-posed-problem/) in the sense of Hadamard.
- **How much of k-space is near the cone (theorem).** For directions uniform on the sphere, $u = \cos\theta$ is uniform on $[-1, 1]$, so the fraction of directions with $|D| < \varepsilon$ is $\sqrt{1/3 + \varepsilon} - \sqrt{1/3 - \varepsilon}$ for $\varepsilon \le \frac13$, about $\sqrt3\, \varepsilon$ for small $\varepsilon$. For $\varepsilon = 0.05, 0.1, 0.2$ this is 0.087, 0.175 and 0.365. On a $32^3$ grid the measured fractions were 0.122, 0.242 and 0.472, larger because the cube holds many frequencies along its diagonals, which lie on the cone.
- **A discrete null space (theorem).** On a cubic grid, every integer frequency with $2 k_z^2 = k_x^2 + k_y^2$, for example $(1, 1, 1)$, has $D = 0$. Any $\chi$ with its spectrum on these frequencies gives zero field, so no method can recover that part from one orientation.
- **Noise gain (theorem).** TKD with threshold $t$ multiplies the noise at each frequency by at most $1/t$. Tikhonov multiplies it by $|D|/(D^2 + \alpha) \le 1/(2\sqrt\alpha)$, the maximum of $x/(x^2 + \alpha)$ at $x = \sqrt\alpha$.
- **Several orientations (theorem).** At frequency $k$, the least squares estimate from $n_o$ orientations is unique if and only if $\sum_i D_i(k)^2 > 0$, and with white noise of variance $\sigma^2$ in each field its variance is $\sigma^2 / \sum_i D_i(k)^2$. Three orthogonal directions of $B_0$ are not enough: all three kernels vanish where $(k \cdot b_i)^2 = |k|^2/3$ for each $i$, which is $|k_x| = |k_y| = |k_z|$, the four diagonal lines. On the $32^3$ grid that left 121 common zeros, all on these lines (measurement).

## Reductions

- **Dipole inversion to deconvolution.** The field is a convolution of $\chi$ with $d$, so dipole inversion is a deconvolution with a known kernel, like [image deblurring](/image-deblurring/), and the [Wiener filter](/wiener-filter/) and Tikhonov regularization apply in k-space.
- **Background removal to a harmonic problem.** For $r \ne 0$, $d(r) = \frac{1}{4\pi} \partial_z^2 (1/|r|)$, because $\partial_z^2 (1/|r|) = (3 z^2 - |r|^2)/|r|^5$. Since $1/|r|$ is harmonic away from $0$, so is $d$. So the background field, made by sources outside $\Omega$, satisfies the Laplace equation inside $\Omega$, a [Poisson equation](/poisson-equation/) with zero right side. Methods such as SHARP and the Laplacian boundary value method use this fact.
- **Phase to field.** The field comes from the unwrapped phase, so QSM depends on [phase unwrapping](/phase-unwrapping/).
- **Several orientations to stacked least squares.** COSMOS stacks the $n_o$ diagonal systems, and the normal equations are diagonal in k-space.

## Applications

- **Iron in the brain.** Deep gray matter nuclei hold iron, which is paramagnetic ($\chi > 0$ relative to water). QSM measures it in studies of aging and of neurodegenerative diseases.
- **Calcium against blood.** Calcifications are diamagnetic ($\chi < 0$) and blood products are paramagnetic. Both look dark in magnitude images, and the sign of $\chi$ tells them apart.
- **Venous oxygen.** Deoxyhemoglobin is paramagnetic, so the susceptibility of veins depends on the oxygen saturation of the blood.
- **White matter.** Myelin is diamagnetic and anisotropic, which motivates susceptibility tensor imaging.

## References
