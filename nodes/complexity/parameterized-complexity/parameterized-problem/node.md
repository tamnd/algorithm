---
tag: J1GS6A
kind: definition
slug: parameterized-problem
name: Parameterized problem
aliases:
- parameterized language
area: complexity/parameterized-complexity
level: intro
summary: "A language L of pairs (x, k), where x is an instance and the natural number k is its parameter. It is the object that FPT, XP and the W hierarchy classify."
prereqs: [parameter, decision-problem]
see_also: [fixed-parameter-tractable, xp, parameterized-reduction, w-hierarchy, kernel, parameterized-vertex-cover, parameterized-clique, parameterized-dominating-set]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 1, Introduction (the definition of a parameterized problem and of the size of an instance)
  - book: isbn:9783540299523
    title: Jörg Flum and Martin Grohe, Parameterized Complexity Theory, Springer, 2006
    locator: Chapter 1, Fixed-Parameter Tractability (parameterized problems as pairs of a language and a parameterization, and their slices)
  - book: isbn:9781447155584
    title: Rodney G. Downey and Michael R. Fellows, Fundamentals of Parameterized Complexity, Springer, 2013
    locator: Chapter 2, The Basic Definitions
  - paper: doi:10.1137/S0097539792228228
    title: "Rodney G. Downey and Michael R. Fellows, Fixed-parameter tractability and completeness I: basic results, SIAM Journal on Computing 24(4), 873-921 (1995)"
    locator: the definition of a parameterized problem
---

A parameterized problem is a [decision problem](/decision-problem/) in which every instance carries a natural number, its [parameter](/parameter/). Formally it is a set $L \subseteq \Sigma^* \times \mathbb{N}$ of pairs $(x, k)$, and the question is whether a given pair is in $L$. The parameter lets us measure the running time in two variables: the size $n = |x|$ of the instance and the value of $k$. The classes [FPT](/fixed-parameter-tractable/), [XP](/xp/) and the levels of the [W hierarchy](/w-hierarchy/) are sets of parameterized problems, and the [parameterized reduction](/parameterized-reduction/) compares them. A classical problem gives many parameterized problems, one for each choice of the parameter, and they can have different complexity.

## Definition

Let $\Sigma$ be a finite alphabet. A *parameterized problem* is a language $L \subseteq \Sigma^* \times \mathbb{N}$. For an instance $(x, k) \in \Sigma^* \times \mathbb{N}$, the number $k$ is the *parameter*. The instance is a *yes-instance* when $(x, k) \in L$ and a *no-instance* otherwise. The size of the instance is $|(x, k)| = |x| + k$. Most authors write $n$ for $|x|$, because in the usual problems $k \le |x|$ or the answer is trivial for large $k$.

For a fixed value $k$, the *slice* $L_k = \{x : (x, k) \in L\}$ is a classical language. The *classical form* of $L$ is the language $\{x \# 1^k : (x, k) \in L\}$, with the parameter written in unary.

An equivalent form, used by Flum and Grohe, is a pair $(Q, \kappa)$ of a classical language $Q \subseteq \Sigma^*$ and a parameterization $\kappa : \Sigma^* \to \mathbb{N}$ that is computable in polynomial time. The two forms translate into each other. From $(Q, \kappa)$ we get the set of pairs $(x, \kappa(x))$ with $x \in Q$. From $L$ we get $Q$ as the classical form of $L$ and $\kappa(x \# 1^k) = k$.

The name of a parameterized problem must name the parameter. Flum and Grohe mark it with a prefix, for example p-VERTEX-COVER when the parameter is the size of the cover. This page uses the same style.

## Examples and non-examples

The standard examples take the solution size as the parameter. In each one, the input is a graph $G = (V, E)$ and a number $k$:

- [p-Vertex-Cover](/parameterized-vertex-cover/): is there a set $S \subseteq V$ with $|S| \le k$ such that every edge has an endpoint in $S$?
- [p-Clique](/parameterized-clique/): is there a set of $k$ vertices that are pairwise adjacent?
- [p-Independent-Set](/parameterized-independent-set/): is there a set of $k$ vertices with no edge between them?
- [p-Dominating-Set](/parameterized-dominating-set/): is there a set $D$ with $|D| \le k$ such that every vertex is in $D$ or has a neighbor in $D$?

All four have an NP-complete classical form, and they differ in the parameterized view: p-Vertex-Cover is in FPT, p-Clique and p-Independent-Set are W[1]-complete, and p-Dominating-Set is W[2]-complete.

A small worked case. Let $G$ be the path $P_6$ with vertices $1, \ldots, 6$ and edges $\{i, i+1\}$. The least vertex cover has 3 vertices, for example $\{2, 4, 6\}$. So $(P_6, 3)$ and $(P_6, 4)$ are in p-Vertex-Cover, and $(P_6, 2)$ is not: two vertices cover at most 4 of the 5 edges, because each vertex of a path has degree at most 2.

Slices show how a parameter can help. Each slice of p-Vertex-Cover is in P, because for fixed $k$ there are at most $\binom{n}{k}$ candidate sets. The same holds for p-Clique. In contrast, take the coloring problem with the number $q$ of colors as parameter. Its slice for $q = 3$ is [3-coloring](/three-coloring/), which is NP-complete. A problem with an NP-complete slice is not in XP unless P = NP, and it is [para-NP-hard](/para-np-hardness/).

The following are not parameterized problems:

- The optimization problem "find a least vertex cover". It has no parameter and asks for a set, not a yes or no answer. The decision form with the bound $k$ as the parameter is p-Vertex-Cover.
- The classical language VERTEX-COVER $= \{(G, k) : \tau(G) \le k\}$ without a stated parameter. The same set of pairs is a parameterized problem only when we say which number is the parameter. With $k$ it is p-Vertex-Cover. With $|V| - k$ it is the independent set problem in disguise, which is W[1]-hard.

## Related definitions

- The [parameter](/parameter/) page discusses the choice of the parameter and lists common parameters.
- [Fixed-parameter tractable](/fixed-parameter-tractable/) problems are decided in time $f(k) n^{O(1)}$, and problems in [XP](/xp/) in time $n^{f(k)}$.
- A [parameterized reduction](/parameterized-reduction/) maps $(x, k)$ to $(x', k')$ in FPT time with $k' \le g(k)$. It is the reduction that defines hardness for the [W hierarchy](/w-hierarchy/).
- A [kernel](/kernel/) maps $(x, k)$ to an equivalent instance whose size depends only on $k$.

## References
