---
tag: YX5957
kind: model
slug: lpv-system
name: Linear parameter-varying system
aliases:
- LPV system
area: control/robust-and-adaptive-control
level: advanced
summary: A linear system whose matrices depend on a measured time-varying parameter, the model behind systematic gain scheduling.
prereqs: [state-space-representation, linear-time-varying-system, linear-matrix-inequality]
see_also: [gain-scheduling, quadratic-stability, lmi-h-infinity-synthesis, semidefinite-programming, linear-fractional-transformation, bounded-real-lemma, switched-system, structured-singular-value]
sources:
  - paper: doi:10.1016/0005-1098(91)90116-J
    title: Jeff S. Shamma and Michael Athans, Guaranteed properties of gain scheduled control for linear parameter-varying plants, Automatica 27(3), 559-564, 1991
    locator: the LPV plant model and the result that frozen-parameter designs keep their properties when the parameter varies slowly enough
  - paper: doi:10.1016/0167-6911(94)90102-3
    title: Andy Packard, Gain scheduling via linear fractional transformations, Systems and Control Letters 22(2), 79-92, 1994
    locator: plants and controllers that depend on the parameter through an LFT, and the LMI synthesis conditions with scalings
  - paper: doi:10.1016/0005-1098(95)00038-X
    title: Pierre Apkarian, Pascal Gahinet and Greg Becker, Self-scheduled H-infinity control of linear parameter-varying systems, a design example, Automatica 31(9), 1251-1261, 1995
    locator: polytopic LPV plants, the vertex LMIs with one common Lyapunov matrix, and the controller as a convex combination of vertex controllers
  - paper: doi:10.1109/9.384219
    title: Pierre Apkarian and Pascal Gahinet, A convex characterization of gain-scheduled H-infinity controllers, IEEE Transactions on Automatic Control 40(5), 853-864, 1995
    locator: LMI conditions for gain-scheduled H-infinity controllers of plants with LFT parameter dependence
  - paper: "doi:10.1002/(sici)1099-1239(199611)6:9/10<983::aid-rnc263>3.0.co;2-c"
    title: Fen Wu, Xin Hua Yang, Andy Packard and Greg Becker, Induced L2-norm control for LPV systems with bounded parameter variation rates, International Journal of Robust and Nonlinear Control 6(9-10), 983-998, 1996
    locator: parameter-dependent Lyapunov matrices, the rate-bounded analysis and synthesis LMIs, and their solution on a parameter grid
  - paper: doi:10.1016/S0005-1098(00)00058-3
    title: Wilson J. Rugh and Jeff S. Shamma, Research on gain scheduling, Automatica 36(10), 1401-1425, 2000
    locator: survey of LPV models, quasi-LPV models and LPV synthesis methods
  - paper: "Lawrence Markus and Hidehiko Yamabe, Global stability criteria for differential systems, Osaka Mathematical Journal 12(2), 305-317, 1960"
    locator: the time-varying linear system with constant frozen eigenvalues in the left half plane and growing solutions
---

A linear parameter-varying (LPV) system is a linear state model whose matrices are known functions of a parameter vector $\rho(t)$. The parameter is not known in advance, but it is measured in real time, and it stays in a known set, often with a known bound on its rate. Shamma and Athans used the model to analyze [gain scheduling](/gain-scheduling/) (Shamma and Athans 1991). For a fixed parameter trajectory an LPV system is a [linear time-varying system](/linear-time-varying-system/); for a fixed parameter value it is a linear time-invariant system. The model asks for properties that hold for every admissible trajectory, and it makes possible controllers that are scheduled on $\rho$ by design, with [linear matrix inequalities](/linear-matrix-inequality/) (Packard 1994; Apkarian, Gahinet and Becker 1995).

## The machine

**Parameter set.** A compact set $\mathcal{P} \subset \mathbb{R}^q$ of parameter values, and optionally rate bounds $|\dot\rho_i| \le \nu_i$. An admissible trajectory is a function $\rho : [0, \infty) \to \mathcal{P}$, piecewise continuous, or continuously differentiable with $\dot\rho$ in the rate bounds when these are given.

**Dynamics.** Matrix functions $A(\rho)$, $B(\rho)$, $C(\rho)$, $D(\rho)$, continuous on $\mathcal{P}$, define

$$\dot x(t) = A(\rho(t))\,x(t) + B(\rho(t))\,u(t), \qquad y(t) = C(\rho(t))\,x(t) + D(\rho(t))\,u(t).$$

