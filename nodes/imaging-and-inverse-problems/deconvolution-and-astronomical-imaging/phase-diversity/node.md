---
tag: 3P3S66
kind: technique
slug: phase-diversity
name: Phase diversity
aliases:
- phase diverse imaging
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: "Estimate an unknown wavefront aberration and the object together from two or more images that differ by a known aberration, such as a defocus."
prereqs: [point-spread-function, optical-transfer-function, phase-retrieval, nonlinear-least-squares]
see_also: [zonal-wavefront-reconstruction, ayers-dainty-blind-deconvolution, variational-bayes-blind-deconvolution, gerchberg-saxton-algorithm, speckle-interferometry, limited-memory-bfgs, gauss-newton-algorithm, maximum-likelihood-estimation]
sources:
  - paper: "Robert A. Gonsalves, Phase retrieval and diversity in adaptive optics, Optical Engineering 21(5), 1982"
    title: Gonsalves 1982
    locator: pages 829 to 832 (an in-focus and a defocused image, and the error metric in which the object is eliminated)
  - paper: "Richard G. Paxman, Timothy J. Schulz and James R. Fienup, Joint estimation of object and aberrations by using phase diversity, Journal of the Optical Society of America A 9(7), 1992"
    title: Paxman, Schulz and Fienup 1992
    locator: pages 1072 to 1085 (the metric for any number of images under Gaussian noise, the Poisson case, and the gradients for the aberration parameters)
---

Phase diversity is a technique to measure the unknown aberration of an imaging system from images of an unknown object. You record two or more images of the same object at the same time, and each one has an extra aberration that you add on purpose and know exactly, most often a defocus. One image alone cannot separate the object from the blur, because any blur can be explained by a suitable object. With several images, the object is the same in all of them, and only the aberration changes in a known way, so the unknown aberration is overdetermined. Gonsalves (1982) showed that for Gaussian noise the object can be eliminated in closed form, which leaves an error metric of the aberration alone. You minimize it over a few aberration parameters with a standard nonlinear optimizer, and then recover the object by a Wiener-type filter with the estimated [point spread functions](/point-spread-function/). It is used as a wavefront sensor and as a blind deconvolution method in which the PSF is constrained by optics.

## In plain words

A blurred photo of an unknown scene does not tell you what is wrong with the lens: a sharp scene behind a bad lens and a soft scene behind a good lens can give the same photo. Now take a second photo of the same scene at the same time, through the same lens, but slightly out of focus by an amount you know. The scene is the same in both photos. Only the lens error changes, and it changes in a way you control. A wrong guess of the lens error now fails to explain the two photos together, even with the best scene for that guess. So you search for the lens error under which one scene explains both photos. That search also gives you the scene.

## When it applies

- **Incoherent imaging with a known pupil.** The PSF of channel $k$ is $s_k = |\mathcal F^{-1}\{A\, e^{i(\phi + \theta_k)}\}|^2$, scaled to sum 1, where $A$ is the known pupil amplitude (the aperture), $\phi$ is the unknown phase aberration and $\theta_k$ is the known diversity phase. The [optical transfer function](/optical-transfer-function/) $S_k$ is the DFT of $s_k$, the normalized autocorrelation of the generalized pupil $A e^{i(\phi + \theta_k)}$.
- **The same object in every channel.** The images are taken at the same time, for example by a beam splitter and two cameras at different focus, or the object does not change between exposures.
- **The aberration is common to the channels.** It is the same field angle and the same optics up to the known diversity. For a wide field, the aberration changes across the field, and you must work on patches.
- **Shift-invariant blur on each patch**, so that $d_k = s_k \ast f + n_k$.
- **The aberration has a few parameters,** for example the coefficients $a_j$ of $\phi = \sum_j a_j Z_j$ in a basis of smooth modes on the pupil. A phase value at each pupil sample is also possible but needs more data and a regularizer.

## The template

On a periodic grid, write $D_k$, $S_k$ and $F$ for the DFTs of $d_k$, $s_k$ and $f$. With Gaussian noise of equal variance in all channels, the maximum likelihood estimate minimizes $L(f, \phi) = \sum_k \lVert d_k - s_k \ast f\rVert^2$. By Parseval this is $\frac1N\sum_u \sum_k |D_k(u) - S_k(u) F(u)|^2$, a separate least squares problem for $F(u)$ at each frequency. Its minimizer is $F(u) = \sum_k \overline{S_k(u)} D_k(u) / \sum_k |S_k(u)|^2$. Put it back, and $N$ times the minimum is

