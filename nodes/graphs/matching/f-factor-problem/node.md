---
tag: X5TB7N
kind: problem
slug: f-factor-problem
name: f-factor problem
aliases:
- general factor problem
area: graphs/matching
level: advanced
summary: Find a spanning subgraph in which each vertex v has degree exactly f(v).
prereqs: [b-matching]
see_also: [perfect-matching, tutte-theorem, petersens-theorem, edmonds-blossom, micali-vazirani-algorithm, max-flow-problem, hamiltonian-cycle-problem, regular-graph]
sources:
  - paper: doi:10.4153/CJM-1952-028-2
    title: William T. Tutte, The factors of graphs, Canadian Journal of Mathematics 4, 314 to 328 (1952)
    locator: the whole paper (the f-factor theorem)
  - paper: doi:10.4153/CJM-1954-033-3
    title: William T. Tutte, A short proof of the factor theorem for finite graphs, Canadian Journal of Mathematics 6, 347 to 352 (1954)
    locator: the whole paper (the reduction of f-factors to perfect matchings)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.3, Matchings in general graphs (f-factors and Tutte's reduction to 1-factors)
  - book: isbn:9780821847596
    title: László Lovász and Michael D. Plummer, Matching Theory, AMS Chelsea Publishing (2009 reprint of the 1986 edition)
    locator: Chapter 10, The f-factor problem
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 33, Simple b-matchings and b-factors
---

The f-factor problem gives each vertex $v$ of a [graph](/graph/) a target degree $f(v)$ and asks for a set of edges $F$ in which every vertex $v$ has exactly $f(v)$ edges. With $f \equiv 1$ it is the [perfect matching](/perfect-matching/) problem, and with $f \equiv 2$ it asks for a 2-factor, a spanning set of disjoint cycles. It is the perfect case of the simple [b-matching](/b-matching/) problem. Tutte characterized the graphs that have an f-factor and reduced the problem to perfect matching, so it is solvable in polynomial time in general graphs; the page covers bipartite and general graphs, without weights and with them.

## In plain words

Each point of a network has a number, and you must keep some of the links so that every point ends up with exactly its number of links. If every number is one, you are pairing up all the points. If every number is two, you are covering the points with closed loops.

Some demands are impossible for simple reasons: a point cannot keep more links than it has, and the numbers must add up to an even total, since each link is counted at both ends. Tutte found the full rule that decides when the demands can be met, and a trick that turns the question into pairing up the points of a larger network.

## Definition

**Input.** A finite undirected graph $G = (V, E)$, bipartite or general, and a function $f: V \to \mathbb{Z}_{\ge 0}$. Optionally, edge weights $w: E \to \mathbb{R}$.

**Output.** A set $F \subseteq E$ with $\deg_F(v) = f(v)$ for every $v \in V$, an *f-factor*, or the answer that none exists. In the weighted version, an f-factor of least or greatest weight.

**Necessary conditions.** $f(v) \le \deg_G(v)$ for each $v$, and $f(V) = \sum_v f(v)$ is even, since $f(V) = 2|F|$. A *k-factor* is an f-factor with $f \equiv k$. For $V = \emptyset$ the empty set is an f-factor.

**Tutte's f-factor theorem (1952).** For disjoint $S, T \subseteq V$, let $q(S, T)$ be the number of components $C$ of $G - S - T$ for which $f(C) + e(C, T)$ is odd, where $e(C, T)$ is the number of edges between $C$ and $T$, and let

$$\delta(S, T) = f(S) - f(T) + \sum_{v \in T} \deg_{G - S}(v) - q(S, T).$$

Then $G$ has an f-factor if and only if $\delta(S, T) \ge 0$ for all disjoint $S$ and $T$. Moreover $\delta(S, T) \equiv f(V) \pmod 2$. For $f \equiv 1$ and $T = \emptyset$ the condition is $|S| \ge q(G - S)$, [Tutte's theorem](/tutte-theorem/).

*Why the condition is necessary.* Let $F$ be an f-factor, $R = V \setminus (S \cup T)$, and write $e_F(X, Y)$ and $e_{\bar F}(X, Y)$ for the numbers of edges between $X$ and $Y$ that are in $F$ and not in $F$. At $S$, $f(S) \ge e_F(S, T) + e_F(S, R)$. At $T$, $\sum_{v \in T} \deg_{G-S}(v) - f(T)$ counts the edges at $T$ that avoid $S$ and are not in $F$, minus $e_F(T, S)$, and so is at least $e_{\bar F}(T, R) - e_F(T, S)$. Hence $\delta(S, T) + q(S, T) \ge e_F(S, R) + e_{\bar F}(T, R)$. For a component $C$ of $G[R]$, $f(C) = 2e_F(C, C) + e_F(C, S) + e_F(C, T)$, so if $f(C) + e(C, T)$ is odd then $e_F(C, S) + e_{\bar F}(C, T)$ is odd, hence at least 1. Summing over the $q(S, T)$ such components gives $\delta(S, T) \ge 0$.

## Variants

- **k-factors.** $f \equiv k$. A 1-factor is a perfect matching. Petersen's 2-factor theorem: every $2k$-regular graph has a 2-factor, and so decomposes into $k$ of them. [Petersen's theorem](/petersens-theorem/) gives a 1-factor in every bridgeless cubic graph.
- **Connected factors.** A connected 2-factor is a Hamiltonian cycle, and finding one is the [NP-hard](/np-hard/) [Hamiltonian cycle problem](/hamiltonian-cycle-problem/). Connectivity is what separates the two: 2-factors are found in polynomial time.
- **Interval factors.** $a(v) \le \deg_F(v) \le b(v)$, the $(a, b)$-factor problem; Lovász gave a theorem of Tutte's type for it, and it reduces to f-factors with extra slack vertices.
- **General factors.** A set $B_v$ of allowed degrees at each vertex. Lovász introduced the problem; Cornuéjols showed it is polynomial when no set has a gap of two or more consecutive missing values, and NP-complete otherwise, for example with $B_v = \{0, 3\}$.
- **Weighted f-factors.** Least weight f-factor, solved by weighted perfect matching on Tutte's gadget, or by Gabow's direct algorithms.
- **Uncapacitated.** Edges may be used several times: a perfect uncapacitated b-matching, which has a simpler condition with odd components only.

## Examples

**Triangle.** With $f \equiv 1$, $f(V) = 3$ is odd: no 1-factor. With $f \equiv 2$, the whole triangle is the unique 2-factor.

**Star $K_{1,3}$, centre $c$.** With $f(c) = 3$ and $f = 1$ at the leaves, the whole star is the f-factor. With $f \equiv 1$, $f(V) = 4$ is even and every degree bound holds, yet no 1-factor exists: for $S = \{c\}$ and $T = \emptyset$, the three leaves are components with $f(C) = 1$ odd, so $q = 3$ and $\delta = 1 - 0 + 0 - 3 = -2 < 0$.

**$K_4$.** With $f \equiv 1$: three 1-factors. With $f \equiv 2$: three 2-factors, each a Hamiltonian 4-cycle. With $f \equiv 3$: the whole graph.

**The Petersen graph.** It is cubic and bridgeless, so it has a 1-factor, and the complement of a 1-factor is a 2-factor, two disjoint 5-cycles. It has no Hamiltonian cycle, so its 2-factors are never connected, which shows the gap between 2-factors and Hamiltonian cycles.

**No edges.** With $E = \emptyset$, an f-factor exists only if $f \equiv 0$, and then it is empty.

**Bipartite.** In the path $a\,b\,c$ with $f(a) = f(c) = 1$ and $f(b) = 2$, the whole path is the f-factor; with $f(b) = 1$ and $f(a) = f(c) = 1$, $f(V) = 3$ is odd and none exists.

## Known algorithms

- **Bipartite graphs, by flow.** With sides $X$ and $Y$, a source arc of capacity $f(u)$ to each $u \in X$, a unit arc for each edge, and an arc of capacity $f(v)$ from each $v \in Y$ to the sink. An f-factor exists if and only if the [maximum flow](/max-flow-problem/) equals $f(X) = f(Y)$. Weighted: [min-cost flow](/min-cost-flow-problem/).
- **Tutte's gadget, general graphs.** For each edge $uv$, create an outer vertex at each end, $o_{uv}^u$ and $o_{uv}^v$, joined by an edge. For each vertex $v$, create $\deg(v) - f(v)$ inner vertices and join each of them to all $\deg(v)$ outer vertices at $v$. Then $G$ has an f-factor if and only if the new graph $G'$ has a perfect matching: an edge $uv$ is in $F$ exactly when its two outer vertices are matched to each other, and the inner vertices at $v$ absorb the $\deg(v) - f(v)$ edges at $v$ that are left out. $G'$ has at most $4|E|$ vertices and $|E| + \sum_v \deg(v)(\deg(v) - f(v))$ edges, so [Edmonds' blossom algorithm](/edmonds-blossom/) or the [Micali-Vazirani algorithm](/micali-vazirani-algorithm/) solves the problem in polynomial time. Weighted matching on $G'$, with weight $w(uv)$ on the edge between the two outer vertices of $uv$, solves the weighted version.
- **Copies gadget.** Alternatively, replace each vertex by $f(v)$ copies and each edge by a path of three edges, as on the [b-matching](/b-matching/) page; this is pseudo-polynomial in $f$.
- **Direct algorithms.** Gabow gave blossom-style algorithms for f-factors that work on a graph of size $O(|E|)$ without expanding the degrees, and extended them to the weighted case.

