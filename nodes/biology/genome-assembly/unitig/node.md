---
tag: S5AZ5M
kind: definition
slug: unitig
name: Unitig
aliases:
- unambiguous contig
- maximal non-branching path
area: biology/genome-assembly
level: core
summary: A maximal path of an assembly graph whose inner vertices have one way in and one way out. Each walk that enters it must run through it, so it is a safe contig.
prereqs: [contig, de-bruijn-graph, walk]
see_also: [de-bruijn-assembly, string-graph, overlap-graph, tip-removal, bubble-popping, genome-repeat, eulerian-path, genome-assembly-problem]
sources:
  - paper: doi:10.1126/science.287.5461.2196
    title: Eugene W. Myers and others, A whole-genome assembly of Drosophila, Science 287(5461) (2000)
    locator: pp. 2196 to 2204 (the Unitigger, unitigs as uncontested overlap paths, the A-statistic for unique unitigs)
  - paper: doi:10.1093/bioinformatics/bti1114
    title: Eugene W. Myers, The fragment assembly string graph, Bioinformatics 21(Suppl 2) (2005)
    locator: pp. ii79 to ii85 (chains of the string graph collapsed into composite edges)
  - paper: doi:10.1093/bioinformatics/btw279
    title: Rayan Chikhi, Antoine Limasset and Paul Medvedev, Compacting de Bruijn graphs from sequencing data quickly and in low memory, Bioinformatics 32(12) (2016)
    locator: pp. i201 to i208 (BCALM 2, the node-centric definition, minimizer partitions)
  - paper: doi:10.1093/bioinformatics/btw609
    title: Ilia Minkin, Son Pham and Paul Medvedev, TwoPaCo, an efficient algorithm to build the compacted de Bruijn graph from many complete genomes, Bioinformatics 33(24) (2017)
    locator: pp. 4024 to 4032
  - paper: doi:10.1089/cmb.2016.0141
    title: Alexandru I. Tomescu and Paul Medvedev, Safe and complete contig assembly through omnitigs, Journal of Computational Biology 24(6) (2017)
    locator: pp. 590 to 602 (unitigs are safe; omnitigs are the maximal safe walks)
---

A unitig is a maximal path in an assembly graph whose inner vertices each have exactly one edge in and one edge out. A walk that enters a unitig has no choice until it leaves at the far end, so the string of a unitig is a part of every genome that the graph allows. Unitigs are the contigs of the simplest [de Bruijn assembler](/de-bruijn-assembly/), and the graph that has one vertex for each unitig is the *compacted* de Bruijn graph. The word comes from the Celera assembler, where a unitig was a "uniquely assembled contig" in an overlap graph.

## Definition

Let $H$ be a directed graph. Multiple edges and loops are allowed. A vertex $v$ is **simple** if its in-degree and its out-degree are both 1.

**Edge-centric unitig.** This is the definition for the de Bruijn graph of order $k$ with the $(k-1)$-mers as vertices and the $k$-mers as edges. A **unitig** is a [walk](/walk/) $e_1 e_2 \cdots e_m$, with $m \ge 1$, such that

1. for each $i < m$, the head of $e_i$ is a simple vertex and is the tail of $e_{i+1}$, and
2. the walk cannot be made longer under rule 1: the tail of $e_1$ is not simple and the head of $e_m$ is not simple, or else the walk is a cycle that is a whole connected component of $H$ and all its vertices are simple.

**Node-centric unitig.** This is the definition used by BCALM 2, where the vertices are the $k$-mers and an edge joins $x$ to $y$ when the last $k - 1$ letters of $x$ are the first $k - 1$ letters of $y$. A **unitig** is a path $v_1 v_2 \cdots v_m$ such that, for each $i < m$, the vertex $v_i$ has out-degree 1 and $v_{i+1}$ has in-degree 1, and that cannot be made longer at either end under the same rule.

In both cases the **string of a unitig** is the first $k$-mer followed by the last letter of each later $k$-mer. A unitig of $m$ edges in the edge-centric graph spells a string of length $m + k - 1$.

**Partition.** Each edge (in the edge-centric case) or each vertex (in the node-centric case) lies in exactly one unitig. The reason: under the rule "$e$ is followed by $f$ if they meet at a simple vertex", each edge has at most one successor and at most one predecessor. So the edges fall into disjoint chains and cycles, and these are the unitigs. The proof is on the [de Bruijn assembly](/de-bruijn-assembly/) page.

**The two definitions agree on a full de Bruijn graph.** Let $e$ and $f$ be $k$-mers with $e[2 \ldots k] = f[1 \ldots k-1] = v$. In the edge-centric graph, $v$ is simple if and only if $f$ is the only kept $k$-mer that starts with $v$ and $e$ is the only one that ends with $v$. In the node-centric graph, these two facts say that $e$ has out-degree 1 and $f$ has in-degree 1. So the same consecutive pairs are joined, and the unitigs spell the same strings. The two definitions differ on graphs whose edges are not all the $(k-1)$-overlaps, such as overlap graphs with variable overlaps.

