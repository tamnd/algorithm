---
tag: 0626ZG
kind: problem
slug: graph-motif
name: Graph motif
aliases:
- colorful graph motif
area: complexity/parameterized-complexity
level: research
summary: "Given a vertex-colored graph and a multiset M of k colors, find a connected set of vertices whose colors are exactly M. NP-hard even on trees; FPT in k, with randomized time O*(2^k)."
prereqs: [color-coding, fixed-parameter-tractable]
see_also: [color-coding, parameterized-longest-path, k-path-color-coding, kernel-lower-bounds, w-hierarchy, set-cover-conjecture, tree]
sources:
  - paper: doi:10.1016/j.jcss.2010.07.003
    title: "Michael R. Fellows, Guillaume Fertin, Danny Hermelin and Stéphane Vialette, Upper and lower bounds for finding connected motifs in vertex-colored graphs, Journal of Computer and System Sciences 77(4), 799-811 (2011)"
    locator: NP-hardness on trees and bipartite graphs, W[1]-hardness in the number of colors, and the FPT algorithm in the motif size
  - paper: doi:10.1109/tcbb.2006.55
    title: "Vincent Lacroix, Cristina G. Fernandes and Marie-France Sagot, Motif search in graphs: application to metabolic networks, IEEE/ACM Transactions on Computational Biology and Bioinformatics 3(4), 360-368 (2006)"
    locator: the definition of the problem and its motivation from metabolic networks
  - paper: doi:10.1007/s00453-015-9981-1
    title: "Andreas Björklund, Petteri Kaski and Lukasz Kowalik, Constrained multilinear detection and generalized graph motifs, Algorithmica 74(2), 947-967 (2016)"
    locator: randomized O*(2^k) time, and the lower bound from the set cover conjecture
  - paper: doi:10.1007/978-3-662-44465-8_50
    title: "Ron Y. Pinter, Hadas Shachnai and Meirav Zehavi, Deterministic parameterized algorithms for the graph motif problem, Mathematical Foundations of Computer Science 2014 (MFCS 2014), Lecture Notes in Computer Science 8635, 589-600"
    locator: the deterministic O*(5.22^k) algorithm
  - paper: doi:10.1007/978-3-642-17493-3_4
    title: "Abhimanyu M. Ambalath, Radheshyam Balasundaram, Chintan Rao H., Venkata Koppula, Neeldhara Misra, Geevarghese Philip and M. S. Ramanujan, On the kernelization complexity of colorful motifs, Parameterized and Exact Computation (IPEC 2010), Lecture Notes in Computer Science 6478, 14-25"
    locator: no polynomial kernel for the colorful motif, even on restricted trees
---

Graph motif asks for a connected piece of a vertex-colored graph whose colors match a given list. The input is a graph $G$, a coloring of its vertices, and a multiset $M$ of $k$ colors, the *motif*. The question is whether some set $S$ of $k$ vertices induces a connected subgraph and has exactly the colors of $M$, with the same number of each color. Unlike [subgraph isomorphism](/subgraph-isomorphism/), the motif fixes only the colors, not the shape: any connected shape counts. Lacroix, Fernandes and Sagot (2006) introduced the problem to find groups of reactions in metabolic networks. It is NP-hard even when $G$ is a tree of maximum degree 3 and the motif is colorful (each color once), but with the motif size $k$ as the [parameter](/parameter/) it is [fixed-parameter tractable](/fixed-parameter-tractable/), in randomized time $O^*(2^k)$, where $O^*$ hides factors polynomial in $n$.

## In plain words

Each point of a network has a color, such as a type of chemical reaction. You are given a short shopping list of colors, for example two red points, one green and one blue. You want a group of points that hangs together in the network and has exactly the colors on the list, no more and no less.

The shape of the group does not matter. Only two things count: the points must be connected to each other inside the group, and the colors must match the list.

This is hard in general, even when the network is a tree. But when the list is short, there are methods whose cost grows fast with the length of the list and only slowly with the size of the network.

## Definition

A *vertex-colored graph* is a graph $G = (V, E)$ with a map $c: V \to C$ to a set of colors $C$. For $S \subseteq V$, $c(S)$ is the multiset of the colors of the vertices of $S$. $G[S]$ is the subgraph induced by $S$.

**GRAPH-MOTIF**

- Instance: a graph $G = (V, E)$, a coloring $c: V \to C$, and a multiset $M$ of colors from $C$ with $|M| = k$.
- Parameter: $k$, the size of the motif.
- Question: is there a set $S \subseteq V$ such that $G[S]$ is connected and $c(S) = M$?

The coloring need not be proper: adjacent vertices may have the same color. A yes-instance has a certificate of $k$ vertices, checked in $O(k + m)$ time by a graph search and a count of colors. The *colorful* case is the case where $M$ is a set, so every color appears at most once in the motif.

## Variants

