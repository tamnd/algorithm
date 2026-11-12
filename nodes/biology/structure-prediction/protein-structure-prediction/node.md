---
tag: 3A4XR2
kind: problem
slug: protein-structure-prediction
name: Protein structure prediction
aliases:
- Tertiary structure prediction
- Protein folding prediction
area: biology/structure-prediction
level: intro
summary: Predict the 3D coordinates of a protein's native fold from its amino acid sequence. Exact versions in simple lattice models are NP-complete, and practical methods are heuristics or learned systems.
prereqs: [thermodynamic-hypothesis]
see_also: [ab-initio-protein-folding, comparative-modeling, protein-threading, alphafold, hp-model, hp-folding-np-completeness, energy-function, rna-secondary-structure-prediction]
sources:
  - paper: doi:10.1126/science.1219021
    title: Ken A. Dill and Justin L. MacCallum, The protein-folding problem, 50 years on, Science 338(6110), 2012, 1042-1046
    locator: the three questions of the folding problem (the folding code, the folding mechanism and structure prediction), and the progress of prediction methods
  - paper: doi:10.1146/annurev.biophys.37.092707.153558
    title: Ken A. Dill, S. Banu Ozkan, M. Scott Shell and Thomas R. Weikl, The protein folding problem, Annual Review of Biophysics 37, 2008, 289-316
    locator: the definition of the folding problem as three problems, and the physical and the knowledge-based routes to prediction
  - paper: doi:10.1002/prot.340230303
    title: John Moult, Jan T. Pedersen, Richard Judson and Krzysztof Fidelis, A large-scale experiment to assess protein structure prediction methods, Proteins 23(3), 1995
    locator: the design of CASP, a blind test on structures that are not yet public
  - paper: doi:10.1038/s41586-021-03819-2
    title: John Jumper et al., Highly accurate protein structure prediction with AlphaFold, Nature 596, 2021, 583-589
    locator: the AlphaFold network and its results in CASP14
  - book: isbn:9780815323051
    title: Carl Branden and John Tooze, Introduction to Protein Structure, second edition, Garland, 1999
    locator: the chapter on the prediction, engineering and design of protein structures
  - book: isbn:9780198716846
    title: Arthur M. Lesk, Introduction to Protein Science, third edition, Oxford University Press, 2016
    locator: the chapter on protein structure prediction and the classes of prediction methods
---

Protein structure prediction is the problem of computing the three-dimensional structure of a protein from its amino acid sequence alone. The [thermodynamic hypothesis](/thermodynamic-hypothesis/) says that the sequence fixes the native structure, so the answer exists, but the hypothesis gives no fast way to compute it. Exact versions of the problem in simple lattice models are [NP-complete](/hp-folding-np-completeness/). The methods in use are heuristics or learned systems with no worst-case guarantee, and they are judged by blind tests against structures from experiment.

## In plain words

A protein is a chain of small building blocks, and there are 20 kinds of block. A cell makes the chain as a straight string, and then the chain folds by itself into one compact shape. The shape decides what the protein does. Experiments can measure the shape, but they are slow and costly, while reading the string is cheap.

Structure prediction asks a computer to go from the string to the shape. One way is to copy the shape of a known protein with a similar string. Another way is to model the physics: give each possible shape a score for how stable it is, and search for the best shape. The number of possible shapes is so large that no program can try them all, so every method uses shortcuts, and none of them is sure to be right.

## Definition

**Input.** A sequence $s = s_1 s_2 \cdots s_n \in \Sigma^n$, where $\Sigma$ is the set of the 20 standard amino acids and $n$ is the number of residues.

**Conformation.** A conformation $X$ of $s$ gives a point in $\mathbb{R}^3$ to each atom of the chain. The bond lengths and the bond angles are almost fixed, so a conformation is in practice given by its internal coordinates: the backbone [dihedral angles](/dihedral-angle/) $\phi_i, \psi_i, \omega_i$ of each residue and the side-chain angles $\chi$. A coarse model keeps only the $\text{C}_\alpha$ atom of each residue, so $X \in \mathbb{R}^{3n}$, with about 3.8 Å between consecutive $\text{C}_\alpha$ atoms. Two conformations are the same structure when a rotation and a translation map one to the other. A mirror image is a different structure, because the amino acids are chiral.

**Energy version.** Given $s$ and an [energy function](/energy-function/) $E_s$ on the set $\Omega(s)$ of valid conformations, find

$$X^\ast = \arg\min_{X \in \Omega(s)} E_s(X).$$

Under the thermodynamic hypothesis, $X^\ast$ is the native structure when $E_s$ is the true free energy. With any energy function that a program can compute, $X^\ast$ is only a model of the native structure.

**Blind version.** Given $s$, output a conformation $X$. The score is a distance $d(X, X_{\text{nat}})$ to the structure $X_{\text{nat}}$ from an experiment (X-ray crystallography, NMR or cryo-electron microscopy), which the predictor does not see. Common scores are the [RMSD](/rmsd/) in Å after the best superposition, the [GDT_TS](/gdt-ts/) and the [TM-score](/tm-score/) in $[0, 1]$.

## Variants

