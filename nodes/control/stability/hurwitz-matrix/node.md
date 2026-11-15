---
tag: BWCSRN
kind: definition
slug: hurwitz-matrix
name: Hurwitz matrix
aliases:
- Hurwitz stable matrix
area: control/stability
level: intro
summary: A square matrix is Hurwitz if every eigenvalue has a negative real part. Then e^(At) decays exponentially, and x' = Ax is globally exponentially stable.
prereqs: [eigenvalue, characteristic-polynomial]
see_also: [routh-hurwitz-criterion, lyapunov-theorem-for-linear-systems, asymptotic-stability, exponential-stability, matrix-exponential, gershgorin-circle-theorem, kharitonov-theorem, jury-stability-test]
sources:
  - paper: doi:10.1007/BF01446812
    title: "A. Hurwitz, Ueber die Bedingungen, unter welchen eine Gleichung nur Wurzeln mit negativen reellen Theilen besitzt, Mathematische Annalen 46, 273-284, 1895"
    locator: the determinant conditions for a polynomial to have only roots with negative real parts
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 4.3, Linear Systems and Linearization (Hurwitz matrices and the Lyapunov equation)
  - book: isbn:9780521467131
    title: Roger A. Horn and Charles R. Johnson, Topics in Matrix Analysis, Cambridge University Press, 1991
    locator: Chapter 2, Stable matrices and inertia (the book says positive stable for eigenvalues in the open right half plane, so A is Hurwitz when -A is positive stable)
---

A real square matrix $A$ is a Hurwitz matrix when every eigenvalue of $A$ has a strictly negative real part. The name comes from Adolf Hurwitz, who gave in 1895 a determinant test for a polynomial to have all its roots in the open left half of the complex plane. The property matters because it is exactly the condition for every solution of the linear differential equation $\dot x = A x$ to decay to zero, and then the decay is exponential. It is tested on the [characteristic polynomial](/characteristic-polynomial/) by the [Routh-Hurwitz criterion](/routh-hurwitz-criterion/), or on the matrix by the [Lyapunov equation](/lyapunov-theorem-for-linear-systems/). The discrete-time analogue is a Schur matrix, with all eigenvalues inside the unit disc.

## Definition

**Definition.** A matrix $A \in \mathbb{R}^{n \times n}$ (or $\mathbb{C}^{n \times n}$) is *Hurwitz* if

$$\operatorname{Re} \lambda < 0 \quad \text{for every eigenvalue } \lambda \text{ of } A .$$

Equivalently, the spectral abscissa $\alpha(A) = \max_i \operatorname{Re} \lambda_i(A)$ is negative. A polynomial is *Hurwitz* if all its roots have negative real parts, so $A$ is Hurwitz if and only if its characteristic polynomial $\det(sI - A)$ is. Some books call such a matrix *stable* or *Hurwitz stable*; this encyclopedia says Hurwitz, because "stable" alone does not say which kind.

**Equivalent conditions.** For $A \in \mathbb{R}^{n \times n}$ these statements are equivalent:

1. $A$ is Hurwitz.
2. $e^{At} \to 0$ as $t \to \infty$.
3. There are $k \ge 1$ and $\lambda > 0$ with $\|e^{At}\| \le k e^{-\lambda t}$ for all $t \ge 0$, in an induced [matrix norm](/matrix-norms/). Every $\lambda < -\alpha(A)$ works with a suitable $k$.
4. The origin of $\dot x = A x$ is [asymptotically stable](/asymptotic-stability/), and then globally [exponentially stable](/exponential-stability/).
5. For some, and then for every, symmetric $Q > 0$, the Lyapunov equation $A^T P + P A = -Q$ has a solution $P > 0$. This is the [Lyapunov theorem for linear systems](/lyapunov-theorem-for-linear-systems/).
6. The characteristic polynomial passes the [Routh-Hurwitz criterion](/routh-hurwitz-criterion/): its Routh array has no sign change and no zero entry in the first column.

