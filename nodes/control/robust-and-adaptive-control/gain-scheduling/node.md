---
tag: 4JNB6P
kind: technique
slug: gain-scheduling
name: Gain scheduling
aliases:
- scheduled control
area: control/robust-and-adaptive-control
level: core
summary: Designs linear controllers at many operating points of a nonlinear plant and interpolates them by a measured scheduling variable.
prereqs: [jacobian-linearization, equilibrium-point, pid-controller]
see_also: [lpv-system, lmi-h-infinity-synthesis, linear-time-varying-system, quadratic-stability, adaptive-control, feedback-linearization, lyapunov-indirect-method, switched-system]
sources:
  - paper: doi:10.1109/9.58498
    title: Jeff S. Shamma and Michael Athans, Analysis of gain scheduled control for nonlinear plants, IEEE Transactions on Automatic Control 35(8), 898-907, 1990
    locator: the conditions under which a scheduled design keeps the properties of the frozen designs, with slow variation of the scheduling variable
  - paper: doi:10.1109/37.165527
    title: Jeff S. Shamma and Michael Athans, Gain scheduling, potential hazards and possible remedies, IEEE Control Systems Magazine 12(3), 101-107, 1992
    locator: examples where frozen designs are good and the scheduled loop fails, and remedies
  - paper: doi:10.1016/S0005-1098(00)00058-3
    title: Wilson J. Rugh and Jeff S. Shamma, Research on gain scheduling, Automatica 36(10), 1401-1425, 2000
    locator: survey of the classical procedure, the linearization property of the scheduled controller, and LPV methods
  - paper: doi:10.1080/002071700411304
    title: Douglas J. Leith and William E. Leithead, Survey of gain-scheduling analysis and design, International Journal of Control 73(11), 1001-1025, 2000
    locator: survey of analysis and design methods, including the velocity-based form
  - paper: "Lawrence Markus and Hidehiko Yamabe, Global stability criteria for differential systems, Osaka Mathematical Journal 12(2), 305-317, 1960"
    locator: the time-varying linear system with constant frozen eigenvalues in the left half plane and growing solutions
  - paper: doi:10.1109/TAC.1969.1099336
    title: Charles A. Desoer, Slowly varying system x' = A(t)x, IEEE Transactions on Automatic Control 14(6), 780-781, 1969
    locator: exponential stability of a slowly varying linear system whose frozen matrices are uniformly Hurwitz
---

Gain scheduling controls a nonlinear plant with a family of linear controllers. The designer picks a scheduling variable that is measured and that says where the plant is operating, such as the speed and altitude of an aircraft or the level in a tank. At several values of this variable the plant is linearized about an [equilibrium](/equilibrium-point/) ([Jacobian linearization](/jacobian-linearization/)), and a linear controller is designed for each point. In operation, the controller gains are interpolated from the measured variable. It is an old and common way to apply linear design to nonlinear plants, and it is widely used in flight control and process control (Rugh and Shamma 2000). It has no general guarantee: the frozen designs say nothing certain about the loop when the scheduling variable moves fast. Shamma and Athans (1990, 1992) gave the conditions and the hazards, and the surveys of Rugh and Shamma (2000) and Leith and Leithead (2000) cover the field.

## In plain words

A plant behaves differently at different operating points. A tank is slow when it is full and fast when it is nearly empty; an aircraft responds to its control surfaces more strongly at high speed. One fixed linear controller is a compromise for all of these. Gain scheduling designs one good linear controller per operating point, then blends them as the operating point changes, using a measured signal that tracks the operating point. It works well when that signal changes slowly compared with the speed of the loop. If it changes fast, the blend can fail even when every single design is good, and the way the controller is built inside matters as much as its gains.

## When it applies

- The plant has a family of equilibria indexed by a variable $\sigma$, and its linearization changes with $\sigma$ enough to hurt a single fixed design.
- The scheduling variable $\sigma$, or a good estimate of it, is measured in real time.
- $\sigma$ varies slowly compared with the closed loop dynamics (rule of thumb; Shamma and Athans 1990). Signals that move with the loop, such as fast states, are poor choices.
- $\sigma$ captures the nonlinearity: at a fixed $\sigma$, the linear model is a good description of the plant near the equilibrium.

