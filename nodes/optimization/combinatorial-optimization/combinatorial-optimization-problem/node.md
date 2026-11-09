---
tag: XYQCTZ
kind: definition
slug: combinatorial-optimization-problem
name: Combinatorial optimization problem
aliases:
- discrete optimization problem
- NP optimization problem
area: optimization/combinatorial-optimization
level: intro
summary: Optimize an objective over a finite but exponentially large set of discrete configurations.
prereqs: [np-hard, polynomial-time-reduction]
see_also: [knapsack-problem, traveling-salesman-problem, npo-class, approximation-ratio, lp-relaxation, local-search-problem, matroid, submodular-function]
sources:
  - book: isbn:9780486402581
    title: Christos H. Papadimitriou and Kenneth Steiglitz, Combinatorial Optimization, Algorithms and Complexity, Dover, 1998 (first published by Prentice Hall, 1982)
    locator: Chapter 1 (optimization problems, instances, neighborhoods and local optima) and Chapter 15 (the optimization, evaluation and recognition versions of a problem)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer, 2018
    locator: Chapter 1 (introduction) and Chapter 15 (NP-completeness, with optimization problems and their decision versions)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer, 2003
    locator: Chapter 1 (introduction) and Chapter 5 (polyhedral combinatorics, the convex hull of the incidence vectors of the feasible sets)
  - book: isbn:9783540654315
    title: Giorgio Ausiello, Pierluigi Crescenzi, Giorgio Gambosi, Viggo Kann, Alberto Marchetti-Spaccamela and Marco Protasi, Complexity and Approximation, Springer, 1999
    locator: Chapter 1 (the class NPO of NP optimization problems)
---

A combinatorial optimization problem asks for a best element of a finite set of discrete feasible solutions, where the set is not listed but is described by a short input, and is usually exponentially large in the length of that input. [Minimum spanning tree](/minimum-spanning-tree/), the [assignment problem](/assignment-problem/), the [knapsack problem](/knapsack-problem/) and the [traveling salesman problem](/traveling-salesman-problem/) are all of this kind. A search over all feasible solutions always finds the answer, but it takes too long for all but tiny inputs, so the field studies which problems have polynomial-time algorithms and which are [NP-hard](/np-hard/).

## Definition

**Instance.** An instance of an optimization problem is a pair $(F, c)$, where $F$ is a set, the *feasible solutions*, and $c : F \to \mathbb{Q}$ is the *cost function*. A minimization instance asks for an $x^* \in F$ with

$$ c(x^*) \le c(x) \quad \text{for all } x \in F. $$

Such an $x^*$ is an *optimal solution*, and $f^* = c(x^*)$ is the *optimal value*. A maximization instance reverses the inequality, and is the minimization instance of $-c$. If $F = \emptyset$, the instance is *infeasible*.

**Problem.** An optimization problem is a set of instances, each given by a string $I$ of length $|I|$, from which $F$ and $c$ are defined. It is *combinatorial* when $F$ is finite for each instance. Then each instance has an optimal solution or is infeasible, and the difficulty is only the size of $F$.

**The usual form.** There is a finite ground set $E$ with $|E| = n$ (the items, the edges, the cities), and $F \subseteq 2^E$ is a family of subsets of $E$. Each $e \in E$ has a weight $c_e$, and the cost is linear: $c(S) = \sum_{e \in S} c_e$. In the language of vectors, write $x \in \{0,1\}^n$ for the incidence vector of $S$ and $X \subseteq \{0,1\}^n$ for the set of incidence vectors of the feasible sets. The problem is then

$$ \min \{ c^\top x : x \in X \}, \qquad X \subseteq \{0,1\}^n, $$

which is a [binary integer program](/binary-integer-programming/) once $X$ is described by linear inequalities. Since a linear function takes its minimum over a finite set at a vertex of the convex hull, the problem is also $\min \{ c^\top x : x \in \operatorname{conv}(X) \}$, which is a [linear program](/linear-programming-problem/) over the polytope $\operatorname{conv}(X)$. Polyhedral combinatorics studies the inequalities that describe this polytope.

**NP optimization problems.** A problem is in the class [NPO](/npo-class/) when (1) the instances can be recognized in polynomial time, (2) each feasible solution has length polynomial in $|I|$, and membership $x \in F$ can be decided in polynomial time, and (3) $c(x)$ can be computed in polynomial time. Most combinatorial optimization problems are in NPO.

**Three versions.** Each problem has three versions:

- *optimization*: find an optimal $x^*$;
- *evaluation*: find the value $f^*$;
- *decision* (or recognition): given $(I, k)$, is there an $x \in F$ with $c(x) \le k$?

The decision version of an NPO problem is in [NP](/np/): a feasible $x$ with $c(x) \le k$ is the certificate. The decision version is never harder than the optimization version, so if the decision version is [NP-complete](/np-complete/), the optimization version is [NP-hard](/np-hard/). In the other direction, with integer costs in $[-C, C]$, a binary search over $k$ finds $f^*$ with $O(\log C)$ calls to the decision version. For many problems (TSP, knapsack, clique), a further self-reduction turns the value into an optimal solution with polynomially many calls, so the three versions are polynomially equivalent.

