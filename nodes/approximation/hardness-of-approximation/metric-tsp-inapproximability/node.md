---
tag: XPTJYD
kind: theorem
slug: metric-tsp-inapproximability
name: Metric TSP inapproximability
aliases:
- 123/122 TSP hardness
- 123/122 bound for metric TSP
- Inapproximability of metric TSP
- Papadimitriou-Vempala hardness
- path cover identity for (1,2)-TSP
area: approximation/hardness-of-approximation
level: research
summary: No polynomial algorithm approximates metric TSP within 123/122 unless P = NP. This page proves the path cover identity behind all (1,2)-TSP bounds and sketches the 123/122 reduction.
prereqs: [metric-tsp, gap-problem, gap-preserving-reduction, hamiltonian-cycle-problem, minimum-path-cover-problem]
see_also: [general-tsp-inapproximability, max-3sat-inapproximability, hastad-3bit-pcp, christofides-algorithm, karlin-klein-oveis-gharan-algorithm, asymmetric-tsp, arora-euclidean-tsp-ptas, apx-class]
sources:
  - paper: doi:10.1016/j.jcss.2015.06.003
    title: Marek Karpinski, Michael Lampis and Richard Schmied, New inapproximability bounds for TSP, Journal of Computer and System Sciences 81(8), 2015
    locator: pages 1665 to 1677 (no ratio below 123/122 for TSP and below 75/74 for asymmetric TSP unless P = NP)
  - paper: doi:10.1007/s00493-006-0008-z
    title: Christos H. Papadimitriou and Santosh Vempala, On the approximability of the traveling salesman problem, Combinatorica 26(1), 2006
    locator: the bounds 220/219 for TSP and 117/116 for asymmetric TSP
  - paper: "C. H. Papadimitriou and M. Yannakakis, The traveling salesman problem with distances one and two, Mathematics of Operations Research 18(1), 1993"
    locator: MAX SNP-hardness of (1,2)-TSP and the 7/6 approximation
  - paper: "M. Lampis, Improved inapproximability for TSP, Theory of Computing 10, 2014"
    locator: the bound 185/184 for TSP (conference version APPROX 2012)
  - paper: "L. Engebretsen, An explicit lower bound for TSP with distances one and two, Algorithmica 35(4), 2003"
    locator: the first explicit constant, 5381/5380 (conference version STACS 1999)
  - paper: doi:10.1145/502090.502098
    title: Johan Håstad, Some optimal inapproximability results, Journal of the ACM 48(4), 2001
    locator: the gap for equations mod 2 with three variables, the starting point of the reductions
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.4 (the TSP and its approximation algorithms)
---

The metric TSP inapproximability theorem says that no polynomial algorithm approximates the [metric TSP](/metric-tsp/) within a ratio below $\frac{123}{122} \approx 1.0082$ unless P = NP. Karpinski, Lampis and Schmied proved it in 2013, after a line of smaller constants that started with the APX-hardness of TSP with costs 1 and 2 by Papadimitriou and Yannakakis (1993). This page proves the identity that turns every hardness result for costs 1 and 2 into a statement about path covers, and the gap lemma that follows from it. The reduction for $\frac{123}{122}$ is only sketched. The NP-hardness of the exact problem is on the [metric TSP](/metric-tsp/) page and is not repeated here.

## Statement

An instance of the metric TSP is a complete graph with symmetric costs that satisfy the triangle inequality. $\mathrm{OPT}$ is the least cost of a tour, and a ratio $\rho \ge 1$ means a tour of cost at most $\rho \cdot \mathrm{OPT}$ on every instance. For a graph $G = (V, E)$ on $n \ge 3$ vertices, the **(1,2) instance** $I(G)$ gives cost 1 to the pairs in $E$ and cost 2 to the other pairs; it is metric because $2 \le 1 + 1$. The **path cover number** $\pi(G)$ is the least number of vertex-disjoint paths in $G$ that cover $V$ (a single vertex is a path).

**Theorem 1 (Karpinski, Lampis and Schmied 2015).** For every $\varepsilon > 0$, a polynomial algorithm for the metric TSP with ratio $\frac{123}{122} - \varepsilon$ gives P = NP. The hard instances are shortest path metrics of weighted graphs. For the asymmetric TSP with the triangle inequality, the same holds with $\frac{75}{74} - \varepsilon$.

