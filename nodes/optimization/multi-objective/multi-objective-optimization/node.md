---
tag: VSJ33M
kind: problem
slug: multi-objective-optimization
name: Multi-objective optimization
aliases:
- multiobjective optimization
- MOO
- multicriteria optimization
- vector optimization
- multiple criteria optimization
area: optimization/multi-objective
level: intro
summary: Minimize several conflicting objectives at once. The answer is the set of Pareto optimal solutions, the solutions that no other solution improves in one objective without a loss in another.
prereqs: [constrained-optimization]
see_also: [pareto-optimality, pareto-front, scalarization, preference-articulation, multi-objective-linear-programming, pareto-front-computation, nsga-ii, approximate-pareto-set]
sources:
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapter 1 (the problem and the orders on the objective space), Chapter 2 (efficiency and nondominance) and Chapter 8 (intractability of multiobjective combinatorial problems)
  - book: isbn:9780792382782
    title: Kaisa Miettinen, Nonlinear Multiobjective Optimization, Kluwer, 1999
    locator: Part I, Chapters 1 and 2 (problem statement, Pareto optimality, the ranges of the Pareto set)
  - book: isbn:9780471873396
    title: Kalyanmoy Deb, Multi-Objective Optimization Using Evolutionary Algorithms, Wiley, 2001
    locator: Chapter 2 (multi-objective optimization, dominance and the non-dominated set)
  - paper: doi:10.1109/SFCS.2000.892068
    title: Christos H. Papadimitriou and Mihalis Yannakakis, On the approximability of trade-offs and optimal access of Web sources, FOCS 2000
    locator: pages 86 to 92, the existence theorem for epsilon-approximate Pareto sets of polynomial size
  - paper: doi:10.1007/BF00932634
    title: Wolfram Stadler, A survey of multicriteria optimization or the vector maximum problem, part I, 1776 to 1960, Journal of Optimization Theory and Applications 29(1), 1979
    locator: pages 1 to 52 (history, Edgeworth and Pareto)
---

Multi-objective optimization asks for the best solutions of a problem that has two or more objective functions, when no single solution makes all of them best at the same time. The answer is not one optimal value but the set of [Pareto optimal](/pareto-optimality/) solutions: the solutions that no other solution improves in one objective without a loss in another. Their images in the objective space form the [Pareto front](/pareto-front/). A decision maker then picks one point of the front, before, during or after the search (see [preference articulation](/preference-articulation/)).

## In plain words

You want to buy a laptop that is cheap and also light. The cheapest laptop is heavy, and the lightest laptop is expensive. No laptop wins on both counts, so there is no single best answer.

You can still throw some laptops away. If one laptop is cheaper and lighter than another, nobody should buy the second one. After you remove every laptop that some other laptop beats on both counts, the rest is a list of fair trade-offs. To move along this list, you must pay more to carry less.

Multi-objective optimization finds this list of trade-offs. It is the job of a person, or of a rule that the person gives, to pick one item from it.

## Definition

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$. The feasible set is $X$, and its elements are called solutions. The objective map is $f = (f_1, \ldots, f_p) : X \to \mathbb{R}^p$. For a solution $x$, the vector $y = f(x)$ is the *image* of $x$, and $Y = f(X) \subseteq \mathbb{R}^p$ is the image of the feasible set, also called the outcome set. When $X \subseteq \mathbb{R}^n$, $n$ is the number of variables. The pages of this sub-area use the same convention.

**Orders on $\mathbb{R}^p$.** For $y, y' \in \mathbb{R}^p$ we write

- $y \leqq y'$ when $y_i \le y'_i$ for all $i = 1, \ldots, p$,
- $y \prec y'$, read "$y$ [dominates](/pareto-dominance/) $y'$", when $y \leqq y'$ and $y \ne y'$,
- $y < y'$ when $y_i < y'_i$ for all $i$.

None of these is a total order when $p \ge 2$: the vectors $(1, 2)$ and $(2, 1)$ are not comparable.

**The problem.** The input is the pair $(X, f)$. The problem

$$\min_{x \in X} \; \big(f_1(x), \ldots, f_p(x)\big)$$

asks for the *efficient set* (or Pareto set)

$$X_E = \{\, x \in X : \text{there is no } x' \in X \text{ with } f(x') \prec f(x) \,\}$$

and its image $Y_N = f(X_E)$, the *nondominated set* or Pareto front. A point $y \in Y$ is in $Y_N$ exactly when no other point of $Y$ dominates it. The output can take three forms, which differ a lot in size:

1. the full efficient set $X_E$ (all solutions, also those with equal images),
2. a *minimal complete set*: one solution $x$ for each point $y \in Y_N$, so the output size is $|Y_N|$,
3. one efficient solution, or a few that a decision maker selects.

Most exact methods for combinatorial problems compute a minimal complete set. Many authors call $Y_N$ the solution of the problem, because two solutions with the same image are equal for the decision maker.

