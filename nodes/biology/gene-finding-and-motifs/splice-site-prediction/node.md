---
tag: YZWFM8
kind: problem
slug: splice-site-prediction
name: Splice site prediction
aliases:
- donor and acceptor site prediction
area: biology/gene-finding-and-motifs
level: core
summary: Decide which GT and AG dinucleotides are real exon-intron boundaries from the sequence around them.
prereqs: [position-specific-scoring-matrix]
see_also: [maximal-dependence-decomposition, gene-prediction, generalized-hmm-gene-finder, sequence-logo, logistic-regression, support-vector-machine, decision-tree, spliced-read-alignment]
sources:
  - paper: doi:10.1093/nar/15.17.7155
    title: Marvin B. Shapiro and Periannan Senapathy, RNA splice junctions of different classes of eukaryotes, sequence statistics and functional implications in gene expression, Nucleic Acids Research 15(17), 1987
    locator: pp. 7155 to 7174; the base frequencies and consensus sequences of donor and acceptor splice junctions compiled from many eukaryotic genes
  - paper: doi:10.1006/jmbi.1997.0951
    title: Chris Burge and Samuel Karlin, Prediction of complete gene structures in human genomic DNA, Journal of Molecular Biology 268(1), 1997
    locator: pp. 78 to 94; the maximal dependence decomposition model of the donor site and the signal models of GENSCAN
  - paper: doi:10.1016/S0959-440X(98)80069-9
    title: Christopher B. Burge and Samuel Karlin, Finding the genes in genomic DNA, Current Opinion in Structural Biology 8(3), 1998
    locator: pp. 346 to 354; the GT and AG rule, the list of splice site models, and Table 1 (the accuracy of the GENSCAN splice site models alone and inside the gene finder)
  - paper: doi:10.1089/1066527041410418
    title: Gene Yeo and Christopher B. Burge, Maximum entropy modeling of short sequence motifs with applications to RNA splicing signals, Journal of Computational Biology 11(2-3), 2004
    locator: pp. 377 to 394; maximum entropy models of 9 base donor sites and 23 base acceptor sites, compared with simpler splice site models
---

A splice site is a boundary between an exon and an intron in a gene of a eukaryote. The donor (5') site is at the start of an intron, and the acceptor (3') site is at its end. Almost all introns of the major class begin with GT and end with AG, but GT and AG also occur everywhere else in the genome, so the two bases alone do not mark a site. Splice site prediction asks which occurrences are real, from the bases around them. It is a binary classification of short, aligned windows, and the classic solutions are probability models of the window: a [position weight matrix](/position-specific-scoring-matrix/), a weight array model with dependence between neighbours, a [maximal dependence decomposition](/maximal-dependence-decomposition/) tree, or a maximum entropy model. A gene finder uses such a model as a signal sensor: on its own a splice site model makes many false calls, and the rest of the [gene model](/gene-prediction/) removes most of them.

## In plain words

When a cell makes RNA from a gene, it cuts out the introns and joins the exons. The machine that cuts recognizes short patterns at the two ends of each intron. The intron almost always starts with GT and ends with AG, and the bases next to these two are more often some letters than others. But GT appears about once in every 16 bases of random DNA, so a genome has millions of GT pairs that are not splice sites. To find the real ones, look at a short window around each GT or AG, and ask whether it looks like the real sites you already know or like random DNA.

## Definition

**Input.** A training set of true donor sites (or acceptor sites), aligned on the boundary, a set of false sites (GT or AG pairs that are not splice sites) or a background model, and a query sequence.

**Output.** For each GT in the query (for donors) or AG (for acceptors), a score $s(w)$ of its window $w$, and a decision "site" when $s(w)$ is above a threshold. With probability models, the score is the log-likelihood ratio

$$s(w) = \log \frac{P(w \mid \text{site})}{P(w \mid \text{not a site})}.$$

**The windows.** The donor window covers the last bases of the exon and the first bases of the intron. Yeo and Burge (2004) use 9 bases for the donor and 23 bases for the acceptor, whose window reaches further into the intron.

**Accuracy.** Sensitivity is the fraction of true sites with a score above the threshold, and specificity, in the gene finding usage, is the fraction of called sites that are true. Since false candidates outnumber true ones by far, a small false positive rate per candidate still gives a low specificity.

## Variants

- **Donor against acceptor.** The donor signal is short and has a clear consensus around the GT. The acceptor signal is longer and weaker: the AG, the pyrimidine-rich stretch before it, and the branch point further upstream.
- **Isolated sites against sites in a gene model.** A signal sensor inside a [generalized HMM](/generalized-hmm-gene-finder/) returns a probability, and the decoder combines it with the coding statistics and the rules of a gene structure.
- **Non-canonical introns.** A small fraction of introns begin with GC, or belong to the minor class with other boundary pairs, such as AT and AC. Most predictors ignore them.
- **Effect of a variant.** Given a reference site and a mutated one, predict whether the mutation weakens a site or creates a new one, by the change of the score.
- **Long-range prediction.** Classifiers that look at hundreds or thousands of bases around a candidate can use exon and intron content, not only the local signal.

