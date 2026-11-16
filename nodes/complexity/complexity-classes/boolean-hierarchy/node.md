---
tag: 3FMGRJ
kind: definition
slug: boolean-hierarchy
name: Boolean hierarchy (DP and levels)
aliases:
- DP
- difference hierarchy
area: complexity/complexity-classes
level: advanced
summary: The classes of languages built from NP languages by unions, intersections and complements. Level 2 is the class of differences of two NP sets, with complete problems such as exact clique.
prereqs: [np, co-np, polynomial-time-reduction]
see_also: [polynomial-hierarchy, np, co-np, clique-problem, maximum-clique, valiant-vazirani-theorem, sat, karp-lipton-theorem]
sources:
  - paper: doi:10.1016/0022-0000(84)90068-0
    title: Christos H. Papadimitriou and Mihalis Yannakakis, The complexity of facets (and some facets of complexity), Journal of Computer and System Sciences 28(2), 244 to 259 (1984)
    locator: the definition of the class D^P and its complete problems, including exact clique and facets of the TSP polytope
  - paper: doi:10.1137/0217078
    title: Jin-Yi Cai, Thomas Gundermann, Juris Hartmanis, Lane A. Hemachandra, Vivian Sewelson, Klaus Wagner and Gerd Wechsung, The Boolean hierarchy I, structural properties, SIAM Journal on Computing 17(6), 1232 to 1252 (1988)
    locator: the definition of the levels, the normal forms and the structural properties
  - paper: doi:10.1137/0217080
    title: Jim Kadin, The polynomial time hierarchy collapses if the Boolean hierarchy collapses, SIAM Journal on Computing 17(6), 1263 to 1282 (1988)
    locator: the main theorem
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley (1994)
    locator: Chapter 17, The polynomial hierarchy (the class D^P)
---

The Boolean hierarchy is the sequence of complexity classes obtained from [NP](/np/) by closing it under Boolean operations a fixed number of times. Its second level, written $\mathsf{D}^{\mathsf{P}}$ and introduced by Papadimitriou and Yannakakis in 1984, is the class of languages $A \cap \overline{B}$ with $A$ and $B$ in NP: an NP condition and a [coNP](/co-np/) condition at the same time. Its typical problems ask for an exact value, such as "the largest clique has exactly $k$ vertices", which needs a yes answer for $k$ and a no answer for $k + 1$. The whole hierarchy lies inside $\mathsf{P}^{\mathsf{NP}}$, the class of problems solved with a constant number of NP queries, and if it collapses then so does the [polynomial hierarchy](/polynomial-hierarchy/).

## Definition

**Levels.** Define classes $\mathsf{BH}_k$ for $k \ge 1$ by

$$\mathsf{BH}_1 = \mathsf{NP}, \qquad \mathsf{BH}_{2k} = \{ A \cap \overline{B} : A \in \mathsf{BH}_{2k-1},\ B \in \mathsf{NP} \}, \qquad \mathsf{BH}_{2k+1} = \{ A \cup B : A \in \mathsf{BH}_{2k},\ B \in \mathsf{NP} \}.$$

The Boolean hierarchy is $\mathsf{BH} = \bigcup_k \mathsf{BH}_k$, and $\mathsf{co}\mathsf{BH}_k$ is the class of complements. The second level is

$$\mathsf{D}^{\mathsf{P}} = \mathsf{BH}_2 = \{ A \cap \overline{B} : A, B \in \mathsf{NP} \} = \{ A \cap C : A \in \mathsf{NP},\ C \in \mathsf{coNP} \}.$$

$\mathsf{D}^{\mathsf{P}}$ is not the same as $\mathsf{NP} \cap \mathsf{coNP}$. That class asks one language to be in both NP and coNP. $\mathsf{D}^{\mathsf{P}}$ intersects one language from each class, and it contains both NP and coNP.

**Nested differences.** Cai and others (1988) proved that $L \in \mathsf{BH}_k$ if and only if there are NP languages $A_1 \supseteq A_2 \supseteq \cdots \supseteq A_k$ with

$$L = A_1 - (A_2 - (A_3 - \cdots - A_k)).$$

Because the chain decreases, $x \in L$ exactly when the number of $i$ with $x \in A_i$ is odd. This gives the name "difference hierarchy", used for the same construction in recursion theory.

**Queries to NP.** The odd-count form shows that $\mathsf{BH}_k$ is decided by a polynomial-time machine that asks $k$ queries to an NP oracle at once (non-adaptively) and outputs the parity of the answers. In the other direction, $k$ non-adaptive queries can be simulated in $\mathsf{BH}_{k+1}$. So

$$\mathsf{BH} = \mathsf{P}^{\mathsf{NP}}_{\|}[O(1)] = \mathsf{P}^{\mathsf{NP}}[O(1)] \subseteq \mathsf{P}^{\mathsf{NP}} = \Delta_2^p,$$

where the middle class allows a constant number of adaptive queries.

