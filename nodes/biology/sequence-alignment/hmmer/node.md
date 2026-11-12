---
tag: DR111J
kind: algorithm
slug: hmmer
name: HMMER
aliases:
- profile HMM search
area: biology/sequence-alignment
level: advanced
summary: "Searches a sequence database with a profile HMM: a fast ungapped MSV filter, then Viterbi, then the Forward score with an E-value from fitted Gumbel and exponential tails."
prereqs: [profile-hmm, forward-algorithm, e-value]
see_also: [blast, sequence-profile-alignment, position-specific-scoring-matrix, smith-waterman, viterbi-algorithm, karlin-altschul-statistics, pair-hmm, multiple-sequence-alignment]
sources:
  - paper: doi:10.1093/bioinformatics/14.9.755
    title: Sean R. Eddy, Profile hidden Markov models, Bioinformatics 14(9), 1998, pages 755 to 763
    locator: "review of profile HMMs; the Plan 7 architecture of HMMER2 with the special states N, B, E, C, J and seven transitions per node"
  - paper: doi:10.1371/journal.pcbi.1002195
    title: Sean R. Eddy, Accelerated profile HMM searches, PLoS Computational Biology 7(10), 2011, e1002195
    locator: "the MSV filter (optimal sum of ungapped segments, striped SIMD with 16 lanes of 8-bit scores in units of 1/3 bit), sparse rescaling of Forward and Backward, the pipeline with default P-value thresholds 0.02, 0.001 and 1e-5, the bias filter and the domain definition step"
  - paper: doi:10.1371/journal.pcbi.1000069
    title: Sean R. Eddy, A probabilistic model of local sequence alignment that simplifies statistical significance estimation, PLoS Computational Biology 4(5), 2008, e1000069
    locator: "Gumbel distribution of local Viterbi scores and exponential tail of local Forward scores, both with lambda close to log 2 for scores in bits, and the length-dependent configuration of the flanking states"
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: "Chapter 5: searching with profile HMMs and the non-global (local and multi-hit) model configurations"
---

HMMER is the profile [hidden Markov model](/profile-hmm/) package of Sean Eddy, and `hmmsearch` is its search algorithm: score every sequence of a database against one profile HMM and report the sequences whose score is unlikely for an unrelated sequence. HMMER3 scores with the [Forward algorithm](/forward-algorithm/), the sum over all local alignments, and converts the score into an [E-value](/e-value/) from distributions fitted once per model. Because Forward is slow, a pipeline of filters runs first: the MSV filter (best sum of ungapped segments), then Viterbi (best gapped alignment), and only a small fraction of the database reaches Forward. With SIMD code for the filters, HMMER3 searches proteins about as fast as [BLAST](/blast/).

## In plain words

You have a model of a protein family: for each position, which amino acids it likes, and how often the family has extra or missing residues there. You want to find all family members in a large database.

The most careful test adds up the evidence over every way the database sequence could line up with the model. That test is slow. So HMMER first asks a quick question: are there a few stretches of the sequence that fit the model well without gaps? Most unrelated sequences fail here and are dropped. The survivors get a better test that allows gaps, and the few that pass get the careful test.

Each test turns a score into a probability that an unrelated sequence would score as high. The last one becomes the expected number of false hits in a database of this size. Small values mean real family members.

## The problem

**Input.** A core profile HMM in the Plan 7 form, with $m$ nodes. Node $k$ has a match state $M_k$ with emission probabilities $e_k(a)$, an insert state $I_k$ and a delete state $D_k$, and seven transitions: $M_k \to M_{k+1}, I_k, D_{k+1}$; $I_k \to M_{k+1}, I_k$; $D_k \to M_{k+1}, D_{k+1}$. A background distribution $f(a)$. A database of $Z$ target sequences.

**The search model.** For a target $x$ of length $L$, HMMER puts the core model in a frame of special states (Plan 7):

