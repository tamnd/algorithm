---
tag: A4QTQK
kind: definition
slug: observability
name: Observability
aliases:
- state observability
- complete observability
area: control/state-space-control
level: core
summary: A system is observable if its initial state is fixed by the input and output over some finite interval.
prereqs: [state-space-representation, controllability]
see_also: [kalman-rank-condition, popov-belevitch-hautus-test, observability-gramian, detectability, kalman-decomposition, state-observer, luenberger-observer, kalman-filter]
sources:
  - paper: doi:10.1137/0301009
    title: Elmer G. Gilbert, Controllability and observability in multivariable control systems, SIAM Journal on Control 1(2), 128-151, 1963
    locator: observability of multivariable systems with distinct eigenvalues, read from the modal form
  - paper: doi:10.1137/0301010
    title: R. E. Kalman, Mathematical description of linear dynamical systems, SIAM Journal on Control 1(2), 152-192, 1963
    locator: observability, its duality with controllability, and the observable part of a system
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 6.3 (observability and its tests), Section 6.6 (discrete time) and Section 6.7 (observability after sampling)
  - book: isbn:9780387984896
    title: Eduardo D. Sontag, Mathematical Control Theory, Deterministic Finite Dimensional Systems, second edition, Springer, 1998
    locator: Chapter 6, Outputs (observability, indistinguishable states and duality)
---

A linear system is observable when its initial state can be computed from the input and the output over a finite time interval. It is the property that makes state estimation possible: the eigenvalues of the error matrix $A - L C$ of a [Luenberger observer](/luenberger-observer/) can be put anywhere exactly when the pair $(C, A)$ is observable. Observability is the dual of [controllability](/controllability/), and the weaker property that the unseen part of the state decays by itself is [detectability](/detectability/).

## Definition

**Notation.** The system is the continuous-time [state-space model](/state-space-representation/)

$$\dot x = A x + B u, \qquad y = C x + D u, \qquad x \in \mathbb{R}^n,\ u \in \mathbb{R}^m,\ y \in \mathbb{R}^p .$$

Inputs are piecewise continuous. By the [variation of constants formula](/variation-of-constants-formula/),

$$y(t) = C e^{At} x(0) + \int_0^t C e^{A(t - s)} B u(s)\, ds + D u(t).$$

The input and the matrices are known; the initial state $x(0)$ is not.

**Definition.** The system, or the pair $(C, A)$, is *observable* if there is a time $T > 0$ such that for every input $u$, the output $y$ on $[0, T]$ determines $x(0)$ uniquely.

**Reduction to zero input.** The part of $y$ that the input produces is known, so it can be subtracted. Two initial states $x_0$ and $x_0'$ give the same output for the same input if and only if $C e^{At} (x_0 - x_0') = 0$ for $t$ in $[0, T]$. So the system is observable if and only if the zero-input output $C e^{At} x_0$ vanishes on $[0, T]$ only for $x_0 = 0$. The matrices $B$ and $D$ play no part.

**The unobservable subspace.** The initial states that give the zero output with zero input form the subspace

$$\mathcal{N} = \ker \begin{bmatrix} C \\ CA \\ \vdots \\ CA^{n-1} \end{bmatrix} .$$

It does not depend on $T > 0$. It is $A$-invariant, it lies inside $\ker C$, and it is the largest subspace with these two properties. Two states are *indistinguishable* exactly when their difference lies in $\mathcal{N}$. The system is observable if and only if $\mathcal{N} = \{0\}$, that is, if the observability matrix has rank $n$; see [Kalman rank condition](/kalman-rank-condition/).

**Duality.** The transpose of the observability matrix of $(C, A)$ is $[C^T, A^T C^T, \dots, (A^T)^{n-1} C^T]$, the controllability matrix of $(A^T, C^T)$. So $(C, A)$ is observable if and only if $(A^T, C^T)$ is controllable. Every test for one property gives a test for the other: the dual [Popov-Belevitch-Hautus test](/popov-belevitch-hautus-test/) asks that $\begin{bmatrix} A - \lambda I \\ C \end{bmatrix}$ have rank $n$ at each eigenvalue $\lambda$, and the [observability gramian](/observability-gramian/) is positive definite exactly for observable pairs.

