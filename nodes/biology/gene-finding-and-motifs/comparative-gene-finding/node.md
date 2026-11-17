---
tag: YEG0E8
kind: technique
slug: comparative-gene-finding
name: Comparative gene finding
aliases:
- comparative gene prediction
- dual-genome gene finding
area: biology/gene-finding-and-motifs
level: advanced
summary: Predict genes in one genome with help from an aligned related genome, since coding exons are conserved more than the sequence around them.
prereqs: [generalized-hmm-gene-finder, pair-hmm, gene-prediction]
see_also: [whole-genome-alignment, spliced-alignment-problem, phylogenetic-footprinting, genome-annotation, viterbi-algorithm, hidden-semi-markov-model, splice-site-prediction, blast]
sources:
  - paper: doi:10.1093/bioinformatics/17.suppl_1.S140
    title: Ian Korf, Paul Flicek, Daniel Duan and Michael R. Brent, Integrating genomic homology into gene structure prediction, Bioinformatics 17 Suppl 1, 2001
    locator: pp. S140 to S148; TWINSCAN, a GENSCAN-like generalized HMM that also reads a conservation sequence made from the alignment of the target with an informant genome
  - url: https://genome.cshlp.org/content/13/3/496
    title: Marina Alexandersson, Simon Cawley and Lior Pachter, SLAM, cross-species gene finding and alignment with a generalized pair hidden Markov model, Genome Research 13(3), 2003, pp. 496 to 502
    locator: the generalized pair HMM that predicts genes in two sequences and aligns them at the same time, restricted by an approximate alignment
  - paper: "Lior Pachter, Marina Alexandersson and Simon Cawley, Applications of generalized pair hidden Markov models to alignment and gene finding problems, Journal of Computational Biology 9(2), 2002, pp. 389 to 399"
    locator: the theory of generalized pair HMMs that SLAM uses
---

Comparative gene finding predicts the genes of a target genome with the help of a second, related genome, called the informant. It uses the fact that natural selection keeps the coding parts of genes much more than the introns and the DNA between genes, so an alignment of the two genomes shows where the exons are and often which reading frame they use. The usual form adds the alignment as a second input to a [generalized HMM gene finder](/generalized-hmm-gene-finder/), as TWINSCAN did in 2001, or replaces the gene model by a [pair HMM](/pair-hmm/) that predicts genes in both genomes and aligns them at once, as SLAM did in 2003.

## In plain words

Two related species, such as human and mouse, have mostly the same genes. Over tens of millions of years, random changes collect in their DNA. Where the DNA does nothing, the changes stay, so the two genomes look less and less alike there. Where the DNA codes for protein, most changes harm the protein, and they are lost. So the exons of the two species still look much alike, while the introns and the long stretches between genes do not. The changes that remain in exons also have a pattern: they fall mostly on the third letter of each codon, where many changes do not alter the protein. A gene finder that sees where the two genomes agree, and how, can find exons that it would miss with one genome alone.

## When it applies

- **A genome at the right distance is available.** If the informant is too close (for example two primates), almost everything is conserved, and conservation says little about function. If it is too far (for example human and fish for most genes), only some exons still align, and short or fast-changing exons are lost. Human and mouse, at roughly 75 to 90 million years, were the classic pair.
- **The gene structures are mostly kept.** The method assumes that most exons of the target have a matching exon in the informant. Genes that are new in one lineage, or that changed their exon structure, get little help.
- **A gene model already exists.** Comparative gene finding is an addition to a gene model of the target, with its signals ([splice sites](/splice-site-prediction/), start and stop codons) and its length distributions. The informant only changes the scores.
- **An alignment can be made.** The two genomes, or the target and a set of informant contigs, are aligned first. For TWINSCAN this was a local alignment search such as [BLAST](/blast/); for SLAM, an approximate global alignment of the two regions. See [whole-genome alignment](/whole-genome-alignment/).

## The template

The technique has two forms. Both keep the dynamic programming of the [Viterbi algorithm](/viterbi-algorithm/) over a gene model, so the answer is still the single most probable gene structure under the model.

**Form 1: one target and a conservation sequence (TWINSCAN).**

1. Align the target $x$ (length $n$) to the informant, and keep the best local alignments.
2. Turn the alignments into a *conservation sequence* $c = c_1 \ldots c_n$ over a small alphabet: for each base of the target, whether it is aligned to an equal base, aligned to a different base, or not aligned. A gap in the target is written on its neighbours, so $c$ has the same length as $x$.
3. Give each state $q$ of the gene model two emission models: the usual model $P(x_i \mid q, \text{context})$ for the bases, and a new model $P(c_i \mid q, \text{context})$ for the conservation symbols. Coding states use a model with a period of 3, so that a mismatch at the third codon position costs less than one at the first or second.
4. Score a parse by the product of the two emissions, under the assumption that $x$ and $c$ are independent given the state.
5. Run the usual GHMM Viterbi algorithm on the pair $(x_i, c_i)$.

The cost is the cost of the one-genome gene finder times a constant, because $c$ adds one lookup per base and state. The alignment step is separate and often costs more.

**Form 2: two genomes in one model (SLAM).**

