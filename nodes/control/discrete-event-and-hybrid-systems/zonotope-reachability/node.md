---
tag: XHB5KP
kind: algorithm
slug: zonotope-reachability
name: Zonotope reachability
aliases:
- Girard's zonotope reachability
area: control/discrete-event-and-hybrid-systems
level: research
summary: Over-approximates the reachable sets of linear systems by zonotopes, which stay zonotopes under linear maps and Minkowski sums.
model: real-ram
complexity:
  vars: {n: the state dimension, N: the number of time steps, m: the number of generators kept after each step}
  time: {worst: O(n^3 + N n^2 m + N m log m)}
  space: {extra: O(N n m)}
properties: {deterministic: true, exact: false, online: false}
history:
  year: 2005
  people: [Wolfgang Kühn, Antoine Girard]
  note: "Kühn used zonotopes in 1998 to stop the wrapping effect in validated orbit enclosures. Girard gave the reachability algorithm for linear systems with bounded inputs at HSCC 2005."
prereqs: [reachable-set-computation, minkowski-sum, matrix-exponential]
see_also: [reachable-set-computation, hamilton-jacobi-reachability, support-function, interval-arithmetic, convex-polytope, hybrid-automata, tube-mpc, positively-invariant-set]
sources:
  - paper: doi:10.1007/978-3-540-31954-2_19
    title: "A. Girard, Reachability of uncertain linear systems using zonotopes, Hybrid Systems: Computation and Control (HSCC 2005), LNCS 3414, Springer, 2005, pages 291 to 305"
    locator: the algorithm for the reach sets over time intervals, the bounds alpha_r and beta_r, and the reduction of the order
  - paper: doi:10.1007/BF02684450
    title: "W. Kühn, Rigorously computed orbits of dynamical systems without the wrapping effect, Computing 61(1), 1998, pages 47 to 67"
    locator: zonotopes as enclosures that do not suffer from the wrapping effect of boxes
  - paper: doi:10.1007/11730637_21
    title: "A. Girard, C. Le Guernic and O. Maler, Efficient computation of reachable sets of linear time-invariant systems with inputs, HSCC 2006, LNCS 3927, Springer, 2006, pages 257 to 271"
    locator: the wrapping-free form of the recurrence
  - paper: doi:10.1016/j.nahs.2009.03.002
    title: "C. Le Guernic and A. Girard, Reachability analysis of linear systems using support functions, Nonlinear Analysis: Hybrid Systems 4(2), 2010, pages 250 to 262"
    locator: the same recurrence with support functions instead of zonotopes
  - paper: doi:10.1146/annurev-control-071420-081941
    title: "M. Althoff, G. Frehse and A. Girard, Set propagation techniques for reachability analysis, Annual Review of Control, Robotics, and Autonomous Systems 4, 2021, pages 369 to 395"
    locator: the survey of set representations, zonotopes among them
---

Zonotope reachability computes sets that contain every state that a linear system $x' = Ax + u$ can reach, for all initial states in a set $X_0$ and all inputs with $\|u(t)\|_\infty \le \mu$. It is one method for the [reachable set computation](/reachable-set-computation/) problem. It cuts the time axis into steps of length $r$, and it returns one zonotope $Q_i$ for each interval $[ir, (i+1)r]$. A zonotope is the image of a cube under an affine map, $\langle c, g_1, \ldots, g_p \rangle = \{c + \sum_j a_j g_j : |a_j| \le 1\}$. A linear map and a [Minkowski sum](/minkowski-sum/) of zonotopes are again zonotopes, and the program computes them exactly with a matrix product and a list concatenation. The method is due to Girard (2005), and it uses the zonotopes that Kühn (1998) introduced against the wrapping effect of [interval arithmetic](/interval-arithmetic/). The result is sound: it never misses a reachable state. It is not exact.

## In plain words

