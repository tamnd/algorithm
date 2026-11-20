---
tag: WKKW7Y
kind: definition
slug: amplitude-and-phase-shift-keying
name: Amplitude and phase-shift keying
aliases:
- APSK
area: communications/modulation-and-detection
level: advanced
summary: "A constellation of PSK rings of different radii, such as 4+12 points. Few amplitude levels and a low peak power suit the nonlinear amplifiers of satellite links, as in DVB-S2."
prereqs: [phase-shift-keying, quadrature-amplitude-modulation]
see_also: [phase-shift-keying, quadrature-amplitude-modulation, signal-constellation, peak-to-average-power-ratio, minimum-distance-detector, soft-demapping, gray-labeling, spectral-efficiency]
sources:
  - paper: doi:10.1109/TWC.2006.1687763
    title: Riccardo De Gaudenzi, Albert Guillén i Fàbregas and Alfonso Martinez, Performance analysis of turbo-coded APSK modulations over nonlinear satellite channels, IEEE Transactions on Wireless Communications 5(9), 2006
    locator: pp. 2396 to 2407 (APSK on a nonlinear satellite channel, with ring radii and phases chosen for the channel, and the predistortion of each ring)
  - paper: "Riccardo De Gaudenzi, Albert Guillén i Fàbregas and Alfonso Martinez, Turbo-coded APSK modulations design for satellite broadband communications, International Journal of Satellite Communications and Networking 24(4), 2006"
    locator: pp. 261 to 281 (the design of 16-APSK and 32-APSK ring ratios for each code rate, as adopted in DVB-S2)
  - paper: "ETSI EN 302 307, Digital Video Broadcasting (DVB); Second generation framing structure, channel coding and modulation systems for Broadcasting, Interactive Services, News Gathering and other broadband satellite applications (DVB-S2)"
    locator: clause 5.4.3 and Table 9 (the 16APSK constellation of 4 + 12 points and its ring ratio for each code rate)
---

Amplitude and phase-shift keying (APSK) is a family of constellations whose points lie on a few concentric rings, each ring holding equally spaced points as in [PSK](/phase-shift-keying/). A 16-point APSK constellation has, for example, $4$ points on an inner ring and $12$ on an outer ring. Compared with square [QAM](/quadrature-amplitude-modulation/) of the same size it has fewer amplitude levels and a lower peak power. This makes it the usual choice when the transmitter must drive a nonlinear amplifier close to saturation, as on a satellite, and it is the 16-point and 32-point modulation of DVB-S2.

## Definition

An **APSK constellation** with $K$ rings is given by radii $0 < r_1 < r_2 < \cdots < r_K$, numbers of points $n_1, \ldots, n_K$ with $\sum_k n_k = M$, and phase offsets $\theta_1, \ldots, \theta_K$. Its points are

$$s_{k,i} = r_k\, e^{j(\theta_k + 2\pi i/n_k)}, \qquad k = 1, \ldots, K, \quad i = 0, \ldots, n_k - 1,$$

where $j$ is the imaginary unit. It is written $n_1 + n_2 + \cdots + n_K$-APSK, for example 4+12-APSK. The **ring ratios** are $\gamma_k = r_{k+1}/r_1$. With equally likely points the average energy is $E_s = \frac{1}{M}\sum_k n_k r_k^2$; in code the radii are scaled so that $E_s = 1$, that is $\sum_k n_k r_k^2 = M$.

For 4+12-APSK with ring ratio $\gamma$:

$$r_1 = \sqrt{\frac{16}{4 + 12\gamma^2}}, \qquad r_2 = \gamma r_1.$$

The phases used here (and in DVB-S2) are $\pi/4 + k\pi/2$ on the inner ring and $\pi/12 + k\pi/6$ on the outer ring, so that the inner points sit on the bisectors of the outer ones.