## Examples

Take the sequence of the spliced gene in [gene prediction](/gene-prediction/), $x = \mathrm{ATGGCAG\,GTAAGTCCTTTTTCAG\,GTTGGTAA}$. It has GT at positions 7 and 11, with the windows GTAAGT and GTCCTT. Score the three bases after the GT (positions +3, +4 and +5 of the intron) with this toy weight matrix and a uniform background of $1/4$:

| intron position | A | C | G | T |
|---|---|---|---|---|
| +3 | 0.6 | 0.05 | 0.3 | 0.05 |
| +4 | 0.7 | 0.1 | 0.1 | 0.1 |
| +5 | 0.1 | 0.05 | 0.8 | 0.05 |

- GTAAGT has A, A, G at +3, +4, +5: $s = \log_2 \frac{0.6}{0.25} + \log_2 \frac{0.7}{0.25} + \log_2 \frac{0.8}{0.25} = 1.263 + 1.485 + 1.678 = 4.43$ bits.
- GTCCTT has C, C, T: $s = \log_2 0.2 + \log_2 0.4 + \log_2 0.2 = -2.322 - 1.322 - 2.322 = -5.97$ bits.

With a threshold of 0, the GT at position 7 is called a donor and the GT at position 11 is not, which agrees with the only valid gene structure of the example. The toy matrix follows the common donor pattern, in which A or G, then A, then G follow the GT.

## Known algorithms

- **Consensus and weight matrices.** Shapiro and Senapathy (1987) compiled the base frequencies of splice junctions in many eukaryotic genes; a score against the consensus or a [position weight matrix](/position-specific-scoring-matrix/) treats the positions as independent. Scoring a window of length $w$ costs $O(w)$.
- **Weight array models.** A first-order Markov chain along the window, with one table for each position, models the dependence of each base on its neighbour. GENSCAN uses a windowed weight array model for the acceptor.
- **Maximal dependence decomposition.** A binary tree of weight matrices that splits the training sites on the positions with the strongest dependences by chi-squared tests ([MDD](/maximal-dependence-decomposition/)). Burge and Karlin (1997) introduced it for the GENSCAN donor model.
- **Maximum entropy models.** Yeo and Burge (2004) fit the distribution of largest entropy that matches chosen marginal counts of the true sites, which models dependences between all pairs of positions, and found it more accurate than the simpler models.
- **Hidden Markov models, decision trees and neural networks.** The 1998 review of Burge and Karlin lists these with MDD and weight array models as the main types of splice site models. [Hidden Markov models](/hidden-markov-model/) and [decision trees](/decision-tree/) model the site, and discriminative classifiers such as [logistic regression](/logistic-regression/), [support vector machines](/support-vector-machine/) and neural networks learn the boundary between true and false sites, often from [k-mer](/kmer/) features.

## Bounds

- **Many candidates.** In random DNA with equal base frequencies, a given position starts a GT with probability $1/16$, so a sequence of length $n$ has about $n / 16$ donor candidates and as many acceptor candidates. A scan with a model of window length $w$ costs $O(n w)$ time.
- **Weak signals.** The splice site models of GENSCAN, used in isolation at 50% sensitivity, reach a specificity of only 36% for donor sites and 34% for acceptor sites. Inside the full gene model, the same sites are predicted with sensitivity 91% (donor) and 89% (acceptor) at specificity 89% and 85% (Burge and Karlin 1998, Table 1, on the Burset and Guigó set of 570 vertebrate genes). The local signal does not carry enough information to find the sites; the context of the gene does most of the work.
- **No exact optimum.** As a classification problem, the task has no single correct algorithm. Methods are compared by their sensitivity and specificity on held-out sites.

## Reductions

- **To motif scoring.** With a weight matrix, splice site prediction is the scoring of a fixed-length motif at every candidate position, the same task as the search for binding sites with a [PSSM](/position-specific-scoring-matrix/).
- **To binary classification.** Each candidate window is a labeled example, and any classifier on fixed-length strings applies.
- **As a part of gene prediction.** In a generalized HMM, the score of a splice site is a factor of the probability of each parse, so the site is predicted jointly with the exons and introns around it.

## Applications

- Signal sensors of *ab initio* gene finders, for the boundaries of exons and introns.
- The interpretation of genetic variants near exon boundaries, by the change of the score between the reference and the variant sequence.
- The choice between candidate junctions in [spliced read alignment](/spliced-read-alignment/) of RNA-seq data, where a junction with good splice signals is more likely to be real.
- The study of splicing itself: which positions of the signal matter, and how they depend on each other, which a [sequence logo](/sequence-logo/) and an MDD tree show.

## References
