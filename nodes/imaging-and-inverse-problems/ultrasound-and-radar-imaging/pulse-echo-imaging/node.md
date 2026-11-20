---
tag: P1KXZX
kind: model
slug: pulse-echo-imaging
name: Pulse-echo imaging model
aliases:
- pulse-echo model
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: intro
summary: "Model the received echoes as the transmitted pulse convolved with the scatterer reflectivity, each echo delayed by its round trip time. The map from reflectivity to data is linear."
prereqs: [discrete-convolution, point-spread-function]
see_also: [delay-and-sum-beamforming, b-mode-image-formation, speckle, synthetic-aperture-radar, matched-filter, impulse-response, linear-time-invariant-system, wave-equation]
sources:
  - paper: doi:10.1121/1.400497
    title: "Jorgen Arendt Jensen, A model for the propagation and scattering of ultrasound in tissue, Journal of the Acoustical Society of America 89(1), 1991, 182 to 190"
    locator: "the pulse-echo signal as a convolution of the excitation, the transmit and receive spatial impulse responses and the scattering term (general locator)"
  - book: isbn:9780123964878
    title: "Thomas L. Szabo, Diagnostic Ultrasound Imaging: Inside Out, 2nd edition, Academic Press, 2014"
    locator: "Chapter 8, Wave scattering and imaging; Chapter 4, Attenuation"
---

The pulse-echo imaging model describes what an ultrasound or radar system records. A transducer sends a short pulse into a medium. Each small scatterer reflects a weak copy of the pulse back, and the copy arrives after the time the sound needs to go to the scatterer and back. The recorded signal is the sum of all these delayed copies. For one transducer looking straight down, the echo from depth $z$ arrives at $t = 2z/c$ for the speed of sound $c$, and the recorded line is the pulse convolved with the reflectivity along the line, in the depth coordinate $z = c t/2$. For an array, each transmit and receive pair has its own delay, the sum of the two path lengths over $c$. In both cases the data are a linear function of the reflectivity. Every image formation method on the pages of this area, from [delay-and-sum](/delay-and-sum-beamforming/) to the [total focusing method](/total-focusing-method/), inverts or approximates the adjoint of this map. The model ignores multiple scattering and changes of the speed of sound, which are the main sources of error in practice.

## The machine

The medium has a constant speed of sound $c$ and a reflectivity $f(q)$ at the points $q$. In the simplest form it is a sum of point scatterers, $f = \sum_k a_k \delta_{q_k}$, with complex amplitudes $a_k$. An array has elements at the positions $e_1, \ldots, e_M$. Element $i$ transmits the pulse $p(t) = g(t) \cos(2\pi f_0 t)$, with a short envelope $g$ and a center frequency $f_0$. Element $j$ records

$$r_{ij}(t) = \sum_k a_k\, p\!\left(t - \frac{|q_k - e_i| + |q_k - e_j|}{c}\right) + n_{ij}(t),$$

with noise $n_{ij}$. This is the forward map of the model: reflectivity in, traces out. It assumes single scattering (each echo is reflected once, the Born approximation), point-like elements without directivity, and no spreading loss or attenuation; those add a known weight to each term.

**The one-dimensional case.** For one transducer at the origin and scatterers on the line below it, $|q_k - e| = z_k$, and

$$r(t) = \sum_k a_k\, p(t - 2 z_k / c) = (p * f_t)(t), \qquad f_t(t) = \sum_k a_k\, \delta(t - 2 z_k/c),$$

a convolution of the pulse with the reflectivity mapped to time by $t = 2z/c$. Sampled at the rate $f_s$, it becomes a [discrete convolution](/discrete-convolution/).

**The general case.** Jensen (1991) writes the received pressure as a convolution in time and space of the excitation, the transmit and receive [impulse responses](/impulse-response/) of the transducer apertures, and a scattering term from the density and speed of sound perturbations. Point elements and point scatterers give the formula above.

**Complex baseband.** Systems often store the analytic signal of each trace, mixed down by $e^{-i 2\pi f_0 t}$ and low-pass filtered. The trace becomes $b_{ij}(t) = \sum_k a_k\, g(t - \tau_{ijk})\, e^{-i 2\pi f_0 \tau_{ijk}}$, with the delay $\tau_{ijk}$ in a phase factor; the image formation pages of this area use this form.