| state | role | transitions |
|---|---|---|
| $N$ | emits unrelated residues before the first hit | $N \to N$: $L/(L+3)$; $N \to B$: $3/(L+3)$ |
| $B$ | begins a hit | $B \to M_k$ with probability $\text{occ}_k / \sum_i \text{occ}_i (m - i + 1)$ |
| $E$ | ends a hit | entered from any $M_k$ or $D_k$; $E \to C$ and $E \to J$: $1/2$ each |
| $J$ | emits residues between two hits | $J \to J$: $L/(L+3)$; $J \to B$: $3/(L+3)$ |
| $C$ | emits residues after the last hit | $C \to C$: $L/(L+3)$; $C \to T$: $3/(L+3)$ |

Here $\text{occ}_k$ is the probability that a global path through the core uses $M_k$, so the entry distribution favors well-used match states and is uniform, $2/(m(m+1))$, when every node is used. The local exit $M_k \to E$ and $D_k \to E$ is implicit, with odds 1. $N$, $C$, $J$ and the insert states emit with the background $f$, so their residues score 0 bits. The *null model* $R$ emits $L$ residues from $f$ with a self-loop $L/(L+1)$.

**Output.** For each target the bit score $S(x) = \log_2 \bigl(P(x \mid \text{search model}) / P(x \mid R)\bigr)$, where $P(x \mid \text{search model})$ is the Forward sum over all state paths, its P-value $P = \Pr_R(S \ge S(x))$, and the E-value $E = P \cdot Z$. The targets with $E$ at most a threshold (10 by default) are reported, best first.

## The algorithm

All three stages run in *odds space*: each probability is divided by the background probability of the residues it emits, so a match emission contributes $\hat e_k(a) = e_k(a) / f(a)$ and every other emission contributes 1. Write $\oplus$ for sum (Forward) or max (Viterbi), "loop" for $L/(L+3)$ and "move" for $3/(L+3)$.

```pseudo id=main
HMMSEARCH(core model, targets, calibration)
L1  Z ← number of targets
L2  λ ← ln 2 + 1.44/(m·H)            ▷ H = mean relative entropy of the match emissions
L3  (μ_MSV, μ_Vit, τ_Fwd) ← calibration of this model on random sequences
L4  for each target x, of length L:
L5      configure the search model for L (loop, move, entry_k)
L6      s ← MSV(x) in bits; if 1 − exp(−e^(−λ(s − μ_MSV))) > F1 then skip x
L7      s ← SCORE(x, max) in bits; if 1 − exp(−e^(−λ(s − μ_Vit))) > F2 then skip x
L8      s ← SCORE(x, sum) in bits; P ← e^(−λ(s − τ_Fwd)); if P > F3 then skip x
L9      E ← P·Z; report x if E ≤ the reporting threshold

SCORE(x, ⊕)                           ▷ Viterbi (⊕ = max) or Forward (⊕ = sum), odds space
L10 N ← 1;  J ← 0;  C ← 0;  B ← N·move;  M, I, D ← 0 for all k
L11 for i ← 1 to L:
L12     for k ← 1 to m:
L13         M_k(i) ← ê_k(x_i) · ⊕{ B(i−1)·entry_k, M_{k−1}(i−1)·t_MM, I_{k−1}(i−1)·t_IM, D_{k−1}(i−1)·t_DM }
L14         I_k(i) ← ⊕{ M_k(i−1)·t_MI, I_k(i−1)·t_II }                  ▷ k < m
L15         D_k(i) ← ⊕{ M_{k−1}(i)·t_MD, D_{k−1}(i)·t_DD }                ▷ k > 1
L16     E(i) ← ⊕{ M_k(i) for all k, D_k(i) for k > 1 }
L17     J(i) ← ⊕{ J(i−1)·loop, E(i)/2 };  C(i) ← ⊕{ C(i−1)·loop, E(i)/2 }
L18     N(i) ← N(i−1)·loop;  B(i) ← ⊕{ N(i), J(i) }·move
L19 return C(L)·move

MSV(x)                                ▷ like SCORE(x, max) with no I or D and M → M = 1
L20 M_k(i) ← ê_k(x_i) · max{ M_{k−1}(i−1), B(i−1)·2/(m(m+1)) }
L21 E(i) ← max_k M_k(i)
L22 J(i) ← max{ J(i−1)·loop, E(i)/2 };  C(i) ← max{ C(i−1)·loop, E(i)/2 }
L23 N(i) ← N(i−1)·loop;  B(i) ← max{ N(i), J(i) }·move;  after the loop return C(L)·move
```

