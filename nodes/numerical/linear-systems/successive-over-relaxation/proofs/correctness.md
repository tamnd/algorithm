---
title: SOR is a splitting iteration whose limit solves A x = b, and it converges for symmetric positive definite A exactly when 0 < omega < 2
proves: [correctness, termination]
status: full
---

Write $A = D - E - F$ with $D$ the diagonal of $A$, $-E$ its strictly lower part and $-F$ its strictly upper part, and assume $a_{ii} \ne 0$ for all $i$ and $\omega \ne 0$. Let $x_k$ be the vector after $k$ sweeps and $e_k = x_k - x$ with $A x = b$.

**Termination.** The outer loop runs at most `maxiter` times and each sweep is a fixed number of operations, so the algorithm stops. It returns `converged = true` only when the test at line L6 holds.

**Lemma 1 (the sweep is a splitting).** One sweep, lines L3 to L5, maps $x_k$ to
$$x_{k+1} = x_k + M_\omega^{-1}(b - A x_k), \qquad M_\omega = \tfrac{1}{\omega} D - E.$$

*Proof.* When line L5 runs for row $i$, the entries $x_j$ with $j < i$ are already new and those with $j > i$ are old, so it states
$$a_{ii} x_{k+1,i} = (1 - \omega) a_{ii} x_{k,i} + \omega\Big(b_i - \sum_{j<i} a_{ij} x_{k+1,j} - \sum_{j>i} a_{ij} x_{k,j}\Big).$$
In matrix form this is $D x_{k+1} = (1-\omega) D x_k + \omega(b + E x_{k+1} + F x_k)$, that is $(D - \omega E) x_{k+1} = ((1-\omega) D + \omega F) x_k + \omega b$. Dividing by $\omega$ gives $M_\omega x_{k+1} = (M_\omega - A) x_k + b$, since $M_\omega - A = \tfrac{1-\omega}{\omega} D + F$. $M_\omega$ is lower triangular with nonzero diagonal, so it is invertible. $\square$

**Lemma 2 (fixed point).** $x$ is a fixed point of the sweep, and $e_{k+1} = G_\omega e_k$ with $G_\omega = I - M_\omega^{-1} A = (D - \omega E)^{-1}((1-\omega)D + \omega F)$. If the iterates converge to some $y$, then $A y = b$.

*Proof.* $b - A x = 0$, so Lemma 1 maps $x$ to itself; subtracting the two relations gives $e_{k+1} = (I - M_\omega^{-1} A) e_k$. If $x_k \to y$, passing to the limit in Lemma 1 gives $M_\omega^{-1}(b - A y) = 0$, and $M_\omega$ is invertible. $\square$

So $e_k = G_\omega^k e_0$, and by the facts on the [spectral radius](/spectral-radius/) page the iteration converges for every $x_0$ if and only if $\rho(G_\omega) < 1$. The residual test at line L6 is then met after finitely many sweeps for every `tol` above the rounding level.

**Lemma 3 (Kahan's bound).** $\rho(G_\omega) \ge |\omega - 1|$. Hence SOR fails to converge for some $x_0$ when $\omega \le 0$ or $\omega \ge 2$.

*Proof.* $D - \omega E$ is lower triangular with diagonal $D$, and $(1-\omega) D + \omega F$ is upper triangular with diagonal $(1-\omega)D$. So $\det G_\omega = \det((1-\omega)D)/\det D = (1-\omega)^n$. The determinant is the product of the $n$ eigenvalues, so at least one has modulus at least $|1 - \omega|$. $\square$

**Lemma 4 (Ostrowski-Reich).** If $A$ is symmetric positive definite and $0 < \omega < 2$, then $\rho(G_\omega) < 1$.

*Proof.* Here $F = E^T$ and $D$ has positive diagonal. Let $G_\omega v = \lambda v$ with $v \ne 0$ in $\mathbb{C}^n$. Then $(M_\omega - A) v = \lambda M_\omega v$, so $A v = (1 - \lambda) M_\omega v$. Since $A$ is nonsingular, $\lambda \ne 1$. Put $\alpha = v^* A v > 0$ and $\delta = v^* D v > 0$. From $v^* M_\omega v = \alpha/(1-\lambda)$ and its conjugate $v^* M_\omega^T v = \alpha/(1-\bar\lambda)$,
$$\alpha\Big(\frac{1}{1-\lambda} + \frac{1}{1-\bar\lambda}\Big) = v^*(M_\omega + M_\omega^T) v = v^*\big(\tfrac{2}{\omega} D - E - E^T\big) v = \alpha + \big(\tfrac{2}{\omega} - 1\big)\delta.$$
The left side is $\alpha \cdot 2\,\mathrm{Re}\,\frac{1}{1-\lambda}$, and $2\,\mathrm{Re}\,\frac{1}{1-\lambda} - 1 = \frac{1 - |\lambda|^2}{|1 - \lambda|^2}$. So
$$\frac{1 - |\lambda|^2}{|1-\lambda|^2} = \Big(\frac{2}{\omega} - 1\Big)\frac{\delta}{\alpha} > 0$$
for $0 < \omega < 2$, which gives $|\lambda| < 1$. $\square$

**Conclusion.** The algorithm always stops. If it reports convergence, the returned $x_k$ satisfies $\|b - A x_k\|_2 \le \mathrm{tol}\,\|b\|_2$, and therefore $\|x_k - x\|/\|x\| \le \kappa(A)\,\mathrm{tol}$ in the 2-norm. For symmetric positive definite $A$ and $0 < \omega < 2$ the iterates converge to $x$ in exact arithmetic for every $x_0$ (Lemmas 2 and 4), and for $\omega$ outside $(0, 2)$ they do not converge for every $x_0$ (Lemma 3). $\blacksquare$

**About floating point.** These statements are about exact arithmetic. In floating point the iterates do not converge but settle at a level set by rounding; the computed residual cannot be pushed below a modest multiple of $u\,\|A\|\,\|x\|$. The tests observe this level for the model problem; Higham, Chapter 17, gives forward and backward error bounds for stationary iterations that depend on $G_\omega$ and on $|M_\omega^{-1}|(|M_\omega| + |M_\omega - A|)$.
