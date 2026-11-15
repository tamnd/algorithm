---
tag: 40Y4Z0
kind: technique
slug: jacobian-linearization
name: Linearization about an equilibrium
aliases:
- Jacobian linearization
- small-signal linearization
area: control/modeling-and-identification
level: intro
summary: Replaces a nonlinear system near an equilibrium by the linear system given by the Jacobians of the vector field and the output map.
prereqs: [equilibrium-point, state-space-representation]
see_also: [lyapunov-indirect-method, feedback-linearization, linear-time-varying-system, gain-scheduling, ac-small-signal-analysis, automatic-differentiation, finite-differences, brockett-condition]
sources:
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 2.3, Qualitative Behavior Near Equilibrium Points; Section 4.3, Linear Systems and Linearization (the indirect method); Section 4.6, Linear Time-Varying Systems and Linearization
  - book: isbn:9780134412054
    title: Wilson J. Rugh, Linear System Theory, second edition, Prentice Hall, 1996
    locator: Chapter 2, State Equation Representation (linearization about a nominal solution)
  - paper: doi:10.1090/S0002-9939-1960-0121542-7
    title: Philip Hartman, A lemma in the theory of structural stability of differential equations, Proceedings of the American Mathematical Society 11(4), 610-620, 1960
    locator: the local topological equivalence of a flow and its linearization at a hyperbolic equilibrium
  - paper: "D. M. Grobman, Homeomorphism of systems of differential equations, Doklady Akademii Nauk SSSR 128, 880-881, 1959"
    locator: the same equivalence, found independently
  - book: isbn:9780691193984
    title: Karl J. Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: the chapter on linear systems (linearization of nonlinear models about an equilibrium)
---

