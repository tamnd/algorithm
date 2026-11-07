---
tag: 52RXJY
kind: definition
slug: residual
name: Residual
aliases:
- residual vector r = b - Ax
- residual vector
- normwise backward error
area: numerical/linear-systems
level: intro
summary: The vector r = b - A x̂, which measures how far an approximate solution is from satisfying A x = b, and which iterative methods drive to zero.
prereqs: [matrix-norms, condition-number]
see_also: [backward-error-analysis, iterative-refinement, linear-system-solving, conjugate-gradient-method, gmres, least-squares-problem, hilbert-matrix, krylov-subspace]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 7, Perturbation Theory for Linear Systems (Theorem 7.1, the Rigal and Gaches normwise backward error; Theorem 7.3, the Oettli and Prager componentwise backward error; Section 7.2); Chapter 12, Iterative Refinement (Section 12.1, the error in the computed residual); Section 17.5, Stopping an Iterative Method
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 2.6, The Sensitivity of Square Systems; Section 3.5, Improving and Estimating Accuracy (residuals and iterative improvement)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Chapter 2, Linear Equation Solving (Section 2.4.1, the residual and the backward error; Section 2.5, improving the accuracy of a solution)
  - paper: "J. L. Rigal and J. Gaches, On the compatibility of a given solution with the data of a linear system, Journal of the ACM 14(3), 1967"
    locator: pp. 543 to 548 (the normwise backward error formula)
  - paper: "W. Oettli and W. Prager, Compatibility of approximate solution of linear equations with given error bounds for coefficients and right-hand sides, Numerische Mathematik 6, 1964"
    locator: pp. 405 to 409 (the componentwise backward error formula)
---

The residual of an approximate solution $\hat x$ of a linear system $A x = b$ is the vector $r = b - A \hat x$. It is zero exactly when $\hat x$ solves the system, it costs one matrix-vector product to compute, and, divided by the right scale, it is exactly the smallest relative change in the data $A$ and $b$ that makes $\hat x$ an exact solution: the [backward error](/backward-error-analysis/) of $\hat x$. A small residual does not mean a small error in $\hat x$; the two are linked by the [condition number](/condition-number/). Iterative methods produce residuals $r_k = b - A x_k$ and stop when they are small enough.

## Definition

**Notation.** $A$ is an $n \times n$ real matrix, $b \in \mathbb{R}^n$, $x$ is the exact solution of $A x = b$, $\hat x$ is a computed or approximate solution, $\|\cdot\|$ is a vector norm with its induced [matrix norm](/matrix-norms/), $\kappa(A) = \|A\|\,\|A^{-1}\|$, and $u$ is the unit roundoff ($2^{-53}$ in binary64). For an iterative method, $x_k$ is the $k$-th iterate.

The *residual* of $\hat x$ is

$$r = b - A \hat x, \qquad r_k = b - A x_k \text{ for an iterate.}$$

The *error* is $e = x - \hat x$. The two are related by the *residual equation*

$$A e = r, \qquad \text{so} \qquad e = A^{-1} r \text{ when } A \text{ is nonsingular.}$$

For a rectangular $A \in \mathbb{R}^{m \times n}$ the residual $r = b - A \hat x$ is defined in the same way; at the least squares solution it is not zero but satisfies $A^T r = 0$.

**The normwise backward error (Rigal and Gaches).** For $\hat x \ne 0$ or $b \ne 0$,

$$\eta(\hat x) = \min\{\varepsilon : (A + \Delta A)\hat x = b + \Delta b,\ \|\Delta A\| \le \varepsilon \|A\|,\ \|\Delta b\| \le \varepsilon \|b\|\} = \frac{\|r\|}{\|A\|\,\|\hat x\| + \|b\|}.$$

*Proof for the 2-norm* (Higham, Theorem 7.1, gives each induced norm). If $(A + \Delta A)\hat x = b + \Delta b$ with the two bounds, then $r = \Delta A\, \hat x - \Delta b$, so $\|r\| \le \varepsilon(\|A\|\,\|\hat x\| + \|b\|)$, and $\varepsilon \ge \eta$. Conversely, let $\eta$ be the quotient, and set

$$\Delta A = \frac{\|A\|_2\, \|\hat x\|_2}{\|A\|_2 \|\hat x\|_2 + \|b\|_2} \cdot \frac{r\, \hat x^T}{\|\hat x\|_2^2}, \qquad \Delta b = -\frac{\|b\|_2}{\|A\|_2 \|\hat x\|_2 + \|b\|_2}\, r$$

(drop $\Delta A$ when $\hat x = 0$). Then $\Delta A\, \hat x - \Delta b = r$, which is $(A + \Delta A)\hat x = b + \Delta b$, and $\|\Delta A\|_2 = \eta \|A\|_2$, $\|\Delta b\|_2 = \eta \|b\|_2$, because $\|r \hat x^T\|_2 = \|r\|_2 \|\hat x\|_2$. So the minimum is attained at $\eta$. $\square$

When only $A$ is perturbed ($\Delta b = 0$), the same argument gives $\|r\|/(\|A\|\,\|\hat x\|)$.

**The componentwise backward error (Oettli and Prager).** With perturbations measured entry by entry,

$$\omega(\hat x) = \min\{\varepsilon : (A + \Delta A)\hat x = b + \Delta b,\ |\Delta A| \le \varepsilon |A|,\ |\Delta b| \le \varepsilon |b|\} = \max_i \frac{|r_i|}{(|A|\,|\hat x| + |b|)_i},$$

with $0/0$ read as $0$ and $\xi/0$, $\xi \ne 0$, read as $\infty$ (Higham, Theorem 7.3).

