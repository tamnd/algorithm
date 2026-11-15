---
tag: 3VWCBR
kind: algorithm
slug: cbf-safety-filter
name: Control barrier function quadratic program
aliases:
- CBF-QP
- safety filter
area: control/nonlinear-control
level: research
summary: Changes a nominal control as little as possible, by a quadratic program at each state, so that a control barrier function condition holds.
model: real-ram
complexity:
  vars: {m: the number of inputs}
  time: {worst: "O(m log m)"}
  space: {extra: "O(m)"}
properties: {deterministic: true, exact: true, recursive: false, online: true}
history:
  year: 2014
  people: [Aaron D. Ames, Jessy W. Grizzle, Paulo Tabuada, Xiangru Xu]
  note: "Ames, Grizzle and Tabuada (2014) proposed quadratic programs that combine a control barrier function constraint with a control Lyapunov function, for adaptive cruise control; Ames, Xu, Grizzle and Tabuada (2017) gave the theory in IEEE TAC."
prereqs: [control-barrier-function, quadratic-programming, kkt-conditions]
see_also: [barrier-certificate, control-lyapunov-function, sontag-universal-formula, positively-invariant-set, control-invariant-set, reference-governor, model-predictive-control, hamilton-jacobi-reachability]
sources:
  - paper: doi:10.1109/TAC.2016.2638961
    title: "Aaron D. Ames, Xiangru Xu, Jessy W. Grizzle and Paulo Tabuada, Control barrier function based quadratic programs for safety critical systems, IEEE Transactions on Automatic Control 62(8), 3861-3876, 2017"
    locator: zeroing control barrier functions, forward invariance of the safe set, and the quadratic program that combines CBF and CLF constraints
  - paper: doi:10.23919/ECC.2019.8796030
    title: "Aaron D. Ames, Samuel Coogan, Magnus Egerstedt, Gennaro Notomista, Koushil Sreenath and Paulo Tabuada, Control barrier functions: theory and applications, European Control Conference, 3420-3431, 2019"
    locator: survey of CBF based quadratic programs, with the explicit solution for one constraint and no input limits
  - paper: "Aaron D. Ames, Jessy W. Grizzle and Paulo Tabuada, Control barrier function based quadratic programs with application to adaptive cruise control, 53rd IEEE Conference on Decision and Control, 6271-6278, 2014"
    title: Control barrier function based quadratic programs with application to adaptive cruise control
    locator: the first CBF based quadratic program
  - paper: "Peter Wieland and Frank Allgöwer, Constructive safety using control barrier functions, IFAC Proceedings Volumes 40(12), 462-467, 2007"
    title: Constructive safety using control barrier functions
    locator: control barrier functions and a universal formula for safe feedback
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 3.4, the comparison principle (Lemma 3.4)
---

The control barrier function quadratic program (CBF-QP) takes the input $u_{\text{nom}}$ that a nominal controller wants and returns the closest input that satisfies the condition of a [control barrier function](/control-barrier-function/) $h$. For $\dot x = f(x) + g(x) u$ and the safe set $C = \{x : h(x) \ge 0\}$, the condition is $L_f h(x) + L_g h(x)\, u + \alpha(h(x)) \ge 0$, which is linear in $u$. So at each state the filter solves a small [quadratic program](/quadratic-programming/), and if the program is feasible along the way and the closed loop is Lipschitz, the state never leaves $C$. The nominal controller handles the task and the filter only acts near the boundary of $C$. A control barrier function is the function; this page is the controller built on it; a [barrier certificate](/barrier-certificate/) is the different object that proves safety of a system without an input.

## In plain words

A driver steers toward a goal. A guard sits next to the driver and watches one safety score, which is positive while the car is safe and zero at the edge of danger. Close to the edge, the score may only fall slowly, and the closer the car is to the edge, the slower it may fall. Each moment, the guard looks at what the driver wants and asks whether that keeps the score falling slowly enough. If yes, the guard does nothing. If no, the guard makes the smallest change to the driver's command that keeps the rule. The smallest change is easy to find because the rule is a straight line in the space of commands. When the command is limited, the guard may find no allowed command at all, and then the guard has no answer.

## The problem

**Input.** At the current state $x$: the nominal input $u_{\text{nom}} \in \mathbb{R}^m$, the row $a = L_g h(x) = \nabla h(x)^T g(x)$, the number $b = L_f h(x) + \alpha(h(x))$ with $L_f h = \nabla h^T f$, and optional limits $\ell_j \le u_j \le r_j$ (each bound may be absent). Here $h$ is continuously differentiable and $\alpha$ is an extended class K function: continuous, strictly increasing, with $\alpha(0) = 0$; the common choice is $\alpha(s) = \gamma s$ with $\gamma > 0$.

