---
title: The AMP denoiser is the exact scalar posterior, the Gaussian-prior fixed point is the linear MMSE estimate, and the state evolution describes the large system
proves: [correctness]
status: partial
---

The model is $y = H x + w$ with $H \in \mathbb{C}^{m \times n}$, $x \in \mathcal{S}^n$ with equally likely points, and $w \sim \mathcal{CN}(0, N_0 I)$. Let $\beta = n / m$. The lines L1 to L9 are those of the pseudocode on the page. Theorems 1 to 3 below are proved in full. Theorem 4 is quoted with its source and hypotheses, and Statement 5 is quoted with its status. That is why the status of this file is partial.

## Theorem 1 (the denoiser and the decision)

Let $z = X + V$ with $X$ uniform on $\mathcal{S}$ and $V \sim \mathcal{CN}(0, s^2)$ independent of $X$. Then $P(X = a \mid z) = w_a$ with $w_a \propto \exp(-|z - a|^2 / s^2)$, $E[X \mid z] = F(z, s^2)$, $E[|X - F|^2 \mid z] = G(z, s^2)$, and the decision of line L8 maximizes $P(X = a \mid z)$.

*Proof.* The density of $V$ is $(\pi s^2)^{-1} \exp(-|v|^2 / s^2)$. By Bayes' rule, $P(X = a \mid z) \propto (1/M) (\pi s^2)^{-1} \exp(-|z - a|^2 / s^2)$, and the factors that do not depend on $a$ cancel in the normalization. So the posterior is $(w_a)$. Its mean is $\sum_a w_a a = F$ and its variance is $\sum_a w_a |a - F|^2 = G$. The largest $w_a$ belongs to the $a$ with the smallest $|z - a|$, which is the point that line L8 picks. $\square$

The mean $F$ minimizes $E|X - \hat X|^2$ among all functions $\hat X$ of $z$, which is why AMP uses it as the denoiser.

## Lemma 2 (the Onsager coefficient)

With the Wirtinger derivative $\partial / \partial z$ (treating $z$ and $z^*$ as independent), $\partial F / \partial z = G / s^2$.

*Proof.* Write $w_a = e_a / \sum_b e_b$ with $e_a = \exp(-(z - a)(z^* - a^*) / s^2)$. Then $\partial e_a / \partial z = -(z^* - a^*) e_a / s^2$, so

$$\frac{\partial w_a}{\partial z} = \frac{w_a}{s^2}\Big(-(z^* - a^*) + \sum_b w_b (z^* - b^*)\Big) = \frac{w_a}{s^2}\,(a^* - F^*).$$

Hence $\partial F / \partial z = \sum_a a\, \partial w_a / \partial z = s^{-2} \big(\sum_a w_a |a|^2 - F \sum_a w_a a^*\big) = s^{-2} (\sum_a w_a |a|^2 - |F|^2) = G / s^2$. $\square$

So the factor $\beta \bar g / s^2$ in line L6 is $\beta$ times the average derivative of the denoiser over the $n$ streams. This is the Onsager coefficient of AMP (Donoho, Maleki and Montanari 2009), which is $(1/m) \sum_k \partial F(z_k) / \partial z$.

## Theorem 3 (the Gaussian prior gives the linear MMSE estimate)

Replace the constellation prior by $X \sim \mathcal{CN}(0, E_s)$, so that $F(z, s^2) = c z$ and $G(z, s^2) = c s^2$ with $c = E_s / (E_s + s^2)$. Let $N_0 > 0$. If $(\hat x, r, s^2)$ is a fixed point of lines L4 to L7, then

$$\hat x = (H^H H + (N_0 / E_s) I)^{-1} H^H y,$$

and $s^2$ solves $s^2 = N_0 + \beta E_s s^2 / (E_s + s^2)$.

*Proof.* The variance $G = c s^2$ is the same for every stream, so $\bar g = c s^2$, and line L7 at the fixed point reads $s^2 = N_0 + \beta c s^2$, which is the stated equation. It gives $s^2 (1 - \beta c) = N_0 > 0$, so $1 - \beta c > 0$.

