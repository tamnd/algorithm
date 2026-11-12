---
tag: 6V3ZPD
kind: problem
slug: sequence-profile-alignment
name: Profile alignment
aliases:
- profile-to-sequence alignment
- profile-profile alignment
area: biology/sequence-alignment
level: advanced
summary: "Align a sequence to a profile (a column-wise scoring table with position-specific gap costs), or two profiles to each other, by dynamic programming over columns."
prereqs: [position-specific-scoring-matrix, pairwise-sequence-alignment, affine-gap-penalty]
see_also: [smith-waterman, gotoh-algorithm, profile-hmm, hmmer, progressive-alignment, sum-of-pairs-score, protein-threading, strong-exponential-time-hypothesis]
sources:
  - paper: doi:10.1073/pnas.84.13.4355
    title: Michael Gribskov, Andrew D. McLachlan and David Eisenberg, Profile analysis, detection of distantly related proteins, Proceedings of the National Academy of Sciences USA 84(13), 1987, pages 4355 to 4358
    locator: "the profile as a position-specific scoring table with a gap penalty column; the gap penalty PEN = PEN'(p)[OPEN + EXN x L] with OPEN 5 and EXN 0.1; local alignment of a target to the profile; the globin and immunoglobulin tests against a 3800-sequence database"
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: "Chapter 5, Section 5.3 (profiles with position-specific gap costs as a special case of profile HMMs)"
  - paper: doi:10.1145/974614.974626
    title: John D. Kececioglu and Dean Starrett, Aligning alignments exactly, Proceedings of RECOMB 2004, pages 85 to 96
    locator: NP-completeness of aligning two alignments under the sum-of-pairs score with affine gap costs counted exactly
  - paper: doi:10.1093/bioinformatics/bth091
    title: Robert C. Edgar and Kimmen Sjölander, COACH, profile-profile alignment of protein families using hidden Markov models, Bioinformatics 20(8), 2004, pages 1309 to 1318
    locator: profile-profile alignment by aligning a sequence family to a profile HMM
  - paper: doi:10.1093/bioinformatics/bti125
    title: Johannes Söding, Protein homology detection by HMM-HMM comparison, Bioinformatics 21(7), 2005, pages 951 to 960
    locator: "HHsearch: the column score log sum_a q_i(a) p_j(a) / f(a) and HMM-HMM Viterbi alignment"
  - paper: doi:10.1145/2746539.2746612
    title: Arturs Backurs and Piotr Indyk, Edit distance cannot be computed in strongly subquadratic time (unless SETH is false), Proceedings of STOC 2015, pages 51 to 58
    locator: the conditional quadratic lower bound for edit distance, which profile alignment contains as a special case
---

Profile alignment aligns a sequence to a *profile*, a table that gives a score for each residue at each column of a family alignment and a gap cost for each column, or it aligns two profiles to each other. Gribskov, McLachlan and Eisenberg (1987) introduced the profile to find distant members of protein families, which a single family member as query does not find. The algorithm is the dynamic program of [pairwise alignment](/pairwise-sequence-alignment/) with the substitution score $s(a, b)$ replaced by a column score and the fixed gap costs replaced by gap costs that depend on the column. It runs in $O(mn)$ time for a profile of $m$ columns and a sequence of length $n$.

## In plain words

When you compare one new protein with one known protein, a weak match can be a family member or noise. If you know twenty members of the family, you know more: at some positions the family never changes, at others almost anything goes, and some places often have extra residues.

A profile writes this down. For each position of the family it gives points for each possible residue, and it gives a cost for a gap at that position. Gaps are cheap where the family often has gaps and expensive where it never has them.

To compare a new protein with the family, you line the protein up against the profile, the same way you line up two proteins, but you take the points from the profile. You can also line up two families by comparing their profiles column by column.

## Definition

**Profiles.** A profile of length $m$ over an alphabet $\Sigma$ is

- a score $W_j(a)$ for each column $j = 1, \ldots, m$ and residue $a \in \Sigma$, as in a [position-specific scoring matrix](/position-specific-scoring-matrix/);
- a deletion cost $d_j \ge 0$ for skipping column $j$;
- an insertion cost $h_j \ge 0$ for each residue placed between columns $j$ and $j + 1$ ($j = 0, \ldots, m$).

The affine form has an open cost and an extension cost for each column instead of one cost $d_j$ or $h_j$.

**Profile-to-sequence alignment.** Input: a profile $W$ of length $m$ and a sequence $x = x_1 \ldots x_n$. An alignment pairs some columns with some residues, in order, without crossing; each column not paired is deleted and each residue not paired is inserted. Its score is