## The template

1. **Choose the scheduling variable** $\sigma$, an exogenous signal or a slow measured output.
2. **Compute the equilibrium family.** For each $\sigma$, find $(x_0(\sigma), u_0(\sigma), y_0(\sigma))$ with $f(x_0, u_0) = 0$.
3. **Linearize** at a grid of points $\sigma_1, \ldots, \sigma_N$: $A_i = \partial f/\partial x$, $B_i = \partial f/\partial u$, and so on.
4. **Design** a linear controller $K_i$ for each point with any method: [PID](/pid-controller/) tuning, [pole placement](/pole-placement-problem/), LQR or H-infinity.
5. **Interpolate.** Make the controller parameters functions of $\sigma$, by linear interpolation in a table or by a fitted formula.
6. **Choose the realization.** Build the scheduled controller so that its linearization at each equilibrium equals $K_i$. Gains should multiply signals that are 0 at equilibrium, such as the tracking error, and equilibrium offsets $u_0(\sigma)$ should enter explicitly or through an integrator placed after the gain. The velocity-based form of Leith and Leithead is one systematic way.
7. **Check.** Simulate the nonlinear loop over fast and slow changes of $\sigma$, and if a guarantee is needed, analyze it as an [LPV system](/lpv-system/) with a bound on the rate of $\sigma$.

## Classic examples

**A conical tank.** Let the cross section of a tank grow with the level, $A(h) = h$, with inflow $u$ and outflow $\sqrt h$. Then $\dot h = (u - \sqrt h)/h$. The equilibrium at level $h_0$ has $u_0 = \sqrt{h_0}$, and the linearization is $\delta\dot h = -a\,\delta h + b\,\delta u$ with $a = 1/(2 h_0^{3/2})$ and $b = 1/h_0$. Over the range $h_0 \in [0.25, 4]$, the pole $-a$ moves from $-4$ to $-0.0625$ and the gain $b$ from 4 to $0.25$. With negative feedback, $e = r - h$, a PI controller $u = k_p e + k_i \int e$ gives the characteristic polynomial $s^2 + (a + b k_p) s + b k_i$. To place both closed loop poles at $-1$ at every level, take $k_p(h_0) = (2 - a)/b$ and $k_i(h_0) = 1/b$:

| $h_0$ | $a$ | $b$ | scheduled $k_p$, $k_i$ | poles, scheduled | poles with the fixed gains of $h_0 = 1$ |
|---|---|---|---|---|---|
| 0.25 | 4 | 4 | $-0.5$, $0.25$ | $-1$, $-1$ | $-0.417$, $-9.58$ |
| 1 | 0.5 | 1 | $1.5$, $1$ | $-1$, $-1$ | $-1$, $-1$ |
| 4 | 0.0625 | 0.25 | $7.75$, $4$ | $-1$, $-1$ | $-0.219 \pm 0.450j$ |

The fixed design is slow and oscillatory when the tank is full. The scheduled design, with $\sigma = h$, gives the same linear behaviour at every level (exact, from the polynomial).

**The realization matters.** Build the same scheduled PI controller in two ways, both with $k_p(h)$ and $k_i(h)$ as above and $\sigma = h$:

- *Form A:* $u = k_p(h)\,e + x$, $\dot x = k_i(h)\,e$.
- *Form B:* $u = k_p(h)\,e + k_i(h)\,z$, $\dot z = e$.

With frozen gains the two forms are the same transfer function. Linearize the closed loop at the equilibrium with $e = 0$. In form A every scheduled gain multiplies $e$, so the extra terms $k_p'(h_0)\,e_0\,\delta h$ vanish and the linearization has the designed poles $-1$, $-1$ at every level. In form B the term $k_i'(h_0)\,z_0\,\delta h$ remains, with $z_0 = u_0/k_i(h_0) \ne 0$. It adds the feedback $\delta u = \ldots + (1/\sqrt{h_0})\,\delta h$. The characteristic polynomials become $s^2 - 6 s + 1$ at $h_0 = 0.25$, $s^2 + s + 1$ at $h_0 = 1$ and $s^2 + 1.875 s + 1$ at $h_0 = 4$. So form B makes the equilibrium at $h_0 = 0.25$ unstable, with poles at $3 \pm 2\sqrt 2$, although every frozen design places the poles at $-1$. A finite-difference Jacobian of the nonlinear loop gives the same polynomials (measurement). This is the hidden coupling term that Shamma and Athans (1992) and Rugh and Shamma (2000) warn about.

