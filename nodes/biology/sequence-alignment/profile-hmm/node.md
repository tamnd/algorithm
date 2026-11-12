---
tag: MM4SQ5
kind: model
slug: profile-hmm
name: Profile hidden Markov model
aliases:
- profile HMM
- plan 7 model
area: biology/sequence-alignment
level: advanced
summary: "An HMM with a match, an insert and a delete state for each column of a family alignment. It gives each sequence a probability, and its Viterbi path aligns the sequence to the family."
prereqs: [hidden-markov-model, position-specific-scoring-matrix]
see_also: [hmmer, pair-hmm, sequence-profile-alignment, multiple-sequence-alignment, viterbi-algorithm, forward-algorithm, baum-welch-algorithm, sequence-logo]
sources:
  - paper: doi:10.1006/jmbi.1994.1104
    title: Anders Krogh, Michael Brown, I. Saira Mian, Kimmen Sjölander and David Haussler, Hidden Markov models in computational biology, applications to protein modeling, Journal of Molecular Biology 235(5), 1994, pages 1501 to 1531
    locator: the architecture with match, insert and delete states for each position, training from unaligned sequences, and the application to globins, protein kinase catalytic domains and EF-hand motifs
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: "Chapter 5 (from page 100): profile HMMs from ungapped matrices, insert and delete states, estimation from a multiple alignment, the Viterbi and Forward equations for search, non-global variants, pseudocounts and Dirichlet priors, model construction, and sequence weighting"
  - paper: doi:10.1093/bioinformatics/12.4.327
    title: Kimmen Sjölander, Kevin Karplus, Michael Brown, Richard Hughey, Anders Krogh, I. Saira Mian and David Haussler, Dirichlet mixtures, a method for improved detection of weak but significant protein sequence homology, CABIOS 12(4), 1996, pages 327 to 345
    locator: Dirichlet mixture priors for the match emission probabilities
  - paper: doi:10.1093/bioinformatics/14.9.755
    title: Sean R. Eddy, Profile hidden Markov models, Bioinformatics 14(9), 1998, pages 755 to 763
    locator: review of profile HMMs and of the Plan 7 architecture of HMMER, with no transitions between insert and delete states
  - paper: doi:10.1371/journal.pcbi.1000069
    title: Sean R. Eddy, A probabilistic model of local sequence alignment that simplifies statistical significance estimation, PLoS Computational Biology 4(5), 2008, e1000069
    locator: Gumbel Viterbi scores and exponential-tail Forward scores with lambda near log 2 for local profile HMM alignment
---

A profile hidden Markov model describes a family of sequences by a chain of nodes, one for each conserved column of the family's [multiple sequence alignment](/multiple-sequence-alignment/). Each node has a match state that emits the column's residues, an insert state that emits extra residues after the column, and a silent delete state that skips the column. The model gives a probability $P(x \mid \text{model})$ to every sequence $x$, and the most probable state path is an alignment of $x$ to the family. Krogh, Brown, Mian, Sjölander and Haussler (1994) introduced the model, and HMMER, SAM and the Pfam database are built on it.

## The machine

**States.** A model of length $m$ has a silent Begin state $M_0$, a silent End state $M_{m+1}$, and, for each node:

| state | count | emits | role in the alignment |
|---|---|---|---|
| match $M_k$ | $k = 1, \ldots, m$ | one residue, with probability $e_{M_k}(a)$ | the residue of column $k$ |
| insert $I_k$ | $k = 0, \ldots, m$ | one residue, with probability $e_{I_k}(a)$ | residues between columns $k$ and $k+1$ |
| delete $D_k$ | $k = 1, \ldots, m$ | nothing | column $k$ is missing |

**Transitions.** Each state of node $k$ moves forward to $M_{k+1}$ or $D_{k+1}$, or to $I_k$; each insert state can repeat. In the form of Krogh et al. and Durbin et al., all nine moves $\{M, I, D\}_k \to \{M_{k+1}, I_k, D_{k+1}\}$ are allowed. The Plan 7 form of HMMER drops $D_k \to I_k$ and $I_k \to D_{k+1}$, which leaves seven transitions per node; the name Plan 7 comes from this count. The states of node $k$ go only to node $k$ or node $k + 1$, so every path visits the nodes in order and the model is a left-to-right HMM.

**Emissions.** The match emissions are the rows of a [PSSM](/position-specific-scoring-matrix/) in probability form. The insert emissions are usually set to the background $q$, so inserted residues score 0 in log-odds units; the position-specific information about inserts is in the transitions.

**A run.** Start at $M_0$, follow transitions, and emit a residue at every match and insert state until $M_{m+1}$. The emitted sequence $x$ and the path $\pi$ together give an alignment of $x$ to the $m$ columns: $M_k$ puts a residue in column $k$, $D_k$ puts a gap there, and $I_k$ puts a residue between columns $k$ and $k + 1$ that no other sequence needs to share.

