---
tag: 91YVZD
kind: algorithm
slug: total-focusing-method
name: Total focusing method
aliases:
- TFM
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: "Form an ultrasonic image from full matrix capture data: at every pixel, sum the trace of every transmit and receive pair at its two-way time. Focused everywhere, at a cost of O(M^2 n^2)."
solves: [beamforming]
model: real-ram
complexity:
  vars: {M: the number of array elements, n: the number of pixels along one side of the image, T: the number of samples per trace}
  time: {worst: O(M^2 n^2)}
  space: {extra: O(M), data: O(M^2 T)}
properties: {deterministic: true, linear_in_data: true, recursive: false, exact: false}
history:
  year: 2005
  people: [Caroline Holmes, Bruce W. Drinkwater, Paul D. Wilcox]
  note: "Holmes, Drinkwater and Wilcox named the total focusing method in 2005 as a post-processing of the full matrix of transmit and receive signals for nondestructive evaluation; the same sum is synthetic transmit aperture imaging in medical ultrasound."
prereqs: [synthetic-transmit-aperture]
see_also: [delay-and-sum-beamforming, saft, plane-wave-compounding, pulse-echo-imaging, dynamic-receive-focusing, coherence-factor, kirchhoff-migration, sar-backprojection]
sources:
  - paper: doi:10.1016/j.ndteint.2005.04.002
    title: "Caroline Holmes, Bruce W. Drinkwater and Paul D. Wilcox, Post-processing of the full matrix of ultrasonic transmit-receive array data for non-destructive evaluation, NDT and E International 38(8), 2005, 701 to 711"
    locator: "the full matrix capture, the total focusing method and its comparison with conventional array imaging (general locator)"
  - paper: doi:10.1016/j.ndteint.2006.03.006
    title: "Bruce W. Drinkwater and Paul D. Wilcox, Ultrasonic arrays for non-destructive evaluation: A review, NDT and E International 39(7), 2006, 525 to 541"
    locator: "the section on array data acquisition and post-processing, including full matrix capture and TFM (general locator)"
  - paper: doi:10.1016/j.ultras.2006.07.017
    title: "Jorgen Arendt Jensen, Svetoslav Ivanov Nikolov, Kim Lokke Gammelmark and Morten Hogholm Pedersen, Synthetic aperture ultrasound imaging, Ultrasonics 44 (supplement), 2006, e5 to e15"
    locator: "synthetic transmit aperture imaging with one element per emission, the same sum in medical ultrasound (general locator)"
---

The total focusing method (TFM) forms an image from full matrix capture (FMC) data. In FMC, each of the $M$ elements of an array fires in turn and all $M$ elements record, so the data holds one trace for every transmit and receive pair. TFM computes, for every pixel, the two-way travel time of each pair through that pixel, reads each trace at its time and adds the $M^2$ values. The image is focused on transmit and on receive at every pixel, which a physical array with one transmit focus cannot do. TFM is [delay-and-sum beamforming](/delay-and-sum-beamforming/) applied to the full matrix, and it is the image formation step of [synthetic transmit aperture](/synthetic-transmit-aperture/) imaging; the name TFM comes from nondestructive testing. The cost is $O(M^2 n^2)$ for an $n \times n$ image.

## In plain words

Imagine a row of 16 loudspeakers that are also microphones. Each one clicks once while all 16 listen, so you get 256 recordings. To decide how bright one point of the image is, work out for every pair how long a click takes to go from the first one to the point and back to the second one. Read each recording at that moment and add the 256 readings. If something reflects at that point, all readings line up and the sum is large. If nothing is there, the readings come from different places and mostly cancel. Do this for every point of the picture.

## The problem

The input is FMC data $D_{ij}$, $i, j = 1, \ldots, M$: the trace recorded by element $j$ when element $i$ fires, as complex baseband (IQ) samples at $t_k = t_0 + k/f_s$. The analytic radio frequency (RF) signal is $r_{ij}(t) = b_{ij}(t) e^{i 2\pi f_0 t}$, where $b_{ij}$ is the baseband signal and $f_0$ the center frequency (see [analytic signal](/analytic-signal/)). The array lies on $z = 0$ with element $i$ at $e_i = (x_i, 0)$, and the medium has a constant speed of sound $c$. The output is an image $I(p)$ on a grid of $n \times n$ pixels $p = (x, z)$, $z > 0$, that is large where a scatterer is. The [pulse-echo model](/pulse-echo-imaging/) gives the data of a point scatterer at $p_0$: an echo in trace $(i, j)$ at the time $(|p_0 - e_i| + |p_0 - e_j|)/c$.

