---
tag: HE5XFQ
kind: algorithm
slug: delay-and-sum-beamforming
name: Delay-and-sum beamforming
aliases:
- DAS beamformer
area: graphics-and-signals/signal-processing
level: core
summary: "Steer a sensor array to one direction: delay each sensor so that a wave from there lines up, then average. Gain M against white noise; spacing above half a wavelength gives grating lobes."
solves: [beamforming]
model: real-ram
complexity:
  vars: {M: the number of sensors, T: the number of samples per sensor}
  time: {worst: O(M T)}
  space: {extra: O(M)}
properties: {deterministic: true, online: true, recursive: false, exact: true}
history:
  year: 1905
  people: [Karl Ferdinand Braun]
  note: "Braun steered a radio transmission in 1905 with three antennas and a switchable quarter-wave delay; delay-and-sum arrays then grew in sonar, radar and radio astronomy, and Van Veen and Buckley gave the standard account in 1988."
prereqs: [beamforming]
see_also: [aliasing, sampling-theorem, window-functions, music-algorithm, esprit, matched-filter, adaptive-filtering, periodogram]
sources:
  - paper: doi:10.1109/53.665
    title: "Barry D. Van Veen and Kevin M. Buckley, Beamforming: A versatile approach to spatial filtering, IEEE ASSP Magazine 5(2), 1988, pages 4 to 24"
    locator: "the section on data-independent beamforming: the delay-and-sum beamformer, its beam pattern, and the effect of the element spacing"
  - book: isbn:9780130485137
    title: "Don H. Johnson and Dan E. Dudgeon, Array Signal Processing, Concepts and Techniques, Prentice Hall, 1993"
    locator: "Chapter 4, Beamforming: Section 4.1 (delay-and-sum beamforming), Section 4.5 (array gain), Section 4.6 (resolution) and Section 4.8 (discrete-time beamforming)"
  - book: isbn:9780471093909
    title: "Harry L. Van Trees, Optimum Array Processing, Part IV of Detection, Estimation, and Modulation Theory, Wiley, 2002"
    locator: "Chapter 2 (the uniform linear array, its beam pattern, the main lobe and the nulls, grating lobes, and array steering)"
---

Delay-and-sum beamforming is the simplest way to point an array of sensors at one direction. A wave from that direction reaches the sensors at different times. The beamformer delays each sensor by the amount that lines the wave up, and averages the sensors. The wave from the look direction adds in phase and comes out unchanged, and noise that is independent from sensor to sensor partly cancels, so the signal-to-noise ratio grows by the number of sensors $M$. Waves from other directions do not line up and are attenuated by the beam pattern, which for a uniform line of sensors is the Dirichlet kernel $|\sin(M\psi/2) / (M \sin(\psi/2))|$. When the sensors are more than half a wavelength apart, the array samples the wave too coarsely in space, and for some look directions other directions get the full gain too: these are the grating lobes. Delay-and-sum is the data-independent solution of the [beamforming](/beamforming/) problem. It needs only the geometry and the speed of the wave, not the statistics of the data.

## In plain words

Picture a row of microphones and a person talking from the left. The sound reaches the leftmost microphone first and the others a little later, one after another. Hold back each recording by the right amount, so that the voice starts at the same moment in all of them, and add them up. The voice gets stronger, because all copies agree. The hiss of each microphone is different, so the copies disagree and partly cancel. A sound from another direction arrives with other delays, so it does not line up and comes out weaker. To listen in a new direction, change the delays. If the microphones are too far apart, some other direction can line up just as well, and the array cannot tell the two apart.

## The problem

