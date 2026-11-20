---
title: The EP updates match moments, the sites stay proper, the first iterate is the linear MMSE estimate, and the marginals are exact on orthogonal channels
proves: [correctness]
status: full
---

The model is the real form $y_r = H_r x_r + w_r$ of the page, with $d$ real symbols in the alphabet $\mathcal{A}$, $w_r \sim \mathcal{N}(0, \sigma^2 I)$ and $e_s$ the mean of $a^2$ over $\mathcal{A}$. Write $G = H_r^T H_r$ and $b = H_r^T y_r$. The lines L1 to L9 are those of the pseudocode on the page. A Gaussian factor $\exp(\gamma x - \Lambda x^2/2)$ is written in natural parameters $(\gamma, \Lambda)$. For $\Lambda > 0$ it is proportional to $\mathcal{N}(x; \gamma/\Lambda, 1/\Lambda)$. This file claims only the results below. It does not claim that EP converges in general or that it finds the ML vector; the page shows a case where it does not.

## Lemma 1 (the sites stay positive and $q$ exists)

At every point of the algorithm, $\Lambda_i > 0$ for all $i$, and $A = G/\sigma^2 + \mathrm{diag}(\Lambda)$ is positive definite. If column $i$ of $H_r$ is not zero, the cavity precision $1/\Sigma_{ii} - \Lambda_i$ is positive.

*Proof.* Line L1 sets $\Lambda_i = 1/e_s > 0$. Line L7 changes $\Lambda_i$ only when $\Lambda' > 0$, and then to $\beta \Lambda' + (1 - \beta) \Lambda_i$ with $\beta \in (0, 1]$, a convex combination of two positive numbers. So $\Lambda_i > 0$ always, by induction. For $v \ne 0$, $v^T A v = \|H_r v\|^2/\sigma^2 + \sum_j \Lambda_j v_j^2 > 0$, so $A$ is positive definite and $\Sigma = A^{-1}$ exists.

For the cavity, let $A_{-i}$ be $A$ with $\Lambda_i$ replaced by 0. By the Schur complement, $1/\Sigma_{ii} = A_{ii} - a^T B^{-1} a$, where $B$ is $A$ without row and column $i$ and $a$ is column $i$ of $A$ without its entry $i$. The same formula for $A_{-i}$ has the same $B$ and $a$ and the entry $A_{ii} - \Lambda_i$. So $1/\Sigma_{ii} - \Lambda_i$ is the Schur complement of $B$ in $A_{-i}$. It is positive if $A_{-i}$ is positive definite. Now $v^T A_{-i} v = \|H_r v\|^2/\sigma^2 + \sum_{j \ne i} \Lambda_j v_j^2$, which is 0 only if $v_j = 0$ for $j \ne i$ and $v_i H_r e_i = 0$. When column $i$ is not zero, this forces $v = 0$. $\square$

## Theorem 2 (the cavity and the moment-matching site)

Line L4 gives the Gaussian $\mathcal{N}(t_i, h_i^2)$ proportional to $q_i(x_i) / s_i(x_i)$, where $q_i = \mathcal{N}(\mu_i, \Sigma_{ii})$ is the marginal of $q$ and $s_i$ is site $i$. If site $i$ is replaced by the site $(\gamma', \Lambda')$ of line L6, with no damping, the new marginal of $q$ for $x_i$ is $\mathcal{N}(\mu_p, \sigma_p^2)$, the Gaussian with the mean and variance of the tilted distribution $\propto \mathcal{N}(a; t_i, h_i^2)$ on $\mathcal{A}$.

*Proof.* In natural parameters, dividing Gaussian factors subtracts parameters. The marginal $q_i$ has $(\mu_i / \Sigma_{ii}, 1/\Sigma_{ii})$. So the cavity has the precision $1/\Sigma_{ii} - \Lambda_i$, which is positive by Lemma 1, and the linear term $\mu_i/\Sigma_{ii} - \gamma_i$. Its variance is $h_i^2 = 1/(1/\Sigma_{ii} - \Lambda_i) = \Sigma_{ii}/(1 - \Sigma_{ii}\Lambda_i)$, and its mean is $h_i^2 (\mu_i/\Sigma_{ii} - \gamma_i) = t_i$, as in line L4.

