---
tag: GCEKBT
kind: model
slug: molecular-mechanics-force-field
name: Molecular mechanics force field
aliases:
- classical force field
area: scientific-computing/molecular-simulation
level: core
summary: A sum of bond, angle, torsion, Lennard-Jones and Coulomb terms with fitted parameters that models the energy of molecules.
model: real-ram
history:
  year: 1983
  people: [Bernard R. Brooks, Martin Karplus, Peter A. Kollman, Wendy D. Cornell]
  note: Brooks, Karplus and coworkers described CHARMM in 1983, and Cornell, Kollman and coworkers published the AMBER force field for proteins and nucleic acids in 1995. Both build on the molecular mechanics of the 1960s and 1970s.
prereqs: [interatomic-potential, lennard-jones-potential]
see_also: [interatomic-potential, lennard-jones-potential, molecular-dynamics, energy-function, ewald-summation, particle-mesh-ewald, shake-constraint-algorithm, qm-mm-method]
sources:
  - paper: doi:10.1021/ja00124a002
    title: Wendy D. Cornell, Piotr Cieplak, Christopher I. Bayly, Ian R. Gould, Kenneth M. Merz Jr., David M. Ferguson, David C. Spellmeyer, Thomas Fox, James W. Caldwell and Peter A. Kollman, A second generation force field for the simulation of proteins, nucleic acids, and organic molecules, Journal of the American Chemical Society 117(19), 1995, 5179-5197
    locator: the AMBER functional form, the fit of the charges to the electrostatic potential, and the scaling of the 1-4 interactions
  - paper: doi:10.1002/jcc.540040211
    title: Bernard R. Brooks, Robert E. Bruccoleri, Barry D. Olafson, David J. States, S. Swaminathan and Martin Karplus, CHARMM, a program for macromolecular energy, minimization, and dynamics calculations, Journal of Computational Chemistry 4(2), 1983, 187-217
    locator: the CHARMM energy function with bond, angle, dihedral, improper, van der Waals and electrostatic terms
  - book: isbn:9780582382107
    title: Andrew R. Leach, Molecular Modelling, Principles and Applications, second edition, Prentice Hall, 2001
    locator: Chapter 4, empirical force field models, molecular mechanics
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Section 1.5 (force fields)
---

A molecular mechanics force field is an [interatomic potential](/interatomic-potential/) for molecules: the energy is a sum of terms for the covalent bonds, the bond angles and the torsions of a fixed bond graph, plus [Lennard-Jones](/lennard-jones-potential/) and Coulomb terms between atoms that are not close in that graph. Every term has a simple form, and nearly every parameter is fitted to experiments or to quantum calculations on small molecules, then reused for each atom of the same type. AMBER and CHARMM are the force fields of this form that most protein and nucleic acid simulations use. The bond graph does not change during a simulation, so the model cannot break or form bonds.

## The machine

**Unknowns.** The positions $r_1, \ldots, r_N$ of the atoms, including the hydrogens in an all-atom force field.

**Fixed data of the model.** For each molecule, the bond graph and an atom type for each atom (for example an $sp^3$ carbon, or a carbonyl oxygen), with a partial charge $q_i$ in units of the elementary charge $e$. The graph defines three lists: the bonds, the angles (paths of 2 bonds) and the dihedrals (paths of 3 bonds), with internal coordinates $r$ (a bond length), $\theta$ (an angle) and $\phi$ (a dihedral angle).

