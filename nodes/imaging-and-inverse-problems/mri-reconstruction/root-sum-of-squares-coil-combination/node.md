---
tag: 4R76FY
kind: algorithm
slug: root-sum-of-squares-coil-combination
name: Root sum of squares coil combination
aliases:
- RSS coil combination
area: imaging-and-inverse-problems/mri-reconstruction
level: intro
summary: "Combines the images of the coils into one magnitude image: the square root of the sum of the squared coil magnitudes at each pixel, after optional noise whitening. Needs no coil maps."
model: real-ram
complexity:
  vars: {n: "the side of the n x n coil images", c: "the number of coils"}
  time: {worst: O(c^3 + c^2 n^2)}
  space: {extra: O(c^2 + n^2)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 1990
  people: [Peter B. Roemer, William A. Edelstein, Cecil E. Hayes, Steven P. Souza, Otward M. Mueller]
  note: Roemer and colleagues introduced the phased array with separate receivers and gave both the optimal combination with known sensitivities and the sum of squares combination without them.
prereqs: [coil-sensitivity-map]
see_also: [sense, g-factor, espirit, image-noise, cholesky-decomposition, generalized-least-squares, gauss-markov-theorem, mri-reconstruction-problem]
sources:
  - paper: doi:10.1002/mrm.1910160203
    title: P. B. Roemer, W. A. Edelstein, C. E. Hayes, S. P. Souza and O. M. Mueller, The NMR phased array, Magnetic Resonance in Medicine 16(2), 1990, 192 to 225
    locator: the optimal combination with the sensitivities and the noise matrix, and the sum of squares combination as its approximation (general locator)
  - paper: doi:10.1016/S1090-7807(03)00132-0
    title: Erik G. Larsson, Deniz Erdogmus, Rui Yan, Jose C. Principe and Jeffrey R. Fitzsimmons, SNR-optimality of sum-of-squares reconstruction for phased-array magnetic resonance imaging, Journal of Magnetic Resonance 163(1), 2003, 121 to 123
    locator: the sum of squares as the maximum likelihood estimate of the magnitude without known sensitivities, and its SNR at high SNR (general locator)
  - paper: doi:10.1002/mrm.1910380524
    title: Christakis D. Constantinides, Ergin Atalar and Elliot R. McVeigh, Signal-to-noise measurements in magnitude images from NMR phased arrays, Magnetic Resonance in Medicine 38(5), 1997, 852 to 857
    locator: the noncentral chi distribution of the sum of squares image and the noise-only bias (general locator)
  - paper: doi:10.1002/mrm.20713
    title: Peter Kellman and Elliot R. McVeigh, Image reconstruction in SNR units, a general method for SNR measurement, Magnetic Resonance in Medicine 54(6), 2005, 1439 to 1447
    locator: noise prewhitening with the measured noise covariance before the combination (general locator)
---

The root sum of squares (RSS) combination turns the $c$ complex images of a receive coil array into one magnitude image. At each pixel it takes the Euclidean norm of the vector of coil values. It needs no [coil sensitivity maps](/coil-sensitivity-map/) and no parameters. With a known noise covariance, the coils are first whitened. Roemer and colleagues gave it in 1990 together with the optimal combination that needs the maps. RSS is a combination of fully sampled coil images, not a parallel imaging method: it does not replace skipped samples. Without noise it returns the object magnitude times the norm of the coil maps (a theorem), so its image carries the shading of the coils.

## In plain words

Each coil gives its own picture of the same body. A coil sees the parts near it brightly and the far parts dimly, and it adds its own phase. RSS ignores the phases and adds up the brightness of all coils at each point, in the way the length of an arrow is found from its parts. Where at least one coil sees a point well, the point is bright in the result. The method needs nothing but the coil pictures.

## The problem

The input is the $c$ coil images $m_1, \ldots, m_c$ of size $n \times n$, and optionally the $c \times c$ noise covariance $\Psi$ between the coils. At pixel $p$ the model is $v = \rho s + \eta$, where $v_k = m_k(p)$, $\rho$ is the object value, $s$ the vector of map values and $\eta$ the noise. The output is a real nonnegative image. The plain combination is $\sqrt{\sum_k |m_k(p)|^2}$; the prewhitened one is $\sqrt{v^H \Psi^{-1} v}$.

## The algorithm

```pseudo id=main
RSS-PREWHITENED(m, Psi)               ▷ Psi = I gives the plain RSS
L1  L <- Cholesky factor of Psi (Psi = L L^H)
L2  for each pixel p do
L3      v <- (m_1(p), ..., m_c(p))
L4      w <- L^{-1} v                 ▷ forward substitution
L5      out(p) <- ||w||
L6  return out
```

Line L1 runs once. Line L4 whitens the coil values: after it the noise of the coils has the identity covariance. Line L5 gives $\lVert w \rVert = \sqrt{v^H \Psi^{-1} v}$. For $\Psi = I$, lines L1 and L4 do nothing, and the result is the plain RSS. The code of this page also has the optimal combination $s^H \Psi^{-1} v / (s^H \Psi^{-1} s)$ of Roemer et al., which needs the maps.

## Example

Take $c = 2$, the map vector $s = (1, 0.5)$ and the object value $\rho = 2$, so $v = (2, 1)$ without noise, and the covariance $\Psi = \begin{pmatrix} 1 & 0.5 \\ 0.5 & 1 \end{pmatrix}$ with the Cholesky factor $L = \begin{pmatrix} 1 & 0 \\ 0.5 & 0.8660 \end{pmatrix}$.

| coil values $v$ | $\Psi$ | plain RSS | whitened $w$ | prewhitened RSS |
|---|---|---|---|---|
| $(3, 4i, 12)$ | $I$ | 13 | $(3, 4i, 12)$ | 13 |
| $(2, 1)$ | $I$ | 2.2361 | $(2, 1)$ | 2.2361 |
| $(2, 1)$ | as above | 2.2361 | $(2, 0)$ | 2 |
| $(2, -1)$ | as above | 2.2361 | $(2, -2.3094)$ | 3.0551 |

In the second row the output is $|\rho| \lVert s \rVert = 2 \cdot 1.1180$. In the third row it is $|\rho| \sqrt{s^H \Psi^{-1} s} = 2 \cdot 1$, because $\Psi^{-1} s = (1, 0)$. The last row turns the phase of coil 2 by $\pi$: the plain RSS does not change, but the prewhitened value does, because correlated noise makes the relative phase of the coils matter.

## Correctness

The [proof](proofs/correctness.md) shows four theorems about the pixel model. Without noise, the output is $|\rho| \sqrt{s^H \Psi^{-1} s}$. For any data, the squared output is $q |\hat\rho|^2$ plus the energy of $w$ orthogonal to the whitened map, where $\hat\rho = s^H \Psi^{-1} v / q$ is the optimal combination and $q = s^H \Psi^{-1} s$. The optimal combination is the unbiased linear estimate of least variance, $1/q$, by the Cauchy-Schwarz inequality. On noise alone, the output has the mean $\Gamma(c + \frac12)/\Gamma(c)$ in units of the whitened noise.

## Complexity

In the [real RAM](/real-ram/), line L1 costs $O(c^3)$ once. Each of the $n^2$ pixels costs $O(c^2)$ for the forward substitution of line L4 and $O(c)$ for line L5, so the total is $O(c^3 + c^2 n^2)$. The plain RSS costs $O(c n^2)$. The extra memory is the factor $L$ and the output, $O(c^2 + n^2)$.

## Properties

- **Magnitude times coil norm.** Without noise the output is $|\rho| \lVert s \rVert$ for the plain RSS (theorem). The image is shaded by $\lVert s \rVert$, bright near the coils and dark far from them.
- **Phase blind.** The plain RSS does not change when a coil image is multiplied by a phase factor (theorem). So it needs no phase estimate, and it returns no phase.
- **Close to optimal at high SNR.** The prewhitened output is $\sqrt{q} |\hat\rho|$ plus a noise term orthogonal to the whitened map (theorem). At high signal to noise ratio it has the SNR of the optimal combination to first order (Roemer et al. 1990; Larsson et al. 2003).
- **Biased at low SNR.** On noise alone the output is not zero: its mean is $\Gamma(c + \frac12)/\Gamma(c)$, which is 1.9386 for $c = 4$ (theorem). The values follow a noncentral chi distribution with $2c$ degrees of freedom (Constantinides, Atalar and McVeigh 1997).
- **No parameters.** RSS needs no maps, no calibration and no choices.

## Variants and improvements

- **Optimal combination.** With known maps, $s^H \Psi^{-1} v / (s^H \Psi^{-1} s)$ gives an unbiased complex image with the least noise (Roemer et al. 1990). It is [SENSE](/sense/) with $R = 1$.
- **Adaptive combination.** Walsh, Gmitro and Marcellin (2000) estimate the maps from the local correlation of the coil images and then use the optimal weights.
- **Normalization.** Dividing the RSS image by a smooth estimate of $\lVert s \rVert$, for example from a body coil scan, removes the coil shading.
- **Maps from RSS.** The ratio $m_k / \mathrm{RSS}$ is a simple estimate of the normalized [coil sensitivity map](/coil-sensitivity-map/).

## When to use it

Use RSS for magnitude images of fully sampled multi-coil scans, and to combine the coil images that [GRAPPA](/grappa/), [slice-GRAPPA](/slice-grappa/) or [SPIRiT](/spirit/) return. Whiten first when the noise covariance is known, which costs little. When the phase is needed (flow, susceptibility, partial Fourier), or when the bias at low SNR matters, as in diffusion imaging at high $b$ values, use the optimal combination with maps instead.

## Pitfalls

- **Phase is lost.** Line L5 returns a magnitude. Methods that need the image phase, such as [homodyne reconstruction](/homodyne-reconstruction/), cannot work on the RSS image.
- **Noise floor.** At low SNR the output does not fall to zero, so a quantitative fit of a decay curve on RSS images is biased upward.
- **Unwhitened correlated noise.** Without line L4, coils with correlated or unequal noise get the wrong weights, and the SNR is lower than possible.
- **Coil shading.** The image follows $\lVert s \rVert$. A threshold or a quantitative value read from it depends on the position relative to the coils.
- **Wrong covariance.** A $\Psi$ in line L1 that is not positive definite stops the Cholesky factorization; one measured with a different receiver gain gives the wrong whitening.

## Implementations

## History

Roemer, Edelstein, Hayes, Souza and Mueller described the NMR phased array in 1990. They gave the combination with the sensitivities and the noise matrix, and the sum of squares as a practical form that needs neither. Constantinides, Atalar and McVeigh described the statistics of the sum of squares image in 1997. Larsson and colleagues showed in 2003 that the sum of squares is the maximum likelihood estimate of the magnitude when the sensitivities are unknown. Kellman and McVeigh made prewhitening and SNR units standard in 2005.

## References
