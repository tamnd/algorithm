---
tag: 4CFCM8
kind: model
slug: embedded-atom-method
name: Embedded atom method
aliases:
- EAM potential
area: scientific-computing/molecular-simulation
level: advanced
summary: A potential for metals in which each atom's energy is a function of the electron density summed from its neighbors, plus a pair term.
model: real-ram
history:
  year: 1984
  people: [Murray S. Daw, Michael I. Baskes, Stephen M. Foiles, Michael W. Finnis, James E. Sinclair]
  note: Daw and Baskes gave the embedded atom method in 1984, with a derivation from density functional theory. Finnis and Sinclair gave a potential of the same form from tight-binding theory in the same year, and Foiles, Baskes and Daw fitted functions for six fcc metals in 1986.
prereqs: [interatomic-potential, lennard-jones-potential]
see_also: [interatomic-potential, lennard-jones-potential, behler-parrinello-potential, molecular-dynamics, verlet-neighbor-list, periodic-boundary-conditions, cauchy-born-rule, nudged-elastic-band]
sources:
  - paper: doi:10.1103/PhysRevB.29.6443
    title: Murray S. Daw and M. I. Baskes, Embedded-atom method, derivation and application to impurities, surfaces, and other defects in metals, Physical Review B 29(12), 1984, 6443-6453
    locator: the energy as embedding functions of the host electron density plus a pair repulsion, and its derivation from density functional theory
  - paper: doi:10.1103/PhysRevB.33.7983
    title: S. M. Foiles, M. I. Baskes and M. S. Daw, Embedded-atom-method functions for the fcc metals Cu, Ag, Au, Ni, Pd, Pt, and their alloys, Physical Review B 33(12), 1986, 7983-7991
    locator: the fitted embedding functions and pair terms for six fcc metals and the alloy model
  - paper: doi:10.1016/0920-2307(93)90001-U
    title: Murray S. Daw, Stephen M. Foiles and Michael I. Baskes, The embedded-atom method, a review of theory and applications, Materials Science Reports 9(7-8), 1993, 251-310
    locator: the review of the form, the fitting, the limits of pair potentials for metals and the applications
  - paper: doi:10.1080/01418618408244210
    title: M. W. Finnis and J. E. Sinclair, A simple empirical N-body potential for transition metals, Philosophical Magazine A 50(1), 1984, 45-55
    locator: the square-root embedding term from the second moment of the tight-binding density of states
---

The embedded atom method (EAM) is an [interatomic potential](/interatomic-potential/) for metals. Each atom sits in the electron density that its neighbors make at its position, and it gets an energy $F(\rho)$ for being embedded in that density, plus a pair term with each neighbor. Since $F$ is not linear, the energy of a bond depends on how many other bonds the atom has, so the model is many-body and cannot be written as a sum over pairs. It costs about as much as a pair potential, and it fixes the main failures of pair potentials for metals: vacancy energies that are too high and the Cauchy relation between the elastic constants.

## The machine

**Unknowns.** The positions $r_1, \ldots, r_N$ of the atoms, with $r_{ij} = |r_i - r_j|$.

**Functional form.** For one species,
$$U = \sum_{i} F(\rho_i) + \sum_{i<j} \phi(r_{ij}), \qquad \rho_i = \sum_{j \ne i} f(r_{ij}).$$
Here $f(r)$ is the contribution of a neighbor at distance $r$ to the density at an atom, $F$ is the embedding function, and $\phi$ is a pair term, mostly repulsive. All three vanish beyond a cutoff $r_c$. For several species, $F$ depends on the species of atom $i$, $f$ on the species of atom $j$, and $\phi$ on the pair of species.

**Forces.** The derivative of $U$ with respect to the distance of one pair collects three terms, so
$$F_i = -\nabla_i U = -\sum_{j \ne i} \left[\big(F'(\rho_i) + F'(\rho_j)\big) f'(r_{ij}) + \phi'(r_{ij})\right] \frac{r_i - r_j}{r_{ij}} .$$
A pair force thus depends on the densities at both of its atoms, so the forces need two passes: one to compute all $\rho_i$, and one to add the pair forces.

**Parameters, fitted and derived.** The three functions are the parameters. The form is derived: Daw and Baskes obtained it from density functional theory, with the density at an atom approximated by a sum of atomic densities, and Finnis and Sinclair obtained $F(\rho) = -A\sqrt{\rho}$ from tight-binding theory, in which the band energy grows as the square root of the second moment of the density of states. The functions themselves are fitted. In Foiles, Baskes and Daw, $f$ comes from free-atom electron densities, and $F$ and $\phi$ are fitted to the lattice constant, the elastic constants, the sublimation energy and the vacancy formation energy of each metal. Later fits use many quantum energies and forces as well.

**Gauge freedom.** The functions are not unique. For any constant $k$, the change
$$F(\rho) \to F(\rho) + k\rho, \qquad \phi(r) \to \phi(r) - 2k f(r)$$
leaves $U$ unchanged for every configuration, since $\sum_i k\rho_i = 2k\sum_{i<j} f(r_{ij})$. The scaling $f \to s f$, $F(\rho) \to F(\rho / s)$ leaves $U$ unchanged too. So only combinations of the functions are physical, and a fit must fix the gauge, for example by asking $F'(\bar\rho) = 0$ at the density $\bar\rho$ of the perfect crystal. The separation of the energy into "embedding" and "pair" parts has no meaning on its own.

**Standing assumptions.** The electron density at an atom is a sum of spherical contributions of its neighbors, so the model has no angular terms. This suits metals with nearly free electrons and filled or nearly filled d bands, such as the fcc metals Cu, Ag, Au, Ni, Pd and Pt. Covalent materials with directional bonds, such as silicon, need angular terms.

