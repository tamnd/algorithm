---
tag: 4TVG52
kind: algorithm
slug: mafft
name: MAFFT
aliases:
- Multiple Alignment using Fast Fourier Transform
- FFT-NS-2
area: biology/sequence-alignment
level: advanced
summary: A progressive multiple aligner that finds homologous segments with FFT correlation of residue properties and aligns only the regions between them by dynamic programming.
model: word-ram
complexity:
  vars: {k: the number of sequences, n: the length of the longest sequence, L: the length of the alignment}
  time: {worst: "O(k^2 n + k^3 + k^2 L^2)"}
  space: {extra: "O(k^2 + k L + L^2)"}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 2002
  people: [Kazutaka Katoh, Kazuharu Misawa, Kei-ichi Kuma, Takashi Miyata]
  note: The 2002 paper introduced FFT-based segment detection and the FFT-NS strategies; version 5 (2005) added the consistency-based iterative modes L-INS-i, G-INS-i and E-INS-i.
prereqs: [progressive-alignment, fast-fourier-transform, cross-correlation, upgma]
see_also: [multiple-sequence-alignment, iterative-refinement-alignment, sum-of-pairs-score, clustal, muscle, t-coffee, colinear-chaining, convolution-via-fft]
sources:
  - paper: doi:10.1093/nar/gkf436
    title: Kazutaka Katoh, Kazuharu Misawa, Kei-ichi Kuma and Takashi Miyata, MAFFT, a novel method for rapid multiple sequence alignment based on fast Fourier transform, Nucleic Acids Research 30(14), 2002, pages 3059 to 3066
    locator: the residue vectors and the correlation c(k), the 20 highest peaks with a 30-site window and threshold 0.7 per site, the dynamic program on segments, the 6-tuple distance, and FFT-NS-1, FFT-NS-2 and FFT-NS-i
  - paper: doi:10.1093/nar/gki198
    title: Kazutaka Katoh, Kei-ichi Kuma, Hiroyuki Toh and Takashi Miyata, MAFFT version 5, improvement in accuracy of multiple sequence alignment, Nucleic Acids Research 33(2), 2005, pages 511 to 518
    locator: the iterative refinement options with a consistency term, L-INS-i, G-INS-i and E-INS-i
  - paper: doi:10.1093/molbev/mst010
    title: Kazutaka Katoh and Daron M. Standley, MAFFT multiple sequence alignment software version 7, improvements in performance and usability, Molecular Biology and Evolution 30(4), 2013, pages 772 to 780
    locator: the version 7 features, such as adding sequences to an existing alignment
---

MAFFT is a program for [multiple sequence alignment](/multiple-sequence-alignment/) by Kazutaka Katoh, Kazuharu Misawa, Kei-ichi Kuma and Takashi Miyata, published in 2002. It is a [progressive aligner](/progressive-alignment/) with one new idea: before it aligns two groups by dynamic programming, it finds the homologous segments of the groups with the [fast Fourier transform](/fast-fourier-transform/). It turns each column into a numeric vector, computes the [cross-correlation](/cross-correlation/) of the two groups at every shift in $O(N \log N)$ time, looks for conserved segments only on the shifts with the highest correlation, and then runs dynamic programming only on the small regions between the segments. Its basic strategy, FFT-NS-2, aligns twice along two guide trees. Later versions add iterative refinement with a consistency term.

## In plain words

Slide one sequence along the other. At each shift, count how many letters agree. A shift where many letters agree is probably a shift where a long piece of the two sequences is related. The Fourier transform gives all these counts at once, very quickly.

MAFFT takes the best few shifts and looks along each for stretches where most letters agree. It picks a set of stretches that keep their order in both sequences, and fixes their middle letters as matched. Only the short pieces between fixed letters are aligned with the slow method.

Groups of aligned sequences are joined in the order of a guide tree. Then the guide tree is rebuilt from the result, and everything is aligned again.

## The problem

The input is $k$ sequences over an alphabet $\Sigma$, of lengths at most $n$, and a pair score $s$ on $\Sigma \cup \{-\}$ with $s(-, -) = 0$. The output is a multiple alignment: rows of equal length, row $i$ spelling sequence $i$ with gaps added, and no column of gaps only. Like all progressive methods MAFFT does not promise the best value of an objective. Each merge here maximizes the average pair score between the two groups, the cross-group part of the [sum-of-pairs score](/sum-of-pairs-score/), among the merges that match the chosen anchor columns.

This page describes FFT-NS-2 for DNA, with a linear gap penalty and unweighted profiles.

## The algorithm

