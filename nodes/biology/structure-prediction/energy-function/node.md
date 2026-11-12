---
tag: GDQNQ3
kind: concept
slug: energy-function
name: Energy function (scoring function)
area: biology/structure-prediction
level: advanced
summary: A function that gives each conformation of a molecule a number, low for stable structures. Physics-based force fields and knowledge-based potentials are the two main kinds.
prereqs: [thermodynamic-hypothesis, hydrophobic-effect]
see_also: [molecular-dynamics, rosetta, hp-model, energy-landscape, side-chain-packing, partition-function, markov-random-field, image-segmentation-graph-cuts]
sources:
  - paper: doi:10.1021/ja00124a002
    title: Wendy D. Cornell et al., A second generation force field for the simulation of proteins, nucleic acids, and organic molecules, Journal of the American Chemical Society 117(19), 1995, 5179-5197
    locator: the functional form of the AMBER force field, with bond, angle, torsion, Lennard-Jones and Coulomb terms
  - paper: doi:10.1002/jcc.540040211
    title: Bernard R. Brooks et al., CHARMM, a program for macromolecular energy, minimization, and dynamics calculations, Journal of Computational Chemistry 4(2), 1983, 187-217
    locator: the empirical energy function of CHARMM and its use in minimization and dynamics
  - paper: doi:10.1016/S0022-2836(05)80269-4
    title: Manfred J. Sippl, Calculation of conformational ensembles from potentials of mean force, Journal of Molecular Biology 213(4), 1990, 859-883
    locator: the derivation of knowledge-based potentials from the distance distributions in known structures by the inverse Boltzmann relation
  - paper: doi:10.1021/ma00145a039
    title: Sanzo Miyazawa and Robert L. Jernigan, Estimation of effective interresidue contact energies from protein crystal structures, quasi-chemical approximation, Macromolecules 18(3), 1985, 534-552
    locator: the contact energies between residue types, estimated from contact counts with the quasi-chemical approximation
  - paper: doi:10.1021/acs.jctc.7b00125
    title: Rebecca F. Alford et al., The Rosetta all-atom energy function for macromolecular modeling and design, Journal of Chemical Theory and Computation 13(6), 2017, 3031-3048
    locator: the terms of the Rosetta energy function, which mixes physical and statistical terms
  - book: isbn:9780582382107
    title: Andrew R. Leach, Molecular Modelling, Principles and Applications, second edition, Prentice Hall, 2001
    locator: the chapter on empirical force field models (molecular mechanics)
---

An energy function gives each conformation of a molecule a real number, and it should be lowest for the native structure. A program uses it in place of the true free energy that the [thermodynamic hypothesis](/thermodynamic-hypothesis/) talks about. Physics-based energy functions, called force fields, such as AMBER and CHARMM, sum terms for bonds, angles, torsions and pair interactions between atoms. Knowledge-based energy functions, also called statistical potentials or scoring functions, turn the frequencies of features in known structures into energies. Every method of [structure prediction](/protein-structure-prediction/) that searches for a minimum is only as good as its energy function.

## In plain words

A program that folds a protein must be able to compare two shapes and say which one is better. The energy function does this. It looks at a shape and returns one number. A low number means a stable shape, and a high number means a strained or crowded one.

There are two ways to build it. One way follows physics: atoms joined by a bond act like springs, atoms that come too close push each other away, and charged atoms attract or repel. The other way learns from examples: if two kinds of building block touch often in known proteins, touching gets a good score. Both kinds are approximations. A good energy function gives the true shape a better score than any wrong shape, and it is fast enough to compute millions of times.

## The idea

**The general form.** Let $\Omega$ be a set of configurations. An energy function is a map $E : \Omega \to \mathbb{R} \cup \{+\infty\}$, where $+\infty$ marks a forbidden configuration such as a clash. With a temperature $T$, it defines the Boltzmann distribution $p(x) = e^{-E(x)/k_B T} / Z$, where $Z$ is the [partition function](/partition-function/). A minimum of $E$ is a most probable configuration. The same form appears outside biology: the energy of a [Markov random field](/markov-random-field/) in image segmentation is a sum of unary and pair terms, and [graph cuts](/image-segmentation-graph-cuts/) minimize it. Molecular energies are also mostly sums of terms over single atoms and over pairs.

**Force fields.** A molecular mechanics force field such as AMBER (Cornell et al. 1995) writes the potential energy of $N$ atoms at positions $r_1, \ldots, r_N$ as

$$E = \sum_{\text{bonds}} K_r (r - r_{\text{eq}})^2 + \sum_{\text{angles}} K_\theta (\theta - \theta_{\text{eq}})^2 + \sum_{\text{dihedrals}} \frac{V_n}{2} \bigl(1 + \cos(n\phi - \gamma)\bigr) + \sum_{i < j} \left( \frac{A_{ij}}{R_{ij}^{12}} - \frac{B_{ij}}{R_{ij}^{6}} + \frac{q_i q_j}{\varepsilon R_{ij}} \right).$$