The input is the signals $x_0, \ldots, x_{M-1}$ of $M$ sensors, each with $T$ samples at the rate $f_s$, the positions $p_0, \ldots, p_{M-1}$ of the sensors along a line, the speed $c$ of the wave, and the look direction, given as $u_0 = \sin\theta_0$ with the angle $\theta_0$ measured from broadside. A plane wave from the direction $u$ reaches sensor $m$ later than the origin by $p_m u / c$ seconds, so sensor $m$ records $x_m[t] = s[t - \tau_m] + n_m[t]$ for a source $s$ and noise $n_m$. The output is one signal $y$ that holds the wave from $u_0$ at full gain and attenuates the rest. For a planar or 3D array the delay is $p_m \cdot k / c$ with the unit vector $k$ of the direction; nothing else changes.

## The algorithm

```pseudo id=main
DELAY-AND-SUM(x₀ .. x_{M−1}, p₀ .. p_{M−1}, u₀, c, f_s)
L1  for m ← 0 to M − 1: τ_m ← round(f_s · p_m · u₀ / c)   ▷ the arrival delay in samples
L2  τ_min ← min τ_m; Δ ← max τ_m − τ_min
L3  for t ← 0 to T − Δ − 1 do
L4      acc ← 0
L5      for m ← 0 to M − 1 do
L6          acc ← acc + x_m[t + τ_m − τ_min]   ▷ undo the delay of sensor m
L7      y[t] ← acc / M
L8  return y
```

Line L1 computes how much later the wave from $u_0$ reaches each sensor. Line L2 takes the earliest sensor as the reference, so that every index in line L6 is at least $0$, and finds the spread $\Delta$ of the delays, which limits the output to $T - \Delta$ samples. Line L6 reads each sensor $\tau_m - \tau_{\min}$ samples ahead, which cancels its delay. A wave from $u_0$ then contributes the same sample $s[t - \tau_{\min}]$ from every sensor, and line L7 averages, so it comes out with gain $1$. A real-time beamformer delays the other sensors instead of reading ahead, which gives the same output $\Delta$ samples later.

**Narrowband form.** For a signal in a narrow band around the wavelength $\lambda$, a delay is a phase shift. For a uniform linear array with spacing $d$, the snapshot of a unit wave from $u$ is the steering vector $a(u)$ with $a_m(u) = e^{-i 2\pi (d/\lambda) m u}$, and delay-and-sum is the weighted sum $y = w^H x$ with $w = a(u_0)/M$. Its response to a wave from $u$ is

$$B(u) = |w^H a(u)| = \left| \frac{\sin(M\psi/2)}{M \sin(\psi/2)} \right|, \qquad \psi = 2\pi \frac{d}{\lambda} (u - u_0),$$

with $B = 1$ where $\psi$ is a multiple of $2\pi$. It is the [frequency response](/frequency-response/) of an $M$-point moving average, read in the spatial frequency $\psi$. Delays that are not whole samples need interpolation, or the narrowband form in each bin of a short-time transform.

## Example

**Alignment.** Take $M = 3$ sensors with the delays $\tau = (0, 1, 2)$ and the source $s = (5, 1, 3, 2)$, so that $x_0 = (5, 1, 3, 2, 0, 0)$, $x_1 = (0, 5, 1, 3, 2, 0)$ and $x_2 = (0, 0, 5, 1, 3, 2)$. Then $\Delta = 2$, and line L6 reads $x_0[t]$, $x_1[t + 1]$ and $x_2[t + 2]$, which are all $s[t]$. The output is $y = (5, 1, 3, 2)$, the source exactly.

**Beam pattern.** Take $M = 4$, $d = \lambda/2$ and the look direction $u_0 = \frac12$, which is $30$ degrees.

| $u$ | $\psi$ | $B(u)^2$ | $B(u)$ |
|---|---|---|---|
| $1$ | $\pi/2$ | $0$ | $0$ |
| $3/4$ | $\pi/4$ | $(2 + \sqrt2)/8$ | $0.653$ |
| $1/2$ | $0$ | $1$ | $1$ |
| $1/4$ | $-\pi/4$ | $(2 + \sqrt2)/8$ | $0.653$ |
| $0$ | $-\pi/2$ | $0$ | $0$ |
| $-1/4$ | $-3\pi/4$ | $(2 - \sqrt2)/8$ | $0.271$ |
| $-1/2$ | $-\pi$ | $0$ | $0$ |
| $-3/4$ | $-5\pi/4$ | $(2 - \sqrt2)/8$ | $0.271$ |
| $-1$ | $-3\pi/2$ | $0$ | $0$ |

