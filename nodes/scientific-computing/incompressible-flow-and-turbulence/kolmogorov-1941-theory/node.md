---
tag: FAKD6B
kind: concept
slug: kolmogorov-1941-theory
name: Kolmogorov 1941 theory of turbulence
aliases:
- K41 theory
- Kolmogorov five-thirds law
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: "Predicts an inertial range energy spectrum C eps^(2/3) k^(-5/3) and smallest eddies of size (nu^3/eps)^(1/4), which set the cost of resolving turbulence."
model: real-ram
history:
  year: 1941
  people: [Andrey Kolmogorov, Lewis Fry Richardson, Alexander Obukhov]
  note: Richardson described the energy cascade in 1922. Kolmogorov stated the similarity hypotheses and derived the four-fifths law in 1941, and Obukhov gave the spectral form the same year. Kolmogorov refined the theory for intermittency in 1962.
prereqs: [navier-stokes-equations]
see_also: [direct-numerical-simulation, large-eddy-simulation, smagorinsky-model, reynolds-averaged-navier-stokes, k-epsilon-model, spectral-methods, navier-stokes-equations]
sources:
  - paper: doi:10.1098/rspa.1991.0075
    title: A. N. Kolmogorov, The local structure of turbulence in incompressible viscous fluid for very large Reynolds numbers, Proceedings of the Royal Society of London A 434, 1991, 9-13 (English translation of Doklady Akademii Nauk SSSR 30, 1941)
    locator: the hypothesis of local isotropy, the two similarity hypotheses and the two-thirds law for the second-order structure function
  - paper: doi:10.1098/rspa.1991.0076
    title: A. N. Kolmogorov, Dissipation of energy in the locally isotropic turbulence, Proceedings of the Royal Society of London A 434, 1991, 15-17 (English translation of Doklady Akademii Nauk SSSR 32, 1941)
    locator: the four-fifths law for the third-order structure function, derived from the Karman-Howarth equation
  - book: isbn:9780521598866
    title: Stephen B. Pope, Turbulent Flows, Cambridge University Press, 2000
    locator: Section 6.1 (6.1.2 the Kolmogorov hypotheses, 6.1.3 the energy spectrum), Section 6.2 (structure functions), Section 6.5 (6.5.2 Kolmogorov spectra, 6.5.5 the inertial subrange) and Section 6.7.4 (refined similarity hypotheses)
  - book: isbn:9780521457132
    title: Uriel Frisch, Turbulence, The Legacy of A. N. Kolmogorov, Cambridge University Press, 1995
    locator: Chapter 6 (the four-fifths law) and Chapter 7 (the 1941 phenomenology), with Chapter 8 on intermittency
  - paper: doi:10.1017/S002211206200018X
    title: H. L. Grant, R. W. Stewart and A. Moilliet, Turbulence spectra from a tidal channel, Journal of Fluid Mechanics 12(2), 1962, 241-268
    locator: the first clear measurement of a k^(-5/3) range, at very high Reynolds number
  - paper: doi:10.1063/1.868656
    title: Katepalli R. Sreenivasan, On the universality of the Kolmogorov constant, Physics of Fluids 7(11), 1995, 2778-2784
    locator: the collection of measured values of the spectrum constant
---

The Kolmogorov 1941 theory (K41) is a statistical theory of the small scales of turbulence at high Reynolds number, built on three hypotheses about how energy passes from large eddies to small ones. It predicts that the small scales depend only on the [kinematic viscosity](/navier-stokes-equations/) $\nu$ and the mean dissipation rate $\varepsilon$, which gives the smallest eddy size $\eta = (\nu^3/\varepsilon)^{1/4}$ and the $k^{-5/3}$ energy spectrum. Its one exact result is the four-fifths law for the third-order structure function; the spectrum and its constant are predictions that measurements confirm to within small intermittency corrections. The theory gives the scales that [direct numerical simulation](/direct-numerical-simulation/) must resolve and that [large eddy simulation](/large-eddy-simulation/) with the [Smagorinsky model](/smagorinsky-model/) or the [dynamic subgrid model](/dynamic-subgrid-model/) models instead.