Linearization about an equilibrium replaces a nonlinear system $\dot x = f(x, u)$, $y = h(x, u)$ near a rest point $(x^*, u^*)$ by the linear system $\dot{\delta x} = A\, \delta x + B\, \delta u$, $\delta y = C\, \delta x + D\, \delta u$, where $A$, $B$, $C$ and $D$ are the Jacobian matrices of first partial derivatives of $f$ and $h$ at that point, and $\delta x = x - x^*$, $\delta u = u - u^*$, $\delta y = y - y^*$ are the small deviations. It is the first-order Taylor expansion of the equations, the same idea as the small-signal model of a circuit in [AC small-signal analysis](/ac-small-signal-analysis/). The linear model is accurate to second order in the deviation, and at a hyperbolic equilibrium it decides local stability ([Lyapunov's indirect method](/lyapunov-indirect-method/)). It differs from [feedback linearization](/feedback-linearization/), which cancels the nonlinearity exactly by a change of coordinates and feedback, and is valid in a large region.

## In plain words

Most real systems are nonlinear, but most of the tools of control work only for linear systems. If the system works near one operating condition, small changes around that condition behave almost linearly, in the same way that a smooth curve looks like a straight line under a microscope. The method finds the operating condition, measures how sensitive each rate of change is to each state and each input at that point, and keeps only these sensitivities. The result is a linear model of the small deviations from the operating condition. It is reliable for small deviations and for questions about what happens very close to the operating point. It can mislead for large deviations, or when the linear model is on the edge between growth and decay.

## When it applies

- **The point is an equilibrium.** $f(x^*, u^*) = 0$ (see [equilibrium point](/equilibrium-point/)). At a point that is not an equilibrium, the expansion has a constant term $f(x^*, u^*)$, and the result is an affine model, not a linear one. For a moving reference, linearize along the trajectory instead (see Variations).
- **$f$ and $h$ are differentiable at the point.** $C^1$ near $(x^*, u^*)$ gives the Jacobians and a remainder that is $o(\|(\delta x, \delta u)\|)$. $C^2$ gives a remainder of order $\|(\delta x, \delta u)\|^2$. A saturation, a dead zone, Coulomb friction or $|x|$ at its corner has no Jacobian there, and the method does not apply at such a point.
- **The question is local.** The linear model answers questions about small deviations: local stability, local controllability, the response to small inputs, and the design of a controller that keeps the deviations small. It gives no information on the size of the region where these answers hold.
- **The equilibrium is hyperbolic, for stability questions.** If some eigenvalue of $A$ has zero real part, the linear model does not decide stability.

## The template

1. **Find the operating point.** Solve $f(x^*, u^*) = 0$ for the desired $x^*$ or the desired output $y^* = h(x^*, u^*)$. In general there are many solutions, often an $m$-dimensional family parametrized by the input.
2. **Compute the Jacobians.**

   $$A = \frac{\partial f}{\partial x}(x^*, u^*), \quad B = \frac{\partial f}{\partial u}(x^*, u^*), \quad C = \frac{\partial h}{\partial x}(x^*, u^*), \quad D = \frac{\partial h}{\partial u}(x^*, u^*).$$

   Entry $(i, j)$ of $A$ is $\partial f_i / \partial x_j$. Use the formulas when $f$ is known in closed form, [automatic differentiation](/automatic-differentiation/) when $f$ is a program, or [finite differences](/finite-differences/) as a last resort.
3. **Write the deviation model.** With $\delta x = x - x^*$, $\delta u = u - u^*$ and $\delta y = y - y^*$, Taylor's theorem gives

   $$\dot{\delta x} = A\, \delta x + B\, \delta u + r(\delta x, \delta u), \qquad \|r(\delta x, \delta u)\| \le L\, \|(\delta x, \delta u)\|^2$$

   near the point, if $f$ is $C^2$ and $L$ bounds half the second derivatives there. Drop $r$.
4. **Analyze or design on the linear model.** Eigenvalues, controllability, a state feedback $\delta u = -K \delta x$, an observer. The theorem behind step 4 for stability: if $A$ is Hurwitz, $x^*$ is locally exponentially stable for the nonlinear system; if $A$ has an eigenvalue with positive real part, $x^*$ is unstable (Khalil 2002, Section 4.3). At a hyperbolic equilibrium of a $C^1$ system, the Hartman-Grobman theorem says more: the nonlinear flow near $x^*$ is a continuous deformation of the linear flow (Hartman 1960; Grobman 1959).
5. **Map back and check.** Apply $u = u^* + \delta u$ to the real system, not $\delta u$ alone. Check the design by simulation of the nonlinear model from initial deviations of increasing size, or estimate the region of attraction with a Lyapunov function ([region of attraction estimation](/region-of-attraction-estimation/)). The linear analysis gives no region by itself.

**Accuracy on finite time.** If $f$ is $C^2$, and the deviations start with size $\varepsilon$ with an input deviation of size $O(\varepsilon)$, then on a fixed interval $[0, T]$ the nonlinear and the linear deviation trajectories differ by $O(\varepsilon^2)$. The proof writes the nonlinear deviation with the [variation of constants formula](/variation-of-constants-formula/) and the remainder $r$ as an input, and bounds the difference with the [Grönwall inequality](/gronwall-inequality/). If $A$ is Hurwitz, the bound holds uniformly on $[0, \infty)$ for small $\varepsilon$.

## Classic examples

**Pendulum, hanging and upright.** With $x = (\theta, \dot\theta)$, $\dot x_1 = x_2$, $\dot x_2 = -\sin x_1 - 0.5 x_2 + u$ (normalized so that $g / \ell = 1$). The Jacobians are

$$A = \begin{bmatrix} 0 & 1 \\ -\cos x_1^* & -0.5 \end{bmatrix}, \qquad B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}.$$

At $x^* = (0, 0)$, $A$ has eigenvalues $-0.25 \pm 0.9682 i$, a stable focus. At $x^* = (\pi, 0)$, $A = \begin{bmatrix} 0 & 1 \\ 1 & -0.5 \end{bmatrix}$ with eigenvalues $0.7808$ and $-1.2808$, a saddle. For the upright point, the feedback $\delta u = -3\, \delta\theta - 2.5\, \delta\dot\theta$ gives the linear closed loop the characteristic polynomial $s^2 + 3s + 2$, with poles $-1$ and $-2$.

To see the accuracy, start the hanging pendulum at $\theta(0) = \varepsilon$, $\dot\theta(0) = 0$, and compare the nonlinear state at $t = 5$ (RK4, step 0.001) with $e^{5A}(\varepsilon, 0)$. The largest error is $4.76 \times 10^{-5}$ for $\varepsilon = 0.1$, $3.81 \times 10^{-4}$ for $\varepsilon = 0.2$, and $0.047$ for $\varepsilon = 1$. Doubling $\varepsilon$ multiplies the error by 8, not 4: here the second-order term is zero, because $\sin \theta = \theta - \theta^3 / 6 + \cdots$, and the error is of third order.

**A tank with an outflow.** The level $x$ of a tank with inflow $u$ and outflow through a hole obeys $\dot x = u - \sqrt{x}$ (in scaled units, by Torricelli's law). The equilibria are $x^* = (u^*)^2$, and $A = -1 / (2\sqrt{x^*}) = -1 / (2 u^*)$, $B = 1$. At $u^* = 1$ the linear model has time constant 2; at $u^* = 0.5$ it has time constant 1. The linear model depends on the operating point, which is the reason for [gain scheduling](/gain-scheduling/).

**A diode, small-signal.** The current of a diode is $i = I_s (e^{v / V_T} - 1)$. At an operating point with current $I^*$, the small-signal conductance is $di/dv = (I^* + I_s)/V_T$. For $I^* = 1$ mA and $V_T = 25.85$ mV, this is about $0.0387$ S, a resistance of about $25.8$ ohm. A circuit simulator does this for every device at the DC operating point and then solves the linear circuit at each frequency; see [AC small-signal analysis](/ac-small-signal-analysis/).

**Where it fails: a zero eigenvalue.** $\dot x = -x^3$ and $\dot x = x^3$ both have the linearization $\dot{\delta x} = 0$ at 0. The first equilibrium is asymptotically stable (but not exponentially stable), and the second is unstable. The linear model cannot tell them apart.

**Where it fails: lost controllability.** A wheeled robot with position $(p_1, p_2)$, heading $\phi$, forward speed $v$ and turn rate $\omega$ obeys $\dot p_1 = v \cos\phi$, $\dot p_2 = v \sin\phi$, $\dot\phi = \omega$. At rest at the origin, $A = 0$ and $B = \begin{bmatrix} 1 & 0 \\ 0 & 0 \\ 0 & 1 \end{bmatrix}$, so the linear model cannot move sideways and is not controllable. The nonlinear robot can park sideways by a sequence of moves, which the [Lie bracket](/lie-bracket/) of the two input fields shows. By the [Brockett condition](/brockett-condition/), no continuous static feedback stabilizes it at the origin.

## Variations

- **Linearization along a trajectory.** For a nominal solution $(\bar x(t), \bar u(t))$, the Jacobians evaluated along it give a [linear time-varying system](/linear-time-varying-system/) $\dot{\delta x} = A(t)\, \delta x + B(t)\, \delta u$. This is used for trajectory tracking and in the extended Kalman filter.
- **Discrete time.** For $x_{k+1} = F(x_k, u_k)$ with a fixed point $F(x^*, u^*) = x^*$, the linear model is $\delta x_{k+1} = A\, \delta x_k + B\, \delta u_k$ with $A = \partial F / \partial x$. Stability needs the eigenvalues of $A$ inside the unit circle.
- **Linearization of a sampled plant.** Linearize first and then apply [zero-order hold discretization](/zero-order-hold-discretization/). If instead the exact sampled map of the nonlinear system (the flow over one period with the input held constant) is linearized at the equilibrium, the result is the same pair of matrices, because along a constant solution the variational equation is the linear model itself.
- **Families of linearizations.** Linearize at many operating points and interpolate the controllers: [gain scheduling](/gain-scheduling/), or an [LPV system](/lpv-system/) model.
- **Exact linearization.** [Feedback linearization](/feedback-linearization/) and [input-output linearization](/input-output-linearization/) make the closed loop exactly linear in new coordinates, in a whole region, under conditions on Lie brackets. They are different techniques with the same word in the name.
- **Numerical Jacobians.** With central differences, $\partial f / \partial x_j \approx (f(x + \eta e_j) - f(x - \eta e_j)) / (2\eta)$, the truncation error is $O(\eta^2)$ and the rounding error is about $\epsilon_{\text{mach}} \|f\| / \eta$; a step $\eta$ near $\epsilon_{\text{mach}}^{1/3}$ times the scale of $x$ balances them. Automatic differentiation gives the Jacobian to rounding accuracy.

## Pitfalls

- **Forgetting the offsets.** The linear model is in deviations. A controller designed as $\delta u = -K \delta x$ must be applied as $u = u^* - K (x - x^*)$. Applying $u = -K x$ to the real plant is a different controller.
- **Linearizing at a point that is not an equilibrium.** The neglected constant term $f(x^*, u^*)$ makes the state drift, and the linear model predicts no drift.
- **Trusting it at large deviations.** The pendulum example shows the error growing like $\varepsilon^3$; at $\varepsilon = 1$ rad it is already visible. Input saturation makes the region where a linear design works smaller still.
- **Non-hyperbolic points.** Eigenvalues on the imaginary axis leave stability undecided. Use a Lyapunov function, center manifold arguments or simulation.
- **Hidden non-smoothness.** Friction, backlash, quantization and saturation are not differentiable at their corners. Their effects, such as limit cycles in a loop with backlash, are absent from the Jacobian model.
- **Coordinates.** The eigenvalues of $A$ do not depend on the coordinates, but the size of the region of validity does. A badly scaled state makes "small deviation" mean very different things in different components.

## Exercises

1. Linearize the logistic equation $\dot x = x(1 - x) - u$ at the equilibrium with $u^* = 0.16$ and $x^* > 0.5$. Is it stable?
2. For the pendulum above, compute the linear model at the equilibrium of a constant torque $u^* = 0.5$, and its eigenvalues.
3. Show that $\dot x_1 = -x_1 + x_2^2$, $\dot x_2 = -x_2$ has the linearization $\dot{\delta x} = -\delta x$, and that the difference between the solutions of the two models from $(0, \varepsilon)$ is of order $\varepsilon^2$.
4. Find a system $\dot x = f(x)$ with an equilibrium whose linearization has an eigenvalue with positive real part, and show directly that it is unstable.
5. For the wheeled robot, find the linearization along the trajectory $\bar v = 1$, $\bar\omega = 0$, $\bar\phi = 0$, and check that this linear model, which here has constant matrices, is controllable.

## References
