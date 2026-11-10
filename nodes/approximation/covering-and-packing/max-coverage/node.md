---
tag: BKGE2P
kind: problem
slug: max-coverage
name: Maximum coverage problem
aliases:
- maximum coverage
- max k-cover
area: approximation/covering-and-packing
level: intro
summary: Choose k sets from a family to cover as many elements as possible; NP-hard, greedy gives 1 − 1/e, and 1 − 1/e + ε is NP-hard.
prereqs: [set-cover, submodular-function, np-hard]
see_also: [greedy-max-coverage, nemhauser-wolsey-fisher-theorem, set-cover, max-coverage-inapproximability, submodular-function, pipage-rounding, greedy-influence-maximization, facility-location-problem]
sources:
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 3 (approximating covering and packing problems, the maximum coverage section)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 2, Section 2.5 (maximizing float in bank accounts, a coverage-type problem and its greedy 1 − 1/e analysis)
  - paper: doi:10.1007/BF01588971
    title: George L. Nemhauser, Laurence A. Wolsey and Marshall L. Fisher, An analysis of approximations for maximizing submodular set functions I, Mathematical Programming 14(1), 1978
    locator: pages 265 to 294
  - paper: doi:10.1145/285055.285059
    title: Uriel Feige, A threshold of ln n for approximating set cover, Journal of the ACM 45(4), 1998
    locator: pages 634 to 652 (maximum coverage is NP-hard to approximate within 1 − 1/e + ε)
  - title: Samir Khuller, Anna Moss and Joseph Naor, The budgeted maximum coverage problem, Information Processing Letters 70(1), 1999
    locator: pages 39 to 45
  - title: Alexander A. Ageev and Maxim I. Sviridenko, Pipage rounding, a new method of constructing algorithms with proven performance guarantee, Journal of Combinatorial Optimization 8(3), 2004
    locator: pages 307 to 328 (the ratio 1 − (1 − 1/f)^f when each element is in at most f sets)
---

The maximum coverage problem gives a family of sets and a number $k$, and asks for $k$ sets whose union is as large as possible. It is the budget version of [set cover](/set-cover/): set cover asks how many sets are needed to cover everything, and maximum coverage asks how much $k$ sets can cover. The problem is NP-hard. The [greedy algorithm](/greedy-max-coverage/) covers at least $1 - 1/e \approx 0.632$ of the optimum, and Feige (1998) proved that no polynomial-time algorithm does better by a constant unless P = NP. The number of covered elements is a monotone [submodular function](/submodular-function/) of the chosen sets, and maximum coverage is the standard example of submodular maximization.

## In plain words

You have a list of groups, each holding some items, and you may pick only a fixed number of groups. You want the picked groups, together, to hold as many different items as possible. An item counts once, even if several picked groups hold it.

The hard part is the overlap. The two largest groups can hold almost the same items, so the best pair may be two smaller groups that do not overlap. Checking all choices takes too long for large lists, but picking one group at a time, each time the one that adds the most new items, is always close to the best.

## Definition

**Input.** A universe $U$ of $n$ elements, a family of $m$ sets $S_1, \ldots, S_m \subseteq U$, and an integer $k$ with $1 \le k \le m$. In the weighted version, each element $e$ has a weight $w_e \ge 0$.

**Output.** A set $C$ of at most $k$ indices.

**Goal.** Maximize the number of covered elements, $\text{cov}(C) = |\bigcup_{j \in C} S_j|$, or the covered weight $\sum_{e \in \bigcup_{j \in C} S_j} w_e$.

OPT is the largest value of $\text{cov}(C)$ over all $C$ with $|C| \le k$, and ALG is the value of the output. This is a maximization problem, and the ratio convention is ALG $\ge \alpha \cdot$ OPT with $\alpha \le 1$.

**Integer program.** With $x_j = 1$ when set $j$ is chosen and $z_e = 1$ when element $e$ is covered:

$$\max \sum_{e \in U} w_e z_e \quad \text{subject to} \quad z_e \le \sum_{j : e \in S_j} x_j \text{ for each } e, \quad \sum_j x_j \le k, \quad x_j, z_e \in \{0, 1\}.$$

The [LP relaxation](/lp-relaxation/) replaces $\{0, 1\}$ by $[0, 1]$; its optimum LP* is an upper bound on OPT.

**Submodularity.** The function $F(C) = \text{cov}(C)$ is monotone, $F(A) \le F(B)$ when $A \subseteq B$, and submodular: the gain $F(A \cup \{j\}) - F(A)$ of adding set $j$ is at least the gain $F(B \cup \{j\}) - F(B)$ when $A \subseteq B$. The gain of a set counts its elements not yet covered, and a larger $B$ covers more of them.

**Decision version.** Given $U$, the sets, $k$ and a target $t$, do $k$ sets cover at least $t$ elements? It is NP-complete. With $t = n$ it asks whether a set cover of size $k$ exists.

## Variants

- **Weighted maximum coverage.** Elements have weights. Greedy, by the largest new weight, keeps the ratio $1 - (1 - 1/k)^k$.
- **Budgeted maximum coverage.** Sets have costs $c_j$, and the total cost must be at most a budget $B$. Greedy by new weight per cost, together with partial enumeration over the first three sets, gives $1 - 1/e$ (Khuller, Moss and Naor 1999).
- **Maximum vertex coverage.** The sets are the edge sets at the vertices of a graph, so each element (an edge) is in two sets. Choose $k$ vertices that touch the most edges. [Pipage rounding](/pipage-rounding/) gives $3/4$, and in general $1 - (1 - 1/f)^f$ when each element is in at most $f$ sets (Ageev and Sviridenko 2004).
- **Partial set cover.** Find the fewest sets that cover at least $t$ elements. This is the other side of the same trade-off.
- **Matroid constraint.** The chosen sets must be independent in a [matroid](/matroid/). Greedy gives $1/2$, and the continuous greedy with pipage rounding gives $1 - 1/e$ (Călinescu, Chekuri, Pál and Vondrák 2011). The cardinality constraint is the [uniform matroid](/uniform-matroid/).
- **Monotone submodular maximization.** Replace $\text{cov}$ by any monotone submodular function. The [Nemhauser-Wolsey-Fisher theorem](/nemhauser-wolsey-fisher-theorem/) gives greedy the same ratio.