**Building a model from an alignment.** Durbin et al. (Chapter 5) describe the standard construction:

1. Mark the match columns. A common rule marks a column as a match column if at least half its entries are residues; HMMER calls this fraction `symfrac` and uses 0.5 by default (after sequence weighting).
2. Read the state path of each row: a residue in a match column is $M_k$, a gap there is $D_k$, and a residue in another column is $I_k$ for the last match column $k$ to its left.
3. Count the transitions and the emissions over all rows, add pseudocounts or a Dirichlet prior (Sjölander et al. 1996), and normalize each state's outgoing transitions and emissions.

Durbin et al. also give a dynamic program that chooses the set of match columns with the highest posterior probability instead of the 50 percent rule.

**Example.** Take the six DNA rows

```
r1  T A T A - A T
r2  T A T G - A A
r3  T A T G - A T
r4  C A T A G A T
r5  T A - A - G T
r6  T G T G T A C
```

Column 5 has only two residues, so it becomes insert $I_4$, and $m = 6$. Row r5 has the path $M_1 M_2 D_3 M_4 M_5 M_6$; row r4 has $M_1 M_2 M_3 M_4 I_4 M_5 M_6$. With one pseudocount on every transition and every emission:

| node $k$ | out of $M_k$: to $M, I, D$ | out of $I_k$: to $M, I, D$ | out of $D_k$: to $M, I, D$ |
|---|---|---|---|
| 0 (Begin) | 7/9, 1/9, 1/9 | 1/3, 1/3, 1/3 | none |
| 1 | 7/9, 1/9, 1/9 | 1/3, 1/3, 1/3 | 1/3, 1/3, 1/3 |
| 2 | 6/9, 1/9, 2/9 | 1/3, 1/3, 1/3 | 1/3, 1/3, 1/3 |
| 3 | 3/4, 1/8, 1/8 | 1/3, 1/3, 1/3 | 1/2, 1/4, 1/4 |
| 4 | 5/9, 3/9, 1/9 | 3/5, 1/5, 1/5 | 1/3, 1/3, 1/3 |
| 5 | 7/9, 1/9, 1/9 | 1/3, 1/3, 1/3 | 1/3, 1/3, 1/3 |
| 6 | to End 7/8, to $I_6$ 1/8 | to End 1/2, to $I_6$ 1/2 | to End 1/2, to $I_6$ 1/2 |

The match emissions are $e_{M_1}$: T 3/5, C 1/5, A and G 1/10; $e_{M_3}$: T 2/3, others 1/9; $e_{M_4}$: A and G 2/5, C and T 1/10; and so on. The insert state $I_4$, which saw G and T, emits A 1/6, C 1/6, G 1/3, T 1/3. The transition $M_4 \to I_4$ has probability 1/3, against 1/9 for the other match states, so the model has learned where this family puts its insertions. In the Plan 7 form, $D_3$ has only two moves, to $M_4$ with probability 2/3 and to $D_4$ with 1/3.

## What it counts

**Probability of a sequence and its alignment.** For a path $\pi$, $P(x, \pi)$ is the product of its transition and emission probabilities. The model scores $x$ by the best path or by the sum over paths, each against a null model, usually $P(x \mid R) = \prod_i q_{x_i}$.

**Viterbi recurrences.** In log-odds form, with $V^M_k(i)$ the best score of a path that emits $x_1 \ldots x_i$ and ends in $M_k$ (Durbin et al., Chapter 5):

$$V^M_k(i) = \log \frac{e_{M_k}(x_i)}{q_{x_i}} + \max \begin{cases} V^M_{k-1}(i-1) + \log a_{M_{k-1} M_k} \\ V^I_{k-1}(i-1) + \log a_{I_{k-1} M_k} \\ V^D_{k-1}(i-1) + \log a_{D_{k-1} M_k} \end{cases}$$

$$V^I_k(i) = \log \frac{e_{I_k}(x_i)}{q_{x_i}} + \max \begin{cases} V^M_k(i-1) + \log a_{M_k I_k} \\ V^I_k(i-1) + \log a_{I_k I_k} \\ V^D_k(i-1) + \log a_{D_k I_k} \end{cases}$$

$$V^D_k(i) = \max \begin{cases} V^M_{k-1}(i) + \log a_{M_{k-1} D_k} \\ V^I_{k-1}(i) + \log a_{I_{k-1} D_k} \\ V^D_{k-1}(i) + \log a_{D_{k-1} D_k} \end{cases}$$

