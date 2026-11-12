---
tag: SCSNMH
kind: problem
slug: protein-design
name: Protein design (inverse folding)
aliases:
- Inverse folding
- Computational protein design
- Sequence design
area: biology/structure-prediction
level: advanced
summary: Find an amino acid sequence that folds into a given target structure. The fixed-backbone form, a rotamer optimization over all amino acid types, is NP-hard.
prereqs: [side-chain-packing]
see_also: [rna-inverse-folding, dead-end-elimination, rotamer, protein-structure-prediction, rosetta, energy-function, hp-model, alphafold]
sources:
  - paper: doi:10.1038/301200a0
    title: Carl Pabo, Molecular technology, designing proteins and peptides, Nature 301(5897), 1983, 200
    locator: the design of a sequence for a given structure as the inverse of the folding problem
  - paper: doi:10.1126/science.278.5335.82
    title: Bassil I. Dahiyat and Stephen L. Mayo, De novo protein design, fully automated sequence selection, Science 278(5335), 1997, 82-87
    locator: the fully automated choice of a sequence for a fixed backbone with dead-end elimination, and the experimental test of the design
  - paper: doi:10.1126/science.1089427
    title: Brian Kuhlman, Gautam Dantas, Gregory C. Ireton, Gabriele Varani, Barry L. Stoddard and David Baker, Design of a novel globular protein fold with atomic-level accuracy, Science 302(5649), 2003, 1364-1368
    locator: the design of Top7, a fold not seen in nature, by iterating sequence design and backbone optimization, and its crystal structure
  - paper: doi:10.1093/protein/15.10.779
    title: Niles A. Pierce and Erik Winfree, Protein design is NP-hard, Protein Engineering 15(10), 2002, 779-782
    locator: the NP-hardness of minimizing a pairwise energy over sequences and rotamers on a fixed backbone
  - paper: doi:10.1126/science.add2187
    title: Justas Dauparas, Ivan Anishchenko, Nathaniel Bennett, Hua Bai, Robert J. Ragotte, Lukas F. Milles, Basile I. M. Wicky, Alexis Courbet, Rob J. de Haas, Neville Bethel, Philip J. Y. Leung, Timothy F. Huddy, Sam Pellock, Doug Tischer, F. Chan, Brian Koepnick, Hannah Nguyen, Alex Kang, Banumathi Sankaran, Asim K. Bera, Neil P. King and David Baker, Robust deep learning-based protein sequence design using ProteinMPNN, Science 378(6615), 2022, 49-56
    locator: a neural network that outputs sequences for a given backbone
---

Protein design asks for an amino acid sequence that folds into a given three-dimensional structure. It is the inverse of [protein structure prediction](/protein-structure-prediction/), which asks for the structure of a given sequence, and so it is often called *inverse folding* (Pabo 1983). In the most studied form, the backbone is fixed and the designer chooses, at each position, an amino acid and a [rotamer](/rotamer/) of its side chain so that a pairwise energy is least. This is [side-chain packing](/side-chain-packing/) with a much larger choice at each position, and it is NP-hard (Pierce and Winfree 2002). Dahiyat and Mayo (1997) designed a protein by this method fully automatically, and Kuhlman et al. (2003) designed Top7, a fold that is not known in nature.

## In plain words

Structure prediction starts with a sequence of letters and asks which shape it folds into. Design goes the other way: we draw the shape we want and ask for letters that fold into it.

For each place in the shape, we pick one of the 20 amino acids and a way to point its side chain. Some choices fill the inside of the protein well, some fit the surface, and some pairs of neighbours help each other. The goal is a sequence for which the wanted shape is the best one. It is not enough that the sequence fits the shape well. It must also fit every other shape worse, or the protein will fold into one of those instead.

## Definition

**Fixed-backbone design.** Given a backbone of $n$ residues and, at each position $i$, a set $R_i$ of allowed pairs (amino acid, rotamer), find $x \in R_1 \times \cdots \times R_n$ that minimizes

$$E(x) = \sum_i E_i(x_i) + \sum_{i < j} E_{ij}(x_i, x_j).$$

The sequence is read off from the amino acid types of the chosen rotamers. This is the same combinatorial problem as [side-chain packing](/side-chain-packing/), with $|R_i|$ often in the hundreds because it holds the rotamers of many amino acid types.

**Inverse folding.** Given a target structure $S^*$ and an energy $E(a, S)$ of a sequence $a$ in a structure $S$, find $a$ such that $S^*$ is the structure of least energy of $a$, ideally with a large gap:

$$E(a, S^*) < \min_{S \ne S^*} E(a, S).$$

