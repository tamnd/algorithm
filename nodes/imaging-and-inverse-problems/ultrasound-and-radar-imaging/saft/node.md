---
tag: 4W5EDR
kind: algorithm
slug: saft
name: Synthetic aperture focusing technique
aliases:
- SAFT
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: Focus a single moving transducer after the scan by summing its recorded echoes along the hyperbolic delay curve of each image point. A K-position scan costs O(K n^2) for n x n pixels.
solves: [beamforming]
model: real-ram
complexity:
  vars: {K: the number of scan positions, n: the number of pixels along one side of the image, T: the number of samples per trace}
  time: {worst: O(K n^2)}
  space: {extra: O(1), data: O(K T)}
properties: {deterministic: true, linear_in_data: true, recursive: false, exact: false}
history:
  year: 1986
  people: [Steven R. Doctor, Thomas E. Hall, Larry D. Reid]
  note: "SAFT carries the idea of synthetic aperture radar to ultrasonic testing; Doctor, Hall and Reid described its development into a signal processing technology for inspection in 1986."
prereqs: [pulse-echo-imaging, delay-and-sum-beamforming]
see_also: [total-focusing-method, synthetic-transmit-aperture, synthetic-aperture-radar, sar-backprojection, kirchhoff-migration, b-mode-image-formation, dynamic-receive-focusing, coherence-factor]
sources:
  - paper: doi:10.1016/0308-9126(86)90105-7
    title: "Steven R. Doctor, Thomas E. Hall and Larry D. Reid, SAFT, the evolution of a signal processing technology for ultrasonic testing, NDT International 19(3), 1986, 163 to 167"
    locator: "the principle of SAFT (summing along the hyperbola of each point) and its development for inspection (general locator)"
  - paper: doi:10.1016/j.ndteint.2006.03.006
    title: "Bruce W. Drinkwater and Paul D. Wilcox, Ultrasonic arrays for non-destructive evaluation: A review, NDT and E International 39(7), 2006, 525 to 541"
    locator: "the part on synthetic aperture processing of array data, of which SAFT is the monostatic case (general locator)"
  - paper: doi:10.1016/j.ultras.2006.07.017
    title: "Jorgen Arendt Jensen, Svetoslav Ivanov Nikolov, Kim Lokke Gammelmark and Morten Hogholm Pedersen, Synthetic aperture ultrasound imaging, Ultrasonics 44 (supplement), 2006, e5 to e15"
    locator: "the overview of synthetic aperture methods in medical ultrasound, including the monostatic case (general locator)"
---

The synthetic aperture focusing technique (SAFT) makes a focused image from the traces of one transducer that is moved along a line. At each position the transducer sends a pulse and records the echoes at the same place. A point scatterer then appears in the raw scan (the B-scan) along a hyperbola, because its two-way time $2\sqrt{(x_k - x_0)^2 + z_0^2}/c$ grows as the transducer moves away. SAFT sums, for each pixel, the traces along the hyperbola of that pixel. The echoes of a scatterer at the pixel add in phase, so the scan acts like one large focused aperture: the synthetic aperture. SAFT is the monostatic case, transmitter equal to receiver, of the [total focusing method](/total-focusing-method/), which uses every pair of an array. It is the ultrasonic version of [synthetic aperture radar](/synthetic-aperture-radar/) focusing by [back-projection](/sar-backprojection/).

## In plain words

A small transducer has a wide beam, so it hears a small reflector from many places along its path. In the raw scan the reflector looks like a long arc, not a point. If you know where the reflector would be, you know exactly when each recording should contain its echo. Add up all recordings at those moments. At the right place the echoes line up and give a strong value. At a wrong place they do not line up and cancel. Doing this for every point turns each arc back into a small spot.

## The problem

The input is $K$ traces $b_1, \ldots, b_K$ recorded at the positions $q_k = (x_k, 0)$, as complex baseband (IQ) samples at $t_0 + m/f_s$, with the analytic RF signal $r_k(t) = b_k(t) e^{i 2\pi f_0 t}$. The medium has a constant speed of sound $c$. The output is an image $I(p)$ on an $n \times n$ grid of pixels $p = (x, z)$, large where a scatterer is. An optional half angle $\theta$ models the beam of the transducer: position $k$ can see the pixel only if $|x - x_k| \le z \tan\theta$.

## The algorithm

```pseudo id=main
SAFT(r_1 … r_K, q_1 … q_K, pixels, c, θ)    ▷ returns the image I
L1  for each pixel p = (x, z) do
L2      acc ← 0
L3      for k ← 1 to K do
L4          if θ is given and |x - x_k| > z tan θ then skip k
L5          t ← 2 |p - q_k| / c                 ▷ the hyperbola of p
L6          acc ← acc + SAMPLE(r_k, t)
L7      I(p) ← |acc|

SAMPLE(b, t)                                  ▷ analytic RF value of an IQ trace
L8  u ← (t - t_0) f_s;  m ← ⌊u⌋;  φ ← u - m
L9  if m < 0 or m + 1 ≥ T then return 0
L10 return ((1 - φ) b[m] + φ b[m+1]) · e^{i 2π f_0 t}
```

Line L5 is the only geometry: the round trip from the position to the pixel and back on the same path. Line L4 drops positions that cannot see the pixel, which keeps noise from those traces out of the sum and makes the synthetic aperture grow with depth. SAMPLE interpolates the baseband trace and restores the carrier phase, as in TFM.

## Example