The density $q$ is proportional to the likelihood times all sites. Write it as $q(x) \propto s_i(x_i)\, r(x)$, where $r$ collects the likelihood and the other sites. Then the marginal of $q$ is $q_i(x_i) \propto s_i(x_i) \int r(x)\, dx_{-i}$, so $\int r\, dx_{-i} \propto q_i / s_i$, the cavity. Replacing $s_i$ by a new site $s_i'$ does not change $r$, so the new marginal is proportional to $s_i'(x_i) \cdot \mathcal{N}(x_i; t_i, h_i^2)$. With $s_i'$ of parameters $(\mu_p/\sigma_p^2 - t_i/h_i^2,\; 1/\sigma_p^2 - 1/h_i^2)$, the product has the parameters $(\mu_p/\sigma_p^2, 1/\sigma_p^2)$, which is $\mathcal{N}(\mu_p, \sigma_p^2)$. These are the formulas of line L6. $\square$

A negative $\Lambda'$ can make the joint $q$ improper, because the proof of Lemma 1 then fails, and then the marginal of $q$ is not defined. That is why line L7 keeps the old site in that case. Among all Gaussians, $\mathcal{N}(\mu_p, \sigma_p^2)$ minimizes the [Kullback-Leibler divergence](/kullback-leibler-divergence/) from the tilted distribution, which is the general EP rule (Minka 2001).

## Theorem 3 (the first iterate is the linear MMSE estimate)

On the first pass of line L3, $\mu = (G + (\sigma^2/e_s) I)^{-1} b$. For the real form of a complex model with square QAM, this is the real form of $(H^H H + (N_0/E_s) I)^{-1} H^H y$.

*Proof.* Line L1 gives $\gamma = 0$ and $\Lambda = (1/e_s) \mathbf{1}$. So $\mu = (G/\sigma^2 + I/e_s)^{-1} b/\sigma^2 = (G + (\sigma^2/e_s) I)^{-1} b$. For the complex model, $\sigma^2 = N_0/2$ and $e_s = E_s/2$, since the real and imaginary parts of a square QAM point are independent and share the energy equally. So $\sigma^2/e_s = N_0/E_s$. The map $C \mapsto C_r = \begin{pmatrix} \mathrm{Re}\, C & -\mathrm{Im}\, C \\ \mathrm{Im}\, C & \mathrm{Re}\, C \end{pmatrix}$ respects sums and products, sends $C^H$ to $C_r^T$ and the identity to the identity, and acts on vectors by stacking the real and imaginary parts in the same way. So $G = (H^H H)_r$, $b$ is the stacked $H^H y$, and $(H^H H + c I)_r^{-1} = ((H^H H + c I)^{-1})_r$. Hence $\mu$ is the stacked $(H^H H + (N_0/E_s) I)^{-1} H^H y$. $\square$

The test checks this within $10^{-9}$ on five channels with $n = 4$ and $m = 6$. The MMSE detector of the [MMSE page](/mmse-mimo-detector/) rounds this estimate, after a bias correction that does not change the signs. For a constellation with more than two levels per dimension, the bias correction can change the decision, so EP with $T = 0$ equals the MMSE detector without that correction.

## Theorem 4 (fixed points match moments)

