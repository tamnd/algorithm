---
tag: VY1X3J
kind: algorithm
slug: muscle
name: MUSCLE
aliases:
- MUltiple Sequence Comparison by Log-Expectation
area: biology/sequence-alignment
level: advanced
summary: A three-stage multiple aligner. A fast k-mer tree and progressive draft, a second tree from the draft, then refinement that keeps a change only if the SP score improves.
model: word-ram
complexity:
  vars: {k: the number of sequences, L: the length of the sequences and of the alignment}
  time: {worst: "O(k^2 L + k L^2 + k^3 L)"}
  space: {extra: "O(k^2 + k L + L^2)"}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 2004
  people: [Robert C. Edgar]
  note: Edgar published MUSCLE in Nucleic Acids Research and BMC Bioinformatics in 2004.
prereqs: [progressive-alignment, iterative-refinement-alignment, upgma, sum-of-pairs-score]
see_also: [clustal, mafft, t-coffee, probcons, kmer-index, kimura-two-parameter-model, sequence-profile-alignment, multiple-sequence-alignment]
sources:
  - paper: doi:10.1093/nar/gkh340
    title: Robert C. Edgar, MUSCLE, multiple sequence alignment with high accuracy and high throughput, Nucleic Acids Research 32(5), 2004, pages 1792 to 1797
    locator: the three stages, the k-mer and Kimura distances, the log-expectation profile function, tree-dependent restricted partitioning, and the complexity analysis
  - paper: doi:10.1186/1471-2105-5-113
    title: Robert C. Edgar, MUSCLE, a multiple sequence alignment method with reduced time and space complexity, BMC Bioinformatics 5, 2004, article 113
    locator: the algorithm in more detail and the analysis of time and space
  - paper: doi:10.1006/jmbi.1996.0679
    title: Osamu Gotoh, Significant improvement in accuracy of multiple protein sequence alignments by iterative refinement as assessed by reference to structural alignments, Journal of Molecular Biology 264(4), 1996, pages 823 to 838
    locator: iterative refinement of a progressive alignment, the idea that MUSCLE's stage 3 follows
---

MUSCLE is a [multiple sequence alignment](/multiple-sequence-alignment/) program by Robert Edgar, published in 2004. It works in three stages. Stage 1 builds a draft quickly: a distance from shared k-mers, a [UPGMA](/upgma/) guide tree, and [progressive alignment](/progressive-alignment/) with a profile score called log-expectation (LE). Stage 2 measures new distances on the draft alignment, builds a second tree, and realigns the parts of the tree that changed. Stage 3 is [iterative refinement](/iterative-refinement-alignment/): it cuts the second tree at one edge at a time, realigns the two groups, and keeps the new alignment only if its [sum-of-pairs score](/sum-of-pairs-score/) is higher. The design gives accuracy close to slower consistency methods at the speed of a progressive aligner.

## In plain words

MUSCLE makes a rough alignment fast, then improves it.

First it compares the sequences by counting short words they share, which needs no alignment. It joins the most similar sequences into a tree and aligns along that tree.

The rough alignment gives better distances than word counts, so MUSCLE builds a second tree from it. Where the second tree groups sequences in a new way, it aligns those parts again.

Then it tries to fix mistakes. It splits the sequences into two groups at one branch of the tree, pulls the groups apart, and aligns them again. If the result scores better, it keeps it. It does this for every branch, again and again, until nothing improves.

## The problem

The input is $k$ protein or DNA sequences of length about $L$. The output is a multiple alignment: rows of equal length, row $i$ spelling the $i$-th sequence with gaps added, and no column of gaps only. MUSCLE is a heuristic. Its objective in stage 3 is the sum-of-pairs score, and it never returns an alignment worse than the one at the start of stage 3, but it does not promise the optimum, which is [NP-hard](/msa-np-hardness/) to find.

## The algorithm

```pseudo id=main
MUSCLE(S[1..k], maxPasses)
L1  D1[i][j] ← k-mer distance of S_i and S_j, for all pairs
L2  TREE1 ← UPGMA(D1)
L3  MSA1 ← progressive alignment along TREE1, profiles aligned with the LE score
L4  D2[i][j] ← Kimura distance of rows i and j of MSA1, for all pairs
L5  TREE2 ← UPGMA(D2)
L6  MSA ← progressive alignment along TREE2, reusing the alignment of every subtree that is also in TREE1
L7  for pass ← 1 to maxPasses do
L8      improved ← false
L9      for each edge e of TREE2, in order of decreasing distance from the root do
L10         split MSA at e into groups X and Y; remove the columns of gaps only from each
L11         A′ ← PROFILE-ALIGN(X, Y) with the LE score
L12         if SP(A′) > SP(MSA) then MSA ← A′, improved ← true
L13     if not improved then break
L14 return MSA
```