The peak is at the look direction, the nulls are where $\psi$ is a nonzero multiple of $2\pi/M = \pi/2$, and the sidelobe between them is at $0.271$, which is $-11.3$ dB. With $d = \lambda$ and the same look direction, $\psi$ doubles: $u = -\frac12$ now has $\psi = -2\pi$ and $B = 1$. A wave from $-30$ degrees passes at full gain, a grating lobe, and the array cannot tell it from the look direction.

## Correctness

**Claim.** If sensor $m$ records $s[t - \tau_m] + n_m[t]$ with the delays of line L1, the output is $y[t] = s[t - \tau_{\min}]$ plus the average of the $M$ noise samples, whose variance is $\sigma^2/M$ for uncorrelated noise of variance $\sigma^2$. For a uniform linear array, $B(u) \le 1 = B(u_0)$, with equality exactly where $(d/\lambda)(u - u_0)$ is an integer. A grating lobe exists exactly when $d \ge \lambda/(1 + |u_0|)$, so some look direction strictly between the endfire directions has one exactly when $d > \lambda/2$.

**Key invariant.** After line L6 has run for sensors $0$ to $m$, $acc$ holds $(m + 1)\, s[t - \tau_{\min}]$ plus the noise samples of these sensors.

The pattern is a geometric sum, and the triangle inequality shows that it reaches its largest value $M$ only when all its terms are equal. The grating lobes are the other solutions in $[-1, 1]$, and checking the one nearest to $u_0$ gives the exact condition. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Line L1 costs $O(M)$. Lines L3 to L7 run $T - \Delta$ times, with $M$ additions and one division each, so the total is $O(M T)$ in the [real RAM](/real-ram/), and $O(M)$ per output sample. The extra space is $O(M)$ for the delays, besides the input and the output. A real-time version keeps a delay line of $\Delta + 1$ samples per sensor. The narrowband form costs $M$ complex multiplications per snapshot. Scanning $K$ look directions costs $K$ times as much, or $O(T M \log M)$ in total for $K = M$ directions of a uniform array with an FFT across the sensors.

## Properties

- **Distortionless.** The wave from the look direction passes with gain $1$ and no change of shape, at every frequency, when the delays are exact.
- **Optimal against white noise.** The array gain $M$ is the largest that any weights reach against noise that is uncorrelated between sensors with equal power, by the Cauchy-Schwarz inequality.
- **No nulls on interferers.** The pattern depends only on the geometry. A strong source in a sidelobe leaks through at the sidelobe level, $-13.3$ dB for a large uniform array. Adaptive beamformers place nulls on it instead.
- **Resolution.** The main lobe runs between the first nulls at $u - u_0 = \pm \lambda/(M d)$, so the beam is narrower for a longer aperture $M d$. Two sources closer than about this width give one peak in a scan.
- **Frequency dependent beam.** The delays are the same at every frequency, but $\psi$ grows with frequency, so the beam of a broadband signal is wide at low frequencies and narrow at high ones.
- **Grating lobes.** With $d > \lambda/2$, steering far enough from broadside makes a grating lobe enter from the other endfire direction. With $d \ge \lambda$ there is one even at broadside. This is [aliasing](/aliasing/) in space, the analogue of the [sampling theorem](/sampling-theorem/): to avoid it at every steering angle, sample the wave at least twice per wavelength.
- **Robust.** Small errors in the positions or the gains of the sensors change the pattern only a little, unlike optimum beamformers, which can cancel the wanted signal.

## Variants and improvements

