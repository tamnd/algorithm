---
tag: Q0KFXT
kind: problem
slug: partial-fourier-reconstruction
name: Partial Fourier reconstruction
aliases:
- half Fourier imaging
area: imaging-and-inverse-problems/mri-reconstruction
level: core
summary: Recover an image from a little more than half of k-space by using the conjugate symmetry of the transform of a real image with a smooth phase.
model: real-ram
prereqs: [k-space, mri-signal-equation]
see_also: [homodyne-reconstruction, pocs-partial-fourier, mri-reconstruction-problem, loraks, convex-feasibility-problem, least-squares-problem, analytic-signal, discrete-fourier-transform]
sources:
  - paper: doi:10.1148/radiology.161.2.3763926
    title: David A. Feinberg, John D. Hale, John C. Watts, Leon Kaufman and Alexander Mark, Halving MR imaging time by conjugation, demonstration at 3.5 kG, Radiology 161(2), 1986, 527 to 531
    locator: the use of conjugate symmetry to halve the number of phase encoding steps (general locator)
  - paper: "Paul Margosian, F. Schmitt and D. E. Purdy, Faster MR imaging: imaging with half the data, Health Care Instrumentation 1, 1986, pages 195 to 197"
    locator: half Fourier imaging with a low resolution phase correction (general locator)
  - paper: doi:10.1109/42.79473
    title: Douglas C. Noll, Dwight G. Nishimura and Albert Macovski, Homodyne detection in magnetic resonance imaging, IEEE Transactions on Medical Imaging 10(2), 1991, 154 to 163
    locator: the homodyne weighting and the phase estimate from the symmetric band (general locator)
  - paper: doi:10.1016/0022-2364(91)90253-P
    title: E. M. Haacke, E. D. Lindskog and W. Lin, A fast, iterative, partial-Fourier technique capable of local phase recovery, Journal of Magnetic Resonance 92(1), 1991, 126 to 145
    locator: the iterative phase-constrained reconstruction (general locator)
  - paper: doi:10.1002/mrm.1910300109
    title: G. McGibney, M. R. Smith, S. T. Nichols and A. Crawley, Quantitative evaluation of several partial Fourier reconstruction algorithms used in MRI, Magnetic Resonance in Medicine 30(1), 1993, 51 to 59
    locator: the comparison of zero filling, conjugate synthesis, homodyne and iterative methods (general locator)
  - book: isbn:9780120928613
    title: Matt A. Bernstein, Kevin F. King and Xiaohong Joe Zhou, Handbook of MRI Pulse Sequences, Elsevier Academic Press, 2004
    locator: Section 13.4, Partial Fourier Reconstruction
---

Partial Fourier reconstruction is the problem of computing an MR image from a little more than half of its [k-space](/k-space/) samples. The tool is conjugate symmetry: the Fourier transform of a real image satisfies $X(-f) = \overline{X(f)}$, so one half determines the other. MR images are not real. Each pixel carries a phase from field errors, coil phases and the timing of the sequence, so the symmetry holds only after that phase is removed. Every method of this problem therefore estimates the phase first, from the band of low frequencies that is measured on both sides of the center, and assumes that the phase is smooth. [Homodyne reconstruction](/homodyne-reconstruction/) and [POCS partial Fourier](/pocs-partial-fourier/) are the two classic algorithms.

## In plain words

A picture made of real numbers has a frequency description in which every wave has a mirror partner with the same information. So half of the waves would be enough. A scanner that measures only half of them would be almost twice as fast.

MR pictures are not quite real numbers. Each value is tilted by an angle that changes slowly across the picture. The tilt breaks the mirror rule, so the method must first find the tilt and remove it. The scanner therefore measures a little more than half: one side fully, and a small band on the other side near the middle. That band gives a blurry picture whose tilt is a good guess of the true tilt. If the tilt changes fast, the guess is poor and the result has errors.

## Definition

The problem is posed on one line of k-space along the partial axis, usually the phase encoding axis. For an $n_1 \times n_2$ image, an inverse DFT along the fully sampled axis first gives one such line per image column.

**Data.** An even length $n$, a number $k_0$ with $0 \le k_0 < n/2 - 1$, and the samples

$$y_f = (F_u x)(f) + e_f, \qquad f \in S = \{-n/2, \ldots, k_0\},$$

where $F_u = n^{-1/2} F$ is the unitary DFT with frequencies $-n/2, \ldots, n/2 - 1$ (see [discrete Fourier transform](/discrete-fourier-transform/)) and $e_f$ is circular complex Gaussian noise with $E|e_f|^2 = \sigma^2$, independent over $f$. The scan acquires the fraction $a = (n/2 + k_0 + 1)/n$ of the line, for example $a = 5/8$ or $3/4$. The band $|f| \le k_0$ is measured on both sides of the center; the frequencies $f < -k_0$, apart from $-n/2$, have no measured mirror partner.

**Model.** $x = e^{i\varphi} \rho$ pixel by pixel, with a real image $\rho \in \mathbb{R}^n$ and a phase $\varphi$ that is smooth, meaning that its content lies mostly inside the band $|f| \le k_0$.

