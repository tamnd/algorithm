---
title: The spectral filter removes the largest scores, and the top direction of a poisoned mixture follows the mean shift
proves: [correctness]
status: full
---

**Claim 1 (the computation).** Let $M$ be the $n \times d$ matrix with rows $R_i - \hat\mu$, where $\hat\mu$ is the mean of line L1. Line L2 computes $C = \sum_i (R_i - \hat\mu)(R_i - \hat\mu)^\top = M^\top M$. If $M = U S V^\top$ is a singular value decomposition, then $M^\top M = V S^2 V^\top$, so the right singular vectors of $M$ are the eigenvectors of $C$, and the top right singular vector is a unit eigenvector of the largest eigenvalue $s_1^2$. Line L3 returns such a vector. Power iteration converges to it when $s_1^2 > 0$ is simple and the start has a nonzero component on it. The code first forms $P = C^m / \phi$ with $m = 2^8$ by repeated squaring, where $\phi > 0$ is a scale that only avoids overflow; $P$ has the same eigenvectors as $C$, with eigenvalues $s_k^{2m}/\phi$. One column $P e_j$ can be orthogonal to the top eigenvector $v_1$, but not all of them: $\sum_j (v_1^\top P e_j)^2 = \lVert P v_1 \rVert^2 = (s_1^{2m}/\phi)^2 > 0$. The code runs power iteration on $C$ from every nonzero column of $P$ and keeps the result with the largest Rayleigh quotient $v^\top C v$. The run from a column with a nonzero component on $v_1$ reaches $s_1^2$, and no unit vector exceeds it, so the kept vector is a top eigenvector. If $C = 0$, every vector is one, and the code returns $e_1$. Line L4 gives $\tau_i = ((Mv)_i)^2$, which does not depend on the sign of $v$. Lines L5 and L6 sort by $\tau$ in decreasing order and remove the first $k$, so every removed score is at least every kept score, and exactly $k$ indices are removed. $\square$

**Setting for Claims 2 and 3.** $F = (1 - \epsilon) D + \epsilon W$ with $0 < \epsilon < 1$, where $D$ and $W$ have means $\mu_D, \mu_W$ and covariances $\Sigma_D, \Sigma_W$ with $0 \preceq \Sigma_D, \Sigma_W \preceq \sigma^2 I$. Write $\Delta = \mu_W - \mu_D$, $\mu = \mu_F = \mu_D + \epsilon \Delta$, and let $v$ be a unit eigenvector of the largest eigenvalue $\lambda$ of $\Sigma_F$.

**Claim 2.** $\Sigma_F = (1 - \epsilon)\Sigma_D + \epsilon \Sigma_W + \epsilon(1 - \epsilon)\Delta\Delta^\top$, and $\langle v, \Delta \rangle^2 \ge \lVert \Delta \rVert^2 - \sigma^2 / (\epsilon(1 - \epsilon))$.

*Proof.* Let $Z \in \{D, W\}$ be the component of a draw $x$ from $F$. By the law of total covariance, $\Sigma_F = \mathbb{E}[\mathrm{Cov}(x \mid Z)] + \mathrm{Cov}(\mathbb{E}[x \mid Z])$. The first term is $(1 - \epsilon)\Sigma_D + \epsilon\Sigma_W$. The vector $\mathbb{E}[x \mid Z]$ is $\mu_D$ with probability $1 - \epsilon$ and $\mu_W$ with probability $\epsilon$; its mean is $\mu$, and its covariance is $(1 - \epsilon)(\epsilon\Delta)(\epsilon\Delta)^\top + \epsilon((1 - \epsilon)\Delta)((1 - \epsilon)\Delta)^\top = \epsilon(1 - \epsilon)\Delta\Delta^\top$, because $\mu_D - \mu = -\epsilon\Delta$ and $\mu_W - \mu = (1 - \epsilon)\Delta$. This proves the formula.

If $\Delta = 0$ the inequality says $0 \ge -\sigma^2/(\epsilon(1-\epsilon))$, which holds. Otherwise let $u = \Delta / \lVert \Delta \rVert$. Since $v$ maximizes the quadratic form of $\Sigma_F$ over unit vectors,

$$\lambda = v^\top \Sigma_F v \ \ge\ u^\top \Sigma_F u \ \ge\ \epsilon(1 - \epsilon)\lVert \Delta \rVert^2,$$

