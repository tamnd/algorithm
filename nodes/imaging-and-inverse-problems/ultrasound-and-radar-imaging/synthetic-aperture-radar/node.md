---
tag: N960VQ
kind: concept
slug: synthetic-aperture-radar
name: Synthetic aperture radar
aliases:
- SAR
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: core
summary: "A radar on a moving platform that combines the echoes from many positions into the image of a long antenna, reaching fine resolution along the track."
prereqs: [pulse-echo-imaging, pulse-compression]
see_also: [sar-image-formation, range-cell-migration, inverse-synthetic-aperture-radar, sar-interferometry, speckle, saft, moving-target-indication, radar-range-equation]
sources:
  - paper: doi:10.1109/TAES.1985.310578
    title: "Carl A. Wiley, Synthetic aperture radars: a paradigm for technology evolution, IEEE Transactions on Aerospace and Electronic Systems 21(3), 1985, 440 to 443"
    locator: "the account of the Doppler beam sharpening idea of 1951 and its early development (general locator)"
  - paper: doi:10.1109/MGRS.2013.2248301
    title: "Alberto Moreira, Pau Prats-Iraola, Marwan Younis, Gerhard Krieger, Irena Hajnsek and Konstantinos P. Papathanassiou, A tutorial on synthetic aperture radar, IEEE Geoscience and Remote Sensing Magazine 1(1), 2013, 6 to 43"
    locator: "the basic principles of SAR imaging, the resolution in range and azimuth, the operating modes and the history (general locator)"
  - book: isbn:9781580530583
    title: "Ian G. Cumming and Frank H. Wong, Digital Processing of Synthetic Aperture Radar Data, Artech House, 2005"
    locator: "Chapter 4, Synthetic Aperture Concepts, and Chapter 5, SAR Signal Properties"
  - paper: doi:10.1109/TAES.1984.4502060
    title: "Dale A. Ausherman, Adam Kozma, Jack L. Walker, Harrison M. Jones and Enrico C. Poggio, Developments in radar imaging, IEEE Transactions on Aerospace and Electronic Systems 20(4), 1984, 363 to 400"
    locator: "the survey of SAR and ISAR imaging and of the processing methods up to 1984 (general locator)"
---

A synthetic aperture radar (SAR) is an imaging radar on a moving platform, an aircraft or a satellite, that looks to the side of its track. It sends short pulses at a fixed rate and records the echoes at many positions along the track. Each pulse alone gives only range: the [pulse compression](/pulse-compression/) of a chirp resolves the scene to about $c/(2B)$ across the track for a bandwidth $B$. Along the track, a real antenna of length $L$ resolves only about $\lambda R / L$ at the range $R$, which is kilometers from space. SAR records the phase of every echo and combines the echoes of all positions that see a point, as if one antenna as long as the flown path had received them. The resolution along the track then becomes about $L/2$, independent of the range. The data are a two-dimensional echo record, and a focusing algorithm turns it into an image; that computation is the [SAR image formation](/sar-image-formation/) problem.

## In plain words

A radar on an airplane sends a click to the side and listens. The time of the echo tells how far away each reflector is, but a small antenna hears echoes from a wide strip of ground at once, so it cannot tell where along the flight a reflector is. The plane keeps flying and keeps clicking. Each reflector stays in view for many clicks, and its distance to the plane changes in a known way during that time. If you add up the recordings so that the echoes of one ground point line up, that point becomes sharp and the others blur away. The many small recordings then act like one very long antenna, which sees fine detail.

## The idea

**Geometry.** The platform moves on a straight line at the speed $V$. The slow time $\eta$ counts the pulses, and the fast time $\tau$ is the time after each pulse. A point target at the closest range $R_0$, passed at $\eta = 0$, has the range

$$R(\eta) = \sqrt{R_0^2 + V^2 \eta^2} \approx R_0 + \frac{V^2 \eta^2}{2 R_0}.$$

**The echo.** With a pulse $p(\tau)$ at the carrier frequency $f_0$ (wavelength $\lambda = c/f_0$), the demodulated echo of a target of complex reflectivity $a$ is

$$s(\tau, \eta) = a\, w(\eta)\, p\!\left(\tau - \frac{2 R(\eta)}{c}\right) \exp\!\left(-i\, \frac{4\pi f_0 R(\eta)}{c}\right),$$

where $w$ is the antenna pattern along the track. This page and its algorithm pages use the Fourier sign $e^{-i 2\pi f t}$ of the DFT, so the carrier phase of the echo is $e^{-i 4\pi f_0 R/c}$. Radar books often write the carrier as $e^{+j\omega t}$, which flips the signs of the phases below.

