---
tag: 7A1D6E
kind: theorem
slug: neumann-series
name: Neumann series
aliases:
- Neumann series lemma
- geometric series for matrices
- Banach lemma
area: numerical/linear-systems
level: advanced
summary: If the spectral radius of B is below 1, then I - B is invertible with inverse sum of B^k.
prereqs: [spectral-radius, matrix-norms]
see_also: [condition-number, iterative-refinement, jacobi-method, richardson-iteration, preconditioning, matrix-splitting, banach-fixed-point-theorem, residual]
sources:
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Section 5.6, Matrix norms (power series of matrices, convergence when the spectral radius is below one, and the bound on the norm of (I - A)^-1)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 2.3, Matrix Norms (the power series for (I - F)^-1 when the norm of F is below one, and the perturbation of the inverse)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 2.2, Perturbation Theory (the lemma that a norm below one makes I - X invertible, used for the perturbation bound of A x = b)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 7, Perturbation Theory for Linear Systems (perturbation bounds whose proofs expand (I - A^-1 E)^-1)
---

The Neumann series is the matrix form of the geometric series $1/(1 - t) = 1 + t + t^2 + \cdots$: if the spectral radius of $B$ is below one, then $I - B$ is nonsingular and $(I - B)^{-1} = \sum_{k \ge 0} B^k$. With a norm bound $\|B\| < 1$ it also bounds the inverse and the error of the truncated series. It is the tool behind every perturbation bound for $A x = b$, behind the convergence of splitting iterations and iterative refinement, and behind polynomial preconditioners.

## Statement

**Notation.** $B \in \mathbb{C}^{n \times n}$, $\rho(B)$ its [spectral radius](/spectral-radius/), and $\|\cdot\|$ a submultiplicative [matrix norm](/matrix-norms/) with $\|I\| = 1$ (any operator norm). $S_m = \sum_{k=0}^{m-1} B^k$ is the partial sum.

**Theorem.**

1. The series $\sum_{k \ge 0} B^k$ converges if and only if $\rho(B) < 1$. In that case $I - B$ is nonsingular and $(I - B)^{-1} = \sum_{k \ge 0} B^k$.
2. If $\|B\| < 1$, then
$$\|(I - B)^{-1}\| \le \frac{1}{1 - \|B\|}, \qquad \|(I - B)^{-1} - I\| \le \frac{\|B\|}{1 - \|B\|}, \qquad \|(I - B)^{-1} - S_m\| \le \frac{\|B\|^m}{1 - \|B\|}.$$
3. **(Perturbed inverse.)** Let $A$ be nonsingular and $\|A^{-1} E\| < 1$. Then $A + E$ is nonsingular and
$$\|(A + E)^{-1}\| \le \frac{\|A^{-1}\|}{1 - \|A^{-1}E\|}, \qquad \frac{\|(A + E)^{-1} - A^{-1}\|}{\|A^{-1}\|} \le \frac{\|A^{-1} E\|}{1 - \|A^{-1} E\|}.$$
In particular, if $\kappa(A)\,\|E\|/\|A\| < 1$ with $\kappa(A) = \|A\|\,\|A^{-1}\|$, the right side is at most $\kappa(A)\frac{\|E\|}{\|A\|}\big/\big(1 - \kappa(A)\frac{\|E\|}{\|A\|}\big)$.

## In plain words

Adding up the powers of a matrix works like adding up the powers of a number: if the matrix shrinks every vector in the long run, the sum settles down, and it gives exactly the inverse of the identity minus that matrix. A matrix that is close to the identity, closer than one in size, can therefore always be inverted, its inverse is not much bigger than the identity, and a few terms of the sum already give a good approximation. The same fact says that a small change to an invertible matrix keeps it invertible and changes its inverse only a little.

## Proof

**Part 1.** For every $m$,
$$(I - B) S_m = S_m (I - B) = I - B^m,$$
by telescoping. Suppose $\rho(B) < 1$. Choose $\varepsilon > 0$ with $\rho(B) + \varepsilon < 1$. By the spectral radius facts there is an operator norm $\|\cdot\|_\varepsilon$ with $\|B\|_\varepsilon \le \rho(B) + \varepsilon$, so $\|B^k\|_\varepsilon \le (\rho(B) + \varepsilon)^k$ and the series converges absolutely; let $S$ be its sum. Then $B^m \to 0$, and letting $m \to \infty$ in the identity gives $(I - B) S = S (I - B) = I$. So $I - B$ is nonsingular with inverse $S$.

Conversely, if the series converges, its terms tend to $0$: $B^k \to 0$. If $B v = \lambda v$ with $v \ne 0$, then $B^k v = \lambda^k v \to 0$, so $|\lambda| < 1$. Hence $\rho(B) < 1$.

**Part 2.** If $\|B\| < 1$, then $\rho(B) \le \|B\| < 1$ (for an eigenpair $B v = \lambda v$ and any nonzero $w$, $|\lambda|\,\|v w^*\| = \|B v w^*\| \le \|B\|\,\|v w^*\|$), so part 1 applies. Then $\|(I - B)^{-1}\| \le \sum_k \|B\|^k = 1/(1 - \|B\|)$, using $\|I\| = 1$. Also $(I - B)^{-1} - I = \sum_{k \ge 1} B^k$ and $(I - B)^{-1} - S_m = \sum_{k \ge m} B^k = B^m (I - B)^{-1}$, which give the other two bounds.