**Notation on these pages.** $n$ is the number of variables (items, cities, elements of $E$), $m$ the number of constraints or edges, $x$ a solution and $x^*$ an optimal one, $f$ the objective with optimal value $f^*$.

## Examples and non-examples

**Examples.** The table gives, for a small instance, the number of feasible solutions $|F|$, and the status of the problem.

| problem | ground set $E$ | feasible sets $F$ | $\lvert F \rvert$ at size 10 | status |
| --- | --- | --- | --- | --- |
| [minimum spanning tree](/minimum-spanning-tree/) on $K_{10}$ | edges | spanning trees | $10^{8}$ (Cayley: $n^{n-2}$) | polynomial: [Kruskal](/kruskal/) |
| [assignment](/assignment-problem/), $10 \times 10$ | pairs (worker, job) | perfect matchings | $10! = 3628800$ | polynomial: [Hungarian algorithm](/hungarian-algorithm/), $O(n^3)$ |
| [knapsack](/knapsack-problem/), 10 items | items | sets of weight at most $W$ | at most $2^{10} = 1024$ | weakly NP-hard, $O(nW)$ by [dynamic programming](/knapsack-dynamic-programming/) |
| [traveling salesman](/traveling-salesman-problem/), 10 cities | edges of $K_{10}$ | Hamiltonian cycles | $9!/2 = 181440$ | strongly NP-hard |

The size of $F$ does not decide the difficulty. The spanning trees of $K_{10}$ outnumber the tours of 10 cities by a factor of more than 500, but the spanning tree problem is easy. What matters is structure: spanning trees are the bases of a [matroid](/matroid/), so the [greedy algorithm](/greedy-algorithm/) is exact, and nothing like this is known for tours.

**The size of a search.** With 20 cities there are $19!/2 = 60822550204416000$ tours, about $6.1 \times 10^{16}$. A program that checks $10^9$ tours per second needs about 1.9 years. The [Held-Karp algorithm](/held-karp-algorithm/) needs about $20^2 \cdot 2^{20} \approx 4.2 \times 10^8$ steps, which is less than one second.

**More examples.** [Maximum matching](/maximum-matching/), [shortest paths](/single-source-shortest-paths/) with non-negative weights, [set cover](/set-cover/), [vertex cover](/vertex-cover/), [bin packing](/bin-packing/), [graph partitioning](/graph-partitioning-problem/), [facility location](/facility-location-problem/), [matroid intersection](/matroid-intersection/) and [submodular minimization](/submodular-minimization/) are all combinatorial optimization problems.

**Non-examples.**

- *Linear programming.* The feasible set of a [linear program](/linear-programming-problem/) is a polyhedron, which is infinite when it has two points. It is not a combinatorial problem in the sense above. But when the polyhedron has a vertex and the optimum is finite, an optimal vertex exists, and there are finitely many vertices. The [simplex method](/simplex-method/) uses this finite structure: it searches the vertices, as a combinatorial algorithm does.
- *Continuous optimization.* Minimizing a [convex function](/convex-function/) over $\mathbb{R}^n$ has an infinite feasible set and needs different methods.
- *General integer programming.* $\min \{ c^\top x : Ax \le b,\ x \in \mathbb{Z}^n \}$ is a discrete problem, but its feasible set can be infinite, and the instance can be unbounded: $\min \{ -x : x \in \mathbb{Z},\ x \ge 0 \}$ has no optimum. It is combinatorial only when the feasible set is bounded.
- *A listed set.* If the input lists all of $F$, a linear scan solves the problem in time linear in the input. The term is used for problems where $F$ is given implicitly by a short input.
- *Counting.* "How many optimal tours are there?" is a counting problem, not an optimization problem, even though its objects are the same.

## Related definitions

- [NP-hard](/np-hard/), [weakly NP-hard](/weak-np-hardness/) and [strongly NP-hard](/strong-np-hardness/) classify the hard problems. A weakly NP-hard problem such as knapsack has a [pseudo-polynomial](/pseudo-polynomial-time/) algorithm, and a strongly NP-hard problem such as TSP has none unless P = NP.
- The [approximation ratio](/approximation-ratio/) measures a heuristic against $f^*$. A [PTAS](/ptas/) or an [FPTAS](/fptas/) gets within any factor $1 + \varepsilon$. The class [NPO](/npo-class/) is the frame for approximation classes such as [APX](/apx/).
- An [LP relaxation](/lp-relaxation/) replaces $x \in \{0,1\}^n$ by $0 \le x \le 1$ and gives a bound on $f^*$. The [integrality gap](/integrality-gap/) measures how weak this bound can be. [Total unimodularity](/total-unimodularity/) explains when the relaxation is exact.
- A [local search problem](/local-search-problem/) adds a [neighborhood structure](/neighborhood-structure/) on $F$ and asks for a [local optimum](/local-optimum/), which is the frame for [local search](/local-search/) and the [metaheuristics](/metaheuristic/).
- [Matroids](/matroid/) and [submodular functions](/submodular-function/) are the structures that make many combinatorial problems polynomial.
- [Lagrangian relaxation](/lagrangian-relaxation/), [branch and cut](/branch-and-cut/) and [column generation](/column-generation/) are the general methods for exact solutions of hard instances.

## References
