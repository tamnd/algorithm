---
tag: BJYH7J
kind: theorem
slug: regulator-equations
name: Francis regulator equations
aliases:
- regulator equations
area: control/state-space-control
level: advanced
summary: "The linear output regulation problem is solvable if and only if Pi S = A Pi + B Gamma + P and C Pi + Q = 0 have a solution, given a stabilizable plant and an exosystem with no decaying modes."
prereqs: [output-regulation-problem, sylvester-equation]
see_also: [internal-model-principle, integral-state-feedback, transmission-zero, sylvester-equation, schur-decomposition, disturbance-decoupling-problem, feedforward-control, zero-dynamics]
sources:
  - paper: doi:10.1137/0315033
    title: B. A. Francis, The linear multivariable regulator problem, SIAM Journal on Control and Optimization 15(3), 486-505, 1977
    locator: the solvability of the regulator problem with full information and with error feedback in terms of the pair of linear matrix equations
  - paper: doi:10.1007/BF01447855
    title: B. A. Francis and W. M. Wonham, The internal model principle for linear multivariable regulators, Applied Mathematics and Optimization 2(2), 170-194, 1975
    locator: the internal model that a regulator robust to plant perturbations must contain
  - paper: doi:10.1109/TAC.1976.1101137
    title: E. J. Davison, The robust control of a servomechanism problem for linear time-invariant multivariable systems, IEEE Transactions on Automatic Control 21(1), 25-34, 1976
    locator: the existence conditions of the robust servomechanism problem, including the rank condition at the exosystem eigenvalues
  - paper: doi:10.1109/9.45168
    title: A. Isidori and C. I. Byrnes, Output regulation of nonlinear systems, IEEE Transactions on Automatic Control 35(2), 131-140, 1990
    locator: the nonlinear regulator equations, a pair of partial differential equations that reduce to the linear ones
  - book: isbn:9781852333164
    title: Harry L. Trentelman, Anton A. Stoorvogel and Malo Hautus, Control Theory for Linear Systems, Springer, 2001
    locator: Chapter 9, Tracking and regulation
---

The regulator equations are the pair of linear matrix equations $\Pi S = A \Pi + B \Gamma + P$ and $C \Pi + Q = 0$ in the unknowns $\Pi$ and $\Gamma$. Francis (1977) proved that they decide the linear [output regulation problem](/output-regulation-problem/): for a stabilizable plant $\dot x = A x + B u + P w$ with error $e = C x + Q w$, driven by an exosystem $\dot w = S w$ with no decaying modes, a stabilizing controller that drives $e$ to zero exists exactly when the equations have a solution. The solution has a direct meaning. $\Pi w$ is the steady-state motion of the plant that keeps the error at zero, and $\Gamma w$ is the input that produces it. The equations are linear, a [Sylvester equation](/sylvester-equation/) with a constraint, and they have a solution for every $P$ and $Q$ exactly when no invariant zero of the plant is an eigenvalue of $S$. Isidori and Byrnes (1990) extended them to nonlinear systems, where they become partial differential equations.

## Statement

Let $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $P \in \mathbb{R}^{n \times q}$, $C \in \mathbb{R}^{p \times n}$, $Q \in \mathbb{R}^{p \times q}$ and $S \in \mathbb{R}^{q \times q}$, for the system

$$\dot x = A x + B u + P w, \qquad \dot w = S w, \qquad e = C x + Q w.$$

Assume (H1) every eigenvalue of $S$ has real part $\ge 0$, and (H2) $(A, B)$ is [stabilizable](/stabilizability/). The **regulator equations** are

$$\Pi S = A \Pi + B \Gamma + P, \qquad 0 = C \Pi + Q, \qquad \Pi \in \mathbb{R}^{n \times q}, \ \Gamma \in \mathbb{R}^{m \times q}. \tag{RE}$$

**Theorem (Francis 1977).**

