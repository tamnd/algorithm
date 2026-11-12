---
tag: 33MJT0
kind: problem
slug: scaffolding
name: Scaffolding problem
aliases:
- scaffold construction
- contig scaffolding problem
area: biology/genome-assembly
level: core
summary: Order and orient contigs and estimate the gaps between them so that as many read-pair links as possible agree. The problem is NP-hard, so scaffolders use greedy and heuristic methods.
prereqs: [scaffold, np-complete]
see_also: [gap-filling, contig, paired-end-reads, repeat-resolution, reference-guided-assembly, maximum-cut, parameterized-bandwidth, n50]
sources:
  - paper: doi:10.1145/585265.585267
    title: Daniel H. Huson, Knut Reinert and Eugene W. Myers, The greedy path-merging algorithm for contig scaffolding, Journal of the ACM 49(5) (2002)
    locator: pp. 603 to 615, Section 2 (contig-mate-pair graph), Problem 3.1 and Theorem 3.2 (NP-complete by reduction from BANDWIDTH), Algorithm 5.1 and Theorem 5.3 (greedy path merging in O(mn + m^2) time)
  - paper: doi:10.1101/gr.1536204
    title: Mihai Pop, Daniel S. Kosack and Steven L. Salzberg, Hierarchical scaffolding with Bambus, Genome Research 14(1) (2004)
    locator: pp. 149 to 159
  - paper: doi:10.1093/bioinformatics/btq683
    title: Marten Boetzer, Christiaan V. Henkel, Hans J. Jansen, Derek Butler and Walter Pirovano, Scaffolding pre-assembled contigs using SSPACE, Bioinformatics 27(4) (2011)
    locator: pp. 578 to 579
  - paper: doi:10.1089/cmb.2011.0170
    title: Song Gao, Wing-Kin Sung and Niranjan Nagarajan, Opera, reconstructing optimal genomic scaffolds with high-throughput paired-end sequences, Journal of Computational Biology 18(11) (2011)
    locator: pp. 1681 to 1691
  - paper: doi:10.1073/pnas.171285098
    title: Pavel A. Pevzner, Haixu Tang and Michael S. Waterman, An Eulerian path approach to DNA fragment assembly, PNAS 98(17) (2001)
    locator: pp. 9748 to 9753 (EULER-SF combines 91 contigs into 60 scaffolds)
  - paper: doi:10.1126/science.287.5461.2196
    title: Eugene W. Myers and others, A whole-genome assembly of Drosophila, Science 287(5461) (2000)
    locator: pp. 2196 to 2204 (scaffolds from mate pairs of several insert sizes)
---

The scaffolding problem takes the [contigs](/contig/) of an assembly and a set of links between them, usually [read pairs](/paired-end-reads/) whose two reads land in different contigs, and asks for [scaffolds](/scaffold/): an order, a strand and a gap estimate for the contigs, such that as many links as possible agree with the layout. A link agrees if the two contigs have the strands it implies and the distance between its reads is close to the insert size of its library. Links from chimeric pairs and from reads in [repeats](/genome-repeat/) contradict each other, so the best layout must drop some. Huson, Reinert and Myers proved in 2002 that the decision form is NP-complete, by a reduction from BANDWIDTH, and gave a greedy path-merging algorithm. Real scaffolders, such as Bambus, SSPACE and Opera, are heuristics or exact methods for special cases.

## In plain words

After assembly you have many contigs and do not know their order. A read pair is two reads from the two ends of one DNA piece of known length. If one read lands in contig $A$ and the other in contig $B$, then $A$ and $B$ are near each other in the genome, you know which strand each one is on, and you know about how far apart they are.

Scaffolding puts the contigs in a row so that these clues fit. Most clues are true, but some are false: a pair from a repeat can land in a wrong copy, and some pairs join two random pieces. You cannot satisfy every clue, so you look for the layout that satisfies the most, and this search is hard.

