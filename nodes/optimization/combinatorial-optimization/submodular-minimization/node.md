---
tag: VCR9SK
kind: problem
slug: submodular-minimization
name: Submodular function minimization
aliases:
- SFM
- submodular minimization
area: optimization/combinatorial-optimization
level: advanced
summary: Minimize a submodular set function, solvable in polynomial time.
prereqs: [submodular-function, ellipsoid-method, convex-function]
see_also: [submodular-function, min-cut-problem, max-flow-problem, stoer-wagner, ellipsoid-method, rado-edmonds-theorem, matroid-intersection, graph-partitioning-problem]
sources:
  - paper: doi:10.1007/BF02579273
    title: Martin Grötschel, László Lovász and Alexander Schrijver, The ellipsoid method and its consequences in combinatorial optimization, Combinatorica 1(2), 169 to 197, 1981
    locator: the polynomial-time minimization of submodular functions by the ellipsoid method
  - paper: doi:10.1145/502090.502096
    title: Satoru Iwata, Lisa Fleischer and Satoru Fujishige, A combinatorial strongly polynomial algorithm for minimizing submodular functions, Journal of the ACM 48(4), 761 to 777, 2001
    locator: the scaling algorithm and its strongly polynomial version
  - paper: doi:10.1006/jctb.2000.1989
    title: Alexander Schrijver, A combinatorial algorithm minimizing submodular functions in strongly polynomial time, Journal of Combinatorial Theory Series B 80(2), 346 to 355, 2000
    locator: the combinatorial strongly polynomial algorithm
  - paper: doi:10.1007/s10107-007-0189-2
    title: James B. Orlin, A faster strongly polynomial time algorithm for submodular function minimization, Mathematical Programming 118(2), 237 to 251, 2009
    locator: the bound O(n^5 EO + n^6)
  - paper: "László Lovász, Submodular functions and convexity, in Mathematical Programming, The State of the Art (Bonn 1982), Springer, 1983, 235 to 257"
    locator: the convex extension and the reduction of minimization to convex minimization
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer, 2003
    locator: Chapter 45, Submodular function minimization
  - book: isbn:9780444520869
    title: Satoru Fujishige, Submodular Functions and Optimization, second edition, Elsevier, 2005
    locator: the chapters on submodular function minimization and the minimum-norm base
  - paper: "Maurice Queyranne, Minimizing symmetric submodular functions, Mathematical Programming 82, 3 to 12, 1998"
    locator: the O(n^3) algorithm for symmetric submodular functions
---

Submodular function minimization (SFM) asks for a set $S \subseteq E$ that minimizes a [submodular function](/submodular-function/) $f : 2^E \to \mathbb{R}$, given by a value oracle. It is the discrete counterpart of convex minimization, and it is solvable in polynomial time: Grötschel, Lovász and Schrijver (1981) gave the first polynomial algorithm with the [ellipsoid method](/ellipsoid-method/), and Iwata, Fleischer and Fujishige (2001) and Schrijver (2000) gave combinatorial strongly polynomial algorithms. Orlin (2009) reduced the bound to $O(n^5 \cdot \mathrm{EO} + n^6)$, where $\mathrm{EO}$ is the time of one oracle call, and cutting plane methods (Lee, Sidford and Wong, 2015) reduced it further to about $n^3$ oracle calls up to logarithmic factors. Many problems are special cases, among them [minimum $s$-$t$ cut](/min-cut-problem/), the minimum of matroid rank expressions in [matroid intersection](/matroid-intersection/), and separation over polymatroids. Adding a size constraint, as in [graph bisection](/graph-partitioning-problem/), makes the problem NP-hard.

## In plain words

Each group of items has a cost, and the costs have the diminishing returns property: an item adds less when the group is already large. You want the group with the least cost. There are far too many groups to try them all.

This task can be solved quickly for every cost of this kind, even if you can only ask for the cost of one group at a time. The reason is that such costs behave like a smooth bowl shape, so a search can go downhill. Cutting a network into two parts at least cost is the best known example.

## Definition

**Input.** A finite set $E$ with $n = |E|$, and a submodular function $f : 2^E \to \mathbb{R}$, given by a *value oracle* that returns $f(A)$ for any $A \subseteq E$. Often $f(\emptyset) = 0$ is assumed, which loses nothing.

**Output.** A set $S^* \subseteq E$ with $f(S^*) = \min_{A \subseteq E} f(A)$.