**Fast scheduling: the Markus-Yamabe system.** Take

$$\dot x = A(t)\,x, \qquad A(t) = \begin{bmatrix} -1 + 1.5\cos^2 t & 1 - 1.5 \sin t \cos t \\ -1 - 1.5 \sin t \cos t & -1 + 1.5 \sin^2 t \end{bmatrix}.$$

For every frozen $t$, $\mathrm{tr}\,A = -0.5$ and $\det A = 0.5$, so the eigenvalues are $-0.25 \pm 0.661j$, in the open left half plane. Yet $x(t) = e^{t/2}(\cos t, -\sin t)$ is a solution, as direct substitution shows, and it grows without bound (Markus and Yamabe 1960). Read $t$ as the scheduling variable: the frozen systems are all exponentially stable, but the parameter moves at a speed comparable to the dynamics, and the loop is unstable. If instead $A$ is replaced by $A(\epsilon t)$ with $\epsilon$ small enough, the system is exponentially stable, because its frozen matrices are uniformly Hurwitz with bounded derivative (Desoer 1969).

## Variations

- **LPV gain scheduling.** Model the plant as a [linear parameter-varying system](/lpv-system/) and design one controller for all parameter values and rates at once, with LMIs (Packard 1994; Apkarian, Gahinet and Becker 1995). This gives a guarantee where the classical method gives none, at the cost of conservatism and design effort.
- **Velocity-based scheduling.** Leith and Leithead differentiate the plant and controller equations so that every point of the state space, not only the equilibria, has a linear model, and the realization question of step 6 disappears.
- **Switching between controllers.** Instead of interpolation, switch between the point designs, with hysteresis and bumpless transfer. Closed loop stability then depends on the switching rate and the dwell time ([switched system](/switched-system/)).
- **Scheduling on an estimated parameter.** If the scheduling variable comes from an online estimator, the scheme becomes a form of [adaptive control](/adaptive-control/).
- **Feedback linearization** removes the nonlinearity exactly instead of scheduling against it, when the model is good enough ([feedback linearization](/feedback-linearization/)).

## Pitfalls

- **Frozen-point analysis is not a proof.** Exponential stability of every frozen linearization does not imply asymptotic stability of the scheduled loop when $\sigma$ varies, as the Markus-Yamabe system shows (theorem by counterexample). Slow enough variation is sufficient (theorem; Desoer 1969; Shamma and Athans 1990), but the required bound on the rate is often small and hard to compute.
- **Scheduling on a fast output.** If $\sigma$ is a state of the loop itself, it varies as fast as the loop, and the slow variation assumption fails exactly when the plant is moving, for example during large steps.
- **Hidden coupling terms.** As in form B above, the way the gains enter can add feedback that no frozen design contains. Check the linearization of the complete scheduled controller at each equilibrium, not only its frozen transfer functions.
- **Equilibrium offsets.** Away from the design points the interpolated $u_0(\sigma)$ is wrong. An integrator in the controller removes the steady error, but only if it sits after the scheduled gain.
- **Too few design points.** The interpolated controller between two points is not designed. Check points in between, especially where the plant changes fast with $\sigma$.

## Exercises

1. For the tank, find $k_p(h_0)$ and $k_i(h_0)$ that place both closed loop poles at $-2$, and say at which level $k_p$ changes sign.
2. Linearize form B at a general $h_0$ and show that the extra term is $k_i'(h_0)\,z_0\,\delta h = h_0^{-1/2}\,\delta h$.
3. Verify by substitution that $x(t) = e^{t/2}(\cos t, -\sin t)$ solves the Markus-Yamabe system, and compute the frozen eigenvalues.
4. Show that the two forms A and B have the same transfer function from $e$ to $u$ when $h$ is held constant.

## References
