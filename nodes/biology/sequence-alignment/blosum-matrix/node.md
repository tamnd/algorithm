---
tag: 1VBW1F
kind: concept
slug: blosum-matrix
name: BLOSUM matrix
aliases:
- BLOSUM62
- block substitution matrix
area: biology/sequence-alignment
level: core
summary: Protein substitution matrices of Henikoff and Henikoff (1992), log-odds scores counted from ungapped blocks of related proteins clustered at an identity level; BLOSUM62 uses 62%.
prereqs: [substitution-matrix]
see_also: [pam-matrix, scoring-matrix, single-linkage-clustering, multiple-sequence-alignment, blast, karlin-altschul-statistics]
sources:
  - paper: doi:10.1073/pnas.89.22.10915
    title: Steven Henikoff and Jorja G. Henikoff, Amino acid substitution matrices from protein blocks, Proceedings of the National Academy of Sciences USA 89(22), 1992, 10915-10919
    locator: the construction from the BLOCKS database, the clustering at a percentage identity, the half-bit log-odds scores, and the comparison with PAM
  - paper: doi:10.1038/nbt0308-274
    title: Mark P. Styczynski, Kyle L. Jensen, Isidore Rigoutsos and Gregory Stephanopoulos, BLOSUM62 miscalculations improve search performance, Nature Biotechnology 26(3), 2008, 274-275
    locator: the error in the clustering step of the original program, the corrected matrix RBLOSUM64, and its worse search performance
  - paper: doi:10.1186/s12859-016-1060-3
    title: Martin Hess, Frank Keul, Michael Goesele and Kay Hamacher, Addressing inaccuracies in BLOSUM computation improves homology search performance, BMC Bioinformatics 17, 2016
    locator: the rounding of the clustering threshold to an integer number of identities and the corrected CorBLOSUM matrices
  - url: https://ftp.ncbi.nlm.nih.gov/blast/matrices/BLOSUM62
    title: NCBI BLAST matrix file BLOSUM62
    locator: the header (1/2 bit units, cluster percentage at least 62, entropy 0.6979, expected -0.5209) and the rows A, I, L, V, F, Y, W
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.8 (BLOSUM matrices)
---

A BLOSUM matrix is a protein [substitution matrix](/substitution-matrix/) computed by Steven and Jorja Henikoff in 1992 from blocks, ungapped multiple alignments of conserved regions of protein families. Within each block, sequences that are at least $L\%$ identical are merged into one cluster, the aligned amino acid pairs between clusters are counted, and the counts become log-odds scores in half-bits. BLOSUM62 uses $L = 62$ and is the default protein matrix of [BLAST](/blast/). Unlike the [PAM matrices](/pam-matrix/), each BLOSUM matrix is counted directly from data at its own level of divergence, with no evolutionary model and no extrapolation.

## In plain words

Protein families have short stretches that hardly change, because the protein needs them. Line up such a stretch from many family members, without gaps, and you have a block. In every column of the block, any two members show a pair of amino acids that evolution allowed to stand at the same place.

The Henikoffs counted these pairs over many blocks from hundreds of families. One problem: some families contain many nearly identical sequences, which would dominate the counts. So, before counting, they grouped sequences that are very similar and let each group count as one sequence.

How similar is "very similar" is the number in the name. BLOSUM62 groups sequences that are at least 62% identical. A smaller number groups more, keeps only distant pairs, and gives a matrix for distant relatives.

## The idea

**Blocks.** The source data is a set of blocks from the BLOCKS database: each block is a gap-free [multiple sequence alignment](/multiple-sequence-alignment/) of one conserved region in the members of a protein family. Using only ungapped, conserved regions avoids the errors of gapped alignments of distant sequences.

**Clustering at level $L$.** In each block, two sequences are linked when their percent identity over the block is at least $L$. Clusters are the connected groups, which is [single-linkage clustering](/single-linkage-clustering/). A cluster then acts as one sequence: each pair of clusters $A, B$ gives weight $\frac{1}{|A|\,|B|}$ to each pair of their members, so the pair of clusters adds weight 1 per column in total. Pairs inside a cluster are not counted.

**Counting and scoring.** Summed over all columns of all blocks, let $f_{ab}$ be the weighted count of unordered pairs $\{a, b\}$ and $q_{ab} = f_{ab} / \sum f$. The frequency of residue $a$ is

$$p_a = q_{aa} + \tfrac{1}{2} \sum_{b \ne a} q_{ab}.$$

The expected frequency of an unordered pair under independence is $e_{aa} = p_a^2$ and $e_{ab} = 2 p_a p_b$ for $a \ne b$. The BLOSUM score is

$$s(a, b) = \operatorname{round}\Bigl( 2 \log_2 \frac{q_{ab}}{e_{ab}} \Bigr),$$

