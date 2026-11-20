---
tag: W3QYGV
kind: concept
slug: cycle-skipping
name: Cycle skipping
aliases:
- cycle-skipping
- local minima of waveform inversion
area: imaging-and-inverse-problems/seismic-imaging
level: advanced
summary: "The failure of waveform inversion when simulated and recorded events differ by more than half a period, so the misfit has a wrong local minimum."
prereqs: [full-waveform-inversion]
see_also: [full-waveform-inversion, adjoint-state-method, traveltime-tomography, cross-correlation, phase-unwrapping, gradient-descent, simulated-annealing, aliasing]
sources:
  - paper: doi:10.1190/1.1443880
    title: Carey Bunks, Fatimetou M. Saleck, S. Zaleski and Guy Chavent, Multiscale seismic waveform inversion, Geophysics 60(5), 1995, 1457 to 1473
    locator: the local minima of the waveform misfit and their reduction by inverting low frequencies first
  - paper: doi:10.1190/1.3238367
    title: Jean Virieux and Stephane Operto, An overview of full-waveform inversion in exploration geophysics, Geophysics 74(6), 2009, WCC1 to WCC26
    locator: the cycle-skipping condition of half a period and the strategies against it
  - paper: doi:10.4310/CMS.2014.v12.n5.a7
    title: Bjorn Engquist and Brittany D. Froese, Application of the Wasserstein metric to seismic signals, Communications in Mathematical Sciences 12(5), 2014, 979 to 988
    locator: a misfit based on optimal transport that is convex with respect to shifts of a signal
---

Cycle skipping is the main failure of [full-waveform inversion](/full-waveform-inversion/). FWI compares simulated and recorded seismograms sample by sample. If a simulated event arrives more than about half a period away from the recorded one, the least-squares misfit is lowered by matching it to the wrong cycle of the recorded wave, not by moving it to the right one. The misfit then has a local minimum at a wrong model, and a gradient method, which only sees the local slope, converges to it. For a single sinusoid shifted by $\tau$ the basin of the true model is exactly $|\tau| < T/2$ (a theorem). For real data the half-period rule is a heuristic estimate of the basin, and the remedies (low frequencies first, other misfits, better starting models) are heuristics too.

## In plain words

Imagine two copies of the same wavy line, one slid along the other. If the shift is small, sliding it back reduces the difference between them, and a simple downhill method finds the right position. But if the shift is close to one full wave, the peaks of one copy sit on the next peaks of the other, and the difference is already small. Sliding the copy further, onto the wrong peaks, makes the difference even smaller. A downhill method stops there, one wave off, and is happy. In waveform inversion this means a wrong model of the ground that fits the data well enough to look right.

## The idea

**One shifted sinusoid (theorem).** Let the recorded signal be $\cos(\omega t)$ and the simulated one $\cos(\omega(t - \tau))$. Over a whole number of periods, the misfit $\frac12\int(\cos\omega(t - \tau) - \cos\omega t)^2\,dt$ is proportional to $1 - \cos(\omega\tau)$. It is zero at $\tau = 0$ and at every multiple of the period $T = 2\pi/\omega$, and it has its maxima at $\tau = \pm T/2$. So a descent method in $\tau$ reaches $\tau = 0$ exactly when it starts with $|\tau| < T/2$.

**A shifted wavelet (theorem).** For a pulse $w$ of finite energy $E = \int w^2$, the misfit of a shift is $J(\tau) = E - C(\tau)$, where $C$ is the [autocorrelation](/autocorrelation/) of $w$. For the Ricker wavelet with the peak frequency $f_0$,
$$\frac{J(\tau)}{E} = 1 - \Big(1 - 4u + \tfrac43 u^2\Big)e^{-u}, \qquad u = \frac{(\pi f_0\tau)^2}{2}.$$
The basin around $\tau = 0$ ends at the maximum $\tau = 0.4315/f_0$, where $J/E = 1.618$, and the first false minimum is at $\tau = 0.9094/f_0$, where $J/E = 0.884$. The basin is a little less than half of the peak period $1/f_0$, and the false minimum is about one period away.

**Velocity errors make time shifts.** A velocity error changes the traveltime of every event, and the error grows with the distance travelled. A relative velocity error $\epsilon$ over the traveltime $t$ gives a shift of about $\epsilon t$. The half-period rule then asks for $\epsilon t < T/2$, so long paths, late arrivals and high frequencies need more accurate starting models (a heuristic estimate).

**Why the gradient cannot help.** The [adjoint-state method](/adjoint-state-method/) gives the exact gradient of the misfit, but the gradient is a local quantity. Once the starting model is outside the basin, every descent step goes toward the false minimum. Cycle skipping is a property of the misfit function, not of the method that minimizes it.

## Examples

**A 1D transmission test (measurement).** A source and a receiver are 550 m apart in a medium of 2000 m/s, and the source is a 15 Hz Ricker wavelet. For constant trial velocities, the least-squares misfit has a false local minimum at 1625 m/s ($J = 9132$) and another at 2525 m/s ($J = 11596$), with barriers at 1800 m/s ($J = 21831$) and 2225 m/s ($J = 24628$) between them and the true model, where $J = 0$. At 1625 m/s the predicted arrival is $550/1625 - 0.275 = 0.0635$ s late, about one period of 0.0667 s. The barriers are at the shifts 0.0306 s and 0.0278 s, close to the Ricker basin edge $0.4315/15 = 0.0288$ s.

**The half-period rule by hand.** With the same numbers, the rule $|550/v - 0.275| < 0.0333$ s accepts starting velocities between 1784 and 2275 m/s. A start at 1700 m/s is outside. On the grid of 25 m/s steps, the measured misfit rises from 9132 at 1625 m/s through 12593 at 1700 m/s to 21831 at 1800 m/s, so a descent from 1700 m/s goes down to the false minimum at 1625 m/s.

**Lower frequencies widen the basin (theorem for a pure shift).** At 5 Hz instead of 15 Hz, the Ricker basin edge moves to $0.4315/5 = 0.086$ s, three times wider, so a shift of 0.049 s, the one of a start at 1700 m/s, is inside it. This is why FWI starts with the lowest frequencies in the data.

## Where it is used

- **Full-waveform inversion.** Every FWI workflow checks for cycle skipping, for example by comparing predicted and recorded first arrivals, before it trusts an update.
- **Multiscale inversion.** Bunks et al. (1995) inverted low-pass filtered data first and added higher frequencies as the model improved.
- **Starting models.** [Traveltime tomography](/traveltime-tomography/) builds starting models whose traveltimes are accurate enough for the half-period rule.
- **Other misfits.** Misfits based on cross-correlation traveltimes, envelopes, or optimal transport (Engquist and Froese 2014) are convex or nearly convex with respect to time shifts, so their basins are wider.
- **Extended inversion.** Allowing the model to depend on a lag or on the shot lets the data be fitted far from the true model, and a penalty then moves the extended model back.
- **Related ambiguities.** The same $2\pi$ ambiguity appears in [phase unwrapping](/phase-unwrapping/), in carrier-phase positioning, and in [aliasing](/aliasing/) of sampled signals.

## References
