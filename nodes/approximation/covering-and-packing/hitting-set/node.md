---
tag: JC1NM5
kind: problem
slug: hitting-set
name: Hitting set problem
aliases:
- transversal problem
- minimum hitting set
- hypergraph vertex cover
area: approximation/covering-and-packing
level: intro
summary: Choose the fewest elements that meet every set of a family; it is set cover with the roles of elements and sets swapped.
prereqs: [set-cover, hypergraph, np-complete]
see_also: [set-cover, element-frequency, vertex-cover, parameterized-hitting-set, minimal-transversal-enumeration, greedy-set-cover, set-cover-primal-dual, vc-dimension]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability
    locator: Appendix A3.1, problem SP8 (hitting set), NP-complete by a reduction from vertex cover
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 1, Section 1.2 (set cover and the vertex cover special case) and Chapter 7 (the primal-dual method, stated for hitting set problems)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 2 (set cover)
  - paper: doi:10.1137/S0097539704443057
    title: Irit Dinur, Venkatesan Guruswami, Subhash Khot and Oded Regev, A new multilayered PCP and the hardness of hypergraph vertex cover, SIAM Journal on Computing 34(5), 2005
    locator: pages 1129 to 1146 (k − 1 − ε is NP-hard for k-uniform hypergraphs, k ≥ 3)
---

The hitting set problem gives a family of sets over a ground set and asks for a smallest set of ground elements that meets, or "hits", every set of the family. In the language of [hypergraphs](/hypergraph/) it asks for a smallest transversal, also called a hypergraph vertex cover. Hitting set and [set cover](/set-cover/) are the same problem with the roles of elements and sets swapped, so each algorithm and each hardness result for one carries over to the other, with the parameters exchanged. [Vertex cover](/vertex-cover/) is the case where each set has two elements.

## In plain words

You have some groups of items, and you must pick items so that each group contains at least one picked item. You want to pick as few items as possible.

Turn the picture around: for each item, list the groups it belongs to. Picking an item now means buying its list, and each group must appear in some bought list. This is the problem of covering all groups with few lists, which is set cover. So the two problems are one problem seen from two sides.

## Definition

**Input.** A ground set $V$ of $n$ elements, a family of $m$ sets $T_1, \ldots, T_m \subseteq V$, and in the weighted version a cost $c_v \ge 0$ for each $v \in V$.

**Output.** A set $H \subseteq V$ with $H \cap T_i \neq \emptyset$ for each $i$, a *hitting set* or *transversal*.

**Goal.** Minimize $|H|$, or $c(H) = \sum_{v \in H} c_v$. OPT is the least value, and the ratio convention is ALG $\le \rho \cdot$ OPT. If some $T_i$ is empty, no hitting set exists.

The parameters are the largest set size $k = \max_i |T_i|$ and the largest degree $D = \max_v |\{ i : v \in T_i \}|$. The *$k$-hitting set* problem has $|T_i| \le k$ for each $i$. The least size of a transversal of a hypergraph $\mathcal{H}$ is written $\tau(\mathcal{H})$.

**Integer program.** With $x_v = 1$ when $v \in H$,

$$\min \sum_{v \in V} c_v x_v \quad \text{subject to} \quad \sum_{v \in T_i} x_v \ge 1 \text{ for each } i, \quad x_v \in \{0, 1\}.$$

This is the set cover program with the matrix transposed. Its dual is a fractional packing of the sets $T_i$.

**The equivalence with set cover.** Given a hitting set instance, build a set cover instance whose universe is $\{1, \ldots, m\}$, the indices of the sets, with one set $S_v = \{ i : v \in T_i \}$ of cost $c_v$ for each $v \in V$. Then $H \subseteq V$ hits each $T_i$ if and only if $\bigcup_{v \in H} S_v = \{1, \ldots, m\}$, because $i \in S_v$ means $v \in T_i$. The map keeps the cost, so it keeps OPT and each ratio. The same construction, read the other way, turns set cover into hitting set. Under the map:

| hitting set | set cover |
|---|---|
| ground element $v$ | set $S_v$ |
| set $T_i$ | element $i$ |
| largest set size $k$ | largest [element frequency](/element-frequency/) $f$ |
| largest degree $D$ | largest set size $d$ |

## Variants

- **$k$-hitting set.** Each set has at most $k$ elements. This is set cover with frequency $f = k$, and it is the vertex cover problem of a $k$-uniform hypergraph when each set has exactly $k$ elements.
- **Vertex cover.** The case $k = 2$: the sets are the edges of a graph. See [vertex cover](/vertex-cover/) and [weighted vertex cover](/weighted-vertex-cover/).
- **Implicit families.** Many problems are hitting set problems with a family that is given implicitly: [feedback vertex set](/feedback-vertex-set-problem/) hits all cycles, [odd cycle transversal](/odd-cycle-transversal/) hits all odd cycles, and a multicut hits, with edges, all paths between the terminal pairs. The primal-dual method handles such families with a separation step.
- **Geometric hitting set.** Hit a family of ranges, such as disks or rectangles, with points. With bounded [VC dimension](/vc-dimension/), epsilon-nets give an $O(\log \text{OPT})$-approximation (Brönnimann and Goodrich 1995).
- **Enumeration.** List all minimal hitting sets. This is the [minimal transversal enumeration](/minimal-transversal-enumeration/) problem, also called hypergraph dualization.
- **Parameterized.** Decide whether a hitting set of size at most $t$ exists. For fixed $k$, branching on the elements of an unhit set gives $O(k^t \cdot \text{poly})$ time; see [parameterized hitting set](/parameterized-hitting-set/).

