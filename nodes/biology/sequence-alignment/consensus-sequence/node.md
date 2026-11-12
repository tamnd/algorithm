---
tag: 82QDV6
kind: problem
slug: consensus-sequence
name: Consensus sequence
aliases:
- center string
- median string
area: biology/sequence-alignment
level: core
summary: "One sequence that sums up a set of sequences: the string with the least total distance to all of them. For an alignment it is the most frequent residue in each column."
prereqs: [multiple-sequence-alignment, hamming-distance, edit-distance]
see_also: [sequence-logo, position-specific-scoring-matrix, profile-hmm, center-star-method, center-star-approximation-bound, consensus-sequence-calling, majority-rule-consensus, sum-of-pairs-score]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: "Chapter 14 (multiple string comparison): the center star method, and the sections on consensus objective functions (the Steiner string and the consensus string of an alignment)"
  - paper: doi:10.1093/nar/15.4.1353
    title: Douglas R. Cavener, Comparison of the consensus sequence flanking translational start sites in Drosophila and vertebrates, Nucleic Acids Research 15(4), 1987, pages 1353 to 1361
    locator: the rules for writing a consensus (one base above 50 percent and above twice the second base; two bases above 75 percent together; else N)
  - paper: doi:10.1093/nar/13.9.3021
    title: Athel Cornish-Bowden, Nomenclature for incompletely specified bases in nucleic acid sequences, recommendations 1984, Nucleic Acids Research 13(9), 1985, pages 3021 to 3030
    locator: the table of one-letter codes for sets of bases (R, Y, S, W, K, M, B, D, H, V, N)
  - paper: doi:10.1016/s0304-3975(97)00240-5
    title: Colin de la Higuera and Francisco Casacuberta, Topology of strings, median string is NP-complete, Theoretical Computer Science 230(1-2), 2000, pages 39 to 48
    locator: NP-completeness of the median string problem under the edit distance, for an unbounded alphabet
  - paper: doi:10.1016/j.jda.2004.08.015
    title: François Nicolas and Eric Rivals, Hardness results for the center and median string problems under the weighted and unweighted edit distances, Journal of Discrete Algorithms 3(2-4), 2005, pages 390 to 415
    locator: NP-hardness and W[1]-hardness of median string and center string, also for a binary alphabet
  - paper: doi:10.4230/LIPIcs.ESA.2020.61
    title: Gary Hoppenworth, Jason W. Bentley, Daniel Gibney and Sharma V. Thankachan, The fine-grained complexity of median and center string problems under edit distance, ESA 2020, LIPIcs 173
    locator: the SETH lower bound of n to the power k minus epsilon for k strings, and the O(n^k) algorithm of Sankoff (1975) that it matches
  - paper: doi:10.1145/506147.506150
    title: Ming Li, Bin Ma and Lusheng Wang, On the closest string and substring problems, Journal of the ACM 49(2), 2002, pages 157 to 171
    locator: the polynomial-time approximation scheme for the closest string problem
  - paper: doi:10.1016/S0890-5401(03)00057-9
    title: J. Kevin Lanctot, Ming Li, Bin Ma, Shaojiu Wang and Louxin Zhang, Distinguishing string selection problems, Information and Computation 185(1), 2003, pages 41 to 55
    locator: the closest string problem, its NP-hardness and a 4/3 approximation
---

A consensus sequence is one string that sums up a set of related sequences: the string whose total distance to all of them is as small as possible. For a [multiple sequence alignment](/multiple-sequence-alignment/) under the [Hamming distance](/hamming-distance/), this optimum is the most frequent symbol of each column, and it takes linear time to find. For unaligned sequences under the [edit distance](/edit-distance/) the same problem, the *median string*, is [NP-hard](/np-hard/). Biologists write a consensus with IUPAC codes for columns that have no single winner, and they know that it throws away most of what a [position-specific scoring matrix](/position-specific-scoring-matrix/) keeps.

## In plain words

You have many versions of the same short text, for example copies of one gene from different animals, written one above the other so that matching letters stand in the same column. You want one line that best stands for all of them.

Go column by column and write down the letter that occurs most often. If two letters tie, write a special letter that means "either of these". The result is the consensus. No other line agrees with the copies in more places.

If the copies are not lined up, the problem gets much harder, because you must also decide where letters were inserted and deleted. Then no fast method is known that is always right.

The consensus is easy to read, but it is a summary: it does not say whether a column was nearly all one letter or only barely so.

## Definition

**Input.** A set $S = \{s_1, \ldots, s_k\}$ of $k \ge 1$ strings over an alphabet $\Sigma$, and a distance $d$ on strings.

**Median string (the general problem).** Find a string $c \in \Sigma^*$ that minimizes