with $V^M_0(0) = 0$, and the final score is the best way into $M_{m+1}$ from $(m, n)$. The match state indexes the column $k$ and the sequence position $i$ at once, so this is the general [Viterbi algorithm](/viterbi-algorithm/) laid out on a grid, like profile alignment with gap costs $-\log a$ that differ per column. The [Forward algorithm](/forward-algorithm/) replaces max by a sum of probabilities, which gives $P(x \mid \text{model})$. Both take $O(mn)$ time.

**Scores in the example.** Against a uniform background, in bits:

| $x$ | Viterbi path | $P(x, \pi^*)$ | Viterbi bits | Forward bits | share of the best path |
|---|---|---|---|---|---|
| TATAAT | $M_1 \ldots M_6$ | 2401/729000 | 3.754 | 4.077 | 0.799 |
| TATGAT | $M_1 \ldots M_6$ | 2401/729000 | 3.754 | 4.114 | |
| TAAT | $M_1 M_2 D_3 D_4 M_5 M_6$ | 2401/2916000 | $-2.246$ | $-0.554$ | 0.309 |
| TATGTAT | through $I_4$ | | 2.695 | 3.193 | |
| CCGC | | | $-9.323$ | $-5.569$ | |

For TATAAT the best path is the product of seven transitions and six emissions, $\tfrac79 \cdot \tfrac35 \cdot \tfrac79 \cdot \tfrac35 \cdot \tfrac69 \cdot \tfrac23 \cdot \tfrac34 \cdot \tfrac25 \cdot \tfrac59 \cdot \tfrac35 \cdot \tfrac79 \cdot \tfrac12 \cdot \tfrac78 = 2401/729000$. TAAT needs two deletes, and its best path holds less than a third of its probability, so here the Forward score is clearly higher than the Viterbi score. TATGTAT puts its fifth base T in $I_4$, the cheap insertion point of this family. These values were checked against a sum over all state paths.

**Non-global models.** The model above is global: $x$ must cover the model from end to end and contain nothing else. For database search, the model is placed in a frame of flanking states that emit unrelated sequence before and after the match, with entry into any match state and exit from any match state; this is the local and multi-hit configuration that [HMMER](/hmmer/) uses (Durbin et al., Chapter 5).

## Relation to other models

- **[Hidden Markov models](/hidden-markov-model/).** A profile HMM is an HMM with a fixed left-to-right topology. Its Viterbi, Forward, Backward and [Baum-Welch](/baum-welch-algorithm/) algorithms are the general ones, run on a table indexed by node and sequence position.
- **[PSSMs](/position-specific-scoring-matrix/).** A model with only match states and all transitions $M_k \to M_{k+1}$ equal to 1 is a PSSM; the insert and delete states add gaps with position-specific costs.
- **[Profile alignment](/sequence-profile-alignment/).** Viterbi in log space is a profile alignment with gap costs set by the transitions. The HMM gives the costs a probabilistic meaning and a way to estimate them, and it gives the Forward score, which a profile does not have.
- **[Pair HMMs](/pair-hmm/).** A pair HMM aligns two sequences. If one of them is fixed and the pair HMM is unrolled along it, the result is a profile HMM of that one sequence.
- **[Multiple alignment](/multiple-sequence-alignment/).** Aligning each sequence of a set to one profile HMM by Viterbi and stacking the match columns gives a multiple alignment; inserted residues are not aligned to each other. Krogh et al. (1994) produced multiple alignments of their families in this way, and HMMER's `hmmalign` does the same.

## Known results in the model

- **Complexity.** Viterbi and Forward take $O(mn)$ time for a model of length $m$ and a sequence of length $n$, and $O(m)$ space for the score alone.
- **Training from unaligned sequences.** Baum-Welch, or Viterbi training, estimates a model from sequences that are not aligned; it converges to a local optimum, so it needs a good start, noise or annealing, and a way to change the model length when match states are unused or insert states are used too much. Krogh et al. (1994) trained models of globins, protein kinase catalytic domains and EF-hand calcium binding motifs from unaligned sequences.
- **Priors.** With few sequences, the estimates depend strongly on the prior. Dirichlet mixture priors (Sjölander et al. 1996) improve the detection of remote members over single Dirichlet or simple pseudocounts.
- **Sequence weights.** Redundant sequences bias counts; relative weights (for example position-based weights) and an effective sequence number that controls how much the prior is used are part of model construction in HMMER.
- **The Plan 7 restriction.** Dropping $D \to I$ and $I \to D$ loses little in practice, because a residue between two deletions can be shifted to the insert state before or after them, and it simplifies the recurrences. HMMER's `hmmbuild` shifts residues in the input alignment for this reason.
- **Log-odds and search statistics.** For local search with the model configured as in HMMER3, Eddy (2008) gives evidence that Viterbi scores of random sequences follow a Gumbel distribution and Forward scores have an exponential tail, both with slope $\lambda$ close to $\ln 2$ for scores in bits. [HMMER](/hmmer/) uses this to compute E-values after a short calibration of each model.

## References
