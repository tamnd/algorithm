---
tag: A0YPQ3
kind: theorem
slug: stabilizing-riccati-solution-theorem
name: Existence of the stabilizing Riccati solution
aliases:
- stabilizing solution theorem
area: control/optimal-and-predictive-control
level: advanced
summary: If (A, B) is stabilizable, (Q^(1/2), A) is detectable and R > 0, the algebraic Riccati equation has a unique stabilizing solution, which is positive semidefinite.
prereqs: [continuous-algebraic-riccati-equation, hamiltonian-matrix, stabilizability, detectability]
see_also: [discrete-algebraic-riccati-equation, infinite-horizon-lqr, schur-method-riccati, kleinman-iteration, popov-belevitch-hautus-test, lyapunov-theorem-for-linear-systems, kalman-bucy-filter, lqr-problem]
sources:
  - paper: "Vladimír Kučera, A contribution to matrix quadratic equations, IEEE Transactions on Automatic Control 17(3), 344-347, 1972"
    locator: the existence and uniqueness of the stabilizing solution under stabilizability and detectability, through the eigenvectors of the Hamiltonian matrix
  - paper: doi:10.1137/0306044
    title: W. M. Wonham, On a matrix Riccati equation of stochastic control, SIAM Journal on Control 6(4), 681-697, 1968
    locator: the positive semidefinite solution of the algebraic Riccati equation and the stability of the closed loop
  - paper: "R. E. Kalman, Contributions to the theory of optimal control, Boletín de la Sociedad Matemática Mexicana 5(2), 102-119, 1960"
    locator: the regulator problem on an infinite interval
  - book: isbn:9780198537953
    title: Peter Lancaster and Leiba Rodman, Algebraic Riccati Equations, Clarendon Press, Oxford, 1995
    locator: the existence of extremal and stabilizing solutions of the continuous and discrete equations
  - book: isbn:0134565673
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 13, Algebraic Riccati Equations, with the stabilizing solution in terms of the Hamiltonian matrix
---

The stabilizing solution theorem gives conditions under which the [continuous-time algebraic Riccati equation](/continuous-algebraic-riccati-equation/) $A^T P + P A - P B R^{-1} B^T P + Q = 0$ has exactly one solution $P$ that makes the closed loop $A - B R^{-1} B^T P$ Hurwitz. The conditions are that $(A, B)$ is [stabilizable](/stabilizability/), that $(Q^{1/2}, A)$ is [detectable](/detectability/), and that $R > 0$. The solution is then positive semidefinite, and it is the only positive semidefinite solution. In this form the theorem is due to Kučera (1972). It is the reason that infinite-horizon LQR always gives a stabilizing gain under these conditions, and the reason that the [Schur method](/schur-method-riccati/) can divide by the block $X_1$. The same statement holds for the [DARE](/discrete-algebraic-riccati-equation/), with Schur in place of Hurwitz. The detectability is written as $(Q^{1/2}, A)$, in the $(C, A)$ order of this area: $Q = C^T C$ with $C = Q^{1/2}$.

## Statement

**Data.** $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $Q = Q^T \ge 0$ and $R = R^T > 0$. Let $G = B R^{-1} B^T$ and let $H = \begin{bmatrix} A & -G \\ -Q & -A^T \end{bmatrix}$ be the [Hamiltonian matrix](/hamiltonian-matrix/). A symmetric solution $P$ of the CARE is *stabilizing* if $A - G P$ is Hurwitz.

**Theorem (continuous time).** Assume that $(A, B)$ is stabilizable and $(Q^{1/2}, A)$ is detectable. Then:

1. $H$ has no eigenvalue on the imaginary axis. Let the columns of $\begin{bmatrix} X_1 \\ X_2 \end{bmatrix} \in \mathbb{R}^{2n \times n}$ be a basis of the invariant subspace of its $n$ eigenvalues in the open left half plane. Then $X_1$ is invertible.
2. $P = X_2 X_1^{-1}$ is symmetric, solves the CARE, and is stabilizing.
3. $P$ is the only stabilizing solution.
4. $P \ge 0$, and $P$ is the only positive semidefinite solution of the CARE.
5. If $(Q^{1/2}, A)$ is observable, then $P > 0$.