**Output.** The solution of

$$\min_u \ |u - u_{\text{nom}}|^2 \quad \text{subject to} \quad a \cdot u + b \ge 0, \quad \ell \le u \le r,$$

or a report that the constraints are infeasible. The feasible set is convex and the cost is strictly convex, so the solution is unique when it exists.

Used as feedback, $u = k(x)$ makes $\dot h \ge -\alpha(h)$ along the closed loop. With $f$, $g$ locally Lipschitz (see the [Lipschitz condition](/lipschitz-condition/)) and a locally Lipschitz $k$, the solutions are unique by the [Picard-Lindelöf theorem](/picard-lindelof-theorem/), and the comparison lemma gives $h(x(t)) \ge 0$ for all $t \ge 0$ when $h(x(0)) \ge 0$. So $C$ is forward invariant (a [positively invariant set](/positively-invariant-set/) of the closed loop).

## The algorithm

```pseudo id=main
CBF-QP(u_nom, a, b, ℓ, r)
L1  u ← clip(u_nom)
L2  if a·u + b ≥ 0 then return u
L3  if Σ_j max_{ℓ_j ≤ v ≤ r_j} a_j v + b < 0 then return INFEASIBLE
L4  Λ ← sorted values λ > 0 with u_nom,j + λ a_j ∈ {ℓ_j, r_j}
L5  binary search Λ for the piece [λ_-, λ_+] where ψ(λ_-) < 0 ≤ ψ(λ_+), ψ(λ) = a·clip(u_nom + λa) + b; λ ← root of ψ on that piece
L6  return clip(u_nom + λ a)
```

Line L1 respects the limits first, and line L2 returns that input if it already satisfies the barrier condition. This is the usual case far from the boundary, where the filter does nothing. Line L3 checks whether any allowed input can satisfy the condition. For a fixed multiplier $\lambda \ge 0$, the Lagrangian $|u - u_{\text{nom}}|^2 / 2 - \lambda (a \cdot u + b)$ is separable, and its minimizer over the box is $\operatorname{clip}(u_{\text{nom}} + \lambda a)$. The function $\psi$ is continuous, nondecreasing and linear between the points of line L4, where a coordinate reaches a bound. Line L5 finds the multiplier with $\psi(\lambda) = 0$, which makes the barrier constraint active, and line L6 returns the input. These are the [KKT conditions](/kkt-conditions/) of the program, and the proof checks optimality directly.

Without input limits, lines L4 and L5 reduce to one formula:

$$u = u_{\text{nom}} + \frac{\max\bigl(0, -(a \cdot u_{\text{nom}} + b)\bigr)}{|a|^2}\, a^T \qquad (a \neq 0).$$

The filter adds the smallest multiple of $a = L_g h$, the direction that increases $h$ fastest per unit of input.

## Example

A point robot in the plane has $\dot x = u$ with $x, u \in \mathbb{R}^2$. A round obstacle of radius 1 sits at $(2, 0)$, so $h(x) = (x_1 - 2)^2 + x_2^2 - 1$. Use $\alpha(s) = s$ and the nominal controller $u_{\text{nom}} = (4, 0) - x$, which drives the robot in a straight line to the goal $(4, 0)$ through the obstacle. Here $f = 0$ and $g = I$, so $a = \nabla h(x)^T = (2(x_1 - 2), 2 x_2)$ and $b = h(x)$.

At $x(0) = (0, 0.2)$: $h = 4 + 0.04 - 1 = 3.04$, $a = (-4, 0.4)$, $u_{\text{nom}} = (4, -0.2)$, and $a \cdot u_{\text{nom}} + b = -16 - 0.08 + 3.04 = -13.04 < 0$, so the filter acts. With no limits, $|a|^2 = 16.16$, $\lambda = 13.04 / 16.16 = 0.80693$ and $u = (4, -0.2) + 0.80693\, (-4, 0.4) = (0.77228, 0.12277)$. Check: $a \cdot u + b = -3.08911 + 0.04911 + 3.04 = 0$, so the constraint is active.

A 4th order Runge-Kutta simulation with step $0.01$ and the filter evaluated inside the right side gives:

| $t$ | $x_1$ | $x_2$ | $h$ | $u_1$ | $u_2$ | filter active |
|---|---|---|---|---|---|---|
| 0 | 0 | 0.2 | 3.04 | 0.77228 | 0.12277 | yes |
| 1 | 0.62007 | 0.46277 | 1.11835 | 0.56645 | 0.48076 | yes |
| 2 | 1.68245 | 1.14481 | 0.41142 | 1.90340 | 0.34827 | yes |
| 3 | 3.14916 | 0.57364 | 0.64965 | 0.85084 | -0.57364 | no |
| 4 | 3.68700 | 0.21103 | 1.89049 | 0.31300 | -0.21103 | no |
| 8 | 3.99427 | 0.00387 | 2.97712 | 0.00573 | -0.00387 | no |
| 12 | 3.99989 | 0.00007 | 2.99958 | 0.00011 | -0.00007 | no |

The smallest value of $h$ is $0.25003$, at $t = 2.52$, and the filter changes the input for the last time at $t = 2.47$ (measurements). After that, the nominal controller runs alone and the robot reaches the goal.

## Correctness

The full proof is in proofs/correctness.md. Its main steps:

- **Inner problem.** For $\lambda \ge 0$, $\operatorname{clip}(u_{\text{nom}} + \lambda a)$ minimizes the Lagrangian over the box, because the Lagrangian is a sum of one-dimensional quadratics.
- **Shape of psi.** Each term $a_j \operatorname{clip}_j(u_{\text{nom}, j} + \lambda a_j)$ is nondecreasing in $\lambda$, whatever the sign of $a_j$, and it is linear between the points where the coordinate meets a bound. So the binary search of line L5 is valid, and the root on one linear piece is found exactly.
- **Optimality.** If $\lambda \ge 0$, $u(\lambda)$ is feasible and $\lambda \psi(\lambda) = 0$, then for every feasible $v$, $\frac12 |v - u_{\text{nom}}|^2 \ge L(v, \lambda) \ge L(u(\lambda), \lambda) = \frac12 |u(\lambda) - u_{\text{nom}}|^2$. Strict convexity gives uniqueness.
- **Infeasibility.** Line L3 computes the supremum of $a \cdot u$ over the box, which decides feasibility. If the supremum is infinite, the last piece of $\psi$ has a positive slope, so a root exists.
- **Safety.** Along the closed loop, $\dot h = a \cdot k(x) + b - \alpha(h) \ge -\alpha(h)$. By the comparison lemma (Khalil 2002, Section 3.4), $h(x(t))$ stays above the solution of $\dot y = -\alpha(y)$, $y(0) = h(x(0)) \ge 0$, which never becomes negative. For $\alpha(s) = \gamma s$, $\frac{d}{dt}(e^{\gamma t} h) \ge 0$ gives $h(x(t)) \ge e^{-\gamma t} h(x(0))$.

The tests compare the algorithm in exact Fraction arithmetic with a brute force solver that tries every active set, on 600 random instances with $m = 1$ to $4$, random boxes with missing bounds and some $a_j = 0$, and check the KKT conditions. They also check the closed form without limits, that integer data give exact fractions, the infeasible example below, the closed loop $\dot x = u$, $h = 1 - x$, $u_{\text{nom}} = 1$ against $x(t) = 1 - e^{-t}$ within $10^{-8}$, the obstacle run above ($h \ge 0.25$ throughout and arrival at the goal), and the sampled-data failure in the pitfalls.

## Complexity

With $m$ inputs, lines L1 to L3 take $O(m)$ time. Line L4 sorts at most $2m$ breakpoints in $O(m \log m)$. The binary search of line L5 evaluates $\psi$ at $O(\log m)$ points, $O(m)$ each. In total $O(m \log m)$ time and $O(m)$ extra space. Without limits it is $O(m)$. Forming $a$ and $b$ costs one gradient of $h$ and one evaluation of $f$ and $g$, which usually dominates. With several barrier constraints, or with a Lyapunov constraint added, the program is a general convex QP and needs a QP solver.

## Properties

- **Minimally invasive.** When $\operatorname{clip}(u_{\text{nom}})$ satisfies the condition, the filter returns it unchanged. Far from the boundary of $C$ the nominal controller acts alone.
- **Pointwise.** The program uses only the current state. It does not predict, so it cannot plan around a future conflict; the condition limits only how fast $h$ may fall.
- **Unique.** The solution is unique when the program is feasible.
- **Lipschitz in the simple case.** Without limits and with $L_g h \neq 0$, the closed form is locally Lipschitz when $u_{\text{nom}}$, $f$, $g$ and $\nabla h$ are, so the closed loop has unique solutions and the safety theorem applies.
- **Exact.** With rational data, every step is a field operation, and the result is exact.

## Variants and improvements