**How the state is recovered.** With the zero-input output $y_0(t) = C e^{At} x_0$ on $[0, T]$,

$$x_0 = W_o(T)^{-1} \int_0^T e^{A^T t} C^T y_0(t)\, dt, \qquad W_o(T) = \int_0^T e^{A^T t} C^T C e^{At} dt .$$

This is the least squares solution, and it is the formula to use with noisy data. In practice the state is not computed once from a stored record. A [state observer](/state-observer/) estimates it online, and the [Kalman filter](/kalman-filter/) does so with a noise model.

**What does not change it.** A change of state coordinates $(C, A) \to (C T^{-1}, T A T^{-1})$ maps $\mathcal{N}$ to $T \mathcal{N}$. Output injection $A \to A - L C$ keeps $\mathcal{N}$, by the dual of the argument for state feedback on the controllability page. State feedback can destroy observability: it can move a pole onto a zero and cancel it.

**Discrete time.** For $x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$, the outputs $y_0, \dots, y_{n-1}$ determine $x_0$ if and only if the observability matrix has rank $n$, and more samples do not help. The weaker property *reconstructibility* asks only for the current state $x_k$ from past outputs. The two agree when $A$ is invertible. With $A$ nilpotent and $C = 0$, the state is $0$ after $n$ steps whatever $x_0$ was, so it is reconstructible but not observable.

**Nonlinear systems.** For $\dot x = f(x, u)$, $y = h(x)$ the useful notions are local. The observability rank condition asks that the differentials of $h$ and of its repeated [Lie derivatives](/lie-derivative/) along $f$ span the cotangent space at a point. It is a sufficient condition for a local form of observability (local weak observability), and it is not necessary.

## Examples and non-examples

- **Double integrator, position measured.** $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$ and $C = [1, 0]$ give the observability matrix $\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$, rank 2. With zero input, $y(t) = x_1(0) + t\, x_2(0)$, so $y(0)$ gives the position and the slope of $y$ gives the velocity.
- **Double integrator, velocity measured (non-example).** With $C = [0, 1]$ the matrix is $\begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, rank 1, and $\mathcal{N}$ is the position axis. Two masses that move at the same speed from different positions give the same output. A speedometer does not tell where the car is.
- **A hidden mode (non-example).** $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ and $C = [1, 1]$. Here $CA = [-2, -2]$, so the observability matrix $\begin{bmatrix} 1 & 1 \\ -2 & -2 \end{bmatrix}$ has rank 1 and $\mathcal{N}$ is spanned by $(1, -1)$. That vector is an eigenvector of $A$ for the eigenvalue $-1$, and $C (1, -1)^T = 0$, so the mode $e^{-t}$ never shows in the output. The transfer function is $(s + 1)/((s + 1)(s + 2)) = 1/(s + 2)$: the pole at $-1$ cancels with a zero.
- **Sampling can destroy observability.** The oscillator $A = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$ with $C = [1, 0]$ is observable. Sampled with the period $h = \pi$ s, $A_d = e^{A\pi} = -I$, and the observability matrix $\begin{bmatrix} 1 & 0 \\ -1 & 0 \end{bmatrix}$ has rank 1. The samples $x_1(k\pi)$ alternate in sign and never show the velocity.
- **Reconstructible but not observable (discrete time).** $n = 1$, $A = 0$, $C = 0$: after one step the state is $0$, so the current state is known, but $x_0$ is lost.

## Related definitions

- [Controllability](/controllability/): the dual property.
- [Detectability](/detectability/): every mode that the output cannot see is asymptotically stable.
- [Kalman rank condition](/kalman-rank-condition/) and [Popov-Belevitch-Hautus test](/popov-belevitch-hautus-test/): the algebraic tests, proved on their pages for controllability and applied here by duality.
- [Observability gramian](/observability-gramian/): the output energy of each initial state.
- [Kalman decomposition](/kalman-decomposition/): coordinates that split off the unobservable part.
- [Observable canonical form](/observable-canonical-form/): the companion form of an observable single-output pair.
- [State observer](/state-observer/): a dynamic system whose state converges to the plant state; it exists with arbitrary error eigenvalues for observable pairs and with decaying error for detectable pairs.

## References