**k-mer distance (line L1).** For sequences $x$ and $y$, let $F$ be the number of k-mers they share, counted with multiplicity, divided by the number of k-mers in the shorter sequence. The distance is $1 - F$. MUSCLE counts k-mers of proteins in a compressed alphabet, where groups of similar amino acids are one letter. No alignment is needed, so all pairs take $O(k^2 L)$ time.

**Log-expectation score (lines L3, L6, L11).** For a column $x$ of one profile and a column $y$ of the other, let $f_{xi}$ be the fraction of rows of $x$ with letter $i$, $f_{xG}$ the fraction with a gap, $p_i$ the background frequency of letter $i$, and $p_{ij}$ the joint frequency of $i$ and $j$ in related sequences. Then

$$\mathrm{LE}_{xy} = (1 - f_{xG})(1 - f_{yG}) \log \sum_i \sum_j f_{xi}\, f_{yj}\, \frac{p_{ij}}{p_i\, p_j}.$$

The sum inside the logarithm is the expected odds ratio of a letter of $x$ against a letter of $y$, and the factor in front lowers the weight of columns with many gaps. MUSCLE uses the frequencies of the 240 PAM VTML matrix and position-specific affine gap penalties. The profile alignment is the global alignment recurrence on columns, with gap columns inserted into whole groups.

**Kimura distance (line L4).** For two rows of the draft, let $D$ be the fraction of differing letters among the columns where both have a letter. The distance is $-\ln(1 - D - D^2/5)$, Kimura's correction for multiple substitutions in proteins. It is more accurate than the k-mer distance because it uses an alignment.

**Reuse in stage 2 (line L6).** A subtree of TREE2 with the same leaves and the same branching order as a subtree of TREE1 already has an alignment from line L3. Only the nodes whose subtrees changed are aligned again.

**Tree-dependent restricted partitioning (lines L7 to L13).** Deleting an edge of TREE2 splits the sequences into two groups. The groups are realigned as profiles, and the result replaces the current alignment only if its SP score is higher. Edges are visited from the deepest to the root, and passes repeat until a pass changes nothing or the limit is reached.

## Example

Take $k = 4$ DNA sequences. The implementation uses $k$-mers of length 2, a toy DNA model with $p_{ii} = 0.16$, $p_{ij} = 0.03$ for $i \ne j$ and $p_i = 0.25$, so a match scores $\ln 2.56 \approx 0.94$ and a mismatch $\ln 0.48 \approx -0.73$ in the SP objective, and a linear gap penalty of 1.5.

$$S_1 = \texttt{ACGGTGG},\quad S_2 = \texttt{ACGTGG},\quad S_3 = \texttt{ATGTTGC},\quad S_4 = \texttt{ACGTTG}.$$

**Stage 1.** The k-mer distances are $d(S_1, S_2) = 0$, $d(S_1, S_4) = d(S_2, S_4) = 1/5$, $d(S_3, S_4) = 2/5$, $d(S_2, S_3) = 3/5$ and $d(S_1, S_3) = 2/3$. UPGMA gives TREE1 $= (S_3, (S_4, (S_1, S_2)))$, and the progressive draft is

```
S1  ACGGTGG-
S2  AC-GTGG-
S3  AT-GTTGC
S4  AC-GTTG-
```

$S_2$ has one `G` fewer than $S_1$. Placing its gap in column 3 or in column 4 gives the same score against $S_1$; the tie is broken in favor of column 3.

**Stage 2.** The Kimura distances on the draft are 0 for $S_1, S_2$, about 0.19 for $S_4$ against each of the others, and about 0.44 for $S_3$ against $S_1$ and $S_2$. UPGMA joins $S_1$ with $S_2$, and then, of two equal distances of about 0.19, the tie rule joins $S_3$ with $S_4$. TREE2 $= ((S_1, S_2), (S_3, S_4))$. The subtree $(S_1, S_2)$ is in TREE1, so its alignment `ACGGTGG` over `AC-GTGG` is reused. The new alignment is

```
S1  ACGGTGG
S2  AC-GTGG
S3  ATGTTGC
S4  ACGTTG-
```

with SP score about 9.77.

**Stage 3.** TREE2 has six edges, one above each leaf and one above each pair; the two edges at the root give the same split, so there are $2k - 3 = 5$ different cuts. Cutting the edge above $S_1$ changes nothing. Cutting the edge above $S_2$ realigns $S_2$ alone against the other three rows, which now prefer the gap in column 4:

```
S1  ACGGTGG
S2  ACG-TGG
S3  ATGTTGC
S4  ACGTTG-
```

