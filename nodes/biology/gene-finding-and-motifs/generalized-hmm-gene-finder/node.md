---
tag: FHW813
kind: algorithm
slug: generalized-hmm-gene-finder
name: Generalized HMM gene finding
aliases:
- GHMM gene finder
- GENSCAN model
area: biology/gene-finding-and-motifs
level: advanced
summary: Parse a genome into exons, introns and intergenic regions with a generalized HMM, whose states emit whole segments with explicit length distributions, decoded by a segment Viterbi recursion.
model: real-ram
complexity:
  vars: {n: the length of the sequence, K: the number of states, D: the largest segment length of a state}
  time: {worst: Θ(n K D + n K^2), average: Θ(n K D + n K^2), best: Θ(n K D + n K^2)}
  space: {extra: Θ(n K)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [hidden-markov-model, viterbi-algorithm, hidden-semi-markov-model]
see_also: [gene-prediction, splice-site-prediction, maximal-dependence-decomposition, periodic-markov-chain-gene-model, interpolated-markov-model, forward-backward-algorithm, comparative-gene-finding, conditional-random-field]
sources:
  - paper: doi:10.1006/jmbi.1997.0951
    title: Chris Burge and Samuel Karlin, Prediction of complete gene structures in human genomic DNA, Journal of Molecular Biology 268(1), 1997
    locator: pp. 78 to 94; the GENSCAN state diagram (exon, intron and intergenic states on both strands, introns in three phases), the length distributions, and the signal models for splice sites and start and stop codons
  - url: https://pubmed.ncbi.nlm.nih.gov/8877513/
    title: David Kulp, David Haussler, Martin G. Reese and Frank H. Eeckman, A generalized hidden Markov model for the recognition of human genes in DNA, Proceedings of ISMB 4, 1996, pp. 134 to 142
    locator: the GHMM that describes the legal parses of a DNA sequence into gene parts (the Genie gene finder)
  - paper: doi:10.1016/j.artint.2009.11.011
    title: Shun-Zheng Yu, Hidden semi-Markov models, Artificial Intelligence 174(2), 2010
    locator: pp. 215 to 243, Section 3.1, the explicit duration model and the cost of its recursions
---

A generalized hidden Markov model (GHMM) is a [hidden Markov model](/hidden-markov-model/) in which a state emits a whole segment of the sequence at once, not one letter. Each state has its own length distribution and its own model of the letters of a segment. For gene finding, the states are the parts of a gene: intergenic DNA, exons, introns, and the signals between them. A path through the states that covers the sequence is a *parse*, a complete gene structure such as "intergenic, exon from 1001 to 1210, intron to 1874, exon to 2050, intergenic". The decoder finds the parse of largest probability with a segment form of the [Viterbi algorithm](/viterbi-algorithm/): for each end position and state, it tries every segment length. Kulp, Haussler, Reese and Eeckman (1996) used a GHMM for the Genie gene finder, and Burge and Karlin (1997) built GENSCAN on the same idea. The model is the [hidden semi-Markov model](/hidden-semi-markov-model/) of speech recognition, with segment models suited to DNA.

## In plain words

A gene has parts of different kinds and lengths. Exons have a typical length that is not well described by a coin that decides at each letter whether to stop, and introns must start with GT and end with AG. A GHMM lets each kind of part choose its length from a table and then write all of its letters at once, in its own style. To read a DNA sequence, the decoder walks from left to right. At each position and for each kind of part, it asks: if a part of this kind ends here, what is the best length for it, and what was the best explanation of everything before it? It writes down the answer, and at the end it follows the answers back to recover the best list of parts.

## The problem

**Input.** A sequence $x = x_1 \cdots x_n$, and a GHMM with states $Q = \{1, \ldots, K\}$ and, for each state $q$: a start probability $\pi_q$, an end weight $\epsilon_q$, transition probabilities $a_{pq}$ to other states, a length distribution $d_q(l)$ for $1 \le l \le D_q$, and a segment model $f_q(x[a, b))$, the probability that state $q$ emits the bases $x[a, b)$ as one segment of length $b - a$.

**Output.** A parse $(q_1, b_0, b_1), (q_2, b_1, b_2), \ldots, (q_m, b_{m-1}, b_m)$ with $0 = b_0 < b_1 < \cdots < b_m = n$ that maximizes

$$P(x, \text{parse}) = \pi_{q_1} \Big(\prod_{r=2}^{m} a_{q_{r-1} q_r}\Big) \Big(\prod_{r=1}^{m} d_{q_r}(b_r - b_{r-1}) \, f_{q_r}(x[b_{r-1}, b_r))\Big) \, \epsilon_{q_m}.$$

The segment model $f_q$ can be anything that scores a whole segment. In a gene finder, the segment model of an exon is a *content sensor*, such as a [three-periodic Markov chain](/periodic-markov-chain-gene-model/) whose phase follows the reading frame, times *signal sensors* at its ends, such as a [splice site model](/splice-site-prediction/) for the donor and acceptor, or a model of the start or stop codon. A segment that breaks a hard rule, such as an exon with an in-frame stop codon or an intron that does not start with GT, gets probability 0. The finding of the best parse is the [gene prediction](/gene-prediction/) problem for this model.

## The algorithm

Let $\Gamma_b(q)$ be the best log score of a parse of $x[0, b)$ whose last segment has state $q$ and ends at $b$, and let $\Delta_b(q) = \max_p (\Gamma_b(p) + \ln a_{pq})$ be the best log score of such a parse followed by a step into $q$. Positions are 0-based and intervals half-open.

```pseudo id=main
GHMM-VITERBI(x, model)
L1  for b ← 1 to n do
L2      for each state q do
L3          Γ[b][q] ← -∞
L4          for l ← 1 to min(D_q, b) do
L5              enter ← ln π_q if l = b, else Δ[b - l][q]
L6              s ← enter + ln d_q(l) + ln f_q(x[b - l, b))
L7              if s > Γ[b][q] then Γ[b][q] ← s; back[b][q] ← l
L8      for each state q: Δ[b][q] ← max over p of Γ[b][p] + ln a_pq, and keep the best p
L9  q ← the state with the largest Γ[n][q] + ln ε_q
L10 trace back from (n, q): emit the segment (q, n - l, n) with l = back[n][q], move to (n - l, the best p of Δ[n - l][q]), and repeat until position 0
L11 return the segments in order
```

Line L8 precomputes the best way to enter each state at each position, so the loop over lengths does not loop over the previous state too. The segment score of line L6 must take $O(1)$ time. For a Markov content model this comes from prefix sums: store $P[i] = \sum_{j < i} \ln p(x_j)$ once, and the score of any segment is $P[b] - P[a]$. A three-periodic model needs three prefix arrays, one for each phase of the segment start.

## Example

Take a GHMM with two states, N (AT-rich) and G (GC-rich). N emits A and T with probability 0.4 each and C and G with 0.1 each; G does the opposite. N has a uniform length on 1 to 10, so $d_N(l) = 1/10$; G has a uniform length on 2 to 10, so $d_G(l) = 1/9$ and $d_G(1) = 0$. The start probabilities are $1/2$, every state may end the sequence, and the states alternate: $a_{NG} = a_{GN} = 1$ and $a_{NN} = a_{GG} = 0$. Decode $x = \mathrm{ATGCGCGCAT}$. The table gives $\Gamma_b(N)$ and $\Gamma_b(G)$ in natural logarithms, rounded, with the best length $l$ in brackets.

| $b$ | base $x_b$ | $\Gamma_b(N)$ [$l$] | $\Gamma_b(G)$ [$l$] |
|---|---|---|---|
| 1 | A | $-3.912$ [1] | $-\infty$ |
| 2 | T | $-4.828$ [2] | $-7.496$ [2] |
| 3 | G | $-7.131$ [3] | $-8.412$ [3] |
| 4 | C | $-9.433$ [4] | $-8.858$ [2] |
| 5 | G | $-11.736$ [5] | $-9.774$ [3] |
| 6 | C | $-14.039$ [6] | $-10.691$ [4] |
| 7 | G | $-15.296$ [1] | $-11.607$ [5] |
| 8 | C | $-16.212$ [1] | $-12.523$ [6] |
| 9 | A | $-15.742$ [1] | $-14.826$ [7] |
| 10 | T | $-16.658$ [2] | $-17.128$ [8] |

For example, $\Gamma_4(G)$ with $l = 2$ enters G at position 2 from the N segment AT, $\Gamma_2(N) = \ln \frac12 + \ln \frac1{10} + 2 \ln 0.4 = -4.828$, and adds $\ln \frac19 + 2 \ln 0.4 = -4.030$, for $-8.858$. At $b = 10$ the better end is N with $-16.658$ and $l = 2$, so the last segment is N on $[8, 10)$. It was entered from G at position 8, whose best length is 6, so the segment before is G on $[2, 8)$, and it was entered from N at position 2 with length 2. The parse is N $[0, 2)$, G $[2, 8)$, N $[8, 10)$, with log probability $-16.658$. A single N segment scores $-20.476$, and a single G segment $-17.598$: the two extra segments cost $\ln \frac1{10} + \ln \frac19$, but placing GCGCGC in the GC-rich state gains more.

## Correctness

The best partial parse that ends with a segment $(q, b - l, b)$ consists of a best partial parse of $x[0, b - l)$, then a step into $q$, then the segment. The terms of the last step depend only on $q$, $l$, $b$ and the previous state, so the best prefix can be chosen independently, and $\Gamma_b(q) = \max_l (\Delta_{b-l}(q) + \ln d_q(l) + \ln f_q(x[b - l, b)))$, with $\ln \pi_q$ in place of $\Delta_0(q)$. Lines L3 to L7 compute this maximum, and line L8 computes $\Delta_b$ from the finished row. By induction on $b$ the tables are right, line L9 picks the best end, and the stored choices of line L10 rebuild a parse with exactly that score. The full proof is in the proofs folder, and the test file checks the decoder against the enumeration of all parses of short sequences.

## Complexity

- **Time.** For each of the $n$ positions and $K$ states, line L4 tries up to $D$ lengths, and line L8 costs $K^2$. With segment scores in $O(1)$, the time is $\Theta(n K D + n K^2)$, that is $O(n D)$ per state. With $D$ equal to $n$, the general GHMM costs $\Theta(n^2 K)$, which is too slow for a chromosome.
- **Space.** The tables $\Gamma$, $\Delta$ and the back pointers take $\Theta(n K)$.
- **How gene finders stay linear.** Burge and Karlin give introns and intergenic regions geometric length distributions. A state with a geometric length is an ordinary HMM state with a self-loop, so it costs $O(1)$ per position instead of $O(D)$. Only exons have general length distributions, and an exon cannot contain an in-frame stop codon, so its candidate starts at each end position are limited to the current open reading frame. With a list of candidate signals (splice sites, start and stop codons), the loop of line L4 runs only over the candidates.

## Properties

- **Exact for its model.** The decoder returns a parse of largest probability. The quality of the gene structure depends on the model.
- **An HMM is a special case.** If every $D_q = 1$, a GHMM is an HMM, and the recursion is the ordinary Viterbi algorithm. The test file checks this case.
- **Explicit lengths.** An HMM state has a geometric length distribution, whose most likely length is 1. Exons have a peaked length distribution, which only an explicit $d_q$ can model well.
- **Modular.** Each state can use its own segment model: a Markov chain, a position weight matrix, a [maximal dependence decomposition](/maximal-dependence-decomposition/) tree, or a whole sub-model. The decoder needs only the segment scores.
- **Hard constraints.** Rules such as GT at the start of an intron, no in-frame stop codon in an exon, and a total coding length that is a multiple of 3 are written as zero probabilities. The phase rule needs one intron state for each of the three phases, as in GENSCAN, so that the frame of the next exon follows from the frame of the previous one.

## Variants and improvements

- **Posterior probabilities.** The segment forms of the forward and backward recursions (see [forward-backward](/forward-backward-algorithm/)) give the probability of each exon given the sequence. GENSCAN reports such a probability for each predicted exon.
- **Both strands.** A full gene finder has a mirror copy of every gene state for the reverse strand, with reverse-complemented models.
- **Training.** The parameters come from a set of annotated genes: length tables from the observed lengths, segment models from counts. With labeled data these are [maximum likelihood estimates](/maximum-likelihood-estimation/) and need no iteration; the [Baum-Welch](/baum-welch-algorithm/) form of EM is used when the labels are missing.
- **Comparative and discriminative models.** A pair GHMM or a phylogenetic GHMM scores two or more genomes at once ([comparative gene finding](/comparative-gene-finding/)). A semi-Markov [conditional random field](/conditional-random-field/) uses the same decoder with weights trained to separate correct from wrong parses.
- **External evidence.** Alignments of proteins or transcripts can be added as extra factors in the segment scores, which turns the GHMM into a combiner of evidence.

## When to use it

Use a GHMM to predict complete gene structures in eukaryotic genomes, where genes are split into exons and introns and the signals at their ends are weak. It is the core of *ab initio* gene prediction. For bacterial genomes, where most genes are single open reading frames, a simpler model, such as an [interpolated Markov model](/interpolated-markov-model/) on each ORF, is usually enough. When transcripts or close genomes are available, combine the GHMM with that evidence.

## Pitfalls

- **Quadratic time.** A general length distribution on every state makes the decoder $\Theta(n^2 K)$. Bound the lengths, or make the long states geometric.
- **Segment scores must be fast.** Scoring a segment by a loop over its bases adds a factor $D$. Use prefix sums.
- **Phase errors.** Without separate intron states for the three phases, the decoder can join exons whose frames do not fit, and the predicted protein is wrong after the first intron.
- **Underflow and minus infinity.** Work in log space and skip impossible terms; adding $-\infty$ to $+\infty$ by mistake gives NaN.
- **Probabilities that are not comparable.** The segment scores of different states must be probabilities of the same bases. A state whose model ignores part of its segment gets an unfair advantage.
- **Ties.** Equal scores are common with integer-valued toy models. Fix a rule, such as the shortest length and the smallest state index, so that the output is the same on every run.

## Implementations

## History

Kulp, Haussler, Reese and Eeckman (1996) described a GHMM for human genes, in which each state models a whole gene part with its own length and content model. Burge and Karlin (1997) published GENSCAN, a GHMM with exon, intron and intergenic states on both strands, introns in three phases, geometric lengths for introns and intergenic regions, and signal models for the splice sites and the start and stop codons. The model is the explicit duration HMM, which Ferguson introduced for speech in 1980 and which Yu (2010) surveys as the hidden semi-Markov model.

## References
