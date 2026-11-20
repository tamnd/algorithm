---
tag: C270V5
kind: algorithm
slug: chirp-scaling-algorithm
name: Chirp scaling algorithm
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: "Focus SAR data with phase multiplies and FFTs only, using the chirp structure of the pulse to equalize range cell migration without interpolation."
solves: [sar-image-formation]
model: real-ram
complexity:
  vars: {M: the number of pulses, N: the number of range samples per pulse}
  time: {worst: O(M N log(M N))}
  space: {extra: O(M N), data: O(M N)}
properties: {deterministic: true, linear_in_data: true, recursive: false, exact: false}
history:
  year: 1994
  people: [R. Keith Raney, Hartmut Runge, Richard Bamler, Ian G. Cumming, Frank H. Wong]
  note: "Raney, Runge, Bamler, Cumming and Wong published the chirp scaling algorithm in 1994 as a precise SAR processor that needs no interpolation."
prereqs: [range-doppler-algorithm, linear-frequency-modulation-pulse]
see_also: [omega-k-algorithm, range-cell-migration, sar-image-formation, pulse-compression, sar-backprojection, sar-interferometry, fast-fourier-transform, synthetic-aperture-radar]
sources:
  - paper: doi:10.1109/36.298008
    title: "R. Keith Raney, Hartmut Runge, Richard Bamler, Ian G. Cumming and Frank H. Wong, Precision SAR processing using chirp scaling, IEEE Transactions on Geoscience and Remote Sensing 32(4), 1994, 786 to 799"
    locator: "the chirp scaling operation in the range-Doppler domain, the bulk migration correction and range compression in the 2D frequency domain, and the residual phase (general locator)"
  - book: isbn:9781580530583
    title: "Ian G. Cumming and Frank H. Wong, Digital Processing of Synthetic Aperture Radar Data, Artech House, 2005"
    locator: "Chapter 7, The Chirp Scaling Algorithm"
---

The chirp scaling algorithm (CSA) focuses stripmap [synthetic aperture radar](/synthetic-aperture-radar/) data with FFTs and multiplications by phase functions only. Like the [range-Doppler algorithm](/range-doppler-algorithm/), it works in the range-Doppler domain, where the [range cell migration](/range-cell-migration/) of a target depends only on its range. But it does not compress the range first. While the echoes are still [linear FM chirps](/linear-frequency-modulation-pulse/), it multiplies them by a weak chirp in range. That changes the slope of each echo a little and moves its center by an amount that grows with the distance from a reference range. The amount is chosen so that every target ends up with the migration of the reference range. That common migration is a shift, so a linear phase in the range frequency removes it, together with range compression and secondary range compression, without any interpolation.

## In plain words

The echo of each point slides across range bins by an amount that depends on its distance, and correcting different slides at different distances needs interpolation. The chirp scaling trick uses the shape of the radar pulse. The pulse is a chirp, a tone that sweeps in pitch, and multiplying a chirp by another weak chirp moves it in time. A carefully chosen multiply moves the echoes of near and far points so that they all slide by the same amount. One equal slide is easy to undo for every point at once in the frequency domain, by multiplying with a phase. So the whole focus becomes Fourier transforms and multiplies.

## The problem

The input is the raw data $s[p][j]$ of $M$ pulses on a straight track at the speed $V$, at the pulse rate PRF, with $N$ range samples at the rate $f_s$. Sample $j$ has the two-way time $\tau_j$ and the slant range $R_j = r_{\text{start}} + j c/(2 f_s)$. The pulse is a chirp $e^{i\pi K_r t^2}$ of length $T$ and bandwidth $B = K_r T$, the carrier is $f_0$ ($\lambda = c/f_0$), and the squint is zero. A target of amplitude $a$ at $(x_0, R_0)$ gives $a\, \text{chirp}(\tau - 2R(\eta)/c)\, e^{-i 4\pi f_0 R(\eta)/c}$ with $R(\eta) = \sqrt{R_0^2 + (V\eta - x_0)^2}$. The Fourier sign is $e^{-i 2\pi f t}$, as for the DFT; radar books often use $e^{+j\omega t}$ and the opposite signs. A reference range $r_{\text{ref}}$, usually the middle of the swath, is a parameter. The output is the complex image on the $M \times N$ grid, as for [SAR image formation](/sar-image-formation/).