## In plain words

A stirred fluid holds eddies of many sizes. The largest eddies take energy from the stirring. They break up into smaller eddies, which break up again, and the energy passes down this chain of sizes with almost no loss. Only at the smallest sizes does the stickiness of the fluid turn the motion into heat. Kolmogorov guessed that the small eddies forget the shape and direction of the large ones. Then they can depend only on two things: how sticky the fluid is, and how fast energy arrives from above. From these two things alone he found the size of the smallest eddies and how the energy shares out over the middle sizes. These are guesses tested by experiment, and they agree well. One result about the middle sizes follows from the flow equations without any guess beyond the symmetry.

## The idea

**Setting.** Take statistically homogeneous turbulence governed by the incompressible [Navier-Stokes equations](/navier-stokes-equations/), with velocity $u$, kinematic viscosity $\nu$ in m^2/s, large-eddy size $L$ and velocity $U$, and Reynolds number $Re = UL/\nu$. Let $\varepsilon$ (m^2/s^3) be the mean rate of dissipation of kinetic energy per unit mass. The velocity increment over a separation $r$ in the direction $\hat r$ is $\delta u(r) = (u(x + r\hat r) - u(x)) \cdot \hat r$, and the structure function of order $p$ is $S_p(r) = \langle \delta u(r)^p \rangle$.

**The hypotheses.** In Pope's form (Section 6.1.2), with a length $\ell_{EI}$ well below $L$:

1. **Local isotropy.** At high Reynolds number, the small-scale motions ($\ell \ll \ell_{EI}$) are statistically isotropic.
2. **First similarity hypothesis.** The statistics of the small-scale motions have a universal form that depends only on $\nu$ and $\varepsilon$.
3. **Second similarity hypothesis.** In the inertial subrange $\eta \ll \ell \ll L$, the statistics depend only on $\varepsilon$, not on $\nu$.

These are hypotheses. Nothing in the Navier-Stokes equations forces them, and the 1962 refinement (Pope 6.7.4) changes the second one to allow for the spatial variation of the dissipation (intermittency).

**Kolmogorov scales (consequence of hypothesis 2).** The only length, time and velocity that can be made from $\nu$ and $\varepsilon$ are
$$\eta = \left(\frac{\nu^3}{\varepsilon}\right)^{1/4}, \qquad \tau_\eta = \left(\frac{\nu}{\varepsilon}\right)^{1/2}, \qquad v_\eta = (\nu\varepsilon)^{1/4}.$$
The Reynolds number made from them is $\eta v_\eta / \nu = 1$, which says that these are the eddies where viscosity is as strong as inertia.

**Scale separation (heuristic plus measurement).** Taylor's estimate $\varepsilon \approx U^3/L$ is a rule of thumb: measurements show that $\varepsilon L / U^3$ tends to a constant of order one at high $Re$, but the constant depends on the flow. With it,
$$\frac{L}{\eta} \sim Re^{3/4}, \qquad \frac{T}{\tau_\eta} \sim Re^{1/2}, \qquad \frac{U}{v_\eta} \sim Re^{1/4},$$
where $T = L/U$. A grid that resolves $\eta$ in a cube of side $L$ needs about $Re^{9/4}$ points.

**The four-fifths law (theorem, under stated assumptions).** For homogeneous isotropic turbulence, in the limit of infinite Reynolds number and for $r$ in the inertial range,
$$S_3(r) = -\frac{4}{5}\,\varepsilon\, r.$$
Kolmogorov derived it from the Karman-Howarth equation, which follows from the Navier-Stokes equations; the only extra inputs are isotropy and the limit $\nu \to 0$ with $\varepsilon$ fixed. It contains no fitted constant, and it says that energy flows on average from large scales to small ones (the negative sign). It is the one exact nontrivial result of the theory.

