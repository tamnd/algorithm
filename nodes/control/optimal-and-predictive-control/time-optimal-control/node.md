---
tag: PDVQFZ
kind: problem
slug: time-optimal-control
name: Time-optimal control
aliases:
- minimum-time control
area: control/optimal-and-predictive-control
level: core
summary: Bring the state to a target in the least time with a bounded input.
prereqs: [optimal-control-problem, controllability]
see_also: [bang-bang-control, pontryagin-maximum-principle, singular-arc, hamilton-jacobi-bellman-equation, minimum-energy-control, reachable-set-computation, transversality-conditions, model-predictive-control]
sources:
  - book: isbn:9780691151878
    title: Daniel Liberzon, Calculus of Variations and Optimal Control Theory, A Concise Introduction, Princeton University Press, 2012
    locator: Section 4.4 (time-optimal control problems, with 4.4.1 on the double integrator and 4.4.2 on the bang-bang principle for linear systems) and Section 4.5 (existence of optimal controls)
  - url: https://math.berkeley.edu/~evans/control.course.pdf
    title: Lawrence C. Evans, An Introduction to Mathematical Optimal Control Theory, lecture notes, University of California, Berkeley
    locator: Chapter 2 (controllability and the bang-bang principle) and Chapter 3 (linear time-optimal control)
  - book: isbn:9780123426505
    title: Henry Hermes and Joseph P. LaSalle, Functional Analysis and Time Optimal Control, Academic Press, 1969
    locator: Part II (linear time optimal control)
  - book: isbn:9780486434841
    title: Donald E. Kirk, Optimal Control Theory, An Introduction, Prentice-Hall, 1970 (Dover reprint, 2004)
    locator: Section 5.4 (minimum-time problems)
  - paper: "Donald W. Bushaw, Differential equations with a discontinuous forcing term, PhD thesis, Princeton University, 1952; published as Experimental Towing Tank Report 469, Stevens Institute of Technology, 1953"
---

The time-optimal control problem asks for a bounded input that brings the state of a system from a given start to a target, usually the origin, in the shortest possible time. It is the [optimal control problem](/optimal-control-problem/) with a free final time and the running cost $L = 1$. For linear systems with a box of inputs, the answer takes only the extreme values of the box and switches between them at a few times ([bang-bang principle](/bang-bang-control/)). The double integrator, with its parabolic switching curve, is the standard example.

## In plain words

You must move a cart to a stop at a marked spot as fast as you can, and the motor can push with at most a fixed force either way. Common sense says: push fully toward the spot, then at the right moment push fully the other way to brake, and arrive with zero speed exactly at the spot. That is the answer. The only question is when to switch, and the answer depends on where the cart is and how fast it moves. For many systems the best plan always uses full force, and the art is to find the switching times. Some systems cannot reach the target at all with limited force, and then there is no answer.

## Definition

**Input.** A system $\dot x = f(x, u)$ with $x \in \mathbb{R}^n$, $f$ continuous and $C^1$ in $x$; a compact input set $U \subset \mathbb{R}^m$; an initial state $x_0$; and a closed target set $S$, often $S = \{0\}$. In the linear case, $\dot x = A x + B u$ with $U = [-1, 1]^m$, so each input component satisfies $|u_i(t)| \le 1$.

**Question.** Among the measurable inputs $u : [0, t_f] \to U$ whose trajectory from $x_0$ reaches $S$ at the time $t_f$, find one with the smallest $t_f$. The answer is the minimum time $T^*(x_0)$ and an input that attains it. If no admissible input reaches $S$, $T^*(x_0) = +\infty$.

**What is known for the linear case** ($S = \{0\}$, $U = [-1, 1]^m$):

