---
tag: G27EZ3
kind: definition
slug: thermodynamic-hypothesis
name: Thermodynamic hypothesis (Anfinsen's dogma)
aliases:
- Anfinsen's dogma
area: biology/structure-prediction
level: intro
summary: The native fold of a protein is fixed by its sequence and its environment, and it is the state of lowest free energy of the whole system (Anfinsen 1973).
see_also: [protein-structure-prediction, levinthal-paradox, energy-landscape, energy-function, hydrophobic-effect, partition-function, hp-model]
sources:
  - paper: doi:10.1126/science.181.4096.223
    title: Christian B. Anfinsen, Principles that govern the folding of protein chains, Science 181(4096), 1973, 223-230
    locator: the statement of the thermodynamic hypothesis, and the refolding of reduced ribonuclease
  - paper: doi:10.1073/pnas.47.9.1309
    title: Christian B. Anfinsen, Edgar Haber, Michael Sela and F. H. White Jr., The kinetics of formation of native ribonuclease during oxidation of the reduced polypeptide chain, PNAS 47(9), 1961, 1309-1314
    locator: the recovery of enzyme activity when the reduced chain is oxidized again
  - paper: doi:10.1146/annurev.biophys.37.092707.153558
    title: Ken A. Dill, S. Banu Ozkan, M. Scott Shell and Thomas R. Weikl, The protein folding problem, Annual Review of Biophysics 37, 2008, 289-316
    locator: the folding code and the role of the thermodynamic hypothesis in the folding problem
  - book: isbn:9780815344308
    title: Ken A. Dill and Sarina Bromberg, Molecular Driving Forces, second edition, Garland Science, 2011
    locator: the chapters on the Boltzmann distribution and on free energies of states
---

The thermodynamic hypothesis says that the native structure of a protein in its normal environment is the state with the lowest Gibbs free energy of the whole system, protein and solvent together. So the amino acid sequence and the environment fix the native structure, and the cell machinery that made the chain does not. Christian Anfinsen stated it in his Nobel lecture (Anfinsen 1973), from experiments in which an unfolded enzyme folded back to its active form in a test tube. It is the reason why [protein structure prediction](/protein-structure-prediction/) can be posed as a minimization of free energy.

## Definition

Fix a protein sequence $s$ and an environment $c$: the solvent, the pH, the ionic strength, the temperature, and any metal ions or other small molecules that bind. Let $\mathcal{X}$ be the set of microstates of the system, and let $E(x)$ be the energy of a microstate $x$. At temperature $T$, the probability of $x$ at equilibrium is proportional to $e^{-E(x)/k_B T}$, where $k_B$ is the Boltzmann constant.

A *state* (or macrostate) $A \subseteq \mathcal{X}$ is a set of microstates, for example all conformations within a small distance of one structure. Its free energy is

$$G(A) = -k_B T \ln Z_A, \qquad Z_A = \sum_{x \in A} e^{-E(x)/k_B T}.$$

With $Z = \sum_{x \in \mathcal{X}} e^{-E(x)/k_B T}$ the [partition function](/partition-function/), the probability of $A$ is $P(A) = Z_A / Z = e^{-(G(A) - G(\mathcal{X}))/k_B T}$. So, of two disjoint states, the one with the lower free energy is the more probable one. The free energy counts both the energy of the microstates and their number.

**The hypothesis.** For a small globular protein, the native state $N(s, c)$ is the state of lowest free energy:

$$N(s, c) = \arg\min_{A} G(A),$$

where $A$ ranges over the distinct folded states and the unfolded state. The native state is a function of $s$ and $c$ only. It does not depend on the path by which the chain reached it.

Three conditions are usually listed for the hypothesis to hold in practice:

- **Uniqueness.** No other state, folded or unfolded, has a free energy close to $G(N)$. Then $P(N)$ is close to 1 under native conditions.
- **Stability.** Small changes of the environment change $N$ only by small amounts.
- **Kinetic accessibility.** The chain reaches $N$ from the unfolded state in a biological time. This condition is not about free energy at all, and [Levinthal's paradox](/levinthal-paradox/) asks why it holds.

The hypothesis is a statement about equilibrium. It says what the final state is, not how fast it forms.

## Examples and non-examples

**Example: ribonuclease A.** Bovine pancreatic ribonuclease A has 124 residues, with 8 cysteines that form 4 disulfide bonds. Anfinsen and his group unfolded it in 8 M urea and broke the disulfide bonds with a reducing agent, which destroyed the enzyme activity. When they removed the urea and the reducing agent and let air oxidize the cysteines again, the chain recovered its activity (Anfinsen, Haber, Sela and White 1961). The information for the fold was in the chain.

The number of ways to pair 8 cysteines into 4 disulfide bonds is the number of perfect matchings of 8 points:

$$(2k - 1)!! = (2k-1)(2k-3) \cdots 3 \cdot 1, \qquad k = 4: \quad 7 \cdot 5 \cdot 3 \cdot 1 = 105.$$

*Proof of the count.* Let $M_k$ be the number of perfect matchings of $2k$ points. Point 1 has $2k - 1$ possible partners. After it is paired, the other $2k - 2$ points have $M_{k-1}$ matchings, and different partners of point 1 give different matchings. So $M_k = (2k-1) M_{k-1}$ with $M_0 = 1$, which gives $(2k-1)!!$. $\square$

If the bonds formed at random, only 1 chain in 105, about 0.95 percent, would have the native pairing. The native pairing forms because it belongs to the state of lowest free energy. When the reoxidation is done in urea, wrong pairings form, and a trace of reducing agent lets these scrambled forms exchange their bonds and go back to the native pairing (Anfinsen 1973).

**Example: a lattice model.** In the 2D [HP model](/hp-model/), the energy is minus the number of contacts between hydrophobic residues. The sequence HHPPHPPHPPHH has minimum energy $-5$, and only one fold reaches it, up to the rotations and reflections of the square lattice. So it has a unique native state in the sense of the definition. The sequence HPHPPHHPHH has minimum energy $-4$ with 3 different folds, so it fails the uniqueness condition. Both facts come from the enumeration of all self-avoiding walks of these lengths.

**Non-example: insulin.** Insulin is made as one chain, proinsulin, which folds and forms its disulfide bonds. Then a middle segment is cut out, which leaves two chains. When the two chains of mature insulin are separated and reduced, they do not refold well to the native hormone. The native state of insulin is set by the folding of its precursor, not by the free energy of the final two chains.

**Non-example: serpins.** In some serine protease inhibitors, such as plasminogen activator inhibitor 1, the active fold is metastable. The chain can slowly change to a "latent" fold of lower free energy, which is inactive. Here the functional state is a kinetic trap, not the global minimum.

**Non-example: prions and disordered proteins.** The prion protein can take a normal fold or a misfolded form that aggregates, with the same sequence. Intrinsically disordered proteins have no single folded state under native conditions. In both cases there is no unique minimum to predict.

## Related definitions

- **Native state.** The state $N(s, c)$ above. Experiments measure it as an average structure with small fluctuations.
- **Free energy and the partition function.** See [partition function](/partition-function/). A compact state of low energy can lose to a large unfolded state of higher energy when the temperature is high, which is why proteins unfold when they are heated.
- **Energy landscape.** The function $E$ over the conformations, and its shape. A funnel-shaped landscape explains how the native state can be both the global minimum and fast to reach. See [energy landscape](/energy-landscape/).
- **Levinthal's paradox.** The argument that a random search for the native state would take too long. See [Levinthal's paradox](/levinthal-paradox/).
- **Energy function.** A computable function that a program uses in place of the true free energy. See [energy function](/energy-function/).
- **Hydrophobic effect.** The main force that makes the native state compact. See [hydrophobic effect](/hydrophobic-effect/).

## References
