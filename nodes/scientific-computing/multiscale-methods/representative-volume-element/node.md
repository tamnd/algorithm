---
tag: 8MM4BA
kind: definition
slug: representative-volume-element
name: Representative volume element
aliases:
- RVE
area: scientific-computing/multiscale-methods
level: core
summary: The smallest material sample whose averaged response represents the bulk, used to compute effective properties.
prereqs: [periodic-homogenization]
see_also: [fe2-method, two-scale-convergence, heterogeneous-multiscale-method, multiscale-modeling, central-limit-theorem, law-of-large-numbers, finite-element-method]
sources:
  - paper: doi:10.1016/0022-5096(63)90036-X
    title: R. Hill, Elastic properties of reinforced solids, some theoretical principles, Journal of the Mechanics and Physics of Solids 11(5), 1963, 357-372
    locator: the definition of the representative volume, the averages of stress and strain under uniform boundary data, and the energy identity now called the Hill-Mandel condition
  - paper: doi:10.1016/S0020-7683(03)00143-4
    title: T. Kanit, S. Forest, I. Galliet, V. Mounoury and D. Jeulin, Determination of the size of the representative volume element for random composites, statistical and numerical approach, International Journal of Solids and Structures 40(13-14), 2003, 3647-3679
    locator: the statistical definition of the RVE size from the variance of the apparent property over realizations, and the effect of the boundary conditions
  - book: isbn:9781107096547
    title: Weinan E, Principles of Multiscale Modeling, Cambridge University Press, 2011
    locator: Chapter 2 (homogenization, random media) and Chapter 6 (capturing the macroscale behavior)
---

A representative volume element (RVE) is a sample of a heterogeneous material that is large enough for its averaged response to be the response of the bulk, within a stated tolerance, and as small as possible otherwise. Hill (1963) asked that it be typical of the whole material on average and that it hold enough inclusions for the computed overall moduli not to depend on the surface data, as long as those data are macroscopically uniform. An RVE is the micro problem of computational homogenization, for example in the [FE2 method](/fe2-method/). For a periodic material, one period with periodic boundary conditions is an exact RVE; for a random material the RVE size is a matter of statistics and must be measured.

## Definition

Let a material occupy a large region, with a stiffness tensor $C(x)$ that is a statistically homogeneous random field (or a periodic one). For a sample $V$ of size $L$ and a macroscopic strain $E$, solve the equilibrium problem $\nabla \cdot \sigma = 0$, $\sigma = C(x) : \varepsilon(u)$ in $V$, with one of these boundary conditions:

- KUBC (kinematic uniform): $u = E \cdot x$ on $\partial V$;
- SUBC (static uniform): $\sigma n = \Sigma \cdot n$ on $\partial V$, for a given macroscopic stress $\Sigma$;
- PBC (periodic): $u - E \cdot x$ periodic on $\partial V$, with antiperiodic tractions.

Write $\langle \cdot \rangle = |V|^{-1} \int_V \cdot\, dx$. The *apparent tensor* $C^{\mathrm{app}}_V$ is defined by $\langle \sigma \rangle = C^{\mathrm{app}}_V : \langle \varepsilon \rangle$; it depends on $V$, on the boundary condition and, for a random medium, on the realization.

**Definition.** For a tolerance $\delta > 0$, a volume $V$ is an RVE of the property $Z$ (a component or an invariant of $C^{\mathrm{app}}$) if the apparent values $Z_V$ agree with the effective value $Z^{\mathrm{eff}}$ within $\delta$: deterministically, if all admissible boundary conditions give values within $\delta$ of each other; statistically, in the sense of Kanit et al. (2003), if $n$ independent realizations of size $V$ give a mean with relative error

$$\varepsilon_{\mathrm{rel}} = \frac{2\, D_Z(V)}{\bar Z \sqrt n} \le \delta,$$

where $D_Z(V)$ is the standard deviation of $Z_V$ over realizations and $\bar Z$ its mean. The factor 2 is a confidence level of about 95% by the [central limit theorem](/central-limit-theorem/). The RVE size thus depends on the property, the contrast of the phases, the tolerance and the number of realizations that one can afford.

**The Hill-Mandel condition.** The average stress and strain of an RVE must satisfy

$$\langle \sigma : \varepsilon \rangle = \langle \sigma \rangle : \langle \varepsilon \rangle,$$

