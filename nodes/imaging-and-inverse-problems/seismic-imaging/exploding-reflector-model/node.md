---
tag: S57EEX
kind: model
slug: exploding-reflector-model
name: Exploding reflector model
aliases:
- exploding reflector
- exploding reflector concept
area: imaging-and-inverse-problems/seismic-imaging
level: core
summary: "Model zero offset data as one-way waves from sources on all reflectors at time zero in a medium of half the velocity."
history:
  year: 1976
  people: [D. Loewenthal, L. Lu, R. Roberson, J. W. C. Sherwood]
  note: Loewenthal, Lu, Roberson and Sherwood introduced the exploding reflector model in 1976 to justify migration of stacked sections by the one-way wave equation in half the velocity.
prereqs: [wave-equation, seismic-reflection-model]
see_also: [seismic-migration, phase-shift-migration, stolt-migration, kirchhoff-migration, imaging-condition, common-midpoint-stacking, seismic-reflection-model, omega-k-algorithm]
sources:
  - paper: doi:10.1111/j.1365-2478.1976.tb00934.x
    title: D. Loewenthal, L. Lu, R. Roberson and J. W. C. Sherwood, The wave equation applied to migration, Geophysical Prospecting 24(2), 1976, 380 to 399
    locator: the exploding reflector model of the zero-offset section and the migration that follows from it
  - book: isbn:9780865423046
    title: Jon F. Claerbout, Imaging the Earth's Interior, Blackwell Scientific, 1985
    locator: the exploding reflector concept and its limits
  - book: isbn:9781560800941
    title: Oz Yilmaz, Seismic Data Analysis, Society of Exploration Geophysicists, 2001
    locator: Chapter 4 (migration), the exploding reflector model of a stacked section
  - paper: doi:10.1190/1.1440899
    title: Jeno Gazdag, Wave equation migration with the phase-shift method, Geophysics 43(7), 1978, 1342 to 1351
    locator: migration of zero-offset data by downward continuation in half the velocity
---

The exploding reflector model describes a zero-offset seismic section, one in which every trace has its source and its receiver at the same point. Instead of a wave that goes down from the source and comes back up, it imagines that every reflector explodes at time $t = 0$ with a strength equal to its reflection coefficient, and that the waves travel only up to the surface, in a medium where every velocity is halved, $v' = v/2$. A one-way trip at half the velocity takes exactly as long as the two-way trip at the full velocity, so the recorded times agree for primary reflections (a theorem of ray theory). The model turns migration of a zero-offset section into a one-way problem: continue the recorded field down into the earth and read it at $t = 0$, where it equals the reflectivity. It is a model of the data, and it is wrong for multiples, for amplitudes, and for some wave paths in strong lateral velocity changes.

## The machine

**Ingredients.** A velocity model $v(x, z)$ and a reflectivity $r(x, z)$, nonzero on the reflectors. The surface is $z = 0$, with depth $z$ positive down.

