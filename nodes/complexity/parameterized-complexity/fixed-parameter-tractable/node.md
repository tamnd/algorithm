---
tag: 9GDNHX
kind: definition
slug: fixed-parameter-tractable
name: Fixed-parameter tractable
aliases:
- FPT
- fpt
- fixed-parameter tractability
area: complexity/parameterized-complexity
level: intro
summary: "A parameterized problem is fixed-parameter tractable when an algorithm decides each instance (x, k) in time f(k) n^c, for a computable function f and a constant c."
prereqs: [parameterized-problem, polynomial-time, computable-function]
see_also: [xp, kernel, w-hierarchy, parameterized-reduction, fpt-w1-conjecture, parameterized-vertex-cover, bounded-search-tree, para-np-hardness]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 1, Introduction (the definition of FPT and XP); Chapter 2, Kernelization, Lemma 2.2 (a decidable problem is FPT exactly when it has a kernel)
  - book: isbn:9781447155584
    title: Rodney G. Downey and Michael R. Fellows, Fundamentals of Parameterized Complexity, Springer, 2013
    locator: Chapter 2, The Basic Definitions (strongly uniform, uniform and nonuniform FPT)
  - book: isbn:9783540299523
    title: Jörg Flum and Martin Grohe, Parameterized Complexity Theory, Springer, 2006
    locator: Chapter 1, Fixed-Parameter Tractability
  - paper: doi:10.1137/S0097539792228228
    title: "Rodney G. Downey and Michael R. Fellows, Fixed-parameter tractability and completeness I: basic results, SIAM Journal on Computing 24(4), 873-921 (1995)"
    locator: the definition of fixed-parameter tractability
  - paper: doi:10.1016/j.tcs.2010.06.026
    title: "Jianer Chen, Iyad A. Kanj and Ge Xia, Improved upper bounds for vertex cover, Theoretical Computer Science 411(40-42), 3736-3756 (2010)"
    locator: the main theorem, O(1.2738^k + kn) time for vertex cover
---

A [parameterized problem](/parameterized-problem/) is fixed-parameter tractable when some algorithm decides every instance $(x, k)$ in time $f(k) \cdot n^{c}$, where $n = |x|$, $f$ is a computable function and $c$ is a constant that does not depend on $k$. The class of these problems is FPT. All the growth that is faster than polynomial sits in a function of the [parameter](/parameter/) alone, so for a fixed $k$ the time is a polynomial of degree $c$, the same degree for every $k$. This is the property that separates FPT from the larger class [XP](/xp/), where the time is $n^{f(k)}$ and the degree grows with $k$. Vertex cover with the cover size $k$ as parameter is the standard example: a [search tree](/vertex-cover-branching/) solves it in time $O(2^k (n + m))$.

## Definition

Let $L \subseteq \Sigma^* \times \mathbb{N}$ be a parameterized problem. $L$ is *fixed-parameter tractable* if there are an algorithm $A$, a computable function $f : \mathbb{N} \to \mathbb{N}$ and a constant $c$ such that, for every $(x, k)$, the algorithm $A$ decides whether $(x, k) \in L$ in at most $f(k) \cdot |x|^{c}$ steps. FPT is the class of all fixed-parameter tractable problems. An algorithm with this time bound is an *FPT algorithm*.

Three remarks make the definition precise.

**The shape of the bound.** The bound $f(k) \cdot n^c$ can be replaced by $f(k) + n^c$, and the class does not change. In one direction, $f(k) + n^c \le (f(k) + 1) \cdot n^c$ for $n \ge 1$. In the other direction, $ab \le a^2 + b^2$ for all real $a, b$, so $f(k) \cdot n^c \le f(k)^2 + n^{2c}$. So FPT time is "polynomial time plus a cost that depends on $k$ alone".

**Computability of f.** Downey and Fellows call the definition above *strongly uniform* FPT. If $f$ may be any function, the class is *uniform* FPT. If a different algorithm may be used for each value of $k$, with time $O(n^c)$ for each one, the class is *nonuniform* FPT. Most textbooks, including Cygan et al. and Flum and Grohe, use the strongly uniform form.

