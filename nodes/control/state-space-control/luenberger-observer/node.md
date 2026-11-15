---
tag: 7T6PY4
kind: algorithm
slug: luenberger-observer
name: Luenberger observer
aliases:
- full-order observer
- Luenberger state observer
area: control/state-space-control
level: core
summary: Estimates the state by a copy of the model corrected by L times the output error, with error dynamics A - LC placed by the choice of L.
solves: [state-estimation]
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of inputs, p: the number of outputs, N: the number of updates}
  time: {worst: "O(p n^4 + N n (n + m + p))"}
  space: {extra: "O(n (n + p))"}
properties: {deterministic: true, exact: true, recursive: true, online: true}
history:
  year: 1964
  people: [David G. Luenberger]
  note: "Luenberger introduced the observer in 1964 as a linear system driven by the inputs and outputs of the plant whose state tracks a linear function of the plant state, and gave the canonical forms for multi-output design in 1966 and 1971."
prereqs: [state-observer, observability, pole-placement-theorem, ackermann-formula]
see_also: [state-observer, reduced-order-observer, separation-principle, unknown-input-observer, kalman-filter, high-gain-observer, detectability, observable-canonical-form]
sources:
  - paper: doi:10.1109/tme.1964.4323124
    title: David G. Luenberger, Observing the state of a linear system, IEEE Transactions on Military Electronics 8(2), 74-80, 1964
    locator: the definition of an observer and the result that its error decays with eigenvalues that can be chosen
  - paper: doi:10.1109/tac.1966.1098323
    title: David G. Luenberger, Observers for multivariable systems, IEEE Transactions on Automatic Control 11(2), 190-197, 1966
    locator: the design of observers for systems with several outputs
  - paper: doi:10.1109/tac.1971.1099826
    title: David G. Luenberger, An introduction to observers, IEEE Transactions on Automatic Control 16(6), 596-602, 1971
    locator: the tutorial account of the identity observer and its error equation
  - paper: doi:10.1109/tac.1977.1101617
    title: M. L. J. Hautus, A simple proof of Heymann's lemma, IEEE Transactions on Automatic Control 22(5), 885-886, 1977
    locator: the construction of a feedback that makes a multi-input pair controllable from one input, used here for several outputs
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 8.4, State Estimator, and Section 8.7, State Estimators, Multivariable Case
  - book: isbn:9780691193984
    title: Karl J. Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 8, Output Feedback, the section State Estimation
---

A Luenberger observer estimates the state of a linear system $\dot x = A x + B u$, $y = C x$ from the input $u$ and the measured output $y$. It runs a copy of the model and corrects it with a gain $L$ times the output error:

$$\dot{\hat x} = A \hat x + B u + L (y - C \hat x).$$

The error $e = x - \hat x$ obeys $\dot e = (A - LC) e$, whatever the input is. The design task is to choose $L$ so that $A - LC$ is Hurwitz with chosen eigenvalues. This is the [pole placement problem](/pole-placement-problem/) for the dual pair $(A^T, C^T)$, and it has a solution for all eigenvalues if and only if $(C, A)$ is [observable](/observability/). This page gives the full-order observer, which estimates all $n$ states. The [state observer](/state-observer/) page defines observers in general. The [reduced-order observer](/reduced-order-observer/) estimates only the $n - p$ states that the output does not give directly. The [unknown input observer](/unknown-input-observer/) and the [disturbance observer](/disturbance-observer/) handle inputs that are not measured. The [high-gain observer](/high-gain-observer/) and the [sliding mode observer](/sliding-mode-observer/) are for nonlinear systems. The [Kalman-Bucy filter](/kalman-bucy-filter/) has the same structure, but it gets $L$ from noise statistics, while the observer on this page uses no noise model.

## In plain words

Some quantities of a machine can be measured, and some cannot. The observer is a computer model of the machine that gets the same commands as the machine. The model would drift away from the real machine if its starting point were wrong. So the observer compares the measured output of the machine with the output that the model predicts. It pushes the model toward the machine in proportion to the difference. The designer chooses how hard to push. With a good choice, the error of the model dies out at a chosen speed, whatever commands the machine gets. This is possible only when the measurements together show every part of the state over time. Pushing very hard makes the error die out fast, but it also passes more sensor noise into the estimate.

## The problem

Input: $A \in \mathbb{R}^{n \times n}$, $C \in \mathbb{R}^{p \times n}$ and a monic real polynomial $\alpha(s) = s^n + \alpha_1 s^{n-1} + \cdots + \alpha_n$, usually $\alpha(s) = \prod_i (s - \mu_i)$ for chosen observer poles $\mu_i$ in conjugate pairs. Output: $L \in \mathbb{R}^{n \times p}$ with $\det(sI - (A - LC)) = \alpha(s)$, and the observer that uses it. A solution exists for every $\alpha$ if and only if $(C, A)$ is observable. If $(C, A)$ is only [detectable](/detectability/), a stable $A - LC$ still exists, but the unobservable eigenvalues cannot be moved.