**Inclusions.** $\mathsf{BH}_k \cup \mathsf{co}\mathsf{BH}_k \subseteq \mathsf{BH}_{k+1} \cap \mathsf{co}\mathsf{BH}_{k+1}$ for every $k$. If $\mathsf{BH}_k = \mathsf{co}\mathsf{BH}_k$ for some $k$, then $\mathsf{BH} = \mathsf{BH}_k$, in the same way as for the polynomial hierarchy. If $\mathsf{P} = \mathsf{NP}$, every level equals P.

## Examples and non-examples

**SAT-UNSAT is complete for $\mathsf{D}^{\mathsf{P}}$.** The language SAT-UNSAT is the set of pairs $(\varphi, \psi)$ of Boolean formulas with $\varphi$ satisfiable and $\psi$ unsatisfiable. It is in $\mathsf{D}^{\mathsf{P}}$, as the intersection of $\{(\varphi, \psi) : \varphi \in \mathrm{SAT}\}$ and $\{(\varphi, \psi) : \psi \notin \mathrm{SAT}\}$. For hardness, let $L = A \cap \overline{B}$ with $A, B \in \mathsf{NP}$. By the [Cook-Levin theorem](/cook-levin-theorem/) there are polynomial-time many-one reductions $f$ from $A$ to [SAT](/sat/) and $g$ from $B$ to SAT. Then

$$x \in L \iff f(x) \in \mathrm{SAT} \text{ and } g(x) \notin \mathrm{SAT} \iff (f(x), g(x)) \in \text{SAT-UNSAT},$$

so $x \mapsto (f(x), g(x))$ is a polynomial-time many-one reduction from $L$ to SAT-UNSAT.

**Exact clique.** EXACT CLIQUE is the set of pairs $(G, k)$ such that the [largest clique](/maximum-clique/) of $G$ has exactly $k$ vertices. It is in $\mathsf{D}^{\mathsf{P}}$: $(G, k)$ is in the [clique problem](/clique-problem/) and $(G, k+1)$ is not. Papadimitriou and Yannakakis (1984) proved that it is complete for $\mathsf{D}^{\mathsf{P}}$ under polynomial-time many-one reductions. A small case: the 5-cycle on vertices $0, \ldots, 4$ has a clique of size $2$ and none of size $3$, so $(C_5, 2)$ is a yes-instance. Add the chord $\{0, 2\}$. Now $\{0, 1, 2\}$ is a clique of size $3$ and no clique of size $4$ exists, so $(C_5 + \{0,2\}, 3)$ is a yes-instance and $(C_5 + \{0,2\}, 2)$ is a no-instance, because the "no clique of size $3$" part fails. A certificate of the yes part is easy to check, but the no part needs a coNP argument.

**Other complete problems for $\mathsf{D}^{\mathsf{P}}$.**

- *Critical SAT*: a CNF formula that is unsatisfiable, but becomes satisfiable when any one clause is removed.
- *Facets*: whether a given inequality defines a facet of the polytope of tours of the traveling salesman problem (Papadimitriou and Yannakakis 1984).
- *Exact versions of optimization problems*: "the optimum is exactly $k$" for TSP, maximum cut, chromatic number and others.

**Unique satisfiability.** USAT, the set of formulas with exactly one satisfying assignment, is in $\mathsf{D}^{\mathsf{P}}$: at least one satisfying assignment is an NP condition, and no two distinct ones is a coNP condition. It is not known to be complete under deterministic reductions. By the [Valiant-Vazirani theorem](/valiant-vazirani-theorem/), it is complete under randomized reductions.

**Complete problems for higher levels.** For $\mathsf{BH}_k$, take tuples $(\varphi_1, \ldots, \varphi_k)$ of formulas such that $\varphi_{i+1}$ satisfiable implies $\varphi_i$ satisfiable, and ask whether the number of satisfiable $\varphi_i$ is odd. By the nested-difference form this is $\mathsf{BH}_k$-complete.

**Non-examples.** Problems complete for $\mathsf{P}^{\mathsf{NP}}$ with a polynomial number of queries, such as "the lexicographically largest satisfying assignment ends in 1", are not in BH unless BH and PH collapse. Problems in $\Sigma_2^p$ that are complete for it are not in BH unless $\Sigma_2^p \subseteq \Delta_2^p$, which would collapse PH.

## Related definitions

- [Polynomial hierarchy](/polynomial-hierarchy/): BH is inside its level $\Delta_2^p$. Kadin (1988) proved that if $\mathsf{BH}_k = \mathsf{co}\mathsf{BH}_k$ for some $k$, then PH collapses to its third level. Later work moved the collapse lower, inside $\Delta_3^p$. This mirrors the [Karp-Lipton theorem](/karp-lipton-theorem/), and Kadin's proof also uses advice.
- $\mathsf{P}^{\mathsf{NP}}[O(\log n)]$, also written $\Theta_2^p$: logarithmically many adaptive NP queries, equal to polynomially many non-adaptive ones. It contains BH.
- [NP](/np/) and [coNP](/co-np/): the first level and its complement.
- Difference hierarchies over other classes, such as the Ershov hierarchy over the computably enumerable sets, use the same nested-difference form.

## References
