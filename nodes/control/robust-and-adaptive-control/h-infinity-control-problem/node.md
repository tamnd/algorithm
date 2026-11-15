---
tag: CA67B6
kind: problem
slug: h-infinity-control-problem
name: H-infinity control problem
aliases:
- H-infinity synthesis
- H-infinity optimal control
area: control/robust-and-adaptive-control
level: advanced
summary: Find an internally stabilizing controller that makes the H-infinity norm of the closed loop from disturbances to errors less than a given gamma, or the least such gamma.
model: real-ram
prereqs: [h-infinity-norm, linear-fractional-transformation, stabilizability]
see_also: [dgkf-h-infinity-synthesis, lmi-h-infinity-synthesis, mixed-sensitivity-design, h-infinity-loop-shaping, youla-parametrization, h2-optimal-control, small-gain-theorem, dk-iteration]
sources:
  - paper: doi:10.1109/TAC.1981.1102603
    title: George Zames, Feedback and optimal sensitivity, model reference transformations, multiplicative seminorms, and approximate inverses, IEEE Transactions on Automatic Control 26(2), 301-320, 1981
    locator: the problem of minimizing a weighted sensitivity in the H-infinity norm
  - paper: doi:10.1109/9.29425
    title: John C. Doyle, Keith Glover, Pramod P. Khargonekar and Bruce A. Francis, State-space solutions to standard H2 and H-infinity control problems, IEEE Transactions on Automatic Control 34(8), 831-847, 1989
    locator: the standard problem, its assumptions, and the solution by two Riccati equations
  - paper: doi:10.1002/rnc.4590040403
    title: Pascal Gahinet and Pierre Apkarian, A linear matrix inequality approach to H-infinity control, International Journal of Robust and Nonlinear Control 4(4), 421-448, 1994
    locator: the solvability conditions as LMIs without rank assumptions on D12 and D21
  - paper: doi:10.1016/0005-1098(94)90110-4
    title: Tetsuya Iwasaki and Robert E. Skelton, All controllers for the general H-infinity control problem, LMI existence conditions and state space formulas, Automatica 30(8), 1307-1317, 1994
    locator: the LMI existence conditions and the formulas for all controllers
  - paper: doi:10.1137/S0363012994272630
    title: Vincent D. Blondel and John N. Tsitsiklis, NP-hardness of some linear control design problems, SIAM Journal on Control and Optimization 35(6), 2118-2127, 1997
    locator: the NP-hardness of stabilization by static output feedback with bounds on the gains, of simultaneous stabilization and of decentralized control
  - paper: doi:10.1016/0005-1098(93)90122-A
    title: Huibert Kwakernaak, Robust control and H-infinity optimization, tutorial paper, Automatica 29(2), 255-273, 1993
    locator: the mixed sensitivity problem, its reduction to the standard problem, and the polynomial solution methods
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 16, H-infinity Control, Simple Case, and Chapter 17, H-infinity Control, General Case
  - book: isbn:9780470011683
    title: Sigurd Skogestad and Ian Postlethwaite, Multivariable Feedback Control, Analysis and Design, second edition, Wiley, 2005
    locator: Section 9.3, H2 and H-infinity control, with mixed sensitivity and signal based design
---

The H-infinity control problem asks for a controller that keeps the worst-case energy gain from disturbances to errors below a given level. The plant is a generalized plant $P$ with two inputs (the disturbance $w$ and the control $u$) and two outputs (the error $z$ and the measurement $y$). The controller $K$ closes the loop from $y$ to $u$, and the closed loop is the lower [linear fractional transformation](/linear-fractional-transformation/) $T_{zw} = \mathcal{F}_l(P, K)$. The suboptimal problem fixes $\gamma > 0$ and asks for an internally stabilizing $K$ with $\|T_{zw}\|_\infty < \gamma$, where $\|\cdot\|_\infty$ is the [H-infinity norm](/h-infinity-norm/). The optimal problem asks for the infimum $\gamma_{\rm opt}$ over all such $K$. Zames (1981) posed the problem. For finite-dimensional linear plants and controllers of any order, it is solved exactly by two Riccati equations ([two-Riccati synthesis](/dgkf-h-infinity-synthesis/)) or by linear matrix inequalities ([LMI synthesis](/lmi-h-infinity-synthesis/)). If the order or the structure of the controller is fixed, the problem becomes nonconvex, and some of its forms are NP-hard.

