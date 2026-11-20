---
tag: CC9PV7
kind: algorithm
slug: kasai-autocorrelation-estimator
name: Kasai autocorrelation estimator
aliases:
- lag-one autocorrelation velocity estimator
- pulse-pair estimator
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: core
summary: "Estimate the mean Doppler velocity at a pixel from the phase of the lag one autocorrelation of its slow time IQ samples: v = c PRF arg R(1) / (4 pi f0)."
solves: [spectral-estimation]
model: real-ram
complexity:
  vars: {N: the ensemble length (pulses per pixel), G: the number of depth samples averaged per pixel, n: the number of pixels along one side of the image}
  time: {worst: O(n^2 G N)}
  space: {extra: O(1)}
properties: {deterministic: true, linear_in_data: false, recursive: false, exact: false}
history:
  year: 1985
  people: [C. Kasai, K. Namekawa, A. Koyano, R. Omoto]
  note: "Kasai, Namekawa, Koyano and Omoto (1985) used the phase of the lag one autocorrelation for real-time two-dimensional color flow imaging. The same pulse-pair estimate was known in weather radar; Miller and Rochwarger (1972) analyzed it."
prereqs: [autocorrelation, analytic-signal, pulse-echo-imaging]
see_also: [svd-clutter-filter, power-spectral-density, periodogram, phase-unwrapping, b-mode-image-formation, moving-target-indication, range-doppler-processing, cramer-rao-bound]
sources:
  - paper: doi:10.1109/T-SU.1985.31615
    title: "C. Kasai, K. Namekawa, A. Koyano and R. Omoto, Real-time two-dimensional blood flow imaging using an autocorrelation technique, IEEE Transactions on Sonics and Ultrasonics 32(3), 1985, 458 to 464"
    locator: "the mean Doppler frequency from the phase of the autocorrelation at lag one pulse, and the variance from its magnitude (general locator)"
  - paper: doi:10.1109/TIT.1972.1054886
    title: "K. Miller and M. Rochwarger, A covariance approach to spectral moment estimation, IEEE Transactions on Information Theory 18(5), 1972, 588 to 596"
    locator: "the pulse-pair estimate of the mean frequency and the spectral width from the covariance at one lag, and its statistics (general locator)"
  - paper: doi:10.1109/58.393110
    title: "T. Loupas, J. T. Powers and R. W. Gill, An axial velocity estimator for ultrasound blood flow imaging, based on a full evaluation of the Doppler equation by means of a two-dimensional autocorrelation approach, IEEE Transactions on Ultrasonics, Ferroelectrics and Frequency Control 42(4), 1995, 672 to 688"
    locator: "the two-dimensional autocorrelator that also estimates the mean RF frequency over depth (general locator)"
  - paper: doi:10.1109/58.985705
    title: "S. Bjaerum, H. Torp and K. Kristoffersen, Clutter filter design for ultrasound color flow imaging, IEEE Transactions on Ultrasonics, Ferroelectrics and Frequency Control 49(2), 2002, 204 to 216"
    locator: "the clutter filters that must run before the velocity estimator (general locator)"
  - book: isbn:9780123964878
    title: "Thomas L. Szabo, Diagnostic Ultrasound Imaging: Inside Out, second edition, Academic Press, 2014"
    locator: "the chapter on Doppler modes (color flow imaging and the autocorrelation estimator)"
---

The Kasai autocorrelation estimator gives the mean axial velocity of blood at one pixel of a color flow image. Each pixel is sampled once per transmitted pulse, so it has a short slow time sequence of $N$ complex IQ samples, the ensemble. Motion of the scatterers turns the phase of these samples at a rate equal to the Doppler frequency. The estimator takes the lag one [autocorrelation](/autocorrelation/) $R(1)$ of the ensemble and reads the velocity from its phase: $v = \frac{c \cdot \mathrm{PRF}}{4 \pi f_0} \arg R(1)$. It needs one complex multiply and add per sample, which made real-time color Doppler possible in 1985. The magnitude of $R(1)$ against the power $R(0)$ also gives the spectral width. In radar the same method is called the pulse-pair estimator. It is a [spectral estimation](/spectral-estimation/) method for one number, the center of the Doppler spectrum, and it assumes that tissue echoes were removed first, for example by an [SVD clutter filter](/svd-clutter-filter/).

