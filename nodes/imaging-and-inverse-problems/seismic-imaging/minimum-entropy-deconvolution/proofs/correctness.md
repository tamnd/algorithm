---
title: The varimax norm lies between 1/T and 1, its gradient has a closed form, and the fixed points of Wiggins' iteration are exactly the stationary points of the total varimax
proves: [correctness]
status: full
---

**Setting.** There are $M$ traces $x_1, \ldots, x_M$, real and not all zero, and a real filter $f$ of $L$ taps, $f \ne 0$. The output of trace $i$ is the full convolution $y_i = f * x_i$, $y_{it} = \sum_k f_k x_{i,t-k}$, of length $T_i$. The varimax norm of a nonzero $y$ is $V(y) = \sum_t y_t^4 / (\sum_t y_t^2)^2$. We write $E_i = \sum_t y_{it}^2$, $F_i = \sum_t y_{it}^4$, $b_{ik} = \sum_t y_{it}^3 x_{i,t-k}$, and $R_i$ for the $L \times L$ matrix $(R_i)_{kj} = \sum_t x_{i,t-k} x_{i,t-j}$, which is Toeplitz because the convolution is full. The objective is $\Phi(f) = \sum_i V(y_i)$. Lines L3 to L7 form
$$A(f) = \sum_i \frac{F_i}{E_i^3} R_i, \qquad c(f) = \sum_i \frac{b_i}{E_i^2},$$
solve $A(f) u = c(f)$, and set the new filter to $u / \|u\|$.

**Claim 1 (bounds of the varimax norm).** For a nonzero $y$ of length $T$, $1/T \le V(y) \le 1$. $V = 1$ exactly when $y$ has one nonzero sample, and $V = 1/T$ exactly when all $|y_t|$ are equal.

*Proof.* For the upper bound, $\sum_t y_t^4 \le (\max_t y_t^2) \sum_t y_t^2 \le (\sum_t y_t^2)^2$. The second inequality is an equality only if at most one $y_t$ is nonzero, and then the first is too. For the lower bound, the Cauchy-Schwarz inequality for $(y_t^2)_t$ and $(1)_t$ gives $(\sum_t y_t^2)^2 \le T \sum_t y_t^4$, with equality exactly when all $y_t^2$ are equal. $\square$

**Claim 2 (scale invariance).** $\Phi(\lambda f) = \Phi(f)$ for every $\lambda \ne 0$. So the normalization after line L7 does not change $\Phi$, and the problem is a search over directions of $f$.

*Proof.* $y_i$ scales by $\lambda$, the numerator of $V$ by $\lambda^4$ and the denominator by $\lambda^4$. $\square$

**Claim 3 (the gradient).** $\dfrac{\partial \Phi}{\partial f_k} = 4\sum_i \dfrac{b_{ik} E_i - F_i (R_i f)_k}{E_i^3}$.

*Proof.* Since $\partial y_{it}/\partial f_k = x_{i,t-k}$, we get $\partial F_i/\partial f_k = 4\sum_t y_{it}^3 x_{i,t-k} = 4 b_{ik}$ and $\partial E_i/\partial f_k = 2\sum_t y_{it} x_{i,t-k}$. Further $\sum_t y_{it} x_{i,t-k} = \sum_j f_j \sum_t x_{i,t-j} x_{i,t-k} = (R_i f)_k$. The quotient rule on $F_i/E_i^2$ gives $(4 b_{ik} E_i^2 - F_i \cdot 2E_i \cdot 2 (R_i f)_k)/E_i^4$, which is the term of trace $i$. $\square$

**Claim 4 (the system is solvable).** If some $y_i$ is not zero, $A(f)$ is symmetric positive definite, so line L7 has exactly one solution.

*Proof.* Each $R_i$ is the Gram matrix of the shifted copies $(x_{i,t-k})_t$, $k = 0, \ldots, L - 1$. For a nonzero $x_i$ these copies are linearly independent (take the largest $k$ with a nonzero coefficient and the last nonzero sample of $x_i$; that output sample is not cancelled), so $R_i$ is positive definite, and it is the zero matrix for $x_i = 0$. The weights $F_i/E_i^3$ are positive for every trace with $y_i \ne 0$, and $y_i \ne 0$ whenever $x_i \ne 0$ because convolution by a nonzero $f$ is injective. So $A(f)$ is a positive combination of positive definite matrices plus zero matrices. $\square$

**Claim 5 (fixed points are stationary points).** A unit vector $f$ is a fixed point of the iteration (the new filter equals $f$) if and only if $\nabla \Phi(f) = 0$.

*Proof.* By Claim 3, $\nabla \Phi(f) = 4(c(f) - A(f) f)$, so $f$ is stationary exactly when $A(f) f = c(f)$. If $A(f) f = c(f)$, then line L7 returns $u = f$ by Claim 4, and $u/\|u\| = f$. Conversely, let $u/\|u\| = f$, so $u = \mu f$ with $\mu = \|u\| > 0$ and $c(f) = \mu A(f) f$. Take the inner product with $f$. On one side, $f^T b_i = \sum_t y_{it}^3 \sum_k f_k x_{i,t-k} = \sum_t y_{it}^4 = F_i$, so $f^T c(f) = \sum_i F_i/E_i^2$. On the other side, $f^T R_i f = \sum_t y_{it}^2 = E_i$, so $f^T A(f) f = \sum_i F_i/E_i^2$. These are equal and positive, so $\mu = 1$ and $A(f) f = c(f)$. $\square$

So when the iteration converges to a limit $f^\ast$ and the map is continuous there (it is, since $A$ is invertible near $f^\ast$), $f^\ast$ is a stationary point of $\Phi$: a local maximum, a saddle point or, in principle, a local minimum. The iteration is not proved to increase $\Phi$ at every step, and it is not proved to converge; Wiggins reported that it converges quickly in practice, and the tests and the example on the page measure an increase of $\Phi$ on their data, which is not a theorem. The global maximum of $\Phi$ over $f$ need not be the inverse of the wavelet: on a finite record the sparsest output can be sparser than the true reflectivity.

**Claim 6 (cost).** With traces of $n$ samples, the matrices $R_i$ cost $O(M n L)$ once. Each iteration costs $O(M (n L + L^2))$ to form $A(f)$ and $c(f)$, and $O(L^3)$ for the solve by Gaussian elimination, or $O(L^2)$ by Levinson recursion, because $A(f)$ is Toeplitz.

*Proof.* Line L3 computes $M$ full convolutions of length $n + L - 1$ with $L$ taps; line L6 computes $L$ sums of $n + L - 1$ products per trace; line L5 adds $M$ matrices of size $L \times L$. A sum of Toeplitz matrices with scalar weights is Toeplitz, so $A(f)$ is Toeplitz and symmetric positive definite (Claim 4), and Levinson recursion applies; the code uses the general solver. $\square$
