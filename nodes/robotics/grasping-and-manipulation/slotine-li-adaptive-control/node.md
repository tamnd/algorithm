---
tag: RN7MPK
kind: algorithm
slug: slotine-li-adaptive-control
name: Slotine-Li adaptive controller
aliases:
- adaptive computed torque
area: robotics/grasping-and-manipulation
level: advanced
summary: "Tracks a joint trajectory while it adapts the dynamic parameters along the regressor. Its stability proof uses the skew symmetry of the arm dynamics."
model: real-ram
complexity:
  vars: {n: "the number of joints; the arm has 10 n inertial parameters, and the bounds are for one control step with the regressor formed explicitly"}
  time: {per_step: O(n^2)}
  space: {extra: O(n^2)}
properties: {deterministic: true, online: true, exact: false}
history:
  year: 1987
  people: [Jean-Jacques E. Slotine, Weiping Li]
  note: Slotine and Li gave an adaptive law for manipulators that needs neither the joint accelerations nor the inverse of the estimated inertia matrix.
prereqs: [computed-torque-control, linearity-in-dynamic-parameters, skew-symmetry-of-manipulator-dynamics, adaptive-control]
see_also: [pd-control-with-gravity-compensation, passivity-based-control, model-reference-adaptive-control, barbalat-lemma, persistent-excitation, sliding-mode-control, dynamic-parameter-identification, base-inertial-parameters]
sources:
  - paper: doi:10.1177/027836498700600303
    title: Jean-Jacques E. Slotine and Weiping Li, On the adaptive control of robot manipulators, The International Journal of Robotics Research 6(3), 1987
    locator: pages 49 to 59
  - paper: doi:10.1177/027836498700600202
    title: John J. Craig, Ping Hsu and S. Shankar Sastry, Adaptive control of mechanical manipulators, The International Journal of Robotics Research 6(2), 1987
    locator: pages 16 to 28
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: Chapter 9, Section 9.4 (passivity-based control) and Section 9.4.2 (passivity-based adaptive control)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 8 (motion control, adaptive control)
---

The Slotine-Li adaptive controller makes a robot arm follow a joint trajectory when the masses, centers of mass and inertias of its links are not known. It uses the fact that the arm dynamics are linear in these parameters, $M(q)\ddot q + C(q, \dot q)\dot q + g(q) = Y(q, \dot q, \ddot q)\pi$, and updates an estimate $\hat\pi$ online from the tracking error. Unlike adaptive versions of [computed-torque control](/computed-torque-control/), it needs neither the measured joint accelerations nor the inverse of the estimated inertia matrix. Its Lyapunov proof uses the [skew symmetry](/skew-symmetry-of-manipulator-dynamics/) of $\dot M - 2C$, which places it among the [passivity-based](/passivity-based-control/) controllers. The tracking error goes to zero; the parameter estimate goes to the true value only if the trajectory is rich enough.

## In plain words

A controller with a model of the arm can follow a path closely, but only if the model is right. A new payload in the gripper changes the model. This controller starts with a guess of the masses and inertias and keeps correcting the guess while it moves.

It combines the position error and the speed error into one number per joint, called $s$. When $s$ is zero, the position error dies out by itself at a fixed rate. The controller pushes $s$ toward zero with a model-based torque and a damping term. Each time $s$ is not zero, it shifts the guessed parameters in the direction that would have reduced $s$. A sum of a kinetic energy in $s$ and the squared parameter error never grows, and this gives the proof.

## The problem

The arm has $n$ joints and obeys the [manipulator equation](/manipulator-equation/) $M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau$ with no contact. The matrix $C$ is built from the Christoffel symbols, so $\dot M - 2C$ is skew-symmetric. By [linearity in the dynamic parameters](/linearity-in-dynamic-parameters/), there is a known regressor matrix $Y$ with

$$M(q) a + C(q, \dot q) v + g(q) = Y(q, \dot q, v, a)\,\pi$$

for all $q$, $\dot q$, $v$, $a$, where $\pi \in \mathbb{R}^p$ is a constant but unknown parameter vector. A desired trajectory $q_d(t)$ is given, with $q_d$, $\dot q_d$ and $\ddot q_d$ bounded. The task is to choose $\tau$ from $q$, $\dot q$ and the trajectory, without $\pi$, so that $q - q_d \to 0$.

## The algorithm

The gains are symmetric positive definite matrices $\Lambda$ and $K_D$ of size $n$ and $\Gamma$ of size $p$. In practice they are diagonal. The state of the controller is the estimate $\hat\pi$.

