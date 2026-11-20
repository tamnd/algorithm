---
title: Consistent DSA keeps the transport solution, its diffusion equation is the diamond difference P1 system, it is exact for S2 with reflection, and its Fourier factor is below the scattering ratio for every cell size
proves: [correctness]
status: full
---

We assume exact arithmetic. The slab, the cross sections and the lines L1 to L8 are those of the page. Cell $j$ has $\Sigma_{t,j} > 0$, $0 \le \Sigma_{s,j} \le \Sigma_{t,j}$, the absorption $\Sigma_{a,j} = \Sigma_{t,j} - \Sigma_{s,j}$ and the width $h_j > 0$, and it lies between the edges $j$ and $j + 1$. The directions and weights are the $N$-point Gauss-Legendre rule with $N$ even, so the weights are positive, they sum to 2, and the rule is exact for $\mu^2$: $\tfrac12\sum_n w_n\mu_n^2 = \tfrac13$.

As in the [source iteration](/source-iteration/) proof, line L4 with the source of line L3 is the affine map $\phi \mapsto T\phi + b$. Here $T$ sweeps the source $\Sigma_s v/2$ with zero incoming data and the same reflection, and $b$ sweeps $q/2$ with the given data. That proof shows that the sweep with exact reflection has exactly one solution (its Lemma 1) and that, if $\Sigma_{s,j} < \Sigma_{t,j}$ in every cell, the diamond difference equations have exactly one solution $\phi = T\phi + b$ (its Theorem 3).

## The diffusion equation for the correction

Write $g_j = 2/(3\Sigma_{t,j}h_j)$ and $s_j = \Sigma_{a,j}h_j/2$. The consistent correction of line L6 solves the edge system $Af = d$ with the rows
$$(-g_L + s_L)f_{i-1} + (g_L + g_R + s_L + s_R)f_i + (-g_R + s_R)f_{i+1} = R_Lh_L + R_Rh_R \tag{1}$$
at the inner edge $i$ between the cells $L = i - 1$ and $R = i$. The face rows keep only the terms of the one cell next to the face, and a vacuum face adds 1 to its diagonal entry. The cell correction is $(f_j + f_{j+1})/2$.

**Theorem 1 (the edge system is symmetric positive definite).** If some cell has $\Sigma_{a,j} > 0$ or some face is vacuum, then $A$ is symmetric positive definite. So line L6 has exactly one solution, and the tridiagonal elimination without pivoting computes it.

*Proof.* Each cell adds the matrix $g_j\begin{pmatrix}1 & -1\\ -1 & 1\end{pmatrix} + s_j\begin{pmatrix}1 & 1\\ 1 & 1\end{pmatrix}$ to the rows and columns of its two edges. This gives the entries of (1). So
$$f^{\mathsf T}Af = \sum_j \left[g_j(f_{j+1} - f_j)^2 + s_j(f_j + f_{j+1})^2\right] + \sum_{\text{vacuum faces}} f_{\text{face}}^2 \ge 0 .$$
If the form is 0, then $f_{j+1} = f_j$ for every $j$ because $g_j > 0$, so $f$ is a constant $F$. Then a cell with $s_j > 0$ or a vacuum face gives $F = 0$. So $A$ is positive definite. The pivots of the elimination are ratios of leading principal minors, which are positive for such a matrix. $\square$

**Theorem 2 (the edge system is the diamond difference P1 system).** Consider the P1 equations for a flux $f$ and a current $J$ with one value at each edge, the source $R_j$ in cell $j$, and diamond difference in space:
$$J_{j+1} - J_j + \Sigma_{a,j}h_j\,\frac{f_j + f_{j+1}}{2} = R_jh_j, \qquad \frac13(f_{j+1} - f_j) + \Sigma_{t,j}h_j\,\frac{J_j + J_{j+1}}{2} = 0, \tag{2}$$
with $J = 0$ at a reflecting face and the Marshak condition $J_0 = -f_0/2$ or $J_M = f_M/2$ at a vacuum face. Then $(f, J)$ solves these equations if and only if $f$ solves the edge system, with $J$ given by (3) below.

*Proof.* In cell $j$, the two equations (2) give the sum and the difference of the currents at its edges: $J_j + J_{j+1} = -g_j(f_{j+1} - f_j)$ and $J_{j+1} - J_j = R_jh_j - s_j(f_j + f_{j+1})$. So the cell fixes the currents at its edges:
$$J_j = \tfrac12\left[-g_j(f_{j+1} - f_j) - R_jh_j + s_j(f_j + f_{j+1})\right], \quad J_{j+1} = \tfrac12\left[-g_j(f_{j+1} - f_j) + R_jh_j - s_j(f_j + f_{j+1})\right]. \tag{3}$$
At an inner edge $i$, the value from cell $i - 1$ must equal the value from cell $i$. Multiply this equation by 2 and move all terms to the left: this is (1). At a reflecting face $x = 0$, $J_0 = 0$ in (3) gives $(g_0 + s_0)f_0 + (-g_0 + s_0)f_1 = R_0h_0$, the face row. At a vacuum face, $J_0 = -f_0/2$ gives the same row with $1$ added to the coefficient of $f_0$. The face $x = L$ is the mirror case. Each step can be reversed, so the two systems have the same solutions. $\square$

