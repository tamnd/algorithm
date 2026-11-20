---
tag: R4DMS8
kind: algorithm
slug: omega-k-algorithm
name: Omega-k algorithm
aliases:
- wavenumber domain algorithm
- range migration algorithm
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: "Focus SAR data exactly in the 2D frequency domain by a reference function multiply and a Stolt change of variables."
solves: [sar-image-formation]
model: real-ram
complexity:
  vars: {M: the number of pulses, N: the number of range samples per pulse, K: the number of taps of the Stolt interpolator}
  time: {worst: O(M N (log(M N) + K))}
  space: {extra: O(M N), data: O(M N)}
properties: {deterministic: true, linear_in_data: true, recursive: false, exact: false}
history:
  year: 1991
  people: [Ciro Cafforio, Claudio Prati, Fabio Rocca]
  note: "Cafforio, Prati and Rocca derived SAR focusing from the seismic migration of Stolt in 1991, which gave the wavenumber domain algorithm."
prereqs: [range-doppler-algorithm, stolt-migration]
see_also: [chirp-scaling-algorithm, range-cell-migration, sar-image-formation, exploding-reflector-model, seismic-migration, sinc-interpolation, polar-format-algorithm, sar-backprojection]
sources:
  - paper: doi:10.1109/7.78293
    title: "Ciro Cafforio, Claudio Prati and Fabio Rocca, SAR data focusing using seismic migration techniques, IEEE Transactions on Aerospace and Electronic Systems 27(2), 1991, 194 to 207"
    locator: "the SAR record as a zero-offset seismic section and its focusing by the Stolt mapping (general locator)"
  - paper: doi:10.1190/1.1440826
    title: "R. H. Stolt, Migration by Fourier transform, Geophysics 43(1), 1978, 23 to 48"
    locator: "the change of variables from temporal frequency to vertical wavenumber (general locator)"
  - book: isbn:9781580530583
    title: "Ian G. Cumming and Frank H. Wong, Digital Processing of Synthetic Aperture Radar Data, Artech House, 2005"
    locator: "Chapter 8, The Omega-K Algorithm"
  - paper: doi:10.1109/36.158864
    title: "Richard Bamler, A comparison of range-Doppler and wavenumber domain SAR focusing algorithms, IEEE Transactions on Geoscience and Remote Sensing 30(4), 1992, 706 to 713"
    locator: "the wavenumber domain algorithm as the reference without approximation for a straight track (general locator)"
  - book: isbn:0890067287
    title: "Walter G. Carrara, Ron S. Goodman and Ronald M. Majewski, Spotlight Synthetic Aperture Radar: Signal Processing Algorithms, Artech House, 1995"
    locator: "the range migration algorithm for spotlight data (general locator)"
---

The omega-k algorithm, also called the wavenumber domain algorithm or the range migration algorithm, focuses [synthetic aperture radar](/synthetic-aperture-radar/) data from a straight track with a constant speed in the two-dimensional frequency domain. The name "range migration algorithm" means this algorithm; it should not be confused with [range cell migration](/range-cell-migration/), the effect that every SAR focusing method must correct. After a 2D FFT, the phase of a point target is $-R_0 \sqrt{K^2 - k_x^2} - k_x x_0$, where $K$ is the range wavenumber and $k_x$ the along-track wavenumber. A multiply by a reference function focuses the targets at one reference range exactly. The Stolt change of variables, an interpolation in range frequency, then makes the remaining phase linear for every range, and one 2D inverse FFT focuses the whole scene. It is the radar form of [Stolt migration](/stolt-migration/) of seismic data, and for its geometry it makes no approximation beyond the stationary phase step.

## In plain words

Each point on the ground leaves a curved, smeared trace in the radar data. Instead of tracing those curves one by one, the omega-k method looks at the data as a sum of waves. In that view, the blur of a point has a simple formula that depends only on the distance to the point. A first multiply removes the blur exactly for points at one chosen distance. For the other points, a stretch of the frequency axis, the same for every point, finishes the job. After the stretch, one inverse transform gives a sharp image of every point at once.

## The problem

