---
tag: D91MJT
kind: algorithm
slug: greedy-shortest-common-superstring
name: Greedy shortest common superstring
aliases:
- greedy SCS heuristic
area: biology/genome-assembly
level: intro
summary: Assemble reads by merging, again and again, the two strings with the largest overlap. It returns a superstring within a constant factor of the shortest.
solves: [shortest-common-superstring]
model: word-ram
complexity:
  vars: {m: the number of reads, n: the total length of the reads}
  time: {worst: O(m·n + m^2·log m)}
  space: {extra: O(n + m^2)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [shortest-common-superstring, overlap-graph, genome-repeat]
see_also: [greedy-superstring-merge, shortest-common-superstring-np-hard, overlap-detection, overlap-layout-consensus, lander-waterman-model, de-bruijn-assembly, string-graph, approximation-ratio]
sources:
  - paper: doi:10.1145/179812.179818
    title: Avrim Blum, Tao Jiang, Ming Li, John Tromp and Mihalis Yannakakis, Linear approximation of shortest superstrings, Journal of the ACM 41(4), 1994
    locator: pp. 630 to 647, the proof that the greedy superstring is at most 4 times the optimum
  - paper: doi:10.1016/j.ipl.2004.09.012
    title: Haim Kaplan and Nira Shafrir, The greedy algorithm for shortest superstrings, Information Processing Letters 93(1), 2005
    locator: pp. 13 to 17, the factor 3.5
  - paper: doi:10.1186/1471-2105-14-S5-S18
    title: Guy Bresler, Ma'ayan Bresler and David Tse, Optimal assembly for high throughput shotgun sequencing, BMC Bioinformatics 14(Suppl 5), S18, 2013
    locator: Theorem 2, greedy reconstructs the genome when every repeat is bridged by a read
  - paper: doi:10.1016/j.ygeno.2010.03.001
    title: Jason R. Miller, Sergey Koren and Granger Sutton, Assembly algorithms for next-generation sequencing data, Genomics 95(6), 2010
    locator: pp. 315 to 327, the section on greedy graph assemblers
  - paper: "Granger G. Sutton, Owen White, Mark D. Adams and Anthony R. Kerlavage, TIGR Assembler: a new tool for assembling large shotgun sequencing projects, Genome Science and Technology 1(1), 1995"
    locator: pp. 9 to 19
  - url: "https://arxiv.org/abs/2111.03968"
    title: Matthias Englert, Nicolaos Matsakis and Pavel Veselý, Improved approximation guarantees for shortest superstrings using cycle classification by overlap to length ratios, STOC 2022
    locator: the factor (13 + 57^(1/2))/6 for the greedy algorithm
  - url: "https://arxiv.org/abs/2609.01365"
    title: Nikolai Chukhin, Rishikesh Gajjala, Juha Harviainen, Alexander S. Kulikov, Ivan Mihajlin, Hiroki Shibata and Alexander V. Smal, The Greedy Superstring Conjecture Is False, arXiv preprint, 2026
    locator: abstract, the claimed lower bound tending to 2.4 and upper bound 3 (not peer reviewed)
---

Greedy shortest common superstring assembly builds a genome from sequencing reads by merging, again and again, the two current strings with the largest [overlap](/overlap-graph/), until one string is left or no overlap reaches a threshold. It is the oldest assembly heuristic and a constant-factor approximation of the NP-hard [shortest common superstring](/shortest-common-superstring/): the result is at most about 3.425 times the optimum in the worst case. For assembly the length bound matters less than a second fact: when every pair of adjacent reads overlaps by more than the longest [repeat](/genome-repeat/) of the genome, greedy returns the genome exactly. This page takes the assembly view; the graph form and the approximation proofs are on [greedy superstring merging](/greedy-superstring-merge/).

## In plain words

You have many short pieces of text, cut at random places from copies of one long text. First you throw away every piece that already appears inside another piece. Then you look for the two pieces where the end of one agrees with the start of the other over the longest stretch, and you glue them together on that stretch. You repeat with the glued pieces. You stop when one piece is left, or when the best agreement is too short to trust.

The method trusts the longest agreement first. That is right when long agreements are rare by chance. It goes wrong when the text has two long equal passages: a piece that ends in one passage can then be glued to a piece that starts in the other.

## The problem

**Model.** The genome is a string $x$ of length $G$ over $\{A, C, G, T\}$. Sequencing gives $N$ reads, each a substring of $x$ of length about $L$, so the coverage is $c = NL/G$. On this page the reads have no errors and all come from the same strand; the [read error correction](/read-error-correction/) and reverse-complement issues are in the pitfalls. The longest repeat $R$ of $x$ is the largest length of a string that occurs at two different positions of $x$.

**Input.** A list of reads $r_1, \ldots, r_N$ and a threshold $\tau \ge 0$. For strings $a \ne b$, $\mathrm{ov}(a, b)$ is the length of the longest proper suffix of $a$ that is also a proper prefix of $b$.

**Output.** A list of contigs: strings such that every read occurs inside one of them. With $\tau = 0$ there is one contig, a common superstring of all reads. The goal is to output $x$; the stated guarantee is the reconstruction theorem below, and the length bound relative to the [shortest common superstring](/shortest-common-superstring/).

## The algorithm

The algorithm keeps the reads as vertices and joins them into chains, one chain for each contig. For a chain it stores the head (its first read) and the tail (its last read). Merging two contigs is joining the chain ending at a tail $i$ to the chain starting at a head $j$, and the overlap of the two contigs is $w(i, j) = \mathrm{ov}(s_i, s_j)$ (see Correctness). So the overlaps are computed once.

```pseudo id=main
GREEDY-ASSEMBLE(reads, τ)
L1  remove empty reads, repeated reads and reads inside other reads; call the rest s[0 .. m − 1]
L2  w(i, j) ← ov(s[i], s[j]) for all i ≠ j; sort the pairs by decreasing w, ties by smaller i, then smaller j
L3  for each pair (i, j) in this order, until m − 1 pairs are accepted do
L4      if i is not a tail, or j is not a head, or head[i] = j then skip the pair
L5      if w(i, j) < τ then stop the loop
L6      accept: next[i] ← j, prev[j] ← i
L7      join the chains: head[tail[j]] ← head[i], tail[head[i]] ← tail[j]
L8  return, for each chain, s[h] for its head h followed by each next read without its first w letters
```

Line L4 skips a pair whose reads are no longer the end and the start of two different contigs; the test $\mathit{head}[i] = j$ catches the pair that would close a chain into a cycle. Line L5 stops at the first usable pair below the threshold, because the pairs come in decreasing order of overlap. With $\tau = 0$ every usable pair passes, and one contig remains. The overlaps of line L2 come from the prefix function of $s_j \,\#\, s_i$ with a separator $\#$.

## Example

The genome is $x =$ `ATGGCGTGCAATG`, with $G = 13$. Its longest repeat is `ATG`, at positions 0 and 10, so $R = 3$. There are five reads: `ATGGCGT` (position 0), `GGCGTGC` (2), `CGTGCAA` (4), `TGCAATG` (6) and `GCGTG` (3). Line L1 removes `GCGTG`, which lies inside `GGCGTGC`, and leaves $s_0, s_1, s_2, s_3$ in this order. The overlaps $w(i, j)$ are:

| $w(i, j)$ | $s_0$ | $s_1$ | $s_2$ | $s_3$ |
|---|---|---|---|---|
| $s_0$ = `ATGGCGT` | | 5 | 3 | 1 |
| $s_1$ = `GGCGTGC` | 0 | | 5 | 3 |
| $s_2$ = `CGTGCAA` | 1 | 0 | | 5 |
| $s_3$ = `TGCAATG` | 3 | 1 | 0 | |

With $\tau = 3$ the scan goes as follows.

| pair | $w$ | L4 | L5 | contigs after the step |
|---|---|---|---|---|
| $(0, 1)$ | 5 | usable | $5 \ge 3$ | `ATGGCGTGC`, `CGTGCAA`, `TGCAATG` |
| $(1, 2)$ | 5 | usable | $5 \ge 3$ | `ATGGCGTGCAA`, `TGCAATG` |
| $(2, 3)$ | 5 | usable | $5 \ge 3$ | `ATGGCGTGCAATG` |

After three accepted pairs the loop ends, and the one contig is $x$. The pair $(3, 0)$ with overlap 3, the repeat `ATG`, is never reached; if it were, line L4 would skip it, because $\mathit{head}[3] = 0$. Every adjacent overlap is 5 and $5 > R$, so the reconstruction theorem below predicts this result.

**A repeat that no read spans.** The genome `CATTGACAGTTGACG` has length 15 and the repeat `TTGAC` at positions 2 and 9, so $R = 5$. Take the six reads of length 6 at positions 0, 2, 4, 6, 8 and 9: `CATTGA`, `TTGACA`, `GACAGT`, `CAGTTG`, `GTTGAC`, `TTGACG`. The adjacent true overlaps are 4, 4, 4, 4 and 5, none above $R$. The largest overlap of all is 5, from `GTTGAC` (position 8) to `TTGACA` (position 2): the shared part is the repeat, and the merge is false. Greedy with $\tau = 0$ returns `CATTGACGTTGACAGTTG`, of length 18. It contains every read, but it is not the genome, and it is longer than the shortest superstring, which has length 15. With $\tau = 2$ it returns two contigs, `CATTGACG` and `GTTGACAGTTG`, and both are misassembled.

## Correctness

Three facts make the algorithm right. First, line L1 loses no read: each removed read occurs in a strictly longer read, and following this relation ends at a kept read. Second, the merge of a pair with the largest overlap creates no new containment, and the overlap of a merged contig with any other contig equals the overlap of its tail read, or of its head read, with that contig. So the scan over the fixed list of read pairs merges, at each round, two current contigs with the largest overlap, exactly as the string form does. Third, a contig string ends with its tail read, so each appended part overlaps the current string on a real suffix, and the contig contains all of its reads.

**Reconstruction theorem.** Let the reads be substrings of $x$. Call a read maximal if its interval in $x$ is not inside the interval of another read, and sort the distinct maximal intervals by start. If the first starts at 0, the last ends at $G$, and every two adjacent maximal reads overlap by more than $R$ letters, then GREEDY-ASSEMBLE with any $\tau \le R + 1$ returns $x$. The reason: every current contig is an interval of $x$ longer than $R$, so it occurs at one place in $x$. The largest overlap is longer than $R$, so its shared part also occurs once, and the merge joins two contigs that are adjacent in $x$, on their true overlap. The full proof, with the lemmas above, is in the correctness file. Bresler, Bresler and Tse (2013, Theorem 2) prove a stronger version: greedy reconstructs $x$ when each repeat is bridged, that is, when some read covers a copy of the repeat together with one more letter on each side.

## Complexity

Let $m$ be the number of reads and $n$ their total length, on the word RAM. These are worst-case bounds.

- **Line L1.** Each containment test of $r$ in $t$ uses the prefix function in $O(|r| + |t|)$ time. Over all ordered pairs this is $O(m \cdot n)$.
- **Line L2.** The overlaps also cost $O(m \cdot n)$ in total, and sorting the $m(m - 1)$ pairs costs $O(m^2 \log m)$. The list of pairs takes $O(m^2)$ space.
- **Lines L3 to L7.** Each pair is looked at once, in $O(1)$ time.
- **Line L8.** Spelling the contigs takes $O(n)$ time.

The total is $O(m \cdot n + m^2 \log m)$ time and $O(n + m^2)$ space. All overlaps can also be found in $O(n + m^2)$ time with a [generalized suffix tree](/generalized-suffix-tree/). For real data the $m^2$ term is the problem: a run with $10^6$ reads has about $10^{12}$ pairs. Practical greedy assemblers therefore first run [overlap detection](/overlap-detection/), keep only the candidate pairs it reports, and sort those.

**How much coverage the theorem needs.** Assume reads of equal length $L$ whose starts form a Poisson process of rate $N/G$ along the genome, and ignore the two ends. The gap from one start to the next is exponential with rate $N/G$, and adjacent reads overlap by more than $R$ letters exactly when the gap is less than $L - R$. So the expected number of adjacent pairs that break the condition is about
$$ N \, e^{-(N/G)(L - R - 1)} = N \, e^{-c \, (L - R - 1)/L}. $$
For $G = 5 \cdot 10^6$, $L = 1000$ and $R = 300$, coverage $c = 15$ ($N = 75\,000$) gives about 2.1 expected breaks, and $c = 30$ ($N = 150\,000$) gives about $1.2 \cdot 10^{-4}$. This is an expectation under the stated random model, not a worst-case bound. If $R \ge L - 1$, no read can cover the longest repeat with one more letter on each side, the condition fails at every coverage, and greedy can merge across the repeat. The [Lander-Waterman model](/lander-waterman-model/) gives the matching analysis of coverage gaps.

## Properties

- **Length guarantee.** With $\tau = 0$, the output has length at most about $3.425 \cdot \mathrm{OPT}$ in the worst case, where $\mathrm{OPT}$ is the length of a shortest common superstring (Blum et al. proved 4, Kaplan and Shafrir 3.5, Englert, Matsakis and Veselý about 3.425). On the repeat example above, the ratio is $18/15 = 1.2$.
- **Shortest is not right.** Even an exact shortest superstring can be the wrong genome, because it collapses repeats. The reconstruction theorem is the guarantee that matters for assembly, and it needs the repeat condition.
- **Deterministic.** With the fixed tie rule, the output depends only on the list of reads and its order.
- **Not online.** All overlaps must be known before the first merge.
- **Nested thresholds.** Up to the point where it stops, the scan with a higher $\tau$ makes the same decisions as the scan with a lower one. So its accepted pairs are a subset of the accepted pairs at the lower threshold, and each of its contigs is a part of a contig at the lower threshold.

## Variants and improvements

- **Reverse complements.** Real reads come from both strands. An assembler stores each read and its reverse complement, compares all four orientations of a pair, and makes sure that a read and its complement are not used in two different places of one contig.
- **Errors and similarity scores.** With sequencing errors, exact overlaps are replaced by alignments with a score, and the threshold applies to the score and to the identity. TIGR Assembler first compares reads by shared oligonucleotides and aligns only the promising pairs.
- **Short-read greedy assemblers.** Several early assemblers for short reads extended contigs greedily by the read with the best overlap; Miller, Koren and Sutton (2010) review them and their limits with repeats.
- **Graph assemblers.** The [overlap-layout-consensus](/overlap-layout-consensus/) method keeps all overlaps in a graph and simplifies it before it commits to a layout, and the [string graph](/string-graph/) removes the overlaps that greedy would never need. [De Bruijn assembly](/de-bruijn-assembly/) avoids pairwise overlaps altogether.
- **The plain superstring problem.** For the approximation algorithms with better ratios, see [greedy superstring merging](/greedy-superstring-merge/) and the problem page.

## When to use it

Use greedy merging for small assembly tasks with long accurate reads and short repeats, such as a plasmid, an amplicon set or a short-read test case, and as a baseline for other assemblers. Its result is easy to explain and to check. Do not use it on genomes with repeats longer than the read overlaps, for example on most eukaryotic genomes with short reads: it merges across the first repeat it meets and it never undoes a merge.

## Pitfalls

- **False merges at repeats.** The largest overlap can be a repeat, as in the second example. Greedy commits to it, and later merges build on the error. A threshold above the longest repeat of the reads is safe only when the reads are long enough to have such overlaps.
- **Thresholds that are too low.** A short overlap such as 1 to 5 bases occurs by chance between many reads. With $\tau$ near 0, greedy glues unrelated contigs and the output looks complete but is wrong. Report contigs with a threshold, not one forced superstring.
- **Containment test with errors.** A read that differs from a longer read by one error is not a substring of it and is not removed; it then produces extra overlaps. Error correction or alignment-based containment is needed.
- **Ignoring the reverse strand.** Reads from the other strand overlap nothing in the forward sense, so a forward-only greedy leaves them as separate contigs or merges them by chance.
- **Quadratic memory.** Storing all $m^2$ pairs fails for millions of reads; filter the candidate pairs first.

## Implementations

## History

TIGR Assembler (Sutton, White, Adams and Kerlavage, 1995) merged reads greedily by overlap score and was used for early whole-genome shotgun projects at The Institute for Genomic Research. Blum, Jiang, Li, Tromp and Yannakakis gave the first constant factor for the length, 4, in 1991 (journal 1994), Kaplan and Shafrir improved it to 3.5 in 2005, and Englert, Matsakis and Veselý to about 3.425 in 2022. Tarhio and Ukkonen conjectured in 1988 that the factor is 2. A 2026 preprint by Chukhin, Gajjala, Harviainen, Kulikov, Mihajlin, Shibata and Smal claims to refute this conjecture with instances of ratio approaching 2.4, and claims an upper bound of 3; it has not yet been peer reviewed. Bresler, Bresler and Tse (2013) analysed greedy as an assembler and gave its reconstruction condition in terms of bridged repeats.

## References
