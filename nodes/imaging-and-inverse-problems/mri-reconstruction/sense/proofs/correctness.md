---
title: SENSE recovers the image exactly when every unfolding matrix has full column rank, and its g-factor is at least 1
proves: [correctness]
status: full
---

The setting is that of the algorithm. The image $x$ and the coil maps $s_1, \ldots, s_c$ are $n \times n$ arrays, indexed $(i, j)$ with $i$ the phase encoding axis. The k-space of coil $k$ is $F_u(s_k x)$, where $F_u = F/n$ is the unitary 2D DFT, $(F_u f)(\kappa, l) = n^{-1} \sum_{i, j} f(i, j)\, e^{-2\pi i (\kappa i + l j)/n}$. The reduction factor $R$ divides $n$, $m = n/R$, and the scan keeps the rows $\kappa = R \kappa'$ for $\kappa' = 0, \ldots, m - 1$. Line L2 forms, for each coil, $n$ times the inverse DFT of size $m \times n$ of the kept rows:

$$a_k(i, j) = \frac{n}{m n} \sum_{\kappa'=0}^{m-1} \sum_{l=0}^{n-1} y_k(R\kappa', l)\, e^{2\pi i (\kappa' i/m + l j/n)}, \qquad 0 \le i < m.$$

For a folded pixel $(i, j)$ the unfolding matrix $E$ is the $c \times R$ matrix with $E[k][p] = s_k(i + p m, j)$, and $v_p = x(i + pm, j)$.

**Theorem.** Let $\Psi$ be Hermitian positive definite (the identity when no covariance is given) and $\lambda = 0$. If $E$ has full column rank $R$ at every folded pixel, which needs $R \le c$, and the data have no noise, then SENSE returns $x$. If the k-space samples carry noise that is independent between samples, with zero mean and covariance $\Psi$ between the coils at each sample, the output at pixel $i + pm$ has the noise variance $R\,[(E^H \Psi^{-1} E)^{-1}]_{pp}$, and the g-factor $g_p = \sqrt{[(E^H \Psi^{-1} E)^{-1}]_{pp}\, [E^H \Psi^{-1} E]_{pp}}$ is at least 1.

**Lemma 1 (folding).** Without noise, $a_k(i, j) = \sum_{p=0}^{R-1} s_k(i + pm, j)\, x(i + pm, j) = (E v)_k$.

*Proof.* Write $f = s_k x$. For a kept row, $y_k(R\kappa', l) = n^{-1} \sum_{i'', j'} f(i'', j')\, e^{-2\pi i (\kappa' i''/m + l j'/n)}$, because $R \kappa' i''/n = \kappa' i''/m$. Write $i'' = i' + p m$ with $0 \le i' < m$; then $e^{-2\pi i \kappa' i''/m} = e^{-2\pi i \kappa' i'/m}$, so the kept rows are $n^{-1}$ times the DFT of size $m \times n$ of the folded array $\phi(i', j') = \sum_p f(i' + pm, j')$. The inverse DFT of size $m \times n$ gives back $n^{-1} \phi$, and the factor $n$ in line L2 gives $\phi$. $\square$

**Lemma 2.** With $\Psi = L L^H$ (Cholesky), lines L6 and L7 solve the weighted least squares problem $\min_v (a - Ev)^H \Psi^{-1} (a - Ev)$. If $E$ has full column rank, the solution is unique and is $v^\star = (E^H \Psi^{-1} E)^{-1} E^H \Psi^{-1} a$.

*Proof.* Line L6 replaces $E$ and $a$ by $L^{-1}E$ and $L^{-1}a$, and $\lVert L^{-1}(a - Ev) \rVert^2 = (a - Ev)^H \Psi^{-1}(a - Ev)$. The normal equations of this least squares problem are $E^H \Psi^{-1} E\, v = E^H \Psi^{-1} a$, which line L7 forms and solves. If $E$ has full column rank and $\Psi^{-1}$ is positive definite, then $w^H E^H \Psi^{-1} E w = \lVert L^{-1} E w \rVert^2 > 0$ for $w \ne 0$, so the matrix is positive definite and the solution is unique. $\square$

*Proof of the theorem.* Exactness. By Lemma 1, $a = E v$ at each folded pixel, so $a - E v = 0$ and $v$ minimizes the objective of Lemma 2 with the value 0. The minimizer is unique, so line L7 returns $v$, and line L8 writes $x(i + pm, j)$ for $p = 0, \ldots, R - 1$. The folded pixels $(i, j)$ with $0 \le i < m$ and the offsets $p$ cover every pixel exactly once, so the output is $x$. A $c \times R$ matrix has rank at most $\min(c, R)$, so full column rank needs $R \le c$.

Noise. The map from the kept samples to $a_k(i, j)$ is $(1/m)$ times a sum over the $m n$ kept samples with weights of modulus 1. For independent samples with covariance $\Psi$ between the coils, the folded noise vector at a pixel has the covariance $m n \cdot m^{-2}\, \Psi = R \Psi$. The output is $v^\star = H a$ with $H = (E^H \Psi^{-1} E)^{-1} E^H \Psi^{-1}$, so its noise covariance is $H (R\Psi) H^H = R\,(E^H \Psi^{-1} E)^{-1}$, and the variance at pixel $i + pm$ is the diagonal entry $p$.

g-factor. Let $M = E^H \Psi^{-1} E$, positive definite, and $e_p$ the unit vector. By the Cauchy-Schwarz inequality,

$$1 = (e_p^H e_p)^2 = \bigl|(M^{1/2} e_p)^H (M^{-1/2} e_p)\bigr|^2 \le (e_p^H M e_p)(e_p^H M^{-1} e_p) = [M]_{pp}\,[M^{-1}]_{pp},$$

so $g_p \ge 1$. Equality holds if and only if $M^{1/2} e_p$ and $M^{-1/2} e_p$ are parallel, that is, $M e_p$ is a multiple of $e_p$: column $p$ of $E$ is orthogonal to the other columns in the inner product $\langle u, w \rangle = u^H \Psi^{-1} w$. $\square$

**Remarks.**
- With full sampling ($R = 1$) the same model gives the variance $1/[M]_{pp}$, the variance of the optimal coil combination at that pixel. The ratio of the two signal to noise ratios is therefore $\sqrt{R}\, g_p$, which is the formula of Pruessmann et al. (1999).
- With $\lambda > 0$, line L7 solves $(M + \lambda I) v = E^H \Psi^{-1} a$, a Tikhonov problem. Its output is biased, and the theorem does not apply.
- The theorem is about the discrete model $y_k = M F_u(s_k x)$ with known maps. Errors in the maps, a field of view smaller than the object, and motion are outside it.
