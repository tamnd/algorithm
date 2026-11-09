---
tag: 57FP0C
kind: problem
slug: mixed-integer-programming
name: Mixed-integer programming
aliases:
- MIP
- MILP
- mixed-integer linear programming
- integer linear programming
area: optimization/integer-programming
level: core
summary: Optimize a linear objective over the points that satisfy linear inequalities, when some of the variables must take integer values and the rest are continuous.
prereqs: [linear-programming-problem, polyhedron, np-hard]
see_also: [binary-integer-programming, integer-feasibility, lp-relaxation, integer-hull, branch-and-cut, cutting-plane-method-integer-programming, lenstra-algorithm, total-unimodularity]
sources:
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 1 (the problem and its relaxation), Chapter 2 (formulations) and Chapter 4 (Meyer's theorem on the mixed-integer hull)
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 16 (introduction to integer linear programming and the integer hull), Chapter 17 (estimates on the size of solutions) and Chapter 18 (the complexity of integer linear programming)
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming, Wiley, 1998
    locator: Chapter 1 (formulations) and Chapter 2 (optimality, relaxation and bounds)
  - paper: "Robert R. Meyer, On the existence of optimal solutions to integer and mixed-integer programming problems, Mathematical Programming 7 (1974), 223 to 235"
    locator: the main theorem (the mixed-integer hull of a rational polyhedron is a rational polyhedron)
  - paper: "Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (editors), Complexity of Computer Computations, Plenum, 1972, pages 85 to 103"
    locator: the list of 21 problems (0-1 integer programming is NP-complete)
  - paper: doi:10.1287/moor.8.4.538
    title: H. W. Lenstra Jr., Integer programming with a fixed number of variables, Mathematics of Operations Research 8(4), 1983
    locator: the main theorem (polynomial time for each fixed number of variables)
---

Mixed-integer linear programming (MILP) asks for a point that maximizes a linear function subject to linear inequalities, when some of the variables must be integers and the others are real. It extends [linear programming](/linear-programming-problem/) by one condition, integrality, and this condition makes the problem [NP-hard](/np-hard/). Most discrete decision problems of industry (scheduling, routing, network design, production planning) are written and solved as MILPs. Solvers combine the [LP relaxation](/lp-relaxation/), [cutting planes](/cutting-plane-method-integer-programming/) and [branch and cut](/branch-and-cut/).

## In plain words

A linear program chooses amounts, such as litres of fuel or hours of work, that can be any real number. Many real decisions are not like that. You open a factory or you do not. You buy whole trucks, not 2.7 trucks. A mixed-integer program lets you say that some of the unknowns must be whole numbers, and leaves the others free to take any value.

The objective and the rules stay linear: sums of the unknowns times fixed numbers. This small change has a large cost. Without the whole-number rule, the best point can be found fast. With it, no fast method is known that works for all problems, and the best point can be far from the best fractional point. Solvers still handle many large instances, because they use strong bounds and cut away fractional points.

## Definition

This page uses the form that the integer programming books use. Let $A \in \mathbb{Q}^{m \times n}$, $b \in \mathbb{Q}^m$, $c \in \mathbb{Q}^n$, and let $I \subseteq \{1, \ldots, n\}$ be the set of integer variables. The MILP is

$$\max \{\, c^T x : Ax \le b,\ x \ge 0,\ x_j \in \mathbb{Z} \text{ for all } j \in I \,\}.$$

Here $n$ is the number of variables and $m$ the number of constraints. The [linear programming](/linear-programming-problem/) pages use the form $\min c^T x$, $Ax = b$, $x \ge 0$. The two forms convert into each other with [slack variables](/slack-variables/) and a change of sign of $c$. When $c$ is integral and $I$ holds all variables, the slacks of an integral system $Ax \le b$ are integers too, so the conversion keeps a pure integer program pure.

- **Input.** The rational data $A$, $b$, $c$ and the index set $I$. The input size $L$ is the number of bits needed to write them.
- **Feasible set.** $S = \{x \in \mathbb{R}^n : Ax \le b,\ x \ge 0,\ x_I \in \mathbb{Z}^{I}\}$. This set is a union of pieces of polyhedra, and it is not convex in general.
- **Output.** One of three answers: "infeasible" when $S = \emptyset$; "unbounded" when $c^T x$ has no upper bound on $S$; or a point $x^* \in S$ with $c^T x^* = f^* = \sup \{c^T x : x \in S\}$.

With rational data the three answers cover all cases: if $S \ne \emptyset$ and the supremum is finite, then it is attained. This follows from Meyer's theorem: the convex hull of $S$ is a rational polyhedron, so the maximum of a linear function over it is attained at a point of $S$ when it is finite. With irrational data this fails. For example, $\sup\{x_1 - \sqrt{2}\,x_2 : x_1 - \sqrt{2}\,x_2 \le 0,\ x_1 \ge 1,\ x \in \mathbb{Z}^2\} = 0$ is not attained: each feasible point has $x_1 < \sqrt{2}\,x_2$ because $\sqrt{2}$ is irrational, but the fractions $x_1/x_2$ come as close to $\sqrt{2}$ as you want.

## Variants

- **Pure integer program (IP or ILP).** $I = \{1, \ldots, n\}$: all variables are integers.
- **Binary integer program.** All integer variables are restricted to $\{0, 1\}$. See [binary integer programming](/binary-integer-programming/). The mixed form with binary and continuous variables is the most common form in practice.
- **Feasibility version.** Decide if $S \ne \emptyset$. This is the [integer feasibility problem](/integer-feasibility/). Optimization reduces to it by binary search on the value of $c^T x$, because the optimum has a size polynomial in $L$.
- **Equality form.** $\max\{c^T x : Ax = b, x \ge 0, x_I \text{ integer}\}$. It is the form of the simplex tableau and of Gomory's cuts.
- **Linear programming.** $I = \emptyset$. Then the problem is the [linear programming problem](/linear-programming-problem/), which is in P.
- **Fixed dimension.** The number of integer variables is a constant. Then the problem is in P; see [integer programming in fixed dimension](/integer-programming-fixed-dimension/).
- **Mixed-integer nonlinear programming (MINLP).** The objective or the constraints are not linear. This page does not cover it.

## Examples

**A plant opening problem.** Two plants can serve a demand of 9 units. Plant 1 costs 10 to open, has capacity 8, and costs 1 per unit. Plant 2 costs 6 to open, has capacity 5, and costs 2 per unit. Let $y_i \in \{0, 1\}$ say if plant $i$ is open and let $x_i \ge 0$ be the amount it makes:

$$\min\ 10y_1 + 6y_2 + x_1 + 2x_2 \quad\text{s.t.}\quad x_1 + x_2 = 9,\ \ x_1 \le 8y_1,\ \ x_2 \le 5y_2,\ \ x \ge 0,\ \ y \in \{0,1\}^2.$$

No single plant can make 9 units, so both plants open. Then the best split is $x = (8, 1)$, and $f^* = 10 + 6 + 8 + 2 = 26$. The [LP relaxation](/lp-relaxation/) lets $y$ take values in $[0, 1]$. Its optimum is $y = (1, 1/5)$, $x = (8, 1)$, with value $106/5 = 21.2$: it pays only one fifth of the opening cost of plant 2. The constraint $x_2 \le 5y_2$ is a [big-M constraint](/big-m-formulation/).

**A pure integer program.** $\max x_2$ subject to $3x_1 + 2x_2 \le 6$, $-3x_1 + 2x_2 \le 0$, $x \ge 0$, $x \in \mathbb{Z}^2$. The feasible integer points are $(0,0)$, $(1,0)$, $(2,0)$ and $(1,1)$, so $f^* = 1$. The LP relaxation has its optimum at the vertex $(1, 3/2)$ with value $3/2$. The [Chvátal-Gomory cut](/chvatal-gomory-cut/) $x_2 \le 1$, which is $\tfrac14$ of the sum of the two constraints rounded down, cuts off that vertex.

**Infeasible although the relaxation is feasible.** $2x_1 - 2x_2 = 1$ with $x \in \mathbb{Z}^2$ has no solution, because the left side is even. The point $(1/2, 0)$ solves the relaxation.

## Known algorithms

- **Branch and bound and [branch and cut](/branch-and-cut/).** Solve the LP relaxation, branch on an integer variable with a fractional value, prune nodes by bound, and add cuts. This is the method of all general-purpose solvers. The worst case is exponential in the number of integer variables.
- **[Cutting-plane methods](/cutting-plane-method-integer-programming/).** Add valid inequalities until the LP optimum is integral. [Gomory's algorithm](/gomory-cutting-plane-algorithm/) is finite for pure integer programs with a lexicographic rule. Cuts such as the [Gomory mixed-integer cut](/gomory-mixed-integer-cut/) and the [mixed-integer rounding inequality](/mixed-integer-rounding-inequality/) also handle continuous variables.
- **Decomposition.** [Branch and price](/branch-and-price/), [Benders decomposition](/benders-decomposition/) and [Lagrangian relaxation](/lagrangian-relaxation/) split a large model into a master problem and subproblems.
- **[Lenstra's algorithm](/lenstra-algorithm/) and [Kannan's algorithm](/kannan-algorithm/).** For a fixed number of integer variables, they run in polynomial time. Kannan's algorithm takes $n^{O(n)}$ times a polynomial in $L$ arithmetic steps.
- **Dynamic programming.** For a fixed number of constraints and integral data, [Papadimitriou's algorithm](/papadimitriou-pseudopolynomial-theorem/) is pseudo-polynomial.
- **Primal heuristics.** The [feasibility pump](/feasibility-pump/), [diving](/diving-heuristic/), [RINS](/relaxation-induced-neighborhood-search/) and [local branching](/local-branching/) find good feasible points fast. They give no guarantee of optimality.

## Bounds

- **NP-hardness.** The feasibility version is NP-complete. It is NP-hard even when each variable is binary, because 0-1 integer programming is one of Karp's 21 problems (1972), and [3-SAT](/3-sat/) reduces to it with one constraint per clause. It stays NP-hard with one equality constraint, since the [subset sum problem](/subset-sum-problem/) is the case $\sum_j a_j x_j = b$, $x \in \{0,1\}^n$.
- **Membership in NP.** If an integer program with rational data has a feasible point, then it has one whose size is polynomial in $L$, and if it has an optimum, it has an optimal point of size polynomial in $L$ (Schrijver 1986, Chapter 17). So a short certificate exists.
- **Strong NP-hardness.** Problems such as [bin packing](/bin-packing/) are MILPs with numbers bounded by the input length, so no pseudo-polynomial algorithm exists for general MILP unless P = NP. See [strong NP-hardness](/strong-np-hardness/).
- **Upper bounds.** For a fixed number $n$ of integer variables, Lenstra (1983) solves the problem in polynomial time, and Kannan's bound is $n^{O(n)} \cdot \text{poly}(L)$. For a fixed number $m$ of equality constraints with integral entries, dynamic programming is pseudo-polynomial; the [proximity theorem](/eisenbrand-weismantel-proximity-theorem/) of Eisenbrand and Weismantel gives the best known bounds of this type.
- **Easy classes.** When $A$ is [totally unimodular](/total-unimodularity/) and $b$ is integral, every vertex of the LP relaxation is integral, so one LP solve gives the integer optimum. Flows, bipartite matching and the shortest path problem are in this class.

## Reductions

- **To linear programming over the hull.** By Meyer's theorem, the MILP equals the LP $\max\{c^T x : x \in \operatorname{conv}(S)\}$. The description of $\operatorname{conv}(S)$, the [integer hull](/integer-hull/), can have exponentially many inequalities, and finding them is as hard as the MILP itself.
- **To binary programs.** A bounded integer variable $0 \le x \le u$ becomes $x = \sum_{k=0}^{K} 2^k z_k$ with $z_k \in \{0,1\}$ and $K = \lfloor \log_2 u \rfloor$, plus the constraint $x \le u$. This adds $O(\log u)$ binary variables per integer variable.
- **From combinatorial problems.** [Vertex cover](/vertex-cover/), [set cover](/set-cover/), [knapsack](/knapsack-problem/), the [traveling salesman problem](/traveling-salesman-problem/), [facility location](/facility-location-problem/) and [graph coloring](/graph-coloring/) have standard MILP models. These models carry hardness back to MILP and are the start of LP rounding approximation algorithms.
- **To and from satisfiability.** A 0-1 program is a [pseudo-Boolean](/pseudo-boolean-sat/) constraint problem. Pure integer feasibility is the satisfiability problem of [linear integer arithmetic](/linear-integer-arithmetic-satisfiability/).

## Applications

- **Production and supply chain.** Lot sizing, plant location with fixed costs, and capacity planning, as in the plant example.
- **Scheduling and timetabling.** Machine scheduling with disjunctive constraints, crew scheduling and rostering. Airline crew pairing is a large set partitioning model, solved by [branch and price](/branch-and-price/).
- **Routing and network design.** Vehicle routing, the traveling salesman problem, and the design of telecommunication and power networks.
- **Energy.** Unit commitment of power plants, with on and off decisions and minimum up and down times.
- **Proofs in mathematics and verification.** Exact MILP solvers have proved results in combinatorics, and integer constraints appear in program analysis.

## References