## In plain words

You have a machine that disturbances push around, and you have a list of errors that you want small. You measure some signals and you choose a controller that acts on them. A disturbance of a given energy can come at any frequency and in any direction. You want a guarantee that the energy of the errors is never more than $\gamma$ times the energy of the disturbance, however the disturbance looks. The problem is to find such a controller, or to show that none exists. The least $\gamma$ that you can reach is the best guarantee. Because the guarantee is worst case, it also gives robustness: by the small gain theorem, the loop stays internally stable when an unknown system with gain below $1/\gamma$ is connected from $z$ to $w$.

## Definition

**Input.** A generalized plant with state $x \in \mathbb{R}^n$:

$$\dot x = A x + B_1 w + B_2 u, \qquad z = C_1 x + D_{11} w + D_{12} u, \qquad y = C_2 x + D_{21} w + D_{22} u,$$

with $w \in \mathbb{R}^{m_1}$, $u \in \mathbb{R}^{m_2}$, $z \in \mathbb{R}^{p_1}$ and $y \in \mathbb{R}^{p_2}$, and a level $\gamma > 0$ for the suboptimal problem.

**Controllers.** A controller is a finite-dimensional linear time-invariant system $K$ with input $y$ and output $u$, wired as $u = K y$. The closed loop must be well posed ($I - D_{22} K(\infty)$ invertible) and internally stable: every state of the plant and of the controller goes to 0 for zero inputs, which for a stabilizable and detectable realization means that the closed loop $A$ matrix is Hurwitz. A stabilizing controller exists if and only if $(A, B_2)$ is [stabilizable](/stabilizability/) and $(C_2, A)$ is [detectable](/detectability/) (Zhou, Doyle and Glover 1996, chapter 12).

**Questions.**

- *Suboptimal problem:* decide whether some internally stabilizing $K$ gives $\|\mathcal{F}_l(P, K)\|_\infty < \gamma$, and if so, find one.
- *Optimal problem:* compute $\gamma_{\rm opt} = \inf_K \|\mathcal{F}_l(P, K)\|_\infty$ over all internally stabilizing $K$.

Here $\|T\|_\infty = \sup_\omega \bar\sigma(T(j\omega))$, which equals the induced L2 gain $\sup_{w \ne 0} \|z\|_2/\|w\|_2$ for $T \in RH_\infty$. The infimum is not always reached: in the singular example below, no controller reaches it. At $\gamma = \gamma_{\rm opt}$ the controller formulas of the two-Riccati method break down, so practical tools solve the suboptimal problem at a level a little above $\gamma_{\rm opt}$.

**Sign convention.** The loop $u = K y$ is the one of the standard references. The classical loop uses negative feedback, $e = r - y$ and $u = C e$. If the generalized plant gives the controller the error $e$ as its measurement, then $K = C$. If it gives the plant output $y$, then $K = -C$.

## Variants