**Theorem (discrete time).** Assume that $(A, B)$ is stabilizable, $(Q^{1/2}, A)$ is detectable and $R > 0$. Then the DARE $P = A^T P A - A^T P B (R + B^T P B)^{-1} B^T P A + Q$ has exactly one stabilizing solution: one with $A - B (R + B^T P B)^{-1} B^T P A$ Schur. It is positive semidefinite, it is the only positive semidefinite solution, and the Riccati recursion from $P_0 = 0$ converges to it.

## In plain words

The Riccati equation is quadratic in a matrix, so it can have many solutions. Only one of them gives a feedback that brings every state to zero, and the theorem says when that one exists. Two things must hold. First, every unstable part of the system must be reachable by the input, or there is nothing the controller can do about it. Second, every unstable part of the system must show up in the cost, or the controller has no reason to act on it. If both hold and the input weight is positive, the good solution exists, there is only one, and it is the only solution with no negative directions. A solver can then look for the nonnegative solution and know it has found the right one.

## Proof

The proof is for continuous time. The discrete case is proved on the [infinite-horizon LQR](/infinite-horizon-lqr/) page (its correctness proof): the recursion from 0 increases to a limit, the limit solves the DARE, detectability makes it stabilizing, and completing the square makes it unique. The same steps give "only positive semidefinite solution" there, because Lemma 4 of that proof applies to every positive semidefinite solution.

**Step 1: no eigenvalue on the imaginary axis.** Suppose $H \begin{bmatrix} x \\ y \end{bmatrix} = i \omega \begin{bmatrix} x \\ y \end{bmatrix}$ with $\omega$ real and $(x, y) \ne 0$. The two block rows are $A x - G y = i \omega x$ and $-Q x - A^T y = i \omega y$. Multiply the first by $y^*$ on the left. Take the conjugate transpose of the second and multiply by $x$ on the right. The sum is $-y^* G y - x^* Q x = 0$. Both terms are at most 0, so both are 0: $B^T y = 0$ and $Q x = 0$. The rows become $A x = i \omega x$ and $y^* A = i \omega\, y^*$. If $x \ne 0$, then $x$ is an eigenvector of $A$ on the imaginary axis with $Q^{1/2} x = 0$, which the [PBH test](/popov-belevitch-hautus-test/) for detectability forbids. If $y \ne 0$, then $y$ is a left eigenvector of $A$ on the imaginary axis with $y^* B = 0$, which the PBH test for stabilizability forbids. So $(x, y) = 0$, a contradiction.

The spectrum of $H$ is symmetric about the imaginary axis (see the Hamiltonian matrix page), so exactly $n$ eigenvalues lie in the open left half plane. Their invariant subspace is real, because the set of these eigenvalues is closed under conjugation, so a real basis $X = \begin{bmatrix} X_1 \\ X_2 \end{bmatrix}$ exists, with $H X = X \Lambda$ and $\Lambda$ Hurwitz.

**Step 2: $X_1^T X_2$ is symmetric.** This is the Lagrangian property, proved on the Hamiltonian matrix page: $M = X^T J X$ satisfies $\Lambda^T M + M \Lambda = 0$ with $\Lambda$ Hurwitz, so $M = X_1^T X_2 - X_2^T X_1 = 0$.

**Step 3: $X_1$ is invertible.** The block rows of $H X = X \Lambda$ are

$$A X_1 - G X_2 = X_1 \Lambda, \qquad -Q X_1 - A^T X_2 = X_2 \Lambda.$$

