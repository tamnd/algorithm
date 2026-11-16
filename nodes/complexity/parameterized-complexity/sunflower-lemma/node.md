---
tag: BVARH4
kind: theorem
slug: sunflower-lemma
name: Sunflower lemma
aliases:
- Erdos-Rado sunflower lemma
area: complexity/parameterized-complexity
level: advanced
summary: "More than d!(p-1)^d distinct sets of size d always contain p sets with the same pairwise intersection. It gives kernels with O(k^d) sets for d-hitting set and d-set packing."
prereqs: [hypergraph, pigeonhole-principle]
see_also: [parameterized-hitting-set, parameterized-set-packing, kernelization, polynomial-kernel, hitting-set, kernel-lower-bounds, representative-families, crown-reduction]
sources:
  - paper: doi:10.1112/jlms/s1-35.1.85
    title: "Paul Erdős and Richard Rado, Intersection theorems for systems of sets, Journal of the London Mathematical Society 35(1), 85-90 (1960)"
    locator: the original lemma with the bound d!(p-1)^d and the lower construction with (p-1)^d sets
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 2, Kernelization (the sunflower lemma and the kernel for d-hitting set)
  - book: isbn:9781107057760
    title: Fedor V. Fomin, Daniel Lokshtanov, Saket Saurabh and Meirav Zehavi, Kernelization, Theory of Parameterized Preprocessing, Cambridge University Press, 2019
    locator: Chapter 8, Sunflower lemma
  - paper: doi:10.4007/annals.2021.194.3.5
    title: "Ryan Alweiss, Shachar Lovett, Kewen Wu and Jiapeng Zhang, Improved bounds for the sunflower lemma, Annals of Mathematics 194(3), 795-815 (2021)"
    locator: Theorem 1.4, the bound (C p^3 log d log log d)^d
  - paper: doi:10.19086/da.11887
    title: "Anup Rao, Coding for sunflowers, Discrete Analysis 2020:2"
    locator: a simpler proof and the bound (C p log(pd))^d
  - paper: doi:10.1016/j.disc.2021.112367
    title: "Tolson Bell, Suchakree Chueluecha and Lutz Warnke, Note on sunflowers, Discrete Mathematics 344(7), 112367 (2021)"
    locator: the bound (C p log d)^d
---

The sunflower lemma of Erdős and Rado says that a large family of sets of the same size must contain a *sunflower*: several sets whose pairwise intersections are all the same set, the *core*. In parameterized complexity it is the main tool for kernels of problems on set systems with sets of size $d$, such as [d-hitting set](/parameterized-hitting-set/) and [d-set packing](/parameterized-set-packing/). The proof is short, constructive and runs in polynomial time, which is what a [kernelization](/kernelization/) needs.

## Statement

A *sunflower with $p$ petals* is a family of $p$ distinct sets $S_1, \ldots, S_p$ such that $S_i \cap S_j = Y$ for all $i \ne j$, for one set $Y$, the *core*. The *petals* are the sets $S_i \setminus Y$, and they are pairwise disjoint. The core may be empty, so $p$ pairwise disjoint sets also form a sunflower.

**Theorem (Erdős and Rado, 1960).** Let $d \ge 1$ and $p \ge 2$. Every family $\mathcal{F}$ of more than $d!\,(p-1)^d$ distinct sets, each of size $d$, contains a sunflower with $p$ petals. Such a sunflower can be found in time polynomial in $|\mathcal{F}|$, $d$ and $p$.

The bound cannot drop below $(p-1)^d$: there is a family of $(p-1)^d$ distinct sets of size $d$ with no sunflower of $p$ petals.

## In plain words

Take many groups of people, each group of the same size. A sunflower is a set of groups that all share the same few people and have no one else in common. Those shared people form the center, and the rest of each group is its own petal.

The lemma says that if you have enough groups, you cannot avoid a sunflower. Either many groups share no one at all, and they form a sunflower with an empty center, or a few people appear in a large share of the groups. Pick such a person, look only at the groups that contain that person, remove the person, and repeat. The groups get smaller each time, so the search ends after a few steps.

## Proof

**Upper bound.** Induction on $d$.

For $d = 1$ the sets are distinct singletons. More than $p - 1$ of them gives $p$ pairwise disjoint sets, a sunflower with an empty core.

Let $d \ge 2$ and $|\mathcal{F}| > d!\,(p-1)^d$. Choose a maximal subfamily $\mathcal{G} \subseteq \mathcal{F}$ of pairwise disjoint sets, greedily. If $|\mathcal{G}| \ge p$, any $p$ sets of $\mathcal{G}$ form a sunflower with an empty core. Otherwise $|\mathcal{G}| \le p - 1$, and the union $U$ of $\mathcal{G}$ has at most $d(p-1)$ elements. Every set of $\mathcal{F}$ meets $U$, because otherwise it could be added to $\mathcal{G}$. By the [pigeonhole principle](/pigeonhole-principle/) some element $u \in U$ lies in more than

$$\frac{d!\,(p-1)^d}{d(p-1)} = (d-1)!\,(p-1)^{d-1}$$

