---
tag: 6VKWRG
kind: theorem
slug: kalman-yakubovich-popov-lemma
name: Kalman-Yakubovich-Popov lemma
aliases:
- KYP lemma
- positive real lemma
area: control/stability
level: advanced
summary: A quadratic inequality on the frequency response of a linear system holds at every frequency if and only if a linear matrix inequality in its state-space matrices has a solution.
prereqs: [passivity, transfer-function, lyapunov-equation]
see_also: [bounded-real-lemma, linear-matrix-inequality, semidefinite-programming, circle-criterion, popov-criterion, s-procedure, continuous-algebraic-riccati-equation, prima]
sources:
  - paper: doi:10.1016/0167-6911(95)00063-1
    title: Anders Rantzer, On the Kalman-Yakubovich-Popov lemma, Systems and Control Letters 28(1), 7-10, 1996
    locator: the general statement with a symmetric matrix M, and the short proof of the strict case by a separating hyperplane
  - paper: doi:10.1073/pnas.49.2.201
    title: Rudolf E. Kalman, Lyapunov functions for the problem of Lur'e in automatic control, Proceedings of the National Academy of Sciences 49(2), 201-205, 1963
    locator: the equivalence of the frequency condition and the matrix equations for a quadratic Lyapunov function of the Lur'e system
  - paper: "V. A. Yakubovich, The solution of certain matrix inequalities in automatic control theory, Soviet Mathematics Doklady 3, 620-623, 1962 (Russian original in Doklady Akademii Nauk SSSR 143(6), 1962)"
    locator: the first proof that the Popov frequency condition gives a Lyapunov function of the Lur'e form
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 6.3 (positive real and strictly positive real transfer functions, the positive real lemma and the Kalman-Yakubovich-Popov lemma with the matrices P, L and W)
  - book: isbn:9780898713343
    title: Stephen Boyd, Laurent El Ghaoui, Eric Feron and Venkataramanan Balakrishnan, Linear Matrix Inequalities in System and Control Theory, SIAM, 1994
    locator: Chapter 2 (standard LMI problems, frequency domain inequalities and their LMI forms)
  - paper: doi:10.1109/TAC.1971.1099831
    title: Jan C. Willems, Least squares stationary optimal control and the algebraic Riccati equation, IEEE Transactions on Automatic Control 16(6), 621-634, 1971
    locator: the links between the frequency domain inequality, the Riccati equation and inequality, and the Hamiltonian matrix
---

The Kalman-Yakubovich-Popov (KYP) lemma connects two ways to state one property of a linear system. One way is an inequality on the frequency response, which must hold at every frequency. The other way is a [linear matrix inequality](/linear-matrix-inequality/) (LMI) on an unknown symmetric matrix $P$, built from the state-space matrices, which has a solution or not. The first form is a condition on infinitely many frequencies; the second is one finite convex problem that a [semidefinite programming](/semidefinite-programming/) solver can decide, and its solution $P$ gives a quadratic energy function $x^T P x$. For an electric circuit model, the positive real case says that the model is [passive](/passivity/), that is, it cannot produce energy at its ports, exactly when such an energy function exists. This is one way to check the passivity of reduced interconnect models such as those of [PRIMA](/prima/). The [bounded real lemma](/bounded-real-lemma/) is the case of the L2 gain, and the [circle criterion](/circle-criterion/) and the [Popov criterion](/popov-criterion/) use the lemma to turn a Nyquist plot condition into a Lyapunov function.

## Statement

**Setting.** $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, and a symmetric $M \in \mathbb{R}^{(n+m) \times (n+m)}$. $A$ has no eigenvalue on the imaginary axis, so $(j\omega I - A)^{-1}$ exists for every real $\omega$. Write

$$\Phi(\omega) = \begin{bmatrix} (j\omega I - A)^{-1} B \\ I \end{bmatrix}, \qquad \Phi(\infty) = \begin{bmatrix} 0 \\ I \end{bmatrix}, \qquad \mathcal{F}(P) = \begin{bmatrix} A^T P + P A & P B \\ B^T P & 0 \end{bmatrix}.$$

