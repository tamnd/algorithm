---
tag: GZ9RFM
kind: problem
slug: reachable-set-computation
name: Reachable set computation
aliases:
- reach set computation
- reachability analysis of continuous systems
area: control/discrete-event-and-hybrid-systems
level: advanced
summary: Compute or over-approximate the set of states a continuous or hybrid system can reach from an initial set within a time bound.
model: real-ram
prereqs: [state-space-representation, reachability-problem]
see_also: [zonotope-reachability, hamilton-jacobi-reachability, barrier-certificate, hybrid-automata, symbolic-reachability, reachability-problem, support-function, control-invariant-set]
sources:
  - paper: doi:10.1146/annurev-control-071420-081941
    title: "M. Althoff, G. Frehse and A. Girard, Set propagation techniques for reachability analysis, Annual Review of Control, Robotics, and Autonomous Systems 4, 2021, pages 369 to 395"
    locator: the survey of the problem, the set representations and the algorithms for linear, nonlinear and hybrid systems
  - paper: doi:10.1006/jcss.1998.1581
    title: "T. A. Henzinger, P. W. Kopke, A. Puri and P. Varaiya, What's decidable about hybrid automata?, Journal of Computer and System Sciences 57(1), 1998, pages 94 to 124"
    locator: decidability of reachability for initialized rectangular automata and undecidability for small extensions
  - paper: doi:10.1016/S0005-1098(98)00175-7
    title: "V. D. Blondel and J. N. Tsitsiklis, Complexity of stability and controllability of elementary hybrid systems, Automatica 35(3), 1999, pages 479 to 489"
    locator: Section 1, on point-to-point reachability for piecewise constant derivative and piecewise linear systems
  - paper: doi:10.1109/TAC.2005.851439
    title: "I. M. Mitchell, A. M. Bayen and C. J. Tomlin, A time-dependent Hamilton-Jacobi formulation of reachable sets for continuous dynamic games, IEEE Transactions on Automatic Control 50(7), 2005, pages 947 to 957"
    locator: backward reachable sets with inputs and disturbances as sublevel sets of a viscosity solution
  - paper: doi:10.1016/j.nahs.2009.03.002
    title: "C. Le Guernic and A. Girard, Reachability analysis of linear systems using support functions, Nonlinear Analysis: Hybrid Systems 4(2), 2010, pages 250 to 262"
    locator: the support function of the reach set of a linear system and its computation
---

Reachable set computation asks for the set of all states that a dynamical system can reach from a set of initial states, with inputs or disturbances in a given set, within a given time. It is the continuous counterpart of the graph [reachability problem](/reachability-problem/), and it is the basic step of safety verification: if the reachable set does not meet the unsafe set, the system is safe. Exact reach sets are rarely representable, so most methods compute an over-approximation, which proves safety when it misses the unsafe set, or an under-approximation, which proves that a bad state can be reached. For hybrid systems the problem is undecidable in general (Henzinger, Kopke, Puri and Varaiya 1998). Althoff, Frehse and Girard (2021) survey the methods.

## In plain words

You know roughly where a system starts, and you know how strongly the inputs and the disturbances can push it, but not exactly how. You want to know every place where it can be at some time before a deadline. If none of these places is dangerous, the system is safe for every case at once, which no finite number of simulations can show.

The set of places usually has a curved, complicated shape, so a computer stores a simpler shape that is a little larger (to prove safety) or a little smaller (to find a real problem).

## Definition

**Input.** A system $x' = f(x, u)$ with $x \in \mathbb{R}^n$ (or $x_{k+1} = f(x_k, u_k)$ in discrete time, or a [hybrid automaton](/hybrid-automata/)), a set of initial states $X_0$, a set $U$ of input values, and a time bound $T$. The inputs are measurable functions with $u(t) \in U$, and $f$ is such that solutions exist and are unique, for example Lipschitz in $x$.

**Output.** Write $\phi(t; x_0, u)$ for the state at time $t$. The reachable set at time $t$ and the reachable tube are