## Bounds

- **Upper bound.** Polynomial in $|V|$ and $|E|$, since $f(v) \le \deg(v)$ keeps the gadget small: one perfect matching computation on Tutte's gadget, which has $O(|E|)$ vertices and $O(\sum_v \deg(v)^2)$ edges.
- **Certificate.** If no f-factor exists, a pair $(S, T)$ with $\delta(S, T) < 0$ proves it, and such a pair can be read off a failed search on the gadget; if one exists, the factor itself is the proof. So the problem has a good characterization, in $\mathsf{NP} \cap \mathsf{coNP}$, as Tutte's theorem showed before the algorithms.

## Reductions

- **From perfect matching:** $f \equiv 1$.
- **To perfect matching:** Tutte's gadget, above, with $O(|E|)$ vertices.
- **To max flow,** for bipartite graphs.
- **2-factors and Hamiltonicity:** a Hamiltonian cycle is a connected 2-factor, so the 2-factor problem is a polynomial relaxation of the [Hamiltonian cycle problem](/hamiltonian-cycle-problem/).

## Applications

- Testing degree sequences: a graph with degree sequence $d$ inside a host graph $H$ is an f-factor of $H$ with $f = d$; with $H$ complete this is the Erdős-Gallai question.
- Network design with exact degree requirements, such as overlays where each node keeps exactly $k$ links.
- The 2-factor relaxation of the travelling salesman problem, and cycle covers in approximation algorithms for TSP variants.
- Scheduling and timetabling, where each team or resource must take part in exactly $f(v)$ events, as in round-robin tournament construction from 1-factors of $K_{2n}$.

## References