$$D(c) = \sum_{i=1}^{k} d(c, s_i).$$

With $d$ the edit distance, an optimal $c$ is also called a *Steiner string* of $S$ (Gusfield, Chapter 14).

**Column consensus (the aligned case).** The input is an alignment: $k$ rows of the same length $L$ over $\Sigma \cup \{-\}$, where $s_{ij}$ is the symbol of row $i$ in column $j$. Let $n_j(a) = |\{i : s_{ij} = a\}|$ be the count of symbol $a$ in column $j$. With $d$ the Hamming distance,

$$D(c) = \sum_{i=1}^{k} \sum_{j=1}^{L} [c_j \ne s_{ij}] = \sum_{j=1}^{L} \bigl(k - n_j(c_j)\bigr).$$

The sum splits into one term for each column, and the term of column $j$ depends only on $c_j$. So $c$ is optimal if and only if each $c_j$ is a most frequent symbol of column $j$ (a *plurality* symbol). The optimum value is $\sum_j (k - \max_a n_j(a))$, and the number of optimal strings is the product over the columns of the number of tied symbols. To print the consensus as a sequence, delete the gap symbols from $c$.

**The consensus as a mode.** Let $f_j(a) = n_j(a)/k$. The product model $P(x) = \prod_j f_j(x_j)$ is the simplest profile of the alignment. Its most probable string maximizes each factor on its own, so it is again the column-wise plurality string. The consensus is the mode of the profile, and only the mode.

## Variants

- **Ties and ambiguity codes.** When the top symbols tie, report the set. For DNA the IUPAC codes of Cornish-Bowden (1985) name each set of bases with one letter: R = A or G, Y = C or T, S = G or C, W = A or T, K = G or T, M = A or C, B = not A, D = not C, H = not G, V = not T, N = any base.
- **Threshold rules.** Biologists often require a clear winner. The rule of Cavener (1987) writes one base if its frequency is above 50 percent and above twice that of the second base; else two bases (a code such as R) if their sum is above 75 percent; else N. This is not an optimum of $D$; it is a rule for when to trust a column.
- **Gap rules.** Either the gap is a symbol like any other, and a column whose plurality is the gap drops out of the printed consensus; or the counts ignore gaps; or a column enters the consensus only if its fraction of residues reaches a threshold. HMMER's model builder uses the last rule, with a threshold of one half by default, to decide which columns become match states of a [profile HMM](/profile-hmm/).
- **Weighted consensus.** With a weight $w_i \ge 0$ for each row, minimize $\sum_i w_i \, d(c, s_i)$. The same split by columns shows that the weighted plurality of each column is optimal. Weights correct for groups of near-identical rows.
- **Set median, or center string in Gusfield's sense.** Restrict $c$ to the input strings: find $s_c \in S$ with the least $\sum_i d(s_c, s_i)$. This needs only the $\binom{k}{2}$ pairwise distances. The [center star method](/center-star-method/) starts from this string.
- **Closest string, or center string in the minimax sense.** Minimize $\max_i d(c, s_i)$ instead of the sum. Under the Hamming distance this problem no longer splits by columns, and it is NP-hard (Lanctot et al. 2003).

## Examples

Take this alignment of $k = 6$ DNA rows and $L = 7$ columns.

```
r1  T A T A - A T
r2  T A T G - A A
r3  T A T G - A T
r4  C A T A G A T
r5  T A - A - G T
r6  T G T G T A C
```

| column | counts | plurality | Cavener |
|---|---|---|---|
| 1 | T 5, C 1 | T | T |
| 2 | A 5, G 1 | A | A |
| 3 | T 5, gap 1 | T | T |
| 4 | A 3, G 3 | A or G (tie) | R |
| 5 | gap 4, G 1, T 1 | gap | (insert column) |
| 6 | A 5, G 1 | A | A |
| 7 | T 4, A 1, C 1 | T | T |

The plurality strings are TATA-AT and TATG-AT. Each has total Hamming distance $1 + 1 + 1 + 3 + 2 + 1 + 2 = 11$. A search over all $5^7 = 78125$ strings over $\{A, C, G, T, -\}$ finds no other string with $D = 11$, as the column argument predicts ($1 \cdot 1 \cdot 1 \cdot 2 \cdot 1 \cdot 1 \cdot 1 = 2$ optima). With the tie as a code and the gap column left out, the consensus is printed TATRAT.

The two optima differ under the minimax objective. The largest distance from TATG-AT to a row is 3, and 3 is the best possible radius; TATA-AT has radius 4. So a median and a closest string can be different strings.