**Running time.** It counts oracle calls (EO) and other arithmetic operations. An algorithm is *strongly polynomial* if both counts are bounded by a polynomial in $n$ alone, and *weakly polynomial* if they also depend on $\log M$, where $M$ bounds $|f(A)|$ for integer-valued $f$.

**Min-max theorem.** For normalized $f$, let $B(f) = \{ x \in \mathbb{R}^E : x(A) \le f(A) \text{ for all } A, \; x(E) = f(E) \}$ be the base polytope, and $x^-(E) = \sum_e \min(x_e, 0)$. Then
$$\min_{A \subseteq E} f(A) = \max_{x \in B(f)} x^-(E).$$
A base $x$ is given as a convex combination of greedy vertices, each computed with $n$ oracle calls ([Rado-Edmonds theorem](/rado-edmonds-theorem/)). So both a set $A$ and a base $x$ are short certificates. The combinatorial algorithms find both.

**Structure of the minimizers.** If $A$ and $B$ are minimizers, then $f(A \cup B) + f(A \cap B) \le f(A) + f(B) = 2 \min f$, so $A \cup B$ and $A \cap B$ are minimizers too. The minimizers form a lattice, with a unique smallest and a unique largest minimizer.

## Variants

- **Symmetric functions.** For symmetric $f$, such as a graph cut function, $\emptyset$ and $E$ are trivial minimizers, so the task is to minimize over $\emptyset \ne A \ne E$. Queyranne (1998) solved this with $O(n^3)$ oracle calls, generalizing the global minimum cut algorithms of [Nagamochi and Ibaraki](/nagamochi-ibaraki/) and [Stoer and Wagner](/stoer-wagner/).
- **Minimizing over a lattice family.** Minimizing over sets that contain a given set, or avoid one, or over a ring family, reduces to the basic problem. Minimizing over odd sets, or over sets of a parity family, is also polynomial (Grötschel, Lovász and Schrijver; Goemans and Ramakrishnan).
- **Constrained minimization.** With a constraint $|A| \ge k$ or $|A| = k$, the problem is NP-hard, since it contains [graph bisection](/graph-partitioning-problem/). Svitkina and Fleischer (2011) showed that the version with $|A| \ge k$ cannot be approximated within a factor of about $\sqrt{n / \log n}$ with polynomially many oracle calls.
- **Sums of simple functions.** If $f = \sum_i f_i$ with each $f_i$ depending on few elements, faster methods exist. If each $f_i$ is a submodular function of at most 2 or 3 variables, a [minimum cut](/min-cut-problem/) solves the problem, which is the basis of graph cut methods in computer vision.
- **Approximate minimization.** Projected subgradient methods on the Lovász extension find a set within $\epsilon$ of the minimum with a number of oracle calls that grows with $1 / \epsilon^2$.

## Examples

**Project selection.** Tasks 1, 2 and 3 earn 3, 1 and 2. Task $i$ needs the resources $T_i$, with $T_1 = \{p, q\}$, $T_2 = \{q, u\}$ and $T_3 = \{s, t\}$, and each resource costs 1, paid once however many tasks use it. The cost minus profit of a set $A$ of tasks is $f(A) = |\bigcup_{i \in A} T_i| - \sum_{i \in A} w_i$, a coverage function minus a modular function, so it is submodular.

| $A$ | $\emptyset$ | $\{1\}$ | $\{2\}$ | $\{3\}$ | $\{1, 2\}$ | $\{1, 3\}$ | $\{2, 3\}$ | $\{1, 2, 3\}$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| resources | 0 | 2 | 2 | 2 | 3 | 4 | 4 | 5 |
| profit | 0 | 3 | 1 | 2 | 4 | 5 | 3 | 6 |
| $f(A)$ | 0 | $-1$ | 1 | 0 | $-1$ | $-1$ | 1 | $-1$ |

The minimum is $-1$, so the best profit is 1. The minimizers are $\{1\}$, $\{1, 2\}$, $\{1, 3\}$ and $\{1, 2, 3\}$. They are closed under union and intersection, with smallest minimizer $\{1\}$ and largest $\{1, 2, 3\}$.

**Minimum $s$-$t$ cut.** For a directed graph with capacities and two vertices $s$ and $t$, let $f(A)$ be the capacity of the arcs leaving $A + s$, for $A \subseteq V \setminus \{s, t\}$. Then $f$ is submodular, and its minimum is the minimum cut. In this case [maximum flow](/max-flow-problem/) algorithms such as [push-relabel](/push-relabel/) are much faster than general SFM.