```pseudo id=main
SLOTINE-LI(q, q', q_d, q_d', q_d'', π̂, Λ, K_D, Γ)
L1  q̃ ← q - q_d
L2  q_r' ← q_d' - Λ q̃                      ▷ reference velocity
L3  q_r'' ← q_d'' - Λ (q' - q_d')            ▷ its derivative, without q''
L4  s ← q' - q_r'                           ▷ s = q̃' + Λ q̃
L5  τ ← Y(q, q', q_r', q_r'') π̂ - K_D s
L6  π̂' ← -Γ Y(q, q', q_r', q_r'')ᵀ s        ▷ adaptation law
L7  return τ, π̂'
```

The program integrates $\hat\pi$ with the rate of line L6 between control steps. Line L3 uses $\dot{\tilde q} = \dot q - \dot q_d$, so the law needs no acceleration measurement. The velocity slot of $Y$ gets $\dot q_r$, not $\dot q$: the model torque in line L5 is $\hat M \ddot q_r + \hat C(q, \dot q)\dot q_r + \hat g$. The name "adaptive computed torque" is also used for the earlier scheme of Craig, Hsu and Sastry, which needs the acceleration and the inverse of $\hat M$.

## Example

Take the planar 2R arm with $L_1 = L_2 = 1$ m and point masses of 1 kg at the link ends, in a vertical plane, with $g = 9.81$ m/s$^2$. Its dynamics are linear in $\pi = (a_1, a_2, a_3, b_1, b_2)$, where $a_1 = (m_1 + m_2) l_1^2 + m_2 l_2^2$, $a_2 = m_2 l_1 l_2$, $a_3 = m_2 l_2^2$, $b_1 = (m_1 + m_2) l_1 g$ and $b_2 = m_2 l_2 g$. The true value is $\pi = (3, 1, 1, 19.62, 9.81)$, and the controller starts with half of it, $\hat\pi = (1.5, 0.5, 0.5, 9.81, 4.905)$. The desired trajectory is $q_d(t) = (0.5 \sin t,\ 0.3 \cos 2t)$ rad. The gains are $\Lambda = 5 I$, $K_D = 20 I$ and $\Gamma = \operatorname{diag}(1, 1, 1, 20, 20)$.

At $t = 0$ the arm is at rest at $q = (0.2, 0.1)$, and $q_d = (0, 0.3)$, $\dot q_d = (0.5, 0)$, $\ddot q_d = (0, -1.2)$.

| line | value |
|---|---|
| L1 | $\tilde q = (0.2, -0.2)$ |
| L2 | $\dot q_r = (0.5 - 1,\ 0 + 1) = (-0.5, 1)$ |
| L3 | $\ddot q_r = (0 + 2.5,\ -1.2 - 0) = (2.5, -1.2)$ |
| L4 | $s = (0.5, -1)$ |
| L5 | $\tau = (9.34, 26.58)$ N m |
| L6 | $\dot{\hat\pi} = (-1.25, 0.60, 1.90, -9.80, 9.55)$ |

A simulation of the closed loop with RK4 and a step of 4 ms gives these values, where $V$ is the Lyapunov function of the next section.

| time (s) | largest joint error (rad) | $V$ | $\hat\pi$ |
|---|---|---|---|
| 0 | 0.200 | 4.509 | $(1.50, 0.50, 0.50, 9.81, 4.91)$ |
| 1 | 0.046 | 1.543 | $(1.85, 0.80, 0.01, 16.44, 11.86)$ |
| 2 | 0.012 | 1.372 | $(1.82, 0.83, 0.04, 17.37, 11.44)$ |
| 5 | 0.011 | 1.048 | $(1.85, 0.98, 0.22, 19.54, 11.58)$ |
| 10 | 0.003 | 0.883 | $(1.84, 1.01, 0.37, 19.21, 9.42)$ |

The error falls, and $V$ never grows. The estimate moves toward the truth, but after 10 s it is still far from it in $a_1$ and $a_3$: the tracking does not need the true parameters.

## Correctness

Write $\tilde\pi = \hat\pi - \pi$. Putting line L5 into the arm equation and subtracting $Y\pi = M\ddot q_r + C\dot q_r + g$ gives the closed loop

$$M(q)\dot s + C(q, \dot q)s + K_D s = Y\tilde\pi.$$

