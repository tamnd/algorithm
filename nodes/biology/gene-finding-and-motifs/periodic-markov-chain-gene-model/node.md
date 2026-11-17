---
tag: VMQM9G
kind: model
slug: periodic-markov-chain-gene-model
name: Three-periodic Markov chain gene model
aliases:
- GeneMark model
- inhomogeneous Markov chain for coding regions
area: biology/gene-finding-and-motifs
level: core
summary: A Markov chain whose transitions depend on the codon position, which scores how likely a stretch of DNA is to code in each frame.
history:
  year: 1993
  people: [Mark Borodovsky, James McIninch]
  note: Borodovsky and McIninch combined frame-dependent Markov chains of coding DNA with a Bayes decision over both strands in the GeneMark method.
prereqs: [markov-chain, open-reading-frame]
see_also: [interpolated-markov-model, gene-prediction, orf-finding, generalized-hmm-gene-finder, hidden-markov-model, codon-adaptation-index, kmer, n-gram-language-model]
sources:
  - paper: doi:10.1016/0097-8485(93)85004-V
    title: Mark Borodovsky and James McIninch, GENMARK, parallel gene recognition for both DNA strands, Computers and Chemistry 17(2), 1993
    locator: pp. 123 to 133; the frame-dependent (non-homogeneous) Markov chain models of coding regions, the homogeneous model of non-coding DNA, and the Bayes decision over the frames of both strands
  - paper: doi:10.1093/nar/26.2.544
    title: Steven L. Salzberg, Arthur L. Delcher, Simon Kasif and Owen White, Microbial gene identification using interpolated Markov models, Nucleic Acids Research 26(2), 1998
    locator: pp. 545 and 546 (one model for each of the six frames and one for non-coding DNA, 4^(k+1) probabilities for order k, and the 3-periodic chain of GeneMark), p. 547, Table 1 (a fixed fifth-order model against the IMM on H. influenzae)
  - paper: doi:10.1093/nar/26.4.1107
    title: Alexander V. Lukashin and Mark Borodovsky, GeneMark.hmm, new solutions for gene finding, Nucleic Acids Research 26(4), 1998
    locator: pp. 1107 to 1115; the coding and non-coding chains placed in a hidden Markov model whose state changes mark the gene boundaries
---

A three-periodic Markov chain is a model of protein-coding DNA in which the probability of the next base depends on the bases before it and also on the position of the base in its codon. It has three transition tables, one for the first, second and third codon positions, and it uses them in turn as it reads the sequence. Coding DNA is not the same at the three codon positions, because the genetic code and the amino acid composition of proteins put different bases at each position, so the three tables are different. Non-coding DNA has no such period. A model of each kind, applied to a stretch of DNA, tells how likely the stretch is to code in each of the three frames of each strand, or to be non-coding. Borodovsky and McIninch (1993) made this the core of the GeneMark gene finder. The model is the content sensor of most gene finders: of the [interpolated Markov model](/interpolated-markov-model/), and of the exon states of a [generalized HMM](/generalized-hmm-gene-finder/).

## The machine

**The state.** A position $i$ in a sequence $x = x_0 x_1 \cdots x_{L-1}$ over $\{A, C, G, T\}$, the context $w = x_{i-k} \cdots x_{i-1}$ of the $k$ bases before it, and the codon position $\varphi(i) \in \{1, 2, 3\}$ of $x_i$. For the hypothesis "the stretch codes in frame $f$" ($f \in \{0, 1, 2\}$, the frame in which $x_f$ is the first base of a codon), $\varphi_f(i) = ((i - f) \bmod 3) + 1$.

**The parameters.** For order $k$, three tables $P_1, P_2, P_3$, where $P_c(b \mid w)$ is the probability of base $b$ at codon position $c$ after the context $w$. Each table has $4^k$ rows of 4 probabilities, so the coding model has $3 \cdot 4^{k+1}$ numbers. A non-coding model is an ordinary homogeneous chain $Q(b \mid w)$ of the same order, with $4^{k+1}$ numbers.

**The rule.** Reading in frame $f$, the chain emits $x_i$ from $P_{\varphi_f(i)}(\cdot \mid x_{i-k} \cdots x_{i-1})$, and the codon position steps $1 \to 2 \to 3 \to 1$ with each base. The probability of the stretch in frame $f$ is

$$P(x \mid \text{coding}, f) = \prod_{i} P_{\varphi_f(i)}(x_i \mid x_{i-k} \cdots x_{i-1}),$$

where the first $k$ bases use a lower order or an initial distribution. The three frames of the other strand use the same tables on the reverse complement of $x$. With the non-coding model, there are seven hypotheses: six frames and "non-coding".

**Training.** The maximum likelihood tables are counts. Let $N_c(w b)$ be the number of times the $(k+1)$-mer $w b$ occurs in the training genes with $b$ at codon position $c$. Then $P_c(b \mid w) = N_c(w b) / \sum_{b'} N_c(w b')$, usually with pseudocounts for rare contexts. The training genes can be long open reading frames of the genome itself, which almost never occur by chance.

**Assumptions.** The bases of a coding stretch follow one chain of order $k$ with a fixed period of 3; there are no frame shifts inside the stretch; the training genes are typical of the genes to find. The model does not know about start codons, stop codons or splice sites: those are the work of signal models and of the gene finder around it.

## What it counts

The model assigns a probability to a stretch of DNA under each of the seven hypotheses. With prior probabilities $\pi_h$ of the hypotheses, Bayes' rule gives the posterior