## The algorithm

Write $D(f) = \sqrt{1 - (\lambda f/(2V))^2}$ and let $K_m(f, R)$ be the range FM rate in the range-Doppler domain,

$$K_m = \frac{K_r}{1 - K_r \dfrac{c R f^2}{2 V^2 f_0^3 D^3}}.$$

In the pseudocode, $\tau_j$ is measured from the center of the chirp.

```pseudo id=main
CSA(s, f_0, V, PRF, K_r, r_ref)    ▷ s[p][j]: raw pulse p, range sample j
L1  for every range sample j: S[·][j] ← DFT over p of s[·][j]               ▷ range-Doppler domain
L2  for every Doppler bin k with |f_k| ≤ f_max: D ← D(f_k); a ← 1/D - 1; K_m ← K_m(f_k, r_ref)
L3      S[k][j] ← S[k][j] · e^{iπ K_m a (τ_j - 2 r_ref / (c D))²} for every j      ▷ chirp scaling
L4      Z ← DFT over j of S[k][·]                                            ▷ 2D frequency domain
L5      Z[q] ← Z[q] · (f_s / sqrt(K_r)) e^{iπ D f_q² / K_m} e^{i 2π f_q · 2 r_ref a / c} for every q
L6      S[k][·] ← IDFT(Z)                                                    ▷ back to range-Doppler
L7      S[k][j] ← S[k][j] · (PRF / sqrt(K_a)) e^{i 4π f_0 R_j D / c} e^{-i Δφ_j} for every j
L8  for every range sample j: image[·][j] ← IDFT over k of S[·][j]
```

Line L1 takes the data to the range-Doppler domain without range compression. There a target at $R_0$ is a range chirp of the rate $K_m$, centered at $2R_0/(cD)$. Line L3 is the chirp scaling multiply. Completing the square in the exponent shows that the product is a chirp of the rate $K_m/D$ centered at $2R_0/c + 2 r_{\text{ref}}\, a/c$: the migration of every target is now that of the reference range, a shift that does not depend on $R_0$. Line L5 does three things at once in the range frequency $f_q$: range compression for the new rate $K_m/D$, which includes secondary range compression because $K_m$ is used and not $K_r$; the bulk migration correction, the linear phase that undoes the common shift; and a gain. Line L7 is the azimuth matched filter at the range $R_j$, with the gain set by $K_a = 2 V^2 f_0 D^3/(c\, r_{\text{ref}})$, and the removal of the residual phase $\Delta\varphi_j = 4\pi K_m (1 - D)(R_j - r_{\text{ref}})^2 / (c^2 D^2)$ that the scaling leaves behind. Line L8 returns to the image.

## Example

The tests use the geometry of the range-Doppler algorithm: $f_0 = 300$ MHz, $B = 100$ MHz, $T = 0.2$ us, $f_s = 120$ MHz (bins of 1.25 m), $V = 100$ m/s, PRF $= 80$ Hz, $M = 128$, $N = 64$ from 380 m, a beam with the sine of the half angle 0.125, and $r_{\text{ref}}$ in the middle of the window. The measured peaks, divided by the brute-force matched filter value of each target, are:

| target $(x_0, R_0)$, amplitude | peak / matched filter | phase of peak / amplitude |
|---|---|---|
| (0 m, 400 m), 1 | 0.998 | $-0.3$ degrees |
| (10 m, 410 m), 0.7 | 0.986 | $-0.2$ degrees |
| (-12.5 m, 395 m), 0.5 | 1.017 | $-0.3$ degrees |

Each peak is at its predicted pixel. The phase is close to zero because the phase-only range filter of L5 leaves a factor $e^{+i\pi/4}$ that cancels the $e^{-i\pi/4}$ of the azimuth stationary phase.

A wide beam shows what the scaling does. With the sine of the half angle 0.35, PRF $= 200$ Hz, $M = 256$, a window from 80 m and $r_{\text{ref}} = 120$ m, a target at $R_0 = 96$ m migrates 6.48 m at the edge of the beam, against 8.10 m at the reference range. The full CSA gives 1.048 of the ideal peak at the right pixel. With L3 skipped (and $\Delta\varphi = 0$), only the bulk migration of 120 m is removed; the peak drops to 0.734 and moves by one range bin. The values in this section are measurements on these simulations.

