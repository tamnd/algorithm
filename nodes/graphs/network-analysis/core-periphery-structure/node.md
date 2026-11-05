---
tag: 79WWF5
kind: concept
slug: core-periphery-structure
name: Core-periphery structure
aliases:
- core-periphery
area: graphs/network-analysis
level: advanced
summary: Division into a dense, well-connected core and a sparse periphery.
prereqs: [graph, degree, community-detection]
see_also: [k-core, rich-club-coefficient, community-detection, stochastic-block-model, batagelj-zaversnik-algorithm, assortativity, eigenvector-centrality, degree-centrality]
sources:
  - paper: doi:10.1016/S0378-8733(99)00019-2
    title: Stephen P. Borgatti and Martin G. Everett, Models of core/periphery structures, Social Networks 21(4), 375 to 395 (2000)
    locator: the whole paper (the discrete model with the ideal pattern matrix, the fit by correlation, and the continuous model with coreness values)
  - paper: doi:10.1137/120881683
    title: M. Puck Rombach, Mason A. Porter, James H. Fowler and Peter J. Mucha, Core-periphery structure in networks, SIAM Journal on Applied Mathematics 74(1), 167 to 190 (2014)
    locator: the whole paper (a core score for each vertex with tunable sharpness and size of the core)
  - paper: doi:10.1103/PhysRevE.91.032803
    title: Xiao Zhang, Travis Martin and M. E. J. Newman, Identification of core-periphery structure in networks, Physical Review E 91(3), 032803 (2015)
    locator: the whole paper (core-periphery structure as a stochastic block model with two blocks, fitted by maximum likelihood)
  - paper: doi:10.1093/comnet/cnt016
    title: Peter Csermely, András London, Ling-Yun Wu and Brian Uzzi, Structure and dynamics of core/periphery networks, Journal of Complex Networks 1(2), 93 to 123 (2013)
    locator: the whole paper (a review of definitions, detection methods and roles of cores in many kinds of networks)
---

A network has **core-periphery structure** when its vertices split into a **core**, whose members are densely linked to each other, and a **periphery**, whose members link mostly to the core and hardly to each other. It is a different pattern from [community structure](/community-detection/): communities are several dense groups that are sparse between them, while a core-periphery network has one dense group that the rest hangs on. Borgatti and Everett gave the first formal models in 2000, for social networks; the pattern has since been found in trade networks, transport networks, the Internet, financial and neural networks.

## In plain words

Think of a city's airline network. A few big airports have direct flights to each other and to many small airports. The small airports mostly fly only to a big one, rarely to each other. The big airports form the core and the small ones the periphery.

In a company, the core may be a group of managers who all talk to each other, while each other employee talks mainly to one or two of them.

Finding this split helps to see who holds a network together. Removing a core member cuts many routes at once, while removing a peripheral member changes little for the rest.

## The idea

**The ideal pattern.** Order the vertices with the core first. In a perfect core-periphery network the adjacency matrix has a full block for the core-core pairs and an empty block for the periphery-periphery pairs. The core-periphery block may be taken as full (every peripheral vertex is linked to every core vertex) or left free. Borgatti and Everett write the ideal pattern as a matrix $\Delta$ with $\delta_{ij} = 1$ when $i$ and $j$ are both in the core, $\delta_{ij} = 0$ when both are in the periphery, and either 1 or "not counted" for the mixed pairs.

**Fit of a partition.** For a split of the vertices into core and periphery, the fit is the Pearson correlation between the entries $a_{ij}$ of the adjacency matrix and the entries $\delta_{ij}$, over the pairs $i < j$ that are counted. A perfect pattern gives correlation 1. Finding the split with the best fit is an optimization over all subsets, done in practice with heuristics such as local search or genetic algorithms.

**Continuous version.** Instead of a split, give each vertex a coreness $c_i \ge 0$ and use the pattern $\delta_{ij} = c_i c_j$; the core is then a matter of degree. Rombach, Porter, Fowler and Mucha define a core score for each vertex with two parameters, one for the sharpness of the boundary and one for the size of the core.

**As a block model.** Zhang, Martin and Newman treat core-periphery structure as a [stochastic block model](/stochastic-block-model/) with two blocks and the edge probabilities $p_{\mathrm{cc}} > p_{\mathrm{cp}} > p_{\mathrm{pp}}$, and fit it by maximum likelihood. This gives a statistical test of whether a core is there at all.

**Related but different notions.**

- The [k-core](/k-core/) of a graph, the largest subgraph of minimum degree $k$, is a nested family computed in linear time by the [Batagelj-Zaversnik algorithm](/batagelj-zaversnik-algorithm/). A high $k$-core is often used as the core, but it only needs every vertex to have many neighbours inside, not a dense core-core block.
- The [rich-club coefficient](/rich-club-coefficient/) measures how densely the highest-degree vertices are linked to each other, one ingredient of a core.
- A core-periphery split does not fix the sign of [degree assortativity](/assortativity/): links between core members push it up, links from the core to low-degree peripheral vertices push it down.

Directed networks have their own patterns, such as a core with both in-links and out-links and a periphery that only sends or only receives. Weighted networks use the weights in place of $a_{ij}$. Disconnected networks are handled as they are, although a component that does not touch the core is far from the ideal pattern and lowers the fit; it is common to restrict the analysis to the largest component. Ties between equally good splits are common, since the fit changes little when one peripheral vertex of high degree moves into the core.

## Examples

**A clean core.** Take the 10 vertices 0 to 9, with $K_4$ on $\{0, 1, 2, 3\}$ and the 8 edges $\{4, 0\}$, $\{5, 0\}$, $\{5, 1\}$, $\{6, 1\}$, $\{7, 2\}$, $\{8, 2\}$, $\{8, 3\}$, $\{9, 3\}$, so each of 4 to 9 is linked to one or two core vertices and to no other peripheral vertex. A search over all $2^{10}$ splits gives:

- With the mixed pairs not counted, the split with the core $\{0, 1, 2, 3\}$ has correlation exactly 1: its 6 core-core pairs are all edges and its 15 periphery-periphery pairs are all non-edges. The next best splits, such as the core $\{0, 1, 2, 3, 5\}$, have correlation about 0.816.
- With the mixed pairs counted as 1, the same core is still the best, with correlation about 0.475, since only 8 of the 24 mixed pairs are edges. The cores of 3 vertices from $\{0, 1, 2, 3\}$ follow with about 0.436.

Here the core is also the 3-core of the graph, since the core vertices have degree 5 and the others degree 1 or 2.

**Two groups instead.** In the graph with the vertices 0 to 6 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$, the two triangles $\{0, 1, 2\}$ and $\{4, 5, 6\}$ are dense, with few edges between them. Any core containing one triangle leaves the other triangle as three periphery-periphery edges, so this graph is better described by two communities than by a core and a periphery.

**Real networks.** The world trade network has a core of large economies trading heavily with each other. Airline networks have a core of hub airports. The network of the Internet's autonomous systems has a dense core of large providers. In many of these, the core found by a method depends on the method and its parameters, which is why several measures are often compared.

## Where it is used

- **Social networks.** Borgatti and Everett's original setting: finding the elite of an organization, or the central members of a scientific field.
- **Economics and finance.** Core banks in interbank lending networks and core countries in trade networks, where the core carries most of the systemic risk.
- **Transport and infrastructure.** Hubs in airline and road networks, and the backbone of the Internet; protecting the core protects most routes.
- **Network science methods.** As a check before [community detection](/community-detection/), since methods for communities can give misleading results on a network that is really a core with a periphery, and as a feature in the study of spreading and robustness.

## References
