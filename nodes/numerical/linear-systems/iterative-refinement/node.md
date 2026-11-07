---
tag: 6MBZF8
kind: technique
slug: iterative-refinement
name: Iterative refinement
aliases:
- residual correction
- mixed precision iterative refinement
- GMRES-IR
area: numerical/linear-systems
level: advanced
summary: Improve a computed solution by solving for the residual correction with the same factorization.
prereqs: [lu-decomposition, residual, condition-number, backward-error-analysis, floating-point-model]
see_also: [residual, lup-decomposition, growth-factor, gmres, condition-number, hilbert-matrix, least-squares-problem, preconditioning]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 12, Iterative Refinement (Section 12.1, behaviour of the forward error, Theorem 12.1; Section 12.2, iterative refinement implies stability, Theorem 12.3; Section 12.3, notes)
  - paper: doi:10.1145/321386.321394
    title: Cleve B. Moler, Iterative refinement in floating point, Journal of the ACM 14(2), 1967
    locator: pp. 316 to 321 (convergence with the residual in double the working precision)
  - paper: doi:10.1090/S0025-5718-1980-0572859-4
    title: Robert D. Skeel, Iterative refinement implies numerical stability for Gaussian elimination, Mathematics of Computation 35(151), 1980
    locator: pp. 817 to 832 (one step in fixed precision gives a componentwise backward error of order u)
  - paper: doi:10.1137/17M1140819
    title: Erin Carson and Nicholas J. Higham, Accelerating the solution of linear systems by iterative refinement in three precisions, SIAM Journal on Scientific Computing 40(2), 2018
    locator: pp. A817 to A847 (the three precision analysis and GMRES-IR)
  - paper: doi:10.1137/17M1122918
    title: Erin Carson and Nicholas J. Higham, A new analysis of iterative refinement and its application to accurate solution of ill-conditioned sparse linear systems, SIAM Journal on Scientific Computing 39(6), 2017
    locator: pp. A2834 to A2856 (GMRES-based refinement for kappa(A) up to about 1/u)
  - paper: doi:10.1145/1141885.1141894
    title: James Demmel, Yozo Hida, William Kahan, Xiaoye S. Li, Sonil Mukherjee and E. Jason Riedy, Error bounds from extra-precise iterative refinement, ACM Transactions on Mathematical Software 32(2), 2006
    locator: pp. 325 to 351 (the LAPACK xGERFSX design and its stopping tests)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 3.5.3, Iterative improvement
---

Iterative refinement improves a computed solution $\hat x$ of $A x = b$ by computing the [residual](/residual/) $r = b - A \hat x$, solving $A d = r$ with the factorization already at hand, and updating $\hat x \leftarrow \hat x + d$. Each step costs about $4 n^2$ flops against $2 n^3/3$ for the factorization. What it buys depends on the precisions. With the residual in twice the working precision (Wilkinson, Moler 1967), the forward error falls to about $u$, independent of $\kappa(A)$, as long as $\kappa(A) u$ is safely below $1$. With everything in working precision (Skeel 1980), one step turns a possibly unstable LU solve into a componentwise backward stable one. With the factorization in low precision and the residual in high precision (the mixed precision form used on GPUs), a cheap single or half precision LU gives double precision accuracy.

## In plain words

You solve a system and get an answer that is close but not exact. Plug the answer back into the equations and see how far off each one is. That leftover is itself the right side of a new system whose solution is exactly the correction you need. You already did the hard work of factoring the matrix, so solving for the correction is cheap. Add the correction and repeat. If the leftovers are computed carefully, each round gains several correct digits until the answer is as good as the arithmetic allows.

## When it applies

The technique applies to any solver of $A x = b$ that can be reused cheaply for new right sides: an LU or Cholesky factorization, a QR factorization for least squares, or a preconditioned Krylov method. It needs $A$ itself (not only the factors) to form the residual. It converges when the correction solves are accurate to at least one digit relative to the error, which for LU means roughly $\kappa(A) u_f < 1$.