## Examples

**A small instance.** Let $k = 3$ and

| set | elements |
|---|---|
| $S_1$ | 1, 2, 3, 4 |
| $S_2$ | 5, 6, 7, 8 |
| $S_3$ | 2, 3, 6, 7, 9 |
| $S_4$ | 10, 11, 12 |

The universe has 12 elements. The optimum is $\{S_1, S_2, S_4\}$ with OPT $= 4 + 4 + 3 = 11$; no three sets cover all 12, because element 9 is only in $S_3$, and then $S_1$ and $S_2$ would both be needed besides $S_4$, which makes four sets. Greedy takes the largest set $S_3$ first, then $S_4$ and $S_1$, and covers 10. With $k = 2$, both $\{S_1, S_2\}$ and $\{S_3, S_4\}$ cover 8, which is optimal.

**Greedy at its bound for $k = 2$.** Take 8 elements in two rows of four columns. The sets are the two rows $R_1$ and $R_2$, the block $G_1$ of columns 1 and 2 (4 elements), and the block $G_2$ of column 3 (2 elements). OPT $= 8$, with the two rows. In the first round, $R_1$, $R_2$ and $G_1$ all add 4. If greedy takes $G_1$, then in the second round each of $R_1$, $R_2$ and $G_2$ adds 2, and greedy can take $G_2$. Then it covers 6, and $6/8 = 3/4 = 1 - (1 - 1/2)^2$.

**Coverage as a set cover test.** For any instance, OPT $= n$ if and only if $k$ sets cover $U$. So an exact algorithm for maximum coverage solves set cover, by trying $k = 1, 2, \ldots$.

## Known algorithms

| algorithm | ratio | note |
|---|---|---|
| [Greedy](/greedy-max-coverage/) | $1 - (1 - 1/k)^k \ge 1 - 1/e$ | tight for the algorithm and, up to $\varepsilon$, for the problem |
| Greedy for budgeted coverage with partial enumeration | $1 - 1/e$ | Khuller, Moss and Naor 1999 |
| LP with [pipage rounding](/pipage-rounding/) | $1 - (1 - 1/f)^f$ | $f$ the largest element frequency |
| Exhaustive search | exact | $O(m^k \cdot s)$ time with $s$ the total input size |
| Integer programming | exact | exponential in the worst case |

All ratios hold in the worst case. The LP has polynomial size and is solved in polynomial time by the ellipsoid or an interior point method.

## Bounds

- **Upper bound (proved on the greedy page).** Greedy covers at least $1 - (1 - 1/k)^k$ of OPT. The proof is on the [greedy maximum coverage](/greedy-max-coverage/) page.
- **Lower bound (cited).** For each $\varepsilon > 0$, approximating maximum coverage within $1 - 1/e + \varepsilon$ is NP-hard (Feige 1998). The proof uses the same PCP construction as the $\ln n$ hardness of set cover; see [max coverage inapproximability](/max-coverage-inapproximability/).
- **Integrality gap.** Pipage rounding shows OPT $\ge (1 - 1/e)\,\text{LP}^*$ on each instance. The bound is nearly reached: take one element for each $f$-subset of the $m$ sets, held by exactly the sets of its subset, and let $k = m/f$. Then LP* counts all elements, with $x_j = 1/f$, while $k$ sets cover only a fraction $1 - \binom{m-k}{f}/\binom{m}{f}$, which tends to $1 - 1/e$ as $f$ and $m/f$ grow. So LP rounding alone cannot beat greedy on general instances.
- **Exact time.** For fixed $k$ the problem is in P, by trying all $\binom{m}{k}$ choices. With $k$ as a parameter, it is W[2]-hard, because it contains set cover with $t = n$.

## Reductions

- **From set cover (NP-hardness).** A set cover instance has a cover of size $k$ if and only if the maximum coverage instance with the same sets and the same $k$ has OPT $= n$. So the decision version is NP-complete, by the NP-completeness of set cover (Karp 1972); see [Karp's 21 NP-complete problems](/karps-21-np-complete-problems/).
- **To set cover (an algorithm).** Running greedy for maximum coverage with growing $k$ is the [greedy set cover algorithm](/greedy-set-cover/); the step bound of maximum coverage gives the bound $k \lceil \ln(n/k) \rceil + k$ on the number of sets, with $k$ the size of an optimal cover.
- **Vertex coverage from vertex cover.** Maximum vertex coverage with target $|E|$ is [vertex cover](/vertex-cover/).

## Applications

- **Facility siting by coverage.** Place $k$ facilities, such as fire stations or cell towers, to serve the most customers within a given distance. This is the maximal covering location problem.
- **Sensor placement.** Choose $k$ sensor sites so that the most points of interest are observed.
- **Influence maximization.** Choose $k$ seed users in a social network to reach the most users. Its expected spread is monotone submodular, and [greedy influence maximization](/greedy-influence-maximization/) uses the same bound.
- **Document summaries and search results.** Choose $k$ sentences or results that cover the most topics, so that they repeat little.
- **Bank account location.** Cornuéjols, Fisher and Nemhauser (1977) studied where to open accounts to maximize float, the problem used by Williamson and Shmoys to present the greedy bound.

## References
