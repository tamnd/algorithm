---
tag: AJACX4
kind: concept
slug: structural-equivalence
name: Structural equivalence
area: graphs/network-analysis
level: core
summary: Two nodes are equivalent when they have the same neighbourhoods.
prereqs: [graph, neighborhood, adjacency-matrix]
see_also: [node-similarity, stochastic-block-model, structural-holes, simrank, cosine-similarity, weisfeiler-leman, agglomerative-clustering, structural-balance-theorem]
sources:
  - paper: doi:10.1080/0022250X.1971.9989788
    title: François Lorrain and Harrison C. White, Structural equivalence of individuals in social networks, Journal of Mathematical Sociology 1(1), 49 to 80 (1971)
    locator: the definition of structurally equivalent individuals as those with the same relations to all others, and the reduction of a network to its classes
  - paper: doi:10.1086/226141
    title: Harrison C. White, Scott A. Boorman and Ronald L. Breiger, Social structure from multiple networks I, Blockmodels of roles and positions, American Journal of Sociology 81(4), 730 to 780 (1976)
    locator: blockmodels, in which approximately equivalent actors are grouped into blocks with zero or one blocks of ties between them
  - book: isbn:9780521387071
    title: Stanley Wasserman and Katherine Faust, Social Network Analysis, Methods and Applications, Cambridge University Press, 1994
    locator: Chapter 9, Structural equivalence (the definition, the Euclidean distance and correlation measures, and CONCOR), and Chapter 12 (automorphic and regular equivalence)
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 7, Measures and metrics (the section on similarity, with structural and regular equivalence)
---

Two vertices of a network are *structurally equivalent* when they have exactly the same ties to every other vertex: the same neighbours, and in a directed network the same in-neighbours and the same out-neighbours. Lorrain and White (1971) introduced it to define social positions: equivalent actors can be swapped without changing the network, so they hold the same position. It is an equivalence relation, its classes can be found in linear time, and its relaxations, measured by the distance between rows of the [adjacency matrix](/adjacency-matrix/), are the basis of blockmodels and of many [node similarity](/node-similarity/) scores.

## In plain words

Two people are in the same position if they know exactly the same people. If two employees report to the same manager, work with the same colleagues and deal with the same clients, then from the point of view of the network they are interchangeable.

This is a strict test: one extra friend breaks it. In real networks exact matches are rare, so people also measure how close two members come to it, by counting the contacts that one has and the other lacks. Members who come close can then be grouped into positions.

The idea is to describe a network by its positions and how they connect, instead of by every individual.

## The idea

**Definition.** Let $G = (V, E)$ be an undirected simple [graph](/graph/) with [neighbourhoods](/neighborhood/) $N(v)$. Vertices $u \ne v$ are structurally equivalent, written $u \equiv v$, when

$$N(u) \setminus \{v\} = N(v) \setminus \{u\},$$

and every vertex is equivalent to itself. The removal of $u$ and $v$ means that the tie between the two of them does not matter; in the terms of graph theory, $u$ and $v$ are *twins*, *false twins* when they are not adjacent ($N(u) = N(v)$) and *true twins* when they are adjacent ($N(u) \cup \{u\} = N(v) \cup \{v\}$).

- **Directed graphs.** $u \equiv v$ when $u$ and $v$ have the same out-neighbours and the same in-neighbours, apart from each other.
- **Weighted graphs.** $u \equiv v$ when the rows $u$ and $v$ of the weight matrix agree in every column other than $u$ and $v$, and the columns agree too for a directed graph.
- **Disconnected graphs.** Nothing changes: the condition is about neighbourhoods, and all isolated vertices form one class, since they have the same empty neighbourhood.

**It is an equivalence relation.** Reflexivity and symmetry are clear. For transitivity, let $u \equiv v$ and $v \equiv w$ with $u, v, w$ distinct. The two kinds of twin cannot mix: if $u$ is adjacent to $v$ but $v$ is not adjacent to $w$, then $u \in N(v) \setminus \{w\} = N(w) \setminus \{v\}$, so $w$ is adjacent to $u$, and then $w \in N(u) \setminus \{v\} = N(v) \setminus \{u\}$, so $v$ is adjacent to $w$, a contradiction; the other mixed case is symmetric. So either all three are false twins, and $N(u) = N(v) = N(w)$, or the closed neighbourhoods are all equal. In both cases $u \equiv w$.

