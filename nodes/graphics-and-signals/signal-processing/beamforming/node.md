---
tag: 3BMGCR
kind: problem
slug: beamforming
name: Beamforming
aliases:
- spatial filtering
area: graphics-and-signals/signal-processing
level: core
summary: "Combine the signals of an array of sensors with weights or delays so that the array passes a wave from a chosen direction and weakens waves and noise from other directions."
prereqs: [discrete-time-fourier-transform]
see_also: [delay-and-sum-beamforming, music-algorithm, esprit, adaptive-filtering, window-functions, aliasing, spectral-estimation, matched-filter]
sources:
  - paper: doi:10.1109/53.665
    title: "Barry D. Van Veen and Kevin M. Buckley, Beamforming: A versatile approach to spatial filtering, IEEE ASSP Magazine 5(2), 1988, pages 4 to 24"
    locator: "the data model, the beam pattern, data-independent and statistically optimum beamformers, and adaptive algorithms"
  - book: isbn:9780471093909
    title: "Harry L. Van Trees, Optimum Array Processing, Part IV of Detection, Estimation, and Modulation Theory, Wiley, 2002"
    locator: "Chapter 2 (arrays and spatial filters, beam patterns, uniform linear arrays and array steering), Chapter 6 (optimum waveform estimation, MVDR and LCMV) and Chapter 7 (adaptive beamformers)"
  - paper: doi:10.1109/PROC.1969.7278
    title: "J. Capon, High-resolution frequency-wavenumber spectrum analysis, Proceedings of the IEEE 57(8), 1969, pages 1408 to 1418"
    locator: "the minimum-variance distortionless response weights"
  - paper: doi:10.1109/PROC.1972.8817
    title: "Otis Lamont Frost III, An algorithm for linearly constrained adaptive array processing, Proceedings of the IEEE 60(8), 1972, pages 926 to 935"
    locator: "the linearly constrained minimum-variance criterion and its constrained LMS algorithm"
---

Beamforming is the problem of combining the outputs of $M$ sensors at different positions, such as antennas, microphones or hydrophones, into one output that responds strongly to a wave from a chosen direction and weakly to waves and noise from other directions. A wave from direction $\theta$ reaches each sensor at a slightly different time, and the pattern of these delays is the signature of the direction. A beamformer applies a weight, a delay or a filter to each sensor and adds the results. Choosing these to shape the response over direction is filtering in space, as an ordinary filter shapes the response over frequency. The simplest solution is [delay-and-sum beamforming](/delay-and-sum-beamforming/); the statistically optimum ones adapt the weights to the measured noise and interference.

## In plain words

Several microphones listen to the same room. A voice from one side reaches the near microphones a little earlier than the far ones. If you delay each microphone by the right amount so that the voice lines up in all of them, and then add them, the voice adds up strongly. Sounds from other directions do not line up, so they partly cancel. Random noise in each microphone also partly cancels. That is a beam: a direction in which the group listens well. Smarter rules also look at where the unwanted sounds come from and place deep blind spots on them, at the cost of more computation and more risk if the setup is not exactly as assumed. The same ideas steer radar beams, phone signals and ultrasound scans.

## Definition

**Narrowband model.** Sensors at positions $p_1, \ldots, p_M$ receive a plane wave of wavelength $\lambda$ from a direction with unit vector $k(\theta)$. After demodulation to complex baseband, one snapshot of the array is

$$x[t] = a(\theta)\, s[t] + n[t], \qquad a_m(\theta) = e^{-i 2\pi\, p_m \cdot k(\theta) / \lambda},$$

where $s$ is the source signal, $a(\theta)$ is the steering vector and $n$ holds noise and the other sources. For a uniform linear array with spacing $d$ along one axis and $\theta$ measured from broadside, $a_m(\theta) = e^{-i 2\pi (d/\lambda)\, m \sin\theta}$ for $m = 0, \ldots, M-1$.

