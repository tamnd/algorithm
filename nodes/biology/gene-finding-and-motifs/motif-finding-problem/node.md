---
tag: YHVM5G
kind: problem
slug: motif-finding-problem
name: Motif finding
aliases:
- motif discovery
- regulatory motif finding
area: biology/gene-finding-and-motifs
level: core
summary: Given sequences thought to share binding sites, find the short pattern or weight matrix over-represented in them.
prereqs: [hamming-distance, consensus-sequence, position-specific-scoring-matrix]
see_also: [median-string-problem, planted-motif-problem, motif-information-content, sequence-logo, gibbs-motif-sampler, meme-algorithm, phylogenetic-footprinting, np-hard]
sources:
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Chapter 4, Sections 4.6 to 4.9 (the motif finding problem, search trees, finding motifs and finding a median string)
  - book: isbn:9780990374619
    title: Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms, An Active Learning Approach, Volume I, 2nd edition, Active Learning Publishers, 2015
    locator: Chapter 2, Sections 2.3 (scoring motifs) and 2.4 (from motif finding to finding a median string)
  - paper: doi:10.1006/jcss.2002.1823
    title: Ming Li, Bin Ma and Lusheng Wang, Finding similar regions in many sequences, Journal of Computer and System Sciences 65(1), 2002
    locator: the Consensus Patterns problem, its NP-hardness and its polynomial-time approximation scheme
  - paper: doi:10.1093/bioinformatics/15.7.563
    title: Gerald Z. Hertz and Gary D. Stormo, Identifying DNA and protein patterns with statistically significant alignments of multiple sequences, Bioinformatics 15, 1999
    locator: the information content score of an alignment of sites and its p-value
  - paper: doi:10.1126/science.8211139
    title: Charles E. Lawrence, Stephen F. Altschul, Mark S. Boguski, Jun S. Liu, Andrew F. Neuwald and John C. Wootton, Detecting subtle sequence signals, a Gibbs sampling strategy for multiple alignment, Science 262(5131), 1993
    locator: pp. 208 to 214, the site sampler for one site in each sequence
---

Motif finding asks for a short pattern that occurs, with small changes, in each of a set of sequences that are thought to share a function. The usual input is a set of DNA regions upstream of genes that one transcription factor controls, and the pattern is the binding site of that factor. The output is one window in each sequence, the starts of the sites, and a summary of them: a [consensus sequence](/consensus-sequence/) or a [position-specific scoring matrix](/position-specific-scoring-matrix/). The common score counts the letters of the windows that differ from the consensus. With this score the problem is NP-hard, and it is equivalent to the [median string problem](/median-string-problem/).

## In plain words

You have a few DNA pieces, perhaps a few hundred letters each. Somewhere in each piece there is a short word, such as a word of 15 letters, that a protein binds to. The copies of the word are not exact: each copy can have a few letters changed. You do not know the word, and you do not know where the copies are.

The job is to pick one window of the right length in each piece so that the picked windows look as much alike as possible. Write the windows one under the other. In each column, find the most common letter, and count the letters that are not that letter. A small total means a good choice. The most common letters, read across, give the guess for the hidden word.

## Definition

**Input.** Sequences $s_1, \ldots, s_n$ over the alphabet $\{A, C, G, T\}$, each of length $G$, and a motif length $L \le G$. Each sequence has $W = G - L + 1$ windows of length $L$. Positions on this page are 1-based; the code of the method pages uses 0-based positions.

**A choice of sites** is a vector $p = (p_1, \ldots, p_n)$ with $1 \le p_i \le W$. It picks the window $t_i = s_i[p_i .. p_i + L - 1]$ in each sequence. Write the windows as the rows of an $n \times L$ alignment matrix. For a column $j$ and a letter $a$, let $c_j(a)$ be the number of rows with $a$ in column $j$. The *profile* is the matrix $c_j(a)/n$.

**The score.** The consensus of $p$ has in column $j$ a letter with the largest count $c_j(a)$. The score is the number of letters that differ from the consensus,