## The algorithm

```pseudo id=main
TFM(D, e_1 … e_M, pixels, c, f_s, t_0, f_0)    ▷ returns the image I
L1  for each pixel p do
L2      d_i ← |p - e_i| / c for i = 1 … M      ▷ one-way times
L3      acc ← 0
L4      for i ← 1 to M do                      ▷ transmit element
L5          for j ← 1 to M do                  ▷ receive element
L6              acc ← acc + SAMPLE(D_ij, d_i + d_j)
L7      I(p) ← |acc|
L8  return I

SAMPLE(b, t)                                   ▷ analytic RF value of an IQ trace at time t
L9  u ← (t - t_0) f_s;  k ← ⌊u⌋;  φ ← u - k
L10 if k < 0 or k + 1 ≥ T then return 0
L11 return ((1 - φ) b[k] + φ b[k+1]) · e^{i 2π f_0 t}
```

Line L2 computes the travel time from each element to the pixel once, and the pair $(i, j)$ then uses $d_i + d_j$: out from $e_i$, back to $e_j$. SAMPLE interpolates the baseband trace linearly and restores the carrier phase at the exact time $t$. The sum in L6 is coherent: it adds complex values, so echoes that arrive in phase add up and the others cancel. Line L7 takes the modulus, which is the envelope of the focused signal; a B-mode display then applies [log compression](/b-mode-image-formation/).

## Example

The tests use $M = 16$ elements with pitch 0.3 mm, centered at $x = 0$, so the outer elements are at $x = \pm 2.25$ mm. The speed of sound is $c = 1.54$ mm/us (1540 m/s), $f_0 = 5$ MHz (wavelength 0.308 mm), $f_s = 40$ MHz, and the pulse has a Gaussian envelope with $\sigma_t = 0.1$ us. One point scatterer of amplitude 1 sits at $(0, 6)$ mm.

For the pixel $p = (0, 6)$, line L2 gives $d_1 = \sqrt{6^2 + 2.25^2}/1.54 = 4.1610$ us for the outer element and $d_8 = \sqrt{6^2 + 0.15^2}/1.54 = 3.8973$ us for an inner one. The pair $(1, 1)$ is read at $8.3221$ us and the pair $(1, 8)$ at $8.0584$ us. These are exactly the times of the simulated echoes, so all 256 terms are close to $1$, and the pixel value is $254.67$. Theorem 2 of the proof gives $M^2 = 256$ for exact samples; the small loss comes from the linear interpolation.

The lateral profile at $z = 6$ mm, normalized to its peak, at $x = -0.3, -0.2, \ldots, 0.3$ mm:

| x (mm) | -0.3 | -0.2 | -0.1 | 0 | 0.1 | 0.2 | 0.3 |
|---|---|---|---|---|---|---|---|
| TFM | 0.179 | 0.426 | 0.802 | 1 | 0.802 | 0.426 | 0.179 |
| one transmit (element 8), dynamic receive | 0.313 | 0.624 | 0.893 | 1 | 0.893 | 0.625 | 0.315 |

The single transmit row focuses on receive only, as a [dynamic receive](/dynamic-receive-focusing/) beamformer does after an unfocused transmit. TFM adds the transmit focus and the peak is narrower. With two scatterers at $x = \pm 0.4$ mm, the TFM profile drops to $0.176$ of the peak at $x = 0$, so the two points are clearly resolved. These numbers are measurements on this simulation, not properties of TFM in general.

## Correctness

TFM is a linear map of the data followed by a modulus, and the code checks the linear part against its exact adjoint. For a point scatterer and exact samples, every term at the scatterer equals the amplitude times $g(0)$, so the pixel value is $M^2 |a|\, g(0)$. By the triangle inequality no pixel is larger, and with at least two elements the maximum is only at the scatterer, because two distinct elements at equal distances from two points in $z > 0$ force the points to be equal. If the data is reciprocal, $D_{ij} = D_{ji}$, the half matrix gives the same image. The proofs are in proofs/correctness.md.