```pseudo id=main
MAFFT-FFT-NS-2(S[1..k])
L1  for each pair i, j do D[i][j] ← 1 − T_ij / min(T_ii, T_jj), with T_ij the number of k-tuples shared by S_i and S_j
L2  G ← UPGMA(D)
L3  A ← PROGRESSIVE(G, S), with GROUP-ALIGN at each internal node
L4  G ← UPGMA(distances between the rows of A)
L5  A ← PROGRESSIVE(G, S), with GROUP-ALIGN at each internal node
L6  return A, with its rows in input order

GROUP-ALIGN(X, Y)
L7  u, v ← the column vectors of X and Y; c(ℓ) ← Σ_p u(p) · v(p + ℓ) for every lag ℓ, by FFT
L8  segs ← for each of the lags ℓ with the highest c(ℓ), the runs of sites on diagonal ℓ covered by windows whose mean score is above the threshold
L9  chain ← the collinear set of segments with the largest total score, by dynamic programming on segments
L10 anchors ← the center column pair of each segment in chain
L11 for each region between consecutive anchors do align the region by the profile dynamic program
L12 return the aligned regions and the matched anchor columns, joined in order
```

**Residue vectors (line L7).** For DNA a column becomes a vector of four numbers, the frequencies of A, C, G and T in the column; gaps add nothing. For proteins the paper uses two numbers per amino acid, its volume and its polarity, each normalized, and a column of a group becomes the weighted sum of the vectors of its residues, with sequence weights. The product $u(p) \cdot v(p + \ell)$ is large when the two columns are alike. The sum over $p$ is a cross-correlation, and with the FFT all $m + n - 1$ lags cost $O((m + n) \log (m + n))$ time per vector component, instead of $O(mn)$.

**Segments (lines L8 to L10).** The paper takes the 20 highest peaks of $c$, moves a window of 30 sites along each diagonal, and keeps the sites of the windows whose score is above 0.7 per site; neighboring segments are merged, and segments longer than 150 sites are split. A dynamic program on a matrix of segment scores then picks the best arrangement of segments that keeps their order in both groups. The DP matrix is cut into submatrices at the centers of the chosen segments, so dynamic programming runs only inside the submatrices.

**Distances (lines L1 and L4).** Line L1 counts shared 6-tuples, in the formula of the pseudocode; for proteins the 20 amino acids are first grouped into 6 classes. The guide tree comes from UPGMA. FFT-NS-1 stops after line L3. FFT-NS-2 builds a second tree from the first alignment and aligns again. The implementation measures the distance in line L4 by the fraction of mismatches among aligned letter pairs.

**Gap penalties.** The paper's group-to-group score uses sequence weights and a gap opening penalty that is reduced where gaps already exist, with a term that acts as a gap extension penalty. The implementation uses a linear gap penalty and equal weights.

## Example

Use $+1$ for a match, $-1$ for a mismatch and $-2$ for a letter against a gap, and these sequences:

$$S_1 = \texttt{AACCGGTTAC},\quad S_2 = \texttt{CCGGTTACAA},\quad S_3 = \texttt{ACCGGTAC}.$$

The implementation uses a window of 4 sites, threshold 0.7 per site, the 4 highest peaks and tuples of length 2. Every 2-tuple of $S_3$ occurs in $S_1$, so $D[1][3] = 0$; also $D[1][2] = 1/9$ and $D[2][3] = 1/7$. UPGMA joins $S_1$ with $S_3$ first.

**Merge $S_1$ with $S_3$.** The correlation is highest at lag $-1$, with value 6 (position $p$ of $S_1$ against position $p - 1$ of $S_3$), and next at lag $-2$, with value 5. On lag $-1$ the windows mark one segment: positions 2 to 8 of $S_1$ (`ACCGGTT`) against positions 1 to 7 of $S_3$ (`ACCGGTA`), with 6 agreeing sites. On lag $-2$ there is a segment of 5 sites with score 4 that overlaps it, so the chain keeps only the first. Its center fixes position 5 of $S_1$ against position 4 of $S_3$, both `G`. The two regions on each side are aligned by dynamic programming:

```
S1  AACCGGTTAC
S3  -ACCGG-TAC
```

**Add $S_2$.** Now the columns of the pair are vectors with entries $1/2$ or $1$. The highest peak, 7.5, is at lag $-2$, and one segment covers columns 3 to 10 of the pair against positions 1 to 8 of $S_2$. Its center fixes column 7 against position 5 of $S_2$, and the result is

```
S1  AACCGGTTAC--
S2  --CCGGTTACAA
S3  -ACCGG-TAC--
```

with sum-of-pairs score 3. Every aligned letter pair is identical, so all distances in line L4 are 0, UPGMA breaks the ties and joins $S_1$ with $S_2$ first, and the second pass gives the same alignment. Its score 3 is the optimum, found by exact dynamic programming over the three-dimensional lattice. The anchor of the second merge says at once that $S_2$ starts two places to the right of $S_1$; a plain dynamic program has to discover this by filling the whole table.

## Correctness

The output is a valid multiple alignment, and each merge is optimal among the merges that match its anchors.

