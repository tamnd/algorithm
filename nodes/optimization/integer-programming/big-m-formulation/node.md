---
tag: 56J4DA
kind: concept
slug: big-m-formulation
name: Big-M formulation
aliases:
- big-M constraints
- big-M method
- big-M constraint
area: optimization/integer-programming
level: core
summary: Modeling technique that uses a large constant to switch constraints on and off with a binary variable.
prereqs: [binary-integer-programming, lp-relaxation]
see_also: [indicator-constraint, ideal-formulation, integrality-gap, disjunctive-cut, presolve, big-m-method, mixed-integer-programming, flow-cover-inequality]
sources:
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming, Wiley, 1998
    locator: Chapter 1 (modeling with binary variables, fixed costs and disjunctions)
  - paper: "Juan Pablo Vielma, Mixed integer linear programming formulation techniques, SIAM Review 57(1) (2015), 3 to 57"
    locator: the sections on Big-M formulations and their strength compared with the union formulation
  - paper: "Pietro Belotti, Pierre Bonami, Matteo Fischetti, Andrea Lodi, Michele Monaci, Amaya Nogales-Gómez and Domenico Salvagnin, On handling indicator constraints in mixed integer programming, Computational Optimization and Applications 65 (2016), 545 to 566"
    locator: the discussion of numerical trouble with large M and of bound tightening
  - book: isbn:9780471828198
    title: George L. Nemhauser and Laurence A. Wolsey, Integer and Combinatorial Optimization, Wiley, 1988
    locator: Part I, Chapter 1 (modeling with integer variables)
---

A Big-M formulation models a logical condition, such as "if $z = 1$ then $a^T x \le \beta$", with one linear constraint

$$a^T x \le \beta + M(1 - z),$$

where $z \in \{0, 1\}$ and $M$ is a constant large enough that the constraint is redundant when $z = 0$. It is the most common way to write fixed costs, either-or constraints, scheduling orders and other logic as a [mixed-integer program](/mixed-integer-programming/). It is simple and needs no new variables, but a large $M$ gives a weak [LP relaxation](/lp-relaxation/) and numerical trouble. A good model uses the smallest valid $M$, or an [indicator constraint](/indicator-constraint/) or a [union formulation](/ideal-formulation/) instead.

## In plain words

Sometimes a rule must hold only in some cases. For example, a factory can produce only if it is open. A Big-M constraint writes this with an on and off switch, a variable that is 0 or 1, and a large number $M$. When the switch is on, the rule is in force. When it is off, the large number makes the rule so loose that it does nothing.

The trouble comes when the solver relaxes the switch to a fraction. With a huge $M$, a switch at 0.001 is enough to allow almost anything, so the relaxed problem learns little. The fix is to choose $M$ as small as the data allows.

## The idea

**The basic pattern.** Let $D$ be a bounded set that contains all values of $x$ of interest, such as a box $\ell \le x \le u$ of variable bounds. To enforce $a^T x \le \beta$ only when $z = 1$, write

$$a^T x \le \beta + M(1 - z), \qquad z \in \{0, 1\}.$$

With $z = 1$ this is the constraint itself. With $z = 0$ it reads $a^T x \le \beta + M$, which holds for all $x \in D$ if and only if

$$M \ge M^* = \max\{a^T x : x \in D\} - \beta.$$

For a box, $M^* = \sum_j \max(a_j \ell_j,\ a_j u_j) - \beta$. A smaller $M$ cuts off feasible points with $z = 0$, so the model is wrong. A larger $M$ is valid but weaker. If $D$ is not bounded, no finite $M$ is valid in general, and the model needs bounds or a different formulation.

**Common uses.**

- *Fixed charge.* A quantity $0 \le x \le u$ costs $f$ once if it is positive: $x \le M y$ with $y \in \{0,1\}$ and cost $f y$. The best $M$ is $u$.
- *Either-or.* At least one of $a^T x \le \beta$ and $g^T x \le \gamma$ holds: $a^T x \le \beta + M_1 z$ and $g^T x \le \gamma + M_2 (1 - z)$.
- *At least $k$ of $m$.* $a_i^T x \le \beta_i + M_i(1 - z_i)$ for each $i$, and $\sum_i z_i \ge k$.
- *Order in scheduling.* For jobs $i$ and $j$ on one machine with start times $s$ and processing times $p$, one of them is first: $s_i + p_i \le s_j + M(1 - z_{ij})$ and $s_j + p_j \le s_i + M z_{ij}$. Here $M$ is the length of the planning horizon.
- *Implications between binaries.* "$z_1 = 1$ implies $x \ge \ell$" becomes $x \ge \ell z_1$, the case where the smallest $M$ is part of the data.

