---
tag: H8NC6E
kind: problem
slug: minimum-energy-control
name: Minimum-energy control
aliases:
- minimum-norm control
area: control/optimal-and-predictive-control
level: core
summary: Reach a given state at a given time with the input of least energy, solved by a formula in the controllability Gramian.
model: real-ram
prereqs: [controllability-gramian, controllability, matrix-exponential]
see_also: [lqr-problem, finite-horizon-lqr, reachability, observability-gramian, balanced-truncation, pontryagin-maximum-principle, bang-bang-control, zero-order-hold-discretization]
sources:
  - book: isbn:9781611973877
    title: Roger W. Brockett, Finite Dimensional Linear Systems, Wiley, 1970 (SIAM Classics in Applied Mathematics 74, 2015)
    locator: the treatment of controllability and of inputs of least norm
  - paper: doi:10.1109/TAC.1978.1101743
    title: Charles F. Van Loan, Computing integrals involving the matrix exponential, IEEE Transactions on Automatic Control 23(3), 395-404, 1978
    locator: integrals such as the Gramian computed from the exponential of one block triangular matrix
---

The minimum-energy control problem asks for the input that moves a linear system $\dot x = A x + B u$ from a given state $x_0$ to a given state $x_1$ in a given time $t_1$, with the least energy $\int_0^{t_1} |u(t)|^2\, dt$. If the [controllability Gramian](/controllability-gramian/) $W(t_1) = \int_0^{t_1} e^{A s} B B^T e^{A^T s}\, ds$ is invertible, the answer is unique and has a closed form:

$$u^*(t) = B^T e^{A^T (t_1 - t)} W(t_1)^{-1} d, \qquad d = x_1 - e^{A t_1} x_0,$$

and the least energy is $d^T W(t_1)^{-1} d$. The Gramian is invertible exactly when the system has [controllability](/controllability/), so the problem is also the standard proof that a controllable system can reach every state. The discrete-time problem has the same form with the $N$-step Gramian and is a least-norm solution of a linear system. The formula belongs to the controllability theory of linear systems that Kalman, Ho and Narendra developed in the early 1960s; textbooks such as Brockett (1970) present it as a least-norm problem in a space of functions, and Van Loan (1978) gave the block exponential method that computes the Gramian.

## In plain words

You must bring the system to a target at a fixed time and you pay for the square of the input. Of all the inputs that arrive on time, take the one that is cheapest. Without the free motion, the system would need to cover the distance $d$. The input that does this cheaply pushes hardest in the directions where the input moves the state easily, and the Gramian measures how easily each direction is reached. A target in a direction where $W$ has a small eigenvalue is expensive, and a short time $t_1$ makes every target expensive.

## Definition

**Input.** Real matrices $A$ ($n \times n$) and $B$ ($n \times m$), states $x_0, x_1 \in \mathbb{R}^n$ and a time $t_1 > 0$.

**Output.** An input $u^* : [0, t_1] \to \mathbb{R}^m$, square integrable, such that the solution of $\dot x = A x + B u^*$, $x(0) = x_0$ has $x(t_1) = x_1$, and

$$\int_0^{t_1} |u^*(t)|^2\, dt \le \int_0^{t_1} |u(t)|^2\, dt$$

for every input $u$ with the same property; or the answer that no input reaches $x_1$.

**Solution.** Let $d = x_1 - e^{A t_1} x_0$. If $W(t_1)$ is invertible, the unique optimal input is the formula above. The proof (proofs/correctness.md) writes the reached state as $e^{A t_1} x_0 + \mathcal{L} u$ for a linear map $\mathcal{L}$ from inputs to $\mathbb{R}^n$, shows that $\mathcal{L} \mathcal{L}^* = W$, and finds that $u^* = \mathcal{L}^* W^{-1} d$ is orthogonal to every input that $\mathcal{L}$ maps to 0. Any other admissible input is $u^* + v$ with $\mathcal{L} v = 0$, and its energy is $|u^*|^2 + |v|^2$. If $W(t_1)$ is singular, the reachable values of $d$ lie in a proper subspace, the range of $W(t_1)$; for $d$ in that range the formula holds with the pseudoinverse.

## Variants