**Matroid intersection.** $U \mapsto r_1(U) + r_2(E \setminus U)$ is submodular, and its minimum is the size of a largest common independent set ([matroid intersection theorem](/matroid-intersection-theorem/)).

**Polymatroid separation.** A vector $x \ge 0$ is in $P(f)$ exactly when $\min_A \bigl( f(A) - x(A) \bigr) \ge 0$. So SFM is the separation problem for polymatroids, and for matroid polytopes.

## Known algorithms

| method | bound | notes |
| --- | --- | --- |
| Ellipsoid method (Grötschel, Lovász and Schrijver 1981, 1988) | polynomial, later strongly polynomial | not practical |
| Cunningham (1985) | pseudo-polynomial | the first combinatorial method for general $f$ |
| Iwata, Fleischer and Fujishige (2001) | strongly polynomial | combinatorial, by scaling |
| Schrijver (2000) | $O(n^8 \cdot \mathrm{EO} + n^9)$ | combinatorial, strongly polynomial |
| Orlin (2009) | $O(n^5 \cdot \mathrm{EO} + n^6)$ | combinatorial, strongly polynomial |
| Lee, Sidford and Wong (2015) | $O(n^3 \log^2 n \cdot \mathrm{EO} + n^4 \log^{O(1)} n)$ | cutting plane method |
| Fujishige-Wolfe minimum-norm point | pseudo-polynomial bounds only | often the fastest in practice |
| Queyranne (1998), symmetric $f$ | $O(n^3)$ oracle calls | proper nonempty minimizer |

The combinatorial algorithms keep a point $x \in B(f)$ as a convex combination of greedy vertices and improve $x^-(E)$ by exchanges along chains, in the spirit of augmenting paths. The ellipsoid and cutting plane methods minimize the Lovász extension, which is convex, over the cube $[0, 1]^E$; its minimum value equals $\min f$, and a minimizing set can be read off from a minimizing point.

## Bounds

- **Upper bound.** Strongly polynomial: $O(n^3 \log^2 n)$ oracle calls with polynomial extra time (Lee, Sidford and Wong, 2015). With integer values bounded by $M$, about $O(n^2 \log(nM))$ oracle calls suffice in the same work.
- **Lower bound.** Every algorithm must call the oracle on many sets; the known lower bounds on the number of calls are much smaller than the upper bounds, and closing the gap is open.
- **Exactness.** The value $\min f$ is attained at a set, and the min-max theorem gives a certificate of optimality. Maximization of submodular functions is NP-hard and is studied through approximation ratios such as $1 - 1/e$ and $1/2$. Minimization without constraints is solved exactly.
- **Constraints.** Under a cardinality constraint the problem is NP-hard, and in the oracle model it needs exponentially many calls to approximate within $o(\sqrt{n / \log n})$ (Svitkina and Fleischer, 2011).

## Reductions

- **Minimum cut to SFM**, with the cut function, as above. In the other direction, functions that are sums of submodular terms of at most 3 variables reduce to a minimum cut.
- **Matroid intersection to SFM**: the min side of the matroid intersection theorem is an SFM instance. The optimal set itself needs the matroid intersection algorithm.
- **SFM to convex minimization**: by the Lovász extension, minimizing $f$ is minimizing a convex function over $[0, 1]^E$, with subgradients computed by one greedy step.
- **Separation over $P(f)$ to SFM**, as above. With the equivalence of separation and optimization through the [ellipsoid method](/ellipsoid-method/) and [separation oracles](/separation-oracle/), this is how polynomial algorithms for polymatroid problems were first obtained.
- **Graph bisection to constrained SFM**: the cut function with $|A| = n / 2$. This shows that the constraint makes the problem NP-hard.

## Applications

- **Computer vision.** Energy minimization in [Markov random fields](/markov-random-field/) with submodular pair terms, for example [image segmentation](/image-segmentation/), solved by minimum cuts.
- **Combinatorial optimization.** Separation for matroid and polymatroid polytopes, minimum cuts of all kinds, and the minimum of rank expressions in matroid intersection and union.
- **Machine learning.** Structured sparsity norms, clustering by minimum normalized cuts, and the decomposable SFM problems that arise from them.
- **Economics and operations research.** Project selection and the closure problem, and the test whether a cost function is in the core of a cooperative game.

## References
