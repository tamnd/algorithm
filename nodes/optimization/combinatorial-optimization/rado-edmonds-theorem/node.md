---
tag: WHPVS3
kind: theorem
slug: rado-edmonds-theorem
name: Rado-Edmonds theorem
aliases:
- matroid greedy characterization
- Edmonds' greedy theorem
- greedy characterization of matroids
area: optimization/combinatorial-optimization
level: core
summary: Greedy yields a maximum-weight independent set for every weight function exactly when the system is a matroid.
prereqs: [matroid, matroid-greedy-algorithm, lp-duality]
see_also: [matroid-greedy-theorem, matroid-greedy-algorithm, maximum-weight-matroid-basis, spanning-tree-polytope, submodular-function, submodular-minimization, matroid-intersection-theorem, total-unimodularity]
sources:
  - paper: doi:10.1007/BF01584082
    title: Jack Edmonds, Matroids and the greedy algorithm, Mathematical Programming 1(1), 127 to 136, 1971
    locator: the theorem that greedy is optimal for all weights exactly on matroids, and the description of the matroid polytope
  - paper: doi:10.1112/plms/s3-7.1.300
    title: Richard Rado, Note on independence functions, Proceedings of the London Mathematical Society s3-7(1), 300 to 320, 1957
    locator: the greedy property of independence functions
  - paper: "Jack Edmonds, Submodular functions, matroids, and certain polyhedra, in Combinatorial Structures and Their Applications (Proceedings of the Calgary International Conference, 1969), Gordon and Breach, 1970, 69 to 87"
    locator: the greedy algorithm for polymatroids and the matroid polytope
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer, 2018
    locator: Chapter 13, Matroids (the greedy algorithm, the rank quotient and the matroid polytope)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer, 2003
    locator: Chapter 40, The greedy algorithm and the independent set polytope
  - paper: "Bernhard Korte and Dirk Hausmann, An analysis of the greedy heuristic for independence systems, Annals of Discrete Mathematics 2, 1978"
    locator: the rank quotient bound for greedy on independence systems
---

The Rado-Edmonds theorem says that an independence system is a [matroid](/matroid/) exactly when the [greedy algorithm](/matroid-greedy-algorithm/) finds a heaviest independent set for every choice of weights. Edmonds (1971) gave it a linear programming form: for a matroid with rank function $r$, greedy solves $\max \{ w^\top x : x \ge 0, \; x(S) \le r(S) \text{ for all } S \}$ for every weight vector $w$, and its order gives an optimal dual solution on a chain of sets. This page proves that form. Its main consequence is Edmonds' description of the matroid polytope: the convex hull of the independent sets is cut out by the rank inequalities. The exchange proof of the plain statement is on the page [greedy optimality on matroids](/matroid-greedy-theorem/).

## Statement

An *independence system* is a pair $(E, \mathcal{I})$ with $E$ finite, $\emptyset \in \mathcal{I}$, and $I \in \mathcal{I}$, $J \subseteq I$ implying $J \in \mathcal{I}$. Its *rank function* is $r(S) = \max \{ |I| : I \in \mathcal{I}, I \subseteq S \}$, and its *rank polytope* is
$$P(r) = \{ x \in \mathbb{R}^E : x \ge 0, \; x(S) \le r(S) \text{ for all } S \subseteq E \}, \qquad x(S) = \textstyle\sum_{e \in S} x_e .$$
For $w \in \mathbb{R}^E$, GREEDY sorts the elements as $e_1, \ldots, e_n$ with $w(e_1) \ge \cdots \ge w(e_n)$, starts with $J = \emptyset$, and for $i = 1, \ldots, n$ stops if $w(e_i) \le 0$ and otherwise adds $e_i$ to $J$ when $J + e_i \in \mathcal{I}$.

**Theorem (Rado 1957, Edmonds 1971).** For an independence system $(E, \mathcal{I})$ the following are equivalent.

1. $(E, \mathcal{I})$ is a matroid.
2. For every $w \in \mathbb{R}^E$ and every order of equal weights, GREEDY returns $J$ with $w(J) = \max \{ w^\top x : x \in P(r) \}$.
3. For every $w \in \mathbb{Z}_{\ge 0}^E$, GREEDY returns an independent set of largest weight.

We use the matroid axiom in this form: *for every $S \subseteq E$, all maximal independent subsets of $S$ have the same size*. This is equivalent to the augmentation axiom.