The SP score rises to about 13.12, and the change is kept. The other edges and a second pass find no improvement, so MUSCLE stops. The exact dynamic program over all alignments gives the same score, 13.12, so here the refinement reaches the optimum. The draft of stage 1 also scored 13.12: the gap that the tie of stage 1 put in column 3 of $S_2$ became a poor place only after stage 2 realigned $S_3$ and $S_4$ without it, and stage 3 moved it and won back the lost score.

## Correctness

Three claims hold for every input: the output is a valid multiple alignment; the SP score of the alignment never decreases during stage 3; and stage 3 ends. Validity holds after lines L3 and L6 because each profile alignment keeps both groups as blocks and adds only whole gap columns. It holds after each accepted step of stage 3 because removing columns of gaps only from a group keeps the group valid, and the realignment of two valid groups is valid. The SP score never decreases because line L12 replaces the alignment only with one of strictly higher score. Stage 3 ends after at most maxPasses passes, and even without the limit, because the input has finitely many alignments and each accepted step strictly increases the score. For $k = 2$ the LE score of two one-row columns is the pair score $\log(p_{ij}/(p_i p_j))$, so the result is an optimal global alignment. The proof file has the details.

## Complexity

Edgar's analysis, with $k$ sequences of length about $L$, in the word RAM:

- **Line L1.** k-mer counts take $O(kL)$ time, and comparing all pairs $O(k^2 L)$.
- **Lines L2 and L5.** UPGMA takes $O(k^2)$ time with the right data structures (and $O(k^3)$ with a plain search for the closest pair).
- **Lines L3 and L6.** $k - 1$ profile alignments, each with an $O(L^2)$ table and constant-size frequency vectors per column: $O(k L^2)$.
- **Line L4.** $O(k^2 L)$ time for the Kimura distances.
- **Lines L7 to L13.** Each pass tries $2k - 3$ edges, each with an $O(L^2)$ profile alignment and an SP score over $O(k^2)$ pairs and $O(L)$ columns: $O(k L^2 + k^3 L)$ per pass.

Edgar reports $O(k^2 L + k L^2)$ time and $O(k^2 + kL + L^2)$ space for the first two stages, and an extra $O(k^3 L)$ time for refinement, with the number of passes bounded by a constant.

## Properties

- **Deterministic.** Ties in UPGMA and tracebacks are broken by fixed rules.
- **Anytime.** The result after stage 1 or stage 2 is already an alignment; stage 3 only improves the SP score, so it can stop at any time.
- **Monotone stage 3.** The SP score is nondecreasing over stage 3, so the output scores at least as high as the alignment after stage 2.
- **Optimal for two sequences**, not for three or more.

## Variants and improvements

- **MUSCLE-p.** Stages 1 and 2 only, the progressive part, for large sets of sequences.
- **MUSCLE version 5.** Edgar's later version uses posterior probabilities from a pair HMM with consistency, close to [ProbCons](/probcons/), and can produce an ensemble of alignments.
- **Related tools.** [MAFFT](/mafft/) in its FFT-NS-i mode uses the same tree-dependent restricted partitioning; [Clustal](/clustal/) has no refinement stage.

## When to use it

Use MUSCLE for a few hundred to a few thousand related protein or DNA sequences, when a fast and accurate alignment is needed. For very many sequences, use stage 1 alone or a tool built for scale. For small sets of distant proteins, consistency methods such as [T-Coffee](/t-coffee/) or [ProbCons](/probcons/) are often more accurate.

## Pitfalls

- **The SP score is not accuracy.** Stage 3 improves the objective, which usually, but not always, brings the alignment closer to the reference alignment from structures.
- **k-mer distances on short or very different sequences.** The k-mer fraction is crude; for distant sequences, stage 1 trees can be poor, and stage 2 matters.
- **Saturated Kimura distance.** When $1 - D - D^2/5 \le 0$ the formula is undefined; an implementation must cap the distance.
- **Empty columns after a split.** Each group must lose its columns of gaps only before realignment, or the profile score sees phantom columns.
- **Floating-point ties.** The LE score uses logarithms, so exact ties are rare and depend on rounding. Compare scores with a small tolerance when testing for improvement.

## Implementations

## History

Robert Edgar published MUSCLE in 2004, in Nucleic Acids Research for the method and benchmark results, and in BMC Bioinformatics for the detailed algorithm and its complexity. The refinement stage follows the iterative strategies of Berger and Munson (1991), Hirosawa and others (1995) and Gotoh (1996), restricted to the edges of the guide tree. MUSCLE became one of the most used aligners, and Edgar released a rewritten version 5 in 2022.

## References