Suppose that in an iteration with $\beta \in (0, 1]$, every site was kept ($\Lambda' > 0$) and no site changed. Then for every $i$, the marginal of $q$ for $x_i$ has the mean and variance of its tilted distribution.

*Proof.* No change with $\beta > 0$ means $\Lambda' = \Lambda_i$ and $\gamma' = \gamma_i$ for every $i$. All sites in the iteration were computed from the same $q$, so by Theorem 2 the marginal of $q$ divided by the cavity is the site $(\gamma', \Lambda') = (\gamma_i, \Lambda_i)$. So the marginal is the cavity times the site, which by the proof of Theorem 2 is $\mathcal{N}(\mu_p, \sigma_p^2)$. $\square$

The floor $\varepsilon$ of line L5 changes $\sigma_p^2$ only when it is below $\varepsilon$. In that case the statement holds with $\sigma_p^2$ replaced by $\varepsilon$.

## Theorem 5 (exact marginals on orthogonal channels)

Suppose $G = \mathrm{diag}(g_1, \dots, g_d)$ with all $g_i > 0$, and $\sigma^2 / g_i > \max_{a \in \mathcal{A}} a^2$ for every $i$. Then every update of line L7 is kept, and as $T \to \infty$ the mean and variance of each marginal of $q$ converge to the mean and variance of $x_i$ under the exact posterior. With $\beta = 1$ they are equal after one iteration (ignoring the floor $\varepsilon$).

*Proof.* With $G$ diagonal, $A$ is diagonal, so $\Sigma_{ii} = 1/(g_i/\sigma^2 + \Lambda_i)$ and $\mu_i = \Sigma_{ii}(b_i/\sigma^2 + \gamma_i)$. Then line L4 gives $h_i^2 = \sigma^2/g_i$ and $t_i = b_i/g_i$, whatever the sites are.

The exact posterior factorizes. Indeed, $\|y_r - H_r x\|^2 = \|y_r\|^2 - 2 b^T x + \sum_i g_i x_i^2$, so

$$p(x \mid y_r) \propto \prod_i \exp\Big(-\frac{g_i x_i^2 - 2 b_i x_i}{2\sigma^2}\Big) \mathbb{1}[x_i \in \mathcal{A}] \propto \prod_i \mathcal{N}(x_i; t_i, h_i^2)\, \mathbb{1}[x_i \in \mathcal{A}].$$

So the exact marginal of $x_i$ is the tilted distribution of site $i$, and it does not depend on the sites. Let $(\mu_p, \sigma_p^2)$ be its moments. The variance $\sigma_p^2$ is at most $E[x_i^2] \le \max_a a^2 < h_i^2$, so $\Lambda' = 1/\sigma_p^2 - 1/h_i^2 > 0$ and every update is kept. The targets $(\gamma', \Lambda')$ are the same at every iteration, so line L7 gives $\Lambda_i^{(t)} - \Lambda' = (1 - \beta)^t (\Lambda_i^{(0)} - \Lambda')$, and the same for $\gamma_i$. Both go to 0 for $\beta \in (0, 1]$, and they are 0 after one step when $\beta = 1$. With the limit site, the marginal of $q$ is the cavity times the site, which is $\mathcal{N}(\mu_p, \sigma_p^2)$ by Theorem 2. The mean and variance of $q_i$ are continuous in $(\gamma_i, \Lambda_i)$, so they converge to $(\mu_p, \sigma_p^2)$. $\square$

For the complex model, $G$ is diagonal exactly when $H^H H$ is diagonal, since $G = (H^H H)_r$ and the off-diagonal blocks are $\pm \mathrm{Im}(H^H H)$, whose diagonal is 0. The test builds $H = U\, \mathrm{diag}(d)$ with $U$ a rotation, $|d_1| = 0.6$, $|d_2| = 0.5$, 16-QAM and $N_0 = 1$, so $\sigma^2/g_i \ge 0.5/0.36 = 1.39 > 0.9 = \max_a a^2$. It compares the means and variances with a sum over all 256 vectors, within $10^{-6}$.

## What the tests check

- Theorem 2 with BPSK: the tilted mean and variance equal $\tanh(t/h^2)$ and $1 - \tanh^2(t/h^2)$ within $10^{-12}$.
- Theorem 3: the first iterate against the complex linear MMSE solve, within $10^{-9}$.
- Theorem 5: exact posterior means and variances on orthogonal channels, within $10^{-6}$.
- The page example, step by step, within $10^{-4}$, and that further steps do not change $q$ (Theorem 4 in a concrete case).
- Measurements: agreement with brute-force ML on at least 92 of 100 vectors for 4-QAM, $n = m = 4$, 15 dB (seed 2204; 97 in the run), at most $3/5$ of the MMSE symbol errors for $n = m = 8$ at 10 dB (seed 2206; 19 against 38), and the strongly correlated case where EP settles on a non-ML vector.
