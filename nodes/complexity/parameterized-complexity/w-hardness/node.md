---
tag: HYGDGP
kind: definition
slug: w-hardness
name: W[t]-hardness
aliases:
- W[1]-hard
- W[t]-complete
area: complexity/parameterized-complexity
level: advanced
summary: "A problem is W[t]-hard if every problem in W[t] has a parameterized reduction to it. A W[1]-hard problem is not FPT unless FPT = W[1]; this says nothing about XP."
prereqs: [w-hierarchy, parameterized-reduction]
see_also: [clique-w1-completeness, parameterized-clique, parameterized-independent-set, parameterized-dominating-set, fpt-w1-conjecture, para-np-hardness, xp, np-hard]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 13, Fixed-parameter intractability (W[1]-hardness and W[2]-hardness proofs from multicolored clique and dominating set)
  - book: isbn:9783540299523
    title: Jörg Flum and Martin Grohe, Parameterized Complexity Theory, Springer, 2006
    locator: Chapter 2 (Reductions and Parameterized Intractability) and Chapters 6 and 7 (the W hierarchy and its complete problems)
  - paper: doi:10.1137/S0097539792228228
    title: "Rodney G. Downey and Michael R. Fellows, Fixed-parameter tractability and completeness I: basic results, SIAM Journal on Computing 24(4), 873-921 (1995)"
    locator: W[2]-completeness of dominating set and related problems
  - paper: doi:10.1016/0304-3975(94)00097-3
    title: "Rodney G. Downey and Michael R. Fellows, Fixed-parameter tractability and completeness II: on completeness for W[1], Theoretical Computer Science 141(1-2), 109-131 (1995)"
    locator: the main theorem, W[1]-completeness of independent set and clique
---

A [parameterized problem](/parameterized-problem/) is W[t]-hard if every problem in the class $\mathsf{W}[t]$ of the [W-hierarchy](/w-hierarchy/) has a [parameterized reduction](/parameterized-reduction/) to it, and W[t]-complete if it is also in $\mathsf{W}[t]$. It is the parameterized analogue of [NP-hardness](/np-hard/): a W[1]-hard problem has no FPT algorithm unless $\mathsf{FPT} = \mathsf{W}[1]$. The hardness always belongs to a pair of a problem and a parameter, and it gives no bound on the running time by itself.

## Definition

Let $t \ge 1$, and let $\mathsf{W}[t]$ be the class of parameterized problems that have a parameterized reduction to weighted circuit satisfiability for circuits of weft at most $t$ and some constant depth (see [W-hierarchy](/w-hierarchy/)).

A parameterized problem $Q$ is *$\mathsf{W}[t]$-hard* if $Q' \le_{\mathrm{fpt}} Q$ for every $Q' \in \mathsf{W}[t]$. It is *$\mathsf{W}[t]$-complete* if it is $\mathsf{W}[t]$-hard and in $\mathsf{W}[t]$. The same words are used for $\mathsf{W}[\mathsf{SAT}]$ and $\mathsf{W}[\mathsf{P}]$.

Since parameterized reductions compose, $Q$ is W[t]-hard as soon as one W[t]-hard problem reduces to it. In practice one reduces from a known complete problem: multicolored clique or [clique](/parameterized-clique/) for W[1], and [dominating set](/parameterized-dominating-set/) or [set cover](/set-cover/) for W[2].

**What hardness gives.** If $Q$ is W[t]-hard and $Q \in \mathsf{FPT}$, then every problem in $\mathsf{W}[t]$ is in FPT, because FPT is closed under parameterized reductions. So $\mathsf{FPT} = \mathsf{W}[t]$, and in particular $\mathsf{FPT} = \mathsf{W}[1]$. Hence the standard phrase: a W[1]-hard problem is not FPT unless $\mathsf{FPT} = \mathsf{W}[1]$. The [FPT versus W[1] conjecture](/fpt-w1-conjecture/) says that this does not happen.

**What hardness does not give.**