## Definition

The input follows Huson, Reinert and Myers. Each contig $B_i$ has a length $l(B_i)$ and two end nodes. A **mate-edge** $e$ joins one end of $B_i$ to one end of $B_j$, with $i \ne j$, and has a mean length $m(e)$, a standard deviation $\sigma(e)$ and a weight $w(e)$, the number of pairs that support it. The contig edges and the mate-edges form the **contig-mate-pair graph** $G$.

An **ordering** of $G$ is a map $\varphi$ from the nodes to the integers such that the two ends of each contig are $l(B_i)$ apart, and no two contigs get the same pair of coordinates. It fixes the position and the strand of each contig. A mate-edge $e$ between the end $v$ of $B_i$ and the end $w$ of $B_j$ is **happy** if the two contigs have the strands the edge implies and

$$\big| \varphi(w) - \varphi(v) - m(e) \big| \le 3\sigma(e),$$

with $v$ the right end of $B_i$ and $w$ the left end of $B_j$ in the layout, or the same with the roles of $v$ and $w$ exchanged. Otherwise $e$ is unhappy.

**Contig scaffolding problem (Problem 3.1).** Given $G$, find an ordering $\varphi$ that maximizes the total weight of the happy mate-edges.

The output is read as a set of scaffolds: contigs whose layouts are joined by happy edges form one scaffold, in the order and with the strands of $\varphi$, and the gaps are the differences of the coordinates.

## Variants

- **By link type.** Paired ends and mate pairs with several insert sizes; long reads that span two contigs; Hi-C contacts, which say that two contigs are on the same chromosome and near each other, without a distance; optical or genetic maps; a related genome, as in [reference-guided assembly](/reference-guided-assembly/).
- **Orientation only.** Choose a strand for each contig to agree with the most links, and ignore order and distance.
- **Order only.** The strands are known, and only the order and the gaps are free.
- **Count discordant links.** Minimize the number of links that disagree with the scaffold, which is the same as maximizing the agreeing ones for a fixed input.
- **Linear or circular.** Bacterial chromosomes and plasmids are circular, so the last contig links to the first.

## Examples

**One false link.** Take contigs $A$, $B$, $C$ of lengths 1,000, 500 and 800, all on the forward strand, and three mate-edges, each with $\sigma = 50$:

| edge | from | to | mean gap $m$ | weight $w$ |
|---|---|---|---|---|
| $e_1$ | right end of $A$ | left end of $B$ | 200 | 5 |
| $e_2$ | right end of $B$ | left end of $C$ | 100 | 4 |
| $e_3$ | right end of $A$ | left end of $C$ | 300 | 2 |

The layout $A, B, C$ with gaps 200 and 100 makes $e_1$ and $e_2$ happy. The gap from $A$ to $C$ is then $200 + 500 + 100 = 800$, outside $300 \pm 150$, so $e_3$ is unhappy, and the happy weight is 9. The three edges cannot all be happy. If $e_1$ and $e_3$ are happy, $B$ ends 550 to 850 letters after the end of $A$, and $C$ starts 150 to 450 letters after it, so the gap from $B$ to $C$ is at most $450 - 550 = -100$, outside $100 \pm 150$. A layout with $e_3$ happy therefore has weight at most $2 + 5 = 7$. So $A, B, C$ is the best layout, and $e_3$ is the false link.

**The greedy algorithm on it.** Greedy path merging takes the edges in decreasing order of weight. It merges $A$ and $B$ along $e_1$, then $AB$ and $C$ along $e_2$. When it reaches $e_3$, both ends are already on the same path, so it makes no change. The result is the optimal layout.

**Strands from a cycle of links.** Three contigs with links "same strand" between $A$ and $B$, "same strand" between $B$ and $C$, and "opposite strands" between $A$ and $C$ cannot all agree: going around the cycle, the strand changes once. Any choice of strands breaks at least one link, so the best choice drops the lightest of the three.

