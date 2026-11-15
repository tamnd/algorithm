---
title: The two Riccati solutions give the LQG controller, its closed loop has the separated eigenvalues, and no output feedback has a lower average cost
proves: [correctness]
status: full
---

The plant is $\dot x = A x + B u + w$, $y = C x + v$, with $w$ and $v$ independent zero mean Gaussian white noises of intensities $W \ge 0$ and $V > 0$, and $x(0)$ Gaussian and independent of both. The cost is $J = \lim_{T \to \infty} \frac1T \mathbb{E} \int_0^T (x^T Q x + u^T R u)\, dt$ with $Q \ge 0$ and $R > 0$. The standing assumptions are: $(A, B)$ stabilizable, $(Q^{1/2}, A)$ detectable, $(C, A)$ detectable and $(A, W^{1/2})$ stabilizable. The input $u(t)$ may be any function of the past outputs $y(s)$, $s \le t$, for which the closed loop has a stationary regime.

The proof has four parts. Part 1 shows that lines L6 to L9 return the stabilizing solution of the CARE. Part 2 applies Part 1 to the filter equation by duality (lines L3 and L4). Part 3 gives the eigenvalues of the closed loop. Part 4 proves that $u = -K \hat x$ has the least cost.

## Part 1: the sign function step

Let $G = B R^{-1} B^T$ and $H = \begin{bmatrix} A & -G \\ -Q & -A^T \end{bmatrix}$. With $J_0 = \begin{bmatrix} 0 & I \\ -I & 0 \end{bmatrix}$, the matrix $J_0 H$ is symmetric, so $H$ is similar to $-H^T$ and its eigenvalues come in pairs $\lambda, -\bar\lambda$.

**Lemma 1.** Under the assumptions, $H$ has no eigenvalue on the imaginary axis, and the CARE has a unique stabilizing solution $P = P^T \ge 0$. The stable invariant subspace of $H$ is the range of $\begin{bmatrix} I \\ P \end{bmatrix}$.

*Proof.* This is the theorem on the [stabilizing Riccati solution](/stabilizing-riccati-solution-theorem/) (Kučera 1972). For the last claim: the CARE says $H \begin{bmatrix} I \\ P \end{bmatrix} = \begin{bmatrix} I \\ P \end{bmatrix} (A - G P)$, so the range is invariant under $H$ and $H$ acts on it as $A - G P$, which is Hurwitz. It has dimension $n$, which is the number of eigenvalues of $H$ in the open left half plane. $\square$

**Lemma 2.** Let $H = T \,\mathrm{diag}(J_-, J_+)\, T^{-1}$ with $J_-$ holding the $n$ eigenvalues with negative real part and $J_+$ the $n$ with positive real part. The iteration $Z_0 = H$, $Z_{k+1} = \frac12 (c_k Z_k + c_k^{-1} Z_k^{-1})$ with $c_k > 0$ converges to $\mathrm{sign}(H) = T\, \mathrm{diag}(-I, I)\, T^{-1}$.

