---
tag: NTEQC6
kind: problem
slug: sequence-to-graph-alignment
name: Sequence-to-graph alignment
aliases:
- pangenome alignment
- string matching in labeled graphs
area: biology/sequence-alignment
level: research
summary: Find a path in a graph with letters on its nodes whose string is closest to a query. On a DAG this takes O((|V|+|E|)m) time; cycles need more care; edits to the graph make it NP-complete.
prereqs: [edit-distance, topological-sort]
see_also: [partial-order-alignment, read-mapping, whole-genome-alignment, dijkstra, dag-shortest-paths, edit-distance-hardness, sellers-algorithm, de-bruijn-graph]
sources:
  - paper: doi:10.1093/bioinformatics/18.3.452
    title: Christopher Lee, Catherine Grasso and Mark F. Sharlow, Multiple sequence alignment using partial order graphs, Bioinformatics 18(3), 2002
    locator: pages 452 to 464, the dynamic programming of a sequence against a partial order graph
  - paper: doi:10.1016/S0304-3975(99)00333-3
    title: Gonzalo Navarro, Improved approximate pattern matching on hypertext, Theoretical Computer Science 237(1-2), 2000
    locator: pages 455 to 463, approximate matching on a general graph with errors in the pattern only
  - paper: "Amihood Amir, Moshe Lewenstein and Noa Lewenstein, Pattern matching in hypertext, Journal of Algorithms 35(1), 2000, pages 82 to 99"
    locator: the hypertext model and the hardness of allowing errors in the hypertext
  - paper: doi:10.1101/216127
    title: Mikko Rautiainen and Tobias Marschall, Aligning sequences to general graphs in O(V + mE) time, bioRxiv preprint, 2017
    locator: the dynamic program over a cyclic graph and its row-by-row computation
  - paper: doi:10.1089/cmb.2019.0066
    title: Chirag Jain, Haowen Zhang, Yu Gao and Srinivas Aluru, On the complexity of sequence-to-graph alignment, Journal of Computational Biology 27(4), 2020
    locator: pages 640 to 654, NP-completeness when the graph labels may change, and the O(|V| + m|E|) algorithm when only the query changes
  - paper: doi:10.4230/LIPIcs.ICALP.2019.55
    title: Massimo Equi, Roberto Grossi, Veli Mäkinen and Alexandru I. Tomescu, On the complexity of string matching for graphs, ICALP 2019, LIPIcs 132
    locator: article 55, the conditional lower bound for exact matching in labeled graphs under the strong exponential time hypothesis
  - paper: doi:10.1038/nbt.4227
    title: Erik Garrison, Jouni Sirén, Adam M. Novak and colleagues, Variation graph toolkit improves read mapping by representing genetic variation in the reference, Nature Biotechnology 36(9), 2018
    locator: pages 875 to 879, read mapping to a variation graph with the vg toolkit
---

Sequence-to-graph alignment is the problem of aligning a query string, such as a sequencing read, to a graph whose nodes carry letters, so that the query is matched to the string spelled by some path of the graph. A *genome graph* or *variation graph* stores a reference genome together with known variants as alternative paths, so it can represent a whole population, a pangenome, in one structure. Aligning a read to it, instead of to one linear reference, removes the bias against reads that carry non-reference alleles. When the graph is a directed acyclic graph (DAG), the classical [edit distance](/edit-distance/) table generalizes directly and takes $O((|V| + |E|)\,m)$ time for a query of length $m$. Graphs with cycles, such as [de Bruijn graphs](/de-bruijn-graph/) and graphs of repeats, need a shortest-path step in each row, and the problem becomes NP-complete if the letters of the graph may also be changed.

## In plain words

A reference genome is one long text. But people differ: at some places, some people have a different letter, or an extra or missing piece. A genome graph stores all these versions at once. Where people agree there is a single path, and where they differ the graph splits into two or more branches that join again.

To place a read in such a graph, we look for a walk through the graph whose letters are as close as possible to the read. A read that carries a rare version of a gene then matches its own branch exactly, while against the one-text reference it would show false differences.

## Definition

**Input.** A directed graph $G = (V, E)$ with a letter $\ell(v)$ on each node $v$, and a query $q$ of length $m$. A path $v_1 \ldots v_k$ spells the string $\ell(v_1) \cdots \ell(v_k)$.

**Output.** A path $P$ of $G$, which may start and end at any node, that minimizes the edit distance between $q$ and the string of $P$, together with that distance and an alignment.

Changes are allowed in the query only: the alignment may mismatch, insert or delete letters relative to the path, but the path itself must exist in the graph. Graphs with strings on the nodes, as built by most tools, reduce to this form by splitting each string into a chain of one-letter nodes.

**The dynamic program.** Let $C[i][v]$ be the least cost of aligning $q[1 \ldots i]$ to a path that ends at $v$, with $\ell(v)$ as the last letter of the path. Then, with $C[0][v] = 1$ and a path allowed to start at $v$,

$$C[i][v] = \min\Big( \min_{u \to v} C[i-1][u] + \delta_{i,v},\ \ (i - 1) + \delta_{i,v},\ \ C[i-1][v] + 1,\ \ \min_{u \to v} C[i][u] + 1 \Big),$$

