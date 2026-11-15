---
tag: 2AXRCG
kind: definition
slug: controlled-invariant-subspace
name: Controlled invariant subspace
aliases:
- "(A,B)-invariant subspace"
area: control/state-space-control
level: advanced
summary: A subspace V with A V contained in V + im B. Then some state feedback u = -K x makes V invariant. It is the central object of the geometric approach of Wonham and Basile-Marro.
prereqs: [state-space-representation, controllability]
see_also: [invariant-subspace-algorithm, disturbance-decoupling-problem, control-invariant-set, zero-dynamics, unknown-input-observer, kalman-decomposition, transmission-zero, state-feedback]
sources:
  - paper: doi:10.1007/BF00931370
    title: G. Basile and G. Marro, Controlled and conditioned invariant subspaces in linear system theory, Journal of Optimization Theory and Applications 3(5), 306-315, 1969
    locator: the definitions of controlled invariant and conditioned invariant subspaces and their duality
  - paper: doi:10.1137/0308001
    title: W. M. Wonham and A. S. Morse, Decoupling and pole assignment in linear multivariable systems, a geometric approach, SIAM Journal on Control 8(1), 1-18, 1970
    locator: the (A, B)-invariant subspaces, the feedback that makes them invariant, and the largest one in a given subspace
  - book: isbn:9780387960715
    title: W. Murray Wonham, Linear Multivariable Control, A Geometric Approach, third edition, Springer, 1985
    locator: Chapter 4, Disturbance Decoupling and Output Stabilization (the (A, B)-invariant subspaces and the supremal one in a subspace)
  - book: isbn:9781852333164
    title: Harry L. Trentelman, Anton A. Stoorvogel and Malo Hautus, Control Theory for Linear Systems, Springer, 2001
    locator: Chapter 4, Controlled invariant subspaces
---

A controlled invariant subspace of the linear system $\dot x = A x + B u$ is a subspace $\mathcal{V}$ of the state space with $A \mathcal{V} \subseteq \mathcal{V} + \operatorname{im} B$. The name says what the condition means: for every start in $\mathcal{V}$ some input keeps the state in $\mathcal{V}$, and one linear [state feedback](/state-feedback/) $u = -K x$ does this for all starts at once. Basile and Marro (1969) introduced the idea, and Wonham and Morse (1970) called it an $(A, B)$-invariant subspace. It is the basic object of geometric control: the [disturbance decoupling problem](/disturbance-decoupling-problem/), the [zero dynamics](/zero-dynamics/) of a linear system and the decoupling of outputs are all stated with it, and the [invariant subspace algorithm](/invariant-subspace-algorithm/) computes the largest one inside a given subspace. Do not confuse it with a [control invariant set](/control-invariant-set/), which is a set of states, often a polytope, kept by inputs that must obey constraints. A controlled invariant subspace is linear and has no input bound.

## Definition

Let $A \in \mathbb{R}^{n \times n}$ and $B \in \mathbb{R}^{n \times m}$, and write $\mathcal{B} = \operatorname{im} B$. A subspace $\mathcal{V} \subseteq \mathbb{R}^n$ is **controlled invariant**, or **$(A, B)$-invariant**, if

$$A \mathcal{V} \subseteq \mathcal{V} + \mathcal{B}.$$

A matrix $K \in \mathbb{R}^{m \times n}$ with $(A - BK) \mathcal{V} \subseteq \mathcal{V}$ is called a **friend** of $\mathcal{V}$. Wonham writes the feedback as $u = F x$ and the condition as $(A + BF)\mathcal{V} \subseteq \mathcal{V}$; this page uses $u = -K x$, so $F = -K$.

**Theorem (three equivalent conditions).** For a subspace $\mathcal{V}$ the following are equivalent:

1. $A \mathcal{V} \subseteq \mathcal{V} + \mathcal{B}$.
2. There is a $K$ with $(A - BK)\mathcal{V} \subseteq \mathcal{V}$.
3. For every $x_0 \in \mathcal{V}$ there is a continuous input $u$ such that the solution of $\dot x = A x + B u$, $x(0) = x_0$, stays in $\mathcal{V}$ for all $t \ge 0$.

*Proof.* (1) to (2): take a basis $v_1, \dots, v_q$ of $\mathcal{V}$. By (1), $A v_i = w_i - B u_i$ with $w_i \in \mathcal{V}$ and $u_i \in \mathbb{R}^m$. Complete the basis to a basis $v_1, \dots, v_n$ of $\mathbb{R}^n$, and let $K$ be the matrix with $K v_i = -u_i$ for $i \le q$ and $K v_i = 0$ for $i > q$. Then $(A - BK) v_i = A v_i + B u_i = w_i \in \mathcal{V}$, so $(A - BK)\mathcal{V} \subseteq \mathcal{V}$. (2) to (3): use $u = -K x$. The solution is $x(t) = e^{(A - BK)t} x_0$, and every power of $A - BK$ maps $\mathcal{V}$ into itself, so the series of the exponential stays in $\mathcal{V}$. (3) to (1): let $x_0 \in \mathcal{V}$ and let $x$ stay in $\mathcal{V}$. Then $\dot x(0^+) = \lim_{t \to 0^+} (x(t) - x_0)/t \in \mathcal{V}$, because $\mathcal{V}$ is closed. Also $\dot x(0^+) = A x_0 + B u(0)$. So $A x_0 \in \mathcal{V} + \mathcal{B}$. $\blacksquare$

