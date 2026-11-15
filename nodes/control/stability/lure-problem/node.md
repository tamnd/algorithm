---
tag: EEFXSJ
kind: problem
slug: lure-problem
name: Lur'e problem
aliases:
- absolute stability problem
- Lurie problem
area: control/stability
level: advanced
summary: Decide whether a linear system in feedback with any static nonlinearity in a given sector is globally asymptotically stable.
prereqs: [feedback-control-loop, lyapunov-function]
see_also: [circle-criterion, popov-criterion, kalman-yakubovich-popov-lemma, describing-function, absolute-stability, small-gain-theorem, quadratic-stability, switched-system]
sources:
  - paper: "A. I. Lur'e and V. N. Postnikov, On the theory of stability of control systems, Prikladnaya Matematika i Mekhanika 8(3), 246-248, 1944"
    title: A. I. Lur'e and V. N. Postnikov, On the theory of stability of control systems, 1944
    locator: the feedback form of a linear system and one nonlinearity, and a Lyapunov function of quadratic form plus an integral of the nonlinearity
  - paper: "M. A. Aizerman, On a problem concerning the stability in the large of dynamical systems, Uspekhi Matematicheskikh Nauk 4(4), 187-188, 1949"
    title: M. A. Aizerman, On a problem concerning the stability in the large of dynamical systems, 1949
    locator: the conjecture that the Hurwitz sector of the linear gains is the sector of absolute stability
  - paper: doi:10.1109/TAC.1966.1098369
    title: R. E. Fitts, Two counterexamples to Aizerman's conjecture, IEEE Transactions on Automatic Control 11(3), 553-556, 1966
    locator: fourth-order examples with periodic solutions found by simulation
  - paper: "R. E. Kalman, Physical and mathematical mechanisms of instability in nonlinear automatic control systems, Transactions of the ASME 79(3), 553-566, 1957"
    title: R. E. Kalman, Physical and mathematical mechanisms of instability in nonlinear automatic control systems, 1957
    locator: the conjecture with the slope of the nonlinearity in the Hurwitz sector
  - paper: doi:10.1137/0306007
    title: G. Zames and P. L. Falb, Stability conditions for systems with monotone and slope-restricted nonlinearities, SIAM Journal on Control 6(1), 89-108, 1968
    locator: the multipliers for monotone and slope-restricted nonlinearities
  - paper: doi:10.1016/S0005-1098(00)00050-9
    title: Vincent D. Blondel and John N. Tsitsiklis, A survey of computational complexity results in systems and control, Automatica 36(9), 1249-1274, 2000
    locator: the survey of complexity results for stability questions
  - paper: doi:10.1142/S0218127413300024
    title: G. A. Leonov and N. V. Kuznetsov, Hidden attractors in dynamical systems, International Journal of Bifurcation and Chaos 23(1), 1330002, 2013
    locator: the survey of the Aizerman and Kalman problems, their counterexamples and hidden oscillations
  - paper: doi:10.1109/81.486446
    title: E. S. Pyatnitskiy and L. B. Rapoport, Criteria of asymptotic stability of differential inclusions and periodic motions of time-varying nonlinear control systems, IEEE Transactions on Circuits and Systems I 43(3), 219-229, 1996
    locator: the exact test for second-order systems with a time-varying sector nonlinearity
  - paper: doi:10.1109/9.587335
    title: Alexandre Megretski and Anders Rantzer, System analysis via integral quadratic constraints, IEEE Transactions on Automatic Control 42(6), 819-830, 1997
    locator: multipliers and integral quadratic constraints for sector and slope bounds, and their LMI tests
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 7.1 (absolute stability, the circle criterion and the Popov criterion)
---

The Lur'e problem asks when a feedback loop of a linear system and one nonlinearity is globally asymptotically stable, if all that is known about the nonlinearity is a sector that bounds its graph. A loop with this property for every nonlinearity in the sector is called absolutely stable. A. I. Lur'e and V. N. Postnikov posed the problem in 1944 for aircraft and engine controllers, where an actuator, a relay or a valve adds a nonlinearity whose exact shape is unknown. The [circle criterion](/circle-criterion/) and the [Popov criterion](/popov-criterion/) are the classic sufficient tests, and the [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/) turns them into matrix tests. The name "absolute stability" has a different meaning in numerical analysis: there, [absolute stability](/absolute-stability/) is a property of an ODE solver on the test equation $y' = \lambda y$, and it has nothing to do with feedback loops or sectors.

