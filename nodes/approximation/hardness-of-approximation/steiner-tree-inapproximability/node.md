---
tag: 46CJ97
kind: theorem
slug: steiner-tree-inapproximability
name: Steiner tree inapproximability
aliases:
- Steiner tree hardness 96/95
- APX-hardness of Steiner tree
- Bern-Plassmann Steiner tree hardness
area: approximation/hardness-of-approximation
level: advanced
summary: Steiner tree is APX-hard already with edge lengths 1 and 2 (Bern and Plassmann 1989, proved here), and a ratio below 96/95 is NP-hard (Chlebík and Chlebíková 2008).
prereqs: [steiner-tree-problem, vertex-cover, l-reduction, apx-class, minimum-spanning-tree]
see_also: [vertex-cover-inapproximability, apx-completeness, ptas, planar-steiner-tree-ptas, steiner-forest, metric-tsp-inapproximability, set-cover-inapproximability, gadget-reduction]
sources:
  - paper: doi:10.1016/0020-0190(89)90039-2
    title: Marshall Bern and Paul Plassmann, The Steiner problem with edge lengths 1 and 2, Information Processing Letters 32(4), 1989
    locator: the reduction from vertex cover in graphs of bounded degree and the MAX SNP-hardness
  - paper: doi:10.1016/j.tcs.2008.06.046
    title: Miroslav Chlebík and Janka Chlebíková, The Steiner tree problem on graphs, inapproximability results, Theoretical Computer Science 406(3), 2008
    locator: the main theorem, ratio 96/95 is NP-hard (the computed bound is 1.01063)
  - paper: doi:10.1016/0022-0000(91)90023-X
    title: Christos H. Papadimitriou and Mihalis Yannakakis, Optimization, approximation, and complexity classes, Journal of Computer and System Sciences 43(3), 1991
    locator: MAX SNP-hardness of vertex cover in graphs of bounded degree
  - paper: "J. Byrka, F. Grandoni, T. Rothvoß and L. Sanità, Steiner tree approximation via iterative randomized rounding, Journal of the ACM 60(1), 2013"
    locator: the ratio ln 4 + ε
  - paper: "L. Trevisan, Inapproximability of combinatorial optimization problems, arXiv cs/0409043, 2004"
    locator: Section 4.3 (the Bern and Plassmann reduction as an example of an L-reduction)
  - paper: "E. Halperin and R. Krauthgamer, Polylogarithmic inapproximability, Proceedings of the 35th ACM Symposium on Theory of Computing (STOC), 2003"
    locator: group Steiner tree, ratio log^(2 - ε) n
  - book: isbn:9783540654315
    title: G. Ausiello, P. Crescenzi, G. Gambosi, V. Kann, A. Marchetti-Spaccamela and M. Protasi, Complexity and Approximation
    locator: Appendix B, compendium entry ND8 (minimum Steiner tree)
---

The Steiner tree problem asks for a cheapest tree that connects a set of terminals in a weighted graph, and it may use other vertices. It has constant-factor algorithms, the best with ratio $\ln 4 + \varepsilon \approx 1.39$, but no [PTAS](/ptas/) unless P = NP. Bern and Plassmann (1989) proved this, the APX-hardness, with a simple [L-reduction](/l-reduction/) from [vertex cover](/vertex-cover/) in graphs of bounded degree: the terminals are the edges of the graph, the Steiner points are its vertices, and all distances are 1 or 2. This page proves that reduction in full. The best known explicit bound, that a ratio below $\frac{96}{95}$ is NP-hard, is due to Chlebík and Chlebíková (2008) and is cited.

## Statement

An instance of the [Steiner tree problem](/steiner-tree-problem/) has a graph with nonnegative edge lengths and a set $T$ of terminals. A Steiner tree is a tree in the graph that contains all of $T$, and its cost is the sum of its edge lengths. Other vertices are *Steiner points*. For this minimization problem, a ratio $\rho \ge 1$ means $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. The case with lengths 1 and 2 means a complete graph in which every edge has length 1 or 2; such lengths always form a metric.

For a graph $G$, $\tau(G)$ is the least size of a vertex cover.

**Theorem.**