The first form scores the target only; it is *positive design*. The second also pushes the competing structures up; it is *negative design*. The minimum over all structures $S$ cannot be computed in general, so practice uses the first form, sometimes with a few explicit competitors, and then checks the design by structure prediction and experiment.

## Variants

- **Design of a new fold.** The backbone itself is not given in full. It is chosen together with the sequence, by iterating sequence design and backbone optimization, as for Top7.
- **Partial design.** Only some positions are designed, for example a binding site or the core. The other positions keep their amino acid and only repack.
- **Function design.** Design for binding a target, for catalysis or for a switch between states. The energy then includes the partner or several states.
- **RNA inverse folding.** The same inverse question for RNA secondary structure has its own algorithms ([RNA inverse folding](/rna-inverse-folding/)).
- **Learned design.** A neural network maps the backbone to a distribution over sequences, as in ProteinMPNN (Dauparas et al. 2022).

## Examples

**Positive design is not enough.** Take a toy model with sequences of five residues over H (hydrophobic) and P (polar), and the energy $-1$ for each contact between two H residues and 0 otherwise. The target $S_1$ has the single contact $(1, 4)$; a competitor $S_2$ has the single contact $(2, 5)$.

| sequence | $E(\cdot, S_1)$ | $E(\cdot, S_2)$ | folds to $S_1$? |
|---|---|---|---|
| HHHHH | $-1$ | $-1$ | no, a tie |
| HPPHP | $-1$ | 0 | yes, gap 1 |
| HHPHH | $-1$ | $-1$ | no, a tie |
| PHPPH | 0 | $-1$ | no, folds to $S_2$ |

The sequences with $a_1 = a_4 = \mathrm{H}$ all reach the least energy $-1$ on $S_1$, and there are $2^3 = 8$ of them. Positive design alone cannot tell them apart. Two of them, those with also $a_2 = a_5 = \mathrm{H}$, are equally happy in $S_2$, so only the 6 others are specific. Negative design picks one of these 6.

**The size of the choice.** With 20 amino acids at each of 100 positions there are $20^{100} \approx 1.3 \times 10^{130}$ sequences, before any rotamers. Exhaustive search is out of the question, and the methods rely on pruning and on the sparse contacts of the backbone.

## Known algorithms

- **[Dead-end elimination](/dead-end-elimination/) and A\*.** Remove rotamers, and with them amino acids, that cannot be in the optimum, then search the rest exactly. Dahiyat and Mayo (1997) used DEE to find the global optimum of their design energy.
- **Monte Carlo with simulated annealing.** Change one rotamer or one amino acid at a time and accept by the Metropolis rule at a falling temperature. Rosetta uses this for its packer; it gives no certificate but scales to large designs.
- **Exact methods on sparse graphs.** Tree decomposition and integer programming, as for [side-chain packing](/side-chain-packing/).
- **Iterating sequence and backbone.** Kuhlman et al. (2003) alternated sequence design on a fixed backbone with backbone relaxation for the new sequence, and so designed the new fold Top7. Its crystal structure matched the design model closely.
- **Deep learning.** ProteinMPNN predicts sequences for a backbone in one pass of a network and is checked by structure prediction, for example with [AlphaFold](/alphafold/).

## Bounds

- **NP-hard.** Pierce and Winfree (2002) proved that fixed-backbone design with a pairwise energy is NP-hard. Since side-chain packing is the special case with one amino acid type per position, hardness also follows from the 3-coloring reduction on the [side-chain packing](/side-chain-packing/) page.
- **Polynomial for bounded treewidth.** Given a tree decomposition of width $w$ of the interaction graph, the optimum takes $O(n p^{w+1})$ time for $p$ choices per position, with $p$ now counting all rotamers of all allowed amino acids.
- **Inverse folding is harder to even state exactly.** Checking that $S^*$ is the best structure of a sequence is itself a structure prediction problem over all conformations, so no exact algorithm for the full inverse problem is known for realistic energies.

## Reductions

- **To side-chain packing.** Fixed-backbone design is side-chain packing with the union of the rotamer sets of the allowed amino acid types at each position.
- **To MAP inference.** As for packing, the optimum is the most probable assignment of a pairwise Markov random field with $P(x) \propto e^{-E(x)}$.
- **Inverse of structure prediction.** A design is accepted if structure prediction maps the sequence back to the target, so a predictor is the check of a design method.

## Applications

- **New proteins.** Stable folds, including folds not seen in nature such as Top7.
- **Binders and vaccines.** Proteins that bind a given target, and protein cages and scaffolds that present antigens.
- **Enzymes and sensors.** Active sites placed on stable scaffolds, and proteins that change shape on a signal.
- **Stabilization.** Mutations that make a natural protein more stable or more soluble, chosen by design on its known structure.

## References
