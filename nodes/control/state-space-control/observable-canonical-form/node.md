---
tag: 6MHF8K
kind: definition
slug: observable-canonical-form
name: Observable canonical form
aliases:
- observer canonical form
area: control/state-space-control
level: core
summary: The dual of the controllable canonical form, in which the output map is a unit vector and the coefficients appear in one column.
prereqs: [controllable-canonical-form, observability]
see_also: [controllable-canonical-form, luenberger-observer, state-observer, realization-problem, minimal-realization, markov-parameters, kalman-rank-condition, root-conditioning]
sources:
  - paper: doi:10.1109/TAC.1967.1098584
    title: David G. Luenberger, Canonical forms for linear multivariable systems, IEEE Transactions on Automatic Control 12(3), 290-293, 1967
    locator: canonical forms for multi-output systems, built from the observability indices by duality
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 4.4 (realizations of a proper rational transfer function) and Section 7.5 (realizations from Markov parameters)
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Section 3.4, Pole Placement and Canonical Forms
  - book: isbn:9780135369616
    title: Thomas Kailath, Linear Systems, Prentice Hall, 1980
    locator: the observer canonical form of a scalar transfer function and its relation to the other canonical realizations
---

The observable canonical form is a state-space model of a single-output system in which $C$ is the last unit row vector and $A$ is a companion matrix with the coefficients of the characteristic polynomial in its last column. It is the transpose of the [controllable canonical form](/controllable-canonical-form/): $A$ and $C$ here are $A^T$ and $B^T$ there, and $B$ here holds the numerator coefficients. Every observable single-output pair $(C, A)$ can be brought to this form, and in it the design of an observer gain is a matter of matching coefficients.

## Definition

**Notation.** As on the controllable canonical form page,

$$G(s) = \frac{b_1 s^{n-1} + b_2 s^{n-2} + \dots + b_n}{s^n + a_1 s^{n-1} + \dots + a_n} + d .$$

**Definition.** The *observable canonical form* of $G$ is

$$A = \begin{bmatrix} 0 & 0 & \cdots & 0 & -a_n \\ 1 & 0 & \cdots & 0 & -a_{n-1} \\ 0 & 1 & \cdots & 0 & -a_{n-2} \\ \vdots & & \ddots & & \vdots \\ 0 & 0 & \cdots & 1 & -a_1 \end{bmatrix}, \quad B = \begin{bmatrix} b_n \\ b_{n-1} \\ \vdots \\ b_1 \end{bmatrix}, \quad C = \begin{bmatrix} 0 & \cdots & 0 & 1 \end{bmatrix}, \quad D = d .$$

**Why it realizes $G$.** If $(A_c, B_c, C_c, d)$ is the controllable canonical form, this one is $(A_c^T, C_c^T, B_c^T, d)$. A scalar transfer function equals its transpose, so $C (sI - A)^{-1} B + d = \bigl(C_c (sI - A_c)^{-1} B_c\bigr)^T + d = G(s)$. A direct reading also works: the rows give $\dot z_1 = -a_n z_n + b_n u$ and $\dot z_k = z_{k-1} - a_{n-k+1} z_n + b_{n-k+1} u$, with $y = z_n + d u$. Eliminating $z_1, \dots, z_{n-1}$ gives $a(s) (Y - dU) = b(s) U$. The input enters each integrator of a chain, which is why the form is drawn as nested integrators with feedback from the output.

**Properties.** They are the transposes of those of the controllable form.

- The characteristic polynomial of $A$ is $a(s) = s^n + a_1 s^{n-1} + \dots + a_n$.
- $(C, A)$ is always observable: the observability matrix has ones on the antidiagonal and zeros above it.
- $(A, B)$ is controllable if and only if $a(s)$ and $b(s)$ have no common root.

**Transformation to the form.** Let $(c, A)$ be an observable single-output pair with characteristic polynomial $s^n + a_1 s^{n-1} + \dots + a_n$, let $O = [c; cA; \dots; cA^{n-1}]$ be its observability matrix and $W$ the symmetric matrix of coefficients from the controllable form page. The coordinates $z = W O x$ give $W O A (W O)^{-1}$ in observable canonical form and $c (W O)^{-1} = [0, \dots, 0, 1]$. This is the controllable case applied to $(A^T, c^T)$ and transposed back.