The input is the raw data $s[p][j]$ of $M$ pulses on a straight track at the speed $V$ and the pulse rate PRF, with $N$ range samples at the rate $f_s$ from the two-way time $t_{\text{start}}$, that is from the range $r_{\text{start}}$ with bins of $\Delta r = c/(2f_s)$. The pulse is a chirp $p$ of bandwidth $B$, the carrier is $f_0$, and the squint is zero. A target at $(x_0, R_0)$ gives $a\, p(\tau - 2R(\eta)/c)\, e^{-i 4\pi f_0 R(\eta)/c}$ with $R(\eta) = \sqrt{R_0^2 + (V\eta - x_0)^2}$. The page uses the Fourier sign $e^{-i 2\pi f t}$ of the DFT; radar books often use $e^{+j\omega t}$ and the opposite signs. For the range frequency $f_r$ and the Doppler frequency $f_a$, write $K = 4\pi (f_0 + f_r)/c$ and $k_x = 2\pi f_a / V$. The output is the complex image on the $M \times N$ grid, as for [SAR image formation](/sar-image-formation/).

## The algorithm

```pseudo id=main
OMEGA-K(s, P, f_0, V, PRF, r_ref)    ▷ s[p][j]: raw pulse p, range sample j; P = DFT(chirp)
L1  S ← 2D DFT of s                                       ▷ range f_r (index q) and Doppler f_a (index k)
L2  S[k][q] ← S[k][q] · conj(P[q]) · e^{-i 2π f_r t_start}             ▷ range compression, absolute time
L3  S[k][q] ← S[k][q] · G e^{+i r_ref sqrt(K² - k_x²)}                ▷ reference function multiply
L4  T[k][q'] ← S[k][·] read at f_r = sqrt((f_0 + f_r')² + (c f_a / (2V))²) - f_0    ▷ Stolt mapping
L5  T[k][q'] ← T[k][q'] · e^{-i 2π f_r' · 2 (r_ref - r_start) / c}       ▷ put r_ref at its bin
L6  I ← 2D IDFT of T
L7  image[p][j] ← I[p][j] · e^{+i 4π f_0 (r_start + j Δr - r_ref) / c}     ▷ restore the carrier phase
```

Line L1 is a 2D FFT. Line L2 is [pulse compression](/pulse-compression/) by the [matched filter](/matched-filter/), and the factor $e^{-i 2\pi f_r t_{\text{start}}}$ refers the range phase to the time of transmission, so the phase of a target becomes $-K R(\eta)$. By stationary phase in $\eta$, the 2D spectrum of the target is $|P|^2 e^{-i R_0 \sqrt{K^2 - k_x^2} - i k_x x_0}$ times a slowly varying amplitude. Line L3 multiplies by the conjugate phase of the reference range, with the gain $G = \text{PRF}/\sqrt{K_a}$ of the azimuth compression. What is left is $e^{-i (R_0 - r_{\text{ref}}) \sqrt{K^2 - k_x^2}}$, which is still not linear in $f_r$. Line L4 is the Stolt mapping: it defines a new range frequency $f_r'$ by $\sqrt{K^2 - k_x^2} = 4\pi (f_0 + f_r')/c$ and reads the old spectrum at the matching $f_r$ by [sinc interpolation](/sinc-interpolation/), for $|f_r'| \le B/2$. Now the phase is $-4\pi (f_0 + f_r')(R_0 - r_{\text{ref}})/c - k_x x_0$, linear in both frequencies. Line L5 adds the shift that makes the inverse DFT of L6 put each target at the bin of its $R_0$ and the pulse of its $x_0$. Line L7 removes the constant $e^{-i 4\pi f_0 (R_0 - r_{\text{ref}})/c}$ that is left at each range.

## Example

The tests use the geometry of the range-Doppler algorithm: $f_0 = 300$ MHz, $B = 100$ MHz, $T = 0.2$ us, $f_s = 120$ MHz (bins of 1.25 m), $V = 100$ m/s, PRF $= 80$ Hz, $M = 128$, $N = 64$ from 380 m, a beam with the sine of the half angle 0.125, and $r_{\text{ref}}$ in the middle of the window. Three targets with complex amplitudes give, at their predicted pixels:

| target $(x_0, R_0)$, amplitude | peak / matched filter | phase of peak / amplitude |
|---|---|---|
| (0 m, 400 m), 1 | 0.924 | $-43.7$ degrees |
| (10 m, 410 m), $0.6i$ | 0.911 | $-43.6$ degrees |
| (-12.5 m, 425 m), $-0.5$ | 0.906 | $-44.1$ degrees |

The common phase of about $-44$ degrees is the $e^{-i\pi/4}$ of the azimuth stationary phase, so the ratios of complex amplitudes are kept, within 0.06 in the tests. With a wide beam (sine of the half angle 0.35, PRF $= 200$ Hz, $M = 256$, window from 80 m) and $r_{\text{ref}} = 120$ m, a target at $R_0 = 96$ m reaches 0.957 of its ideal peak. With L4 skipped, that is with the reference multiply alone, it reaches only 0.213, while a target at $R_0 = r_{\text{ref}}$ is focused the same with or without L4. In the same wide case the basic [range-Doppler algorithm](/range-doppler-algorithm/) reaches 0.855. These values are measurements on these simulations.

