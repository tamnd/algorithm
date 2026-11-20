---
tag: CDM80T
kind: algorithm
slug: qm-mm-method
name: QM/MM method
aliases:
- hybrid quantum mechanics molecular mechanics
area: scientific-computing/multiscale-methods
level: advanced
summary: Treats a small reactive region by quantum mechanics and the rest by a molecular mechanics force field, with coupling terms between them.
model: real-ram
complexity:
  vars: {q: the number of sites in the QM model system, N: the number of atoms}
  time: {worst: O(q^3 + N)}
  space: {extra: O(q^2 + N)}
properties: {deterministic: true, randomized: false, exact: false, iterative: false}
history:
  year: 1976
  people: [Arieh Warshel, Michael Levitt]
  note: Warshel and Levitt treated the reacting part of an enzyme by quantum mechanics and the protein around it by a classical model in 1976. Field, Bash and Karplus gave a general QM/MM potential for molecular dynamics in 1990, and Morokuma and coworkers gave the subtractive IMOMM and ONIOM schemes in 1995 and 1996.
prereqs: [molecular-mechanics-force-field, born-oppenheimer-molecular-dynamics]
see_also: [molecular-dynamics, car-parrinello-molecular-dynamics, interatomic-potential, behler-parrinello-potential, ewald-summation, jacobi-eigenvalue-algorithm, quasicontinuum-method, multiscale-modeling]
sources:
  - paper: doi:10.1016/0022-2836(76)90311-9
    title: "A. Warshel and M. Levitt, Theoretical studies of enzymic reactions: dielectric, electrostatic and steric stabilization of the carbonium ion in the reaction of lysozyme, Journal of Molecular Biology 103(2), 1976, 227-249"
    locator: the first combined model, with a quantum region inside a classical protein
  - paper: doi:10.1002/jcc.540110605
    title: Martin J. Field, Paul A. Bash and Martin Karplus, A combined quantum mechanical and molecular mechanical potential for molecular dynamics simulations, Journal of Computational Chemistry 11(6), 1990, 700-733
    locator: the additive QM/MM Hamiltonian with link atoms and electrostatic coupling, used for molecular dynamics
  - paper: doi:10.1002/jcc.540160911
    title: "Feliu Maseras and Keiji Morokuma, IMOMM: A new integrated ab initio + molecular mechanics geometry optimization scheme of equilibrium structures and transition states, Journal of Computational Chemistry 16(9), 1995, 1170-1179"
    locator: the subtractive combination of an ab initio model system with molecular mechanics for the whole system
  - paper: doi:10.1021/jp962071j
    title: "Mats Svensson, Stephane Humbel, Robert D. J. Froese, Toshiaki Matsubara, Stefan Sieber and Keiji Morokuma, ONIOM: A multilayered integrated MO + MM method for geometry optimizations and single point energy predictions, The Journal of Physical Chemistry 100(50), 1996, 19357-19363"
    locator: the ONIOM extrapolation with several layers
  - paper: doi:10.1002/anie.200802019
    title: Hans Martin Senn and Walter Thiel, QM/MM methods for biomolecular systems, Angewandte Chemie International Edition 48(7), 2009, 1198-1229
    locator: a review of additive and subtractive schemes, mechanical and electrostatic embedding, and the treatment of the boundary
---

The QM/MM method computes the energy and forces of a large molecular system by treating a small region, where bonds break or electrons move, with quantum mechanics (QM), and everything else with a [molecular mechanics force field](/molecular-mechanics-force-field/) (MM). Quantum calculations cost at least the cube of the size of the region, while force fields cost about linear time, so the split makes reactions in enzymes, in solution and in materials possible to model. The two regions are coupled by bonded terms across the boundary, by electrostatics and by van der Waals terms, and bonds cut by the boundary are capped with link atoms. With these energies and forces, the system can be optimized or moved by [molecular dynamics](/molecular-dynamics/) in the spirit of [Born-Oppenheimer molecular dynamics](/born-oppenheimer-molecular-dynamics/) for the QM part.

## In plain words

Think of an enzyme with thousands of atoms. Only a few of them take part in the chemical reaction; the rest hold the stage. Computing the electrons of all atoms would take far too long, so you compute the electrons only for the small group at the center, and treat all other atoms as balls on springs.

