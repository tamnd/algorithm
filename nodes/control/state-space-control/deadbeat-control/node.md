---
tag: HZQ8MT
kind: algorithm
slug: deadbeat-control
name: Deadbeat control
aliases:
- deadbeat controller
area: control/state-space-control
level: core
summary: A discrete-time state feedback that places all closed-loop poles at the origin, so the state reaches zero in at most n steps.
solves: [pole-placement-problem]
model: real-ram
complexity:
  vars: {n: the number of states, m: the number of inputs, N: the number of steps to reach zero}
  time: {worst: "O(N n^2 (n + m))"}
  space: {extra: "O(n (n + m))"}
properties: {deterministic: true, exact: true, recursive: false, online: false}
history:
  year: 1981
  people: [John O'Reilly]
  note: "Finite settling time designs for sampled systems date from the early years of sampled-data control; O'Reilly surveyed the state-space theory of discrete time-optimal control, deadbeat control among it, in 1981."
prereqs: [ackermann-formula, pole-placement-theorem, zero-order-hold-discretization, controllability]
see_also: [pole-placement-problem, ackermann-formula, robust-pole-placement, luenberger-observer, sampled-data-system, z-transform, state-feedback, minimum-energy-control]
sources:
  - paper: doi:10.1016/0005-1098(81)90053-4
    title: John O'Reilly, The discrete linear time invariant time-optimal control problem, an overview, Automatica 17(2), 363-370, 1981
    locator: the survey of the minimum-time problem for discrete linear systems and its deadbeat solutions
  - book: isbn:9780486486130
    title: Karl J. Åström and Björn Wittenmark, Computer-Controlled Systems, Theory and Design, third edition, Prentice Hall, 1997 (Dover reprint, 2011)
    locator: Chapter 4, on pole placement by state feedback in discrete time and on the deadbeat case
  - paper: doi:10.1524/auto.1972.20.112.297
    title: Jürgen Ackermann, Der Entwurf linearer Regelungssysteme im Zustandsraum, Regelungstechnik 20(7), 297-300, 1972
    locator: the single-input gain formula, which gives the deadbeat gain for p(z) = z^n
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 8.2, State Feedback, and Section 8.6, State Feedback, Multivariable Case
---

Deadbeat control is a state feedback $u_k = -K x_k$ for a discrete-time system $x_{k+1} = A x_k + B u_k$ that makes $A - BK$ nilpotent: $(A - BK)^N = 0$ for some $N \le n$. All closed-loop eigenvalues are then at $z = 0$, and every initial state reaches the origin exactly after $N$ steps and stays there. The algorithm on this page finds a gain with the least possible $N$, for any number of inputs. With one input, it is [Ackermann's formula](/ackermann-formula/) with the polynomial $z^n$. Deadbeat control has no continuous-time counterpart: no finite gain brings a continuous linear system to rest in finite time. The price is large inputs, especially for short sampling periods.

## In plain words

A computer controls a machine at fixed clock ticks. A deadbeat controller is a rule that brings the machine exactly to rest after a fixed number of ticks, from any starting point. It is not a slow approach that gets closer and closer: after the last tick, the error is zero. The method builds the rule backwards. First it finds the states that can be stopped in one tick, then those that can be moved into that set in one tick, and so on, until every state is covered. Then it picks, for each kind of state, the push that moves it one set closer to rest. The pushes can be very large, and the motion between ticks is not controlled.

## The problem

Input: $A \in \mathbb{R}^{n \times n}$ and $B \in \mathbb{R}^{n \times m}$ for the system $x_{k+1} = A x_k + B u_k$. Output: $K \in \mathbb{R}^{m \times n}$ and the least $N$ with $(A - BK)^N = 0$.

A deadbeat gain exists if and only if every uncontrollable eigenvalue of $A$ is $0$; this holds in particular when $(A, B)$ is [controllable](/controllability/). By the [pole placement theorem](/pole-placement-theorem/), the eigenvalues of the uncontrollable part do not move under feedback, so they must already be 0. With one input and $(A, b)$ controllable, $N = n$ and $K$ is unique. With several inputs, $K$ is not unique and $N$ can be smaller than $n$.

The least $N$ is the same for feedback and for open-loop input sequences: it is the least $j$ such that every state can be brought to 0 in $j$ steps by some inputs, that is, the least $j$ with $\operatorname{range} A^j \subseteq \operatorname{range} [B, AB, \dots, A^{j-1} B]$. If $A$ is invertible, this is the controllability index, the least $j$ with $\operatorname{rank} [B, AB, \dots, A^{j-1} B] = n$.

## The algorithm

```pseudo id=main
DEADBEAT(A, B)
L1  V ← [] (basis of S_0 = {0}); C ← []; N ← 0; while |V| < n: N ← N + 1
L2      S_N ← {x : A x = V a + B c for some a, c}      ▷ null space of [A, -V, -B]
L3      for each vector x of S_N that is independent of V: append x to V, its c to C
L4      if no vector was appended: fail                ▷ an uncontrollable eigenvalue is not 0
L5  return K = C V^(-1), N                            ▷ K v_i = c_i for every basis vector
```

The subspace $S_j$ is the set of states that some input sequence brings to 0 in $j$ steps: $x \in S_j$ exactly when one input $u = -c$ moves $x$ to $Ax - Bc \in S_{j-1}$. Line L2 computes $S_j$ as the projection of a null space, and the null vector also gives the input $c$. Line L3 extends the basis, so the basis vectors are ordered by the first $S_j$ that contains them. Line L5 defines $K$ by its values on this basis: for a basis vector $v$ of $S_j$, $(A - BK) v = Av - Bc$ lies in $S_{j-1}$. So $A - BK$ maps $S_j$ into $S_{j-1}$, and $N$ steps map $S_N = \mathbb{R}^n$ to $S_0 = \{0\}$.

## Example

**Double integrator, sampled.** The [zero-order hold](/zero-order-hold-discretization/) model of a unit mass with period $h$ is $A = \begin{bmatrix} 1 & h \\ 0 & 1 \end{bmatrix}$, $B = \begin{bmatrix} h^2/2 \\ h \end{bmatrix}$. The algorithm gives $N = 2$ and

$$K = \begin{bmatrix} 1/h^2 & 3/(2h) \end{bmatrix}, \qquad A - BK = \begin{bmatrix} 1/2 & h/4 \\ -1/h & -1/2 \end{bmatrix}, \qquad (A - BK)^2 = 0.$$

From $x_0 = (1, 0)$, the inputs are $u_0 = -1/h^2$ and $u_1 = 1/h^2$, and $x_1 = (1/2, -1/h)$, $x_2 = 0$. With $h = 0.1$ the inputs are $\mp 100$ and the peak velocity is 10, for a move of length 1. Halving $h$ makes the inputs four times larger. This is the price of deadbeat control.

**Two inputs, fewer steps.** For

$$A = \begin{bmatrix} 1 & 1 & 0 \\ 0 & 1 & 1 \\ 0 & 0 & 1 \end{bmatrix}, \qquad B = \begin{bmatrix} 0 & 0 \\ 1 & 0 \\ 0 & 1 \end{bmatrix},$$

$\operatorname{rank}[B, AB] = 3$, so the controllability index is 2. The algorithm returns $N = 2$ and $K = \begin{bmatrix} 1 & 2 & 1 \\ 0 & 0 & 1 \end{bmatrix}$, with $A - BK = \begin{bmatrix} 1 & 1 & 0 \\ -1 & -1 & 0 \\ 0 & 0 & 0 \end{bmatrix}$, whose square is 0. Any single input of this system needs three steps.

**Singular $A$.** For $A = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix}$ and $B = e_2$, the third state is not controllable, but its eigenvalue is 0, and $A$ maps it to 0 in one step. The algorithm returns $K = 0$ and $N = 2$: the open loop is already deadbeat.

## Correctness

The full proof is in proofs/correctness.md. Its steps:

- **The subspaces grow.** $S_0 \subseteq S_1 \subseteq \cdots$, by induction on $j$. If $S_j = S_{j-1}$ for some $j$, then $S_i = S_j$ for all $i \ge j$, so the loop ends after at most $n$ rounds, by success or by line L4.
- **Meaning of $S_j$.** $S_j$ is exactly the set of states that some input sequence brings to 0 in $j$ steps.
- **Nilpotency.** For the gain of line L5, $(A - BK) S_j \subseteq S_{j-1}$, so $(A - BK)^N = 0$.
- **Minimality.** If $(A - BK')^{N'} = 0$ for some gain $K'$, then the feedback inputs bring every state to 0 in $N'$ steps, so $S_{N'} = \mathbb{R}^n$ and $N' \ge N$.
- **Failure.** If the loop stops with $S_j = S_{j-1} \ne \mathbb{R}^n$, no input sequence brings every state to 0, so no gain is deadbeat. This happens exactly when an uncontrollable eigenvalue is not 0.

## Complexity

In the [real RAM](/real-ram/), with exact arithmetic: each round of the loop computes the null space of a matrix with $n$ rows and at most $2n + m$ columns, by elimination in $O(n^2 (n + m))$ operations, and tests at most $2n + m$ vectors for independence. With the independence tests done incrementally against an echelon form of $V$, each costs $O(n^2)$, so a round costs $O(n^2 (n + m))$, and there are $N \le n$ rounds. Line L5 is one solve with $m$ right sides, $O(n^3 + n^2 m)$. The total is $O(N n^2 (n + m))$ and the extra space is $O(n (n + m))$. The code on this page recomputes each rank from scratch, which is simpler and slower by a factor of $n$. With rational data the entries can grow; the implementation uses exact fractions, and the bit cost is polynomial but larger.

In floating point, the rank decisions in lines L2 to L4 need a tolerance, and a system close to an uncontrollable one gives a gain that is very large or wrong. For one input, the [Ackermann formula](/ackermann-formula/) with $p(z) = z^n$ has the same numerical weakness.

## Properties

- **Exact zero, not decay.** After $N$ steps the state is 0, not small. In the $z$-domain, all closed-loop poles are at $z = 0$, and the closed-loop response to any initial state is a polynomial in $z^{-1}$ of degree below $N$, a finite impulse response.
- **Minimum time.** No feedback and no open-loop input sequence reaches the origin from every state in fewer than $N$ steps.
- **Size of the inputs.** The gain grows as $h$ shrinks. In the double integrator, $\|K\|$ grows like $1/h^2$. With bounded inputs, the deadbeat law works only for small enough states; a time-optimal controller with bounds needs more steps.
- **Not unique with several inputs.** For $m > 1$ the algorithm returns one of many deadbeat gains. The choice of basis in line L3 decides which one. The Jordan structure of $A - BK$ can also differ between gains with the same $N$.
- **Observers.** Applied to $(A^T, C^T)$, the algorithm gives a deadbeat observer gain $L = K^T$: the estimation error of a [Luenberger observer](/luenberger-observer/) is then exactly 0 after $N$ steps.

## Variants and improvements

- **Single input.** Use [Ackermann's formula](/ackermann-formula/) with $p(z) = z^n$: $K = e_n^T W^{-1} A^n$.
- **Deadbeat tracking.** Add a feedforward term so that the output follows a step reference after a finite number of steps; with integral action as in [state feedback with integral action](/integral-state-feedback/), the augmented system is made deadbeat.
- **Bounded inputs.** If the inputs must stay within bounds, the minimum time problem becomes a linear program for each initial state, or a model predictive control problem. The deadbeat gain is its unbounded limit.
- **Ripple-free deadbeat.** A deadbeat design on the sampled model can leave oscillations between samples, for example when it cancels a sampling zero near $-1$. Ripple-free designs constrain the controller so that the continuous output also settles; see [sampled-data system](/sampled-data-system/).
- **Robust alternatives.** Placing all poles at a small positive radius $r$ instead of 0 gives a smooth decay like $r^k$, much smaller inputs, and less sensitivity. The design is then ordinary [pole placement](/pole-placement-problem/).

## When to use it

Use deadbeat control when the samples must settle in the least number of steps and the inputs can be large: for slow sampling relative to the plant, in digital servo loops with a strong actuator, or as the observer in a system where the state must be known exactly after $n$ samples. It is also a clean test case for discrete-time designs, because the result can be checked exactly. Avoid it when the sampling is fast relative to the plant dynamics, when the actuator saturates, or when the model is uncertain: the gain is large and the poles at 0 are very sensitive.

## Pitfalls

- **Large gains for short periods.** The inputs grow like $1/h^2$ for the double integrator, and faster for higher order systems. Check the input sequence for the largest expected initial state.
- **Sensitive poles.** A nilpotent matrix with one Jordan block of size $n$ has eigenvalues that move like $\varepsilon^{1/n}$ under a change $\varepsilon$ of its entries. A small model error therefore moves the poles far from 0, and the finite settling is lost.
- **Intersample ripple.** The design controls only the samples. Simulate the continuous plant with the held input, as the [zero-order hold](/zero-order-hold-discretization/) page shows.
- **Not continuous-time.** For $\dot x = Ax + Bu$ with $u = -Kx$, the state is $e^{(A - BK)t} x_0$, which is never 0 for $x_0 \ne 0$. Finite time settling in continuous time needs nonlinear or time-varying control.
- **Uncontrollable modes.** The algorithm fails when an uncontrollable eigenvalue is not 0. A stable uncontrollable mode still decays, but not in finite time; then use ordinary pole placement for the controllable part.

## Implementations

## History

Designs with a finite settling time for sampled systems appeared in the early transfer-function theory of sampled-data control, under the name deadbeat response. The state-space form, with the minimum number of steps given by the controllability structure of $(A, B)$, came with the state-space theory of the 1960s. O'Reilly (1981) surveyed the discrete time-optimal control problem and its deadbeat solutions. For one input, [Ackermann's formula](/ackermann-formula/) of 1972 gives the deadbeat gain directly.

## References
