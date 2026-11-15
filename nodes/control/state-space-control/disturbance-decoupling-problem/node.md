---
tag: QGJH1J
kind: problem
slug: disturbance-decoupling-problem
name: Disturbance decoupling problem
aliases:
- disturbance decoupling by state feedback
area: control/state-space-control
level: advanced
summary: Find a state feedback that removes every effect of a disturbance on the output. It is solvable exactly when the disturbance enters inside the largest controlled invariant subspace in ker C.
prereqs: [invariant-subspace-algorithm, controlled-invariant-subspace]
see_also: [output-regulation-problem, disturbance-observer, unknown-input-observer, feedforward-control, zero-dynamics, transmission-zero, state-feedback, internal-model-principle]
sources:
  - paper: doi:10.1137/0308001
    title: W. M. Wonham and A. S. Morse, Decoupling and pole assignment in linear multivariable systems, a geometric approach, SIAM Journal on Control 8(1), 1-18, 1970
    locator: the disturbance decoupling problem by state feedback and its solution with the supremal (A, B)-invariant subspace in ker C
  - paper: doi:10.1007/BF00931370
    title: G. Basile and G. Marro, Controlled and conditioned invariant subspaces in linear system theory, Journal of Optimization Theory and Applications 3(5), 306-315, 1969
    locator: the controlled invariant subspaces used for the decoupling of disturbances
  - book: isbn:9780387960715
    title: W. Murray Wonham, Linear Multivariable Control, A Geometric Approach, third edition, Springer, 1985
    locator: Chapter 4, Disturbance Decoupling and Output Stabilization
  - book: isbn:9781852333164
    title: Harry L. Trentelman, Anton A. Stoorvogel and Malo Hautus, Control Theory for Linear Systems, Springer, 2001
    locator: Chapter 4, Controlled invariant subspaces (disturbance decoupling, with and without internal stability)
---

The disturbance decoupling problem (DDP) asks for a [state feedback](/state-feedback/) $u = -Kx$ for the system $\dot x = A x + B u + E d$, $y = C x$ such that the disturbance $d$ has no effect at all on the output $y$, for every disturbance signal and with zero initial state. Wonham and Morse (1970) solved it with geometric methods: a solution exists if and only if $\operatorname{im} E \subseteq \mathcal{V}^\ast$, where $\mathcal{V}^\ast$ is the largest [controlled invariant subspace](/controlled-invariant-subspace/) inside $\ker C$. The [invariant subspace algorithm](/invariant-subspace-algorithm/) computes $\mathcal{V}^\ast$ in at most $n + 1$ exact passes, so the problem is decidable in polynomial arithmetic time, and the proof gives a feedback when one exists. The problem asks for exact decoupling at all frequencies. Approximate rejection, with a small but nonzero gain from $d$ to $y$, is an $H_\infty$ problem; rejection of disturbances from a known model, such as constants or sinusoids, is the [output regulation problem](/output-regulation-problem/).

## In plain words

A machine is pushed by an unknown force, such as wind on a crane or a load change on a motor. You measure the full internal state and you choose the control law. You want one quantity, the output, never to feel the force at all. The idea is to let the force move the machine only in directions that the output cannot see, and to use the control to stop it from leaving those directions. The test is whether the force acts only on directions from which the control can keep the output blind. If it does, a fixed linear control law exists and the output is exactly unaffected. If it does not, no such control law exists, however large the gains.

## Definition

**Data.** Matrices $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $E \in \mathbb{R}^{n \times q}$ and $C \in \mathbb{R}^{p \times n}$ of the system

$$\dot x = A x + B u + E d, \qquad y = C x.$$

**Problem (DDP).** Find $K \in \mathbb{R}^{m \times n}$ such that, with $u = -Kx$, the transfer function from $d$ to $y$ is zero:

$$C \left(sI - (A - BK)\right)^{-1} E = 0 \quad \text{for all } s.$$

Equivalent forms: the Markov parameters $C (A - BK)^k E$ vanish for $k = 0, \dots, n - 1$; or the reachable subspace $\langle A - BK \mid \operatorname{im} E \rangle = \operatorname{im} E + (A - BK)\operatorname{im} E + \dots + (A - BK)^{n-1} \operatorname{im} E$ lies in $\ker C$.

**Theorem (Wonham and Morse 1970).** DDP is solvable if and only if $\operatorname{im} E \subseteq \mathcal{V}^\ast$, where $\mathcal{V}^\ast$ is the largest $(A, B)$-invariant subspace in $\ker C$. Every friend $K$ of $\mathcal{V}^\ast$, that is every $K$ with $(A - BK)\mathcal{V}^\ast \subseteq \mathcal{V}^\ast$, solves it.