**Strength.** In the relaxation, $z$ can take any value in $[0,1]$, and the constraint becomes $a^T x \le \beta + M(1 - z)$. For the fixed charge, the relaxation chooses $y = x / M$ and pays only $f x / M$. So the relaxed fixed cost falls like $1/M$. For a disjunction of two polytopes, the Big-M relaxation contains the convex hull of the union, and is usually much larger. The union formulation of Balas, on the [ideal formulation](/ideal-formulation/) page, gives the convex hull exactly, but it copies the variables.

**Numerics.** Solvers accept $z$ as integral when it lies within a tolerance $\varepsilon$ of an integer, such as $10^{-5}$. With $z = 1 - \varepsilon$, the constraint allows $a^T x \le \beta + M\varepsilon$, so with $M = 10^6$ a constraint that should hold can be violated by 10. Large $M$ values also make the LP badly scaled, which slows the [simplex method](/simplex-method/) and harms the accuracy of the bound.

**Remedies.**

1. Compute the smallest valid $M$ from variable bounds, and tighten the bounds first. [Presolve](/presolve/) does this with bound propagation, and some solvers tighten $M$ again at each node of the search.
2. Use different constants $M_i$ for different rows, each from its own bound.
3. Use an [indicator constraint](/indicator-constraint/), which the solver enforces by branching, so no $M$ is needed.
4. Use the union formulation, or add valid inequalities such as [flow covers](/flow-cover-inequality/) and [disjunctive cuts](/disjunctive-cut/) that recover part of the convex hull.

Do not confuse this with the [Big-M method](/big-m-method/) of linear programming, which uses a large penalty in the objective to find a first feasible basis.

## Examples

**Fixed charge with three values of M.** A product must meet a demand of $d = 10$ units. Producing costs 1 per unit and a setup cost of $f = 100$. The model is

$$\min\ 100 y + x \quad\text{s.t.}\quad x = 10,\quad x \le M y,\quad y \in \{0, 1\}.$$

The integer optimum is $y = 1$, $x = 10$ with cost 110. The relaxation sets $y = 10/M$:

| $M$ | LP $y$ | LP value | ratio IP/LP |
|---|---|---|---|
| 10 | 1 | 110 | 1 |
| 20 | 1/2 | 60 | 11/6 |
| 100 | 1/10 | 20 | 11/2 |

With $M = d = 10$ the formulation is [ideal](/ideal-formulation/) for this one product, and the relaxation is exact. With $M = 100$, the bound is 20 and a branch-and-bound search must branch on $y$ to find the truth.

**A box-derived M.** To enforce $2x_1 - 3x_2 \le 4$ when $z = 1$, with $0 \le x_1 \le 5$ and $0 \le x_2 \le 3$, the largest value of $2x_1 - 3x_2$ on the box is $2 \cdot 5 - 3 \cdot 0 = 10$. So $M^* = 10 - 4 = 6$, and the constraint is $2x_1 - 3x_2 \le 4 + 6(1 - z)$. Any $M < 6$ forbids the feasible point $(5, 0)$ with $z = 0$.

## Where it is used

- **Facility location and network design.** Arcs and facilities are opened by binaries, and flows are linked to them by $x \le u y$.
- **Scheduling.** Disjunctive models of machine scheduling use one order variable per pair of jobs. Their weak relaxations are a known reason to prefer time-indexed or constraint programming models for hard instances.
- **Piecewise linear and logical models.** Choices among regimes, such as tax brackets or operating modes, are often first written with Big-M constraints.
- **Verification of neural networks.** A ReLU unit $y = \max(0, w^T x + b)$ is written with one binary and Big-M constants from bounds on $w^T x + b$, and the strength of these constants decides how fast the model solves.
- **Bilevel optimization.** The optimality conditions of a lower-level linear program contain complementarity conditions, and the usual single-level model writes each one with a binary and Big-M constraints.

## References
