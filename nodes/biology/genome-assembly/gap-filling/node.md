---
tag: X8BX3K
kind: problem
slug: gap-filling
name: Gap filling
aliases:
- gap closing
- scaffold gap closure
area: biology/genome-assembly
level: core
summary: Replace the run of N between two adjacent contigs of a scaffold by sequence that the reads support and whose length matches the gap estimate. With a length constraint it is NP-hard in general.
prereqs: [scaffolding, de-bruijn-graph]
see_also: [scaffold, contig, paired-end-reads, read-mapping, subset-sum-problem, repeat-resolution, de-bruijn-assembly, kmer]
sources:
  - paper: doi:10.1186/gb-2012-13-6-r56
    title: Marten Boetzer and Walter Pirovano, Toward almost closed genomes with GapFiller, Genome Biology 13(6) R56 (2012)
    locator: Background (SOAPdenovo gap closure and IMAGE use local de Bruijn assembly without the gap size) and Materials and methods (parameters t, k, o, r, n, d and i)
  - paper: doi:10.1186/gb-2010-11-4-r41
    title: Isheng J. Tsai, Thomas D. Otto and Matthew Berriman, Improving draft assemblies by iterative mapping and assembly of short reads to eliminate gaps, Genome Biology 11(4) R41 (2010)
    locator: the IMAGE method
  - paper: doi:10.1186/2047-217X-1-18
    title: Ruibang Luo and others, SOAPdenovo2, an empirically improved memory-efficient short-read de novo assembler, GigaScience 1 18 (2012)
    locator: the GapCloser step
  - paper: doi:10.1089/cmb.2015.0197
    title: Leena Salmela, Kristoffer Sahlin, Veli Makinen and Alexandru I. Tomescu, Gap filling as exact path length problem, Journal of Computational Biology 23(5) (2016)
    locator: pp. 347 to 361 (the exact path length problem, its NP-hardness, and the dynamic programming algorithm of Gap2Seq)
  - paper: doi:10.1145/585265.585267
    title: Daniel H. Huson, Knut Reinert and Eugene W. Myers, The greedy path-merging algorithm for contig scaffolding, Journal of the ACM 49(5) (2002)
    locator: Algorithm 7.1 (contig extension and gap filling)
---

Gap filling, also called gap closing, replaces the gaps of a [scaffold](/scaffold/) by sequence. After [scaffolding](/scaffolding/), two adjacent contigs are known to be about $d$ letters apart, and the letters between them are written as $\mathtt{N}$. The gaps are usually repeats or regions with low coverage, so the first assembly could not cross them. Gap filling uses the read pairs that have one read on a contig next to the gap, and the reads of the whole data set, to build the missing sequence. GapFiller (Boetzer and Pirovano, 2012) extends the two contig ends letter by letter and accepts a closure only if its length matches the gap estimate. The local assembly in SOAPdenovo's gap closure and in IMAGE does not use the estimate. Gap2Seq (Salmela and others, 2016) states the problem as finding a path of a given length in a de Bruijn graph, which is NP-hard in general and solvable by dynamic programming in time proportional to the gap length.

## In plain words

A scaffold has two contigs with a hole of about 900 letters between them. You know the end of the left contig and the start of the right contig. Some read pairs have one read on the left contig and the other read in the hole. You collect those reads and use them to grow the left contig to the right, one letter at a time, and the right contig to the left. When the two growing ends meet, you have a candidate for the hole.

The candidate must also have about the right length. If the hole contains a repeat, the reads may also suggest a shortcut through another copy of the repeat, and its length is wrong. So the length estimate helps you reject false closures.

## Definition

**Gap filling.** Given a scaffold gap between the contig ends $A$ and $B$ with an estimated length $d$ and a tolerance $\delta$, and a set of reads, find a string $X$ such that $A X B$ is supported by the reads and $d - \delta \le |X| \le d + \delta$, or report that there is none.

