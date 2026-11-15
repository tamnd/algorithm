---
tag: N353PN
kind: definition
slug: controllable-canonical-form
name: Controllable canonical form
aliases:
- controller canonical form
- phase-variable form
area: control/state-space-control
level: core
summary: A state-space form of a single-input system with a companion matrix whose last row holds the coefficients of the characteristic polynomial.
prereqs: [controllability, kalman-rank-condition, characteristic-polynomial]
see_also: [observable-canonical-form, pole-placement-theorem, ackermann-formula, realization-problem, minimal-realization, rational-canonical-form, root-conditioning, robust-pole-placement]
sources:
  - paper: doi:10.1109/TAC.1967.1098584
    title: David G. Luenberger, Canonical forms for linear multivariable systems, IEEE Transactions on Automatic Control 12(3), 290-293, 1967
    locator: canonical forms for controllable multi-input pairs, built from the controllability indices
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 4.4 (realizations of a proper rational transfer function in companion form)
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Section 3.4, Pole Placement and Canonical Forms
  - book: isbn:9780135369616
    title: Thomas Kailath, Linear Systems, Prentice Hall, 1980
    locator: the controller canonical form of a scalar transfer function and its relation to the other canonical realizations
---

The controllable canonical form is a state-space model of a single-input system in which $A$ is a companion matrix, with the coefficients of the characteristic polynomial in its last row, and $B$ is the last unit vector. Every controllable single-input pair $(A, b)$ can be brought to this form by a change of coordinates, and the form can be written down directly from a transfer function. It makes state feedback design a matter of matching coefficients. The dual form, with the coefficients in a column and the output as a unit vector, is the [observable canonical form](/observable-canonical-form/).

## Definition

**Notation.** A single-input single-output transfer function of order $n$ is written

$$G(s) = \frac{b_1 s^{n-1} + b_2 s^{n-2} + \dots + b_n}{s^n + a_1 s^{n-1} + \dots + a_n} + d .$$

Any proper rational function can be put in this form, with $d = \lim_{s \to \infty} G(s)$.

**Definition.** The *controllable canonical form* of $G$ is

$$A = \begin{bmatrix} 0 & 1 & 0 & \cdots & 0 \\ 0 & 0 & 1 & \cdots & 0 \\ \vdots & & & \ddots & \vdots \\ 0 & 0 & 0 & \cdots & 1 \\ -a_n & -a_{n-1} & -a_{n-2} & \cdots & -a_1 \end{bmatrix}, \quad B = \begin{bmatrix} 0 \\ 0 \\ \vdots \\ 0 \\ 1 \end{bmatrix}, \quad C = \begin{bmatrix} b_n & b_{n-1} & \cdots & b_1 \end{bmatrix}, \quad D = d .$$

**Why it realizes $G$.** The first $n - 1$ rows say $\dot z_k = z_{k+1}$, so $z_k = z_1^{(k-1)}$; the states are $z_1$ and its derivatives, which is the reason for the name phase-variable form. The last row says

$$z_1^{(n)} + a_1 z_1^{(n-1)} + \dots + a_n z_1 = u ,$$

so $Z_1(s) = U(s)/a(s)$ with $a(s) = s^n + a_1 s^{n-1} + \dots + a_n$. The output is $y = b_n z_1 + b_{n-1} \dot z_1 + \dots + b_1 z_1^{(n-1)} + d u$, so $Y(s) = (b(s)/a(s) + d)\, U(s)$ with $b(s) = b_1 s^{n-1} + \dots + b_n$.

**Properties.**

- The characteristic polynomial of $A$ is $a(s)$.
- The pair $(A, B)$ is always controllable. The controllability matrix $[B, AB, \dots, A^{n-1} B]$ has ones on the antidiagonal and zeros above it, so its determinant is $\pm 1$.
- The pair $(C, A)$ is observable if and only if $a(s)$ and $b(s)$ have no common root. So the form is a [minimal realization](/minimal-realization/) exactly when $G = b/a$ is in lowest terms.

**Transformation to the form.** Let $(A, b)$ be any controllable single-input pair with characteristic polynomial $s^n + a_1 s^{n-1} + \dots + a_n$. Let $M = [b, Ab, \dots, A^{n-1} b]$ and

$$W = \begin{bmatrix} a_{n-1} & a_{n-2} & \cdots & a_1 & 1 \\ a_{n-2} & a_{n-3} & \cdots & 1 & 0 \\ \vdots & & & & \vdots \\ a_1 & 1 & \cdots & 0 & 0 \\ 1 & 0 & \cdots & 0 & 0 \end{bmatrix}.$$

The coordinates $z$ with $x = M W z$ give $(W^{-1} M^{-1} A M W, W^{-1} M^{-1} b)$ in controllable canonical form, and the output matrix becomes $C M W$. Two controllable single-input pairs with the same characteristic polynomial are therefore similar, and the form is unique for each such polynomial.