You want to know everywhere a system can go, when you know only roughly where it starts and how strongly it can be pushed. You cannot run every possible case, so you carry a whole set of states through time instead of one state.

The set is a special shape: a box that you can stretch, tilt and add other boxes to. Such shapes stay the same kind of shape when the system moves them, and when you add the push, so each step is cheap and exact. The only losses come from two places. To cover the times between two steps, you blow the first shape up a little. To keep the shapes small enough to store, you sometimes replace some thin parts by a box around them. Both losses make the answer larger, never smaller, so a state outside the answer is truly unreachable.

## The problem

The input is a matrix $A \in \mathbb{R}^{n \times n}$, an initial zonotope $X_0 = \langle c, g_1, \ldots, g_p \rangle$, an input bound $\mu \ge 0$, a step $r > 0$, a number of steps $N$ and a maximum number $m \ge n$ of generators. The system is $x' = Ax + u$ with $\|u(t)\|_\infty \le \mu$. For $x' = Ax + Bw$ with $\|w\|_\infty \le \mu'$, set $u = Bw$ and $\mu = \|B\|_\infty \mu'$. The output is a list of zonotopes $Q_0, \ldots, Q_{N-1}$ such that every solution satisfies $x(t) \in Q_i$ for $ir \le t \le (i+1)r$. All norms are infinity norms: $\|x\| = \max_i |x_i|$, $\|A\|$ is the largest absolute row sum, and the ball $B(\rho)$ is the box $\langle 0, \rho e_1, \ldots, \rho e_n \rangle$.

## The algorithm

```pseudo id=main
ZONOTOPE-REACH(A, X0 = <c, g_1 .. g_p>, mu, r, N, m)
L1  Phi ← e^(rA)
L2  a ← ‖A‖;  s ← max of ‖x‖ over X0;  alpha ← (e^(ra) - 1 - ra) s;  beta ← (e^(ra) - 1) mu / a
L3  P0 ← <(c + Phi c)/2, (g_j + Phi g_j)/2, (c - Phi c)/2, (g_j - Phi g_j)/2>
L4  Q_0 ← P0 ⊕ B(alpha + beta)
L5  for i ← 0 to N - 2 do
L6      Q_{i+1} ← Phi Q_i ⊕ B(beta)
L7      if Q_{i+1} has more than m generators then Q_{i+1} ← REDUCE(Q_{i+1}, m)
L8      append Q_{i+1} to the output
L9  return Q_0, ..., Q_{N-1}
```

Line L1 computes the [matrix exponential](/matrix-exponential/) once. At line L2, $s = \max_i (|c_i| + \sum_j |g_{j,i}|)$, and if $a = 0$ then $\beta = r\mu$. Line L3 builds a zonotope that contains the convex hull of $X_0$ and $\Phi X_0$, the sets at times $0$ and $r$. Line L4 adds a box: $\alpha$ covers the gap between the true curve $e^{tA}x_0$ and the straight segment from $x_0$ to $\Phi x_0$, and $\beta$ covers the effect of the input over one step. Line L6 moves the set one step forward and adds the input effect of the new step. REDUCE at line L7 sorts the generators by $\|g\|_1 - \|g\|_\infty$, keeps the $m - n$ largest, and replaces the others by the smallest box around their sum, which is $n$ axis-parallel generators. This sort key is the one of Girard (2005); it boxes first the generators that are close to an axis, where the box loses little.

## Example

Take $A = \begin{pmatrix} -1 & -4 \\ 4 & -1 \end{pmatrix}$, the box $X_0$ with center $(1, 0)$ and radius $0.1$, $\mu = 0.05$ and $r = 0.05$. Then $\Phi = e^{-0.05} \begin{pmatrix} \cos 0.2 & -\sin 0.2 \\ \sin 0.2 & \cos 0.2 \end{pmatrix} = \begin{pmatrix} 0.93227 & -0.18898 \\ 0.18898 & 0.93227 \end{pmatrix}$.

