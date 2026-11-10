---
tag: E9MDHX
kind: definition
slug: element-frequency
name: Element frequency
aliases:
- frequency f of a set system
- maximum element frequency
area: approximation/covering-and-packing
level: core
summary: The frequency of an element is the number of sets that contain it, and f is the largest one; LP rounding and the primal-dual method give an f-approximation for set cover.
prereqs: [set-cover]
see_also: [set-cover-primal-dual, frequency-rounding-set-cover, set-cover, vertex-cover, hitting-set, greedy-set-cover, set-cover-inapproximability]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 1, Sections 1.3 to 1.5 (f = max_i |{j ∋ e_i}| and the f-approximations by rounding and by the primal-dual method)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 2, Section 2.2 (layering for set cover with frequency f), Chapter 14 and Chapter 15
  - paper: doi:10.1137/0211045
    title: Dorit S. Hochbaum, Approximation algorithms for the set covering and vertex cover problems, SIAM Journal on Computing 11(3), 1982
    locator: pages 555 to 556
  - paper: doi:10.1137/S0097539704443057
    title: Irit Dinur, Venkatesan Guruswami, Subhash Khot and Oded Regev, A new multilayered PCP and the hardness of hypergraph vertex cover, SIAM Journal on Computing 34(5), 2005
    locator: pages 1129 to 1146
---

The frequency of an element in a set system is the number of sets that contain it, and the frequency $f$ of the system is the largest frequency of an element. It measures how much the sets overlap at one point. For [set cover](/set-cover/), $f$ is the parameter of the LP-based algorithms: [frequency rounding](/frequency-rounding-set-cover/) and the [primal-dual algorithm](/set-cover-primal-dual/) both give ratio $f$, and $f = 2$ is [vertex cover](/vertex-cover/). The other natural parameter, the largest set size $d$, controls the [greedy algorithm](/greedy-set-cover/) instead, and the two parameters swap roles under the duality of set cover and [hitting set](/hitting-set/).

## Definition

Let $U$ be a universe of $n$ elements and $S_1, \ldots, S_m \subseteq U$ a family of sets. The **frequency** of an element $e \in U$ is

$$f_e = |\{ j : e \in S_j \}|,$$

the number of sets that contain $e$. The **frequency of the family** is $f = \max_{e \in U} f_e$. A family has **bounded frequency** $f$ if each element is in at most $f$ sets.

Three facts follow from the definition.

- **Sum.** $\sum_{e \in U} f_e = \sum_{j=1}^{m} |S_j|$, because both sides count the pairs $(e, j)$ with $e \in S_j$. So the average frequency is $s/n$, where $s$ is the total size of the input.
- **Range.** If the family covers $U$, then $1 \le f_e \le m$ for each $e$, so $1 \le f \le m$.
- **Duality.** Turn the family into its dual: one set $T_e$ for each element $e$, made of the indices $j$ with $e \in S_j$. Then $|T_e| = f_e$. So the frequency of the family equals the largest set size $d$ of the dual family, and the largest set size of the family equals the frequency of the dual. This is the duality between set cover and hitting set.

**Where it matters.** Let OPT be the least cost of a cover and LP* the optimum of the LP relaxation. The LP relaxation $\min \sum_j c_j x_j$ with $\sum_{j : e \in S_j} x_j \ge 1$ and $x \ge 0$ has a constraint with exactly $f_e$ variables for each element. If $x$ is feasible, then some $j \ni e$ has $x_j \ge 1/f_e \ge 1/f$. So taking each set with $x_j \ge 1/f$ gives a cover of cost at most $f \cdot \text{LP}^* \le f \cdot \text{OPT}$. This is the threshold rule of [frequency rounding](/frequency-rounding-set-cover/). The [primal-dual algorithm](/set-cover-primal-dual/) reaches the same ratio, and its proof uses that each element pays at most $f_e$ chosen sets. The ratio is close to the best possible: $f - 1 - \varepsilon$ is NP-hard for each fixed $f \ge 3$ (Dinur, Guruswami, Khot and Regev 2005), and $f - \varepsilon$ is hard under the [Unique Games Conjecture](/unique-games-conjecture/) (Khot and Regev 2008).