so that the macroscopic work $\Sigma : E$ equals the mean microscopic work. It holds for every statically admissible $\sigma$ ($\nabla \cdot \sigma = 0$) and every compatible $\varepsilon = \varepsilon(u)$ under KUBC, SUBC and PBC. For KUBC: write $u = E \cdot x + w$ with $w = 0$ on $\partial V$. Then $\langle \varepsilon \rangle = E$, because $\int_V \nabla w = \int_{\partial V} w \otimes n = 0$, and

$$\langle \sigma : \varepsilon \rangle = \langle \sigma \rangle : E + \frac{1}{|V|} \int_{\partial V} (\sigma n) \cdot w\, ds - \frac{1}{|V|} \int_V (\nabla \cdot \sigma) \cdot w\, dx = \langle \sigma \rangle : E,$$

since $w = 0$ on $\partial V$ and $\nabla \cdot \sigma = 0$. The proofs for SUBC and PBC are the same, with the boundary term zero by the traction data or by periodicity.

**Bounds.** In the order of quadratic forms, $\langle C^{-1} \rangle^{-1} \le C^{\mathrm{SUBC}}_V \le C^{\mathrm{PBC}}_V \le C^{\mathrm{KUBC}}_V \le \langle C \rangle$ for each sample, with the Reuss and Voigt bounds of the sample at the two ends. The middle inequalities hold because the fluctuations allowed by KUBC are a subset of the periodic ones, and the dual statement holds for the stresses. KUBC is too stiff and SUBC too soft at a finite size; both converge to $C^{\mathrm{eff}}$ as $L$ grows, and PBC usually converges fastest.

## Examples and non-examples

**Example: a periodic composite.** One period $Y$ with PBC gives the apparent tensor $A^*$ of [periodic homogenization](/periodic-homogenization/) exactly: the cell problem is the RVE problem. A laminate of phases 1 and 4 in equal fractions has $A^*_{11} = 1.6$ across the layers and $A^*_{22} = 2.5$ along them. KUBC on the same cell gives $A^{\mathrm{KUBC}}_{11} \ge 1.6$, which is not exact for a single cell; the error decreases as the window holds more periods.

**Example: a random bar, by hand.** A bar is a chain of cells of length 1, each with conductivity 1 or 4 with probability $\tfrac12$, independently. A window of $m$ cells has the apparent conductivity $a_m = (\tfrac1m \sum_i 1/a_i)^{-1}$ with any boundary condition, because in 1D the flux is constant. The effective value is $1/\mathbb E[1/a] = 1/0.625 = 1.6$ by the [law of large numbers](/law-of-large-numbers/). The values $1/a_i \in \{1, 0.25\}$ have mean 0.625 and standard deviation 0.375, so the relative standard deviation of $a_m$ is about $0.375 / (0.625 \sqrt m) = 0.6 / \sqrt m$ for large $m$. For a relative error of 1% with the factor 2 and $n = 1$ realization, $2 \cdot 0.6 / \sqrt m \le 0.01$ gives $m \ge 14400$ cells; with $n = 100$ realizations, $m \ge 144$ cells per window. A window of $m = 4$ cells has the value 1, 1.231, 1.6, 2.286 or 4, and the value 1.6 has probability $6/16$, so a small window is far from 1.6 in most draws.

**Non-example: a sample below the correlation length.** A single fiber with its matrix, cut from a random fiber composite, is a periodic cell of an ordered arrangement that the material does not have. Its apparent tensor is not the effective tensor of the random material, whatever the boundary condition.

**Non-example: a graded material.** If the volume fraction changes across the part, no sample is typical of the whole. Each region needs its own RVE, and the region must still be small compared with the gradient.

**Non-example: strain localization.** In softening materials, damage concentrates in a band whose width is set by the microstructure, and the apparent response depends on the sample size for every size. In that case no RVE exists for the softening branch.

## Related definitions

- [Periodic homogenization](/periodic-homogenization/): the cell problem is the RVE problem with PBC on one period.
- [Two-scale convergence](/two-scale-convergence/): the limit theory that justifies the cell problem for periodic media.
- [FE2 method](/fe2-method/): solves an RVE problem at each integration point of a macroscopic finite element model, with the Hill-Mandel condition as the link between the scales.
- [Heterogeneous multiscale method](/heterogeneous-multiscale-method/): uses micro samples of size $\delta$ that need not be RVEs, and controls the error from $\delta$ and the boundary condition.
- Statistical homogeneity and ergodicity: the hypotheses under which the apparent values converge to one deterministic effective value as the volume grows.

## References