- *Nothing about XP.* Clique is W[1]-complete and is in [XP](/xp/), with time $O(n^k k^2)$. Coloring with $k$ colors is W[t]-hard for every $t$ and is not in XP unless P = NP, because it is NP-hard for $k = 3$; see [para-NP-hardness](/para-np-hardness/). Both are "W[1]-hard".
- *No running time bound.* W[1]-hardness rules out time $f(k) \cdot n^{O(1)}$ under a conjecture, and nothing more. The bound "no $f(k) \cdot n^{o(k)}$ algorithm for clique" is a different statement, conditional on the [Exponential Time Hypothesis](/strong-exponential-time-hypothesis/), and it is proved with reductions that keep $k' = O(k)$.
- *Nothing for another parameter.* The same classical problem can be W[1]-hard with one parameter and FPT with another.

## Examples and non-examples

**Clique and independent set are W[1]-complete.** Downey and Fellows (1995) proved that independent set is W[1]-complete. The map $(G, k) \mapsto (\overline{G}, k)$ to the [complement graph](/complement-graph/) moves the result to clique, with the same $k$. The proof of hardness is on [clique is W[1]-complete](/clique-w1-completeness/).

**Dominating set and set cover are W[2]-complete.** Downey and Fellows (1995) proved that dominating set is W[2]-complete. Set cover with $k$ sets is W[2]-hard by the map from a graph to its closed neighborhoods $N[v]$, with the same $k$. [Hitting set](/hitting-set/) with $k$ elements is W[2]-hard by the dual map: from a family $\mathcal{F}$ over a universe $U$, make one element for each set of $\mathcal{F}$ and, for each $u \in U$, the set of members of $\mathcal{F}$ that contain $u$. A choice of $k$ sets covers $U$ exactly when the matching $k$ elements hit every new set. Every W[2]-hard problem is also W[1]-hard.

**Non-example: vertex cover.** [Vertex cover](/parameterized-vertex-cover/) with the cover size $k$ is FPT, with a [search tree](/vertex-cover-branching/) in time $O(2^k (n + m))$. If it were W[1]-hard, FPT would equal W[1]. The polynomial-time map from vertex cover to independent set, $(G, k) \mapsto (G, n - k)$, does not make it hard, because $n - k$ is not bounded by a function of $k$.

**Non-example: clique by maximum degree.** Take the parameter $\Delta$, the maximum degree. A clique that contains $v$ lies in the closed neighborhood $N[v]$, which has at most $\Delta + 1$ vertices. Trying every subset of every $N[v]$ takes time $O(2^{\Delta + 1} \Delta^2 n)$, so clique with parameter $\Delta$ is FPT. The W[1]-hardness of clique is for the parameter $k$ only.

**Non-example: planar independent set.** On [planar graphs](/planar-graph/), independent set with parameter $k$ is FPT. By the [four color theorem](/four-color-theorem/), a planar graph on $n$ vertices has a color class with at least $\lceil n/4 \rceil$ vertices, and a color class is independent. So if $n \ge 4k$ the answer is yes, and otherwise $n < 4k$ and trying all sets takes time bounded by a function of $k$. The general problem stays W[1]-complete, so the hardness is lost by the restriction of the input.

## Related definitions

- *[W-hierarchy](/w-hierarchy/).* The classes $\mathsf{W}[1] \subseteq \mathsf{W}[2] \subseteq \cdots \subseteq \mathsf{W}[\mathsf{P}]$ that the hardness refers to.
- *[NP-hardness](/np-hard/).* Hardness for NP under polynomial-time reductions. The two notions are independent: clique is both NP-hard and W[1]-hard, and vertex cover is NP-hard and FPT.
- *[Para-NP-hardness](/para-np-hardness/).* Hardness for para-NP under parameterized reductions. A para-NP-hard problem is W[P]-hard, and so W[t]-hard for every $t$, since W[P] is inside para-NP.
- *#W[1]-hardness.* The counting form, under parameterized Turing reductions; see [parameterized counting complexity](/parameterized-counting-complexity/). Counting $k$-paths is #W[1]-hard, although finding one is FPT.
- *Lower bounds under ETH.* Statements of the form "no $f(k) \cdot n^{o(k)}$ algorithm unless ETH fails". They are stronger than W[1]-hardness for running times, and they rest on a different assumption.

## References