The Marshak condition is the P1 form of "no particles enter": with $\psi = f/2 + 3J\mu/2$, the incoming current at $x = 0$ is $\int_0^1 \mu\psi\,d\mu = f/4 + J/2$, and it is zero when $J = -f/2$.

## The same fixed point

**Theorem 3 (DSA keeps the transport solution).** Let $\phi$ be the diamond difference solution, $\phi = T\phi + b$, and let $C$ be the linear map from the residual $R$ to the correction of line L6. The error $e^{(l)} = \phi^{(l)} - \phi$ of DSA satisfies
$$e^{(l+1)} = \left(T + C\Sigma_s(T - I)\right)e^{(l)}.$$
So $\phi$ is a fixed point of lines L3 to L7, and the iteration converges to $\phi$ from every start if and only if the spectral radius of $T + C\Sigma_s(T - I)$ is less than 1.

*Proof.* Line L4 gives $\phi^{(l+1/2)} = T\phi^{(l)} + b$, so $\phi^{(l+1/2)} - \phi = Te^{(l)}$. Line L5 gives $R = \Sigma_s(\phi^{(l+1/2)} - \phi^{(l)}) = \Sigma_s(Te^{(l)} - e^{(l)})$. Line L7 adds $CR$ and subtracts nothing else. So $e^{(l+1)} = Te^{(l)} + C\Sigma_s(T - I)e^{(l)}$. The last claim is the standard fact for a linear iteration with a fixed matrix. $\square$

**Theorem 4 (S2 with reflection is exact in one iteration).** Let $N = 2$, let both faces reflect, let every cell have $\Sigma_{s,j} < \Sigma_{t,j}$, and let the cross sections and widths vary from cell to cell. Then from any $\phi^{(0)}$, one DSA iteration gives the diamond difference solution $\phi$.

*Proof.* Let $\delta = \phi - \phi^{(l+1/2)}$. Since $\phi = T\phi + b$ and $\phi^{(l+1/2)} = T\phi^{(l)} + b$, we have $\delta = T(\phi - \phi^{(l)}) = T\delta + T(\phi^{(l+1/2)} - \phi^{(l)})$. Here $T(\phi^{(l+1/2)} - \phi^{(l)})$ is the sweep of the source $R/2$. So $\delta$ is the scalar flux of the diamond difference $S_2$ problem with scattering $\Sigma_s$, the source $R$ in place of $q$ and reflection at both faces. By the source iteration proof, this problem has exactly one solution.

The $S_2$ rule has $\mu = \pm 1/\sqrt3$ and the weights 1 and 1. Write $f = \psi_+ + \psi_-$ and $J = \mu(\psi_+ - \psi_-)$ at each edge. The diamond difference equations of the two directions in cell $j$ are $\pm\mu(\psi_{\pm,j+1} - \psi_{\pm,j})/h_j + \Sigma_{t,j}\bar\psi_\pm = (\Sigma_{s,j}\bar f + R_j)/2$, with the cell values $\bar\psi_\pm$ equal to the mean of the edge values. Their sum, times $h_j$, is the first equation (2). Their difference, times $\mu h_j$ and with $\mu^2 = 1/3$, is the second equation (2). Reflection $\psi_+ = \psi_-$ is $J = 0$. The change of variables is invertible, $\psi_\pm = (f \pm J/\mu)/2$. So the $S_2$ problem and the P1 problem (2) are the same system. By Theorem 2 its $f$ solves the edge system, and its cell flux is the mean of the edge values, which is the correction of line L6. Since $\Sigma_a > 0$, Theorem 1 says that this correction is unique. So $CR = \delta$, and line L7 gives $\phi^{(l+1/2)} + \delta = \phi$. $\square$

With vacuum faces the claim fails: $S_2$ with no incoming particles gives $J_0 = -f_0/\sqrt3$, while line L6 uses the Marshak value $J_0 = -f_0/2$. The tests measure a relative error of about 2 percent after one step in that case.

## Fourier analysis