Proof of $1 \Rightarrow 3$. Write $A = T J T^{-1}$ in [Jordan normal form](/jordan-normal-form/). Then $e^{At} = T e^{Jt} T^{-1}$, and each entry of $e^{Jt}$ is $0$ or $t^j e^{\mu t} / j!$ for an eigenvalue $\mu$ and some $j < n$. Fix $\lambda$ with $0 < \lambda < -\alpha(A)$. Then $|t^j e^{\mu t}| e^{\lambda t} = t^j e^{(\operatorname{Re} \mu + \lambda) t}$ with $\operatorname{Re} \mu + \lambda < 0$, which is bounded on $t \ge 0$. So $e^{\lambda t} \|e^{Jt}\|$ is bounded, and $k = \|T\|\,\|T^{-1}\| \sup_t e^{\lambda t} \|e^{Jt}\|$ works. $3 \Rightarrow 2$ is clear. $2 \Rightarrow 1$: if $A v = \mu v$ with $v \ne 0$, then $e^{At} v = e^{\mu t} v$, which has norm $e^{t \operatorname{Re} \mu} |v|$; it goes to $0$ only if $\operatorname{Re} \mu < 0$. Statement 4 is statement 3 applied to $x(t) = e^{At} x(0)$. Statements 5 and 6 are proved on their pages. $\blacksquare$

**Necessary conditions that are easy to check.** If $A$ is Hurwitz, then:

- $\operatorname{trace} A < 0$, because the trace is the sum of the eigenvalues, and the sum of the real parts is negative;
- $(-1)^n \det A > 0$, because the determinant is the product of the eigenvalues, the real ones are negative, and the complex ones come in conjugate pairs with positive products $|\mu|^2$;
- every coefficient of $\det(sI - A) = s^n + a_1 s^{n-1} + \dots + a_n$ is positive, because the polynomial is a product of factors $s + r$ with $r > 0$ and $s^2 + 2 \sigma s + \sigma^2 + \omega^2$ with $\sigma > 0$.

For $n = 2$ the first two conditions are also sufficient: $s^2 - (\operatorname{trace} A) s + \det A$ is Hurwitz if and only if both coefficients are positive. For $n \ge 3$ they are not: $s^3 + s^2 + 2s + 8$ has positive coefficients and two roots in the right half plane.

**Sufficient conditions.** If $A$ is symmetric, $A$ is Hurwitz if and only if $-A$ is [positive definite](/positive-definite-matrix/). If $a_{ii} < 0$ and $|a_{ii}| > \sum_{j \ne i} |a_{ij}|$ for each row, every [Gershgorin disc](/gershgorin-circle-theorem/) lies in the open left half plane, so $A$ is Hurwitz. If $A + A^T < 0$, then $A$ is Hurwitz: for $A v = \mu v$ with $|v| = 1$, $2 \operatorname{Re} \mu = v^* (A + A^T) v < 0$.

**Structure of the set.** The Hurwitz matrices form an open subset of $\mathbb{R}^{n \times n}$, because the eigenvalues depend continuously on the entries. The set is not convex, and the sum of two Hurwitz matrices need not be Hurwitz (example below). The distance from a Hurwitz $A$ to the nearest complex matrix with an eigenvalue on the imaginary axis, in the induced 2-norm, is $\min_{\omega \in \mathbb{R}} \sigma_{\min}(A - i \omega I)$. The reason is that $A + E$ has the eigenvalue $i \omega$ exactly when $A - i\omega I + E$ is singular, and the smallest such $E$ has norm $\sigma_{\min}(A - i\omega I)$ by the [singular value decomposition](/singular-value-decomposition/). This distance can be much smaller than $-\alpha(A)$ when $A$ is far from normal.