**The O-star notation.** Many papers write the time as $O^*(f(k))$. The star hides all factors that are polynomial in $n$, so $O^*(f(k))$ means $f(k) \cdot n^{O(1)}$. It is used only when the exponential part is the topic, because it hides the degree $c$.

Two facts about the class follow from the definition.

- FPT is closed under [parameterized reductions](/parameterized-reduction/): if $L$ reduces to $L'$ and $L' \in \mathrm{FPT}$, then $L \in \mathrm{FPT}$. This is why W[1]-hardness is evidence against an FPT algorithm.
- A decidable parameterized problem is in FPT if and only if it has a [kernel](/kernel/). Cai, Chen, Downey and Fellows proved this in 1997, and Cygan et al. give it as Lemma 2.2.

## Examples and non-examples

The difference between $2^k \cdot n$ and $n^k$ is the reason for the definition. For an instance with $n = 1000$:

| $k$ | $2^k \cdot n$ | $n^k$ |
|---|---|---|
| 5 | $3.2 \cdot 10^{4}$ | $10^{15}$ |
| 10 | $1.0 \cdot 10^{6}$ | $10^{30}$ |
| 20 | $1.0 \cdot 10^{9}$ | $10^{60}$ |

Problems in FPT:

- [Vertex cover](/parameterized-vertex-cover/) with the parameter $k$, the size of the cover. The [edge branching](/vertex-cover-branching/) takes $O(2^k (n + m))$ time, and Chen, Kanj and Xia gave $O(1.2738^k + kn)$. The [Buss kernel](/buss-kernel/) reduces any instance to one with $O(k^2)$ edges in linear time.
- [k-path](/parameterized-longest-path/), which asks for a simple path on $k$ vertices, is solved in time $2^{O(k)} \cdot n^{O(1)}$ by [color coding](/k-path-color-coding/).
- Independent set with the parameter $\mathrm{tw}(G)$, the [treewidth](/treewidth/), is solved in time $2^{\mathrm{tw}} \cdot n^{O(1)}$ when a tree decomposition of width $\mathrm{tw}$ is given. [Courcelle's theorem](/courcelle-theorem/) extends this to every graph property that monadic second-order logic can express.
- [Feedback vertex set](/parameterized-feedback-vertex-set/) and [odd cycle transversal](/odd-cycle-transversal/) with the solution size as the parameter.

Problems that are not believed to be in FPT:

- [Clique](/parameterized-clique/) and [independent set](/parameterized-independent-set/) with the solution size $k$. Both are in XP, by trying all $\binom{n}{k}$ vertex sets, and both are W[1]-complete. If one of them is in FPT, then $\mathrm{FPT} = \mathrm{W[1]}$, which the [FPT versus W[1] conjecture](/fpt-w1-conjecture/) says is false.
- [Dominating set](/parameterized-dominating-set/) with the solution size $k$, which is W[2]-complete.
- Graph coloring with the number $q$ of colors. It is NP-complete for $q = 3$, so it is not even in XP unless P = NP. It is [para-NP-hard](/para-np-hardness/).

Every decidable problem becomes fixed-parameter tractable with the parameter $k = |x|$, and a problem with a constant parameter is fixed-parameter tractable exactly when it is in P. Both choices are useless, as the [parameter](/parameter/) page explains.

## Related definitions

- [XP](/xp/) is the class of problems solved in time $n^{f(k)}$. FPT is a proper subset of XP, and this holds without any assumption.
- A [kernel](/kernel/) is the preprocessing form of FPT, and a [polynomial kernel](/polynomial-kernel/) is a stronger property that not every FPT problem has.
- The [W hierarchy](/w-hierarchy/) $\mathrm{FPT} \subseteq \mathrm{W[1]} \subseteq \mathrm{W[2]} \subseteq \cdots$ holds the problems that are not believed to be in FPT. Whether $\mathrm{FPT} = \mathrm{W[1]}$ is open.
- The [Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) gives finer lower bounds inside FPT. For example, it rules out time $2^{o(k)} \cdot n^{O(1)}$ for vertex cover. These bounds are separate from W[1]-hardness.
- The [bounded search tree](/bounded-search-tree/) and [kernelization](/kernelization/) are the two basic techniques that give FPT algorithms.

## References
