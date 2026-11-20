---
tag: YQX6PN
kind: concept
slug: interatomic-potential
name: Interatomic potential
area: scientific-computing/molecular-simulation
level: intro
summary: A function that gives the potential energy of a set of atoms from their positions, whose negative gradient gives the forces used in molecular dynamics.
prereqs: [hamiltonian-systems]
see_also: [lennard-jones-potential, molecular-mechanics-force-field, embedded-atom-method, behler-parrinello-potential, molecular-dynamics, born-oppenheimer-molecular-dynamics, periodic-boundary-conditions, energy-function]
sources:
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Section 1.3 (model systems and interaction potentials), Section 1.4 (constructing an intermolecular potential from first principles) and Section 1.5 (force fields)
  - book: isbn:9780582382107
    title: Andrew R. Leach, Molecular Modelling, Principles and Applications, second edition, Prentice Hall, 2001
    locator: Chapter 4, empirical force field models
  - paper: doi:10.1016/0920-2307(93)90001-U
    title: Murray S. Daw, Stephen M. Foiles and Michael I. Baskes, The embedded-atom method, a review of theory and applications, Materials Science Reports 9(7-8), 1993, 251-310
    locator: the limits of pair potentials for metals and the many-body form that replaces them
  - paper: doi:10.1021/acs.chemrev.0c00868
    title: Jörg Behler, Four generations of high-dimensional neural network potentials, Chemical Reviews 121(16), 2021, 10037-10072
    locator: the place of machine-learned potentials among the classes of interatomic potentials
---

An interatomic potential is a function $U(r_1, \ldots, r_N)$ that gives the potential energy of $N$ atoms from their positions alone, with no electrons in the model. The force on atom $i$ is the negative gradient $F_i = -\nabla_i U$, and [molecular dynamics](/molecular-dynamics/) integrates Newton's equations with these forces. The function approximates the energy that quantum mechanics would give for the same positions, at a small part of the cost, and its form and its fitted parameters decide what a simulation can predict.

## In plain words

Atoms push each other apart when they are too close and pull together when they are a little farther away. An interatomic potential is a rule that turns the positions of all the atoms into one number, the stored energy.

The force on each atom follows from that number. Move one atom a small distance and see how much the energy changes: the atom is pushed in the direction where the energy goes down fastest. So one rule gives both the energy and all the forces.

The true energy comes from the electrons, and computing it is slow. The potential is a cheap formula with a few numbers chosen to match experiments or accurate calculations. A good formula for one material and one range of conditions can be poor for another, so each potential has a range where it is trusted.

## The idea

**Where the function comes from.** The nuclei are thousands of times heavier than the electrons, so for each set of nuclear positions the electrons settle into their ground state almost at once. Their energy, plus the repulsion of the nuclei, is a function of the nuclear positions alone: the Born-Oppenheimer energy surface. [Born-Oppenheimer molecular dynamics](/born-oppenheimer-molecular-dynamics/) computes this surface from the electrons at each step. An interatomic potential replaces that computation by a formula.

**Forces and conservation.** With $H = \sum_i |p_i|^2 / (2 m_i) + U$, the equations of motion form a [Hamiltonian system](/hamiltonian-systems/), and $H$ is constant along exact trajectories. Three symmetries of $U$ give more (theorems):

- If $U$ does not change when all atoms move by the same vector, then $\sum_i F_i = 0$, and the total momentum is constant.
- If $U$ does not change when all atoms rotate together, the total torque is zero, and the total angular momentum is constant. With [periodic boundary conditions](/periodic-boundary-conditions/) this symmetry is lost, so only the momentum is conserved there.
- If $U$ does not change when two atoms of the same species exchange places, the model treats identical atoms in the same way.

Every potential in use has these symmetries by construction. It must also be smooth enough for the integrator: a jump in the force, for example at a cutoff, makes the energy drift.

**The many-body expansion.** Any such $U$ can be written as
$$U = \sum_i U_1(r_i) + \sum_{i<j} U_2(r_i, r_j) + \sum_{i<j<k} U_3(r_i, r_j, r_k) + \cdots$$
The classes of potential differ in where they stop and how they write the terms:

- **Pair potentials** keep only $U_2 = \phi(r_{ij})$, a function of the distance. The [Lennard-Jones potential](/lennard-jones-potential/) is the standard one. They are good for noble gases and simple liquids.
- **Molecular force fields** add terms for bonds, angles and torsions between atoms that a fixed bond list connects, plus pair terms between all other atoms. The [molecular mechanics force field](/molecular-mechanics-force-field/) is this class.
- **Many-body potentials** make the energy of a bond depend on the other neighbors. In the [embedded atom method](/embedded-atom-method/) each atom has an energy that depends on the sum of contributions from its neighbors, which pairs cannot express.
- **Machine-learned potentials** fit a flexible function of the local environment of each atom to quantum energies. The [Behler-Parrinello potential](/behler-parrinello-potential/) uses one neural network per atom.

**Locality and cost.** If every term involves only atoms closer than a cutoff $r_c$, then at fixed density each atom has a bounded number of partners, and one evaluation of $U$ and all forces costs $O(N)$ with a [linked-cell list](/linked-cell-list/) or a [Verlet neighbor list](/verlet-neighbor-list/). The Coulomb energy between charges decays as $1/r$, too slowly for a cutoff, and is summed by [Ewald summation](/ewald-summation/) instead.

**Fitted and derived.** Some parts of a potential are derived from physics, for example the $r^{-6}$ dispersion term or the $1/r$ Coulomb term. Most parameters are fitted, either to experiment (lattice constants, elastic constants, densities, heats of vaporization) or to quantum calculations of energies and forces. A potential is then trusted near the states it was fitted to. Its accuracy elsewhere, its transferability, is a measurement, not a theorem.

## Examples

**A spring on a line.** Two atoms at $x_1 = 0$ and $x_2 = 1.5$ with $U = \tfrac{k}{2}(r - a)^2$, $r = x_2 - x_1$, $k = 2$ and $a = 1$. Then $U = \tfrac{2}{2}(0.5)^2 = 0.25$. The derivative is $\partial U / \partial x_2 = k(r - a) = 1$, so $F_2 = -1$ and $F_1 = +1$: the stretched spring pulls the atoms together, and $F_1 + F_2 = 0$ as translation symmetry requires.

**Three Lennard-Jones atoms.** Put three atoms at the corners of an equilateral triangle with side $2^{1/6}\sigma$, the distance of the minimum of the Lennard-Jones potential, where $\phi = -\epsilon$ and $\phi' = 0$. Then $U = 3\phi = -3\epsilon$, and every pair force is zero, so the triangle is at rest. It is a minimum of $U$ for three atoms.

**What pairs miss.** Take a crystal in which each atom has $z$ nearest neighbors, and count only nearest-neighbor pair bonds of energy $-b$. The cohesive energy per atom is $E_c = z b / 2$, since each bond has two ends. To make a vacancy, take one atom out of the bulk, which breaks $z$ bonds, and put it at a step on the surface, where on average it gains $z/2$ bonds. The cost, before the neighbors relax, is $E_v = z b - z b / 2 = z b / 2 = E_c$. A pair model so ties the vacancy energy to the cohesive energy. In most metals the vacancy energy is much smaller than the cohesive energy, and this is one reason metals use many-body potentials.

**The Cauchy relation.** For a cubic crystal held together by central pair forces, with each atom a center of inversion and no applied pressure, the elastic constants satisfy $C_{12} = C_{44}$ (a theorem of lattice theory). Many metals do not satisfy it. The [embedded atom method](/embedded-atom-method/) can break the relation, because its embedding term adds to $C_{12}$ but not to $C_{44}$.

## Where it is used

- **[Molecular dynamics](/molecular-dynamics/)** needs $U$ and all forces once per time step, and spends most of its time on them.
- **Monte Carlo simulation** needs only energy differences between the old and the new positions.
- **Energy minimization and transition paths:** relaxed structures, defect energies and barriers come from the minima and the saddle points of $U$, for example with the [nudged elastic band](/nudged-elastic-band/) method.
- **Structure prediction:** an [energy function](/energy-function/) for proteins is a potential of this kind, often with extra knowledge-based terms.
- **Coarse graining:** [force matching](/force-matching-coarse-graining/) and [iterative Boltzmann inversion](/iterative-boltzmann-inversion/) fit effective potentials between groups of atoms, so the same machinery runs on fewer sites.
- **Combined methods:** a [QM/MM method](/qm-mm-method/) uses a potential for most of the system and quantum mechanics for a small region.

## References