**Information.** The controller can use $\rho(t)$ at time $t$, but not its future values. This separates an LPV system from an uncertain system, where the parameter is not measured, and from a linear time-varying system, where the whole function of time is known in advance.

**Common forms of the parameter dependence.**

- *Affine:* $A(\rho) = A_0 + \rho_1 A_1 + \cdots + \rho_q A_q$, with $\mathcal{P}$ a box or a polytope.
- *Polytopic:* the system matrix $\begin{bmatrix} A(\rho) & B(\rho) \\ C(\rho) & D(\rho) \end{bmatrix}$ lies in the convex hull of $N$ vertex matrices, with known convex coordinates $\alpha_i(t)$. An affine system on a box of $q$ parameters is polytopic with $N = 2^q$.
- *LFT:* the system is a [linear fractional transformation](/linear-fractional-transformation/) of a constant system and the block $\mathrm{diag}(\rho_1 I_{r_1}, \ldots, \rho_q I_{r_q})$. This covers rational dependence, and it has the same form as the repeated scalar blocks of the [structured singular value](/structured-singular-value/).

**Example.** A mass with a spring of varying stiffness and a damper, $\dot x_1 = x_2$, $\dot x_2 = -\rho\,x_1 - c\,x_2 + u$, with $\rho \in [0.5, 1.5]$ and $c > 0$, is affine with one parameter and two vertices.

## What it counts

- **Stability over all trajectories.** The basic question is whether $\dot x = A(\rho(t))\,x$ is uniformly exponentially stable for every admissible $\rho$. Because the set of trajectories is infinite, the tests are sufficient conditions in the form of LMIs, and their cost is the size of the [semidefinite program](/semidefinite-programming/).
- **Worst-case induced gain.** The performance measure is the induced $L_2$ gain from $w$ to $z$, the supremum of $\|z\|_2/\|w\|_2$ over all inputs and all admissible trajectories, with $x(0) = 0$. For a constant parameter it reduces to the [H-infinity norm](/h-infinity-norm/) at that value, and in general it can be larger than the largest of these norms, or infinite, as the resonance example below shows.
- **SDP size.** For quadratic stability of an affine system on a box (next section), the SDP has $n(n+1)/2$ variables and $2^q + 1$ blocks of size $n$. For polytopic H-infinity synthesis it has the $n(n+1) + 1$ variables of the [LMI synthesis](/lmi-h-infinity-synthesis/) for one plant and two LMI blocks per vertex plus one coupling block. Interior-point methods solve such an SDP to accuracy $\varepsilon$ in time polynomial in the size and $\log(1/\varepsilon)$, if the problem is strictly feasible and the solutions are bounded. The number of vertices, $2^q$, grows exponentially with the number of parameters, so the size is the limit in practice.

## Relation to other models

- **LTI systems** are LPV systems with one parameter value. Each frozen value $\rho_0$ gives the LTI system $(A(\rho_0), B(\rho_0), C(\rho_0), D(\rho_0))$, the object of classical [gain scheduling](/gain-scheduling/).
- **LTV systems.** Each admissible trajectory gives a [linear time-varying system](/linear-time-varying-system/). An LPV property is a property of the whole family.
- **Quasi-LPV systems.** If the parameter is a function of the state, $\rho = \rho(x)$, a nonlinear system can be written in LPV form, for example $\dot x = A(\rho(x))\,x$. The LPV analysis still applies, because the actual trajectory is one of the admissible ones, but it ignores the link between $\rho$ and $x$ and can be conservative (Rugh and Shamma 2000).
- **Uncertain systems.** If $\rho$ is not measured, the same model with a constant or slowly varying $\rho$ is a parametric uncertainty model. The analysis tests for LPV systems then still hold, but the controller cannot use $\rho$.
- **Switched systems.** A [switched linear system](/switched-system/) is an LPV system whose parameter takes a finite set of values and jumps. Polytopic LPV analysis with no rate bound also covers all switching signals among the vertices.

## Known results in the model