**Task.** Find weights $w \in \mathbb{C}^M$ for the output $y[t] = w^H x[t]$. The beam pattern is $B(\theta) = w^H a(\theta)$, the response to a unit wave from $\theta$.

**Criteria.**

- *Data independent.* Meet a specification for $|B(\theta)|$: gain $1$ at the look direction $\theta_0$, a given width of the main lobe, and low sidelobes.
- *Maximum SINR.* Maximize the ratio of the signal power to the power of interference plus noise, $\sigma_s^2 |w^H a(\theta_0)|^2 / (w^H R_n w)$, where $R_n$ is the covariance of $n$.
- *Minimum variance distortionless response (MVDR).* Minimize the output power $w^H R w$ subject to $w^H a(\theta_0) = 1$. The solution is $w = R^{-1} a(\theta_0) / (a(\theta_0)^H R^{-1} a(\theta_0))$.
- *Linearly constrained minimum variance (LCMV).* Minimize $w^H R w$ subject to $C^H w = f$, for several directions and responses at once.
- *Minimum mean-square error.* Minimize $E|y - s|^2$; this is the multichannel [Wiener filter](/wiener-filter/).

**Broadband model.** For signals that are not narrowband, each sensor gets an FIR filter instead of one weight (filter-and-sum), or the problem is solved in each frequency bin of a short-time transform.

## Variants

- **Receive and transmit.** The same weights shape the pattern of a transmitting array, by reciprocity.
- **Far field and near field.** A near source has curved wavefronts; the delays depend on distance as well as direction, and the beamformer focuses on a point. Medical ultrasound imaging focuses this way.
- **Data independent or adaptive.** Fixed weights from the geometry alone, or weights from the measured covariance $R$, updated as the scene changes. See [adaptive filtering](/adaptive-filtering/).
- **Analog, digital and hybrid.** Phase shifters before a single receiver, a digitizer per sensor, or a few digital channels feeding analog subarrays, as in large antenna systems.
- **Direction finding.** Scan the beam over $\theta$ and look for peaks of the output power. The same data model underlies the subspace methods [MUSIC](/music-algorithm/) and [ESPRIT](/esprit/), which estimate directions but are not beamformers.
- **Robust beamforming.** The steering vector or the array positions are known only approximately. Diagonal loading of $R$ and constraints on the norm of $w$ keep the optimum beamformers from cancelling the desired signal.

## Examples

**Two elements at half a wavelength.** Take $M = 2$, $d = \lambda/2$, look direction broadside, and $w = \tfrac12 (1, 1)$. With $u = \sin\theta$, $a(\theta) = (1, e^{-i\pi u})$ and

$$|B(\theta)| = \tfrac12 |1 + e^{-i\pi u}| = |\cos(\pi u / 2)|.$$

The gain is $1$ at broadside ($u = 0$), $\cos(\pi/4) \approx 0.707$ at $u = \tfrac12$ (30 degrees), and $0$ at endfire ($u = \pm 1$). A wave from endfire arrives half a period later at the second sensor and cancels exactly.

**Array gain against white noise.** Let $n$ be white with $R_n = \sigma^2 I$, and $w = a(\theta_0)/M$. The signal adds in phase, $w^H a(\theta_0) = 1$, and the noise power at the output is $\sigma^2 \|w\|^2 = \sigma^2 / M$. The signal-to-noise ratio grows by the factor $M$: $6$ dB for four sensors and $10$ dB for ten.

## Known algorithms