If $x = (j\omega I - A)^{-1} B u$, then $\Phi(\omega) u = (x, u)$ is the steady-state response of $\dot x = Ax + Bu$ to the input $u e^{j\omega t}$, so $\Phi(\omega)^* M \Phi(\omega) \le 0$ says that the quadratic form $M$ is at most $0$ on all sinusoidal steady states at the frequency $\omega$.

**Theorem (Rantzer's form, 1996).**
1. *Strict form.* $\Phi(\omega)^* M \Phi(\omega) < 0$ for all $\omega \in \mathbb{R} \cup \{\infty\}$ if and only if there is a symmetric $P$ with $M + \mathcal{F}(P) < 0$.
2. *Non-strict form.* If in addition $(A, B)$ is controllable, then $\Phi(\omega)^* M \Phi(\omega) \le 0$ for all $\omega \in \mathbb{R} \cup \{\infty\}$ if and only if there is a symmetric $P$ with $M + \mathcal{F}(P) \le 0$.

$P$ is not required to be positive definite here. Sign conditions on $P$ come from the special cases.

**Special cases, side by side.** Let $G(s) = C(sI - A)^{-1}B + D$ with $m$ inputs and $m$ outputs for the first two rows.

| Property | Frequency domain inequality | Linear matrix inequality |
|---|---|---|
| positive real; $(A, B)$ controllable and $(A, C)$ observable | $G(j\omega) + G(j\omega)^* \ge 0$ for all $\omega$ with $j\omega$ not a pole, plus the pole conditions of [passivity](/passivity/) | $P > 0$ and $\begin{bmatrix} A^T P + P A & P B - C^T \\ B^T P - C & -(D + D^T) \end{bmatrix} \le 0$ |
| strictly positive real; $(A, B)$ controllable and $(A, C)$ observable | $G(s - \varepsilon)$ positive real for some $\varepsilon > 0$ | $P > 0$, $\varepsilon > 0$ and $\begin{bmatrix} A^T P + P A + \varepsilon P & P B - C^T \\ B^T P - C & -(D + D^T) \end{bmatrix} \le 0$ |
| H-infinity norm below $\gamma$; $A$ Hurwitz | $G(j\omega)^* G(j\omega) < \gamma^2 I$ for all $\omega \in \mathbb{R} \cup \{\infty\}$ | $P > 0$ and $\begin{bmatrix} A^T P + P A + C^T C & P B + C^T D \\ B^T P + D^T C & D^T D - \gamma^2 I \end{bmatrix} < 0$ |

The first row is the positive real lemma. Khalil (2002, Section 6.3) writes it with matrices $L$ and $W$: $PA + A^T P = -L^T L$, $PB = C^T - L^T W$, $W^T W = D + D^T$. These equations say that minus the matrix in the table equals $[L \ \ W]^T [L \ \ W]$, which is positive semidefinite. The second row is what Khalil calls the Kalman-Yakubovich-Popov lemma, with $-L^T L - \varepsilon P$ in the first equation; it needs the observability of $(A, C)$. The third row is the strict [bounded real lemma](/bounded-real-lemma/).

## In plain words

A linear system can be tested one frequency at a time: feed it a sine wave, wait for the steady state, and check an inequality on what goes in and what comes out. To be sure, one must do this at every frequency, and there are infinitely many. The lemma says that one can replace all these checks by one search for a single symmetric matrix that solves a matrix inequality. If such a matrix exists, it gives an energy-like function of the state that proves the property for all inputs, not only for sine waves. If no such matrix exists, some frequency breaks the inequality. The extra condition about controllability makes sure that the state can be moved enough for the two tests to agree.

## Proof

**From the LMI to the frequency inequality.** Let $M + \mathcal{F}(P) \le 0$. Fix a real $\omega$ and a complex $u \in \mathbb{C}^m$, and let $x = (j\omega I - A)^{-1}Bu$, so that $Ax + Bu = j\omega x$. Then

$$\begin{bmatrix} x \\ u \end{bmatrix}^* \mathcal{F}(P) \begin{bmatrix} x \\ u \end{bmatrix} = (Ax + Bu)^* P x + x^* P (Ax + Bu) = (-j\omega + j\omega)\, x^* P x = 0.$$

So $u^* \Phi(\omega)^* M \Phi(\omega) u = [x; u]^* (M + \mathcal{F}(P)) [x; u] \le 0$. At $\omega = \infty$, $x = 0$ and the same quadratic form is $u^* M_{22} u$, the lower right block of $M + \mathcal{F}(P)$, which is at most $0$. With strict inequalities the same steps give a strict result, because $(x, u) \ne 0$ when $u \ne 0$.

**From the strict frequency inequality to the LMI** (Rantzer's argument). Suppose no symmetric $P$ gives $M + \mathcal{F}(P) < 0$. Then the affine set $\{M + \mathcal{F}(P)\}$ does not meet the open convex cone of negative definite matrices. By the [separating hyperplane theorem](/separating-hyperplane-theorem/) there is a symmetric $W \ne 0$ with $\operatorname{tr}(W Y) \le c \le \operatorname{tr}(W (M + \mathcal{F}(P)))$ for every $Y < 0$ and every $P$. The cone condition forces $W \ge 0$ and $c \ge 0$. The affine set is unbounded in every direction $\mathcal{F}(P)$, so $\operatorname{tr}(W \mathcal{F}(P)) = 0$ for every $P$, and then $\operatorname{tr}(W M) \ge 0$.

Factor $W = [X; U][X; U]^T$ with $X \in \mathbb{R}^{n \times r}$, $U \in \mathbb{R}^{m \times r}$ and $r = \operatorname{rank} W \ge 1$, so that $[X; U]$ has full column rank. Expanding $\operatorname{tr}(W \mathcal{F}(P)) = \operatorname{tr}(P (F X^T + X F^T))$ with $F = AX + BU$ shows that $F X^T + X F^T = 0$. Then

$$(F + X)(F + X)^* = F F^* + X X^* = (F - X)(F - X)^*,$$

and two $n \times r$ matrices with the same Gram matrix differ by a unitary factor: $F + X = (F - X) V$ with $V$ unitary. Let $v_1, \ldots, v_r$ be an orthonormal basis of eigenvectors of $V$, with $V v_k = e^{j\theta_k} v_k$. Then $(1 - e^{j\theta_k}) F v_k = -(1 + e^{j\theta_k}) X v_k$. Put $x_k = X v_k$ and $u_k = U v_k$; they are not both $0$.
- If $\theta_k \ne 0$, this reads $A x_k + B u_k = j\omega_k x_k$ with the real number $\omega_k = -\cot(\theta_k / 2)$. Since $A$ has no eigenvalue $j\omega_k$, $u_k \ne 0$ and $x_k = (j\omega_k I - A)^{-1} B u_k$, so $[x_k; u_k] = \Phi(\omega_k) u_k$.
- If $\theta_k = 0$, then $x_k = 0$, $u_k \ne 0$ and $[x_k; u_k] = \Phi(\infty) u_k$.

Finally $0 \le \operatorname{tr}(W M) = \sum_k [x_k; u_k]^* M [x_k; u_k]$, so some term is at least $0$. That term is $u_k^* \Phi(\omega_k)^* M \Phi(\omega_k) u_k \ge 0$ with $u_k \ne 0$, against the strict frequency inequality. $\square$

**The non-strict form.** The direction from the LMI is proved above. The converse takes more work, and Rantzer (1996) gives it; controllability of $(A, B)$ is used there and nowhere else. Without controllability the converse fails; see Tightness.

## Consequences

**Worked example, positive real case.** $G(s) = 1/(s + 1)$, with $A = -1$, $B = 1$, $C = 1$, $D = 0$. The frequency side is $\operatorname{Re} G(j\omega) = 1/(1 + \omega^2) > 0$. The LMI of the first row is

$$\begin{bmatrix} -2p & p - 1 \\ p - 1 & 0 \end{bmatrix} \le 0.$$

A zero diagonal entry forces the off-diagonal entry to be $0$, so $p = 1$, the only solution. Then $L^T L = 2$ gives $L = \sqrt 2$, and $W = 0$. The storage $V = \frac{1}{2} x^T P x = \frac{1}{2}x^2$ gives $\dot V = -x^2 + xu = uy - y^2$. In the second row, the first entry becomes $-2p + \varepsilon p$, so $p = 1$ works for every $\varepsilon \in (0, 2]$, and $G$ is strictly positive real.

**Worked example, bounded real case.** For the same $G$ with $\gamma = 1$, the non-strict LMI is $\begin{bmatrix} 1 - 2p & p \\ p & -1 \end{bmatrix} \le 0$. Its determinant is $-(p - 1)^2$, so only $p = 1$ works, and no $P$ makes it strictly negative. This matches $\|G\|_\infty = 1$, reached at $\omega = 0$. For $\gamma = 2$ the solutions form the interval $p \in [4 - 2\sqrt 3,\ 4 + 2\sqrt 3] = [0.53590,\ 7.46410]$; these are the quadratic storage functions of [dissipativity](/dissipativity/) for the L2 gain supply.

**Absolute stability.** With $M$ chosen from a sector, the lemma turns the frequency condition of the [circle criterion](/circle-criterion/) into a common quadratic Lyapunov function, and the [Popov criterion](/popov-criterion/) into a Lyapunov function of the Lur'e form $x^T P x + 2\eta k \int_0^{y} \varphi(\sigma)\, d\sigma$.

**Riccati form.** If $M_{22} < 0$, the [Schur complement](/schur-complement/) turns $M + \mathcal{F}(P) \le 0$ into a Riccati inequality in $P$. Willems (1971) connects the frequency inequality, the Riccati equation and the eigenvalues of a [Hamiltonian matrix](/hamiltonian-matrix/) of size $2n$; a solution of the [continuous algebraic Riccati equation](/continuous-algebraic-riccati-equation/) is the extreme case of the LMI.

**Size and cost.** The LMI has $n(n+1)/2$ scalar unknowns (the entries of $P$) and one matrix of size $(n + m) \times (n + m)$; the positive real case adds the constraint $P > 0$ of size $n$. An interior point method solves it to accuracy $\varepsilon$ in a number of iterations polynomial in $n$ and $\log(1/\varepsilon)$ under strict feasibility; see [semidefinite programming](/semidefinite-programming/). For large $n$, a frequency sweep or a Hamiltonian eigenvalue test is cheaper, but a sweep on a grid can miss a narrow violation between grid points.

**S-procedure.** The frequency inequality says that a quadratic form is at most $0$ on the vectors $(x, u)$ with $j\omega x = Ax + Bu$, and the term $\mathcal{F}(P)$ is a quadratic form that vanishes on those vectors. In this sense the lemma is a case of the [S-procedure](/s-procedure/) in which the relaxation loses nothing.

## Tightness

**Controllability cannot be dropped in the non-strict form.** Take $n = m = 1$, $A = -1$, $B = 0$ and $M = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$. Here $(j\omega I - A)^{-1} B = 0$, so $\Phi(\omega)^* M \Phi(\omega) = M_{22} = 0 \le 0$ at every frequency. The LMI is $\begin{bmatrix} -2p & 1 \\ 1 & 0 \end{bmatrix} \le 0$, which fails for every $p$, because the diagonal has a $0$ next to a nonzero off-diagonal entry. The strict forms are consistent: $M_{22} = 0$ is not $< 0$.

**Observability and the sign of P.** In the positive real lemma, observability gives $P > 0$. Without it, a solution $P$ can be singular, and $\frac{1}{2}x^T P x$ is then only positive semidefinite, which still proves passivity but not the Lyapunov stability of the unobservable part.

**Imaginary-axis eigenvalues.** Rantzer's form needs $A$ without eigenvalues on the imaginary axis, because $\Phi(\omega)$ must exist. The positive real lemma allows simple poles on the axis, as for $G(s) = 1/s$ with $A = 0$, $B = C = 1$, $D = 0$: the LMI $\begin{bmatrix} 0 & p - 1 \\ p - 1 & 0 \end{bmatrix} \le 0$ holds with $p = 1$.

## History

Popov (1961) gave a frequency domain condition for the absolute stability of the [Lur'e problem](/lure-problem/). Yakubovich (1962) proved that the condition implies the existence of a Lyapunov function of the Lur'e form, by solving the matrix inequalities. Kalman (1963) gave a proof in the form that is now called the lemma, with controllability and observability. Anderson extended it to multivariable positive real matrices in 1967, and Willems (1971) linked it to the Riccati equation and to optimal control. Rantzer (1996) gave the short proof by convex separation that is followed above. The names "positive real lemma" and "KYP lemma" are used for different special cases in different books, so check which form a source states.

## References
