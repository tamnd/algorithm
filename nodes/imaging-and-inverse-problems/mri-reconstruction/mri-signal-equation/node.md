---
tag: T3J6N5
kind: model
slug: mri-signal-equation
name: MRI signal equation
aliases:
- Fourier encoding model
area: imaging-and-inverse-problems/mri-reconstruction
level: core
summary: "The received MRI signal at time t is the integral of coil sensitivity times magnetization times exp(-i 2 pi k(t) . r): a Fourier sample at k(t), the time integral of the gradient times gammabar."
history:
  year: 1983
  people: [Stig Ljunggren, Donald B. Twieg]
  note: Lauterbur encoded position with field gradients in 1973. Ljunggren and Twieg wrote the signal as samples of the Fourier transform of the image along a path k(t) set by the gradients.
prereqs: [bloch-equations, discrete-fourier-transform]
see_also: [k-space, k-space-trajectory, mri-reconstruction-problem, nonuniform-discrete-fourier-transform, coil-sensitivity-map, forward-operator, fourier-slice-theorem, aliasing]
sources:
  - book: isbn:9780780347236
    title: Zhi-Pei Liang and Paul C. Lauterbur, Principles of Magnetic Resonance Imaging, A Signal Processing Perspective, IEEE Press, 2000
    locator: the chapter on signal localization (frequency and phase encoding and the k-space interpretation; chapter number not confirmed)
  - paper: doi:10.1038/242190a0
    title: Paul C. Lauterbur, Image formation by induced local interactions, examples employing nuclear magnetic resonance, Nature 242(5394), 1973, 190 to 191
    locator: position encoding by field gradients (general locator)
  - paper: doi:10.1016/0022-2364(83)90060-4
    title: Stig Ljunggren, A simple graphical representation of Fourier-based imaging methods, Journal of Magnetic Resonance 54(2), 1983, 338 to 343
    locator: the signal as a sample of the Fourier transform at a point that the gradients move (general locator)
  - paper: doi:10.1118/1.595331
    title: Donald B. Twieg, The k-trajectory formulation of the NMR imaging process with applications in analysis and synthesis of imaging methods, Medical Physics 10(5), 1983, 610 to 621
    locator: the k-trajectory formulation of the signal (general locator)
  - paper: doi:10.1016/0022-2364(75)90224-3
    title: Anil Kumar, Dieter Welti and Richard R. Ernst, NMR Fourier zeugmatography, Journal of Magnetic Resonance 18(1), 1975, 69 to 83
    locator: image formation by phase and frequency encoding and a Fourier transform (general locator)
---

The MRI signal equation is the forward model of magnetic resonance imaging. It says that the signal a receive coil picks up at time $t$ is one sample of the Fourier transform of the image, weighted by the coil sensitivity, at the spatial frequency $k(t)$. The gradient coils move $k(t)$ through [k-space](/k-space/): $k(t)$ is $\bar\gamma$ times the time integral of the gradient. The equation follows from the [Bloch equations](/bloch-equations/) when relaxation and field errors during the readout are ignored, and it turns image reconstruction into the inversion of a Fourier transform from samples. Lauterbur (1973) encoded position with gradients, Kumar, Welti and Ernst (1975) used a Fourier transform, and Ljunggren and Twieg (1983) gave the k-space form used here.

## The machine

**The unknown.** The transverse magnetization $m(r)$ right after excitation, a complex function of the position $r \in \mathbb{R}^d$ ($d = 2$ for a slice, $d = 3$ for a volume), zero outside the field of view.

**The parameters.**

- The gradient waveform $G(t) \in \mathbb{R}^d$, in T/m.
- The k-space trajectory $k(t) = \bar\gamma \int_0^t G(\tau)\, d\tau$, in cycles per meter, with $\bar\gamma = \gamma/(2\pi) = 42.577$ MHz/T for the proton.
- The coil sensitivity $c(r)$, complex; $c = 1$ for one uniform coil. With $J$ coils there are $J$ functions $c_j$.

**The forward map.**

$$s(t) = \int c(r)\, m(r)\, e^{-2\pi i\, k(t) \cdot r}\, dr + e(t).$$

The sign is that of the forward Fourier transform and of the forward DFT. Some scanners and books use the opposite sign or demodulation; a flip of the sign gives a mirrored image. The noise $e$ is circular complex Gaussian: real and imaginary parts are independent with the same variance, white over time for one coil, and correlated between coils.

**The discrete model.** On a Cartesian grid with the field of view $L$ and $n$ samples per axis, the k-space spacing is $\Delta k = 1/L$ and the pixel size is $L/n$. With the image $x$ of $n^d$ pixels, the data are

$$y = M F_u x + e \quad \text{(one coil)}, \qquad y_j = M F_u C_j x + e_j \quad \text{(coil } j\text{)},$$

where $F_u = n^{-d/2} F$ is the unitary DFT, so that $F_u^H F_u = I$, $M$ selects the acquired samples and $C_j$ is the diagonal matrix of the sensitivity of coil $j$. Non-Cartesian data use the [nonuniform discrete Fourier transform](/nonuniform-discrete-fourier-transform/) in place of $M F_u$. This page uses $F_u$ throughout.

**Where it holds.** During one readout of a few milliseconds, when $T_2^\ast$ is long compared with the readout, the field is uniform apart from the gradients, and nothing moves.

