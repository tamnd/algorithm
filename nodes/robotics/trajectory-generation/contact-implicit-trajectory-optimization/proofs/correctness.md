---
title: The complementarity makes the optimized motion physical, its absence allows levitation, and the barrier continuation keeps every iterate strictly feasible
proves: [correctness]
status: full
---

We use the notation of the page and of the code. A unit mass at height $q \ge 0$ has thrust $u_k$, gravity $g > 0$ and ground force $\lambda_k$ in step $k$, with the time-stepping model

$$v_{k+1} = v_k + h(u_k - g + \lambda_k), \qquad q_{k+1} = q_k + h v_{k+1}, \qquad 0 \le q_{k+1} \perp \lambda_k \ge 0,$$

for $k = 0, \dots, N - 1$, where $a \perp b$ means $ab = 0$. The mass starts at rest on the ground, $q_0 = v_0 = 0$, and must end at rest at height $H > 0$. The energy is $E = \frac h2 \sum_k u_k^2$. The variables of the code are $x = (q_1, \dots, q_{N-2}, \lambda_0, \dots, \lambda_{N-1})$.

## Lemma 1: the elimination of the velocities is exact

**Claim.** For every $x$, put $q_{-1} = q_0 = 0$, $q_{N-1} = q_N = H$, $v_{k+1} = (q_{k+1} - q_k)/h$ and $u_k = (q_{k+1} - 2q_k + q_{k-1})/h^2 + g - \lambda_k$. Then the first two equations of the model hold for every $k$, the start is at rest on the ground, and the end is at rest at height $H$. Conversely, every motion of the model with these ends arises in this way from its heights and forces.

*Proof.* With $v_k = (q_k - q_{k-1})/h$ (which gives $v_0 = 0$), the formula for $u_k$ is $v_{k+1} = v_k + h(u_k - g + \lambda_k)$ solved for $u_k$, and $q_{k+1} = q_k + h v_{k+1}$ is the definition of $v_{k+1}$. The end has $q_N = H$ and $v_N = (q_N - q_{N-1})/h = 0$. Conversely, a motion of the model determines $v_k$ from the heights by the second equation and $u_k$ from the first. $\square$

So the problem is: minimize the convex quadratic $E(x)$ subject to $q_k \ge 0$, $\lambda_k \ge 0$ and $q_{k+1}\lambda_k = 0$.

## Lemma 2: a complementary solution is what the simulator does

**Claim.** Let $x$ satisfy $q_k \ge 0$, $\lambda_k \ge 0$ and $q_{k+1}\lambda_k = 0$ for all $k$. Then the forward simulation of the code, run with the thrust $u(x)$, produces exactly the heights $q_1, \dots, q_N$ and the forces $\lambda_0, \dots, \lambda_{N-1}$ of $x$.

*Proof.* In one step, with $q_k, v_k$ given, put $v^{\text{free}} = v_k + h(u_k - g)$ and $q^{\text{free}} = q_k + h v^{\text{free}}$. The model gives $q_{k+1} = q^{\text{free}} + h^2 \lambda_k$, so the step is the problem: find $\lambda \ge 0$ with $q^{\text{free}} + h^2\lambda \ge 0$ and $\lambda(q^{\text{free}} + h^2\lambda) = 0$. It has exactly one solution: $\lambda = 0$ if $q^{\text{free}} \ge 0$, because a positive $\lambda$ would need $q^{\text{free}} + h^2\lambda = 0$, which is impossible; and $\lambda = -q^{\text{free}}/h^2$ if $q^{\text{free}} < 0$, because $\lambda = 0$ would leave the height negative. This is the rule of the simulator. The pair $(q_{k+1}, \lambda_k)$ of $x$ solves the same problem, so it is that solution, and then $v_{k+1}$ agrees as well. Induction over $k$ from the common start $q_0 = v_0 = 0$ ends the proof. $\square$

So every feasible point of the problem with complementarity is a motion that a physics simulator would produce from its thrust: the ground pushes only while the mass touches it.

## Theorem 1: without the complementarity, the optimizer levitates

**Claim.** Drop the condition $q_{k+1}\lambda_k = 0$ and keep $q \ge 0$ and $\lambda \ge 0$. If $2H/(N(N-1)) \le g h^2$, the minimum energy is $0$, attained with $u \equiv 0$ and a positive ground force while the mass is in the air. With the complementarity, the minimum energy is positive.

*Proof.* Let $D = 2H/N$ and set the height differences $d_k = q_{k+1} - q_k = D(N - 1 - k)/(N - 1)$ for $k = 0, \dots, N - 1$, and $d_{-1} = 0$. They sum over $k = 0, \dots, N - 2$ to $D N/2 = H$, and $d_{N-1} = 0$, so the ends are right. The second differences are $d_0 - d_{-1} = D$ and $d_k - d_{k-1} = -D/(N - 1)$ for $k \ge 1$. Choose $\lambda_k = (d_k - d_{k-1})/h^2 + g$; then $u_k = 0$ for all $k$, and $\lambda_k \ge g - D/((N-1)h^2) \ge 0$ by the assumption. The heights are positive for $k \ge 1$, and the force is positive at the same steps when the assumption holds strictly, so this motion is not physical. Its energy is $0$, the least possible.