- **Discrete time.** For $x_{k+1} = A x_k + B u_k$ and $N$ steps, minimize $\sum_{k=0}^{N-1} |u_k|^2$ with $x_N = x_1$. With $W_N = \sum_{j=0}^{N-1} A^j B B^T (A^T)^j$ and $d = x_1 - A^N x_0$, the answer is $u_k = B^T (A^T)^{N-1-k} W_N^{-1} d$, energy $d^T W_N^{-1} d$. It is rational for rational data.
- **Weighted energy.** Minimize $\int u^T R u\, dt$ with $R > 0$: replace $B B^T$ by $B R^{-1} B^T$ in the Gramian and $B^T$ by $R^{-1} B^T$ in the input.
- **Time-varying systems.** Replace $e^{A (t - s)}$ by the state transition matrix $\Phi(t, s)$ in all formulas.
- **Soft target.** Penalize $x(t_1) - x_1$ in place of requiring it to be zero. This is a [finite-horizon LQR](/finite-horizon-lqr/) problem with $Q = 0$ and a terminal weight $Q_f$, and as $Q_f \to \infty$ its solution tends to the minimum-energy input.
- **Input bounds.** With $|u_i| \le 1$ there is no closed form. Minimum time with bounded input gives [bang-bang control](/bang-bang-control/), and minimum fuel $\int |u|\, dt$ gives inputs that switch between $-1$, $0$ and $1$; both follow from the [maximum principle](/pontryagin-maximum-principle/).

## Examples

**Double integrator.** $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, so $e^{A s} B = \begin{bmatrix} s \\ 1 \end{bmatrix}$ and

$$W(t_1) = \int_0^{t_1} \begin{bmatrix} s^2 & s \\ s & 1 \end{bmatrix} ds = \begin{bmatrix} t_1^3/3 & t_1^2/2 \\ t_1^2/2 & t_1 \end{bmatrix}.$$

Move from rest at 0 to rest at 1 in $t_1 = 1$: $d = (1, 0)$, $W^{-1} = \begin{bmatrix} 12 & -6 \\ -6 & 4 \end{bmatrix}$, $\eta = W^{-1} d = (12, -6)$. With $e^{A^T \tau} \eta = (12, 12 \tau - 6)$ and $\tau = 1 - t$, the input is $u^*(t) = 6 - 12 t$: full push at the start, full brake at the end, and it changes sign at $t = 1/2$. The energy is $\int_0^1 (6 - 12 t)^2\, dt = 12 = d^T \eta$. For a general time the energy is $12 / t_1^3$, so half the time costs eight times the energy.

**A stable scalar plant.** $a = -1$, $b = 1$: $W(t_1) = (1 - e^{-2 t_1})/2$. From $0$ to $1$ in $t_1 = 1$ the energy is $2/(1 - e^{-2}) \approx 2.3130$, and $u^*(t) = e^{-(1 - t)} / W(1)$ grows toward the end, since an early push decays before $t_1$.

**Discrete scalar plant.** $x_{k+1} = 2 x_k + u_k$ from 0 to 21 in 3 steps: $C = [4, 2, 1]$, $W_3 = 21$, $\eta = 1$, so $u = (4, 2, 1)$ and the energy is 21. Early inputs are larger because the plant doubles them.

**No solution.** $A = I_2$, $B = (1, 1)^T$. Both states move together, $W$ is a multiple of $\begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}$ and is singular, and the target $(1, 0)$ from $0$ cannot be reached.

## Known algorithms

The closed form is computed in a fixed number of matrix operations:

```pseudo id=main
MINIMUM-ENERGY-CONTROL(A, B, x_0, x_1, t_1)
L1  W ← Gramian(A, B, t_1)          ▷ e^{M t_1}, M = [[-A, B B^T], [0, A^T]] (Van Loan)
L2  if W is not positive definite then return "x_1 cannot be reached from every x_0"
L3  d ← x_1 - e^{A t_1} x_0
L4  η ← W^(-1) d
L5  u(t) ← B^T e^{A^T (t_1 - t)} η, for 0 ≤ t ≤ t_1
L6  return u and the energy d^T η
```