- **Frozen stability is not enough** (theorem, by counterexample). Take the Markus-Yamabe matrix with parameter $\rho \in [0, 2\pi]$:
  $$A(\rho) = \begin{bmatrix} -1 + 1.5\cos^2 \rho & 1 - 1.5 \sin\rho \cos\rho \\ -1 - 1.5 \sin\rho \cos\rho & -1 + 1.5 \sin^2 \rho \end{bmatrix}.$$
  For every frozen $\rho$, $\mathrm{tr}\,A = -0.5$ and $\det A = 0.5$, so $A(\rho)$ is Hurwitz with eigenvalues $-0.25 \pm 0.661j$. But along the trajectory $\rho(t) = t$ modulo $2\pi$, with rate 1 (the reset at $2\pi$ does not change $A$), the solution $x(t) = e^{t/2}(\cos t, -\sin t)$ grows without bound (Markus and Yamabe 1960).
- **Slow variation** (theorem; Shamma and Athans 1991). If the frozen closed loops are exponentially stable uniformly over $\mathcal{P}$ and the matrices are smooth enough, the LPV closed loop is exponentially stable for all trajectories with a small enough rate. The proof gives a rate bound, but it is usually conservative.
- **Parametric resonance** (measurement). In the spring example with $c = 0.1$, every frozen system $s^2 + 0.1 s + \rho$ is Hurwitz with real part $-0.05$. With $u = 0$ and $\rho(t) = 1 + 0.5\cos 2t$, whose rate is at most 1, the monodromy matrix over one period $\pi$ has spectral radius $1.26255$, so the solutions grow like $e^{0.0742\,t}$. With the slow trajectory $\rho(t) = 1 + 0.5\cos 0.2t$, the spectral radius over one period $10\pi$ is $0.20788$, a decay like $e^{-0.05\,t}$. For $\rho(t) = 1 + a\cos 2t$ the growth starts near $a = 0.2$. The numbers come from a fourth order Runge-Kutta integration of the two columns of the monodromy matrix.
- **Quadratic stability** (theorem). If one matrix $P > 0$ satisfies $A(\rho)^T P + P A(\rho) < 0$ for all $\rho \in \mathcal{P}$, then $V = x^T P x$ proves exponential stability for every trajectory, with no rate bound. For affine or polytopic dependence it is enough to check the vertices ([quadratic stability](/quadratic-stability/)). In the spring example with $c = 1$, $P = \begin{bmatrix} 1 & 1/4 \\ 1/4 & 1 \end{bmatrix}$ gives $A^T P + P A = \begin{bmatrix} -\rho/2 & 3/4 - \rho \\ 3/4 - \rho & -3/2 \end{bmatrix}$, which is negative definite exactly when $3\rho/4 > (\rho - 3/4)^2$, true at both vertices $0.5$ and $1.5$. For $c = 0.1$ no such $P$ exists, because the resonant trajectory above would contradict it.
- **Parameter-dependent Lyapunov functions** (theorem; Wu, Yang, Packard and Becker 1996). With rate bounds, $V = x^T P(\rho)\,x$ with $P(\rho) > 0$ proves exponential stability for all trajectories within the rate bounds if $A(\rho)^T P(\rho) + P(\rho) A(\rho) + \sum_i \pm \nu_i\,\partial P/\partial\rho_i < 0$ for all $\rho$ and all sign choices. This is less conservative than one fixed $P$. The condition is an infinite family of LMIs; in practice $P(\rho)$ is a combination of chosen basis functions and the LMIs are imposed on a grid, so they must be checked again between the grid points.
- **Quadratic H-infinity performance** (theorem). If one $X > 0$ satisfies the [bounded real lemma](/bounded-real-lemma/) LMI for level $\gamma$ at every $\rho \in \mathcal{P}$, the induced $L_2$ gain is below $\gamma$ for all trajectories.
- **Polytopic synthesis** (theorem; Apkarian, Gahinet and Becker 1995). If $B_2$, $C_2$, $D_{12}$ and $D_{21}$ do not depend on $\rho$ (this can be arranged with input and output filters) and $D_{22} = 0$, a controller of plant order with quadratic H-infinity performance $\gamma$ exists if the LMI synthesis conditions hold at all vertices with one common pair of Lyapunov matrices. The controller is $\sum_i \alpha_i(t)\,K_i$, the same convex combination of vertex controllers as the plant.
- **LFT synthesis** (theorem; Packard 1994; Apkarian and Gahinet 1995). For LFT dependence, the controller also depends on $\rho$ through an LFT, and the conditions are LMIs in Lyapunov matrices and in scalings that commute with the parameter block, as in the D scalings of mu.
- **Conservatism.** All these tests allow every trajectory in the set, including ones that the physical parameter cannot follow. A quadratic test with no rate bound treats the parameter as if it could jump.

## References