**Notation.** $A \in \mathbb{R}^{n \times n}$ nonsingular, $x = A^{-1} b$, $\hat x_i$ the iterates, $r_i = b - A \hat x_i$, $e_i = x - \hat x_i$. Three precisions: $u_f$ for the factorization and correction solve, $u$ for storing $\hat x_i$ (the working precision, $u = 2^{-53}$ in binary64), $u_r$ for the residual. $\kappa_\infty(A) = \|A\|_\infty \|A^{-1}\|_\infty$ and $\operatorname{cond}(A, x) = \|\,|A^{-1}|\,|A|\,|x|\,\|_\infty / \|x\|_\infty$ (Skeel's condition number). The componentwise backward error is $\omega(\hat x) = \max_i |r_i| / (|A|\,|\hat x| + |b|)_i$.

## The template

```pseudo id=main
ITERATIVE-REFINEMENT(A, b, SOLVE, tol, maxit)
L1  x₀ ← SOLVE(b)                                    ▷ precision u_f, e.g. from P A = L U
L2  for i ← 0 to maxit − 1 do
L3      r_i ← b − A x_i                              ▷ hole: precision u_r of the residual
L4      if STOP(r_i, x_i) then return x_i            ▷ hole: the stopping test
L5      d_i ← SOLVE(r_i)                             ▷ hole: the correction solver
L6      x_{i+1} ← x_i + d_i                          ▷ precision u
L7      if ‖d_i‖ > ‖d_{i−1}‖ / 2 then report "no contraction"; return x_{i+1}
L8  return x_maxit
```

The holes are the residual precision, the correction solver and the stopping test. Line L3 is where accuracy is decided: $r_i$ is the small difference of nearly equal vectors, and its relative error in precision $u_r$ is about $u_r \|A\| \|\hat x_i\| / \|r_i\|$. Line L7 is a divergence and stagnation check of the kind used in LAPACK.

**Why it works (proved).** If SOLVE returns $\hat d_i = (A + E_i)^{-1} \hat r_i$ with $\|A^{-1} E_i\| \le \eta < 1$, and $\hat r_i = r_i + f_i$ is the computed residual, then exactly

$$e_{i+1} = (A + E_i)^{-1} E_i\, e_i - (A + E_i)^{-1} f_i - (\text{rounding of line L6}).$$

So $\|e_{i+1}\| \le \frac{\eta}{1 - \eta} \|e_i\| + \frac{\|A^{-1}\|\,\|f_i\|}{1 - \eta} + u \|\hat x_{i+1}\|$: the error contracts by about $\eta$ per step down to a floor set by the residual error and the storage precision. For LU with partial pivoting, $\eta$ is of order $n u_f \rho_n \kappa_\infty(A)$ in the worst case and closer to $u_f \kappa_\infty(A)$ in practice.

**The two floors (proved, Higham Theorem 12.1, with constants of order $n$).**

- *Extra precise residual*, $u_r = u^2$: $\|f_i\| \lesssim u^2 (\|A\| \|\hat x_i\| + \|b\|)$, so the limiting forward error is about $u + n u^2 \operatorname{cond}(A, x)$, which is $\approx u$ whenever $n\,\operatorname{cond}(A, x)\,u \le 1$.
- *Fixed precision*, $u_r = u$: the floor is about $n u \operatorname{cond}(A, x)$, no better than a backward stable solver. What improves instead is the backward error.

**Fixed precision gives stability (proved, Skeel 1980; Higham Theorem 12.3).** If $u_r = u_f = u$, and $\operatorname{cond}(A^{-1})\,\sigma(A, \hat x_0)\, u$ is sufficiently small, where $\sigma(A, x) = \max_i (|A||x|)_i / \min_i (|A||x|)_i$, then one step of refinement after Gaussian elimination with partial pivoting gives $\omega(\hat x_1) \le c\, n u$, a componentwise relative backward error of order $u$. LAPACK's `gerfs` implements this form.

**Cost.** Line L3 is $2 n^2$ flops (in precision $u_r$) and line L5 is $2 n^2$ for two triangular solves, so a step is $4 n^2$ flops, plus the $n^2$ storage for a copy of $A$ when the factors overwrite it. Three to five steps are typical. For sparse $A$ with $z$ nonzeros and factors with $f$ nonzeros, a step costs $2 z + 4 f$ flops. The steps are matrix-vector work, limited by memory bandwidth rather than by flops.

## Classic examples

**Hilbert matrix in binary64.** Let $A = \mathrm{fl}(H_{10})$, the [Hilbert matrix](/hilbert-matrix/) rounded to binary64, with $\kappa_\infty(A) \approx 3.5 \times 10^{13}$, and $b = \mathrm{fl}(A e)$. Gaussian elimination with partial pivoting gives forward error $7.2 \times 10^{-5}$ and normwise backward error $2.0 \times 10^{-17}$. With the residual computed exactly and rounded to binary64 (which models $u_r \ll u$), the forward errors of the next iterates are $9.8 \times 10^{-10}$, $1.3 \times 10^{-14}$ and $6.5 \times 10^{-17}$, after which they stay put: about five digits per step, so $\eta \approx 10^{-5}$, and a limit at the storage precision. With the residual in binary64 the forward error only moves to $2.9 \times 10^{-5}$ and stays there. These numbers were measured with the exact solution of the rounded system as reference.

**Rescuing an unstable LU.** For $A = \begin{pmatrix} 10^{-20} & 1 \\ 1 & 1 \end{pmatrix}$ and $b = (1, 2)^T$, LU without pivoting gives $\hat x_0 = (0, 1)$, which is wrong in the first component. The residual in binary64 is $r_0 = (0, 1)^T$, and solving with the same bad factors gives $\hat d_0 = (1, -10^{-20})$, so $\hat x_1 = (1, 1)$, correct to working precision. One step of fixed precision refinement has restored the backward stability that pivoting would have given, as Skeel's theorem predicts.

**Mixed precision LU.** Factor $A$ in binary32 ($u_f = 2^{-24}$), and refine with residuals and updates in binary64. If $\kappa(A) u_f \ll 1$ this converges to binary64 accuracy in a few steps, with the $O(n^3)$ work done at single precision speed. LAPACK's `dsgesv` and `dsposv` do this and fall back to a binary64 factorization if the iteration fails to converge (Langou, Buttari, Dongarra and others, 2006 and 2007).

**GMRES-IR.** When $\kappa(A) u_f \ge 1$ the LU correction solve no longer contracts. Carson and Higham (2017, 2018) solve the correction equation with [GMRES](/gmres/) preconditioned by the low precision factors, $\hat U^{-1} \hat L^{-1} A d = \hat U^{-1} \hat L^{-1} r$. The preconditioned matrix is close to $I$ even when the factors are poor, and the analysis gives convergence for $\kappa_\infty(A)$ up to about $u^{-1}$ with a half precision factorization, under stated hypotheses on the GMRES residual accuracy.

**Least squares.** Refining the solution of $\min \|b - A x\|_2$ through the normal equations does not work well, but refinement of the augmented system $\begin{pmatrix} I & A \\ A^T & 0 \end{pmatrix} \begin{pmatrix} r \\ x \end{pmatrix} = \begin{pmatrix} b \\ 0 \end{pmatrix}$ with a QR factorization, as proposed by Björck (1967), corrects both $x$ and the residual. See [least squares problem](/least-squares-problem/).

## Variations

- **Precision choices.** $(u_f, u, u_r) = (u, u, u^2)$ is the classical form, $(u, u, u)$ the fixed precision form, and $(u_{\text{low}}, u, u)$ or $(u_{\text{low}}, u, u^2)$ the mixed precision forms of the last decade.
- **Correction solver.** LU or Cholesky solves, a few steps of a Krylov method preconditioned by the factors, or a sparse incomplete factorization.
- **Stopping tests.** Stop when $\omega(\hat x_i) \le u$ (Skeel's test, used by `gerfs`), when $\|d_i\| \le u \|\hat x_i\|$, or when $\|d_i\| / \|d_{i-1}\|$ exceeds $1/2$ (no more contraction). Demmel et al. (2006) also stop per component and return error bounds for each one.
- **Refinement for eigenvectors and other problems.** The same idea, Newton's method on the residual, refines eigenpairs, matrix square roots and solutions of Sylvester equations.

## Pitfalls

- **Residual in working precision does not improve the forward error.** Unless $u_r < u$, the forward error stays at about $n u\,\operatorname{cond}(A, x)$, as the Hilbert example shows.
- **Divergence when $\kappa(A) u_f \gtrsim 1$.** The contraction factor $\eta$ exceeds $1$ and the iterates move away. Detect it with line L7 and switch to a better factorization or to GMRES-IR.
- **Losing $A$.** LU in place overwrites $A$; the residual needs the original. Keep a copy, or for sparse matrices keep the original arrays.
- **Rounding $b$ or $A$.** If $A$ or $b$ were rounded on input, refinement solves the rounded system to high accuracy, not the original one. The error from rounding the data, about $u\,\kappa(A)$, remains.
- **Extra precision must be real.** Computing $r$ in binary64 with fused multiply-add is not $u_r = u^2$. Use double-double arithmetic, a wider format, or a compensated dot product.
- **Stopping only on the residual norm.** A small $\|r_i\|$ says the backward error is small; it says nothing about the forward error when $\kappa(A)$ is large.

## Exercises

1. Derive the error recurrence $e_{i+1} = (A + E_i)^{-1}(E_i e_i - f_i)$ ignoring the rounding of line L6.
2. Show that if $\eta = 1/2$ the iteration gains one binary digit per step, and if $\eta = 10^{-5}$ about five decimal digits, as in the Hilbert example.
3. Reproduce the tiny pivot example and check that $\hat d_0 = (1, -10^{-20})$.
4. With exact residuals ($f_i = 0$), $\eta < 1/2$ and line L6 adding an error of at most $u \|x\|$, show that $\limsup_i \|e_i\| \le u \|x\| (1 - \eta)/(1 - 2\eta)$.
5. Back substitution is already componentwise backward stable. Explain why fixed precision refinement of a triangular solve therefore cannot improve $\omega(\hat x)$ by more than a constant factor.
6. Implement mixed precision refinement with a binary32 LU (simulate it by rounding with `struct.pack('f', ...)` after each operation) and find the $n$ at which it fails for the Hilbert matrix.

## References
