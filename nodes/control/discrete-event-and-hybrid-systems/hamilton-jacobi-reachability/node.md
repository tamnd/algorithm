---
tag: CFEBTN
kind: algorithm
slug: hamilton-jacobi-reachability
name: Hamilton-Jacobi reachability
aliases:
- HJ reachability
- level set reachability
area: control/discrete-event-and-hybrid-systems
level: research
summary: Computes backward reachable sets of nonlinear systems with inputs and disturbances as the sublevel set of the viscosity solution of an HJ PDE.
model: real-ram
complexity:
  vars: {n: the state dimension, k: the number of grid nodes per axis, K: the number of time steps}
  time: {worst: O(K n k^n)}
  space: {extra: O(k^n)}
properties: {deterministic: true, exact: false, online: false}
history:
  year: 2005
  people: [Ian M. Mitchell, Alexandre M. Bayen, Claire J. Tomlin]
  note: "Mitchell, Bayen and Tomlin showed in 2005 that the backward reachable set of a dynamic game is the zero sublevel set of the viscosity solution of a time-dependent HJ equation, and computed it with level set methods."
prereqs: [reachable-set-computation, hamilton-jacobi-bellman-equation, level-set-method]
see_also: [reachable-set-computation, zonotope-reachability, hamilton-jacobi-bellman-equation, lax-friedrichs-scheme, level-set-method, curse-of-dimensionality, control-invariant-set, zero-sum-game]
sources:
  - paper: doi:10.1109/TAC.2005.851439
    title: "I. M. Mitchell, A. M. Bayen and C. J. Tomlin, A time-dependent Hamilton-Jacobi formulation of reachable sets for continuous dynamic games, IEEE Transactions on Automatic Control 50(7), 2005, pages 947 to 957"
    locator: the theorem that the zero sublevel set of the viscosity solution is the backward reachable set, and the numerical method
  - paper: doi:10.1016/j.automatica.2004.01.012
    title: "J. Lygeros, On reachability and minimum cost optimal control, Automatica 40(6), 2004, pages 917 to 927"
    locator: reachable sets as level sets of the value function of an optimal control problem
  - paper: doi:10.1090/S0025-5718-1984-0744921-8
    title: "M. G. Crandall and P.-L. Lions, Two approximations of solutions of Hamilton-Jacobi equations, Mathematics of Computation 43(167), 1984, pages 1 to 19"
    locator: convergence of monotone schemes and the error bound of order the square root of the grid step
  - paper: doi:10.1137/0728049
    title: "S. Osher and C.-W. Shu, High-order essentially nonoscillatory schemes for Hamilton-Jacobi equations, SIAM Journal on Numerical Analysis 28(4), 1991, pages 907 to 922"
    locator: the Lax-Friedrichs numerical Hamiltonian and higher order ENO schemes
  - paper: doi:10.1109/CDC.2017.8263977
    title: "S. Bansal, M. Chen, S. Herbert and C. J. Tomlin, Hamilton-Jacobi reachability: A brief overview and recent advances, IEEE Conference on Decision and Control, 2017, pages 2242 to 2253"
    locator: the overview of the formulation, its variants and the methods against the curse of dimensionality
---

Hamilton-Jacobi reachability computes the set of states from which a control input can drive a nonlinear system $x' = f(x, u, d)$ into a target set within a time $T$, whatever a bounded disturbance $d$ does. This is the backward reachable tube. The method writes the target as $\{x : g(x) \le 0\}$, solves a Hamilton-Jacobi equation for a value function $V(x, \tau)$ on a grid, and reads the tube as $\{x : V(x, T) \le 0\}$. Mitchell, Bayen and Tomlin (2005) proved that this sublevel set is the reachable set of the dynamic game when $V$ is the viscosity solution. The equation is a [Hamilton-Jacobi-Bellman equation](/hamilton-jacobi-bellman-equation/) with an extra $\min(0, \cdot)$. It handles nonlinear dynamics, sets that are not convex, and two players. The price is a grid, so the cost is exponential in the state dimension. It is one method for the [reachable set computation](/reachable-set-computation/) problem.

## In plain words

Put a number on every point of the state space: negative inside the target, positive outside, and roughly the distance to the edge of the target. Now let time run backward. At each point, ask how fast the best input can push the state toward lower numbers, when the disturbance pushes the other way. Lower the number at that point by this speed. A point whose number drops to zero or below can reach the target in the time you have.

A point that reached the target once stays counted, so numbers only go down. The computer does this on a grid of points, with a small time step. It is easy and works for curved, nonlinear systems, but the grid has an enormous number of points when the state has more than four or five components.

## The problem

The system is $x' = f(x, u, d)$ with $x \in \mathbb{R}^n$, $u \in U$ and $d \in D$ compact, and $f$ bounded and Lipschitz in $x$. The target is $\{x : g(x) \le 0\}$, for a Lipschitz function $g$, often a signed distance. The control tries to reach the target and the disturbance tries to prevent it. The backward reachable tube of horizon $T$ is the set of initial states from which the control can reach the target at some time in $[0, T]$, for every behavior of the disturbance, when the disturbance may react to the current input (a nonanticipative strategy). In time to go $\tau = T - t$, the value function solves

