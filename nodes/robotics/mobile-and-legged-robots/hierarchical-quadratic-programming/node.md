---
tag: 7BEBTS
kind: algorithm
slug: hierarchical-quadratic-programming
name: Hierarchical quadratic programming
aliases:
- HQP
- lexicographic quadratic programming
area: robotics/mobile-and-legged-robots
level: research
summary: "Solves a stack of equality and inequality tasks in strict priority, each optimized without degrading the higher ones."
model: real-ram
complexity:
  vars: {n: "the number of variables", m: "the number of task rows over all levels", i: "the total number of active-set iterations over all levels"}
  time: {worst: O(i (n + m)^3)}
  space: {extra: O((n + m)^2)}
properties: {deterministic: true, randomized: false, online: true, exact: true}
history:
  year: 2011
  people: [Oussama Kanoun, Florent Lamiraux, Pierre-Brice Wieber, Adrien Escande, Nicolas Mansard]
  note: "Kanoun, Lamiraux and Wieber put inequality tasks at any priority level with a cascade of QPs in 2011; Escande, Mansard and Wieber gave a dedicated solver for the whole hierarchy in 2014."
prereqs: [quadratic-programming, lexicographic-optimization, null-space-projection]
see_also: [task-priority-inverse-kinematics, whole-body-control, convex-mpc-legged-locomotion, kkt-conditions, least-squares-problem, jacobian-pseudoinverse-method, operational-space-formulation, goal-programming]
sources:
  - paper: doi:10.1109/TRO.2011.2142450
    title: "Kinematic control of redundant manipulators: generalizing the task-priority framework to inequality task"
    locator: "the whole paper (one QP per priority level, with slack variables, and the higher levels fixed at their optimal slacks)"
  - paper: doi:10.1177/0278364914521306
    title: "Hierarchical quadratic programming: fast online humanoid-robot motion generation"
    locator: the whole paper (the hierarchical active-set solver and the speed comparison with the cascade of QPs)
  - book: isbn:9780387303031
    title: Numerical Optimization (second edition)
    locator: Chapter 16 (the active-set method for convex quadratic programs)
  - paper: doi:10.1142/S0219843605000594
    title: Synthesis of whole-body behaviors through hierarchical control of behavioral primitives
    locator: "the whole paper (task priorities for a humanoid robot, with equality tasks in null spaces)"
---

Hierarchical quadratic programming (HQP) finds the joint velocities, accelerations or torques of a robot that meet a stack of tasks in strict priority. Each level of the stack is a set of linear equalities $A_kx = b_k$ and linear inequalities $C_kx \le d_k$, such as "keep the center of mass over the feet", "keep each joint inside its limits" or "move the hand to the target". The solver minimizes the error of the first level, then the error of the second level among the points that keep the first error optimal, and so on. It is [lexicographic optimization](/lexicographic-optimization/) where every objective is a least-squares error, so every step is a [quadratic program](/quadratic-programming/). With equalities only, it gives the same answer as the classic [task-priority method](/task-priority-inverse-kinematics/) with [null-space projections](/null-space-projection/); its gain is that inequalities can sit at any level. HQP is the solver inside much of [whole-body control](/whole-body-control/) for humanoid and legged robots, and it applies in the same way to a fixed arm with redundant joints.

## In plain words

A robot often has more wishes than it can meet at once: do not fall, do not hit the joint stops, reach the cup, keep the head level. Some wishes matter more than others. A weighted sum lets a minor wish pull a little on a major one. A strict order does not.

HQP handles the wishes in order. It meets the first group as well as it can. Then it looks at all the ways to do that equally well, and among them it picks the ones that meet the second group best. It goes on down the list. A wish that cannot be met is met as closely as possible, and the rest of the list still gets the freedom that is left.

## The problem

**Input.** The number of variables $n$, and $p$ levels. Level $k$ has a matrix $A_k$ and a vector $b_k$ (equality tasks), and a matrix $C_k$ and a vector $d_k$ (inequality tasks). Any of them may be empty. Arithmetic and square roots cost one step each, as in the [real RAM](/real-ram/).

**Output.** A vector $x$ such that, for each $k$ in order, the error
$$f_k(x) = \tfrac12\|A_kx - b_k\|^2 + \tfrac12\|\max(0, C_kx - d_k)\|^2$$
is the least possible among the points that keep $f_1, \dots, f_{k-1}$ at their optimal values. The maximum is taken in each component. The optimal residuals $w_k = A_kx - b_k$ and violations $v_k = \max(0, C_kx - d_k)$ are the same for every optimal $x$ (Lemma 2 of the proof), so the output also reports them.