The first three sums are over bonded atoms: bond lengths $r$, bond angles $\theta$ and [dihedral angles](/dihedral-angle/) $\phi$. The last sum is over pairs of atoms that are not close in the bond graph, with the distance $R_{ij}$. Its first two terms are the Lennard-Jones repulsion and attraction, and the last is the Coulomb energy of the partial charges $q_i$ and $q_j$. The parameters come from quantum chemistry calculations and from experiments on small molecules. The water is either explicit, as thousands of extra molecules, or implicit, as a continuum term.

**Cost.** The bonded terms take $O(N)$ time. The pair sum has $\Theta(N^2)$ terms. A cutoff distance with a cell list or a neighbour list makes the short-range part $O(N)$ at a fixed density. The long-range Coulomb part is usually computed with Ewald summation on a grid, in $O(N \log N)$ time with the [fast Fourier transform](/fast-fourier-transform/).

**Knowledge-based potentials.** Count how often a feature occurs in a set of known structures, and compare with how often it would occur by chance. For two residue types $a$ and $b$ at distance $r$, Sippl (1990) uses the inverse Boltzmann relation

$$\Delta E_{ab}(r) = -k_B T \ln \frac{f_{ab}(r)}{f(r)},$$

where $f_{ab}(r)$ is the observed frequency of the pair at distance $r$ and $f(r)$ is the frequency in a reference state, for example all pairs of all types. Miyazawa and Jernigan (1985) estimated contact energies between residue types in a similar way. The result is not a true free energy: it depends on the reference state, and the terms are not independent. It works because the features of known structures are those of low free energy.

**What a good energy function needs.**

- **Discrimination.** The native structure has a lower energy than the wrong structures, the decoys, that the search will produce. One measure is the z-score $(E_{\text{nat}} - \bar{E}) / \sigma$ of the native energy against the mean $\bar{E}$ and the standard deviation $\sigma$ of the decoy energies.
- **A useful landscape.** For a search, the energy should also fall toward the native structure from nearby structures, not only be lowest at it. See [energy landscape](/energy-landscape/).
- **Speed.** A Monte Carlo search evaluates the function millions of times. So many methods use a coarse function in an early stage and a detailed one at the end, as [Rosetta](/rosetta/) does.
- **Smoothness.** [Molecular dynamics](/molecular-dynamics/) and gradient minimization need the gradient. A function with a hard cutoff has jumps, and an integrator does not conserve energy across them.

## Examples

**The Lennard-Jones pair.** With $U(r) = 4\epsilon\bigl((\sigma/r)^{12} - (\sigma/r)^6\bigr)$, the energy is 0 at $r = \sigma$, and the minimum is $-\epsilon$ at $r = 2^{1/6} \sigma \approx 1.1225\,\sigma$. Put 8 atoms at the corners of a cube of side $2^{1/6}\sigma$. The 28 pairs are 12 edges, 12 face diagonals and 4 body diagonals, and the sum of their energies is $-15.1033\,\epsilon$. Each edge pair is at the minimum and adds $-\epsilon$, and the diagonal pairs add the rest.

**A torsion term.** The term $\frac{V_3}{2}(1 + \cos 3\phi)$ has its minima where $3\phi = 180°$ modulo $360°$, that is, at $\phi = 60°, 180°$ and $300°$. These are the three staggered positions of a bond between two carbon atoms with four bonds each.

**An inverse Boltzmann energy.** Suppose that a pair of residue types is in contact 120 times in a set of structures, where the reference state predicts 60 contacts. Then $\Delta E = -k_B T \ln 2$. At 300 K, $k_B T = 0.596$ kcal/mol, so $\Delta E = -0.413$ kcal/mol, a favourable contact.

**A decoy test.** Use the [HP model](/hp-model/) energy as the energy function and all 16,268 folds of the sequence HPHPPHHPHH on the square lattice as the decoys. Their energies have mean $-0.513$ and standard deviation $0.666$. The native energy $-4$ has the z-score $(-4 + 0.513)/0.666 = -5.24$. A z-score far below 0 means that the function separates the native fold well from a random fold, but it says nothing about the 24 folds that tie at $-4$.

## Where it is used

- **Molecular dynamics.** A force field gives the forces $-\nabla E$ that the integrator uses. See [molecular dynamics](/molecular-dynamics/).
- **Structure prediction.** [Rosetta](/rosetta/) scores [fragment assembly](/fragment-assembly/) moves with a coarse statistical energy and refines with an all-atom energy that mixes physical and statistical terms (Alford et al. 2017). Threading methods score the fit of a sequence to a fold with contact potentials.
- **Side chains and design.** When the energy is a sum of pair terms over residues, [side-chain packing](/side-chain-packing/) and [protein design](/protein-design/) become discrete pairwise minimization problems, which [dead-end elimination](/dead-end-elimination/) can prune.
- **Model quality assessment.** The same functions rank the models of a prediction server and choose the one to submit.
- **Lattice models.** The [HP model](/hp-model/) is the simplest energy function: minus the number of contacts between hydrophobic residues.

## References