- **Reachability.** The set of states that can be steered to 0 is all of $\mathbb{R}^n$ if and only if $(A, B)$ is [controllable](/controllability/) and no eigenvalue of $A$ has a positive real part (Evans, Chapter 2). With a bounded input, an exponentially growing mode can only be cancelled from a bounded region.
- **Existence.** If $x_0$ can be steered to 0 in some time, then a time-optimal input exists. The reason is that the set of states reachable at time $t$ is convex and compact and depends continuously on $t$ (Liberzon, Section 4.5; Hermes and LaSalle, Part II).
- **Structure.** Under normality, meaning that $(A, b_i)$ is controllable for each column $b_i$ of $B$, the time-optimal input is unique, bang-bang, and has finitely many switches. With all eigenvalues of $A$ real and $m = 1$, it has at most $n - 1$ switches ([bang-bang principle](/bang-bang-control/)).

## Variants

- **A general target.** A target set $S$ instead of a point, for example a ball around 0. The [transversality conditions](/transversality-conditions/) then apply at the end point.
- **Nonlinear systems.** Time-optimal controls may contain [singular arcs](/singular-arc/), where the input takes values inside $U$, and they may chatter.
- **Discrete time.** For $x_{k+1} = A x_k + B u_k$ with $|u_{k,i}| \le 1$, find the smallest number of steps $N$ that brings $x_0$ to 0. For each $N$ this is a linear feasibility problem.
- **Minimum time with a penalty.** Costs $t_f + \int (\text{fuel})\, dt$ mix time with fuel use. A pure minimum-fuel problem gives inputs with values $-1$, $0$ and $1$.
- **Minimum-time feedback.** The synthesis problem asks for the optimal input as a function of the state, $u = \kappa(x)$, valid for all starts. For the double integrator it is a switching curve.

## Examples

**The double integrator.** Let $\dot x_1 = x_2$, $\dot x_2 = u$, $|u| \le 1$, target $0$. This is a mass with a bounded force, with position $x_1$ and velocity $x_2$. With $u = +1$ the quantity $x_1 - x_2^2/2$ is constant, and with $u = -1$ the quantity $x_1 + x_2^2/2$ is constant, so the trajectories are parabolas. The only trajectories that reach 0 without a switch are the two half parabolas that end at 0, which together form the **switching curve**

$$x_1 = -\frac{x_2 |x_2|}{2}.$$

The optimal feedback is $u = -1$ above the curve (where $x_1 + x_2|x_2|/2 > 0$), $u = +1$ below it, and $u = -\operatorname{sgn}(x_2)$ on it. Each optimal input has at most one switch, which agrees with the bound $n - 1 = 1$, since both eigenvalues of $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$ are 0.

From $x_0 = (1, 0)$: use $u = -1$. Then $x_2 = -t$ and $x_1 = 1 - t^2/2$, which reaches the curve at $t = 1$ in the state $(1/2, -1)$. Switch to $u = +1$ for 1 more second: $x_2 = -1 + s$ and $x_1 = 1/2 - s + s^2/2$, which is $(0, 0)$ at $s = 1$. The minimum time is 2. In general, above the curve,

$$T^*(x) = x_2 + 2\sqrt{x_1 + x_2^2/2},$$

and below it $T^*(x) = -x_2 + 2\sqrt{-x_1 + x_2^2/2}$. For $(0, 1)$ this gives $1 + \sqrt 2 \approx 2.4142$. The function $T^*$ is continuous but not differentiable on the switching curve, which is why the [HJB equation](/hamilton-jacobi-bellman-equation/) needs viscosity solutions here.

**The harmonic oscillator.** Let $\dot x_1 = x_2$, $\dot x_2 = -x_1 + u$, $|u| \le 1$. The eigenvalues $\pm i$ are not real. The switching function is $\lambda_2(t)$, and the costate equation makes it a sine wave $\rho \sin(t + \phi)$, so the optimal input switches every $\pi$ seconds. From far away, many half periods are needed, so the number of switches grows without bound with the distance of $x_0$ from 0. The bound $n - 1$ needs real eigenvalues.

**An unreachable state.** For $\dot x = x + u$, $|u| \le 1$, the state can reach 0 only from $|x_0| < 1$: at $x_0 = 1$ the best input $u = -1$ gives $\dot x = 0$. So $T^*(x_0) = +\infty$ for $|x_0| \ge 1$, even though the system is controllable. For $|x_0| < 1$, the input $u = -\operatorname{sgn}(x_0)$ gives $T^*(x_0) = -\ln(1 - |x_0|)$.