1. *Full information.* There are $K$ and $L$ such that $A - BK$ is Hurwitz and $u = -Kx + Lw$ gives $e(t) \to 0$ for all initial states if and only if (RE) has a solution. Then any $K$ with $A - BK$ Hurwitz and $L = \Gamma + K\Pi$ work.
2. *Error feedback.* If also (H3) the pair $\left(\begin{bmatrix} C & Q \end{bmatrix}, \begin{bmatrix} A & P \\ 0 & S \end{bmatrix}\right)$ is [detectable](/detectability/), there is a dynamic controller driven by $e$ alone that makes the loop internally stable and gives $e(t) \to 0$ if and only if (RE) has a solution.
3. *Solvability for all data.* (RE) has a solution for every $P$ and $Q$ if and only if
$$\operatorname{rank} \begin{bmatrix} A - \lambda I & B \\ C & 0 \end{bmatrix} = n + p \quad \text{for every eigenvalue } \lambda \text{ of } S.$$
This needs $m \ge p$. If $m = p$, the solution is unique.

This page writes the feedback as $u = -Kx + Lw$, as the rest of this area does. The rank condition of part 3 is proved here with a Schur form of $S$; it is not quoted from Francis.

## In plain words

A machine must follow a signal of a known kind, made by a small model that runs on its own. Suppose the error is already zero and stays zero. Then the machine moves in a steady pattern that copies the signal, and the input follows a steady pattern too. Both patterns are linear functions of the state of the signal model. The two equations say exactly this: the first says that the steady pattern of the machine is a possible motion under the steady input, and the second says that the error is zero on it. The theorem says that a good controller exists if and only if such patterns exist. A controller then only has to push the machine onto the pattern and keep it there.

## Proof

The full proof is in [proofs/main.md](proofs/main.md). It has two lemmas and three parts.

**Lemma 1.** If every eigenvalue of $S$ has real part $\ge 0$ and $M e^{St} w_0 \to 0$ for every $w_0$, then $M = 0$. The proof goes along each Jordan chain of $S$: on the first vector, $M e^{St} v_1 = e^{\lambda t} M v_1$ and $|e^{\lambda t}| \ge 1$.

**Lemma 2.** If $A_c$ is Hurwitz, then $X S = A_c X + R$ has a unique solution, because the spectra of $A_c$ and $S$ are disjoint.

**Full information, sufficiency.** With $L = \Gamma + K\Pi$, the deviation $z = x - \Pi w$ satisfies $\dot z = (A - BK) z$ by the first equation, and $e = C z$ by the second. So $e \to 0$.

**Full information, necessity.** With $A_c = A - BK$ Hurwitz, Lemma 2 gives $\Pi$ with $\Pi S = A_c \Pi + BL + P$. Then $\delta = x - \Pi w$ satisfies $\dot \delta = A_c \delta$, and $e = C\delta + (C\Pi + Q) e^{St} w(0)$. Since $e \to 0$ and $\delta \to 0$, Lemma 1 gives $C\Pi + Q = 0$, and $\Gamma = L - K\Pi$ completes the solution.

**Error feedback.** Sufficiency: an observer for the joint state $(x, w)$, which exists by (H3), feeds the full information law. The closed loop is block triangular in the coordinates (plant state, observer error), so it is internally stable, and the error decays because the observer error does. Necessity: apply Lemma 2 to the whole closed loop of plant and controller. The first block row of its steady-state map gives $\Pi$, and $\Gamma = H \Sigma$, where $\Sigma$ is the steady state of the controller and $u = H\xi$ is its output map.

**Rank condition.** Write $X = \begin{bmatrix} \Pi \\ \Gamma \end{bmatrix}$. Then (RE) is $L X - E X S = R$ with $L = \begin{bmatrix} A & B \\ C & 0 \end{bmatrix}$, $E = \begin{bmatrix} I & 0 \\ 0 & 0 \end{bmatrix}$ and $R = -\begin{bmatrix} P \\ Q \end{bmatrix}$. If $y(L - \lambda E) = 0$ and $S v = \lambda v$, then $y (L X - E X S) v = 0$ for every $X$, so the map is not onto. If $L - \lambda E$ has full row rank at every eigenvalue, triangularize $S = U T U^\ast$ and solve column by column: column $j$ is $(L - t_{jj} E) y_j = (\text{known})$. The real part of a complex solution is a real solution. $\blacksquare$

## Consequences

