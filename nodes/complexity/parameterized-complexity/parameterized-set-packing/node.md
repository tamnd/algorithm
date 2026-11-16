---
tag: 6RPVAQ
kind: problem
slug: parameterized-set-packing
name: Parameterized set packing
aliases:
- d-set packing
area: complexity/parameterized-complexity
level: advanced
summary: "Decide whether a family of sets of size at most d has k pairwise disjoint members. FPT in k for fixed d, with a sunflower kernel of O(d!(dk)^d) sets; W[1]-complete for unbounded d."
prereqs: [set-packing, fixed-parameter-tractable, sunflower-lemma]
see_also: [parameterized-hitting-set, three-dimensional-matching, color-coding, representative-families, parameterized-independent-set, kernel-lower-bounds, w-hierarchy, exact-cover]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 2, Kernelization (sunflowers), Chapter 5, Randomized methods in parameterized algorithms (color coding), and Chapter 15, Lower bounds for kernelization
  - book: isbn:9781107057760
    title: Fedor V. Fomin, Daniel Lokshtanov, Saket Saurabh and Meirav Zehavi, Kernelization, Theory of Parameterized Preprocessing, Cambridge University Press, 2019
    locator: Chapter 8, Sunflower lemma
  - paper: doi:10.1112/jlms/s1-35.1.85
    title: "Paul Erdős and Richard Rado, Intersection theorems for systems of sets, Journal of the London Mathematical Society 35(1), 85-90 (1960)"
    locator: the sunflower lemma used by the kernel
---

Parameterized set packing is the [set packing](/set-packing/) problem in its decision form, with the number $k$ of disjoint sets as the [parameter](/parameter/). When every set has at most $d$ elements for a constant $d$, the problem is called *d-set packing*, and it is [fixed-parameter tractable](/fixed-parameter-tractable/): the [sunflower lemma](/sunflower-lemma/) gives a kernel with $O(d!\,(dk)^d)$ sets, and [color coding](/color-coding/) gives time $2^{O(dk)} n^{O(1)}$. With no bound on the set size, the problem is W[1]-complete. This page gives the parameterized view; the set packing page has the optimization problem and its approximation algorithms.

## In plain words

You have a list of teams, and each team has at most a few members, say three. A person can play for only one team at a time. You want to know whether you can field a given number of teams at once, with no person in two of them.

If the teams are small, the answer depends on a small part of the list. When very many teams share the same few people and differ elsewhere, you can throw one of them away, because some other team can always take its place. After this cleanup the list is short, with a length that depends only on the team size and the number of teams you want. If the teams can be of any size, no such cleanup is known, and the problem is hard in a precise sense.

## Definition

**d-Set packing.**

- Instance: a finite set $U$, a family $\mathcal{F}$ of subsets of $U$ each of size at most $d$, and an integer $k \ge 0$.
- Parameter: $k$. The number $d$ is a constant that is part of the problem.
- Question: are there $k$ sets $S_1, \ldots, S_k \in \mathcal{F}$ that are pairwise disjoint?

Such sets form a *packing* of size $k$. In the language of hypergraphs it is a matching of size $k$ in the hypergraph $(U, \mathcal{F})$. For $d = 2$ it is maximum matching in a graph, which is solvable in polynomial time, so the problem is interesting for $d \ge 3$.

**Set packing.** The same with no bound $d$ on the set size, and with parameter $k$.

## Variants

- **Unbounded set size.** Parameter $k$ only. This is W[1]-complete. It contains [independent set](/parameterized-independent-set/): map each vertex to the set of its incident edges, and then disjoint sets are exactly independent vertices.
- **3-Dimensional matching.** The elements split into three classes, and every set takes one element from each class. This is a special case of 3-set packing; see [three-dimensional matching](/three-dimensional-matching/).
- **Perfect packing.** Ask for $k = |U|/d$ disjoint sets, which is [exact cover](/exact-cover/) by sets of size $d$. Here $k$ is not small, so the parameter is the size of $U$.
- **Weighted.** Each set has a weight, and the question asks for $k$ disjoint sets of total weight at least $w$.

## Examples