in half-bits. Both $q_{ab}$ and $e_{ab}$ count the two orders together, so the ratio is the same as $q_{ab} / (p_a p_b)$ for ordered pairs.

**The number in the name.** A high $L$ merges only near-identical sequences, so many fairly similar pairs are counted, and the matrix is tuned to close relatives: BLOSUM80 has a higher relative entropy. A low $L$ merges more, the remaining pairs between clusters are distant, and the matrix is tuned to distant relatives, as BLOSUM45 is. The NCBI file for BLOSUM62 gives relative entropy $0.6979$ bits and expected score $-0.5209$.

**BLOSUM versus PAM.** PAM counts substitutions in close relatives and extrapolates to large distances by a Markov model. BLOSUM measures each distance directly, from conserved regions only. In the 1992 paper, BLOSUM62 found distant family members better than PAM matrices in database searches, and it became the BLAST default.

## Examples

**A toy block.** Take four sequences of length 5 over $\{A, I, L, V\}$:

```
1  ILVLA
2  ILVLV
3  VLILA
4  LIVAA
```

The identities are: 1 and 2 share 4 of 5 positions, $80\%$; 1 and 3, $60\%$; 1 and 4, $40\%$; 2 and 3, $40\%$; 2 and 4, $20\%$; 3 and 4, $20\%$. At $L = 62$ only the pair 1, 2 is linked, so the clusters are $\{1, 2\}$, $\{3\}$, $\{4\}$. Each of the three pairs of clusters adds weight 1 per column, 15 in total over five columns. Column 5 holds A, V, A, A: the pair $\{1, 2\}$ with $\{3\}$ gives A-A with weight $\frac{1}{2}$ and V-A with weight $\frac{1}{2}$, the pair $\{1, 2\}$ with $\{4\}$ gives the same, and $\{3\}$ with $\{4\}$ gives A-A with weight 1. Over all columns the weighted counts are

| pair | A-A | A-L | A-V | I-L | I-V | L-L | L-V | V-V |
|---|---|---|---|---|---|---|---|---|
| count | 2 | 2 | 1 | 3 | 3 | 2 | 1 | 1 |

so $p_A = \frac{2 + 1.5}{15} = \frac{7}{30}$, $p_I = \frac{3}{15} = \frac{1}{5}$, $p_L = \frac{2 + 3}{15} = \frac{1}{3}$ and $p_V = \frac{7}{30}$. For I-V, $q = \frac{3}{15}$ and $e = 2 \cdot \frac{1}{5} \cdot \frac{7}{30} = \frac{7}{75}$, so $2 \log_2 \frac{15}{7} = 2.20$, rounded to $2$. The other scores are A-A $2.58 \to 3$, I-L $1.17 \to 1$, L-L $0.53 \to 1$, V-V $0.58 \to 1$, A-L $-0.45 \to 0$, A-V $-1.42 \to -1$ and L-V $-2.45 \to -2$. The pairs I-I and A-I never occur; a real matrix needs far more data than one block so that every pair is seen. Without clustering, the near-duplicates 1 and 2 would add their four identical pairs, and identities would score higher.

**The real BLOSUM62.** An excerpt of the NCBI file:

|   | I | L | V | F | Y | W |
|---|---|---|---|---|---|---|
| I | 4 | 2 | 3 | 0 | -1 | -3 |
| L | 2 | 4 | 1 | 0 | -1 | -2 |
| V | 3 | 1 | 4 | -1 | -1 | -3 |
| F | 0 | 0 | -1 | 6 | 3 | 1 |
| Y | -1 | -1 | -1 | 3 | 7 | 2 |
| W | -3 | -2 | -3 | 1 | 2 | 11 |

The row of alanine is $4$ against itself, $1$ against serine, $0$ against cysteine, glycine, threonine and valine, and between $-3$ and $-1$ against the rest.

## Where it is used

- BLOSUM62 is the default matrix of protein [BLAST](/blast/), and many other protein aligners and [multiple sequence alignment](/multiple-sequence-alignment/) programs use a BLOSUM matrix.
- BLAST offers BLOSUM45 and BLOSUM50 for distant queries and BLOSUM80 and BLOSUM90 for close ones, each with its own gap costs and statistical parameters in [Karlin-Altschul statistics](/karlin-altschul-statistics/).
- **A famous bug.** Styczynski, Jensen, Rigoutsos and Stephanopoulos (2008) found that the original program made errors in the clustering step, so the published BLOSUM62 is not what the method describes. Their corrected matrix, RBLOSUM64, performed worse than BLOSUM62 at finding distant homologs in their test. Hess, Keul, Goesele and Hamacher (2016) traced a further inaccuracy, the rounding of the clustering threshold to a whole number of identical positions, and reported that their corrected CorBLOSUM matrices often did better. The matrix in daily use is still the 1992 BLOSUM62.

## References