**Functional form.** In the AMBER form of Cornell et al.,
$$U = \sum_{\text{bonds}} K_r (r - r_{eq})^2 + \sum_{\text{angles}} K_\theta (\theta - \theta_{eq})^2 + \sum_{\text{dihedrals}} \frac{V_n}{2}\left[1 + \cos(n\phi - \gamma)\right] + \sum_{i<j} \left[\frac{A_{ij}}{R_{ij}^{12}} - \frac{B_{ij}}{R_{ij}^6} + \frac{q_i q_j}{\varepsilon R_{ij}}\right].$$
The bond and angle terms are harmonic, with no factor $1/2$ in this convention: $K_r$ is half the second derivative. A dihedral can have several terms with periodicities $n = 1, 2, 3$ and phases $\gamma$. The last sum runs over the nonbonded pairs, in which $A_{ij}/R^{12} - B_{ij}/R^6$ is a Lennard-Jones term, $A_{ij} = 4\epsilon_{ij}\sigma_{ij}^{12}$ and $B_{ij} = 4\epsilon_{ij}\sigma_{ij}^6$, and $\varepsilon$ is a dielectric constant, 1 for explicit solvent. CHARMM has the same structure, with an extra Urey-Bradley term between the two ends of an angle and harmonic improper dihedral terms that keep planar groups planar.

**Units.** Energies in kcal/mol, lengths in Å, charges in $e$. The Coulomb energy $q_i q_j / (4\pi\epsilon_0 R)$ in SI becomes $332.0637\, q_i q_j / R$ kcal/mol with $R$ in Å; programs use slightly different values of this constant, which changes energies in the fifth digit.

**Exclusions and 1-4 scaling.** Pairs joined by one bond (1-2 pairs) or by two bonds (1-3 pairs) get no nonbonded term: the bond and angle terms already describe them. Pairs at the ends of a dihedral (1-4 pairs) get a scaled nonbonded term; in AMBER the Lennard-Jones part is divided by 2 and the Coulomb part by 1.2. All other pairs, including pairs in different molecules, get the full term.

**Parameters, fitted and derived.**

- **Fitted:** the force constants $K_r$, $K_\theta$ and the equilibrium values $r_{eq}$, $\theta_{eq}$, fitted to crystal structures, vibrational spectra and quantum calculations; the torsion terms $V_n$, $\gamma$, fitted to quantum energies of rotation about a bond; the partial charges, fitted in AMBER to the quantum electrostatic potential around small molecules; the Lennard-Jones $\sigma_i$ and $\epsilon_i$ of each type, fitted to liquid densities and heats of vaporization. The 1-4 scale factors are fitted too.
- **Derived:** the $1/R$ form of the Coulomb term and the $R^{-6}$ form of the dispersion. The mixed parameters $\sigma_{ij}$ and $\epsilon_{ij}$ come from combining rules such as Lorentz-Berthelot, which are a choice of the model, not a result.
- **Transferable by type:** the same parameters are used for every atom of a type, in every molecule. This is what makes the model usable for a protein never seen in the fit, and it is also its main approximation.

**Standing assumptions.** The bond graph is fixed. The charges are fixed and do not respond to the field of the other atoms (no polarization). The energy is a sum of terms of at most 4 atoms. The electrons do not appear.

## What it counts

The model gives the potential energy $U$ and the forces $F_i = -\nabla_i U$, and through them:

- **Structures:** minima of $U$, conformations of molecules and their relative energies.
- **Dynamics:** trajectories by [molecular dynamics](/molecular-dynamics/), from which come averages, free energies and rates, for proteins, nucleic acids, membranes and liquids.
- **Vibrations:** frequencies from the second derivatives of $U$ at a minimum.

**Cost.** The bonded terms number $O(N)$, since each atom has a bounded number of bonds. The Lennard-Jones terms are cut at $r_c$, often 0.8 to 1.2 nm, and cost $O(N)$ with a [Verlet neighbor list](/verlet-neighbor-list/). The Coulomb terms decay as $1/R$ and are summed by [Ewald summation](/ewald-summation/) or [particle-mesh Ewald](/particle-mesh-ewald/) in $O(N \log N)$. Bonds to hydrogen vibrate fastest, so they are often held fixed with [SHAKE](/shake-constraint-algorithm/), which permits a time step $h$ of about 2 fs.

