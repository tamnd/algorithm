---
tag: EAKMFX
kind: algorithm
slug: capon-beamformer
name: Capon beamformer
aliases:
- MVDR beamformer
- minimum variance beamformer
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: "Choose the array weights that minimize the output power with unit gain in the look direction: w = R^-1 a / (a^H R^-1 a). In ultrasound, R comes from subarray averages at each pixel."
solves: [beamforming]
model: real-ram
complexity:
  vars: {M: the number of array elements, L: the subarray length, K: the number of snapshots per pixel, n: the number of pixels along one side of the image}
  time: {worst: O(n^2 (K M L^2 + L^3))}
  space: {extra: O(L^2)}
properties: {deterministic: true, linear_in_data: false, recursive: false, exact: true}
history:
  year: 1969
  people: [Jack Capon]
  note: "Capon (1969) introduced the minimum variance distortionless method for high-resolution frequency-wavenumber analysis with arrays of seismometers. Synnevag, Austeng and Holm (2007) adapted it to medical ultrasound imaging with spatial smoothing and diagonal loading."
prereqs: [beamforming, delay-and-sum-beamforming, positive-definite-matrix]
see_also: [covariance-matrix, music-algorithm, spectral-estimation, woodbury-identity, coherence-factor, delay-multiply-and-sum, plane-wave-compounding, adaptive-filtering]
sources:
  - paper: doi:10.1109/PROC.1969.7278
    title: "Jack Capon, High-resolution frequency-wavenumber spectrum analysis, Proceedings of the IEEE 57(8), 1969, 1408 to 1418"
    locator: "the minimum variance estimate of the frequency-wavenumber spectrum and its weights (general locator)"
  - paper: doi:10.1109/TUFFC.2007.431
    title: "Johan-Fredrik Synnevag, Andreas Austeng and Sverre Holm, Adaptive beamforming applied to medical ultrasound imaging, IEEE Transactions on Ultrasonics, Ferroelectrics, and Frequency Control 54(8), 2007, 1606 to 1613"
    locator: "the minimum variance beamformer per pixel, with subarray averaging, diagonal loading and the comparison with delay-and-sum (general locator)"
  - paper: doi:10.1109/TASSP.1985.1164649
    title: "Tie-Jun Shan, Mati Wax and Thomas Kailath, On spatial smoothing for direction-of-arrival estimation of coherent signals, IEEE Transactions on Acoustics, Speech, and Signal Processing 33(4), 1985, 806 to 811"
    locator: "spatial smoothing over subarrays to decorrelate coherent sources (general locator)"
  - paper: doi:10.1109/TASSP.1987.1165054
    title: "Henry Cox, Robert M. Zeskind and Mark M. Owen, Robust adaptive beamforming, IEEE Transactions on Acoustics, Speech, and Signal Processing 35(10), 1987, 1365 to 1376"
    locator: "diagonal loading and the robustness of the minimum variance beamformer (general locator)"
---

The Capon beamformer, also called the minimum variance distortionless response (MVDR) beamformer, chooses the array weights from the data. Fixed weights, as in [delay-and-sum](/delay-and-sum-beamforming/) (DAS), give every direction the same treatment. Capon instead asks for the weights $w$ that make the output power $w^H R w$ as small as possible, for the covariance $R$ of the channel data, under the constraint $w^H a = 1$, which keeps a signal from the look direction $a$ unchanged. The answer is $w = R^{-1} a / (a^H R^{-1} a)$. The constraint protects the wanted signal, and the minimum removes as much as possible of everything else, so the beamformer places nulls on strong interferers and narrows the main lobe. In medical ultrasound, the look direction after the focusing delays is the all-ones vector, and $R$ is estimated at each pixel from the delayed channel data, with averaging over subarrays and diagonal loading. The method is one instance of adaptive [beamforming](/beamforming/); [MUSIC](/music-algorithm/) uses the same covariance, but the eigenvectors of its noise subspace.

## In plain words

Delay-and-sum adds all channels with equal weight. That is fine when only the wanted echo is present, but strong echoes from the side leak into the sum. The Capon beamformer looks at the data first and chooses a weight for each channel. There is one rule: an echo from exactly the point you want must come through unchanged. Among all weights that keep this rule, it picks the ones that make the total output as quiet as possible. Since the wanted echo is protected, the only way to be quiet is to cancel the unwanted echoes. The result is a sharper image, at the cost of a small matrix problem for every pixel.

## The problem