## In plain words

An ultrasound scanner sends many pulses down the same line, one after another. At a fixed depth, the echo from moving blood comes back a little earlier or later each time. After demodulation, each echo is one complex number, an arrow with a length and an angle. If the blood moves toward the probe, the arrow turns by the same angle from one pulse to the next.

The estimator measures this turn. It multiplies each sample by the conjugate of the sample before it, which gives an arrow whose angle is the turn, and it adds these products up. The angle of the sum is the average turn per pulse. A fixed formula converts the angle into a velocity. Angles beyond half a turn cannot be told apart from smaller ones in the other direction, which limits the velocity that can be measured.

## The problem

The input is, for one pixel, $G$ ensembles $x_g[0 \ldots N-1]$ of complex baseband (IQ) samples, one per depth sample $g$ near the pixel, taken at the pulse repetition frequency PRF, so the slow time step is $T = 1/\mathrm{PRF}$. The parameters are the center frequency $f_0$ and the speed of sound $c$, taken as 1540 m/s in soft tissue. That value is a convention close to measured averages, not a constant of nature.

**Model.** The IQ demodulation multiplies the RF signal by $e^{-i 2 \pi f_0 t}$. A scatterer at depth $z_0$ that moves toward the probe with axial velocity $v$ has the round trip delay $\tau_k = 2(z_0 - v k T)/c$ at pulse $k$, so its IQ sample is $a\, e^{-i 2 \pi f_0 \tau_k} = a\, e^{i\varphi_0} e^{i 2 \pi f_D k T}$ with the Doppler frequency

$$f_D = \frac{2 v f_0}{c}.$$

So $v > 0$ means motion toward the probe. The pulse length is short against the motion between pulses, and the beam is along the flow; for an angle $\theta$ between beam and flow the estimate is $v \cos\theta$.

**Output.** An estimate of the mean axial velocity, of the power $R(0)$ and of the spectral width.

## The algorithm

```pseudo id=main
KASAI(x_1 … x_G, c, PRF, f0)                       ▷ G ensembles of N IQ samples
L1  R0 ← (1/(G N)) Σ_g Σ_{k=0}^{N-1} |x_g[k]|^2          ▷ power
L2  R1 ← (1/(G (N-1))) Σ_g Σ_{k=0}^{N-2} conj(x_g[k]) x_g[k+1]   ▷ lag one autocorrelation
L3  v ← (c PRF / (4 π f0)) · arg R1                 ▷ mean axial velocity
L4  σ_v ← (c PRF / (4 π f0)) · sqrt(2 (1 - |R1| / R0))   ▷ spectral width
L5  return v, R0, σ_v
```

Line L2 averages the products of each sample with the conjugate of the sample before it. For one moving scatterer each product is $|a|^2 e^{i 2 \pi f_D T}$, so its phase is the phase step per pulse. Line L3 turns the phase into a frequency with $f_D = \arg R_1 / (2 \pi T)$ and then into a velocity with $v = c f_D / (2 f_0)$. The function arg returns a value in $(-\pi, \pi]$, so the velocities that can be told apart lie in $(-v_a, v_a]$ with the aliasing velocity

$$v_a = \frac{c \cdot \mathrm{PRF}}{4 f_0}.$$

Line L4 is the width estimate of Kasai et al.; it is zero when all products have the same phase and grows as the phases spread. The sum over $g$ averages several depth samples of the same pixel, which lowers the variance and costs depth resolution. $R_0$ is the power Doppler value of the pixel.

## Example

**Check value.** With $c = 1540$ m/s, PRF $= 5$ kHz and $f_0 = 5$ MHz, the aliasing velocity is $1540 \cdot 5000 / (4 \cdot 5 \cdot 10^6) = 0.385$ m/s.

