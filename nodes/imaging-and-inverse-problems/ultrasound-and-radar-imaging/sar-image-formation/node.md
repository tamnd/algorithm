---
tag: 6RRSHN
kind: problem
slug: sar-image-formation
name: SAR image formation
aliases:
- SAR focusing
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: core
summary: "Turn the raw two-dimensional echo data of a synthetic aperture radar into a focused reflectivity image of the ground."
model: real-ram
prereqs: [synthetic-aperture-radar, matched-filter]
see_also: [range-cell-migration, inverse-problem, forward-operator, point-spread-function, tomographic-reconstruction-problem, seismic-migration, pulse-echo-imaging, inverse-synthetic-aperture-radar]
sources:
  - book: isbn:9781580530583
    title: "Ian G. Cumming and Frank H. Wong, Digital Processing of Synthetic Aperture Radar Data, Artech House, 2005"
    locator: "Chapters 6 (range-Doppler algorithm), 7 (chirp scaling algorithm), 8 (omega-K algorithm) and 11 (comparison of algorithms)"
  - book: isbn:9780792396772
    title: "Charles V. Jakowatz Jr., Daniel E. Wahl, Paul H. Eichel, Dennis C. Ghiglia and Paul A. Thompson, Spotlight-Mode Synthetic Aperture Radar: A Signal Processing Approach, Kluwer, 1996"
    locator: "the chapters A Tomographic Foundation for Spotlight-Mode SAR Imaging and Aspects of Spotlight-Mode Image Formation"
  - paper: doi:10.1109/PROC.1983.12698
    title: "David C. Munson Jr., James D. O'Brien and W. Kenneth Jenkins, A tomographic formulation of spotlight-mode synthetic aperture radar, Proceedings of the IEEE 71(8), 1983, 917 to 925"
    locator: "the spotlight SAR data as samples of the Fourier transform of the scene, as in the projection slice theorem (general locator)"
  - paper: doi:10.1109/7.78293
    title: "Ciro Cafforio, Claudio Prati and Fabio Rocca, SAR data focusing using seismic migration techniques, IEEE Transactions on Aerospace and Electronic Systems 27(2), 1991, 194 to 207"
    locator: "SAR focusing as wave equation migration, and the wavenumber domain algorithm (general locator)"
  - paper: doi:10.1109/MGRS.2013.2248301
    title: "Alberto Moreira, Pau Prats-Iraola, Marwan Younis, Gerhard Krieger, Irena Hajnsek and Konstantinos P. Papathanassiou, A tutorial on synthetic aperture radar, IEEE Geoscience and Remote Sensing Magazine 1(1), 2013, 6 to 43"
    locator: "the SAR signal model and the overview of focusing (general locator)"
---

SAR image formation, also called SAR focusing, is the problem of turning the raw echo record of a [synthetic aperture radar](/synthetic-aperture-radar/) into an image of the reflectivity of the ground. The record is two-dimensional: one row of fast-time samples per pulse, and one pulse per position along the track. The echo of one point is spread over the whole synthetic aperture, along a curve given by its range history, and it carries a known phase. Focusing collects that energy back into one pixel. The usual target is the [matched filter](/matched-filter/) image, the adjoint of the [forward operator](/forward-operator/) applied to the data, whose response to a point is the [point spread function](/point-spread-function/) of the system. The exact sum costs one term per pulse and pixel, and the fast algorithms trade exactness or generality of the flight path for FFTs.

## In plain words

The radar has a long list of recordings, one per pulse, and every point on the ground left a faint trace in many of them, at slightly different delays. The task is to make a picture in which each point on the ground is one bright spot. To do this, you must know where each point's trace lies in the recordings and add the trace up so that its parts agree. Doing that one point at a time is simple but slow. The fast methods do the same adding with Fourier transforms, which needs a simple flight path, or with a clever reuse of partial sums.

## Definition