$$\sum_{(j, i) \text{ paired}} W_j(x_i) \;-\; \sum_{j \text{ deleted}} d_j \;-\; \sum_{\text{residue inserted after column } j} h_j .$$

The global problem asks for an alignment of maximum score that uses all of $x$ and all columns. The local problem asks for the maximum over all pairs of a contiguous block of columns and a substring of $x$, as in [Smith-Waterman](/smith-waterman/).

**Profile-to-profile alignment.** Input: two profiles $A$ (length $m$) and $B$ (length $n$), and a column score $S(A_j, B_k)$. The alignment and its score are as above, with $W_j(x_i)$ replaced by $S(A_j, B_k)$ and with gap costs from either profile. The problem depends on the choice of $S$; common choices are below.

## Variants

- **Profiles from counts and a substitution matrix.** Gribskov et al. built the column scores from the residues seen in the column and the Dayhoff matrix, so that a residue never seen in the column but similar to the residues seen still scores well. The gap penalty column $\text{PEN}'(p)$ was low where the family alignment had gaps and high in regions of regular secondary structure. A gap of length $L$ at position $p$ cost $\text{PEN}'(p)\,[\text{OPEN} + \text{EXN} \times L]$; their examples used $\text{OPEN} = 5$ and $\text{EXN} = 0.1$.
- **Log-odds profiles.** With $W_j(a) = \log (p_j(a)/q_a)$ the profile is a PSSM, and with gap costs it is the max-score (Viterbi) form of a [profile HMM](/profile-hmm/). The profile HMM gives the gap costs a meaning as log transition probabilities and learns them from the counts of gaps in each column.
- **Profile-profile column scores.** For column frequency vectors $f = A_j$ and $g = B_k$ (with pseudocounts):
  - the *average score* $\sum_{a, b} f(a)\, g(b)\, s(a, b)$ for a substitution matrix $s$; this is the sum-of-pairs score of the two columns divided by the number of pairs;
  - the *log-odds of co-emission* $\log \sum_a f(a)\, g(a) / q_a$, the log of the ratio of the probability that the two columns emit the same residue to the probability under the background; HHsearch (Söding 2005) uses this score;
  - correlation and distance measures between $f$ and $g$, used by other profile-profile tools.
- **Aligning alignments.** In [progressive alignment](/progressive-alignment/) two alignments are merged by aligning their profiles. With a [sum-of-pairs score](/sum-of-pairs-score/) and linear gap costs, the profile-profile score of a column pair and of a gap column is exact. With affine gap costs counted exactly, a gap in the merged alignment can open or extend in each row depending on the gaps already in that row, and the column profile no longer has enough information.
- **Probabilistic alignment.** A profile HMM can be aligned to a sequence by the Forward algorithm (sum over alignments) instead of Viterbi, and two profile HMMs can be aligned by a pair HMM over their states, as in COACH (Edgar and Sjölander 2004) and HHsearch.

## Examples

Use the six-column Laplace PSSM of the [position-specific scoring matrix](/position-specific-scoring-matrix/) page, in bits:

| column | A | C | G | T |
|---|---|---|---|---|
| 1 | $-1.322$ | $-0.322$ | $-1.322$ | $1.263$ |
| 2 | $1.263$ | $-1.322$ | $-0.322$ | $-1.322$ |
| 3 | $-1.170$ | $-1.170$ | $-1.170$ | $1.415$ |
| 4 | $0.678$ | $-1.322$ | $0.678$ | $-1.322$ |
| 5 | $1.263$ | $-1.322$ | $-0.322$ | $-1.322$ |
| 6 | $-0.322$ | $-0.322$ | $-1.322$ | $1.000$ |

Take global alignment with linear gap costs, $d_j = 2$ bits for each deleted column and $h_j = 2$ bits for each inserted residue.

- TATAAT aligns with no gaps and scores 6.882.
- CATGAT aligns with no gaps and scores 5.297; the C costs 1.585 bits against T at column 1.
- TAAT aligns as `MMDDMM`: T and A to columns 1 and 2, columns 3 and 4 deleted, A and T to columns 5 and 6. The score is $1.263 + 1.263 - 2 - 2 + 1.263 + 1.000 = 0.789$ bits.
- TATGTAT aligns as `MMMMIMM`, with the extra T inserted after column 4. With $h_4 = 2$ the score is 4.882. The family alignment that gave the profile has its insertions between columns 4 and 5, so a profile builder lowers $h_4$; with $h_4 = 0.5$ the score is 6.382, and the gapped sequence scores almost as well as a perfect site. A fixed gap cost cannot do this, because it would also make gaps cheap in the conserved columns 1 to 3.