**The two-thirds law and the five-thirds spectrum (predictions).** Hypothesis 3 and dimensional reasoning give, in the inertial range,
$$S_2(r) = C_2\,(\varepsilon r)^{2/3}, \qquad E(k) = C\,\varepsilon^{2/3} k^{-5/3},$$
where $E(k)$ is the energy spectrum at wavenumber $k$ (1/m). The exponents follow from the hypotheses. The constants do not: $C_2$ and $C$ are measured. The data collected by Sreenivasan put the Kolmogorov constant at $C \approx 1.5$, and the two constants are tied by the exact relation $C_2 = \frac{27}{55}\Gamma(1/3)\, C \approx 1.315\, C$, which gives $C_2 \approx 2.0$.

**Higher orders (measurement against prediction).** The hypotheses predict $S_p \propto (\varepsilon r)^{p/3}$ for every $p$. Measurements and simulations show exponents below $p/3$ for $p > 3$, and the gap grows with $p$. For $p = 2$ the correction to the exponent is a few hundredths, so the $-5/3$ spectrum is a good working law; for $p = 3$ the four-fifths law has no correction.

## Examples

**Kolmogorov scale in air.** Take air with $\nu = 1.5 \times 10^{-5}$ m^2/s and a dissipation rate $\varepsilon = 1$ m^2/s^3. Then $\nu^3 = 3.375 \times 10^{-15}$, its square root is $5.81 \times 10^{-8}$, and the square root of that is
$$\eta = 2.41 \times 10^{-4}\ \text{m}, \qquad \tau_\eta = \sqrt{1.5 \times 10^{-5}} = 3.87 \times 10^{-3}\ \text{s}, \qquad v_\eta = (1.5 \times 10^{-5})^{1/4} = 0.0622\ \text{m/s}.$$
Check: $\eta v_\eta / \nu = 2.41 \times 10^{-4} \times 0.0622 / 1.5 \times 10^{-5} = 1.00$.

**Scale range.** With $U = 1$ m/s and $L = 1$ m in the same air, $Re = 66\,667$. If $\varepsilon = U^3/L = 1$ m^2/s^3, then $L/\eta = 4149$, and $Re^{3/4} = 66\,667^{0.75} = 4149$ too: with the constant set to one, the two agree exactly.

**Four-fifths law.** With $\varepsilon = 1$ m^2/s^3 and $r = 0.01$ m (inside the range $\eta \ll r \ll L$ above), $S_3 = -0.8 \times 1 \times 0.01 = -0.008$ m^3/s^3. Doubling $r$ doubles $S_3$.

**Spectrum slope.** In the inertial range, doubling $k$ divides $E(k)$ by $2^{5/3} = 3.17$. The energy in a band from $k$ to $2k$ is $\int_k^{2k} E\,dk = \frac{3}{2} C \varepsilon^{2/3} k^{-2/3}(1 - 2^{-2/3})$, so each octave toward smaller eddies holds $2^{-2/3} = 0.63$ of the energy of the octave before it.

## Where it is used

- **Grid size for simulation.** The scale $\eta$ and the estimate $L/\eta \sim Re^{3/4}$ give the resolution and cost of [direct numerical simulation](/direct-numerical-simulation/), and with it the reason why direct simulation of engineering flows is out of reach.
- **Subgrid models.** [Large eddy simulation](/large-eddy-simulation/) puts the filter in the inertial range, where the hypotheses say the small scales are universal. Lilly used the $-5/3$ spectrum to fix the constant of the [Smagorinsky model](/smagorinsky-model/), and the [dynamic subgrid model](/dynamic-subgrid-model/) uses scale similarity in the same range.
- **RANS closures.** The dissipation rate $\varepsilon$ is the transport variable of the [k-epsilon model](/k-epsilon-model/), and the eddy viscosity $k^2/\varepsilon$ is the only viscosity that can be made from $k$ and $\varepsilon$. The decay of grid turbulence fixes one of its constants.
- **Code checks.** A [spectral method](/spectral-methods/) code for isotropic turbulence is checked by its spectrum: a range near $k^{-5/3}$, a fall-off near $k\eta \approx 1$, and a dissipation that matches the energy input.
- **Geophysics and optics.** Measurements of ocean and atmospheric turbulence, and the models of the blurring of starlight by the air, use the $k^{-5/3}$ spectrum and its temperature analog.

## References