$$\mathcal{R}(t) = \{\phi(t; x_0, u) : x_0 \in X_0, \ u(s) \in U\}, \qquad \mathcal{R}([0, T]) = \bigcup_{0 \le t \le T} \mathcal{R}(t).$$

An algorithm returns a set $\bar{\mathcal{R}} \supseteq \mathcal{R}([0, T])$ (over-approximation), a set $\underline{\mathcal{R}} \subseteq \mathcal{R}([0, T])$ (under-approximation), or the exact set where it has a finite representation.

**Decision version.** Given also an unsafe set $X_u$, decide whether $\mathcal{R}([0, T]) \cap X_u = \emptyset$. An over-approximation that misses $X_u$ proves the answer yes; an under-approximation that meets $X_u$ proves it no.

## Variants

- **Backward reachable set.** The set of initial states from which some input brings the state into a target set $G$ within time $T$. With a disturbance $d \in D$ that acts against the input, the question becomes a game, and the answer depends on what each player knows; [Hamilton-Jacobi reachability](/hamilton-jacobi-reachability/) treats this case.
- **Inputs that are uncertain, or chosen.** With "for some input", the reach set is what a controller can achieve; with "for all disturbances", it is what an adversary can force. Forward reach sets with bounded uncertain inputs are the usual form for verification.
- **Bounded or unbounded time.** With $T = \infty$, the question asks for an invariant: a set that contains $X_0$, is closed under the dynamics and misses $X_u$. See [positively invariant set](/positively-invariant-set/) and [control invariant set](/control-invariant-set/).
- **Discrete time and hybrid systems.** For a [piecewise affine system](/piecewise-affine-system/) one step maps a polyhedron to a union of polyhedra. For a hybrid automaton, the computation alternates between the continuous flow in a location and the discrete jumps through guards and resets.
- **Finite-state systems.** For finite graphs, [timed automata](/timed-automata/) and other systems with a finite quotient, the problem is graph search on the quotient; see [symbolic reachability](/symbolic-reachability/) and the [region graph](/region-graph/).

## Examples

**No input.** For $x' = -x$ and $X_0 = [1, 2]$, $\phi(t; x_0) = x_0 e^{-t}$, so $\mathcal{R}(1) = [e^{-1}, 2e^{-1}] = [0.3679, 0.7358]$ and $\mathcal{R}([0, 1]) = [0.3679, 2]$. Here the tube is the convex hull of $X_0$ and $\mathcal{R}(1)$. In two or more dimensions the tube is the union of the sets at all times, and it is not convex in general.

**A bounded input.** For $x' = u$ with $|u| \le 1$ and $X_0 = \{0\}$, $\mathcal{R}(t) = [-t, t]$. The backward reachable set of the target $[-0.2, 0.2]$ within time $T$ is $[-0.2 - T, 0.2 + T]$.

**A curved set from polytopes.** For $x_1' = x_2$, $x_2' = u$ with $|u| \le 1$ and $X_0 = \{0\}$, $\mathcal{R}(t)$ is a convex set whose boundary is made of two parabolic arcs, the states reached with one switch of $u$ between $+1$ and $-1$. So the reach set of a linear system with a box of inputs is not a polytope in general, and a polytope or a zonotope can only approximate it.

**The pages of the methods.** [Zonotope reachability](/zonotope-reachability/) has a worked example with a rotating linear system and a bounded input, and [Hamilton-Jacobi reachability](/hamilton-jacobi-reachability/) has examples with exact backward reachable sets for comparison.

## Known algorithms