**Theorem 5 (the factor of consistent DSA).** Let the slab have $M$ equal cells of width $h$ with the same $\Sigma_t$ and $\Sigma_s$, let $c = \Sigma_s/\Sigma_t < 1$, and let both faces reflect. For $k = 0, \ldots, M - 1$ let $\theta = \pi k/M$, $e_j = \cos(\theta(j + 1/2))$ and $\lambda = 2\tan(\theta/2)/(\Sigma_th)$. Then $e$ is an eigenvector of the DSA error map of Theorem 3 with the eigenvalue
$$\omega(\lambda) = \omega_{SI}(\lambda) - \frac{c\,(1 - \omega_{SI}(\lambda))}{1 - c + \lambda^2/3}, \qquad \omega_{SI}(\lambda) = \frac c2\sum_n \frac{w_n}{1 + \lambda^2\mu_n^2}.$$

*Proof.* By Theorem 5 of the source iteration proof, $Te = \omega_{SI}e$. So $R = \Sigma_s(\omega_{SI} - 1)e = \hat R\,e$ with $\hat R = \Sigma_s(\omega_{SI} - 1)$. Try the edge values $f_i = F\cos(\theta i)$ for $i = 0, \ldots, M$. All cells have the same $g$ and $s$. Since $\cos(\theta(i - 1)) + \cos(\theta(i + 1)) = 2\cos\theta\cos(\theta i)$, the left side of (1) is
$$F\cos(\theta i)\left[2(g + s) + 2(s - g)\cos\theta\right] = F\cos(\theta i)\left[4g\sin^2(\theta/2) + 4s\cos^2(\theta/2)\right],$$
and since $\cos(\theta(i - \tfrac12)) + \cos(\theta(i + \tfrac12)) = 2\cos(\theta/2)\cos(\theta i)$, the right side is $2h\hat R\cos(\theta/2)\cos(\theta i)$. At the face $i = 0$ both sides are half of these values with $\cos 0 = 1$, and at $i = M$ they are half of them with $\cos(\theta M) = (-1)^k$. So every row holds if
$$F\left[4g\sin^2(\theta/2) + 2\Sigma_ah\cos^2(\theta/2)\right] = 2h\hat R\cos(\theta/2).$$
Since $0 \le \theta < \pi$, $\cos(\theta/2) > 0$ and the bracket is positive, so this fixes $F$. By Theorem 1 (here $\Sigma_a > 0$) it is the solution. The cell correction is $F(\cos(\theta j) + \cos(\theta(j + 1)))/2 = F\cos(\theta/2)\,e_j$. Divide the equation for $F$ by $\cos(\theta/2)$ and use $g = 2/(3\Sigma_th)$:
$$F\cos(\theta/2) = \frac{2h\hat R}{8\tan^2(\theta/2)/(3\Sigma_th) + 2\Sigma_ah} = \frac{\hat R}{\Sigma_t(\lambda^2/3 + 1 - c)} = \frac{c(\omega_{SI} - 1)}{\lambda^2/3 + 1 - c}.$$
Line L7 adds this to $\omega_{SI}e$. $\square$

The $M$ vectors $e$ are orthogonal, so they are all the eigenvectors in this case, and the spectral radius is the largest $|\omega|$ over the $M$ values of $\theta$.

**Corollary (the flat mode).** For $k = 0$, $\lambda = 0$ and $\omega_{SI} = c$, so $\omega = c - c(1 - c)/(1 - c) = 0$. The mode that source iteration damps the least, by the factor $c$, is removed in one step. In particular, in a homogeneous slab with both faces reflecting and a flat source, one DSA iteration from a flat start gives the exact solution.

Write $a(\lambda) = \tfrac12\sum_n w_n/(1 + \lambda^2\mu_n^2)$, so $\omega_{SI} = ca$. A short computation gives the second form
$$\omega(\lambda) = \frac{c\left[a(\lambda)(1 + \lambda^2/3) - 1\right]}{1 - c + \lambda^2/3}. \tag{4}$$
The factor of the diamond difference scheme is the factor of the $S_N$ equations exact in space, evaluated at $\lambda = 2\tan(\theta/2)/(\Sigma_th)$. As $\theta$ runs over $[0, \pi)$, $\lambda$ runs over $[0, \infty)$ for every cell size. As $N \to \infty$, $a(\lambda) \to \arctan(\lambda)/\lambda$, which gives the factor of the continuous problem.

**Theorem 6 (a bound for every cell size).** Let $H_N = \tfrac12\sum_{\mu_n^2 < 1/3} w_n(1/3 - \mu_n^2)$. Then $H_N < 1/3$, and for every $\lambda \ge 0$ and $c \le 1$ (with $\lambda > 0$ if $c = 1$),
$$|\omega(\lambda)| \le 3H_N\,c < c .$$
So consistent DSA on equal cells with reflecting faces converges for every cell thickness $\Sigma_th$, with a rate that does not depend on it.