The consensus also hides strength. Column 1 (T in 5 of 6 rows) and column 7 (T in 4 of 6) both give T. Under Cavener's rule, column 4 gives R for the counts A 3, G 3, and it would also give R for the counts A 4, G 3, C 1, because neither base is above 50 percent and A and G together are above 75 percent. A [sequence logo](/sequence-logo/) and a PSSM keep these differences.

**A consensus that is not in the set.** Take AAC, ACA and CAA. Each input string has total distance $0 + 2 + 2 = 4$ to the set, but the consensus AAA has total distance $1 + 1 + 1 = 3$. So the set median can be worse than the median.

## Known algorithms

- **Column plurality.** Count each symbol in each column, then take a maximum. This takes $\Theta(kL)$ time and $O(|\Sigma|)$ extra space for each column, and it solves the aligned problem exactly, by the split of $D$ above.
- **Exact median string for a fixed number of strings.** A $k$-dimensional dynamic program over all prefixes of the $k$ inputs, as in multiple alignment, finds a median under the edit distance in $O(n^k)$ time for $k$ strings of length at most $n$ and a fixed $k$ (Sankoff 1975, as cited by Hoppenworth et al. 2020). The constant grows exponentially in $k$.
- **Set median as an approximation.** The best input string is within a factor $2 - 2/k$ of the median under any metric $d$. *Proof.* Let $c^*$ be a median and $D^* = D(c^*)$. For each $j$, the triangle inequality gives $\sum_{i \ne j} d(s_j, s_i) \le \sum_{i \ne j} \bigl(d(s_j, c^*) + d(c^*, s_i)\bigr) = (k-2)\, d(s_j, c^*) + D^*$. Add this over $j = 1, \ldots, k$: the total is at most $(k-2) D^* + k D^* = (2k - 2) D^*$. The smallest of the $k$ values $D(s_j)$ is at most their mean, which is at most $(2 - 2/k) D^*$. $\blacksquare$ The factor is tight: for the $k$ strings of length $k$ that have a C at position $i$ and A elsewhere, each $D(s_j) = 2(k-1)$, while A...A has $D = k$. The example AAC, ACA, CAA above is the case $k = 3$.
- **Closest string.** Li, Ma and Wang (2002) give a polynomial-time approximation scheme for the Hamming closest string problem, and Lanctot et al. (2003) a factor $4/3 + o(1)$ algorithm by linear programming and rounding.
- **Heuristics for the median.** Build a multiple alignment by a heuristic such as [progressive alignment](/progressive-alignment/), then take its column consensus. The result is a median of the alignment, not of the unaligned strings.

## Bounds

- **Aligned case.** $\Theta(kL)$ time is optimal: each of the $kL$ symbols can change the answer, so each must be read.
- **Median string under edit distance.** NP-complete for an unbounded alphabet (de la Higuera and Casacuberta 2000), and NP-hard and W[1]-hard with respect to $k$ even over a binary alphabet (Nicolas and Rivals 2005). Hoppenworth, Bentley, Gibney and Thankachan (2020) show that an $O(n^{k - \varepsilon})$ algorithm, for some $\varepsilon > 0$ and alphabets of size $O(k)$, would refute the Strong Exponential Time Hypothesis. So the $O(n^k)$ dynamic program is close to optimal. The same lower bound holds for the center string under edit distance. The page [edit distance under SETH](/edit-distance-seth-lower-bound/) gives the case $k = 2$.
- **Closest string under Hamming distance.** NP-hard (see Lanctot et al. 2003), but it has a PTAS.

## Reductions

- **Median string and alignment.** A median string $c$ of $S$ gives a multiple alignment of $S$: align each $s_i$ optimally to $c$ and merge these pairwise alignments on the columns of $c$. Conversely, the column consensus of an alignment is a median for the cost of that alignment. Gusfield (Chapter 14) shows that an optimal alignment under this *consensus objective* and a Steiner string are equivalent problems.
- **Consensus as a degenerate profile.** A PSSM with score 1 for the plurality symbol and 0 for all others scores a sequence by the number of positions where it agrees with the consensus. So a consensus search is a profile search that keeps only the identity of the top symbol of each column.

## Applications

- **Naming motifs.** Binding sites, splice sites and start-codon contexts are often written as a consensus with IUPAC codes, for example in Cavener's comparison of the sequence around start codons in Drosophila and vertebrates.
- **Probes and primers.** A consensus with ambiguity codes describes a set of oligonucleotides, one for each choice at the coded positions.
- **Read consensus in assembly.** In genome assembly the bases of the reads stacked on one position are voted on to give the contig sequence; see [consensus sequence calling](/consensus-sequence-calling/).
- **Labels for models.** HMMER and other profile tools print a consensus line under each model, for a quick read of the model.
- **Analogues.** The same majority idea gives the [majority-rule consensus](/majority-rule-consensus/) of phylogenetic trees.

## References