Let $v \in \mathbb{C}^n$ be in the kernel of $X_1$. Multiply the first row by $v^* X_2^T$ on the left and by $v$ on the right. The left side is $-v^* X_2^T G X_2 v$, because $X_1 v = 0$. The right side is $v^* X_2^T X_1 \Lambda v = v^* X_1^T X_2 \Lambda v = (X_1 v)^* X_2 \Lambda v = 0$, by Step 2. So $v^* X_2^T G X_2 v = |R^{-1/2} B^T X_2 v|^2 = 0$, hence $B^T X_2 v = 0$, hence $G X_2 v = 0$. The first row applied to $v$ now gives $X_1 \Lambda v = 0$. So the kernel of $X_1$ is invariant under $\Lambda$. If it is not $\{0\}$, it contains an eigenvector: $\Lambda v = \lambda v$ with $\operatorname{Re} \lambda < 0$, $v \ne 0$ complex, $X_1 v = 0$ and $B^T X_2 v = 0$. The second row applied to $v$ gives $-A^T X_2 v = \lambda X_2 v$. The vector $y = X_2 v$ is not 0, because $X$ has full column rank and $X_1 v = 0$. Then $y^* A = -\bar\lambda\, y^*$ with $\operatorname{Re}(-\bar\lambda) > 0$ and $y^* B = 0$. That is an uncontrollable mode in the closed right half plane, which contradicts stabilizability. So $X_1$ is invertible.

**Step 4: $P = X_2 X_1^{-1}$ is a symmetric stabilizing solution.** $P$ is real, and $P = X_1^{-T} (X_1^T X_2) X_1^{-1}$ is symmetric by Step 2. The columns of $X X_1^{-1} = \begin{bmatrix} I \\ P \end{bmatrix}$ span the same invariant subspace, and $H \begin{bmatrix} I \\ P \end{bmatrix} = \begin{bmatrix} I \\ P \end{bmatrix} X_1 \Lambda X_1^{-1}$. The first block row says $A - G P = X_1 \Lambda X_1^{-1}$, which is Hurwitz. The second block row says $-Q - A^T P = P (A - G P)$, which is the CARE.

**Step 5: uniqueness.** Let $P_1$ and $P_2$ be stabilizing solutions, and $D = P_1 - P_2$. Subtracting the two equations gives $(A - G P_1)^T D + D (A - G P_2) = 0$. The eigenvalues of $(A - G P_1)^T$ and $A - G P_2$ all have negative real parts, so no two of them sum to 0, and this Sylvester equation has only the solution $D = 0$.

**Step 6: $P \ge 0$.** Write the CARE with $A_c = A - G P$: $A_c^T P + P A_c = -(Q + P G P)$. The right side is negative semidefinite and $A_c$ is Hurwitz, so

$$P = \int_0^\infty e^{A_c^T t} (Q + P G P) e^{A_c t}\, dt \ \ge\ 0.$$

**Step 7: every positive semidefinite solution is stabilizing.** Let $X \ge 0$ solve the CARE, let $A_X = A - G X$, and let $A_X v = \lambda v$ with $v \ne 0$. The CARE in the form $A_X^T X + X A_X = -(Q + X G X)$ gives $2 \operatorname{Re}(\lambda)\, v^* X v = -v^* Q v - v^* X G X v$. If $\operatorname{Re} \lambda \ge 0$, the left side is at least 0 and the right side at most 0, so $Q^{1/2} v = 0$ and $B^T X v = 0$. Then $A v = A_X v + G X v = \lambda v$, an unobservable mode of $(Q^{1/2}, A)$ in the closed right half plane, which detectability forbids. So $A_X$ is Hurwitz, and by Step 5, $X = P$.

**Step 8: $P > 0$ under observability.** If $P v = 0$, the integral of Step 6 gives $\int_0^\infty (|Q^{1/2} e^{A_c t} v|^2 + |R^{-1/2} B^T P e^{A_c t} v|^2)\, dt = 0$. So $B^T P e^{A_c t} v = 0$ for all $t$, hence $x(t) = e^{A_c t} v$ solves $\dot x = A x$, so $x(t) = e^{A t} v$. Also $Q^{1/2} e^{A t} v = 0$ for all $t$. Observability then forces $v = 0$. $\square$

## Consequences