| quantity | value |
|---|---|
| $a = \|A\|_\infty$ | 5 |
| $s = \max_{X_0} \|x\|_\infty$ | 1.1 |
| $\alpha = (e^{0.25} - 1.25) \cdot 1.1$ | 0.037428 |
| $\beta = (e^{0.25} - 1) \cdot 0.05 / 5$ | 0.0028403 |
| center of $P_0$ | $(0.96613, 0.09449)$ |
| generators of $P_0$, $Q_0$, $Q_{19}$ | 5, 7, 45 |
| interval hull of $Q_0$ | $[0.7731, 1.1592] \times [-0.1592, 0.3481]$ |
| interval hull of $Q_{19}$ | $[-0.4310, -0.1154] \times [-0.4035, -0.1115]$ |
| interval hull of $Q_{19}$, at most 6 generators | $[-0.5427, -0.0037] \times [-0.5149, -0.0002]$ |

$X_0$ has 2 generators, so $P_0$ has $2 \cdot 2 + 1 = 5$, $Q_0$ adds the 2 of the box, and each step adds 2 more. $Q_{19}$ covers the times $0.95$ to $1$. With $u = 0$, the center of $X_0$ moves to $e^{A}(1, 0) = (-0.2405, -0.2784)$ at $t = 1$, inside the interval hull of $Q_{19}$. The reduction to 6 generators makes the interval hull about $1.7$ times wider in each coordinate. The tests of the implementation reproduce these numbers. They also run RK4 solutions with random inputs of size $\mu$ and check, with an exact membership test for zonotopes in the plane, that each solution stays in $Q_i$ on every interval.

## Correctness

The proof has four parts. (1) A linear map and a Minkowski sum of zonotopes are exact, by the definition. (2) The zonotope of line L3 contains the convex hull of $X_0 \cup \Phi X_0$: a point $\lambda z + (1 - \lambda)\Phi z'$ of the hull has coefficients $2\lambda - 1$, $\lambda a_j + (1 - \lambda) b_j$ and $\lambda a_j - (1 - \lambda) b_j$ in this zonotope, and all of them are in $[-1, 1]$. (3) For $t \in [0, r]$, the power series gives $\|e^{tA}x_0 - x_0 - \frac{t}{r}(\Phi - I)x_0\| \le (e^{ra} - 1 - ra)\|x_0\| \le \alpha$, because $|t^k - t r^{k-1}| \le r^k$, and the input adds at most $\int_0^r e^{\sigma a} \mu \, d\sigma = \beta$. So $Q_0$ contains the states of $[0, r]$. (4) A state at time $t + r$ is $\Phi x(t)$ plus an input term of norm at most $\beta$, so line L6 keeps the invariant, and REDUCE only adds points. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [real RAM](/real-ram/), with the cost counted in arithmetic operations.

- Line L1 costs $O(n^3)$ for a dense matrix exponential by scaling and squaring.
- Without reduction, $Q_i$ has $2p + 1 + n(i + 1)$ generators, and line L6 costs $O(n^2)$ per generator. $N$ steps cost $O(N^2 n^3)$ in total when $p \le n$.
- With reduction to $m$ generators, a step costs $O(n^2 m)$ for the product and $O(m \log m)$ for the sort. $N$ steps cost $O(n^3 + N n^2 m + N m \log m)$, and storing all $Q_i$ takes $O(N n m)$ numbers.

The cost is polynomial in $n$. This is the main reason to use zonotopes: a grid method such as [Hamilton-Jacobi reachability](/hamilton-jacobi-reachability/) has a cost exponential in $n$, and a polytope in vertex or facet form can need exponentially many vertices or facets to write the same set.

## Properties

