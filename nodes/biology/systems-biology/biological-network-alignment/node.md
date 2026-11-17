---
tag: 77QF98
kind: problem
slug: biological-network-alignment
name: Biological network alignment
aliases:
- protein interaction network alignment
area: biology/systems-biology
level: advanced
summary: "Map the proteins of one interaction network to another so that both sequence similarity and conserved interactions are high. NP-hard; solved by heuristics such as IsoRank."
prereqs: [needleman-wunsch, subgraph-isomorphism, maximum-weight-matching]
see_also: [isorank, maximum-common-subgraph, quadratic-assignment-problem, graph-isomorphism-problem, multiple-sequence-alignment, blast, clique-problem, graph-edit-distance]
sources:
  - paper: doi:10.1038/nbt1196
    title: Roded Sharan and Trey Ideker, Modeling cellular machinery through biological network comparison, Nature Biotechnology 24(4), 427-433, 2006
    locator: the review of network alignment, the difference between local and global alignment, and the applications
  - paper: doi:10.1073/pnas.1534710100
    title: Brian P. Kelley, Roded Sharan, Richard M. Karp, Taylor Sittler, David E. Root, Brent R. Stockwell and Trey Ideker, Conserved pathways within bacteria and yeast as revealed by global protein network alignment, PNAS 100(20), 11394-11399, 2003
    locator: PathBLAST, the search for conserved paths in the network of protein pairs
  - paper: doi:10.1073/pnas.0806627105
    title: Rohit Singh, Jinbo Xu and Bonnie Berger, Global alignment of multiple protein interaction networks with application to functional orthology detection, PNAS 105(35), 12763-12768, 2008
    locator: the global alignment problem with a weight between sequence and topology, and the IsoRank method
  - paper: doi:10.1098/rsif.2010.0063
    title: Oleksii Kuchaiev, Tijana Milenković, Vesna Memišević, Wayne Hayes and Nataša Pržulj, Topological network alignment uncovers biological function and phylogeny, Journal of the Royal Society Interface 7(50), 1341-1354, 2010
    locator: GRAAL, alignment by graphlet degree signatures, and the edge correctness measure
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: the entry for subgraph isomorphism in the list of NP-complete problems
---

Biological network alignment compares the protein interaction networks of two or more species. It asks for a map between their proteins under which matched proteins have similar sequences and many interactions in one network are also present, between the matched proteins, in the other. A good alignment transfers knowledge: a protein of unknown function inherits a guess from its partner, and conserved groups of interactions point to protein complexes and pathways that evolution kept. The problem is [NP-hard](/np-hard/), because with the sequence part removed it contains [subgraph isomorphism](/subgraph-isomorphism/). So the methods in use, such as [IsoRank](/isorank/), are heuristics, and they are compared by measured scores. This page is about the optimization problem; IsoRank is one algorithm for it, and [graph isomorphism](/graph-isomorphism-problem/) is the exact, all or nothing version without sequences.

## In plain words

Two species have many proteins with a common ancestor. In each species, we know which proteins touch each other, which gives two networks. We want to pair each protein of the first species with one of the second, so that paired proteins look alike in sequence and so that, when two proteins touch in the first species, their partners also touch in the second.

These two wishes can disagree, and the second one is a puzzle of the kind that is hard to solve exactly for large networks. Methods therefore mix the two wishes into one score and look for a good, not a perfect, pairing.

## Definition

**Input.** Two undirected graphs $G_1 = (V_1, E_1)$ and $G_2 = (V_2, E_2)$, with $|V_1| = n_1 \le n_2 = |V_2|$; a node similarity $s : V_1 \times V_2 \to \mathbb{R}_{\ge 0}$, usually from [BLAST](/blast/) scores of the protein sequences; and a weight $\alpha \in [0, 1]$.

**Global pairwise alignment.** Find a one to one map $f$ from $V_1$ into $V_2$ that maximizes

$$\mathrm{score}(f) = \alpha \cdot \mathrm{EC}(f) + (1 - \alpha) \cdot \mathrm{S}(f),$$

where $\mathrm{EC}(f) = |\{\{u, v\} \in E_1 : \{f(u), f(v)\} \in E_2\}|$ counts the conserved edges and $\mathrm{S}(f) = \sum_{u \in V_1} s(u, f(u))$ is the total similarity. Many variants allow $f$ to be partial, so that a protein can stay unmatched. The values of the two terms are often scaled before they are mixed, and each method fixes its own scaling.

**Local alignment.** Find small connected subnetworks, one in each graph, with a map between them that conserves many edges and matches similar proteins. Several local alignments can overlap, and the map can be many to many.

**Multiple alignment.** For $k \ge 3$ networks, find groups of proteins, at most one per species or more, such that groups are similar and the interactions between groups are conserved across species.

**Quality measures.** The *edge correctness* $\mathrm{EC}(f) / |E_1|$ is the fraction of edges of $G_1$ that are conserved. When the true correspondence is known, as in tests on a network and a perturbed copy of it, the *node correctness* is the fraction of nodes mapped correctly. On real data, alignments are also scored by how often matched proteins share functional annotations.

## Variants

- **Topology only or with sequence.** $\alpha = 1$ uses the graphs only, as in GRAAL; $\alpha = 0$ ignores the graphs.
- **Global or local.** A global map covers all of $V_1$; a local alignment covers a few conserved regions.
- **Pairwise or multiple.** Two networks or $k$ networks.
- **Induced or not.** Some scores also penalize edges of $G_2$ between matched nodes that have no counterpart in $G_1$.
- **Directed and weighted networks.** The same scheme applies to [gene regulatory networks](/gene-regulatory-network/), metabolic networks, and networks with confidence weights on the edges.