The function $V = \tfrac12 s^T M(q) s + \tfrac12 \tilde\pi^T \Gamma^{-1}\tilde\pi$ has the derivative $\dot V = -s^T K_D s + \tfrac12 s^T(\dot M - 2C)s = -s^T K_D s$, because the adaptation law of line L6 cancels the cross term $s^T Y \tilde\pi$ and $\dot M - 2C$ is skew-symmetric. So $V$ never grows, and $s$ and $\tilde\pi$ stay bounded. The integral of $s^T K_D s$ is at most $V(0)$, and [Barbalat's lemma](/barbalat-lemma/) then gives $s \to 0$. Since $\dot{\tilde q} = -\Lambda\tilde q + s$, also $\tilde q \to 0$ and $\dot{\tilde q} \to 0$. The full proof is in the proof file.

The skew symmetry is used with the vector $s$, not with $\dot q$. This needs the matrix $C$ from the Christoffel symbols; another factorization with the same product $C\dot q$ does not work.

## Complexity

In the [real-RAM](/real-ram/) model, a serial arm with $n$ joints has $p = 10 n$ inertial parameters (fewer after reduction to the [base inertial parameters](/base-inertial-parameters/)). The regressor $Y$ is an $n \times p$ matrix, but the torque of joint $i$ depends only on the parameters of links $i$ to $n$, so it has $O(n^2)$ nonzero entries. Forming $Y$, the product $Y\hat\pi$ and the product $Y^T s$ take $O(n^2)$ operations per control step with recursive kinematics, and the memory is $O(n^2)$. The 2R example has $p = 5$ and constant cost.

## Properties

- **Tracking without parameters.** The tracking error goes to zero for any constant parameter error, from any initial state, with no bound on the gains other than positive definiteness.
- **No acceleration, no inverse.** The law uses only $q$, $\dot q$ and the trajectory, and it never inverts the estimated inertia matrix, which could become singular during adaptation.
- **Asymptotic, not exponential.** Without more conditions, the proof gives only $\tilde q \to 0$. With [persistent excitation](/persistent-excitation/) of $Y$ along the desired trajectory, the estimate converges to $\pi$ and the convergence becomes exponential.
- **Bounded parameter estimate.** The estimate stays bounded but need not converge. For a set point, it usually stops at a wrong value that matches the gravity torque at the goal.

## Variants and improvements

- **Passivity-based form.** With $\hat\pi$ fixed to a known model, the law $\tau = \hat M\ddot q_r + \hat C\dot q_r + \hat g - K_D s$ is the passivity-based tracking controller (Spong, Hutchinson and Vidyasagar call the adaptive case passivity-based adaptive control).
- **Robust modifications.** With noise or unmodeled dynamics, the estimate can drift. A dead zone on $s$, projection of $\hat\pi$ onto a known box, or sigma modification keeps the estimate bounded.
- **Composite adaptation.** Slotine and Li also combined the tracking error with a prediction error of the torque in the update, which uses the data better.
- **Physically consistent estimates.** Projection onto parameters with positive masses and valid inertia tensors keeps $\hat M$ positive definite, which some variants need.
- **Other adaptive schemes.** Craig, Hsu and Sastry adapt computed-torque control; their proof needs the joint acceleration and a bounded $\hat M^{-1}$. For general systems, see [adaptive control](/adaptive-control/) and [model-reference adaptive control](/model-reference-adaptive-control/).

## When to use it

Use it when the arm follows trajectories with an unknown or changing payload, and the structure of the dynamics is known exactly. Typical cases are direct drive and low-friction arms where the rigid body model dominates. If the parameters are known well from [dynamic parameter identification](/dynamic-parameter-identification/), a fixed-model law is simpler. If the model structure is wrong, for example with large friction, add friction terms to $Y$ or use a robust law such as [sliding mode control](/sliding-mode-control/).

## Pitfalls

- **Wrong $C$.** Using a factorization of the Coriolis terms that is not the Christoffel one breaks the proof, because the proof needs $s^T(\dot M - 2C)s = 0$ for $s \ne \dot q$.
- **Drift of the estimate.** Bounded noise or a small model error can make $\hat\pi$ drift slowly without bound in the pure law. Use one of the robust modifications on a real arm.
- **Large adaptation gains.** A large $\Gamma$ makes the estimate react to noise and can excite unmodeled dynamics. Choose $\Gamma$ by scale: parameters in kg m$^2$ and in N m need different gains.
- **Expecting identification.** A converged tracking error does not mean a converged parameter estimate. Do not use $\hat\pi$ as an identified model unless the trajectory was persistently exciting.
- **Discrete time.** The proof is for continuous time. A slow control rate or a crude integration of line L6 adds errors that the proof does not cover.

## Implementations

## History

Adaptive control of manipulators was an active topic in the mid-1980s. Craig, Hsu and Sastry published an adaptive computed-torque law in the International Journal of Robotics Research in 1987, after a conference version in 1986. In the same year and journal, Slotine and Li published their law, which uses the reference velocity $\dot q_r$ and the skew symmetry of the dynamics, and needs no acceleration and no inverse of $\hat M$. Textbooks now present it as the main example of adaptive robot control and of passivity-based design.

## References
