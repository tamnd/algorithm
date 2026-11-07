---
tag: W6N9YA
kind: concept
slug: condition-number
name: Condition number
aliases:
- conditioning
- kappa(A)
- matrix condition number
- ill-conditioning
area: numerical/floating-point
level: core
summary: Measures how much a problem's output changes relative to a change in its input.
prereqs: [relative-error, floating-point-model]
see_also: [backward-error-analysis, forward-error-analysis, numerical-stability, matrix-norms, hilbert-matrix, catastrophic-cancellation, iterative-refinement, accurate-dot-product]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 1.6, Conditioning (the relative condition number of a scalar function and the rule forward error below condition number times backward error); Chapter 6, Norms (the distance to singularity); Section 7.1, Normwise Analysis (Theorem 7.2); Section 7.2, Componentwise Analysis (the Skeel condition number); Chapter 15, Condition Number Estimation
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 12, Conditioning and Condition Numbers
  - paper: "John R. Rice, A theory of condition, SIAM Journal on Numerical Analysis 3(2) (1966), 287-310"
    title: John R. Rice, A theory of condition (1966)
    locator: the general definition of the condition of a problem as the limit of the ratio of relative output to relative input perturbations
  - paper: "Alan M. Turing, Rounding-off errors in matrix processes, Quarterly Journal of Mechanics and Applied Mathematics 1 (1948), 287-308"
    title: Alan M. Turing, Rounding-off errors in matrix processes (1948)
    locator: the introduction of the term condition number for matrices
---

The condition number of a problem measures how much its exact answer can change, relative to its size, when the input changes by a small relative amount. A problem with a small condition number is well conditioned; one with a large condition number is ill conditioned, and no algorithm can be expected to solve it accurately in floating point, because the rounding of the input alone changes the answer. For a linear system $Ax = b$ the condition number is $\kappa(A) = \|A\|\,\|A^{-1}\|$, and about $\log_{10}\kappa(A)$ decimal digits are lost. With [backward error analysis](/backward-error-analysis/) it gives the basic estimate of numerical analysis: forward error is at most about condition number times backward error.

## In plain words

Some questions have answers that hardly move when the question changes a little. Others have answers that jump. The condition number is the factor between the two changes: if the input moves by one part in a million and the answer by one part in a thousand, the condition number is about a thousand.

On a computer every number is already slightly wrong when it is stored. So the condition number tells you how much accuracy you can hope for at best. A good method cannot fix a badly conditioned question; it can only avoid adding its own damage. A large condition number is a property of the question, not a fault of the method.

## The idea

**Notation.** Binary64 with round to nearest and unit roundoff $u = 2^{-53}$; see [floating-point arithmetic](/floating-point-arithmetic/) for the full notation.

**The definition.** Let $y = f(x)$ with $x$ and $y$ nonzero. The relative condition number of $f$ at $x$ is

$$\mathrm{cond}_f(x) = \lim_{\epsilon \to 0} \ \sup_{|\Delta x| \le \epsilon |x|} \frac{|f(x + \Delta x) - f(x)|}{\epsilon\,|f(x)|}$$

(Rice, 1966). For a differentiable scalar $f$ this is

