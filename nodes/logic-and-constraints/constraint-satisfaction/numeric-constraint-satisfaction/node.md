---
tag: VVVFN0
kind: problem
slug: numeric-constraint-satisfaction
name: Numeric constraint satisfaction problem
aliases:
- numeric CSP
- NCSP
- continuous CSP
- interval CSP
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: A CSP over real variables with interval domains and nonlinear equations or inequalities. The output is a set of small boxes that covers all solutions, found by branch and prune.
prereqs: [constraint-satisfaction-problem, interval-arithmetic]
see_also: [interval-constraint-propagation, interval-newton-method, interval-branch-and-bound, bisection-method, nonlinear-real-arithmetic-satisfiability, delta-satisfiability, newton-method-for-systems, global-optimization]
sources:
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 16, Continuous and interval constraints, by Frédéric Benhamou and Laurent Granvilliers (numeric CSPs, outer and inner boxes, branch and prune)
  - paper: "Pascal Van Hentenryck, David McAllester and Deepak Kapur, Solving polynomial systems using a branch and prune approach, SIAM Journal on Numerical Analysis 34(2), 1997, pages 797 to 827"
    locator: the branch and prune algorithm with box consistency and its use on polynomial systems
  - paper: "Olivier Lhomme, Consistency techniques for numeric CSPs, Proceedings of IJCAI-93, 1993, pages 232 to 238"
    locator: the definition of numeric CSPs over interval domains and of 2B and 3B consistency
  - paper: "Sicun Gao, Jeremy Avigad and Edmund M. Clarke, Delta-complete decision procedures for satisfiability over the reals, Proceedings of IJCAR 2012, Lecture Notes in Computer Science 7364, pages 286 to 300"
    locator: the delta-decision problem and its decidability for formulas with computable functions
  - book: isbn:9780898716696
    title: Ramon E. Moore, R. Baker Kearfott and Michael J. Cloud, Introduction to Interval Analysis, SIAM, 2009
    locator: Chapters 6 and 8 (the interval Newton method, the Krawczyk test, and the proof that a box holds a unique solution)
  - paper: doi:10.2307/2271358
    title: Daniel Richardson, Some undecidable problems involving elementary functions of a real variable, Journal of Symbolic Logic 33(4), 1968
    locator: pages 514 to 520 (deciding whether an expression with sin, exp and the absolute value has a real zero is undecidable)
---

A numeric constraint satisfaction problem (numeric CSP) has real variables, each with an interval as its domain, and constraints that are equations or inequalities, often nonlinear, such as $x^2 + y^2 = 1$ or $\sin x \le y$. Its solution set is usually infinite, or a finite set of irrational points, so a computer cannot list it. A solver returns instead a finite set of small boxes whose union contains every solution, and sometimes a proof that a box holds exactly one solution. The standard method is *branch and prune*: [interval constraint propagation](/interval-constraint-propagation/) shrinks each box, and bisection splits boxes that are still too wide. Interval constraint propagation is one algorithm for the pruning step. This page is about the problem it serves: what a solution is, what output is possible, and how hard the problem is.

## In plain words

The unknowns are real numbers in given ranges, and the rules are formulas, such as "the point lies on the unit circle and on the line $x = y$". The answers can be single points with endless decimals, curves, or whole regions, so a computer cannot write them down exactly.

So the goal changes: cover all the answers with small boxes, as small as you want, and never leave an answer out. Some boxes may hold no answer at all, because the method cannot always tell. For a box around a single point, an extra test can sometimes prove that exactly one answer is inside.

## Definition

A numeric CSP is a triple $(X, B, C)$:

- $X = (x_1, \ldots, x_n)$ are real variables.
- $B = I_1 \times \cdots \times I_n$ is a box of closed intervals with float ends, possibly infinite.
- $C$ is a finite set of constraints $c$, each of the form $f_c(x) = 0$, $f_c(x) \le 0$ or $\ell_c \le f_c(x) \le u_c$, where $f_c$ is an expression in the variables built from constants, $+$, $-$, $\times$, $/$, powers and elementary functions such as $\sqrt{\ }$, $\exp$, $\log$, $\sin$.