- **Weighted delay-and-sum.** Multiply sensor $m$ by a taper $g_m$ before the sum. A Hann, Taylor or Dolph-Chebyshev taper lowers the sidelobes and widens the main lobe, the same tradeoff as [window functions](/window-functions/) in spectral analysis.
- **Fractional delays.** Interpolate between samples with a short FIR filter, upsample, or apply the delays as phase shifts in each frequency bin of a short-time transform.
- **Filter-and-sum.** Give each sensor an FIR filter, to shape the beam over frequency and keep its width constant.
- **Near-field focusing.** Compute the delays from the distance of each sensor to a point, not a plane wave. Ultrasound imaging focuses this way on each pixel.
- **Steered response power.** Scan $u_0$ and measure the output power. Its peaks estimate the directions of the sources. This is the spatial [periodogram](/periodogram/). [MUSIC](/music-algorithm/) and [ESPRIT](/esprit/) resolve sources that are closer together.
- **Adaptive beamformers.** The MVDR beamformer and the generalized sidelobe canceller start from the delay-and-sum weights and add an [adaptive filtering](/adaptive-filtering/) part that cancels interference.
- **Transmit beamforming.** The same delays applied to the signals sent from each element form a beam in transmission, as in a phased-array radar.

## When to use it

Use delay-and-sum when the geometry of the array is known and a robust, cheap beam is needed: microphone arrays in conference systems and hearing aids, ultrasound image formation, radio telescope arrays, sonar and radar with fixed beams, and as the reference against which other beamformers are measured. It is the best choice against diffuse or sensor noise. When strong interferers come from known or unknown directions, use an adaptive beamformer such as MVDR. To find the directions of several close sources, use a subspace method. Design the array with $d \le \lambda/2$ at the highest frequency, or limit the steering angles, to avoid grating lobes.

## Pitfalls

- **The sign of the delay.** Line L6 written as $x_m[t - \tau_m + \tau_{\min}]$ doubles the delays in place of cancelling them, and the array points at $-u_0$ instead of $u_0$. Read ahead by $\tau_m - \tau_{\min}$, or delay every other sensor by $\max \tau - \tau_m$.
- **Missing reference shift.** Line L6 as $x_m[t + \tau_m]$ without $\tau_{\min}$ reads past the end of the signal when some delay is positive, and before its start for negative delays when $u_0 < 0$. Subtract $\tau_{\min}$ and stop the loop of line L3 at $T - \Delta$.
- **Rounding the delays.** Line L1 rounds to whole samples. With a delay of $3.4$ samples rounded to $3$, high frequencies no longer add in phase and the main lobe shifts. Use a higher sample rate, fractional-delay filters or phase shifts per frequency bin.
- **Degrees in place of the sine.** Line L1 needs $u_0 = \sin\theta_0$. Writing $\theta_0$ in radians there points the beam to a wrong angle except near broadside.
- **Spacing for the wrong frequency.** An array designed with $d = \lambda/2$ for the middle of the band has $d > \lambda/2$ at the top of the band, and grating lobes appear there when the beam is steered. Choose $d$ for the highest frequency, or low-pass the sensors.
- **A grating lobe taken for a source.** In a scan with $d > \lambda/2$, the peaks at $u_0 + k\lambda/d$ have the full height. Check every peak against the lobe positions before you report a direction.

## Implementations

## History

Karl Ferdinand Braun steered a radio transmission in 1905 in Strasbourg with three antennas at the corners of a triangle, with a quarter-wave delay that could be switched into the feed of one of them, and he described the directional effect in his Nobel lecture of 1909. In the First World War, arrays of microphones and hydrophones were steered to a target by mechanical delay lines, and in the 1930s and 1940s phased antenna arrays became part of radar. Radio astronomers formed beams on the sky with arrays of dipoles from the 1950s. Digital processing then made the delays programmable, so that one array forms many beams at once. Van Veen and Buckley's 1988 tutorial set delay-and-sum as the data-independent beamformer in a common framework with the statistically optimum and adaptive methods, and Johnson and Dudgeon (1993) and Van Trees (2002) give the textbook account.

## References