- **State feedback and full information.** If $y = x$, or $y = (x, w)$, the problem has a solution with one Riccati equation and a static gain.
- **Mixed sensitivity.** The error is a stack of weighted closed loop maps, such as $W_1 S$, $W_2 K S$ and $W_3 T$ ([mixed sensitivity design](/mixed-sensitivity-design/)).
- **Robust stabilization of coprime factors.** A special case with a closed form for $\gamma_{\rm opt}$ and no bisection ([H-infinity loop shaping](/h-infinity-loop-shaping/)).
- **Structured uncertainty.** If the worst case is taken over a block diagonal uncertainty, the problem becomes mu-synthesis, which is not convex ([D-K iteration](/dk-iteration/)).
- **Fixed order or fixed structure.** The controller has a given order below $n$, a given sparsity (decentralized control), or a fixed form such as a PID controller. These forms are nonconvex in general.
- **Discrete time.** The same problem for $x_{k+1} = A x_k + \ldots$ with the H-infinity norm on the unit circle.
- **Mixed H2 and H-infinity.** Minimize an [H2 norm](/h2-optimal-control/) of one channel subject to an H-infinity bound on another; LMI methods give an upper bound with a common Lyapunov matrix.

## Examples

**A scalar plant.** $\dot x = a x + w_1 + u$, $z = (x, u)$, $y = x + w_2$. So $A = a$, $B_1 = [1, 0]$, $B_2 = 1$, $C_1 = [1; 0]$, $D_{12} = [0; 1]$, $C_2 = 1$ and $D_{21} = [0, 1]$. The two-Riccati conditions reduce to one scalar inequality, and $\gamma_{\rm opt} = a + \sqrt{a^2 + 2}$. For $a = 1$ this is $1 + \sqrt 3 = 2.73205$. The [two-Riccati page](/dgkf-h-infinity-synthesis/) derives this value and gives the central controller at $\gamma = 3$, and the [LMI page](/lmi-h-infinity-synthesis/) finds the same value from three LMIs.

**A limit from a right half plane zero.** Let $P(s) = (1 - s)/(1 + s)$, which has its pole at $-1$ and a zero at $s = 1$, and let the weight be $W(s) = (s + 2)/(s + 0.5)$, which is in $RH_\infty$ and has no zeros in the right half plane. The problem is to minimize $\|W S\|_\infty$ over stabilizing $C$, with $S = 1/(1 + P C)$. By the [Youla parametrization](/youla-parametrization/) of a plant in $RH_\infty$, $S = 1 - P Q$ for a free $Q \in RH_\infty$. So $S(1) = 1$ for every stabilizing $C$. The function $W S$ is analytic and bounded in the right half plane, so by the maximum modulus principle

$$\|W S\|_\infty \ge |W(1) S(1)| = |W(1)| = 3/1.5 = 2.$$

The bound is reached. Set $W S = 2$, that is $S = 2(s + 0.5)/(s + 2)$. Then $P Q = 1 - S = (1 - s)/(s + 2)$, so $Q = (s + 1)/(s + 2)$, which is in $RH_\infty$. The controller is $C = Q/S = (s + 1)/(2 s + 1)$. So $\gamma_{\rm opt} = 2$ for this problem, and $|S(j\omega)| = 2/|W(j\omega)|$ at every frequency. The weight asks for $|S| \le 1/4$ at low frequency, but the zero at $s = 1$ allows only $|S(0)| = 1/2$.

**A non-example.** For the plant $\dot x = x + w + u$, $z = x$, $y = x$ (no weight on $u$), $D_{12} = 0$ and the two-Riccati formulas do not apply. The problem is still well defined: high gain feedback $u = -k x$ gives $T_{zw} = 1/(s + k - 1)$ with norm $1/(k - 1)$, so $\gamma_{\rm opt} = 0$, and it is not reached by any controller. This is a singular problem.

## Known algorithms

- **Two-Riccati synthesis** (Doyle, Glover, Khargonekar and Francis 1989): for a fixed $\gamma$, decides the suboptimal problem exactly with two Riccati equations of size $n$ and a coupling condition, under rank and normalization assumptions on $D_{12}$ and $D_{21}$. A bisection on $\gamma$ gives $\gamma_{\rm opt}$. See [two-Riccati H-infinity synthesis](/dgkf-h-infinity-synthesis/).
- **LMI synthesis** (Gahinet and Apkarian 1994; Iwasaki and Skelton 1994): three LMIs in two symmetric $n \times n$ matrices decide the suboptimal problem with no rank assumptions; minimizing $\gamma$ subject to them is one [semidefinite program](/semidefinite-programming/). See [LMI-based H-infinity synthesis](/lmi-h-infinity-synthesis/).
- **Frequency domain methods.** The early solutions used the Youla parametrization to reduce the problem to model matching, and then Nehari or Nevanlinna-Pick interpolation, or polynomial equations (Kwakernaak 1993). They gave high-order controllers and are now mostly of historical and teaching interest.
- **Fixed-structure methods.** For a fixed order or structure, nonsmooth local optimization of the closed loop norm is used. These methods give only local optima, with no guarantee.

