---
tag: CQA2NV
kind: model
slug: piecewise-affine-system
name: Piecewise affine system
aliases:
- PWA system
area: control/discrete-event-and-hybrid-systems
level: advanced
summary: A system whose dynamics are affine on each cell of a polyhedral partition of the state and input space.
prereqs: [state-space-representation, switched-system]
see_also: [mixed-logical-dynamical-system, hybrid-mpc, switched-system, hybrid-automata, timed-automata, reachable-set-computation, common-lyapunov-function, linear-matrix-inequality]
sources:
  - paper: doi:10.1109/TAC.1981.1102596
    title: "E. D. Sontag, Nonlinear regulation: The piecewise linear approach, IEEE Transactions on Automatic Control 26(2), 1981, pages 346 to 358"
    locator: piecewise linear systems in discrete time as a class of models for nonlinear control
  - paper: doi:10.1016/S0005-1098(01)00059-0
    title: "W. P. M. H. Heemels, B. De Schutter and A. Bemporad, Equivalence of hybrid dynamical models, Automatica 37(7), 2001, pages 1085 to 1091"
    locator: the equivalence of PWA, MLD, linear complementarity, extended linear complementarity and max-min-plus-scaling systems
  - paper: doi:10.1016/S0005-1098(98)00175-7
    title: "V. D. Blondel and J. N. Tsitsiklis, Complexity of stability and controllability of elementary hybrid systems, Automatica 35(3), 1999, pages 479 to 489"
    locator: "Theorem 1 (asymptotic stability of systems with two half spaces is NP-hard) and Theorem 2 (null-controllability and complete reachability of sign systems are undecidable)"
  - paper: doi:10.1109/tac.2000.880987
    title: "A. Bemporad, G. Ferrari-Trecate and M. Morari, Observability and controllability of piecewise affine and hybrid systems, IEEE Transactions on Automatic Control 45(10), 2000, pages 1864 to 1876"
    locator: tests of observability and controllability of PWA systems by mixed-integer linear programming
  - book: isbn:978-1-107-01688-0
    title: "F. Borrelli, A. Bemporad and M. Morari, Predictive Control for Linear and Hybrid Systems, Cambridge University Press, 2017"
    locator: "Chapter 16, Models of Hybrid Systems"
---

A piecewise affine (PWA) system is a dynamical system whose state space, or state and input space, is cut into finitely many polyhedra, with an affine dynamics in each one. It is the simplest model that has both continuous dynamics and discrete switching that depends on the state. A PWA model can approximate any continuous nonlinear system on a bounded set, it describes saturations, dead zones and contact exactly, and it has polyhedral pieces, so linear and mixed-integer programming apply to it. Sontag (1981) proposed piecewise linear systems as a general approach to nonlinear control. Heemels, De Schutter and Bemporad (2001) showed that PWA systems are equivalent to [mixed logical dynamical systems](/mixed-logical-dynamical-system/) and to other hybrid model classes, under mild conditions. The price of this generality is that many analysis questions are NP-hard or undecidable for PWA systems.

## The machine

In discrete time, with state $x_k \in \mathbb{R}^n$, input $u_k \in \mathbb{R}^m$ and output $y_k \in \mathbb{R}^p$:

$$x_{k+1} = A_i x_k + B_i u_k + f_i, \qquad y_k = C_i x_k + D_i u_k + g_i \qquad \text{if } \begin{pmatrix} x_k \\ u_k \end{pmatrix} \in \Omega_i, \quad i = 1, \ldots, s.$$

The cells $\Omega_i = \{(x, u) : H_i x + J_i u \le h_i\}$ are polyhedra. Their union is the set of allowed state and input pairs, and their interiors do not meet. Two standing assumptions make the model well posed.

- **One mode per point.** If two cells share a boundary and the two affine maps differ there, the model must say which mode applies, for example with strict inequalities on one side. Otherwise the next state is not unique.
- **The state stays in the domain.** If the cells do not cover all of $\mathbb{R}^n \times \mathbb{R}^m$, the state and input constraints must keep the pair inside the union.

With $f_i = 0$ and $g_i = 0$ the system is piecewise linear. If the affine maps agree on every shared boundary, the system is continuous; it is then a continuous piecewise affine map, the same class of functions that a neural network with [ReLU](/relu/) activations computes. In continuous time, $x' = A_i x + B_i u + f_i$ on $\Omega_i$ needs more care at the boundaries: a solution can slide along a boundary, or switch infinitely often in a finite time (see [Zeno behavior](/zeno-behavior/)), and a solution concept for discontinuous right-hand sides is needed.

## What it counts