**From the residual to the error.** From $e = A^{-1} r$ and $\|b\| \le \|A\|\,\|x\|$,

$$\frac{\|x - \hat x\|}{\|x\|} \le \kappa(A) \frac{\|r\|}{\|b\|}, \qquad \frac{\|r\|}{\|A\|\,\|x\|} \le \frac{\|x - \hat x\|}{\|x\|}.$$

Both bounds are exact inequalities for $b \ne 0$, with no assumption on how $\hat x$ was found. The first is attained for some $b$ and $r$ ($r$ along a direction where $\|A^{-1} r\| = \|A^{-1}\|\,\|r\|$, and $b$ with $\|b\| = \|A\|\,\|x\|$). In terms of the backward error, to first order, $\|x - \hat x\|/\|x\| \lesssim 2\kappa(A)\,\eta(\hat x)$ (Higham, Theorem 7.2, gives the exact form).

**The computed residual.** In floating point the residual itself has an error. Under the [standard model](/floating-point-model/), the residual $\hat r = \mathrm{fl}(b - A\hat x)$ computed in working precision satisfies

$$|\hat r - r| \le \gamma_{n+1}(|A|\,|\hat x| + |b|), \qquad \gamma_{n+1} = \frac{(n+1)u}{1 - (n+1)u},$$

because each component is a dot product of length $n + 1$ (Higham, Section 12.1). So the computed residual of a backward stable solution, whose true residual is already of order $u(|A||\hat x| + |b|)$, may have no correct digits. This is why [iterative refinement](/iterative-refinement/) for a better forward error computes $r$ in higher precision.

## Examples and non-examples

**A small residual and a large error.** Let $A = \begin{pmatrix} 1 & 1 \\ 1 & 1.0001 \end{pmatrix}$ and $b = (2, 2.0001)^T$, with the exact numbers taken as exact. Then $x = (1, 1)^T$. The far wrong vector $\hat x = (2, 0)^T$ has $r = b - A\hat x = (0, 0.0001)^T$. In the $\infty$-norm, $\|A\|_\infty = 2.0001$, $A^{-1} = 10^4 \begin{pmatrix} 1.0001 & -1 \\ -1 & 1 \end{pmatrix}$, $\|A^{-1}\|_\infty = 20001$, and $\kappa_\infty(A) = 2.0001 \cdot 20001 \approx 4.0004 \times 10^4$. The normwise backward error is $\eta = 10^{-4}/(2.0001 \cdot 2 + 2.0001) \approx 1.667 \times 10^{-5}$. The relative error is $\|x - \hat x\|_\infty/\|x\|_\infty = 1$, and the bound $\kappa_\infty(A)\|r\|_\infty/\|b\|_\infty = 40004 \cdot 10^{-4}/2.0001 = 2.0$ holds.

**A backward stable solve of an ill-conditioned system.** Solve $H_{10}\, x = b$ in binary64 by Gaussian elimination with [partial pivoting](/partial-pivoting/), where $H_{10}$ is the stored [Hilbert matrix](/hilbert-matrix/) of order 10 and $b$ is the stored vector of its row sums. Measured against the exact solution of the stored system, in the $\infty$-norm, the computed $\hat x$ has normwise backward error $\eta \approx 1.47 \times 10^{-17} \approx 0.13u$ and relative forward error about $2.5 \times 10^{-4}$. The residual is as small as the data allow, and the error is about $\kappa_\infty(H_{10}) \approx 3.5 \times 10^{13}$ times the backward error.

**Residuals in an iteration.** The [conjugate gradient method](/conjugate-gradient-method/) and [GMRES](/gmres/) update $r_k$ by a recurrence instead of computing $b - A x_k$. In exact arithmetic the two agree. In floating point the *updated* residual can keep decreasing after the *true* residual $b - A x_k$ stagnates at a level of about $u\,\|A\|\,\max_j \|x_j\|$. A stopping test on the updated residual alone can therefore report a precision that the iterate does not have; production codes recompute $b - A x_k$ at the end.

**Stopping tests.** Common tests are $\|r_k\| \le \tau \|b\|$ and $\|r_k\| \le \tau(\|A\|\,\|x_k\| + \|b\|)$. The second is the backward error test, $\eta(x_k) \le \tau$; it is the one that a tolerance near $u$ can meet, because a tolerance below the backward error of the data has no meaning (Higham, Section 17.5).

**Non-example: the residual is not the error.** For $A = 10^{-8} I$ and any $\hat x$, $r = b - 10^{-8}\hat x$ can be small while $\hat x$ is far from $x = 10^8 b$. A residual is meaningful only relative to $\|A\|\,\|\hat x\| + \|b\|$, which is what $\eta$ does.

**Non-example: the least squares residual.** For an overdetermined system, the residual at the solution is not zero, and a small $\|r\|$ is not the goal. The optimality condition is $A^T r = 0$; see the [least squares problem](/least-squares-problem/).

## Related definitions

- [Backward error analysis](/backward-error-analysis/): $\eta$ and $\omega$ are the backward errors of a linear system solution.
- [Condition number](/condition-number/): converts the residual or the backward error into a bound on the forward error.
- [Iterative refinement](/iterative-refinement/): solves $A e = r$ for a correction.
- [Krylov subspace](/krylov-subspace/): the residuals of Krylov methods are polynomials in $A$ applied to $r_0$.
- [Least squares problem](/least-squares-problem/): minimizes $\|b - Ax\|_2$.
- [Matrix norms](/matrix-norms/): the norms in which $\eta$ is measured.

## References