**The field.** The model field $p(x, z, t)$ solves the wave equation in half the velocity,
$$\frac{1}{v'(x, z)^2}\,\frac{\partial^2 p}{\partial t^2} = \Delta p, \qquad v' = \frac{v}{2},$$
with the initial state $p(x, z, 0) = r(x, z)$ (the explosion) and only waves that travel up. The zero-offset section is modeled as the field at the surface, $d(t, x) = p(x, 0, t)$ for $t \ge 0$.

**Imaging.** Migration inverts the model: given $d(t, x) = p(x, 0, t)$, find $p(x, z, t)$ at every depth by downward continuation of the one-way equation, and take the image
$$m(x, z) = p(x, z, 0).$$
This is the imaging condition of the exploding reflector: the image is the field at time zero.

**Plane waves in constant velocity.** A plane wave $e^{i(k_x x + k_z z - \omega t)}$ solves the model equation when $k_x^2 + k_z^2 = (\omega/v')^2 = (2\omega/v)^2$. With the transform $U(\omega) = \int u\,e^{-i\omega t}\,dt$, downward continuation by $\Delta z$ multiplies each component of the data by $e^{i k_z \Delta z}$ with $k_z = \operatorname{sgn}(\omega)\sqrt{\omega^2/v'^2 - k_x^2}$.

**A worked case.** A flat reflector at 600 m in the velocity 2000 m/s gives a zero-offset reflection at the two-way time $2 \cdot 600/2000 = 0.6$ s. In the model it explodes at $t = 0$ and its wave reaches the surface after $600/1000 = 0.6$ s, the same time. A point scatterer at $(x_0, z_0) = (0, 300)$ m appears on the trace at $x = 400$ m at the time $500/1000 = 0.5$ s, on the curve $t = (2/v)\sqrt{z_0^2 + (x - x_0)^2}$.

## What it counts

The model fixes what is unknown (the reflectivity $r$, given $v$) and what is seen (the zero-offset section $d$). Under the model the data are a linear function of $r$, and migration computes $r$ back as the field at $t = 0$. The cost of a migration method in the model is counted in the number of time samples $n_t$, traces $n_x$ and depth steps $n_z$, and the accuracy in how well it continues the one-way equation for each propagation angle.

## Relation to other models

- **[Seismic reflection model](/seismic-reflection-model/).** The 1D convolution model writes one trace as the reflectivity convolved with a wavelet. The exploding reflector model is its extension to 2D and 3D: for a flat earth and vertical waves it reduces to that model with time and depth related by $t = 2z/v$.
- **Born modeling.** The full linearized model has a source wave going down and a scattered wave going up, for any source and receiver positions. For zero offset, the down and up paths of a primary are the same normal-incidence ray, and Born modeling and the exploding reflector agree in their traveltimes. Their amplitudes differ: the spreading of a two-way path is not the spreading of a one-way path.
- **[Common midpoint stacking](/common-midpoint-stacking/).** A stacked section approximates a zero-offset section after normal moveout correction, which is why migration of stacked data uses this model.
- **Monostatic radar.** In synthetic aperture radar the transmitter and the receiver are at the same place, and the two-way path is modeled in the same way with the wavenumber $2\omega/c$. The [omega-k algorithm](/omega-k-algorithm/) of radar uses this factor of 2 exactly as Stolt migration does.

## Known results in the model

- **Equal times (theorem in ray theory).** For a primary reflection recorded at zero offset, the ray from the source to the reflector and back is one ray traversed twice, and it meets the reflector at normal incidence. Its two-way time at $v$ equals its one-way time at $v/2$.
- **Exact migration for $v(z)$ (theorem).** [Phase-shift migration](/phase-shift-migration/) continues the model field exactly when the velocity depends only on depth, so it recovers $p(x, z, 0)$ within the recorded band.
- **Exact migration in constant velocity (theorem).** [Stolt migration](/stolt-migration/) maps the data spectrum to the image spectrum with $k_z = \sqrt{(2\omega/v)^2 - k_x^2}$, exactly up to the interpolation.
- **Ray approximation (theorem in the high-frequency limit).** [Kirchhoff migration](/kirchhoff-migration/) sums the data along the curves $t = (2/v)\sqrt{z^2 + (x - x_r)^2}$ with weights; it agrees with the exact one-way image as the frequency grows.
- **The dip relation (theorem for constant velocity).** A plane reflector with the dip $\alpha$ appears on the depth-scaled section with $\tan\alpha_{\text{section}} = \sin\alpha$, so migration must steepen dips; see [seismic migration](/seismic-migration/).
- **Failures (heuristic statements).** The model has no multiples, no waves that go down after the explosion, and no correct amplitudes. In strong lateral velocity changes, waves from one reflector can reach a surface point along several paths, some of which are not zero-offset primaries; migration then puts energy in false places. Prestack migration with the [imaging condition](/imaging-condition/) avoids these limits.

## References
