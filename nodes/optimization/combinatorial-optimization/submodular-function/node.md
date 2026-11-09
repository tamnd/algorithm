---
tag: X2QZ8A
kind: definition
slug: submodular-function
name: Submodular function
aliases:
- diminishing returns function
- submodularity
- submodular set function
area: optimization/combinatorial-optimization
level: core
summary: Set function with diminishing marginal returns, generalizing rank and cut functions.
prereqs: [matroid, convex-function]
see_also: [submodular-minimization, rado-edmonds-theorem, matroid-intersection-theorem, min-cut-problem, maximum-cut, facility-location-problem, influence-maximization, greedy-set-cover]
sources:
  - book: isbn:9780444520869
    title: Satoru Fujishige, Submodular Functions and Optimization, second edition, Elsevier, 2005
    locator: Chapter II, Submodular systems and base polyhedra
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer, 2003
    locator: Chapter 44, Submodular functions and polymatroids
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer, 2018
    locator: Chapter 14, Generalizations of matroids (the sections on polymatroids and submodular function minimization)
  - paper: "László Lovász, Submodular functions and convexity, in Mathematical Programming, The State of the Art (Bonn 1982), Springer, 1983, 235 to 257"
    locator: the extension of a set function to the cube and the theorem that it is convex exactly for submodular functions
  - paper: doi:10.1007/BF01588971
    title: George L. Nemhauser, Laurence A. Wolsey and Marshall L. Fisher, An analysis of approximations for maximizing submodular set functions I, Mathematical Programming 14, 265 to 294, 1978
    locator: the greedy bound 1 - 1/e for monotone submodular maximization under a cardinality constraint
  - paper: "Jack Edmonds, Submodular functions, matroids, and certain polyhedra, in Combinatorial Structures and Their Applications (Proceedings of the Calgary International Conference, 1969), Gordon and Breach, 1970, 69 to 87"
    locator: polymatroids and the greedy algorithm for submodular functions
---

A submodular function is a set function $f : 2^E \to \mathbb{R}$ on a finite set $E$ with $f(A) + f(B) \ge f(A \cup B) + f(A \cap B)$ for all $A, B \subseteq E$. Equivalently, it has *diminishing returns*: adding an element to a set gains at most as much as adding it to a subset of that set. Rank functions of [matroids](/matroid/), cut functions of graphs, coverage functions and entropy are submodular. Submodularity plays for set functions the role that convexity plays for functions on $\mathbb{R}^n$: a submodular function can be minimized in polynomial time ([submodular minimization](/submodular-minimization/)), and its Lovász extension is a [convex function](/convex-function/). But it also behaves like concavity: maximizing it is NP-hard in general, and greedy gives good approximations.

## Definition

Let $E$ be a finite set with $n = |E|$, and $f : 2^E \to \mathbb{R}$. For $A \subseteq E$ and $e \in E \setminus A$, write $A + e = A \cup \{e\}$ and $f(e \mid A) = f(A + e) - f(A)$, the *marginal gain* of $e$ at $A$.

**Definition.** $f$ is *submodular* if
$$f(A) + f(B) \ge f(A \cup B) + f(A \cap B) \qquad \text{for all } A, B \subseteq E.$$

The following are equivalent:

1. $f$ is submodular.
2. **Diminishing returns.** $f(e \mid A) \ge f(e \mid B)$ for all $A \subseteq B \subseteq E$ and $e \in E \setminus B$.
3. **Local form.** $f(A + e) + f(A + e') \ge f(A) + f(A + e + e')$ for all $A \subseteq E$ and distinct $e, e' \in E \setminus A$.

Condition 1 gives 2 with $A + e$ and $B$ in place of $A$ and $B$. Condition 2 gives 3 with $B = A + e'$. Condition 3 gives 1 by adding the local inequalities along a chain from $A \cap B$ to $A$ and from $A \cap B$ to $B$.

**Further terms.**

- $f$ is *normalized* if $f(\emptyset) = 0$, and *monotone* (nondecreasing) if $f(A) \le f(B)$ for $A \subseteq B$.
- $f$ is *supermodular* if $-f$ is submodular, and *modular* if both hold. Modular functions are exactly $f(A) = c + \sum_{e \in A} w(e)$.
- $f$ is *symmetric* if $f(A) = f(E \setminus A)$ for all $A$.

**Model of computation.** In algorithms, $f$ is usually given by a *value oracle* that returns $f(A)$ for a given $A$. Running times count oracle calls and further arithmetic operations.

## Examples and non-examples

**Examples.**