```pseudo id=main
EAM-ENERGY-FORCES(r_1..r_N, F, f, φ, r_c)
L1  ρ_i ← 0 for each atom i; U ← 0
L2  for each pair i < j with r = |r_ij| < r_c:
L3      ρ_i ← ρ_i + f(r); ρ_j ← ρ_j + f(r); U ← U + φ(r)
L4  for each atom i: U ← U + F(ρ_i)
L5  for each pair i < j with r = |r_ij| < r_c:
L6      g ← (F'(ρ_i) + F'(ρ_j)) f'(r) + φ'(r)        ▷ dU/dr for this pair
L7      F_i ← F_i - g r_ij / r; F_j ← F_j + g r_ij / r
L8  return U, ρ, F
```

With a [Verlet neighbor list](/verlet-neighbor-list/), both passes cost $O(N)$ at fixed density, about twice the cost of a pair potential. In parallel codes, the second pass needs the $F'(\rho_j)$ of atoms owned by other processors, which is one extra communication step per force call.

## What it counts

The model gives the energy $U$ and the forces, and through simulation, static calculations and [molecular dynamics](/molecular-dynamics/):

- **Bulk properties:** lattice constants, cohesive energies, elastic constants and phonons.
- **Defects:** the formation and migration energies of vacancies and interstitials, surface and grain boundary energies, and dislocation cores. Barriers come from saddle points, for example with the [nudged elastic band](/nudged-elastic-band/) method.
- **Alloys:** heats of mixing and segregation, with functions for each species.
- **Thermal behavior:** melting, thermal expansion and diffusion, from molecular dynamics.

## Relation to other models

- **Pair potentials.** If $F$ is linear, $F(\rho) = c\rho$, then $U = \sum_{i<j} [\phi(r_{ij}) + 2c f(r_{ij})]$ is a pair potential, such as the [Lennard-Jones potential](/lennard-jones-potential/). The nonlinearity of $F$ is the whole difference. A convex $F$ with $F'' > 0$, such as $-\sqrt\rho$, makes each extra bond worth less than the one before.
- **Finnis-Sinclair and second-moment potentials.** The same form with $F = -A\sqrt\rho$, from tight binding. The two models differ in the fitting, not in the form.
- **Modified EAM and bond-order potentials.** Modified EAM adds angular terms to the density, for metals with partly filled d bands and for silicon. Bond-order potentials such as Tersoff's make the strength of each bond depend on the angles to the other bonds.
- **Machine-learned potentials.** The [Behler-Parrinello potential](/behler-parrinello-potential/) has the same structure, a sum of atomic energies that depend on the neighborhood, but it replaces $F(\sum f)$ by a neural network of many descriptors of that neighborhood.
- **Continuum models.** The [Cauchy-Born rule](/cauchy-born-rule/) maps a uniform strain of the crystal to a strain energy density, and EAM is a common atomistic model behind it.

## Known results in the model

The results below are exact properties of the form, hand computations checked by the tests, and measurements.

**Bonds weaken with coordination (a hand computation).** Take $F(\rho) = -\sqrt\rho$, no pair term, and a density function with $f = 1$ at distance 1 and $f = 0$ beyond the first neighbors. A dimer at distance 1 has $\rho = 1$ at each atom, so $U = -2$, an energy of $-2$ per bond. An equilateral triangle with side 1 has $\rho = 2$ at each atom, so $U = -3\sqrt 2 = -4.243$ for 3 bonds, an energy of $-1.414$ per bond. A pair potential gives the same energy per bond in both.

**Vacancy energy (a hand computation).** In the same model, a crystal in which each atom has $z$ nearest neighbors has $\rho = z$ at each atom and cohesive energy $E_c = \sqrt z$ per atom. Remove one atom: its $z$ neighbors each lose one neighbor. The unrelaxed vacancy formation energy is
$$E_v = z\left(\sqrt z - \sqrt{z - 1}\right).$$
For fcc, $z = 12$: $E_v = 12(3.4641 - 3.3166) = 1.7698$, while $E_c = 3.4641$, so $E_v / E_c = 0.511$. A nearest-neighbor pair model gives $E_v / E_c = 1$, as the [interatomic potential](/interatomic-potential/) page shows. The tests build a 108-atom fcc crystal in a periodic box and recover these values. Real fcc metals have a ratio well below 1, and the fitted EAM functions reproduce the measured vacancy energies, which is one reason the model is used.

**The Cauchy relation (theorem).** For a cubic crystal with central pair forces, with each atom a center of inversion and no applied pressure, $C_{12} = C_{44}$. In EAM, the embedding term adds to $C_{12} - C_{44}$ a term proportional to $F''(\bar\rho)$, and $C_{44}$ gets no such term. So a convex $F$ gives $C_{12} > C_{44}$, as in most fcc metals, and the model can fit both constants.

**Other exact properties.**

- The total force is zero and the energy does not change under rotations, since $U$ depends only on distances.
- The gauge change above leaves energies and forces unchanged; the tests check this on random clusters.
- If $f$, $F$ and $\phi$ have continuous first derivatives and $f$ and $\phi$ go to zero with their derivatives at $r_c$, the forces are continuous and the energy is conserved in molecular dynamics up to the integrator error.

**Accuracy (measurements).** Daw, Foiles and Baskes review comparisons with experiment for surfaces, defects, alloys and liquid metals. The model is weakest where angular forces matter: bcc transition metals with partly filled d bands, and covalent materials.

## References