$$L_M(\phi) = \sum_u \Big[\sum_k |D_k|^2 - \frac{|\sum_k \overline{S_k} D_k|^2}{\sum_k |S_k|^2}\Big],$$

where a frequency with $\sum_k |S_k|^2 = 0$ contributes $\sum_k |D_k|^2$. This is a theorem (a projection onto one complex dimension at each frequency). For two channels the Lagrange identity $(|D_1|^2 + |D_2|^2)(|S_1|^2 + |S_2|^2) - |\overline{S_1}D_1 + \overline{S_2}D_2|^2 = |D_1 S_2 - D_2 S_1|^2$ gives the form of Gonsalves,

$$L_M(\phi) = \sum_u \frac{|D_1 S_2 - D_2 S_1|^2}{|S_1|^2 + |S_2|^2}.$$

The numerator says it directly: if $D_k = S_k F$, then $D_1 S_2 = S_1 S_2 F = D_2 S_1$. So with no noise the true aberration gives $L_M = 0$, its smallest value (a theorem). The object never has to be known.

```pseudo id=main
PHASE-DIVERSITY(d_1..d_K, A, θ_1..θ_K, Z_1..Z_J, γ)
L1  D_k ← DFT(d_k) for every channel k
L2  a ← 0                                        ▷ or a start from another sensor
L3  repeat until L_M stops falling
L4      φ ← Σ_j a_j Z_j
L5      for every k: s_k ← |IDFT(A e^{i(φ + θ_k)})|², scaled to sum 1; S_k ← DFT(s_k)
L6      L_M(a) ← Σ_u [Σ_k |D_k|² - |Σ_k conj(S_k) D_k|² / (γ + Σ_k |S_k|²)]
L7      a ← one step of a quasi-Newton method on L_M(a)
L8  F ← Σ_k conj(S_k) D_k / (γ + Σ_k |S_k|²); return a, IDFT(F)
```

The weight $\gamma \ge 0$ is a Tikhonov term on the object. It keeps the division stable at frequencies where all OTFs are small, and with $\gamma > 0$ the metric is the minimum of $L(f, \phi) + \gamma\lVert f\rVert^2$ over $f$, by the same argument. Paxman, Schulz and Fienup (1992) gave the metric for any number of channels and the gradient of $L_M$ with respect to the parameters, which costs a few FFTs. Line L7 can then be [L-BFGS](/limited-memory-bfgs/) or another gradient method. Finite differences also work for a few modes, at the cost of $J$ extra evaluations per step.

**What cannot be measured.** Three things are hidden for any data (theorems, each a short computation).

- *Piston.* A constant $c$ added to $\phi$ multiplies the field by $e^{ic}$ and does not change any $s_k$.
- *Tilt.* A linear phase $2\pi \langle t, u\rangle / N$ shifts every PSF by the same vector $t$, and a shift of the object by $-t$ undoes it in all channels. So with an unknown object, the tilt is lost too. Remove both modes from the basis $Z_j$.
- *The sign of the even part, with one image.* Let $A(-u) = A(u)$. For a phase that is even, $\phi(-u) = \phi(u)$, the field $a = \mathcal F^{-1}\{A e^{i\phi}\}$ is even, and the field for $-\phi$ is $\overline{a(-x)} = \overline{a(x)}$. Both have the same intensity, so one image cannot tell $\phi$ from $-\phi$ even when the object is known. A known even diversity breaks this, because $|\cdot|^2$ of the fields for $\phi + \theta$ and $-\phi + \theta$ differ in general. This is why defocus, an even mode, is the usual diversity.

**Example.** Take a pupil of three samples at $u = -1, 0, 1$ with $A = 1$ on a grid of $N \ge 3$ points, and the even phase $\phi = (\alpha, 0, \alpha)$, a crude defocus of size $\alpha$. With $c = \cos(2\pi x/N)$ the field is $a(x) = 1 + 2e^{i\alpha} c$, and

$$|a(x)|^2 = 1 + 4c\cos\alpha + 4c^2.$$

This depends on $\alpha$ only through $\cos\alpha$, so $\alpha$ and $-\alpha$ give the same PSF. Add the known diversity $\theta = (\beta, 0, \beta)$. The second PSF is $1 + 4c\cos(\alpha + \beta) + 4c^2$, and $\cos(\alpha + \beta) - \cos(-\alpha + \beta) = -2\sin\alpha\sin\beta$. This is not zero when $\sin\alpha \ne 0$ and $\sin\beta \ne 0$, so the pair of PSFs fixes the sign of $\alpha$. The sum of $|a(x)|^2$ over the grid is $N + 0 + 2N = 3N$ in all cases, so the scaling to sum 1 does not change the argument.