- **Infinite-horizon LQR.** Under the hypotheses, $u = -R^{-1} B^T P x$ is the optimal input for every initial state, the optimal cost is $x_0^T P x_0$, and the closed loop is Hurwitz ([infinite-horizon LQR](/infinite-horizon-lqr/)).
- **The Kalman-Bucy filter.** By duality, if $(C, A)$ is detectable and $(A, W^{1/2})$ is stabilizable, the filter Riccati equation has a unique stabilizing solution, and the steady-state [Kalman-Bucy filter](/kalman-bucy-filter/) has a Hurwitz error dynamics.
- **Solvers.** The Schur method may compute $P = X_2 X_1^{-1}$, because Step 3 makes $X_1$ invertible. A solver that returns a positive semidefinite solution has returned the stabilizing one, by Step 7. The [Kleinman iteration](/kleinman-iteration/) converges to this $P$ from any stabilizing gain.
- **Order.** $P$ is the largest symmetric solution of the CARE. It also bounds the Riccati inequality: if $X$ is symmetric and $\mathcal{R}(X) = A^T X + X A - X G X + Q \ge 0$, then $X \le P$ (proof on the [CARE](/continuous-algebraic-riccati-equation/) page).
- **The sharp condition.** For $Q \ge 0$ and $R > 0$, the stabilizing solution exists if and only if $(A, B)$ is stabilizable and $(Q^{1/2}, A)$ has no unobservable mode on the imaginary axis. Necessity: if $A x = i \omega x$ and $Q x = 0$, then $H \begin{bmatrix} x \\ 0 \end{bmatrix} = i \omega \begin{bmatrix} x \\ 0 \end{bmatrix}$, but the spectrum of $H$ is that of $A - G P$ and its mirror image, which avoids the axis. (The similarity with $\begin{bmatrix} I & 0 \\ P & I \end{bmatrix}$ turns $H$ into $\begin{bmatrix} A - G P & -G \\ 0 & -(A - G P)^T \end{bmatrix}$.) Sufficiency follows from Steps 2 to 6, which use only this weaker condition through Step 1. Detectability is what adds Step 7, the uniqueness among positive semidefinite solutions.
- **A rule of thumb.** When the hypotheses hold only barely, for example with a weakly damped mode that $Q$ hardly sees, $H$ has eigenvalues close to the imaginary axis and $P$ is sensitive to the data.

## Tightness

**Without detectability, positive semidefinite does not mean stabilizing.** Take $a = 1$, $b = r = 1$ and $q = 0$. The CARE $2 p - p^2 = 0$ has the two solutions $p = 0$ and $p = 2$, both positive semidefinite. Only $p = 2$ is stabilizing. Part 4 fails, but a stabilizing solution still exists, because the unobservable mode $+1$ is not on the axis.

**Without detectability, the largest solution may not be stabilizing.** Take $a = 0$, $b = r = 1$ and $q = 0$. The CARE is $-p^2 = 0$, its only (so its largest) solution is $p = 0$, and the closed loop is $0$, not Hurwitz. The unobservable mode $0$ is on the imaginary axis, and $H = \begin{bmatrix} 0 & -1 \\ 0 & 0 \end{bmatrix}$ has the double eigenvalue 0.

**Without stabilizability.** Take $a = 1$, $b = 0$ and $q = r = 1$. The CARE is $2 p + 1 = 0$, so $p = -1/2$. It is not positive semidefinite, and the closed loop is $1$ for every gain.

**$R > 0$ is needed.** With $R$ singular, $R^{-1}$ does not exist, and the problem is a singular (cheap control) problem with a different theory. With $R$ indefinite, $G$ is indefinite, Steps 1 and 6 fail, and the equation is of the H-infinity type.

**Positive definiteness needs observability.** In the first example, $p = 2 > 0$ although $(q^{1/2}, a)$ is not observable, so observability is not necessary for $P > 0$. With $a = -1$, $b = r = 1$ and $q = 0$, the system is detectable but not observable, the CARE $-2 p - p^2 = 0$ has the stabilizing solution $p = 0$, and $P > 0$ fails.

## History

Kalman (1960) treated the infinite-interval regulator under conditions of controllability and observability. Wonham (1968) studied the algebraic equation of stochastic control under weaker conditions. Kučera (1972) gave the result in the form stated here, with stabilizability and detectability, using the eigenvectors of the Hamiltonian matrix. The book of Lancaster and Rodman (1995) collects the theory, including the indefinite case and the discrete equation.

## References