- **Constant references and integral action.** For $S = 0$, (RE) is $\begin{bmatrix} A & B \\ C & 0 \end{bmatrix} \begin{bmatrix} \Pi \\ \Gamma \end{bmatrix} = -\begin{bmatrix} P \\ Q \end{bmatrix}$. It has a solution for all constant references and disturbances exactly when this matrix has full row rank: the plant has no invariant zero at 0, and $m \ge p$. This is the condition for [integral state feedback](/integral-state-feedback/).
- **Zeros block regulation.** By part 3, an invariant zero of the plant at an eigenvalue of $S$ makes the problem unsolvable for some data. A plant with a zero at $s = i\omega$ cannot track a sinusoid of frequency $\omega$, because its steady-state gain at $i\omega$ is singular. For a minimal plant with one input and one output, part 3 says that no eigenvalue of $S$ is a zero of $G(s) = C(sI - A)^{-1}B$ (see [transmission zero](/transmission-zero/)). A pole of $G$ at an eigenvalue of $S$ does no harm: the plant then contains part of the internal model.
- **A design recipe.** Solve (RE), which is linear; choose $K$ by pole placement or LQR; set $L = \Gamma + K\Pi$. The feedforward part $(\Gamma + K\Pi) w$ is a [feedforward](/feedforward-control/) term from the exosystem state, and the error decays at the rate of $A - BK$.
- **The internal model principle.** The necessity proof for error feedback gives $\Gamma = H\Sigma$, and the second block row of its steady-state equation is $\Sigma S = F\Sigma + G(C\Pi + Q) = F\Sigma$. So the controller dynamics $F$ reproduce the exosystem dynamics on the image of $\Sigma$, and the controller generates the steady-state input from its own state. When the regulation must hold for all small changes of the plant, this forces the controller to contain $p$ copies of the dynamics of $S$, which is the [internal model principle](/internal-model-principle/) of Francis and Wonham (1975).
- **Cost of a solution.** (RE) has $(n + p) q$ scalar equations in $(n + m) q$ unknowns. With $S$ in Schur form, the column by column method of the proof costs $O(q (n + m)^3 + q^3 + q^2 n)$ operations in the [real RAM](/real-ram/), against $O((n + m)^3 q^3)$ for the Kronecker form.

## Tightness

- **(H1) cannot be dropped.** If $S = -1$ (a decaying disturbance) and $C = 0$, $Q = 1$, then $e = w$ decays on its own and every stabilizing $K$ regulates, but $C\Pi + Q = 1 \ne 0$ for every $\Pi$. So the "only if" direction needs every eigenvalue of $S$ in the closed right half plane; Lemma 1 is false for decaying modes.
- **(H3) cannot be dropped for error feedback.** With $e = 0 \cdot x + 0 \cdot w$ the controller sees nothing; (RE) can still be solvable, for example when $P = 0$, $Q = 0$, but if $A$ is unstable no controller driven by $e$ stabilizes the plant.
- **The rank condition is sharp.** For $G(s) = s / ((s + 1)(s + 2))$ with $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $C = \begin{bmatrix} 0 & 1 \end{bmatrix}$, and $S = 0$, $P = 0$, $Q = -1$, the rank drops at $\lambda = 0$ and (RE) requires both $\pi_2 = 0$ and $\pi_2 = 1$. A step reference cannot be tracked.
- **Uniqueness needs $m = p$.** With $m > p$ the solution set is an affine space of dimension $(m - p) q$ when the rank condition holds; any of its points gives a regulator.
- **The first-order example of the output regulation page.** $\dot x = x + u$, $e = x - w_1$, $S = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$ gives the unique solution $\Pi = \begin{bmatrix} 1 & 0 \end{bmatrix}$, $\Gamma = \begin{bmatrix} -1 & 1 \end{bmatrix}$; the rank condition holds at $\pm i$ with determinant $-1$.

## History

Francis and Wonham (1975) proved the internal model principle for linear multivariable regulators, and Davison (1976) gave the existence conditions and the servocompensator for the robust servomechanism problem, including the rank condition at the exosystem eigenvalues. Francis (1977) gave the clean statement for the problem without robustness: solvability of the regulator problem with full information or with error feedback is equivalent to the solvability of the two linear matrix equations. Isidori and Byrnes (1990) showed that the nonlinear output regulation problem is decided, locally, by a nonlinear version of the equations, a pair of partial differential equations for maps $\pi(w)$ and $c(w)$; since then the equations are often called the Francis equations or the regulator equations.

## References
