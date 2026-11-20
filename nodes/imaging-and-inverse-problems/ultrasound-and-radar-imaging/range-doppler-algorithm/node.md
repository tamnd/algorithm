---
tag: 76HEMZ
kind: algorithm
slug: range-doppler-algorithm
name: Range-Doppler algorithm
aliases:
- RDA
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: core
summary: "Focus SAR data by range compression, range cell migration correction in the range-Doppler domain and azimuth matched filtering by FFT."
solves: [sar-image-formation]
model: real-ram
complexity:
  vars: {M: the number of pulses, N: the number of range samples per pulse, K: the number of taps of the interpolator}
  time: {worst: O(M N (log(M N) + K))}
  space: {extra: O(M N), data: O(M N)}
properties: {deterministic: true, linear_in_data: true, recursive: false, exact: false}
history:
  year: 1976
  people: [C. Wu]
  note: "Wu described a digital SAR processor in 1976; the method of range compression, migration correction in the range-Doppler domain and azimuth compression became the standard processor for stripmap data."
prereqs: [sar-image-formation, range-cell-migration, pulse-compression, fast-fourier-transform]
see_also: [chirp-scaling-algorithm, omega-k-algorithm, sar-backprojection, range-doppler-processing, matched-filter, sinc-interpolation, phase-gradient-autofocus, synthetic-aperture-radar]
sources:
  - paper: "C. Wu, A digital system to produce imagery from SAR data, AIAA Systems Design Driven by Sensors, paper 76-968, 1976"
    title: Wu 1976
    locator: "the digital processor with range compression and azimuth correlation (general locator; full text not seen)"
  - book: isbn:9781580530583
    title: "Ian G. Cumming and Frank H. Wong, Digital Processing of Synthetic Aperture Radar Data, Artech House, 2005"
    locator: "Chapter 6, The Range Doppler Algorithm, and Chapter 5, SAR Signal Properties"
  - paper: doi:10.1109/36.158864
    title: "Richard Bamler, A comparison of range-Doppler and wavenumber domain SAR focusing algorithms, IEEE Transactions on Geoscience and Remote Sensing 30(4), 1992, 706 to 713"
    locator: "the approximations of the range-Doppler algorithm against the wavenumber domain algorithm (general locator)"
---

The range-Doppler algorithm (RDA) focuses stripmap [synthetic aperture radar](/synthetic-aperture-radar/) data with one-dimensional FFTs and one interpolation. It first compresses each pulse in range with the [matched filter](/matched-filter/) of the chirp. Then it takes an FFT along the track for every range bin, into the range-Doppler domain. There, all targets at one closest range follow one curve of [range cell migration](/range-cell-migration/), so a range-varying interpolation straightens all of them together. Last, it multiplies each Doppler line by the azimuth matched filter of its range and takes the inverse FFT along the track. It is not the [range-Doppler processing](/range-doppler-processing/) of pulse-Doppler radar, which estimates the range and the radial velocity of targets from a burst of pulses; the RDA forms an image.

## In plain words

The raw data hold, for every pulse, a long smeared echo of every point. The first step sharpens each pulse along the range direction. The echo of one point still runs along the flight direction as a long, faint, slightly curved streak. Changing the flight direction into frequencies makes every point at one distance share the same curve, so one correction straightens them all. After that, a second sharpening along the flight direction, done with a quick transform, turns each streak into one bright spot.

## The problem

The input is the raw data $s[p][j]$ of $M$ pulses on a straight track at the speed $V$, with the pulse repetition frequency PRF, and $N$ range samples per pulse at the rate $f_s$. Sample $j$ is the slant range $r_{\text{start}} + j\, \Delta r$ with $\Delta r = c/(2 f_s)$. The pulse is a chirp with the FM rate $K_r$, the carrier is $f_0$ with $\lambda = c/f_0$, and the beam has zero squint. A point at the along-track position $x_0$ and the closest range $R_0$ gives $a\, \text{chirp}(\tau - 2R(\eta)/c)\, e^{-i 4\pi f_0 R(\eta)/c}$ with $R(\eta) = \sqrt{R_0^2 + (V\eta - x_0)^2}$. The page uses the Fourier sign $e^{-i 2\pi f t}$ of the DFT; radar books often use $e^{+j\omega t}$ and so write the opposite signs. The output is the complex image on the same $M \times N$ grid, with a peak of each target at the pulse closest to it and at the bin of $R_0$, close to the [SAR image formation](/sar-image-formation/) matched filter value.

## The algorithm

