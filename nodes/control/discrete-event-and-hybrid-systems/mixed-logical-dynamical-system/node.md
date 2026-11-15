---
tag: 9HNM8B
kind: model
slug: mixed-logical-dynamical-system
name: Mixed logical dynamical system
aliases:
- MLD system
area: control/discrete-event-and-hybrid-systems
level: advanced
summary: A model that writes hybrid dynamics with logic as linear equations and inequalities in real and binary variables.
prereqs: [piecewise-affine-system, mixed-integer-programming, big-m-formulation]
see_also: [piecewise-affine-system, hybrid-mpc, big-m-formulation, mixed-integer-programming, hybrid-automata, timed-automata, petri-net, model-predictive-control]
sources:
  - paper: doi:10.1016/S0005-1098(98)00178-2
    title: "A. Bemporad and M. Morari, Control of systems integrating logic, dynamics, and constraints, Automatica 35(3), 1999, pages 407 to 427"
    locator: the MLD form, the translation of propositional logic into mixed-integer inequalities, well-posedness, and predictive control of MLD systems
  - paper: doi:10.1016/S0005-1098(01)00059-0
    title: "W. P. M. H. Heemels, B. De Schutter and A. Bemporad, Equivalence of hybrid dynamical models, Automatica 37(7), 2001, pages 1085 to 1091"
    locator: the equivalence of MLD, PWA, linear complementarity, extended linear complementarity and max-min-plus-scaling systems
  - paper: doi:10.1109/TCST.2004.824309
    title: "F. D. Torrisi and A. Bemporad, HYSDEL: a tool for generating computational hybrid models for analysis and synthesis problems, IEEE Transactions on Control Systems Technology 12(2), 2004, pages 235 to 249"
    locator: the HYSDEL language and its compilation into MLD form
  - paper: doi:10.1109/tac.2000.880987
    title: "A. Bemporad, G. Ferrari-Trecate and M. Morari, Observability and controllability of piecewise affine and hybrid systems, IEEE Transactions on Automatic Control 45(10), 2000, pages 1864 to 1876"
    locator: observability and controllability tests for MLD and PWA systems by mixed-integer linear programming
  - book: isbn:978-1-107-01688-0
    title: "F. Borrelli, A. Bemporad and M. Morari, Predictive Control for Linear and Hybrid Systems, Cambridge University Press, 2017"
    locator: "Chapter 16, Models of Hybrid Systems"
---

A mixed logical dynamical (MLD) system is a discrete-time model in which the state update is linear in real variables and binary variables, and a set of linear inequalities ties the binary variables to the state and the input. The inequalities encode logic (if, and, or, implies), switching between modes, saturations and the condition that a real quantity is above a threshold. Bemporad and Morari (1999) introduced the form so that the finite-horizon optimal control of a hybrid plant becomes a mixed-integer linear or quadratic program, which a standard solver can handle. The model is the input format of [hybrid MPC](/hybrid-mpc/). It describes the same systems as a [piecewise affine system](/piecewise-affine-system/) under mild conditions (Heemels, De Schutter and Bemporad 2001), but in a form that an optimizer reads directly.

## The machine

The state $x_k = (x_c, x_\ell)$ has real components $x_c \in \mathbb{R}^{n_c}$ and binary components $x_\ell \in \{0, 1\}^{n_\ell}$, and the input and output are split the same way. The model adds auxiliary binary variables $\delta_k \in \{0, 1\}^{r_\ell}$ and auxiliary real variables $z_k \in \mathbb{R}^{r_c}$:

$$x_{k+1} = A x_k + B_1 u_k + B_2 \delta_k + B_3 z_k,$$
$$y_k = C x_k + D_1 u_k + D_2 \delta_k + D_3 z_k,$$
$$E_2 \delta_k + E_3 z_k \le E_1 u_k + E_4 x_k + E_5.$$

Time is discrete. For a given $x_k$ and $u_k$, the inequalities define the allowed $(\delta_k, z_k)$. The model is well posed if, for every $(x_k, u_k)$ for which the inequalities have a solution, the next state $x_{k+1}$ and the output $y_k$ are unique (Bemporad and Morari 1999). The pairs $(x_k, u_k)$ with no solution are forbidden, so the inequalities also express state and input constraints.

**From logic to inequalities.** Let $f(x)$ be affine with $m \le f(x) \le M$ on the bounded domain, and let $\varepsilon > 0$ be a small tolerance.

| statement | inequalities |
|---|---|
| $\delta_1 \lor \delta_2$ | $\delta_1 + \delta_2 \ge 1$ |
| $\delta_1 \land \delta_2$ | $\delta_1 = 1$, $\delta_2 = 1$ |
| $\delta_1 \Rightarrow \delta_2$ | $\delta_1 \le \delta_2$ |
| $[f(x) \le 0] \Leftrightarrow [\delta = 1]$ | $f(x) \le M(1 - \delta)$, $f(x) \ge \varepsilon + (m - \varepsilon)\delta$ |
| $z = \delta f(x)$ | $m\delta \le z \le M\delta$, $f(x) - M(1 - \delta) \le z \le f(x) - m(1 - \delta)$ |

