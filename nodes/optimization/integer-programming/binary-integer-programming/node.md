---
tag: MZNBSH
kind: problem
slug: binary-integer-programming
name: Binary integer programming
aliases:
- 0-1 integer programming
- zero-one programming
- 0-1 linear programming
- BIP
area: optimization/integer-programming
level: core
summary: Integer programming where every variable is restricted to 0 or 1, so that each variable models a yes or no decision.
prereqs: [mixed-integer-programming, linear-programming-problem]
see_also: [knapsack-problem, set-cover, vertex-cover, cover-inequality, lift-and-project, pseudo-boolean-sat, karp-21-np-complete, lp-relaxation]
sources:
  - paper: "Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (editors), Complexity of Computer Computations, Plenum, 1972, pages 85 to 103"
    locator: the list of 21 problems (0-1 integer programming, reduced from satisfiability)
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming, Wiley, 1998
    locator: Chapter 1 (0-1 models such as knapsack, assignment and set covering) and Chapter 9 (valid inequalities for the 0-1 knapsack set)
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 2 (formulations with binary variables) and Chapter 5 (lift-and-project for 0-1 programs)
  - paper: "Egon Balas, An additive algorithm for solving linear programs with zero-one variables, Operations Research 13(4) (1965), 517 to 546"
    locator: the implicit enumeration method
---