The bit score of an odds value $v$ is $\log_2 v - \log_2 \bigl((L/(L+1))^L / (L+1)\bigr)$, which divides by the null model. The thresholds are $F_1 = 0.02$, $F_2 = 10^{-3}$ and $F_3 = 10^{-5}$ by default (Eddy 2011).

**Calibration (line L3).** When the model is built, HMMER scores random sequences drawn from $f$: 200 sequences of length 200 for MSV and for Viterbi, and 200 of length 100 for Forward. It fixes $\lambda$ by line L2 and fits only the location $\mu$ of a Gumbel distribution to the MSV and Viterbi scores. For Forward it fits a Gumbel to the scores and places the start $\tau$ of an exponential tail of slope $\lambda$ so that the tail matches the top 4 percent of the Gumbel: $\tau = \mu_G - \ln(-\ln(1 - 0.04))/\lambda_G + \ln(0.04)/\lambda$. The search model is configured anew for each target length $L$, and its flanking states are designed so that the score distribution does not depend much on $L$ (Eddy 2008).

**The MSV filter.** MSV (multiple segment Viterbi) keeps only the match states, sets $M_{k-1} \to M_k$ to 1 and uses a uniform entry. Its score is the best sum of one or more ungapped segments, each a diagonal of the $m \times L$ table, joined through $J$. Each cell needs one max and one multiplication (an addition in log space), and HMMER3 runs it with striped SIMD code on 8-bit scores in units of 1/3 bit, 16 cells at a time (Eddy 2011).

## Example

**A small model.** Build a Plan 7 model from the six-row DNA alignment of the [profile HMM](/profile-hmm/) page (six match columns, one pseudocount on each count), with a uniform background. The occupancies are $1, 8/9, 121/162, 3197/3888, 57371/69984, 1031453/1259712$, so the entry into $M_1$ is $1259712/23124869 \approx 0.0545$, a little above the uniform $1/21 \approx 0.0476$. Scores in bits:

| target $x$ | $L$ | MSV | Viterbi | Forward |
|---|---|---|---|---|
| TATAAT | 6 | 2.462 | 0.083 | 2.570 |
| GCGCTATAATGCGC | 14 | $-0.456$ | $-2.835$ | 1.138 |
| GCGCTAATGCGC | 12 | $-3.169$ | $-5.022$ | 0.299 |
| TATAATGCTATGAT | 14 | 0.212 | $-2.835$ | 2.621 |

The Viterbi score of TATAAT is near 0 although the target is a perfect site: the local search model pays about 4.2 bits for the entry into $M_1$ (probability 0.0545), and it pays for the flanking states; the global model of the profile HMM page has no such costs. MSV is higher than Viterbi, because it ignores the transition probabilities of the core. The fourth target has two sites; Viterbi uses one of them, while Forward adds the paths through $J$ that use both, and scores 2.621 bits.

**A search.** Draw a random DNA core model with $m = 25$ (seed 2026), calibrate it, and search 2000 random sequences of length 100 plus four sequences made by sampling a homolog of the model and adding 40 random bases on each side ($Z = 2004$). The calibration gives $H = 1.130$ bits, $\lambda = 0.7441$, $\mu_{\text{MSV}} = -6.718$, $\mu_{\text{Vit}} = -7.087$ and $\tau_{\text{Fwd}} = -2.835$. In total 56 targets pass the MSV filter (about $0.02 \times 2004 \approx 40$ are expected by chance), 5 pass Viterbi, and 2 pass Forward:

| target | MSV bits | P | Viterbi bits | P | Forward bits | P | E | result |
|---|---|---|---|---|---|---|---|---|
| h2 | 18.76 | $5.9 \times 10^{-9}$ | 16.52 | $2.3 \times 10^{-8}$ | 19.14 | $7.9 \times 10^{-8}$ | $1.6 \times 10^{-4}$ | reported |
| h1 | 10.97 | $1.9 \times 10^{-6}$ | 8.82 | $7.2 \times 10^{-6}$ | 13.74 | $4.4 \times 10^{-6}$ | $8.8 \times 10^{-3}$ | reported |
| h3 | $-1.46$ | 0.0198 | 5.56 | $8.2 \times 10^{-5}$ | 8.78 | $1.8 \times 10^{-4}$ | 0.35 | stopped by $F_3$ |
| h0 | $-2.97$ | 0.059 | $-3.71$ | 0.078 | 0.72 | 0.071 | 142 | stopped by $F_1$ |

The homolog h3 has gaps, so its ungapped MSV score is poor and it passes $F_1$ only just. Its Forward E-value of 0.35 would be reported, but its P-value is above $F_3 = 10^{-5}$, so the pipeline drops it. The sample h0 happened to be a weak homolog, with no signal above chance at any stage. All Forward, Viterbi and MSV values of this implementation agree with sums and maxima over all state paths, enumerated for small random models and targets.

## Correctness

The search model is a finite HMM in which every state of row $i$ depends only on states of row $i - 1$ and on states of row $i$ that come earlier in the order $M_k, I_k, D_k$ (increasing $k$), $E$, $J$, $C$, $N$, $B$. Lines L13 to L18 list, for each state, exactly its predecessors and the transition probabilities from them, and the silent states $D$, $E$ and $B$ take their predecessors from the same row. Because $\times$ distributes over both sum and max on nonnegative numbers, induction over this order shows that each cell holds the sum (Forward) or the maximum (Viterbi) of the odds of all partial paths that end in that state after emitting $x_1 \ldots x_i$. Line L19 then gives $P(x \mid \text{search model}) / \prod_i f(x_i)$ for Forward and the best path for Viterbi. The same argument, on the smaller MSV model, proves lines L20 to L23.

The E-value is correct given the P-value: if the $Z$ targets were drawn from the null model, each would score at least $s$ with probability $P$, and by linearity of expectation the expected number of such targets is $P \cdot Z$. The P-values themselves rest on the conjectured Gumbel and exponential-tail forms (Eddy 2008), which simulations support but no theorem proves. The filters are heuristics. Every reported target has a correct Forward score and E-value, but a target with a small E-value can be lost at a filter, as h3 shows. The full proof is below.

## Complexity

- **Per target.** Each stage fills an $m \times L$ table with $O(1)$ work per cell, so each costs $O(mL)$ time. Keeping two rows gives $O(m)$ space for the scores; the alignment needs Backward, posterior decoding and an $O(mL)$ table for each region with a hit.
- **Per database.** With $N = \sum L$ residues, MSV costs $O(mN)$ in the worst case and in practice. Viterbi runs on about $F_1 = 2$ percent of the unrelated targets and Forward on about $F_2 = 0.1$ percent, so their share of the time is small.
- **Calibration.** $O(m)$ per residue of $200 \cdot 200 + 200 \cdot 200 + 200 \cdot 100 = 100{,}000$ random residues, done once when the model is built.
- **Constant factors.** MSV needs one max and one add per cell, on 16 cells at once with 8-bit SIMD. Eddy (2011) reports that HMMER3 is 100 to 1000 times faster than HMMER2, that sparse rescaling speeds up Forward and Backward by about 20 times, and that HMMER3 is about as fast as BLAST for protein searches.

## Properties

- **The score is a log-likelihood ratio.** With the Forward score, a target is compared with the null model by its total probability over all alignments, which is the basis of the Neyman-Pearson argument for using it. Eddy (2008, 2011) argues that this makes Forward a more sensitive score than Viterbi for remote homologs, whose alignments are uncertain.
- **Known $\lambda$.** For bit scores of local alignments of a probabilistic model, $\lambda$ is close to $\ln 2$ (Eddy 2008). HMMER3 adds the small correction $1.44/(mH)$ and fits only the location, which needs far fewer random samples than fitting both parameters.
- **Length-adjusted flanks.** Because loop and move depend on $L$, the expected number of residues in $N$, $C$ and $J$ grows with $L$, and the null model also scales with $L$. The score of a fixed hit then changes little with the length of the sequence around it.
- **Multihit.** The $J$ state lets one target contain several hits (domains), and Forward adds their evidence; the domain definition step later splits them.
- **Deterministic.** The DP is exact; with the same model and target the scores are the same. The randomness is only in the calibration samples, which HMMER draws with a fixed seed by default.