**How it differs from close pages.** The [task-priority method](/task-priority-inverse-kinematics/) and the [pseudoinverse method](/jacobian-pseudoinverse-method/) handle equalities only, in closed form. A weighted [QP](/quadratic-programming/) sums the levels with weights, which is one QP but gives only a soft priority. [Goal programming](/goal-programming/) also has priority levels but is usually linear. [Convex MPC for legged robots](/convex-mpc-legged-locomotion/) is one weighted QP over a horizon, and whole-body control often runs HQP or a weighted QP at each control step.

## The algorithm

The cascade of Kanoun, Lamiraux and Wieber solves one QP per level. After a level is solved, its optimal residuals become hard constraints for the lower levels.

```pseudo id=main
HQP((A_k, b_k, C_k, d_k) for k = 1..p)
L1  x ← 0;  E ← no rows (hard equalities);  G ← no rows (hard inequalities);  Z ← I
L2  for k ← 1 to p
L3      (y, v) ← argmin ½|A_k(x + Zy) - b_k|² + ½|v|² + ½ε|y|²  s.t.  G(x + Zy) ≤ g,  C_k(x + Zy) - d_k ≤ v
L4      x ← x + Zy;  w_k ← A_k x - b_k;  v_k ← max(0, C_k x - d_k)
L5      add the rows A_k x = b_k + w_k to E, and each violated row C_k,i x = d_k,i + v_k,i to E
L6      add each other row C_k,i x ≤ d_k,i to G
L7      Z ← an orthonormal basis of the null space of E
L8  return x and (w_k, v_k) for k = 1..p
```

Line L3 is a QP in the slack form of Kanoun et al.: the slack $v$ measures how much each inequality is violated, and its square is in the objective. The current $x$ satisfies $E$, so every point $x + Zy$ satisfies $E$ too, and the equalities drop out. The start $y = 0$, $v = \max(0, C_kx - d_k)$ is feasible, and the code solves the QP with the primal active-set method (Nocedal and Wright, Chapter 16), keeping each step in least-squares form and solving it by modified [Gram-Schmidt](/gram-schmidt-process/). The damping $\varepsilon$ (here $10^{-9}$) makes the QP strictly convex; the code also uses it to pick, among equal optima, the one closest to the previous $x$. Line L5 turns a violated row into an equality, because every optimal point violates it by the same amount (Lemma 2 of the proof). In code, a violation below $10^{-6}(1 + |d_{k,i}|)$ counts as no violation, since the damping alone can cause one, and the row then stays an inequality with its bound moved by that tiny amount. Line L7 uses Gram-Schmidt and drops rows of $E$ that depend on the others; they are consistent, because $x$ satisfies them all.

## Example

Take $x = (x_1, x_2)$ and three levels: a joint limit $x_1 \le 1$; a task $x_1 + x_2 = 3$; a rest posture $x_1 = 0$, $x_2 = 0$.

Level 1: $x = 0$ meets the limit, so $v_1 = 0$, and the row becomes a hard inequality. Level 2: the task can be met exactly without passing the limit, so $w_2 = 0$ and the line $x_1 + x_2 = 3$ becomes a hard equality, with $Z = (1, -1)/\sqrt2$. Level 3: on that line, the point closest to the origin is $(1.5, 1.5)$, but it breaks the limit. The best point on the line with $x_1 \le 1$ is $(1, 2)$, with posture error $w_3 = (1, 2)$. So $x = (1, 2)$: the limit holds, the task holds, and the posture gives way.

A weighted QP does not keep the order. Measured, with the inequality written as a squared violation and the same damping:

| Weights (limit, task, posture) | $x$ | Limit violation | Task error |
|---|---|---|---|
| 1, 1, 1 | (1.000, 1.000) | 0 | 1.000 |
| 100, 10, 1 | (1.008, 1.811) | 0.008 | 0.181 |
| 10000, 100, 1 | (1.0001, 1.980) | 0.0001 | 0.020 |
| HQP | (1, 2) | 0 | 0 |

The weighted answer approaches the HQP answer as the ratios of the weights grow, but it never reaches it, and large ratios make the QP badly conditioned.

## Correctness