With the complementarity, suppose $E = 0$, so $u \equiv 0$. By Lemma 2 the motion is the simulation of $u \equiv 0$ from rest on the ground. In each step $q^{\text{free}} = -h^2 g < 0$, so $\lambda_k = g$ and the mass stays at $q = 0$, which contradicts $q_N = H > 0$. So every feasible point has positive energy. The minimum exists: by Theorem 2 below, the feasible set is a finite union of polyhedra, and a convex quadratic that is bounded below on a polyhedron attains its minimum there (the theorem of Frank and Wolfe). So the minimum is positive. $\square$

For the example of the page, $2H/(N(N-1)) = 1/90 \le 9.81 \cdot 0.01$, so the condition holds.

## Theorem 2: the problem is a union of convex pieces

**Claim.** For each set $S$ of steps, let $P_S$ be the convex quadratic program: minimize $E$ with $q_{k+1} = 0$ and $\lambda_k \ge 0$ for $k \in S$, and $q_{k+1} \ge 0$ and $\lambda_k = 0$ for $k \notin S$. The feasible set of the problem with complementarity is the union of the feasible sets of the $P_S$, so its global minimum is the smallest of their minima. A step $k$ with $q_{k+1}$ fixed at $H$ can only be outside $S$.

*Proof.* A point is feasible exactly when, for each $k$, $q_{k+1} = 0$ or $\lambda_k = 0$ (with both signs nonnegative); put $k$ in $S$ in the first case. Each $P_S$ has linear constraints and the convex objective $E$. $\square$

The test of the page uses this to find the global minimum by enumeration. The number of pieces grows as $2^{N-2}$, which is why the method of the page does not enumerate.

## Theorem 3: the barrier continuation

Write $\varphi(x) = E(x) - \mu\bigl(\sum_j \log x_j + \sum_k \log(\varepsilon - q_{k+1}\lambda_k)\bigr)$ on the open set $\Omega_\varepsilon$ where all $x_j > 0$ and all $q_{k+1}\lambda_k < \varepsilon$.

**Claim.** (a) Every Newton step of lines L4 to L8 keeps $x$ in $\Omega_\varepsilon$ and lowers $\varphi$, and the line search of line L7 ends. (b) Line L11 maps the result into $\Omega_{\varepsilon'}$ for the new $\varepsilon' = \varepsilon/\kappa$. (c) So the returned $x$ has $q > 0$, $\lambda > 0$ and $\max_k q_{k+1}\lambda_k < \varepsilon_{\text{final}} < \varepsilon_{\min}$.

*Proof.* (a) Line L5 makes $H + \tau I$ positive definite, so $d = -(H + \tau I)^{-1}\nabla\varphi$ has $\nabla\varphi^{\mathsf T} d = -d^{\mathsf T}(H + \tau I)d < 0$ whenever $\nabla\varphi \ne 0$; if the decrement $-\nabla\varphi^{\mathsf T} d/2$ is below the tolerance, line L8 stops before any step. $\Omega_\varepsilon$ is open and $\varphi$ is continuously differentiable on it, so for all small $s > 0$ the point $x + sd$ lies in $\Omega_\varepsilon$ and $\varphi(x + sd) \le \varphi(x) + 10^{-4}\, s\, \nabla\varphi^{\mathsf T} d$. Halving $s$ reaches such a value after finitely many steps. (Line L5 itself ends, because $H + \tau I$ is positive definite once $\tau$ exceeds the most negative eigenvalue of $H$.) (b) Each height $q_{k+1}$ and each force $\lambda_k$ belongs to exactly one product, so changing one pair does not change the others. Line L11 changes a pair only if its product is at least $\varepsilon'$, and it replaces one factor by $\varepsilon'/2$ divided by the other, which is positive; the new product is $\varepsilon'/2 < \varepsilon'$. Variables stay positive. (c) follows from (a) and (b) by induction over the stages, since the last stage ends with $\varepsilon < \varepsilon_{\min}$. $\blacksquare$

## What is not proved

The barrier problem is not convex, because the products $q_{k+1}\lambda_k$ are not convex functions, so Newton's method finds a local minimizer of each stage, and the path of the stages can end at a local solution of the original problem. The example of the page shows this: one start ends with the mass leaving the ground one step late, at a higher energy. Nothing here says that the limit of the stages is a minimizer, or even a stationary point in a strong sense; problems with complementarity constraints violate the usual constraint qualifications, which is why relaxations like this one are used. For $\varepsilon > 0$ the relaxed motion is not exactly physical; Lemma 2 applies only in the limit, and the test of the page measures the difference.