## In plain words

You have a list of items, each with a value, and a rule that says which groups of items you may keep together. The rule allows every part of an allowed group. The simple greedy plan takes the most valuable item, then the next one that still fits, and so on.

The theorem says that this plan is best for every list of values exactly when the rule has the matroid property. It says more: the greedy plan is even best against a relaxed problem, in which you may take fractions of items as long as no group gets more than its size limit. So, for matroids, the fractional problem and the whole-item problem have the same answer.

## Proof

**(1) implies (2).** Let $w \in \mathbb{R}^E$, with the elements in the order used by GREEDY, and let $k$ be the number of elements with $w(e_i) > 0$, so GREEDY looks only at $e_1, \ldots, e_k$. Write $w_i = w(e_i)$, $S_i = \{e_1, \ldots, e_i\}$ and $S_0 = \emptyset$.

*Step 1: $|J \cap S_i| = r(S_i)$ for $i \le k$.* The set $J \cap S_i$ is independent. If $e_j \in S_i \setminus J$, then GREEDY rejected $e_j$, so $(J \cap S_{j-1}) + e_j \notin \mathcal{I}$, and since $\mathcal{I}$ is closed under subsets, $(J \cap S_i) + e_j \notin \mathcal{I}$. So $J \cap S_i$ is a maximal independent subset of $S_i$. In a matroid it has size $r(S_i)$.

*Step 2: the value of $J$.* By Step 1, $e_i \in J$ exactly when $r(S_i) - r(S_{i-1}) = 1$ for $i \le k$, and otherwise this difference is 0. So, by summation by parts,
$$w(J) = \sum_{i=1}^{k} w_i \bigl( r(S_i) - r(S_{i-1}) \bigr) = \sum_{i=1}^{k-1} (w_i - w_{i+1}) \, r(S_i) + w_k \, r(S_k).$$

*Step 3: an upper bound on $P(r)$.* Let $x \in P(r)$. Since $x \ge 0$ and $w_i \le 0$ for $i > k$, $w^\top x \le \sum_{i=1}^{k} w_i x_{e_i}$. Summation by parts again gives
$$\sum_{i=1}^{k} w_i x_{e_i} = \sum_{i=1}^{k-1} (w_i - w_{i+1}) \, x(S_i) + w_k \, x(S_k) \le \sum_{i=1}^{k-1} (w_i - w_{i+1}) \, r(S_i) + w_k \, r(S_k),$$
because the coefficients $w_i - w_{i+1}$ and $w_k$ are nonnegative and $x(S_i) \le r(S_i)$. By Step 2 the right side is $w(J)$.

*Step 4: $J$ attains the bound.* The vector $\chi^J$ is in $P(r)$, because $|J \cap S| \le r(S)$ for every $S$. So $w(J) = \max \{ w^\top x : x \in P(r) \}$. If $k = 0$, then $J = \emptyset$ and both sides are 0.

**(2) implies (3).** Let $w \ge 0$ and let $I$ be any independent set. Then $\chi^I \in P(r)$, so $w(I) \le \max_{P(r)} w^\top x = w(J)$ by (2), and $J$ is independent. So $J$ has largest weight.

**(3) implies (1).** Suppose $(E, \mathcal{I})$ is not a matroid. Then some $S \subseteq E$ has maximal independent subsets $A$ and $B$ with $a = |A| < |B|$. Define
$$w(e) = a + 2 \text{ for } e \in A, \qquad w(e) = a + 1 \text{ for } e \in S \setminus A, \qquad w(e) = 0 \text{ for } e \notin S.$$
GREEDY first takes all of $A$, because $A$ is independent and its elements are the heaviest. Then every element of $S \setminus A$ is rejected, because $A$ is maximal in $S$, and GREEDY stops at the elements of weight 0. So GREEDY returns $A$, with $w(A) = a(a + 2) = a^2 + 2a$. But $B$ is independent with $w(B) \ge |B| (a + 1) \ge (a + 1)^2 = a^2 + 2a + 1$. So (3) fails. $\blacksquare$

**The dual solution.** Steps 2 and 3 are [LP duality](/lp-duality/) in disguise. The dual of $\max \{ w^\top x : x \in P(r) \}$ is $\min \{ \sum_S r(S) \, y_S : y \ge 0, \; \sum_{S \ni e} y_S \ge w(e) \text{ for all } e \}$, and
$$y_{S_i} = w_i - w_{i+1} \;\; (1 \le i < k), \qquad y_{S_k} = w_k, \qquad y_S = 0 \text{ otherwise}$$
is a feasible dual solution with value $w(J)$. It is supported on the chain $S_1 \subset \cdots \subset S_k$, and it is integral when $w$ is integral.

