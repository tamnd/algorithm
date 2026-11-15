---
tag: 601MX7
kind: theorem
slug: bounded-real-lemma
name: Bounded real lemma
aliases:
- bounded real lemma for the H-infinity norm
area: control/robust-and-adaptive-control
level: advanced
summary: "A is Hurwitz and the H-infinity norm of C(sI - A)^(-1)B + D is less than gamma if and only if an LMI in P > 0 is feasible, or a Riccati equation has a stabilizing solution P >= 0."
prereqs: [h-infinity-norm, linear-matrix-inequality, kalman-yakubovich-popov-lemma]
see_also: [h-infinity-norm-computation, kalman-yakubovich-popov-lemma, small-gain-theorem, lmi-h-infinity-synthesis, dissipativity, continuous-algebraic-riccati-equation, linear-matrix-inequality, h-infinity-control-problem]
sources:
  - book: isbn:089871334X
    title: Stephen Boyd, Laurent El Ghaoui, Eric Feron and Venkataramanan Balakrishnan, Linear Matrix Inequalities in System and Control Theory, SIAM Studies in Applied Mathematics 15, SIAM, 1994
    locator: Section 2.7.3, The bounded-real lemma (the nonstrict LMI for a minimal realization with A Hurwitz, the Riccati equation and its Hamiltonian matrix), and the Notes and References of Chapter 2
  - book: isbn:9780486453576
    title: Brian D. O. Anderson and Sumeth Vongpanitlerd, Network Analysis and Synthesis, A Modern Systems Theory Approach, Prentice-Hall, 1973 (Dover reprint 2006)
    locator: the state-space bounded real lemma for minimal realizations and its use in network synthesis
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: the chapter on algebraic Riccati equations (the bounded real lemma in Riccati form, and the existence of the stabilizing solution)
  - paper: doi:10.1007/BF02551385
    title: Stephen Boyd, Venkataramanan Balakrishnan and Pierre Kabamba, A bisection method for computing the H-infinity norm of a transfer matrix and related problems, Mathematics of Control, Signals, and Systems 2(3) (1989) 207-219
    locator: the link between the singular values of G(j omega) and the imaginary eigenvalues of the Hamiltonian matrix
---

The bounded real lemma turns the frequency domain statement "the [H-infinity norm](/h-infinity-norm/) of $G$ is less than $\gamma$" into a statement about one symmetric matrix $P$: a [linear matrix inequality](/linear-matrix-inequality/) that $P$ satisfies, or an algebraic Riccati equation that $P$ solves. The quadratic function $V(x) = x^T P x$ is then a storage function: along every trajectory, the stored energy grows at most by $\gamma^2 |u|^2 - |y|^2$. The LMI form makes the H-infinity norm an object of convex optimization, and it is the base of [LMI H-infinity synthesis](/lmi-h-infinity-synthesis/). The name comes from network theory, where the scattering matrix of a passive network is called bounded real.

## Statement

**Setting.** $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $C \in \mathbb{R}^{p \times n}$, $D \in \mathbb{R}^{p \times m}$, $G(s) = C (sI - A)^{-1} B + D$, and $\gamma > 0$. No controllability or observability is assumed. For symmetric matrices, $P > 0$ means positive definite and $< 0$ means negative definite.

**Theorem (bounded real lemma, strict form).** The following are equivalent.

1. $A$ is [Hurwitz](/hurwitz-matrix/) and $\|G\|_\infty < \gamma$.
2. There is a symmetric $P > 0$ with
$$\begin{bmatrix} A^T P + P A + C^T C & P B + C^T D \\ B^T P + D^T C & D^T D - \gamma^2 I \end{bmatrix} < 0 .$$
3. There is a symmetric $\tilde P > 0$ with
$$\begin{bmatrix} A^T \tilde P + \tilde P A & \tilde P B & C^T \\ B^T \tilde P & -\gamma I & D^T \\ C & D & -\gamma I \end{bmatrix} < 0 .$$
4. $A$ is Hurwitz, $R = \gamma^2 I - D^T D > 0$, and the Riccati equation
$$A^T X + X A + (X B + C^T D) R^{-1} (B^T X + D^T C) + C^T C = 0$$
has a symmetric solution $X \ge 0$ that is stabilizing: $A + B R^{-1}(B^T X + D^T C)$ is Hurwitz.