*Proof.* If $\operatorname{im} E \subseteq \mathcal{V}^\ast$ and $K$ is a friend, then $\mathcal{V}^\ast$ is $(A - BK)$-invariant and contains $\operatorname{im} E$, so it contains $\langle A - BK \mid \operatorname{im} E \rangle$. It lies in $\ker C$, so every Markov parameter $C(A - BK)^k E$ is zero. Conversely, let $K$ solve DDP and set $\mathcal{R} = \langle A - BK \mid \operatorname{im} E \rangle$. It is $(A - BK)$-invariant, so $A \mathcal{R} \subseteq \mathcal{R} + \operatorname{im} B$, and $\mathcal{R} \subseteq \ker C$. So $\mathcal{R}$ is a controlled invariant subspace in $\ker C$, hence $\mathcal{R} \subseteq \mathcal{V}^\ast$, and $\operatorname{im} E \subseteq \mathcal{R} \subseteq \mathcal{V}^\ast$. $\blacksquare$

## Variants

- **DDP with stability (DDPS).** Also require $A - BK$ to be [Hurwitz](/hurwitz-matrix/). The condition is that $(A, B)$ is [stabilizable](/stabilizability/) and $\operatorname{im} E$ lies in the largest stabilizability subspace in $\ker C$, the largest controlled invariant subspace in $\ker C$ that has a friend making $A - BK$ restricted to it Hurwitz (Trentelman, Stoorvogel and Hautus treat this version in their chapter on controlled invariant subspaces). A friend of $\mathcal{V}^\ast$ that solves DDP can leave unstable fixed poles; these are invariant zeros of $(A, B, C)$ in the closed right half plane.
- **Measured disturbance (DDPM).** If $d$ is measured, allow $u = -Kx - G d$. The condition becomes $\operatorname{im} E \subseteq \mathcal{V}^\ast + \operatorname{im} B$. *Proof.* If it holds, write $E = E_1 + B G$ with $\operatorname{im} E_1 \subseteq \mathcal{V}^\ast$, which is possible column by column. With $u = -Kx - Gd$ the disturbance enters through $E - BG = E_1$, and a friend of $\mathcal{V}^\ast$ decouples it. If a pair $(K, G)$ works, the reachable subspace of $(A - BK, E - BG)$ is controlled invariant and lies in $\ker C$, so $\operatorname{im}(E - BG) \subseteq \mathcal{V}^\ast$ and $\operatorname{im} E \subseteq \mathcal{V}^\ast + \operatorname{im} B$. $\blacksquare$
- **Output feedback.** With only $y_m = C_m x$ measured, use a dynamic controller. The condition then involves both $\mathcal{V}^\ast$ and the smallest conditioned invariant subspace $\mathcal{S}^\ast$ containing $\operatorname{im} E$: without a stability requirement, a solution exists if and only if $\mathcal{S}^\ast \subseteq \mathcal{V}^\ast$, where $\mathcal{S}^\ast$ is computed for the measured output $C_m$. The version with stability needs further conditions.
- **Almost decoupling.** Ask for $\|C(sI - A + BK)^{-1}E\|_\infty < \gamma$ for every $\gamma > 0$, with the [H-infinity norm](/h-infinity-norm/). The conditions use the almost controlled invariant subspaces and allow high-gain feedback.
- **Discrete time.** The same theorem holds for $x_{k+1} = A x_k + B u_k + E d_k$ with the same $\mathcal{V}^\ast$, because the proof uses only the Markov parameters.

## Examples

- **The example of the ISA page.** $A = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & -1 \end{bmatrix}$, $B = e_2$, $C = \begin{bmatrix} 1 & 0 & 0 \end{bmatrix}$, $E = e_3$. The [invariant subspace algorithm](/invariant-subspace-algorithm/) gives $\mathcal{V}^\ast = \operatorname{span}(e_3)$, so $\operatorname{im} E \subseteq \mathcal{V}^\ast$ and DDP is solvable. The friends are $K = \begin{bmatrix} k_1 & k_2 & 1 \end{bmatrix}$ for all $k_1, k_2$: the entry 1 cancels the path from $x_3$ to $x_2$. The closed-loop characteristic polynomial is $(s^2 + k_2 s + k_1)(s + 1)$, so $K = \begin{bmatrix} 1 & 2 & 1 \end{bmatrix}$ puts all poles at $-1$ and also solves DDPS. The gain $K = \begin{bmatrix} 1 & 2 & 0 \end{bmatrix}$ has the same first two entries but does not decouple; the tests check both.
- **A disturbance in the input channel.** Same system with $E = e_2$. Now $\operatorname{im} E = \operatorname{im} B \not\subseteq \mathcal{V}^\ast$, so DDP has no solution: the disturbance reaches $x_1$ through $\dot x_1 = x_2$ before any feedback can act. The tests confirm this with a brute force search over all integer gains in $\{-2, \dots, 2\}^3$. If $d$ is measured, $\operatorname{im} E \subseteq \mathcal{V}^\ast + \operatorname{im} B$ holds and $u = -Kx - d$ cancels it exactly, as in [feedforward control](/feedforward-control/).
- **A disturbance at the output.** If $C E \ne 0$, the disturbance changes $\dot y$ at once, and no state feedback can help: $\operatorname{im} E \not\subseteq \ker C \supseteq \mathcal{V}^\ast$.
- **Relative degree.** For one input, one disturbance and one output, DDP is solvable exactly when the disturbance reaches the output through more integrators than the input does: if $\rho$ is the relative degree from $u$ to $y$, the condition is $C A^k E = 0$ for $k < \rho$. This is a theorem that follows from $\mathcal{V}^\ast = \ker \begin{bmatrix} C^T & (CA)^T & \cdots & (CA^{\rho-1})^T \end{bmatrix}^T$.