The solution set is $\Sigma = \{ p \in B : p \text{ meets every } c \in C \}$. Since $\Sigma$ cannot be computed exactly in general, the usual tasks are:

- **Outer approximation (paving).** Given $\varepsilon > 0$, return a finite set of boxes, each of width at most $\varepsilon$, whose union contains $\Sigma$. An empty set is a proof that $\Sigma = \emptyset$.
- **Inner approximation.** For inequalities, return boxes that lie entirely inside $\Sigma$, so that every point of them is a solution.
- **Certified isolation.** For square systems ($n$ equations in $n$ variables), return boxes, each proved to hold exactly one solution, for example by the [interval Newton method](/interval-newton-method/).
- **Feasibility.** Decide whether $\Sigma$ is empty. Because of the bounds below, solvers often decide the weaker [delta-satisfiability](/delta-satisfiability/) question instead.

## Variants

- **Polynomial constraints.** All $f_c$ are polynomials. This is the existential theory of the reals when the box is all of $\mathbb{R}^n$.
- **Square systems.** $n$ equations in $n$ variables with isolated solutions, the case of most numerical solvers.
- **Under-constrained systems.** Fewer equations than variables, or only inequalities. The solution set is a curve, a surface or a region, and the output is a paving with many boxes.
- **Mixed problems.** Some variables are integers, as in [mixed integer programming](/mixed-integer-programming/) with nonlinear constraints.
- **Optimization.** Minimize $f(x)$ subject to the constraints. This is [interval branch and bound](/interval-branch-and-bound/) and part of [global optimization](/global-optimization/).
- **SMT form.** Boolean combinations of nonlinear real constraints, the logic of [nonlinear real arithmetic](/nonlinear-real-arithmetic-satisfiability/).

## Examples

The numbers below come from running branch and prune with the HC4 propagator of the [interval constraint propagation](/interval-constraint-propagation/) page, bisecting the widest domain at its midpoint.

**Two points.** $x, y \in [-2, 2]$, with $x^2 + y^2 = 1$ and $x = y$. The solutions are $\pm(1/\sqrt 2, 1/\sqrt 2) \approx \pm(0.70711, 0.70711)$.

| step | box | result of propagation |
|---|---|---|
| start | $[-2, 2]^2$ | $[-1, 1]^2$ |
| split $x$ at 0 | $[0, 1] \times [-1, 1]$ | $[0, 1]^2$, since $y = x \ge 0$ |
| split $x$ at 0 | $[-1, 0] \times [-1, 1]$ | $[-1, 0]^2$ |

Propagation alone stops at $[-1, 1]^2$, since each constraint by itself allows every end of each domain. Splitting is needed to separate the two solutions. With $\varepsilon = 10^{-3}$, the solver makes 7 splits, proves 6 boxes empty, and returns 2 boxes, one around each solution, for example $[0.70671, 0.70750]^2$. With $\varepsilon = 10^{-6}$ it makes 9 splits and returns 2 boxes of width about $2 \times 10^{-7}$.

**A curve.** With only $x^2 + y^2 = 1$ on $[-2, 2]^2$ and $\varepsilon = 0.1$, the solver returns 96 boxes that cover the circle. For a curve, the number of boxes grows about like $1 / \varepsilon$, and for a solution set of dimension $k$ about like $1 / \varepsilon^k$.

**A box with no solution that is not removed.** On $[-1, 1]^2$, the system $x + y = 0$, $x - y = 0$ has only the solution $(0, 0)$, but propagation removes nothing from $[-1, 1]^2$. A box returned by a solver may therefore be much larger than the set of solutions it holds, until it is split.

## Known algorithms

