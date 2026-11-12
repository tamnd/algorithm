---
tag: E9WEGD
kind: problem
slug: contact-map-prediction
name: Contact map prediction
aliases:
- Residue contact prediction
area: biology/structure-prediction
level: advanced
summary: Predict which pairs of residues are in spatial contact from the sequence and its alignment. Judged by the precision of the top L/5 long-range predictions.
prereqs: [contact-map, multiple-sequence-alignment]
see_also: [direct-coupling-analysis, alphafold, precision-and-recall, potts-model, gaussian-graphical-model, ab-initio-protein-folding, protein-structure-prediction, rosetta]
sources:
  - paper: doi:10.1002/prot.340180402
    title: Ulrike Göbel, Chris Sander, Reinhard Schneider and Alfonso Valencia, Correlated mutations and residue contacts in proteins, Proteins 18(4), 1994, 309-317
    locator: the prediction of contacts from correlated mutations in a multiple sequence alignment
  - paper: doi:10.1093/bioinformatics/btm604
    title: Stanley D. Dunn, Lindi M. Wahl and Gregory B. Gloor, Mutual information without the influence of phylogeny or entropy dramatically improves residue contact prediction, Bioinformatics 24(3), 2008, 333-340
    locator: the average product correction of covariation scores
  - paper: doi:10.1073/pnas.1111471108
    title: Faruck Morcos, Andrea Pagnani, Bryan Lunt, Arianna Bertolino, Debora S. Marks, Chris Sander, Riccardo Zecchina, José N. Onuchic, Terence Hwa and Martin Weigt, Direct-coupling analysis of residue coevolution captures native contacts across many protein families, PNAS 108(49), 2011, E1293-E1301
    locator: mean-field direct coupling analysis and its contact predictions across many families
  - paper: doi:10.1371/journal.pone.0028766
    title: Debora S. Marks, Lucy J. Colwell, Robert Sheridan, Thomas A. Hopf, Andrea Pagnani, Riccardo Zecchina and Chris Sander, Protein 3D structure computed from evolutionary sequence variation, PLoS One 6(12), 2011, e28766
    locator: folding proteins with predicted contacts as distance restraints
  - paper: doi:10.1103/PhysRevE.87.012707
    title: Magnus Ekeberg, Cecilia Lövkvist, Yueheng Lan, Martin Weigt and Erik Aurell, Improved contact prediction in proteins, using pseudolikelihoods to infer Potts models, Physical Review E 87(1), 2013, 012707
    locator: pseudo-likelihood DCA and its comparison with mean-field DCA
  - paper: doi:10.1093/bioinformatics/btr638
    title: David T. Jones, Daniel W. A. Buchan, Domenico Cozzetto and Massimiliano Pontil, PSICOV, precise structural contact prediction using sparse inverse covariance estimation on large multiple sequence alignments, Bioinformatics 28(2), 2012, 184-190
    locator: contact prediction by a sparse inverse covariance estimate
  - paper: doi:10.1371/journal.pcbi.1005324
    title: Sheng Wang, Siqi Sun, Zhen Li, Renyu Zhang and Jinbo Xu, Accurate de novo prediction of protein contact map by ultra-deep learning model, PLoS Computational Biology 13(1), 2017, e1005324
    locator: RaptorX-Contact, a deep residual network on sequence profiles and coevolution features
  - paper: doi:10.1038/s41586-019-1923-7
    title: Andrew W. Senior, Richard Evans, John Jumper, James Kirkpatrick, Laurent Sifre, Tim Green, Chongli Qin, Augustin Žídek, Alexander W. R. Nelson, Alex Bridgland, Hugo Penedones, Stig Petersen, Karen Simonyan, Steve Crossan, Pushmeet Kohli, David T. Jones, David Silver, Koray Kavukcuoglu and Demis Hassabis, Improved protein structure prediction using potentials from deep learning, Nature 577(7792), 2020, 706-710
    locator: the prediction of distance distributions between residues and their use as a potential
---

Contact map prediction asks, for a protein sequence of length $L$, which of its $L(L-1)/2$ residue pairs are in contact in the folded structure. A contact usually means that the $C_\beta$ atoms ($C_\alpha$ for glycine) are less than 8 Å apart, as defined on the [contact map](/contact-map/) page. The main source of information is a [multiple sequence alignment](/multiple-sequence-alignment/) of the family: residues in contact tend to mutate together. The first methods measured this coevolution directly, from correlated mutations (Göbel et al. 1994) to [direct coupling analysis](/direct-coupling-analysis/) (Morcos et al. 2011). Deep networks that take these signals as input, such as RaptorX-Contact (Wang et al. 2017), then made the predictions much more precise. The standard score is the precision of the top $L/5$ predicted long-range contacts.

## In plain words

A protein folds so that some residues far apart in the chain end up side by side. We want to guess these pairs without knowing the shape.

The clue comes from relatives of the protein in other species. If two residues touch, a change in one often needs a matching change in the other, or the protein stops working. So in a table of related sequences, the columns of touching residues change together. Counting how often columns change together gives a first guess. Better methods remove the false signals that pass along a chain of neighbours, and the best ones today learn the patterns of true contacts from many known structures.

We judge a guess by its most confident pairs: of the top few pairs between residues far apart in the chain, how many truly touch?

## Definition

**Input.** A target sequence $a_1 \cdots a_L$, and usually an alignment of $N$ homologous sequences with $L$ columns.

**Output.** A score $s_{ij}$ for each pair $i < j$, often a probability that $i$ and $j$ are in contact.

**Ground truth.** The contact map $C_{ij} = [\, d(C_\beta^i, C_\beta^j) < 8 \text{ Å} \,]$ of the experimental structure.