- **Matroid rank.** The rank function $r$ of a matroid is normalized, monotone, submodular, and has $r(A) \le |A|$ and integer values. Conversely, every such function is the rank function of a matroid.
- **Cut functions.** For a graph with nonnegative edge weights, the weight $\delta(S)$ of the edges with exactly one end in $S$ is symmetric and submodular, but not monotone. The same holds for the weight of the arcs leaving $S$ in a directed graph, without symmetry. These functions underlie [minimum cut](/min-cut-problem/) and [maximum cut](/maximum-cut/).
- **Coverage.** For sets $T_1, \ldots, T_n$, the function $f(S) = |\bigcup_{i \in S} T_i|$ is monotone submodular. It is the objective of maximum coverage and of [set cover](/greedy-set-cover/).
- **Facility location.** With values $v_{ij} \ge 0$ for site $i$ and customer $j$, the function $f(S) = \sum_j \max_{i \in S} v_{ij}$ is monotone submodular. It is the objective of the [facility location problem](/facility-location-problem/) in its profit form.
- **Concave functions of the size.** $f(S) = g(|S|)$ with $g$ concave, and more generally $f(S) = g(w(S))$ with $w \ge 0$.
- **Entropy and information.** For random variables $X_e$, $e \in E$, the joint entropy $H(X_S)$ is monotone submodular. This is one of the Shannon inequalities. Spread functions in [influence maximization](/influence-maximization/) are submodular for the standard models.
- **Log-determinants.** For a positive definite matrix $K$, the function $S \mapsto \log \det K_{S,S}$ is submodular.

**A worked example.** Let $T_1 = \{1, 2\}$, $T_2 = \{2, 3\}$ and $T_3 = \{3, 4\}$, with coverage $f$. The gain of element 2 at $\emptyset$ is $f(\{2\}) = 2$. At $\{1\}$ it is $f(\{1, 2\}) - f(\{1\}) = 3 - 2 = 1$, and at $\{1, 3\}$ it is $f(\{1, 2, 3\}) - f(\{1, 3\}) = 4 - 4 = 0$. The gains fall as the set grows. With $A = \{1, 2\}$ and $B = \{2, 3\}$: $f(A) + f(B) = 3 + 3 = 6 \ge f(A \cup B) + f(A \cap B) = 4 + 2 = 6$.

**Non-examples.**

- $f(S) = |S|^2$ is supermodular, not submodular: the gain $2|S| + 1$ grows with $S$.
- The number of edges of a graph with both ends in $S$ is supermodular.
- Complementary goods: on $E = \{a, b\}$, let $f(S) = 1$ if $S = E$ and $0$ otherwise. Then $f(\{a\}) + f(\{b\}) = 0 < f(E) + f(\emptyset) = 1$.
- The size of a largest [matching](/bipartite-matching/) in the subgraph induced by $S$ is not submodular in general. On the path $a - b - c - d$, take $A = \{a, b, c\}$ and $B = \{b, c, d\}$. Then $f(A) + f(B) = 1 + 1 = 2$, but $f(A \cup B) + f(A \cap B) = 2 + 1 = 3$. The gain of $d$ is 0 at $\{b, c\}$ but 1 at the larger set $\{a, b, c\}$.

## Related definitions

- **Polymatroid.** A normalized, monotone submodular $f$ defines the polymatroid $P(f) = \{x \ge 0 : x(S) \le f(S) \text{ for all } S\}$ and the base polytope $B(f) = \{x \in P(f) : x(E) = f(E)\}$. Edmonds (1970) showed that greedy optimizes linear functions over them. See the [Rado-Edmonds theorem](/rado-edmonds-theorem/).
- **Lovász extension.** For $x \in [0, 1]^E$, let $\hat f(x) = \int_0^1 f(\{e : x_e \ge \theta\}) \, d\theta$. It agrees with $f$ on 0-1 vectors and is piecewise linear. Lovász (1983) proved that $\hat f$ is convex exactly when $f$ is submodular, and that $\min_{[0,1]^E} \hat f = \min_A f(A)$. This links [submodular minimization](/submodular-minimization/) to convex optimization.
- **Submodular minimization.** Polynomial in the value oracle model, by the ellipsoid method (Grötschel, Lovász and Schrijver 1981) and by combinatorial algorithms (Iwata, Fleischer and Fujishige 2001; Schrijver 2000). See [submodular minimization](/submodular-minimization/).
- **Submodular maximization.** NP-hard, as it contains [maximum cut](/maximum-cut/). For monotone normalized $f$ and the constraint $|S| \le k$, greedy reaches $1 - 1/e$ of the optimum (Nemhauser, Wolsey and Fisher, 1978), and no polynomial algorithm does better unless P = NP, already for coverage.
- **Intersection theorems.** The [matroid intersection theorem](/matroid-intersection-theorem/) uses only the submodularity of the two rank functions, and extends to polymatroid intersection.
- **Discrete convexity.** L-convex and M-convex functions (Murota) refine submodularity on integer lattices.

## References