1. *(Bern and Plassmann 1989.)* For a connected graph $G$ with $m \ge 2$ edges there is a Steiner instance $I(G)$ with lengths 1 and 2, built in polynomial time, with $\mathrm{OPT}(I(G)) = m + \tau(G) - 1$. Each Steiner tree of cost $c$ gives, in polynomial time, a vertex cover with at most $c - m + 1$ vertices. If $G$ has largest degree $\Delta$, this is an L-reduction with $\alpha = \Delta + 1$ and $\beta = 1$.
2. *(Consequence.)* Steiner tree with lengths 1 and 2 is APX-hard, so it has no PTAS unless P = NP.
3. *(Chlebík and Chlebíková 2008, cited.)* A polynomial algorithm with ratio below $\frac{96}{95}$ for Steiner tree gives P = NP.

## In plain words

Take a network of roads and crossings and ask for the fewest crossings that touch every road. Make a new puzzle: each road becomes a town that must be joined, and each crossing becomes an optional hub. A town and the two hubs at the ends of its road are one step apart. Everything else is two steps apart, except that two hubs are one step apart.

A good set of crossings gives a cheap tree: link the chosen hubs in a row, then hang every town on a chosen hub at one step. Each town costs one step, and each extra hub costs one more. In the other direction, any tree pays an extra step for each town that has no chosen hub next to it. So the cheapest tree tells you the fewest crossings, and the fewest crossings is hard to approximate well.

## Proof

*The construction.* Let $G = (V, E)$ be connected with $n$ vertices and $m \ge 2$ edges. The instance $I(G)$ is the complete graph on $V \cup E$, with terminals $T = E$ and Steiner points $V$. The lengths are

$$\ell(v, v') = 1, \qquad \ell(v, e) = \begin{cases} 1 & v \in e, \\ 2 & v \notin e, \end{cases} \qquad \ell(e, e') = 2$$

for distinct $v, v' \in V$ and $e, e' \in E$. The instance has $n + m$ points, so the map takes polynomial time. All lengths are 1 or 2, so they satisfy the triangle inequality.

*Upper bound.* Let $C$ be a vertex cover with $|C| = \tau(G) \ge 1$. Join the vertices of $C$ in a path, which costs $|C| - 1$. Attach each terminal $e$ to an end of $e$ that lies in $C$, at length 1. The result is a Steiner tree of cost $m + \tau(G) - 1$.

*Lower bound and the solution map.* Let $Y$ be a Steiner tree, let $S \subseteq V$ be the Steiner points in $Y$, and let $u(S)$ be the number of edges of $G$ with no end in $S$. Then $S$ together with one end of each such edge is a vertex cover with at most $|S| + u(S)$ vertices. We show that $\mathrm{cost}(Y) \ge m + |S| + u(S) - 1$.

- If $S \neq \emptyset$, root $Y$ at a point of $S$. Each of the other $m + |S| - 1$ points has one edge to its parent, and these are all the edges of $Y$. Each has length at least 1. Let $e$ be a terminal with no end in $S$. Its parent is a terminal or a Steiner point not in $e$, so its parent edge has length 2. So the cost is at least $(m + |S| - 1) + u(S)$.
- If $S = \emptyset$, then $Y$ is a tree on the $m$ terminals, with $m - 1$ edges of length 2, so its cost is $2m - 2$. Here $u(S) = m$, and the bound would need $2m - 2 \ge 2m - 1$, which is false, so we use a better cover. Since $G$ is connected and $m \ge 2$, some vertex $x$ is on two edges. Then $x$ together with one end of each of the other $m - 2$ edges is a vertex cover with at most $m - 1 = \mathrm{cost}(Y) - m + 1$ vertices.

In both cases the cover has at most $\mathrm{cost}(Y) - m + 1$ vertices. With $\mathrm{cost}(Y) = \mathrm{OPT}$, this gives $\tau(G) \le \mathrm{OPT} - m + 1$, and with the upper bound, $\mathrm{OPT}(I(G)) = m + \tau(G) - 1$.

*The L-reduction.* If $G$ has largest degree $\Delta$, each vertex covers at most $\Delta$ edges, so $\tau(G) \ge m / \Delta$, and

$$\mathrm{OPT}(I(G)) = m + \tau(G) - 1 < (\Delta + 1) \tau(G).$$