## Variants

- **By the feasible set.** [Multi-objective linear programming](/multi-objective-linear-programming/) has a polyhedron $X$ and linear $f$. Multi-objective integer and combinatorial problems have a finite $X$, for example the [multi-objective shortest path](/multi-objective-shortest-path/), the [multi-objective minimum spanning tree](/multi-objective-minimum-spanning-tree/) and the [multi-objective knapsack problem](/multi-objective-knapsack/). Convex problems have a convex $X$ and convex $f_i$. In the [Pareto front computation](/pareto-front-computation/) problem, $X$ is a finite list of vectors and $f$ is the identity.
- **By the notion of optimality.** [Weakly Pareto optimal](/pareto-optimality/) solutions only need that no solution is strictly better in every objective. Properly Pareto optimal solutions also need bounded trade-offs. Lexicographic optimality ([lexicographic optimization](/lexicographic-optimization/)) ranks the objectives by priority. Max-ordering minimizes $\max_i f_i(x)$.
- **By what the decision maker gives.** With no preference information, the task is to compute or to approximate $Y_N$. With a [utility function](/utility-function/), the task is one solution that minimizes the utility. With a reference point or goals, the task is the efficient solution closest to them ([reference point method](/reference-point-method/), [goal programming](/goal-programming/)). With interaction, the method and the decision maker alternate.
- **Exact and approximate.** An [approximate Pareto set](/approximate-pareto-set/) covers $Y_N$ up to a factor $1 + \varepsilon$ in each objective. Evolutionary methods such as [NSGA-II](/nsga-ii/) return a finite set of mutually nondominated points with no guarantee of distance to $Y_N$.

## Examples

**A finite problem.** Seven solutions have these images, with both objectives to be minimized:

| solution | a | b | c | d | e | f | g |
|---|---|---|---|---|---|---|---|
| $y_1$ | 2 | 3 | 4 | 5 | 7 | 8 | 9 |
| $y_2$ | 9 | 6 | 7 | 4 | 3 | 5 | 1 |

The point $c = (4, 7)$ is dominated by $b = (3, 6)$, and $f = (8, 5)$ is dominated by $d = (5, 4)$ and by $e = (7, 3)$. The other five points are nondominated, so $Y_N = \{a, b, d, e, g\}$. Each objective alone has a unique best solution: $a$ for $f_1$ and $g$ for $f_2$. The [ideal point](/ideal-point/) is $(2, 1)$ and the [nadir point](/nadir-point/) is $(9, 9)$. This instance comes back on the pages of the methods. There, the [weighted sum method](/weighted-sum-method/) finds $a, b, d, g$ but never $e$, while the [weighted Tchebycheff method](/weighted-tchebycheff-method/) and the [epsilon-constraint method](/epsilon-constraint-method/) find all five.