Form 2 is affine in $(P, \gamma^2)$, and form 3 is affine in $(\tilde P, \gamma)$; the two are related by $P = \gamma \tilde P$.

## In plain words

Think of $x^T P x$ as energy stored inside the system. The inequality says that, at every moment, the stored energy can grow by at most $\gamma^2$ times the power that goes in, minus the power that comes out. Start empty, run any input, and the stored energy can never be negative, so the energy that comes out is less than $\gamma^2$ times the energy that went in. That is exactly a gain below $\gamma$. The lemma says the converse holds too: whenever the gain is below $\gamma$, such an energy function exists, and it can be found by solving a convex problem or one quadratic matrix equation.

## Proof

**2 and 3 are equivalent.** Apply the [Schur complement](/schur-complement/) to the last block $-\gamma I < 0$ of form 3. It holds if and only if

$$\begin{bmatrix} A^T \tilde P + \tilde P A + \gamma^{-1} C^T C & \tilde P B + \gamma^{-1} C^T D \\ B^T \tilde P + \gamma^{-1} D^T C & \gamma^{-1} D^T D - \gamma I \end{bmatrix} < 0 .$$

Multiply by $\gamma > 0$ and set $P = \gamma \tilde P$; this is form 2.

**2 implies 1.** Call the matrix of form 2 $L$. Its upper left block gives $A^T P + P A < -C^T C \le 0$ with $P > 0$, so $A$ is Hurwitz by the [Lyapunov theorem for linear systems](/lyapunov-theorem-for-linear-systems/). Since $L < 0$, there is $\varepsilon > 0$ with $L \le -\varepsilon I$. Let $x(0) = 0$ and let $u$ have finite energy. With $V = x^T P x$ and $y = C x + D u$, a direct expansion gives

$$\frac{d}{dt} V + |y|^2 - \gamma^2 |u|^2 = \begin{bmatrix} x \\ u \end{bmatrix}^T L \begin{bmatrix} x \\ u \end{bmatrix} \le -\varepsilon |u|^2 .$$

Integrate from 0 to $T$ and use $V(0) = 0$ and $V(T) \ge 0$: $\int_0^T |y|^2 dt \le (\gamma^2 - \varepsilon) \int_0^T |u|^2 dt$. Let $T \to \infty$. The $L_2$ gain of the system is at most $\sqrt{\gamma^2 - \varepsilon} < \gamma$, and for $A$ Hurwitz the $L_2$ gain equals $\|G\|_\infty$ (see the H-infinity norm page). So $\|G\|_\infty < \gamma$.

**4 implies 2.** Let $X$ be as in 4, $F = R^{-1}(B^T X + D^T C)$ and $A_F = A + B F$, which is Hurwitz. Let $Y > 0$ solve $A_F^T Y + Y A_F = -I$; it exists because $A_F$ is Hurwitz. Write $\operatorname{Ric}(P)$ for the left side of the Riccati equation with $X$ replaced by $P$. Expanding,

$$\operatorname{Ric}(X + \delta Y) = \operatorname{Ric}(X) + \delta (A_F^T Y + Y A_F) + \delta^2 Y B R^{-1} B^T Y = -\delta I + \delta^2 Y B R^{-1} B^T Y,$$

which is negative definite for small $\delta > 0$. Then $P = X + \delta Y > 0$, because $X \ge 0$ and $Y > 0$. Since the lower right block of form 2 is $-R < 0$, the Schur complement shows that form 2 holds exactly when $\operatorname{Ric}(P) < 0$. So $P$ satisfies form 2.

**1 implies 4 (sketch).** As $\omega \to \infty$, $G(j\omega) \to D$, so $\sigma_{\max}(D) \le \|G\|_\infty < \gamma$ and $R > 0$. The Hamiltonian matrix of the Riccati equation is