**Input.** The antenna positions $a_p \in \mathbb{R}^3$ for the pulses $p = 1, \ldots, P$; the transmitted pulse $s_0(\tau)$ with carrier frequency $f_0$ and bandwidth $B$; and the demodulated data $d[p][j]$, sampled at the fast times $\tau_j = \tau_{\text{start}} + j / f_s$, $j = 0, \ldots, N - 1$.

**Model.** A scene of point scatterers $\sigma(x)$ on a surface gives, under single scattering, a constant speed of propagation $c$ and the stop-and-go approximation (the antenna does not move during one echo),

$$d[p][j] = \sum_x \sigma(x)\, w_p(x)\, s_0\!\left(\tau_j - \frac{2 R_p(x)}{c}\right) e^{-i 4\pi f_0 R_p(x)/c} + n[p][j], \qquad R_p(x) = |a_p - x|,$$

with the antenna pattern $w_p$ and noise $n$. Write $d = A \sigma + n$ for this linear map. The Fourier sign is $e^{-i 2\pi f t}$, as for the DFT; radar books often write $e^{+j\omega t}$ and get the opposite sign of the carrier phase.

**Output.** An image $I(x)$ on a grid of pixels, ideally $I = A^H d$:

$$I(x) = \sum_{p=1}^{P} w_p(x)\, \big(d_p \star s_0\big)\!\left(\frac{2 R_p(x)}{c}\right) e^{+i 4\pi f_0 R_p(x)/c},$$

where $d_p \star s_0$ is the range-compressed pulse $p$. For one point $\sigma = a\, \delta_{x_0}$ with no noise, $I(x_0) = a \lVert A \delta_{x_0}\rVert^2$, the largest value of $|I|$ over all $x$ by the Cauchy-Schwarz inequality. The quality of a solution is measured on such point targets: the position and height of the peak, the width of the main lobe, and the levels of the side lobes.

## Variants

- **Stripmap.** A straight track at a constant speed and a fixed beam. The geometry is the same for every along-track position, so the problem is shift-invariant along the track, and FFT algorithms apply.
- **Spotlight.** The beam follows one patch. After dechirping on the patch center, each pulse is a slice of the 2D Fourier transform of the scene on a polar raster.
- **Squint.** The beam points forward or backward; the Doppler centroid is not zero, and the [range cell migration](/range-cell-migration/) has a linear part.
- **Any flight path.** The positions $a_p$ are known but do not lie on a line, for drones, low-frequency and wide-angle systems.
- **Unknown phase errors.** The path is known only to a fraction of a wavelength. The problem then has an extra unknown phase per pulse, the autofocus problem.
- **Moving target or still radar.** [Inverse SAR](/inverse-synthetic-aperture-radar/) images a turning target with a fixed radar.
- **Regularized inversion.** Instead of $A^H d$, solve a [least squares problem](/least-squares-problem/) for $\sigma$ with a penalty, as an [inverse problem](/inverse-problem/). This sharpens sparse scenes and costs many applications of $A$ and $A^H$.

## Examples

**One point target.** In the stripmap geometry of the [range-Doppler algorithm](/range-doppler-algorithm/) tests ($f_0 = 300$ MHz, $B = 100$ MHz, a 0.2 us chirp sampled at 120 MHz, $V = 100$ m/s, a pulse every 1.25 m), a unit target at $R_0 = 400$ m is in the beam for 81 pulses, and each echo has 24 or 25 chirp samples of modulus 1, 1945 in total. So the matched filter value at the target is $\lVert A\delta_{x_0}\rVert^2 = 1945$, and the answer is the image with a peak of 1945 at that pixel. Its main lobe is about $c/(2B) = 1.5$ m wide in range and about $V/50\ \text{Hz} = 2$ m wide along the track. The algorithm pages compare their fast images with this brute-force sum.

**Two targets.** Add a second target of amplitude 0.7 at 10 m along the track and 410 m range; it is in the beam for 83 pulses, with $\lVert A\delta_{x_1}\rVert^2 = 1992$. The map is linear, so the answer is the sum of the two point responses, with a peak close to $0.7 \cdot 1992$ at the second pixel; the side lobes of each add a little to the peak of the other.