**A continuous problem.** Minimize $f_1(x) = x^2$ and $f_2(x) = (x - 2)^2$ over $x \in \mathbb{R}$ (Schaffer's first test problem). For $x < 0$, the point $0$ is better in both objectives, and for $x > 2$, the point $2$ is better in both. For $0 \le x < x' \le 2$, $f_1$ increases and $f_2$ decreases, so the two points do not dominate each other. So $X_E = [0, 2]$, and the front is the curve $y_2 = (2 - \sqrt{y_1})^2$ for $y_1 \in [0, 4]$. The ideal point is $(0, 0)$, which no solution reaches.

**An exponential front.** Take a path of $k + 1$ vertices, and join each pair of consecutive vertices by two parallel edges with costs $(2^i, 0)$ and $(0, 2^i)$ for $i = 0, \ldots, k - 1$. Each of the $2^k$ paths from the first to the last vertex has the cost $(a, 2^k - 1 - a)$, where $a$ is the sum of the chosen first costs. The values of $a$ are the integers $0, \ldots, 2^k - 1$, so all $2^k$ paths are Pareto optimal and their images are distinct. The input has $2k$ edges. This construction (Hansen, 1980) is on the page of the [multi-objective shortest path](/multi-objective-shortest-path/).

## Known algorithms

- **One efficient solution by a single-objective method.** [Scalarization](/scalarization/) turns the problem into one objective: the [weighted sum method](/weighted-sum-method/), the [epsilon-constraint method](/epsilon-constraint-method/), the [weighted Tchebycheff method](/weighted-tchebycheff-method/), the [achievement scalarizing function](/achievement-scalarizing-function/), [goal programming](/goal-programming/) and [lexicographic optimization](/lexicographic-optimization/). Each page states which kind of efficient solution its optimum is.
- **The full front of a finite set of vectors.** [Kung's algorithm](/kung-algorithm/) of Kung, Luccio and Preparata finds the nondominated vectors of $N$ given vectors in $O(N \log N)$ comparisons for $p = 2$ and $p = 3$, and in $O(N \log^{p-2} N)$ for $p \ge 4$.
- **Linear problems.** [Benson's outer approximation algorithm](/benson-algorithm/) computes all extreme nondominated points of a [multi-objective linear program](/multi-objective-linear-programming/). Multi-objective simplex methods move between efficient bases.
- **Even spread on smooth problems.** [Normal boundary intersection](/normal-boundary-intersection/) places points on the front along a regular grid.
- **Combinatorial problems.** Label-setting and label-correcting methods for the [multi-objective shortest path](/multi-objective-shortest-path/), dynamic programming for the [multi-objective knapsack problem](/multi-objective-knapsack/), and the two-phase method (first the supported points by weighted sums, then the others by enumeration in the gaps).
- **Heuristics.** Evolutionary methods such as [NSGA-II](/nsga-ii/), [SPEA2](/spea2/) and [MOEA/D](/moea-d/), [Pareto local search](/pareto-local-search/) and [multi-objective simulated annealing](/multi-objective-simulated-annealing/). They have no guarantee in general, and their output is judged with quality indicators such as the [hypervolume indicator](/hypervolume-indicator/).

## Bounds

- **Output size.** For combinatorial problems, $|Y_N|$ can be exponential in the input size. The example above gives $2^k$ nondominated points for the shortest path problem with $2k$ edges. Hamacher and Ruhe (1994) show the same for spanning trees. Ehrgott (2005, Chapter 8) calls a problem *intractable* when $|Y_N|$ can be exponential in the size of the instance. For such a problem, no algorithm lists $Y_N$ in time polynomial in the input size alone, and the right measure is the time per output point or the time as a function of the input and the output sizes.
- **Hardness of one point.** The decision version "is there a solution with $f(x) \leqq b$?" is NP-complete for the bi-objective shortest path problem, although each objective alone is solved by [Dijkstra's algorithm](/dijkstra/). It is the [constrained shortest path](/constrained-shortest-path/) problem (Garey and Johnson, problem ND30).
- **Approximation.** Papadimitriou and Yannakakis (2000) show that for a fixed $p$ and each $\varepsilon > 0$ an $\varepsilon$-approximate Pareto set exists whose size is polynomial in the input size and in $1/\varepsilon$, when the objective values are positive and lie in $[2^{-m}, 2^m]$ for $m$ polynomial in the input size. A set $P$ is $\varepsilon$-approximate when each $y \in Y$ has a $y' \in f(P)$ with $y'_i \le (1 + \varepsilon) y_i$ for all $i$. The proof is a grid: cut each of the first $p - 1$ axes into the $K = O(m / \varepsilon)$ intervals $[(1+\varepsilon)^k, (1+\varepsilon)^{k+1})$, and keep in each box of the grid one point with the least value of $f_p$. The kept set has at most $K^{p-1}$ points and covers $Y$. They also show that such a set can be computed in polynomial time exactly when a "gap" version of the problem is solvable in polynomial time. See [approximate Pareto set](/approximate-pareto-set/).
- **Finite vector sets.** For $N$ given vectors, Kung, Luccio and Preparata (1975) prove a lower bound of $\Omega(N \log N)$ comparisons for $p \ge 2$, which matches their algorithm for $p = 2$ and $p = 3$.

## Reductions

- **To single-objective problems.** Each scalarization reduces the search for one efficient solution to one single-objective problem of the same type, sometimes with extra constraints. The [epsilon-constraint method](/epsilon-constraint-method/) adds $p - 1$ constraints. The [weighted sum method](/weighted-sum-method/) keeps the constraints, so a polynomial single-objective algorithm stays usable, but it finds only the supported points.
- **The full front with integer objectives.** For $p = 2$ and integer objective values, the epsilon-constraint loop finds all of $Y_N$ with $|Y_N| + 1$ lexicographic single-objective solves. So the work is output-sensitive when the single-objective problem with one extra constraint is easy.
- **From hard single-objective problems.** The knapsack and constrained shortest path problems reduce to the decision version of a bi-objective problem. This is why one point of the front can be NP-hard to find even when each objective alone is easy.

## Applications

- **Engineering design.** Weight against stiffness, cost against reliability. Marler and Arora (2004) survey the methods that engineers use.
- **Finance.** Markowitz's portfolio selection (1952) minimizes the risk and maximizes the expected return. Its front is the efficient frontier.
- **Routing and transport.** Travel time against cost or against the number of transfers. See the [multi-objective shortest path](/multi-objective-shortest-path/).
- **Scheduling and logistics.** Makespan against total tardiness, cost against service level.
- **Machine learning.** Accuracy against model size or against a fairness measure, and the choice of hyperparameters with several criteria.

The idea of an efficient trade-off goes back to Edgeworth (1881) and Pareto (1906) in economics. Kuhn and Tucker (1951) and Koopmans (1951) brought it into optimization. Stadler (1979) traces this history.

## References