- **Set propagation for linear systems.** For $x' = Ax + Bu$ with convex $X_0$ and $U$, $\mathcal{R}(t) = e^{tA} X_0 \oplus \int_0^t e^{sA} BU \, ds$, a [Minkowski sum](/minkowski-sum/). [Zonotope reachability](/zonotope-reachability/) (Girard 2005) and the method of [support functions](/support-function/) (Le Guernic and Girard 2010) compute sound over-approximations over time intervals, in polynomial time per step, and they have been applied to systems with hundreds of state variables.
- **Grid methods for nonlinear systems and games.** [Hamilton-Jacobi reachability](/hamilton-jacobi-reachability/) (Mitchell, Bayen and Tomlin 2005) computes backward reachable sets as sublevel sets of a value function on a grid. It handles nonlinear dynamics and disturbances, but the cost is exponential in $n$.
- **Validated integration.** [Interval arithmetic](/interval-arithmetic/) and Taylor models enclose the flow of a nonlinear system; boxes suffer from the wrapping effect, which zonotopes reduce.
- **Polyhedra and ellipsoids.** Polyhedral operations give exact reach sets for discrete-time PWA systems over short horizons. Ellipsoids give smooth over-approximations with closed-form steps for linear systems.
- **Hybrid systems.** Tools combine continuous set propagation in each location with intersection with guards and with resets, and repeat until a fixed point or a bound on the number of jumps; Althoff, Frehse and Girard (2021) describe the approach.
- **Certificates instead of sets.** A [barrier certificate](/barrier-certificate/) proves that the reach set misses $X_u$ without computing the set.
- **Abstraction.** A finite abstraction, with [symbolic reachability](/symbolic-reachability/) on the finite model, gives an over-approximation when the abstraction simulates the system; see [symbolic control](/symbolic-control/).

## Bounds

- **Undecidable for hybrid automata.** Henzinger, Kopke, Puri and Varaiya (1998) proved that reachability is decidable for initialized rectangular hybrid automata, and that it becomes undecidable under small extensions, for example when the initialization condition is dropped. See [undecidability](/undecidability/).
- **Undecidable for simple switched dynamics.** Blondel and Tsitsiklis (1999, Section 1) recall that point-to-point reachability is decidable for piecewise constant derivative systems in dimension two and undecidable in dimension three, by a simulation of Turing machines, and they derive undecidability for continuous-time piecewise linear systems with $4 \times 4$ matrices.
- **Finite cases.** Reachability in a finite graph takes linear time in its size. Reachability for [timed automata](/timed-automata/) is decidable with the region graph.
- **Size of exact representations.** The exact reach set of a discrete-time PWA system after $N$ steps can be a union of $s^N$ polyhedra for $s$ modes. Grid methods need $k^n$ cells for $k$ cells per axis, the [curse of dimensionality](/curse-of-dimensionality/).
- **Linear systems.** For $x' = Ax + Bu$ with polytopes $X_0$ and $U$, the support function of $\mathcal{R}(t)$ in a direction $\ell$ is $\rho_{X_0}(e^{tA^T}\ell) + \int_0^t \rho_{BU}(e^{sA^T}\ell)\, ds$, so each direction costs one matrix exponential and one integral. Over-approximations with a fixed number of directions or generators are polynomial; the error comes from the time discretization and the finite representation.

## Reductions

- **Safety verification to reachability.** A system is safe up to time $T$ if and only if $\mathcal{R}([0, T]) \cap X_u = \emptyset$.
- **Backward to forward.** For "some input" questions without a disturbance, the backward reachable set of $G$ for $x' = f(x, u)$ is the forward reachable set of $G$ for the time-reversed system $x' = -f(x, u)$.
- **Controller synthesis.** The largest set from which a controller can keep the state in a safe set is the limit of a backward iteration, the [control invariant set](/control-invariant-set/) computation; the complement of the backward reachable set of the unsafe set under a disturbance gives the same set.
- **Discrete abstraction.** If a finite transition system simulates the continuous system, a graph search on it gives an over-approximation of the reach set; see [simulation relation](/simulation-relation/) and [bisimulation](/bisimulation/).

## Applications

Verification of automated driving functions against traffic rules, collision avoidance for aircraft and drones, safety of power systems and of analog circuits, and the safety filters of learned controllers. In predictive control, reach sets of the error dynamics give the tubes of [tube MPC](/tube-mpc/).

## References
