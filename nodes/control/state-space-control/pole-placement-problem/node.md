---
tag: GNBVAT
kind: problem
slug: pole-placement-problem
name: Pole placement problem
aliases:
- eigenvalue assignment problem
- pole assignment
area: control/state-space-control
level: core
summary: Given (A, B) and a set of desired eigenvalues, find a gain K such that A - BK has exactly those eigenvalues.
prereqs: [controllability, state-space-representation, eigenvalue]
see_also: [pole-placement-theorem, ackermann-formula, robust-pole-placement, state-feedback, deadbeat-control, luenberger-observer, kalman-decomposition, sylvester-equation]
sources:
  - paper: doi:10.1109/TAC.1967.1098739
    title: W. M. Wonham, On pole assignment in multi-input controllable linear systems, IEEE Transactions on Automatic Control 12(6), 660-665, 1967
    locator: the solvability of the problem for every spectrum if and only if the pair is controllable
  - paper: doi:10.1080/0020718508961188
    title: Jaroslav Kautsky, Nancy K. Nichols and Paul Van Dooren, Robust pole assignment in linear state feedback, International Journal of Control 41(5), 1129-1155, 1985
    locator: the set of all solutions in the multi-input case, parametrized by the closed-loop eigenvectors, and the choice of a well conditioned one
  - paper: "Volker Mehrmann and Hongguo Xu, An analysis of the pole placement problem I. The single-input case, Electronic Transactions on Numerical Analysis 4, 89-105, 1996"
    locator: the conditioning of the single-input problem
  - paper: "Volker Mehrmann and Hongguo Xu, An analysis of the pole placement problem II. The multi-input case, Electronic Transactions on Numerical Analysis 5, 77-97, 1997"
    locator: the conditioning of the multi-input problem
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 8.2 (the single-input case), Section 8.4 (the dual observer problem) and Section 8.6 (the multivariable case)
---

