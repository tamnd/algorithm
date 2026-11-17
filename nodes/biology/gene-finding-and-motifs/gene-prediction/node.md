---
tag: YRX7FB
kind: problem
slug: gene-prediction
name: Gene prediction
aliases:
- gene finding
- ab initio gene prediction
area: biology/gene-finding-and-motifs
level: core
summary: Find the genes in a genome sequence and their exon and intron structure, from sequence signals and statistics or from similarity.
prereqs: [open-reading-frame, hidden-markov-model]
see_also: [generalized-hmm-gene-finder, orf-finding, splice-site-prediction, periodic-markov-chain-gene-model, interpolated-markov-model, exon-chaining, spliced-alignment-problem, genome-annotation]
sources:
  - paper: doi:10.1006/jmbi.1997.0951
    title: Chris Burge and Samuel Karlin, Prediction of complete gene structures in human genomic DNA, Journal of Molecular Biology 268(1), 1997
    locator: pp. 78 to 94; gene prediction as the most probable parse of a sequence under a generalized HMM with genes on both strands
  - paper: doi:10.1016/S0959-440X(98)80069-9
    title: Christopher B. Burge and Samuel Karlin, Finding the genes in genomic DNA, Current Opinion in Structural Biology 8(3), 1998
    locator: pp. 346 to 354; a review of the methods of the time, and Table 1, the accuracy of splice site models alone and inside GENSCAN on the Burset and Guigó set of 570 vertebrate genes
  - url: https://pubmed.ncbi.nlm.nih.gov/8877513/
    title: David Kulp, David Haussler, Martin G. Reese and Frank H. Eeckman, A generalized hidden Markov model for the recognition of human genes in DNA, Proceedings of ISMB 4, 1996, pp. 134 to 142
    locator: the legal parses of a DNA sequence into gene parts, and their scoring by a generalized HMM
  - paper: doi:10.1093/nar/26.2.544
    title: Steven L. Salzberg, Arthur L. Delcher, Simon Kasif and Owen White, Microbial gene identification using interpolated Markov models, Nucleic Acids Research 26(2), 1998
    locator: pp. 544 to 548; gene finding in bacteria by scoring long ORFs in six frames, and the results on H. influenzae and H. pylori
  - paper: doi:10.1016/0097-8485(93)85004-V
    title: Mark Borodovsky and James McIninch, GENMARK, parallel gene recognition for both DNA strands, Computers and Chemistry 17(2), 1993
    locator: pp. 123 to 133; coding region recognition on both strands by Markov chain models and a Bayes decision
---

Gene prediction is the task of marking the genes in a DNA sequence: where each gene starts and ends, on which strand it lies, and, in eukaryotes, which parts are exons and which are introns. The output is a list of gene structures, each of which gives a protein by splicing its exons and translating them. *Ab initio* methods use only the sequence: statistics that separate coding from non-coding DNA, such as a [three-periodic Markov chain](/periodic-markov-chain-gene-model/), and models of the signals at the gene boundaries, such as [splice sites](/splice-site-prediction/) and start and stop codons. Evidence-based methods also use alignments of proteins, transcripts or related genomes. In its most common formal version, the problem asks for the most probable parse of the sequence under a [generalized HMM](/generalized-hmm-gene-finder/), which dynamic programming solves exactly.

## In plain words

A genome is a long string of A, C, G and T, and the genes are hidden in it with no marks between them. In bacteria, a gene is usually one unbroken [open reading frame](/open-reading-frame/): from a start codon to a stop codon, three bases at a time. In humans and other eukaryotes, a gene is broken into pieces (exons) separated by pieces that are cut out of the RNA (introns), and most of the genome is not genes at all. A gene finder looks for stretches whose bases look like protein code, for the short signals at the edges of the pieces, and for the rules that the pieces must obey together, and puts them into the best complete explanation of the sequence.

## Definition

**Input.** A DNA sequence $x$ of length $n$ (often a whole chromosome or contig), and, depending on the version, a model of genes and optional evidence such as aligned proteins or RNA-seq reads.