$$V_\tau = \min\big(0, H(x, \nabla V)\big), \qquad V(x, 0) = g(x), \qquad H(x, p) = \min_{u \in U} \max_{d \in D} \; p \cdot f(x, u, d),$$

and the tube is $\{x : V(x, T) \le 0\}$ (Mitchell, Bayen and Tomlin 2005). Without the $\min(0, \cdot)$, the zero sublevel set is the set of states that are in the target exactly at time $T$. The input to the program is a grid, $g$, the function $G = -H$, bounds $\alpha_i \ge \sup |\partial G / \partial p_i|$ on the grid, and $T$. The output is $V(\cdot, T)$ on the grid.

## The algorithm

The scheme is the first order Lax-Friedrichs scheme (see [Lax-Friedrichs scheme](/lax-friedrichs-scheme/) and Osher and Shu 1991), with $p_i^-$ and $p_i^+$ the backward and forward differences of $V$ along axis $i$.

```pseudo id=main
HJ-REACH(grid, g, G, alpha, T)
L1  for each node x_j do V_j ← g(x_j)
L2  K ← ceil(T * sum_i alpha_i / dx_i);  dtau ← T / K
L3  for k ← 1 to K do
L4      for each node j do
L5          p-_i ← (V_j - V_{j - e_i}) / dx_i;  p+_i ← (V_{j + e_i} - V_j) / dx_i  for each axis i
L6          Ghat_j ← G(x_j, (p+ + p-) / 2) - sum_i alpha_i (p+_i - p-_i) / 2
L7      for each node j do V_j ← V_j - dtau * max(0, Ghat_j)
L8  return V
```

Line L2 chooses the time step by the CFL condition $\Delta\tau \sum_i \alpha_i / \Delta x_i \le 1$. Line L6 is the numerical Hamiltonian: $G$ at the central difference, plus a diffusion term $\alpha_i (p_i^+ - p_i^-)/2$ that makes the scheme monotone. Line L7 is a forward Euler step of $V_\tau = -\max(0, G)$. At the edge of the grid, the program fills the missing neighbor by linear extrapolation. For the common control-affine case $f = f_0(x) + g_u(x) u + g_d(x) d$ with box or ball sets $U$ and $D$, $H$ has a closed form. For example, $x' = u + d$ with $|u| \le a$, $|d| \le b$ gives $H(p) = -(a - b)|p|$.

## Example

Take $x' = x + u$ with $|u| \le 1$, and the target $|x| \le 0.2$, with $g(x) = |x| - 0.2$. Here $H(x, p) = px - |p|$, so $G(x, p) = |p| - px$ and $|\partial G / \partial p| \le 1 + |x|$. The open loop is unstable, and the input can stop the drift only where $|x| < 1$. The best input is $u = -\operatorname{sign}(x)$, and from $x_0 \in (0, 1)$ the solution is $x(t) = 1 - (1 - x_0)e^t$. It reaches $0.2$ at time $T$ if $x_0 = 1 - 0.8 e^{-T}$, so the exact tube is $|x| \le 1 - 0.8 e^{-T}$, which is $0.514775$ for $T = 0.5$. The program runs on $[-2, 2]$ with $\alpha = 3$.

| nodes | $\Delta x$ | steps $K$ | computed edge of the tube | error |
|---|---|---|---|---|
| 101 | 0.04 | 38 | 0.474709 | 0.040 |
| 201 | 0.02 | 75 | 0.498601 | 0.016 |
| 401 | 0.01 | 150 | 0.509698 | 0.005 |

The edge is the zero of the linear interpolant of $V$. Here the error falls faster than $\sqrt{\Delta x}$, the rate that the theory guarantees. The computed set is inside the true tube on these grids, because the diffusion term rounds the kink of $g$ at its minimum. For $x' = u + d$ with $|u| \le 1$, $|d| \le 0.5$ and $g(x) = |x| - 0.5$, the exact tube at $T = 1$ is $|x| \le 1$, and the program finds the edge at $\pm 1$ to rounding error, because $V$ stays linear on each side. With a stronger disturbance ($|d| \le 1$, $|u| \le 0.5$) the tube is the target itself, and $V$ does not change. For $x' = u$ in the plane with $\|u\|_2 \le 1$ and a disk target of radius $0.5$, the tube at $T = 0.5$ is the disk of radius $1$. On a 41 by 41 grid the program puts its edge at radius $0.964$ on the axes and $0.962$ on the diagonal. The tests check all these cases.

## Correctness

Under the CFL condition and $\alpha_i \ge \sup |\partial G / \partial p_i|$, the update of line L7 is monotone: a larger $V$ at a node or at a neighbor never gives a smaller new value. It commutes with adding a constant, so it does not increase the maximum difference of two solutions. It is consistent with the equation to first order. Crandall and Lions (1984) proved that monotone consistent schemes for $u_t + H(Du) = 0$ converge to the viscosity solution, with an error of order $\sqrt{\Delta x}$. Mitchell, Bayen and Tomlin (2005) proved that the zero sublevel set of this viscosity solution is the backward reachable tube. Lygeros (2004) gives the same kind of characterization through an optimal control problem whose cost is the minimum of $g$ along the solution. The scheme also never raises $V$, so the computed set grows with $\tau$, like the true tube. The proof of the scheme properties, and the exact statements that it quotes, are in [the correctness proof](proofs/correctness.md). The theorems give convergence, not a guaranteed inner or outer bound on a fixed grid.