**Computing the classes.** Group the vertices by the sorted list $N(v)$ (for false twins) and by the sorted list $N(v) \cup \{v\}$ (for true twins), by hashing or by radix sort. Since the two kinds never mix within a class, each class with more than one vertex is a group of one of the two kinds, and the whole partition takes $O(n + m)$ time.

**Approximate equivalence.** Exact classes are usually tiny. Burt's Euclidean distance

$$d(u, v) = \sqrt{\sum_{k \ne u, v} (A_{uk} - A_{vk})^2}$$

is 0 exactly when $u \equiv v$ in a graph without weights, and counts the vertices adjacent to one of $u, v$ but not the other. The Pearson correlation of the rows and the [cosine similarity](/cosine-similarity/) of the rows are the other common choices. [Agglomerative clustering](/agglomerative-clustering/) on such a measure, or the CONCOR method of repeated correlations, groups the vertices into *blocks*; the blockmodel then records, for each pair of blocks, whether ties between them are dense or absent.

**Weaker notions.** Structural equivalence asks for the *same* neighbours. *Automorphic equivalence* asks for an automorphism of the graph that maps $u$ to $v$, and *regular equivalence* asks only that equivalent vertices have neighbours in the same classes. Two teachers in different schools are regularly equivalent (each has students) but not structurally equivalent (they have different students). Each notion implies the next: structural implies automorphic (swap $u$ and $v$), and automorphic implies regular. [SimRank](/simrank/) is a graded form of regular equivalence, and [colour refinement](/weisfeiler-leman/) computes a partition that every automorphism respects.

## Examples

Take the graph on $0, \ldots, 6$ with the edges $01, 02, 03, 04, 34, 35, 45, 56, 16, 26$. The neighbourhoods are $N(1) = N(2) = \{0, 6\}$, $N(3) = \{0, 4, 5\}$ and $N(4) = \{0, 3, 5\}$. So the classes are

$$\{0\}, \quad \{1, 2\}, \quad \{3, 4\}, \quad \{5\}, \quad \{6\}.$$

Vertices 1 and 2 are false twins, and 3 and 4 are true twins: they are adjacent, and apart from each other both see $0$ and $5$. Vertices 0 and 6 are not equivalent, although both are joined to 1 and 2: 0 also sees 3 and 4, and 6 sees 5, so the Euclidean distance between them is $\sqrt 3$. The reduced graph on the five classes has an edge between two classes when their members are joined, and it describes the whole graph, because all members of a class have the same ties.

**Non-examples.**

- In a cycle with 5 or more vertices, no two vertices are structurally equivalent, although every two are automorphically equivalent: the vertices all look the same, but they have different neighbours.
- In a star, the leaves form one class, and the centre is alone. In the path $a - b - c - d$, no two vertices are equivalent: $a$ and $d$ are symmetric but have different neighbours.

## Where it is used

- **Social positions and roles.** Blockmodels reduce a network of people to a few positions, such as "manager" and "staff", from the pattern of ties alone.
- **[Node similarity](/node-similarity/) and link prediction.** The common-neighbour, Jaccard and cosine scores are graded versions of structural equivalence.
- **[Stochastic block model](/stochastic-block-model/).** The probabilistic form of a blockmodel: vertices in the same block are *stochastically* equivalent, with the same probability of a tie to each other vertex.
- **[Structural holes](/structural-holes/).** Burt's measures of redundancy treat two contacts as redundant when they are tied to each other or structurally equivalent.
- **Graph algorithms.** Twin classes are modules of the graph; contracting them shrinks the input of problems such as colouring and independent set, and a graph is a cograph exactly when merging twins again and again shrinks it to one vertex.

## References
