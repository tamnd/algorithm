---
tag: HTFN8H
kind: algorithm
slug: plane-wave-compounding
name: Coherent plane-wave compounding
aliases:
- plane-wave compounding
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: "Transmit unfocused plane waves at a few tilt angles, beamform each one at every pixel, and add the complex images. N angles give a synthetic transmit focus at a high frame rate, for O(N M n^2) work."
solves: [beamforming]
model: real-ram
complexity:
  vars: {N: the number of plane-wave angles, M: the number of array elements, n: the number of pixels along one side of the image}
  time: {worst: O(N M n^2)}
  space: {extra: O(M)}
properties: {deterministic: true, linear_in_data: true, recursive: false, exact: false}
history:
  year: 2009
  people: [Gabriel Montaldo, Mickael Tanter, Jeremy Bercoff, Nicolas Benech, Mathias Fink]
  note: "Montaldo, Tanter, Bercoff, Benech and Fink (2009) showed that the coherent sum of a few tilted plane-wave images reaches the quality of focused imaging at frame rates of thousands of images per second, for ultrafast imaging and transient elastography."
prereqs: [dynamic-receive-focusing, synthetic-transmit-aperture]
see_also: [delay-and-sum-beamforming, total-focusing-method, b-mode-image-formation, coherence-factor, svd-clutter-filter, kasai-autocorrelation-estimator, pulse-echo-imaging, speckle]
sources:
  - paper: doi:10.1109/TUFFC.2009.1067
    title: "Gabriel Montaldo, Mickael Tanter, Jeremy Bercoff, Nicolas Benech and Mathias Fink, Coherent plane-wave compounding for very high frame rate ultrasonography and transient elastography, IEEE Transactions on Ultrasonics, Ferroelectrics, and Frequency Control 56(3), 2009, 489 to 506"
    locator: "the beamforming of tilted plane waves, the coherent sum over angles, the choice of the number of angles, and the comparison with focused imaging (general locator)"
  - paper: doi:10.1016/j.ultras.2006.07.017
    title: "Jorgen Arendt Jensen, Svetoslav Ivanov Nikolov, Kim Lokke Gammelmark and Morten Hogholm Pedersen, Synthetic aperture ultrasound imaging, Ultrasonics 44 (supplement), 2006, e5 to e15"
    locator: "synthetic aperture imaging and its relation to the transmit focus (general locator)"
  - book: isbn:9780123964878
    title: "Thomas L. Szabo, Diagnostic Ultrasound Imaging: Inside Out, 2nd edition, Academic Press, 2014"
    locator: "Chapter 7, Array beamforming (transmit and receive focusing of arrays)"
---

Coherent plane-wave compounding forms an ultrasound image from a few unfocused transmissions. All elements of the array fire together, with small delays that tilt the wavefront by an angle $\alpha$, so a plane wave crosses the whole field at once. Every pixel is then beamformed on receive with the exact two-way time: the plane wave reaches $(x, z)$ at $(z \cos\alpha + x \sin\alpha)/c$, and the echo goes back to element $j$ in $\sqrt{z^2 + (x - x_j)^2}/c$. One plane wave gives a full image that is focused on receive only. The complex images of $N$ angles are added before the envelope, which builds a transmit focus after the fact, as [synthetic transmit aperture](/synthetic-transmit-aperture/) does with single elements. Since each firing covers the whole field, a frame needs $N$ firings, often 5 to 40, against one firing per line for focused imaging. The receive step is [delay-and-sum beamforming](/delay-and-sum-beamforming/) with [dynamic receive focusing](/dynamic-receive-focusing/).

## In plain words

Instead of sending a narrow beam down one line at a time, the whole array sends one flat wave that lights up the entire picture at once. Listening to the echoes, you can already work out an image, but it is blurry, because the light was not focused. Now send the flat wave a few more times, each time a little tilted. Each tilt gives another blurry image, and the blur is different each time. Add the images while they are still waves, before taking the brightness, and the parts that agree add up while the blur cancels. A few flat waves give an image almost as sharp as the slow, focused one.

## The problem