- **CLF-CBF QP.** Add a [control Lyapunov function](/control-lyapunov-function/) constraint $\dot V \le -c V + \delta$ with a penalized slack $\delta$, so that stability gives way to safety when they conflict (Ames, Xu, Grizzle and Tabuada 2017).
- **Several barriers.** Each barrier adds one linear constraint. The program is then a general QP, and the constraints can be jointly infeasible even when each one alone is feasible.
- **High order barriers.** When $L_g h = 0$, the input does not appear in $\dot h$. Exponential or high order CBFs put the condition on a higher derivative of $h$ (see the [control barrier function](/control-barrier-function/) page).
- **Sampled data and robustness.** Margins added to $b$, or conditions that bound $h$ over the whole sampling interval, keep safety for held inputs and model errors.
- **Closed form without optimization.** For one constraint, a smooth formula in the style of [Sontag's universal formula](/sontag-universal-formula/) also gives a safe feedback (Wieland and Allgöwer 2007).
- **Predictive filters.** A [reference governor](/reference-governor/) or a predictive filter based on [model predictive control](/model-predictive-control/) looks ahead and can handle input limits that the pointwise program cannot.

## When to use it

Use it when a nominal controller already does the task, perhaps a learned or hand-tuned one, and you need a guarantee that the state stays in a set described by one or a few smooth inequalities. It suits robots that avoid obstacles, vehicles that keep a distance, and systems with state limits. It needs a function $h$ that really is a control barrier function with the input limits you have; without that, the program can become infeasible. When the input limits are tight or the safe set is complex, use a method that computes a [control invariant set](/control-invariant-set/) directly, such as [Hamilton-Jacobi reachability](/hamilton-jacobi-reachability/), or a predictive method.

## Pitfalls

- **Held inputs at line L6.** The safety theorem assumes the input is updated continuously. For $\dot x = u$, $h = 1 - x$, $u_{\text{nom}} = 1$ and $\alpha(s) = \gamma s$, holding the input for time $T$ gives $1 - x_{k+1} = (1 - \gamma T)(1 - x_k)$ near the boundary (a calculation for this example). With $\gamma = 10$ and $T = 0.15$ the factor is $-0.5$, and the simulation reaches $h = -0.05$, an unsafe state (measurement). With $T = 0.05$, or with $\gamma = 1$ and $T = 0.15$, $h$ stays nonnegative (measurement). Here $\gamma T < 1$ is the condition; in general, add a margin.
- **Infeasible program at line L3.** For $\dot x = x + u$ with $|u| \le 1$, $h = 2 - x$ and $\alpha(s) = s$, the condition is $-u + 2 - 2x \ge 0$, which some $|u| \le 1$ satisfies only when $x \le 1.5$. For $1.5 < x \le 2$ the state is safe but no allowed input keeps the condition, so $h$ is not a control barrier function with these limits. Choose $h$ so that the condition is feasible with the real limits, for example $h = 0.5 - x$ here.
- **Undesired equilibria at line L6.** When $u_{\text{nom}}$ points straight into the obstacle, the filter can cancel it exactly. In the example, from $x(0) = (0, 0)$ the robot moves along the axis and stops in front of the obstacle: at $t = 12$ it is at $(0.99999, 0)$ with $h = 0.00002$ (measurement). The filter keeps safety but not the task.
- **The choice of alpha at line L2.** A large $\gamma$ lets the state come close to the boundary, and a small $\gamma$ makes the filter act early. In the example, $\gamma = 0.2$, $1$ and $5$ give smallest values of $h$ of about $1.495$, $0.250$ and $0.0002$, and arrival within $0.1$ of the goal at $t = 6.11$, $5.33$ and $4.79$ (measurements).
- **Zero gradient at line L5.** If $L_g h(x) = 0$, the input does not affect $\dot h$, and the program is feasible only if $b \ge 0$. A position limit on a system with force input has this problem. Use a high order barrier.
- **Floating point at line L2.** With floats, $a \cdot u + b$ can be $-10^{-16}$ for an input that is safe in exact arithmetic, and the solver then makes a tiny change. This is harmless, but tests that compare inputs must allow a tolerance.

## Implementations

## History

Barrier functions for control systems with inputs appear in Wieland and Allgöwer (2007), who called them control barrier functions and gave a universal formula for a safe feedback. Ames, Grizzle and Tabuada (2014) put a barrier condition and a control Lyapunov function condition into one quadratic program, for adaptive cruise control. Ames, Xu, Grizzle and Tabuada (2017) gave the theory, with reciprocal and zeroing control barrier functions, forward invariance and conditions for a Lipschitz solution. The survey of Ames and others (2019) collected the extensions to high relative degree, several constraints and applications in robotics.

## References
