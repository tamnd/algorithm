---
tag: RVQSBG
kind: technique
slug: dynamic-receive-focusing
name: Dynamic receive focusing
aliases:
- dynamic focusing
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: core
summary: "Update the receive delays of an array with the depth of the echo being received, so that every depth is in focus on receive. A growing aperture keeps the f-number constant."
prereqs: [delay-and-sum-beamforming, pulse-echo-imaging]
see_also: [beamforming, synthetic-transmit-aperture, plane-wave-compounding, total-focusing-method, b-mode-image-formation, coherence-factor, window-functions, point-spread-function]
sources:
  - book: isbn:9780123964878
    title: "Thomas L. Szabo, Diagnostic Ultrasound Imaging: Inside Out, 2nd edition, Academic Press, 2014"
    locator: "Chapter 7, Array beamforming (receive focusing, dynamic focusing and apodization); Chapter 6, Beamforming"
  - paper: doi:10.1109/ULTSYM.1996.584398
    title: "Kai E. Thomenius, Evolution of ultrasound beamformers, Proceedings of the 1996 IEEE Ultrasonics Symposium"
    locator: "the move from fixed and zoned receive focusing to dynamic focusing in digital beamformers (general locator)"
---

Dynamic receive focusing is the rule that makes the receive beam of an ultrasound array sharp at every depth. In a pulse-echo scan, echoes from deeper points arrive later, so at each moment the array is listening to one depth only: $z = c t/2$ along the beam. A fixed set of receive delays focuses at one depth and blurs the others. Dynamic focusing changes the delays continuously with the arrival time, so that for each output sample the delays are those of the point that is being received at that moment. For a beam along $x = 0$ and element $i$ at $x_i$, the echo from depth $z$ reaches the element at $(z + \sqrt{z^2 + x_i^2})/c$, which is later than at the center element by

$$\tau_i(z) = \frac{z + \sqrt{z^2 + x_i^2}}{c} - \frac{2z}{c}.$$

A dynamic aperture adds a second rule: only the elements within a width of $z/F$ around the beam take part, so the f-number $F$, the ratio of depth to aperture, stays constant, and so does the lateral resolution, until the full array is in use. Together, the two rules turn [delay-and-sum](/delay-and-sum-beamforming/) of one line into a receive focus at every depth. The transmit focus stays fixed; [synthetic transmit aperture](/synthetic-transmit-aperture/) and [plane-wave compounding](/plane-wave-compounding/) also focus the transmit at every depth.

## In plain words

The array sends one pulse down a line and then listens. Echoes from near points come back first and echoes from deep points come back later. To focus on a point, each element must wait the right extra time, because the outer elements are farther away. But the right waiting times are different for near and deep points. Dynamic focusing changes the waiting times while the echoes come in, so that at every moment the array is focused on the point it is hearing. It also starts with a few elements near the middle and adds more as the echoes come from deeper, which keeps the picture equally sharp at all depths.

## When it applies

Use it whenever an array receives echoes along a beam and forms the beam by delays: linear, phased and curved arrays in medical ultrasound, arrays in nondestructive testing, and sonar. It needs the speed of sound, assumed constant, the element positions and the direction of the beam. It focuses the receive side only. The pulse sent by a focused transmit is narrow only near its focal depth; outside the focal zone the two-way beam is limited by the transmit beam.

## The template

```pseudo id=main
DYNAMIC-RECEIVE(r_1 … r_M, x_1 … x_M, depths, c, F)   ▷ one beam along x = 0
L1  for each output depth z do
L2      acc ← 0
L3      for each element i with |x_i| ≤ z/(2F) do         ▷ dynamic aperture
L4          t ← (z + √(z² + x_i²)) / c                     ▷ transmit down, receive back to element i
L5          acc ← acc + w_i(z) · SAMPLE(r_i, t)
L6      y(z) ← acc
```

The weight $w_i(z)$ is an apodization over the active aperture, for example a window from [window functions](/window-functions/) scaled to the width $z/F$. SAMPLE interpolates the trace at the exact time, as on the [TFM](/total-focusing-method/) page. For a steered beam along the angle $\theta$, the point is $(z \sin\theta, z \cos\theta)$ at the distance $z$ from the center, and line L4 becomes $t = (z + |q - e_i|)/c$ with $q$ that point. In analog and early digital systems, the delays were updated in steps, in a few zones of depth; a digital beamformer computes them for each output sample.

