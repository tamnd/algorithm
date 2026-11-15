---
tag: EPXGJS
kind: technique
slug: passivity-based-control
name: Passivity-based control
aliases:
- PBC
- energy shaping control
area: control/nonlinear-control
level: advanced
summary: Designs a feedback that makes the closed loop passive with a chosen storage function that has its minimum at the target, often by shaping the energy and adding damping.
prereqs: [passivity, lyapunov-function, lasalle-invariance-principle]
see_also: [port-hamiltonian-system, ida-pbc, passivity-theorem, dissipativity, pd-control-with-gravity-compensation, slotine-li-adaptive-control, backstepping, feedback-linearization]
sources:
  - paper: "R. Ortega and M. W. Spong, Adaptive motion control of rigid robots: a tutorial, Automatica 25(6), 877-888, 1989"
    title: "Adaptive motion control of rigid robots: a tutorial"
    locator: the introduction of the term passivity-based control for robot controllers
  - book: isbn:9781852330163
    title: "Romeo Ortega, Antonio Loría, Per Johan Nicklasson and Hebertt Sira-Ramírez, Passivity-based Control of Euler-Lagrange Systems, Springer, 1998"
    locator: the passivity-based design for mechanical, electrical and electromechanical Euler-Lagrange systems
  - paper: doi:10.1115/1.3139651
    title: "Morikazu Takegaki and Suguru Arimoto, A new feedback method for dynamic control of manipulators, Journal of Dynamic Systems, Measurement, and Control 103(2), 119-125, 1981"
    locator: PD feedback with gravity compensation for manipulators and its global convergence
  - paper: doi:10.1109/9.100932
    title: "Christopher I. Byrnes, Alberto Isidori and Jan C. Willems, Passivity, feedback equivalence, and the global stabilization of minimum phase nonlinear systems, IEEE Transactions on Automatic Control 36(11), 1228-1240, 1991"
    locator: feedback equivalence to a passive system (relative degree one and weakly minimum phase)
  - paper: doi:10.1016/S0005-1098(01)00278-3
    title: "Romeo Ortega, Arjan van der Schaft, Bernhard Maschke and Gerardo Escobar, Interconnection and damping assignment passivity-based control of port-controlled Hamiltonian systems, Automatica 38(4), 585-596, 2002"
    locator: Sections 1 and 2 (the passivation objective and energy balancing)
  - paper: "K. J. Åström and K. Furuta, Swinging up a pendulum by energy control, Automatica 36(2), 287-295, 2000"
    title: Swinging up a pendulum by energy control
    locator: the energy control strategy for the swing-up
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Chapter 6 (passivity) and Section 14.4 (passivity-based control)
---

Passivity-based control (PBC) is a way to design a feedback for a nonlinear system so that the closed loop is passive with a storage function that you choose, and that has a strict minimum at the target state. The storage function is then a [Lyapunov function](/lyapunov-function/), and the target is Lyapunov stable; damping on a suitable output makes it asymptotically stable. For physical systems the storage function is usually an energy, and the design has two steps: energy shaping moves the minimum of the energy to the target, and damping injection makes the energy decrease. [Passivity](/passivity/) is the property, the [passivity theorem](/passivity-theorem/) is the result about feedback loops of passive systems, the [port-Hamiltonian system](/port-hamiltonian-system/) is a model class with a built-in energy, and [IDA-PBC](/ida-pbc/) is one systematic algorithm of this technique. This page is about the technique in general.

## In plain words

A marble in a bowl rolls to the bottom and stays there, because friction takes its energy away. If you want the marble to stop at another place, you can reshape the bowl so that its lowest point is where you want it, and you can add some extra friction so that it settles faster. A passivity-based controller does the same with a machine. The controller adds forces that act like new springs, so that the total energy of machine and controller has its minimum at the target. It also adds forces that act like dampers, so that this energy can only go down. The machine then goes to the target for the same physical reason that the marble goes to the bottom. The design keeps much of the physical structure, so the controller often stays simple and works well when the model is not exact.

## When it applies

The technique needs a storage function and an output. The usual cases:

- **Systems with a physical energy.** Mechanical systems (robot arms, pendulums), electric circuits, motors and power converters have an energy $H(x)$ and a power balance $\dot H \le y^T u$, where $y$ is the output conjugate to the input (velocity for a force, current for a voltage). [Port-Hamiltonian systems](/port-hamiltonian-system/) and Euler-Lagrange systems have this property by construction.
- **Systems that feedback can make passive.** For a [control-affine system](/control-affine-system/) $\dot x = f(x) + g(x) u$ with output $y = h(x)$, a smooth state feedback $u = \alpha(x) + \beta(x) v$ that makes the system passive exists, locally around an equilibrium and under regularity conditions, if and only if the system has [relative degree](/relative-degree/) one and is weakly minimum phase (Byrnes, Isidori and Willems 1991). This is called feedback passivation.
- **Full actuation, or matching conditions.** If every degree of freedom has an actuator, the energy can be changed freely. With fewer actuators than degrees of freedom, only some energies can be reached, and the design must solve matching equations. These are partial differential equations; [IDA-PBC](/ida-pbc/) is the standard way to set them up.

The technique does not apply directly when no output with relative degree one exists, when the system is not weakly minimum phase, or when the matching equations have no solution with a minimum at the target.

## The template

1. **Find the storage and the output.** Write the system with a storage function $H(x)$, bounded below, and an output $y$ such that $\dot H \le y^T u$ along all solutions.
2. **Shape the energy.** Choose a feedback $u = \beta(x) + v$ and a new storage $H_d(x)$ with a strict minimum at the target $x^\star$, such that the closed loop satisfies $\dot H_d \le y_d^T v$ for a new output $y_d$. For a fully actuated mechanical system this means: keep the kinetic energy, and replace the potential energy $V(q)$ by $V_d(q)$ with its minimum at $q^\star$, using $\beta = \nabla V - \nabla V_d$.
3. **Inject damping.** Close the loop with $v = -K_v y_d$, $K_v = K_v^T > 0$. Then $\dot H_d \le -y_d^T K_v y_d \le 0$.
4. **Prove convergence.** $H_d - H_d(x^\star)$ is a Lyapunov function, so $x^\star$ is a Lyapunov stable equilibrium ([Lyapunov's direct method](/lyapunov-direct-method/)). If $x^\star$ is the only solution that keeps $y_d \equiv 0$ (a detectability condition), then the [LaSalle invariance principle](/lasalle-invariance-principle/) on a compact sublevel set of $H_d$ gives local asymptotic stability, with that sublevel set inside the region of attraction. If $H_d$ is radially unbounded and $x^\star$ is its only critical point, the result is global.

**The theorem behind steps 3 and 4.** Let the closed loop be autonomous, with a locally Lipschitz right side. Let $H_d$ be $C^1$ with a strict local minimum at $x^\star$, and let $\dot H_d \le -y_d^T K_v y_d$ along solutions. Then $x^\star$ is Lyapunov stable. If, moreover, no solution other than $x^\star$ stays in $\{y_d = 0\}$ within a compact sublevel set $\Omega_c = \{H_d \le c\}$ around $x^\star$, every solution that starts in $\Omega_c$ converges to $x^\star$. This is the invariance principle of Khalil 2002 (Section 4.2) applied to $H_d$, and it is the form used in Khalil 2002, Section 14.4.

## Classic examples

**1. A pendulum: energy shaping plus damping.** Take a pendulum with inertia 1, $m g l = 9.81$ (units of torque, N m), friction $b = 0.1$ and torque input $u$:

$$\ddot q = -9.81 \sin q - 0.1\, \dot q + u.$$

The target is the horizontal position $q^\star = \pi / 2$. The open-loop energy is $H = \frac12 \dot q^2 + 9.81 (1 - \cos q)$. Shape the potential to

$$V_d(q) = 9.81 (1 - \cos q) + \tfrac{k_p}{2} (q - q^\star)^2 - 9.81 \sin(q^\star)(q - q^\star),$$

which has $V_d'(q^\star) = 0$ and $V_d''(q) = 9.81 \cos q + k_p \ge k_p - 9.81 > 0$ for $k_p > 9.81$. So $q^\star$ is the only minimum, and $V_d$ grows without bound. The feedback that gives this potential, with damping injection $k_d$, is

$$u = 9.81 \sin q^\star - k_p (q - q^\star) - k_d \dot q,$$

a PD controller with a constant gravity term. The closed loop is $\ddot q = -V_d'(q) - (b + k_d) \dot q$, and with $H_d = \frac12 \dot q^2 + V_d(q) - V_d(q^\star)$,

$$\dot H_d = -(b + k_d)\, \dot q^2 \le 0.$$

On the set $\dot q = 0$ the closed loop gives $\ddot q = -V_d'(q)$, which is zero only at $q^\star$, so LaSalle gives global asymptotic stability. With $k_p = 20$ and $k_d = 6$, from rest at $q = 0$, $H_d(0) = 30.2735$ and $u(0) = 41.2259$. A classical RK4 simulation with step $0.01$ gives:

| $t$ | 0 | 0.25 | 0.5 | 1 | 1.5 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|---|---|
| $q$ | 0 | 0.71642 | 1.45608 | 1.67335 | 1.57481 | 1.56589 | 1.57103 | 1.57079 |
| $H_d$ | 30.2735 | 15.7564 | 1.82617 | 0.13218 | 0.00380 | 0.00033 | 0.000001 | 0.000000 |

$H_d$ decreases at every step, up to rounding of order $10^{-15}$. The largest angle is $1.6986$, an overshoot of $0.128$ rad. For comparison, the plain PD law $u = -20 (q - q^\star) - 6 \dot q$ without the gravity term settles at $q = 1.1277$: its shaped potential has its minimum at the wrong place.

**2. PD with gravity compensation for robot arms.** For a fully actuated arm $M(q) \ddot q + C(q, \dot q) \dot q + \nabla V(q) = u$, Takegaki and Arimoto (1981) used $u = \nabla V(q) - K_p (q - q^\star) - K_d \dot q$ with $K_p, K_d > 0$. The function $H_d = \frac12 \dot q^T M(q) \dot q + \frac12 (q - q^\star)^T K_p (q - q^\star)$ has $\dot H_d = -\dot q^T K_d \dot q$, because $\dot M - 2C$ is skew-symmetric for the Christoffel choice of $C$. LaSalle gives global asymptotic stability of $(q^\star, 0)$. See [PD control with gravity compensation](/pd-control-with-gravity-compensation/).

**3. Damping injection alone.** For the mass, spring and damper on the [port-Hamiltonian system](/port-hamiltonian-system/) page, $u = -K_v y$ with the velocity $y$ adds friction and keeps the minimum of the energy where it is. This is step 3 without step 2. It is enough when the open-loop energy already has its minimum at the target.

**4. Feedback passivation.** For $\dot z = f_0(z) + p(z, y) y$, $\dot y = a(z, y) + b(z, y) u$ with $b \neq 0$ and a storage $W(z)$ for the zero dynamics with $\nabla W^T f_0 \le 0$, the feedback $u = b^{-1}(-a - (\nabla W^T p)^T + v)$ makes the system passive from $v$ to $y$ with storage $W(z) + \frac12 |y|^2$. Then $v = -K_v y$ gives $\dot W + \frac{d}{dt}\frac12 |y|^2 = \nabla W^T f_0 - y^T K_v y \le 0$. The result of Byrnes, Isidori and Willems (1991) says when such a form exists.

**5. Swing-up by energy control.** Åström and Furuta (2000) swing up a pendulum by controlling its energy instead of its position. For a frictionless pendulum with torque input, $\dot E = \dot q\, u$ with $E = \frac12 \dot q^2 + m g l (1 - \cos q)$. The feedback $u = -k (E - E_{\text{top}}) \dot q$ with $E_{\text{top}} = 2 m g l$ gives $\frac{d}{dt}(E - E_{\text{top}}) = -k (E - E_{\text{top}}) \dot q^2$, so the energy goes to the energy of the upright position. A local controller then catches the pendulum near the top. Here the passive output $\dot q$ is used, but the target is a level of energy, not a point.

## Variations

- **IDA-PBC.** Instead of choosing $H_d$ first, choose the desired interconnection and damping matrices and solve the matching equations for $H_d$. This handles underactuated and electromechanical systems. See [IDA-PBC](/ida-pbc/).
- **Energy balancing.** If the closed-loop energy equals the stored energy minus the energy supplied by the controller, the controller acts like a physical system connected to the plant. Ortega et al. (2002) show when this holds. It fails when dissipation acts on the coordinates that must be shaped, which is the dissipation obstacle described on the [port-Hamiltonian system](/port-hamiltonian-system/) page.
- **Tracking.** For robots that follow a trajectory, the Slotine-Li controller and its adaptive form use the passivity of the map from a filtered tracking error to the velocity error (Ortega and Spong 1989). See [Slotine-Li adaptive control](/slotine-li-adaptive-control/).
- **Without velocity measurements.** The damping can be injected through a filter of the position, which makes the closed loop passive from a filtered output. Ortega, Loría, Nicklasson and Sira-Ramírez (1998) treat these output feedback designs.
- **Combination with other designs.** [Backstepping](/backstepping/) can make a cascade passive step by step, and the passivity of the subsystems gives the cross terms that cancel.

## Pitfalls

- **Stability without convergence.** Damping injection only on some coordinates gives $\dot H_d \le 0$, not $< 0$. Without the detectability condition of step 4, the state can stay on a level set of $H_d$ forever. Check the largest invariant set in $\{y_d = 0\}$.
- **A local minimum is a local result.** If $H_d$ has other minima or is not radially unbounded, the result holds only on a sublevel set that contains no other critical point. In the pendulum example, $k_p < 9.81$ makes $V_d''$ negative at some angles, and other equilibria appear.
- **Cancellation needs a good model.** The gravity term $\nabla V(q)$ in example 2 must be exact. An error $\Delta V$ moves the minimum of the shaped potential and gives a steady-state error. Example 1 uses only the constant $9.81 \sin q^\star$, which still must be right.
- **Passive for a new output.** After energy shaping, the closed loop is passive from $v$ to $y_d$, which need not be the physical output. Robustness arguments that use the physical output need $y_d = y$ (Ortega et al. 2002, Section 3.2).
- **Sampling and saturation.** The power balance holds for the continuous-time loop. A sampled controller can inject energy, and actuator saturation removes part of the damping. Both can destroy the guarantee for large gains or slow sampling.
- **The damping does not always help.** Larger $K_v$ makes $\dot H_d$ more negative, but it can make the response slower in other directions and amplify measurement noise.

## Exercises

1. For the pendulum of example 1, find the smallest $k_p$ for which $V_d$ is convex on all of $\mathbb{R}$. *Answer:* $V_d'' = 9.81 \cos q + k_p$, so $k_p > 9.81$ is needed, and $k_p = 9.81$ fails at $q = \pi$.
2. Show that with $u = -20 (q - \pi/2) - 6 \dot q$ (no gravity term) the pendulum settles where $9.81 \sin q = 20 (\pi/2 - q)$, and that the root is near $q = 1.1277$.
3. For the mass, spring and damper with $m = 1$, $k = 2$, $b = 0.5$, shape the energy so that the new rest position is $q^\star = 1$. *Answer:* $u = k q^\star + k_1 (q^\star - q) - k_v \dot q$ gives $H_d = \frac12 \dot q^2 + \frac12 (k + k_1)(q - q^\star)^2$, with $\dot H_d = -(b + k_v) \dot q^2$.
4. In example 5, show that $E = E_{\text{top}}$ is reached only in the limit, and explain why a second controller is needed near the top.
5. Show that a port-Hamiltonian system with the feedback $u = -K_v y + v$ is again port-Hamiltonian from $v$ to $y$, with the same $H$ and $J$. *Answer:* the dissipation matrix becomes $R + g K_v g^T$, which is symmetric positive semidefinite.

## References