**Output.** An estimate of $\rho$ (a real image), or of $x$ (a complex image that agrees with the data), or of $|x|$.

**Conjugate symmetry (theorem).** If $\rho$ is real, then $(F_u \rho)(-f) = \overline{(F_u \rho)(f)}$ for every $f$, with indices taken mod $n$. *Proof.* $\overline{(F_u \rho)(f)} = n^{-1/2} \sum_j \rho_j e^{+2\pi i j f/n} = (F_u \rho)(-f)$, because $\rho_j$ is real. $\square$ The symmetry holds only for a real image. For $x = e^{i\varphi}\rho$ with a nonconstant $\varphi$ it fails, and this is why a phase estimate is needed.

## Variants

- **Known phase.** $\varphi$ is given. The problem is then linear in the real unknown $\rho$.
- **Constant unknown phase.** $\varphi = \varphi_0$ everywhere. The model of the first conjugate synthesis methods.
- **Smooth unknown phase.** The general case. It has no exact solution; the methods give approximations.
- **Partial echo.** The readout axis is partial. The echo comes earlier, which shortens the echo time, and the scan time does not change.
- **Partial Fourier in two or three axes.** Both axes partial, or the slice axis of a 3D scan.
- **With parallel imaging or compressed sensing.** The phase constraint joins coil sensitivities or a sparsity penalty in one model.

## Examples

All examples use $n = 8$ and $k_0 = 1$, so the scan acquires $f = -4, \ldots, 1$ (6 of 8 samples) and misses $f = 2, 3$.

**Constant unknown phase, solved exactly.** Take $\rho = [1, 2, 3, 4, 0, 0, 0, 0]$ and $\varphi_0 = 0.7$ rad. The center sample is $y_0 = e^{0.7i} \cdot 10/\sqrt{8} = 2.7041 + 2.2777i$. Then $y_0^2 / |y_0|^2 = e^{1.4i}$ gives $e^{2i\varphi_0}$. The missing sample $f = 2$ is $e^{2i\varphi_0}\, \overline{y_{-2}} = -0.9964 + 0.0853i$, and $f = 3$ is $e^{2i\varphi_0}\, \overline{y_{-3}} = 0.9359 + 0.2138i$; both equal the true values. An inverse DFT of the completed line returns $x$.

**No phase model, no answer.** Let $w_j = 0.2\, e^{2\pi i \cdot 3 j/8}$. Its transform lives only at $f = 3$, which is not measured, so $x$ and $x + w$ give the same data. Every complex image is a real image times some phase, so without a smoothness condition on the phase the data do not single out one image.

**Noise cost.** With the true constant phase, the least squares estimate of $\rho$ has the variance $\sigma^2 (n - k_0 - 1)/n$ per pixel (theorem below): $0.75\, \sigma^2$ here, against $0.5\, \sigma^2$ for the full line. The noise standard deviation grows by $\sqrt{1.5} = 1.225$, and the scan takes $6/8$ of the time. For $n = 256$ and $k_0 = 32$ ($a = 0.629$) the factor is 1.320.

**Smooth phase.** On a $16 \times 16$ modified Shepp-Logan phantom with the phase $0.4 + 0.5x - 0.6y + 0.2xy$ rad on $[-1, 1]^2$ and 12 of 16 phase encoding lines, homodyne reconstruction had a relative error of 0.094, POCS 0.046 after 5 iterations, and the zero filled magnitude 0.333. These are measurements with the code of the two algorithm pages, not bounds.

## Known algorithms

| Method | Phase model | What it gives |
|---|---|---|
| Zero filling | none | the inverse DFT with the missing samples set to 0; a blurred complex image, no gain in resolution over a symmetric scan of the same length |
| Conjugate synthesis (Feinberg and colleagues 1986) | constant | fills the missing half with $\overline{y_{-f}}$ after a constant phase correction |
| Phase-corrected half Fourier (Margosian, Schmitt and Purdy 1986) | smooth, from the band | removes a low resolution phase, then uses the symmetry |
| [Homodyne reconstruction](/homodyne-reconstruction/) (Noll, Nishimura and Macovski 1991) | smooth, from the band | weights that sum to 2 across the center, phase removal and the real part; one pass; exact for a constant phase and $\rho \ge 0$ |
| [POCS partial Fourier](/pocs-partial-fourier/) (Haacke, Lindskog and Lin 1991) | smooth, from the band | alternating projections onto the phase set and the data set; converges; exact for a constant phase |
| Least squares with a known phase | given | the minimum of $\sum_{f \in S} \lvert y_f - (F_u(e^{i\varphi}\rho))(f) \rvert^2$ over real $\rho$, by the [conjugate gradient method](/conjugate-gradient-method/) |
| [LORAKS](/loraks/) | smooth phase and limited support as low rank | low rank completion of k-space |

McGibney and colleagues (1993) compared several of these methods on phantoms and MR data. Their findings are measurements on those data.