$$H = \begin{bmatrix} A + B R^{-1} D^T C & B R^{-1} B^T \\ -C^T (I + D R^{-1} D^T) C & -(A + B R^{-1} D^T C)^T \end{bmatrix}.$$

It has an eigenvalue $j\omega$ if and only if $\gamma$ is a singular value of $G(j\omega)$ (Boyd, Balakrishnan and Kabamba 1989; for $D = 0$, $H$ is similar to the matrix $H_\gamma$ of [H-infinity norm computation](/h-infinity-norm-computation/) by the scaling $\operatorname{diag}(I, \gamma I)$, and that page proves the claim). Since $\|G\|_\infty < \gamma$, $H$ has no imaginary eigenvalue, so it has $n$ eigenvalues in each open half plane. The remaining step shows that the invariant subspace of the $n$ stable eigenvalues has the form $\operatorname{range} \begin{bmatrix} I \\ X \end{bmatrix}$; then $X$ is symmetric, solves the Riccati equation, and $A + B F$ (with $F$ from $X$) has the stable eigenvalues of $H$. This step uses that $A$ is Hurwitz and is proved in Zhou, Doyle and Glover (1996), in the chapter on algebraic Riccati equations; see also the [stabilizing Riccati solution theorem](/stabilizing-riccati-solution-theorem/) for the method in the LQR case. Finally, the Riccati equation reads $A^T X + X A = -(F^T R F + C^T C)$, whose right side is $\le 0$, and $A$ is Hurwitz, so $X = \int_0^\infty e^{A^T t} (F^T R F + C^T C) e^{A t} dt \ge 0$.

A second proof of 1 implies 2 goes through the strict frequency domain form of the [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/) with the quadratic form $|y|^2 - \gamma^2 |u|^2$: for $A$ Hurwitz, $\|G\|_\infty < \gamma$ is the strict inequality $G(j\omega)^H G(j\omega) < \gamma^2 I$ for all $\omega$ in $\mathbb{R} \cup \{\infty\}$, and the strict KYP lemma, which needs no controllability, gives a symmetric $P$ with form 2. Then $P > 0$ follows from $A^T P + P A < 0$ and $A$ Hurwitz.

## Consequences

- **The norm as a semidefinite program.** Minimize $\gamma^2$ subject to form 2. The unknowns are $P$ and $\gamma^2$, $n(n+1)/2 + 1$ scalars, and the constraint matrices have size $n + m$ (and $n$ for $P > 0$). This is a [semidefinite program](/semidefinite-programming/). Its solution is the H-infinity norm, but to compute the norm alone the Hamiltonian method of [H-infinity norm computation](/h-infinity-norm-computation/) is much cheaper, $O(n^3)$ per step against an SDP with $O(n^2)$ unknowns.
- **Robustness with scalings.** With a scaling matrix in the LMI, the lemma gives the scaled small gain tests for structured uncertainty, which are upper bounds on the [structured singular value](/structured-singular-value/). The [small-gain theorem](/small-gain-theorem/) uses the plain form.
- **Synthesis.** Form 3 is affine in the closed-loop matrices. For the closed loop of a plant and a controller, it is the starting point of [LMI H-infinity synthesis](/lmi-h-infinity-synthesis/), which removes the controller variables by elimination or by a change of variables.
- **Dissipativity.** Form 2 says that $V = x^T P x$ is a storage function for the supply rate $\gamma^2 |u|^2 - |y|^2$; see [dissipativity](/dissipativity/). The positive real lemma (the [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/)) is the same statement for the supply rate $u^T y$.
- **Discrete time.** For $G(z) = C(zI - A)^{-1}B + D$: $A$ is Schur and $\|G\|_\infty < \gamma$ if and only if there is $P > 0$ with $\begin{bmatrix} A^T P A - P + C^T C & A^T P B + C^T D \\ B^T P A + D^T C & B^T P B + D^T D - \gamma^2 I \end{bmatrix} < 0$.