1. Take two homologous regions $x$ and $y$, and an approximate alignment of them.
2. Use a *generalized pair HMM*: its states are the parts of a gene, as in a GHMM, but each exon or intron state emits a pair of segments, one in each sequence, aligned to each other by a pair HMM inside the state.
3. Find the best joint parse: a gene structure in $x$, a gene structure in $y$, and an alignment of the two that agrees with them. In the basic model, paired exons in the two genomes have the same phase, so the two genes have the same exon structure.
4. Restrict the dynamic program to the cells near the approximate alignment. Without the restriction, a pair HMM costs $O(n m)$ cells per state for lengths $n$ and $m$, and the generalized version, which also chooses segment lengths, costs more. With the restriction, the cost is close to linear in the length of the alignment.

**What the result means.** In both forms, the output is optimal for the model, which is a theorem about the dynamic program. How good the model is, and so how good the genes are, is a measurement on annotated genes, not a guarantee.

## Classic examples

**A toy conservation score.** Take a coding conservation model with a period of 3: at codon positions 1 and 2 the probabilities of match, mismatch and unaligned are 0.9, 0.05 and 0.05; at position 3 they are 0.6, 0.35 and 0.05. Take a non-coding model with 0.5, 0.2 and 0.3 at every position. These numbers are only for the example. For the 15 positions

`| | : | | : | | | | | : | | :` (11 matches, 4 mismatches)

the log-odds score of coding against non-coding, in bits, is 11.97 when the mismatches fall on the third codon positions, and -1.60 in each of the two other frames. The 10 matches at positions 1 and 2 give $10 \cdot \log_2(0.9 / 0.5) = 8.48$, the one match at a third position gives 0.26, and the four mismatches at third positions give $4 \cdot \log_2(0.35 / 0.2) = 3.23$. So the same alignment raises the score of a coding parse in one frame and lowers it in the others. This frame signal is the main gain over a plain "conserved or not" flag.

**TWINSCAN (Korf, Flicek, Duan and Brent 2001).** A GENSCAN-like gene model, with each state extended by a conservation model, run on human sequence with mouse sequence as the informant. The paper reports, as a measurement on its own test set, that the mouse informant made the predictions more accurate than those of GENSCAN.

**SLAM (Alexandersson, Cawley and Pachter 2003).** A generalized pair HMM that predicts genes in human and mouse regions and aligns them in one run. It uses an approximate alignment to limit the dynamic program, and its exon states use a fifth-order Markov model of the coding sequence.

**Earlier and later programs.** Before TWINSCAN, ROSETTA aligned syntenic human and mouse regions first and then predicted genes on both. Later programs use several informants at once, with the conservation scored on a [phylogenetic tree](/phylogenetic-tree/) instead of one pairwise alignment.

## Variations

- **Several informants.** With many genomes, a single conservation symbol per base is too coarse. Phylogenetic models score each column of a [multiple alignment](/multiple-sequence-alignment/) by a tree likelihood, which separates fast and slow regions better. The same idea finds regulatory sites in [phylogenetic footprinting](/phylogenetic-footprinting/).
- **Protein and transcript evidence.** Instead of a genome, the second input can be a known protein or transcript; then the exact tool is [spliced alignment](/spliced-alignment-problem/), and gene finders add such alignments as hints.
- **Discriminative training.** The emission and transition parameters can be fit to maximize the accuracy of the predicted parses instead of the likelihood of the data.
- **Approximate alignment first, or no alignment.** Form 1 trusts the alignment; Form 2 corrects it. In between, a program can use the alignment only to restrict the search space.
- **Conservation without gene structure.** A model that only marks conserved regions, without exons and introns, gives a track of conserved elements; such tracks are used later as evidence in [genome annotation](/genome-annotation/).

## Pitfalls

- **Conservation is not coding.** Many conserved regions are not exons: promoters, enhancers, non-coding RNAs and ultra-conserved elements. A model that rewards all conservation predicts false exons there. The period-3 pattern of the coding model helps to tell them apart.
- **Alignment errors.** A wrong alignment gives a wrong conservation sequence. Repeats are the usual cause, so mask them first ([repeat masking](/repeat-masking/)).
- **Pseudogenes.** A processed pseudogene in the target can align well to a real gene in the informant, and conservation then pushes the model to call it a gene.
- **Unequal evidence.** Where the informant has a gap in its assembly, every base is "not aligned", which the model reads as weak evidence against coding. The model cannot tell missing data from true divergence unless it has a separate symbol for it.
- **Genes specific to one lineage.** A gene with no counterpart in the informant gets no help and can lose to its competitors. Such genes are often the most interesting ones.
- **Independence assumption.** Form 1 treats the bases and the conservation symbols as independent given the state. They are not: a C in the target paired with a mismatch tells something about the informant base. The model still works, but its probabilities are not calibrated.

## Exercises

1. In the toy example, find the conservation sequence of length 15 with 4 mismatches that gives the largest score in frame 0, and the one that gives the smallest.
2. Show that if the coding and non-coding conservation models are the same, Form 1 gives the same parse as the one-genome gene finder.
3. A generalized pair HMM has $Q$ states and segment lengths up to $D$ in each sequence. Give the cost of its dynamic program on sequences of lengths $n$ and $m$ without any restriction, and with a band of width $w$ around a given alignment.
4. Explain why an informant at a very short distance gives little information, using the expected fraction of mismatches in coding and in non-coding DNA.
5. Design a fourth conservation symbol for "no informant sequence here", and say which probabilities it should have in the coding and non-coding models.

## References
