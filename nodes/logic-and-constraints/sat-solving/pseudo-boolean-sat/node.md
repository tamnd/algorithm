---
tag: V0G0DJ
kind: problem
slug: pseudo-boolean-sat
name: Pseudo-Boolean satisfiability
aliases:
- PB-SAT
- 0-1 linear constraints
- pseudo-Boolean solving
- PBS
area: logic-and-constraints/sat-solving
level: advanced
summary: Decide whether a set of linear inequalities with integer coefficients over 0-1 variables has a solution; NP-complete, and the 0-1 form of integer programming.
prereqs: [sat, literal, np-complete]
see_also: [binary-integer-programming, sequential-counter-encoding, totalizer-encoding, max-sat, cdcl, haken-resolution-lower-bound, subset-sum-problem, cutting-plane-method]
sources:
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 28 (Roussel and Manquinho, Pseudo-Boolean and Cardinality Constraints), the normal form, propagation, translations to SAT and native PB solvers; Chapter 7 (Buss and Nordström, Proof Complexity and SAT Solving), the section on cutting planes
  - paper: "Niklas Eén and Niklas Sörensson, Translating pseudo-Boolean constraints into SAT, Journal on Satisfiability, Boolean Modeling and Computation 2, 2006, pages 1 to 26"
    title: Translating pseudo-Boolean constraints into SAT (MiniSat+)
    locator: the translations through BDDs, adders and sorting networks, and their propagation strength
  - paper: doi:10.1016/0166-218X(87)90039-4
    title: William Cook, Collette R. Coullard and György Turán, On the complexity of cutting-plane proofs, Discrete Applied Mathematics 18(1), 1987, 25-38
    locator: cutting planes p-simulate resolution and have polynomial-size refutations of the pigeonhole formulas
---

Pseudo-Boolean satisfiability asks whether a set of linear inequalities with integer coefficients over 0-1 variables has a solution. A pseudo-Boolean (PB) constraint such as $3x_1 + 2x_2 + \bar x_3 \ge 3$ generalizes a [clause](/clause/), which is the case $l_1 + \cdots + l_k \ge 1$, and a cardinality constraint, which has all coefficients 1. The problem is [NP-complete](/np-complete/). It is the same problem as the feasibility version of [0-1 integer programming](/binary-integer-programming/). Solvers either translate the constraints to CNF and call a SAT solver, or run a [CDCL](/cdcl/) search that reasons with the inequalities directly, using cutting planes. On some formulas, such as the pigeonhole formulas, cutting planes are exponentially stronger than resolution.

## In plain words

Each constraint is a weighted vote. Every literal that comes out true adds its weight, and the total must reach a threshold. "At least two of these five tasks run" and "the chosen items weigh at most 10" are both constraints of this kind. A clause is the special vote "at least one of these literals is true".

The question is whether one yes or no choice for each variable meets every threshold at the same time. It is as hard as SAT, but the weights let you write many constraints much more briefly. A solver can also add two constraints, divide by a number and round up, which is a stronger kind of reasoning than the clause steps of a normal SAT solver.

## Definition

Notation: $x_1, \ldots, x_n$ are 0-1 variables, $\bar x = 1 - x$, a literal $l$ is $x$ or $\bar x$, $m$ is the number of constraints, and $|F|$ is the total number of terms over all constraints, with the bit lengths of the coefficients.

A **PB constraint** is $\sum_i a_i l_i \ge b$ with integers $a_i$ and $b$. Each constraint with $\le$, $=$, negative coefficients or a variable that occurs twice can be put into the **normal form** $\sum_i a_i l_i \ge b$ with all $a_i > 0$, $b > 0$ and distinct variables:

- $\sum a_i l_i \le b$ becomes $\sum (-a_i) l_i \ge -b$, and an equation becomes two inequalities;
- a term $-a\,x$ with $a > 0$ becomes $a\,\bar x - a$, since $x = 1 - \bar x$; move the constant into $b$;
- $a\,x + c\,\bar x$ becomes $(a - c)\,x + c$, and the same for repeated literals;
- if $b \le 0$ after this, the constraint is always true.

A normalized constraint can also be **saturated**: replace each $a_i > b$ by $b$. This keeps the set of solutions, because one such literal already meets the threshold.

**PB-SAT.** Input: a set of PB constraints. Question: is there an assignment $\alpha \in \{0,1\}^n$ that satisfies all of them?

**PB optimization (PBO).** Also given an objective $\sum_i c_i l_i$, find a satisfying assignment with the least objective value, or report that none exists.

## Variants

- **Cardinality constraints.** All $a_i = 1$: $\sum l_i \ge b$, "at least $b$ of these literals".
- **CNF-SAT.** All $a_i = 1$ and $b = 1$.
- **One constraint.** A single normalized inequality is always satisfiable (set every literal true). A single equation $\sum a_i x_i = b$ is [subset sum](/subset-sum-problem/), which is NP-complete.
- **Linear PB versus nonlinear PB.** Nonlinear PB allows products of literals in the terms. Each product can be replaced by a new variable $y$ with $y \leftrightarrow (l_1 \wedge l_2)$, so it reduces to the linear case.
- **Weighted MaxSAT** is PBO in which each soft clause gets a relaxation literal with the clause weight in the objective. See [MaxSAT](/max-sat/).

## Examples

