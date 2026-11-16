---
tag: RHNP37
kind: definition
slug: parameter
name: Parameter
aliases:
- problem parameter
area: complexity/parameterized-complexity
level: intro
summary: "A number k attached to each instance, such as the solution size or the treewidth, that parameterized complexity measures apart from the input size n."
prereqs: [decision-problem, input-size]
see_also: [parameterized-problem, fixed-parameter-tractable, xp, para-np-hardness, parameterized-vertex-cover, parameterized-independent-set, treewidth, w-hierarchy]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 1, Introduction (parameterized problems and the choice of the parameter)
  - book: isbn:9783540299523
    title: Jörg Flum and Martin Grohe, Parameterized Complexity Theory, Springer, 2006
    locator: Chapter 1, Fixed-Parameter Tractability (parameterizations as maps from instances to natural numbers)
  - book: isbn:9781447155584
    title: Rodney G. Downey and Michael R. Fellows, Fundamentals of Parameterized Complexity, Springer, 2013
    locator: Chapter 2, The Basic Definitions
  - paper: doi:10.1137/S0097539792228228
    title: "Rodney G. Downey and Michael R. Fellows, Fixed-parameter tractability and completeness I: basic results, SIAM Journal on Computing 24(4), 873-921 (1995)"
    locator: the definitions of parameterized problems and of fixed-parameter tractability
---

A parameter is a natural number $k$ that is attached to each instance $x$ of a problem and that is measured apart from the [input size](/input-size/) $n = |x|$. Typical parameters are the size of the solution that the instance asks for, a structural measure of the input such as the [treewidth](/treewidth/) or the largest degree of a graph, or the number of colors, variables or layers. Parameterized complexity asks how the running time depends on $n$ and $k$ together. A good parameter is small on the inputs that occur in practice, so that a time such as $2^k n$ is fast even when $n$ is large. The same problem can be easy for one parameter and hard for another, so a statement about parameterized complexity always names its parameter.

## Definition

There are two equivalent ways to attach the parameter.

**As part of the input.** A [parameterized problem](/parameterized-problem/) is a set $L \subseteq \Sigma^* \times \mathbb{N}$ of pairs $(x, k)$. In the pair $(x, k)$, the string $x$ is the instance and the number $k$ is its parameter. This is the form of Downey and Fellows and of Cygan et al. The instance and the parameter are given together, and the size of the input is $|x| + k$ or $|x|$, which makes no difference to the classes below once $k \le |x|$ or $k$ is written in unary.

**As a map.** A parameterization of $\Sigma^*$ is a map $\kappa : \Sigma^* \to \mathbb{N}$ that is computable in polynomial time. A parameterized problem is then a pair $(Q, \kappa)$ with $Q \subseteq \Sigma^*$, and the parameter of an instance $x$ is $\kappa(x)$. This is the form of Flum and Grohe. It fits structural parameters, which are properties of $x$ itself.

A parameter that is hard to compute, such as the treewidth of a graph, fits the first form: the input gives a number $k$ and the question is asked only under the bound $\mathrm{tw}(G) \le k$, or the algorithm first checks that bound.

The point of a parameter is to measure running times in two variables. An algorithm runs in time $f(k) \cdot n^{c}$ when its number of steps on $(x, k)$ is at most that value for a computable function $f$ and a constant $c$. This is [fixed-parameter tractable](/fixed-parameter-tractable/) time. Time $n^{f(k)}$, where the degree of the polynomial grows with $k$, is the weaker class [XP](/xp/).

## Examples and non-examples

The table gives the value of some common graph parameters on small graphs. Here $\tau$ is the least size of a vertex cover, $\alpha$ the largest size of an independent set, $\omega$ the largest size of a clique, $\chi$ the chromatic number, $\Delta$ the largest degree and $\mathrm{tw}$ the treewidth. Each value was found by exhaustive search.

| graph | $n$ | $m$ | $\tau$ | $\alpha$ | $\omega$ | $\chi$ | $\Delta$ | $\mathrm{tw}$ |
|---|---|---|---|---|---|---|---|---|
| path $P_6$ | 6 | 5 | 3 | 3 | 2 | 2 | 2 | 1 |
| star $K_{1,6}$ | 7 | 6 | 1 | 6 | 2 | 2 | 6 | 1 |
| cycle $C_5$ | 5 | 5 | 3 | 2 | 2 | 3 | 2 | 2 |
| complete graph $K_4$ | 4 | 6 | 3 | 1 | 4 | 4 | 3 | 3 |
| $3 \times 3$ grid | 9 | 12 | 4 | 5 | 2 | 2 | 4 | 3 |
| Petersen graph | 10 | 15 | 6 | 4 | 2 | 3 | 3 | 4 |

The same problem behaves differently under different parameters:

- [Vertex cover](/parameterized-vertex-cover/) with the parameter $k$, the size of the cover, is fixed-parameter tractable: a [search tree](/vertex-cover-branching/) of depth $k$ solves it in time $O(2^k (n + m))$.
- Vertex cover with the parameter $n - k$ is the [independent set](/parameterized-independent-set/) problem with parameter $n - k$, because a set $S$ is a vertex cover exactly when $V \setminus S$ is independent. That problem is W[1]-hard, so it is not fixed-parameter tractable unless $\mathrm{FPT} = \mathrm{W[1]}$. The question is the same, and only the parameter changed.
- Independent set with the parameter $k$ is W[1]-hard, but with the parameter $\mathrm{tw}(G)$ it is solved in time $2^{\mathrm{tw}} \cdot n^{O(1)}$ by dynamic programming over a [tree decomposition](/tree-decomposition/).
- [Graph coloring](/k-coloring/) with the parameter $q$, the number of colors, is NP-complete already for $q = 3$. So no algorithm runs in time $n^{f(q)}$ unless P = NP. The problem is [para-NP-hard](/para-np-hardness/), and the number of colors is a poor parameter.

Two choices of the parameter are useless, and they show why the choice matters:

- The parameter $k = |x|$. Every decidable problem is fixed-parameter tractable under it: run any decision procedure, and its time $T(|x|)$ is a function of $k$ alone. The result says nothing about large inputs.
- A constant parameter, such as $k = 0$ for every instance. The time $f(k) n^c$ is then a polynomial, so the problem is fixed-parameter tractable exactly when it is in [P](/p/). The parameter adds no information.

A parameter is a number, not a set or a graph. The solution itself, for example a vertex cover $S$, is not a parameter, but its size $|S|$ can be.

## Related definitions

- A [parameterized problem](/parameterized-problem/) is the set of pairs $(x, k)$; it is the object that the classes FPT, XP and W[t] contain.
- [Fixed-parameter tractable](/fixed-parameter-tractable/) and [XP](/xp/) are the two basic time classes in terms of $n$ and the parameter.
- A [kernel](/kernel/) bounds the size of an equivalent instance by a function of the parameter alone.
- The [W hierarchy](/w-hierarchy/) and [para-NP-hardness](/para-np-hardness/) are the tools to show that a parameter does not help.
- Structural parameters such as [treewidth](/treewidth/) are the subject of [Courcelle's theorem](/courcelle-theorem/).

## References
