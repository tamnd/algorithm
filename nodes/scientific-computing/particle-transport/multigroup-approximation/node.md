---
tag: R6A42H
kind: technique
slug: multigroup-approximation
name: Multigroup energy approximation
aliases:
- multigroup method
area: scientific-computing/particle-transport
level: core
summary: "Divides the energy range into groups with averaged cross sections, which turns the transport equation into coupled one-group equations."
prereqs: [linear-boltzmann-transport-equation]
see_also: [k-eigenvalue-problem, source-iteration, gauss-seidel-method, power-iteration, discrete-ordinates-method, method-of-characteristics-transport, diffusion-approximation-of-transport, monte-carlo-criticality]
sources:
  - book: isbn:9780471092452
    title: E. E. Lewis and W. F. Miller, Jr., Computational Methods of Neutron Transport, Wiley, 1984
    locator: the derivation of the multigroup equations, the group constants and the outer and inner iterations (general locator)
  - book: isbn:9780471223634
    title: J. J. Duderstadt and L. J. Hamilton, Nuclear Reactor Analysis, Wiley, 1976
    locator: the chapters on multigroup diffusion theory and on the calculation of group constants (general locator)
---

The multigroup approximation removes the energy variable from the [transport equation](/linear-boltzmann-transport-equation/). It cuts the energy range into $G$ intervals, called groups, and replaces each cross section by an average over each group, weighted with an assumed shape of the flux in energy. The result is a set of $G$ one-speed transport equations, one per group, that are coupled only through their scattering and fission sources. Every one-speed method, such as the [discrete ordinates method](/discrete-ordinates-method/), the [method of characteristics](/method-of-characteristics-transport/) or [diffusion](/diffusion-approximation-of-transport/), then solves a group at a time. The averages are exact when the weight has the true shape of the flux in each group; in practice the weight comes from a simpler calculation, and the quality of the method is the quality of that weight.

## In plain words

Neutrons in a reactor have speeds that differ by a factor of many thousands, and the chance that a neutron hits a nucleus changes with its speed, sometimes very quickly. You cannot follow every speed. So you sort the neutrons into a few boxes by speed, from fast to slow, and treat all the neutrons in a box as if they had one speed.

Each box needs one number for each kind of collision. You get it by averaging over the speeds in the box, giving more weight to the speeds where there are more neutrons. If you knew the true mix of speeds, the boxes would give the right answer. You do not, so you guess it from a simpler problem.

Neutrons move from fast boxes to slow boxes when they collide, so you can solve the boxes in order, from fast to slow.

## When it applies

Use it whenever a deterministic transport or diffusion code has to treat energy: reactor core and lattice calculations, shielding, and radiation transport in general. It needs:

- cross sections as functions of energy, for example from an evaluated nuclear data library;
- a weight function in each group, which is a guess of the energy shape of the flux there;
- a solver for the one-speed equation with a given source.

It works best when the flux shape inside each group changes little in space and angle, so that one weight fits the whole problem. Monte Carlo codes can work with continuous energy instead, and some use multigroup data too.

## The template

**The continuous energy equation.** With isotropic scattering for simplicity, the angular flux $\psi(r, \Omega, E)$ of the [k-eigenvalue problem](/k-eigenvalue-problem/) satisfies
$$\Omega\cdot\nabla\psi + \Sigma_t(r, E)\,\psi = \frac{1}{4\pi}\int_0^\infty \Sigma_s(r, E' \to E)\,\phi(r, E')\,dE' + \frac{\chi(E)}{4\pi k}\int_0^\infty \nu\Sigma_f(r, E')\,\phi(r, E')\,dE',$$
with the scalar flux $\phi = \int\psi\,d\Omega$ and the fission spectrum $\chi$, which integrates to 1.

**Step 1: groups.** Choose energies $E_0 > E_1 > \cdots > E_G$ that cover the range. Group $g$ is $[E_g, E_{g-1}]$, so group 1 is the fastest. Define the group fluxes $\psi_g = \int_g \psi\,dE$ and $\phi_g = \int_g\phi\,dE$.

**Step 2: weights and group constants.** Choose a weight $w(E) > 0$ in each group and set
$$\Sigma_{t,g} = \frac{\int_g \Sigma_t w\,dE}{\int_g w\,dE}, \qquad \nu\Sigma_{f,g} = \frac{\int_g \nu\Sigma_f w\,dE}{\int_g w\,dE}, \qquad \chi_g = \int_g\chi\,dE,$$
$$\Sigma_{s,g' \to g} = \frac{\int_{g'}\int_g \Sigma_s(E' \to E)\,w(E')\,dE\,dE'}{\int_{g'} w\,dE'} .$$
In each region of the problem the weight can differ.

