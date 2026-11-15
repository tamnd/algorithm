---
tag: K9K5BQ
kind: technique
slug: singular-perturbation-method
name: Singular perturbation method
aliases:
- Tikhonov's theorem
- two-time-scale analysis
area: control/nonlinear-control
level: advanced
summary: Splits a system with fast and slow states into a reduced slow model and a boundary layer model, and analyzes each.
prereqs: [exponential-stability, lyapunov-direct-method]
see_also: [averaging-method, high-gain-observer, model-order-reduction, balanced-truncation, cascade-control, stiff-ode-problem, gronwall-inequality, region-of-attraction]
sources:
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Chapter 11 (the standard singularly perturbed model, Tikhonov's theorem on a finite time interval, the infinite interval, slow and fast manifolds, and stability analysis with a composite Lyapunov function)
  - book: isbn:9780898714449
    title: Petar Kokotović, Hassan K. Khalil and John O'Reilly, Singular Perturbation Methods in Control, Analysis and Design, Academic Press, 1986; reprinted in SIAM Classics in Applied Mathematics, 1999
    locator: the standard model, time-scale properties, and composite control design
  - paper: "A. N. Tikhonov, Systems of differential equations containing small parameters in the derivatives, Matematicheskii Sbornik (N.S.) 31(73), no. 3, 575-586, 1952 (in Russian)"
    title: Systems of differential equations containing small parameters in the derivatives
    locator: the limit of the solutions as the small parameter goes to zero
---

The singular perturbation method studies a system in which some states change much faster than the others. A small parameter $\varepsilon > 0$ multiplies the derivative of the fast states. At $\varepsilon = 0$ the fast states obey an algebraic equation, and the order of the model drops. The method replaces one hard analysis by two easier ones: a reduced model for the slow states, with the fast states at their equilibrium, and a boundary layer model for the fast states, with the slow states frozen. If the boundary layer is exponentially stable, uniformly in the slow states, then the full solution stays within $O(\varepsilon)$ of the approximation built from the two models. This is the theorem of Tikhonov (1952). In control it justifies neglecting fast actuator, sensor or electrical dynamics, and it explains high-gain observers and cascade loops.

## In plain words

Many machines have fast parts and slow parts. The current in a motor settles in milliseconds, but the shaft speed changes over seconds. The method looks at the two parts one at a time. First, it pretends that the fast part settles at once, which gives a simpler model of the slow part. Then it looks at the fast part alone, as if the slow part were frozen. If the fast part always settles quickly on its own, then the real machine behaves like the simple model, with a small error. The error gets smaller when the fast part gets faster. Just after the start, the fast part has not settled yet, and you must add a short burst that dies out quickly. If the fast part does not settle on its own, the method fails.

## When it applies

- The model can be put in the **standard form** below, with a small parameter $\varepsilon$ in front of the derivative of some states. The parameter is a ratio of time constants, a small mass or inductance, or the inverse of a high gain. Finding the right $\varepsilon$ and the right scaling of the states is part of the work.
- The equation $0 = g(t, x, z, 0)$ has an **isolated root** $z = h(t, x)$ on the region of interest. A root that branches or meets another root breaks the method there.
- The **boundary layer is exponentially stable**, uniformly in the frozen slow variables (rule: this is the hypothesis that people forget to check).
- The question is about a **finite time interval**, or the reduced model has an **exponentially stable equilibrium**, which extends the result to all $t \ge 0$.

## The template

The standard singularly perturbed model is

$$\dot x = f(t, x, z, \varepsilon), \qquad \varepsilon \dot z = g(t, x, z, \varepsilon), \qquad x(t_0) = \xi, \ z(t_0) = \eta,$$

with $x \in \mathbb{R}^n$ slow, $z \in \mathbb{R}^m$ fast and $f$, $g$ smooth enough.

1. **Find the quasi-steady state.** Set $\varepsilon = 0$ and solve $0 = g(t, x, z, 0)$ for an isolated root $z = h(t, x)$.
2. **Write the reduced model.** $\dot{\bar x} = f(t, \bar x, h(t, \bar x), 0)$, $\bar x(t_0) = \xi$. It has order $n$, not $n + m$. Note that $\bar x$ starts at $\xi$, but $h(t_0, \xi)$ need not equal $\eta$.
3. **Write the boundary layer model.** Put $y = z - h(t, x)$ and the fast time $\tau = (t - t_0) / \varepsilon$. With $t$ and $x$ frozen as parameters, $\frac{dy}{d\tau} = g(t, x, y + h(t, x), 0)$, $y(0) = \eta - h(t_0, \xi)$. Its equilibrium is $y = 0$.
4. **Check the boundary layer.** Show that $y = 0$ is exponentially stable, uniformly in $(t, x)$, and that $y(0)$ lies in its region of attraction. For a linear model this is a uniform bound on the eigenvalues of $\partial g / \partial z$ in the open left half plane; in general use a Lyapunov function $W(t, x, y)$ with bounds that do not depend on $(t, x)$.
5. **Apply Tikhonov's theorem.** On a finite interval $[t_0, t_1]$ on which the reduced model has a unique solution, there is $\varepsilon^* > 0$ such that for $0 < \varepsilon < \varepsilon^*$ (theorem, Khalil 2002, Chapter 11):
   $$x(t) = \bar x(t) + O(\varepsilon), \qquad z(t) = h(t, \bar x(t)) + \hat y(t / \varepsilon) + O(\varepsilon),$$
   uniformly on $[t_0, t_1]$, where $\hat y$ is the solution of the boundary layer model with $x$ and $t$ frozen at their initial values. After any fixed $t_b > t_0$, the term $\hat y$ is exponentially small, and $z(t) = h(t, \bar x(t)) + O(\varepsilon)$.
6. **Extend to all time, if needed.** If, in addition, the reduced model has an exponentially stable equilibrium and $\xi$ is in a compact subset of its region of attraction, the same estimates hold uniformly on $[t_0, \infty)$ (theorem, Khalil 2002, Chapter 11).
7. **For stability of the full system, build a composite Lyapunov function.** For the autonomous case with an equilibrium at the origin and $h(0) = 0$, take $V(x)$ for the reduced model and $W(x, y)$ for the boundary layer, with the bounds
   - $\nabla V^T f(x, h(x)) \le -\alpha_1 \psi_1(x)^2$ and $\nabla_y W^T g(x, y + h(x)) \le -\alpha_2 \psi_2(y)^2$,
   - $\nabla V^T [f(x, y + h(x)) - f(x, h(x))] \le \beta_1 \psi_1 \psi_2$,
   - $[\nabla_x W - \nabla_y W\, \partial h / \partial x]^T f(x, y + h(x)) \le \beta_2 \psi_1 \psi_2 + \gamma \psi_2^2$,

   where $\psi_1$, $\psi_2$ are positive definite. Then $\nu = (1 - d) V + d W$ with $d = \beta_1 / (\beta_1 + \beta_2)$ shows that the origin is asymptotically stable for $0 < \varepsilon < \varepsilon^* = \alpha_1 \alpha_2 / (\alpha_1 \gamma + \beta_1 \beta_2)$ (theorem, Khalil 2002, Chapter 11). The bound comes from asking that the $2 \times 2$ matrix of the quadratic form in $(\psi_1, \psi_2)$ be positive definite, and from the best choice of $d$.

## Classic examples

**A second-order system with a small mass.** The system $\varepsilon \ddot x + \dot x + x = 0$ in standard form is $\dot x = z$, $\varepsilon \dot z = -z - x$, with $x(0) = 1$ and $z(0) = 0$. The root is $z = h(x) = -x$, the reduced model is $\dot{\bar x} = -\bar x$, so $\bar x(t) = e^{-t}$, and the boundary layer is $dy/d\tau = -y$ with $y(0) = 0 - h(1) = 1$, so $\hat y(\tau) = e^{-\tau}$. It is exponentially stable for every frozen $x$. The exact eigenvalues are the roots of $\varepsilon \lambda^2 + \lambda + 1 = 0$. For $\varepsilon = 0.01$ they are $-1.0102$ and $-98.99$, a slow mode near the reduced one and a fast mode near $-1/\varepsilon$. The table gives measured errors from the exact solution, sampled with step 0.0005 on $[0, 10]$:

| $\varepsilon$ | $\max_t \lvert x(t) - e^{-t} \rvert$ | $\max_t \lvert z(t) + e^{-t} - e^{-t/\varepsilon} \rvert$ | $\max_{t \ge 0.5} \lvert z(t) + e^{-t} \rvert$ |
|---|---|---|---|
| 0.1 | 0.0709 | 0.1395 | 0.1130 |
| 0.01 | 0.00931 | 0.0187 | 0.00936 |
| 0.001 | 0.000989 | 0.00198 | 0.000912 |

All three errors scale like $\varepsilon$, as Tikhonov's theorem says. Without the boundary layer term, the error in $z$ near $t = 0$ is about 1 for every $\varepsilon$, because $z(0) = 0$ and $h(x(0)) = -1$.

**The composite bound on the same system.** With $V = x^2 / 2$ and $W = y^2 / 2$, the reduced model gives $\dot V = -x^2$ ($\alpha_1 = 1$, $\psi_1 = |x|$), the boundary layer gives $-y^2$ ($\alpha_2 = 1$, $\psi_2 = |y|$), the coupling term is $x y$ ($\beta_1 = 1$), and the last term is $y (y - x)$ ($\beta_2 = 1$, $\gamma = 1$). So $\varepsilon^* = 1 / (1 + 1) = 1/2$. The true system is stable for every $\varepsilon > 0$, because all coefficients of $\varepsilon \lambda^2 + \lambda + 1$ are positive. The composite bound is sufficient, not tight (rule of thumb: it is often conservative by a large factor).

**DC motor with armature inductance.** With shaft speed $\omega$, current $i$ and voltage $v$, the model is $J \dot\omega = k i$, $L \dot i = -k \omega - R i + v$. The inductance $L$ is small, so after scaling $\varepsilon = L / R$ times a slow time constant. The root is $i = (v - k \omega) / R$, the reduced model is the first-order $J \dot\omega = k (v - k \omega) / R$, and the boundary layer $L\, dy / dt = -R y$ is exponentially stable because $R > 0$. This is why a first-order motor model is enough for a speed loop that is slow compared with $L / R$.

**Cascade loops and fast actuators.** In [cascade control](/cascade-control/), an inner loop that is much faster than the outer loop is a boundary layer. The outer loop is designed on the reduced model in which the inner loop is at steady state. The same argument justifies neglecting actuator dynamics that are much faster than the closed loop.

**High-gain observers.** In a [high-gain observer](/high-gain-observer/) with gains $\alpha_i / \varepsilon^i$, the scaled estimation error obeys $\varepsilon \dot \eta = A_0 \eta + \varepsilon\, (\cdot)$ with $A_0$ Hurwitz. It is a fast boundary layer, and the closed loop with the observer recovers the performance of state feedback as $\varepsilon \to 0$, by a singular perturbation argument.

## Variations

- **Slow manifold.** For $\varepsilon > 0$ the set $z = h(t, x)$ is not invariant, but a nearby set $z = H(t, x, \varepsilon) = h(t, x) + \varepsilon H_1(t, x) + \dots$ is, under the same hypotheses. Substituting $z = H$ into the equations gives a reduced model that is correct to higher order in $\varepsilon$. Fenichel's geometric theory gives the same result for compact normally hyperbolic manifolds.
- **Linear systems.** For $\dot x = A_{11} x + A_{12} z$, $\varepsilon \dot z = A_{21} x + A_{22} z$ with $A_{22}$ Hurwitz, the reduced matrix is $A_{11} - A_{12} A_{22}^{-1} A_{21}$, and a change of coordinates separates the slow and fast subsystems exactly for small $\varepsilon$. This is a form of [model order reduction](/model-order-reduction/) that keeps the static gain, unlike [balanced truncation](/balanced-truncation/), which keeps the most observable and controllable states.
- **Composite control.** Design a slow control $u_s$ on the reduced model and a fast control $u_f$ on the boundary layer, and apply $u = u_s + u_f$. The fast control can stabilize a boundary layer that is not stable by itself.
- **Two parameters or more time scales.** Several small parameters give a chain of time scales, analyzed from the fastest to the slowest.
- **Numerical methods.** A singularly perturbed system is a [stiff problem](/stiff-ode-problem/). An explicit integrator needs a step of order $\varepsilon$; an implicit one does not.

## Pitfalls

- **An unstable boundary layer.** For $\dot x = -z$, $\varepsilon \dot z = z - x$, the root is $z = x$ and the reduced model $\dot{\bar x} = -\bar x$ is stable, but the boundary layer $dy/d\tau = y$ is unstable. The matrix of the full system has trace $1/\varepsilon > 0$ and determinant $-1/\varepsilon < 0$, so one eigenvalue is positive for every $\varepsilon > 0$. The reduced model predicts stability and is wrong. Always do step 4.
- **Stability that is not uniform in the slow variables.** If the boundary layer decays at a rate that goes to zero for some value of $x$, there is no single $\varepsilon^*$. Check the rate on the whole region that the slow state visits.
- **The initial layer.** The fast state does not start on $z = h$. The approximation $z \approx h(t, \bar x)$ is wrong for $t - t_0$ of order $\varepsilon$, and peaks in $z$ there can saturate actuators. Use the term $\hat y(t / \varepsilon)$ of step 5, or start on the slow manifold.
- **Infinite time without exponential stability.** On $[t_0, \infty)$ the $O(\varepsilon)$ errors can add up unless the reduced model has an exponentially stable equilibrium (step 6). Tikhonov's theorem on a finite interval says nothing about the limit as $t \to \infty$.
- **The wrong small parameter.** Writing a model in standard form needs a scaling in which $f$ and $g$ are of order 1. A parameter that is small in some units can be large in others. Compare time constants, not raw numbers.
- **A value of $\varepsilon$ that is "small enough".** The theorem gives existence of $\varepsilon^*$, not its size. Estimate it with step 7 or check the full model by simulation.

## Exercises

1. For $\dot x = -x + z$, $\varepsilon \dot z = -z + \sin t$, write the reduced and boundary layer models, and give $\bar x(t)$ for $x(0) = 0$.
2. For the second-order example, expand the slow eigenvalue in powers of $\varepsilon$ and show that it is $-1 - \varepsilon + O(\varepsilon^2)$.
3. Show that for the linear model of the Variations section with $A_{22}$ Hurwitz, the eigenvalues of the full matrix are close to those of $A_{11} - A_{12} A_{22}^{-1} A_{21}$ and of $A_{22} / \varepsilon$ for small $\varepsilon$.
4. Derive the formula $\varepsilon^* = \alpha_1 \alpha_2 / (\alpha_1 \gamma + \beta_1 \beta_2)$ by asking for the positive definiteness of the matrix in step 7 and choosing $d$ to make the bound largest.
5. Write the DC motor model in standard form with $\varepsilon = L / R$ divided by the mechanical time constant $J R / k^2$, and check the hypotheses of Tikhonov's theorem.

## References
