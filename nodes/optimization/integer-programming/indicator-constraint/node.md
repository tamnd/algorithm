---
tag: 9K26XB
kind: concept
slug: indicator-constraint
name: Indicator constraint
aliases:
- indicator variable constraint
- conditional constraint
- on/off constraint
area: optimization/integer-programming
level: advanced
summary: Constraint enforced only when a binary indicator variable equals 1.
prereqs: [big-m-formulation, binary-integer-programming]
see_also: [big-m-formulation, ideal-formulation, disjunctive-cut, branch-and-cut, mixed-integer-programming, lp-relaxation, presolve, integer-hull]
sources:
  - paper: "Pierre Bonami, Andrea Lodi, Andrea Tramontani and Sven Wiese, On mathematical programming with indicator constraints, Mathematical Programming 151 (2015), 191 to 223"
    locator: the definition of indicator constraints, the convex hull results and the perspective reformulation
  - paper: "Pietro Belotti, Pierre Bonami, Matteo Fischetti, Andrea Lodi, Michele Monaci, Amaya Nogales-Gómez and Domenico Salvagnin, On handling indicator constraints in mixed integer programming, Computational Optimization and Applications 65 (2016), 545 to 566"
    locator: the comparison of Big-M linearization with branching on the disjunction
  - paper: "Robert G. Jeroslow and James K. Lowe, Modelling with integer variables, Mathematical Programming Study 22 (1984), 167 to 184"
    locator: the characterization of sets that a mixed-integer program can represent
  - paper: "Antonio Frangioni and Claudio Gentile, Perspective cuts for a class of convex 0-1 mixed integer programs, Mathematical Programming 106 (2006), 225 to 236"
    locator: the perspective cuts for a convex cost that is switched on by a binary variable
  - paper: "Juan Pablo Vielma, Mixed integer linear programming formulation techniques, SIAM Review 57(1) (2015), 3 to 57"
    locator: the section on representability by mixed-integer formulations
---

An indicator constraint is a logical implication between a binary variable $z$ and a linear constraint:

$$z = 1 \ \Longrightarrow\ a^T x \le \beta.$$

When $z = 0$, the constraint is not imposed. Modern MIP solvers accept indicator constraints directly. They either turn them into a [Big-M constraint](/big-m-formulation/) when a safe small $M$ follows from the bounds, or keep them as a disjunction and enforce them by branching. The second way needs no $M$, so it works with unbounded variables and avoids the numerical trouble of a huge $M$. Its cost is that the [LP relaxation](/lp-relaxation/) learns nothing from the constraint until the solver branches on $z$.

## In plain words

Many rules apply only in some cases. "If the machine is on, its output is at least 10." "If this customer is served by depot 3, the truck leaves before noon." An indicator constraint says this directly: a yes or no variable, and a rule that holds when the variable says yes.

The older trick writes the rule with a very large number, so that the rule becomes harmless when the switch is off. That trick needs a safe large number, and a too large number confuses the solver. With an indicator constraint, the solver itself decides how to handle the rule: by the old trick when a safe small number exists, or by trying both cases, switch on and switch off, one at a time.

## The idea

**Definition.** Let $z \in \{0, 1\}$ and $x \in \mathbb{R}^n$. An indicator constraint is the pair $(z, a^T x \le \beta)$, read as $z = 1 \Rightarrow a^T x \le \beta$. The variant $z = 0 \Rightarrow a^T x \le \beta$ is the same with $1 - z$, and an equation is two inequalities. The implication goes one way only: $a^T x \le \beta$ does not force $z = 1$. The converse "$a^T x \le \beta \Rightarrow z = 1$" is $z = 0 \Rightarrow a^T x > \beta$, and since a solver cannot use a strict inequality, it is written as $z = 0 \Rightarrow a^T x \ge \beta + \delta$ with a small $\delta > 0$ chosen by the modeler.

The feasible set is the union of two pieces:

$$S = \{(x, 0) : x \in X\} \ \cup\ \{(x, 1) : x \in X,\ a^T x \le \beta\},$$

where $X$ is the set given by the other constraints.

**Three ways to handle it.**