**The overlap graph definition.** In the Celera assembler (Myers and others, 2000), the Unitigger joined reads along overlaps that no other overlap contradicts, so that the reads in a unitig form an unbranched chain. A coverage test, the A-statistic, then marks a unitig as unique when its read density fits one copy, and as a likely repeat when the density is too high. In the [string graph](/string-graph/) (Myers, 2005), the chains of simple vertices are collapsed into composite edges, which are unitigs in the edge-centric sense.

**Safety.** Assume that the genome is circular and that its walk uses every edge of the graph. Then the walk passes through each unitig from start to end, so the string of each unitig is a substring of the genome. Tomescu and Medvedev (2017) call such a string *safe*. For a linear genome the same holds when the first and the last $(k-1)$-mer of the genome occur only once in it.

**Construction.** Given the $m$ kept $k$-mers in a hash table, a pass that starts at each non-simple vertex and follows the simple vertices finds all unitigs in $O(km)$ expected time. BCALM 2 (Chikhi, Limasset and Medvedev, 2016) builds them from a large $k$-mer set in low memory: it splits the $k$-mers into buckets by minimizer, compacts each bucket on its own, and joins the parts in a second step. TwoPaCo (Minkin, Pham and Medvedev, 2017) builds them from many complete genomes: it finds the junction positions with a Bloom filter in a first pass and confirms them in a second pass.

## Examples and non-examples

**One repeat-free genome.** For $S = \mathtt{GATGCATACGCCTTTA}$ and $k = 4$, no 3-mer occurs twice. The graph is one path of 13 edges, so it has one unitig, and its string is $S$.

**A triple repeat.** For $S = \mathtt{CCGTAAGTATTGTAG}$ and $k = 4$, the 3-mer $\mathtt{GTA}$ occurs three times, so it is a vertex with in-degree 3 and out-degree 3. The source $\mathtt{CCG}$ and the sink $\mathtt{TAG}$ are not simple either. The unitigs are

| unitig | edges | from | to |
|---|---|---|---|
| CCGTA | 2 | CCG | GTA |
| GTAAGTA | 4 | GTA | GTA |
| GTATTGTA | 5 | GTA | GTA |
| GTAG | 1 | GTA | TAG |

They hold $2 + 4 + 5 + 1 = 12$ edges, which are all 12 distinct 4-mers of $S$. The node-centric definition gives the same four strings.

**Non-example: a path that crosses a branch.** In the same graph, the walk $\mathtt{CCGTAAGTA}$ (6 edges) crosses the vertex $\mathtt{GTA}$, which has three edges out. Another genome with the same 4-mers, $\mathtt{CCGTATTGTAAGTAG}$, does not contain $\mathtt{CCGTAAGTA}$. So the walk is not a unitig and its string is not safe.

**Non-example: a path that is too short.** The walk $\mathtt{CCGT}$ of one edge has a simple head, $\mathtt{CGT}$. It can be made longer, so it is not a unitig. It is a part of the unitig $\mathtt{CCGTA}$.

**A unitig that is not a substring of a linear genome.** For $S = \mathtt{AABABAA}$ and $k = 3$, the vertex $\mathtt{AA}$ is simple, and the unitig $\mathtt{BAA}, \mathtt{AAB}$ spells $\mathtt{BAAB}$. This string is not in $S$. The genome walk starts at $\mathtt{AA}$, in the middle of the unitig, so it never runs through the whole unitig.

**An isolated cycle.** The 3-mers $\mathtt{AAC}, \mathtt{ACG}, \mathtt{CGT}, \mathtt{GTA}, \mathtt{TAA}$ of the circular genome $\mathtt{AACGT}$ form one cycle of five simple vertices. The whole cycle is one unitig, and no vertex is a natural start.

## Related definitions

- **[Contig](/contig/).** The general word for an assembled gap-free sequence. A unitig is the most conservative kind of contig; omnitigs are longer contigs that are still safe.
- **[de Bruijn graph](/de-bruijn-graph/).** The graph on which edge-centric and node-centric unitigs are defined. Its compacted form has one vertex or edge for each unitig.
- **[Overlap graph](/overlap-graph/) and [string graph](/string-graph/).** The read-based graphs in which the Celera unitig and the composite edge are defined.
- **[Genome repeat](/genome-repeat/).** A repeat of length at least $k - 1$ makes a vertex with more than one edge in or out. So it ends unitigs.
- **[Tip](/tip-removal/) and [bubble](/bubble-popping/).** Read errors make branch points, which cut true unitigs into short ones. Simplification removes them, and the unitigs of the simplified graph are longer.
- **Compacted de Bruijn graph.** The graph whose vertices (node-centric) or edges (edge-centric) are the unitigs. It is the input of most later steps of a de Bruijn assembler.

## References