Where the two parts meet, a chemical bond is cut in two. To keep the small group chemically sensible, you put a stand-in atom, usually hydrogen, on the cut bond. The forces on the stand-in are passed back to the two real atoms of the bond. There are two ways to add up the energies: add the small group and the rest, taking care not to count anything twice, or compute the whole system cheaply and replace the cheap energy of the center by the accurate one.

## The problem

The input is the positions of $N$ atoms, a QM region $Q$ of atoms, a QM method that gives the energy and the forces of a small molecule, and an MM force field for the whole system. The output is a total energy $E$ and forces $F = -\nabla E$ on all atoms, so that geometry optimization and molecular dynamics can use them. The **model system** is the QM region with a link atom $L$ on each cut bond $(a, b)$, $a \in Q$, $b \notin Q$, placed on the bond at
$$y_L = y_a + g\, (y_b - y_a)$$
with a fixed ratio $g$ (for a carbon-hydrogen link that replaces a carbon-carbon bond, $g$ is near the ratio of the two bond lengths). The **additive** energy is
$$E = E_{QM}(\text{model}) + E_{MM}(\text{outside } Q) + E_{QM\text{-}MM},$$
where $E_{QM\text{-}MM}$ couples the regions. The **subtractive** energy (IMOMM, ONIOM) is
$$E = E_{MM}(\text{real}) + E_{QM}(\text{model}) - E_{MM}(\text{model}).$$
In **mechanical embedding**, the coupling is the MM terms between QM and MM atoms. In **electrostatic embedding**, the MM charges also enter the QM Hamiltonian, so the electrons of the QM region are polarized by the environment.

## The algorithm

```pseudo id=main
QMMM-ADDITIVE(positions y, QM region Q, ratio g)
L1  build the model system: the atoms of Q, and a link atom at y_L = y_a + g (y_b - y_a) on each cut bond (a, b)
L2  (E_Q, F_Q) ← QM energy and forces of the model system
L3  for each link atom L on the cut bond (a, b): F_a ← F_a + (1 - g) F_L,  F_b ← F_b + g F_L,  then drop L
L4  (E_M, F_M) ← MM energy and forces of every term with at least one atom outside Q
L5  return E = E_Q + E_M and F = F_Q + F_M
```

The link atom is not a real atom: its position is a function of $y_a$ and $y_b$, so its force must be passed to them by the chain rule, which is line L3. Line L4 takes the coupling terms (bonds, angles and dihedrals across the boundary, and the van der Waals terms between the regions) from the force field, which is mechanical embedding; in electrostatic embedding the MM charges also go into the QM calculation of line L2, and the MM terms of line L4 leave out the electrostatics between the regions, because the QM calculation already contains them.

The implementation is a toy. The QM method is a Hückel tight-binding model of a chain on a line, with hopping $t(r) = t_0 e^{-\beta (r - r_0)}$, one electron per site and the energy $2 \sum_{\text{occupied}} \lambda_k + \sum_i A e^{-2 \beta (r_i - r_0)}$. The matrix is diagonalized by the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/), and the forces follow from the Hellmann-Feynman formula. The MM part is harmonic bonds $(k/2)(r - d_0)^2$. The parameters $t_0 = 1$, $\beta = \ln 2$, $A = 1$, $r_0 = 1$, $k = 10$, $d_0 = 2$ and $g = 1/2$ are choices that make the numbers simple. The code also has the subtractive scheme.

## Example

