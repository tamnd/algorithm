---
tag: R56T5W
kind: definition
slug: state-observer
name: State observer
aliases:
- state estimator
area: control/state-space-control
level: intro
summary: A dynamical system that takes the input and output of a plant and produces an estimate of its state that converges to the true state.
prereqs: [state-space-representation, observability, detectability]
see_also: [luenberger-observer, reduced-order-observer, unknown-input-observer, disturbance-observer, high-gain-observer, sliding-mode-observer, kalman-bucy-filter, state-estimation]
sources:
  - paper: doi:10.1109/tme.1964.4323124
    title: David G. Luenberger, Observing the state of a linear system, IEEE Transactions on Military Electronics 8(2), 74-80, 1964
    locator: the definition of an observer as a linear system driven by the plant input and output, and the conditions TA - FT = HC and G = TB
  - paper: doi:10.1109/tac.1971.1099826
    title: David G. Luenberger, An introduction to observers, IEEE Transactions on Automatic Control 16(6), 596-602, 1971
    locator: the tutorial account of identity, reduced-order and functional observers
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 8.4 (state estimators, including the reduced-dimensional estimator) and Section 8.7 (the multivariable case)
  - book: isbn:9780691193984
    title: Karl J. Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 8, Output Feedback (the sections Observability and State Estimation)
---

## Definition

Consider a plant

$$\dot x = Ax + Bu, \qquad y = Cx,$$

with state $x \in \mathbb{R}^n$, a known input $u \in \mathbb{R}^m$ and a measured output $y \in \mathbb{R}^p$. A **state observer** for the plant is a dynamical system with input $(u, y)$, state $z \in \mathbb{R}^q$ and output $\hat x \in \mathbb{R}^n$,

$$\dot z = Fz + Gu + Hy, \qquad \hat x = Mz + Ny,$$

such that for every initial state $x(0)$, every initial state $z(0)$ and every locally integrable input $u$,

$$\lim_{t \to \infty} \bigl(x(t) - \hat x(t)\bigr) = 0.$$

The observer is **exponential** if moreover $|x(t) - \hat x(t)| \le c\,e^{-\sigma t}\bigl(|x(0) - \hat x(0)| + |z(0)|\bigr)$ for constants $c, \sigma > 0$ that do not depend on $u$. The number $q$ is the **order** of the observer. For linear time-invariant observers the two notions agree. In discrete time the definition is the same with $z_{k+1} = Fz_k + Gu_k + Hy_k$ and $\hat x_k = Mz_k + Ny_k$. For a nonlinear plant $\dot x = f(x, u)$, $y = h(x)$, the observer is a system $\dot z = \varphi(z, u, y)$, $\hat x = \psi(z, y)$ with the same convergence property, often only for initial states in a given set.

The observers of this area are deterministic: they need no noise model, and the convergence is a property of the error dynamics. Estimators that use a model of the noise belong to [state estimation](/state-estimation/) in the stochastic sense, such as the [Kalman filter](/kalman-filter/) and the [Kalman-Bucy filter](/kalman-bucy-filter/).

**A sufficient condition (Luenberger).** If $F$ is Hurwitz and there is $T \in \mathbb{R}^{q \times n}$ with

$$TA - FT = HC, \qquad G = TB,$$

then $z - Tx \to 0$ for every input. Indeed, $e = z - Tx$ satisfies $\dot e = Fz + Gu + HCx - TAx - TBu = Fe + (FT + HC - TA)x + (G - TB)u = Fe$. If moreover $MT + NC = I$, then $\hat x - x = Me \to 0$, so the system is a state observer. The identity observer has $q = n$, $T = I$, $F = A - LC$, $H = L$, $G = B$, $M = I$ and $N = 0$.

**Existence.** For a linear time-invariant plant, a state observer exists if and only if $(C, A)$ is [detectable](/detectability/). An observer whose error decays with any prescribed rate (all eigenvalues of $F$ freely chosen) exists if and only if $(C, A)$ is [observable](/observability/). Both follow from the identity observer and the [pole placement theorem](/pole-placement-theorem/) applied to $(A^T, C^T)$. Conversely, if $(C, A)$ is not detectable, there is an initial state $x(0) \ne 0$ with $y(t) = 0$ for $u = 0$ and $x(t) \not\to 0$. The plant started at $x(0)$ and the plant started at 0 then give the same input and output, so no system that sees only $u$ and $y$ can estimate both states correctly.