## Known algorithms

- **Greedy path merging** (Huson, Reinert and Myers, Algorithm 5.1). Start with each contig as its own path. Take the mate-edges in decreasing order of weight. For an edge between two different paths, try to merge them guided by the edge, placing the contigs of one path between those of the other by their distances. Keep the merge if the happy weight it gains is at least the unhappy weight it adds. The running time is $O(mn + m^2)$ for $n$ contigs and $m$ mate-edges (Theorem 5.3). It has no approximation guarantee.
- **Hierarchical scaffolding** (Bambus, Pop, Kosack and Salzberg). Bundle the links between each pair of contig ends, and build scaffolds in stages, using the most reliable links first.
- **Greedy contig extension** (SSPACE, Boetzer and others). Map the read pairs to pre-assembled contigs and join the contigs greedily by the links with the most support.
- **Exact search** (Opera, Gao, Sung and Nagarajan). Search for the scaffold with the fewest discordant links. The search is exact, and its cost depends on a width parameter of the scaffold, so it is fast on the inputs where that width is small.
- **Bundling and transitive reduction.** Before the search, merge the parallel links that agree into one edge of higher weight, and delete a long link that a path of shorter links already explains. Huson, Reinert and Myers do both.

## Bounds

**NP-completeness (Huson, Reinert and Myers, Theorem 3.2).** The decision form, "is there an ordering with happy weight at least $W$", is NP-complete. A given ordering is checked edge by edge, so the problem is in NP. For hardness, take an instance of BANDWIDTH: a graph and a number $K$, asking for a numbering of the vertices by $1, \ldots, n$ such that each edge joins two vertices whose numbers differ by at most $K$. Make each vertex a contig of length 0, and each edge a mate-edge with weight 1, $m(e) = 1 + (K-1)/2$ and $\sigma(e) = (K-1)/6$, so that the happy range of distances is exactly $[1, K]$. Then all mate-edges can be happy if and only if the graph has bandwidth at most $K$. See [parameterized bandwidth](/parameterized-bandwidth/) for the BANDWIDTH problem.

**Orientation alone is NP-hard.** Give each contig a strand in $\{+, -\}$, and let each link require either equal or opposite strands, with a weight. If every link requires opposite strands, a choice of strands is a cut of the link graph, and a link agrees exactly when it crosses the cut. So the maximum agreeing weight is the [maximum cut](/maximum-cut/), which is NP-hard.

**Polynomial cases.** If the links contain no contradiction, the problem is easy. For strands, a breadth-first search fixes the strand of one contig per connected component and propagates it; it finds a contradiction exactly when a cycle of links has an odd number of "opposite" links, as in the example above. For positions, if the links form a tree, the same search fixes all coordinates up to a shift. The hardness comes only from choosing which conflicting links to drop.

## Reductions

- **From BANDWIDTH.** As in Theorem 3.2 above.
- **From [maximum cut](/maximum-cut/).** As in the orientation bound above.
- **To [gap filling](/gap-filling/).** Each gap of an output scaffold, with its length estimate, is an input of gap filling.
- **From [repeat resolution](/repeat-resolution/).** Repeats that the graph cannot resolve end contigs. Links that jump over a repeat give the order that the repeat hid, so scaffolding resolves repeats at the level of contigs without their sequence.

## Applications

Each genome project that starts with short reads scaffolds its contigs, because the contig N50 is limited by the longest unresolved repeats and the scaffold [N50](/n50/) is not. Mate-pair libraries with inserts of several kilobases were made for this purpose. EULER-SF combined 91 contigs of *N. meningitidis* into 60 scaffolds with clone-end pairs. The Celera whole-genome assembly of *Drosophila* used mate pairs of several insert sizes to build its scaffolds. Later projects add long reads, Hi-C or optical maps to reach chromosome-scale scaffolds.

## References