## Examples and non-examples

- **Vertex cover, $f = 2$.** For a graph, let the elements be the edges and let each vertex $v$ be the set of edges at $v$. Each edge has two endpoints, so each element has frequency exactly 2. Set cover with $f = 2$ is [weighted vertex cover](/weighted-vertex-cover/), and the $f$-approximations give the ratio 2.
- **Hypergraph vertex cover, $f = r$.** In an $r$-uniform hypergraph, each hyperedge has $r$ vertices. With the hyperedges as elements and the vertices as sets, each element has frequency $r$.
- **Dominating set, $f = \Delta + 1$.** In the set cover form of [dominating set](/dominating-set/), the sets are the closed neighbourhoods $N[v]$. A vertex $u$ is in $N[v]$ for $v = u$ and for each neighbour $v$, so $f_u = \deg(u) + 1$ and $f = \Delta + 1$. Here the set sizes are also $\Delta + 1$ at most, so greedy, with $H_{\Delta + 1}$, is better than $f$.
- **A small instance.** On the five sets $S_1 = \{1, 2, 3, 5\}$, $S_2 = \{3, 4, 6, 7\}$, $S_3 = \{2, 5, 6\}$, $S_4 = \{3, 7\}$ and $S_5 = \{1, 2, 4, 7\}$ of the [set cover](/set-cover/) page, the frequencies of the elements 1 to 7 are $2, 3, 3, 2, 2, 2, 3$. So $f = 3$. The sum is $17$, which equals $4 + 4 + 3 + 2 + 4$, the total size of the sets.
- **Disjoint sets, $f = 1$.** If the sets are pairwise disjoint and cover $U$, each element is in one set, and each set that holds an element must be chosen. The problem is trivial, and the ratio $f = 1$ says that the algorithms are exact.
- **The Fano plane, $f = 4$.** In the family of the seven sets $S_v = \{ u : u \cdot v \equiv 1 \pmod 2 \}$ over the non-zero vectors of $\{0, 1\}^3$, each element is in 4 sets and each set has 4 elements. Here OPT $= 3$, and the $f$-approximations only promise $4 \cdot \text{LP}^* = 7$.
- **Not the set size.** In a star with $n - 1$ leaves, the centre's set holds all $n - 1$ edges, so $d = n - 1$, but $f = 2$. Greedy gets the bound $H_{n-1}$ and the $f$-approximations get 2. In the other direction, the family of all singletons $\{e\}$ together with $U$ has $d = n$ but $f = 2$, and a family of many copies of one large set has $d = n$ and a large $f$.
- **Not the average.** The bound uses the largest frequency. A family where one element is in all $m$ sets and each other element is in one set has average frequency near 1, but $f = m$, and the $f$-approximations then promise only ratio $m$. The finer bound $\sum_e f_e y_e$ of the primal-dual proof can help here.

## Related definitions

- **Largest set size $d$.** The other parameter of set cover. The [greedy algorithm](/greedy-set-cover/) has ratio $H_d \le \ln d + 1$, which does not depend on $f$. Under the duality above, $d$ of a set cover instance is $f$ of the dual [hitting set](/hitting-set/) instance.
- **Degree of a hypergraph.** For a hypergraph, the degree of a vertex is the number of hyperedges that contain it. The frequency of an element is its degree in the hypergraph whose hyperedges are the sets.
- **Rank of a hypergraph.** The largest size of a hyperedge. In the hitting set view, the rank is the parameter $f$ of the matching set cover instance.
- **Integrality gap.** The LP relaxation has an integrality gap at most $f$, by the threshold rule. This is why the LP is useful when $f$ is small, while for large $f$ the gap can be $\Omega(\log n)$, as in the Fano plane family of the [set cover](/set-cover/) page.

## References
