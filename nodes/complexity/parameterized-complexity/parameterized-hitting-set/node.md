---
tag: N0FKR0
kind: problem
slug: parameterized-hitting-set
name: Parameterized hitting set
aliases:
- d-hitting set
- k-hitting set
area: complexity/parameterized-complexity
level: advanced
summary: "Decide whether k elements hit every set of a family of sets of size at most d. FPT in O(d^k) times a polynomial, with a kernel of O(d! k^d) sets; W[2]-complete for unbounded d."
prereqs: [hitting-set, fixed-parameter-tractable, sunflower-lemma]
see_also: [parameterized-vertex-cover, parameterized-set-packing, parameterized-dominating-set, set-cover, bounded-search-tree, kernel-lower-bounds, cluster-editing, w-hierarchy]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 2, Kernelization (the sunflower kernel for d-hitting set), Chapter 3, Bounded search trees, and Chapter 15, Lower bounds for kernelization
  - book: isbn:9781107057760
    title: Fedor V. Fomin, Daniel Lokshtanov, Saket Saurabh and Meirav Zehavi, Kernelization, Theory of Parameterized Preprocessing, Cambridge University Press, 2019
    locator: Chapter 8, Sunflower lemma
  - paper: doi:10.1016/j.jcss.2009.09.002
    title: "Faisal N. Abu-Khzam, A kernelization algorithm for d-Hitting Set, Journal of Computer and System Sciences 76(7), 524-531 (2010)"
    locator: a kernel with O(k^(d-1)) elements
  - paper: doi:10.1145/2629620
    title: "Holger Dell and Dieter van Melkebeek, Satisfiability allows no nontrivial sparsification unless the polynomial-time hierarchy collapses, Journal of the ACM 61(4), article 23 (2014)"
    locator: no compression of d-hitting set into O(k^(d-e)) bits unless NP is a subset of coNP/poly
---

Parameterized hitting set is the [hitting set](/hitting-set/) problem in its decision form, with the size $k$ of the hitting set as the [parameter](/parameter/). With sets of size at most a constant $d$, the problem is called *d-hitting set*, and it is [fixed-parameter tractable](/fixed-parameter-tractable/): a search tree runs in time $O(d^k \cdot d\,|\mathcal{F}|)$, and the [sunflower lemma](/sunflower-lemma/) gives a kernel with $O(d!\,k^d)$ sets. With no bound on the set size, the problem is W[2]-complete, so it is not FPT unless $\mathrm{FPT} = \mathrm{W[2]}$. This page gives the parameterized view; the hitting set page has the optimization problem and its approximation algorithms.

## In plain words

You have a list of groups, and each group has at most a few members, say three. You want to pick at most a small number of people so that every group contains at least one picked person. The question is whether a small pick is enough.

If the groups are small, there is a fast method. Take any group that has no picked person yet. One of its few members must be picked, so try each of them in turn. Each try uses one pick, so after the allowed number of picks the search stops. The number of cases depends on the group size and the number of picks, not on the length of the list.

If the groups can be of any size, no such method is known, and the problem is hard in a precise sense.

## Definition

**d-Hitting set.**

- Instance: a finite set $U$, a family $\mathcal{F}$ of subsets of $U$ each of size at most $d$, and an integer $k \ge 0$.
- Parameter: $k$. The number $d$ is a constant that is part of the problem, not of the instance.
- Question: is there a set $H \subseteq U$ with $|H| \le k$ such that $H \cap S \ne \emptyset$ for each $S \in \mathcal{F}$?

A set $H$ with this property is a *hitting set* or a *transversal* of $\mathcal{F}$. In the language of hypergraphs it is a vertex cover of the hypergraph $(U, \mathcal{F})$, so the problem is also called d-vertex cover in hypergraphs. For $d = 2$ it is [vertex cover](/parameterized-vertex-cover/), with singleton sets as forced vertices.

**Hitting set.** The same with no bound $d$ on the set size, and with parameter $k$.

## Variants

- **Unbounded set size.** Parameter $k$ only. This is W[2]-complete; it is the dual of [set cover](/set-cover/), where the roles of elements and sets swap, and it is equivalent to [dominating set](/parameterized-dominating-set/) under parameterized reductions.
- **Combined parameter $k + d$.** The search tree runs in time $d^k$ times a polynomial, so the problem is FPT in $k$ and $d$ together, even when $d$ is part of the input.
- **Universe size $n = |U|$ as the parameter.** Trying all subsets of $U$ takes $O^*(2^n)$ time, so the problem is FPT in $n$. Here $O^*$ hides factors polynomial in the input size.
- **Weighted.** Each element has a weight, and the parameter bounds the weight of $H$. The search tree still works when all weights are at least 1.

## Examples