The pole placement problem asks for a state feedback gain that gives the closed loop a chosen set of eigenvalues. It is the computational core of [state feedback](/state-feedback/) design and, by duality, of observer design. This page states the problem and its variants. The [pole placement theorem](/pole-placement-theorem/) says when it can be solved. [Ackermann's formula](/ackermann-formula/) is an exact solution method for one input. [Robust pole placement](/robust-pole-placement/) uses the freedom that several inputs give to pick a solution whose eigenvalues are insensitive to errors.

## In plain words

A linear system has natural modes, given by the eigenvalues of its matrix. They decide how fast it settles and whether it oscillates or diverges. Feeding the state back to the input changes the matrix and so changes the modes. The problem is to choose the feedback weights so that the new modes are exactly the ones the designer wants. It can be solved for every wanted set if the input can steer every part of the system. With more than one input there are many solutions, and some are much better than others.

## Definition

**Input:** a matrix $A \in \mathbb{R}^{n \times n}$, a matrix $B \in \mathbb{R}^{n \times m}$, and a list $\Lambda = (\lambda_1, \dots, \lambda_n)$ of complex numbers that is closed under complex conjugation, with multiplicities. Equivalently, a monic real polynomial $\alpha(s) = \prod_i (s - \lambda_i)$ of degree $n$.

**Output:** a matrix $K \in \mathbb{R}^{m \times n}$ with

$$\det(sI - A + BK) = \alpha(s),$$

or the answer that no such $K$ exists.

The condition on $\Lambda$ is needed because $A - BK$ is real, so its non-real eigenvalues come in conjugate pairs. For a real $K$ the problem asks for the characteristic polynomial, not for the Jordan structure. With $m = 1$ the solution is unique when it exists. With $m > 1$ the solutions form a set with $n(m - 1)$ free parameters for a generic choice of distinct eigenvalues.

**Solvability.** Let the [Kalman decomposition](/kalman-decomposition/) split the state into a controllable part of dimension $n_c$ and an uncontrollable part with characteristic polynomial $\chi_u(s)$ of degree $n - n_c$. Then $\det(sI - A + BK) = \chi_u(s)\,\beta(s)$, where $\beta$ ranges over all monic real polynomials of degree $n_c$ as $K$ varies. So the problem has a solution if and only if $\chi_u$ divides $\alpha$. In particular it has a solution for every $\alpha$ if and only if $(A, B)$ is [controllable](/controllability/). That is the pole placement theorem.

## Variants

- **Observer gain.** Find $L$ with $\det(sI - A + LC) = \alpha(s)$. Since $\det(sI - A + LC) = \det(sI - A^T + C^T L^T)$, this is the problem for the pair $(A^T, C^T)$, and it is solvable for every $\alpha$ if and only if $(C, A)$ is [observable](/observability/). The [Luenberger observer](/luenberger-observer/) uses it.
- **Discrete time.** The same algebra with $\Phi - \Gamma K$. Choosing $\alpha(z) = z^n$ gives [deadbeat control](/deadbeat-control/).
- **Robust pole placement.** Among all solutions, find one whose closed-loop eigenvector matrix is well conditioned, so that the eigenvalues move little under perturbations of $A$, $B$ and $K$.
- **Eigenstructure assignment.** Assign the eigenvalues and also the eigenvectors, within the subspaces that $B$ allows. This is used to decouple modes from some outputs.
- **Partial pole placement.** Move only some eigenvalues of $A$, for example the unstable ones, and keep the others.
- **Regional placement.** Ask only that all eigenvalues lie in a region, such as a sector and a half plane that give a minimum damping and a minimum decay rate. This is a convex problem in suitable variables and is usually solved with linear matrix inequalities.
- **Static output feedback.** Find $K$ with $u = -Ky$. The eigenvalues can then not be placed freely in general, and the problem is much harder than with state feedback. No simple necessary and sufficient condition is known.

## Examples

**One input.** $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, $\Lambda = (-1 + i, -1 - i)$. Then $\det(sI - A + BK) = s^2 + k_2 s + k_1$ must equal $s^2 + 2s + 2$, so the unique solution is $K = [2, 2]$.

**Two inputs, many solutions.** $A = 0 \in \mathbb{R}^{2 \times 2}$, $B = I$, $\Lambda = (-1, -2)$. Then $A - BK = -K$, so every $K$ with eigenvalues 1 and 2 solves the problem, for example $K = \begin{bmatrix} 1 & t \\ 0 & 2 \end{bmatrix}$ for every real $t$. As $|t|$ grows, the eigenvector matrix of $-K$ gets worse conditioned: for $t = 100$ a perturbation of size $10^{-4}$ in one entry moves the eigenvalues by about $10^{-2}$. The choice $t = 0$ gives orthogonal eigenvectors.

**Not controllable, but solvable.** $A = \begin{bmatrix} -1 & 0 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$. Here $A - BK = \begin{bmatrix} -1 & 0 \\ -k_1 & -k_2 \end{bmatrix}$ has the eigenvalues $-1$ and $-k_2$. The list $(-1, -3)$ is reached with $k_2 = 3$ and any $k_1$. The list $(-2, -3)$ is not reached by any $K$, because $\chi_u(s) = s + 1$ does not divide $(s + 2)(s + 3)$.

## Known algorithms

- **Canonical form (Bass-Gura type).** For one input and a controllable pair, transform to [controllable canonical form](/controllable-canonical-form/), where $K$ is read off from the difference of the coefficients of $\alpha$ and of $\det(sI - A)$, and transform back.
- **[Ackermann's formula](/ackermann-formula/).** For one input, $K = e_n^T W^{-1} \alpha(A)$ with the controllability matrix $W = [B, AB, \dots, A^{n-1}B]$. It is exact in rational arithmetic but numerically unstable for larger $n$.
- **Reduction to one input.** If $(A, B)$ is controllable, there are $F$ and a column $b = Bg$ with $(A + BF, b)$ controllable (Heymann's lemma). Placing the eigenvalues for $(A + BF, b)$ solves the problem. The observer pages of this area use this construction.
- **Sylvester equation method.** Choose a matrix $\Lambda_d$ with the wanted spectrum and a matrix $G$, solve the [Sylvester equation](/sylvester-equation/) $AX - X\Lambda_d = BG$, and set $K = GX^{-1}$ when $X$ is invertible. Then $(A - BK)X = X\Lambda_d$.
- **Robust methods.** The method of Kautsky, Nichols and Van Dooren chooses the eigenvectors one at a time from the subspaces that $B$ allows, to make the eigenvector matrix as close to orthogonal as possible. See [robust pole placement](/robust-pole-placement/).
- **Orthogonal reduction.** Methods that first reduce $(A, B)$ to a staircase or Hessenberg form with orthogonal transformations avoid the controllability matrix and are the numerically preferred way for larger $n$.

## Bounds

In exact arithmetic the problem is solved with a polynomial number of operations. The implementation on the Ackermann page uses $O(n^4)$ operations, and orthogonal reduction methods use $O(n^3)$ for a fixed number of inputs. Reading $A$ alone needs $\Omega(n^2)$ operations.

The real limit is numerical. Mehrmann and Xu analyzed the condition of the problem for one input (1996) and for several inputs (1997). Their results show that pole placement is often ill conditioned, that the conditioning tends to get worse quickly as $n$ grows, and that a bad choice of eigenvalues makes it worse. A gain computed in floating point can therefore give eigenvalues that are far from the wanted ones, even with a backward stable algorithm. Check the computed eigenvalues of $A - BK$ every time.

## Reductions

- **Observer design to pole placement.** By duality, as above.
- **Multi-input to single-input.** By Heymann's lemma.
- **Pole placement to a linear system.** For fixed $m = 1$, the coefficients of $\det(sI - A + BK)$ are affine in $K$, so solving for $K$ is a linear system with the matrix $W$ times a triangular Toeplitz matrix. This is why the problem is solvable for every $\alpha$ exactly when $W$ is invertible.
- **Stabilization to pole placement.** A pair is [stabilizable](/stabilizability/) if and only if the problem has a solution for some $\alpha$ with all roots in the open left half plane.

## Applications

- Design of [state feedback](/state-feedback/) from time-domain specifications, such as settling time and damping.
- Design of observer gains for the [Luenberger observer](/luenberger-observer/), the [reduced-order observer](/reduced-order-observer/) and the [unknown input observer](/unknown-input-observer/).
- [Deadbeat control](/deadbeat-control/) in discrete time.
- [State feedback with integral action](/integral-state-feedback/), where the eigenvalues of the augmented system are placed.

## References
