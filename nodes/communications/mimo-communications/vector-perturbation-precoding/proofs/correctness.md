---
title: Vector perturbation removes the interference, meets the power exactly, lets each user recover its symbol by a modulo, and the search finds the perturbation of least power
proves: [correctness]
status: full
---

The model is $y_k = h_k^H x + w_k$ for $k = 1, \ldots, K$, with $H = [h_1, \ldots, h_K]^H \in \mathbb{C}^{K \times M}$ of full row rank and $w_k \sim \mathcal{CN}(0, N_0)$. The data symbols $s_k$ have real and imaginary parts in $[-\tau/2, \tau/2)$. Lines L1 to L7 compute $F = H^H (H H^H)^{-1}$, $A = (H H^H)^{-1}$, the Cholesky factor of the real form of $A$, a vector $l$ of Gaussian integers, $u = s + \tau l$, $\gamma = \|F u\|^2$ and $x = \sqrt{P / \gamma}\, F u$. Line L8 at user $k$ computes $\mathrm{mod}_\tau(\sqrt{\gamma / P}\, y_k)$, where $\mathrm{mod}_\tau$ reduces the real and the imaginary part separately into $[-\tau/2, \tau/2)$ by $t \mapsto t - \tau \lfloor t / \tau + 1/2 \rfloor$.

**Lemma 1 (no interference, exact power).** For every $l$, $\|x\|^2 = P$ and $H x = \sqrt{P / \gamma}\, (s + \tau l)$.

*Proof.* $\|x\|^2 = (P / \gamma) \|F u\|^2 = P$. Also $H F = H H^H (H H^H)^{-1} = I$, so $H x = \sqrt{P / \gamma}\, u$. $\square$

So user $k$ receives $y_k = \sqrt{P / \gamma}\, (s_k + \tau l_k) + w_k$, with no signal for the other users.

**Lemma 2 (the modulo receiver).** If $w_k = 0$, line L8 returns $s_k$. With noise, it returns $\mathrm{mod}_\tau(s_k + \sqrt{\gamma / P}\, w_k)$.

*Proof.* Line L8 forms $s_k + \tau l_k + \sqrt{\gamma / P}\, w_k$. The map $t \mapsto t - \tau \lfloor t / \tau + 1/2 \rfloor$ does not change when an integer multiple of $\tau$ is added to $t$, because the floor then grows by the same integer. So the term $\tau l_k$, whose real and imaginary parts are integer multiples of $\tau$, drops out. If $t \in [-\tau/2, \tau/2)$, then $t / \tau + 1/2 \in [0, 1)$, the floor is 0, and the map returns $t$. So with $w_k = 0$ the result is $s_k$. $\square$

So the noise at user $k$ is scaled by $\sqrt{\gamma / P}$, and the effective SNR is $P / (\gamma N_0)$. A smaller $\gamma$ is better for every user at once. The rest of the proof shows that lines L2 to L4 find the $l$ with the smallest $\gamma$.

**Lemma 3 (the power as a quadratic form).** $\gamma = u^H A u$ with $A = (H H^H)^{-1}$, which is Hermitian positive definite.

*Proof.* $F^H F = (H H^H)^{-1} H H^H (H H^H)^{-1} = A$, so $\|F u\|^2 = u^H F^H F u = u^H A u$. $H H^H$ is positive definite because $H$ has full row rank, so its inverse is too. $\square$

**Lemma 4 (the real form).** Let $A = A_R + j A_I$ and $A_r = \begin{pmatrix} A_R & -A_I \\ A_I & A_R \end{pmatrix}$. For $u = a + j b$ and $v = (a, b)$, $u^H A u = v^T A_r v$. The matrix $A_r$ is symmetric positive definite, so $A_r = L L^T$ for a real lower triangular $L$ with a positive diagonal, and $u^H A u = \|R v\|^2$ with the upper triangular $R = L^T$.

*Proof.* $A$ Hermitian means $A_R^T = A_R$ and $A_I^T = -A_I$, so $A_r$ is symmetric. Expand $u^H A u = (a - j b)^T (A_R + j A_I)(a + j b)$. Its real part is $a^T A_R a + b^T A_R b - a^T A_I b + b^T A_I a$, which is $v^T A_r v$, and its imaginary part is 0 because $u^H A u$ is real. For $v \ne 0$, $v^T A_r v = u^H A u > 0$. The Cholesky factorization of a symmetric positive definite matrix exists, and the helper computes it with the real entries of $A_r$. $\square$

