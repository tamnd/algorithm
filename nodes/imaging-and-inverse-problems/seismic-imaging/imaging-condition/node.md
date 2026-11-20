---
tag: MVZ7EX
kind: definition
slug: imaging-condition
name: Imaging condition
aliases:
- Claerbout imaging principle
- cross-correlation imaging condition
- imaging principle
area: imaging-and-inverse-problems/seismic-imaging
level: core
summary: "A reflector exists where the downgoing source wavefield and the upgoing receiver wavefield coincide in time, as found by their zero lag cross-correlation."
prereqs: [wave-equation, cross-correlation]
see_also: [reverse-time-migration, exploding-reflector-model, seismic-migration, cross-correlation, adjoint-state-method, least-squares-migration, seismic-interferometry, matched-filter]
sources:
  - paper: doi:10.1190/1.1440185
    title: Jon F. Claerbout, Toward a unified theory of reflector mapping, Geophysics 36(3), 1971, 467 to 481
    locator: the principle that reflectors exist where the first arrival of the downgoing wave coincides in time with the upgoing wave
  - paper: doi:10.1190/1.1441434
    title: Edip Baysal, Dan D. Kosloff and John W. C. Sherwood, Reverse time migration, Geophysics 48(11), 1983, 1514 to 1524
    locator: the imaging condition at time zero for the exploding reflector model in reverse-time migration
  - paper: doi:10.1190/1.1441754
    title: Albert Tarantola, Inversion of seismic reflection data in the acoustic approximation, Geophysics 49(8), 1984, 1259 to 1266
    locator: the zero-lag correlation of the forward field and the back-propagated residuals as the gradient of the least-squares misfit
  - book: isbn:9780865423046
    title: Jon F. Claerbout, Imaging the Earth's Interior, Blackwell Scientific, 1985
    locator: the imaging principle for shot profiles and its ratio and correlation forms
---

An imaging condition is the rule that turns two wavefields into an image of the reflectors. Claerbout (1971) stated the principle: reflectors exist at points where the downgoing wave from the source and the upgoing reflected wave coincide in time. The source wavefield $S$ is simulated forward in time from the source; the receiver wavefield $R$ is the recorded data propagated back into the earth. The cross-correlation imaging condition measures the coincidence by the zero-lag correlation of $S$ and $R$ at every point, summed over shots. It is what makes [reverse-time migration](/reverse-time-migration/) and shot-profile migration produce an image, and with the right weights it is the adjoint of Born modeling (a theorem).

## Definition

Let a shot $s$ have the source wavefield $S(x, t; s)$, the field of the source in the background velocity, and the receiver wavefield $R(x, t; s)$, the recorded data injected at the receivers and propagated backward in time. The **cross-correlation imaging condition** is

$$I(x) = \sum_s \int S(x, t; s)\, R(x, t; s)\, dt.$$

At a reflector the source wave arrives at some time $t_0$, and the reflected wave, run backward, is at the same point at the same time $t_0$, so the product has a large sum. Away from reflectors the two fields pass the point at different times and the product sums to little. In the frequency domain, with $U(\omega) = \int u\,e^{-i\omega t}\,dt$, Parseval's identity gives $I(x) = \frac{1}{2\pi}\sum_s\int S(x, \omega; s)\,\overline{R(x, \omega; s)}\,d\omega$.

**Other forms.**

- **Ratio (deconvolution) form.** Claerbout's reflection coefficient is $R/S$ at the time when the source wave arrives, or $\sum_\omega \overline{S}R/(\overline{S}S + \varepsilon)$ in the frequency domain. It corrects for the strength of the source wave, at the price of instability where $S$ is weak.
- **Excitation-time form.** Read $R$ only at the arrival time $t_0(x)$ of the source wave, $I(x) = R(x, t_0(x))$.
- **Exploding reflector form.** For zero-offset data in the [exploding reflector model](/exploding-reflector-model/), the source field is the explosion at $t = 0$, and the image is $R(x, 0)$, the receiver field at time zero.
- **Extended forms.** Correlate with a subsurface offset $h$ or a time lag $\tau$, $I(x, h, \tau) = \sum_s\int S(x - h, t - \tau)\,R(x + h, t + \tau)\,dt$. At the right velocity the energy focuses at $h = 0$, $\tau = 0$; a wrong velocity spreads it, which is used for velocity analysis.

**Adjoint of Born modeling (theorem).** Let $\delta d = L\,\delta m$ be Born modeling for the equation $m\,u_{tt} - \Delta u = f$. Then $L^{\mathsf T}r = -\sum_s\int \partial_t^2 S(x, t; s)\,R(x, t; s)\,dt$, where $R$ solves the adjoint (time-reversed) equation with the residual $r$ as its source. So the cross-correlation imaging condition with $\partial_t^2 S$ in place of $S$ is the adjoint of Born modeling; for a band-limited source the two differ by a filter of $-\omega^2$. This is the discrete statement proved on the [reverse-time migration](/reverse-time-migration/) page.

## Examples and non-examples

Examples:

- **A flat reflector in 1D.** Take $v = 2000$ m/s, a source and a receiver at the surface, and a reflector at 600 m. The source wave reaches 600 m at 0.3 s. The reflection is recorded at 0.6 s; propagated backward, it is at depth $z$ at the time $0.6 - z/2000$, which is 0.3 s at 600 m. Both fields are at 600 m at 0.3 s, so the product is large there. At 400 m the source wave passes at 0.2 s and the back-propagated reflection at 0.4 s; for a short wavelet the product is zero, and so is the image.
- **One shot in RTM.** In the test of [reverse-time migration](/reverse-time-migration/), the correlation of $\partial_t^2 S$ with the back-propagated Born data of one scatterer peaks at the scatterer, with the sign of the perturbation.
- **Zero-offset migration.** [Phase-shift migration](/phase-shift-migration/) and [Stolt migration](/stolt-migration/) continue the data downward and keep the field at $t = 0$, the exploding reflector form.
- **The gradient of waveform inversion.** In [full-waveform inversion](/full-waveform-inversion/), the same correlation with the back-propagated residuals is the gradient of the misfit, computed by the [adjoint-state method](/adjoint-state-method/).

Non-examples:

- **The sum $S + R$.** Adding the two fields at a fixed time does not measure coincidence; it shows both waves wherever they are.
- **The receiver field alone.** In prestack migration, $R(x, t)$ at any single time is not an image, because the reflection time depends on the source position; the source field supplies the time.
- **A correlation with a wrong velocity.** With a wrong background velocity, $S$ and $R$ still correlate, but at a shifted point or at a nonzero lag. The image is defocused, which is a result of the wrong model, not of the condition.
- **Correlation with the full data.** Correlating the recorded traces with each other, without propagation, is [seismic interferometry](/seismic-interferometry/): it builds new virtual-source data, not an image.

## Related definitions

- [Cross-correlation](/cross-correlation/): the imaging condition is a zero-lag cross-correlation in time at every point of space.
- [Matched filter](/matched-filter/): the correlation with the predicted source wave is the matched filter for its arrival, which explains why it is the best linear detector in white noise (a heuristic link for the imaging setting).
- [Exploding reflector model](/exploding-reflector-model/): the special case with the source field at $t = 0$.
- [Seismic migration](/seismic-migration/): the problem whose solutions use an imaging condition.
- [Adjoint-state method](/adjoint-state-method/): the general rule behind the correlation of a forward and a backward field.
- [Least-squares migration](/least-squares-migration/): uses the adjoint form inside conjugate gradients to correct amplitudes.

## References