## Consequences

- **The matroid polytope (Edmonds 1970, 1971).** For a matroid, $P(r) = \operatorname{conv} \{ \chi^I : I \in \mathcal{I} \}$. The hull is contained in $P(r)$ by Step 4. If a point of $P(r)$ were outside the hull, a weight vector $w$ would separate it, so $\max_{P(r)} w^\top x$ would be larger than the weight of every independent set, which contradicts (2). The [spanning tree polytope](/spanning-tree-polytope/) is a face of the polytope of the graphic matroid.
- **Total dual integrality.** The chain dual shows that the system $x \ge 0$, $x(S) \le r(S)$ is totally dual integral. The rows of a chain form a matrix with the consecutive ones property, which is [totally unimodular](/total-unimodularity/).
- **Polymatroids.** Let $f$ be a nondecreasing [submodular function](/submodular-function/) with $f(\emptyset) = 0$, and $P(f)$ its polytope, defined as $P(r)$ with $f$ in place of $r$. Take the greedy vector $x_{e_i} = f(S_i) - f(S_{i-1})$ for $i \le k$ and $x_{e_i} = 0$ for $i > k$. Submodularity puts it in $P(f)$, and Steps 2 to 4 show that it maximizes $w^\top x$ over $P(f)$ (Edmonds 1970). This is the basis of the theory of polymatroids and of [submodular minimization](/submodular-minimization/).
- **Optimization and separation.** By the theorem, linear optimization over $P(r)$ takes one sort and $n$ oracle calls. Testing whether $x \in P(r)$ means minimizing the submodular function $r(S) - x(S)$, which is also polynomial. Both directions agree with the equivalence of optimization and separation by the [ellipsoid method](/ellipsoid-method/).
- **Intersections.** The polytope of common independent sets of two matroids is $P(r_1) \cap P(r_2)$ ([matroid intersection theorem](/matroid-intersection-theorem/)). For three matroids this fails.
- **Bases.** Greedy with all weights shifted to be positive returns a heaviest [basis](/maximum-weight-matroid-basis/). For graphic matroids this is [Kruskal's algorithm](/kruskal/).

## Tightness

- **Integrality is not enough.** On the path with edges $ab$, $bc$, $cd$, the matchings form an independence system that is not a matroid: $\{bc\}$ and $\{ab, cd\}$ are both maximal. Its rank polytope is the bipartite matching polytope of the path, which is integral. But with weights $w(ab) = 2$, $w(bc) = 3$, $w(cd) = 2$, GREEDY takes $bc$ and stops at weight 3, while $\{ab, cd\}$ weighs 4. So (2) is about GREEDY, not only about $P(r)$ having integral vertices.
- **How far greedy can be from optimal.** For an independence system, let the *rank quotient* $q$ be the minimum over $S$ of the ratio of the smallest to the largest size of a maximal independent subset of $S$. Jenkyns (1976) and Korte and Hausmann (1978) proved that GREEDY always reaches at least $q$ times the optimum for $w \ge 0$, and that this is tight. A matroid is exactly a system with $q = 1$. For matchings $q \ge 1/2$, and in the path example $q = 1/2$.
- **The stop rule.** With negative weights, GREEDY must stop at the first element of weight at most 0. Without the stop rule it returns a heaviest *basis*, which is a different problem, and (2) fails.
- **Few weight values suffice.** The proof of (3) implies (1) uses only three weight values, so the matroid property is already forced by weights in $\{0, a + 1, a + 2\}$.

## History

Richard Rado (1957) studied independence functions and showed that a greedy-type property holds for them. David Gale (1968) proved the optimality of greedy for matroids in the form of optimal assignments. Jack Edmonds presented the polyhedral view at the Calgary conference of 1969, published in 1970, with the greedy algorithm for polymatroids, and his 1971 paper "Matroids and the greedy algorithm" proved that greedy is optimal for all weights exactly on matroids and described the matroid polytope. For spanning trees the greedy method is much older: Borůvka (1926) and Kruskal (1956). The rank quotient bound for systems that are not matroids is due to Jenkyns (1976) and to Korte and Hausmann (1978).

## References