**Output.** A set of gene structures. Each gives a strand and an ordered list of coding exons $[a_1, b_1), [a_2, b_2), \ldots, [a_m, b_m)$ with $a_1 < b_1 < a_2 < \cdots < b_m$, such that, on that strand:

- the first exon begins with a start codon (usually ATG) and the last exon ends with a stop codon (TAA, TAG or TGA);
- each intron $[b_r, a_{r+1})$ begins with GT and ends with AG (the canonical rule; a few introns use other pairs);
- the total length $\sum_r (b_r - a_r)$ is a multiple of 3;
- the spliced sequence has no stop codon in frame before its last codon.

Most gene models do not let two genes overlap. In bacteria, $m = 1$ for almost every gene, so a gene is an [ORF](/open-reading-frame/) with a chosen start codon.

**As an optimization problem.** Given a probabilistic model $M$ of genomic DNA, find the parse $\phi$ (the full labeling of $x$ into intergenic, exon and intron segments on both strands) that maximizes $P(x, \phi \mid M)$. For a generalized HMM, this is the segment form of the [Viterbi algorithm](/viterbi-algorithm/).

**Accuracy.** Predictions are compared with a reference annotation at three levels: bases (is each base correctly called coding?), exons (are both ends exactly right?), and whole genes. At each level, the sensitivity is the fraction of true features that are predicted and the specificity, in the usage of the gene finding literature, is the fraction of predicted features that are true. The test set of 570 vertebrate genes of Burset and Guigó is a common benchmark for these measures.

## Variants

- **Prokaryotic gene finding.** Most genes are single ORFs and most of the genome is coding. The problem is to choose which ORFs are genes, which of their start codons is the true one, and which of two overlapping ORFs to keep.
- **Eukaryotic *ab initio* prediction.** Genes have introns, the coding part is a small fraction of the genome, and the signals are weak. The full parse with exons in three phases on both strands is needed.
- **Evidence-based prediction.** Align known proteins or transcripts to the genome ([spliced alignment](/spliced-alignment-problem/), [exon chaining](/exon-chaining/)), or map RNA-seq reads with [spliced read alignment](/spliced-read-alignment/) and assemble them ([transcript assembly](/transcript-assembly/)).
- **Comparative prediction.** Use the pattern of conservation between two or more genomes, since coding exons evolve differently from introns ([comparative gene finding](/comparative-gene-finding/)).
- **Alternative splicing.** One gene can have several transcripts. A single best parse gives one; posterior probabilities or evidence are needed for the others.
- **Untranslated regions and non-coding RNA genes.** Most gene finders predict only the coding part. Genes for RNAs that are not translated need other methods.

## Examples

**A spliced gene.** Take the 31 bases

$$x = \mathrm{ATGGCAG}\;\mathrm{GTAAGTCCTTTTTCAG}\;\mathrm{GTTGGTAA},$$

with 0-based positions. Read straight, frame 0 gives ATG GCA GGT AAG TCC TTT TTC AGG TTG GTA A, which has no stop codon. Now look for introns. GT occurs at positions 7, 11, 23 and 27, and AG at positions 5, 10 and 21. An intron from a GT at $i$ to an AG at $j$ is $[i, j + 2)$, which gives three candidates: $[7, 12)$, $[7, 23)$ and $[11, 23)$. Removing $[7, 12)$ leaves 26 bases, and removing $[11, 23)$ leaves 19; neither is a multiple of 3. Removing $[7, 23)$ leaves ATGGCAG + GTTGGTAA = ATG GCA GGT TGG TAA, 15 bases that translate to M A G W and end with a stop. So the only one-intron gene that starts at position 0 has the exons $[0, 7)$ and $[23, 31)$, and the intron splits the codon GGT after its first base (an intron of phase 1). In a real genome, introns are much longer and there are many more candidates, so the rules alone do not decide, and the statistics of the content and the signals choose among the parses.

**A bacterial genome.** On the 1.8 million bases of *Haemophilus influenzae*, with 1717 annotated genes, Glimmer scored the long ORFs in the six frames with an [interpolated Markov model](/interpolated-markov-model/) and found 1680 of the genes (97.8%); a fixed fifth-order Markov chain found 1574 (91.7%) (Salzberg et al. 1998).