The [proof](proofs/correctness/) shows, in exact arithmetic with $\varepsilon = 0$ and an exact QP solver, that the cascade returns a lexicographic optimum. Lemma 1: the slack QP of line L3 has the same optimal value as the minimum of $f_k$ over the set left by the higher levels. Lemma 2: all optimal points of a level have the same residual $w_k$, violate the same rows by the same amounts $v_k$, and satisfy the other rows; so the set kept by lines L5 to L7 is exactly the optimal set of the level. The theorem follows by induction over the levels. With $\varepsilon > 0$, each level loses at most $\tfrac12\varepsilon\|y^*\|^2$, where $y^*$ is an undamped optimum. The active-set method stops after finitely many steps on a strictly convex QP when no step cycles. The tests compare the code with brute force over the active rows on random stacks, with the level-by-level null-space solution on stacks of equalities, and with hand cases.

## Complexity

- **Time.** Each active-set iteration of level $k$ has at most $n + m$ variables (the step $y$ and the slacks) and at most $m$ constraints; the code computes a null-space basis of the working set and a least-squares step by Gram-Schmidt, in $O((n + m)^3)$ time. The number of iterations is finite but has no useful polynomial bound in general; with a good start it is small. Measured: 4 levels of 6 equalities and 6 inequalities each, on 30 variables, take about 1.8 s in this pure Python code. Escande, Mansard and Wieber report that their dedicated solver handles a hierarchy of equalities about 10 times faster than the classic method, and inequality hierarchies at the control rates of humanoid robots.
- **Space.** $O((n + m)^2)$ for the matrices of one level QP.

## Properties

- **Strict priority.** A lower level never changes the optimal residual of a higher level (the test `test_lower_levels_never_degrade_higher_levels` checks this on random stacks).
- **Feasibility is not required.** An infeasible level is solved in the least-squares sense, and the lower levels still run.
- **Equalities match the null-space method.** With no inequalities, the result is the task-priority solution with pseudoinverses of the projected tasks.
- **Continuity is not guaranteed.** When a row of an inequality becomes active or inactive, the solution can change direction suddenly; damping and smooth task gains reduce this.
- **Exact up to the damping.** The result is a lexicographic optimum up to $O(\varepsilon)$, not an approximation by weights.

## Variants and improvements

- **Dedicated hierarchical solvers.** Escande, Mansard and Wieber solve all levels in one active-set loop with a complete orthogonal decomposition shared by the levels, instead of one separate QP per level.
- **Weighted QP.** One QP with large weight ratios. It is simpler and is used in many controllers for legged robots, at the price of a soft priority.
- **Damped levels.** Adding $\varepsilon\|x\|^2$ at each level, or a final level $x = 0$, picks a unique answer and limits large motions near singular tasks, as in [damped least squares](/damped-least-squares-inverse-kinematics/).
- **Warm start.** At a control rate of 1 kHz, the active set of the last step is a good first guess and usually needs few changes.
- **Dynamics levels.** In [whole-body control](/whole-body-control/), the first level holds the equations of motion and the contact constraints, so the solution is physically consistent before any task is considered.

## When to use it

Use HQP when a redundant robot has tasks with a clear order of importance and some of them are inequalities: joint limits, friction cones, collision distances, balance limits. For a few equality tasks, the closed-form task-priority method is faster and simpler. When the order is not strict, or a solver for one QP is already in place, a weighted QP is often enough.

## Pitfalls

- **Singular tasks.** Near a singular configuration of a task, the step in its null space can be large. Damp it, or put a regularization level at the bottom.
- **Thresholds.** The test for a violated row needs a tolerance. A tiny violation caused by roundoff, made into an equality, removes freedom that the lower levels need.
- **Feasible start.** Each level QP needs a feasible start. The previous $x$ with $v = \max(0, Cx - d)$ is one; a start that breaks a hard row of a higher level is not.
- **Too many levels.** Each level costs a QP. Group tasks of the same importance into one level instead of giving each its own.
- **Inconsistent units.** Tasks in meters and radians on the same level are weighted by their units. Scale them before you put them together.

## Implementations

## History

Task priorities for redundant robots go back to Nakamura, Hanafusa and Yoshikawa in 1987 and to Siciliano and Slotine in 1991, who solved each task in the null space of the higher ones with pseudoinverses. Sentis and Khatib built whole-body behaviors for humanoid robots on prioritized tasks in 2005. Inequalities did not fit this scheme: they were handled by weights or by switching. Kanoun, Lamiraux and Wieber showed in 2011 that a cascade of QPs, one per level with the higher levels fixed at their optimal slacks, puts an inequality at any priority level. Escande, Mansard and Wieber gave a solver for the whole hierarchy in 2014, fast enough for the control loop of a humanoid robot.

## References