## In plain words

A known linear system drives an unknown device, and the device output goes back into the system. The device is not a fixed gain: its output can be any curve that stays between two straight lines through the origin. The question is whether the loop settles to rest from every start, for every such curve. If each straight line in the sector gives a loop that settles, the curved ones often do too, but not always. The problem is to find tests that a computer can check and that prove the answer for all curves at once.

## Definition

**Lur'e system.** A linear part $\dot x = Ax + Bu$, $y = Cx$ with $x \in \mathbb{R}^n$ and scalar $u$ and $y$, with the transfer function $G(s) = C(sI - A)^{-1}B$. The loop is closed by negative feedback through a nonlinearity:

$$u = -\psi(t, y).$$

The function $\psi$ is piecewise continuous in $t$ and locally Lipschitz in $y$, so the solutions are unique.

**Sector.** For $k_1 < k_2$, the nonlinearity is in the sector $[k_1, k_2]$ if

$$k_1 y^2 \ \le\ y\, \psi(t, y) \ \le\ k_2 y^2 \qquad \text{for all } t \ge 0 \text{ and all } y.$$

The graph of $\psi(t, \cdot)$ then lies between the lines of slope $k_1$ and $k_2$. The value $k_2 = \infty$ is allowed, and gives the sector $[k_1, \infty)$. Linear gains $\psi = ky$ with $k \in [k_1, k_2]$ are in the sector.

**Absolute stability.** The loop is absolutely stable for the sector if the origin is globally uniformly asymptotically stable for every nonlinearity $\psi$ in the sector. The Lur'e problem is: given $(A, B, C)$ and $[k_1, k_2]$, decide whether the loop is absolutely stable. There are two versions. In the time-varying version, $\psi$ can depend on $t$. In the time-invariant version, $\psi = \psi(y)$ only.

**A necessary condition.** Since the linear gains are in the sector, absolute stability needs $A - kBC$ to be [Hurwitz](/hurwitz-matrix/) for every $k \in [k_1, k_2]$. The largest interval of such $k$ that contains the sector is the Hurwitz sector, which the [Routh-Hurwitz criterion](/routh-hurwitz-criterion/) or the [Nyquist stability criterion](/nyquist-stability-criterion/) gives.

## Variants

- **Time-varying sector nonlinearity.** Along a solution, $\psi(t, y(t)) = k(t) y(t)$ with $k(t) = \psi(t, y(t))/y(t) \in [k_1, k_2]$. So this version is the same as the uniform asymptotic stability of the linear time-varying loop $\dot x = (A - k(t)BC)x$ for every measurable $k(t) \in [k_1, k_2]$, which is a [switched system](/switched-system/) or linear differential inclusion with the two vertex matrices $A - k_1 BC$ and $A - k_2 BC$.
- **Time-invariant nonlinearity.** $\psi(y)$ has no explicit time dependence. The set of nonlinearities is smaller, so the sector of absolute stability can be larger. The [Popov criterion](/popov-criterion/) uses this.
- **Slope restrictions.** If also $0 \le (\psi(a) - \psi(b))/(a - b) \le k$, as for a saturation, the Zames-Falb multipliers (Zames and Falb 1968) give larger sectors than the Popov criterion.
- **Multivariable sectors.** For vector $u$ and $y$, the sector condition is $(\psi - K_1 y)^T(\psi - K_2 y) \le 0$ with matrices $K_1$ and $K_2$. The circle criterion extends with a matrix transfer function.
- **Discrete time.** $x_{k+1} = Ax_k + Bu_k$ with the same feedback has its own frequency tests, with the unit circle in place of the imaginary axis.

## Examples