The tests scan $K = 21$ positions with a step of 0.15 mm, from $x = -1.5$ to $1.5$ mm. The speed of sound is $c = 1.54$ mm/us, $f_0 = 5$ MHz (wavelength 0.308 mm), $f_s = 40$ MHz, and the Gaussian pulse envelope has $\sigma_t = 0.1$ us. One scatterer of amplitude 1 is at $(0, 6)$ mm.

The echo arrives at $2 \cdot 6/1.54 = 7.7922$ us at the center position and at $2\sqrt{6^2 + 1.5^2}/1.54 = 8.0321$ us at the end positions. The difference, $0.24$ us, is $1.2$ periods of the carrier, so the plain sum of the traces at a fixed time would cancel. Along the hyperbola of $(0, 6)$, all 21 terms are close to $1$, and the pixel value is $20.886$ against $K = 21$ for exact samples.

The width of the peak shrinks as the synthetic aperture grows. At $z = 6$ mm, on 15 pixels from $x = -0.7$ to $0.7$ mm with a step of 0.1 mm, the number of pixels at or above half of the peak is:

| positions K | 5 | 11 | 21 | 41 |
|---|---|---|---|---|
| aperture length (mm) | 0.6 | 1.5 | 3.0 | 6.0 |
| pixels at or above half the peak | 13 | 7 | 3 | 1 |

The unfocused B-scan, the envelope of each trace at the depth of the pixel without the hyperbola, is above half its peak at all 15 pixels. With a half angle of $\arctan(0.8/6) = 7.6$ degrees, only the 11 positions with $|x_k| \le 0.8$ mm enter the sum at the scatterer, and its value is close to 11. These widths are measurements on this simulation.

## Correctness

Before the modulus, SAFT is linear in the traces, and the code checks it against its exact adjoint. For a point scatterer and exact samples, every term at the scatterer equals the amplitude times $g(0)$, so the peak is $|a|\, g(0)$ times the number of positions in the sum. No pixel is larger, and with two positions at different $x$ the maximum is only at the scatterer. In the far field, a step $d$ between positions acts like an array with spacing $2d$, because the path is two-way; a step of at most a quarter wavelength gives no grating lobe at any angle. The proofs are in proofs/correctness.md. These results hold for the model: point scatterers, single scattering, a known constant $c$ and a straight scan line.

## Complexity

In the real-RAM model, lines L3 to L6 run at most $K$ times per pixel at $O(1)$ each, so an $n \times n$ image costs $O(K n^2)$. With a half angle, the number of positions per pixel is about $2 z \tan\theta / d$ for a step $d$, which grows with depth. The extra space is $O(1)$ per pixel, besides the $K T$ samples of data. Frequency-domain versions of SAFT (wavenumber migration) cost $O(K T \log(K T))$ on a regular grid with an FFT.

## Properties

- Linear in the data before the modulus, with an exact adjoint.
- Gain $K$ for a point scatterer against $1$ for one trace, when all $K$ positions see it.
- Lateral resolution set by the synthetic aperture, not by the transducer. A rule of thumb from the far-field approximation, as for strip-map synthetic aperture radar: the beam of a transducer of width $D$ spreads over an angle of about $\lambda/D$, so the synthetic aperture at depth $z$ is about $z\lambda/D$ long, and the two-way resolution $\lambda z / (2 \cdot z\lambda/D) = D/2$ does not depend on depth. This is a heuristic estimate, not a theorem of this page.
- Only one element fires and receives at a time, so the hardware is simple and the signal-to-noise ratio per trace is low.

## Variants and improvements

- **Frequency domain SAFT.** For a straight scan and constant $c$, the hyperbola sums become a remapping in the 2D Fourier domain of the B-scan, as in [Stolt migration](/stolt-migration/) of seismic data, at a cost of FFTs.
- **Arrays.** With an array, [TFM](/total-focusing-method/) uses all transmit and receive pairs; SAFT uses only the diagonal, so it needs one channel.
- **Virtual sources.** In medical ultrasound, the focal point of a focused transmit can be treated as a virtual source, and the same summation extends the focus beyond the focal zone.
- **Weights.** Apodization over the positions, or a [coherence factor](/coherence-factor/) per pixel, lowers side lobes.
- **Curved surfaces and layers.** The times in L5 can follow refracted paths through a coupling layer.

## When to use it

Use SAFT when only one transducer is available, or when a mechanical scan is cheaper than an array, and the target does not move during the scan. It is used in ultrasonic testing of thick parts and in other one-channel pulse-echo systems. If an array is available, TFM or [plane-wave compounding](/plane-wave-compounding/) uses more of its data.

## Pitfalls

- **Motion and position errors.** An error of a quarter wavelength in the position or a motion of the target changes the phase of the terms by about $\pi$ and destroys the focus.
- **Step too large.** The two-way path doubles the phase step, so the step must be smaller than for a receive-only array; see Theorem 3 of the proof.
- **No half angle.** Positions outside the beam add only noise. Without L4 the noise level of deep pixels grows.
- **Wrong speed of sound.** It moves and blurs the focus, worse for long synthetic apertures.
- **RF interpolation.** Linear interpolation of RF samples at a few samples per period lowers the gain; interpolate IQ data as in L10.

## Implementations

## History

Synthetic aperture radar showed that a moving antenna with a wide beam, together with coherent processing, can give a resolution much finer than its real aperture. SAFT applies the same idea to pulse-echo ultrasound. Doctor, Hall and Reid (1986) described how SAFT grew into a signal processing technology for ultrasonic testing. With digital arrays, the same summation over transmit and receive pairs became synthetic transmit aperture imaging in medicine and the total focusing method in nondestructive testing.

## References