**Example.** Take $G(s) = 1/(s + 1)$: $A = -1$, $B = C = 1$, $D = 0$, with $\|G\|_\infty = 1$. Form 2 is the $2 \times 2$ matrix $\begin{bmatrix} 1 - 2p & p \\ p & -\gamma^2 \end{bmatrix} < 0$. It holds if and only if $1 - 2p < 0$ and $\gamma^2 (2p - 1) - p^2 > 0$, that is $p^2 - 2\gamma^2 p + \gamma^2 < 0$, so

$$\gamma^2 - \gamma\sqrt{\gamma^2 - 1} < p < \gamma^2 + \gamma\sqrt{\gamma^2 - 1}.$$

The interval is not empty exactly when $\gamma > 1 = \|G\|_\infty$, as the lemma says. For $\gamma = 2$ it is $(0.5359, 7.4641)$, and $p = 1$ gives $\begin{bmatrix} -1 & 1 \\ 1 & -4 \end{bmatrix}$, with trace $-5$ and determinant $3$, so it is negative definite. The Riccati equation of form 4 is $-2x + x^2/\gamma^2 + 1 = 0$. Its stabilizing root is $x = \gamma^2 (1 - \sqrt{1 - 1/\gamma^2})$, with $A + B R^{-1} B^T x = -\sqrt{1 - 1/\gamma^2} < 0$; for $\gamma = 2$ this is $x = 4 - 2\sqrt 3 = 0.5359$, the lower end of the interval. For the lightly damped check system $1/(s^2 + 0.2 s + 1)$, form 2 is feasible exactly for $\gamma > 5.02519$.

## Tightness

- **Strictness.** At $\gamma = \|G\|_\infty$ the strict LMI is infeasible: in the example, the interval for $p$ is empty at $\gamma = 1$. The nonstrict LMI ($\le 0$) characterizes $\|G\|_\infty \le \gamma$ only under more hypotheses: Boyd et al. (1994, Section 2.7.3) assume $A$ Hurwitz and $(A, B, C)$ minimal.
- **The nonstrict LMI does not give Hurwitz.** With $A = 0$, $B = 0$, $C = 0$, $D = 0$ ($n = m = p = 1$), $P = 1$ satisfies the nonstrict form 2, whose matrix is $\operatorname{diag}(0, -\gamma^2)$, but $A$ is not Hurwitz. The mode at 0 is neither controllable nor observable, so $G = 0$ does not see it.
- **P > 0 is needed.** For $G(s) = 1/(s - 1)$ ($A = 1$, $B = C = 1$, $D = 0$) and $\gamma = 2$, the value $p = -1$ makes the matrix of form 2 equal to $\begin{bmatrix} -1 & -1 \\ -1 & -4 \end{bmatrix} < 0$. But $A$ is not Hurwitz and $G \notin H_\infty$. Without $P > 0$, the inequality only bounds the peak of $\sigma_{\max}(G(j\omega))$ on the imaginary axis (here $1 < 2$), which is not an $L_2$ gain of the causal system.
- **The stabilizing condition in 4.** The Riccati equation of the example has a second root, $x = \gamma^2(1 + \sqrt{1 - 1/\gamma^2})$, which is $\ge 0$ but not stabilizing. Only the stabilizing root gives form 2 by the perturbation in the proof.

## History

The bounded real condition comes from the synthesis of passive electrical networks: the scattering matrix of a passive network is bounded real. The state-space lemma for minimal realizations, a companion of the positive real lemma of Kalman, Yakubovich and Popov, is in Anderson and Vongpanitlerd (1973). Willems (1971) related Riccati equations, frequency domain inequalities and LMIs, and his later work on dissipative systems gave the storage function reading. Boyd, Balakrishnan and Kabamba (1989) used the Hamiltonian matrix of the lemma to compute the H-infinity norm. In the 1990s the strict LMI form, without minimality, became the standard tool of LMI based robust control, as in Boyd, El Ghaoui, Feron and Balakrishnan (1994).

## References