These are [big-M](/big-m-formulation/) constraints. The constants $M$ and $m$ come from bounds on $x$ and $u$, so the domain must be bounded in the directions that the logic uses. The tolerance $\varepsilon$ is needed because a strict inequality $f(x) > 0$ cannot be written as a closed constraint.

**Example.** Take the scalar PWA system $x_{k+1} = 0.5x_k + u_k$ if $x_k \ge 0$ and $x_{k+1} = 2x_k + u_k$ if $x_k < 0$, on $|x| \le 5$, $|u| \le 1$. Let $\delta = 1$ stand for $x \ge 0$. With $f(x) = -x \in [-5, 5]$, the event gives $-x \le 5(1 - \delta)$ and $-x \ge \varepsilon - (5 + \varepsilon)\delta$. Write the update as $x_{k+1} = 2x_k + u_k + z_k$ with $z = \delta \cdot (-1.5x)$, where $-1.5x \in [-7.5, 7.5]$:

$$-7.5\delta \le z \le 7.5\delta, \qquad -1.5x - 7.5(1 - \delta) \le z \le -1.5x + 7.5(1 - \delta).$$

For $\delta = 1$ the second pair gives $z = -1.5x$ and $x_{k+1} = 0.5x_k + u_k$. For $\delta = 0$ the first pair gives $z = 0$ and the second pair holds because $|1.5x| \le 7.5$. So $A = 2$, $B_1 = 1$, $B_2 = 0$, $B_3 = 1$, with one binary variable, one auxiliary real variable and six inequalities. The model is well posed: the event inequalities fix $\delta$ for every $x$ outside $(-\varepsilon, 0)$, and the inequalities forbid that small interval.

## What it counts

The model predicts the next state and the output, but each prediction is a feasibility problem: given $x_k$ and $u_k$, find $(\delta_k, z_k)$ that satisfy the inequalities. Over a horizon of $N$ steps, the unknowns are $N(m + r_\ell + r_c)$ input and auxiliary variables, of which $N r_\ell$ are binary (plus binary inputs if any). With a quadratic cost, the optimal control problem is a mixed-integer quadratic program; with a 1-norm or infinity-norm cost, a mixed-integer linear program (Bemporad and Morari 1999). The size of the MLD model, and the tightness of the big-M constants, decide how hard these programs are for branch and bound (see [mixed-integer programming](/mixed-integer-programming/)).

## Relation to other models

- **PWA systems.** A PWA system on a bounded domain becomes an MLD system with one binary variable per mode, $\sum_i \delta_i = 1$, and $z_i = \delta_i(A_i x + B_i u + f_i)$; the next state is $\sum_i z_i$. A well-posed MLD system defines a PWA system: for each value of the binary variables the remaining constraints are a polyhedron in $(x, u)$ and the update is affine. Heemels, De Schutter and Bemporad (2001) proved this equivalence, with the conditions on boundedness and well-posedness, and they extended it to linear complementarity, extended linear complementarity and max-min-plus-scaling systems. The PWA form is better for analysis by cells; the MLD form is better as input to an optimizer.
- **Hybrid automata.** A [hybrid automaton](/hybrid-automata/) has continuous time, locations with flows, guards and resets, and can be nondeterministic. An MLD system is in discrete time and is deterministic when it is well posed. A discrete-time hybrid automaton with affine flows, polyhedral guards and affine resets can be written in MLD form.
- **Timed automata and Petri nets.** A [timed automaton](/timed-automata/) has only clocks, and a [Petri net](/petri-net/) only discrete markings. The MLD form can encode the discrete part of both with binary variables, but it is meant for plants with real dynamics, not for model checking.
- **Mixed-integer programs.** One step of an MLD system is a set of constraints of a [mixed-integer program](/mixed-integer-programming/). Stacking $N$ copies gives the constraints of a planning problem.

## Known results in the model

- **Predictive control.** The finite-horizon optimal control of an MLD system is an MIQP or MILP, and with a terminal equality constraint the receding horizon law makes the state converge to the equilibrium when the first problem is feasible (Bemporad and Morari 1999). See [hybrid MPC](/hybrid-mpc/) and the [MPC stability theorem](/mpc-stability-theorem/).
- **Equivalence.** MLD and PWA systems describe the same input and state behaviors under the conditions of Heemels, De Schutter and Bemporad (2001), so the hardness results for PWA systems also hold here: asymptotic stability is NP-hard to decide even for two half spaces (Blondel and Tsitsiklis 1999), see [piecewise affine system](/piecewise-affine-system/).
- **Observability and controllability.** Bemporad, Ferrari-Trecate and Morari (2000) reduced these questions for MLD and PWA systems to mixed-integer linear programs.
- **Modeling tools.** The HYSDEL language (Torrisi and Bemporad 2004) takes a description with logic, automata, events and linear dynamics and generates the MLD matrices, with the big-M constants computed from the given bounds.
- **Explicit solutions.** The optimal input of the finite-horizon problem is a piecewise affine function of the state, and it can be computed offline by multiparametric mixed-integer programming or dynamic programming (Borrelli, Bemporad and Morari 2017, Chapters 16 and 17). See [explicit MPC](/explicit-mpc/).

## References