## Known algorithms

- **ORF scanning with a coding score.** Find all ORFs above a length ([ORF finding](/orf-finding/)), score each in its frame against the other frames and non-coding DNA with a [three-periodic chain](/periodic-markov-chain-gene-model/) or an [interpolated Markov model](/interpolated-markov-model/), and resolve overlaps. This is the method of GeneMark and Glimmer for bacteria.
- **HMM and GHMM parsing.** Model all gene parts as states of a [hidden Markov model](/hidden-markov-model/), or of a [generalized HMM](/generalized-hmm-gene-finder/) with explicit length distributions ([hidden semi-Markov model](/hidden-semi-markov-model/)), and decode with the Viterbi recursion. Genie (Kulp et al. 1996) and GENSCAN (Burge and Karlin 1997) work this way. The [forward-backward](/forward-backward-algorithm/) recursions give the posterior probability of each exon, and training uses counts on annotated genes, or [Baum-Welch](/baum-welch-algorithm/) when the labels are missing.
- **Exon chaining.** Score candidate exons, then choose the best chain of compatible, non-overlapping exons by dynamic programming ([exon chaining](/exon-chaining/)).
- **Spliced alignment.** Find the chain of candidate exons whose spliced sequence is closest to a known related protein or transcript ([spliced alignment problem](/spliced-alignment-problem/)).
- **Discriminative and comparative models.** Semi-Markov [conditional random fields](/conditional-random-field/) and pair or phylogenetic GHMMs use the same decoders with other scores.
- **Pipelines.** [Genome annotation](/genome-annotation/) combines [repeat masking](/repeat-masking/), *ab initio* predictions, and protein and transcript evidence.

## Bounds

- **The decoder.** For a GHMM with $K$ states and segment lengths up to $D$, the best parse costs $\Theta(n K D + n K^2)$ time and $\Theta(n K)$ space. With geometric lengths for introns and intergenic regions and exons limited by stop codons, gene finders run in time close to linear in $n$.
- **Prokaryotes.** Finding all ORFs is $\Theta(n)$ on both strands, and a Markov score of every ORF in all frames is $O(n)$ with prefix sums.
- **Exon chaining.** With $m$ candidate exons, the best chain takes $O(m \log m)$ time, as in weighted interval scheduling.
- **Limits of the signals.** The problem is solved exactly only relative to a model, and the models are imperfect. The 1998 review of Burge and Karlin shows how weak the signals are alone: the GENSCAN splice site models, used in isolation at 50% sensitivity, have a specificity of only 36% for 5' sites and 34% for 3' sites, while inside the full gene model, with the content and the rules of the parse, the splice sites are found with sensitivity 91% and 89% and specificity 89% and 85% (Table 1, on the Burset and Guigó set). Accuracy at the level of whole genes is lower than at the level of exons, because one wrong exon makes the whole gene wrong.

## Reductions

- **To a longest path.** The parses of $x$ under a GHMM are the paths through a directed acyclic graph whose nodes are the pairs (position, state), and the log probability is additive along the path. The best parse is a longest path in that DAG, which dynamic programming finds.
- **To weighted interval scheduling.** With candidate exons as weighted intervals and compatibility rules between neighbours, choosing the best gene structure is a chain problem on intervals ([exon chaining](/exon-chaining/)).
- **From evidence to alignment.** With a related protein, the problem becomes the [spliced alignment problem](/spliced-alignment-problem/), which is solved in polynomial time by dynamic programming over the candidate blocks.
- **Prokaryotic case to classification.** Each ORF is a candidate, and the task is to classify it as a gene in its frame or not, which a likelihood ratio of a coding model against the other frames and a non-coding model does.

## Applications

- The first annotation of every new genome, and of fragments from metagenomes, where most genes have no close relative with a known structure.
- Prediction of the proteins of an organism, the starting point for function prediction, the search for drug targets, and comparative genomics.
- The detection of genes that transcript data misses because they are expressed weakly or only in some tissues.
- Gene finders also give the coordinates for later work: the codon usage of the genes ([codon adaptation index](/codon-adaptation-index/)), promoter search upstream of the start codons, and the study of splice signals.

## References