The narrowband problem: given a Hermitian positive definite $L \times L$ matrix $R$ and a vector $a \ne 0$, find

$$w^\star = \arg\min_w\, w^H R w \quad \text{subject to} \quad w^H a = 1.$$

The value $P(a) = 1/(a^H R^{-1} a)$ of the minimum, as a function of the look direction, is the Capon spectrum.

The ultrasound problem: for one pixel, the input is $2Q + 1$ delayed analytic channel vectors $x^{(q)} \in \mathbb{C}^M$ at the sample times around the pixel, as in [dynamic receive focusing](/dynamic-receive-focusing/); the middle one is the pixel sample. The parameters are a subarray length $L$ and a loading factor $\delta$. The output is one complex pixel value.

## The algorithm

```pseudo id=main
CAPON-WEIGHTS(R, a, λ)                        ▷ the minimum variance weights
L1  R_λ ← R + λ I                            ▷ diagonal loading
L2  z ← solve R_λ z = a
L3  return w ← z / (a^H z)

CAPON-PIXEL(x^(1) … x^(K), L, δ)               ▷ K = 2Q + 1 delayed snapshots of length M
L4  S ← all subarrays x^(k)[l … l+L-1], l = 1 … M-L+1, k = 1 … K
L5  R ← (1/|S|) Σ_{y ∈ S} y y^H                ▷ spatially smoothed covariance
L6  w ← CAPON-WEIGHTS(R, 1, δ tr(R)/L)          ▷ steering vector of all ones
L7  g ← mean of the subarrays of the centre snapshot
L8  return w^H g
```

Line L2 is a linear solve, done in the code by Gaussian elimination from a shared helper; a Cholesky factorization fits because $R_\lambda$ is positive definite. Line L3 scales the result so that $w^H a = 1$. Lines L4 and L5 average the covariance over the subarrays and over the snapshots near the pixel: without this, one snapshot gives a matrix of rank one. The loading of L6 is relative to the mean power on the diagonal. The parameters $L$, $\delta$ and $Q$ are design choices that must be tuned; the tests use $L = M/2$, $\delta = 0.01$ and $Q = 2$.

## Example

Take $R = \begin{pmatrix} 3 & 1 \\ 1 & 2 \end{pmatrix}$ and $a = (1, 1)$. Line L2 gives $z = R^{-1} a = (1/5, 2/5)$, $a^H z = 3/5$, and line L3 gives $w = (1/3, 2/3)$. The output power is $w^H R w = 5/3$. The DAS weights $(1/2, 1/2)$ also satisfy $w^H a = 1$, but give $7/4$. Capon puts more weight on the second channel, which has less power.

**One interferer.** For $M = 8$ elements at half-wavelength spacing, a look direction $u = 0$ and an interferer at $u = 0.4$ with power 100 over unit noise, the gain toward the interferer is $0.000263$ for Capon and $0.2023$ for DAS, and the output power is $0.1303$ against $4.216$. The closed form of the gain comes from the [Woodbury identity](/woodbury-identity/).

**Two close sources.** For two sources at $u = \pm 0.1$ with noise power $0.01$ and $M = 8$, the Capon spectrum at $u = 0$ is $0.0184$ times its value at $u = 0.1$: two clear peaks. The DAS power at $u = 0$ is $1.093$ times its value at $u = 0.1$: one merged peak.

**Ultrasound.** The tests simulate $M = 16$ elements with pitch 0.3 mm, a plane wave at normal incidence, $f_0 = 5$ MHz, $f_s = 40$ MHz and a Gaussian envelope with $\sigma_t = 0.1$ us. With one scatterer at $(0, 6)$ mm, both beamformers have a peak at the scatterer with values $0.995$ (unit gain), but at $x = 0.1$ mm the normalized value is $0.038$ for Capon and $0.893$ for DAS. With two scatterers at $x = \pm 0.3$ mm, the value midway between them is $0.229$ of the peak for Capon and $0.68$ for DAS. These are measurements on a simulation without noise; with speckle and noise the gain is smaller and depends on $L$ and $\delta$.

## Correctness

By the Cauchy-Schwarz inequality, $1 = |w^H a|^2 \le (w^H R w)(a^H R^{-1} a)$ for every feasible $w$, with equality only for $w$ parallel to $R^{-1} a$. So line L3 returns the unique minimizer, and the least power is $1/(a^H R^{-1} a)$. For white noise, $R = \sigma^2 I$, the weights are those of DAS. For one interferer of power $s$, the gain toward it falls like $1/(L s)$, while DAS keeps a fixed gain. At an ultrasound pixel, an aligned echo passes with unit gain for any loading, and a very large loading gives a DAS with a trapezoidal taper. The proofs are in proofs/correctness.md.