## Classic examples

**Delays for a 16-element array.** With pitch 0.3 mm and $c = 1.54$ mm/us, the elements are at $x_i = \pm 0.15, \pm 0.45, \ldots, \pm 2.25$ mm. The extra delays $\tau_i(z)$ are:

| depth z | x = 0.15 mm | x = 1.05 mm | x = 2.25 mm |
|---|---|---|---|
| 6 mm | 0.0012 us | 0.0592 us | 0.2649 us |
| 20 mm | 0.0004 us | 0.0179 us | 0.0819 us |

The delays shrink with depth, because the wavefront from a deep point is flatter across the array.

**A fixed focus is wrong elsewhere.** If the delays for 20 mm are used for an echo from 6 mm, the outer element is off by $0.2649 - 0.0819 = 0.183$ us. At 5 MHz this is $0.915$ periods, so the outer elements add with almost the opposite phase, and the receive focus at 6 mm is lost. Dynamic focusing removes this error at every depth.

**A constant f-number.** With $F = 2$, the aperture width $z/F$ is 1.5 mm at $z = 3$ mm (6 elements), 3 mm at 6 mm (10 elements) and 6 mm at 12 mm (all 16). With $F = 1$, 10 elements are active at 3 mm and all 16 at 6 mm. Beyond the depth where the whole array is used, $F$ grows and the lateral resolution, about $\lambda F$, gets worse with depth (a heuristic from the far-field beam width).

**Image formation.** Every per-pixel method on the pages of this area uses dynamic receive focusing: [TFM](/total-focusing-method/), [plane-wave compounding](/plane-wave-compounding/) and the [B-mode](/b-mode-image-formation/) chain after a line beamformer.

## Variations

- **Zones.** Delays and apertures that change in steps at a few depths; cheaper in analog hardware and close to dynamic focusing for small steps.
- **Dynamic apodization.** The weights change with depth together with the aperture, to keep the side lobes of the receive beam constant.
- **Multiple transmit foci.** Several firings per line, each with a transmit focus at another depth, joined in depth; this extends the two-way focus at the cost of frame rate.
- **Synthetic transmit focusing.** [Synthetic transmit aperture](/synthetic-transmit-aperture/), [TFM](/total-focusing-method/) and [plane-wave compounding](/plane-wave-compounding/) apply the same per-depth idea to the transmit delays as well.
- **Adaptive combination.** The delayed samples of line L5 can be combined with a [coherence factor](/coherence-factor/), [delay-multiply-and-sum](/delay-multiply-and-sum/) or the [Capon beamformer](/capon-beamformer/) in place of the weighted sum.

## Pitfalls

- **Wrong speed of sound.** The delays assume one $c$. Fat and muscle have different speeds, and a wrong $c$ moves and blurs the focus; the error grows with the aperture.
- **Coarse delays.** Rounding the delays to whole samples adds phase errors of up to half a sample; at $f_s = 40$ MHz and 5 MHz this is up to $1/16$ of a period. Interpolate, or use IQ data with a phase correction.
- **Too small an f-number.** Elements far off the axis receive at large angles, where their directivity is weak and grating lobes appear; a minimum $F$ around 1 is common, but the right value is a design choice.
- **Near field.** At very small depths the aperture has few elements, so the lateral resolution there is set by the minimum aperture.
- **Transmit is not dynamic.** A sharp receive focus does not fix a wide transmit beam outside the focal zone; the two-way beam is the product of both.

## Exercises

1. Show that $\tau_i(z) \approx x_i^2 / (2 c z)$ for $z \gg |x_i|$, and use it to estimate $\tau_i$ at $z = 20$ mm and $x_i = 2.25$ mm. (The estimate is $0.0822$ us, against the exact $0.0819$ us.)
2. For an array of pitch $d$ and $F = 1.5$, at what depth does the active aperture first include $k$ elements on each side of the center? (When $z/(2F)$ reaches the position of the $k$-th element, $(k - 1/2) d$, so at $z = 3 (k - 1/2) d$.)
3. Explain why the delay error of a fixed focus at $z_f$, used at depth $z$, is largest for the outer elements, and show that it tends to $0$ as $z$ tends to $z_f$.

## References