**Step 3: the multigroup equations.** Integrate the equation over group $g$ and replace each integral $\int_g \Sigma\,\psi\,dE$ by $\Sigma_g\psi_g$:
$$\Omega\cdot\nabla\psi_g + \Sigma_{t,g}\psi_g = \frac{1}{4\pi}\sum_{g'=1}^G \Sigma_{s,g' \to g}\phi_{g'} + \frac{\chi_g}{4\pi k}\sum_{g'=1}^G \nu\Sigma_{f,g'}\phi_{g'}, \qquad g = 1, \ldots, G .$$
This replacement is exact when $\psi(r, \Omega, E) = \psi_g(r, \Omega)\,w(E)/\int_g w\,dE$ in the group, that is, when the flux separates in energy inside each group and has the shape of the weight (a theorem, by putting this form into the integrals). Otherwise it is the approximation.

**Step 4: the iterations.** Solve the coupled system with two loops:

```
repeat                                          -- outer (fission) iteration
    F ← sum over g' of νΣf,g' φg'               -- fission source with the last fluxes
    for g = 1 to G:                             -- inner loop over groups, fast to slow
        S_g ← χg F / k + sum over g' ≠ g of Σs,g'→g φg'   -- the newest φg' that exist
        solve the one-speed problem of group g with the source S_g and the self scatter Σs,g→g
    if some groups have upscatter: repeat the loop over those groups until their fluxes settle
    update k and F as in power iteration
until k and the fission source settle
```