## Classic examples

- **Wavefront sensing for adaptive optics.** Gonsalves proposed an in-focus and a defocused image of an extended scene as a wavefront sensor that needs no reference star and no extra optics beyond a beam splitter. Compare a slope sensor, whose data are inverted by [zonal reconstruction](/zonal-wavefront-reconstruction/).
- **Solar telescopes.** The Sun has no point source to use as a reference, but it has fine granulation. Phase diversity on short exposures estimates the aberrations of the telescope and the atmosphere together with the scene, and then restores it. With many frames through changing turbulence it becomes phase-diverse speckle imaging, a relative of [speckle interferometry](/speckle-interferometry/).
- **Alignment of optics.** Defocused images of a star, taken on purpose, give the aberrations of a telescope with a segmented or deformable mirror. When the object is a point, the problem is focus-diverse [phase retrieval](/phase-retrieval/), and algorithms of the [Gerchberg-Saxton](/gerchberg-saxton-algorithm/) type also apply.
- **Calibration of microscopes and cameras.** Images of a fixed sample at a few focus settings give the pupil phase, which then feeds a PSF model for deconvolution.

## Variations

- **More channels.** The metric above holds for any $K$. More channels with different diversities make the minimum better defined and reduce the effect of noise.
- **Other noise models.** For photon counting, Paxman, Schulz and Fienup derived the Poisson likelihood. The object no longer drops out in closed form, so it is estimated jointly with the aberration.
- **Parameters.** A few low-order modes, a phase value per pupil sample with a smoothness penalty, or the parameters of a deformable mirror. Amplitude errors of the pupil can be added in the same way.
- **Other diversities.** Any known change works in principle: a known astigmatism, a shift of the pupil, or a change of wavelength. Defocus is the most common because it is even and easy to make.
- **Joint object priors.** Positivity of the object, or a regularizer stronger than $\gamma\lVert f\rVert^2$, when the object is estimated after the aberration.

## Pitfalls

- **Local minima.** $L_M$ is not convex in the aberration. For aberrations of more than about a wave, start from a coarse estimate, fit low-order modes first, or start from several points. This is a heuristic, with no proof of a threshold.
- **Wrong diversity.** The method trusts the known diversity exactly. An error in the defocus distance moves into the estimate of the even modes. Calibrate the diversity, or fit its size as one more parameter.
- **Sampling.** The PSF is the squared modulus of the field, so its spectrum is twice as wide as the pupil. Embed the pupil in a grid at least twice its diameter, or the periodic model wraps the OTF around and the metric is wrong.
- **Registration and gain.** The channels must be aligned to a fraction of a pixel and scaled to the same flux. A relative shift between the cameras looks like a tilt difference, and a gain difference looks like a change of the PSF.
- **Edges of the field.** The periodic model assumes that the scene wraps around. On a patch of a larger scene, apodize the patch edges or the metric fits the edge jumps.
- **Noise at high frequencies.** With $\gamma = 0$, frequencies where all OTFs are small add noise to the metric and to the object. Use $\gamma > 0$, or limit the sum to frequencies inside the cutoff of the optics.
- **Hidden modes.** Piston and tilt are not observable, and a basis that contains them makes the problem singular.

## Exercises

1. Show that for fixed $\phi$ the minimizer of $\sum_k |D_k - S_k F|^2$ over the complex number $F$ is $\sum_k \overline{S_k} D_k / \sum_k |S_k|^2$, and derive $L_M$.
2. Prove the Lagrange identity used for two channels, and show that $L_M(\phi_{\text{true}}) = 0$ when the data have no noise.
3. In the example, compute the two PSFs for $\alpha = \beta = \pi/4$ on a grid of $N = 4$ points, and check that the pair for $-\alpha$ is different.
4. Show that a linear phase in the pupil shifts the PSF, and explain why the tilt cannot be found when the object is unknown.
5. Show that with one channel and an unknown object, every aberration whose OTF has no zeros fits the data exactly. What does a second channel add?
6. With $\gamma > 0$, derive the minimizing $F$ of $\sum_k |D_k - S_k F|^2 + \gamma |F|^2$ and the corresponding metric.

## References