## Examples

**A path against a star.** Let $G_1$ be the path $a - b - c$ and $G_2$ the star with center $x$ and leaves $y, z, w$, with $\alpha = 1$. A map that sends the middle node $b$ to the center $x$, and $a$ and $c$ to two leaves, conserves both edges, so $\mathrm{EC}(f) / |E_1| = 1$. A map that sends $b$ to a leaf conserves at most one edge, since a leaf has only one neighbor. The IsoRank page works this example out with its scores: the score of the pair $(b, x)$ is the largest, and the greedy matching takes it first.

**The sequence term can disagree with the topology term.** Let $G_1$ be the edge $a - b$ and $G_2$ the path $x - y - z$, with $s(a, x) = s(b, z) = 1$ and all other similarities 0. The map $a \to x$, $b \to z$ has $\mathrm{S} = 2$ and $\mathrm{EC} = 0$, while $a \to x$, $b \to y$ has $\mathrm{S} = 1$ and $\mathrm{EC} = 1$. The first map has score $2 (1 - \alpha)$ and the second has score 1, so the first is the unique best map for $\alpha < 1/2$, and the second is a best map for $\alpha > 1/2$, tied with $a \to y$, $b \to z$.

## Known algorithms

- **Exact search.** Enumerate the $n_2! / (n_2 - n_1)!$ one to one maps, or solve the problem as a [quadratic assignment problem](/quadratic-assignment-problem/) or an integer program by branch and bound, often with [Lagrangian relaxation](/lagrangian-relaxation/) for the bounds. This is practical only for small networks or for problems that the bounds solve.
- **Sequence only.** For $\alpha = 0$, the best map is a [maximum weight matching](/maximum-weight-matching/) of the bipartite graph with weights $s$, found in polynomial time by the [Hungarian algorithm](/hungarian-algorithm/).
- **IsoRank (global).** [IsoRank](/isorank/) (Singh, Xu and Berger) scores each pair of proteins by a fixed point equation in which a pair is similar if its neighbors are similar, mixed with the sequence score, and then extracts a one to one map by a greedy matching. It is a heuristic: the matching is a 1/2 approximation for the pair scores, but the pair scores do not bound the number of conserved edges.
- **PathBLAST (local).** Kelley et al. (2003) built a graph whose nodes are pairs of similar proteins, with an edge when both pairs interact or are close in their networks, and searched it for high scoring paths, which are conserved pathways.
- **Graphlet methods.** GRAAL (Kuchaiev et al. 2010) describes each node by counts of the small subgraphs that touch it, matches nodes with similar counts from seed pairs outward, and uses no sequence.
- **Local search.** Start from a map given by a fast method and improve it by swaps or by simulated annealing on the score.

## Bounds

**NP-hardness (theorem).** Deciding whether a one to one map $f$ with $\mathrm{EC}(f) = |E_1|$ exists is NP-complete, so maximizing $\mathrm{score}(f)$ is NP-hard for $\alpha = 1$.

*Proof.* A map with $\mathrm{EC}(f) = |E_1|$ sends every edge of $G_1$ to an edge of $G_2$, so it is an embedding of $G_1$ as a subgraph of $G_2$, not necessarily induced; conversely, every such embedding has $\mathrm{EC}(f) = |E_1|$. This is the subgraph isomorphism problem, which is NP-complete (Garey and Johnson); the certificate is the map. An algorithm for the maximum of $\mathrm{EC}$ decides it by comparing the maximum with $|E_1|$. $\square$

With $G_1$ a complete graph on $k$ nodes, the same argument gives the [clique problem](/clique-problem/), so the problem is hard even when one network is very simple. With all similarities equal, the sequence term is a constant, so the hardness holds for any $\alpha > 0$.

**The topology term is a quadratic assignment (theorem).** With adjacency matrices $A_1$ and $A_2$, $\mathrm{EC}(f) = \frac12 \sum_{u, v \in V_1} A_1[u, v] \, A_2[f(u), f(v)]$, which is the objective of a quadratic assignment problem. Each edge $\{u, v\}$ of $G_1$ appears twice in the sum, once as $(u, v)$ and once as $(v, u)$, and contributes 1 each time exactly when its image is an edge.

**Exact search grows fast.** For $n_1 = n_2 = n$ there are $n!$ maps, and real networks have thousands of proteins, so global alignment is solved only by heuristics, whose quality is measured, not proven.

## Reductions

- **From subgraph isomorphism and clique.** As in the bounds above.
- **To quadratic assignment.** The global problem with any $\alpha$ is a quadratic assignment problem with a linear term $s$.
- **To maximum weight matching.** For $\alpha = 0$; IsoRank also ends with a matching, on its pair scores instead of $s$.
- **To a search in the product graph.** Local alignment becomes a search for dense or high scoring subgraphs, or for paths, in the graph on pairs $(u, v)$, as in PathBLAST.
- **To maximum common subgraph.** For $\alpha = 1$ and a partial map, maximizing the conserved edges is the maximum common edge subgraph problem, a form of [maximum common subgraph](/maximum-common-subgraph/).

## Applications

- **Function prediction.** A protein of unknown function is given the annotation of the protein it is aligned with in a well studied species.
- **Orthology.** Proteins that align in sequence and in network position are candidate orthologs, the same gene in two species; Singh, Xu and Berger used IsoRank for this.
- **Conserved complexes and pathways.** Local alignments show groups of interactions that several species share.
- **Evolution.** Kuchaiev et al. (2010) built trees of species from the topological similarity of their networks.
- **Checking data.** Interactions that are conserved across species are more likely to be real than those seen in one data set only.

## References