$$\mathrm{cond}_f(x) = \left| \frac{x f'(x)}{f(x)} \right|.$$

For vector problems the absolute values become norms, or are kept componentwise; the choice of how the input is allowed to change (normwise or entry by entry, all data or only some) is part of the definition, and different choices give different condition numbers for the same problem.

**The rule of thumb.** If an algorithm is backward stable, its computed $\hat y$ is $f(x + \Delta x)$ with $|\Delta x| \le c u |x|$. To first order,

$$\frac{|\hat y - y|}{|y|} \lesssim \mathrm{cond}_f(x) \cdot c\,u.$$

This is a first-order statement: it holds as $u \to 0$, and it needs the perturbed problem to stay close to the original one (Higham, Section 1.6).

**The matrix condition number.** For a nonsingular $A$ and a subordinate matrix norm ([matrix norms](/matrix-norms/)), $\kappa(A) = \|A\|\,\|A^{-1}\| \ge 1$. It controls the linear system: if $Ax = b$, $(A + \Delta A)(x + \Delta x) = b + \Delta b$, $\|\Delta A\| \le \epsilon\|A\|$, $\|\Delta b\| \le \epsilon\|b\|$ and $\epsilon\,\kappa(A) < 1$, then

$$\frac{\|\Delta x\|}{\|x\|} \le \frac{2\epsilon\,\kappa(A)}{1 - \epsilon\,\kappa(A)}.$$

This follows from Theorem 7.2 of Higham, and it is an exact bound with no first-order assumption. Two more facts explain the name:

- **Distance to singularity.** $\min\{\|\Delta A\|/\|A\| : A + \Delta A \text{ singular}\} = 1/\kappa(A)$ for subordinate norms (the theorem of Gastinel and Kahan, Higham, Chapter 6). An ill-conditioned matrix is a small relative distance from a singular one.
- **The 2-norm.** $\kappa_2(A) = \sigma_{\max}(A)/\sigma_{\min}(A)$, the ratio of the largest to the smallest singular value.

**Componentwise condition.** If only relative changes of each entry of $A$ are allowed, $|\Delta A| \le \epsilon|A|$, the relevant quantity is the Skeel condition number $\|\,|A^{-1}|\,|A|\,|x|\,\|_\infty / \|x\|_\infty$ (Higham, Section 7.2). It is never larger than $\kappa_\infty(A)$ and is invariant under row scaling, so a badly scaled but otherwise harmless matrix is not called ill conditioned.

**Condition and stability.** Condition belongs to the problem and stability to the algorithm. A [numerically stable](/numerical-stability/) algorithm applied to an ill-conditioned problem gives a large forward error, and the right response is to change the problem (reformulate, or use more precision), not the algorithm. An unstable algorithm can give a large error on a well-conditioned problem, as with [catastrophic cancellation](/catastrophic-cancellation/) in a bad formula.

## Examples

**Scalar functions.** From $\mathrm{cond}_f(x) = |xf'(x)/f(x)|$:

| $f(x)$ | $\mathrm{cond}_f(x)$ | ill conditioned when |
|---|---|---|
| $\sqrt{x}$ | $1/2$ | never |
| $e^x$ | $\lvert x\rvert$ | $\lvert x\rvert$ large |
| $\log x$ | $1/\lvert\log x\rvert$ | $x$ near $1$ |
| $x - 1$ | $\lvert x/(x - 1)\rvert$ | $x$ near $1$ |
| $\sum_i x_i$ (relative changes of each $x_i$) | $\sum_i \lvert x_i\rvert / \lvert\sum_i x_i\rvert$ | the terms cancel |
| $x^{T}y$ (relative changes of each entry) | $2\sum_i \lvert x_i y_i\rvert / \lvert x^{T}y\rvert$ | the products cancel |

**The logarithm near 1.** The decimal number $1.00000001$ is stored as a binary64 float $x$ with relative error about $6.1 \times 10^{-17}$, and $\mathrm{cond}_{\log}(x) \approx 10^{8}$. Python's `math.log(1.00000001)` returns $9.999999889225291 \times 10^{-9}$. Against the exact $\log x$ of the stored float, its relative error is $1.3 \times 10^{-17}$, so the library function is accurate. Against $\log(1 + 10^{-8}) = 9.99999995 \times 10^{-9}$ its relative error is $-6.1 \times 10^{-9}$: the storage error, multiplied by $10^{8}$. No algorithm that receives the rounded input can do better; `math.log1p(1e-8)`, which receives $10^{-8}$ itself, avoids the problem by changing the input.

**A nearly singular 2 by 2 system.** Let

$$A = \begin{pmatrix} 1 & 1 \\ 1 & 1 + 10^{-10} \end{pmatrix}, \qquad b = \begin{pmatrix} 2 \\ 2 + 10^{-10} \end{pmatrix}, \qquad x = \begin{pmatrix} 1 \\ 1 \end{pmatrix}.$$

Here $\kappa_\infty(A) = 4 \times 10^{10} + 4$. Changing $b_2$ by $10^{-10}$, a relative change of $5 \times 10^{-11}$ in $\|b\|_\infty$, changes the exact solution to $(0, 2)$: a relative change of $1$. The bound of Theorem 7.2 with $\Delta A = 0$ allows a change up to about $\epsilon\,\kappa = 2$.

**Hilbert matrices.** The [Hilbert matrix](/hilbert-matrix/) $H_n = (1/(i + j - 1))$ is the classical ill-conditioned matrix. Computed exactly with rational arithmetic:

| $n$ | 2 | 3 | 4 | 5 | 6 | 8 |
|---|---|---|---|---|---|---|
| $\kappa_\infty(H_n)$ | $27$ | $748$ | $28375$ | $943656$ | $29070279$ | $33872791095$ |

The growth is about a factor $e^{3.5}$ per step. For $n = 12$, $\kappa_\infty(H_n)$ is above $10^{16}$, so a solution of $H_{12}x = b$ in binary64 can have no correct digit even with a backward stable solver.

**Roots of polynomials.** The roots of $\prod_{k=1}^{20}(x - k)$, Wilkinson's polynomial, are very ill conditioned as functions of the coefficients in the monomial basis: changing the coefficient $-210$ of $x^{19}$ by $2^{-23}$, a relative change of about $6 \times 10^{-10}$, turns several real roots into complex pairs. The conditioning depends on the representation: the same roots are perfectly conditioned as functions of the factors $x - k$.

## Where it is used

- **Accuracy estimates.** Libraries report an estimate of $\kappa(A)$ with the solution of a linear system (LAPACK's condition estimators), so the user can predict the number of correct digits as about $16 - \log_{10}\kappa(A)$ in binary64. The estimators cost $O(n^2)$ given an LU factorization, against $O(n^3)$ for computing $A^{-1}$ (Higham, Chapter 15).
- **Choosing an algorithm and a precision.** When $\kappa(A)\,u$ is near $1$, [iterative refinement](/iterative-refinement/) with residuals computed in higher precision, or an [accurate dot product](/accurate-dot-product/), recovers accuracy; for least squares, the conditioning of the normal equations is $\kappa(A)^2$, which is why [QR factorization](/qr-decomposition/) is preferred.
- **Analysis of [Gaussian elimination](/gaussian-elimination/).** Backward stability plus $\kappa(A)$ gives the forward error bound of [LU decomposition](/lu-decomposition/) with partial pivoting.
- **Compensated algorithms.** The error bounds of compensated summation and dot products are stated as $u + c\,u^2\,\mathrm{cond}$, so the condition number tells when doubled precision is enough.
- **Perturbation theory.** Eigenvalues, singular values, least squares solutions and polynomial roots each have their own condition numbers, and the theory of each starts by computing it.

## References