```pseudo id=main
RDA(s, chirp, f_0, V, PRF, r_start, Δr)    ▷ s[p][j]: pulse p, range bin j; returns the image
L1  for every pulse p: s_c[p] ← IDFT(DFT(s[p]) · conj(DFT(chirp)))      ▷ range compression
L2  for every range bin j: S[·][j] ← DFT over p of s_c[·][j]              ▷ to the range-Doppler domain
L3  for every Doppler bin k with |f_k| ≤ f_max: f ← f_k                   ▷ f_k wrapped to [-PRF/2, PRF/2)
L4      D ← sqrt(1 - (λ f / (2V))²)
L5      for every range bin j: R_0 ← r_start + j Δr; u ← (R_0 / D - r_start) / Δr
L6          v ← SINC-INTERP(S[k][·], u)                                  ▷ RCMC
L7          K_a ← 2 V² f_0 D³ / (c R_0); H ← (PRF / sqrt(K_a)) e^{+i 4π f_0 R_0 D / c}
L8          I[k][j] ← v · H                                                ▷ azimuth matched filter
L9  for every range bin j: image[·][j] ← IDFT over k of I[·][j]
```

Line L1 is [pulse compression](/pulse-compression/) by fast convolution. It is circular, so the record must hold the whole chirp of every target. Line L2 moves to the range-Doppler domain. By the principle of stationary phase, Doppler frequency $f$ comes from the slow time at which the target is seen at the squint angle with sine $-\lambda f/(2V)$, so its range there is $R_0 / D(f)$. Lines L4 to L6 read the line of Doppler bin $k$ at that range, which is a range-varying shift; SINC-INTERP is an 8-tap Hann-weighted [sinc interpolation](/sinc-interpolation/). After L6, the energy of every target at $R_0$ is in bin $j$ of $R_0$, whatever its along-track position. The azimuth phase there is $-4\pi f_0 R_0 D(f)/c - 2\pi f x_0/V$ plus a constant, so the factor of L7 cancels the first term, and the inverse DFT of L9 turns the linear phase that is left into a peak at $x_0$. The gain $\text{PRF}/\sqrt{K_a}$ of L7 makes the peak close to the brute-force matched filter value; $K_a$ is the azimuth FM rate at $f$. The Doppler band $f_{\max} = 2 V \sin\theta / \lambda$ of a beam with the half angle $\theta$ limits the loop of L3.

## Example

The tests use $f_0 = 300$ MHz ($\lambda = 1$ m), a chirp of $B = 100$ MHz and 0.2 us sampled at $f_s = 120$ MHz ($\Delta r = 1.25$ m), $V = 100$ m/s and PRF $= 80$ Hz (a pulse every 1.25 m), $M = 128$ pulses, $N = 64$ range bins from 380 m, and a beam with $\sin\theta = 0.125$. A target at $R_0 = 400$ m is in view for 81 pulses, and its migration at the edge of the beam is 3.16 m, about 2.5 bins. The Doppler band is $\pm 25$ Hz.

| target $(x_0, R_0)$, amplitude | matched filter value | RDA peak / matched filter | without RCMC (L5 with $u = j$) |
|---|---|---|---|
| (0 m, 400 m), 1 | 1945 | 0.904 | 0.468 |
| (10 m, 410 m), 0.7 | 1394 | 0.904 | 0.461 |

Both peaks are at the predicted pixels (pulse 64 and bin 16 for the first). The ratio of the two peaks, each divided by its own ideal value, is 0.70, the ratio of the amplitudes. Both outputs carry the same constant phase of about $-38$ degrees, close to the $-45$ degrees of the stationary phase factor $e^{-i\pi/4}$, which L7 does not remove. Along range, the neighbors of the peak at $\pm 1.25$ m are 0.29 and 0.26 of the peak; along the track they are 0.50 of the peak at $\pm 1.25$ m and 0.17 at $\pm 2.5$ m, as expected for the resolutions $c/(2B) = 1.5$ m and $V/(50\ \text{Hz}) = 2$ m. All numbers in this section are measurements on this simulation.

## Correctness

Every step is linear in the data, so the image of a scene is the sum of the images of its points. For one point, the stationary phase approximation of the azimuth DFT gives the range-Doppler signal $W(f)\, p_c(\tau - 2R_0/(c D(f)))\, e^{-i 4\pi f_0 R_0 D(f)/c - i 2\pi f x_0/V}$ times a constant, with the compressed pulse $p_c$. This is the key invariant: the migration curve depends on $R_0$ and $f$ only. With exact interpolation, L5 and L6 put the target in the bin of $R_0$ for every $f$; L7 cancels the phase that depends on $f$ except the linear term; and L9 gives a peak at $x_0$ of about $a$ times the number of pulses in view times the compressed pulse peak, which is the matched filter value. The result is exact only up to the stationary phase approximation, the interpolation and the coupling of range and azimuth, which this basic form ignores. The proofs are in proofs/correctness.md.