**Part 3.** $A + E = A(I + A^{-1} E) = A(I - B)$ with $B = -A^{-1} E$ and $\|B\| < 1$. By part 2, $I - B$ is nonsingular with $\|(I - B)^{-1}\| \le 1/(1 - \|B\|)$, so $(A + E)^{-1} = (I - B)^{-1} A^{-1}$ has norm at most $\|A^{-1}\|/(1 - \|A^{-1}E\|)$. Moreover $(A + E)^{-1} - A^{-1} = \big((I - B)^{-1} - I\big) A^{-1}$, whose norm is at most $\frac{\|B\|}{1 - \|B\|}\|A^{-1}\|$. Finally $\|A^{-1} E\| \le \|A^{-1}\|\,\|E\| = \kappa(A)\|E\|/\|A\|$, and $t \mapsto t/(1-t)$ is increasing on $[0, 1)$. $\blacksquare$

## Consequences

- **Distance to singularity.** By part 3, $A + E$ is nonsingular whenever $\|E\| < 1/\|A^{-1}\|$. So the relative distance from $A$ to the nearest singular matrix is at least $1/\kappa(A)$; in the 2-norm it equals $1/\kappa_2(A)$ (Gastinel and Kahan), the nearest singular matrix coming from the smallest singular value.
- **Perturbation of $A x = b$.** If $(A + E)\hat{x} = b + f$ with $\kappa(A)\|E\|/\|A\| < 1$, then
$$\frac{\|\hat{x} - x\|}{\|x\|} \le \frac{\kappa(A)}{1 - \kappa(A)\|E\|/\|A\|}\Big(\frac{\|E\|}{\|A\|} + \frac{\|f\|}{\|b\|}\Big),$$
the standard forward error bound used with a backward error result (Higham, Chapter 7). With $\hat{x}$ from a backward stable solver, $\|E\|/\|A\|$ is a modest multiple of $u = 2^{-53}$, which turns into the rule of thumb that $\hat{x}$ has about $16 - \log_{10}\kappa(A)$ correct digits.
- **Stationary iterations.** For a splitting $A = M - N$ with $G = M^{-1}N$ and $\rho(G) < 1$, the iterates from $x_0 = 0$ are the partial sums $x_m = S_m(G)\, M^{-1} b \to (I - G)^{-1} M^{-1} b = A^{-1} b$, so [Jacobi](/jacobi-method/), Gauss-Seidel and [Richardson](/richardson-iteration/) are truncated Neumann series, with error at most $\|G\|^m\|x\|$ in any norm with $\|G\| < 1$.
- **Iterative refinement.** The analysis of [iterative refinement](/iterative-refinement/) writes the correction step as a contraction $I - \hat{A}^{-1} A$ and needs its norm below one.
- **Polynomial preconditioners.** $M^{-1} \approx \sum_{k < m} (I - D^{-1}A)^k D^{-1}$ is a truncated Neumann series of the Jacobi splitting; it needs only products with $A$.
- **Nonnegative inverses.** If $B \ge 0$ entrywise and $\rho(B) < 1$, then $(I - B)^{-1} = \sum B^k \ge 0$: this is how M-matrices get their nonnegative inverses.

## Tightness

- **The spectral condition is sharp.** For $B = I$ (or any $B$ with an eigenvalue $1$), $I - B$ is singular. For $B = -I$, $I - B = 2I$ is nonsingular, yet the series $I - I + I - \cdots$ diverges: $\rho(B) < 1$ is needed for the series, not for the invertibility of $I - B$.
- **The norm bound is attained.** For $B = \beta I$ with $0 \le \beta < 1$, $\|(I - B)^{-1}\| = 1/(1 - \beta)$ exactly. For $B = \begin{pmatrix} 0.5 & 0.25 \\ 0 & 0.5 \end{pmatrix}$, $\|B\|_\infty = 0.75$ gives the bound $4$, while $(I - B)^{-1} = \begin{pmatrix} 2 & 1 \\ 0 & 2 \end{pmatrix}$ has $\infty$-norm $3$.
- **A norm below one is sufficient, not necessary.** $B = \begin{pmatrix} 0.9 & 10 \\ 0 & 0.9 \end{pmatrix}$ has $\rho(B) = 0.9$ but $\|B\|_\infty = 10.9$. The series converges to $(I - B)^{-1} = \begin{pmatrix} 10 & 1000 \\ 0 & 10 \end{pmatrix}$, but slowly at first: the $(1,2)$ entry of $B^k$ is $10 k (0.9)^{k-1}$, which peaks near $k = 10$ at about $39$, and the $(1,2)$ entry of $S_m$ is $264$ for $m = 10$, $966$ for $m = 50$, and reaches relative accuracy $1.6 \times 10^{-8}$ only at $m = 200$. Part 2 gives no bound here; the transient is governed by the departure from normality.
- **Nilpotent $B$.** If $B^p = 0$ the series stops: for $B = \begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}$, $(I - B)^{-1} = I + B$ exactly.

## History

Carl Neumann used the series in 1877 to solve the integral equations of potential theory by successive substitution, and the operator version on Banach spaces, with the bound $1/(1 - \|B\|)$, is often called the Banach lemma. In numerical linear algebra it became the standard device for perturbation bounds in the work of Wilkinson and others; its spectral radius form follows from the Jordan form or from Gelfand's formula.

## References