$$\mathrm{Score}(p) = \sum_{j=1}^{L} \Big(n - \max_a c_j(a)\Big).$$

**The question.** Find a choice $p$ with the smallest score. Jones and Pevzner write the same objective as the largest value of $\sum_j \max_a c_j(a) = nL - \mathrm{Score}(p)$; the two forms have the same optimal choices.

**Lemma (the consensus is the best center).** For a fixed $p$ and any string $v$ of length $L$, $\sum_i d_H(v, t_i) \ge \mathrm{Score}(p)$, where $d_H$ is the [Hamming distance](/hamming-distance/), with equality exactly when $v$ is a consensus of $p$.

*Proof.* Count the mismatches by columns. Column $j$ adds $n - c_j(v_j)$ to $\sum_i d_H(v, t_i)$, and $n - c_j(v_j) \ge n - \max_a c_j(a)$, with equality exactly when $v_j$ has the largest count. Sum over $j$. $\square$

So the score of a choice is the total Hamming distance from its windows to their best center. This is the step that turns the problem into the median string problem below.

## Variants

- **The total distance score.** The score above. It is the Consensus Patterns problem of Li, Ma and Wang.
- **The largest distance score.** Ask for a center $v$ and windows with $\max_i d_H(v, t_i) \le d$. This is the closest substring problem. With random background sequences it is the [planted motif problem](/planted-motif-problem/).
- **Information content.** Score the matrix by its [information content](/motif-information-content/), the relative entropy of the column frequencies against the background. CONSENSUS (Hertz and Stormo) and MEME use scores of this kind. A rare letter in a column counts more than a common one.
- **Likelihood models.** Treat the sites as draws from a column-wise model and the rest as background, and fit the model by maximum likelihood ([MEME](/meme-algorithm/), with [expectation maximization](/expectation-maximization/)) or sample it ([Gibbs motif sampler](/gibbs-motif-sampler/), with [Gibbs sampling](/gibbs-sampling/)). The models differ in how many sites a sequence may hold: exactly one, zero or one, or any number.
- **Both strands.** A binding site can be on either strand of the DNA, so a method may also scan the reverse complement of each sequence.
- **Gaps and spacers.** Some sites have two halves with a spacer of variable length between them. Gapped motifs need other models, such as a [profile HMM](/profile-hmm/).

## Examples

Take the five sequences of length $G = 12$ from the sample of Rosalind problem BA2D, with $L = 3$, so $W = 10$:

| $i$ | $s_i$ |
|---|---|
| 1 | GGCGTTCAGGCA |
| 2 | AAGAATCAGTCA |
| 3 | CAAGGAGTTCGC |
| 4 | CACGTCAATCAC |
| 5 | CAATAATATTCG |

The choice $p = (7, 7, 1, 6, 1)$ picks CAG, CAG, CAA, CAA and CAA. The first two columns are all C and all A, and the third column has two G and three A. So the consensus is CAA and the score is $0 + 0 + 2 = 2$. The choice $p = (5, 5, 8, 8, 9)$ picks TTC, ATC, TTC, ATC and TTC, with consensus TTC and score $2 + 0 + 0 = 2$.

An exhaustive check of all $10^5$ choices finds that 2 is the smallest score, and that 14 choices reach it. So the problem can have many optimal answers with different consensus strings. The median strings of the same input, with total distance 2, are CAA, TCA and TTC.

The sizes grow fast. In the challenge of Pevzner and Sze, $n = 20$, $G = 600$ and $L = 15$, so $W = 586$ and there are $586^{20} \approx 2.28 \times 10^{55}$ choices of sites. There are only $4^{15} = 1{,}073{,}741{,}824$ strings of length 15, which is why exact methods search the strings and not the sites.

## Known algorithms