**Lemma 2 (path cover identity).** $\mathrm{OPT}(I(G)) = n$ if $G$ has a Hamiltonian cycle, and $\mathrm{OPT}(I(G)) = n + \pi(G)$ otherwise. A tour of cost $n + j$ with $j \ge 1$ gives $j$ paths of $G$ that cover $V$, and $j$ such paths give a tour of cost at most $n + j$, both in linear time.

**Lemma 3 (gap transfer).** Let $0 \le a < b$ be constants, and suppose that on some class of graphs it is NP-hard to tell $\pi(G) \le a n$ from $\pi(G) \ge b n$. Then for each $\rho < \frac{1 + b}{1 + a}$, a polynomial algorithm with ratio $\rho$ on (1,2) instances gives P = NP.

Theorem 1 is cited. Lemmas 2 and 3 are proved below, and the code for this page checks Lemma 2 by brute force.

## In plain words

Take a graph and make a travel problem from it: a trip along a line of the graph costs 1, and any other trip costs 2. A full tour costs the number of cities plus one for each expensive step. If you remove the expensive steps, the tour falls into pieces, and each piece is a path in the graph. So the cheapest tour is the number of cities plus the least number of paths that cover the graph, except when one cycle covers it all.

So to show that tours are hard to approximate, it is enough to show that the least number of covering paths is hard to approximate. The best known result uses more general costs and a careful puzzle built from equations, and it shows that no fast method can always get within about 0.8 percent of the best tour.

## Proof

*Lemma 2.* If $G$ has a Hamiltonian cycle, that cycle is a tour of cost $n$, and no tour costs less because every pair costs at least 1. Suppose now that $G$ has no Hamiltonian cycle, and take any tour. Let $j$ be the number of its edges with cost 2. Then $j \ge 1$, since otherwise the tour is a Hamiltonian cycle of $G$, and the cost is $(n - j) + 2j = n + j$. Delete the $j$ edges of cost 2 from the cycle. What remains is $j$ vertex-disjoint paths that use only edges of $G$ and cover $V$, so $j \ge \pi(G)$ and the cost is at least $n + \pi(G)$. Conversely, take $\pi = \pi(G)$ covering paths $P_1, \ldots, P_\pi$ and join the end of $P_i$ to the start of $P_{i+1}$, and the end of $P_\pi$ to the start of $P_1$. This adds $\pi$ edges, each of cost at most 2, to $n - \pi$ edges of cost 1, so the tour costs at most $n + \pi$. (When $\pi = 1$ the single added edge closes the path into a cycle; it has cost 2 because $G$ is not Hamiltonian.) So $\mathrm{OPT} = n + \pi(G)$. Both conversions only read the tour or the paths once. $\blacksquare$

*Lemma 3.* Instances with $n < 2/b$ form a finite set, and the algorithm can solve them by a fixed table. For $n \ge 2/b$, a NO instance has $\pi(G) \ge b n \ge 2$, so $G$ has no Hamiltonian cycle and $\mathrm{OPT} = n + \pi(G) \ge (1 + b) n$ by Lemma 2. A YES instance has $\mathrm{OPT} \le n + \pi(G) \le (1 + a) n$, also by Lemma 2. An algorithm with ratio $\rho$ returns at most $\rho (1 + a) n < (1 + b) n$ on a YES instance, and at least $(1 + b) n$ on a NO instance. So comparing its answer with $(1 + b) n$ decides the NP-hard question. $\blacksquare$

The identity is exact, so Lemma 3 loses nothing: every hardness result for (1,2) instances is a hardness result for the path cover number, and the reverse. Papadimitriou and Yannakakis proved that $\pi$ is hard to approximate within some constant on graphs of bounded degree, by a reduction from satisfiability with each variable in a bounded number of clauses. With the [PCP theorem](/pcp-theorem/), this makes (1,2)-TSP APX-hard, and so the metric TSP has no PTAS unless P = NP. Their reduction is cited.

*Theorem 1, sketch.* This is a sketch; the gadget weights and the analysis of the amplifiers are in the paper and are not checked here.