## Examples and non-examples

- **Identity observer of the double integrator.** $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $C = [1, 0]$. The system $\dot{\hat x} = A\hat x + Bu + L(y - C\hat x)$ with $L = [5, 6]^T$ has the error matrix $A - LC = \begin{bmatrix} -5 & 1 \\ -6 & 0 \end{bmatrix}$ with characteristic polynomial $s^2 + 5s + 6$, eigenvalues $-2$ and $-3$. It is an exponential state observer of order 2. This is the [Luenberger observer](/luenberger-observer/).
- **Reduced-order observer of the same plant.** Since $y = x_1$ is measured, only $x_2$ must be estimated. The system $\dot z = -3z - 9y + u$, $\hat x_2 = z + 3y$ has $\hat x_2 - x_2 = e^{-3t}(\hat x_2(0) - x_2(0))$. It is a state observer of order 1. See the [reduced-order observer](/reduced-order-observer/).
- **A copy of the model is not an observer in general.** With $L = 0$, the system $\dot{\hat x} = A\hat x + Bu$ has the error $e(t) = e^{At}e(0)$. For the double integrator with $e(0) = (0, 1)$ the position error is $t$, which grows without bound. A copy of the model is a state observer exactly when $A$ is Hurwitz.
- **A differentiator is not an observer in this sense.** For the double integrator, $\hat x = (y, \dot y)$ gives the state exactly, but it is not a system of the form above: it needs the derivative of $y$, which is not proper and amplifies measurement noise without bound at high frequency.
- **A detectable but unobservable plant.** $A = \begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}$, $C = [0, 1]$. The first state is not seen in $y$, but it decays by itself. An identity observer with $L = [0, \ell]^T$, $\ell > 1$, is a state observer, but the error in $x_1$ always decays like $e^{-t}$, whatever $L$ is.
- **A plant with no observer.** $A = \begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$, $C = [0, 1]$. The first state grows and is not seen. No state observer exists.
- **An unknown input breaks the definition.** If the plant is $\dot x = Ax + Bu + Ed$ with an unmeasured $d$, the identity observer has $\dot e = (A - LC)e + Ed$, and the error does not go to 0 in general. An [unknown input observer](/unknown-input-observer/) restores the definition for every $d$ under a rank condition.

## Related definitions

The observers of this area differ in what they estimate, in what they assume, and in their order:

- **[Luenberger observer](/luenberger-observer/).** The identity observer of order $n$, $\dot{\hat x} = A\hat x + Bu + L(y - C\hat x)$, with $L$ from pole placement for the dual pair.
- **[Reduced-order observer](/reduced-order-observer/).** Order $n - p$. It takes the part of the state that $y$ gives directly and estimates only the rest. It passes measurement noise to $\hat x$ without filtering.
- **[Unknown input observer](/unknown-input-observer/).** Its error does not depend on an unmeasured input $d$ at all, when $\operatorname{rank}(CE) = \operatorname{rank}(E)$ and the invariant zeros of $(A, E, C)$ are stable.
- **[Disturbance observer](/disturbance-observer/).** It estimates a lumped disturbance on the input, not the state, from a nominal inverse model and a low-pass filter, and is usually used to cancel it.
- **[High-gain observer](/high-gain-observer/).** For nonlinear plants in an observable normal form. Large gains make the error small quickly, at the price of peaking and noise sensitivity.
- **[Sliding mode observer](/sliding-mode-observer/).** Uses a discontinuous output injection, which makes the error insensitive to matched uncertainties and can reconstruct unknown inputs.
- **[Kalman-Bucy filter](/kalman-bucy-filter/) and [Kalman filter](/kalman-filter/).** Observers whose gain minimizes the error covariance under a noise model, in continuous and in discrete time.
- **Functional observer.** An observer that estimates only $Kx$, for example the signal that a state feedback needs. It can have a lower order than $n - p$.
- **[Separation principle](/separation-principle/).** If a state feedback $u = -K\hat x$ uses the estimate of a linear observer, the closed-loop eigenvalues are those of the feedback and those of the observer.
- **[Observability](/observability/) and [detectability](/detectability/).** The conditions for an observer with any error rate, and for an observer at all.

## References