**The Aizerman and Kalman conjectures.** Aizerman (1949) conjectured that the Hurwitz sector is always the sector of absolute stability for time-invariant $\psi(y)$. Kalman (1957) made the same conjecture for nonlinearities whose slope stays in the Hurwitz sector, a stronger hypothesis. Both are false in general. Fitts (1966) reported fourth-order examples with a nonlinearity in the Hurwitz sector and a periodic solution found by simulation. The Kalman conjecture is true for $n \le 3$ and false for $n \ge 4$. Leonov and Kuznetsov (2013) survey the counterexamples and their history. The periodic solutions in them are hidden oscillations: they are not found by a [describing function](/describing-function/) analysis or by a simulation that starts near the origin.

**A third-order lag.** Take $G(s) = 1/(s + 1)^3$, with the realization

$$A = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -1 & -3 & -3 \end{bmatrix}, \qquad B = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}, \qquad C = \begin{bmatrix} 1 & 0 & 0 \end{bmatrix}.$$

With $\psi = ky$, the characteristic polynomial is $s^3 + 3s^2 + 3s + 1 + k$. The Routh test gives the Hurwitz sector $(-1, 8)$: the loop needs $1 + k > 0$ and $9 > 1 + k$. At $k = 8$ the polynomial is $(s + 3)(s^2 + 3)$, with poles $\pm j\sqrt 3$. The [Nyquist plot](/nyquist-plot/) has $G(j\sqrt 3) = -1/8$ and $\operatorname{Re} G(j\omega) = (1 - 3\omega^2)/(1 + \omega^2)^3$, with the minimum $-1/4$ at $\omega = 1$. The tests give:
- Small gain: $\|G\|_\infty = 1$ at $\omega = 0$, so the [small-gain theorem](/small-gain-theorem/) covers the sector $[-k, k]$ for $k < 1$.
- Circle criterion: $\operatorname{Re} G(j\omega) > -1/\beta$ for all $\omega$ if and only if $\beta < 4$, so it covers $[0, \beta]$ for $\beta < 4$, also for time-varying $\psi$.
- Popov criterion: for time-invariant $\psi(y)$ it covers $[0, k]$ for every $k < 8$, as the [Popov criterion](/popov-criterion/) page shows. So for this $G$ and the sectors $[0, k]$, the Aizerman conjecture holds.

**Time-varying versus time-invariant.** Take $\ddot y + 0.2\dot y + \psi(t, y) = 0$, so $G(s) = 1/(s^2 + 0.2s)$, with $\psi$ in the sector $[1, 9]$. Every constant gain $k > 0$ gives the Hurwitz polynomial $s^2 + 0.2s + k$, and every time-invariant $\psi(y)$ in the sector gives a globally asymptotically stable loop, with the Lyapunov function $\frac{1}{2}\dot y^2 + \int_0^y \psi(\sigma)\, d\sigma$ and the [LaSalle invariance principle](/lasalle-invariance-principle/). But the time-varying gain $k(t) = 1$ when $y \dot y > 0$ and $k(t) = 9$ when $y \dot y < 0$ makes the solution grow. From $y = 0$, $\dot y = 1$, the solution reaches $\dot y = 0$ at $y = 0.86260$ after 1.47804 s with $k = 1$, and comes back to $y = 0$ with $|\dot y| = 2.45299$ after 0.53501 s more with $k = 9$. Each half swing multiplies the speed at $y = 0$ by $2.45299$, so the loop is not absolutely stable for time-varying $\psi$. The soft spring when the mass moves out and the stiff spring when it moves back pump energy into the loop.

## Known algorithms

- **[Circle criterion](/circle-criterion/).** A test on the Nyquist plot of $G$: the plot must avoid a disk set by $k_1$ and $k_2$. It is sufficient for the time-varying version. By the [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/) it is the same as a [linear matrix inequality](/linear-matrix-inequality/) of size $(n + 1) \times (n + 1)$ in a symmetric $P$, with $n(n + 1)/2$ unknowns, which gives the quadratic Lyapunov function $x^T P x$.
- **[Popov criterion](/popov-criterion/).** For time-invariant $\psi(y)$: the Popov plot must lie to the right of a line through $-1/k$. The Lyapunov function is $x^T P x$ plus an integral of $\psi$. The LMI is affine in $P$ and the Popov multiplier $\eta$ together, so it has $n(n + 1)/2 + 1$ unknowns.
- **Multipliers and integral quadratic constraints.** Zames-Falb multipliers for slope-restricted nonlinearities, and the integral quadratic constraints of Megretski and Rantzer (1997), give larger certified sectors with larger LMIs. All of them are solved by [semidefinite programming](/semidefinite-programming/).
- **Exact tests for $n = 2$.** For second-order systems with a time-varying sector nonlinearity, Pyatnitskiy and Rapoport (1996) give a necessary and sufficient test, in terms of the worst switching law.
- **Search for periodic solutions.** The [describing function](/describing-function/) method predicts a [limit cycle](/limit-cycle/) when the Nyquist plot meets $-1/N(a)$. It is a heuristic in both directions: it can predict a limit cycle that does not exist, and it can miss one, as for the hidden oscillations in the counterexamples to the Aizerman conjecture.