## Correctness

The algorithm is linear. In the 2D frequency domain, by stationary phase in the slow time, a target has the phase $-R_0 \sqrt{K^2 - k_x^2} - k_x x_0$; this is the only approximation, and it uses no expansion of the square root in range frequency or Doppler, unlike the range-Doppler algorithm. The reference multiply leaves $-(R_0 - r_{\text{ref}})\sqrt{K^2 - k_x^2}$, and the Stolt mapping makes $\sqrt{K^2 - k_x^2}$ the new range wavenumber, so the phase becomes linear in both new frequencies for every $R_0$ at once. An inverse DFT of a linear phase is a peak at the right place. So the algorithm is exact for a straight track at a constant speed, up to the stationary phase step and the interpolation of L4. The proofs are in proofs/correctness.md.

## Complexity

Lines L1 and L6 are 2D FFTs of $M \times N$ samples, $O(M N \log(M N))$. Lines L2, L3, L5 and L7 cost $O(1)$ per sample. Line L4 costs $O(K)$ per output sample with a $K$-tap interpolator. The total is $O(M N (\log(M N) + K))$ in the real-RAM model, with $O(M N)$ extra space.

## Properties

- Linear in the data.
- Exact for the hyperbolic range history of a straight track at constant speed, including wide beams, high squint and long apertures, up to stationary phase and interpolation.
- Range-invariant: every operation is in the 2D frequency domain, so it cannot follow a speed or a geometry that changes with range, such as the curved orbit of a satellite. Variants handle that approximately.
- The only interpolation is the 1D Stolt mapping along range frequency.

## Variants and improvements

- **Approximate Stolt mapping.** Replace L4 by a phase multiply that is exact at the reference range and a range-varying correction later, which gives an algorithm close to the [chirp scaling algorithm](/chirp-scaling-algorithm/).
- **Spotlight data.** For dechirped spotlight data the same mapping applies after the deramp; Carrara, Goodman and Majewski call it the range migration algorithm. The [polar format algorithm](/polar-format-algorithm/) uses a polar instead of a Stolt resampling.
- **Seismic and ultrasonic imaging.** With the [exploding reflector model](/exploding-reflector-model/), the same mapping is [Stolt migration](/stolt-migration/), and in ultrasound it is the frequency domain form of the [synthetic aperture focusing technique](/saft/).
- **Satellite orbits.** An effective speed that changes with range is handled by range blocks or by extra correction terms.

## When to use it

Use omega-k for straight-track data with wide beams, high squint or long apertures, where the approximations of the range-Doppler algorithm fail, as in low-frequency and airborne systems with wide beams. It needs an interpolation, which the chirp scaling algorithm avoids, but it makes fewer approximations. For curved tracks or a speed that varies, use [backprojection](/sar-backprojection/).

## Pitfalls

- **Missing time reference.** Without the factor $e^{-i 2\pi f_r t_{\text{start}}}$ in L2, the phase is relative to the start of the record, not to the transmission, and L3 no longer matches.
- **Interpolating in the wrong order.** The spectrum must be in increasing frequency order (after an fftshift) before L4 reads it at fractional positions; the wrapped DFT order puts the band edges next to each other.
- **Reading outside the band.** For large $|f_a|$ the Stolt mapping asks for frequencies above the band; L4 must restrict $f_r'$ to $|f_r'| \le B/2$ and leave the rest zero.
- **Targets near the ends of the range window.** The 2D FFT is circular, so a chirp that runs past the last sample wraps. In the tests a target at 385 m, near the start of the window, measured only 0.75 of its ideal peak.
- **The carrier phase.** Without L7, the phase of each target varies with $R_0 - r_{\text{ref}}$; the modulus is right, but interferometry fails.

## Implementations

## History

Stolt (1978) introduced migration by Fourier transform for seismic data, a change of variables from temporal frequency to vertical wavenumber. Cafforio, Prati and Rocca (1991) showed that SAR focusing is a migration problem of the same kind and derived the wavenumber domain algorithm from it. Bamler (1992) compared it with the range-Doppler algorithm and showed that it is free of the approximations of the latter for a straight track. Carrara, Goodman and Majewski (1995) described its spotlight form as the range migration algorithm. Cumming and Wong (2005, Chapter 8) call it the omega-K algorithm.

## References