**Exact path length problem.** A precise form uses the [de Bruijn graph](/de-bruijn-graph/) $H$ of the reads. Let $s$ be the last $k$-mer of $A$, $t$ the first $k$-mer of $B$, and give each edge $e$ of $H$ a length $\ell(e) \ge 1$, the number of letters it adds. Given the interval $[d - \delta, d + \delta]$, find a walk from $s$ to $t$ whose total length lies in the interval. In the graph with one $k$-mer per vertex, each edge adds one letter, and a walk of $j$ edges from $s$ to $t$ gives a gap of $j - k$ letters. In a compressed graph, each edge is a [unitig](/unitig/) and adds as many letters as the unitig is long.

Each solution is a candidate. If several walks fit, the reads do not determine the gap, and a careful method fills only the part that all candidates share, or leaves the gap open.

## Variants

- **With or without the length.** GapFiller and Gap2Seq use the gap estimate. SOAPdenovo's gap closure and IMAGE run a local assembly and fill the gap with what they find.
- **Local or global reads.** GapFiller uses only the read pairs whose second read falls in the gap. Gap2Seq searches the de Bruijn graph of all reads.
- **Partial filling.** Extend each contig end into the gap as far as the reads allow, and leave a shorter gap when the two ends do not meet.
- **Long reads.** Align long reads that span the gap to both contig ends, and fill the gap with their consensus.
- **Gaps from a negative estimate.** If the estimate is below zero, the contigs probably overlap, and the step is an alignment of the two ends, not a search.

## Examples

**Length rejects a shortcut.** Let the compressed graph between $s$ and $t$ have these edges, with the number of letters each adds:

| edge | $s \to a$ | $a \to t$ | $s \to b$ | $b \to c$ | $c \to b$ | $c \to t$ |
|---|---|---|---|---|---|---|
| $\ell$ | 4 | 3 | 5 | 4 | 2 | 3 |

The walks from $s$ to $t$ have the lengths $4 + 3 = 7$, $5 + 4 + 3 = 12$, $5 + 4 + 2 + 4 + 3 = 18$, and so on, adding 6 for each extra turn of the cycle through $b$ and $c$. With $d = 12$ and $\delta = 3$, only the walk $s\,b\,c\,t$ of length 12 lies in $[9, 15]$. A method that ignores the length could choose the shorter walk through $a$.

**The dynamic program on it.** Let $R(v)$ be the set of lengths $\le 15$ of walks from $s$ to $v$. Then $R(s) = \{0\}$, $R(a) = \{4\}$, $R(b) = \{5, 11\}$, $R(c) = \{9, 15\}$ and $R(t) = \{7, 12\}$. The set $R(t)$ meets $[9, 15]$ only at 12, so the answer is unique. Keeping a predecessor for each pair (vertex, length) gives the walk.

**GapFiller settings.** By default GapFiller trims 10 letters from each contig end next to a gap (parameter $t$), because ends often hold misassemblies. It splits the reads in the gap into $k$-mers of length 30, which extend a contig end by one letter when they overlap it in 29 letters. It adds a letter only if at least 2 reads support it (parameter $o$), and, if reads disagree, only if one letter has a ratio of at least 0.7 (parameter $r$). A gap counts as closed only if the two extensions overlap in at least 10 letters (parameter $n$) and the length differs from the estimate by at most 50 (parameter $d$). The whole process can be repeated up to 10 times (parameter $i$).

## Known algorithms

- **Iterative extension with a length check** (GapFiller). Map the read pairs to the scaffold with Bowtie or BWA, keep the pairs with one read mapped and the other read expected in a gap, and extend both contig ends with the $k$-mers of those reads by majority vote. Accept a closure only if the ends overlap and the length matches the estimate.
- **Iterative mapping and local assembly** (IMAGE, Tsai, Otto and Berriman). Map the reads, assemble the unmapped mates near each contig end, extend the contigs with the result, and repeat.
- **Local de Bruijn assembly** (the GapCloser step of SOAPdenovo). Assemble the reads that belong to a gap and fill the gap with the result.
- **Exact path length by dynamic programming** (Gap2Seq). Compute, for each vertex $v$ and each length $\lambda \le d + \delta$, whether a walk from $s$ to $v$ of length $\lambda$ exists. With positive integer lengths, the value for $(v, \lambda)$ depends only on the values for $(u, \lambda - \ell(u, v))$, so the table fills in increasing order of $\lambda$. The time is $O((d + \delta)\, m)$ for $m$ edges.
- **Contig extension in scaffolding** (Huson, Reinert and Myers, Algorithm 7.1). Use the fragments whose mates are on a contig to extend contigs and to fill gaps after the scaffold is fixed.