**Where it fails, and the usual extensions.**

- Relaxation during a long readout multiplies the integrand by $e^{-t/T_2^\ast(r)}$. This blurs the image along the direction in which time grows, which matters in echo planar and spiral imaging.
- A field error $\Delta\omega(r)$ multiplies it by $e^{-i \Delta\omega(r) t}$. This shifts and blurs the image; [conjugate phase reconstruction](/conjugate-phase-reconstruction/) corrects it with a field map.
- Motion between or during readouts makes the image different for each sample, which [PROPELLER](/propeller-mri/) and other methods correct.
- Gradient errors and eddy currents make the true $k(t)$ differ from the planned one.

## What it counts

- **The data.** One complex number per sample time and per coil.
- **The resolution and field of view.** With samples up to $|k| \le k_{\max}$ on each axis, the pixel size is $1/(2 k_{\max})$. With the spacing $\Delta k$, the image repeats with the period $1/\Delta k$, which must be at least the size of the object.
- **The gradient a scan needs.** For $L = 256$ mm and $n = 256$, $\Delta k = 3.906$ cycles per meter and $k_{\max} = 500$ cycles per meter. A readout with a dwell time of 4 microseconds needs $G = \Delta k / (\bar\gamma \cdot 4\ \mu\text{s}) = 22.9$ mT/m and takes 1.024 ms, a bandwidth of 977 Hz per pixel.
- **The reconstruction problem.** The model is the forward operator of the [MRI reconstruction problem](/mri-reconstruction-problem/); a fit minimizes $\frac{1}{2}\|M F_u x - y\|^2$ plus a penalty, which is the negative log-likelihood under Gaussian noise.

## Relation to other models

- **[Bloch equations](/bloch-equations/).** In the field $B_0 + G(t) \cdot r$ and without relaxation, the transverse magnetization at $r$ turns by $\gamma B_0 t + 2\pi k(t) \cdot r$. The coil integrates over the body, and the receiver removes the carrier $e^{-i \gamma B_0 t}$. What remains is the signal equation.
- **Fourier transform.** For a fixed time, $s(t) = \widehat{c m}(k(t))$, the Fourier transform of the weighted image at one point. A Cartesian scan samples it on a grid, so the image is an inverse DFT away.
- **Projections.** A radial line through the center of k-space is the 1D Fourier transform of the projection of the image at that angle, by the [Fourier slice theorem](/fourier-slice-theorem/). Early MRI used projection reconstruction for this reason.
- **Parallel imaging.** With several coils, the sensitivities $c_j$ add spatial information; [SENSE](/sense/) and [GRAPPA](/grappa/) use it to undersample.
- **Dynamic models.** Time-resolved MRI makes $m$ depend on time; the [partial separability model](/partial-separability-model/) restricts it to a low rank form.

## Known results in the model

**Conjugate symmetry (theorem).** If $c m$ is real, then $s(-k) = \overline{s(k)}$. Half of k-space then determines the rest. In practice $m$ has a phase, and [partial Fourier reconstruction](/partial-fourier-reconstruction/) uses the symmetry with a model of that phase.

*Proof.* $\overline{s(k)} = \int \overline{c m}\, e^{+2\pi i k \cdot r}\, dr = \int c m\, e^{-2\pi i (-k) \cdot r}\, dr = s(-k)$ when $c m$ is real. $\square$

**Full Cartesian sampling is invertible (theorem).** If all $n^d$ grid samples are acquired with one coil and no noise, $x = F_u^H y$. With noise $e \sim$ circular Gaussian of variance $\sigma^2$ per sample, the error $F_u^H e$ has the same distribution, because $F_u$ is unitary.

**Undersampling folds the image (theorem).** In 1D, let $n = R n'$ and keep every $R$-th sample, $X(R f')$ for $f' = 0, \ldots, n' - 1$. Then these are the DFT of length $n'$ of the folded image $x'_{j'} = \sum_{q=0}^{R-1} x_{j' + q n'}$. So the image from the kept samples is the sum of $R$ copies of the true image, shifted by $L/R$: the field of view shrinks by $R$ and the image folds $R$ times.

*Proof.* $X(R f') = \sum_{j=0}^{n-1} x_j e^{-2\pi i j R f'/n}$. Write $j = j' + q n'$ with $0 \le j' < n'$ and $0 \le q < R$. Then $j R f'/n = j' f'/n' + q f'$, and $e^{-2\pi i q f'} = 1$. So $X(R f') = \sum_{j'} \bigl(\sum_q x_{j' + q n'}\bigr) e^{-2\pi i j' f'/n'}$. $\square$

**What the data cannot see.** With a mask $M$ that drops samples, every image whose spectrum lives only on the dropped samples gives zero data. So the problem has a null space, and a unique answer needs prior knowledge: a smooth phase (partial Fourier), coil sensitivities (SENSE), or sparsity ([compressed sensing MRI](/compressed-sensing-mri/)).

**Least squares is the maximum likelihood estimate.** With white circular Gaussian noise, the negative log-likelihood is $\|A x - y\|^2 / \sigma^2$ plus a constant, where $A$ is the forward operator. For coils with a noise covariance $\Psi$, the weight is $\Psi^{-1}$.

## References
