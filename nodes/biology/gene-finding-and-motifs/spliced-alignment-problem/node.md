---
tag: CAPGHE
kind: problem
slug: spliced-alignment-problem
name: Spliced alignment problem
aliases:
- Gelfand-Mironov-Pevzner spliced alignment
area: biology/gene-finding-and-motifs
level: core
summary: Find a chain of candidate exons in a genome whose concatenation best aligns to a known related protein or transcript.
prereqs: [exon-chaining, global-alignment, needleman-wunsch]
see_also: [dag-longest-path, alignment-graph, gene-prediction, splice-site-prediction, spliced-read-alignment, maximal-mappable-prefix-alignment, colinear-chaining, edit-distance-seth-lower-bound]
sources:
  - paper: doi:10.1073/pnas.93.17.9061
    title: Mikhail S. Gelfand, Andrey A. Mironov and Pavel A. Pevzner, Gene recognition via spliced sequence alignment, Proceedings of the National Academy of Sciences USA 93(17), 1996
    locator: pp. 9061 to 9066; the spliced alignment problem, its dynamic programming solution over candidate blocks, and the test of gene recognition with related proteins
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Chapter 6, Section 6.14 (the Spliced Alignment Problem, p. 204, and the alignment as a path in a directed acyclic graph), Section 6.13 (exon chaining) and Problem 6.57 (a faster algorithm by a change of the graph)
---

The spliced alignment problem asks for a chain of non-overlapping candidate exons in a genomic DNA sequence whose concatenation has the best alignment score with a target sequence, usually a protein or an mRNA of a related gene. Gelfand, Mironov and Pevzner stated it in 1996 as a way to predict the exon and intron structure of a gene from a similar gene that is already known. It is solved exactly in polynomial time by dynamic programming over the candidate blocks, which is a longest path computation in a [directed acyclic graph](/dag-longest-path/). It is not the same task as [spliced read alignment](/spliced-read-alignment/), which maps millions of short RNA-seq reads to a genome.

## In plain words

A gene in a plant or an animal is stored in the genome in pieces. The pieces that end up in the protein are exons, and the pieces that are cut out between them are introns. Often we already know a protein from a related species, and we want to find the matching gene in a new genome. First mark many stretches of the genome that could be exons. Most of them are false. Then choose some of these stretches, left to right and with no overlap, and glue them together. Of all the ways to do this, find the one whose glued string looks most like the known protein. The known protein acts as a template: it tells us which pieces belong together and in which order.

## Definition

**Input.**
- A genomic sequence $G = g_1 \ldots g_n$.
- A target sequence $T = t_1 \ldots t_m$. Jones and Pevzner take $T$ over the same alphabet as $G$ for simplicity; with a protein target, the blocks are translated first.
- A set $\mathcal{B}$ of $b$ candidate blocks. Each block $B = [f(B), l(B)]$ is an interval of positions of $G$, and its string is $G_B = g_{f(B)} \ldots g_{l(B)}$.
- A scoring scheme for alignment: a score $\delta(x, y)$ for a pair of letters and a penalty $\sigma > 0$ for a letter against a gap.

**Chains.** Write $B' \prec B$ when $l(B') < f(B)$. A chain is a sequence of blocks $\Gamma = (B_1, \ldots, B_k)$ with $B_1 \prec B_2 \prec \cdots \prec B_k$, and its string is the concatenation $\Gamma^* = G_{B_1} G_{B_2} \cdots G_{B_k}$.

**Question.** Find a chain $\Gamma$ that maximizes $s(\Gamma^*, T)$, the score of the best [global alignment](/global-alignment/) of $\Gamma^*$ with $T$.

The problem looks at all chains at once, and there can be exponentially many of them: with $b$ disjoint blocks, every one of the $2^b - 1$ non-empty subsets is a chain. The point of the problem is that one dynamic program finds the best chain without listing them.

The blocks come from outside the problem. In the paper, they are the stretches between a candidate acceptor site (AG) and a candidate donor site (GT), filtered by statistics of coding sequence, or the stretches that are similar to the target. The quality of the answer depends on the blocks: the true exons must be among them.

**Notation of this page.** Positions are 1-based and intervals are closed, as in the book. In the examples, $\delta(x, y) = +1$ for $x = y$ and $-1$ otherwise, and $\sigma = 1$.

## Variants