**One scatterer.** For $v = 0.2$ m/s, $f_D = 2 \cdot 0.2 \cdot 5 \cdot 10^6 / 1540 = 1298.70$ Hz, and the phase step per pulse is $2 \pi f_D / \mathrm{PRF} = 1.63200$ rad. With a little noise, rounded to two decimals, an ensemble of $N = 5$ samples is

$x = (0.97 + 0.05i,\ -0.08 + 0.97i,\ -1.09 - 0.14i,\ 0.29 - 0.94i,\ 1.07 + 0.27i)$.

| $k$ | $\overline{x[k]}\, x[k+1]$ | phase (rad) |
|---|---|---|
| 0 | $-0.0291 + 0.9449i$ | 1.6016 |
| 1 | $-0.0486 + 1.0685i$ | 1.6163 |
| 2 | $-0.1845 + 1.0652i$ | 1.7423 |
| 3 | $0.0565 + 1.0841i$ | 1.5187 |

The mean of the four products is $R_1 = -0.051425 + 1.040675i$, with $\arg R_1 = 1.62017$ rad and $|R_1| = 1.04194$. The mean of $|x[k]|^2$ is $R_0 = 1.05678$. Line L3 gives $v = 0.122549 \cdot 1.62017 = 0.19855$ m/s, close to 0.2. Line L4 gives $\sigma_v = 0.122549 \cdot \sqrt{2(1 - 1.04194/1.05678)} = 0.0205$ m/s, a small width caused only by the noise.

**Aliasing.** For $v = 0.5$ m/s the phase step is $4.07999$ rad, which arg returns as $4.07999 - 2\pi = -2.20319$ rad. The estimate is $-0.27$ m/s, that is $0.5 - 2 \cdot 0.385$: fast flow toward the probe shows as flow away from it.

## Correctness

The estimator is exact for one scatterer: every product in line L2 has the phase $2 \pi f_D T$, so if $|f_D| < \mathrm{PRF}/2$ then $\arg R_1 = 2 \pi f_D T$ and line L3 returns $v$. The general statement is about a stationary slow time process with [power spectral density](/power-spectral-density/) $S(f)$ on one period $[-\mathrm{PRF}/2, \mathrm{PRF}/2)$. By the Wiener-Khinchin relation, $R(T) = \int S(f) e^{i 2 \pi f T} df$. If $S$ is symmetric about a frequency $\bar f$ and its mass lies within $1/(4T)$ of $\bar f$ on the circle, then

$$R(T) = e^{i 2 \pi \bar f T} \int S(\bar f + u) \cos(2 \pi u T)\, du$$

with a positive integral, so $\arg R(T) = 2 \pi \bar f T$ exactly: the phase gives the center of the spectrum. Line L2 is an unbiased estimate of $R(T)$, so for an ergodic process the estimate converges to $\bar f$ as $G N$ grows. For a spectrum that is not symmetric the phase of $R(T)$ is not the mean frequency, but it is close to it when the spectrum is narrow: the first moment of $S$ equals the derivative of the phase of $R(\tau)$ at $\tau = 0$, and $\arg R(T)/T$ is the slope of a chord. The width formula of line L4 comes from $|R(T)|/R(0) \approx 1 - 2 \pi^2 \sigma_f^2 T^2$ for small $\sigma_f T$; it is an approximation. The proofs are in proofs/correctness.md.

## Complexity

In the real-RAM model, lines L1 and L2 cost $O(G N)$ complex operations, and lines L3 and L4 cost $O(1)$, with one arctangent and one square root. An image of $n \times n$ pixels costs $O(n^2 G N)$. The extra space is $O(1)$ per pixel. A sliding sum along depth makes the cost of the depth averaging independent of $G$. This is the reason for the method: a [periodogram](/periodogram/) on a grid of $F$ frequencies costs $O(N F)$ per pixel, and a fit of a spectral model costs more.

## Properties