where $\delta_{i,v}$ is 0 if $q[i] = \ell(v)$ and 1 otherwise. The four terms are a match or mismatch after a predecessor, a match or mismatch at the start of the path, an inserted letter of the query, and a deleted letter of the graph. The answer is $\min_v C[m][v]$. On a linear graph this is [Sellers' algorithm](/sellers-algorithm/).

## Variants

- **Acyclic graphs.** Variation graphs built from a reference and a set of small variants are DAGs. The last term of the recurrence refers only to predecessors, which come earlier in a [topological order](/topological-sort/), so each row is one pass. This is the alignment step of [partial order alignment](/partial-order-alignment/).
- **Graphs with cycles.** In a cyclic graph the last term creates dependencies along cycles inside one row. Each row is then a single-source shortest path problem with unit edge costs and many sources, solved with a bucket queue or [Dijkstra's algorithm](/dijkstra/).
- **Changes in the graph.** If the letters of the graph may also change, the problem is NP-complete (Jain et al., 2020), as is the related hypertext problem studied by Amir, Lewenstein and Lewenstein (2000).
- **Exact and Hamming matching.** The query must spell a path exactly, or with substitutions only. Even exact matching has a conditional quadratic lower bound (see Bounds).
- **Local, affine and banded scores.** The same recurrence takes [Smith-Waterman](/smith-waterman/) local scores and affine gap costs, with three tables instead of one.
- **Both strands and haplotypes.** Genome graphs are often bidirected, so a path may cross a node on either strand. Some tools also restrict the paths to those seen in known haplotypes.

## Examples

Take a reference ACGTTGCA with two known variants: a T/C substitution at the fourth base and a deletion of the C at the seventh base. The graph has nine nodes:

| node | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| letter | A | C | G | T | C | T | G | C | A |

with the edges $0 \to 1 \to 2$, $2 \to 3$, $2 \to 4$, $3 \to 5$, $4 \to 5$, $5 \to 6$, $6 \to 7 \to 8$ and $6 \to 8$. Node 4 is the alternative allele, and the edge $6 \to 8$ skips the deleted C. The graph spells four strings: ACGTTGCA, ACGCTGCA, ACGTTGA and ACGCTGA.

For the query $q = \texttt{ACGCTGA}$, the last row of the dynamic program is

| node | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $C[7][v]$ | 6 | 5 | 4 | 3 | 3 | 2 | 1 | 1 | 0 |

so the best path ends at node 8 with cost 0: it is $0, 1, 2, 4, 5, 6, 8$, which takes both variants. Against the linear reference ACGTTGCA the same read has edit distance 2. For the query ACGATGA, which has a new allele A at the variant site, the best cost is 1, a single mismatch.

**A cycle.** The graph with nodes G, C, A, T and edges $\texttt{G} \to \texttt{C} \to \texttt{A} \to \texttt{T}$ and $\texttt{A} \to \texttt{C}$ spells $\texttt{G}(\texttt{CA})^k\texttt{T}$ for every $k \ge 1$, a tandem repeat of any copy number. The query GCACACAT aligns to it with cost 0 by going round the cycle three times. A DAG would need a separate path for each copy number.

## Known algorithms

| setting | time | source |
|---|---|---|
| DAG, edits in the query | $O((\lvert V \rvert + \lvert E \rvert)\,m)$ | partial order alignment, Lee, Grasso and Sharlow (2002) |
| general graph, edits in the query | $O(m(\lvert V \rvert + \lvert E \rvert))$ | Navarro (2000) |
| general graph, edits in the query | $O(\lvert V \rvert + m \lvert E \rvert)$ | Rautiainen and Marschall (2017); Jain et al. (2020) |
| edits also in the graph | NP-complete | Jain et al. (2020) |

Navarro's algorithm was stated for hypertext, a graph with text on its nodes, and handles cycles without unrolling them. Rautiainen and Marschall gave the $O(|V| + m|E|)$ bound for alignment to general graphs, and their work is the basis of the tool GraphAligner. Practical read mappers such as vg (Garrison and colleagues, 2018) first find seeds in an index of the graph, then align only the subgraph around them, as linear mappers do with [seed-and-extend](/seed-and-extend/).

## Bounds

- The table has $m |V|$ cells and each edge is used once per row, so $\Omega(m|E|)$ is the natural cost of the dynamic program, and the algorithms above match it.
- On a linear graph the problem contains edit distance, which has no $O(n^{2-\varepsilon})$ algorithm unless the strong exponential time hypothesis (SETH) fails ([edit distance hardness](/edit-distance-hardness/)).
- Equi, Grossi, Mäkinen and Tomescu (2019) showed that even exact matching of a string in a labeled graph has no $O(m^{1-\varepsilon}|E|)$ or $O(m|E|^{1-\varepsilon})$ algorithm unless SETH fails. So, unlike strings, graphs do not allow linear-time exact matching in general.
- When the graph letters may change, the problem is NP-complete, so no polynomial algorithm is expected.

## Reductions

- **From approximate string matching.** A path graph that spells a text $T$ turns the problem into finding the best substring of $T$ for $q$, which is [Sellers' algorithm](/sellers-algorithm/).
- **To shortest paths.** Build the alignment graph with a node $(i, v)$ for each row $i$ and graph node $v$, and edges of cost 0 or 1 for the four moves. An optimal alignment is a shortest path from row 0 to row $m$. On a DAG this is a [DAG shortest path](/dag-shortest-paths/); with cycles it needs [Dijkstra's algorithm](/dijkstra/) or a bucket queue.
- **From multiple alignment.** Aligning a new sequence to the graph of a partial multiple alignment is the core step of [partial order alignment](/partial-order-alignment/).
- **From SAT, under SETH.** The lower bounds above come from reductions of orthogonal vectors to matching in a labeled graph.

## Applications

- Read mapping to pangenome graphs, which lowers reference bias in variant calling, as in [read mapping](/read-mapping/) with vg.
- Genotyping known structural variants by aligning reads to a graph that contains them.
- Error correction of long reads by aligning them to a de Bruijn graph built from short reads.
- Building multiple alignments and consensus sequences with [partial order alignment](/partial-order-alignment/).
- Adding new genomes to a pangenome graph after a [whole-genome alignment](/whole-genome-alignment/).

## References