The input is, for each angle $\alpha_a$, $a = 1, \ldots, N$, the $M$ traces of the array as complex baseband (IQ) samples at $t_0 + k/f_s$, with the analytic RF signal $r_{aj}(t) = b_{aj}(t) e^{i 2\pi f_0 t}$. The array lies on $z = 0$ with element $j$ at $(x_j, 0)$, and the medium has the speed of sound $c$. The time origin of angle $a$ is the moment when its wavefront passes $(0, 0)$. The output is an image on an $n \times n$ grid, as large as possible where a scatterer is. An optional receive f-number $F$ limits element $j$ to the pixels with $|x - x_j| \le z/(2F)$.

## The algorithm

```pseudo id=main
COMPOUND(r, α_1 … α_N, x_1 … x_M, pixels, c, F)     ▷ returns the image I
L1  for each pixel p = (x, z) do
L2      ρ_j ← √(z² + (x - x_j)²) / c for j = 1 … M     ▷ receive times
L3      acc ← 0
L4      for a ← 1 to N do
L5          τ ← (z cos α_a + x sin α_a) / c            ▷ transmit time of the tilted wave
L6          for j ← 1 to M do
L7              if F is not given or |x - x_j| ≤ z/(2F) then
L8                  acc ← acc + SAMPLE(r_aj, τ + ρ_j)
L9      I(p) ← |acc|
```

SAMPLE is the same as on the [TFM](/total-focusing-method/) page: linear interpolation of the baseband trace and the carrier phase at the exact time. Line L5 is the only new part. The receive times of L2 do not depend on the angle, so they are computed once per pixel. Line L9 takes the modulus after the sum over all angles; this is what makes the compounding coherent.

## Example

The tests use $M = 16$ elements with pitch 0.3 mm, $c = 1.54$ mm/us, $f_0 = 5$ MHz, $f_s = 40$ MHz and a Gaussian pulse envelope with $\sigma_t = 0.1$ us. One scatterer of amplitude 1 is at $(0, 6)$ mm.

For a wave tilted by $\alpha = 10$ degrees and the pixel $(0.3, 6)$ mm, line L5 gives $\tau = (6 \cos 10° + 0.3 \sin 10°)/1.54 = 3.8707$ us, and for the outer element at $x_j = -2.25$ mm, L2 gives $\sqrt{36 + 2.55^2}/1.54 = 4.2334$ us. With a scatterer at that pixel, the peak of the image of this single tilted wave is at $(0.3, 6)$, as the test checks for $\pm 10$ degrees. A sign error in L5 moves the peak.

Lateral profiles at $z = 6$ mm, normalized to the peak, with the largest side lobe at $|x| \ge 0.6$ mm:

| angles | peak (N M) | x = -0.3 | -0.2 | -0.1 | 0 | 0.1 | 0.2 | 0.3 | side lobe |
|---|---|---|---|---|---|---|---|---|---|
| 1 (0°) | 15.92 (16) | 0.315 | 0.625 | 0.893 | 1 | 0.893 | 0.625 | 0.315 | 0.076 |
| 3 (-4° to 4°) | 47.74 (48) | 0.305 | 0.610 | 0.887 | 1 | 0.887 | 0.610 | 0.305 | 0.054 |
| 9 (-8° to 8°, step 2°) | 143.24 (144) | 0.289 | 0.588 | 0.878 | 1 | 0.878 | 0.588 | 0.289 | 0.026 |
| 11 (-15° to 15°, step 3°) | 175.06 (176) | 0.235 | 0.508 | 0.842 | 1 | 0.842 | 0.508 | 0.235 | 0.037 |

The peak is $N M$ times the amplitude up to the interpolation loss, as Theorem 2 of the proof says. A wider span of angles narrows the main lobe, and more angles in a span lower the side lobes. The table is a measurement on this small simulation; the numbers depend on the array, the depth and the pulse.

## Correctness

The compounded image is linear in the data before the modulus, the code checks it against its exact adjoint, and it equals the sum of the complex single-angle images. For a point scatterer and exact samples, every term at the scatterer equals the amplitude times $g(0)$, so the pixel value there is $N M |a| g(0)$ (or $N$ times the number of elements in the aperture), and the triangle inequality shows that no pixel is larger. The transmit time of L5 is exact for a plane wave that passes the origin at time $0$. The proofs are in proofs/correctness.md.