1. Start from [Håstad's](/hastad-3bit-pcp/) gap for systems of equations mod 2 with three variables each: it is NP-hard to tell whether a $1 - \varepsilon$ fraction of the equations can be satisfied or only a $\frac12 + \varepsilon$ fraction.
2. Make each variable occur a bounded number of times. Karpinski, Lampis and Schmied use amplifier graphs: each variable is replaced by many copies, joined by consistency equations along an expander-like graph, so that an assignment that is not consistent on the copies loses more than it can gain.
3. Build a weighted graph. Each variable becomes a gadget that a tour can cross in one of two ways, read as the value 0 or 1, and each equation becomes a gadget whose cheapest traversal costs one more unit when the equation is false. The metric is the shortest path metric of this graph, so a tour is a closed walk.
4. A good assignment gives a short tour. Conversely, a tour can be changed, without raising its cost, into one that reads off an assignment, and each false equation then adds at least a fixed amount to its cost. The weights are chosen to make the ratio of the two cases as large as possible, and this gives $\frac{123}{122} - \varepsilon$.

The instance has size linear in the number of equations, so the reduction is polynomial.

### Example

The star $K_{1,4}$ has $n = 5$ and no Hamiltonian cycle. Its path cover number is 3: one path passes through the centre and two leaves, and the other two leaves are paths alone. So $\mathrm{OPT}(I(K_{1,4})) = 8$, reached by the tour $1, 0, 2, 3, 4$ with costs $1 + 1 + 2 + 2 + 2$. Two disjoint triangles have $n = 6$ and $\pi = 2$, so $\mathrm{OPT} = 8$. The Petersen graph on the [metric TSP](/metric-tsp/) page is the case $\pi = 1$ with no Hamiltonian cycle, where $\mathrm{OPT} = n + 1 = 11$. For Lemma 3, a gap between $\pi \le n/100$ and $\pi \ge 2n/100$ would give the bound $\frac{102}{101}$.

## Consequences

- **No PTAS.** The metric TSP has no polynomial-time approximation scheme unless P = NP. The hard metrics are far from geometric: in the plane, [Arora's scheme](/arora-euclidean-tsp-ptas/) gives a PTAS.
- **Asymmetric TSP.** With the triangle inequality but no symmetry, no ratio below $\frac{75}{74}$ is possible, by the same method. The best known algorithms for the [asymmetric TSP](/asymmetric-tsp/) have a constant ratio far above this bound.
- **Costs 1 and 2.** By Lemma 2, an approximation for (1,2)-TSP is an approximation for the path cover number with an additive $n$. The best ratio for (1,2)-TSP is $\frac87$, by Berman and Karpinski (2006).
- **What a better bound needs.** Each step in the line of results came from a reduction with smaller gadgets, not from a new PCP. A bound of $\frac43$, the conjectured integrality gap of the subtour LP, would need a different idea.

## Tightness

The lower bound is far from the upper bounds. [Christofides' algorithm](/christofides-algorithm/) has ratio $\frac32$, and [Karlin, Klein and Oveis Gharan](/karlin-klein-oveis-gharan-algorithm/) improved it to $\frac32 - 10^{-36}$. So the true threshold is somewhere between about $1.0082$ and $1.5$. Lemmas 2 and 3 are tight: Lemma 2 is an identity, and Lemma 3 turns a gap in $\pi$ into exactly the ratio $\frac{1 + b}{1 + a}$ of the two optimal costs.

## History

Papadimitriou and Yannakakis (1993) showed that TSP with costs 1 and 2 is MAX SNP-hard, which became a constant bound after the PCP theorem in 1992. Engebretsen gave the first explicit constant, $\frac{5381}{5380}$, in 1999, and Böckenhauer, Hromkovič, Klasing, Seibert and Unger raised it to $\frac{3813}{3812}$ in 2000. Papadimitriou and Vempala proved $\frac{220}{219}$ in 2000, with the journal version in 2006, together with $\frac{117}{116}$ for the asymmetric case. Lampis proved $\frac{185}{184}$ in 2012, and Karpinski, Lampis and Schmied proved $\frac{123}{122}$ and $\frac{75}{74}$ in 2013, with the journal version in 2015.

## References
