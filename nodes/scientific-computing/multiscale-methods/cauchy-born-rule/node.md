---
tag: MS2TZP
kind: concept
slug: cauchy-born-rule
name: Cauchy-Born rule
area: scientific-computing/multiscale-methods
level: core
summary: Assumes the atoms of a crystal follow the macroscopic deformation gradient, giving a continuum energy density from an interatomic potential.
prereqs: [deformation-gradient, interatomic-potential]
see_also: [quasicontinuum-method, hyperelastic-material, lennard-jones-potential, embedded-atom-method, heterogeneous-multiscale-method, representative-volume-element, periodic-homogenization, multiscale-modeling]
sources:
  - book: isbn:9780198503699
    title: Max Born and Kun Huang, Dynamical Theory of Crystal Lattices, Oxford University Press (Oxford Classic Texts edition)
    locator: the derivation of the elastic constants from lattice sums under a homogeneous deformation (general locator)
  - paper: doi:10.1007/s00205-006-0031-7
    title: "Weinan E and Pingbing Ming, Cauchy-Born rule and the stability of crystalline solids: static problems, Archive for Rational Mechanics and Analysis 183(2), 2007, 241-297"
    locator: the stability conditions on the phonon spectrum and the proof that the atomistic solution converges to the Cauchy-Born elasticity solution for smooth loads
  - paper: doi:10.1007/s00332-002-0495-z
    title: Gero Friesecke and Florian Theil, Validity and failure of the Cauchy-Born hypothesis in a two-dimensional mass-spring lattice, Journal of Nonlinear Science 12(5), 2002, 445-478
    locator: a lattice in which the rule holds for some spring constants and fails for others
  - book: isbn:9780521856980
    title: "Ellad B. Tadmor and Ronald E. Miller, Modeling Materials: Continuum, Atomistic and Multiscale Techniques, Cambridge University Press, 2011"
    locator: Chapter 11, atomistic constitutive relations for crystals, with the Cauchy-Born rule for simple lattices and multilattices
---

The Cauchy-Born rule connects an atomistic model of a crystal with continuum elasticity. It assumes that when a crystal is deformed uniformly with the [deformation gradient](/deformation-gradient/) $F$, every bond vector of the lattice is mapped by $F$, so each atom moves to $F$ times its rest position. The energy of the deformed crystal per unit rest volume is then a function $W(F)$ that a lattice sum of the [interatomic potential](/interatomic-potential/) gives, and $W$ is the stored energy of a [hyperelastic material](/hyperelastic-material/). Graphics simulators pick a stored energy such as the [neo-Hookean model](/neo-hookean-model/) by hand; the rule instead derives $W$ from the atoms, so the continuum inherits the crystal's elastic constants, its anisotropy and its nonlinear response at large strain. The rule is an approximation: it holds for smooth deformations of stable crystals, it needs an inner relaxation in crystals with more than one atom per cell, and it fails near defects and past the point where the lattice becomes unstable.

## In plain words

A crystal is atoms on a regular grid. If you stretch a large piece of it evenly, it is natural to guess that the grid stays a grid and just stretches with the piece, so every atom moves as the piece moves. With this guess you can compute the energy of any even stretch or shear from the forces between atoms, and use that energy as the material law of a continuum.

The guess works when the stretch changes slowly over many atoms. It fails at cracks, at the edges of the material and at defects, where atoms move very differently from their neighbors. It also fails in crystals where each repeating block has several atoms, because those atoms can shift inside the block, and in crystals stretched so far that the grid itself becomes unstable.

## The idea

**Simple lattices.** Let the rest lattice be the points $X = \sum_\alpha n_\alpha A_\alpha$ with integer $n_\alpha$ and a cell of volume $\Omega_0$, and let the atoms interact by a pair potential $V(r)$. The Cauchy-Born rule sets $x = F X$ for every atom. All atoms are then alike, and the energy per atom is $\frac12 \sum_{X \ne 0} V(|F X|)$, so the stored energy density is
$$W(F) = \frac{1}{2 \Omega_0} \sum_{X \ne 0} V(|F X|).$$
The same construction works for many-body potentials such as the [embedded atom method](/embedded-atom-method/): put the deformed neighbors $F X$ into the energy of one atom and divide by $\Omega_0$. The first Piola-Kirchhoff stress is $P = \partial W / \partial F$ and the elastic moduli at rest are $\partial^2 W / \partial F^2$ at $F = I$. $W$ depends on $F$ only through $F^T F$, because $V$ depends on lengths only, so $W$ is frame indifferent.

**Multilattices.** If the cell has several atoms, at offsets $p_1, \dots, p_m$, the plain rule maps each offset by $F$ too. This is wrong in general: the sublattices can shift with respect to each other at no cost to the continuum, and they do, to lower the energy. The corrected rule maps the lattice by $F$ and minimizes over the shifts:
$$W(F) = \min_{p_1, \dots, p_m} \frac{1}{\Omega_0} E_{\text{cell}}(F; p_1, \dots, p_m).$$