## Variants and improvements

- **Programs.** `hmmsearch` searches a database with one model; `hmmscan` searches one sequence against a database of models, such as Pfam; `phmmer` and `jackhmmer` build a model from one query sequence and a substitution matrix, and `jackhmmer` iterates like PSI-BLAST, adding hits to the model each round; `nhmmer` searches DNA and uses an SSV filter (single segment Viterbi) on long targets.
- **Bias filter and null2.** Targets of biased composition, such as low-complexity or membrane regions, can pass MSV too often. HMMER3 adds a fast bias filter after MSV and the null2 correction of the score later in the pipeline (Eddy 2011). This page's model leaves both out.
- **Domain definition.** After Forward, HMMER runs Backward, finds regions with high posterior probability of being in the model, and for each region computes a Forward score, a posterior decoding and a maximum expected accuracy alignment.
- **Sparse rescaling.** Forward and Backward in HMMER3 work with probabilities scaled per row, not with logarithms, which avoids the slow log-sum operation.
- **HMMER2.** HMMER2 searched with Viterbi scores, used the Plan 7 model with a local configuration, and fitted both Gumbel parameters by simulation with `hmmcalibrate`.
- **Other profile HMM tools.** SAM is a separate package for profile HMMs; HHsearch and HHblits compare profile HMMs with each other.

## When to use it

- To find remote members of a protein family or domain when you have a multiple alignment of known members; profile HMMs find more of them than pairwise BLAST.
- To annotate the domains of new proteins against Pfam with `hmmscan`, or to build a new family by iterative search with `jackhmmer`.
- When you need a calibrated E-value that accounts for all alignments, not only the best one.
- Use BLAST or other pairwise search when there is only one query and no family, when you need the fastest search of a very large nucleotide database, or when the hits must be very close; HMMER's advantage is in remote homology.

## Pitfalls

- **Filters lose hits in small databases.** The filter thresholds are P-values per target, while the reporting threshold is an E-value. With $Z = 2004$, a target with $E = 0.35$ has $P = 1.8 \times 10^{-4}$ and fails $F_3 = 10^{-5}$, as in the example. Use the option that turns the filters off (`--max`) for small searches where this matters.
- **The database size $Z$.** E-values scale with $Z$. Searching a subset, or setting $Z$ by hand, changes every E-value; compare E-values only between searches with the same $Z$.
- **Gapped homologs and MSV.** MSV has no gaps. A homolog with many short ungapped pieces passes because MSV sums segments, but a homolog whose segments are each too short can fail $F_1$.
- **Model quality.** The model is only as good as its seed alignment: a wrong match column choice, too few sequences, or redundant sequences without weights give a model that misses or overcalls. HMMER's default entropy weighting lowers the effective number of sequences so that the model is not too sharp.
- **Composition bias.** Without the bias filter and null2, low-complexity targets get high scores. Implementations that leave them out, like the one on this page, will report false hits in real protein databases.
- **Numeric range.** In probability space, long targets underflow; use logarithms or row scaling. The exact Fraction arithmetic used for tests is only practical for tiny inputs.

## Implementations

## History

Krogh, Brown, Mian, Sjölander and Haussler (1994) introduced profile HMMs for protein families. Eddy released HMMER 1.8 in April 1995. HMMER2, a rewrite begun in November 1996, introduced the Plan 7 architecture with its special states for local and multihit alignment (Eddy 1998), and it was the search engine of the Pfam database. Eddy (2008) proposed the probabilistic model of local alignment with $\lambda \approx \ln 2$, which removed the need to fit $\lambda$ for each model. HMMER3 (Eddy 2011) changed the score to Forward, added the MSV filter with striped SIMD code and sparse rescaling, and made profile HMM search about as fast as BLAST. Version 3.4 appeared in August 2023.

## References
