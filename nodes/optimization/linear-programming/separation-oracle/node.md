---
tag: 4EWS2G
kind: concept
slug: separation-oracle
name: Separation oracle
aliases:
- separation problem
- separation routine
area: optimization/linear-programming
level: advanced
summary: Subroutine that, given a point, either certifies membership or returns a violated inequality; the basis of the ellipsoid method.
prereqs: [polyhedron, convex-set, linear-programming-problem]
see_also: [ellipsoid-method, lp-in-p, cutting-plane-method, subtour-elimination-lp, matching-polytope, semidefinite-programming, column-generation, branch-and-cut]
sources:
  - book: isbn:9783642782428
    title: Martin Grötschel, László Lovász and Alexander Schrijver, Geometric Algorithms and Combinatorial Optimization, second edition, Springer, 1993
    locator: Chapter 2 (the strong and weak separation, membership and optimization problems), Chapter 4 (their equivalence for convex bodies) and Chapter 6 (the equivalence of optimization and separation for rational polyhedra)
  - paper: doi:10.1007/BF02579273
    title: Martin Grötschel, László Lovász and Alexander Schrijver, The ellipsoid method and its consequences in combinatorial optimization, Combinatorica 1(2), 1981
    locator: pages 169 to 197, optimization from separation by the ellipsoid method
  - paper: doi:10.1287/moor.7.1.67
    title: Manfred W. Padberg and M. R. Rao, Odd minimum cut-sets and b-matchings, Mathematics of Operations Research 7(1), 1982
    locator: pages 67 to 80, separation of the odd set constraints by a minimum odd cut
  - paper: doi:10.1287/opre.2.4.393
    title: George B. Dantzig, D. R. Fulkerson and Selmer M. Johnson, Solution of a large-scale traveling-salesman problem, Operations Research 2(4), 1954
    locator: pages 393 to 410, the subtour constraints added only when they are violated
---

A separation oracle for a [convex set](/convex-set/) $K \subseteq \mathbb{R}^n$ is a subroutine that takes a point $y$ and either answers that $y \in K$ or returns a vector $a$ with $a^\top x < a^\top y$ for all $x \in K$, a hyperplane that separates $y$ from $K$. For a [polyhedron](/polyhedron/) $\{x : Ax \le b\}$, this means: find an inequality of the system that $y$ violates, or report that there is none. The [ellipsoid method](/ellipsoid-method/) needs nothing else from the constraints, so a linear program with exponentially many constraints is solvable in polynomial time whenever its separation problem is. Grötschel, Lovász and Schrijver proved the converse too: separation and optimization are polynomially equivalent.

## In plain words

Some problems have far too many rules to list, for example one rule for every subset of the cities of a tour. A separation oracle avoids the list. Hand it a proposed answer, and it either says "this answer breaks no rule" or names one rule that the answer breaks.

Many methods for optimization need only this service. They propose an answer, ask the oracle, and if a rule is broken, they use that rule to cut away a part of the search space that contains the bad answer, then try again. So the question "can we solve this huge problem fast?" becomes "can we find a broken rule fast?", which often has a neat answer with graphs or matrices.

## The idea

**The problem.** Let $K$ be a closed convex set. The *strong separation problem* is: given $y \in \mathbb{Q}^n$, decide whether $y \in K$, and if not, find $a \in \mathbb{Q}^n$ with $a^\top x < a^\top y$ for all $x \in K$. Such an $a$ always exists for $y \notin K$, by the separating hyperplane theorem, and for a polyhedron one of the facet inequalities can serve. For general convex sets, where an exact answer can need irrational numbers, Grötschel, Lovász and Schrijver use *weak* versions, which allow errors of $\varepsilon$ on both sides of the answer.

**From separation to optimization.** The [ellipsoid method](/ellipsoid-method/) keeps an ellipsoid that contains the part of $K$ that is still of interest. It asks the oracle about the center $y$. If $y \notin K$, the answer $a$ shows that $K$ lies in the half-space $a^\top x < a^\top y$. If $y \in K$, the objective of $\max c^\top x$ gives the cut: keep only the half-space $c^\top x \ge c^\top y$. In both cases the next ellipsoid contains the half of the old one on the right side and has a smaller volume by a fixed factor. So the number of calls is polynomial in $n$ and in the encoding size, and it does not depend on the number of constraints of $K$.

**The equivalence.** For a well-described polyhedron $P$, that is, one whose facets have encoding size at most $\varphi$:

- If the separation problem for $P$ is solvable in polynomial time, so is the optimization problem $\max\{c^\top x : x \in P\}$, by the ellipsoid method.
- If optimization over $P$ is solvable in polynomial time, so is separation. The reason is polarity: $y$ is separated from $P$ exactly when some inequality $a^\top x \le \beta$ valid for $P$ has $a^\top y > \beta$, and the valid inequalities form a polyhedron (the polar) over which the ellipsoid method can optimize, with the optimization oracle for $P$ as its separation oracle.

This is the theorem of Grötschel, Lovász and Schrijver (1981). Its practical form is: an LP is easy when its separation problem is easy, even when the explicit LP has exponential size.

**Cost of the oracle.** For an explicit system $Ax \le b$ with $m$ rows, separation is a scan of the rows in $O(mn)$ time. The interesting cases are those where $m$ is exponential and the oracle is a combinatorial algorithm.

## Examples

**The cross-polytope.** The $\ell_1$ ball $K = \{x : \sum_i |x_i| \le 1\}$ is the polyhedron of the $2^n$ inequalities $s^\top x \le 1$ for $s \in \{-1, 1\}^n$. The oracle computes $\sum_i |y_i|$. If it is at most $1$, then $y \in K$. Otherwise it returns $s = \operatorname{sign}(y)$: for every $x \in K$, $s^\top x \le \sum_i |x_i| \le 1 < \sum_i |y_i| = s^\top y$. For $y = (0.5, -0.75, 0.25)$ the sum is $1.5 > 1$, and the oracle returns $s = (1, -1, 1)$, the inequality $x_1 - x_2 + x_3 \le 1$. This takes $O(n)$ time for $2^n$ constraints.

**Subtour elimination.** The [subtour LP](/subtour-elimination-lp/) for the traveling salesman problem on a graph with vertex set $V$ has $x(\delta(v)) = 2$ for each vertex, $0 \le x \le 1$, and $x(\delta(S)) \ge 2$ for every nonempty $S \subsetneq V$. For a given $y \ge 0$, the least value of $y(\delta(S))$ over all $S$ is the [global minimum cut](/global-min-cut-problem/) of the graph with capacities $y$. If it is below $2$, its side $S$ is a violated constraint; if not, $y$ satisfies all of them. For six cities with $y_e = 1$ on the two triangles $\{1, 2, 3\}$ and $\{4, 5, 6\}$ and $0$ elsewhere, every degree is $2$, but the cut $S = \{1, 2, 3\}$ has $y(\delta(S)) = 0$, so the oracle returns $x(\delta(\{1,2,3\})) \ge 2$. Dantzig, Fulkerson and Johnson (1954) already added these constraints one at a time, only when a solution violated them.

**Odd set constraints.** The [perfect matching polytope](/matching-polytope/) needs $x(\delta(S)) \ge 1$ for every odd set $S$. Padberg and Rao (1982) showed that a minimum cut with an odd side can be found among the $n - 1$ cuts of a [Gomory-Hu tree](/gomory-hu-tree/), so separation takes $n - 1$ maximum flow computations, and optimization over the matching polytope is polynomial by the equivalence above.

**The positive semidefinite cone.** For a symmetric matrix $Y$, compute the least eigenvalue $\lambda$ and an eigenvector $v$. If $\lambda \ge 0$, then $Y$ is positive semidefinite. Otherwise $v^\top Y v = \lambda \|v\|^2 < 0 \le v^\top X v$ for every positive semidefinite $X$, so the linear inequality $\langle vv^\top, X \rangle \ge 0$ separates $Y$. This oracle is behind the polynomial-time results for [semidefinite programming](/semidefinite-programming/) by the ellipsoid method.

## Where it is used

- **Polynomial-time results.** Through the ellipsoid method, separation gives polynomial algorithms for matching, matroid intersection, submodular function minimization and the stable sets of perfect graphs, and it extends the theorem that [linear programming is in P](/lp-in-p/) to programs that are given only by a separation oracle.
- **Cutting planes in practice.** [Cutting-plane](/cutting-plane-method/) and [branch-and-cut](/branch-and-cut/) codes solve an LP with a few constraints, call separation routines on the solution, add the violated constraints, and solve again. TSP codes compute the [Held-Karp bound](/held-karp-bound/) in this way.
- **Column generation.** The pricing problem of [column generation](/column-generation/) is the separation problem of the dual program: a column with negative reduced cost is a dual constraint that the current dual solution violates.
- **Convex optimization.** First-order and cutting-plane methods for nonsmooth convex problems use subgradients as separating hyperplanes for the level sets of the objective.

## References