In discrete time the model is $x_{k+1} = A x_k + B u_k$, $y_k = C x_k$, the observer is $\hat x_{k+1} = A \hat x_k + B u_k + L(y_k - C \hat x_k)$, and $A - LC$ must be Schur. The design of $L$ is the same.

## The algorithm

```pseudo id=main
LUENBERGER-GAIN(A, C, alpha)
L1  K_d ← PLACE(A^T, C^T, alpha)          ▷ fails if (C, A) is not observable
L2  return L ← K_d^T                     ▷ A - L C = (A^T - C^T K_d)^T
LUENBERGER-UPDATE(xhat, u, y)
L3  r ← y - C xhat                        ▷ output error, p numbers
L4  return A xhat + B u + L r             ▷ the derivative, or the next estimate in discrete time
```

Line L1 solves a state feedback problem. The matrices $A - LC$ and $A^T - C^T L^T$ are transposes of each other, so they have the same characteristic polynomial, and $(C, A)$ is observable if and only if $(A^T, C^T)$ is [controllable](/controllability/). With one output, PLACE is [Ackermann's formula](/ackermann-formula/). With several outputs, the implementation uses the construction of Hautus for Heymann's lemma: it starts with one column $b$ of $C^T$ and builds vectors $x_1 = b$, $x_{k+1} = A^T x_k + C^T u_k$ with $u_k$ equal to $0$ or a unit vector, so that each new vector is independent of the earlier ones. The feedback $F$ with $F x_k = u_k$ makes $(A^T + C^T F, b)$ controllable, and Ackermann's formula then places the poles of this single-input pair. The [pole placement theorem](/pole-placement-theorem/) page proves that this construction always succeeds for a controllable pair. Lines L3 and L4 run at each time step, with an ODE solver in continuous time or as a plain recursion in discrete time.

## Example

**Double integrator.** A cart with position $x_1$ and velocity $x_2$ has $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, and only the position is measured, $C = \begin{bmatrix} 1 & 0 \end{bmatrix}$. For the observer poles $-2$ and $-3$, $\alpha(s) = s^2 + 5s + 6$. With $L = \begin{bmatrix} l_1 \\ l_2 \end{bmatrix}$,

$$A - LC = \begin{bmatrix} -l_1 & 1 \\ -l_2 & 0 \end{bmatrix}, \qquad \det(sI - (A - LC)) = s^2 + l_1 s + l_2,$$

so $L = \begin{bmatrix} 5 \\ 6 \end{bmatrix}$. The observer is $\dot{\hat x}_1 = \hat x_2 + 5(y - \hat x_1)$, $\dot{\hat x}_2 = u + 6(y - \hat x_1)$. If the observer starts at the true position but with a velocity error of 1, the error is

$$e_1(t) = e^{-2t} - e^{-3t}, \qquad e_2(t) = 3e^{-2t} - 2e^{-3t},$$

whatever the input $u$ is:

| $t$ | 0 | 0.5 | 1 | 2 | 3 |
|---|---|---|---|---|---|
| position error $e_1$ | 0 | 0.145 | 0.086 | 0.016 | 0.002 |
| velocity error $e_2$ | 1 | 0.657 | 0.306 | 0.050 | 0.007 |

**Deadbeat observer.** For the [zero-order hold](/zero-order-hold-discretization/) model of the same cart with period $h$, $A = \begin{bmatrix} 1 & h \\ 0 & 1 \end{bmatrix}$. The polynomial $\alpha(z) = z^2$ gives $L = \begin{bmatrix} 2 \\ 1/h \end{bmatrix}$, and $(A - LC)^2 = 0$. The estimate is then exact after two samples, for every initial error and every input sequence. This is the dual of [deadbeat control](/deadbeat-control/).

**Two outputs.** For $A = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 1 & 0 & 0 \end{bmatrix}$ and $C = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 0 & 1 \end{bmatrix}$ with the poles $-1, -2, -3$, the implementation starts from the first output, which alone already makes the pair observable, and returns $L = \begin{bmatrix} 6 & 0 \\ 11 & 0 \\ 7 & 0 \end{bmatrix}$. This is one valid gain among many. [Robust pole placement](/robust-pole-placement/) uses the freedom to get a better conditioned $A - LC$.

## Correctness

The error equation follows by subtraction: $\dot x - \dot{\hat x} = Ax + Bu - A\hat x - Bu - L(Cx - C\hat x) = (A - LC)(x - \hat x)$. The input cancels, so the error is $e(t) = e^{(A - LC)t} e(0)$ for every input, and it goes to 0 if and only if $A - LC$ is Hurwitz. The gain of line L2 gives $\det(sI - (A - LC)) = \det(sI - (A^T - C^T K_d)) = \alpha(s)$, because a matrix and its transpose have the same determinant. The correctness of PLACE is the [pole placement theorem](/pole-placement-theorem/), proved constructively by the same steps. The full proof is in [proofs/correctness.md](proofs/correctness.md). The tests check the exact characteristic polynomial for random systems with up to 3 outputs, the error of a simulated observer against $e^{(A - LC)t} e(0)$ for an unstable plant, and the exact convergence of a deadbeat observer in $n$ steps.

## Complexity

PLACE builds $n$ vectors. For each new vector it tests at most $p + 1$ candidates, and each test is a rank computation on at most $n$ vectors of length $n$, which costs $O(n^3)$. This gives $O(p n^4)$ for the gain. A rank test that updates one elimination instead of starting again brings this down to $O(p n^3)$, and the solve for $F$ and Ackermann's formula cost $O(n^3)$. Each update of lines L3 and L4 costs $O(n^2 + nm + np)$. An RK4 step calls it four times.

## Properties

- **The error is independent of the input.** Feedback $u = -K\hat x$ therefore does not change the error dynamics, which is the basis of the [separation principle](/separation-principle/).
- **No noise model.** The observer assumes exact measurements and an exact model. With noise, a fast observer passes more noise into $\hat x$; the [Kalman filter](/kalman-filter/) chooses $L$ to balance this.
- **Exact arithmetic.** With rational data the implementation is exact, so the characteristic polynomial matches $\alpha$ exactly.
- **Non-uniqueness.** With one output, $L$ is unique for a given $\alpha$. With several outputs, a family of gains gives the same eigenvalues but different eigenvectors.
- **Peaking.** A fast observer can have a large transient error before the error decays, because $A - LC$ is far from normal for large $L$. The [high-gain observer](/high-gain-observer/) page studies this effect.

## Variants and improvements

- **Reduced-order observer.** When $p$ outputs are measured exactly, only $n - p$ states need estimating. See [reduced-order observer](/reduced-order-observer/).
- **Kalman filter.** The gain that minimizes the error covariance for white process and measurement noise. See [Kalman filter](/kalman-filter/) and [Kalman-Bucy filter](/kalman-bucy-filter/).
- **Observers for unknown inputs.** If part of the input is not measured, an [unknown input observer](/unknown-input-observer/) decouples the error from it, and a [disturbance observer](/disturbance-observer/) estimates it.
- **Current observer.** In discrete time, the estimate of $x_k$ can use $y_k$ itself, not only $y_{k-1}$. This removes one sample of delay from the estimate.
- **Nonlinear systems.** Copy the nonlinear model and add $L(y - h(\hat x))$; the [high-gain observer](/high-gain-observer/) and the [sliding mode observer](/sliding-mode-observer/) give conditions under which this works.

## When to use it

Use the full-order observer when the model is known well, the noise is small or not characterized, and a simple, fixed linear estimator is wanted, for example for state feedback in an embedded controller. Choose the observer poles a few times faster than the controller poles, but not so fast that sensor noise dominates. If the outputs are exact and the computing budget is tight, use the reduced-order observer. If noise statistics are known, use the Kalman filter.

## Pitfalls

- **Unobservable modes.** If $(C, A)$ is not observable, PLACE fails. If the unobservable modes are stable, design for the observable part only; if one is unstable, no observer converges.
- **Too fast poles.** Large $L$ amplifies sensor noise and causes peaking. Check the error transient and the noise gain, not only the eigenvalues.
- **Model mismatch.** The error equation holds only for the exact model. A wrong $A$ or $B$ gives a bias that the input drives.
- **Different inputs.** The observer must get the same input as the plant. If the actuator saturates, feed the saturated value to the observer; see [anti-windup](/anti-windup/).
- **Numerical conditioning.** Ackermann's formula is unstable for larger $n$. For more than a few states use a numerically stable method on $(A^T, C^T)$.

## Implementations

## History

Luenberger introduced the observer in 1964, in a paper that showed how a linear system driven by the inputs and outputs of a plant can reconstruct its state, with an error that decays at a rate the designer chooses. His 1966 paper treated systems with several outputs, and his 1971 tutorial gave a short account of the identity observer and the reduced-order observer. The duality with state feedback, which turns the observer design into pole placement for $(A^T, C^T)$, follows Kalman's duality between controllability and observability. The Kalman-Bucy filter of 1961 has the same structure and gets its gain from noise statistics.

## References