## Examples

**A small instance.** Let $V = \{a, b, c, d, e\}$ and

| set | elements |
|---|---|
| $T_1$ | $a, b$ |
| $T_2$ | $b, c$ |
| $T_3$ | $c, d$ |
| $T_4$ | $a, d, e$ |
| $T_5$ | $e$ |

The set $T_5$ forces $e \in H$. Then $T_1$, $T_2$ and $T_3$ must be hit by elements of $\{a, b, c, d\}$, and no one element is in all three, so two more elements are needed. So OPT $= 3$, for example $H = \{b, d, e\}$. Here $k = 3$ and $D = 2$. The matching set cover instance has the universe $\{1, 2, 3, 4, 5\}$ and the sets $S_a = \{1, 4\}$, $S_b = \{1, 2\}$, $S_c = \{2, 3\}$, $S_d = \{3, 4\}$ and $S_e = \{4, 5\}$; the cover $\{S_b, S_d, S_e\}$ matches $H$. The greedy algorithm, which picks the element in the most unhit sets with ties to the first letter, takes $a$, then $c$, then $e$, and also finds an optimal set.

**Vertex cover.** For a graph, the sets are the edges, so $k = 2$. A hitting set is a vertex cover, and the 2-approximations of vertex cover are the $k$-approximations below with $k = 2$.

**The Fano plane.** The seven lines of the Fano plane, each with three points, form a 3-uniform family in which each point is on three lines. Two points $p$ and $q$ are not enough: three lines pass through $p$, three through $q$, and exactly one through both, so only 5 of the 7 lines are hit. A whole line is a hitting set, because two lines of the Fano plane always meet. So $\tau = 3$.

## Known algorithms

| algorithm | ratio | lower bound used |
|---|---|---|
| Greedy, the element in the most unhit sets ([greedy set cover](/greedy-set-cover/) on the dual) | $H_D \le \ln D + 1$ | LP*, by dual fitting |
| [Primal-dual](/set-cover-primal-dual/) on the dual | $k$ | a fractional packing of the sets |
| [Frequency rounding](/frequency-rounding-set-cover/): take each $v$ with $x_v \ge 1/k$ | $k$ | LP* |
| Branching on an unhit set | exact, $O(k^t \cdot \text{poly})$ for answer size $t$ | none |

All ratios hold in the worst case. The LP has one row for each set and is solved in polynomial time; for implicit families with exponentially many sets, a separation oracle is needed.

## Bounds

- **NP-hardness.** Hitting set is NP-complete, even for $k = 2$, where it is vertex cover (Karp 1972; Garey and Johnson, problem SP8).
- **Hardness for general families (cited).** By the equivalence, the hardness of set cover carries over: no $(1 - \varepsilon) \ln m$-approximation exists unless P = NP, where $m$ is the number of sets to hit (Dinur and Steurer 2014); see [set cover inapproximability](/set-cover-inapproximability/).
- **Hardness for $k$-hitting set (cited).** For each fixed $k \ge 3$, a $(k - 1 - \varepsilon)$-approximation is NP-hard (Dinur, Guruswami, Khot and Regev 2005), and a $(k - \varepsilon)$-approximation is hard under the [Unique Games Conjecture](/unique-games-conjecture/) (Khot and Regev 2008). For $k = 2$ see [vertex cover inapproximability](/vertex-cover-inapproximability/).
- **Upper bounds (proved on the linked pages).** $H_D$ on the [greedy set cover](/greedy-set-cover/) page and $k$ on the [primal-dual set cover](/set-cover-primal-dual/) page.
- **Fractional duality.** The least size of a fractional hitting set equals the largest size of a fractional packing of the sets, by [LP duality](/lp-duality/). The integral numbers satisfy $\nu \le \tau$, where $\nu$ is the largest number of pairwise disjoint sets, and $\tau \le k \nu$, because the union of the sets of a maximal disjoint subfamily is a hitting set.

## Reductions

- **To and from set cover.** The equivalence above maps instances both ways in linear time and keeps the cost of each solution, so it is an exact, approximation-preserving reduction.
- **From vertex cover.** A graph gives the 2-hitting set instance of its edges. This proves NP-hardness for $k = 2$.
- **From triangle problems.** Hitting set with $k = 3$ includes the problem of hitting all triangles of a graph and the feedback vertex set problem in tournaments, which hits all directed triangles.
- **Dualization.** The family of minimal hitting sets of a family is its *blocker*, and the blocker of the blocker is the family of its minimal sets. This is the basis of [minimal transversal enumeration](/minimal-transversal-enumeration/).

## Applications

- **Model-based diagnosis.** Each conflict set is a set of components that cannot all work, and a diagnosis is a minimal hitting set of the conflict sets (Reiter 1987).
- **Test and probe selection.** Choose the fewest tests so that each fault is detected by some test.
- **Breaking cycles.** Choosing vertices or edges to break all cycles, all odd cycles or all short cycles is a hitting set problem with an implicit family.
- **Data mining and databases.** Minimal keys of a relation and minimal infrequent itemsets are minimal transversals of derived families.

## References