**Evaluation.** Pairs are split by sequence separation $|i - j|$: short range $6 \le |i - j| \le 11$, medium range $12 \le |i - j| \le 23$ and long range $|i - j| \ge 24$. Pairs closer than 6 in the chain are always near each other and are not scored. Sort the pairs of one class by decreasing $s_{ij}$ and take the top $k$, usually $k = L/5$, $L/2$ or $L$. The score is the [precision](/precision-and-recall/)

$$P_k = \frac{1}{k} \sum_{(i, j) \in \mathrm{top}_k} C_{ij}.$$

The top $L/5$ long-range precision is the headline number, because long-range contacts carry most of the information about the fold and a few correct ones go a long way.

## Variants

- **Distance prediction.** Predict a distribution over binned distances for each pair, a distogram, instead of a yes or no. AlphaFold 1 (Senior et al. 2020) did this and used the distributions as a potential for folding.
- **Contacts between chains.** Predict the residues at the interface of two proteins, from a paired alignment of the two families.
- **Single-sequence prediction.** Predict without an alignment, for orphan proteins or designed ones, from the sequence alone or with a protein language model.
- **RNA contacts.** The same coevolution methods apply to RNA alignments, where base pairs coevolve.

## Examples

**Scoring a prediction.** Take $L = 40$, so $L/5 = 8$. The ranked predictions, with their separation and whether the pair is a true contact:

| rank | pair | $\lvert i - j \rvert$ | long range? | true contact? |
|---|---|---|---|---|
| 1 | (3, 35) | 32 | yes | yes |
| 2 | (5, 12) | 7 | no | |
| 3 | (4, 30) | 26 | yes | yes |
| 4 | (10, 38) | 28 | yes | no |
| 5 | (2, 36) | 34 | yes | yes |
| 6 | (8, 20) | 12 | no | |
| 7 | (6, 33) | 27 | yes | yes |
| 8 | (1, 30) | 29 | yes | no |
| 9 | (11, 37) | 26 | yes | yes |
| 10 | (7, 32) | 25 | yes | yes |
| 11 | (9, 34) | 25 | yes | no |

The pairs at ranks 2 and 6 are not long range and are skipped. The first 8 long-range pairs are those at ranks 1, 3, 4, 5, 7, 8, 9 and 10, and 6 of them are true contacts, so the top $L/5$ long-range precision is $6/8 = 0.75$.

**Why correlation is not enough.** If residue A touches B and B touches C, but A does not touch C, then A and C still mutate together, through B. A score that counts raw correlation, such as mutual information, ranks the false pair (A, C) high. The [direct coupling analysis](/direct-coupling-analysis/) page works through such a chain with numbers and shows how a global model removes the indirect signal.

**The sparse target.** Each residue has only a bounded number of neighbours within 8 Å, because atoms cannot overlap. So the number of contacts grows about linearly with $L$ while the number of pairs grows as $L^2$. A random guess has a low precision, and a high top $L/5$ precision is a strong signal.

## Known algorithms

- **Correlated mutations.** Göbel et al. (1994) scored pairs of alignment columns by the correlation of their substitution scores. Mutual information is another local score of the same kind.
- **Average product correction.** Dunn, Wahl and Gloor (2008) subtracted from each pair score the product of its row and column means divided by the overall mean. This removes much of the signal of entropy and phylogeny and improves every local and global score.
- **[Direct coupling analysis](/direct-coupling-analysis/).** Fit a [Potts model](/potts-model/) to the alignment and rank pairs by the strength of the fitted couplings. The mean-field version (Morcos et al. 2011) takes one matrix inversion; the pseudo-likelihood version (Ekeberg et al. 2013) is more accurate.
- **Sparse inverse covariance.** PSICOV (Jones et al. 2012) estimates a sparse inverse of the covariance of the one-hot alignment, a [Gaussian graphical model](/gaussian-graphical-model/) view of the same idea.
- **Deep learning.** RaptorX-Contact (Wang et al. 2017) feeds sequence profiles, predicted secondary structure and coevolution scores into a deep residual network over the $L \times L$ pair matrix. The network learns that contacts come in patterns, such as the diagonal bands of paired strands, and predicts them much more precisely than coevolution alone, in particular for families with few sequences.
- **Distograms and end-to-end models.** AlphaFold 1 predicted distance distributions; [AlphaFold](/alphafold/) 2 predicts the structure directly and gives contacts as a by-product.

## Bounds

- **Information.** Coevolution methods need many diverse sequences. With few effective sequences the estimates are noise, and the precision falls. Deep networks reduce, but do not remove, this need.
- **Cost.** Scoring all pairs takes $\Omega(L^2)$ time and space. Mean-field DCA adds the inversion of a matrix of side $L(q - 1)$, which takes $O(L^3 q^3)$ time for $q$ states per column.
- **Indirect signal.** No local pair score can separate a direct from an indirect correlation in general; this needs a global model of all columns.

## Reductions

- **To graph structure learning.** Under a pairwise model of the alignment, predicting contacts is estimating the edges of a [Markov random field](/markov-random-field/), the Potts model, from samples.
- **To folding with restraints.** Predicted contacts become distance restraints for [ab initio folding](/ab-initio-protein-folding/), as in Marks et al. (2011), who computed three-dimensional structures from coevolution alone.

## Applications

- **Folding without templates.** Contact restraints guide fragment assembly and other ab initio methods, as in [Rosetta](/rosetta/) pipelines.
- **Interfaces.** Contacts between two families point to the residues of a protein complex.
- **Checking models.** Agreement of a model with the predicted contacts is a sign of its quality.

## References
