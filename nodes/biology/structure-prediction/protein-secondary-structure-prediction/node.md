---
tag: JMA33G
kind: problem
slug: protein-secondary-structure-prediction
name: Protein secondary structure prediction
aliases:
- Secondary structure prediction
area: biology/structure-prediction
level: core
summary: Label each residue of a protein sequence as helix, strand or coil. Scored by Q3, the fraction of correct residues against DSSP; modern methods reach about 82 to 84 percent.
prereqs: [protein-secondary-structure]
see_also: [chou-fasman-method, gor-method, psipred, protein-structure-prediction, protein-threading, hidden-markov-model, cross-validation, rna-secondary-structure-prediction]
sources:
  - paper: doi:10.1093/bib/bbw129
    title: Yuedong Yang, Jianzhao Gao, Jihua Wang, Rhys Heffernan, Jack Hanson, Kuldip Paliwal and Yaoqi Zhou, Sixty-five years of the long march in protein secondary structure prediction, the final stretch?, Briefings in Bioinformatics 19(3), 2018, pages 482 to 494
    locator: the history of three-state accuracy from single residue statistics to deep learning, the 82 to 84 percent range of current methods without templates, and the estimated limit of about 88 to 90 percent
  - paper: doi:10.1006/jmbi.1993.1413
    title: Burkhard Rost and Chris Sander, Prediction of protein secondary structure at better than 70% accuracy, Journal of Molecular Biology 232(2), 1993, pages 584 to 599
    locator: the PHD method, the first to use multiple sequence alignments as network input, and its cross-validated three-state accuracy
  - paper: doi:10.1002/bip.360221211
    title: Wolfgang Kabsch and Christian Sander, Dictionary of protein secondary structure, pattern recognition of hydrogen-bonded and geometrical features, Biopolymers 22(12), 1983, pages 2577 to 2637
    locator: the DSSP states used as the true labels
  - paper: doi:10.1006/jmbi.1999.3091
    title: David T. Jones, Protein secondary structure prediction based on position-specific scoring matrices, Journal of Molecular Biology 292(2), 1999, pages 195 to 202
    locator: the effect of the 8 to 3 state reduction on Q3
---

Protein secondary structure prediction is the problem of giving each residue of a protein sequence one of three labels, helix (H), strand (E) or coil (C), with only the sequence, and often its relatives, as input. The true labels come from a solved 3D structure by the DSSP rules of [protein secondary structure](/protein-secondary-structure/), so the problem is a supervised classification with a known answer for training data. Accuracy is measured, not proved: the usual score Q3 is the percentage of residues with the right label, and it went from well under 70 percent for the single sequence methods of the 1970s to about 82 to 84 percent for deep networks on sequence profiles.

## In plain words

A protein is a string of letters, one letter for each amino acid. When the protein folds, each amino acid becomes part of a helix, part of a flat strand, or part of the rest. The task is to guess, for each letter, which of the three it will be, without folding the protein.

There is no formula for the answer. Methods learn it from proteins whose shape is known. Early methods counted how often each amino acid is found in helices and strands. Later ones also looked at the neighbours of each letter. The big step came from using many related proteins at once: if a position stays similar across the family, the pattern of changes tells a lot about the shape. A method is judged by the share of letters it gets right on proteins that it did not learn from.

## Definition

**Input.** A protein sequence $s = s_1 s_2 \cdots s_n$ over the alphabet of the 20 amino acids. Many methods also take a [position-specific scoring matrix](/position-specific-scoring-matrix/) or a profile of the family of $s$, built from a [multiple sequence alignment](/multiple-sequence-alignment/) of homologs found in a database.

**Output.** A string $y = y_1 \cdots y_n$ over $\{H, E, C\}$. Some methods also give a score or a probability for each state at each position.

**Truth.** For a protein of known structure, the target $t = t_1 \cdots t_n$ is the DSSP assignment of the structure, cut from 8 states to 3. The cut must be stated, because there is more than one in use.

**Score.** The main measure is

$$Q_3 = \frac{100}{n} \, \lvert \{ i : y_i = t_i \} \rvert ,$$

the percentage of residues with the right label. Over a test set it is reported either per residue (all residues of all chains pooled) or per chain (the mean of the chain values); the two differ. The per-state measures are $Q_H$, $Q_E$ and $Q_C$, the percentage of true residues of each state that get that state. The segment overlap score SOV compares predicted and true segments instead of residues, so that a strand predicted one residue too short loses less than a strand that is not predicted at all.

**Evaluation protocol.** Q3 is meaningful only on proteins that are not close relatives of the training proteins. A fair test removes from the test set every chain with significant sequence similarity (or, better, structural similarity) to a training chain, or uses [cross-validation](/cross-validation/) with such a split. Two published Q3 values are comparable only when the test set, the 8 to 3 cut and the per-residue or per-chain average are the same.

## Variants

- **Eight states.** Predict all DSSP states. The score is Q8, and it is lower than Q3 because G, I, B, T and S are rarer and less regular.
- **Single sequence.** Predict from $s$ alone, with no homologs. This is the setting of the early methods, and it is needed for proteins with no known relatives. Accuracy is lower.
- **With templates.** If a homolog of known structure exists, copy its states through an alignment. This is a different method, closer to [comparative modeling](/comparative-modeling/), and its accuracy depends on how close the template is.
- **Related labels.** The same models predict solvent accessibility, backbone angles $\phi$ and $\psi$, disordered regions and transmembrane helices. Transmembrane prediction is a separate problem with its own methods.