## Bounds

For a fixed $G$ and the sectors $[0, k]$, the certified values of $k$ are ordered:

$$k_{\text{circle}} \ \le\ k_{\text{Popov}} \ \le\ k_{\text{abs}} \ \le\ k_{\text{Hurwitz}}.$$

Here $k_{\text{abs}}$ is the true limit of absolute stability for time-invariant $\psi$. The first inequality holds because the Popov test with $\eta = 0$ is the circle test. The last one holds because linear gains are in the sector. For $G = 1/(s + 1)^3$ the values are $4$, $8$, $8$ and $8$, with $8$ as a supremum that the Popov test approaches but does not reach. The counterexamples to the Aizerman conjecture are cases with $k_{\text{abs}} < k_{\text{Hurwitz}}$. For the time-varying version, the circle criterion is only a sufficient test too, and the example above shows that the time-varying limit can be far below the Hurwitz sector.

Each LMI test is a convex problem of polynomial size. An interior-point method solves it to a fixed accuracy in time polynomial in $n$. This does not decide the Lur'e problem itself, since the tests are only sufficient. Blondel and Tsitsiklis (2000) survey the computational complexity of related stability questions for systems with switching and uncertain parameters.

## Reductions

- **Loop transformation.** The substitution $\psi_T = \psi - k_1 y$ moves the sector $[k_1, k_2]$ to $[0, k_2 - k_1]$ and replaces $G$ by $G_T = G/(1 + k_1 G)$, with the state matrix $A - k_1 BC$. So it is enough to study sectors $[0, k]$ with a Hurwitz linear part.
- **To linear differential inclusions.** The time-varying version is the stability of $\dot x \in \operatorname{co}\{A - k_1 BC,\ A - k_2 BC\}\, x$. A [common Lyapunov function](/common-lyapunov-function/) for the two vertex matrices proves it. A quadratic one is [quadratic stability](/quadratic-stability/), and since the two vertex matrices differ by the rank one matrix $(k_2 - k_1)BC$, the KYP lemma makes the existence of a common quadratic Lyapunov function, up to boundary cases, the condition of the circle criterion. The discrete-time analog leads to the [joint spectral radius](/joint-spectral-radius/).
- **To the small-gain and passivity theorems.** The sector $[-k, k]$ is a gain bound, so the [small-gain theorem](/small-gain-theorem/) applies. The sector $[0, \infty)$ is a passive static map, so the [passivity theorem](/passivity-theorem/) applies when $G$ is strictly positive real.

## Applications

- **Actuator saturation.** $\operatorname{sat}(y)$ is in the sector $[0, 1]$. A loop that is absolutely stable for $[0, 1]$ stays globally asymptotically stable when the actuator saturates, which is the question behind [anti-windup](/anti-windup/) designs.
- **Relays, dead zones and friction.** These maps are in sectors $[0, k]$ or have slope bounds, and the Popov and Zames-Falb tests apply to them.
- **Neural networks.** The activations $\tanh$ and the logistic function with its center moved to the origin are slope-restricted, with slopes in $[0, 1]$ and $[0, 1/4]$, so sector and multiplier tests certify the stability of recurrent networks and of loops with neural network controllers.
- **Robustness margins.** A sector of absolute stability is a nonlinear version of a [gain margin](/gain-margin/): it says how much the loop gain can vary, in a nonlinear and possibly time-varying way, before the loop can lose stability.

## References