sets of $\mathcal{F}$. The family $\mathcal{F}_u = \{S \setminus \{u\} : u \in S \in \mathcal{F}\}$ has that many distinct sets, each of size $d - 1$. By induction it contains a sunflower $S_1', \ldots, S_p'$ with core $Y'$. Then the sets $S_i' \cup \{u\}$ are in $\mathcal{F}$, and they form a sunflower with core $Y' \cup \{u\}$: the element $u$ is in every intersection and in no petal. $\square$

The proof is an algorithm. Each level picks a greedy disjoint family in time $O(|\mathcal{F}| d)$, counts the elements of $U$, and recurses on one element. There are at most $d$ levels, so the time is polynomial.

**Lower bound.** Take $d$ disjoint blocks $B_1, \ldots, B_d$, each with $p - 1$ elements, and let $\mathcal{F}$ be all sets that take exactly one element from each block. There are $(p-1)^d$ of them. Assume $p$ of them form a sunflower with core $Y$. In each block $B_i$ the $p$ sets choose among $p - 1$ elements, so two of them choose the same element $e$. Then $e$ lies in the intersection of those two sets, which is $Y$, so all $p$ sets contain $e$. This holds for each block, so all $p$ sets agree in every block and are equal, which is a contradiction. $\square$

**A small case.** For $d = 2$ and $p = 3$ the sets are the edges of a graph. The lemma bound is $2! \cdot 2^2 = 8$ and the block construction gives $2^2 = 4$ edges. The true maximum is 6, reached by two disjoint triangles. Three edges at one vertex form a sunflower, so the maximum degree is at most 2, and three disjoint edges form a sunflower, so the largest matching has at most 2 edges. A graph of maximum degree 2 is a union of paths and cycles, and each such component with $e$ edges has a matching of at least $e/3$ edges. So there are at most 6 edges. A scratch search over all edge sets on $n \le 8$ vertices finds the maxima 3, 4, 5, 6, 6, 6 for $n = 3, \ldots, 8$, the same 6. It also confirmed that the block families for $(d, p) = (2, 3)$, $(3, 3)$ and $(2, 4)$, with 4, 8 and 9 sets, have no sunflower with $p$ petals, and it ran the constructive proof on 90 random families just above the bound, all with success (seed 3).

## Consequences

- **d-Hitting set.** If a family of sets of size at most $d$ has a sunflower with $k + 1$ petals and core $Y$, then every hitting set of size at most $k$ meets $Y$, because $k$ elements cannot hit $k + 1$ disjoint petals outside $Y$. So the sunflower can be replaced by $Y$. Applying this in each set size gives a kernel with at most $d!\,k^d$ sets of size $d$, and $O(d!\,k^d)$ sets in total. See [parameterized hitting set](/parameterized-hitting-set/).
- **d-Set packing.** A sunflower with $d(k-1) + 2$ petals contains a set that some solution of $k$ disjoint sets can avoid, so one petal can be deleted. This leaves $O(d!\,(dk)^d)$ sets. See [parameterized set packing](/parameterized-set-packing/).
- **Vertex cover.** Vertex cover is 2-hitting set, and the sunflower kernel keeps at most $2k^2$ edges, close to the [Buss kernel](/buss-kernel/).
- **The exponent d is right.** Dell and van Melkebeek proved that d-hitting set has no compression into any language of size $O(k^{d - \varepsilon})$ bits unless $\mathrm{NP} \subseteq \mathrm{coNP/poly}$, so the sunflower kernel has the best exponent up to the $\varepsilon$. See [kernel lower bounds](/kernel-lower-bounds/).
- **Representative sets.** The [representative families](/representative-families/) method of later work plays a similar role for problems where sunflowers are too weak.

## Tightness

Write $f(d, p)$ for the least number such that every family of more than $f(d, p)$ sets of size $d$ has a sunflower with $p$ petals. The proof above gives $(p-1)^d \le f(d, p) \le d!\,(p-1)^d$. The factor $d!$ is the gap.

- Erdős and Rado conjectured that $f(d, p) \le C(p)^d$ for a constant $C(p)$ that depends only on $p$. This *sunflower conjecture* is open, even for $p = 3$.
- Alweiss, Lovett, Wu and Zhang (2021) proved $f(d, p) \le (C p^3 \log d \log\log d)^d$ for a constant $C$, the first bound of the form $(\log d)^{d(1 + o(1))}$ for fixed $p$.
- Rao (2020) gave a shorter proof with $(C p \log(pd))^d$, and Bell, Chueluecha and Warnke (2021) proved $(C p \log d)^d$.

For kernels the improvements matter little, because $p = k + 1$ grows with the parameter and the constants are not explicit. The kernels in practice use the bound $d!\,(p-1)^d$ with its simple algorithm.

## History

Erdős and Rado proved the lemma in 1960 and also treated families of infinite sets. Sunflowers are also called $\Delta$-systems. Their use for kernels came much later, with the theory of parameterized complexity, and the books of Cygan et al. and Fomin et al. present the kernel for d-hitting set as the standard example. The bound stood almost unchanged for 60 years until the paper of Alweiss, Lovett, Wu and Zhang, first posted in 2019.

## References