## Examples

Take the true string and a prediction for 18 residues:

```
true       C H H H H H H H C C C E E E E E C C
predicted  C C H H H H H H H H C C E E C C C C
```

The labels agree at 12 of 18 positions, so $Q_3 = 66.7$. Of the 7 true helix residues, 6 get H, so $Q_H = 85.7$. Of the 5 true strand residues, 2 get E, so $Q_E = 40.0$. Of the 6 true coil residues, 4 get C, so $Q_C = 66.7$. The helix is found with its start one residue late and its end two residues late, which costs three residues. The strand is found but too short, which costs three. A segment score sees one correct helix and one correct but short strand, and so ranks this prediction higher than Q3 does.

A trivial method sets the floor. If it predicts the most common state of the true string at every position, here H, it gets $Q_3 = 7/18 = 38.9$. Predicting C everywhere gets $6/18 = 33.3$. On real data sets coil is the most common state, and the floor is the coil fraction of the set.

## Known algorithms

The methods are usually grouped in generations. Each is a learned or statistical model: none has a worst-case guarantee on accuracy, and each is described by what it computes and by its measured Q3.

| method | year | what it uses | three-state accuracy |
|---|---|---|---|
| [Chou-Fasman method](/chou-fasman-method/) | 1974 | the helix and strand propensity of each amino acid, with rules for nuclei and their growth | below PHD in later tests on larger sets; the value depends on the set |
| [GOR method](/gor-method/) | 1978 | information values of each amino acid at each offset in a window of 17, summed over the window | below PHD in later tests on larger sets; the value depends on the set |
| PHD (Rost and Sander) | 1993 | a neural network on the profile of a multiple alignment, with a second network over the first outputs | 69.7 percent in the history of Yang et al. |
| [PSIPRED](/psipred/) | 1999 | two window networks on a PSI-BLAST position-specific scoring matrix | 76.5 percent in the paper's own cross-validation |
| deep networks (for example SPIDER3) | 2010s | deep, recurrent or convolutional networks on profiles and other features | about 82 to 84 percent |

The jump between the second and third rows came from evolutionary information. A family alignment shows which positions keep their chemistry, and the period of hydrophobic positions (about every 3 or 4 residues in a helix, every 2 in a strand) shows up across the family even where one sequence does not show it. Yang and coworkers give 82 to 84 percent as the range of current methods without templates, on test sets of chains that are not similar to the training chains, with the common 8 to 3 cut.

All of these methods can run in $O(n)$ time for a sequence of length $n$, for a fixed window and a fixed model, plus the cost of building the profile. The direct form of the Chou-Fasman rules takes $\Theta(n^2)$ time in the worst case, and a precomputation brings it down to $\Theta(n)$. The profile search (PSI-BLAST against a large database) dominates the running time in practice.

## Bounds

There is no proved upper bound on Q3, but there are three reasons why 100 percent is out of reach:

- **The truth is not unique.** DSSP is one rule among several, and DSSP itself gives different states for the ends of helices and strands in two structures of the same protein. Yang and coworkers estimate the limit from such disagreement at about 88 to 90 percent.
- **The state is not local.** A strand forms only with a partner strand that may be far away in the sequence. A window method sees only nearby residues, and the same short sequence can be a helix in one protein and a strand in another.
- **The cut and the test set move the number.** Jones reports that PSIPRED scores 76.5 percent with one 8 to 3 cut and 78.3 percent with another, on the same predictions.

The lower bound is the trivial one: the most common state at every residue. A method that does not beat it by a wide margin has learned nothing.

## Reductions

- **Sequence labeling.** The problem is an instance of labeling each element of a sequence. A [hidden Markov model](/hidden-markov-model/) with states for helix, strand and coil, and [Viterbi decoding](/viterbi-algorithm/), gives labels that respect segment lengths. A [conditional random field](/conditional-random-field/) does the same with learned features.
- **Window classification.** Most methods turn the problem into $n$ independent classifications: the features of the residues at offsets $-h, \ldots, h$ around position $i$ give the label of $i$. A second stage then smooths the labels. The [GOR method](/gor-method/) is the simplest case: a naive Bayes style sum of log ratios over the window.
- **Into structure prediction.** Predicted states are inputs to fold recognition and to [protein structure prediction](/protein-structure-prediction/). Methods that predict the full 3D structure, such as [AlphaFold](/alphafold/), give secondary structure as a by-product: run DSSP on the predicted model.

## Applications

- **Fold recognition and threading.** Predicted states are scored against the states of a template in [protein threading](/protein-threading/).
- **Restraints for 3D prediction.** Fragment libraries and early contact predictors use predicted states to choose local shapes.
- **Annotation.** Large sequence databases get predicted states for each protein, with no structure needed.
- **Design and engineering.** A designed sequence can be checked for the intended pattern of helices and strands before it is made.

[RNA secondary structure prediction](/rna-secondary-structure-prediction/) has a similar name but is a different problem: it predicts a set of nested base pairs by dynamic programming over an energy model, not a label per residue by a learned classifier.

## References