*Proof.* Since $\tfrac12\sum_n w_n = 1$,
$$a(\lambda)(1 + \lambda^2/3) - 1 = \frac12\sum_n w_n\frac{(1 + \lambda^2/3) - (1 + \lambda^2\mu_n^2)}{1 + \lambda^2\mu_n^2} = \lambda^2\,p(\lambda), \qquad p(\lambda) = \frac12\sum_n w_n\frac{1/3 - \mu_n^2}{1 + \lambda^2\mu_n^2}.$$
The terms with $\mu_n^2 < 1/3$ are positive and at most $\tfrac12 w_n(1/3 - \mu_n^2)$, so $p \le H_N$. The terms with $\mu_n^2 > 1/3$ are negative and at least $-\tfrac12 w_n(\mu_n^2 - 1/3)$. Since the rule is exact for $\mu^2$, $\tfrac12\sum_n w_n(1/3 - \mu_n^2) = 0$, so the sum of the numbers $\tfrac12 w_n(\mu_n^2 - 1/3)$ over $\mu_n^2 > 1/3$ is $H_N$, and $p \ge -H_N$. With (4) and $1 - c + \lambda^2/3 \ge \lambda^2/3$, $|\omega| \le c\lambda^2H_N/(\lambda^2/3) = 3H_Nc$. For $\lambda = 0$ and $c < 1$, $\omega = 0$. Finally, $H_N \le \tfrac13\cdot\tfrac12\sum_{\mu_n^2 < 1/3} w_n \le \tfrac13$, and equality would need all the weight at $\mu = 0$; for $N$ even no node is 0, so $H_N < 1/3$. $\square$

For $N = 2$, $\mu^2 = 1/3$, so $H_2 = 0$ and $\omega \equiv 0$, which agrees with Theorem 4. The values of $3H_N$ are 0.4260 for $S_4$, 0.3799 for $S_8$ and 0.3862 for $S_{16}$, and $2/(3\sqrt3) = 0.3849$ for the continuous rule. The true maximum of $|\omega|$ is smaller. For the continuous factor with $c = 1$, the maximum over a fine grid of $\lambda$ is $0.2247$ near $\lambda = 2.5$; this value is a computation, not part of the theorem.

**Theorem 7 (the inconsistent scheme).** With the same slab and modes, the cell-centered correction of the page (face coefficient $D/h$ between equal cells, no current at a reflecting face) has the eigenvalue
$$\omega_I(\theta) = \omega_{SI}(\lambda) - \frac{c\,(1 - \omega_{SI}(\lambda))}{1 - c + 4\sin^2(\theta/2)/(3\tau^2)}, \qquad \tau = \Sigma_th .$$
If $c > 1/2$ and $\tau > 2/\sqrt{3(2c - 1)}$, then $|\omega_I| > 1$ for $\theta$ close enough to $\pi$, so the iteration diverges on fine enough meshes of thick cells.

*Proof.* The cell row is $\Sigma_ahf_j + (D/h)(2f_j - f_{j-1} - f_{j+1}) = R_jh$ with $D = 1/(3\Sigma_t)$. At a reflecting face the missing neighbor has the same value as the cell, which holds for $e$ because $\cos(-\theta/2) = \cos(\theta/2)$ and $\cos(\theta(M + \tfrac12)) = \cos(\theta(M - \tfrac12))$ for $\theta = \pi k/M$. With $f = \hat fe$ every row becomes $\hat f[\Sigma_ah + 4D\sin^2(\theta/2)/h] = \hat Rh$, so $\hat f = \hat R/(\Sigma_t(1 - c + 4\sin^2(\theta/2)/(3\tau^2)))$, and $\hat R = \Sigma_s(\omega_{SI} - 1)$ as before. As $\theta \to \pi$, $\lambda \to \infty$ and $\omega_{SI} \to 0$ because no node is 0, so $\omega_I \to -c/(1 - c + 4/(3\tau^2))$. This has absolute value greater than 1 exactly when $\tau^2 > 4/(3(2c - 1))$. By continuity, $|\omega_I| > 1$ for $\theta$ near $\pi$, and these values of $\theta = \pi k/M$ occur once $M$ is large. $\square$

Since $4\sin^2(\theta/2)/\tau^2 = \lambda^2\cos^2(\theta/2)$, the two schemes agree for smooth modes, $\theta \to 0$. They differ for the modes that change sign from cell to cell. In thick cells these modes have $\omega_{SI}$ near 0, and the consistent scheme gives them almost no correction while the inconsistent one gives them a correction of nearly $-c/(1 - c)$ times their size. For $c = 0.99$ the threshold is $\tau > 1.1664$.