## Bounds

- **Minimal data for a known constant phase (theorem).** If $\varphi = \varphi_0$ is known and $k_0 \ge 0$, the data determine $\rho$ exactly in the absence of noise: the set $\{-n/2, \ldots, 0\}$ holds the frequencies $0$ and $-n/2$, which are their own mirrors, and one member of every other pair $\{f, -f\}$, and the symmetry gives the rest. With $k_0 = -1$ the sample $f = 0$ is missing and has no partner, so the mean of $\rho$ is not determined. So $n/2 + 1$ samples are the least that can work, and partial Fourier saves at most a little less than half of the scan.
- **Unknown constant phase (theorem).** If $\varphi = \varphi_0$ is unknown, $k_0 \ge 0$ and $\sum_j \rho_j \ne 0$, then $y_0 = e^{i\varphi_0} \sum_j \rho_j / \sqrt{n}$ gives $e^{2i\varphi_0} = y_0^2/|y_0|^2$, and the data determine $x$ and determine $\rho$ up to its sign. The sign is never determined, because $(\rho, \varphi_0)$ and $(-\rho, \varphi_0 + \pi)$ give the same $x$.
- **Noise with a known constant phase (theorem).** The least squares estimate of $\rho$ from the data on $S$ has per-pixel variance $\sigma^2 (n - k_0 - 1)/n$, and the homodyne output computed with the true phase is equal to it. For the full line, $k_0 = n/2 - 1$, the value is $\sigma^2/2$.

  *Proof.* Let $y'_f = e^{-i\varphi_0} y_f$ and $R = F_u \rho$, so $y'_f = R(f) + e'_f$ with the same noise law. A real $\rho$ corresponds to a Hermitian $R$. The objective splits over the pairs $\{f, -f\}$. In the band $0 < |f| \le k_0$ both $y'_f$ and $\overline{y'_{-f}}$ measure $R(f)$, and the minimizer is their average, with error variance $\sigma^2/2$. For $f < -k_0$, $f \ne -n/2$, only $y'_f$ measures $R(f)$, with error variance $\sigma^2$. For $f = 0$ and $f = -n/2$, $R(f)$ is real and $\operatorname{Re} y'_f$ is the estimate, with variance $\sigma^2/2$. A pixel is $\rho_j = n^{-1/2}\bigl(R(0) + (-1)^j R(-n/2) + \sum_{f=1}^{n/2-1} 2\operatorname{Re}(R(f) e^{2\pi i f j/n})\bigr)$. The errors of different pairs are independent, and for a circular error $\varepsilon$ of variance $v$, $2\operatorname{Re}(\varepsilon e^{i\theta})$ has variance $2v$. Summing, the variance is $\frac{1}{n}\bigl(\frac{\sigma^2}{2} + \frac{\sigma^2}{2} + k_0 \sigma^2 + 2\sigma^2 (\frac{n}{2} - 1 - k_0)\bigr) = \sigma^2 \frac{n - k_0 - 1}{n}$. The homodyne weights give, after the real part, the spectrum $\frac{1}{2}(H(f) y'_f + \overline{H(-f) y'_{-f}})$, which is the same average in the band, $y'_f$ for the unpaired frequencies and $\operatorname{Re} y'_f$ at $0$ and $-n/2$. $\square$
- **Smooth phase.** No method has an exactness theorem for a general smooth phase. The error depends on the phase content outside the band and is measured, not bounded, in the literature. Choosing $k_0$ large enough to show the phase is a rule of thumb.
- **Cost in the [real RAM](/real-ram/).** Homodyne costs $O(n \log n)$ per line with an FFT, $O(n^2 \log n)$ for an $n \times n$ image. POCS costs $K$ times that for $K$ iterations.

## Reductions

- **To a real linear problem.** With a known phase, $x = e^{i\varphi}\rho$ turns the data into a real-linear map of $\rho \in \mathbb{R}^n$, and the problem becomes a real [least squares problem](/least-squares-problem/).
- **To a convex feasibility problem.** The images with a given phase form a real subspace, and the images that agree with the data form an affine subspace. A point in both is a solution, which is a [convex feasibility problem](/convex-feasibility-problem/); POCS solves it by alternating projections.
- **To a one-sided spectrum.** The homodyne weights relate partial Fourier to the [analytic signal](/analytic-signal/): doubling one side of a spectrum and keeping the real part returns a real signal.
- **To low rank completion.** A smooth phase and a limited support make structured matrices built from k-space low rank, which [LORAKS](/loraks/) uses.

## Applications

- **Fast spin echo and gradient echo scans.** Fewer phase encoding lines shorten the scan by up to nearly half.
- **Echo planar imaging.** Partial Fourier along the phase encoding axis shortens the echo time and the echo train, which reduces distortion and $T_2^\ast$ blur; it is common in diffusion and functional MRI.
- **Partial echo.** A partial readout gives a short echo time for gradient echo and angiography scans.
- **Single shot sequences.** Half Fourier single shot fast spin echo acquires a whole slice in one echo train.

## References