## Bounds

**Theorem (pseudo-polynomial time).** If each edge length is a positive integer, the exact path length problem can be solved in time $O(D \cdot m)$ and space $O(D \cdot n)$, where $D = d + \delta$, $n$ is the number of vertices and $m$ the number of edges.

*Proof.* Let $R(v, \lambda)$ be true if some walk from $s$ to $v$ has length exactly $\lambda$. Then $R(s, 0)$ is true, $R(v, 0)$ is false for $v \ne s$, and for $\lambda \ge 1$, $R(v, \lambda)$ is true if and only if some edge $(u, v)$ has $\ell(u, v) \le \lambda$ and $R(u, \lambda - \ell(u, v))$ is true. This holds because the last edge of a walk of length $\lambda \ge 1$ ends at $v$ and the rest is a walk of length $\lambda - \ell(u, v) < \lambda$. Each entry for one $\lambda$ uses only smaller lengths, so computing the entries for $\lambda = 0, 1, \ldots, D$ in order is correct. Each length looks at each edge once, which gives $O(D \cdot m)$ time, and the table has $(D + 1)\, n$ entries. The answer is yes if and only if $R(t, \lambda)$ is true for some $\lambda$ in $[d - \delta, D]$. $\square$

The bound is polynomial in the value $D$, not in its number of digits. In the graph with one $k$-mer per vertex, all lengths are 1 and $D$ is bounded by the insert size, so the algorithm is polynomial in the input there.

**Theorem (NP-hardness with lengths in binary).** The exact path length problem is NP-hard when edge lengths are written in binary, as in a compressed graph with long unitigs.

*Proof.* Reduce from [subset sum](/subset-sum-problem/): given positive integers $a_1, \ldots, a_n$ and a target $T$, is there a subset with sum $T$? Build the vertices $v_0, \ldots, v_n$, and for each $i$ two parallel edges from $v_{i-1}$ to $v_i$, of lengths $a_i + 1$ and 1. The graph has no cycle, so each walk from $s = v_0$ to $t = v_n$ uses exactly one of the two edges for each $i$, and its length is $n$ plus the sum of the $a_i$ whose long edge it uses. So a walk of length exactly $T + n$ exists if and only if some subset sums to $T$. Take $d = T + n$ and $\delta = 0$. The construction has size polynomial in the input. $\square$

**What the reads cannot decide.** If the gap holds a tandem repeat, or two walks of lengths within $\delta$ of each other, the length check does not separate them. This is the same limit as in [repeat resolution](/repeat-resolution/): without a read or pair that spans the ambiguous part, no method can choose.

## Reductions

- **From [subset sum](/subset-sum-problem/).** As in the hardness theorem.
- **To reachability in a layered graph.** The table $R$ is reachability in the graph whose vertices are the pairs $(v, \lambda)$, with an arc from $(u, \lambda)$ to $(v, \lambda + \ell(u, v))$. A [breadth-first search](/breadth-first-search/) over it solves the problem.
- **From scaffolding.** The input is the output of [scaffolding](/scaffolding/): the pairs of adjacent contigs, their gap estimates and the read pairs that map near them.

## Applications

Draft genomes submitted to public databases often keep many gaps, and the missing regions can contain genes. Boetzer and Pirovano report that GapFiller closes most gaps of bacterial draft assemblies with fewer errors than IMAGE and the SOAPdenovo gap closure, and that the length check discards closures that are too short or too long. Gap filling is the last automatic step before finishing with targeted sequencing, and it is also used to improve old assemblies with new short or long reads.

## References
