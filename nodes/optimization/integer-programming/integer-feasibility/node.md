---
tag: WEAVGP
kind: problem
slug: integer-feasibility
name: Integer feasibility problem
aliases:
- integer feasibility
- integer programming feasibility
- lattice point problem for polyhedra
area: optimization/integer-programming
level: intro
summary: Decide whether a system of linear inequalities has a solution in integers, that is, whether a polyhedron contains an integer point.
prereqs: [polyhedron, linear-feasibility, np-complete]
see_also: [mixed-integer-programming, binary-integer-programming, lenstra-algorithm, hermite-normal-form, linear-diophantine-equation, chvatal-gomory-cut, integer-hull]
sources:
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 4 (Hermite normal form and systems of linear Diophantine equations, with the integer form of Farkas' lemma), Chapter 17 (size of solutions) and Chapter 18 (NP-completeness and Lenstra's algorithm)
  - paper: doi:10.1145/322276.322287
    title: Christos H. Papadimitriou, On the complexity of integer programming, Journal of the ACM 28(4), 1981
    locator: the bound on the size of a solution of Ax = b, x >= 0 integer, and the pseudo-polynomial algorithm for a fixed number of constraints
  - paper: doi:10.1287/moor.8.4.538
    title: H. W. Lenstra Jr., Integer programming with a fixed number of variables, Mathematics of Operations Research 8(4), 1983
    locator: the main theorem
  - paper: "Robert G. Jeroslow, Trivial integer programs unsolvable by branch-and-bound, Mathematical Programming 6 (1974), 105 to 109"
    locator: the parity example
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 1 (the integer Farkas lemma) and Chapter 9 (Lenstra's algorithm and the flatness theorem)
---

The integer feasibility problem asks whether a [polyhedron](/polyhedron/) $\{x : Ax \le b\}$ contains a point with integer coordinates. It is the decision version of [integer programming](/mixed-integer-programming/), and it is [NP-complete](/np-complete/). Its continuous version, [linear feasibility](/linear-feasibility/), is in P, and the gap between the two is the reason integer programming is hard. Special cases are easy: a system of linear equations with no sign constraints is solved with the [Hermite normal form](/hermite-normal-form/), and a fixed number of variables is handled by [Lenstra's algorithm](/lenstra-algorithm/).

## In plain words

You have a set of linear rules, such as "twice the first number plus three times the second is at most ten". The question is whether whole numbers exist that obey all the rules at the same time.

If fractions were allowed, a fast method would answer. With whole numbers, the region that the rules allow can be large and still miss every whole-number point, for example a long thin strip that passes between them. No fast method is known for all cases. The question is still very useful: many puzzles and planning tasks reduce to it, and solvers answer it for large practical systems.

## Definition

**Input.** A matrix $A \in \mathbb{Q}^{m \times n}$ and a vector $b \in \mathbb{Q}^m$. Here $n$ is the number of variables and $m$ the number of constraints.

**Question.** Is there $x \in \mathbb{Z}^n$ with $Ax \le b$?

The search version asks for such an $x$. Sign constraints $x \ge 0$ and bounds $x \le u$ are rows of $A$. An equation $a^T x = \beta$ is the pair of rows $a^T x \le \beta$ and $-a^T x \le -\beta$.

## Variants

- **Equations without sign constraints.** Is there $x \in \mathbb{Z}^n$ with $Ax = b$? This is in P. Bring $A$ to [Hermite normal form](/hermite-normal-form/) by unimodular column operations, then solve a triangular system. For one equation $a_1 x_1 + \cdots + a_n x_n = \beta$ with integer data, a solution exists if and only if $\gcd(a_1, \ldots, a_n)$ divides $\beta$; see [linear Diophantine equations](/linear-diophantine-equation/).
- **Equations with sign constraints.** Is there $x \in \mathbb{Z}^n_{\ge 0}$ with $Ax = b$? This is NP-complete even for one equation, because it contains the [subset sum problem](/subset-sum-problem/) when bounds $x \le 1$ are added, and the unbounded knapsack problem without them.
- **0-1 feasibility.** $x \in \{0,1\}^n$. See [binary integer programming](/binary-integer-programming/).
- **Fixed dimension.** For each fixed $n$ the problem is in P (Lenstra 1983). See [integer programming in fixed dimension](/integer-programming-fixed-dimension/).
- **Mixed version.** Only some variables must be integers. The complexity is the same as for the pure version.

## Examples

**Parity.** The equation $2x_1 - 2x_2 = 1$ has the real solution $(1/2, 0)$ but no integer solution, because the left side is even for each integer point. In the language of the integer Farkas lemma: the multiplier $y = 1/2$ makes $yA = (1, -1)$ integral and $yb = 1/2$ not integral.

**One equation with three variables.** Take $6x + 10y + 15z = \beta$. The gcd of $6, 10, 15$ is 1, so there is an integer solution for each integer $\beta$; for $\beta = 1$ one is $(1, 1, -1)$. With $x, y, z \ge 0$ the answer changes: $\beta = 29$ has no nonnegative solution, and each $\beta \ge 30$ has one. So 29 is the Frobenius number of $\{6, 10, 15\}$.

**A trap for branch and bound.** Let $k$ be odd and take $2(x_1 + \cdots + x_k) = k$ with $x \in \{0,1\}^k$. There is no solution, since the left side is even. The LP relaxation has many fractional solutions, and Jeroslow (1974) showed that branch and bound on single variables needs a number of nodes that is exponential in $k$. One [Chvátal-Gomory cut](/chvatal-gomory-cut/) decides it: half of $2\sum x_j \le k$ gives $\sum x_j \le \lfloor k/2 \rfloor = (k-1)/2$, and half of $-2\sum x_j \le -k$ gives $\sum x_j \ge (k+1)/2$. The two cuts contradict each other.

## Known algorithms

- **Linear algebra over the integers.** For $Ax = b$ with $x$ free, the [Hermite normal form](/hermite-normal-form/) solves the problem in polynomial time. The [extended Euclidean algorithm](/extended-euclidean-algorithm/) is the case of one equation.
- **[Lenstra's algorithm](/lenstra-algorithm/).** It uses lattice basis reduction ([LLL](/lll-algorithm/)) and the flatness theorem: a convex body with no integer point is thin in some integer direction. It then branches on the few hyperplanes that cross the body. The time is polynomial for each fixed $n$. [Kannan's algorithm](/kannan-algorithm/) improves the dependence on $n$ to $n^{O(n)}$.
- **[Branch and cut](/branch-and-cut/).** The general method of solvers. It decides feasibility by branching and by [cutting planes](/cutting-plane-method-integer-programming/), and it has no polynomial bound.
- **Dynamic programming.** For $Ax = b$, $x \ge 0$ with a fixed number $m$ of rows and small integer entries, [Papadimitriou's algorithm](/papadimitriou-pseudopolynomial-theorem/) is pseudo-polynomial.
- **Linear programming as a filter.** If the [LP relaxation](/lp-relaxation/) is infeasible, a [Farkas](/farkas-lemma/) certificate proves that no integer point exists. If $A$ is [totally unimodular](/total-unimodularity/) and $b$ is integral, LP feasibility already implies integer feasibility.

## Bounds

- **In NP.** If $Ax = b$, $x \ge 0$ with integer data has an integer solution, then it has one with each entry at most $n(ma)^{2m+1}$, where $a$ is the largest absolute value of an entry of $A$ and $b$ (Papadimitriou 1981). The same holds in general form with a bound polynomial in the input size (Schrijver 1986, Chapter 17). So a solution of polynomial size is a certificate.
- **NP-hard.** 0-1 feasibility is NP-complete (Karp 1972), by a reduction from satisfiability with one constraint per clause.
- **Polynomial in fixed dimension.** Lenstra (1983) gives a polynomial algorithm for each fixed $n$. Without a fixed $n$, no algorithm in time $2^{o(n)}$ is expected, by the same reduction from 3-SAT.
- **Lower bounds for proof systems.** Branch and bound on variables needs exponentially many nodes on the parity example above, while cutting planes need one round. Other families are hard for cutting planes too, so neither method is polynomial in general.

## Reductions

- **Optimization to feasibility.** To solve $\max\{c^T x : Ax \le b, x \in \mathbb{Z}^n\}$, add the constraint $c^T x \ge t$ and search on $t$. The optimal value has size polynomial in the input size, so binary search needs a polynomial number of calls.
- **Satisfiability to feasibility.** A clause $\ell_1 \lor \ell_2 \lor \ell_3$ becomes $\ell_1 + \ell_2 + \ell_3 \ge 1$ with $\lnot x$ written as $1 - x$, and $0 \le x \le 1$.
- **Feasibility to satisfiability.** Over bounded variables, each constraint is a [pseudo-Boolean constraint](/pseudo-boolean-sat/), and the whole system is a formula of [linear integer arithmetic](/linear-integer-arithmetic-satisfiability/).

## Applications

- **Phase one of integer programming.** Solvers must first find a feasible point. Primal heuristics such as the [feasibility pump](/feasibility-pump/) target this question.
- **Program analysis.** Checks of array bounds and of loop dependences in compilers ask if a system of integer inequalities has a solution.
- **Number theory and coin problems.** The Frobenius problem and questions on representations of numbers are integer feasibility questions.

## References