**Use in pole placement.** In the canonical coordinates, the feedback $u = -K z$ with $K = [k_1, \dots, k_n]$ changes only the last row, which becomes $[-(a_n + k_1), \dots, -(a_1 + k_n)]$. The closed loop characteristic polynomial is $s^n + (a_1 + k_n) s^{n-1} + \dots + (a_n + k_1)$. To get a desired polynomial $s^n + \alpha_1 s^{n-1} + \dots + \alpha_n$, take $k_{n + 1 - i} = \alpha_i - a_i$. The gain in the original coordinates is $K (M W)^{-1}$. This is the proof of the single-input [pole placement theorem](/pole-placement-theorem/), and written out it is the [Ackermann formula](/ackermann-formula/).

**Numerical caution.** The form is a tool for proofs and small examples, not for computing. The coefficients $a_i$ can be very sensitive to the eigenvalues and the reverse, as for the [Wilkinson polynomial](/wilkinson-polynomial/); see [root conditioning](/root-conditioning/). The transformation $M W$ inherits the conditioning of the controllability matrix $M$, which for $A = \operatorname{diag}(-1, \dots, -10)$ and $b$ the vector of ones has a condition number near $2 \times 10^{12}$. Numerical pole placement uses orthogonal transformations instead; see [robust pole placement](/robust-pole-placement/).

**Conventions.** Books differ in the order of the states. Some put the coefficients $-a_1, \dots, -a_n$ in the first row and take $B = e_1$; Kailath (1980) calls a form of this kind the controller canonical form. The two orders are related by the permutation that reverses the states. The names "controllable", "controller" and "phase-variable" are also used for slightly different forms in different books, so the matrices, not the name, fix the meaning.

**Multi-input systems.** A controllable pair with $m > 1$ inputs has no single companion form. Luenberger (1967) chose basis vectors $b_j, A b_j, \dots, A^{\mu_j - 1} b_j$ by the controllability indices $\mu_1, \dots, \mu_m$, with $\mu_1 + \dots + \mu_m = n$. In these coordinates $A$ is block companion with diagonal blocks of sizes $\mu_j$ and $B$ is nearly a selection of unit vectors. The indices, but not all the coefficients, are invariant under changes of state and input coordinates.

## Examples and non-examples

- **A two-state example.** $G(s) = (s + 3)/(s^2 + 3 s + 2)$ has $a_1 = 3$, $a_2 = 2$, $b_1 = 1$ and $b_2 = 3$. Its form is $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $B = (0, 1)^T$, $C = [3, 1]$, $D = 0$. Check: $C (sI - A)^{-1} B = (3 + s)/(s^2 + 3 s + 2)$, since $(sI - A)^{-1} B = (1, s)^T / (s^2 + 3 s + 2)$.
- **Transforming a diagonal pair.** $A = \operatorname{diag}(-1, -2)$, $b = (1, 1)^T$. The characteristic polynomial is $s^2 + 3 s + 2$, $M = \begin{bmatrix} 1 & -1 \\ 1 & -2 \end{bmatrix}$ and $W = \begin{bmatrix} 3 & 1 \\ 1 & 0 \end{bmatrix}$, so $M W = \begin{bmatrix} 2 & 1 \\ 1 & 1 \end{bmatrix}$ with inverse $\begin{bmatrix} 1 & -1 \\ -1 & 2 \end{bmatrix}$. Then $(M W)^{-1} A M W = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$ and $(M W)^{-1} b = (0, 1)^T$.
- **Pole placement on the double integrator.** $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = (0, 1)^T$ is already in the form with $a_1 = a_2 = 0$. For the closed loop polynomial $s^2 + 2 s + 1$, $k_2 = 2$ and $k_1 = 1$, so $K = [1, 2]$.
- **A form that is not minimal.** $G(s) = (s + 1)/(s^2 + 3 s + 2)$ gives the same $A$ and $B$ with $C = [1, 1]$. The pair is controllable but not observable: $C A = [-2, -2]$. The common factor $s + 1$ cancels, and the minimal order is 1.
- **No form for an uncontrollable pair (non-example).** $A = -I_2$, $b = (1, 1)^T$: $M = \begin{bmatrix} 1 & -1 \\ 1 & -1 \end{bmatrix}$ is singular. Every pair in controllable canonical form is controllable, and controllability does not change under a change of coordinates, so no $T$ exists.

## Related definitions

- [Observable canonical form](/observable-canonical-form/): the dual form, obtained by transposing this one.
- [Rational canonical form](/rational-canonical-form/): the companion form of a single matrix in linear algebra, without $B$ and $C$.
- [Controllability](/controllability/): exactly the single-input pairs that have this form.
- [Pole placement theorem](/pole-placement-theorem/) and [Ackermann formula](/ackermann-formula/): the main use of the form.
- [Realization problem](/realization-problem/): the form is a direct answer for scalar transfer functions.
- [Minimal realization](/minimal-realization/): the form is minimal exactly when the transfer function has no cancellation.

## References