**Profile to profile.** Build a second profile $B$ from the three rows CTATAA, TTATGA and CTATGA, with Laplace pseudocounts, and score column pairs by the log-odds of co-emission, $\log_2 \sum_a 4 f(a) g(a)$. Local alignment with a linear gap cost of 1 bit gives a best score of 3.142 bits: columns 1 to 5 of the PSSM against columns 2 to 6 of $B$, with no gaps. The column scores are $0.678 + 0.678 + 0.778 + 0.330 + 0.678$. The DP finds the shift of one position between the two families, which the first column of $B$ (C or T) causes.

## Known algorithms

- **Dynamic programming, linear gaps.** For profile-to-sequence alignment fill $V[j][i]$, the best score of an alignment of columns $1..j$ with $x_1 \ldots x_i$:
  $$V[j][i] = \max\{V[j-1][i-1] + W_j(x_i),\; V[j-1][i] - d_j,\; V[j][i-1] - h_j\}.$$
  The local version adds 0 to the maximum and takes the maximum entry. This is $O(mn)$ time, and the space drops to $O(m + n)$ with [Hirschberg's method](/hirschberg-algorithm/).
- **Affine gaps.** Three tables, as in [Gotoh's algorithm](/gotoh-algorithm/), with the open and extension costs read from column $j$. Still $O(mn)$. With HMM transition scores this is the Viterbi recurrence of the profile HMM, with match, insert and delete states for each column.
- **Profile-profile.** The same DP over $m \times n$ column pairs. Computing $S(A_j, B_k)$ costs $O(|\Sigma|)$ for the co-emission score, and $O(|\Sigma|)$ for the average score after the vector $f^{\top} s$ is computed once per column of $A$, so the total is $O(mn|\Sigma|)$.
- **Sum over alignments.** The Forward algorithm of the profile HMM replaces max by sum in the same recurrences and gives a score that uses all alignments; [HMMER](/hmmer/) uses it for its final scores.
- **Exact alignment of alignments under affine gaps.** Kececioglu and Starrett (2004) give an exact algorithm by search with bounds, practical for many inputs but exponential in the worst case.

## Bounds

- **Upper bound.** $O(mn)$ time for profile-to-sequence alignment with linear or affine column gap costs, after $O(m|\Sigma|)$ time to read the profile; $O(mn|\Sigma|)$ for profile-to-profile with the scores above.
- **Conditional lower bound.** A profile of one sequence $y$ with $W_j(a) = s(y_j, a)$ and constant gap costs is ordinary pairwise alignment. So any algorithm for profile alignment also aligns two sequences. Backurs and Indyk (2015) show that edit distance has no $O(n^{2-\varepsilon})$ algorithm for any $\varepsilon > 0$ unless the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) fails, and the same bound holds for profile alignment.
- **Hardness of aligning alignments.** When each input is itself an alignment and the target is the exact sum-of-pairs score with affine gaps, the problem is NP-complete (Kececioglu and Starrett 2004; Ma, Wang and Zhang showed the same result independently). The profile-profile DP solves a simpler problem, in which the gap costs of the merged rows are estimated, not counted.

## Reductions

- **From pairwise alignment.** As above, pairwise alignment with a substitution matrix is profile alignment with a one-sequence profile. Profile alignment is no easier.
- **To pairwise alignment DP.** Profile-to-sequence alignment is an instance of DP alignment with a cost function that depends on the position in the first input. Any alignment DP that allows position-dependent costs (Gotoh, Hirschberg, banded alignment, local alignment) applies without change.
- **To profile HMM decoding.** With log-probability scores the profile is a profile HMM, and the optimal alignment is a Viterbi path of that HMM. Any profile with finite gap costs can be read as an HMM after the scores are scaled, although the result need not be a normalized probability model.

## Applications

- **Distant homology search.** Gribskov et al. built a profile from five globins (124 columns) and searched a database of 3800 sequences. All globins scored from 469.5 to 928.7 and all other proteins from 32.4 to 455.8, so a threshold separated them; a 49-column profile from four immunoglobulin variable regions also separated its family. Today this role is filled by PSI-BLAST, [HMMER](/hmmer/) and HMM-HMM search.
- **Progressive and iterative multiple alignment.** Tools such as [Clustal](/clustal/) and [MUSCLE](/muscle/) build a multiple alignment by aligning the profiles of two sub-alignments at each node of a guide tree.
- **Fold recognition.** Profile-profile comparison detects pairs of protein families with the same fold even when no two members are clearly similar, and it is used to choose templates for [protein threading](/protein-threading/) and structure modeling.
- **Adding sequences to an alignment.** A new sequence is aligned to the profile of an existing alignment and inserted without realigning the rest.

## References