## Known algorithms

- **The maximum principle with a switching function.** For the linear case, $H = \lambda_0 + \lambda^T (A x + B u)$, the costate is $\lambda(t) = e^{-A^T t} \lambda(0)$, and $u_i(t) = -\operatorname{sgn}(b_i^T \lambda(t))$. The unknowns are the $n$ components of $\lambda(0)$ (up to scaling) and $t_f$, found by shooting ([indirect method](/indirect-method-optimal-control/)).
- **Switching-time optimization.** Fix the number and order of the switches and optimize over the switching times with a nonlinear equation solver or a gradient method. For the double integrator two unknowns (the switch time and $t_f$) are enough.
- **Reachable sets.** For linear systems, $x_0$ can be steered to 0 at time $t$ if and only if $-x_0$ lies in the convex compact set $\mathcal{R}(t) = \{\int_0^t e^{-A s} B u(s)\, ds\}$, whose support function is $h_t(\eta) = \int_0^t \|B^T e^{-A^T s} \eta\|_1\, ds$. So $T^*(x_0)$ is the smallest $t$ with $-\eta^T x_0 \le h_t(\eta)$ for all $\eta$, and iterative methods search over $\eta$ and $t$. See [reachable set computation](/reachable-set-computation/).
- **Linear programming in discrete time.** For a given $N$, steering $x_0$ to 0 in $N$ steps is a feasibility problem with $N m$ variables, $n$ equality constraints and $2 N m$ bounds. Bisection over $N$, or one LP per $N$, gives the minimum number of steps.
- **Dynamic programming.** The minimum time solves a stationary [HJB equation](/hamilton-jacobi-bellman-equation/), which can be solved on a grid in low dimension.

## Bounds

- For a single-input linear system with all eigenvalues real, at most $n - 1$ switches (Feldbaum 1953; see the [bang-bang principle](/bang-bang-control/) for the proof). With complex eigenvalues there is no bound independent of $x_0$.
- The minimum time $T^*(x)$ of a controllable linear system with eigenvalues in the closed left half plane is finite on $\mathbb{R}^n$ (Evans, Chapter 2), and because 0 is an interior point of $U$ it is also continuous. It is not differentiable in general.
- The discrete-time test for a given $N$ is a linear program with $N m$ variables. With rational data it can be solved in time polynomial in the bit size of the data by interior point methods; no strongly polynomial algorithm for linear programming is known. The minimum number of steps $N^*$ costs $O(\log N^*)$ such programs by doubling and bisection.

## Reductions

- **To the general problem.** The cost $t_f$ is the Lagrange cost $\int_0^{t_f} 1\, dt$ or the Mayer cost $K = t_f$. With a free final time, the [transversality condition](/transversality-conditions/) gives $H \equiv 0$, that is, $\lambda_0 + \lambda^T f(x^*, u^*) = 0$ along the extremal.
- **To a fixed final time.** Time scaling $t = t_f s$ with $s \in [0, 1]$ makes $t_f$ a parameter of the dynamics, $dx/ds = t_f f(x, u)$.
- **Minimum time and reachability are dual.** The minimum time to the target is the first time at which $x_0$ enters the backward reachable set of the target. Algorithms for one solve the other.
- **To minimum energy.** Without input bounds, the minimum time is zero for a controllable linear system, and the natural question becomes the least energy for a fixed time ([minimum-energy control](/minimum-energy-control/)).

## Applications

- Positioning servos, such as the head of a disk drive or a gantry crane, where bang-bang motion with a braking switch is the time-optimal move.
- Attitude slews of spacecraft with bounded torque.
- Minimum-time trajectories of robot arms along a given path.
- Early analog controllers for the double integrator and for relay systems, where Bushaw (1952) and Feldbaum (1953) studied switching rules.

## References