**Relation to discrete time.** $A$ is Hurwitz if and only if $e^{Ah}$ is Schur for one (and then every) $h > 0$, since the eigenvalues of $e^{Ah}$ are $e^{\lambda h}$ and $|e^{\lambda h}| = e^{h \operatorname{Re} \lambda}$. $A$ is also Hurwitz if and only if $I - A$ is invertible and $(I - A)^{-1} (I + A)$ is Schur: the map $s \mapsto (1 + s)/(1 - s)$ sends the open left half plane onto the open unit disc. This is the [bilinear transform](/bilinear-transform/).

## Examples and non-examples

- **The check matrix.** $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$ has $\det(sI - A) = s^2 + 3s + 2 = (s + 1)(s + 2)$, so the eigenvalues are $-1$ and $-2$, and $A$ is Hurwitz. As the test for $n = 2$ says, $\operatorname{trace} A = -3 < 0$ and $\det A = 2 > 0$. With $Q = I$ the Lyapunov equation gives $P = \begin{bmatrix} 5/4 & 1/4 \\ 1/4 & 1/4 \end{bmatrix} > 0$.
- **Rotation (non-example).** $A = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$ has the eigenvalues $\pm i$. It is not Hurwitz: $e^{At}$ is a rotation and does not decay. The origin of $\dot x = A x$ is only Lyapunov stable.
- **Negative diagonal is not enough (non-example).** $A = \begin{bmatrix} -1 & 4 \\ 1 & -1 \end{bmatrix}$ has $\det A = -3 < 0$, and its eigenvalues are $1$ and $-3$.
- **The sum of Hurwitz matrices.** $A_1 = \begin{bmatrix} -1 & 10 \\ 0 & -1 \end{bmatrix}$ and $A_2 = \begin{bmatrix} -1 & 0 \\ 10 & -1 \end{bmatrix}$ are Hurwitz (both have the double eigenvalue $-1$). Their sum $\begin{bmatrix} -2 & 10 \\ 10 & -2 \end{bmatrix}$ has the eigenvalues $8$ and $-12$, and their average has $4$ and $-6$. So a system that switches between two Hurwitz matrices can diverge; see [common Lyapunov function](/common-lyapunov-function/) and [switched system](/switched-system/).
- **Hurwitz, with a large transient.** For the same $A_1$, $\|e^{A_1 t}\|_2$ rises to $3.716$ near $t = 0.98$ before it decays. Hurwitz says nothing about the size of the transient; the constant $k$ in statement 3 does.
- **Companion form.** The companion matrix of $s^3 + 3s^2 + 2s + K$ is Hurwitz if and only if $0 < K < 6$, by the Routh array (see [Routh-Hurwitz criterion](/routh-hurwitz-criterion/)). At $K = 6$ it has the eigenvalues $\pm i \sqrt{2}$ and $-3$.

## Related definitions

- *Schur matrix*: every eigenvalue has modulus less than 1; the condition for $x_{k+1} = A x_k$. Tested by the [Jury stability test](/jury-stability-test/) or the [Schur-Cohn test](/schur-cohn-test/) on the characteristic polynomial.
- *Hurwitz polynomial*: a polynomial with all roots in the open left half plane; see [Routh-Hurwitz criterion](/routh-hurwitz-criterion/) and [Routh array](/routh-array/).
- *Hurwitz matrix of a polynomial*: a different object with the same name. For $a_0 s^n + a_1 s^{n-1} + \dots + a_n$ it is the $n \times n$ matrix with the entries $a_{2j - i}$ (zero outside $0 \dots n$), whose leading principal minors are the Hurwitz determinants. It is defined on [Routh-Hurwitz criterion](/routh-hurwitz-criterion/).
- [Kharitonov's theorem](/kharitonov-theorem/): a test for a whole family of characteristic polynomials with interval coefficients.
- [Quadratic stability](/quadratic-stability/): one $P > 0$ works for a whole set of matrices.

## References