- **[Delay-and-sum beamforming](/delay-and-sum-beamforming/).** Delay each sensor to align the look direction and average. $O(M)$ operations per output sample, no statistics needed, the best array gain against white noise.
- **Tapered delay-and-sum.** Multiply the sensors by a window before the sum, such as a Dolph-Chebyshev or a Taylor taper. Lower sidelobes for a wider main lobe, the same tradeoff as [window functions](/window-functions/) in spectral analysis.
- **MVDR (Capon) beamformer.** $w \propto R^{-1} a(\theta_0)$. Forming and inverting a sample covariance costs $O(M^2)$ per snapshot and $O(M^3)$ per inversion; applying $w$ costs $O(M)$ per sample. It puts deep nulls on strong interferers.
- **LCMV beamformer and the generalized sidelobe canceller.** Several linear constraints, for example a unit response at the look direction and zeros at known jammers. The generalized sidelobe canceller writes the LCMV solution as a fixed beamformer minus an unconstrained adaptive noise canceller.
- **Adaptive beamformers.** Frost's constrained [LMS algorithm](/lms-algorithm/) at $O(M)$ per snapshot, [RLS](/rls-algorithm/) at $O(M^2)$, and sample matrix inversion, which estimates $R$ from $K$ snapshots. Reed, Mallett and Brennan showed that about $K = 2M$ snapshots keep the average loss in SINR within 3 dB.
- **Broadband beamformers.** Filter-and-sum with FIR filters per sensor, or narrowband beamformers in each frequency bin.

## Bounds

- **White-noise array gain.** For white noise, the SNR gain of any $w$ is $|w^H a|^2 / \|w\|^2 \le \|a\|^2 = M$ by the Cauchy-Schwarz inequality, with equality exactly for $w \propto a$. So delay-and-sum is optimal for white noise, and no beamformer gains more than $M$ against it.
- **Maximum SINR.** For any noise covariance $R_n$, the SINR is at most $\sigma_s^2\, a^H R_n^{-1} a$, reached by $w \propto R_n^{-1} a$. The MVDR, maximum SINR and MMSE criteria all give weights proportional to $R_n^{-1} a$, and differ only in scale.
- **Resolution.** For a uniform linear array with uniform weights, the main lobe in $u = \sin\theta$ runs from the look direction to the first nulls at $\pm \lambda/(M d)$. Two sources closer than about this width are not separated by a scanning beamformer. A longer aperture $M d$ gives a narrower beam.
- **Spatial aliasing.** A uniform linear array samples the wave in space. If $d > \lambda/2$, then for some look directions the pattern has grating lobes: other directions with the full gain of the main lobe. The exact condition is on the [delay-and-sum beamforming](/delay-and-sum-beamforming/) page, and it is the spatial form of [aliasing](/aliasing/).
- **Superdirectivity.** With closely spaced sensors, weights exist with a directivity above $M$, but $\|w\|$ becomes large, so the white-noise gain drops and small errors in the sensors destroy the pattern.

## Reductions

- **To FIR filter design.** For a uniform linear array, $B$ as a function of $\psi = 2\pi (d/\lambda) \sin\theta$ is the [frequency response](/frequency-response/) of an FIR filter with taps $\bar w_m$. Every FIR design method, from windows to the Parks-McClellan algorithm, designs array patterns.
- **To the Wiener filter.** The MMSE beamformer is the multichannel [Wiener filter](/wiener-filter/) $w = R^{-1} r_{xs}$, with $r_{xs} = E[x\, s^\ast] = \sigma_s^2 a(\theta_0)$.
- **To adaptive filtering.** The generalized sidelobe canceller turns the constrained problem into an unconstrained [adaptive filtering](/adaptive-filtering/) problem in interference-cancelling form.
- **To spectral estimation.** The output power of a scanning beamformer as a function of direction is a spatial [periodogram](/periodogram/) (delay-and-sum) or the Capon spectrum (MVDR); direction finding is [spectral estimation](/spectral-estimation/) in the spatial frequency.

## Applications

- **Radar and sonar.** Electronically steered beams, jammer nulling and direction finding.
- **Wireless communication.** Multi-antenna base stations steer beams to users and nulls to others; millimeter-wave systems need beams to close the link at all.
- **Microphone arrays.** Conference phones, smart speakers and hearing aids pick up a talker and reduce room noise and reverberation.
- **Medical ultrasound.** The image is formed by delay-and-sum focusing on each point.
- **Radio astronomy.** Arrays of dishes or dipoles form beams on the sky.
- **Seismology.** Arrays of seismometers estimate the direction and speed of waves.

## References