## What it counts

The model fixes what a method may assume and what it costs to measure.

- **Data.** Each firing gives up to $M$ traces of $T$ samples. Full matrix capture, one firing per element, gives $M^2 T$ samples; one plane wave gives $M T$.
- **Time.** One firing must wait for the echo from the deepest point: $2 z_{\max}/c$. This bounds the number of firings per second, and so the frame rate.
- **Operations.** Image formation methods are counted by the samples they read per pixel: $M$ for [delay-and-sum](/delay-and-sum-beamforming/) of one firing, $M^2$ for [TFM](/total-focusing-method/), $N M$ for [plane-wave compounding](/plane-wave-compounding/).
- **Quality.** The image of one point scatterer is the [point-spread function](/point-spread-function/) of the method. Its width along depth is the axial resolution and its width across the beam is the lateral resolution.

## Relation to other models

- **Wave equation.** The model is the single-scattering approximation of the [wave equation](/wave-equation/) with a small perturbation of the medium, at frequencies where the pulse can be treated as a ray with a delay.
- **Linear systems.** For fixed geometry, the map from $f$ to $r$ is linear, and in the one-dimensional case also shift invariant: a [linear time-invariant system](/linear-time-invariant-system/) whose impulse response is the pulse.
- **Radar.** [Synthetic aperture radar](/synthetic-aperture-radar/) uses the same model for electromagnetic waves, with a moving antenna and the stop-and-go approximation; [SAR back-projection](/sar-backprojection/) is the adjoint of its forward map.
- **Seismic reflection.** Kirchhoff migration in geophysics sums along the same travel time curves; see [Kirchhoff migration](/kirchhoff-migration/).
- **Photoacoustics.** In [photoacoustic tomography](/photoacoustic-tomography/) the sources are in the medium, so the delay is one way, $|q - e_j|/c$.

## Known results in the model

- **Depth from time** (theorem in the model). An echo from depth $z$ below a transducer arrives at $2z/c$. With $c = 1.54$ mm/us, the convention for soft tissue (1540 m/s), the echo from 6 mm arrives at $7.7922$ us. The wavelength at 5 MHz is $c/f_0 = 0.308$ mm.
- **Axial resolution** (theorem for a Gaussian envelope). The envelope $g(t) = e^{-t^2/(2\sigma_t^2)}$ has a full width at half maximum of $2\sqrt{2 \ln 2}\, \sigma_t$, which is $\sqrt{2 \ln 2}\, c\, \sigma_t$ in depth. For $\sigma_t = 0.1$ us this is $0.1813$ mm. Two scatterers much closer than the pulse length in depth merge.
- **Lateral resolution** (heuristic). A focused aperture of width $D$ at depth $z$ has a lateral width of about $\lambda z / D = \lambda F$ for the f-number $F = z/D$, from the Fraunhofer approximation; see the [Rayleigh criterion](/rayleigh-criterion/). The constant in front depends on the definition of width and on the apodization.
- **The adjoint is delay-and-sum** (theorem). The adjoint of the forward map spreads each trace back along its travel time curve. For point-like elements it is the sum over pairs at the time $(|q - e_i| + |q - e_j|)/c$, which is [delay-and-sum](/delay-and-sum-beamforming/) and [TFM](/total-focusing-method/). The pages of these methods prove it for their own sampling.
- **Matched filtering** (theorem). For a known pulse in white noise, correlating each trace with the pulse maximizes the signal-to-noise ratio at the echo time; see [matched filter](/matched-filter/) and [pulse compression](/pulse-compression/) for long coded pulses.
- **Frame rate bound** (theorem in the model). With one firing per round trip, a depth of 60 mm allows a firing every $77.92$ us, so 128 focused lines take $9.97$ ms, about 100 frames per second.
- **Speckle** (theorem for the random phasor model). Many unresolved scatterers in one resolution cell add with random phases, and the envelope follows a Rayleigh distribution; see [speckle](/speckle/).
- **Attenuation** (measurement). Soft tissue attenuates the pulse, roughly in proportion to the frequency (Szabo, Chapter 4); a gain that grows with depth compensates for it in [B-mode image formation](/b-mode-image-formation/).

## References
