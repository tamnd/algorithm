---
tag: 0AS03A
kind: technique
slug: inverse-synthetic-aperture-radar
name: Inverse synthetic aperture radar
aliases:
- ISAR
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: "Image a moving target with a fixed radar by using the rotation of the target to make the synthetic aperture, focused by range-Doppler processing."
prereqs: [synthetic-aperture-radar, range-doppler-processing]
see_also: [polar-format-algorithm, sar-image-formation, phase-gradient-autofocus, pulse-compression, cross-correlation, fourier-slice-theorem, stepped-frequency-waveform, image-registration]
sources:
  - paper: doi:10.1109/TAES.1980.308875
    title: "Jack L. Walker, Range-Doppler imaging of rotating objects, IEEE Transactions on Aerospace and Electronic Systems 16(1), 1980, 23 to 52"
    locator: "the range-Doppler image of a rotating object, its resolution, and the polar format processing for larger rotation angles (general locator)"
  - paper: doi:10.1109/TAES.1980.308873
    title: "C. C. Chen and H. C. Andrews, Target-motion-induced radar imaging, IEEE Transactions on Aerospace and Electronic Systems 16(1), 1980, 2 to 14"
    locator: "imaging of a moving target by a fixed radar, with the target motion providing the aperture (general locator)"
  - paper: doi:10.1109/TAES.1984.4502060
    title: "Dale A. Ausherman, Adam Kozma, Jack L. Walker, Harrison M. Jones and Enrico C. Poggio, Developments in radar imaging, IEEE Transactions on Aerospace and Electronic Systems 20(4), 1984, 363 to 400"
    locator: "the unified view of SAR and ISAR as imaging from a change of aspect angle (general locator)"
---

Inverse synthetic aperture radar (ISAR) forms a radar image of a moving object, such as a ship, an aircraft or a satellite, with a radar that does not move. In [SAR](/synthetic-aperture-radar/) the radar moves past a still scene. In ISAR the object turns relative to the line of sight, and what matters for imaging is only the change of the aspect angle, so the two are the same problem seen from different frames. A wideband pulse resolves the object in range. During the rotation, scatterers at different cross-range positions move toward or away from the radar at different speeds, so they have different Doppler frequencies, and a Fourier transform over the pulses separates them. After the translation of the object is removed, an ISAR image is the [range-Doppler](/range-doppler-processing/) map of the pulses. Its cross-range scale depends on the rotation rate, which the radar usually does not know.

## In plain words

A radar on the ground watches a ship that rolls and turns on the waves. Each pulse tells how much the ship reflects at each distance, but not where across the ship. As the ship turns, a part on one side comes a little closer and a part on the other side moves a little away, so their echoes shift in frequency in opposite directions. Line up the pulses so that the ship as a whole seems to stand still, then sort each distance by this small frequency shift. The result is a picture of the ship, with distance on one axis and position across the ship on the other.

## When it applies

- **The object turns relative to the line of sight.** The aspect angle changes by a small total angle $\Delta\theta$ during the coherent processing interval; the cross-range resolution is $\lambda/(2\Delta\theta)$.
- **The object is rigid** over that interval, and its scatterers are points whose response does not change much with the angle.
- **The translation can be removed.** The range of a reference point of the object, and its phase, must be tracked to a small part of the wavelength, from the data themselves.
- **The rotation is smooth.** For range-Doppler imaging the rotation rate $\Omega$ should be close to constant and the axis close to fixed during the interval.
- **The radar has a wide band** $B$, as a chirp after [pulse compression](/pulse-compression/) or a [stepped frequency waveform](/stepped-frequency-waveform/), for the range resolution $c/(2B)$.

## The template

