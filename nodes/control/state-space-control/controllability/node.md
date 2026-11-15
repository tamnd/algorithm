---
tag: 8B4NJD
kind: definition
slug: controllability
name: Controllability
aliases:
- state controllability
- complete controllability
area: control/state-space-control
level: core
summary: A system is controllable if some input moves it from any initial state to any final state in finite time.
prereqs: [state-space-representation, variation-of-constants-formula]
see_also: [kalman-rank-condition, popov-belevitch-hautus-test, controllability-gramian, observability, stabilizability, kalman-decomposition, pole-placement-theorem, minimum-energy-control]
sources:
  - paper: "R. E. Kalman, Contributions to the theory of optimal control, Boletín de la Sociedad Matemática Mexicana (2) 5, 102-119, 1960"
    locator: the definition of controllability for linear systems and its test by the integral that is now called the controllability gramian
  - paper: "R. E. Kalman, Y. C. Ho and K. S. Narendra, Controllability of linear dynamical systems, Contributions to Differential Equations 1, 189-213, 1963"
    locator: controllability of time-invariant and time-varying linear systems, the rank test, and the loss of controllability by sampling
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 6.2 (controllability), Section 6.6 (controllability to the origin and reachability in discrete time), Section 6.7 (controllability after sampling) and Section 6.8 (time-varying systems)
  - book: isbn:9780387984896
    title: Eduardo D. Sontag, Mathematical Control Theory, Deterministic Finite Dimensional Systems, second edition, Springer, 1998
    locator: Chapter 3, Reachability and Controllability
---

A linear system is controllable when its input can move the state from any initial state to any other state in finite time. It is the property that makes state feedback design possible: by the [pole placement theorem](/pole-placement-theorem/), the eigenvalues of $A - BK$ can be put anywhere exactly when the pair $(A, B)$ is controllable. The dual property for the output is [observability](/observability/), and the weaker property that the input can at least stabilize the system is [stabilizability](/stabilizability/). This page is about dynamical systems; the [dynamic controllability](/dynamic-controllability/) of temporal networks in planning is a different notion.

## Definition

**Notation.** The system is the continuous-time [state-space model](/state-space-representation/)

$$\dot x(t) = A x(t) + B u(t), \qquad x(t) \in \mathbb{R}^n, \quad u(t) \in \mathbb{R}^m,$$

with real matrices $A$ ($n \times n$) and $B$ ($n \times m$). Inputs are piecewise continuous functions of the time $t$ in seconds. By the [variation of constants formula](/variation-of-constants-formula/), the state at time $T$ is

$$x(T) = e^{AT} x(0) + \int_0^T e^{A(T - s)} B\, u(s)\, ds .$$

The output equation $y = C x + D u$ plays no part in controllability.

**Definition.** The pair $(A, B)$, or the system, is *controllable* if for every $x_0 \in \mathbb{R}^n$ and every $x_1 \in \mathbb{R}^n$ there are a time $T > 0$ and an input $u$ on $[0, T]$ such that the solution with $x(0) = x_0$ has $x(T) = x_1$.

**Two weaker looking notions.** A state $x_1$ is *reachable* if some input steers $x(0) = 0$ to $x(T) = x_1$. A state $x_0$ is *controllable to the origin* if some input steers $x(0) = x_0$ to $x(T) = 0$. For a continuous-time linear time-invariant system the three properties "controllable", "every state is reachable" and "every state is controllable to the origin" are equivalent, and the time $T$ can be any positive number. The reason is that $e^{AT}$ is invertible, so the map from $x_0$ to $x(T)$ for a fixed input is a bijection.

**The reachable subspace.** The set of states reachable from $0$ is the subspace

$$\mathcal{R} = \operatorname{range} \begin{bmatrix} B & AB & A^2 B & \cdots & A^{n-1} B \end{bmatrix}.$$

It does not depend on $T > 0$. It is $A$-invariant, it contains the range of $B$, and it is the smallest subspace with these two properties. The system is controllable if and only if $\mathcal{R} = \mathbb{R}^n$. The proof and the rank test are on [Kalman rank condition](/kalman-rank-condition/). Two other tests give the same answer: the [Popov-Belevitch-Hautus test](/popov-belevitch-hautus-test/), which checks one eigenvalue at a time, and the [controllability gramian](/controllability-gramian/) $W_c(T) = \int_0^T e^{As} B B^T e^{A^T s} ds$, which is positive definite exactly when the pair is controllable.

**The input that does the job.** If $W_c(T)$ is invertible, the input

$$u(t) = B^T e^{A^T (T - t)}\, W_c(T)^{-1} \bigl(x_1 - e^{AT} x_0\bigr), \qquad 0 \le t \le T,$$

steers $x_0$ to $x_1$ at time $T$. Among all inputs that do this, it has the least energy $\int_0^T |u(t)|^2 dt$, and that energy is $(x_1 - e^{AT} x_0)^T W_c(T)^{-1} (x_1 - e^{AT} x_0)$. See [minimum energy control](/minimum-energy-control/).

**What does not change it.** Controllability is a property of the pair, not of the coordinates. A change of state coordinates $(A, B) \to (T A T^{-1}, T B)$ maps $\mathcal{R}$ to $T \mathcal{R}$. State feedback $u = -K x + v$ gives the pair $(A - BK, B)$, and $\mathcal{R}$ stays the same, because $(A - BK)^k B$ is $A^k B$ plus a combination of the columns of $B, AB, \dots, A^{k-1} B$. An invertible change of input coordinates $B \to B M$ also keeps $\mathcal{R}$.