**Where it fails.** The rule assumes that the deformation varies slowly on the scale of the lattice and that the uniformly deformed lattice is a stable state. E and Ming (2007) proved that, under stability conditions on the phonon spectrum of the deformed lattice and for smooth loads, the atomistic equilibrium converges to the solution of Cauchy-Born elasticity as the lattice spacing goes to zero. Without stability, the rule can fail: Friesecke and Theil (2002) gave a two-dimensional mass-spring lattice in which it holds for some spring constants and fails for others. Near a crack tip, a dislocation core or a free surface the deformation changes from atom to atom, and the rule does not apply.

**History.** Cauchy derived elastic constants from central forces between molecules in the 1820s, which gives the Cauchy relations between the constants. Born and Huang made the lattice sum under a homogeneous deformation the basis of the elasticity of crystal lattices, including the inner displacements of lattices with a basis.

## Examples

**The lattice constant of a chain.** Take the Lennard-Jones potential $V(r) = 4 (r^{-12} - r^{-6})$ in reduced units ([Lennard-Jones potential](/lennard-jones-potential/)) on a chain with spacing $a$, so $F = a / a_0$ in one dimension. With all neighbors, the energy per atom is $\sum_{n \ge 1} V(n a) = 4 (\zeta(12) a^{-12} - \zeta(6) a^{-6})$, where $\zeta$ is the Riemann zeta function. Setting the derivative to zero gives $a^6 = 2 \zeta(12) / \zeta(6)$, so $a_0 = 1.119296$ and the energy per atom is $-\zeta(6)^2 / \zeta(12) = -1.034732$. With nearest neighbors only, $a_0 = 2^{1/6} = 1.122462$ and the energy is $-1$; with first and second neighbors, $a^6 = 2 (1 + 2^{-12}) / (1 + 2^{-6})$ and $a_0 = 1.119611$. The rule turns each of these lattice sums into a stored energy $W(F) = \sum_n V(n a_0 F) / a_0$ per unit rest length.

**Stiffness and the loss of stability.** For the nearest neighbor chain, $W(F) = V(a_0 F) / a_0$, so the modulus at rest is $W''(1) = a_0 V''(a_0)$. With $a_0^6 = 2$, $V''(a_0) = 4 (156 a_0^{-14} - 42 a_0^{-8}) = 72 / 2^{1/3} = 57.146$, and the modulus is $72 / 2^{1/6} = 64.145$. The stored energy is convex only while $V'' > 0$, that is for $r^6 < 156 / 42 = 26 / 7$. So the rule predicts that the chain loses stability at $r = (26/7)^{1/6} = 1.244455$, a strain of $F - 1 = (13/7)^{1/6} - 1 = 10.87\%$, where the tension reaches its largest value $V'(r) = 2.396$. Past this point, a uniform stretch is not a minimum and the chain breaks at one bond, which the uniform rule cannot describe.

**A chain with two atoms per cell.** Join springs of rest length $1$ and stiffness $k_1 = 1$ and $k_2 = 3$ in turn, so a cell of length $2$ has two atoms. The plain rule stretches both springs by $F - 1$, which gives the energy $\frac{1}{2} (k_1 + k_2) (F - 1)^2$ per cell and the modulus $(k_1 + k_2) / 2 = 2$ per unit length. But the inner atom moves until both springs carry the same force, as springs in series do. The relaxed rule gives the series stiffness $k_1 k_2 / (k_1 + k_2)$ for a cell of length $2$, so the modulus is $2 k_1 k_2 / (k_1 + k_2) = 1.5$. This is the correct value for the chain; the plain rule is 33% too stiff. In general the plain rule gives an upper bound on the energy, because the relaxed rule minimizes over the shifts and the plain rule is one choice of the shifts.

## Where it is used

- **Atomistic-continuum coupling.** The [quasicontinuum method](/quasicontinuum-method/) uses the rule in its continuum region, with full atomistic detail near defects. The [heterogeneous multiscale method](/heterogeneous-multiscale-method/) computes the stress of a macroscopic element by a small atomistic calculation, which is the rule when the calculation is a uniformly deformed cell.
- **Elastic constants from potentials.** The moduli $\partial^2 W / \partial F^2$ give the elastic constants of a potential at zero temperature, which is how potentials are fitted and tested against experiment.
- **Ideal strength.** The largest stress along a path of uniform deformations, as in the chain example, is the ideal strength of a perfect crystal, and the loss of convexity of $W$ marks a possible instability.
- **Homogenization.** The rule is the lattice analog of a [representative volume element](/representative-volume-element/) with uniform boundary conditions, and of [periodic homogenization](/periodic-homogenization/) when the cell is relaxed.

## References