These are results for the model: ideal plane waves, point scatterers, single scattering and a known constant $c$. A real array of finite width makes an imperfect plane wave with edge waves, and the image near the edges of the insonified region is worse.

## Complexity

In the real-RAM model, each pixel reads $N M$ samples (fewer with an f-number), so an $n \times n$ image costs $O(N M n^2)$, and the extra space is $O(M)$. This is $M/N$ times less work than TFM on the same grid.

The acquisition is the main gain. A frame needs $N$ firings, each one round trip to the deepest point. For a depth of 60 mm the round trip is $120 / 1.54 = 77.9$ us at 1.54 mm/us, so 9 angles take 0.70 ms per frame (about 1400 frames per second), against 9.97 ms for 128 focused lines (about 100 frames per second). These figures ignore dead time and processing.

## Properties

- Linear in the data before the modulus, with an exact adjoint; the compound is the sum of the angle images.
- Every pixel is in the receive focus; the transmit focus is synthetic and improves with the number and span of the angles.
- The transmitted energy of each firing comes from all elements, so the signal-to-noise ratio per firing is higher than for single-element synthetic aperture.
- Motion between firings changes the phase of the angle images and lowers the gain of the coherent sum; with $N$ firings in a fraction of a millisecond this is small for most tissue.
- The number of angles is a design choice. Montaldo et al. (2009) relate it to the aperture, the wavelength and the f-number, so that the compound matches focused imaging; this is a rule of thumb, not a theorem.

## Variants and improvements

- **Diverging waves.** For phased arrays with a small footprint, virtual point sources behind the array give a sector field of view; the transmit time is the distance to the virtual source.
- **Weights.** Receive apodization, an f-number (line L7) and weights over the angles lower the side lobes.
- **Adaptive combination.** The [coherence factor](/coherence-factor/), [delay-multiply-and-sum](/delay-multiply-and-sum/) and the [Capon beamformer](/capon-beamformer/) can replace the plain sum over elements or angles.
- **Ultrafast Doppler.** The high frame rate allows long ensembles at every pixel, which [SVD clutter filtering](/svd-clutter-filter/) and the [Kasai estimator](/kasai-autocorrelation-estimator/) use for blood flow.
- **Shear wave elastography.** Frames thousands of times per second can follow a shear wave through tissue; this was a main motivation of Montaldo et al.

## When to use it

Use plane-wave compounding when the frame rate matters: Doppler and functional imaging, elastography and fast moving organs. A focused transmit still gives a better signal-to-noise ratio at the focal depth for the same number of firings, and it is simpler on older hardware that cannot store all channel data.

## Pitfalls

- **Time origin.** The formula of L5 assumes that each wave passes $(0, 0)$ at $t = 0$. If the hardware starts the clock when the first element fires, add the offset $\frac{M-1}{2} d\, |\sin\alpha| / c$ for a centered array of pitch $d$, or the image shifts with the angle and the compounding blurs.
- **Incoherent sum.** Taking the modulus of each angle image before the sum gives incoherent compounding: less speckle, but no gain in resolution.
- **Too few or too wide angles.** Few angles leave high side lobes; large tilts with element directivity add little signal and cause grating lobes for a coarse pitch.
- **Motion.** Fast motion during the $N$ firings dephases the angle images; motion compensation or fewer angles help.
- **Edges of the field.** Pixels near the lateral edges are not lit by all tilted waves; limit the sum to the angles that cover the pixel.

## Implementations

## History

Synthetic aperture imaging in medical ultrasound used single elements or small groups of elements and coherent sums after the scan (Jensen, Nikolov, Gammelmark and Pedersen 2006 give an overview). Plane-wave transmissions for very high frame rates were used for transient elastography. Montaldo, Tanter, Bercoff, Benech and Fink (2009) showed that a coherent sum of a small number of tilted plane-wave images matches the quality of conventional focused imaging at much higher frame rates. This made ultrafast imaging, with thousands of frames per second, a standard tool for Doppler, elastography and functional ultrasound.

## References