- **Secondary structure prediction.** Assign each residue to a helix, a strand or a coil. See [protein secondary structure prediction](/protein-secondary-structure-prediction/). This is a labelling of the sequence, not a set of coordinates.
- **Contact prediction.** Predict which pairs of residues are close in space, that is, the [contact map](/contact-map/). See [contact map prediction](/contact-map-prediction/) and [direct coupling analysis](/direct-coupling-analysis/).
- **Template-based modelling.** When a protein of known structure has a similar sequence, copy and adapt its structure. See [comparative modelling](/comparative-modeling/). When the sequence similarity is too low to detect, find a known fold that fits the sequence. See [protein threading](/protein-threading/) and [fold recognition](/protein-fold-recognition/).
- **Template-free modelling.** Predict the fold from the sequence and an energy function only. See [ab initio protein folding](/ab-initio-protein-folding/).
- **Lattice models.** Put the residues on the sites of a lattice and use a very simple energy. The [HP model](/hp-model/) is the standard one. Here the energy version has an exact definition, so its complexity can be studied.
- **Fixed backbone.** Keep the backbone and choose only the side-chain shapes. See [side-chain packing](/side-chain-packing/). The inverse problem, which finds a sequence for a given structure, is [protein design](/protein-design/).
- **RNA.** The same question for RNA is usually asked about base pairs, not coordinates. Without pseudoknots, [RNA secondary structure prediction](/rna-secondary-structure-prediction/) has exact polynomial dynamic programs, which is a large difference from the protein case.

## Examples

**A lattice instance with an exact answer.** In the 2D HP model, take the sequence HPHPPHHPHH with $n = 10$. A conformation is a [self-avoiding walk](/self-avoiding-walk-enumeration/) of 9 steps on the square lattice, and there are 16,268 such walks. The energy is minus the number of contacts between H residues that are not chain neighbours. Enumeration of all 16,268 walks gives the minimum energy $-4$. It is reached by 24 walks, which are 3 different folds up to the 8 rotations and reflections of the lattice. Here the prediction problem is solved exactly, but the cost of the enumeration grows exponentially with $n$.

**The size of a real search.** If each residue of a chain of 100 residues has only 3 backbone states, there are $3^{100} \approx 5.2 \times 10^{47}$ conformations. This is the argument of [Levinthal's paradox](/levinthal-paradox/). A program cannot list them, so every practical method samples a tiny part of the space.

**A blind test.** In CASP, the organizers collect sequences of proteins whose structures are being solved but are not yet public. Groups submit models, and after the release the models are scored against the experimental structures with GDT_TS and other measures. A method cannot tune itself on the answer, so the test measures real predictive power.

## Known algorithms

| approach | what it uses | guarantee |
|---|---|---|
| [comparative modelling](/comparative-modeling/), for example [MODELLER](/modeller/) | an alignment to a template of known structure | none; the model is as good as the template and the alignment |
| [threading](/protein-threading/) and [I-TASSER](/i-tasser/) | a library of known folds and a fit score | none |
| [fragment assembly](/fragment-assembly/) in [Rosetta](/rosetta/) | short pieces of known structures and Monte Carlo search | none; a heuristic |
| [molecular dynamics](/molecular-dynamics/) | a physical force field and Newton's equations | an accurate trajectory only for a short time; folding needs very long runs |
| [AlphaFold](/alphafold/) | a neural network trained on known structures and sequence alignments | none; a learned system |
| exhaustive search in the [HP model](/hp-model/) | enumeration of all lattice conformations | exact, in exponential time |

CASP has run every two years since 1994. The deep learning methods of CASP13 and CASP14 made a large step in accuracy, and AlphaFold in CASP14 often gave models close to the experimental structures (Jumper et al. 2021).

## Bounds

- **Exhaustive search.** On a lattice, the number of conformations of a chain of $n$ residues grows as $\mu^{n + o(n)}$, where $\mu$ is the connective constant of the lattice, about 2.638 for the square lattice and about 4.684 for the cubic lattice. So [brute force](/brute-force-search/) takes exponential time.
- **Hardness.** The decision version of HP folding is NP-complete on the square lattice (Crescenzi et al. 1998) and on the cubic lattice (Berger and Leighton 1998). See [NP-completeness of HP folding](/hp-folding-np-completeness/). So no polynomial-time exact algorithm exists for these models unless $\text{P} = \text{NP}$.
- **Approximation.** For the HP model there are polynomial-time algorithms with a constant [approximation ratio](/approximation-ratio/) on the number of contacts. For realistic energy functions no such guarantee is known.
- **What hardness does not say.** The hardness results are for the worst case over all sequences. Natural proteins are the product of evolution, and many small ones fold in microseconds to seconds, so the hard instances may not occur in nature. See [energy landscape](/energy-landscape/).

## Reductions

- **To optimization.** By the thermodynamic hypothesis, prediction reduces to the [global minimization](/global-optimization/) of a free energy over the conformations. The task then splits into two parts: an accurate energy function and a search that can find its minimum. Each part can fail on its own.
- **From HP folding.** Each exact algorithm for the energy version, with an energy function that contains the HP energy as a special case, solves HP folding. This is how the lattice results give hardness for the general problem.
- **To side-chain packing.** With a fixed backbone and a discrete set of [rotamers](/rotamer/), the rest of the problem is a minimization over rotamer choices with pair energies. This minimization is NP-hard in general, and [dead-end elimination](/dead-end-elimination/) is an exact method that is often fast on proteins.

## Applications

- Guess the function of a protein from the shape of its fold and of its active site.
- Find where a drug can bind, and screen candidate molecules against a predicted pocket.
- Read the effect of a mutation: a change in a buried residue can break the fold.
- Plan experiments: a predicted model can help to solve a crystal structure by molecular replacement.
- Design new proteins, which needs an energy function that is good enough to predict the fold of the designed sequence.

## References