A 2-set packing instance with $k = 2$ has the five sets $\{0,1\}$, $\{0,2\}$, $\{0,3\}$, $\{0,4\}$ and $\{1,2\}$. The rule below uses sunflowers with $p = d(k-1) + 2 = 4$ petals.

- The four sets that contain 0 form a sunflower with core $\{0\}$ and petals $\{1\}$, $\{2\}$, $\{3\}$, $\{4\}$.
- The rule deletes one of them, say $\{0, 1\}$.
- A scratch script found by brute force that the largest packing has 2 sets both before and after the deletion, for example $\{0, 4\}$ and $\{1, 2\}$.

## Known algorithms

- **Sunflower kernel.** Let $p = d(k-1) + 2$. If $\mathcal{F}$ has a sunflower $S_1, \ldots, S_p$, delete $S_1$. This is safe. Take a packing of size $k$ that uses $S_1$. Its other $k - 1$ sets do not meet $S_1$, so they do not meet the core, and they meet the sunflower sets only in their petals. They have at most $d(k-1)$ elements, and the petals of $S_2, \ldots, S_p$ are $d(k-1) + 1$ disjoint sets, so one petal is not touched. Its set $S_j$ is then disjoint from the other $k - 1$ sets and can replace $S_1$. When the rule no longer applies, each size class $i$ has at most $i!\,(p-1)^i$ sets, so the kernel has $O(d!\,(dk)^d)$ sets. A scratch script ran this rule on 20 random families with $d = 2$ and $k \in \{2, 3\}$ (seed 6). The bounds were 18 and 50 sets, every result met its bound, and the answer was the same before and after by brute force.
- **Color coding.** A packing of size $k$ uses at most $dk$ elements. Color the elements at random with $dk$ colors and look for $k$ sets whose elements have different colors, with dynamic programming over subsets of colors. This takes time $2^{O(dk)} n^{O(1)}$ and can be derandomized. See [color coding](/color-coding/).
- **Representative families.** The method of [representative families](/representative-families/) gives deterministic algorithms of the same form $2^{O(dk)} n^{O(1)}$ with smaller constants in the exponent.
- **Greedy bound.** A maximal packing with fewer than $k$ sets has a union of at most $d(k-1)$ elements, and every set of $\mathcal{F}$ meets this union. Many algorithms use this small hitting set as a start.

## Bounds

- **Unbounded sets.** Set packing with parameter $k$ is W[1]-complete, so it is not FPT and has no kernel unless $\mathrm{FPT} = \mathrm{W[1]}$. See [W-hierarchy](/w-hierarchy/).
- **Kernel size for fixed $d$.** Dell and Marx (2012), and also Hermelin and Wu (2012), showed that d-set packing, for $d \ge 3$, has no compression into $O(k^{d - \varepsilon})$ bits for any $\varepsilon > 0$ unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$. So the exponent $d$ of the sunflower kernel is close to the best. See [kernel lower bounds](/kernel-lower-bounds/).
- **Time.** Under the exponential time hypothesis (ETH), 3-dimensional matching with $k$ triples to choose has no $2^{o(k)} n^{O(1)}$ algorithm. So for $d \ge 3$ the form $2^{O(dk)}$ cannot become subexponential in $k$.

## Reductions

- **From independent set.** Vertices become sets of incident edges, as above. This proves W[1]-hardness for unbounded sets.
- **To independent set.** Build the graph whose vertices are the sets of $\mathcal{F}$, with an edge between two sets that meet. A packing is an independent set of this graph. This puts set packing in W[1].
- **Dual to hitting set.** A packing of size $k$ shows that every hitting set has at least $k$ elements. For sets of size $d$ the two numbers differ by a factor of at most $d$, because the union of a maximal packing is a hitting set. See [parameterized hitting set](/parameterized-hitting-set/).

## Applications

Packing problems on graphs often reduce to d-set packing with a small $d$: packing $k$ vertex-disjoint triangles is 3-set packing on the triangles of the graph, and packing $k$ disjoint copies of a fixed graph $H$ is $|V(H)|$-set packing. Each of these inherits the sunflower kernel and the $2^{O(dk)}$ algorithms. The approximation side, with local search ratios for $d$-set packing, is on the [set packing](/set-packing/) page.

## References