## Complexity

Line L1 does $M$ DFTs of length $N$, $O(M N \log N)$. Lines L2 and L9 do $N$ DFTs of length $M$ each, $O(M N \log M)$. Lines L3 to L8 run once per Doppler bin and range bin, with $K$ taps of interpolation and $O(1)$ other work, $O(M N K)$. The total is $O(M N (\log(M N) + K))$ in the real-RAM model with an FFT, and the extra space holds the $M \times N$ range-Doppler array. With $K = 8$ fixed, the cost is $O(M N \log(M N))$.

## Properties

- Linear in the data, and shift-invariant along the track: a target moved by one pulse spacing moves its image by one pixel.
- Range-varying: L5 and L7 depend on the range bin, which is why the correction is done in the range-Doppler domain and not in the 2D frequency domain.
- The only interpolation is along range, in L6; it is the main cost besides the FFTs and the main source of error.
- The image keeps the phase of the targets up to one constant, so it can feed [SAR interferometry](/sar-interferometry/).

## Variants and improvements

- **Secondary range compression (SRC).** In the range-Doppler domain the range chirp has the FM rate $K_m$ of the [range cell migration](/range-cell-migration/) page, not $K_r$. A second range filter for the difference, applied in the 2D frequency domain at one reference range or in the range-Doppler domain, restores the range focus at wide beams and high squint.
- **Squint.** With a nonzero Doppler centroid, the loop of L3 is centered on the centroid, and the centroid must be estimated from the data.
- **Approximate RCMC.** For small migrations, nearest neighbor or shorter interpolators in L6 save time with some loss.
- **Doppler aliasing.** When the PRF is close to the Doppler bandwidth, the frequencies of L3 must be unwrapped around the centroid.
- **Autofocus.** Errors of the motion leave a phase error along the track; [phase gradient autofocus](/phase-gradient-autofocus/) or map drift estimates it after L9.

## When to use it

Use the RDA for stripmap data from a straight, steady track with a narrow beam and low squint, the usual case for satellites. It is simple, fast and easy to adapt to a range-varying Doppler centroid. For wide beams or high squint, the [chirp scaling algorithm](/chirp-scaling-algorithm/) avoids the interpolation and includes SRC, and the [omega-k algorithm](/omega-k-algorithm/) is exact for the straight track. For curved tracks or very wide apertures, use [backprojection](/sar-backprojection/). In the wide-beam test of the omega-k page (sine of the half beam angle 0.35, $R_0 = 96$ m), this basic RDA reaches 0.855 of the ideal peak, against 0.957 for omega-k (measurements).

## Pitfalls

- **Wrong RCMC sign or factor.** L5 must read at $R_0 / D$, a range larger than $R_0$. Reading at $R_0 D$ doubles the migration error instead of removing it.
- **Unwrapped Doppler bins.** DFT bin $k \ge M/2$ is the negative frequency $(k - M)\, \text{PRF}/M$. Using $k\, \text{PRF}/M$ for all bins in L3 gives wrong $D$ and wrong filters for half of the band.
- **Phase sign.** With the echo phase $e^{-i 4\pi f_0 R/c}$, L7 must use $e^{+i 4\pi f_0 R_0 D/c}$. The wrong sign doubles the phase and leaves the target unfocused.
- **Nearest neighbor in L6.** Rounding $u$ to an integer leaves an error of up to half a bin, which lowers the peak and raises the side lobes; use a sinc interpolator with several taps.
- **Targets near the end of the range window.** The fast convolution of L1 is circular, so a chirp that runs past the last sample wraps around. Pad the range record by the length of the chirp, or keep targets inside the window.
- **Wide beams without SRC.** The basic form loses focus as the beam widens, as in the measurement above.

## Implementations

## History

Wu (1976) described a digital system to produce images from SAR data. The steps of this page, range compression, migration correction in the range-Doppler domain and azimuth compression by fast convolution, became the standard processor for spaceborne stripmap data; Cumming and Wong (2005, Chapter 6) describe it with SRC and its variants. Bamler (1992) compared it with the wavenumber domain algorithm and showed which approximations each makes. The chirp scaling algorithm (Raney et al. 1994) later removed its interpolation.

## References