**Discrete time.** For $x_{k+1} = A x_k + B u_k$, the states reachable from $0$ in $N$ steps form the range of $[B, AB, \dots, A^{N-1} B]$, and this range stops growing at $N = n$. Every state is reachable if and only if this matrix has rank $n$ for $N = n$. Here the notions split: every state is controllable to the origin if and only if $\operatorname{range} A^n \subseteq \mathcal{R}$, which holds for every nilpotent $A$, whatever $B$ is. The two notions agree when $A$ is invertible, as for every sampled system with $A_d = e^{Ah}$.

**Time-varying and nonlinear systems.** For $\dot x = A(t) x + B(t) u$ the definition is the same on a fixed interval $[t_0, t_1]$, and the test is the gramian $\int_{t_0}^{t_1} \Phi(t_1, s) B(s) B(s)^T \Phi(t_1, s)^T ds$ with the [state transition matrix](/state-transition-matrix/) $\Phi$; see [linear time-varying system](/linear-time-varying-system/). For a nonlinear system $\dot x = f(x, u)$ the usual notions are local, near an equilibrium. If the linearization at an equilibrium is controllable, the nonlinear system is locally controllable there (Sontag 1998, Chapter 3). The [Lie algebra rank condition](/lie-algebra-rank-condition/) gives local accessibility, which is weaker.

## Examples and non-examples

- **Double integrator.** A unit mass with position $x_1$, velocity $x_2$ and force $u$ has $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$ and $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$. Then $[B, AB] = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$ has rank 2, so the system is controllable. To move from rest at $0$ to rest at position $1$ in $T = 1$ s, the gramian is $W_c(1) = \begin{bmatrix} 1/3 & 1/2 \\ 1/2 & 1 \end{bmatrix}$, the minimum energy input is $u(t) = 6 - 12 t$, and its energy is $\int_0^1 (6 - 12t)^2 dt = 12$. A direct integration gives velocity $\int_0^1 (6 - 12 t) dt = 0$ and position $\int_0^1 (1 - s)(6 - 12 s) ds = 1$ at $t = 1$.
- **Two equal tanks, one input (non-example).** $A = \begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix}$ and $B = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$. The difference $x_1 - x_2$ obeys $(x_1 - x_2)' = -(x_1 - x_2)$ whatever the input is, so no input changes it. The matrix $[B, AB] = \begin{bmatrix} 1 & -1 \\ 1 & -1 \end{bmatrix}$ has rank 1, and $\mathcal{R}$ is the line $x_1 = x_2$.
- **Two different tanks.** With $A = \operatorname{diag}(-1, -2)$ and the same $B$, $[B, AB] = \begin{bmatrix} 1 & -1 \\ 1 & -2 \end{bmatrix}$ has determinant $-1$, so the pair is controllable. One input can steer two decoupled modes when their eigenvalues differ and the input reaches each mode.
- **A mode the input does not reach (non-example).** $A = \operatorname{diag}(1, -2)$ and $B = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$: the second state obeys $x_2' = -2 x_2$ for every input. The pair is not controllable. It is still [stabilizable](/stabilizability/), because the mode that the input does not reach decays.
- **Sampling can destroy controllability.** The oscillator $A = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ is controllable. Its [zero-order-hold model](/zero-order-hold-discretization/) with the sampling period $h = \pi$ s is $A_d = e^{A\pi} = -I$ and $B_d = \int_0^\pi e^{As} ds\, B = \begin{bmatrix} 2 \\ 0 \end{bmatrix}$. Then $[B_d, A_d B_d] = \begin{bmatrix} 2 & -2 \\ 0 & 0 \end{bmatrix}$ has rank 1, so the sampled system is not controllable. The eigenvalues $\pm i$ differ by $2i$, and $h = \pi$ makes $e^{ih} = e^{-ih}$.
- **Controllable to the origin but not reachable (discrete time).** With $n = 1$, $A = 0$ and $B = 0$, the system $x_{k+1} = 0$ sends every state to $0$ in one step, so every state is controllable to the origin. No state other than $0$ is reachable.

## Related definitions

- [Observability](/observability/): the dual property. The pair $(C, A)$ is observable if and only if $(A^T, C^T)$ is controllable.
- [Stabilizability](/stabilizability/): every mode that the input cannot reach is asymptotically stable.
- [Kalman rank condition](/kalman-rank-condition/) and [Popov-Belevitch-Hautus test](/popov-belevitch-hautus-test/): the two algebraic tests, proved on their pages.
- [Controllability gramian](/controllability-gramian/): the integral that measures how much energy each direction needs.
- [Kalman decomposition](/kalman-decomposition/): coordinates that split off the part of the state that the input cannot reach.
- [Controllable canonical form](/controllable-canonical-form/): the companion form of a controllable single-input pair.
- [Controlled invariant subspace](/controlled-invariant-subspace/): a subspace that state feedback can make invariant. It is a tool of geometric control, not a test of controllability.
- *Output controllability*: the output, not the state, can be steered to any value. For $y = C x + D u$ the test is $\operatorname{rank} [CB, CAB, \dots, CA^{n-1} B, D] = p$, where $p$ is the number of outputs. Neither property implies the other: a controllable pair with $C = 0$ and $D = 0$ is not output controllable.

## References