Put the object frame with its origin at a reference point and the axis $y$ along the line of sight at the start. A scatterer at $(x, y)$ in the object frame, after the object has turned by $\theta(t)$, is at the range
$$R(t) = R_{\text{ref}}(t) + x \sin\theta(t) + y \cos\theta(t)$$
for a far radar, where $R_{\text{ref}}$ is the range of the reference point. At the frequency $f$ of the band, the echo has the phase $e^{-i 4\pi f R(t)/c}$. The Fourier sign is $e^{-i 2\pi f t}$, as for the DFT; radar books often use $e^{+j\omega t}$ and so the opposite signs. Once $R_{\text{ref}}$ is removed, the data are the same as the dechirped spotlight data of the [polar format algorithm](/polar-format-algorithm/), with the look angle $\theta(t)$: samples of the 2D Fourier transform of the object on a polar raster. For a small angle and a constant rate, $\theta = \Omega t$, $\sin\theta \approx \Omega t$ and $\cos\theta \approx 1$, so the phase is $-4\pi f y/c - 2\pi (2 f x \Omega / c)\, t$. The first term places the scatterer at the range $y$, and the second is a Doppler frequency $f_D = 2 x \Omega/\lambda$, proportional to the cross-range $x$.

```pseudo id=main
ISAR(pulses, B, λ)    ▷ pulses: echoes of a moving object; returns a range-Doppler image
L1  P ← PULSE-COMPRESSION(pulses)                         ▷ range profiles, resolution c / (2B)
L2  P ← RANGE-ALIGN(P)                                     ▷ hole: remove the change of R_ref in range
L3  P ← PHASE-ADJUST(P)                                    ▷ hole: remove the phase e^{-i 4π f R_ref / c}
L4  I ← FORM-IMAGE(P)                                      ▷ hole: DFT over pulses in each range bin, or polar format
L5  x ← λ f_D / (2 Ω̂) for each Doppler bin f_D            ▷ hole: estimate of Ω for the cross-range scale
L6  return I with range and cross-range axes
```

The holes are filled as follows. RANGE-ALIGN shifts each range profile so that the object stays in the same range bins, for example by the peak of the [cross-correlation](/cross-correlation/) of the magnitude of each profile with that of the previous profiles, smoothed over time. PHASE-ADJUST removes the remaining phase of the reference point, from a single strong scatterer, from the mean over many scatterers, or by an autofocus such as [phase gradient autofocus](/phase-gradient-autofocus/). FORM-IMAGE is a DFT over the pulses in each range bin when the angle is small, and the polar format algorithm, or [backprojection](/sar-backprojection/) once $\theta(t)$ is known, when it is not. The cross-range scale of L5 needs $\Omega$, which can be estimated from the motion data of the object or from the image itself.

Each of these is a heuristic except FORM-IMAGE, whose behavior under the model above is exact. The range-Doppler form also has two limits, which follow from the next terms of $\sin\theta$ and $\cos\theta$. A scatterer at the cross-range $x$ moves in range by about $x\Delta\theta$ during the interval; if this exceeds the range resolution $\rho_r = c/(2B)$, it smears over several range bins. With the cross-range resolution $\rho_a = \lambda/(2\Delta\theta)$, this needs $|x| < \rho_r/\Delta\theta = 2\rho_r\rho_a/\lambda$. A scatterer at the range $y$ has the extra phase $(4\pi y/\lambda)(1 - \cos\theta)$, quadratic in $t$; keeping it below $\pi/2$ at the ends of the interval, $\theta = \pm\Delta\theta/2$, needs $|y| < \lambda/\Delta\theta^2 = 4\rho_a^2/\lambda$. Larger objects need the polar format.

**Example.** An X-band radar with $\lambda = 3$ cm and $B = 500$ MHz watches a ship that turns by $\Delta\theta = 0.05$ rad (about 2.9 degrees) during the interval. The range resolution is $c/(2B) = 0.3$ m, and the cross-range resolution is $0.03/(2 \cdot 0.05) = 0.3$ m. The range-Doppler image is free of range migration for $|x| < 0.3/0.05 = 6$ m and free of the quadratic phase for $|y| < 0.03/0.05^2 = 12$ m. A ship 100 m long needs either a shorter interval, with a coarser cross-range resolution, or polar format processing. If the ship turns at $\Omega = 0.02$ rad/s, the interval is 2.5 s, and a scatterer 10 m off the axis has the Doppler frequency $2 \cdot 10 \cdot 0.02/0.03 \approx 13.3$ Hz.