because $u^\top((1 - \epsilon)\Sigma_D + \epsilon\Sigma_W)u \ge 0$. On the other hand, $v^\top((1 - \epsilon)\Sigma_D + \epsilon\Sigma_W)v \le (1 - \epsilon)\sigma^2 + \epsilon\sigma^2 = \sigma^2$, so

$$\lambda \ \le\ \sigma^2 + \epsilon(1 - \epsilon)\langle v, \Delta \rangle^2 .$$

Together, $\epsilon(1 - \epsilon)\langle v, \Delta\rangle^2 \ge \epsilon(1 - \epsilon)\lVert\Delta\rVert^2 - \sigma^2$, and dividing by $\epsilon(1 - \epsilon) > 0$ gives the claim. $\square$

**Claim 3.** If moreover $\epsilon < 1/2$ and $\lVert \Delta \rVert^2 \ge 6\sigma^2/\epsilon$, let $a = \lvert\langle v, \Delta\rangle\rvert$ and $t = a/2$. Then

$$\Pr_{x \sim D}\big[\lvert\langle x - \mu, v\rangle\rvert \ge t\big] \le \frac{\epsilon}{(1 - 2\epsilon)^2}, \qquad \Pr_{x \sim W}\big[\lvert\langle x - \mu, v\rangle\rvert \le t\big] \le \frac{\epsilon}{(1 - 2\epsilon)^2}.$$

*Proof.* Since $\epsilon \le 1/2$, $1 - \epsilon \ge 1/2$, so $\sigma^2/(\epsilon(1 - \epsilon)) \le 2\sigma^2/\epsilon \le \lVert\Delta\rVert^2/3$. By Claim 2, $a^2 \ge \lVert\Delta\rVert^2 - \lVert\Delta\rVert^2/3 = \tfrac{2}{3}\lVert\Delta\rVert^2 \ge 4\sigma^2/\epsilon$. In particular $a > 0$ when $\sigma > 0$; if $\sigma = 0$ both distributions are points, $a^2 \ge \tfrac{2}{3}\lVert\Delta\rVert^2$, and the claim is checked directly below with zero variance (if also $\Delta = 0$, the hypothesis $\lVert\Delta\rVert^2 \ge 0$ holds trivially and the claim is not meaningful, so assume $\Delta \ne 0$).

*Clean points.* For $x \sim D$, $x - \mu = (x - \mu_D) - \epsilon\Delta$, so $\lvert\langle x - \mu, v\rangle\rvert \le \lvert\langle x - \mu_D, v\rangle\rvert + \epsilon a$. If the left side is at least $t = a/2$, then $\lvert\langle x - \mu_D, v\rangle\rvert \ge (1/2 - \epsilon)a > 0$. The variable $\langle x - \mu_D, v\rangle$ has mean $0$ and variance $v^\top\Sigma_D v \le \sigma^2$, so by Chebyshev's inequality this has probability at most

$$\frac{\sigma^2}{(1/2 - \epsilon)^2 a^2} \ \le\ \frac{\sigma^2 \epsilon}{(1/2 - \epsilon)^2 \cdot 4\sigma^2} \ =\ \frac{\epsilon}{(1 - 2\epsilon)^2}.$$

*Poisoned points.* For $x \sim W$, $x - \mu = (x - \mu_W) + (1 - \epsilon)\Delta$, so $\lvert\langle x - \mu, v\rangle\rvert \ge (1 - \epsilon)a - \lvert\langle x - \mu_W, v\rangle\rvert$. If the left side is at most $a/2$, then $\lvert\langle x - \mu_W, v\rangle\rvert \ge (1/2 - \epsilon)a$, and the same Chebyshev bound with $v^\top\Sigma_W v \le \sigma^2$ applies. (When $\sigma = 0$, the variables $\langle x - \mu_D, v\rangle$ and $\langle x - \mu_W, v\rangle$ are $0$ almost surely, and both probabilities are $0$ because $(1/2 - \epsilon)a > 0$.) $\square$

**Remarks.** Squaring the projection, as line L4 does, keeps the order, so the threshold $t$ on $\lvert\langle x - \mu, v\rangle\rvert$ is the threshold $t^2$ on the score. Claims 2 and 3 are about the population covariance $\Sigma_F$ and the population mean $\mu$; the algorithm uses $\hat\mu$ and $C/n$, and the step from the population to a finite sample is not proved here. The removal of $\lfloor 1.5\,\epsilon n\rfloor$ points in place of a threshold is the tuned heuristic of Tran et al.; the claims say only that a threshold exists that separates most clean points from most poisoned ones. $\blacksquare$