These are theorems for the true covariance. With a covariance estimated from few samples, the weights are random, and a signal that is correlated with the clutter, or a small error in the steering vector, can be partly cancelled. This is why the loading and the smoothing exist.

## Complexity

In the real-RAM model, line L5 costs $O(K (M - L + 1) L^2)$ for $K$ snapshots, line L2 costs $O(L^3)$ and line L7 costs $O(M L)$. One pixel costs $O(K M L^2 + L^3)$, and an $n \times n$ image costs $O(n^2 (K M L^2 + L^3))$, against $O(n^2 M)$ for DAS. The extra space is $O(L^2)$ for the covariance. For $L = M/2$ this is cubic in $M$ per pixel, which is the main cost of the method; faster variants use fewer subarrays, a recursive update of $R$ along depth, or a beamspace with fewer dimensions.

## Properties

- Distortionless: $w^H a = 1$, so a signal from the look direction passes with unit gain.
- Data-adaptive and nonlinear in the data, because $w$ depends on $R$. For fixed $R$, the output $w^H x$ is linear in $x$.
- The least power is $1/(a^H R^{-1} a)$, never more than the DAS power with the same constraint.
- Equal to DAS for white noise; nulls a strong interferer with a gain of order $1/(L s)$.
- Sensitive to errors in the steering vector and in $R$; diagonal loading trades resolution for robustness, and the right amount is a design choice, not derived.

## Variants and improvements

- **Diagonal loading** (Cox, Zeskind and Owen 1987). Adding $\lambda I$ to $R$ limits the size of $w$ and makes the beamformer robust; for large $\lambda$ it tends to DAS.
- **Spatial smoothing** (Shan, Wax and Kailath 1985). Averaging the covariance over subarrays decorrelates coherent sources, such as the echoes of one transmit, and raises the rank of $R$.
- **Forward-backward averaging.** Adding the flipped and conjugated covariance doubles the number of samples.
- **Eigenspace and beamspace methods.** Projecting onto the strongest eigenvectors of $R$, or onto a few fixed beams, lowers the cost and the variance.
- **MUSIC and ESPRIT.** For direction finding, [MUSIC](/music-algorithm/) and [ESPRIT](/esprit/) use the eigenstructure of the same covariance and resolve sources more sharply, but they do not give a power estimate.
- **Other adaptive combiners.** The [coherence factor](/coherence-factor/) scales DAS by a measure of agreement, and [delay-multiply-and-sum](/delay-multiply-and-sum/) uses pairwise products; both are cheaper.

## When to use it

Use the Capon beamformer when lateral resolution or interference rejection matters and there is enough computing power for a small linear solve per pixel: passive arrays in sonar and radio, direction finding, and research ultrasound with channel data. Use DAS when speed, a well-understood speckle pattern or quantitative linear processing matters, or when the data are too few to estimate $R$.

## Pitfalls

- **Self-cancellation.** If the steering vector is slightly wrong, for example from a wrong speed of sound, or if the wanted signal is in the covariance and coherent with clutter, the minimization cancels part of the wanted signal. Use loading and smoothing.
- **Singular covariance.** One snapshot gives a rank-one $R$; without smoothing or loading the solve fails or is unstable.
- **Explicit inverse.** Computing $R^{-1}$ and multiplying is slower and less accurate than a solve with a factorization.
- **Speckle.** Capon on speckle can change the speckle statistics and the brightness of regions; compare the contrast with care.
- **Loading scale.** A fixed absolute $\lambda$ behaves differently at different depths; scale it by $\operatorname{tr}(R)/L$ as in L6.

## Implementations

## History

Capon (1969) introduced the method for high-resolution frequency-wavenumber analysis of the signals of seismometer arrays: the power estimate at each wavenumber is the output power of the filter that passes that plane wave without distortion and has the least output power. The method was also called the maximum likelihood method. It became a standard of adaptive array processing in radar, sonar and communications, where its sensitivity led to diagonal loading (Cox, Zeskind and Owen 1987) and spatial smoothing (Shan, Wax and Kailath 1985). Synnevag, Austeng and Holm (2007) applied the minimum variance beamformer to medical ultrasound imaging with a covariance estimated per pixel, and reported a much narrower main lobe than DAS.

## References