## Correctness

The algorithm is linear in the data. Its key step is an exact identity: for any $R_0$, the product of a chirp of rate $K_m$ centered at $\tau_d = 2R_0/(cD)$ with the scaling chirp $e^{i\pi K_m a (\tau - \tau_{\text{ref}})^2}$ is a chirp of rate $K_m(1 + a) = K_m/D$ centered at $\tau_{\text{ref}} + D(\tau_d - \tau_{\text{ref}}) = 2R_0/c + 2 r_{\text{ref}}\, a/c$, times the constant phase $e^{i\Delta\varphi}$. So after L3 the migration is the same for every range, and L5 removes it exactly. The approximations are those of the range-Doppler signal model: the stationary phase in azimuth, and $K_m$ evaluated at $r_{\text{ref}}$ instead of at each $R_0$. The proofs are in proofs/correctness.md.

## Complexity

Lines L1 and L8 do $N$ DFTs of length $M$, and lines L4 and L6 do $M$ DFTs of length $N$, so the FFTs cost $O(M N \log(M N))$. Lines L2, L3, L5 and L7 cost $O(1)$ per sample. The total is $O(M N \log(M N))$ in the real-RAM model, and the extra space is the $M \times N$ array. There is no interpolation, so no factor $K$ as in the RDA.

## Properties

- Linear in the data; only FFTs and multiplications by phase functions that can be computed in advance.
- No interpolation, so no interpolation error and no extra cost per sample.
- Secondary range compression is built in through $K_m$.
- Phase preserving after the residual phase of L7 is removed, which matters for [SAR interferometry](/sar-interferometry/).
- The accuracy falls as $K_m$ varies across the swath, because L2 uses $r_{\text{ref}}$ for every range.

## Variants and improvements

- **Extended chirp scaling.** For squinted and spotlight data, an extra scaling in azimuth and a range-varying Doppler centroid.
- **Nonlinear chirp scaling.** A cubic term in the scaling function for wide swaths and high squint, where the migration is not well matched by a quadratic phase.
- **Range blocks.** Split a wide swath into blocks with their own $r_{\text{ref}}$ to keep $K_m$ accurate.
- **Dechirped data.** When the receiver removes the chirp in hardware, the scaling cannot act on a chirp; the [omega-k algorithm](/omega-k-algorithm/) or [polar format algorithm](/polar-format-algorithm/) are used instead.

## When to use it

Use the CSA for stripmap data from a straight track when the RDA interpolation is too costly or too inexact, and when phase must be preserved. It is a common choice for spaceborne processors with moderate squint. For very wide apertures or long synthetic apertures in which $K_m$ varies strongly, the [omega-k algorithm](/omega-k-algorithm/) is more exact. For curved tracks, use [backprojection](/sar-backprojection/).

## Pitfalls

- **Range compression first.** L3 must act on the uncompressed chirps. If the data are range compressed before L1, there is no chirp to scale, and L3 only adds a phase.
- **Reference time.** In L3 the time $\tau_j$ is measured from the center of the chirp. If the chirp is stored from its start, as in the code, add $T/2$ to the reference time in L3 and to the shift in L5, or every target moves by half a pulse.
- **Forgetting the residual phase.** Without $e^{-i\Delta\varphi_j}$ in L7 the modulus is fine, but the phase of a target varies with $(R_0 - r_{\text{ref}})^2$, which ruins interferometry.
- **The window.** The scaling moves echoes by up to $2 |R_0 - r_{\text{ref}}|\, a / c$ in time, so the range record must have room for the moved chirps; otherwise the circular FFT of L4 wraps them.
- **Wrong rate in L5.** Using $K_r$ in place of $K_m/D$ leaves range defocus at large Doppler frequencies.

## Implementations

## History

Raney, Runge, Bamler, Cumming and Wong (1994) published the chirp scaling algorithm. Their insight was that the range chirp of the transmitted pulse can be used to equalize the migration before range compression, so the range-varying interpolation of the range-Doppler algorithm is replaced by phase multiplies. Cumming and Wong (2005, Chapter 7) give a full derivation and its relation to the range-Doppler and omega-k algorithms.

## References