**Properties.**
- *Peak power.* The peak power is $r_K^2$. With $E_s = 1$ this is the peak-to-average ratio of the constellation, one part of the [peak-to-average power ratio](/peak-to-average-power-ratio/) of the signal.
- *Few amplitude levels.* A nonlinear amplifier changes the amplitude (AM/AM) and the phase (AM/PM) of each point as a function of its amplitude. With only $K$ amplitudes, the transmitter can predistort each ring with one gain and one phase rotation, and the receiver can track each ring with one center.
- *Minimum distance.* The smallest distance is the least of the distance between neighbors on one ring, $2r_k \sin(\pi/n_k)$, and the distances between rings. APSK gives up some distance against square QAM of the same $M$ in exchange for the lower peak.
- *Labels.* A Gray labeling in which every pair of nearest neighbors differs in one bit is not always possible, because the rings have different numbers of points; practical labelings keep most neighbor pairs at one bit.
- *Detection.* The [minimum-distance detector](/minimum-distance-detector/) applies as for any constellation; there is no simple slicer along two axes as for square QAM. Coded systems use [soft demapping](/soft-demapping/).

## Examples and non-examples

**4+12-APSK at three ring ratios** (unit average energy):

| $\gamma$ | $r_1$ | $r_2$ | $d_{\min}$ | $d_{\min}^2$ | peak power |
|---|---|---|---|---|---|
| 2.57 | 0.43837 | 1.12662 | 0.58318 (outer ring) | 0.34010 | 1.2693 |
| 2.85 | 0.39709 | 1.13171 | 0.56157 (inner ring) | 0.31536 | 1.2808 |
| 3.15 | 0.36057 | 1.13578 | 0.50992 (inner ring) | 0.26001 | 1.2900 |

For $\gamma = 2.85$: $4r_1^2 + 12r_2^2 = 4 \cdot 0.15768 + 12 \cdot 1.28077 = 16$. The inner neighbors are $\sqrt2\, r_1 = 0.56157$ apart, the outer neighbors $2r_2\sin(\pi/12) = 0.58582$, and the rings $r_2 - r_1 = 0.73462$ (an inner point and the outer point at the same phase). The inner ring sets $d_{\min}$. A smaller $\gamma$ moves the inner points apart and the outer ones together, and $d_{\min}$ moves to the outer ring between $2.57$ and $2.85$.

**Against 16-QAM.** Square 16-QAM with unit average energy has $d_{\min}^2 = 0.4$ and peak power $1.8$ ($2.55$ dB). 4+12-APSK with $\gamma = 2.85$ has $d_{\min}^2 = 0.315$, about $1$ dB less in a linear channel, and peak power $1.281$ ($1.07$ dB), about $1.5$ dB less. On a satellite amplifier, where the transmitter must back off from saturation by about the peak-to-average ratio, the smaller back-off wins.

**DVB-S2.** The standard uses 4+12-APSK with a ring ratio that depends on the code rate: $3.15$ at rate $2/3$, $2.85$ at $3/4$, $2.75$ at $4/5$, $2.70$ at $5/6$, $2.60$ at $8/9$ and $2.57$ at $9/10$. The ratio falls as the code rate grows. For 32 points it uses 4+12+16-APSK.

**Non-example: square 16-QAM.** Its points lie on three circles with $4$, $8$ and $4$ points, but the $8$ points on the middle circle are not equally spaced in phase. So 16-QAM is not an APSK constellation in the sense above.

**Edge case: PSK.** One ring, $K = 1$, gives $M$-PSK. APSK is the extension of PSK to several rings.

**Star QAM.** Two rings of $8$ points at the same phases (8+8 with $\theta_1 = \theta_2$) is an APSK constellation. Its rings are aligned so that a receiver can detect the phase step and the ring step separately, which is convenient for differential detection.

## Related definitions

- [Phase-shift keying](/phase-shift-keying/): the one-ring case, with constant amplitude.
- [Quadrature amplitude modulation](/quadrature-amplitude-modulation/): the square grid, with larger distance and larger peaks.
- [Signal constellation](/signal-constellation/): the general set of points that APSK is an example of.
- [Peak-to-average power ratio](/peak-to-average-power-ratio/): the measure that APSK keeps low.
- [Gray labeling](/gray-labeling/): the labeling that APSK can only approach.
- [Spectral efficiency](/spectral-efficiency/): 16-APSK and 32-APSK carry $4$ and $5$ bits per symbol.

## References