Line L6 at the fixed point reads $r = y - H \hat x + \beta c\, r$, so $r = (y - H \hat x) / (1 - \beta c)$. Lines L4 and L5 at the fixed point read $\hat x = c (\hat x + H^H r)$, so $\hat x (1 - c) / c = H^H r$. Here $(1 - c) / c = s^2 / E_s$. Put in $r$:

$$\frac{s^2 (1 - \beta c)}{E_s}\, \hat x = H^H y - H^H H \hat x.$$

The factor on the left is $N_0 / E_s$. So $(H^H H + (N_0/E_s) I) \hat x = H^H y$, and the matrix is positive definite, which gives the formula. $\square$

The proof uses no property of $H$. So whenever the iteration converges, it converges to the output of the [linear MMSE filter](/mmse-mimo-detector/) before the bias correction. This fixes the scale of $\hat x$: AMP with a Gaussian prior is a way to compute the MMSE estimate without an inverse. The test checks the formula within $10^{-8}$ on five channels with $n = 6$ and $m = 24$.

## Theorem 4 (state evolution, quoted)

Bayati and Montanari (2011, IEEE Trans. IT 57(2)) prove the following for the real model. Let the entries of $H$ be i.i.d. $\mathcal{N}(0, 1/m)$, let $n, m \to \infty$ with $n / m \to \beta$, let the entries of $x$ be i.i.d. from a distribution with finite moments, and let the denoisers $\eta_t$ be Lipschitz and fixed in advance (they may depend on $t$ but not on the data). Then for each fixed $t$, the empirical distribution of $(z^t_k - x_k)_k$ converges to $\mathcal{N}(0, s_t^2)$ in the sense of pseudo-Lipschitz test functions, where

$$s_{t+1}^2 = N_0' + \beta\, E\big|\eta_t(X + s_t Z) - X\big|^2, \qquad s_1^2 = N_0' + \beta\, E|X|^2,$$

$Z \sim \mathcal{N}(0, 1)$ independent of $X$, and $N_0'$ is the noise variance per real dimension.

Jeon, Ghods, Maleki and Studer state the complex form with $Z \sim \mathcal{CN}(0, 1)$ and the posterior mean denoiser $F(\cdot, s_t^2)$ (Theorem 1 and Corollary 2 of arXiv:1811.01917). The posterior mean for a finite constellation at a fixed $s_t^2 > 0$ is Lipschitz, because both of its Wirtinger derivatives, $G / s_t^2$ from Lemma 2 and $s_t^{-2} (\sum_a w_a a^2 - F^2)$ by the same computation, have modulus at most $4 \max_a |a|^2 / s_t^2$. The implementation uses the empirical $\bar g$ in line L7 instead of the deterministic $s_t^2$, as LAMA does; the two agree in the limit, but the theorem as quoted is for the deterministic sequence.

## Statement 5 (individual optimality, quoted with its status)

Jeon et al. compare the fixed point of the state evolution with the decoupled noise variance of the individually optimal detector, which Guo and Verdú (2005) derived by the replica method. If the state evolution has a unique fixed point, the two coincide, and LAMA reaches the individually optimal error rate in the large system limit. The step that identifies the optimal detector's variance uses the replica method, which is not a proof in general. For some settings it has since been proved, so read this statement as a theorem only under the hypotheses of those proofs.

## What the tests check

- Theorem 1: the denoiser against the BPSK closed form $F = \tanh(2 \,\mathrm{Re}\, z / s^2)$, $G = 1 - F^2$, within $10^{-12}$, and against a direct posterior for 16-QAM.
- Theorem 3: the Gaussian-prior fixed point against the linear MMSE solve, within $10^{-8}$, and the equation for $s^2$ within $10^{-9}$.
- Theorem 4, as a measurement: for $n = 32$, $m = 64$, 4-QAM and $N_0 = 0.25$, the measured mean of $|z_k - x_k|^2$ is within 25 percent of the tracked $s^2$ and of the state evolution.
- Suboptimality: agreement with brute-force ML on at least 95 of 100 vectors at 15 dB (seed 2103; 98 in the run), and exact recovery of 30 of 30 noiseless vectors (seed 2102).