| method | output | guarantee | notes |
|---|---|---|---|
| branch and prune with [ICP](/interval-constraint-propagation/) and [bisection](/bisection-method/) | outer paving | no solution lost, with outward rounding | HC4, box consistency, or 3B consistency as the prune step |
| [interval Newton](/interval-newton-method/), Krawczyk test | boxes with exactly one solution | proof of existence and uniqueness | for square systems with regular solutions |
| [interval branch and bound](/interval-branch-and-bound/) | enclosure of the global optimum | certified bounds | for the optimization form |
| cylindrical algebraic decomposition (Collins 1975) | exact description of $\Sigma$ | exact, for polynomials | doubly exponential in $n$ in the worst case |
| homotopy continuation | all isolated complex solutions of a polynomial system | numerical, with high probability | not rigorous without extra checks |
| local [Newton's method for systems](/newton-method-for-systems/) | one approximate solution | none | fast near a solution, may diverge |

Branch and prune keeps a list of boxes. It takes a box, prunes it with propagation, drops it if propagation proves it empty, returns it if it is narrower than $\varepsilon$, and otherwise splits it into two halves and puts both back. Each box it drops holds no solution, by the soundness of propagation, and the union of the boxes in the list and the output always contains $\Sigma$. Each split halves the width of one domain, so with bounded domains the process ends.

## Bounds

- **Undecidable with elementary functions.** Richardson (1968) showed that it is undecidable whether an expression built from polynomials, $\sin$, $\exp$ and $|\cdot|$ has a real zero. So the exact feasibility question for numeric CSPs with such functions has no algorithm.
- **Decidable for polynomials.** For polynomial constraints, feasibility is decidable by Tarski's quantifier elimination. The existential theory of the reals is in PSPACE (Canny 1988), and it is NP-hard, since a Boolean variable $b$ can be written as $b(b - 1) = 0$ and a clause as a polynomial equation. Problems that are equivalent to it form the class $\exists\mathbb{R}$.
- **Delta-decisions.** Gao, Avigad and Clarke (2012) showed that the relaxed question is decidable for bounded boxes and computable functions: either the constraints have no solution, or a version of them weakened by $\delta$ has one. A branch and prune solver answers this question.
- **Paving size.** Any outer paving with boxes of width $\varepsilon$ needs at least as many boxes as it takes to cover $\Sigma$, which is of order $\varepsilon^{-k}$ when $\Sigma$ has dimension $k$. For finitely many isolated, regular solutions, interval Newton steps make the boxes shrink quickly once they are small.

## Reductions

- **From SAT.** Each Boolean variable $b$ becomes a real variable with $b (1 - b) = 0$, and each clause $\ell_1 \vee \ell_2 \vee \ell_3$ becomes $(1 - \ell_1)(1 - \ell_2)(1 - \ell_3) = 0$ with $1 - b$ for a negated literal. So feasibility is NP-hard even for polynomials of degree 3.
- **To finite CSP.** Fixing a grid of values in each domain turns a numeric CSP into a finite [CSP](/constraint-satisfaction-problem/), but the grid can miss solutions, and equations almost never hold exactly on a grid. Interval methods avoid this.
- **Of global optimization.** Minimizing $f$ subject to the constraints reduces to a sequence of numeric CSPs with the extra constraint $f(x) \le t$ for a falling bound $t$.
- **Within SMT.** [Nonlinear real arithmetic](/nonlinear-real-arithmetic-satisfiability/) formulas are Boolean combinations of numeric constraints, and solvers such as dReal use branch and prune as their theory solver.

## Applications

- The kinematics of robots: the positions of a parallel robot for given leg lengths are the solutions of a polynomial system.
- Verified computation in geometry and in the design of mechanisms.
- Bounding the reachable states of hybrid systems and the parameters of models that fit measured data with known error bounds.
- Certified global optimization in chemical engineering and in control.

## References
