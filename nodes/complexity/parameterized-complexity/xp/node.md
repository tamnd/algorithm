---
tag: 6JZRAB
kind: definition
slug: xp
name: XP (slicewise polynomial)
aliases:
- XP
- slicewise polynomial
area: complexity/parameterized-complexity
level: advanced
summary: "Parameterized problems solvable in time f(k) n^g(k) for computable f and g. XP contains FPT, and the inclusion is proper without any assumption."
prereqs: [fixed-parameter-tractable, diagonalization-argument]
see_also: [fixed-parameter-tractable, w-hierarchy, parameterized-clique, para-np-hardness, time-hierarchy-theorem, universal-turing-machine, w-hardness, parameter]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 1, Introduction (the definition of XP next to FPT)
  - book: isbn:9781447155584
    title: Rodney G. Downey and Michael R. Fellows, Fundamentals of Parameterized Complexity, Springer, 2013
    locator: the class XP and the proof by diagonalization that FPT is a proper subset of XP
  - book: isbn:9783540299523
    title: Jörg Flum and Martin Grohe, Parameterized Complexity Theory, Springer, 2006
    locator: the class XP of slicewise polynomial problems and its relation to the W hierarchy
  - paper: doi:10.1137/S0097539792228228
    title: "Rodney G. Downey and Michael R. Fellows, Fixed-parameter tractability and completeness I: basic results, SIAM Journal on Computing 24(4), 873-921 (1995)"
    locator: the parameterized classes and the problems in them
---

XP is the class of [parameterized problems](/parameterized-problem/) that an algorithm decides in time $f(k) \cdot n^{g(k)}$ for computable functions $f$ and $g$, where $n$ is the size of the instance and $k$ is the [parameter](/parameter/). For each fixed $k$ the time is a polynomial, so every slice of the problem is in P, and one algorithm handles all slices. That is the reason for the name *slicewise polynomial*. The difference from [FPT](/fixed-parameter-tractable/) is the place of $k$: in FPT it may appear only in a factor in front of a fixed polynomial, and in XP it may appear in the degree. Clique with the clique size $k$ is the typical member: trying all $\binom{n}{k}$ vertex sets takes time $O(n^{k} k^2)$. FPT is a proper subset of XP, and this is a theorem, not a conjecture.

## Definition

A parameterized problem $L \subseteq \Sigma^* \times \mathbb{N}$ is in XP if there are an algorithm $A$ and computable functions $f, g : \mathbb{N} \to \mathbb{N}$ such that $A$ decides whether $(x, k) \in L$ in at most $f(k) \cdot |x|^{g(k)}$ steps.

The factor $f(k)$ can be dropped. For $n \ge 2$ we have $f(k) \le 2^{f(k)} \le n^{f(k)}$, so $f(k) \cdot n^{g(k)} \le n^{f(k) + g(k)}$. Inputs with $n < 2$ are finitely many for each $k$, and a table answers them. So XP is also the class of problems decided in time $n^{h(k)}$ for a computable $h$, which is the form in the short definition.

Flum and Grohe call the class above *uniform* XP. If each slice may have its own polynomial-time algorithm, with no single algorithm for all $k$, the class is *nonuniform* XP. This page uses the uniform class, as Cygan et al. do.

**FPT is a subset of XP.** If $L$ is decided in time $f(k) \cdot n^{c}$, take $g(k) = c$.

**FPT is a proper subset of XP.** There is a problem in XP that is not in FPT. The proof is a [diagonalization](/diagonalization-argument/) in the style of the [time hierarchy theorem](/time-hierarchy-theorem/), and it needs no assumption such as P $\ne$ NP. Fix a model of deterministic multitape [Turing machines](/turing-machine/) and an encoding $\langle M \rangle$ of machines as strings. Let