The group loop is a block [Gauss-Seidel method](/gauss-seidel-method/) over the groups. When there is only downscatter, $\Sigma_{s,g' \to g} = 0$ for $g' > g$, so the matrix of the group coupling is block lower triangular and one pass from fast to slow solves it exactly for a given fission source. The outer loop is a [power iteration](/power-iteration/) for $k$. Inside each group, the one-speed solve is for example [source iteration](/source-iteration/) with sweeps.

**What the collapse keeps.** By construction $\sum_g \Sigma_{s,g' \to g}$ is the weighted average of the total scattering cross section over group $g'$, and $\sum_g\chi_g = 1$. So the group constants keep the totals of scattering out of a group and of the fission spectrum, for any weight.

## Classic examples

**Collapsing an infinite medium.** In an infinite homogeneous medium the flux does not depend on $r$ or $\Omega$, so it separates in every group, and a collapse with the true fine group flux as the weight keeps $k_\infty$ exactly (a theorem, by Step 3). Take four fine groups with
- $\Sigma_t = (0.20, 0.35, 0.60, 1.20)\ \mathrm{cm}^{-1}$;
- the scattering from group 1 to groups 1, 2, 3: 0.10, 0.08, 0.005; from 2 to 2, 3: 0.25, 0.08; from 3 to 3, 4: 0.45, 0.10; and from 4 to 3, 4: 0.05, 1.00, which is an upscatter from group 4 to group 3;
- $\nu\Sigma_f = (0.008, 0.004, 0.03, 0.18)\ \mathrm{cm}^{-1}$ and $\chi = (0.7, 0.3, 0, 0)$.

The infinite medium equations $(\Sigma_t - \Sigma_s)\phi = \chi$ give the fine fluxes $\phi = (7, 8.6, 5.784, 2.892)$ and $k_\infty = \nu\Sigma_f\cdot\phi = 0.78448$. Collapse groups 1 and 2 into a fast group and groups 3 and 4 into a thermal group:

| weight | $\Sigma_t$ (fast, thermal) | $\Sigma_{s,1 \to 2}$ | $\nu\Sigma_f$ (fast, thermal) | $k_\infty$ |
|---|---|---|---|---|
| the true fine flux | 0.282692, 0.8 | 0.046346 | 0.0057949, 0.08 | 0.78448 |
| flat | 0.275, 0.9 | 0.0425 | 0.006, 0.105 | 0.84375 |

With the true fine flux, the two-group fluxes are $(15.6, 8.676)$, the sums of the fine fluxes, and $k_\infty$ is the same as with four groups. With a flat weight, $k_\infty$ is too large by 7.6%, because the flat weight gives too much weight to group 4, where $\nu\Sigma_f$ is large. The upscatter from group 4 to group 3 is now inside the thermal group, so the two-group problem has no upscatter.

**Resonance self-shielding.** Inside a resonance the flux dips where $\Sigma_t$ peaks. In the narrow resonance approximation the weight is $w(E) = 1/(E\,\Sigma_t(E))$, where $\Sigma_t$ includes the cross sections of the other nuclides in the mixture. Then $\Sigma_{t,g}$ is the harmonic mean of $\Sigma_t$ with the measure $dE/E$, which is at most the arithmetic mean that a smooth $1/E$ weight gives (a theorem, by the inequality of the arithmetic and harmonic means). If $\Sigma_t$ is 1 on half of the group in lethargy and 100 on the other half, the smooth weight gives 50.5 and the narrow resonance weight gives $2/1.01 = 1.980198$. Lattice codes compute such shielded group constants for every resonance absorber.

**Two-group diffusion for cores.** Core simulators for light water reactors often use two groups, fast and thermal, with group constants that a lattice code computes from a fine group transport calculation of each fuel assembly. As a rule of thumb, the boundary between the two groups is near 0.625 eV, and the lattice calculations use from tens to a few hundred groups.

**Group sweeps in shielding.** In shielding problems with fixed sources and only downscatter above the thermal range, the group loop of Step 4 runs once from fast to slow, and each group is a fixed source problem for [discrete ordinates](/discrete-ordinates-method/) or [characteristics](/method-of-characteristics-transport/).

## Variations

- **Spectrum from a cell or lattice calculation.** The weight is the fine group flux of a smaller transport calculation, a pin cell or an assembly, which is then collapsed to few groups for the whole core.
- **Leakage corrected spectra.** An infinite medium spectrum ignores leakage. Codes correct it with a critical buckling, for example by the $B_1$ equations, before the collapse.
- **Anisotropic scattering.** The scattering kernel is expanded in Legendre moments, and each moment gets its own group matrix. The transport correction folds the first moment into the total cross section of a reduced problem.
- **Angle dependent total cross section.** The exact group total for the angular flux depends on $\Omega$, since $\int_g\Sigma_t\psi\,dE/\psi_g$ differs from the scalar flux weighted value. Consistent $P_N$ group constants weight the higher moments of the total with the higher moments of the flux.
- **Superhomogenization and discontinuity factors.** When a region is homogenized as well as collapsed, correction factors make the coarse solution reproduce the reaction rates or the face currents of the fine reference.
- **Upscatter acceleration.** Thermal groups with upscatter need many passes of the group loop; codes accelerate them with a two-grid method on a collapsed one-group problem.

## Pitfalls

- **A weight that does not fit.** The method is only as good as the weight. Near interfaces, in reflectors and in strongly absorbing regions the spectrum differs from that of the calculation that gave the weight, and the group constants are biased there.
- **Resonances in wide groups.** Averaging a resonance cross section with a smooth weight overestimates the absorption, by the example above. Without self-shielding the result can be badly wrong.
- **Thermal upscatter.** Putting the group boundaries so that upscatter crosses many groups makes the group loop converge slowly. Count the upscatter iterations, and do not assume one pass from fast to slow is enough.
- **Group order in the code.** Some codes number groups from slow to fast. Check the order of $\chi$ and of the scattering matrix, $g' \to g$ against $g \to g'$, when you read data.
- **Balance of the collapsed data.** For a given weight, the total scattering out of a group and the sum of $\chi$ are kept, but the reaction rates are not kept unless the weight is the true flux. Check the collapsed $k$ against the fine calculation on the problem that gave the weight.
- **Negative group constants.** Higher Legendre moments of the group scattering and transport corrected self scatter can be negative, and some one-speed solvers then produce negative fluxes.

## Exercises

1. Show that if $\psi(r, \Omega, E) = \psi_g(r, \Omega)\,w(E)/\int_g w\,dE$ in every group, the multigroup equations of Step 3 hold exactly for the group fluxes.
2. For the four-group example, collapse with the weight $(1, 1, 0.3, 0.3)$ and explain why $k_\infty$ is the same as with the flat weight.
3. Show that with only downscatter the matrix of the multigroup equations for a fixed source is block lower triangular, and that one pass of the group loop from fast to slow solves it.
4. Show that in an infinite medium the fluxes of the collapsed problem, with the true fine flux as the weight, are the sums of the fine fluxes in each coarse group.
5. Prove that the narrow resonance weight gives a group total cross section that is at most the value of the smooth weight $1/E$, with equality only when $\Sigma_t$ is constant in the group.

## References