A 3-hitting set instance with $k = 2$ has the five sets $\{0,1,2\}$, $\{0,1,3\}$, $\{0,1,4\}$, $\{2,3,5\}$ and $\{4,5,6\}$.

- The first three sets form a sunflower with $k + 1 = 3$ petals and core $\{0, 1\}$: their pairwise intersections are all $\{0, 1\}$, and the petals $\{2\}$, $\{3\}$ and $\{4\}$ are disjoint. A hitting set with 2 elements cannot hit three disjoint petals outside the core, so it must meet $\{0, 1\}$.
- The sunflower rule replaces the three sets by the core. The reduced family is $\{0,1\}$, $\{2,3,5\}$, $\{4,5,6\}$.
- A scratch script found by brute force that both families have least hitting sets of size 2, for example $\{0, 5\}$. With $k = 1$ the original instance is a no-instance.

The search tree on the original instance picks the unhit set $\{0,1,2\}$ and tries 0, 1 and 2. After picking 0, the sets $\{2,3,5\}$ and $\{4,5,6\}$ remain, and picking 5 hits both. So the branch $0, 5$ succeeds at depth 2.

## Known algorithms

- **Bounded search tree.** Choose a set $S$ that $H$ does not hit yet, and branch on its at most $d$ elements, each time lowering $k$ by one. The tree has at most $d^k$ leaves, so the time is $O(d^k \cdot d\,|\mathcal{F}|)$. See [bounded search tree](/bounded-search-tree/). For $d = 3$ refined branching rules give smaller bases.
- **Sunflower kernel.** If the sets of one size $i$ number more than $i!\,k^i$, the sunflower lemma finds a sunflower with $k + 1$ petals in polynomial time; replace its sets by its core, and answer NO if the core is empty. When no rule applies, each size class $i$ has at most $i!\,k^i$ sets, so the kernel has at most $\sum_{i \le d} i!\,k^i = O(d!\,k^d)$ sets and $O(d \cdot d!\,k^d)$ elements. A scratch script ran this kernel on 45 random families with $(d, k) \in \{(2, 2), (3, 2), (2, 3)\}$ (seed 5) and compared the answers before and after by brute force; all agreed, and every size class met its bound.
- **Kernel with fewer elements.** Abu-Khzam (2010) gave a kernel with $O(k^{d-1})$ elements. It counts elements, not sets, so it does not contradict the lower bound below.
- **Iterative compression and exact algorithms.** For small $d$ there are faster exact algorithms, and for $n = |U|$ as the parameter the trivial bound is $O^*(2^n)$.

## Bounds

- **Unbounded sets.** Hitting set with parameter $k$ is W[2]-complete. A kernel of any size would make it FPT, so it has no kernel unless $\mathrm{FPT} = \mathrm{W[2]}$. See [W-hierarchy](/w-hierarchy/).
- **Kernel size for fixed $d$.** Dell and van Melkebeek proved that d-hitting set has no compression into any language with $O(k^{d - \varepsilon})$ bits, for any $\varepsilon > 0$, unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$. So the exponent $d$ of the sunflower kernel cannot be lowered, although the number of elements can be $O(k^{d-1})$. See [kernel lower bounds](/kernel-lower-bounds/).
- **Time.** For $d = 2$ the problem is vertex cover, which has no $2^{o(k)} n^{O(1)}$ algorithm under the exponential time hypothesis (ETH), so neither has d-hitting set for any $d \ge 2$.

## Reductions

- **From vertex cover.** Vertex cover is 2-hitting set, with one set per edge.
- **From dominating set.** A dominating set of $G$ is a hitting set of the closed neighborhoods $N[v]$. This shows W[2]-hardness for unbounded sets. The converse reduction also exists, so the two problems are W[2]-equivalent.
- **To and from set cover.** Swap elements and sets: element $u$ becomes the set of members of $\mathcal{F}$ that contain $u$. A hitting set of size $k$ becomes a set cover of size $k$.
- **Cluster vertex deletion.** A graph is a disjoint union of cliques if and only if it has no induced path on three vertices. So deleting at most $k$ vertices to reach such a graph is 3-hitting set on the vertex triples that induce a path. Compare [cluster editing](/cluster-editing/), the edge version.
- **Feedback vertex set in tournaments.** A tournament has a directed cycle if and only if it has a directed triangle, so this problem is 3-hitting set on the directed triangles.

## Applications

The reductions above make d-hitting set a general tool: any deletion problem whose forbidden structures have at most $d$ vertices and can be listed in polynomial time is a d-hitting set instance. Such a problem inherits the $d^k$ search tree and the sunflower kernel. Examples are deletion to cluster graphs, to graphs with no triangle, and to acyclic tournaments. The approximation side, with the $d$-approximation by LP rounding or by a maximal disjoint family, is on the [hitting set](/hitting-set/) page.

## References