## Bounds

- **Order.** If some controller of any order reaches $\|T_{zw}\|_\infty < \gamma$, then one of order $n$ does: the central controller of the two-Riccati solution, or the controller of the LMI solution (theorem; Zhou, Doyle and Glover 1996, chapters 16 and 17).
- **Cost of the full order problem.** In the real-RAM model, one test of the two-Riccati conditions costs $O(n^3 + n^2(m_1 + m_2 + p_1 + p_2))$ flops with a Schur-based Riccati solver, which is itself iterative (the QR algorithm). The LMI form is an SDP with $n(n + 1) + 1$ scalar variables and three blocks of size at most $\max(2n, n + m_1 + p_1)$. An interior point method solves it to accuracy $\epsilon$ in time polynomial in the size and $\log(1/\epsilon)$, under strict feasibility. See [semidefinite programming](/semidefinite-programming/).
- **Lower bounds from interpolation.** If a scalar plant has a zero $z_0$ in the open right half plane, internal stability forces $S(z_0) = 1$. If it has a pole $p_0$ there, it forces $T(p_0) = 1$. For a weight $W \in RH_\infty$, every stabilizing controller then gives $\|W S\|_\infty \ge |W(z_0)|$ and $\|W T\|_\infty \ge |W(p_0)|$, by the maximum modulus principle, as in the example (theorem).
- **Hardness of structured forms.** Stabilization by static output feedback with bounds on the gains, simultaneous stabilization, and decentralized stabilization are [NP-hard](/np-hard/) (Blondel and Tsitsiklis 1997). With $B_1 = 0$ and $C_1 = 0$ every stabilizing controller gives $T_{zw} = 0$, so the H-infinity problem with the same controller structure contains these problems and is NP-hard as well.

## Reductions

- **From robust stabilization.** By the [small gain theorem](/small-gain-theorem/), the loop with an unknown $\Delta \in RH_\infty$ from $z$ to $w$ is internally stable for all $\|\Delta\|_\infty \le 1/\gamma$ when $\|T_{zw}\|_\infty < \gamma$. So robust stabilization against an unstructured [model uncertainty](/model-uncertainty/) is an H-infinity problem.
- **To model matching.** With the Youla parametrization, $T_{zw} = T_1 - T_2 Q T_3$ with fixed $T_i \in RH_\infty$ and a free $Q \in RH_\infty$. The problem becomes $\min_Q \|T_1 - T_2 Q T_3\|_\infty$, which is convex in $Q$ but infinite dimensional.
- **General D matrices.** Loop shifting moves $D_{22}$ into the controller and scales $D_{12}$ and $D_{21}$, which gives the normalized form of the two-Riccati method (Zhou, Doyle and Glover 1996, chapter 17).
- **From H2.** As $\gamma \to \infty$ the central controller tends to the H2 optimal controller, which is the [LQG](/lqg-control/) controller for the same plant.

## Applications

- Robust stabilization against unmodeled dynamics, with a weighted multiplicative or additive uncertainty model.
- Disturbance rejection and tracking with frequency weights on the sensitivity, the control sensitivity and the complementary sensitivity.
- Robust stabilization with a loop shape chosen by the designer ([H-infinity loop shaping](/h-infinity-loop-shaping/)).
- The K-step of mu-synthesis for structured uncertainty ([D-K iteration](/dk-iteration/)).

## References