This is the first condition with $\alpha = \Delta + 1$. For a tree of cost $c$, the cover $C$ from the solution map has $|C| - \tau(G) \le (c - m + 1) - (\mathrm{OPT} - m + 1) = c - \mathrm{OPT}$, which is the second condition with $\beta = 1$. This proves part 1.

*Part 2.* Vertex cover in graphs of largest degree $\Delta$ is APX-hard for a fixed $\Delta$ (Papadimitriou and Yannakakis 1991, with the [PCP theorem](/pcp-theorem/)), also when restricted to connected graphs with at least 2 edges, because a cover of a disjoint union is a union of covers. An L-reduction from an APX-hard problem shows APX-hardness. Explicitly: if a Steiner algorithm has ratio $1 + \eta$, then the cover it gives has $|C| - \tau \le \eta \, \mathrm{OPT} < \eta (\Delta + 1) \tau$, so vertex cover gets ratio $1 + (\Delta + 1)\eta$. A PTAS for Steiner tree would give a PTAS for vertex cover in these graphs, and so P = NP. $\blacksquare$

*Part 3 (cited).* Chlebík and Chlebíková reduce from Håstad's hardness of Max-E3-LIN-2 with gadgets and bounded-degree expanders, and compute the bound $1.01063 > \frac{96}{95}$. The proof is not given here.

### Example

For the path $0 - 1 - 2 - 3$, with $m = 3$ and $\tau = 2$, the optimum is $3 + 2 - 1 = 4$: join the hubs 1 and 2, and hang the three terminals on them. For the triangle, $m = 3$ and $\tau = 2$, so the optimum is again 4. Here a tree on the three terminals alone, with two edges of length 2, also costs 4, which is why the case $S = \emptyset$ needs the separate argument. The code for this page checks the formula $\mathrm{OPT} = m + \tau - 1$ and the solution map by brute force over all sets of Steiner points.

## Consequences

- **No PTAS in graphs.** Steiner tree in graphs, and already in the metric with lengths 1 and 2, has no PTAS unless P = NP. This contrasts with the Euclidean plane, where Arora and Mitchell gave PTASs, and with planar graphs, where a [PTAS](/planar-steiner-tree-ptas/) exists.
- **Related problems.** [Steiner forest](/steiner-forest/) contains Steiner tree, so it is APX-hard too. Node-weighted Steiner tree contains [set cover](/set-cover-inapproximability/) and has the threshold $\Theta(\log n)$. Group Steiner tree has no ratio $\log^{2 - \varepsilon} n$ unless NP has quasi-polynomial randomized algorithms (Halperin and Krauthgamer 2003).
- **The same pattern for TSP.** A graph with lengths 1 and 2 also gives the APX-hardness of the [metric TSP](/metric-tsp-inapproximability/), where edges of length 1 are the edges of a sparse graph.

## Tightness

The gap is wide. The best ratio is $\ln 4 + \varepsilon \approx 1.39$ (Byrka, Grandoni, Rothvoß and Sanità 2013), and the best hardness is $\frac{96}{95} \approx 1.0105$. For lengths 1 and 2, Bern and Plassmann also gave an algorithm with ratio $\frac43$.

The reduction of part 1 loses the factor $\Delta + 1$, so it gives only a small explicit constant. With $\tau \ge m / \Delta$, a vertex cover gap of $1$ against $1 + \delta$ becomes a Steiner gap of about $1$ against $1 + \delta \frac{\tau}{m + \tau}$, which is at least $1 + \frac{\delta}{\Delta + 1}$ but is close to this value when $\tau$ is close to $m/\Delta$, as in regular graphs. The constant $\frac{96}{95}$ comes from a more careful reduction.

## History

Karp (1972) proved that Steiner tree in graphs is NP-complete. Bern and Plassmann (1989) proved that the case with lengths 1 and 2 is MAX SNP-hard, which became APX-hardness with the PCP theorem (1992). Chlebík and Chlebíková gave the first explicit bound in 2002, in a SWAT paper, and the journal version (2008) states $\frac{96}{95}$. On the algorithm side, the ratio 2 of the MST heuristic was improved step by step, to $\ln 4 + \varepsilon$ in 2010.

## References