## Known algorithms

| Algorithm | Geometry | Cost | Exactness |
|---|---|---|---|
| [Time-domain backprojection](/sar-backprojection/) | any known path | $O(P n^2)$ for an $n \times n$ image | the sum above, up to the range interpolation |
| [Fast factorized backprojection](/fast-factorized-backprojection/) | any path close to a line | $O(n^2 \log n)$ for $P$ of order $n$ | approximate; the error is set by the polar grid sampling |
| [Range-Doppler algorithm](/range-doppler-algorithm/) | straight path, stripmap | $O(M N (\log(M N) + K))$ for $M$ pulses, $N$ range samples and a $K$-tap interpolator | approximate at wide beams and long ranges of migration |
| [Chirp scaling algorithm](/chirp-scaling-algorithm/) | straight path, stripmap | $O(M N \log(M N))$ | approximate; no interpolation |
| [Omega-k algorithm](/omega-k-algorithm/) | straight path at constant speed | $O(M N (\log(M N) + K))$ | exact for that geometry up to the stationary phase step and the interpolation |
| [Polar format algorithm](/polar-format-algorithm/) | spotlight | $O(M N (\log(M N) + K))$ | exact under the plane-wave approximation |
| [Phase gradient autofocus](/phase-gradient-autofocus/) | after any of the above | $O(I M N \log N)$ for $I$ iterations | a heuristic estimate of a phase error |

## Bounds

- **Resolution.** The data hold the scene only in a band of spatial frequencies, so no linear method resolves finer than about $c/(2B)$ in range and about $\lambda/(2\Delta\theta)$ across range for a change $\Delta\theta$ of the look angle; for stripmap, $\Delta\theta \approx \lambda/L$ gives $L/2$. These are far-field estimates of the width of the point spread function, not theorems about every estimator; a prior such as sparsity can do better on special scenes.
- **Cost upper bounds.** The direct sum costs $O(P n^2)$ for $P$ pulses and $n \times n$ pixels. For $P$ of order $n$, the FFT algorithms and FFBP cost $O(n^2 \log n)$.
- **Cost lower bound.** Any algorithm must read the $P N$ samples and write the $n^2$ pixels, so $\Omega(P N + n^2)$. This page states no better lower bound.

## Reductions

- **Spotlight SAR to tomography.** Munson, O'Brien and Jenkins (1983) showed that, under the plane-wave approximation, a dechirped spotlight pulse is a band of one line of the 2D Fourier transform of the scene, as in the [Fourier slice theorem](/fourier-slice-theorem/). Image formation then becomes the [tomographic reconstruction problem](/tomographic-reconstruction-problem/) with band-pass data, and the polar format algorithm is [direct Fourier reconstruction](/direct-fourier-reconstruction/). The reduction costs $O(1)$ per sample.
- **SAR to seismic migration.** With the [exploding reflector model](/exploding-reflector-model/) and the wave speed $c/2$, the SAR record is a zero-offset seismic section, and focusing is [seismic migration](/seismic-migration/). Cafforio, Prati and Rocca (1991) used this to derive the omega-k algorithm from [Stolt migration](/stolt-migration/).
- **SAR to ultrasound.** With sound in place of radio waves, the same sum is the [synthetic aperture focusing technique](/saft/), and with many channels it is [delay-and-sum beamforming](/delay-and-sum-beamforming/).

## Applications

- **Earth observation.** Maps of land, ice and sea in any weather and at night, from aircraft and satellites.
- **Interferometry.** Pairs of focused images give the height of terrain and its motion by [SAR interferometry](/sar-interferometry/); this needs images with an accurate phase, not only a sharp modulus.
- **Surveillance and reconnaissance.** Fine images of small areas in spotlight mode.
- **Planetary radar.** Mapping of cloud-covered planets.
- **Through-wall, ground penetrating and automotive radar.** Short ranges and curved paths, where backprojection is the usual method.

## References