## Classic examples

- **Ships at sea.** Roll, pitch and yaw of the ship give the rotation. The axis changes with time, so the image plane changes too; the choice of the interval decides whether the image looks like a side view or a top view.
- **Aircraft.** A turn or a small change of heading gives the change of aspect angle. Range alignment and [autofocus](/phase-gradient-autofocus/) are the hard steps, because the path of the aircraft is not known.
- **Satellites and space objects.** A ground radar tracks a satellite as it passes over, and the change of aspect angle comes from the orbit and the attitude of the satellite.
- **Planetary radar.** Delay-Doppler mapping of the Moon, Venus and asteroids from Earth uses the rotation of the body in the same way, with delay for range and Doppler for cross-range.
- **Turntable measurement.** An object on a turntable in a measurement range, with a known rotation, gives ISAR images used to find the scattering centers of the object; the polar format algorithm is the usual processor.

## Variations

- **Polar format ISAR.** For larger angles, the data are interpolated onto a rectangular grid, as in the [polar format algorithm](/polar-format-algorithm/), with the angle taken from the estimated rotation.
- **Time-frequency ISAR.** When the rotation is not uniform, a time-frequency distribution replaces the DFT over the pulses, and gives an image for each instant.
- **Interferometric ISAR.** Two or more receivers give the height of the scatterers out of the image plane, as in [SAR interferometry](/sar-interferometry/).
- **Bistatic and passive ISAR.** The transmitter and receiver are apart, or the transmitter is a broadcast station; the geometry changes the scale but not the principle.

## Pitfalls

- **Unknown cross-range scale.** The DFT gives Doppler, not distance. Without an estimate of $\Omega$, lengths along cross-range are not known, and the image can look stretched.
- **Nonuniform rotation.** A changing rate or axis gives a Doppler that changes with time and blurs the image in cross-range. Shorten the interval, or use a time-frequency method.
- **Range alignment errors.** An error of a fraction of a range bin from pulse to pulse leaves a residual phase that autofocus must remove; a jump of one bin breaks the image.
- **Migration through resolution cells.** Scatterers far from the center smear in range and in Doppler when the object is large, as the limits above show; check them before trusting the edges of the image.
- **Image plane.** The image is a projection on the plane that holds the line of sight and the change of the line of sight; it is not a top view in general.

## Exercises

1. From $R(t) = R_{\text{ref}}(t) + x\sin\Omega t + y\cos\Omega t$, show that after removing $R_{\text{ref}}$ the Doppler frequency of a scatterer at small $t$ is $2x\Omega/\lambda$, and that a DFT over a time $T$ resolves $\Delta x = \lambda/(2\Omega T)$.
2. Show that the range of a scatterer at $(x, 0)$ changes by $x\sin(\Delta\theta/2) \cdot 2 \approx x\Delta\theta$ over the interval, and derive the condition $|x| < 2\rho_r\rho_a/\lambda$.
3. Derive the condition $|y| < 4\rho_a^2/\lambda$ from the requirement that the quadratic phase $(4\pi y/\lambda)(1 - \cos\theta)$ is at most $\pi/2$ at $\theta = \pm\Delta\theta/2$.
4. A target turns at $\Omega = 0.01$ rad/s and the radar has $\lambda = 3$ cm. How long must the interval be for a cross-range resolution of 0.5 m? What is the Doppler frequency of a scatterer 5 m off the axis?
5. Show that, for a far radar, the ISAR data after motion compensation are the dechirped spotlight SAR data of the same object seen from a radar that moves around it on a circle, and so are samples of its 2D Fourier transform on a polar raster.

## References