*Proof.* Every $Z_k$ is a rational function of $H$, so $Z_k = T\, \mathrm{diag}(f_k(J_-), f_k(J_+))\, T^{-1}$, and it suffices to look at one eigenvalue $z$. The map $z \mapsto \frac12 (c z + 1/(c z))$ keeps the sign of the real part: if $\mathrm{Re}\, z > 0$ then $\mathrm{Re}\, (c z) > 0$ and $\mathrm{Re}\, (1 / (cz)) > 0$. Write $z' = \frac12 (y + 1/y)$ with $y = c z$. Then $\frac{z' - 1}{z' + 1} = \left(\frac{y - 1}{y + 1}\right)^2$, and $|(y - 1)/(y + 1)| < 1$ when $\mathrm{Re}\, y > 0$. So the eigenvalues go to $1$ in the right half plane and to $-1$ in the left, quadratically once they are close. The scaling $c_k = |\det Z_k|^{-1/(2n)}$ only moves the starting point of each step; it does not change the limit (Byers 1987). For a nontrivial Jordan block the same argument holds on the block, because the iteration is a matrix function. $\square$

**Lemma 3.** Let $Z = \mathrm{sign}(H)$. Then $\begin{bmatrix} Z_{12} \\ Z_{22} + I \end{bmatrix} P = -\begin{bmatrix} Z_{11} + I \\ Z_{21} \end{bmatrix}$, and this overdetermined system has exactly one solution.

*Proof.* $Z + I = T\, \mathrm{diag}(0, 2 I)\, T^{-1}$, so the null space of $Z + I$ is the stable invariant subspace of $H$, which is the range of $\begin{bmatrix} I \\ P \end{bmatrix}$ by Lemma 1. Writing $(Z + I) \begin{bmatrix} I \\ P \end{bmatrix} = 0$ in blocks gives the system. The matrix $Z + I$ has rank $n$, and its range is spanned by its columns; the columns of $\begin{bmatrix} Z_{12} \\ Z_{22} + I \end{bmatrix}$ are independent, because a vector $\begin{bmatrix} 0 \\ \xi \end{bmatrix}$ in the null space of $Z + I$ must be of the form $\begin{bmatrix} I \\ P \end{bmatrix} \eta$, which forces $\eta = 0$ and $\xi = 0$. So the solution is unique, and the normal equations of line L8 return it. $\square$

**Lemma 4.** Line L9 does not move an exact stabilizing solution, and from a nearby matrix it converges quadratically to it.

*Proof.* Line L9 is one step of [Kleinman's iteration](/kleinman-iteration/): given $P_k$ with $A - G P_k$ Hurwitz, $P_{k+1}$ solves $(A - G P_k)^T P_{k+1} + P_{k+1} (A - G P_k) + Q + P_k G P_k = 0$. If $P_k = P$, the CARE says that $P$ solves this equation, and the solution is unique because $A - G P$ is Hurwitz. Kleinman's iteration is Newton's method on the CARE (Kleinman 1968), so near $P$ the error is squared at each step. The steps remove the rounding error of the least squares solve. $\square$

So `CARE-SOLVE` returns $P$ in exact arithmetic, and lines L1 and L2 give $P$ and $K = R^{-1} B^T P$ with $A - B K$ Hurwitz.

## Part 2: the filter equation by duality

Transpose the filter equation $A S + S A^T - S C^T V^{-1} C S + W = 0$. It reads $(A^T)^T S + S A^T - S (C^T) V^{-1} (C^T)^T S + W = 0$, which is the CARE for the data $(A^T, C^T, W, V)$. $(A^T, C^T)$ is stabilizable if and only if $(C, A)$ is detectable, and $(W^{1/2}, A^T)$ is detectable if and only if $(A, W^{1/2})$ is stabilizable. So Part 1 applies, line L3 returns the stabilizing $S \ge 0$, and with $L_o = S C^T V^{-1}$ from line L4 the matrix $(A^T - C^T L_o^T)^T = A - L_o C$ is Hurwitz.

## Part 3: the eigenvalues of the closed loop

The controller of line L5 is $\dot{\hat x} = A \hat x + B u + L_o (y - C \hat x)$, $u = -K \hat x$. In the coordinates $(x, e)$ with $e = x - \hat x$:

$$\frac{d}{dt}\begin{bmatrix} x \\ e \end{bmatrix} = \begin{bmatrix} A - B K & B K \\ 0 & A - L_o C \end{bmatrix} \begin{bmatrix} x \\ e \end{bmatrix} + \begin{bmatrix} w \\ w - L_o v \end{bmatrix}.$$

The matrix is block upper triangular, so its characteristic polynomial is $\det(sI - A + BK) \det(sI - A + L_o C)$. Both factors are Hurwitz by Parts 1 and 2, so the closed loop is internally Hurwitz. This is the [separation principle](/separation-principle/) for eigenvalues. It says nothing about margins.

## Part 4: optimality

Let $u$ be any admissible input and $x$ the resulting state. The Itô formula for $x^T P x$ gives

$$d(x^T P x) = \left(x^T (A^T P + P A) x + 2 u^T B^T P x + \mathrm{tr}(P W)\right) dt + 2 x^T P\, dw_t,$$

where $w_t$ is the Wiener process with $dw_t = w\,dt$. Use the CARE, $A^T P + P A = -Q + P G P$, and complete the square with $K = R^{-1} B^T P$:

$$x^T Q x + u^T R u = (u + K x)^T R (u + K x) + \mathrm{tr}(P W) - \frac{d}{dt}\, \mathbb{E}\,(x^T P x),$$

after taking expectations (the Itô integral has mean 0). Average over $[0, T]$ and let $T \to \infty$. In a stationary regime $\frac1T \mathbb{E}\, x(T)^T P x(T) \to 0$, so

$$J = \mathrm{tr}(P W) + \lim_{T \to \infty} \frac1T \int_0^T \mathbb{E}\,(u + K x)^T R (u + K x)\, dt. \tag{1}$$

Let $\hat x(t) = \mathbb{E}[x(t) \mid y(s), s \le t]$ and $e = x - \hat x$. For a linear Gaussian plant the input is known from the outputs, so $e$ does not depend on the choice of $u$: it is the error of the [Kalman-Bucy filter](/kalman-bucy-filter/), whose covariance tends to $S$. $u + K \hat x$ is a function of the past outputs, and $e$ is orthogonal to every such function. So

$$\mathbb{E}\,(u + K x)^T R (u + K x) = \mathbb{E}\,(u + K \hat x)^T R (u + K \hat x) + \mathrm{tr}(K^T R K\, \mathbb{E}\, e e^T).$$

The second term tends to $\mathrm{tr}(K^T R K S)$ for every admissible $u$, and the first is at least 0, with equality if and only if $u = -K \hat x$. With (1),

$$J \ge J^* = \mathrm{tr}(P W) + \mathrm{tr}(S K^T R K),$$

with equality for the controller of line L5. For that controller the filter of line L5 is the steady state Kalman-Bucy filter, which gives the conditional mean in the stationary regime. $\square$

**Remark.** The two terms of $J^*$ show the split: $\mathrm{tr}(P W)$ is the cost of LQR with the full state, and $\mathrm{tr}(S K^T R K)$ is the price of using an estimate. The same number is the square of the $H_2$ norm of the closed loop from the scaled noise to the scaled output $(Q^{1/2} x, R^{1/2} u)$, which is why [H2 optimal control](/h2-optimal-control/) has the same solution. The test computes $J$ for the loop from the stationary covariance $X$ of $(x, \hat x)$, the solution of $A_{cl} X + X A_{cl}^T + B_n N B_n^T = 0$, and compares it with $J^*$.