## Relation to other models

- **[Lennard-Jones potential](/lennard-jones-potential/).** The nonbonded van der Waals term. A force field of one atom type with no charges and no bonds is the Lennard-Jones fluid.
- **[Interatomic potential](/interatomic-potential/).** A force field is the class of potentials that uses a fixed bond graph. Pair and many-body potentials for metals and crystals, such as the [embedded atom method](/embedded-atom-method/), need no graph.
- **Class II and polarizable force fields.** Class II force fields add anharmonic bond terms and cross terms such as bond-angle coupling. Polarizable force fields let the charges or induced dipoles respond to the field, at a higher cost.
- **Machine-learned potentials.** The [Behler-Parrinello potential](/behler-parrinello-potential/) and its successors fit a general function of the local environment to quantum data and can describe bond breaking, but they cost more per atom and are usually fitted to one system at a time.
- **[QM/MM](/qm-mm-method/).** A force field for the bulk of a protein and quantum mechanics for a reactive site.
- **Knowledge-based energies.** An [energy function](/energy-function/) for protein structure prediction may add terms derived from statistics of known structures, which are not physical energies.

## Known results in the model

**Hand checks of the terms.**

- **A bond.** A C-H bond with $K_r = 340$ kcal/(mol Å$^2$) and $r_{eq} = 1.09$ Å, stretched to 1.12 Å, has energy $340 \cdot 0.03^2 = 0.306$ kcal/mol. The force on each atom is $2 K_r (r - r_{eq}) = 20.4$ kcal/(mol Å), toward the other atom.
- **A pair of charges.** Charges $+0.4\,e$ and $-0.4\,e$ at 3 Å in vacuum, with $\varepsilon = 1$, have energy $332.0637 \cdot (-0.16)/3 = -17.71$ kcal/mol. If they are a 1-4 pair in AMBER, the term is $-17.71/1.2 = -14.76$ kcal/mol.
- **A threefold torsion.** Ethane has 9 dihedrals H-C-C-H. Give each the term $\tfrac{V_3}{2}[1 + \cos 3\phi]$ with $V_3/2 = 0.155$ kcal/mol. In the staggered form the three dihedrals on each hydrogen are at $60°$, $180°$ and $300°$, so $\cos 3\phi = -1$ for all 9 and the torsion energy is 0. In the eclipsed form $\cos 3\phi = 1$ and the energy is $9 \cdot 2 \cdot 0.155 = 2.79$ kcal/mol. The measured barrier of ethane is about 2.9 kcal/mol; in a full force field the 1-4 terms also add to the barrier, so the torsion parameters are fitted with them present.
- **Counting the terms of ethane.** $\mathrm{C_2H_6}$ has 8 atoms and 28 pairs. It has 7 bonds, 12 angles (on each carbon, 3 H-C-H and 3 H-C-C) and 9 dihedrals. The 7 bonded pairs and the 12 pairs at the ends of an angle are excluded, and the 9 pairs at the ends of a dihedral are 1-4 pairs, so $28 - 7 - 12 - 9 = 0$ pairs of one ethane molecule get a full nonbonded term. In a large molecule most pairs are full nonbonded pairs.

**Properties of the form (theorems).**

- **Symmetry.** Every term depends on distances, angles or dihedrals, so $U$ does not change under translations and rotations, and the total momentum is conserved in a simulation.
- **Smoothness.** The harmonic and cosine terms are smooth. The dihedral angle and its gradient are undefined when three atoms of a dihedral are on one line, and implementations must treat that case.
- **No reactions.** The bond graph is a fixed input, so no trajectory can change it: the model cannot describe bond breaking or proton transfer.

**Accuracy (measurements).** How well a force field reproduces folded structures, conformational energies, densities or free energies of solvation is a measurement on test sets, and it depends on the version of the parameters and on the water model used with it. Cornell et al. report such comparisons for their parameter set.

## References
