---
tag: 0ZFP8H
kind: algorithm
slug: hogbom-clean
name: Hogbom CLEAN
aliases:
- CLEAN algorithm
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: core
summary: "Deconvolve a dirty image: find the largest residual pixel, add a point of gain times that value to the model, subtract the shifted dirty beam, and repeat."
solves: [image-deblurring]
model: real-ram
complexity:
  vars: {n: the number of pixels, K: the number of iterations}
  time: {worst: Θ(K n), average: Θ(K n), best: Θ(K n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, iterative: true, linear: false, greedy: true, nonnegative: false, monotone_misfit: true}
history:
  year: 1974
  people: [Jan Hogbom]
  note: Hogbom (1974) built CLEAN to remove the sidelobes of the beam from radio maps made with a non-regular set of interferometer baselines.
prereqs: [dirty-image, point-spread-function, convolution-theorem]
see_also: [cotton-schwab-clean, multiscale-clean, aperture-synthesis, maximum-entropy-method-imaging, coordinate-descent, orthogonal-matching-pursuit, sparse-signal-recovery, w-projection]
sources:
  - paper: "Jan A. Hogbom, Aperture synthesis with a non-regular distribution of interferometer baselines, Astronomy and Astrophysics Supplement Series 15, 1974, pages 417 to 426"
    title: "Hogbom, Aperture synthesis with a non-regular distribution of interferometer baselines, 1974"
    locator: "the whole article (the CLEAN procedure, the clean beam and examples on synthesis maps)"
  - paper: "U. J. Schwarz, Mathematical-statistical description of the iterative beam removing technique (method CLEAN), Astronomy and Astrophysics 65(3), 1978"
    title: "Schwarz, Mathematical-statistical description of the iterative beam removing technique (method CLEAN), 1978"
    locator: the article (CLEAN as a least squares fit of the model to the measured visibilities)
  - paper: "B. G. Clark, An efficient implementation of the algorithm CLEAN, Astronomy and Astrophysics 89(3), 1980"
    title: "Clark, An efficient implementation of the algorithm CLEAN, 1980"
    locator: "the article (minor cycles with a small patch of the beam, major cycles with the FFT)"
  - book: isbn:9783319444314
    title: "A. Richard Thompson, James M. Moran and George W. Swenson Jr., Interferometry and Synthesis in Radio Astronomy, third edition, Springer, 2017"
    locator: "Chapter 11, Further Imaging Techniques (the section on CLEAN)"
  - book: isbn:9783540330240
    title: "Jean-Luc Starck and Fionn Murtagh, Astronomical Image and Data Analysis, second edition, Springer, 2006"
    locator: the chapter on deconvolution (CLEAN among the iterative methods)
---

Hogbom CLEAN removes the sidelobes of the dirty beam from a [dirty image](/dirty-image/) made by a radio interferometer. It finds the largest pixel of the residual image, adds a point source with a fraction $g$ of that value to a model, subtracts the dirty beam shifted to that pixel and scaled by the same amount, and repeats. On the data it is greedy [coordinate descent](/coordinate-descent/) on the misfit to the measured visibilities, so the misfit goes down at every step for $0 < g < 2$. It is the first and simplest member of its family: [Cotton-Schwab CLEAN](/cotton-schwab-clean/) does the subtraction on the visibilities in major cycles, and [multiscale CLEAN](/multiscale-clean/) uses smooth blobs of several sizes in place of points.

## In plain words

A radio telescope array does not take a picture directly. It gives a blurred picture in which each bright point has a pattern of rings and stripes around it. The pattern is the same for every point, and it is known. CLEAN uses this fact. It looks for the brightest spot in the picture and assumes that a point source is there. It removes a small part of the known pattern at that place, and it writes down the position and the amount it removed. Then it looks again. After many steps, the list of points explains the bright parts of the picture, and what is left is mostly noise. For the final picture, CLEAN draws each point as a small smooth spot with no rings, and adds back what is left.

## The problem

The sky is an image $x$ on a periodic grid of $n$ pixels. The formulas below use a 1D index $q$; an image is the same with a 2D index and the 2D DFT. The visibilities are $V = \mathcal F x$, the [DFT](/discrete-fourier-transform/) $V_k = \sum_q x_q e^{-2\pi i kq/n}$. The interferometer measures them only at some frequencies $k$, with weights $w_k \ge 0$, $w_{-k} = w_k$ and $W = \sum_k w_k > 0$. The dirty beam and the dirty image are

$$B_q = \frac{1}{W} \sum_k w_k\, e^{2\pi i kq/n}, \qquad D_q = \frac{1}{W} \sum_k w_k V_k\, e^{2\pi i kq/n}.$$

The beam is real, has $B_0 = 1$ and is the [point spread function](/point-spread-function/) of the array. By the [convolution theorem](/convolution-theorem/), $D = B \ast x$ (periodic convolution).

The input is $D$, $B$, a loop gain $g$, a threshold $\tau \ge 0$ and a maximum number of iterations $K$. The output is a model $M$, which is a list of point components, and the residual $R = D - B \ast M$. The aim is a small residual. CLEAN cannot find $x$ itself: the frequencies with $w_k = 0$ are not measured, so many skies give the same dirty image. It finds one model, built from few points, that explains the measured data.

## The algorithm

```pseudo id=main
HOGBOM-CLEAN(D, B, g, τ, K)              ▷ B is centered at index 0, B_0 > 0
L1  R ← D, M ← 0
L2  for k ← 1 to K do
L3      p ← a pixel with the largest |R_p|
L4      if |R_p| ≤ τ then break
L5      c ← g R_p / B_0
L6      M_p ← M_p + c                     ▷ a point component of flux c at p
L7      R_q ← R_q - c B_{q-p} for every pixel q   ▷ indices mod n
L8  return M, R

RESTORE(M, R, C)                          ▷ C is the clean beam
L9  return C ∗ M + R
```

Line L7 keeps the invariant $R = D - B \ast M$. The loop gain $g$ is a tuned choice; values from $0.05$ to $0.3$ are common, and $0.1$ is a usual default. A small gain lets a later peak take flux that a sidelobe of a near source has moved, at the cost of more iterations. The threshold is set to a few times the noise level of the image, so that CLEAN stops before it fits the noise.

RESTORE makes the image that astronomers look at. The clean beam $C$ is usually a Gaussian fitted to the main lobe of the dirty beam. Convolving the components with it gives a smooth image at the resolution of the array, without the sidelobes. The residual is added back so that sources that CLEAN did not reach, and the noise, stay visible.

Two common options restrict line L3. A *window* (a "clean box") allows only pixels in a mask that the user believes hold emission. A *positive* option takes the largest $R_p$ and stops when it is not positive, for skies that are known to be nonnegative.

## Example

Take $n = 16$ and a 1D sky with $x_4 = 1$ and $x_7 = 0.6$. The array measures the frequencies $0, \pm 1, \pm 2, \pm 3, \pm 5$ with weight $1$, so $W = 9$. The dirty beam has $B_0 = 1$, $B_{\pm 1} = 0.4736$ and $B_8 = -1/3$, a deep negative sidelobe. The dirty image has its peak $D_4 = 1.0234$, and $D_7 = 0.639$. With $g = 0.5$ and the misfit $Q(M) = \frac1W \sum_k w_k |V_k - \hat M_k|^2$, which starts at $1.4068$:

| step | pixel $p$ | $R_p$ | flux $c$ | $Q$ after the step |
|---|---|---|---|---|
| 1 | 4 | 1.0234 | 0.5117 | 0.6213 |
| 2 | 7 | 0.6191 | 0.3095 | 0.3339 |
| 3 | 4 | 0.4996 | 0.2498 | 0.1467 |
| 4 | 7 | 0.2998 | 0.1499 | 0.0793 |
| 5 | 4 | 0.2440 | 0.1220 | 0.0346 |
| 6 | 7 | 0.1451 | 0.0726 | 0.0188 |

Each drop of $Q$ is exactly $(2g - g^2) R_p^2 = 0.75\, R_p^2$; for step 1 that is $0.75 \cdot 1.0234^2 = 0.7855 = 1.4068 - 0.6213$. After 8 steps the model is $M_4 = 0.9431$ and $M_7 = 0.5671$, and after 80 steps it equals the sky to 9 digits. The number of steps to bring $\max_q |R_q|$ below $0.01$ depends on the gain: 81 for $g = 0.1$, 13 for $0.5$, 3 for $1.0$, 13 for $1.5$ and 81 for $1.9$. With $g = 2.1$ the residual grows past $10^8$ in 200 steps.

Here the model also tends to the true sky. That is not guaranteed in general: the theorem below says only that the model comes to fit the measured frequencies.

## Correctness

Let $Q(M) = \frac{1}{W} \sum_k w_k |V_k - \hat M_k|^2$ be the misfit of the model to the measured visibilities. The residual is the negative half gradient of $Q$: $R_p = -\tfrac12\, \partial Q / \partial M_p$. Adding $c$ at pixel $p$ changes the misfit by an exact identity,

$$Q(M + c\,\delta_p) = Q(M) - 2c R_p + c^2 B_0 .$$

With $c = g R_p / B_0$ the drop is $(2g - g^2) R_p^2 / B_0$, which is positive for $0 < g < 2$ and $R_p \ne 0$. The value $c = R_p / B_0$ of $g = 1$ minimizes $Q$ along the coordinate $p$, so CLEAN is greedy coordinate descent with a damped step, and line L3 is the rule that picks the coordinate with the largest gradient. Because $Q \ge 0$, the drops have a finite sum, so $\max_q |R_q| \to 0$. Since the DFT is invertible, $\hat M_k \to V_k$ at each measured frequency, and $Q \to 0$. With $g > 2$ the identity gives a rise, and the iteration can diverge. The full proof is below.

## Complexity

Line L3 scans the $n$ pixels and line L7 updates them, so each iteration takes $\Theta(n)$ time and $K$ iterations take $\Theta(Kn)$. The extra space is $\Theta(n)$ for $R$ and $M$. The number of iterations is the real cost: with $0 < g \le 1$, an isolated point source of flux $F$ needs about $\log(F/\tau) / \log(1/(1-g))$ steps to get below the threshold $\tau$, and an extended source needs many components, each at this cost. Forming the dirty image and beam with the [FFT](/fast-fourier-transform/) takes $\Theta(n \log n)$ once, and RESTORE is one more convolution.

Clark (1980) cut the cost of line L7 by subtracting only a small patch of the beam in fast *minor cycles*, and then recomputing the exact residual with the FFT in a *major cycle*.

## Properties

- **Nonlinear.** The choice of pixel in line L3 depends on the data, so CLEAN of a sum of two skies is not the sum of the two results.
- **Greedy and sparse.** The model holds only pixels that were the peak at some step. For a few point sources, it is a few points.
- **The misfit never rises for $0 < g < 2$.** The drop at each step is $(2g - g^2) R_p^2 / B_0$.
- **Not unique.** The model fits the measured frequencies, and the unmeasured frequencies are whatever the greedy path left there. Another gain or another tie break gives another model.
- **No noise model.** CLEAN fits the data as it is. Only the threshold keeps it from fitting the noise.

## Variants and improvements

- **Clark CLEAN.** Minor cycles with a beam patch and the brightest pixels only, then a major cycle with the FFT. See the complexity section.
- **[Cotton-Schwab CLEAN](/cotton-schwab-clean/).** Each major cycle subtracts the model from the visibilities themselves, so gridding errors and wide-field effects such as the $w$ term (see [W-projection](/w-projection/)) do not build up.
- **[Multiscale CLEAN](/multiscale-clean/).** Components are smooth blobs of several widths, which fit extended emission with far fewer components than points.
- **Positive CLEAN and clean boxes.** Only positive components, or only pixels inside a mask. These add prior knowledge and reduce spurious components.
- **Other priors.** The [maximum entropy method](/maximum-entropy-method-imaging/) fits the same data with a smooth positive image in place of a few points.

## When to use it

Use Hogbom CLEAN on a dirty image of a field that holds mostly compact sources, when the dirty beam is known and the same over the field. It is simple, fast for a small image, and its result is easy to inspect: a list of components. For large images use the Clark or Cotton-Schwab form, which give the same kind of result with cheaper iterations. For smooth extended emission, use multiscale CLEAN or a regularized method, because point components fit it badly.

## Pitfalls

- **A gain of 2 or more.** The misfit does not go down, and for $g > 2$ the residual grows without bound. Even a gain near 1 can put flux on a sidelobe of a near source, and later steps must then correct it.
- **Cleaning into the noise.** With $\tau = 0$ CLEAN puts components on noise peaks. Set the threshold to a few times the noise level.
- **A beam that is too small.** To subtract a source at any pixel from every pixel of the image, the beam must cover twice the image size in each direction. A beam of the image size, as on the periodic grid here, wraps the sidelobes around the edges.
- **Extended emission.** Point components on a smooth source give a mottled model, and at times regular stripes. Multiscale CLEAN or a smaller gain help.
- **Mixed units in the restored image.** The model is convolved with the clean beam, but the residual still has the dirty beam. When the two beams have very different areas, the flux of faint emission in the restored image is wrong.

## Implementations

## History

Jan Hogbom described CLEAN in 1974, as a way to make maps from interferometers whose baselines did not fill a regular grid. The dirty beam of such an array has strong sidelobes, and CLEAN removed them by fitting the map with point sources. Schwarz (1978) described CLEAN as a least squares fit of the model to the measured visibilities, which is the view used in the proof here. Clark (1980) split the work into minor and major cycles, and Schwab (1984) moved the major cycle to the visibilities, which gave [Cotton-Schwab CLEAN](/cotton-schwab-clean/). Cornwell (2008) added several scales in [multiscale CLEAN](/multiscale-clean/).

## References