**By hand.** Three atoms sit at $y = (0, 2.2, 4.2)$ and atom $0$ is the QM region. The cut bond is $(0, 1)$, so line L1 puts the link atom at $0 + 0.5 \cdot 2.2 = 1.1$, and the model system is a dimer of length $1.1$. Its hopping is $t = 2^{-0.1} = 0.933033$ and its repulsion is $A e^{-2\beta \cdot 0.1} = 2^{-0.2} = 0.870551$. The dimer has one bonding orbital with eigenvalue $-t$ and two electrons, so line L2 gives $E_Q = -2t + 2^{-0.2} = -0.995515$, and
$$\frac{dE_Q}{dr} = 2 \beta t - 2 \beta \cdot 2^{-0.2} = 2 \ln 2 \cdot (0.933033 - 0.870551) = 0.086619 .$$
So the force on atom $0$ is $+0.086619$ and the force on the link atom is $-0.086619$. Line L3 gives half of the link force to atom $0$ and half to atom $1$: the QM forces on the real atoms are $(0.043310, -0.043310, 0)$. Line L4 adds the cut bond, stretched by $0.2$, with energy $5 \cdot 0.04 = 0.2$ and forces $(2, -2)$ on atoms $0$ and $1$; bond $(1, 2)$ is at rest. The total is $E = -0.795515$ with $F = (2.043310, -2.043310, 0)$.

**Subtractive.** For the same atoms, ONIOM gives $E = 0.2 - 0.995515 - 0.2 = -0.995515$: the MM energy of the real system is the cut bond, $0.2$, and in the model system the link bond gets the MM parameters $(k / g^2, g d_0) = (40, 1)$, so its MM energy is $20 \cdot 0.1^2 = 0.2$ as well. The two schemes differ by the MM energy of the cut bonds, a fact that the proofs file proves for any chain with this choice of link parameters.

**Dynamics.** On a chain of 8 atoms with the QM region of atoms $2$ to $5$ (two link atoms, a model system of 6 sites), velocity Verlet over 5 time units keeps the total energy to within $2.65 \cdot 10^{-4}$ at $h = 0.02$ and $6.69 \cdot 10^{-5}$ at $h = 0.01$ for the additive scheme, and $3.57 \cdot 10^{-4}$ and $9.24 \cdot 10^{-5}$ for ONIOM. The ratio is close to $4$, the second order of the integrator, which shows that the forces are the gradient of the energy (measurement).

## Correctness

The proofs file shows, for the toy, that the forces are the exact negative gradient of the energy. The model system of an even number of sites on a chain always has a gap between the occupied and the empty orbitals, because the spectrum is symmetric about $0$ and $0$ is not an eigenvalue; with the gap, the derivative of the sum of the occupied eigenvalues is the Hellmann-Feynman expression $2 \sum_k c_k^T (\partial H / \partial r) c_k$. The link atom position is linear in the positions of $a$ and $b$, so line L3 is the chain rule. The proof also shows that the forces sum to zero, that both schemes give the pure QM energy when $Q$ contains all atoms, and that the additive minus the subtractive energy is the MM energy of the cut bonds.

For a real QM method, the same argument needs a converged self-consistent field: the Hellmann-Feynman forces are the gradient only at the variational minimum, and with a basis of atom-centered functions they need the Pulay terms as well. The quality of the result, how close $E$ is to the energy of a full QM calculation, is not a theorem: it depends on the size of the QM region, the boundary and the embedding, and is checked by tests that enlarge the region.

## Complexity

In the [real RAM](/real-ram/) model, the toy costs $O(q^3)$ per sweep of the Jacobi method on the $q$ by $q$ matrix of the model system, with a capped number of sweeps, and $O(N)$ for the bonds of the MM part, so an energy and force evaluation is $O(q^3 + N)$ with $O(q^2 + N)$ memory. In real programs, the QM part dominates: Hartree-Fock and density functional methods cost between the cube and the fourth power of the number of basis functions, and correlated methods more, while the MM part costs $O(N \log N)$ with [particle mesh Ewald](/particle-mesh-ewald/) electrostatics. Electrostatic embedding adds the $N$ MM charges to the QM Hamiltonian, at a cost linear in $N$ per QM matrix element of the external potential.

## Properties

- **Consistent forces.** With a converged QM calculation and the chain rule for link atoms, the forces are the gradient of a single energy, so dynamics conserve energy and optimizations converge (theorem for the toy, Lemma 2 and Lemma 4 of the proofs file).
- **Correct limits.** If the QM region is the whole system, both schemes give the QM energy (theorem). If the QM method is replaced by the MM method, the subtractive scheme gives the MM energy of the real system exactly (theorem, from the form of the formula).
- **Additive versus subtractive.** The subtractive scheme needs no special coupling terms and works with any pair of methods, but needs MM parameters for the model system, including the QM region. The additive scheme needs no MM parameters inside the QM region, which matters when bonds change.
- **Approximate.** The result depends on the choice of the QM region, the link atoms and the embedding, and must be checked by enlarging the QM region (heuristic).
- **Translation invariance.** The energy depends only on the relative positions, so the forces sum to zero (theorem).