- **Target type.** The target can be a cDNA or mRNA (same alphabet, nearly identical to the exons when it comes from the same gene), a protein of a related species (the blocks are read in a reading frame and compared codon against amino acid), or an EST.
- **Codons split by introns.** An intron can fall inside a codon. A protein version must then join the last one or two bases of one block with the first bases of the next before it translates them. Programs for protein to genome alignment, such as GeneWise, model this with extra states.
- **Scores at the joins.** A practical version adds a score for each splice site, a penalty for each intron or for its length, and a reward for blocks that score well as coding sequence. These are all extra terms at block boundaries, and the dynamic program keeps its form.
- **Affine gaps.** Gap costs of the form $o + e \cdot \ell$ need the three tables of the [Gotoh algorithm](/gotoh-algorithm/) for each block, and the block-to-block moves join the tables at the same level.
- **Local and semi-global versions.** If only part of the target is expected to match, for example a protein domain, the alignment is made local in $T$ by the usual changes of the boundary conditions.
- **Exon chaining.** If each block gets a fixed weight, for example from a separate local alignment with the target, and the order on the target is ignored, the problem becomes [exon chaining](/exon-chaining/), which is [weighted interval scheduling](/weighted-interval-scheduling/). It is much faster, but its best chain need not give a good alignment with $T$, because it can use blocks that match parts of the target in the wrong order.
- **Spliced read alignment.** Mapping RNA-seq reads of 100 to 300 bases to a whole genome, with unknown introns, is a different problem with a different cost profile; see [spliced read alignment](/spliced-read-alignment/) and [maximal mappable prefix alignment](/maximal-mappable-prefix-alignment/). There the blocks are not given, the reads are short, and the genome is indexed first.

## Examples

**A small instance.** Let $G = \texttt{CCATGCATTTGGTACAACCTGAGTAGCATT}$ ($n = 30$), with five blocks:

| block | interval | string |
|---|---|---|
| $B_1$ | [3, 7] | ATGCA |
| $B_2$ | [11, 15] | GGTAC |
| $B_3$ | [13, 19] | TACAACC |
| $B_4$ | [18, 22] | CCTGA |
| $B_5$ | [24, 28] | TAGCA |

Let $T = \texttt{ATGCAGGTACCGTGATAGCA}$ ($m = 20$). The block $B_3$ overlaps both $B_2$ and $B_4$, so no chain holds $B_3$ together with either of them. Some chains and their scores:

| chain | $\Gamma^*$ | $s(\Gamma^*, T)$ |
|---|---|---|
| $B_1 B_2 B_4 B_5$ | ATGCAGGTACCCTGATAGCA | 18 |
| $B_1 B_2 B_5$ | ATGCAGGTACTAGCA | 10 |
| $B_1 B_4 B_5$ | ATGCACCTGATAGCA | 10 |
| $B_1 B_3 B_5$ | ATGCATACAACCTAGCA | 6 |

The best chain is $B_1 B_2 B_4 B_5$, with 19 matches and one mismatch (C against G at the 12th letter of $T$), score 18. A search over all chains confirms that it is the only chain with score 18. The dynamic program below finds it from the last rows of the blocks: at $l(B_2)$ the best score against $t_1 \ldots t_{10}$ is 10, at $l(B_4)$ the best score against $t_1 \ldots t_{15}$ is 13, and at the first position of $B_5$ the best predecessor for $t_1 \ldots t_{15}$ is $B_4$ with 13 (the other blocks give 6 for $B_2$, 1 for $B_3$ and -5 for $B_1$). The value at $l(B_5)$ and $t_{20}$ is then 18.

**One block.** With the single block $[1, n]$, the problem is the global alignment of $G$ and $T$.

**Disjoint exact exons.** If $T$ is exactly the concatenation of some blocks and all blocks are disjoint, the chain of those blocks has score $m \cdot \delta_{\max}$, the largest possible, and the problem finds it. It can also find another chain with the same string, which shows that the answer need not be unique.

## Known algorithms

**Dynamic programming over blocks (Gelfand, Mironov and Pevzner 1996).** For a block $B$, a position $i \in B$ and $0 \le j \le m$, let $S(i, j, B)$ be the best score of an alignment of $t_1 \ldots t_j$ with a string of the form $\Gamma^* \, g_{f(B)} \ldots g_i$, where $\Gamma$ is a chain (possibly empty) of blocks that precede $B$. The answer is $\max_B S(l(B), m, B)$.

Inside a block, the step is the [Needleman-Wunsch](/needleman-wunsch/) step. For $f(B) < i \le l(B)$:

$$S(i, j, B) = \max\big(S(i - 1, j - 1, B) + \delta(g_i, t_j),\; S(i - 1, j, B) - \sigma,\; S(i, j - 1, B) - \sigma\big).$$

At the first position $i = f(B)$, the row "above" is the best end of any earlier chain:

$$P(B, j) = \max\big(-j\sigma,\; \max_{B' \prec B} S(l(B'), j, B')\big),$$

where the term $-j\sigma$ stands for the empty chain. Then $S(i, j, B)$ uses $P(B, j - 1) + \delta(g_i, t_j)$, $P(B, j) - \sigma$ and $S(i, j - 1, B) - \sigma$, and $S(i, 0, B) = P(B, 0) - \sigma$.

That this is correct is the usual cut argument of alignment (a theorem): cut a best alignment for $S(i, j, B)$ before its last column; the rest is an alignment of the same kind for a smaller index, and the boundary case at $f(B)$ cuts between the last earlier block and $B$. The alignment and the chain come back by a traceback.

**Cost.** Let $L = \sum_B |B|$ be the total length of the blocks. Filling the block tables costs $O(L m)$. The direct computation of $P(B, \cdot)$ scans all earlier blocks, which costs $O(b m)$ per block and $O(b^2 m)$ in total. So the direct algorithm runs in $O((L + b^2) m)$ time.

**A faster join.** Sort the blocks by their first position and keep a running vector $R(j)$, the best value $S(l(B'), j, B')$ over the blocks $B'$ that end before the current point. Move a block into $R$ when the scan passes its last position. Then $P(B, \cdot) = \max(-j\sigma, R)$, and each block is added once and read once, for $O(b m)$ in total. The time becomes $O((L + b) m + b \log b)$. Jones and Pevzner pose this kind of speed-up, as a change of the graph, in Problem 6.57. These two bounds are derived on this page from the recurrence; the paper and the book give their own forms.

**Space.** The score alone needs the last rows of the blocks, $O(b m)$ numbers, plus one row for the current block. A traceback needs the tables, $O(L m)$, or a divide and conquer method in the style of [Hirschberg](/hirschberg-algorithm/) to trade time for space.

**Programs.** The 1996 paper describes the program PROCRUSTES. Later protein to genome aligners, such as GeneWise, keep the same idea and add a probabilistic model of splice sites, introns and frame shifts.

## Bounds

- **Upper bound.** $O((L + b) m)$ time after sorting, in the word RAM with scores that fit in a word. In the worst case $L$ is $\Theta(b n)$ when the blocks overlap a lot. If the blocks are all the intervals between a candidate AG and a later GT, $b$ can be quadratic in $n$, which is why the blocks are filtered first.
- **Conditional lower bound.** The problem contains global alignment as the case of one block. With $\delta(x, x) = 0$, $\delta(x, y) = -1$ for $x \ne y$, and $\sigma = 1$, the best score is minus the edit distance of $G$ and $T$. So a strongly subquadratic algorithm for spliced alignment in $n$ and $m$ would give one for [edit distance](/edit-distance/), which is impossible unless the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) fails ([Backurs and Indyk](/edit-distance-seth-lower-bound/)).
- **No exponential blow-up.** Although the number of chains can be $2^b - 1$, the cost is polynomial, because a best chain ending in $B$ at a given point of $T$ depends only on the best chains ending before $B$ (optimal substructure).

## Reductions

- **To a longest path in a DAG.** Build the [alignment graph](/alignment-graph/) of each block with $T$: one vertex per pair $(i, j)$ with $i \in B$, and the three usual edges with weights $\delta$ and $-\sigma$. For every pair $B' \prec B$, add edges from the vertices $(l(B'), j)$ to the first row of $B$, as in the recurrence. The graph is acyclic, because every edge moves forward in $G$ or in $T$. A best chain with its alignment is a [longest path](/dag-longest-path/) from a source to a sink. The graph has $O((L + b^2) m)$ edges, and adding one helper vertex per pair $(p, j)$ of a genome position and a target position, which collects the block ends before $p$, gives the faster version with $O((L + b) m + n m)$ edges.
- **From exon chaining.** Exon chaining is the special case in which each block is replaced by a single vertex of fixed weight and $T$ plays no part. The chain graph of [exon chaining](/exon-chaining/) has $2b$ vertices; the spliced alignment graph has one copy of it for each position of $T$.
- **To weighted interval scheduling.** Only through exon chaining; the spliced alignment problem itself does not reduce to it, because the score of a block depends on which part of $T$ it aligns with.
- **Related chaining problems.** [Colinear chaining](/colinear-chaining/) chains anchors that must be in order on both sequences. A spliced alignment also respects the order on both sequences, because the alignment is global, but it scores the letters, not fixed anchors.

## Applications

- **Gene prediction with a related protein.** The main use. Given a protein of a related species, the best chain gives the predicted exons of the gene in the new genome. Gelfand, Mironov and Pevzner report (a measurement, on the test set of their paper) that with a related protein as the target, 87 percent of the genes were predicted correctly, with an average correlation of 99 percent between the predicted and the true gene; with targets as distant as 160 PAM units, the average correlation was 95 percent.
- **Mapping full-length cDNAs and ESTs.** With a transcript of the same gene, the alignment is almost exact, and the exons are read from the chain. Here, faster tools first find seeds and then align only the regions they mark, but the exact problem is the same.
- **Genome annotation.** [Genome annotation](/genome-annotation/) pipelines align known proteins and transcripts to a new genome with spliced aligners and use the results as evidence for the gene models.
- **Checking a gene model.** If an *ab initio* prediction from a [generalized HMM](/generalized-hmm-gene-finder/) and a spliced alignment with a homolog disagree at one exon, that exon is a candidate for a manual check.

**Pitfalls in use.**
- **The mosaic effect.** With many short blocks, the best chain can piece the target together from short fragments of unrelated blocks, each of which matches a few letters. The score is high, but the gene is false. Filtering the blocks, adding intron penalties and requiring a minimum exon length reduce this.
- **Missing exons.** If a true exon is not in $\mathcal{B}$, no chain contains it, and the algorithm returns the best chain without it, often with a gap in the alignment where the exon should be.
- **Distant targets.** With a distant protein, short exons may not be similar enough to be placed, and the ends of the gene are the least reliable.
- **Ties.** Two different chains can have the same string or the same score, so the answer is not always unique. Report the score and, if needed, all chains that reach it.

## References