| method | type | time | source |
|---|---|---|---|
| all choices of sites | exact | $O(L n W^n)$ | Jones and Pevzner, Section 4.6 |
| all strings of length $L$ (median string) | exact | $O(4^L n W L)$ | Jones and Pevzner, Section 4.9 |
| [branch and bound](/branch-and-bound-motif-search/) on either tree | exact | same worst case, often much less | Jones and Pevzner, Sections 4.7 to 4.9 |
| [greedy motif search](/greedy-motif-search/) | heuristic | $O(W^2 n L)$ | Hertz, Hartzell and Stormo 1990; Compeau and Pevzner, Section 2.5 |
| [randomized motif search](/randomized-motif-search/) | heuristic, randomized | $O(n W L)$ per iteration | Compeau and Pevzner, Section 2.7 |
| [Gibbs motif sampler](/gibbs-motif-sampler/) | heuristic, randomized | $O(W L)$ per step | Lawrence et al. 1993 |
| [MEME](/meme-algorithm/) | local optimum of a likelihood | $O(n W L)$ per iteration | Bailey and Elkan 1994 |
| [WINNOWER](/winnower-algorithm/) | graph filter for $(L, d)$ motifs | polynomial per round | Pevzner and Sze 2000 |
| [PROJECTION](/random-projection-motif-finding/) | randomized hashing and EM | depends on the number of trials | Buhler and Tompa 2002 |
| polynomial-time approximation scheme | approximation, total distance | polynomial for each fixed ratio | Li, Ma and Wang 2002 |

## Bounds

- **NP-hard.** With the total distance score and $L$ part of the input, the problem is NP-hard; this is the Consensus Patterns result of Li, Ma and Wang (2002). So no exact method runs in polynomial time unless P = NP. See [NP-hard](/np-hard/).
- **Fixed motif length.** For a fixed $L$, the median string search tries $4^L$ strings, each in $O(nWL)$ time, so the time is polynomial in $n$ and $G$.
- **Fixed number of sequences.** For a fixed $n$, the $W^n$ choices of sites can be tried one by one, so the time is polynomial in $G$ and $L$.
- **Approximation.** Li, Ma and Wang give a polynomial-time approximation scheme for the total distance score: for each $\epsilon > 0$, a choice with score at most $(1 + \epsilon)$ times the optimum. Its running time is polynomial in the input for each fixed $\epsilon$, but the exponent grows fast as $\epsilon$ falls, and it is not used in practice.
- **A trivial bound.** Every choice has $0 \le \mathrm{Score}(p) \le L(n - \lceil n/4 \rceil)$, because the largest of four counts that add to $n$ is at least $\lceil n/4 \rceil$.

## Reductions

- **To the median string problem.** By the lemma, $\min_p \mathrm{Score}(p) = \min_p \min_v \sum_i d_H(v, t_i)$. Swap the two minima: for a fixed $v$, the best window of each sequence can be picked on its own, which gives the total distance $D(v) = \sum_i \min_{q} d_H(v, s_i[q .. q + L - 1])$. So the smallest score equals the smallest $D(v)$, and an optimal $v$ with its closest windows is an optimal choice of sites. The [median string problem](/median-string-problem/) page gives the full proof.
- **To closest substring.** With the largest distance in place of the sum, the same swap gives the closest substring problem: a string $v$ and a window in each sequence, all within distance $d$ of $v$. The [planted motif problem](/planted-motif-problem/) is this problem on random input.
- **From the sites to a scanner.** An optimal choice gives an alignment of sites. Its counts, with pseudocounts and a background, give a [position-specific scoring matrix](/position-specific-scoring-matrix/), and the matrix can then scan new sequences. The [p-value of a matrix score](/pwm-score-p-value/) says how strong a hit is.

## Applications

- **Transcription factor binding sites.** Find the site of a factor in the promoters of genes that it controls, for example genes that change together in an expression experiment or regions bound in a ChIP experiment.
- **Phylogenetic footprinting.** Find sites that stay the same in the regions upstream of one gene in several species. See [phylogenetic footprinting](/phylogenetic-footprinting/).
- **Protein motifs.** The Gibbs site sampler was first used on protein sequences, to align short conserved blocks of distant proteins. The alphabet then has 20 letters.
- **Motif databases and logos.** The found sites give a matrix for a database of binding profiles and a [sequence logo](/sequence-logo/) for display.

## References