The model predicts the next state and the output from the current state and input. Over a horizon of $N$ steps, the prediction is affine in the inputs for each fixed sequence of modes, and there are up to $s^N$ sequences. This is why optimization over a PWA model is a mixed-integer problem: [hybrid MPC](/hybrid-mpc/) solves one at each sampling instant. When a PWA model is fitted to data, the unknowns are the partition and the affine maps of each cell, and the criterion is the prediction error; the partition makes this fit a hard combinatorial problem.

## Relation to other models

- **Linear models.** One cell gives an affine [state-space representation](/state-space-representation/).
- **Switched systems.** A [switched system](/switched-system/) also has several linear dynamics, but its mode is an external signal or is arbitrary. In a PWA system the mode is a function of the state and input. Stability under arbitrary switching implies stability of every PWA system with the same matrices, but not the converse.
- **MLD systems.** A PWA system with a bounded domain can be written as an MLD system with one binary variable per mode and [big-M](/big-m-formulation/) inequalities, and a well-posed MLD system defines a PWA system (Heemels, De Schutter and Bemporad 2001). The same paper adds linear complementarity, extended linear complementarity and max-min-plus-scaling systems to the list, each with its own conditions.
- **Hybrid automata.** A PWA system is a [hybrid automaton](/hybrid-automata/) with one location per cell, guards on the cell boundaries, no resets and deterministic switching. Hybrid automata allow resets of the state, nondeterminism and invariants that do not partition the space.
- **Timed automata and Petri nets.** A [timed automaton](/timed-automata/) has only clocks with rate 1 and resets to zero, and its reachability problem is decidable. A [Petri net](/petri-net/) has no continuous state. PWA systems have general affine dynamics, which makes reachability undecidable.

## Known results in the model

- **Hardness.** Blondel and Tsitsiklis (1999) proved that deciding asymptotic stability of $x_{k+1} = A_+ x_k$ if $c^T x_k \ge 0$ and $x_{k+1} = A_- x_k$ otherwise, a piecewise linear system with two half spaces, is NP-hard (Theorem 1 and its special cases). They also proved that null-controllability and complete reachability are undecidable for sign systems, where the matrix depends on the sign of a linear function of the state and an input enters linearly (Theorem 2; see [undecidability](/undecidability/)). So exact tests are out of reach in general, and the practical tests are sufficient conditions.
- **Stable modes do not give a stable system.** The modes can each be asymptotically stable while the PWA system is not; see the example below. A [common Lyapunov function](/common-lyapunov-function/) for all modes is sufficient for stability. Piecewise quadratic Lyapunov functions, one quadratic form per cell with conditions on the boundaries, are less conservative and are found with [linear matrix inequalities](/linear-matrix-inequality/).
- **Observability and controllability.** Bemporad, Ferrari-Trecate and Morari (2000) gave tests for PWA and hybrid systems by mixed-integer linear programming. Observability of each mode alone does not settle the question, because the sequence of modes also depends on the unknown state.
- **Reach sets.** The image of a polyhedron under one step is a union of at most $s$ polyhedra, so the exact reach set after $N$ steps is a union of polyhedra whose number can grow like $s^N$; see [reachable set computation](/reachable-set-computation/).
- **Optimal control.** For a PWA system with a quadratic or linear cost and polyhedral constraints, the finite horizon optimal control is a mixed-integer program at each state, and the optimal feedback is a piecewise affine function of the state on a partition that need not be convex (Borrelli, Bemporad and Morari 2017, Chapter 17). See [hybrid MPC](/hybrid-mpc/) and [explicit MPC](/explicit-mpc/).

**Example: stable modes, unstable system.** Take

$$A_1 = 0.9\begin{pmatrix} 1 & 2 \\ 0 & 1 \end{pmatrix} \text{ on } \{x_1 \le x_2\}, \qquad A_2 = 0.9\begin{pmatrix} 1 & 0 \\ 2 & 1 \end{pmatrix} \text{ on } \{x_1 > x_2\},$$

with no input. Each matrix has both eigenvalues equal to $0.9$, so each mode alone is asymptotically stable. From $x_0 = (0, 1)$ the states are $(1.8, 0.9)$, $(1.62, 4.05)$, $(8.748, 3.645)$ and $(7.8732, 19.0269)$. Mode 1 makes $x_1$ large, which sends the state into the cell of mode 2, and mode 2 makes $x_2$ large. In the positive quadrant the modes alternate for ever, and two steps multiply the state by $A_2 A_1 = 0.81\begin{pmatrix} 1 & 2 \\ 2 & 5 \end{pmatrix}$ or by $A_1 A_2$, whose largest eigenvalue is $0.81(3 + 2\sqrt{2}) = 4.72$. So the state grows without bound. The strict inequality on the second cell is the rule that makes the model well posed on the line $x_1 = x_2$.

## References