## Complexity

The model is the [real RAM](/real-ram/), with one evaluation of $G$ counted as $O(n)$ operations.

- A grid with $k$ nodes per axis has $M = k^n$ nodes, and each step costs $O(n M)$: this is the [curse of dimensionality](/curse-of-dimensionality/).
- Line L2 gives $K = \lceil T \sum_i \alpha_i / \Delta x_i \rceil$ steps, and $K$ grows linearly with $k$ for a fixed domain.
- The total is $O(K n k^n)$ time and $O(k^n)$ memory for one copy of $V$.

As a rule of thumb from the literature (see Bansal et al. 2017), direct grid methods are practical up to about four or five state dimensions. This is a statement about current hardware, not a theorem.

## Properties

- **Nonlinear and two-player.** It needs only $H$, so nonlinear dynamics, nonconvex targets and a disturbance that plays against the control are all allowed.
- **Approximate.** The result converges to the true tube as the grid is refined. On a fixed grid it is not a guaranteed over-approximation or under-approximation, unlike [zonotope reachability](/zonotope-reachability/).
- **Gives a controller.** Where $V$ is differentiable, $u(x) = \arg\min_u \max_d \nabla V \cdot f(x, u, d)$ is the input that reaches the target. The safety controller of the complement set uses the same gradient, as a [control barrier function](/control-barrier-function/) does.
- **Monotone in time.** The computed tube only grows with $\tau$, like the true one.
- **Exponential in $n$.** The grid limits the method to a few dimensions.

## Variants and improvements

- **Higher order schemes.** Osher and Shu (1991) gave ENO schemes for HJ equations; with a total variation diminishing Runge-Kutta step in time they are the default in level set toolboxes. They are more accurate on smooth parts, but they are not monotone.
- **Local Lax-Friedrichs.** Use a bound $\alpha_i$ at each node instead of one for the whole grid. It adds less diffusion. In the example, $\alpha = 1 + |x|$ instead of $3$.
- **Reach-avoid and avoid sets.** Swap the roles of the players to get the set of states that the disturbance can force into an unsafe set. Its complement is a safe set, and its limit as $T \to \infty$ is the largest [control invariant set](/control-invariant-set/) inside the safe region. Combining a target and an obstacle gives reach-avoid sets.
- **Minimum time.** For time-invariant dynamics, the first time at which a state enters the tube is the minimum time to reach the target. For speeds that depend only on the position, it solves an [eikonal equation](/eikonal-equation/), and the [fast marching method](/fast-marching-method/) computes it in one sweep.
- **Fewer dimensions.** Decomposition of the system, sampling of states, and neural approximations of $V$ trade guarantees for size; Bansal et al. (2017) survey them.

## When to use it

Use it for systems with two to four state dimensions where the nonlinearity or the game matters: collision avoidance between two vehicles in relative coordinates, a pendulum with input limits, an aircraft that must stay in an envelope. Use [zonotope reachability](/zonotope-reachability/) or other set propagation for linear systems in many dimensions. Use a [barrier certificate](/barrier-certificate/) search when you only need a proof of safety, not the exact set.

## Pitfalls

- **No min with zero (line L7).** Without $\max(0, \cdot)$, the program computes the set of states that are in the target exactly at time $T$. A state that passes through the target and leaves again is then missed.
- **Too large a time step (line L2).** If $\Delta\tau \sum_i \alpha_i / \Delta x_i > 1$, the scheme is not monotone and can blow up. $\alpha$ must bound $|\partial G / \partial p|$ on the whole grid, including the large $|x|$ near the edge.
- **The edge of the grid.** Linear extrapolation is not monotone, and with rough data the values near the edge can be wrong by much more than the grid error. The errors move inward one node per step. Put the edge far from the set of interest, by more than $K$ nodes if the data are rough.
- **Order of min and max.** $\min_u \max_d$ lets the disturbance react to the input. $\max_d \min_u$ gives the control the advantage. They agree when $f$ separates into a part with $u$ and a part with $d$; otherwise pick the one that matches the information of the real system.
- **Reading a grid result as a proof.** The computed set is an approximation. For a safety proof, add a margin of the size of the grid error, or verify the result with another method.

## Implementations

## History

Isaacs studied pursuit and evasion games through partial differential equations in the 1950s and 1960s. Crandall and Lions defined viscosity solutions in 1983, and in 1984 they proved the convergence of monotone schemes for HJ equations. Osher and Shu (1991) gave the ENO schemes used in level set methods. Lygeros (2004) linked reachable sets to minimum cost optimal control. Mitchell, Bayen and Tomlin (2005) gave the time-dependent HJ formulation for games and the level set computation used here. Bansal, Chen, Herbert and Tomlin (2017) surveyed the method and later work.

## References
