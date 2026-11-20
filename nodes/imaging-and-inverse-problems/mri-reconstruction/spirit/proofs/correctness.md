---
title: SPIRiT by CGLS decreases the consistency residual at every step and returns the true k-space when the kernel is consistent with it and the missing samples are determined
proves: [correctness]
status: full
---

The setting is that of the algorithm, in exact arithmetic. The unknown is the full multi-coil k-space $x \in \mathbb{C}^{N}$, $N = c n^2$. The kernel operator $G$ of line L1 is linear, $(Gx)_a(\kappa) = \sum_b \sum_{d} g[a][b][d]\, x_b(\kappa + d)$ with $g[a][a][(0,0)] = 0$. $P$ selects the missing samples, so $P^{\mathsf T} z$ puts a vector $z$ of missing values into a k-space that is zero on the acquired samples. $x_0$ is the data with zeros on the missing samples (line L2). Line L3 defines $B = (G - I) P^{\mathsf T}$, with the adjoint $B^H = P (G^H - I)$. Let $r_0 = -(G - I) x_0$ (line L4). The method minimizes

$$\phi(z) = \lVert (G - I)(x_0 + P^{\mathsf T} z) \rVert^2 = \lVert B z - r_0 \rVert^2$$

by CGLS: $z_0 = 0$, $s_0 = p_0 = B^H r_0$, and for each step $q_t = B p_t$ (line L6), $\alpha_t = \lVert s_t \rVert^2 / \lVert q_t \rVert^2$ (line L7), $z_{t+1} = z_t + \alpha_t p_t$ and $r_{t+1} = r_t - \alpha_t q_t$ (line L8), $s_{t+1} = B^H r_{t+1}$ and $p_{t+1} = s_{t+1} + (\lVert s_{t+1}\rVert^2/\lVert s_t \rVert^2) p_t$ (line L9). The output is $x_0 + P^{\mathsf T} z$ (line L10).

**Theorem.**
1. The residual $r_t = r_0 - B z_t$ satisfies $\lVert r_{t+1} \rVert \le \lVert r_t \rVert$ for every step, and $z_t$ minimizes $\phi$ over the Krylov subspace $\mathcal{K}_t = \operatorname{span}\{b, Ab, \ldots, A^{t-1} b\}$ with $A = B^H B$ and $b = B^H r_0$.
2. After at most $M$ steps, where $M$ is the number of missing samples, $z_t$ minimizes $\phi$ over $\mathbb{C}^M$.
3. Let $k$ be the true full k-space, equal to the data on the acquired samples. If $G k = k$, then $z^\dagger = P k$ is a minimizer with $\phi(z^\dagger) = 0$. If moreover $B$ has full column rank, that is, no nonzero k-space that vanishes on the acquired samples satisfies $G v = v$, then $z^\dagger$ is the only minimizer, and the method returns $k$ after at most $M$ steps.

*Proof of 1 and 2.* The recurrences are those of the conjugate gradient method for $A z = b$, with the residual $s_t = b - A z_t = B^H r_t$ and $\langle p_t, A p_t \rangle = \lVert B p_t \rVert^2 = \lVert q_t \rVert^2$; the identity $s_t = B^H r_t$ holds by induction, since $B^H r_{t+1} = B^H r_t - \alpha_t A p_t$. The vector $b$ lies in the range of $B^H$, which is the range of $A$, and so does every Krylov vector. On that range, $A$ is positive definite. The lemma in the [CG-SENSE proof](/cg-sense/), restricted to the range of $A$, shows that the residuals $s_t$ are mutually orthogonal and that $z_t$ minimizes $(z - z^\star)^H A (z - z^\star) = \lVert B(z - z^\star) \rVert^2$ over $\mathcal{K}_t$, where $z^\star$ is the least squares solution in the range of $A$. For any $z$,

$$\phi(z) = \lVert B(z - z^\star) \rVert^2 + \lVert B z^\star - r_0 \rVert^2,$$

because $B z^\star - r_0$ is orthogonal to the range of $B$ (the normal equations). So $z_t$ also minimizes $\phi$ over $\mathcal{K}_t$, and since $\mathcal{K}_t \subseteq \mathcal{K}_{t+1}$, $\phi(z_{t+1}) \le \phi(z_t)$, which is $\lVert r_{t+1} \rVert \le \lVert r_t \rVert$. The nonzero orthogonal residuals $s_t$ are at most $M$ in number, so some $s_t$ with $t \le M$ is 0. Then $z_t$ solves the normal equations and minimizes $\phi$ over $\mathbb{C}^M$. $\square$

*Proof of 3.* Since $k = x_0 + P^{\mathsf T} P k$, we get $\phi(P k) = \lVert (G - I) k \rVert^2 = 0$, the least value of $\phi$. If $B$ has full column rank, $\phi$ is strictly convex and has one minimizer. By part 2 the method finds it, and line L10 returns $x_0 + P^{\mathsf T} P k = k$. $\square$

**Lemma (a consistent kernel exists).** Assume the coil k-space satisfies the model (H1) of the [GRAPPA proof](/grappa/): $x_b(\kappa) = \sum_{e \in H} h_b(e) X(\kappa - e)$ for a finite $H$. If for every coil $a$ the target $x_a(\kappa)$ lies in the span of the other patch entries as functions of the object samples, and the calibration patches contain enough independent object patterns (full column rank of the matrix of object samples), then every exact solution of the fit of line L1 satisfies $G k = k$ on the whole k-space.

*Proof.* This is the argument of the GRAPPA proof with the sources $\{(b, d) : d \text{ in the patch}\} \setminus \{(a, (0,0))\}$ for target coil $a$: an exact kernel exists, the fit has the value 0, every solution agrees with an exact kernel on the object samples, and so it predicts every $x_a(\kappa)$ exactly. $\square$

**Remarks.**
- The condition on $B$ in part 3 can fail even with a consistent kernel. For the band maps of the tests on a $32 \times 32$ grid with uniform sampling at $R = 3$, the residual fell to $4 \times 10^{-7}$ while the error stayed at 0.36, so $B$ was singular or nearly so; random sampling of the same maps on a $16 \times 16$ grid left the error at 0.14 (measurements). Uniform sampling with $R = 2$ gave the exact answer.
- With the small Tikhonov term of the code, the kernel is close to an exact one, and the result has a small error.
- Part 1 is a monotonicity theorem for the consistency residual only. The error against the true k-space is not proved monotone, and the tests do not check it.
- CGLS and LSQR give the same iterates in exact arithmetic. With noisy data the objective treats the acquired samples as exact; Lustig and Pauly (2010) also give a form with a data weight.