**Normalization.** $2x_1 - 3x_2 \ge -1$. Write $-3x_2 = 3\bar x_2 - 3$, so $2x_1 + 3\bar x_2 \ge 2$. Saturation gives $2x_1 + 2\bar x_2 \ge 2$, and dividing by 2 gives the clause $x_1 \vee \bar x_2$. Check: the only excluded point is $x_1 = 0, x_2 = 1$, where $2 \cdot 0 - 3 = -3 < -1$.

**Propagation by slack.** For a normalized constraint $C: \sum a_i l_i \ge b$ and a partial assignment $\rho$, the **slack** is
$$\text{slack}(C, \rho) = \sum_{l_i \text{ not false under } \rho} a_i \;-\; b.$$
If the slack is negative, $C$ is falsified: even with all free literals true the sum stays below $b$. If a free literal $l_i$ has $a_i > \text{slack}$, then $l_i$ must be true, because setting it false lowers the largest reachable sum by $a_i$ and below $b$. Take $C: 3x_1 + 2x_2 + 2x_3 + x_4 \ge 5$. With nothing set, the slack is $3$, so no literal is forced. After $x_2 = 0$ the slack is $1$, so $x_1$ ($3 > 1$) and $x_3$ ($2 > 1$) are forced true, but $x_4$ is not. Unit propagation on clauses is the case $a_i = 1$, $b = 1$: the slack is the number of free literals minus one.

**Pigeonhole.** With $p_{ij}$ for "pigeon $i$ sits in hole $j$", $n + 1$ pigeons and $n$ holes, the constraints $\sum_j p_{ij} \ge 1$ for each pigeon and $\sum_i \bar p_{ij} \ge n$ (at most one pigeon per hole) for each hole are unsatisfiable. Adding all $2n + 1$ constraints gives $\sum_{i,j} (p_{ij} + \bar p_{ij}) \ge (n+1) + n^2$, but the left side equals $n(n+1)$ for every assignment, which is less. Cutting planes find this in one sum; resolution needs size $2^{\Omega(n)}$ on the CNF form, by [Haken's theorem](/haken-resolution-lower-bound/).

## Known algorithms

| Approach | Idea | Notes |
|---|---|---|
| Brute force | try all $2^n$ assignments | $O(2^n \cdot |F|)$ time |
| Translation to SAT | encode each constraint in CNF, call a SAT solver | cardinality constraints: [sequential counter](/sequential-counter-encoding/), [totalizer](/totalizer-encoding/), sorting networks; general constraints: BDDs, adders, sorters (Eén and Sörensson, MiniSat+) |
| Native PB CDCL | CDCL with slack propagation and conflict analysis by cutting planes | learned constraints are PB constraints; see the Handbook, Chapter 28 |
| 0-1 integer programming | LP relaxation, [branch and cut](/branch-and-cut/) | strong when the LP bound is tight |

**Translation sizes.** A BDD translation of $\sum a_i l_i \ge b$ keeps arc consistency under unit propagation, but some constraints have BDDs of exponential size. An adder (binary) translation is $O(\sum_i \log a_i)$ in size but its unit propagation is weak. A sorting network on the unary digits of the coefficients sits between the two. The translations of [cardinality constraints](/totalizer-encoding/) above are polynomial and arc consistent.

**Cutting planes.** The rules on normalized constraints are: add two constraints; multiply a constraint by a positive integer; divide by a positive integer $d$ and round up, $\sum \lceil a_i / d \rceil l_i \ge \lceil b / d \rceil$; and saturate. Division is sound because each left side is an integer. Native PB solvers learn constraints derived by these rules from a conflict.

## Bounds

- **Upper bound.** PB-SAT is in NP: check an assignment in $O(|F|)$ arithmetic steps. Brute force is $O(2^n |F|)$.
- **Conditional lower bound.** CNF-SAT is a special case, so under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) there is no $O(2^{(1-\varepsilon)n})$ algorithm for PB-SAT for any fixed $\varepsilon > 0$.
- **Proof complexity.** Cutting planes p-simulate resolution and have polynomial-size refutations of the pigeonhole formulas (Cook, Coullard and Turán 1987), so they are strictly stronger than resolution. Exponential lower bounds for cutting planes are known too (Pudlák 1997, through monotone interpolation of the clique-coloring formulas). A native PB solver whose learning is closer to resolution, for example one that weakens each conflict to a clause, loses this advantage.

## Reductions

- **SAT to PB-SAT.** Write each clause $l_1 \vee \cdots \vee l_k$ as $l_1 + \cdots + l_k \ge 1$. This and membership in NP give NP-completeness.
- **PB-SAT to SAT.** Encode each constraint in CNF with new variables, by the methods in the table. For cardinality constraints the result has polynomial size; for general coefficients the adder translation has polynomial size.
- **PB-SAT and 0-1 integer programming** are the same problem: a PB constraint is a row of a 0-1 program. See [0-1 integer programming](/binary-integer-programming/) and [integer feasibility](/integer-feasibility/).
- **Subset sum and knapsack to PB-SAT.** A [subset sum](/subset-sum-problem/) instance is one equation; [knapsack](/knapsack-problem/) with a value target is two inequalities.

## Applications

- **Scheduling and timetabling**, where "at most $k$ tasks per slot" and resource budgets are PB constraints.
- **Hardware and software verification**, where counting and weighted constraints appear in bounded model checking and test generation.
- **Weighted [MaxSAT](/max-sat/)** and other optimization problems that are given as PBO.
- **Combinatorics.** Some problems with many cardinality constraints, such as covering designs, are easier to state and solve as PB.
- **Proof logging for other solvers.** The VeriPB format certifies results with cutting planes steps; see [DRAT](/drat-proof/) for the clause-based analogue.

## References