The anchors are strictly increasing in both coordinates: the chain uses segments that do not overlap in either group, and the center of a segment lies inside it. A block alignment of $X$ and $Y$ matches column $i_t$ of $X$ with column $j_t$ of $Y$ for every anchor if and only if it is a block alignment of the region before the first anchor, then the anchor column, then a block alignment of the next region, and so on. The score is a sum over columns, so the best such alignment is made of the best alignment of each region, and the profile dynamic program finds those by the [Needleman-Wunsch](/needleman-wunsch/) argument with columns as letters. Validity follows by induction over the guide tree, as for every progressive method: rows keep their letters in order, gaps are added as whole columns, and every column holds a column of one of the two groups. With no anchors, a merge of two single sequences is an optimal pairwise alignment. The proof file has the details.

The anchors can be wrong, and then the merge is worse than the unrestricted optimum. That is the price of the speed.

## Complexity

The model is the word RAM, with one unit per arithmetic operation. $L$ is the length of the final alignment, $n \le L \le kn$.

- **Line L1.** Counting tuples costs $O(n)$ per pair with a hash table, $O(k^2 n)$ in total.
- **Lines L2 and L4.** UPGMA on $k$ leaves takes $O(k^3)$ time with the simple method. Line L4 also measures $\binom{k}{2}$ distances in $O(k^2 L)$ time.
- **Line L7.** Per merge, $O(|\Sigma|\, L \log L)$ time for the FFTs.
- **Lines L8 and L9.** Per merge, $O(|\Sigma|\, L)$ time per peak, and the chain is quadratic in the number of segments.
- **Line L11.** With no anchors, the profile program of a merge of $a$ rows with $b$ rows fills $O(L^2)$ cells, each costing $O(ab)$ here. The sum of $ab$ over all merges is $\binom{k}{2}$, so this is $O(k^2 L^2)$ in the worst case.

The worst case is $O(k^2 n + k^3 + k^2 L^2)$ time, the same as a plain progressive aligner, because related segments may not exist. The gain comes when they do: if the anchors are at most $w$ columns apart, the regions cover $O(Lw)$ cells instead of $O(L^2)$. The paper states that the FFT reduces the time from $O(N^2)$ to $O(N)$ for highly conserved sequences, and that for distantly related sequences the time is close to that of plain dynamic programming. The space is $O(k^2)$ for distances, $O(kL)$ for the alignment and $O(L^2)$ for one table.

## Properties

- **Deterministic.** Ties among peaks, segments, UPGMA joins and traceback steps are broken by fixed rules.
- **Restricted merges.** Each merge is optimal only among merges through its anchors.
- **Not exact.** It is a heuristic for an [NP-hard](/msa-np-hardness/) problem, and the anchors add a second source of error to the frozen gaps of progressive alignment.
- **Two passes.** FFT-NS-2 uses the first alignment only to build a better guide tree; the second pass starts again from the sequences.

## Variants and improvements

- **FFT-NS-1** stops after the first progressive pass.
- **FFT-NS-i** adds [iterative refinement](/iterative-refinement-alignment/): the alignment is split into two groups at an edge of the guide tree and the groups are realigned, until no better score is found.
- **NW-NS-1 and NW-NS-2** use plain dynamic programming without the FFT step.
- **L-INS-i, G-INS-i and E-INS-i** (version 5, 2005) use iterative refinement with an objective that adds a consistency score from all pairwise alignments, local or global, to the weighted sum-of-pairs score. They are slow and among the most accurate modes.
- **Version 7** (2013) adds options such as adding new sequences to an existing alignment.

## When to use it

Use the FFT-NS-2 mode for many sequences, when speed matters; it is fastest on sequences with long conserved stretches. Use an iterative mode such as L-INS-i for a few hundred hard, divergent sequences when accuracy matters more than time. Compare with [MUSCLE](/muscle/), [Clustal](/clustal/) and [T-Coffee](/t-coffee/) on reference sets for the data at hand.

## Pitfalls

- **Expecting a speedup on divergent data.** With no strong peaks there are no anchors, and the cost is that of plain dynamic programming.
- **Wrong anchors.** Repeats give several peaks of similar height, and a chain through the wrong copy forces a bad match. A higher threshold gives fewer, safer anchors.
- **Reading the guide tree as a phylogeny.** Tuple distances are crude, and UPGMA assumes a molecular clock.
- **Mixing up the modes.** FFT-NS-2, FFT-NS-i and L-INS-i are different algorithms with different costs and accuracy; report the one used.

## Implementations

## History

Kazutaka Katoh, Kazuharu Misawa, Kei-ichi Kuma and Takashi Miyata published MAFFT in Nucleic Acids Research in 2002, with the FFT method for finding homologous segments and the strategies FFT-NS-1, FFT-NS-2 and FFT-NS-i. Version 5, by Katoh, Kuma, Hiroyuki Toh and Miyata in 2005, added the iterative modes with a consistency score. Katoh and Daron Standley described version 7 in 2013.

## References