**Closure under sums.** If $\mathcal{V}_1$ and $\mathcal{V}_2$ are controlled invariant, so is $\mathcal{V}_1 + \mathcal{V}_2$, because $A(\mathcal{V}_1 + \mathcal{V}_2) = A\mathcal{V}_1 + A\mathcal{V}_2 \subseteq \mathcal{V}_1 + \mathcal{V}_2 + \mathcal{B}$. The zero subspace is controlled invariant. So for every subspace $\mathcal{K}$ the family of controlled invariant subspaces contained in $\mathcal{K}$ has a largest element, the sum of all of them. It is written $\mathcal{V}^\ast(\mathcal{K})$, or $\mathcal{V}^\ast$ when $\mathcal{K} = \ker C$ for an output $y = C x$. The [invariant subspace algorithm](/invariant-subspace-algorithm/) computes it in at most $\dim \mathcal{K} + 1$ steps.

The friend is not unique. If $K$ is a friend, so is $K + L$ for every $L$ with $\mathcal{V} \subseteq \ker(BL)$. If $(A, B)$ is controllable, the friend can place the eigenvalues of $A - BK$ restricted to $\mathcal{V}$ only in part; the eigenvalues that every friend shares are the fixed poles of $\mathcal{V}$. For $\mathcal{V}^\ast = \mathcal{V}^\ast(\ker C)$ of a system with as many inputs as outputs and an invertible transfer function, these fixed poles are the invariant zeros of $(A, B, C)$ (see [transmission zero](/transmission-zero/)).

## Examples and non-examples

- **Trivial cases.** The subspaces $\{0\}$, $\mathbb{R}^n$ and $\mathcal{B} = \operatorname{im} B$ are controlled invariant for every $A$. Every $A$-invariant subspace is controlled invariant, with the friend $K = 0$.
- **A chain of integrators.** Take $\dot x_1 = x_2$, $\dot x_2 = x_3$, $\dot x_3 = u$, so $A$ has ones above the diagonal and $B = e_3$. The subspace $\mathcal{V}_1 = \operatorname{span}(e_1, e_2)$ is controlled invariant: $A e_1 = 0$ and $A e_2 = e_1$, so even $A \mathcal{V}_1 \subseteq \mathcal{V}_1$. The subspace $\mathcal{V}_2 = \operatorname{span}(e_2, e_1 + e_3)$ is controlled invariant too: $A e_2 = e_1 = (e_1 + e_3) - e_3$ and $A(e_1 + e_3) = e_2$, and $e_3 \in \mathcal{B}$.
- **Non-example: the intersection.** In the same system, $\mathcal{V}_1 \cap \mathcal{V}_2 = \operatorname{span}(e_2)$. But $A e_2 = e_1$, and $e_1 \notin \operatorname{span}(e_2, e_3)$. So the intersection of two controlled invariant subspaces need not be controlled invariant, and there is no smallest controlled invariant subspace containing a given subspace in general. The tests of the [invariant subspace algorithm](/invariant-subspace-algorithm/) check this example.
- **The disturbance decoupling example.** For $A = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & -1 \end{bmatrix}$, $B = e_2$ and $C = \begin{bmatrix} 1 & 0 & 0 \end{bmatrix}$, the largest controlled invariant subspace in $\ker C$ is $\operatorname{span}(e_3)$. Here $A e_3 = e_2 - e_3$, and the friend $K = \begin{bmatrix} k_1 & k_2 & 1 \end{bmatrix}$ removes the $e_2$ part for any $k_1, k_2$. The subspace $\ker C = \operatorname{span}(e_2, e_3)$ itself is not controlled invariant, because $A e_2 = e_1 \notin \ker C + \mathcal{B}$.
- **Non-example: a set that is not a subspace.** The box $\{x : |x_i| \le 1\}$ can be a [control invariant set](/control-invariant-set/) for a constrained input. It is not a subspace, and the theory of this page does not apply to it.

## Related definitions

- **Conditioned invariant subspace** (Basile and Marro 1969), also called $(C, A)$-invariant: a subspace $\mathcal{S}$ with $A(\mathcal{S} \cap \ker C) \subseteq \mathcal{S}$. It is the dual notion: $\mathcal{S}$ is conditioned invariant for $(C, A)$ exactly when $\mathcal{S}^\perp$ is controlled invariant for $(A^T, C^T)$. Some $L$ then gives $(A - LC)\mathcal{S} \subseteq \mathcal{S}$, which is the property used by an [unknown input observer](/unknown-input-observer/).
- **Controllability subspace**: a controlled invariant subspace $\mathcal{R}$ such that, with a friend $K$ and some $G$, $\mathcal{R}$ is the reachable subspace of $(A - BK, BG)$. Every state in $\mathcal{R}$ can be reached from 0 along a path inside $\mathcal{R}$. The reachable subspace of $(A, B)$ is the largest one (see [controllability](/controllability/) and the [Kalman decomposition](/kalman-decomposition/)).
- **Stabilizability subspace**: a controlled invariant subspace with a friend that makes $A - BK$ restricted to it Hurwitz. It is used for disturbance decoupling with internal stability.
- **$\mathcal{V}^\ast$ and the zero dynamics**: the motions that keep $y = C x$ identically zero are the motions inside $\mathcal{V}^\ast(\ker C)$. The [zero dynamics](/zero-dynamics/) of a linear system is the restriction of $A - BK$ to $\mathcal{V}^\ast$ for a friend $K$, up to the free part of the friend.
- **Invariant subspace**: the case $B = 0$, where the condition is $A \mathcal{V} \subseteq \mathcal{V}$; see [eigenvalue](/eigenvalue/) for the eigenvectors that span such subspaces.

## References