A binary integer program (BIP), or 0-1 integer program, optimizes a linear function subject to linear inequalities, with each variable restricted to the two values 0 and 1. It is the special case of [mixed-integer programming](/mixed-integer-programming/) where each variable is a yes or no decision. Its feasibility version is one of [Karp's 21 NP-complete problems](/karp-21-np-complete/). The problems that it models directly include [knapsack](/knapsack-problem/), [set cover](/set-cover/), [vertex cover](/vertex-cover/) and assignment.

## In plain words

Many decisions have only two answers. You pick an item for the bag or you leave it. You build a warehouse at a site or you do not. A binary program gives one unknown to each decision: the value 1 means yes and 0 means no. The cost and the rules are sums of the unknowns with fixed weights, such as "the total weight of the picked items is at most the capacity".

There are only finitely many choices, two for each decision, so you could try them all. But with a hundred decisions the number of choices has thirty-one digits. Solvers instead use fractional versions of the problem to get bounds, and use these bounds to skip most of the choices.

## Definition

**Input.** A matrix $A \in \mathbb{Q}^{m \times n}$ and vectors $b \in \mathbb{Q}^m$, $c \in \mathbb{Q}^n$. Here $n$ is the number of variables and $m$ the number of constraints.

**Output.** A vector $x^* \in \{0,1\}^n$ with $Ax^* \le b$ and $c^T x^* = f^* = \max\{c^T x : Ax \le b,\ x \in \{0,1\}^n\}$, or the answer "infeasible" when no such vector exists.

The feasible set is finite, so the problem is never unbounded. An equivalent form is $\max\{c^T x : Ax \le b,\ 0 \le x \le 1,\ x \in \mathbb{Z}^n\}$. This form shows the [LP relaxation](/lp-relaxation/): replace $x \in \{0,1\}^n$ by $0 \le x \le 1$.

## Variants

- **Decision version.** Given $A$ and $b$, is there $x \in \{0,1\}^n$ with $Ax \le b$? This is 0-1 integer programming in Karp's list.
- **Mixed binary program.** Some variables are continuous. This is the most common form in practice: the binary variables are the decisions, and the continuous variables are the amounts that depend on them.
- **Set covering, packing and partitioning.** $A$ is a 0-1 matrix and $b = \mathbf{1}$, with $Ax \ge \mathbf{1}$, $Ax \le \mathbf{1}$ or $Ax = \mathbf{1}$. [Set cover](/set-cover/) and crew scheduling have this form.
- **Knapsack.** One constraint $\sum_j w_j x_j \le C$. See the [knapsack problem](/knapsack-problem/).
- **Unconstrained quadratic 0-1 programming.** Maximize $x^T Q x$ over $\{0,1\}^n$. It is not linear, but the products can be made linear as shown in the Reductions section. [Maximum cut](/maximum-cut/) is a special case.

## Examples

**A knapsack.** Items with profits $(10, 13, 7, 5)$ and weights $(5, 6, 4, 3)$, and capacity 10. The 16 subsets give the optimum $x^* = (0, 1, 1, 0)$ with profit $f^* = 20$ and weight 10. The LP relaxation takes the items in order of profit per weight, $13/6$, $2$, $7/4$, $5/3$. It takes item 2 whole and $4/5$ of item 1, for the value $13 + 8 = 21$. The [cover inequality](/cover-inequality/) $x_1 + x_2 \le 1$, valid because $5 + 6 > 10$, cuts off this fractional point.

**Vertex cover of a triangle.** Minimize $x_1 + x_2 + x_3$ subject to $x_i + x_j \ge 1$ for each edge $\{i, j\}$ of the triangle, $x \in \{0,1\}^3$. Each cover needs two vertices, so $f^* = 2$. The relaxation has the solution $x = (1/2, 1/2, 1/2)$ with value $3/2$. On the complete graph with $k$ vertices, the values are $k - 1$ and $k/2$; see [integrality gap](/integrality-gap/).

**A clause.** The clause $x_1 \lor \lnot x_2 \lor x_3$ of a formula in conjunctive normal form becomes $x_1 + (1 - x_2) + x_3 \ge 1$. A formula is satisfiable if and only if the system of these constraints has a 0-1 solution.

## Known algorithms

- **Enumeration.** Check all $2^n$ vectors, each in $O(mn)$ time, so $O(2^n mn)$ time in all. This is the reference for tests of all other methods.
- **Implicit enumeration.** Balas' additive algorithm (1965) fixes variables one at a time and uses simple tests to discard a partial assignment that cannot become feasible or better. It needs only additions.
- **[Branch and cut](/branch-and-cut/).** Branch on a variable with a fractional LP value, so one child fixes it to 0 and the other to 1. Add [cover inequalities](/cover-inequality/), [zero-half cuts](/zero-half-cut/), [lift-and-project cuts](/lift-and-project/) and Gomory cuts. All general solvers use this method.
- **Dynamic programming.** One knapsack constraint with integer weights is solved in $O(nC)$ time by [dynamic programming](/knapsack-dynamic-programming/). For a fixed number of constraints with small integer entries, see [Papadimitriou's theorem](/papadimitriou-pseudopolynomial-theorem/).
- **Special structure.** If $A$ is [totally unimodular](/total-unimodularity/) and $b$ is integral, the LP relaxation has an integral optimal vertex. The assignment problem and [bipartite matching](/bipartite-matching/) are solved this way, or with the [Hungarian algorithm](/hungarian-algorithm/).
- **Hierarchies.** Lift-and-project, and the hierarchies of Sherali and Adams and of Lovász and Schrijver, reach the convex hull of the 0-1 points after at most $n$ rounds.

## Bounds

- **NP-complete.** The decision version is in NP, because a solution is a certificate of $n$ bits that is checked in $O(mn)$ arithmetic steps. It is NP-hard by the reduction from satisfiability above (Karp 1972). The optimization version is therefore NP-hard.
- **Exponential lower bound under a hypothesis.** The reduction from 3-SAT keeps the number of variables. So an algorithm in time $2^{o(n)}$ for 0-1 programs would give one for [3-SAT](/3-sat/), which the exponential time hypothesis rules out.
- **Pseudo-polynomial cases.** One constraint with integer weights takes $O(nC)$ time, and a fixed number of constraints with bounded integer entries also has a pseudo-polynomial algorithm. Without a bound on the number of constraints, the problem is [strongly NP-hard](/strong-np-hardness/), since set cover and vertex cover have only 0-1 data.
- **Approximation.** The general problem has no approximation guarantee: deciding feasibility is already NP-hard. Special cases have good ones, for example 2 for vertex cover by [LP rounding](/lp-rounding-vertex-cover/).

## Reductions

- **From general bounded integer programs.** A variable $0 \le y \le u$ with $y \in \mathbb{Z}$ is $y = \sum_{k=0}^{K} 2^k z_k$ with $z_k \in \{0,1\}$ and $K = \lfloor \log_2 u \rfloor$, plus the constraint $y \le u$. With $u = 10$ this needs 4 binary variables, since $2^3 \le 10 < 2^4$.
- **Linear form of a product.** For $x_i, x_j \in \{0,1\}$, the product $y = x_i x_j$ is the unique 0-1 solution of $y \le x_i$, $y \le x_j$, $y \ge x_i + x_j - 1$, $y \ge 0$. This turns a quadratic 0-1 program into a linear one with one new variable per product.
- **From satisfiability.** Each clause becomes one constraint, as in the example. The size grows only linearly.
- **To satisfiability.** Each linear constraint over 0-1 variables is a [pseudo-Boolean constraint](/pseudo-boolean-sat/). SAT solvers with pseudo-Boolean reasoning solve some 0-1 programs faster than LP-based solvers.

## Applications

- **Selection and budgeting.** Capital budgeting picks a set of projects under a budget. This is a knapsack with several constraints.
- **Covering and location.** Choose sites for stations so that each customer is within reach of one, as a set cover.
- **Crew scheduling.** Choose a set of duties that covers each flight once, as a set partitioning problem.
- **Logic and verification.** Constraints from program analysis and from configuration problems are written as 0-1 programs.

## References