1. *Big-M linearization.* If $a^T x \le \beta + M$ holds on $X$, write $a^T x \le \beta + M(1 - z)$. The smallest such $M$ comes from bounds on $x$. Solvers do this when they can compute a small enough $M$, often after bound tightening in [presolve](/presolve/).
2. *SOS1 form.* Add a slack $s \ge 0$ with $a^T x - s \le \beta$, and require that at most one of $s$ and $z$ is nonzero, a special ordered set of type 1. Then $z = 1$ forces $s = 0$. The solver branches on the set: one child has $s = 0$, the other has $z = 0$.
3. *Branching on the disjunction.* At a node whose LP solution $(x^*, z^*)$ has $z^* > 0$ and $a^T x^* > \beta$, create the children $z = 0$ and $\{z = 1,\ a^T x \le \beta\}$. In the first child the constraint is dropped, and in the second it is a normal row.

Options 2 and 3 are exact for any data, but the root relaxation ignores the constraint. Option 1 gives a stronger root bound when $M$ is small and a weak one when $M$ is large. Belotti and coauthors (2016) studied this trade-off, and solvers now combine both: they linearize with a safe $M$ and still branch on the disjunction when the linear form is weak.

**Representability.** Jeroslow and Lowe (1984) showed that a set is the projection of the feasible set of a mixed-integer program with rational data and binary integer variables if and only if it is a finite union of rational polyhedra that all have the same recession cone. An indicator constraint on an unbounded variable can break this. For example, $\{(x, z) : z = 0 \Rightarrow x \le 0,\ x \ge 0,\ z \in \{0, 1\}\}$ is the union of the point $(0, 0)$ and the half line $\{(x, 1) : x \ge 0\}$, whose recession cones differ. So no Big-M model and no other model with binary variables is exact, while a solver that branches on the indicator handles it.

**Convex hull.** For a single indicator and a polytope $X$, the convex hull of $S$ is given by Balas's union formulation on the [ideal formulation](/ideal-formulation/) page. For a convex function switched on by $z$, such as a cost $f(x)$ that applies only when $z = 1$ and $x = 0$ when $z = 0$, the hull uses the *perspective* $z f(x / z)$. Frangioni and Gentile (2006) derived linear *perspective cuts* from it, and Bonami, Lodi, Tramontani and Wiese (2015) studied when a hull of several indicators has a simple form.

## Examples

**A fixed charge with no bound.** Demand is 10 units, each unit costs 1, and production needs a setup of cost 100:

$$\min\ 100 y + x \quad\text{s.t.}\quad x = 10,\quad y = 0 \Rightarrow x \le 0,\quad y \in \{0, 1\}.$$

As an indicator constraint, the root relaxation drops the implication and returns $y = 0$, $x = 10$, value 10, which violates it. The solver branches. The child $y = 0$ adds $x \le 0$ and is infeasible. The child $y = 1$ gives $x = 10$ with value 110, the optimum. With the Big-M form $x \le 10 y$, the root relaxation already gives 110, since $M = 10$ comes from the demand. With $M = 100$, the root bound is 20. So the indicator is better than a large $M$ and worse than the best $M$.

**Minimum output.** A generator is off ($z = 0$, output $x = 0$) or on with $\ell \le x \le u$. Two indicators state it: $z = 0 \Rightarrow x \le 0$ and $z = 1 \Rightarrow x \ge \ell$. With known bounds, the formulation $\ell z \le x \le u z$ is [ideal](/ideal-formulation/), and the solver should get that form.

**Either-or.** "Either $x_1 \le 2$ or $x_1 \ge 5$" becomes $z = 1 \Rightarrow x_1 \le 2$ and $z = 0 \Rightarrow x_1 \ge 5$. This is a [disjunction](/disjunctive-cut/), and branching on $z$ is the same as branching on the two sides.

## Where it is used

- **Solver interfaces.** CPLEX, Gurobi, Xpress and SCIP accept indicator constraints, and modeling languages translate logical expressions into them.
- **Unit commitment and process design.** On/off units with minimum outputs and switching costs are natural indicator constraints.
- **Machine learning models.** Sparse regression with a limit on the number of nonzero coefficients uses $z_j = 0 \Rightarrow \beta_j = 0$, and perspective cuts strengthen the quadratic loss.
- **Verification and logic.** Models of ReLU networks and of rules in planning problems use indicators when the bounds of the variables are loose or unknown.
- **Branching research.** Indicator constraints are a special case of general disjunctions, and [branch and cut](/branch-and-cut/) frameworks treat both with the same machinery.

## References