$$P(h \mid x) = \frac{\pi_h P(x \mid h)}{\sum_{h'} \pi_{h'} P(x \mid h')},$$

the probability that the stretch codes in frame $h$, or that it is non-coding. GeneMark computes this posterior for the frames of both strands at the same time, for fragments of the genome such as windows that slide along it, and reports the regions where a coding frame has a high posterior. Another common output is the log-odds score $\ln P(x \mid \text{coding}, f) - \ln P(x \mid \text{non-coding})$ of an [open reading frame](/open-reading-frame/), which is positive when the stretch looks like a gene in that frame.

**Example.** Take order $k = 0$ (each base depends only on its codon position), with the toy tables

| codon position | A | C | G | T |
|---|---|---|---|---|
| 1 | 0.3 | 0.2 | 0.4 | 0.1 |
| 2 | 0.3 | 0.2 | 0.1 | 0.4 |
| 3 | 0.1 | 0.4 | 0.3 | 0.2 |

and a uniform non-coding model, $Q(b) = 1/4$. Score $x = \mathrm{GATGAC}$ on the forward strand.

- Frame 0 reads the codons GAT and GAC, so the codon positions are 1, 2, 3, 1, 2, 3: $0.4 \cdot 0.3 \cdot 0.2 \cdot 0.4 \cdot 0.3 \cdot 0.4 = 0.001152$.
- Frame 1 puts $x_0 = G$ at position 3, so the positions are 3, 1, 2, 3, 1, 2: $0.3 \cdot 0.3 \cdot 0.4 \cdot 0.3 \cdot 0.3 \cdot 0.2 = 0.000648$.
- Frame 2 gives positions 2, 3, 1, 2, 3, 1: $0.1 \cdot 0.1 \cdot 0.1 \cdot 0.1 \cdot 0.1 \cdot 0.2 = 0.000002$.
- Non-coding: $0.25^6 \approx 0.000244$.

With equal priors on these four hypotheses (the reverse strand is left out to keep the example short), the posteriors are 0.563 for frame 0, 0.317 for frame 1, 0.001 for frame 2 and 0.119 for non-coding. The log-odds score of frame 0 is $\ln(0.001152 / 0.000244) \approx 1.55$. Six bases do not decide much; over a gene of a few hundred bases the log-odds terms add up, and the right frame wins clearly.

## Relation to other models

- **[Markov chain](/markov-chain/).** If $P_1 = P_2 = P_3$, the model is a homogeneous Markov chain of order $k$. A three-periodic chain is a homogeneous chain on the pairs (codon position, context), in which the codon position moves around a cycle of length 3.
- **[Hidden Markov model](/hidden-markov-model/).** The codon position is a hidden state with a fixed cycle $1 \to 2 \to 3 \to 1$. Add states for non-coding DNA, for the other strand and for the start and stop signals, and let the decoder choose where the frames begin and end: that is the step from GeneMark to GeneMark.hmm (Lukashin and Borodovsky 1998), and from a window score to a full parse with the [Viterbi algorithm](/viterbi-algorithm/).
- **[Interpolated Markov model](/interpolated-markov-model/).** Glimmer keeps the three periodic tables but mixes the orders 0 to 8 for each context, with weights set by how much data supports each context, in place of one fixed order.
- **[Generalized HMM gene finders](/generalized-hmm-gene-finder/).** The exon states of a GHMM score their segments with a three-periodic chain; the phase of the exon fixes the codon position of its first base.
- **Codon statistics.** In a model of order 2 or more, the counts at codon position 3 include the codon counts of the training genes; a [codon adaptation index](/codon-adaptation-index/) uses the codon frequencies of highly expressed genes only. Order 5, which Salzberg et al. (1998) give as the basis of GeneMark, covers the codon and the codon before it.
- **[n-gram models](/n-gram-language-model/).** An order $k$ chain is a $(k+1)$-gram model of DNA, and the counts are those of [k-mers](/kmer/) split by codon position.

## Known results in the model

- **Closed-form training.** The maximum likelihood estimates are the normalized counts by codon position. No iteration is needed when the training genes are known.
- **Linear time for all frames.** One pass over a sequence computes the log-probabilities of every base under the three codon positions; prefix sums of them give the score of any stretch in any frame in $O(1)$. A window scan of a genome of length $n$ therefore takes $O(n)$ time for all six frames.
- **Size of the model.** The number of probabilities grows as $4^{k+1}$ per codon position. Salzberg et al. (1998) count 24 576 for six fifth-order submodels, and note that in a genome of 1.8 million bases many 7-mers do not occur often enough to estimate a sixth-order model. This limit led to the interpolated Markov model.
- **Accuracy on a bacterial genome.** On the *Haemophilus influenzae* genome with 1717 annotated genes, a fixed fifth-order three-periodic model trained on long ORFs found 1574 of them (91.7%), and Glimmer's IMM found 1680 (97.8%), with the same training set and post-processing (Salzberg et al. 1998, Table 1).
- **Both strands at once.** Scoring all six frames and the non-coding hypothesis together, as Borodovsky and McIninch did, lets the posterior of the true frame compete with the frames on the other strand, which a strand-by-strand scan does not do.
- **From windows to gene boundaries.** A window posterior gives coding regions, not exact starts. Placing the same models in a hidden Markov model whose state changes are the gene boundaries made exact gene prediction significantly more accurate (Lukashin and Borodovsky 1998).

## References