- *Colorful motif.* $M$ has $k$ different colors. This is still NP-hard on trees, but a simple dynamic program over color sets solves it in $O^*(3^k)$ time, as in [color coding](/color-coding/): for each vertex $v$ and color set $X$, record whether a connected colorful set with the colors $X$ contains $v$, and combine two such sets that meet at an edge and have disjoint colors.
- *Other parameters.* With the number $|C|$ of colors as the parameter, the problem is W[1]-hard, even on trees (Fellows et al., 2011). See [the W hierarchy](/w-hierarchy/).
- *List colors.* Each vertex has a list of allowed colors, and the set $S$ must have a choice of colors from the lists that equals $M$.
- *Inexact motifs.* Allow some colors of $M$ to be missing from $S$, or some extra vertices in $S$ whose colors are not in $M$. These forms were studied for biological data, where exact matches are rare.
- *Paths and trees as hosts.* On a path, the problem asks for a window of the sequence whose colors are a given multiset. This is jumbled pattern matching, which is polynomial.

## Examples

Take the graph with the vertices $1, \ldots, 8$, the edges $12$, $23$, $34$, $25$, $56$, $67$, $48$, $78$, and the colors $1, 4, 7$ red, $2, 5, 8$ green and $3, 6$ blue. It is a cycle $2, 3, 4, 8, 7, 6, 5$ with a pendant vertex 1 at vertex 2. A brute-force search over all sets of the right size gives:

| motif $M$ | solutions | sets |
|---|---|---|
| red, green, blue | 5 | $\{1,2,3\}$, $\{2,3,4\}$, $\{3,4,8\}$, $\{5,6,7\}$, $\{6,7,8\}$ |
| red, red, green | 1 | $\{4,7,8\}$ |
| red, red, green, blue | 3 | $\{1,2,3,4\}$, $\{3,4,7,8\}$, $\{4,6,7,8\}$ |
| red, red, green, green | 0 | none |
| red, green, blue, blue | 0 | none |

The motif red, red, green, green shows that the colors alone are not enough. The graph has three red and three green vertices, but no connected set has two of each. Without the blue vertices, the red and green vertices fall into two pieces, $\{1, 2, 5\}$ and $\{4, 7, 8\}$, and neither piece has two vertices of each color.

The motif red, green, blue is colorful. In the dynamic program, the entry for vertex 3 and the colors $\{$green, blue$\}$ comes from the edge $23$, and the full entry for vertex 3 then joins the red vertex 4.

## Known algorithms

Time bounds are for a RAM with words of $O(\log n)$ bits; $O^*$ hides factors polynomial in $n$.

- Fellows, Fertin, Hermelin and Vialette (2011): the first FPT algorithm in $k$, based on [color coding](/color-coding/).
- Colorful motif: deterministic $O^*(3^k)$ by dynamic programming over color sets, as above.
- Algebraic methods: randomized $O^*(2^k)$ time and polynomial space (Björklund, Kaski and Kowalik, 2016), by detection of a multilinear monomial with constraints on the colors. This bound also holds for the general motif with repeated colors.
- Deterministic: $O^*(5.22^k)$ time (Pinter, Shachnai and Zehavi, MFCS 2014), by [representative families](/representative-families/).

All randomized bounds have one-sided error: a reported set is checked, and the answer "no" is wrong with a small probability.

## Bounds

- *NP-hardness.* Fellows et al. (2011) proved the problem NP-hard on trees of maximum degree 3 with a colorful motif, and on bipartite graphs of maximum degree 4 with only two colors. So no polynomial algorithm exists on these classes unless P = NP.
- *W[1]-hardness.* With the number of colors as the parameter, the problem is W[1]-hard, even on trees. So no algorithm with time $f(|C|) n^{O(1)}$ exists unless FPT = W[1]. The parameter $k$ is what makes it tractable.
- *Base of the exponent.* An algorithm in time $O^*((2 - \varepsilon)^k)$ for some $\varepsilon > 0$ would give a faster algorithm for set cover and refute the [set cover conjecture](/set-cover-conjecture/) (Björklund, Kaski and Kowalik). So $O^*(2^k)$ is likely the right base.
- *No polynomial kernel.* The colorful motif has no polynomial kernel, in vertices or in bits, unless $\mathsf{NP} \subseteq \mathsf{coNP/poly}$, even on trees of restricted shape such as comb graphs (Ambalath et al., IPEC 2010). See [kernel lower bounds](/kernel-lower-bounds/).

## Reductions

- *Relation to k-path.* The colorful $k$-path problem asks for a colorful path; the colorful motif asks for any connected colorful set. A colorful path is a colorful motif solution, but not the other way round, so the two problems differ. Both are solved by a dynamic program over color sets, as on the page [k-path by color coding](/k-path-color-coding/).
- *From set cover.* The lower bound of Björklund, Kaski and Kowalik maps an instance of [set cover](/set-cover/) to a graph motif instance whose motif size is linear in the size of the universe, so a faster base for graph motif gives a faster base for set cover.
- *To multilinear detection.* The algebraic algorithms build a polynomial whose monomials stand for connected subtrees with $k$ vertices, labeled by their colors, and test for a monomial that is multilinear in the vertex variables and has the color counts of $M$.

## Applications

- *Metabolic networks.* Vertices are reactions, edges link reactions that share a compound, and colors are reaction classes. A motif finds groups of reactions that do the same job in different organisms, whatever the order of the steps.
- *Protein interaction networks.* Colors are protein families, and a motif finds a complex with a known family composition.
- *Testing new algebraic methods.* The problem is a standard test for constrained multilinear detection, because the shape is free but the colors are counted.

## References