- **Sound.** Every $Q_i$ contains the true reach set of its time interval. This is a theorem, under the stated bound on the inputs.
- **Not exact.** The terms $\alpha$ and $\beta$ and the reduction make $Q_i$ larger than the reach set. $\alpha$ is $O(r^2)$, so a smaller step helps, but more steps mean more reductions.
- **Closed operations.** Linear maps and Minkowski sums are exact on zonotopes. Intersection with a half-space and the union are not; they need an enclosure.
- **Cheap queries.** The support function in a direction $d$ is $d \cdot c + \sum_j |d \cdot g_j|$, and the [interval hull](/interval-arithmetic/) is $c \pm \sum_j |g_j|$. Testing whether a point is in a zonotope in $n$ dimensions is a linear program; in the plane it is a list of half-plane tests.
- **Symmetric.** A zonotope is centrally symmetric, so it encloses sets that are not symmetric with some waste.

## Variants and improvements

- **Wrapping-free form.** Girard, Le Guernic and Maler (2006) write $Q_i = \Phi^i Q_0 \oplus S_i$, with $S_{i+1} = S_i \oplus \Phi^i B(\beta)$. The product $\Phi^i Q_0$ is exact, and only $S_i$ is reduced, so a reduction error is not multiplied by $\Phi$ at later steps.
- **Support functions.** Le Guernic and Girard (2010) run the same recurrence on [support functions](/support-function/) in a fixed set of directions. Each direction costs a few matrix products and no set is ever stored in full.
- **Other norms.** Any norm works if $B(\rho)$ is a ball of the same norm, or a set that contains it. The infinity norm is used here because its ball is a zonotope.
- **Hybrid systems.** For [hybrid automata](/hybrid-automata/) with linear dynamics, tools intersect the zonotopes with the guards and continue in the next mode. The intersection is not a zonotope, and it is enclosed again; see the survey of Althoff, Frehse and Girard (2021).
- **Nonlinear systems.** Linearize around the current set and add the Lagrange remainder as an extra input set. The error terms then depend on the size of the set.

## When to use it

Use it to verify a linear system with bounded disturbances over a finite horizon in many dimensions, for example that a closed loop never leaves a safe box. It also gives the disturbance tubes of [tube MPC](/tube-mpc/). Use [Hamilton-Jacobi reachability](/hamilton-jacobi-reachability/) when the dynamics are strongly nonlinear, the state has very few dimensions and a control and a disturbance play against each other. Use a [positively invariant set](/positively-invariant-set/) when you need an infinite horizon.

## Pitfalls

- **Mixed norms (lines L2 and L4).** If $\alpha$ and $\beta$ come from $\|A\|_\infty$, the added ball must be the box. A disk of radius $\alpha + \beta$ does not contain all the error vectors whose infinity norm is at most $\alpha + \beta$.
- **Only the sampled times (line L3).** The set $\Phi^i X_0$ contains the states at the times $ir$ only. Without the hull and $\alpha$, a trajectory can leave the computed sets between two samples.
- **Input term once (line L4).** $\beta$ must be added at every step. Adding it only in $Q_0$ ignores the inputs after the first step.
- **Too much reduction (line L7).** Each reduction adds a box, and $\Phi$ turns the box at the next step. The sets can grow even when the system is stable. This is the wrapping effect that zonotopes were introduced to avoid, now back through the reduction. Keep more generators, or use the wrapping-free form.
- **Tests by sampling.** Random trajectories that stay inside the sets can find a bug, but they do not prove containment. The proof does.

## Implementations

## History

Interval methods for ordinary differential equations lose accuracy because each step wraps a rotated box in a larger box. Kühn (1998) used zonotopes to keep the enclosures tight in validated computations of orbits. Girard (2005) applied them to the reach sets of linear systems with uncertain inputs and gave the bounds $\alpha_r$ and $\beta_r$ and the order reduction used here. Girard, Le Guernic and Maler (2006) removed the wrapping effect of the reduction, and Le Guernic and Girard (2010) moved the recurrence to support functions. Althoff, Frehse and Girard (2021) survey these and other set representations for reachability.

## References