$$Q = \{ (w, k) : w = \langle M \rangle \# 1^{m} \text{ for a machine } M \text{ and an } m \ge 0, \text{ and } M \text{ accepts the input } (w, k) \text{ within } |w|^{k} \text{ steps} \}.$$

1. $Q$ is in XP. Given $(w, k)$, check the form of $w$, compute $t = |w|^k$, and run a [universal machine](/universal-turing-machine/) on $M$ and $(w, k)$ for $t$ simulated steps. The simulation of $t$ steps takes at most $p(|\langle M \rangle|) \cdot t \log t$ steps for a fixed polynomial $p$, and $|\langle M \rangle| \le |w|$. So the total time is at most $|w|^{k + d}$ for a constant $d$ and all large $|w|$. This is XP time with $g(k) = k + d$.
2. $Q$ is not in FPT. Suppose a multitape machine $A$ decides $Q$ in time $f(k) \cdot n^{c}$. An algorithm on another standard model can be changed into such a machine with a larger constant $c$. Let $M_A$ be the machine that, on input $(w, k)$, runs $A$ on $(w, c + 1)$ and accepts exactly when $A$ rejects. On inputs with $k = c + 1$, the machine $M_A$ uses at most $f(c+1) \cdot |w|^{c} + a |w| + b$ steps for constants $a$ and $b$. This is less than $|w|^{c+1}$ once $|w|$ is large. Take $w = \langle M_A \rangle \# 1^{m}$ with $m$ that large. Then $M_A$ halts on $(w, c+1)$ within $|w|^{c+1}$ steps, so $(w, c + 1) \in Q$ exactly when $M_A$ accepts $(w, c+1)$, which happens exactly when $A$ rejects $(w, c+1)$, that is, when $(w, c + 1) \notin Q$. This is a contradiction.

The problem $Q$ is artificial. For natural problems such as clique, the claim that they are in XP but not in FPT is open, and it is the [FPT versus W[1] conjecture](/fpt-w1-conjecture/).

## Examples and non-examples

The brute force for [p-Clique](/parameterized-clique/) checks every set of $k$ vertices. The number of sets for a graph with $n = 1000$ vertices shows how the degree of the polynomial grows with $k$:

| $k$ | $\binom{1000}{k}$ |
|---|---|
| 2 | $5.0 \cdot 10^{5}$ |
| 3 | $1.7 \cdot 10^{8}$ |
| 4 | $4.1 \cdot 10^{10}$ |
| 5 | $8.3 \cdot 10^{12}$ |
| 6 | $1.4 \cdot 10^{15}$ |

Members of XP:

- Every problem in FPT, such as [p-Vertex-Cover](/parameterized-vertex-cover/).
- [p-Clique](/parameterized-clique/) and [p-Independent-Set](/parameterized-independent-set/), by the brute force above. Both are W[1]-complete.
- [p-Dominating-Set](/parameterized-dominating-set/), by trying all sets of at most $k$ vertices in time $O(n^{k+1})$. It is W[2]-complete.
- Every problem in the [W hierarchy](/w-hierarchy/). The levels W[t] are subsets of W[P], and W[P] is a subset of XP.

Problems outside XP:

- Graph coloring with the number $q$ of colors as the parameter, unless P = NP. Its slice $q = 3$ is NP-complete, and a problem in XP has every slice in P. Such problems are [para-NP-hard](/para-np-hardness/).
- Every parameterized problem whose classical form is undecidable, for example the [halting problem](/halting-problem/) with the parameter 0.

## Related definitions

- [Fixed-parameter tractable](/fixed-parameter-tractable/) problems form the subclass FPT, with time $f(k) \cdot n^{c}$.
- The [W hierarchy](/w-hierarchy/) $\mathrm{FPT} \subseteq \mathrm{W[1]} \subseteq \mathrm{W[2]} \subseteq \cdots \subseteq \mathrm{W[P]} \subseteq \mathrm{XP}$ lies between the two classes. Only the last link, FPT $\ne$ XP, is known to be proper.
- [W-hardness](/w-hardness/) of a problem in XP is the usual evidence that its XP algorithm cannot be made FPT.
- [Para-NP](/para-np-hardness/) is the class of problems that a nondeterministic algorithm decides in time $f(k) \cdot n^{c}$. It also contains FPT, and it is not contained in XP unless P = NP.

## References