## Variants and improvements

- **Electrostatic embedding.** The MM point charges enter the QM Hamiltonian, which polarizes the QM region. This is the common choice for reactions in proteins and solution. Charges next to the link atom are often removed, shifted or smeared, to avoid an overpolarization of the boundary.
- **Polarizable embedding.** The MM region has induced dipoles or fluctuating charges, which respond to the QM region in turn.
- **Other boundary treatments.** Instead of link atoms, the cut bond can be capped by frozen localized orbitals or by a boundary atom with special parameters (pseudopotentials).
- **Several layers.** ONIOM uses three or more layers, each with its own method, by repeating the subtraction.
- **Adaptive QM/MM.** Atoms enter and leave the QM region as they move, for example water molecules near a solute, with a smooth switching to keep the energy continuous.
- **Machine learning potentials.** A [Behler-Parrinello](/behler-parrinello-potential/) or other learned potential can replace the QM method, or the MM region, at a much lower cost.

## When to use it

Use QM/MM when a chemical event (a bond that breaks, a change of charge, an excited state) takes place in a small part of a large system, and the rest acts through its shape and its electrostatics. Use a plain [molecular mechanics force field](/molecular-mechanics-force-field/) when no bonds change. Use a full QM method, as in [Born-Oppenheimer](/born-oppenheimer-molecular-dynamics/) or [Car-Parrinello](/car-parrinello-molecular-dynamics/) molecular dynamics, when the system is small enough or when the chemistry is spread out, for example in a metal. Use the [quasicontinuum method](/quasicontinuum-method/) for the analogous split between atoms and a continuum in solids.

## Pitfalls

- **The link force is dropped.** Leaving out line L3, or giving all of $F_L$ to atom $a$, gives forces that are not the gradient of the energy, and molecular dynamics drifts in energy. Write line L3 with the chain rule weights $1 - g$ for $a$ and $g$ for $b$.
- **Terms counted twice.** In the additive scheme, line L4 must leave out the MM terms with all atoms in $Q$, because $E_Q$ already contains them; in the subtractive scheme, $E_{MM}(\text{model})$ must use the same terms as $E_{MM}(\text{real})$ for the model atoms. Write line L4 over the terms with at least one atom outside $Q$.
- **Odd electron counts.** A link atom adds one electron per cut bond. The toy raises an error when the model system has an odd number of electrons; a real calculation must set the charge and spin of the model system on purpose.
- **Overpolarization at the boundary.** In electrostatic embedding, an MM charge on atom $b$ sits very close to the link atom and pulls the QM electrons too strongly. Remove, shift or smear the charges next to the boundary.
- **Cuts through polar or conjugated bonds.** A link atom on a polar bond, or on a bond of a conjugated system, changes the electronic structure of the QM region. Cut nonpolar single bonds, two or three bonds away from the reacting atoms.
- **A QM region too small.** Results can change much with the size of the QM region. Check convergence by enlarging the region.
- **Unconverged QM forces.** A loose convergence of the self-consistent field gives forces that are not the gradient of the energy. Tighten the convergence for dynamics.

## Implementations

## History

Warshel and Levitt built the first QM/MM model in 1976, for the reaction of the enzyme lysozyme, with a semiempirical quantum treatment of the reacting atoms inside a classical model of the protein and its dielectric. Field, Bash and Karplus gave in 1990 a general QM/MM potential with link atoms and electrostatic coupling, built into a molecular dynamics program. Maseras and Morokuma introduced the subtractive IMOMM scheme in 1995, and Svensson, Morokuma and coworkers generalized it to the multilayer ONIOM method in 1996. Karplus, Levitt and Warshel received the Nobel Prize in Chemistry in 2013 for multiscale models of complex chemical systems. Senn and Thiel reviewed the methods for biomolecular systems in 2009.

## References
