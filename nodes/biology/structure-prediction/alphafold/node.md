---
tag: VWHHRT
kind: algorithm
slug: alphafold
name: AlphaFold
aliases:
- AlphaFold 2
- AlphaFold2
area: biology/structure-prediction
level: research
summary: A deep network that maps a sequence and its alignment to atomic coordinates, through Evoformer blocks and a structure module, and scores each residue by pLDDT.
solves: [protein-structure-prediction]
model: real-ram
complexity:
  vars: {n: the number of residues, s: the number of alignment sequences in the main stack}
  time: {worst: "O(s^2 n + s n^2 + n^3)"}
  space: {extra: "O(s n + n^2)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2020
  people: [John Jumper, Demis Hassabis]
  note: DeepMind entered AlphaFold 2 in CASP14 in 2020, and Jumper et al. described it in Nature in 2021. AlphaFold 1 (Senior et al. 2020) had predicted distance distributions for CASP13, and AlphaFold 3 (Abramson et al. 2024) extended the method to complexes with nucleic acids and small molecules.
prereqs: [multiple-sequence-alignment, contact-map-prediction]
see_also: [direct-coupling-analysis, i-tasser, rosetta, protein-design, gdt-ts, tm-score, rmsd, fragment-assembly]
sources:
  - paper: doi:10.1038/s41586-021-03819-2
    title: John Jumper et al., Highly accurate protein structure prediction with AlphaFold, Nature 596(7873), 2021, 583-589
    locator: the Evoformer, the structure module with invariant point attention, recycling, pLDDT, and the CASP14 accuracy of 0.96 Å median backbone r.m.s.d.95 against 2.8 Å for the next best method
  - paper: doi:10.1002/prot.26257
    title: John Jumper et al., Applying and improving AlphaFold at CASP14, Proteins 89(12), 2021, 1711-1721
    locator: the CASP14 entry and its median domain GDT_TS of 92.4
  - paper: doi:10.1038/s41586-019-1923-7
    title: Andrew W. Senior et al., Improved protein structure prediction using potentials from deep learning, Nature 577(7792), 2020, 706-710
    locator: AlphaFold 1, distance distributions from a deep residual network and their use as a potential
  - paper: doi:10.1038/s41586-024-07487-w
    title: Josh Abramson et al., Accurate structure prediction of biomolecular interactions with AlphaFold 3, Nature 630(8016), 2024, 493-500
    locator: AlphaFold 3, with a diffusion module for the coordinates and inputs that include nucleic acids, ligands and ions
  - paper: doi:10.1093/bioinformatics/btt473
    title: Valerio Mariani, Marco Biasini, Alessandro Barbato and Torsten Schwede, lDDT, a local superposition-free score for comparing protein structures and models using distance difference tests, Bioinformatics 29(21), 2013, 2722-2728
    locator: the definition of lDDT, with the inclusion radius of 15 Å and the thresholds 0.5, 1, 2 and 4 Å
  - paper: doi:10.1002/prot.26237
    title: Andriy Kryshtafovych, Torsten Schwede, Maya Topf, Krzysztof Fidelis and John Moult, Critical assessment of methods of protein structure prediction (CASP), Round XIV, Proteins 89(12), 2021, 1607-1617
    locator: the overview of CASP14 and the results of its predictors
  - paper: doi:10.1126/science.abj8754
    title: Minkyung Baek et al., Accurate prediction of protein structures and interactions using a three-track neural network, Science 373(6557), 2021, 871-876
    locator: RoseTTAFold, a network with one-dimensional, two-dimensional and three-dimensional tracks
  - paper: doi:10.1126/science.ade2574
    title: Zeming Lin et al., Evolutionary-scale prediction of atomic-level protein structure with a language model, Science 379(6637), 2023, 1123-1130
    locator: ESMFold, structure prediction from a single sequence with a protein language model
---

AlphaFold is a deep neural network from DeepMind that predicts the three-dimensional structure of a protein from its amino acid sequence. This page is about AlphaFold 2 (Jumper et al. 2021), the version that won CASP14 in 2020. It reads the sequence, a [multiple sequence alignment](/multiple-sequence-alignment/) of its homologues and, when they exist, template structures. A stack of *Evoformer* blocks refines a representation of the alignment and a representation of all residue pairs. A *structure module* then places each residue as a rigid frame in space with *invariant point attention*, and the whole network runs again on its own output (*recycling*). For each residue it also predicts its own error, as *pLDDT*, an estimate of the lDDT score that the prediction would get against the true structure. The network has millions of trained parameters and needs large training data and compute, so the implementation of this page computes lDDT and pLDDT, the measure by which AlphaFold reports its confidence.

## In plain words

Take a protein's sequence and a stack of related sequences from other species. The stack holds clues about which parts of the chain touch, as the [direct coupling analysis](/direct-coupling-analysis/) page explains. AlphaFold is a large network trained on known protein structures to turn these clues into a 3D shape.

Inside, it keeps two tables: one about the stack of sequences, and one about every pair of residues, a bit like a rough map of which residues are near which. Many rounds pass information back and forth between the two tables, with checks that the pair map is consistent, like a triangle that must close. A last part builds the chain in space, one rigid piece per residue, and then the whole process runs again on its own answer.

It also tells you, for each residue, how much to trust the result, on a scale from 0 to 100.

## The problem

**Input.** A sequence of $n$ residues, an alignment of homologous sequences, and optionally template structures with their alignments.

**Output.** Coordinates of all heavy atoms, and for each residue $i$ a confidence $\mathrm{pLDDT}_i \in [0, 100]$. AlphaFold also outputs a predicted aligned error between residue pairs, a distogram and a predicted TM-score.

**Measure of success.** In CASP the predictions are compared with experimental structures by [GDT_TS](/gdt-ts/), by lDDT, by [RMSD](/rmsd/) and by other scores. lDDT, the score behind pLDDT, works as follows (Mariani et al. 2013). For a model $x$ and a reference $x^0$, a pair of residues $(i, j)$, $i \ne j$, is scored if the reference distance $d^0_{ij}$ between their $C_\alpha$ atoms is below $R_0 = 15$ Å. The pair is *preserved* at threshold $t$ if $|d_{ij} - d^0_{ij}| < t$, for $t \in T = \{0.5, 1, 2, 4\}$ Å. The lDDT of residue $i$ is the fraction of its (pair, threshold) tests that pass:

$$\mathrm{lDDT}_i = \frac{1}{|T|\,|P_i|} \sum_{t \in T} \big|\{ j \in P_i : |d_{ij} - d^0_{ij}| < t \}\big|, \qquad P_i = \{ j \ne i : d^0_{ij} < R_0 \}.$$

No superposition is needed, so a model with two correct domains in a wrong relative orientation still scores well on each domain. The lDDT of Mariani et al. uses all atoms; AlphaFold predicts the $C_\alpha$ form shown here.

## The algorithm

AlphaFold 2 at inference, at the level of its parts (Jumper et al. 2021):

```pseudo id=pipeline
ALPHAFOLD(a, A, templates)
P1  m ← embed the sequences of the alignment A;  z ← embed all pairs of residues of a, with template features
P2  for cycle ← 1 to N_cycle do                                    ▷ recycling
P3      add the embedded outputs of the previous cycle to m and z
P4      for each of the 48 Evoformer blocks do
P5          m ← row attention over residues biased by z, then column attention over sequences
P6          z ← z + outer product mean of m                         ▷ alignment to pairs
P7          z ← triangle multiplicative updates and triangle attention on z
P8      frames, angles ← structure module with invariant point attention on (first row of m, z)
P9  x ← atom coordinates from frames and torsion angles
P10 return x, pLDDT from the confidence head
```

**The Evoformer** keeps the alignment representation $m$ ($s \times n$ vectors) and the pair representation $z$ ($n \times n$ vectors). Line P5 lets each sequence attend along the chain, with attention weights biased by the pair representation, and each column attend across the sequences. Line P6 sends coevolution information from the alignment to the pairs. Line P7 updates the edge $(i, j)$ from the edges $(i, k)$ and $(k, j)$ of every third residue $k$: a pair map that describes real distances must satisfy the triangle inequality, and these updates let the network learn such consistency.

**The structure module** treats each residue as a rigid frame, a rotation and a translation, all starting at the origin. Invariant point attention mixes the residue features by attention over the pair representation and over points placed in the local frames of the residues. The result does not change under a global rotation and translation, so the network does not need to learn the arbitrary orientation of the protein. Each block then updates every frame, and side chains come from predicted torsion angles.

**Training** uses a frame aligned point error loss on the coordinates, auxiliary losses (among them a distogram and a masked alignment task), and the confidence loss below. The training set holds structures from the Protein Data Bank and, by self-distillation, high-confidence predictions of the network for sequences without structures.

**The confidence head** gives, for each residue, a distribution over 50 bins of the lDDT-$C_\alpha$ of the predicted structure against the truth. It is trained with cross-entropy against the binned true value, and the reported pLDDT is the mean of the distribution. This part, together with lDDT itself, is the main pseudocode and the implementation:

```pseudo id=main
LDDT-CA(x, x⁰, R₀, T)                  ▷ model x, reference x⁰, R₀ = 15 Å, T = (0.5, 1, 2, 4) Å
L1  for each residue i do
L2      P_i ← {j ≠ i : ‖x⁰_i − x⁰_j‖ < R₀}                           ▷ the reference chooses the pairs
L3      δ_ij ← | ‖x_i − x_j‖ − ‖x⁰_i − x⁰_j‖ | for each j in P_i
L4      s_i ← Σ_{t ∈ T} |{j ∈ P_i : δ_ij < t}| / (|T| |P_i|)
L5  S ← Σ_i Σ_{t ∈ T} |{j ∈ P_i : δ_ij < t}| / (|T| Σ_i |P_i|)            ▷ all scored pairs pooled
L6  return S, (s_1, ..., s_n)
PLDDT(z_1, ..., z_n)                   ▷ z_i: the 50 logits of the confidence head for residue i
L7  for each residue i do p_i ← softmax(z_i)
L8      pLDDT_i ← 100 · Σ_{k=0..49} p_ik (k + 1/2) / 50
L9  return (pLDDT_1, ..., pLDDT_n)
```

A residue with no scored pair has no lDDT; the implementation returns `None` for it. The training target of residue $i$ is the bin $\lfloor 50 \, \mathrm{lDDT}_i \rfloor$, capped at 49.

## Example

**lDDT by hand.** The reference has four $C_\alpha$ atoms on a line at $(0, 0, 0)$, $(3.8, 0, 0)$, $(7.6, 0, 0)$ and $(11.4, 0, 0)$. The model is the same except that residue 4 is at $(9.4, 3.0, 0)$. All six reference distances are below 15 Å, so all pairs are scored. The pairs among residues 1 to 3 have deviation 0 and pass all four tests. The pairs with residue 4:

| pair | $d^0$ | $d$ | $\lvert d - d^0 \rvert$ | tests passed |
|---|---|---|---|---|
| (1, 4) | 11.4 | 9.867 | 1.533 | 2 of 4 (at 2 and 4 Å) |
| (2, 4) | 7.6 | 6.353 | 1.247 | 2 of 4 |
| (3, 4) | 3.8 | 3.499 | 0.301 | 4 of 4 |

Residue 4 passes $2 + 2 + 4 = 8$ of its 12 tests, so $\mathrm{lDDT}_4 = 0.667$. Residues 1 and 2 pass 10 of 12, $0.833$, and residue 3 passes all 12, $1$. The global score pools the 24 tests of the 6 pairs, of which 20 pass, so $S = 5/6 = 0.833$. Each unordered pair is counted from both ends, which does not change the pooled fraction.

**pLDDT from logits.** Suppose the head of one residue puts probability $0.5$ on bin 44, $0.3$ on bin 45 and $0.2$ on bin 40, and 0 elsewhere. The bin centres are $(k + 1/2)/50$, so the three bins stand for lDDT values $0.89$, $0.91$ and $0.81$, and $\mathrm{pLDDT} = 100 (0.5 \cdot 0.89 + 0.3 \cdot 0.91 + 0.2 \cdot 0.81) = 88.0$. A flat head, equal logits in all bins, gives 50.

## Correctness

AlphaFold has no proof of correctness: it is a trained model, and its accuracy is an experimental result. The CASP14 assessment found a median backbone accuracy of 0.96 Å r.m.s.d.95 ($C_\alpha$ RMSD over the best 95% of residues) against 2.8 Å for the next best method (Jumper et al. 2021, Nature), and a median domain GDT_TS of 92.4 (Jumper et al. 2021, Proteins). DeepMind's announcement of the result gave a median GDT_TS of 87.0 on the free-modelling targets, those without a usable template; the two medians are over different sets of targets and should not be mixed.

What can be proved is that the implemented parts compute what they claim. The [proof](proofs/correctness.md) shows that lDDT lies in $[0, 1]$, is 1 for a model identical to the reference up to a rigid motion, does not change under a rotation or translation of the model, and does not see a mirror image; and that pLDDT is the expected value of the bin centres under the predicted distribution, so it lies in $[1, 99]$, and that the cross-entropy loss is positive and tends to 0 only as the head puts all its mass on the true bin. The tests check lDDT against a direct count of the (pair, threshold) tests in exact arithmetic, and pLDDT against a direct sum.

## Complexity

The implemented lDDT computes $O(n^2)$ distances and takes $O(n^2)$ time and $O(n)$ extra space; pLDDT takes $O(n b)$ time for $b = 50$ bins.

The network has a fixed number of blocks, so its cost per cycle is the cost of one Evoformer block times 48 plus the structure module. Row attention in line P5 costs $O(s n^2)$, column attention $O(s^2 n)$, the outer product mean $O(s n^2)$, and the triangle updates and triangle attention of line P7 cost $O(n^3)$. The structure module costs $O(n^2)$ per block. So a cycle takes $O(s^2 n + s n^2 + n^3)$ time, with constants set by the widths of the representations. The pair representation needs $O(n^2)$ memory, and the attention of line P7 needs $O(n^3)$ unless it is computed in chunks; the stated space assumes chunking. The cubic term limits the length of a single prediction, and long proteins are often cut into domains or cropped.

## Properties

- **Not deterministic in general.** The alignment is clustered and sampled at random for each cycle, so runs with different seeds can differ. With a fixed seed and the same inputs, a run is repeatable.
- **Not exact.** It is a learned approximation and has no guarantee for any input.
- **Equivariant structure module.** If all residue frames move by the same rigid motion, the attention weights of invariant point attention do not change and the output moves by that motion.
- **Self-assessing.** pLDDT and the predicted aligned error come with every prediction, and Jumper et al. (2021) show that pLDDT tracks the true lDDT-$C_\alpha$ of the predictions.
- **Superposition-free confidence.** pLDDT estimates a local score, so it says how well each residue's neighbourhood is predicted, not whether the domains are placed correctly relative to each other; the predicted aligned error covers that.

## Variants and improvements

- **AlphaFold 1.** Senior et al. (2020) trained a deep residual network to predict a distribution of distances (a distogram) and torsion angles, and folded the chain by gradient descent on the resulting potential. It led CASP13 in 2018.
- **AlphaFold-Multimer.** A version of AlphaFold 2 retrained on complexes of several chains.
- **AlphaFold 3.** Abramson et al. (2024) replaced the Evoformer by a *Pairformer*, which processes the alignment much less, and the structure module by a diffusion model that outputs atom coordinates directly. Its inputs include DNA, RNA, ligands, ions and modified residues.
- **RoseTTAFold.** Baek et al. (2021) built a network with three tracks, for the sequence, the pairs and 3D coordinates, which exchange information in each block.
- **ESMFold.** Lin et al. (2023) replaced the alignment by the internal states of a protein language model, which makes prediction from a single sequence fast, at some cost in accuracy.

## When to use it

Use AlphaFold for the structure of a single protein chain, or a complex with the Multimer version, when an alignment of homologues can be built. It is the default first step in most modern structural work, and its pLDDT tells you which regions to trust. A predicted structure is a hypothesis. For a binding site, a drug design or a mechanism that depends on details of a few ångströms, check the regions that matter against experiment. For designed proteins it serves as a test of a design: does the designed sequence fold back to the intended structure? See [protein design](/protein-design/).

## Pitfalls

- **Shallow alignments.** The accuracy drops when the alignment has few effective sequences; Jumper et al. (2021) report a strong fall below about 30. Orphan proteins and some designed or viral proteins are hard cases.
- **One static structure.** The output is a single structure. Proteins with several states, induced fits or large motions get one of the states or an average, with no sign of the others.
- **Low pLDDT is not a structure.** Regions with pLDDT below about 50 are often disordered in reality, and the network places them as extended loops or ribbons. These coordinates have no meaning and should not be read as a prediction of a conformation.
- **No ligands, no environment in AlphaFold 2.** Cofactors, metals, membranes and partners are absent, so the structure of a protein that folds only with them may be wrong or right for the wrong reason.
- **Point mutations.** The network was not trained to predict the effect of a single mutation, and the predicted structures of a protein and a destabilized mutant are often the same.
- **Mirror images and local scores.** lDDT, and so pLDDT, sees only distances. A high pLDDT does not exclude a wrong handedness of a part or a wrong placement of domains; use the predicted aligned error for the second.
- **Template leakage in benchmarks.** Tests on structures that were in the training set, or close to them, overstate the accuracy on new folds.

## Implementations

## History

Structure prediction from coevolution and deep learning grew through the 2010s: [direct coupling analysis](/direct-coupling-analysis/) gave contact maps from alignments, and deep residual networks made them far more precise (see [contact map prediction](/contact-map-prediction/)). At CASP13 in 2018, AlphaFold 1 predicted full distance distributions and folded proteins by minimizing a potential built from them (Senior et al. 2020). At CASP14 in 2020, AlphaFold 2 replaced the separate folding step with an end-to-end network and reached accuracies close to those of experiment for many targets (Kryshtafovych et al. 2021; Jumper et al. 2021). RoseTTAFold followed in 2021, ESMFold in 2023 and AlphaFold 3 in 2024. In 2024 Demis Hassabis and John Jumper shared half of the Nobel Prize in Chemistry for this work.

## References