These are theorems about the model: point scatterers, single scattering, a known constant $c$, no attenuation, spreading or directivity. In a real specimen, an error in $c$ moves and blurs the focus, and multiple scattering adds echoes that TFM puts in the wrong place.

## Complexity

In the real-RAM model, lines L4 to L6 run $M^2$ times per pixel, and SAMPLE costs $O(1)$. An $n \times n$ image therefore costs $\Theta(M^2 n^2)$ operations, plus $O(M n^2)$ square roots in L2. The extra space is $O(M)$ for the times, besides the data of size $M^2 T$ and the image of size $n^2$. With $M = 64$ and a $256 \times 256$ grid this is about $2.7 \times 10^8$ samples per frame. Reciprocity halves the reads (Theorem 3 of the proof).

The data acquisition costs $M$ firings, one per element, and each firing needs the full round trip to the deepest point. This limits the frame rate, not the computation.

## Properties

- Linear in the data before the modulus of L7, with an exact adjoint (the code checks the adjoint test to $10^{-10}$).
- Focused on transmit and receive at every pixel. The focus does not depend on a transmit focal depth chosen before the scan.
- Gain $M^2$ for a point scatterer under exact sampling, against $M$ for receive-only focusing of one transmit.
- Uses all of the data. The data needs $M^2 T$ samples, which is $M$ times more than one focused line set.
- Each firing uses one element, so the transmitted energy and the signal-to-noise ratio per firing are low.

## Variants and improvements

- **Half matrix.** For reciprocal data, use the pairs $i \le j$ and count the pairs $i < j$ twice. This halves the reads and the storage.
- **Apodization and aperture.** Weight each pair, or skip pairs outside a receive f-number, to trade the side lobes against the main lobe width, as in [dynamic receive focusing](/dynamic-receive-focusing/).
- **Coherence weighting.** Multiply each pixel by the [coherence factor](/coherence-factor/) of its $M^2$ terms to suppress clutter.
- **Other transmissions.** [Plane-wave compounding](/plane-wave-compounding/) fires all elements with tilts and needs fewer firings; [SAFT](/saft/) uses only the diagonal $i = j$.
- **Layered media.** In nondestructive testing through a wedge or an immersion layer, the times $d_i$ follow refracted ray paths by Fermat's principle in place of straight lines.
- **Frequency domain.** Wavenumber (migration) methods compute the same focusing faster on regular grids; [Kirchhoff migration](/kirchhoff-migration/) is the seismic analogue of the time-domain sum.

## When to use it

Use TFM when the array is small enough that $M$ firings are fast, and when focus everywhere matters more than frame rate: defect sizing in welds and castings is the main case. For large arrays in medical imaging, where the frame rate and the signal-to-noise ratio of single-element firings are a problem, plane-wave compounding or focused transmits are more common.

## Pitfalls

- **Wrong speed of sound.** The times scale with $1/c$. A wrong $c$ moves the image and smears the focus, worst at large angles.
- **Element directivity.** Real elements radiate weakly at large angles. Pairs that see the pixel at a steep angle add noise and little signal; an aperture limit helps.
- **Interpolation.** Linear interpolation of RF data at a few samples per period loses gain. Interpolate the baseband signal and restore the phase, as in L11, or sample faster.
- **The recorded window.** A two-way time outside the window must give $0$ (L10), not an index error or a wrapped sample.
- **Dead zone.** The firing itself saturates the receivers for a short time, so the shallowest pixels are not reliable.

## Implementations

## History

Synthetic aperture methods with one transmitting element at a time come from radar and from the synthetic aperture focusing technique of ultrasonic testing. In medical ultrasound the same sum over all transmit and receive pairs is synthetic transmit aperture imaging (Jensen, Nikolov, Gammelmark and Pedersen 2006 give an overview). Holmes, Drinkwater and Wilcox (2005) named the acquisition full matrix capture and the image formation the total focusing method, and showed better images than conventional array imaging on test specimens. Drinkwater and Wilcox (2006) placed TFM in their review of ultrasonic arrays for nondestructive evaluation. TFM is now a standard mode of phased array flaw detectors.

## References