With $l = c + j d$ and the integer vector $z = (c, d) \in \mathbb{Z}^{2K}$, $u$ maps to $v + \tau z$, so the problem of lines L2 to L4 is to minimize

$$\Phi(z) = \|R (v + \tau z)\|^2 = \sum_{i=1}^{n} \Bigl( r_{ii} (v_i + \tau z_i) + \sum_{j > i} r_{ij} (v_j + \tau z_j) \Bigr)^2, \qquad n = 2K,$$

over $z \in \mathbb{Z}^n$. Term $i$ depends only on $z_i, \ldots, z_n$.

**Theorem 1 (the search is exact).** The Schnorr-Euchner search of line L4 stops after a finite number of steps and returns a $z$ with $\Phi(z) = \min_{z' \in \mathbb{Z}^n} \Phi(z')$. The minimum exists.

*Proof.* The minimum exists: $\Phi(z) \ge \lambda \tau^2 \|z + v / \tau\|^2$ with $\lambda > 0$ the smallest eigenvalue of $R^T R$, so only finitely many $z$ have $\Phi(z) \le \Phi(0)$.

Fix values $z_{i+1}, \ldots, z_n$ and let $D_i$ be the sum of the terms $i+1, \ldots, n$ for them (the argument `partial`). Term $i$ is $(r_{ii} \tau)^2 (z_i - c_i)^2$ with the center $c_i = (-t_i / r_{ii} - v_i) / \tau$, where $t_i = \sum_{j > i} r_{ij} (v_j + \tau z_j)$. The search visits $z_i = \lfloor c_i + 1/2 \rfloor$ first and then alternates to the two sides. In this order $|z_i - c_i|$ never decreases, so the value $d = D_i + (r_{ii} \tau)^2 (z_i - c_i)^2$ never decreases.

*Pruning is safe.* All terms are nonnegative, so every completion of a prefix has $\Phi \ge d$. The loop at level $i$ stops at the first candidate with $d \ge$ best, and every later candidate at that level has a $d$ at least as large. So every leaf that is skipped has $\Phi \ge$ best at that time, and best only decreases. Every leaf that is not skipped is compared with best. So at the end, best is at most $\Phi(z')$ for every $z' \in \mathbb{Z}^n$, and it is the value of the stored leaf.

*Termination.* The first call at each level starts while best may be $\infty$; it then never stops at its first candidate, so the first path goes to a leaf and best becomes finite. After that, the loop at level $i$ visits only candidates with $(r_{ii} \tau)^2 (z_i - c_i)^2 < $ best, and there are finitely many, because $r_{ii} \tau > 0$. By induction on the depth, every call returns. $\square$

**Theorem 2 (correctness of vector perturbation).** The transmit signal has power exactly $P$, user $k$ sees no signal for the other users, without noise it recovers $s_k$ exactly, and the effective SNR $P / (\gamma N_0)$ is the largest over all Gaussian integer perturbations $l$.

*Proof.* Lemma 1 gives the power and the absence of interference, and Lemma 2 gives the recovery. By Lemmas 3 and 4, $\gamma(l) = \Phi(z)$ for $l = c + j d$, $z = (c, d)$, and Theorem 1 shows that line L4 minimizes $\Phi$ over $\mathbb{Z}^{2K}$, that is over all Gaussian integer vectors $l$. $\square$

With $l = 0$ the precoder is zero forcing with channel inversion, so $\gamma_{\mathrm{VP}} \le \gamma_{\mathrm{ZF}}$ for every channel and data vector.

The tests check Lemma 1 within $10^{-9}$, Lemma 2 without noise, Lemma 4 on random Hermitian matrices, Theorem 1 against a search over a box of integer vectors for $K = 1, 2, 3$ (the search result lies in the box, so the two minima must agree), $\gamma_{\mathrm{VP}} \le \gamma_{\mathrm{ZF}}$, and the example of the page.