- **Exact for one tone** inside the Nyquist range, and exact for the center of any symmetric spectrum that is narrow enough (see Correctness).
- **Invariant to a complex gain.** Multiplying all samples by $a e^{i \varphi}$ scales $R_1$ by $|a|^2$, so $v$ does not change. The estimate does not depend on the strength of the echo.
- **Antisymmetric.** Conjugating the data or reversing the slow time order changes the sign of $v$.
- **Aliasing.** The estimate lies in $(-v_a, v_a]$; a true velocity outside that range wraps by multiples of $2 v_a$.
- **Variance.** The variance falls with the number of products $G(N-1)$ and with the signal to noise ratio; for one tone in white noise at high SNR the estimate is close to the [periodogram](/periodogram/) peak, the maximum likelihood estimate, but it is not efficient at low SNR or for wide spectra (Miller and Rochwarger 1972).
- **Bias from clutter.** Any slow or stationary component in the ensemble pulls the phase of $R_1$ toward zero. The clutter filter must come first.

## Variants and improvements

- **Depth averaging.** The sum over $g$ in lines L1 and L2 is the usual form in scanners; it trades depth resolution for variance.
- **Two-dimensional autocorrelator** (Loupas, Powers and Gill 1995). It also estimates the mean RF frequency from the correlation along depth and uses it in place of $f_0$, which removes the bias from the frequency dependent attenuation of tissue.
- **Higher lags.** $\arg R(m)$ divided by $m$ gives a finer estimate when there is no aliasing at lag $m$; combinations of lags extend the measurable range.
- **Staggered PRF** and dual-PRF methods unwrap the aliased velocity with two pulse intervals, as in weather radar.
- **Power Doppler.** The value $R_0$ after the clutter filter alone is the power Doppler image, which shows where blood is but not how fast it moves.
- **Spectral Doppler.** A short-time Fourier transform of a long ensemble at one gate shows the full velocity distribution; it is the method for quantitative peak velocities.

## When to use it

Use the Kasai estimator for color flow and tissue Doppler imaging, where each pixel has only 8 to 16 pulses and the whole image must be computed at frame rate. Use spectral Doppler at one gate when the distribution of velocities or the peak velocity matters. Use the [SVD clutter filter](/svd-clutter-filter/) or another clutter filter before it, and use a longer ensemble or depth averaging when the variance is too high.

## Pitfalls

- **No clutter filter.** Applied to raw data, line L2 is dominated by the tissue echo, which is often tens of decibels stronger than the blood echo, and the estimate is close to zero. Filter first. With tissue 10 times stronger in amplitude than blood at 0.25 m/s, the test gets an estimate below 0.05 m/s.
- **Aliasing.** Flow faster than $v_a$ shows with the opposite sign. Raise the PRF, lower $f_0$, or unwrap the phase in space with care, since a jump of $2 v_a$ inside a vessel looks like a real change of direction.
- **Wrong sign convention.** If the demodulation uses $e^{+i 2 \pi f_0 t}$, the sign of $v$ flips. Check the convention of the IQ data before reading line L3.
- **Mean phase in place of the phase of the mean.** Averaging the phases of the products instead of the products themselves wraps at $\pm \pi$ and gives weak samples the same weight as strong ones. Line L2 averages the complex products, then takes one phase.
- **Normalization of R1.** Dividing by $G(N-1)$ in line L2 and by $GN$ in line L1 matters for the width of line L4: with other factors the ratio $|R_1|/R_0$ is off for short ensembles.
- **Angle.** The method measures only the axial component $v \cos\theta$. Flow across the beam shows as zero velocity.

## Implementations

The Python code takes the ensembles of one pixel as lists of complex numbers. It uses no helper. The tests check the check value 0.385 m/s, exactness for one tone, the wrap of $0.5$ m/s to $-0.27$ m/s, the invariances, the exact phase for a symmetric discrete spectrum, the estimate on a random process with a symmetric spectrum, and compare noisy estimates with the periodogram peak as a reference.

## History

The phase of the autocorrelation at one lag was used in weather radar to estimate the mean Doppler frequency, where it is known as the pulse-pair method; Miller and Rochwarger (1972) gave its statistical analysis as a covariance approach to spectral moment estimation. Kasai, Namekawa, Koyano and Omoto (1985) used it for ultrasound and built a real-time two-dimensional blood flow imager with it, which led to color flow imaging in clinical scanners. Loupas, Powers and Gill (1995) extended it to a two-dimensional autocorrelator over slow time and depth.

## References