**Two chirps.** In fast time, $p$ is a [linear FM pulse](/linear-frequency-modulation-pulse/), and its [matched filter](/matched-filter/) compresses it to a width of about $1/B$ in time, which is $c/(2B)$ in range: 1.5 m for $B = 100$ MHz. In slow time, the phase $-4\pi R(\eta)/\lambda$ is close to $-4\pi R_0/\lambda - 2\pi V^2 \eta^2/(\lambda R_0)$. That is also a chirp, with the azimuth FM rate $K_a = 2V^2/(\lambda R_0)$ in size. A matched filter in slow time compresses it too.

**The resolution along the track.** An antenna of length $L$ has a beam about $\lambda/L$ wide, so a point stays in view for the synthetic aperture $L_s \approx \lambda R_0 / L$, flown in the time $T_s = L_s/V$. The Doppler bandwidth of the azimuth chirp is $K_a T_s \approx 2V/L$, and compression gives the time resolution $1/(K_a T_s)$, which is the distance $V/(K_a T_s) \approx L/2$ along the track. The same value follows from a two-way array of length $L_s$: $\lambda R_0/(2 L_s) = L/2$. This is the standard far-field estimate of the textbooks, not an exact theorem: weighting, squint and the processed bandwidth change it by a factor near 1. A smaller antenna gives a finer image, because it sees each point for longer.

**Range cell migration.** During the synthetic aperture, $R(\eta) - R_0$ can exceed the range resolution, so the echo of one point crosses several range cells. This is [range cell migration](/range-cell-migration/), and a focusing algorithm must follow the curve, not a single range line.

**Sampling.** The pulse rate (PRF) samples the slow time, so it must be larger than the Doppler bandwidth $2V/L$: the platform may move at most about $L/2$ between pulses. The echoes of one pulse must also arrive before the next pulse is sent, or they fold in range. These two limits pull the PRF in opposite directions, and they bound the swath width for a given resolution.

**Modes.** In stripmap mode the antenna points in a fixed direction and the image is a long strip. In spotlight mode the antenna turns to keep one patch in view, which makes the synthetic aperture longer than the beam and the resolution finer than $L/2$; the [polar format algorithm](/polar-format-algorithm/) is the classic processor for it. In [inverse SAR](/inverse-synthetic-aperture-radar/) the radar stands still and the target turns.

## Examples

**A small airborne case.** Take $f_0 = 300$ MHz ($\lambda = 1$ m), $V = 100$ m/s, a beam whose half angle has the sine 0.125, and a target at $R_0 = 400$ m. The real beam is about 100 m wide at that range, so the real aperture resolves only about 100 m along the track. The target stays in view for $L_s \approx 2 \cdot 400 \cdot 0.125 = 100$ m of flight, the Doppler frequency runs from $-2 V \cdot 0.125/\lambda = -25$ Hz to $25$ Hz, a band of 50 Hz, and the azimuth resolution is $V/50 = 2$ m, the same as $\lambda R_0/(2 L_s)$. At the ends of the aperture the range grows from 400 m to $400/\sqrt{1 - 0.125^2} = 403.16$ m, that is 3.16 m or about two range resolution cells for $B = 100$ MHz. This is the geometry of the tests of the [range-Doppler algorithm](/range-doppler-algorithm/).

**A spaceborne case.** A C-band radar ($\lambda = 5.6$ cm) at a range of 850 km with a 10 m antenna has a real beam about $0.056 \cdot 850000 / 10 \approx 4.8$ km wide on the ground. The synthetic aperture is about that long, and the azimuth resolution is about $L/2 = 5$ m. The ratio of the two, about a thousand, is the gain of the synthetic aperture.

## Where it is used

- **Image formation.** The [SAR image formation](/sar-image-formation/) problem and its algorithms: the [range-Doppler algorithm](/range-doppler-algorithm/), the [chirp scaling algorithm](/chirp-scaling-algorithm/), the [omega-k algorithm](/omega-k-algorithm/), the [polar format algorithm](/polar-format-algorithm/), [time-domain backprojection](/sar-backprojection/) and [fast factorized backprojection](/fast-factorized-backprojection/).
- **Autofocus.** Errors in the known flight path leave a phase error, which [phase gradient autofocus](/phase-gradient-autofocus/) estimates from the image.
- **Interferometry.** The phase difference of two SAR images gives the height of the terrain or its motion: [SAR interferometry](/sar-interferometry/), with [phase unwrapping](/phase-unwrapping/).
- **Image statistics.** Coherent images of rough ground show [speckle](/speckle/).
- **Moving targets.** [Moving target indication](/moving-target-indication/) and [space-time adaptive processing](/space-time-adaptive-processing/) separate moving targets from the ground.
- **Other waves.** The [synthetic aperture focusing technique](/saft/) applies the same idea to ultrasound, and the [omega-k algorithm](/omega-k-algorithm/) shares its mathematics with [seismic migration](/seismic-migration/).

## References