## Known algorithms

- **Invariant subspace algorithm.** Compute $\mathcal{V}^\ast$ with the [ISA](/invariant-subspace-algorithm/), test $\operatorname{im} E \subseteq \mathcal{V}^\ast$ by one rank computation, and build a friend from a basis of $\mathcal{V}^\ast$. The cost is $O(n^3 (n + m))$ arithmetic operations, and with exact rational arithmetic the answer is exact. The implementation of the ISA page does all three steps and checks the result by the Markov parameters.
- **Stabilizing friend.** For DDPS, split $\mathcal{V}^\ast$ by the fixed poles, and place the free eigenvalues of $A - BK$ on $\mathcal{V}^\ast$ and on a complement with [pole placement](/pole-placement-theorem/) in each part.
- **Pencil methods.** In floating point, $\mathcal{V}^\ast$ and the fixed poles come from staircase reductions of the system pencil with orthogonal transformations, with a rank tolerance at each step.

The input has $\Theta(n (n + m + p + q))$ numbers, and the ISA uses $O(n^3 (n + m))$ operations. No lower bound above the input size is known, and no faster exact method is needed for the problem sizes of control.

## Bounds

The problem is a yes or no question with a certificate. The criterion $\operatorname{im} E \subseteq \mathcal{V}^\ast$ is exact, and it is decided after at most $\dim \ker C + 1$ passes of the ISA. In floating point the decision is ill posed: arbitrarily small changes of $(A, B, C, E)$ can change the answer, because $\mathcal{V}^\ast$ is not a continuous function of the data (see the pitfalls of the [invariant subspace algorithm](/invariant-subspace-algorithm/)). One case is simple. If $CB$ has full row rank $p$, then $\ker C + \operatorname{im} B = \mathbb{R}^n$, the first pass of the ISA returns $\ker C$, so $\mathcal{V}^\ast = \ker C$, and DDP is solvable exactly when $CE = 0$. This is a theorem, and it covers a generic system with $m \ge p$.

## Reductions

- **To a subspace computation.** DDP reduces to computing $\mathcal{V}^\ast(\ker C)$ and one inclusion test, by the theorem above.
- **Compared with output regulation.** The [output regulation problem](/output-regulation-problem/) asks that the output error tend to zero for the disturbances of one known exosystem. DDP with stability asks that the output not react at all, for every disturbance signal. So a solution of DDPS solves the regulation problem for every exosystem that enters through $E$ alone, but the converse fails: regulation of constant disturbances needs only an integrator, while DDP may have no solution.
- **Duality with unknown input observers.** An observer whose error is not affected by an unknown input $d$ exists under the dual condition with conditioned invariant subspaces. This is the problem of the [unknown input observer](/unknown-input-observer/).
- **To decoupling of outputs.** Wonham and Morse (1970) treated DDP together with the decoupling problem of Morgan, which asks that each output be controlled by its own input only, with the same subspaces.

## Applications

- **Structural design.** The test tells the designer early whether an actuator placement can reject a disturbance exactly, or whether one more actuator or a disturbance sensor is needed, before any tuning.
- **Feedforward from measured disturbances.** In process control, measured load changes are cancelled with $u = -Kx - Gd$; the DDPM condition says when exact cancellation is possible.
- **Fault isolation.** The dual problem gives residual generators that do not react to some faults or disturbances, which is the basis of fault detection filters.
- **Zero dynamics.** The subspace $\mathcal{V}^\ast$ and its friend are the linear case of the input-output normal form used in [input-output linearization](/input-output-linearization/), where the disturbance decoupling condition is the same relative degree condition.

## References