**Use in observer design.** For the observer error matrix $A - L C$ with $L = (l_1, \dots, l_n)^T$, only the last column changes, since $L C$ is $L$ placed in the last column. That column becomes $(-(a_n + l_1), \dots, -(a_1 + l_n))^T$, so the characteristic polynomial of $A - L C$ is $s^n + (a_1 + l_n) s^{n-1} + \dots + (a_n + l_1)$. To get the polynomial $s^n + \alpha_1 s^{n-1} + \dots + \alpha_n$, take $l_{n + 1 - i} = \alpha_i - a_i$. In the original coordinates the gain is $(W O)^{-1} L$. This is the dual of single-input pole placement, used for the [Luenberger observer](/luenberger-observer/).

**The observability form, a variant.** Another companion realization keeps the $A$ of the controllable form, takes $C = e_1^T$, and puts the first $n$ [Markov parameters](/markov-parameters/) $h_1, \dots, h_n$ of $G(s) - d = \sum_{k \ge 1} h_k s^{-k}$ in $B$. Its states are $y$ and its first $n - 1$ derivatives when $u = 0$. Some books call this one the observable form, so the matrices, not the name, fix the meaning. Some books also reverse the state order, which puts the coefficients in the first column and makes $C = e_1^T$.

**Multi-output systems.** For $p > 1$ outputs, Luenberger (1967) built a block companion form from the observability indices $\nu_1, \dots, \nu_p$, with $\nu_1 + \dots + \nu_p = n$, by the dual of the multi-input construction.

**Numerical caution.** As with the controllable form, the coefficients can be badly conditioned functions of the eigenvalues ([root conditioning](/root-conditioning/)), and $W O$ inherits the conditioning of the observability matrix. The form is for proofs and small examples.

## Examples and non-examples

- **A two-state example.** $G(s) = (s + 3)/(s^2 + 3 s + 2)$ gives $A = \begin{bmatrix} 0 & -2 \\ 1 & -3 \end{bmatrix}$, $B = (3, 1)^T$, $C = [0, 1]$. Check: $C (sI - A)^{-1} = [1, s] / (s^2 + 3 s + 2)$, and $[1, s] (3, 1)^T = s + 3$.
- **Transforming a diagonal pair.** $A = \operatorname{diag}(-1, -2)$, $c = [1, 1]$, $b = (1, -1)^T$, so $G(s) = 1/(s + 1) - 1/(s + 2) = 1/(s^2 + 3 s + 2)$. Here $O = \begin{bmatrix} 1 & 1 \\ -1 & -2 \end{bmatrix}$, $W = \begin{bmatrix} 3 & 1 \\ 1 & 0 \end{bmatrix}$, and $W O = \begin{bmatrix} 2 & 1 \\ 1 & 1 \end{bmatrix}$ with inverse $\begin{bmatrix} 1 & -1 \\ -1 & 2 \end{bmatrix}$. Then $W O A (W O)^{-1} = \begin{bmatrix} 0 & -2 \\ 1 & -3 \end{bmatrix}$, $c (W O)^{-1} = [0, 1]$ and $W O b = (1, 0)^T$, which is $(b_2, b_1)^T$ for the numerator $0 \cdot s + 1$.
- **The observability form.** For $G(s) = (s + 3)/(s^2 + 3 s + 2)$ the Markov parameters are $h_1 = 1$ and $h_2 = 0$, from $G(s) = s^{-1} + 0 \cdot s^{-2} - 2 s^{-3} + \dots$. With $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $B = (1, 0)^T$ and $C = [1, 0]$, $C (sI - A)^{-1} B = (s + 3)/(s^2 + 3 s + 2)$.
- **A form that is not minimal.** $G(s) = (s + 1)/(s^2 + 3 s + 2)$ gives $B = (1, 1)^T$ with the same $A$ and $C$. Then $A B = (-2, -2)^T$, so $[B, AB] = \begin{bmatrix} 1 & -2 \\ 1 & -2 \end{bmatrix}$ has rank 1, and the pair $(A, B)$ is not controllable. The factor $s + 1$ cancels.
- **No form for an unobservable pair (non-example).** The double integrator with velocity measured, $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$ and $c = [0, 1]$, has $O = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, which is singular. Every pair in observable canonical form is observable, so no change of coordinates brings this pair to the form.

## Related definitions

- [Controllable canonical form](/controllable-canonical-form/): the dual form.
- [Observability](/observability/): exactly the single-output pairs that have this form.
- [Luenberger observer](/luenberger-observer/) and [state observer](/state-observer/): the main use of the form.
- [Markov parameters](/markov-parameters/): the coefficients that appear in $B$ in the observability form variant.
- [Realization problem](/realization-problem/): the form is a direct answer for scalar transfer functions, and its block version gives a realization of order $p r$ for a $p \times m$ transfer matrix whose entries have the common denominator degree $r$.
- [Minimal realization](/minimal-realization/): the form is minimal exactly when the transfer function has no cancellation.

## References