Line L1 uses Van Loan's block method (1978): if $e^{M t_1} = \begin{bmatrix} \cdot & G \\ 0 & F \end{bmatrix}$, then $F = e^{A^T t_1}$, $G = e^{-A t_1} W(t_1)$, and $W(t_1) = F^T G$. Other ways to compute the Gramian are numerical quadrature of the integral, and the [Lyapunov equation](/lyapunov-equation/) $A W + W A^T + B B^T = e^{A t_1} B B^T e^{A^T t_1}$, which has a unique solution when $\lambda_i + \lambda_j \ne 0$ for all eigenvalues $\lambda_i, \lambda_j$ of $A$, including $i = j$. Line L4 should use a Cholesky factorization, as $W$ is symmetric positive definite. The discrete-time problem is the least-norm solution of $C u = d$ for the reachability matrix $C = [A^{N-1} B, \dots, B]$, solved exactly in rational arithmetic by $u = C^T (C C^T)^{-1} d$.

The implementation computes both versions. Its tests compare the Gramian with the Lyapunov equation on 500 random systems, simulate the plant together with the optimal input (RK4, step $0.01$) and check that the state reaches $x_1$ within $10^{-6}$ with the stated energy, check that piecewise constant inputs on finer grids cost more and tend to the optimum, and compare the discrete answer with the solution of the KKT system of the least-norm problem in exact arithmetic on 500 random problems.

## Bounds

- **Cost.** In the [real RAM](/real-ram/), lines L2 to L4 cost $O(n^3)$. The exponential in line L1 by scaling and squaring costs $O(n^3 \log(\|A\| t_1 + 2))$ operations to a fixed accuracy. Each evaluation of $u(t)$ costs one more exponential. On a time grid it is cheaper to integrate the adjoint system $\dot z = -A^T z$ from $z(0) = e^{A^T t_1} \eta$ and set $u = B^T z$, at $O(n^2 + n m)$ per step. The discrete version costs $O(N n^2 m + n^3)$.
- **Energy bounds.** $|d|^2 / \lambda_{\max}(W) \le d^T W^{-1} d \le |d|^2 / \lambda_{\min}(W)$. The eigenvectors of $W$ for small eigenvalues are the hard directions.
- **Short horizons.** For the double integrator, the energy grows like $t_1^{-3}$ for a change of position. In general, for a target that needs $k$ integrations of the input, the energy grows like $t_1^{-(2 k - 1)}$ as $t_1 \to 0$.
- **Exactness.** In continuous time the answer involves $e^{A t_1}$ and is not rational in general. In discrete time it is rational for rational data and the formula is exact.

## Reductions

- **To least norm in a Hilbert space.** The problem is the least-norm solution of the linear equation $\mathcal{L} u = d$, from the space of square integrable inputs to $\mathbb{R}^n$. The answer is the projection of 0 on an affine subspace, $u^* = \mathcal{L}^* (\mathcal{L} \mathcal{L}^*)^{-1} d$, and $\mathcal{L} \mathcal{L}^* = W$. The discrete version is the same with $\mathcal{L} = C$.
- **To LQR.** As a limit of [LQR](/lqr-problem/) problems with a terminal weight, see Variants. Conversely, the minimum-energy input is the open-loop input of an LQR problem with a terminal constraint.
- **The reachable set.** The states reachable from 0 at time $t_1$ with energy at most 1 form the ellipsoid $\{x : x^T W(t_1)^{-1} x \le 1\}$. The dual statement for the [observability Gramian](/observability-gramian/) gives the output energy of an initial state, and [balanced truncation](/balanced-truncation/) uses both ellipsoids to find the states that are hard to reach and hard to observe.

## Applications

- Proof of reachability: the formula gives an explicit input for every target when $W$ is invertible, so it is the usual proof that the Gramian test or the rank test of [controllability](/controllability/) is sufficient.
- Open-loop transfers, such as moving a satellite or a flexible arm between two rest states, where the energy is a proxy for fuel or heating.
- The energy $d^T W^{-1} d$ as a measure of how hard a system is to control, for example to compare actuator placements, or the nodes of a network that receive the input.
- Model reduction: the Gramian energy of a state is the input energy needed to reach it, which is how balanced truncation ranks states.

## References
